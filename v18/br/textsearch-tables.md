## 12.2. Tabelas e índices [#](#TEXTSEARCH-TABLES)

* [12.2.1. Procurar uma tabela](textsearch-tables.md#TEXTSEARCH-TABLES-SEARCH)
* [12.2.2. Criar índices](textsearch-tables.md#TEXTSEARCH-TABLES-INDEX)

Os exemplos da seção anterior ilustram a correspondência de texto completo usando strings constantes simples. Esta seção mostra como pesquisar dados de tabela, opcionalmente usando índices.

### 12.2.1. Pesquisar uma tabela [#](#TEXTSEARCH-TABLES-SEARCH)

É possível fazer uma pesquisa de texto completo sem um índice. Uma consulta simples para imprimir o `title` de cada linha que contém a palavra `friend` em seu campo `body` é:

```
SELECT title
FROM pgweb
WHERE to_tsvector('english', body) @@ to_tsquery('english', 'friend');
```

Isso também encontrará palavras relacionadas, como `friends` e `friendly`, uma vez que todas essas são reduzidas ao mesmo lexema normalizado.

A consulta acima especifica que a configuração `english` deve ser usada para analisar e normalizar as strings. Alternativamente, poderíamos omitir os parâmetros de configuração:

```
SELECT title
FROM pgweb
WHERE to_tsvector(body) @@ to_tsquery('friend');
```

Essa consulta utilizará a configuração definida por [default_text_search_config][(runtime-config-client.md#GUC-DEFAULT-TEXT-SEARCH-CONFIG)].

Um exemplo mais complexo é selecionar os dez documentos mais recentes que contenham `create` e `table` no `title` ou `body`:

```
SELECT title
FROM pgweb
WHERE to_tsvector(title || ' ' || body) @@ to_tsquery('create & table')
ORDER BY last_mod_date DESC
LIMIT 10;
```

Para maior clareza, omitimos as chamadas à função `coalesce` que seriam necessárias para encontrar linhas que contenham `NULL` em um dos dois campos.

Embora essas consultas funcionem sem um índice, a maioria das aplicações achará essa abordagem muito lenta, exceto talvez para pesquisas ocasionais ad hoc. O uso prático da pesquisa de texto geralmente exige a criação de um índice.

### 12.2.2. Criando índices [#](#TEXTSEARCH-TABLES-INDEX)

Podemos criar um índice GIN ([Seção 12.9](textsearch-indexes.md "12.9. Preferred Index Types for Text Search")) para acelerar as pesquisas de texto:

```
CREATE INDEX pgweb_idx ON pgweb USING GIN (to_tsvector('english', body));
```

Observe que a versão de 2 argumentos de `to_tsvector` é usada. Apenas funções de busca de texto que especificam um nome de configuração podem ser usadas em índices de expressão ([Seção 11.7](indexes-expressional.md "11.7. Indexes on Expressions")). Isso ocorre porque o conteúdo do índice não deve ser afetado por [default_text_search_config](runtime-config-client.md#GUC-DEFAULT-TEXT-SEARCH-CONFIG). Se fossem afetados, o conteúdo do índice poderia ser inconsistente, pois diferentes entradas poderiam conter `tsvector`s que foram criados com diferentes configurações de busca de texto, e não haveria como descobrir qual era qual. Seria impossível drenar e restaurar tal índice corretamente.

Como a versão de dois argumentos de `to_tsvector` foi usada no índice acima, apenas uma referência de consulta que use a versão de dois argumentos de `to_tsvector` com o mesmo nome de configuração usará esse índice. Isso significa que `WHERE to_tsvector('english', body) @@ 'a & b'` pode usar o índice, mas `WHERE to_tsvector(body) @@ 'a & b'` não pode. Isso garante que um índice será usado apenas com a mesma configuração usada para criar as entradas do índice.

É possível configurar índices de expressão mais complexos, onde o nome da configuração é especificado por outra coluna, por exemplo:

```
CREATE INDEX pgweb_idx ON pgweb USING GIN (to_tsvector(config_name, body));
```

onde `config_name` é uma coluna na tabela `pgweb`. Isso permite configurações mistas no mesmo índice, ao mesmo tempo em que registra qual configuração foi usada para cada entrada do índice. Isso seria útil, por exemplo, se a coleção de documentos contivesse documentos em diferentes idiomas. Novamente, as consultas que pretendem usar o índice devem ser formuladas para corresponder, por exemplo, `WHERE to_tsvector(config_name, body) @@ 'a & b'`.

Os índices podem até concatenar colunas:

```
CREATE INDEX pgweb_idx ON pgweb USING GIN (to_tsvector('english', title || ' ' || body));
```

Outra abordagem é criar uma coluna separada `tsvector` para armazenar a saída de `to_tsvector`. Para manter essa coluna automaticamente atualizada com seus dados de origem, use uma coluna gerada armazenada. Este exemplo é uma concatenação de `title` e `body`, usando `coalesce` para garantir que um campo ainda será indexado quando o outro é `NULL`:

```
ALTER TABLE pgweb
    ADD COLUMN textsearchable_index_col tsvector
               GENERATED ALWAYS AS (to_tsvector('english', coalesce(title, '') || ' ' || coalesce(body, ''))) STORED;
```

Em seguida, criamos um índice GIN para acelerar a pesquisa:

```
CREATE INDEX textsearch_idx ON pgweb USING GIN (textsearchable_index_col);
```

Agora, estamos prontos para realizar uma pesquisa rápida de texto completo:

```
SELECT title
FROM pgweb
WHERE textsearchable_index_col @@ to_tsquery('create & table')
ORDER BY last_mod_date DESC
LIMIT 10;
```

Uma vantagem da abordagem de coluna separada em relação a um índice de expressão é que não é necessário especificar explicitamente a configuração de busca de texto nas consultas para fazer uso do índice. Como mostrado no exemplo acima, a consulta pode depender de `default_text_search_config`. Outra vantagem é que as pesquisas serão mais rápidas, uma vez que não será necessário fazer `to_tsvector` chamadas para verificar as correspondências do índice. (Isso é mais importante ao usar um índice GiST do que um índice GIN; veja [Seção 12.9][(textsearch-indexes.md "12.9. Preferred Index Types for Text Search")].). A abordagem de expressão-índice, no entanto, é mais simples de configurar e requer menos espaço em disco, uma vez que a representação `tsvector` não é armazenada explicitamente.