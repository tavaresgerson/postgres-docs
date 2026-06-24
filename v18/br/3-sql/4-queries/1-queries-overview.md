### 7.1. Visão geral [#](#QUERIES-OVERVIEW)

O processo de recuperação ou o comando para recuperar dados de um banco de dados é chamado de *consulta*. No SQL, o comando `SELECT`(sql-select.md "SELECT") é usado para especificar consultas. A sintaxe geral do comando `SELECT` é

```
[WITH with_queries] SELECT select_list FROM table_expression [sort_specification]
```

As seções a seguir descrevem os detalhes da lista selecionada, a expressão da tabela e a especificação de classificação. As consultas `WITH` são tratadas como último item, pois são um recurso avançado.

Uma consulta simples tem a seguinte forma:

```
SELECT * FROM table1;
```

Supondo que haja uma tabela chamada `table1`, este comando recuperaria todas as linhas e todas as colunas definidas pelo usuário de `table1`. (O método de recuperação depende do aplicativo cliente. Por exemplo, o programa psql exibirá uma tabela em ASCII no ecrã, enquanto as bibliotecas de cliente oferecerão funções para extrair valores individuais do resultado da consulta.) A especificação da lista de seleção `*` significa todas as colunas que a expressão da tabela oferece. Uma lista de seleção também pode selecionar um subconjunto das colunas disponíveis ou realizar cálculos usando as colunas. Por exemplo, se `table1` tiver colunas com os nomes `a`, `b` e `c` (e talvez outras) você pode fazer a seguinte consulta:

```
SELECT a, b + c FROM table1;
```

(assumindo que `b` e `c` são de um tipo de dados numérico). Veja [Seção 7.3](queries-select-lists.md) para mais detalhes.

`FROM table1` é um tipo simples de expressão de tabela: ele lê apenas uma tabela. Em geral, as expressões de tabela podem ser construções complexas de tabelas base, junções e subconsultas. Mas você também pode omitir a expressão de tabela inteiramente e usar o comando `SELECT` como um calculador:

```
SELECT 3 * 4;
```

Isso é mais útil se as expressões na lista de seleção retornarem resultados variáveis. Por exemplo, você pode chamar uma função dessa maneira:

```
SELECT random();
```
