## SPI_register_trigger_data

SPI_register_trigger_data — tornar os dados efêmeros de gatilho disponíveis em consultas SPI

## Sinopse

```
int SPI_register_trigger_data(TriggerData *tdata)
```

## Descrição

`SPI_register_trigger_data` torna as relações efêmeras capturadas por um gatilho disponíveis para consultas planejadas e executadas através da conexão atual do SPI. Atualmente, isso significa que as tabelas de transição capturadas por um gatilho `AFTER` definido com uma cláusula `REFERENCING OLD/NEW TABLE AS`... Isso deve ser chamado por uma função de manipulador de gatilho PL após a conexão.

## Argumentos

`TriggerData *tdata`: o objeto `TriggerData` passado para uma função de manipulador de gatilho como `fcinfo->context`

## Valor de retorno

Se a execução do comando tiver sido bem-sucedida, o seguinte valor (não negativo) será retornado:

`SPI_OK_TD_REGISTER`: se os dados do gatilho capturados (se houver) tiverem sido registrados com sucesso

Em caso de erro, um dos seguintes valores negativos é retornado:

`SPI_ERROR_ARGUMENT`: se *`tdata`* é `NULL`

`SPI_ERROR_UNCONNECTED`: se chamado a partir de uma função C não conectada

`SPI_ERROR_REL_DUPLICATE`: se o nome de qualquer relação de dados de transição do gatilho já estiver registrado para esta conexão