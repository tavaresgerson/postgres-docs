## 43.8. PL/Perl sob o capô [#](#PLPERL-UNDER-THE-HOOD)

* [43.8.1. Configuração](plperl-under-the-hood.md#PLPERL-CONFIG)
* [43.8.2. Limitações e Recursos Ausentes](plperl-under-the-hood.md#PLPERL-MISSING)

### 43.8.1. Configuração [#](#PLPERL-CONFIG)

Esta seção lista os parâmetros de configuração que afetam o PL/Perl.

`plperl.on_init` (`string`) [#](#GUC-PLPERL-ON-INIT): Especifica o código Perl a ser executado quando um interpretador Perl é inicializado pela primeira vez, antes de ser especializado para uso por `plperl` ou `plperlu`. As funções SPI não estão disponíveis quando esse código é executado. Se o código falhar com um erro, ele abortará a inicialização do interpretador e propagará para a consulta solicitante, causando o cancelamento da transação ou subtransação atual.

O código Perl é limitado a uma única string. Código mais longo pode ser colocado em um módulo e carregado pela string `on_init`. Exemplos:

```
plperl.on_init = 'require "plperlinit.pl"' plperl.on_init = 'use lib "/my/app"; use MyApp::PgInit;'
```

Qualquer módulo carregado por `plperl.on_init`, diretamente ou indiretamente, estará disponível para uso por `plperl`. Isso pode criar um risco de segurança. Para ver quais módulos foram carregados, você pode usar:

```
DO 'elog(WARNING, join ", ", sort keys %INC)' LANGUAGE plperl;
```

A inicialização ocorrerá no postmaster se a biblioteca `plperl` for incluída em [shared_preload_libraries](runtime-config-client.md#GUC-SHARED-PRELOAD-LIBRARIES), no caso, deve-se dar atenção extra ao risco de desestabilizar o postmaster. A principal razão para o uso desta funcionalidade é que os módulos Perl carregados por `plperl.on_init` precisam ser carregados apenas no início do postmaster e estarão instantaneamente disponíveis sem sobrecarga de carregamento em sessões individuais do banco de dados. No entanto, tenha em mente que a sobrecarga é evitada apenas para o primeiro interpretador Perl usado por uma sessão do banco de dados — seja PL/PerlU ou PL/Perl para o primeiro papel SQL que chama uma função PL/Perl. Qualquer interpretador Perl adicional criado em uma sessão do banco de dados terá que executar `plperl.on_init` novamente. Além disso, no Windows, não haverá economia alguma na pré-carga, uma vez que o interpretador Perl criado no processo do postmaster não se propaga para processos filhos.

Este parâmetro só pode ser definido no arquivo `postgresql.conf` ou na linha de comando do servidor.

`plperl.on_plperl_init` (`string`) `plperl.on_plperlu_init` (`string`) [#](#GUC-PLPERL-ON-PLPERL-INIT): Esses parâmetros especificam o código Perl a ser executado quando um interpretador Perl é especializado para `plperl` ou `plperlu`, respectivamente. Isso ocorrerá quando uma função PL/Perl ou PL/PerlU é executada pela primeira vez em uma sessão de banco de dados, ou quando um interpretador adicional deve ser criado porque o outro idioma é chamado ou uma função PL/Perl é chamada por um novo papel SQL. Isso segue qualquer inicialização feita por `plperl.on_init`. As funções SPI não estão disponíveis quando esse código é executado. O código Perl em `plperl.on_plperl_init` é executado após “desbloquear” o interpretador, e, portanto, só pode realizar operações confiáveis.

Se o código falhar com um erro, ele abortará a inicialização e propagará para a consulta que o solicitou, fazendo com que a transação ou subtransação atual seja abortada. Qualquer ação já realizada dentro do Perl não será desfeita; no entanto, esse interpretador não será usado novamente. Se a linguagem for usada novamente, a inicialização será realizada novamente dentro de um interpretador Perl novo.

Somente os superusuários podem alterar essas configurações. Embora essas configurações possam ser alteradas dentro de uma sessão, tais alterações não afetarão os interpretadores Perl que já foram usados para executar funções.

`plperl.use_strict` (`boolean`) [#](#GUC-PLPERL-USE-STRICT): Quando definido como verdadeiro, as compilações subsequentes das funções PL/Perl terão o pragmatismo `strict` habilitado. Este parâmetro não afeta as funções já compiladas na sessão atual.

### 43.8.2. Limitações e recursos ausentes [#](#PLPERL-MISSING)

As seguintes funcionalidades atualmente estão ausentes no PL/Perl, mas elas contribuiriam de forma bem-vinda.

* As funções PL/Perl não podem ser chamadas diretamente uma pela outra.
* O SPI ainda não está totalmente implementado.
* Se você está obtendo conjuntos de dados muito grandes usando `spi_exec_query`, você deve estar ciente de que todos eles irão para a memória. Você pode evitar isso usando `spi_query`/`spi_fetchrow` como ilustrado anteriormente.

Um problema semelhante ocorre se uma função que retorna um conjunto passar um grande conjunto de linhas de volta ao PostgreSQL através de `return`. Você também pode evitar esse problema usando `return_next` para cada linha retornada, como mostrado anteriormente.
* Quando uma sessão termina normalmente, não devido a um erro fatal, quaisquer blocos `END` que tenham sido definidos são executados. Atualmente, não são realizadas outras ações. Especificamente, os identificadores de arquivo não são limpos automaticamente e os objetos não são destruídos automaticamente.