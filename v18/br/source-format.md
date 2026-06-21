## 55.1. Formatação [#](#SOURCE-FORMAT)

O formato do código-fonte utiliza espaçamento de tabulação de 4 colunas, com tabulações preservadas (ou seja, as tabulações não são expandidas para espaços). Cada nível de indentação lógica é um espaço de parada de tabulação adicional.

As regras de disposição (posicionamento de travessas, etc.) seguem as convenções BSD. Em particular, as chaves espirais para os blocos controlados de `if`, `while`, `switch`, etc. vão em suas próprias linhas.

Limite o comprimento das linhas do código para que ele seja legível em uma janela de 80 colunas. (Isso não significa que você não pode ir além de 80 colunas. Por exemplo, quebrar uma longa string de mensagem de erro em lugares arbitrários apenas para manter o código dentro de 80 colunas provavelmente não é uma vantagem na legibilidade.)

Para manter um estilo de codificação consistente, não use comentários no estilo C++ (comentários `//`). O pgindent os substituirá por `/* ... */`.

O estilo preferido para blocos de comentário de várias linhas é

```
/*
 * comment text begins here
 * and continues here
 */
```

Observe que os blocos de comentário que começam na coluna 1 serão preservados como estão pelo pgindent, mas ele reestruturará os blocos de comentário indenizados como se fossem texto simples. Se você deseja preservar as quebra de linha em um bloco indenizado, adicione traços assim:

```
    /*----------
     * comment text begins here
     * and continues here
     *----------
     */
```

Embora os patches enviados não precisem necessariamente seguir essas regras de formatação, é uma boa ideia fazê-lo. Seu código será executado pelo pgindent antes da próxima versão, então não faz sentido deixá-lo bonito sob algum outro conjunto de convenções de formatação. Uma boa regra geral para patches é “fazer o novo código parecer como o código existente ao seu redor”.

O diretório `src/tools/editors` contém arquivos de configuração de exemplo que podem ser usados com os editores Emacs, xemacs ou vim para ajudar a garantir que eles formatem o código de acordo com essas convenções.

Se você deseja executar o pgindent localmente para ajudar a alinhar seu código com o estilo do projeto, consulte o diretório `src/tools/pgindent`.

As ferramentas de navegação de texto podem ser invocadas cada vez menos como:

```
more -x4
less -x4
```

para que eles mostrem as abas corretamente.