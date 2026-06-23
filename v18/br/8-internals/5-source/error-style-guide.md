## 55.3. Guia de estilo de mensagem de erro [#](#ERROR-STYLE-GUIDE)

Este guia de estilo é oferecido na esperança de manter um estilo consistente e amigável para o usuário em todas as mensagens geradas pelo PostgreSQL.

### Para onde vai [#](#ERROR-STYLE-GUIDE-WHAT-GOES-WHERE)

A mensagem principal deve ser curta, factual e evitar referência a detalhes de implementação, como nomes específicos de funções. “Curta” significa “deverá caber em uma linha sob condições normais”. Use uma mensagem detalhada, se necessário, para manter a mensagem principal curta, ou se sentir a necessidade de mencionar detalhes de implementação, como a chamada específica do sistema que falhou. Tanto as mensagens principais quanto as detalhadas devem ser factuais. Use uma mensagem de dica para sugestões sobre o que fazer para corrigir o problema, especialmente se a sugestão não for sempre aplicável.

Por exemplo, em vez de:

```
IpcMemoryCreate: shmget(key=%d, size=%u, 0%o) failed: %m
(plus a long addendum that is basically a hint)
```

escreva:

```
Primary:    could not create shared memory segment: %m
Detail:     Failed syscall was shmget(key=%d, size=%u, 0%o).
Hint:       The addendum, written as a complete sentence.
```

Razão: manter a mensagem principal curta ajuda a manter o ponto e permite que os clientes disponham o espaço de tela na suposição de que uma linha é suficiente para mensagens de erro. Mensagens de detalhe e dicas podem ser relegadas a um modo verbose, ou talvez uma janela de detalhes de erro pop-up. Além disso, detalhes e dicas normalmente seriam suprimidos do log do servidor para economizar espaço. A referência a detalhes de implementação é melhor evitada, uma vez que não se espera que os usuários conheçam os detalhes.

### Formatação [#](#ERROR-STYLE-GUIDE-FORMATTING)

Não coloque nenhuma suposição específica sobre formatação nos textos das mensagens. Espere que clientes e o log do servidor ajustem as linhas de acordo com suas próprias necessidades. Em mensagens longas, os caracteres de nova linha (\n) podem ser usados para indicar sugestões de quebra de parágrafo. Não termine uma mensagem com uma nova linha. Não use tabs ou outros caracteres de formatação. (Em exibições de contexto de erro, as novas linhas são adicionadas automaticamente para separar os níveis de contexto, como chamadas de função.)

Razão: As mensagens não são necessariamente exibidas em telas de tipo terminal. Em telas de interface gráfica de usuário ou navegadores, essas instruções de formatação são, no máximo, ignoradas.

### Aspas [#](#ERROR-STYLE-GUIDE-QUOTATION-MARKS)

O texto em inglês deve usar aspas duplas quando a citação é apropriada. O texto em outros idiomas deve usar consistentemente um tipo de aspas que esteja de acordo com os costumes de publicação e a saída de computadores de outros programas.

Razão: A escolha de aspas duplas em vez de aspas simples é um tanto arbitrária, mas tende a ser o uso preferido. Alguns sugerem escolher o tipo de aspas dependendo do tipo de objeto de acordo com as convenções SQL (ou seja, strings com aspas simples, identificadores com aspas duplas). Mas essa é uma questão técnica interna à linguagem que muitos usuários nem sequer conhecem, não se aplica a outros tipos de termos citados, não se traduz para outros idiomas e também é bastante inútil.

### Uso de citações [#](#ERROR-STYLE-GUIDE-QUOTES)

Sempre use aspas para delimitar os nomes de arquivos, identificadores fornecidos pelo usuário, nomes de variáveis de configuração e outras variáveis que possam conter palavras. Não use-as para marcar variáveis que não contenham palavras (por exemplo, nomes de operadores).

Existem funções no backend que colocarão as próprias saídas entre aspas, conforme necessário (por exemplo, `format_type_be()`). Não coloque aspas adicionais ao redor das saídas dessas funções.

Razão: Os objetos podem ter nomes que criam ambiguidade quando incorporados em uma mensagem. Seja consistente ao denotar onde um nome conectado começa e termina. Mas não sobrecarregue as mensagens com aspas desnecessárias ou duplicadas.

### Gramática e pontuação [#](#ERROR-STYLE-GUIDE-GRAMMAR-PUNCTUATION)

As regras são diferentes para mensagens de erro primário e para mensagens de detalhe/sinalização:

Mensagens de erro primárias: Não capitalize a primeira letra. Não termine uma mensagem com um ponto. Nem sequer pense em terminar uma mensagem com um ponto de exclamação.

Mensagens de detalhe e dicas: Use frases completas e termine cada uma com um ponto. Capitalize a primeira palavra das frases. Coloque dois espaços após o ponto se outra frase seguir (para texto em inglês; pode ser inadequado em outros idiomas).

Strings de contexto de erro: Não capitalize a primeira letra e não termine a string com um ponto. As strings de contexto normalmente não devem ser frases completas.

Razão: Evitar a pontuação facilita para as aplicações do cliente incorporar a mensagem em uma variedade de contextos gramaticais. Muitas vezes, as mensagens primárias não são frases gramaticalmente completas. (E, se forem longas o suficiente para ser mais do que uma frase, devem ser divididas em partes primárias e de detalhe.) No entanto, as mensagens de detalhe e dicas são mais longas e podem precisar incluir várias frases. Por consistência, elas devem seguir o estilo de frases completas mesmo quando houver apenas uma frase.

### Maiúsculas vs. minúsculas [#](#ERROR-STYLE-GUIDE-CASE)

Use letras minúsculas para a redação da mensagem, incluindo a primeira letra de uma mensagem de erro primária. Use letras maiúsculas para comandos SQL e palavras-chave se elas aparecerem na mensagem.

Razão: É mais fácil fazer tudo parecer mais consistente dessa forma, já que algumas mensagens são frases completas e outras

### Evite a voz passiva [#](#ERROR-STYLE-GUIDE-PASSIVE-VOICE)

Use a voz ativa. Use frases completas quando houver um sujeito ativo (“A não poderia fazer B”). Use o estilo de telegrama sem sujeito se o sujeito for o próprio programa; não use “Eu” para o programa.

Razão: O programa não é humano. Não se faça iludir.

Presente vs. Pretérito [#](#ERROR-STYLE-GUIDE-TENSE)

Use o pretérito se uma tentativa de fazer algo falhou, mas talvez possa ter sucesso na próxima vez (talvez depois de resolver algum problema). Use o presente se o fracasso for definitivamente permanente.

Há uma diferença semântica não trivial entre as frases do tipo:

```
could not open file "%s": %m
```

e:

```
cannot open file "%s"
```

A primeira significa que a tentativa de abrir o arquivo falhou. A mensagem deve fornecer um motivo, como "disco cheio" ou "arquivo não existe". O pretérito é apropriado porque, na próxima vez, o disco pode não estar cheio mais ou o arquivo em questão pode existir.

A segunda forma indica que a funcionalidade de abrir o arquivo nomeado não existe em absoluto no programa, ou que é conceitualmente impossível. O uso do presente é apropriado porque a condição persistirá indefinidamente.

Razão: É claro que o usuário médio não será capaz de tirar grandes conclusões apenas com base na conjugação da mensagem, mas como a língua nos fornece uma gramática que devemos usar corretamente.

### Tipo do Objeto [#](#ERROR-STYLE-GUIDE-OBJECT-TYPE)

Ao citar o nome de um objeto, indique que tipo de objeto é.

Razão: Caso contrário, ninguém saberá a que se refere o "foo.bar.baz".

### Brackets [#](#ERROR-STYLE-GUIDE-BRACKETS)

Os colchetes devem ser usados apenas (1) em sinopses de comandos para denotar argumentos opcionais, ou (2) para denotar um índice de matriz.

Razão: Qualquer outra coisa não corresponde ao uso costumeiro amplamente conhecido e vai confundir as pessoas.

### Mensagens de erro de montagem [#](#ERROR-STYLE-GUIDE-ERROR-MESSAGES)

Quando uma mensagem inclui texto gerado em outro lugar, inclua-o neste estilo:

```
could not open file %s: %m
```

Razão: seria difícil explicar todos os códigos de erro possíveis para colar isso em uma única frase suave, então algum tipo de pontuação é necessário. Colocar o texto embutido entre parênteses também foi sugerido, mas é natural se o texto embutido é provável que seja a parte mais importante da mensagem, como é frequentemente o caso.

### Razões dos erros [#](#ERROR-STYLE-GUIDE-ERROR-REASONS)

As mensagens devem sempre indicar a razão pela qual ocorreu um erro. Por exemplo:

```
BAD:    could not open file %s
BETTER: could not open file %s (I/O failure)
```

Se não houver motivo conhecido, é melhor consertar o código.

### Nomes de Funções [#](#ERROR-STYLE-GUIDE-FUNCTION-NAMES)

Não inclua o nome da rotina de relatórios no texto do erro. Temos outros mecanismos para descobrir isso quando necessário, e para a maioria dos usuários, não são informações úteis. Se o texto do erro não faz muito sentido sem o nome da função, reformule-o.

```
BAD:    pg_strtoint32: error in "z": cannot parse "z"
BETTER: invalid input syntax for type integer: "z"
```

Evite mencionar os nomes das funções chamadas; em vez disso, diga o que o código estava tentando fazer:

```
BAD:    open() failed: %m
BETTER: could not open file %s: %m
```

Se realmente parecer necessário, mencione a chamada de sistema na mensagem detalhada. (Em alguns casos, fornecer os valores reais passados para a chamada de sistema pode ser informações apropriadas para a mensagem detalhada.)

Razão: os usuários não sabem o que todas essas funções fazem.

### Palavras Difíceis para Evitar [#](#ERROR-STYLE-GUIDE-TRICKY-WORDS)

**Impossível.** “Impossível” é quase a voz passiva. Use melhor “não pode” ou “não conseguiu”, conforme apropriado.

**Ruim.** Mensagens de erro como “resultado ruim” são realmente difíceis de interpretar de forma inteligente. É melhor escrever por que o resultado é “ruim”, por exemplo, “formato inválido”.

**Ilegal.** “Ilegal” significa uma violação da lei, o resto é “inválido”. Melhor ainda, diga por que é inválido.

**Desconhecido.** Tente evitar "desconhecido". Considere "erro: resposta desconhecida". Se você não sabe qual é a resposta, como saberá se ela é errada? "Não reconhecido" é muitas vezes uma escolha melhor. Além disso, certifique-se de incluir o valor que está sendo reclamado.

```
BAD:    unknown node type
BETTER: unrecognized node type: 42
```

**Encontrar vs. Existir.** Se o programa usa um algoritmo não trivial para localizar um recurso (por exemplo, uma busca de caminho) e esse algoritmo falha, é justo dizer que o programa não conseguiu “encontrar” o recurso. Por outro lado, se a localização esperada do recurso é conhecida, mas o programa não consegue acessá-lo lá, então diga que o recurso não “existe”. Usar “encontrar” nesse caso parece fraco e confunde o problema.

**May vs. Can vs. Might.** “May” sugere permissão (por exemplo, “Você pode emprestar meu raspa”), e tem pouca utilidade em documentação ou mensagens de erro. “Can” sugere habilidade (por exemplo, “Eu posso levantar aquele tronco”), e “might” sugere possibilidade (por exemplo, “Pode chover hoje.”). Usar a palavra correta esclarece o significado e auxilia na tradução.

**Contrações.** Evite as contrações, como “can't”; use “não pode” em vez disso.

**Não negativo.** Evite "não negativo", pois é ambíguo quanto ao fato de aceitar zero. É melhor usar "maior que zero" ou "maior que ou igual a zero".

### A Escrita Correta [#](#ERROR-STYLE-GUIDE-SPELLING)

Escreva as palavras na íntegra. Por exemplo, evite:

* espec
* estatísticas
* parenteses
* auth
* xact

Razão: Isso melhorará a consistência.

### Localização [#](#ERROR-STYLE-GUIDE-LOCALIZATION)

Tenha em mente que os textos das mensagens de erro precisam ser traduzidos para outros idiomas. Siga as diretrizes em [Seção 56.2.2](nls-programmer.md#NLS-GUIDELINES) para não dificultar a vida dos tradutores.