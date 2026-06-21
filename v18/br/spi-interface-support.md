## 45.2. Funções de Suporte de Interface [#](#SPI-INTERFACE-SUPPORT)

* [SPI_fname](spi-spi-fname.md) — determinar o nome da coluna para o número de coluna especificado
* [SPI_fnumber](spi-spi-fnumber.md) — determinar o número de coluna para o nome da coluna especificado
* [SPI_getvalue](spi-spi-getvalue.md) — retornar o valor de string da coluna especificado
* [SPI_getbinval](spi-spi-getbinval.md) — retornar o valor binário da coluna especificado
* [SPI_gettype](spi-spi-gettype.md) — retornar o nome do tipo de dados da coluna especificado
* [SPI_gettypeid](spi-spi-gettypeid.md) — retornar o OID do tipo de dados da coluna especificado
* [SPI_getrelname](spi-spi-getrelname.md) — retornar o nome da relação especificado
* [SPI_getnspname](spi-spi-getnspname.md) — retornar o namespace da relação especificado
* [SPI_result_code_string](spi-spi-result-code-string.md) — retornar o código de erro como string

As funções descritas aqui fornecem uma interface para extrair informações dos conjuntos de resultados retornados por `SPI_execute` e outras funções SPI.

Todas as funções descritas nesta seção podem ser utilizadas tanto por funções C conectadas quanto por funções C desconectadas.