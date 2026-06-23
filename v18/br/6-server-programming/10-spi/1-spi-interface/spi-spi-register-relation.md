## SPI_register_relation

SPI_register_relation — tornar uma relação nomeada efêmera disponível pelo nome em consultas SPI

## Sinopse

```
int SPI_register_relation(EphemeralNamedRelation enr)
```

## Descrição

`SPI_register_relation` faz uma relação temporária com informações associadas disponível para consultas planejadas e executadas através da conexão atual do SPI.

## Argumentos

`EphemeralNamedRelation enr`: a inscrição efêmera no registro de relações nomeadas]

## Valor de retorno

Se a execução do comando tiver sido bem-sucedida, o seguinte valor (não negativo) será retornado:

`SPI_OK_REL_REGISTER`: se a relação tiver sido registrada com sucesso pelo nome

Em caso de erro, um dos seguintes valores negativos é retornado:

`SPI_ERROR_ARGUMENT`: se *`enr`* é `NULL` ou seu campo `name` é `NULL`

`SPI_ERROR_UNCONNECTED`: se chamado a partir de uma função C não conectada

`SPI_ERROR_REL_DUPLICATE`: se o nome especificado no campo `name` do *`enr`* já estiver registrado para esta conexão