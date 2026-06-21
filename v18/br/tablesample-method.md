## Capítulo 59. Escrever um método de amostragem de tabela

**Índice**

* [59.1. Funções de suporte ao método de amostragem](tablesample-support-functions.md)

A implementação do PostgreSQL da cláusula `TABLESAMPLE` suporta métodos personalizados de amostragem de tabelas, além dos métodos `BERNOULLI` e `SYSTEM` que são exigidos pelo padrão SQL. O método de amostragem determina quais linhas da tabela serão selecionadas quando a cláusula `TABLESAMPLE` for usada.

No nível SQL, um método de amostragem de tabela é representado por uma única função SQL, tipicamente implementada em C, com a assinatura

```
method_name(internal) RETURNS tsm_handler
```

O nome da função é o mesmo nome do método que aparece na cláusula `TABLESAMPLE`. O argumento `internal` é um dummy (sempre com valor zero) que simplesmente serve para impedir que essa função seja chamada diretamente a partir de um comando SQL. O resultado da função deve ser uma estrutura palloc'ada do tipo `TsmRoutine`, que contém ponteiros para funções de suporte ao método de amostragem. Essas funções de suporte são funções em C simples e não são visíveis ou acessíveis no nível SQL. As funções de suporte são descritas em [Seção 59.1][(tablesample-support-functions.md "59.1. Sampling Method Support Functions")].

Além dos ponteiros de função, a estrutura `TsmRoutine` deve fornecer esses campos adicionais:

`List *parameterTypes`: Esta é uma lista de OID que contém os tipos de dados OID dos parâmetros que serão aceitos pela cláusula `TABLESAMPLE` quando este método de amostragem for utilizado. Por exemplo, para os métodos embutidos, esta lista contém um único item com o valor `FLOAT4OID`, que representa a porcentagem de amostragem. Métodos de amostragem personalizados podem ter mais ou diferentes parâmetros.

`bool repeatable_across_queries`: Se `true`, o método de amostragem pode fornecer amostras idênticas em consultas sucessivas, se os mesmos parâmetros e o valor da semente `REPEATABLE` forem fornecidos a cada vez e o conteúdo da tabela não tiver sido alterado. Quando isso ocorre `false`, a cláusula `REPEATABLE` não é aceita para uso com o método de amostragem.

`bool repeatable_across_scans`: Se `true`, o método de amostragem pode fornecer amostras idênticas em varreduras sucessivas na mesma consulta (assumindo que os parâmetros, o valor inicial e o instantâneo permaneçam inalterados). Quando isso é `false`, o planejador não selecionará planos que exijam a varredura da tabela amostrada mais de uma vez, pois isso pode resultar em saída inconsistente da consulta.

O tipo de estrutura `TsmRoutine` é declarado em `src/include/access/tsmapi.h`, que pode ser consultado para obter detalhes adicionais.

Os métodos de amostragem de tabela incluídos na distribuição padrão são boas referências ao tentar escrever a sua própria. Consulte o subdiretório `src/backend/access/tablesample` da árvore de origem para os métodos de amostragem embutidos, e o subdiretório `contrib` para métodos adicionais.