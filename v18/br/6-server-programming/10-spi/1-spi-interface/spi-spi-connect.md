## SPI_connect

SPI_connect, SPI_connect_ext — conectar uma função C ao gerenciador SPI

## Sinopse

```
int SPI_connect(void)
```

```
int SPI_connect_ext(int options)
```

## Descrição

`SPI_connect` abre uma conexão a partir de uma invocação de função C para o gerenciador SPI. Você deve chamar essa função se quiser executar comandos através do SPI. Algumas funções utilitárias do SPI podem ser chamadas a partir de funções C desconectadas.

`SPI_connect_ext` faz o mesmo, mas tem um argumento que permite a passagem de flags de opção. Atualmente, os seguintes valores de opção estão disponíveis:

`SPI_OPT_NONATOMIC`: Define a conexão SPI como *nonatomic*, o que significa que as chamadas de controle de transação (`SPI_commit`, `SPI_rollback`) são permitidas. Caso contrário, a chamada dessas funções resultará em um erro imediato.

`SPI_connect()` é equivalente a `SPI_connect_ext(0)`.

## Valor de retorno

`SPI_OK_CONNECT`: em caso de sucesso

O fato de essas funções retornarem `int` e não `void` é histórico. Todos os casos de falha são relatados via `ereport` ou `elog`. (Em versões anteriores ao PostgreSQL v10, alguns, mas não todos os casos de falha, seriam relatados com um valor de resultado de `SPI_ERROR_CONNECT`.)