## SPI_exec

SPI_exec — executar um comando de leitura/escrita

## Sinopse

```
int SPI_exec(const char * command, long count)
```

## Descrição

`SPI_exec` é o mesmo que `SPI_execute`, sendo que o parâmetro *`read_only`* do último é sempre considerado `false`.

## Argumentos

`const char * command`: string contendo o comando a ser executado

`long count`: número máximo de linhas a serem devolvidas, ou `0` para sem limite

## Valor de retorno

Veja `SPI_execute`.