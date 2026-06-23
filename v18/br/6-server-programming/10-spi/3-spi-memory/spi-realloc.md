## SPI_repalloc

SPI_repalloc — realocar memória no contexto do executor superior

## Sinopse

```
void * SPI_repalloc(void * pointer, Size size)
```

## Descrição

`SPI_repalloc` altera o tamanho de um segmento de memória previamente alocado usando `SPI_palloc`.

Essa função não é mais diferente da simples `repalloc`. Ela é mantida apenas para compatibilidade reversa de código existente.

## Argumentos

`void * pointer`: ponteiro para armazenamento existente para alterar

`Size size`: tamanho em bytes de armazenamento a ser alocado

## Valor de retorno

ponta para novo espaço de armazenamento de tamanho especificado, com o conteúdo copiado da área existente