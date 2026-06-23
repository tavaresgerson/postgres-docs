## 34.16. Modo de compatibilidade Oracle [#](#ECPG-ORACLE-COMPAT)

`ecpg` pode ser executado em um modo de compatibilidade chamado *Oracle*. Se esse modo estiver ativo, ele tenta se comportar como se fosse o Oracle Pro*C.

Especificamente, este modo altera `ecpg` de três maneiras:

* Matrizes de caracteres de bloco que recebem tipos de string de caracteres com espaços finais até o comprimento especificado
* Terminate com byte zero essas matrizes de caracteres e defina a variável indicadora se ocorrer a truncagem
* Defina o indicador nulo para `-1` quando as matrizes de caracteres recebem tipos de string de caracteres vazios