## 7.5. Ordenação de Linhas (`ORDER BY`) [#](#QUERIES-ORDER)

Após uma consulta produzir uma tabela de saída (após a lista de seleção ter sido processada), ela pode ser ordenada opcionalmente. Se a ordenação não for escolhida, as linhas serão devolvidas em uma ordem não especificada. A ordem real, nesse caso, dependerá dos tipos de plano de varredura e junção, mas não deve ser confiada. Uma ordenação específica de saída só pode ser garantida se a etapa de ordenação for explicitamente escolhida.

A cláusula `ORDER BY` especifica a ordem de classificação:

```sql
SELECT select_list
    FROM table_expression
    ORDER BY sort_expression1 [ASC | DESC] [NULLS { FIRST | LAST }]
             [, sort_expression2 [ASC | DESC] [NULLS { FIRST | LAST }] ...]
```

A(s) expressão(ões) de ordenação pode(m) ser qualquer expressão que seja válida na lista de seleção da consulta. Um exemplo é:

```sql
SELECT a, b FROM table1 ORDER BY a + b, c;
```

Quando mais de uma expressão é especificada, os valores posteriores são usados para ordenar as linhas que são iguais de acordo com os valores anteriores. Cada expressão pode ser seguida por uma palavra-chave opcional `ASC` ou `DESC` para definir a direção de ordenação como ascendente ou descendente. A ordem `ASC` é a padrão. A ordem ascendente coloca os valores menores primeiro, onde “menor” é definido em termos do operador `<`. Da mesma forma, a ordem descendente é determinada com o operador `>`. [[6]](#ftn.id-1.5.6.9.5.10)

As opções `NULLS FIRST` e `NULLS LAST` podem ser usadas para determinar se nulos aparecem antes ou depois de valores não nulos na ordem de classificação. Por padrão, os valores nulos são classificados como se fossem maiores que qualquer valor não nulo; ou seja, `NULLS FIRST` é o padrão para a ordem de `DESC`, e `NULLS LAST` de outra forma.

Observe que as opções de ordenação são consideradas de forma independente para cada coluna de classificação. Por exemplo, `ORDER BY x, y DESC` significa `ORDER BY x ASC, y DESC`, que não é o mesmo que `ORDER BY x DESC, y DESC`.

Um *`sort_expression`* também pode ser o rótulo da coluna ou o número de uma coluna de saída, como em:

```sql
SELECT a + b AS sum, c FROM table1 ORDER BY sum;
SELECT a, max(b) FROM table1 GROUP BY a ORDER BY 1;
```

ambos que ordenam pela primeira coluna de saída. Observe que o nome de uma coluna de saída deve ser usado sozinho, ou seja, não pode ser usado em uma expressão — por exemplo, isso não é correto:

```sql
SELECT a + b AS sum, c FROM table1 ORDER BY sum + c;          -- wrong
```

Essa restrição é feita para reduzir a ambiguidade. Ainda há ambiguidade se um item `ORDER BY` for um nome simples que poderia corresponder a um nome de coluna de saída ou a uma coluna da expressão da tabela. A coluna de saída é usada nesses casos. Isso só causaria confusão se você usar `AS` para renomear uma coluna de saída para corresponder ao nome de uma coluna de outra tabela.

`ORDER BY` pode ser aplicado ao resultado de uma combinação de `UNION`, `INTERSECT` ou `EXCEPT`, mas, neste caso, só é permitido ordenar por nomes ou números de colunas de saída, não por expressões.

---

[[6]](#id-1.5.6.9.5.10) De fato, o PostgreSQL utiliza a *classe de operador B-tree padrão* para o tipo de dados da expressão para determinar a ordem de classificação para `ASC` e `DESC`. Convencionalmente, os tipos de dados serão configurados de forma que os operadores `<` e `>` correspondam a essa ordem de classificação, mas o projetista de um tipo de dados definido pelo usuário pode optar por fazer algo diferente.