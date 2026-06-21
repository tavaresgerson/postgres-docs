## SPI_result_code_string

SPI_result_code_string — retornar o código de erro como uma string

## Sinopse

```
const char * SPI_result_code_string(int code);
```

## Descrição

`SPI_result_code_string` retorna uma representação em cadeia do código de resultado retornado por várias funções SPI ou armazenado em `SPI_result`.

## Argumentos

`int code`: código de resultado

## Valor de retorno

Uma representação em cadeia do código de resultado.