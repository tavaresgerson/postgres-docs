## 12.11. Limitações [#](#TEXTSEARCH-LIMITATIONS)

As limitações atuais das funcionalidades de busca de texto do PostgreSQL são:

* O comprimento de cada léxico deve ser menor que 2 kilobytes
* O comprimento de um `tsvector` (léxicos + posições) deve ser menor que 1 megabyte
* O número de léxicos deve ser menor que 264
* Os valores de posição em `tsvector` devem ser maiores que 0 e não mais que 16.383
* A distância de correspondência em um `<N>` (FOLLOWED BY) `tsquery` não pode ser maior que 16.384
* Não mais que 256 posições por léxico
* O número de nós (léxicos + operadores) em um `tsquery` deve ser menor que 32.768

Para comparação, a documentação do PostgreSQL 8.1 continha 10.441 palavras únicas, um total de 335.420 palavras, e a palavra mais frequente “postgresql” foi mencionada 6.127 vezes em 655 documentos.

Outro exemplo — os arquivos da lista de correio do PostgreSQL continham 910.989 palavras únicas com 57.491.343 lexemas em 461.020 mensagens.