## F.47. tsm_system_time — o método de amostragem `SYSTEM_TIME` para `TABLESAMPLE` [#](#TSM-SYSTEM-TIME)

* [F.47.1. Exemplos](tsm-system-time.md#TSM-SYSTEM-TIME-EXAMPLES)

O módulo `tsm_system_time` fornece o método de amostragem de tabela `SYSTEM_TIME`, que pode ser usado na cláusula `TABLESAMPLE` de um comando [`SELECT`](sql-select.md "SELECT").

Este método de amostragem de tabela aceita um único argumento de ponto flutuante que é o número máximo de milissegundos a ser gasto na leitura da tabela. Isso lhe dá controle direto sobre o tempo que a consulta leva, no preço de que o tamanho da amostra se torna difícil de prever. A amostra resultante conterá tantas linhas quanto puderem ser lidas no tempo especificado, a menos que toda a tabela tenha sido lida primeiro.

Assim como o método de amostragem embutido `SYSTEM`, o `SYSTEM_TIME` realiza a amostragem em nível de bloco, de modo que a amostra não seja completamente aleatória, mas pode estar sujeita a efeitos de agrupamento, especialmente se apenas um pequeno número de linhas for selecionado.

`SYSTEM_TIME` não suporta a cláusula `REPEATABLE`.

Este módulo é considerado "confiável", ou seja, pode ser instalado por usuários não superusuários que possuem privilégio `CREATE` no banco de dados atual.

### F.47.1. Exemplos [#](#TSM-SYSTEM-TIME-EXAMPLES)

Aqui está um exemplo de seleção de uma amostra de uma tabela com `SYSTEM_TIME`. Primeiro, instale a extensão:

```
CREATE EXTENSION tsm_system_time;
```

Em seguida, você pode usá-lo em um comando `SELECT`, por exemplo:

```
SELECT * FROM my_table TABLESAMPLE SYSTEM_TIME(1000);
```

Esse comando retornará uma amostra tão grande de `my_table` quanto puder ler em 1 segundo (1000 milissegundos). Claro, se toda a tabela puder ser lida em menos de 1 segundo, todas as suas linhas serão devolvidas.