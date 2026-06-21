## SPI_palloc

SPI_palloc — alocar memória no contexto do executor superior

## Sinopse

```
void * SPI_palloc(Size size)
```

## Descrição

`SPI_palloc` aloca memória no contexto do executor superior.

Essa função só pode ser usada quando conectado ao SPI. Caso contrário, ela lança um erro.

## Argumentos

`Size size`: tamanho em bytes de armazenamento a ser alocado

## Valor de retorno

ponteiro para novo espaço de armazenamento do tamanho especificado