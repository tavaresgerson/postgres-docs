## 7.3. Selecionar listas [#](#QUERIES-SELECT-LISTS)

* [7.3.1. Selecionar itens da lista](queries-select-lists.md#QUERIES-SELECT-LIST-ITEMS)
* [7.3.2. Rótulos de coluna](queries-select-lists.md#QUERIES-COLUMN-LABELS)
* [7.3.3. `DISTINCT`](queries-select-lists.md#QUERIES-DISTINCT)

Como mostrado na seção anterior, a expressão de tabela no comando `SELECT` constrói uma tabela virtual intermediária, combinando tabelas, vistas, eliminando linhas, agrupando, etc. Essa tabela é finalmente passada para o processamento pela *lista de seleção*. A lista de seleção determina quais *colunas* da tabela intermediária são realmente exibidas.

### 7.3.1. Itens de lista selecionada [#](#QUERIES-SELECT-LIST-ITEMS)

O tipo mais simples de lista seletiva é `*`, que emite todas as colunas que a expressão da tabela produz. Caso contrário, uma lista seletiva é uma lista de expressões de valor separadas por vírgula (conforme definido na Seção 4.2 [(sql-expressions.md "4.2. Value Expressions")]). Por exemplo, pode ser uma lista de nomes de colunas:

```
SELECT a, b, c FROM ...
```

Os nomes das colunas `a`, `b` e `c` são os nomes reais das colunas das tabelas referenciadas na cláusula `FROM`, ou os aliases que lhes foram atribuídos, conforme explicado em [Seção 7.2.1.2](queries-table-expressions.md#QUERIES-TABLE-ALIASES "7.2.1.2. Table and Column Aliases"). O espaço de nome disponível na lista de seleção é o mesmo que na cláusula `WHERE`, a menos que seja usado agrupamento, caso em que é o mesmo que na cláusula `HAVING`.

Se mais de uma tabela tiver uma coluna com o mesmo nome, o nome da tabela também deve ser fornecido, como em:

```
SELECT tbl1.a, tbl2.a, tbl1.b FROM ...
```

Ao trabalhar com várias tabelas, também pode ser útil solicitar todas as colunas de uma tabela específica:

```
SELECT tbl1.*, tbl2.a FROM ...
```

Veja [Seção 8.16.5][(rowtypes.md#ROWTYPES-USAGE "8.16.5. Using Composite Types in Queries")] para mais informações sobre a notação *`table_name``.*`.

Se uma expressão de valor arbitrário for usada na lista de seleção, ela conceitualmente adiciona uma nova coluna virtual à tabela devolvida. A expressão de valor é avaliada uma vez para cada linha de resultado, com os valores da linha substituídos por quaisquer referências de coluna. Mas as expressões na lista de seleção não precisam referenciar quaisquer colunas na expressão da tabela da cláusula `FROM`; elas podem ser expressões aritméticas constantes, por exemplo.

### 7.3.2. Rótulos de Coluna [#](#QUERIES-COLUMN-LABELS)

As entradas na lista selecionada podem receber nomes para processamento subsequente, como para uso em uma cláusula `ORDER BY` ou para exibição pelo aplicativo do cliente. Por exemplo:

```
SELECT a AS value, b + c AS sum FROM ...
```

Se não for especificado um nome de coluna de saída usando `AS`, o sistema atribui um nome de coluna padrão. Para referências de coluna simples, este é o nome da coluna referenciada. Para chamadas de função, este é o nome da função. Para expressões complexas, o sistema gerará um nome genérico.

A palavra-chave `AS` é geralmente opcional, mas em alguns casos, quando o nome da coluna desejada corresponde a uma palavra-chave do PostgreSQL, você deve escrever `AS` ou colocar aspas duplas no nome da coluna para evitar ambiguidade. ([Apêndice C](sql-keywords-appendix.md "Appendix C. SQL Key Words") mostra quais palavras-chave exigem que `AS` seja usado como rótulo de coluna.) Por exemplo, `FROM` é uma dessas palavras-chave, então isso não funciona:

```
SELECT a from, b + c AS sum FROM ...
```

mas qualquer uma dessas coisas:

```
SELECT a AS from, b + c AS sum FROM ...
SELECT a "from", b + c AS sum FROM ...
```

Para maior segurança contra possíveis adições futuras de palavras-chave, é recomendável que você sempre escreva `AS` ou coloque aspas duplas no nome da coluna de saída.

### Nota

O nome dos campos de saída aqui é diferente do que é feito na cláusula `FROM` (veja [Seção 7.2.1.2][(queries-table-expressions.md#QUERIES-TABLE-ALIASES "7.2.1.2. Table and Column Aliases")]). É possível renomear o mesmo campo duas vezes, mas o nome atribuído na lista de seleção é o que será passado.

### 7.3.3. `DISTINCT` [#](#QUERIES-DISTINCT)

Após a lista selecionada ter sido processada, a tabela de resultados pode, opcionalmente, ser sujeita à eliminação de linhas duplicadas. A palavra-chave `DISTINCT` é escrita diretamente após `SELECT` para especificar isso:

```
SELECT DISTINCT select_list ...
```

(Em vez de `DISTINCT`, a palavra-chave `ALL` pode ser usada para especificar o comportamento padrão de retenção de todas as linhas.)

Obviamente, duas linhas são consideradas distintas se diferirem em pelo menos um valor de coluna. Valores nulos são considerados iguais nessa comparação.

Alternativamente, uma expressão arbitrária pode determinar quais linhas devem ser consideradas distintas:

```
SELECT DISTINCT ON (expression [, expression ...]) select_list ...
```

Aqui *`expression`* é uma expressão de valor arbitrário que é avaliada para todas as linhas. Um conjunto de linhas para as quais todas as expressões são iguais é considerado duplicado, e apenas a primeira linha do conjunto é mantida na saída. Note que a “primeira linha” de um conjunto é imprevisível, a menos que a consulta seja ordenada em colunas suficientes para garantir uma ordem única das linhas que chegam ao filtro `DISTINCT`. (O processamento de `DISTINCT ON` ocorre após a ordenação de `ORDER BY`.)

A cláusula `DISTINCT ON` não faz parte do padrão SQL e, às vezes, é considerada um estilo ruim devido à natureza potencialmente indeterminada de seus resultados. Com o uso judicioso de `GROUP BY` e subconsultas em `FROM`, esse construtivo pode ser evitado, mas é frequentemente a alternativa mais conveniente.