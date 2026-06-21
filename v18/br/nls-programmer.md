## 56.2. Para o Programador [#](#NLS-PROGRAMMER)

* [56.2.1. Mecânica](nls-programmer.md#NLS-MECHANICS)
* [56.2.2. Diretrizes de Escrita de Mensagens](nls-programmer.md#NLS-GUIDELINES)

### 56.2.1. Mecânica [#](#NLS-MECHANICS)

Esta seção descreve como implementar suporte para idiomas nativos em um programa ou biblioteca que faz parte da distribuição do PostgreSQL. Atualmente, isso se aplica apenas a programas em C.

**Adicionando suporte NLS a um programa**

1. Insira este código na sequência de inicialização do programa:

```
#ifdef ENABLE_NLS
#include <locale.h>
#endif

...

#ifdef ENABLE_NLS
setlocale(LC_ALL, "");
bindtextdomain("progname", LOCALEDIR);
textdomain("progname");
#endif
```

(O *`progname`* pode ser escolhido livremente.)
2. Em qualquer lugar onde é encontrada uma mensagem que é candidata a tradução, é necessário inserir uma chamada para `gettext()`. Exemplo:

```
fprintf(stderr, "panic level %d\n", lvl);
```

seriam alterados para:

```
fprintf(stderr, gettext("panic level %d\n"), lvl);
```

(`gettext` é definido como uma operação não invasiva se o suporte NLS não for configurado.)

Isso tende a adicionar muita confusão. Um atalho comum é usar:

```
#define _(x) gettext(x)
```

Outra solução é viável se o programa fizer grande parte de sua comunicação através de uma ou algumas funções, como `ereport()` no backend. Então, você faz essa chamada de função `gettext` internamente em todas as strings de entrada.
3. Adicione um arquivo `nls.mk` no diretório com as fontes do programa. Este arquivo será lido como um makefile. As seguintes atribuições de variáveis precisam ser feitas aqui:

`CATALOG_NAME` :   O nome do programa, conforme fornecido na chamada `textdomain()`.

`GETTEXT_FILES` :   Lista de arquivos que contêm strings traduzíveis, ou seja, aqueles marcados com `gettext` ou uma solução alternativa. Eventualmente, isso incluirá quase todos os arquivos de origem do programa. Se essa lista ficar muito longa, você pode fazer o primeiro "arquivo" ser um `+` e a segunda palavra ser um arquivo que contém um nome de arquivo por linha.

`GETTEXT_TRIGGERS` :   As ferramentas que geram catálogos de mensagens para os tradutores trabalharem precisam saber quais chamadas de função contêm strings traduzíveis. Por padrão, apenas as chamadas `gettext()` são conhecidas. Se você usou `_` ou outros identificadores, você precisa listá-los aqui. Se a string traduzível não for o primeiro argumento, o item precisa ter a forma `func:2` (para o segundo argumento). Se você tem uma função que suporta mensagens pluralizadas, o item deve parecer como `func:1,2` (identificando os argumentos de mensagem singular e plural). 4. Adicione um arquivo `po/LINGUAS`, que conterá a lista de traduções fornecidas — inicialmente vazia.

O sistema de construção cuidará automaticamente da construção e instalação dos catálogos de mensagens.

### 56.2.2. Diretrizes para a escrita de mensagens [#](#NLS-GUIDELINES)

Aqui estão algumas diretrizes para escrever mensagens que são facilmente traduzíveis.

* Não construa frases em tempo de execução, como:

```
printf("Files were %s.\n", flag ? "copied" : "removed");
```

A ordem das palavras na frase pode ser diferente em outras línguas. Além disso, mesmo que você se lembre de chamar `gettext()` em cada fragmento, os fragmentos podem não se traduzir bem separadamente. É melhor duplicar um pouco de código para que cada mensagem a ser traduzida seja um todo coerente. Apenas números, nomes de arquivos e variáveis de tempo de execução semelhantes devem ser inseridos em tempo de execução em um texto de mensagem. * Por razões semelhantes, isso não funcionará:

```
printf("copied %d file%s", n, n!=1 ? "s" : "");
```

porque ele assume como o plural é formado. Se você pensou que poderia resolvê-lo assim:

```
if (n==1)
    printf("copied 1 file");
else
    printf("copied %d files", n):
```

Então, você ficará decepcionado. Algumas línguas têm mais de duas formas, com algumas regras peculiares. É frequentemente melhor projetar a mensagem para evitar o problema completamente, por exemplo, assim:

```
printf("number of copied files: %d", n);
```

Se você realmente deseja construir uma mensagem pluralizada corretamente, há suporte para isso, mas é um pouco estranho. Ao gerar uma mensagem de erro primária ou detalhada em `ereport()`, você pode escrever algo assim:

```
errmsg_plural("copied %d file",
              "copied %d files",
              n,
              n)
```

O primeiro argumento é a string de formato apropriada para a forma singular em inglês, o segundo é a string de formato apropriada para a forma plural em inglês, e o terceiro é o valor de controle inteiro que determina qual forma plural usar. Os argumentos subsequentes são formatados conforme a string de formato, como de costume. (Normalmente, o valor de controle de pluralização também será um dos valores a serem formatados, então ele tem que ser escrito duas vezes.) Em inglês, só importa se *`n`* é 1 ou não é 1, mas em outras línguas pode haver muitas formas plurrais diferentes. O tradutor vê as duas formas em inglês como um grupo e tem a oportunidade de fornecer várias strings de substituição, com a apropriada sendo selecionada com base no valor de tempo de execução de *`n`*.

Se você precisar pluralizar uma mensagem que não está indo diretamente para um relatório `errmsg` ou `errdetail`, você tem que usar a função subjacente `ngettext`. Veja a documentação do gettext.
* Se você quiser comunicar algo ao tradutor, como sobre como uma mensagem está destinada a se alinhar com outra saída, antecipe a ocorrência da string com um comentário que comece com `translator`, por exemplo:

```
/* translator: This message is not what it seems to be. */
```

Esses comentários são copiados para os arquivos do catálogo de mensagens para que os tradutores possam vê-los.