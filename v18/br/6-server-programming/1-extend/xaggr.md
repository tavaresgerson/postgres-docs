## 36.12. Agregados definidos pelo usuário [#](#XAGGR)

* [36.12.1. Modo de Agregação de Movimento](xaggr.md#XAGGR-MOVING-AGGREGATES)
* [36.12.2. Agregados Polimorfos e Variadicos](xaggr.md#XAGGR-POLYMORPHIC-AGGREGATES)
* [36.12.3. Agregados de Conjunto Ordenado](xaggr.md#XAGGR-ORDERED-SET-AGGREGATES)
* [36.12.4. Agregação Parcial](xaggr.md#XAGGR-PARTIAL-AGGREGATES)
* [36.12.5. Funções de Suporte para Agregados](xaggr.md#XAGGR-SUPPORT-FUNCTIONS)

As funções agregadas no PostgreSQL são definidas em termos de *valores de estado* e *funções de transição de estado*. Isso significa que uma função agregada opera usando um valor de estado que é atualizado à medida que cada linha de entrada sucessiva é processada. Para definir uma nova função agregada, seleciona-se um tipo de dados para o valor de estado, um valor inicial para o estado e uma função de transição de estado. A função de transição de estado recebe o valor de estado anterior e o(s) valor(es) de entrada(s) do agregado para a linha atual e retorna um novo valor de estado. Uma *função final* também pode ser especificada, no caso de o resultado desejado do agregado ser diferente dos dados que precisam ser mantidos no valor de estado em execução. A função final recebe o valor de estado final e retorna o que for desejado como o resultado do agregado. Em princípio, as funções de transição e final são apenas funções comuns que também poderiam ser usadas fora do contexto do agregado. (Na prática, muitas vezes é útil, por razões de desempenho, criar funções de transição especializadas que só podem funcionar quando chamadas como parte de um agregado.)

Assim, além dos tipos de dados de argumento e resultado vistos por um usuário do agregado, há um tipo de dados de valor de estado interno que pode ser diferente tanto dos tipos de argumento quanto do resultado.

Se definirmos um agregado que não use uma função final, teremos um agregado que calcula uma função em execução dos valores da coluna de cada linha. `sum` é um exemplo desse tipo de agregado. `sum` começa em zero e sempre adiciona o valor da linha atual ao seu total em execução. Por exemplo, se quisermos fazer um agregado `sum` funcionar em um tipo de dados para números complexos, só precisamos da função de adição para esse tipo de dados. A definição do agregado seria:

```
CREATE AGGREGATE sum (complex)
(
    sfunc = complex_add,
    stype = complex,
    initcond = '(0,0)'
);
```

que podemos usar assim:

```
SELECT sum(a) FROM test_complex;

   sum
-----------
 (34,53.9)
```

(Observe que estamos confiando na sobrecarga de função: há mais de um agregado com o nome `sum`, mas o PostgreSQL pode descobrir qual tipo de soma se aplica a uma coluna do tipo `complex`.)

A definição acima de `sum` retornará zero (o valor inicial do estado) se não houver valores de entrada não nulos. Talvez queiramos retornar nulo nesse caso, em vez disso — o padrão SQL espera que `sum` se comporte dessa maneira. Podemos fazer isso simplesmente omitindo a frase `initcond`, para que o valor inicial do estado seja nulo. Normalmente, isso significaria que o `sfunc` precisaria verificar uma entrada de valor de estado nulo. Mas para `sum` e alguns outros agregados simples como `max` e `min`, é suficiente inserir o primeiro valor de entrada não nulo na variável de estado e, em seguida, começar a aplicar a função de transição no segundo valor de entrada não nulo. O PostgreSQL fará isso automaticamente se o valor inicial do estado for nulo e a função de transição for marcada como “estricta” (ou seja, não ser chamada para entradas nulos).

Outro comportamento padrão para uma função de transição "estricta" é que o valor do estado anterior é mantido inalterado sempre que um valor de entrada nulo é encontrado. Assim, os valores nulos são ignorados. Se você precisar de outro comportamento para entradas nulos, não declare sua função de transição como estrita; em vez disso, codifique-a para testar entradas nulos e faça o que for necessário.

`avg` (média) é um exemplo mais complexo de um agregado. Ele requer duas partes do estado em execução: a soma dos inputs e a contagem do número de inputs. O resultado final é obtido dividindo essas quantidades. A média é tipicamente implementada usando uma matriz como o valor do estado. Por exemplo, a implementação embutida de `avg(float8)` parece assim:

```
CREATE AGGREGATE avg (float8)
(
    sfunc = float8_accum,
    stype = float8[],
    finalfunc = float8_avg,
    initcond = '{0,0,0}'
);
```

### Nota

`float8_accum` exige um array de três elementos, não apenas dois elementos, porque acumula a soma dos quadrados, bem como a soma e o número de entradas. Isso é para que ele possa ser usado para alguns outros agregados, assim como `avg`.

As chamadas de função agregada no SQL permitem as opções `DISTINCT` e `ORDER BY` que controlam quais linhas são fornecidas à função de transição do agregado e em que ordem. Essas opções são implementadas nos bastidores e não são a preocupação das funções de suporte do agregado.

Para mais detalhes, consulte o comando [CREATE AGGREGATE](sql-createaggregate.md "CREATE AGGREGATE").

### 36.12.1. Modo de Movimento de Agregados [#](#XAGGR-MOVING-AGGREGATES)

As funções agregadas podem, opcionalmente, suportar o modo *agregado em movimento*, que permite uma execução substancialmente mais rápida das funções agregadas dentro de janelas com pontos de início de quadro em movimento. (Consulte [Seção 3.5](tutorial-window.md) e [Seção 4.2.8](sql-expressions.md#SYNTAX-WINDOW-FUNCTIONS) para informações sobre o uso de funções agregadas como funções de janela. A ideia básica é que, além de uma função de transição "avançada" normal, o agregado fornece uma *função de transição inversa*, que permite que as linhas sejam removidas do valor do estado de execução do agregado quando elas saem do quadro da janela. Por exemplo, um agregado `sum` que usa adição como função de transição avançada, usaria subtração como função de transição inversa. Sem uma função de transição inversa, o mecanismo da função de janela deve recalcular o agregado do zero a cada vez que o ponto de início do quadro se move, resultando em um tempo de execução proporcional ao número de linhas de entrada vezes a duração média do quadro. Com uma função de transição inversa, o tempo de execução é apenas proporcional ao número de linhas de entrada.

A função de transição inversa recebe o valor do estado atual e o(s) valor(es) de entrada agregado(s) para a primeira linha incluída no estado atual. Ela deve reconstruir o que o valor do estado teria sido se a linha de entrada dada nunca tivesse sido agregada, mas apenas as linhas que a seguem. Isso, por vezes, exige que a função de transição para frente mantenha mais estado do que o necessário para o modo de agregação simples. Portanto, o modo de agregação móvel usa uma implementação completamente separada do modo simples: tem seu próprio tipo de dados de estado, sua própria função de transição para frente e sua própria função final, se necessário. Estes podem ser o mesmo que o tipo de dados e funções do modo simples, se não houver necessidade de estado adicional.

Como exemplo, poderíamos estender o agregado `sum` dado acima para suportar o modo de agregação em movimento, da seguinte forma:

```
CREATE AGGREGATE sum (complex)
(
    sfunc = complex_add,
    stype = complex,
    initcond = '(0,0)',
    msfunc = complex_add,
    minvfunc = complex_sub,
    mstype = complex,
    minitcond = '(0,0)'
);
```

Os parâmetros cujos nomes começam com `m` definem a implementação de agregação móvel. Exceto pela função de transição inversa `minvfunc`, eles correspondem aos parâmetros de agregação simples sem `m`.

A função de transição para a frente para o modo de agregados móveis não é permitida para retornar nulo como o novo valor do estado. Se a função de transição inversa retornar nulo, isso é considerado uma indicação de que a função inversa não pode reverter o cálculo do estado para este determinado valor de entrada, e assim o cálculo do agregado será feito novamente do zero para a posição inicial do quadro atual. Esta convenção permite que o modo de agregados móveis seja usado em situações onde existem alguns casos infrequentes que são impraticáveis para ser revertidos a partir do valor do estado em execução. A função de transição inversa pode "pular" nesses casos, e ainda assim sair na frente, desde que possa funcionar na maioria dos casos. Como exemplo, um agregado que trabalha com números em ponto flutuante pode optar por pular quando um `NaN` (não um número) deve ser removido do valor do estado em execução.

Ao escrever funções de suporte para agregados móveis, é importante garantir que a função de transição inversa possa reconstruir o valor do estado exatamente. Caso contrário, pode haver diferenças visíveis pelo usuário nos resultados, dependendo se o modo de agregado móvel é usado. Um exemplo de agregado para o qual adicionar uma função de transição inversa parece fácil de início, mas onde essa exigência não pode ser atendida é `sum` sobre `float4` ou `float8` entradas. Uma declaração ingênua de `sum(float8)` poderia ser

```
CREATE AGGREGATE unsafe_sum (float8)
(
    stype = float8,
    sfunc = float8pl,
    mstype = float8,
    msfunc = float8pl,
    minvfunc = float8mi
);
```

Esse agregado, no entanto, pode gerar resultados completamente diferentes do que teria sem a função de transição inversa. Por exemplo, considere

```
SELECT
  unsafe_sum(x) OVER (ORDER BY n ROWS BETWEEN CURRENT ROW AND 1 FOLLOWING)
FROM (VALUES (1, 1.0e20::float8),
             (2, 1.0::float8)) AS v (n,x);
```

Essa consulta retorna `0` como seu segundo resultado, em vez da resposta esperada de `1`. A causa é a precisão limitada dos valores de ponto flutuante: adicionar `1` a `1e20` resulta em `1e20` novamente, e assim, subtrair `1e20` desse resulta em `0`, não `1`. Note que essa é uma limitação da aritmética de ponto flutuante em geral, não uma limitação do PostgreSQL.

### 36.12.2. Aglomerados polimórficos e variadicos [#](#XAGGR-POLYMORPHIC-AGGREGATES)

As funções agregadas podem usar funções de transição de estado polimórficas ou funções finais, de modo que as mesmas funções possam ser usadas para implementar múltiplos agregados. Consulte [Seção 36.2.5] para uma explicação sobre funções polimórficas. Avançando um passo adiante, a própria função agregada pode ser especificada com tipos de entrada polimórficos e tipo de estado, permitindo que uma única definição de agregação sirva para múltiplos tipos de dados de entrada. Aqui está um exemplo de uma agregação polimórfica:

```
CREATE AGGREGATE array_accum (anycompatible)
(
    sfunc = array_append,
    stype = anycompatiblearray,
    initcond = '{}'
);
```

Aqui, o tipo de estado real para qualquer chamada agregada dada é o tipo de matriz que tem o tipo de entrada real como elementos. O comportamento do agregado é concatenar todas as entradas em uma matriz desse tipo. (Nota: o agregado interno `array_agg` fornece uma funcionalidade semelhante, com melhor desempenho do que esta definição teria.)

Aqui está a saída usando dois tipos de dados reais diferentes como argumentos:

```
SELECT attrelid::regclass, array_accum(attname)
    FROM pg_attribute
    WHERE attnum > 0 AND attrelid = 'pg_tablespace'::regclass
    GROUP BY attrelid;

   attrelid    |              array_accum
---------------+---------------------------------------
 pg_tablespace | {spcname,spcowner,spcacl,spcoptions}
(1 row)

SELECT attrelid::regclass, array_accum(atttypid::regtype)
    FROM pg_attribute
    WHERE attnum > 0 AND attrelid = 'pg_tablespace'::regclass
    GROUP BY attrelid;

   attrelid    |        array_accum
---------------+---------------------------
 pg_tablespace | {name,oid,aclitem[],text[]}
(1 row)
```

Normalmente, uma função agregada com um tipo de resultado polimórfico tem um tipo de estado polimórfico, como no exemplo acima. Isso é necessário, pois, caso contrário, a função final não pode ser declarada de forma sensível: ela precisaria ter um tipo de resultado polimórfico, mas nenhum tipo de argumento polimórfico, o que `CREATE FUNCTION` rejeitaria com base no fato de que o tipo de resultado não pode ser deduzido de uma chamada. Mas, às vezes, é inconveniente usar um tipo de estado polimórfico. O caso mais comum é quando as funções de suporte agregado devem ser escritas em C e o tipo de estado deve ser declarado como `internal`, porque não há um equivalente em nível SQL para isso. Para abordar esse caso, é possível declarar a função final como que tomando argumentos "falsos" extras que correspondem aos argumentos de entrada da agregação. Esses argumentos falsos são sempre passados como valores nulos, uma vez que não há um valor específico disponível quando a função final é chamada. Sua única utilidade é permitir que o tipo de resultado de uma função final polimórfica seja conectado ao(s) tipo(s) de entrada da agregação. Por exemplo, a definição do agregado embutido `array_agg` é equivalente a

```
CREATE FUNCTION array_agg_transfn(internal, anynonarray)
  RETURNS internal ...;
CREATE FUNCTION array_agg_finalfn(internal, anynonarray)
  RETURNS anyarray ...;

CREATE AGGREGATE array_agg (anynonarray)
(
    sfunc = array_agg_transfn,
    stype = internal,
    finalfunc = array_agg_finalfn,
    finalfunc_extra
);
```

Aqui, a opção `finalfunc_extra` especifica que a função final recebe, além do valor do estado, argumentos fictícios adicionais correspondentes ao(s) argumento(s) de entrada do agregado. O argumento adicional `anynonarray` permite que a declaração de `array_agg_finalfn` seja válida.

Uma função agregada pode ser feita para aceitar um número variável de argumentos, declarando seu último argumento como um array `VARIADIC`, de maneira muito semelhante à de funções regulares; veja [Seção 36.5.6](xfunc-sql.md#XFUNC-SQL-VARIADIC-FUNCTIONS). A(s) função(ões) de transição da agregação deve ter o mesmo tipo de array que seu(s) último(s) argumento(s). A(s) função(ões) de transição normalmente também seria marcada `VARIADIC`, mas isso não é estritamente necessário.

### Nota

Os agregados variadic são facilmente mal utilizados em conexão com a opção `ORDER BY` (consulte [Seção 4.2.7](sql-expressions.md#SYNTAX-AGGREGATES)), pois o analisador não pode determinar se o número errado de argumentos reais foi dado em tal combinação. Tenha em mente que tudo à direita de `ORDER BY` é uma chave de classificação, não um argumento para o agregado. Por exemplo, em

```
SELECT myaggregate(a ORDER BY a, b, c) FROM ...
```

O analisador verá isso como um argumento de função agregada única e três chaves de ordenação. No entanto, o usuário pode ter intencionado

```
SELECT myaggregate(a, b, c ORDER BY a) FROM ...
```

Se `myaggregate` for variável, ambas as chamadas poderiam ser perfeitamente válidas.

Por essa mesma razão, é prudente pensar duas vezes antes de criar funções agregadas com os mesmos nomes e diferentes números de argumentos regulares.

### 36.12.3. Agregados de Conjunto Ordenado [#](#XAGGR-ORDERED-SET-AGGREGATES)

Os agregados que descrevemos até agora são agregados "normais". O PostgreSQL também suporta agregados *de conjunto ordenado*, que diferem dos agregados normais em dois aspectos-chave. Primeiro, além dos argumentos agregados comuns que são avaliados uma vez por linha de entrada, um agregado de conjunto ordenado pode ter argumentos "diretos" que são avaliados apenas uma vez por operação de agregação. Segundo, a sintaxe dos argumentos agregados normais especifica explicitamente uma ordem de classificação para eles. Um agregado de conjunto ordenado é geralmente usado para implementar uma computação que depende de uma ordem específica de linha, por exemplo, classificação ou percentil, de modo que a ordem de classificação é um aspecto necessário de qualquer chamada. Por exemplo, a definição embutida de `percentile_disc` é equivalente a:

```
CREATE FUNCTION ordered_set_transition(internal, anyelement)
  RETURNS internal ...;
CREATE FUNCTION percentile_disc_final(internal, float8, anyelement)
  RETURNS anyelement ...;

CREATE AGGREGATE percentile_disc (float8 ORDER BY anyelement)
(
    sfunc = ordered_set_transition,
    stype = internal,
    finalfunc = percentile_disc_final,
    finalfunc_extra
);
```

Este agregado recebe um argumento direto `float8` (a fração percentual) e uma entrada agregada que pode ser de qualquer tipo de dados ordenável. Ele pode ser usado para obter um rendimento médio familiar da seguinte forma:

```
SELECT percentile_disc(0.5) WITHIN GROUP (ORDER BY income) FROM households;
 percentile_disc
-----------------
           50489
```

Aqui, `0.5` é um argumento direto; não faria sentido que a fração percentual fosse um valor variável em linhas.

Ao contrário do que ocorre com os agregados normais, a classificação das linhas de entrada para um agregado de conjunto ordenado *não* é feita nos bastidores, mas é responsabilidade das funções de suporte do agregado. A abordagem típica de implementação é manter uma referência a um objeto "tuplesort" no valor do estado do agregado, alimentar as linhas de entrada nesse objeto e, em seguida, completar a classificação e ler os dados na função final. Esse design permite que a função final realize operações especiais, como injetar linhas "hipotéticas" adicionais nos dados a serem classificados. Embora os agregados normais possam muitas vezes ser implementados com funções de suporte escritas em PL/pgSQL ou outro idioma PL, os agregados de conjunto ordenado geralmente precisam ser escritos em C, uma vez que seus valores de estado não podem ser definidos como qualquer tipo de dados SQL. (No exemplo acima, observe que o valor do estado é declarado como tipo `internal` — isso é típico). Além disso, como a função final realiza a classificação, não é possível continuar adicionando linhas de entrada executando a função de transição novamente mais tarde. Isso significa que a função final não é `READ_ONLY`; ela deve ser declarada em `CREATE AGGREGATE`(sql-createaggregate.md "CREATE AGGREGATE") como `READ_WRITE`, ou como `SHAREABLE` se for possível que chamadas adicionais à função final utilizem o estado já classificado.

A função de transição de estado para um agregado de conjunto ordenado recebe o valor atual do estado mais os valores de entrada agregados para cada linha e retorna o valor atualizado do estado. Esta é a mesma definição que para agregados normais, mas observe que os argumentos diretos (se houver) não são fornecidos. A função final recebe o último valor do estado, os valores dos argumentos diretos (se houver) e (se `finalfunc_extra` for especificado) valores nulos correspondentes aos(s) entrada(s) agregados. Como em agregados normais, `finalfunc_extra` é útil apenas se o agregado for polimórfico; então os argumentos de índice adicionais são necessários para conectar o tipo de resultado da função final ao(s) tipo(s) de entrada(s) do agregado.

Atualmente, os agregados de conjunto ordenado não podem ser usados como funções de janela, e, portanto, não há necessidade de que eles suportem o modo de agregado móvel.

### 36.12.4. Aglomeração Parcial [#](#XAGGR-PARTIAL-AGGREGATES)

Opcionalmente, uma função agregada pode suportar *agregada parcial*. A ideia da agregação parcial é executar a função de transição de estado do agregador sobre diferentes subconjuntos dos dados de entrada de forma independente, e então combinar os valores de estado resultantes desses subconjuntos para produzir o mesmo valor de estado que teria resultado da digitalização de todos os dados em uma única operação. Esse modo pode ser usado para agregação paralela, com diferentes processos de trabalho analisando diferentes partes de uma tabela. Cada processo produz um valor parcial de estado, e, no final, esses valores de estado são combinados para produzir um valor de estado final. (No futuro, esse modo também pode ser usado para propósitos como a combinação de agregados sobre tabelas locais e remotas; mas isso ainda não é implementado.)

Para suportar a agregação parcial, a definição do agregado deve fornecer uma *função de combinação*, que recebe dois valores do tipo de estado do agregado (representando os resultados da agregação sobre dois subconjuntos das linhas de entrada) e produz um novo valor do tipo de estado, representando o que o estado teria sido após a agregação sobre a combinação desses conjuntos de linhas. Não é especificado qual seria a ordem relativa das linhas de entrada dos dois conjuntos. Isso significa que, geralmente, é impossível definir uma função de combinação útil para agregados que são sensíveis à ordem das linhas de entrada.

Como exemplos simples, os agregados `MAX` e `MIN` podem ser feitos para suportar agregação parcial, especificando a função combinar como a mesma função de comparação maior entre dois ou menor entre dois, que é usada como sua função de transição. Os agregados `SUM` precisam apenas de uma função de adição como função combinar. (Novamente, isso é o mesmo que sua função de transição, a menos que o valor do estado seja mais amplo do que o tipo de dados de entrada.)

A função de agregação é tratada de maneira muito semelhante a uma função de transição que, por acaso, leva um valor do tipo de estado, não do tipo de entrada subjacente, como seu segundo argumento. Em particular, as regras para lidar com valores nulos e funções estritas são semelhantes. Além disso, se a definição de agregação especificar um `initcond` não nulo, tenha em mente que ele será usado não apenas como o estado inicial para cada execução de agregação parcial, mas também como o estado inicial para a função de agregação, que será chamada para combinar cada resultado parcial nesse estado.

Se o tipo de estado do agregado for declarado como `internal`, é responsabilidade da função combinada que seu resultado seja alocado no contexto de memória correto para os valores do estado do agregado. Isso significa, em particular, que quando o primeiro input é `NULL`, não é válido simplesmente retornar o segundo input, pois esse valor estará no contexto errado e não terá vida útil suficiente.

Quando o tipo de estado do agregado é declarado como `internal`, geralmente também é apropriado que a definição do agregado forneça uma *função de serialização* e uma *função de desserialização*, que permitam que um valor de estado desse tipo seja copiado de um processo para outro. Sem essas funções, a agregação paralela não pode ser realizada, e aplicações futuras, como a agregação local/remota, provavelmente também não funcionarão.

Uma função de serialização deve receber um único argumento do tipo `internal` e retornar um resultado do tipo `bytea`, que representa o valor do estado embalado em um bloco plano de bytes. Por outro lado, uma função de deserialização inverte essa conversão. Deve receber dois argumentos dos tipos `bytea` e `internal`, e retornar um resultado do tipo `internal`. (O segundo argumento é inutilizado e sempre zero, mas é necessário por razões de segurança de tipo.) O resultado da função de deserialização deve simplesmente ser alocado no contexto de memória atual, pois, ao contrário do resultado da função combine, não é de longa duração.

Vale ressaltar também que, para que um agregado seja executado em paralelo, o agregado em si deve ser marcado `PARALLEL SAFE`. As marcações de segurança paralela em suas funções de suporte não são consultadas.

### 36.12.5. Funções de suporte para agregados [#](#XAGGR-SUPPORT-FUNCTIONS)

Uma função escrita em C pode detectar que está sendo chamada como uma função de suporte agregada, chamando `AggCheckCallContext`, por exemplo:

```
if (AggCheckCallContext(fcinfo, NULL))
```

Uma razão para verificar isso é que, quando é verdade, o primeiro valor de entrada deve ser um valor de estado temporário e, portanto, pode ser modificado in-place de forma segura, em vez de alocar uma nova cópia. Veja `int8inc()` para um exemplo. (Embora as funções de transição agregada sempre sejam permitidas para modificar o valor de transição in-place, as funções finais agregadas são geralmente desencorajadas a fazer isso; se assim o fizerem, o comportamento deve ser declarado ao criar o agregado. Veja [CREATE AGGREGATE](sql-createaggregate.md "CREATE AGGREGATE") para mais detalhes.)

O segundo argumento de `AggCheckCallContext` pode ser usado para recuperar o contexto de memória no qual os valores do estado agregado estão sendo mantidos. Isso é útil para funções de transição que desejam usar objetos "expandidos" (ver [Seção 36.13.1](xtypes.md#XTYPES-TOAST)) como seus valores de estado. Na primeira chamada, a função de transição deve retornar um objeto expandido cujo contexto de memória é uma subdivisão do contexto do estado agregado, e então continuar retornando o mesmo objeto expandido em chamadas subsequentes. Veja `array_append()` para um exemplo. (`array_append()` não é a função de transição de nenhum agregado embutido, mas é escrita para se comportar de forma eficiente quando usada como função de transição de um agregado personalizado.)

Outra rotina de suporte disponível para funções agregadoras escritas em C é `AggGetAggref`, que retorna o nó de análise `Aggref` que define a chamada agregadora. Isso é principalmente útil para agregadores de conjuntos ordenados, que podem inspecionar a subestrutura do nó `Aggref` para descobrir que tipo de ordenação devem implementar. Exemplos podem ser encontrados em `orderedsetaggs.c` no código-fonte do PostgreSQL.