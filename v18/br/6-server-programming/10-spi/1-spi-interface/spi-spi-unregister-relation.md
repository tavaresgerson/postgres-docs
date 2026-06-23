## SPI_unregister_relation

SPI_unregister_relation — remover uma relação temporária com nome no registro

## Sinopse

```
int SPI_unregister_relation(const char * name)
```

## Descrição

`SPI_unregister_relation` remove uma relação nomeada efêmera do registro para a conexão atual.

## Argumentos

`const char * name`: o nome da entrada do registro de relações

## Valor de retorno

Se a execução do comando tiver sido bem-sucedida, o seguinte valor (não negativo) será retornado:

`SPI_OK_REL_UNREGISTER`: se o tuplestore tiver sido removido com sucesso do registro

Em caso de erro, um dos seguintes valores negativos é retornado:

`SPI_ERROR_ARGUMENT`: se *`name`* é `NULL`

`SPI_ERROR_UNCONNECTED`: se chamado a partir de uma função C não conectada

`SPI_ERROR_REL_NOT_FOUND`: se *`name`* não for encontrado no registro para a conexão atual