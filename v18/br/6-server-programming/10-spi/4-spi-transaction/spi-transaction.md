## 45.4. Gerenciamento de Transações [#](#SPI-TRANSACTION)

* [SPI_commit](spi-spi-commit.md) — confirmar a transação atual
* [SPI_rollback](spi-spi-rollback.md) — abortar a transação atual
* [SPI_start_transaction](spi-spi-start-transaction.md) — função obsoleta

Não é possível executar comandos de controle de transação, como `COMMIT` e `ROLLBACK`, através de funções SPI, como `SPI_execute`. No entanto, existem funções de interface separadas que permitem o controle de transação através do SPI.

Não é geralmente seguro e sensato iniciar e finalizar transações em funções arbitrariamente definidas pelo usuário que possam ser chamadas por SQL, sem levar em consideração o contexto em que elas são chamadas. Por exemplo, um limite de transação no meio de uma função que faz parte de uma expressão SQL complexa que faz parte de algum comando SQL provavelmente resultará em erros internos obscuros ou travamentos. As funções de interface apresentadas aqui são projetadas principalmente para serem usadas por implementações de linguagem procedural para suportar a gestão de transações em procedimentos de nível SQL que são invocados pelo comando `CALL`, levando em consideração o contexto da invocação do `CALL`. Procedimentos que utilizam SPI implementados em C podem implementar a mesma lógica, mas os detalhes disso estão além do escopo desta documentação.