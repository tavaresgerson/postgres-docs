## B.5. Especificações de Fuso Horário POSIX [#](#DATETIME-POSIX-TIMEZONE-SPECS)

O PostgreSQL pode aceitar especificações de fuso horário escritas de acordo com as regras do padrão POSIX para a variável de ambiente `TZ`. As especificações de fuso horário POSIX são inadequadas para lidar com a complexidade do histórico de fuso horário do mundo real, mas, às vezes, há razões para usá-las.

Uma especificação de fuso horário POSIX tem a forma

```
STD offset [ DST [ dstoffset ] [ , rule ] ]
```

(Para melhor legibilidade, mostramos espaços entre os campos, mas os espaços não devem ser usados na prática.) Os campos são:

* *`STD`* é a abreviação da zona a ser usada para o horário padrão.
* *`offset`* é o deslocamento do horário padrão da zona em relação ao UTC.
* *`DST`* é a abreviação da zona a ser usada para o horário de verão. Se este campo e os campos seguintes forem omitidos, a zona usa um deslocamento UTC fixo sem nenhuma regra de horário de verão.
* *`dstoffset`* é o deslocamento de horário de verão em relação ao UTC. Este campo é tipicamente omitido, pois ele é padrão com uma hora a menos que o *`offset`*, que geralmente é a coisa certa.
* *`rule`* define a regra para quando o horário de verão está em vigor, conforme descrito abaixo.

Nessa sintaxe, uma abreviação de zona pode ser uma cadeia de letras, como `EST`, ou uma cadeia arbitrária cercada por chaves angulares, como `<UTC-05>`. Observe que as abreviações de zona fornecidas aqui são usadas apenas para saída e, mesmo assim, apenas em alguns formatos de saída de marcação de tempo. As abreviações de zona reconhecidas na entrada de marcação de tempo são determinadas conforme explicado em [Seção B.4][(datetime-config-files.md "B.4. Date/Time Configuration Files")].

Os campos de deslocamento especificam as horas e, opcionalmente, os minutos e segundos, diferença em relação ao UTC. Eles têm o formato *`hh`*[`:`*`mm`*[`:`*`ss`*]] opcionalmente com um sinal inicial (`+` ou `-`). O sinal positivo é usado para zonas *a oeste* de Greenwich. (Observe que isso é o oposto da convenção de sinalização ISO-8601 usada em outros lugares no PostgreSQL.) *`hh`* pode ter um ou dois dígitos; *`mm`* e *`ss`* (se usado) devem ter dois.

A transição de horário de verão *`rule`* tem o formato

```
dstdate [ / dsttime ] , stddate [ / stdtime ]
```

(Como antes, os espaços não devem ser incluídos na prática.) Os campos *`dstdate`* e *`dsttime`* definem quando o horário de verão começa, enquanto *`stddate`* e *`stdtime`* definem quando o horário padrão começa. (Em alguns casos, especialmente em zonas ao sul do equador, o primeiro pode ser mais tarde no ano do que o segundo.) Os campos de data têm um desses formatos:

*`n`*: Um número inteiro simples denota um dia do ano, contando de zero a 364, ou até 365 em anos bissextos.

`J`*`n`*: Nesta ficha, *`n`* conta de 1 a 365, e o dia 29 de fevereiro não é contado, mesmo que esteja presente. (Assim, uma transição que ocorre em 29 de fevereiro não pode ser especificada dessa forma. No entanto, os dias após fevereiro têm os mesmos números, seja um ano bissexto ou não, de modo que esta ficha é geralmente mais útil do que a forma de número inteiro simples para transições em datas fixas.)

`M`*`m`*`.`*`n`*`.`*`d`*: Este formulário especifica uma transição que sempre acontece no mesmo mês e no mesmo dia da semana. *`m`* identifica o mês, de 1 a 12. *`n`* especifica a *`n`'ª ocorrência do dia da semana identificada por *`d`*. *`n`* é um número entre 1 e 4, ou 5, o que significa a última ocorrência desse dia da semana no mês (que poderia ser o quarto ou o quinto). *`d`* é um número entre 0 e 6, com 0 indicando domingo. Por exemplo, `M3.2.0` significa “o segundo domingo de março”.

### Nota

O formato `M` é suficiente para descrever muitas leis comuns de transição de horário de verão. Mas observe que nenhuma dessas variantes pode lidar com mudanças na lei de horário de verão, portanto, na prática, os dados históricos armazenados para fusos horários nominais (no banco de dados de fusos horários da IANA) são necessários para interpretar corretamente os marcadores de tempo do passado.

Os campos de tempo em uma regra de transição têm o mesmo formato que os campos de deslocamento descritos anteriormente, exceto que eles não podem conter sinais. Eles definem a hora local atual em que a mudança para o outro tempo ocorre. Se omitidos, eles têm como padrão `02:00:00`.

Se uma abreviação para a mudança de horário de verão for dada, mas o campo *`rule`* de transição for omitido, o comportamento de fallback é usar a regra `M3.2.0,M11.1.0`, que corresponde à prática dos EUA a partir de 2020 (ou seja, avançar no segundo domingo de março, recuar no primeiro domingo de novembro, ambas as transições ocorrendo às 2h do horário predominante). Note que essa regra não fornece datas corretas de transição dos EUA para anos anteriores a 2007.

Como exemplo, `CET-1CEST,M3.5.0,M10.5.0/3` descreve a prática atual (de 2020) de medição do tempo em Paris. Esta especificação diz que o horário padrão tem a abreviação `CET` e está uma hora à frente (leste) do UTC; o horário de verão tem a abreviação `CEST` e implicitamente está duas horas à frente do UTC; o horário de verão começa na última domingo de março às 2h CET e termina na última domingo de outubro às 3h CEST.

Os quatro nomes de fuso horário `EST5EDT`, `CST6CDT`, `MST7MDT` e `PST8PDT` parecem ser especificações de fuso horário POSIX. No entanto, na verdade, são tratados como fusos horários com nomes porque (por razões históricas) existem arquivos com esses nomes no banco de dados de fuso horário da IANA. A implicação prática disso é que esses nomes de fuso horário produzirão transições históricas válidas de horário de verão dos EUA, mesmo quando uma simples especificação POSIX não o faria.

É preciso ter cuidado, pois é fácil escrever mal um horário especificado no estilo POSIX, pois não há verificação da razoabilidade da(s) abreviação(ões) da zona. Por exemplo, `SET TIMEZONE TO FOOBAR0` funcionará, deixando o sistema efetivamente usando uma abreviação bastante peculiar para UTC.