## F.46. tsm_system_rows — o método de amostragem `SYSTEM_ROWS` para `TABLESAMPLE` [#](#TSM-SYSTEM-ROWS)

* [F.46.1. Exemplos](tsm-system-rows.md#TSM-SYSTEM-ROWS-EXAMPLES)

O módulo `tsm_system_rows` fornece o método de amostragem de tabela `SYSTEM_ROWS`, que pode ser usado na cláusula `TABLESAMPLE` de um comando [`SELECT`](sql-select.md "SELECT").

Este método de amostragem de tabela aceita um único argumento inteiro, que é o número máximo de linhas a serem lidas. A amostra resultante sempre conterá exatamente tantas linhas, a menos que a tabela não contenha linhas suficientes, no caso em que toda a tabela é selecionada.

Assim como o método de amostragem embutido `SYSTEM`, o `SYSTEM_ROWS` realiza a amostragem em nível de bloco, de modo que a amostra não seja completamente aleatória, mas pode estar sujeita a efeitos de agrupamento, especialmente se apenas um pequeno número de linhas for solicitado.

`SYSTEM_ROWS` não suporta a cláusula `REPEATABLE`.

Este módulo é considerado "confiável", ou seja, pode ser instalado por usuários não superusuários que possuem privilégio `CREATE` no banco de dados atual.

### F.46.1. Exemplos [#](#TSM-SYSTEM-ROWS-EXAMPLES)

Aqui está um exemplo de seleção de uma amostra de uma tabela com `SYSTEM_ROWS`. Primeiro, instale a extensão:

```
CREATE EXTENSION tsm_system_rows;
```

Em seguida, você pode usá-lo em um comando `SELECT`, por exemplo:

```
SELECT * FROM my_table TABLESAMPLE SYSTEM_ROWS(100);
```

Este comando retornará uma amostra de 100 linhas da tabela `my_table` (a menos que a tabela não tenha 100 linhas visíveis, no caso em que todas as suas linhas serão devolvidas).