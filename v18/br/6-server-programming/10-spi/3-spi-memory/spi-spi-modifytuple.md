## SPI_modifytuple

SPI_modifytuple — criar uma linha substituindo os campos selecionados de uma linha dada

## Sinopse

```
HeapTuple SPI_modifytuple(Relation rel, HeapTuple row, int ncols,
                          int * colnum, Datum * values, const char * nulls)
```

## Descrição

`SPI_modifytuple` cria uma nova linha substituindo novos valores para as colunas selecionadas, copiando as colunas da linha original em outras posições. A linha de entrada não é modificada. A nova linha é devolvida no contexto superior do executor.

Essa função só pode ser usada quando conectado ao SPI. Caso contrário, ela retorna NULL e define `SPI_result` para `SPI_ERROR_UNCONNECTED`.

## Argumentos

`Relation rel`: Usado apenas como fonte do descritor de linha para a linha. (Passar uma relação em vez de um descritor de linha é um erro.)

`HeapTuple row`: linha a ser modificada

`int ncols`: número de colunas a serem alteradas

`int * colnum`: um array de comprimento *`ncols`*, contendo os números das colunas que devem ser alterados (os números das colunas começam em 1)

`Datum * values`: um array de comprimento *`ncols`*, contendo os novos valores para as colunas especificadas

`const char * nulls`: um array de comprimento *`ncols`*, descrevendo quais novos valores são nulos

Se *`nulls`* for `NULL` então `SPI_modifytuple` assume que nenhum novo valor é nulo. Caso contrário, cada entrada do *`nulls`* deve ser `' '` se o valor novo correspondente for não nulo, ou `'n'` se o valor novo correspondente for nulo. (Neste último caso, o valor real na entrada correspondente de *`values`* não importa.) Note que *`nulls`* não é uma string de texto, apenas um array: ele não precisa de um `'\0'` terminator.

## Valor de retorno

nova linha com modificações, alocada no contexto superior do executor, ou `NULL` em caso de erro (consulte `SPI_result` para indicação de erro)

Em caso de erro, `SPI_result` é definido da seguinte forma:

`SPI_ERROR_ARGUMENT`: se *`rel`* é `NULL`, ou se *`row`* é `NULL`, ou se *`ncols`* é menor ou igual a 0, ou se *`colnum`* é `NULL`, ou se *`values`* é `NULL`.

`SPI_ERROR_NOATTRIBUTE`: se *`colnum`* contém um número de coluna inválido (menor ou igual a 0 ou maior que o número de colunas em *`row`*)

`SPI_ERROR_UNCONNECTED`: se o SPI não estiver ativo