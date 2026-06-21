## 45.3. Gerenciamento de memória [#](#SPI-MEMORY)

* [SPI_palloc][(spi-spi-palloc.md)] — alocar memória no contexto do executor superior
* [SPI_repalloc][(spi-realloc.md)] — realocar memória no contexto do executor superior
* [SPI_pfree][(spi-spi-pfree.md)] — liberar memória no contexto do executor superior
* [SPI_copytuple][(spi-spi-copytuple.md)] — fazer uma cópia de uma linha no contexto do executor superior
* [SPI_returntuple][(spi-spi-returntuple.md)] — preparar para retornar uma tupla como um Datum
* [SPI_modifytuple][(spi-spi-modifytuple.md)] — criar uma linha substituindo os campos selecionados de uma linha dada
* [SPI_freetuple][(spi-spi-freetuple.md)] — liberar uma linha alocada no contexto do executor superior
* [SPI_freetuptable][(spi-spi-freetupletable.md)] — liberar uma linha definida criada por `SPI_execute` ou uma função semelhante
* [SPI_freeplan][(spi-spi-freeplan.md)] — liberar uma declaração preparada salva anteriormente

O PostgreSQL aloca memória dentro de contextos *de memória*, que fornecem um método conveniente para gerenciar as alocações feitas em muitos lugares diferentes que precisam existir por diferentes períodos de tempo. A destruição de um contexto libera toda a memória que foi alocada nele. Assim, não é necessário acompanhar objetos individuais para evitar vazamentos de memória; em vez disso, apenas um número relativamente pequeno de contextos precisa ser gerenciado. `palloc` e funções relacionadas alocam memória do contexto “corrente”.

`SPI_connect` cria um novo contexto de memória e o torna atual. `SPI_finish` restaura o contexto de memória atual anterior e destrói o contexto criado por `SPI_connect`. Essas ações garantem que as alocações de memória transitórias feitas dentro da sua função C sejam recuperadas na saída da função C, evitando vazamento de memória.

No entanto, se sua função C precisar retornar um objeto em memória alocada (como um valor de um tipo de dados de passagem por referência), você não pode alocar essa memória usando `palloc`, pelo menos não enquanto estiver conectado ao SPI. Se você tentar, o objeto será realocado por `SPI_finish`, e sua função C não funcionará de forma confiável. Para resolver esse problema, use `SPI_palloc` para alocar memória para seu objeto de retorno. `SPI_palloc` aloca memória no "contexto do executor superior", ou seja, o contexto de memória que estava em uso quando `SPI_connect` foi chamado, que é exatamente o contexto certo para um valor retornado de sua função C. Várias das outras funções utilitárias descritas nesta seção também retornam objetos criados no contexto do executor superior.

Quando `SPI_connect` é chamado, o contexto privado da função C, que é criado por `SPI_connect`, é tornado o contexto atual. Todas as alocações feitas por `palloc`, `repalloc` ou funções utilitárias do SPI (exceto conforme descrito nesta seção) são feitas neste contexto. Quando uma função C se desconecta do gerenciador do SPI (via `SPI_finish`, o contexto atual é restaurado ao contexto do executor superior, e todas as alocações feitas no contexto de memória da função C são liberadas e não podem ser usadas mais.