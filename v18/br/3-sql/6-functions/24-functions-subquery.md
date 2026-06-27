### 9.24. Expressões de subconsultas [#](#FUNCTIONS-SUBQUERY)

* [9.24.1. `EXISTS`](functions-subquery.md#FUNCTIONS-SUBQUERY-EXISTS)
* [9.24.2. `IN`](functions-subquery.md#FUNCTIONS-SUBQUERY-IN)
* [9.24.3. `NOT IN`](functions-subquery.md#FUNCTIONS-SUBQUERY-NOTIN)
* [9.24.4. `ANY`/`SOME`](functions-subquery.md#FUNCTIONS-SUBQUERY-ANY-SOME)
* [9.24.5. `ALL`](functions-subquery.md#FUNCTIONS-SUBQUERY-ALL)
* [9.24.6. Comparação de uma única linha](functions-subquery.md#FUNCTIONS-SUBQUERY-SINGLE-ROW-COMP)

Esta seção descreve as expressões de subconsulta compatíveis com SQL disponíveis no PostgreSQL. Todas as formas de expressão documentadas nesta seção retornam resultados booleanos (verdadeiro/falso).

#### 9.24.1. `EXISTS` [#](#FUNCTIONS-SUBQUERY-EXISTS)

```sql
EXISTS (subquery)
```

O argumento de `EXISTS` é uma declaração arbitrária de `SELECT`, ou *subconsulta*. A subconsulta é avaliada para determinar se ela retorna alguma linha. Se ela retornar pelo menos uma linha, o resultado de `EXISTS` é “verdadeiro”; se a subconsulta não retornar nenhuma linha, o resultado de `EXISTS` é “falsos”.

A subconsulta pode se referir a variáveis da consulta circundante, que atuam como constantes durante qualquer avaliação da subconsulta.

A subconsulta geralmente será executada apenas o tempo suficiente para determinar se pelo menos uma linha é devolvida, e não até a conclusão. Não é prudente escrever uma subconsulta que tenha efeitos colaterais (como funções de chamada de sequência); o fato de os efeitos colaterais ocorrerem pode ser imprevisível.

Como o resultado depende apenas de se quaisquer linhas são retornadas, e não do conteúdo dessas linhas, a lista de saída da subconsulta normalmente é irrelevante. Uma convenção comum de codificação é escrever todos os testes `EXISTS` na forma `EXISTS(SELECT 1 WHERE ...)`. No entanto, existem exceções a essa regra, como subconsultas que usam `INTERSECT`.

Este exemplo simples é como uma junção interna no `col2`, mas produz, no máximo, uma linha de saída para cada linha do `tab1`, mesmo que haja várias linhas correspondentes do `tab2`:

```sql
SELECT col1
FROM tab1
WHERE EXISTS (SELECT 1 FROM tab2 WHERE col2 = tab1.col2);
```

### 9.24.2. `IN` [#](#FUNCTIONS-SUBQUERY-IN)

```sql
expression IN (subquery)
```

O lado direito é uma subconsulta entre parênteses, que deve retornar exatamente uma coluna. A expressão do lado esquerdo é avaliada e comparada a cada linha do resultado da subconsulta. O resultado de `IN` é “verdadeiro” se qualquer linha da subconsulta igual for encontrada. O resultado é “falso” se nenhuma linha igual for encontrada (incluindo o caso em que a subconsulta não retorna nenhuma linha).

Observe que, se a expressão da mão esquerda produzir nulo, ou se não houver valores iguais na mão direita e pelo menos uma linha da mão direita produzir nulo, o resultado da construção `IN` será nulo, não falso. Isso está de acordo com as regras normais do SQL para combinações booleanas de valores nulos.

Assim como no caso de `EXISTS`, não é prudente assumir que a subconsulta será avaliada completamente.

```sql
row_constructor IN (subquery)
```

O lado esquerdo deste formulário de `IN` é um construtor de linha, conforme descrito em [Seção 4.2.13](sql-expressions.md#SQL-SYNTAX-ROW-CONSTRUCTORS). O lado direito é uma subconsulta entre parênteses, que deve retornar exatamente tantas colunas quanto houver expressões na linha esquerda. As expressões da esquerda são avaliadas e comparadas linha a linha com cada linha do resultado da subconsulta. O resultado de `IN` é “verdadeiro” se qualquer linha da subconsulta igual for encontrada. O resultado é “falso” se nenhuma linha igual for encontrada (incluindo o caso em que a subconsulta não retorne nenhuma linha).

Como de costume, os valores nulos nas linhas são combinados de acordo com as regras normais das expressões booleanas do SQL. Duas linhas são consideradas iguais se todos seus membros correspondentes forem não nulos e iguais; as linhas são desiguais se quaisquer membros correspondentes forem não nulos e desiguais; caso contrário, o resultado daquela comparação de linha é desconhecido (nulo). Se todos os resultados por linha forem desiguais ou nulos, com pelo menos um nulo, então o resultado de `IN` é nulo.

#### 9.24.3. `NOT IN` [#](#FUNCTIONS-SUBQUERY-NOTIN)

```sql
expression NOT IN (subquery)
```

O lado direito é uma subconsulta entre parênteses, que deve retornar exatamente uma coluna. A expressão do lado esquerdo é avaliada e comparada a cada linha do resultado da subconsulta. O resultado de `NOT IN` é “verdadeiro” se apenas as linhas da subconsulta desiguais forem encontradas (incluindo o caso em que a subconsulta não retorne nenhuma linha). O resultado é “falso” se qualquer linha igual for encontrada.

Observe que, se a expressão da mão esquerda resultar em nulo, ou se não houver valores iguais na mão direita e pelo menos uma linha da mão direita resultar em nulo, o resultado da construção `NOT IN` será nulo, não verdadeiro. Isso está de acordo com as regras normais do SQL para combinações booleanas de valores nulos.

Assim como no caso de `EXISTS`, não é prudente assumir que a subconsulta será avaliada completamente.

```sql
row_constructor NOT IN (subquery)
```

O lado esquerdo deste formulário de `NOT IN` é um construtor de linha, conforme descrito em [Seção 4.2.13](sql-expressions.md#SQL-SYNTAX-ROW-CONSTRUCTORS). O lado direito é uma subconsulta entre parênteses, que deve retornar exatamente tantas colunas quanto houver expressões na linha esquerda. As expressões da esquerda são avaliadas e comparadas linha a linha com cada linha do resultado da subconsulta. O resultado de `NOT IN` é “verdadeiro” se apenas as linhas da subconsulta desiguais forem encontradas (incluindo o caso em que a subconsulta não retorne nenhuma linha). O resultado é “falso” se qualquer linha igual for encontrada.

Como de costume, os valores nulos nas linhas são combinados de acordo com as regras normais das expressões booleanas do SQL. Duas linhas são consideradas iguais se todos seus membros correspondentes forem não nulos e iguais; as linhas são desiguais se quaisquer membros correspondentes forem não nulos e desiguais; caso contrário, o resultado daquela comparação de linha é desconhecido (nulo). Se todos os resultados por linha forem desiguais ou nulos, com pelo menos um nulo, então o resultado de `NOT IN` é nulo.

#### 9.24.4. `ANY`/`SOME` [#](#FUNCTIONS-SUBQUERY-ANY-SOME)

```sql
expression operator ANY (subquery)
expression operator SOME (subquery)
```

O lado direito é uma subconsulta entre parênteses, que deve retornar exatamente uma coluna. A expressão do lado esquerdo é avaliada e comparada a cada linha do resultado da subconsulta usando o dado *`operator`*, que deve gerar um resultado booleano. O resultado de `ANY` é “verdadeiro” se qualquer resultado verdadeiro for obtido. O resultado é “falso” se nenhum resultado verdadeiro for encontrado (incluindo o caso em que a subconsulta não retorne nenhuma linha).

`SOME` é sinônimo de `ANY`. `IN` é equivalente a `= ANY`.

Observe que, se não houver sucessos e pelo menos uma linha da direita retornar nulo para o resultado do operador, o resultado da construção `ANY` será nulo, não falso. Isso está de acordo com as regras normais do SQL para combinações booleanas de valores nulos.

Assim como no caso de `EXISTS`, não é prudente assumir que a subconsulta será avaliada completamente.

```sql
row_constructor operator ANY (subquery)
row_constructor operator SOME (subquery)
```

O lado esquerdo deste formulário de `ANY` é um construtor de linha, conforme descrito em [Seção 4.2.13](sql-expressions.md#SQL-SYNTAX-ROW-CONSTRUCTORS). O lado direito é uma subconsulta entre parênteses, que deve retornar exatamente tantas colunas quanto houver expressões na linha esquerda. As expressões da esquerda são avaliadas e comparadas linha a linha com cada linha do resultado da subconsulta, usando o dado *`operator`*. O resultado de `ANY` é “verdadeiro” se a comparação retornar verdadeiro para qualquer linha da subconsulta. O resultado é “falso” se a comparação retornar falso para cada linha da subconsulta (incluindo o caso em que a subconsulta não retorne nenhuma linha). O resultado é NULL se nenhuma comparação com uma linha da subconsulta retornar verdadeiro, e pelo menos uma comparação retornar NULL.

Consulte a [Seção 9.25.5](functions-comparisons.md#ROW-WISE-COMPARISON) para obter detalhes sobre o significado da comparação de um construtor de linha.

#### 9.24.5. `ALL` [#](#FUNCTIONS-SUBQUERY-ALL)

```sql
expression operator ALL (subquery)
```

O lado direito é uma subconsulta entre parênteses, que deve retornar exatamente uma coluna. A expressão do lado esquerdo é avaliada e comparada a cada linha do resultado da subconsulta usando o dado *`operator`*, que deve gerar um resultado booleano. O resultado de `ALL` é “verdadeiro” se todas as linhas gerarem verdadeiro (incluindo o caso em que a subconsulta não retorne nenhuma linha). O resultado é “falso” se qualquer resultado falso for encontrado. O resultado é NULL se nenhuma comparação com uma linha da subconsulta retornar falso, e pelo menos uma comparação retornar NULL.

`NOT IN` é equivalente a `<> ALL`.

Assim como no caso de `EXISTS`, não é prudente assumir que a subconsulta será avaliada completamente.

```sql
row_constructor operator ALL (subquery)
```

O lado esquerdo deste formulário de `ALL` é um construtor de linha, conforme descrito em [Seção 4.2.13](sql-expressions.md#SQL-SYNTAX-ROW-CONSTRUCTORS). O lado direito é uma subconsulta entre parênteses, que deve retornar exatamente tantas colunas quanto houver expressões na linha esquerda. As expressões da esquerda são avaliadas e comparadas linha a linha com cada linha do resultado da subconsulta, usando o dado *`operator`*. O resultado de `ALL` é “verdadeiro” se a comparação retornar verdadeiro para todas as linhas da subconsulta (incluindo o caso em que a subconsulta não retorne nenhuma linha). O resultado é “falso” se a comparação retornar falso para qualquer linha da subconsulta. O resultado é NULL se nenhuma comparação com uma linha da subconsulta retornar falso, e pelo menos uma comparação retornar NULL.

Consulte a [Seção 9.25.5](functions-comparisons.md#ROW-WISE-COMPARISON) para obter detalhes sobre o significado da comparação de um construtor de linha.

#### 9.24.6. Comparação de linha única [#](#FUNCTIONS-SUBQUERY-SINGLE-ROW-COMP)

```sql
row_constructor operator (subquery)
```

O lado esquerdo é um construtor de linha, conforme descrito em [Seção 4.2.13](sql-expressions.md#SQL-SYNTAX-ROW-CONSTRUCTORS). O lado direito é uma subconsulta entre parênteses, que deve retornar exatamente tantas colunas quanto houver expressões na linha do lado esquerdo. Além disso, a subconsulta não pode retornar mais de uma linha. (Se ela retornar zero linhas, o resultado é considerado nulo.) O lado esquerdo é avaliado e comparado linha a linha com a única linha do resultado da subconsulta.

Veja [Seção 9.25.5](functions-comparisons.md#ROW-WISE-COMPARISON) para obter detalhes sobre o significado de uma comparação de construtor de linha.