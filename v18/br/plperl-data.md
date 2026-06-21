## 43.2. Valores de dados em PL/Perl [#](#PLPERL-DATA)

Os valores de argumento fornecidos ao código de uma função PL/Perl são simplesmente os argumentos de entrada convertidos para formato de texto (assim como se tivessem sido exibidos por uma declaração `SELECT`). Por outro lado, os comandos `return` e `return_next` aceitarão qualquer string que seja um formato de entrada aceitável para o tipo de retorno declarado da função.

Se esse comportamento for inconveniente para um caso específico, ele pode ser melhorado usando uma transformação, como já ilustrado para os valores de `bool`. Vários exemplos de módulos de transformação estão incluídos na distribuição do PostgreSQL.