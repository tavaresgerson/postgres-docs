## N. 2. Configurando as cores [#](#COLOR-WHICH)

As cores reais a serem usadas são configuradas usando a variável de ambiente `PG_COLORS` (note plural). O valor é uma lista de pares `key=value` separados por colon. As chaves especificam para que a cor será usada. Os valores são especificações SGR (Selecionar Renderização Gráfica), que são interpretadas pelo terminal.

As seguintes teclas estão atualmente em uso:

`error`: usado para destacar o texto “erro” nas mensagens de erro

`warning`: usado para destacar o texto “aviso” em mensagens de aviso

`note`: usado para destacar o texto “detalhe” e “sinal” em tais mensagens

`locus`: usado para destacar informações de localização (por exemplo, nome do programa e nome do arquivo) em mensagens

O valor padrão é `error=01;31:warning=01;35:note=01;36:locus=01` (`01;31` = vermelho em negrito, `01;35` = magenta em negrito, `01;36` = ciano em negrito, `01` = cor padrão em negrito).

DICA

Esse formato de especificação de cor também é usado por outros pacotes de software, como GCC, GNU coreutils e GNU grep.