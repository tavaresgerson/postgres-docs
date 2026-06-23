## 11.4. Índices e `ORDER BY` [#](#INDEXES-ORDERING)

Além de simplesmente encontrar as linhas que devem ser devolvidas por uma consulta, um índice pode ser capaz de entregá-las em uma ordem específica e ordenada. Isso permite que a especificação `ORDER BY` de uma consulta seja respeitada sem uma etapa de ordenação separada. Dos tipos de índice atualmente suportados pelo PostgreSQL, apenas o B-tree pode produzir saída ordenada — os outros tipos de índice retornam linhas correspondentes em uma ordem não especificada, dependente da implementação.

O planejador considerará satisfazer uma especificação de `ORDER BY` ou escaneando um índice disponível que corresponda à especificação, ou escaneando a tabela em ordem física e fazendo uma classificação explícita. Para uma consulta que requer a varredura de uma grande fração da tabela, uma classificação explícita provavelmente será mais rápida do que usar um índice, pois requer menos I/O de disco devido ao seguimento de um padrão de acesso sequencial. Os índices são mais úteis quando apenas algumas linhas precisam ser obtidas. Um caso especial importante é `ORDER BY` em combinação com `LIMIT` *`n`*: uma classificação explícita terá que processar todos os dados para identificar as primeiras linhas de *`n`*, mas se houver um índice que corresponda ao `ORDER BY`, as primeiras linhas de *`n`* podem ser recuperadas diretamente, sem varredura do restante.

Por padrão, os índices de árvore B armazenam suas entradas em ordem crescente com os nulos como último (a tabela TID é tratada como uma coluna de resolução de empate entre entradas que são igualmente iguais). Isso significa que uma varredura para a frente de um índice na coluna `x` produz saída que satisfaz `ORDER BY x` (ou, mais verbosemente, `ORDER BY x ASC NULLS LAST`). O índice também pode ser percorrido para trás, produzindo saída que satisfaz `ORDER BY x DESC` (ou, mais verbosemente, `ORDER BY x DESC NULLS FIRST`, uma vez que `NULLS FIRST` é o padrão para `ORDER BY DESC`).

Você pode ajustar a ordem de um índice de árvore B, incluindo as opções `ASC`, `DESC`, `NULLS FIRST` e/ou `NULLS LAST` ao criar o índice; por exemplo:

```
CREATE INDEX test2_info_nulls_low ON test2 (info NULLS FIRST);
CREATE INDEX test3_desc_index ON test3 (id DESC NULLS LAST);
```

Um índice armazenado em ordem crescente com os nulos primeiro pode satisfazer `ORDER BY x ASC NULLS FIRST` ou `ORDER BY x DESC NULLS LAST`, dependendo da direção em que é scaneado.

Você pode se perguntar por que se preocupar em fornecer todas as quatro opções, quando duas opções juntamente com a possibilidade de varredura reversa cobririam todas as variantes do `ORDER BY`. Em índices de uma coluna, as opções são, de fato, redundantes, mas em índices multicoluna elas podem ser úteis. Considere um índice de duas colunas em `(x, y)`: isso pode satisfazer `ORDER BY x, y` se fizermos uma varredura para frente, ou `ORDER BY x DESC, y DESC` se fizermos uma varredura para trás. Mas pode ser que o aplicativo precise frequentemente usar `ORDER BY x ASC, y DESC`. Não há como obter essa ordenação de um índice simples, mas é possível se o índice for definido como `(x ASC, y DESC)` ou `(x DESC, y ASC)`.

Obviamente, índices com ordenamentos de classificação não padrão são uma característica bastante especializada, mas, às vezes, podem produzir grandes melhorias em determinadas consultas. Se vale a pena manter tal índice depende de quantas vezes você usa consultas que exigem um ordenamento de classificação especial.