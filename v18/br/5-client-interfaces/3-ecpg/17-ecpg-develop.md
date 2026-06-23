## 34.17. Internos [#](#ECPG-DEVELOP)

Esta seção explica como o ECPG funciona internamente. Essa informação pode ser útil ocasionalmente para ajudar os usuários a entender como usar o ECPG.

As quatro primeiras linhas escritas por `ecpg` na saída são linhas fixas. Duas são comentários e duas são linhas de inclusão necessárias para a interface com a biblioteca. Em seguida, o pré-processador lê o arquivo e escreve a saída. Normalmente, ele apenas ecoa tudo na saída.

Quando ele vê uma declaração `EXEC SQL`, ele intervém e a altera. O comando começa com `EXEC SQL` e termina com `;`. Tudo o que está entre eles é tratado como uma declaração SQL e analisado para substituição de variáveis.

A substituição variável ocorre quando um símbolo começa com um colon (`:`). A variável com esse nome é procurada entre as variáveis que foram previamente declaradas dentro de uma seção `EXEC SQL DECLARE`.

A função mais importante da biblioteca é `ECPGdo`, que cuida da execução da maioria dos comandos. Ela aceita um número variável de argumentos. Isso pode facilmente chegar a 50 ou mais argumentos, e esperamos que isso não seja um problema em nenhuma plataforma.

Os argumentos são:

Um número de linha [#](#ECPG-DEVELOP-LINE-NUMBER): Este é o número de linha do texto original; utilizado apenas em mensagens de erro.

Uma cadeia [#](#ECPG-DEVELOP-STRING): Este é o comando SQL que deve ser emitido. Ele é modificado pelas variáveis de entrada, ou seja, as variáveis que não eram conhecidas no momento da compilação, mas devem ser inseridas no comando. Onde as variáveis devem ir, a cadeia contém `?`.

Variáveis de entrada [#](#ECPG-DEVELOP-INPUT-VARIABLES): Cada variável de entrada gera a criação de dez argumentos. (Veja abaixo.)

*`ECPGt_EOIT`* [#](#ECPG-DEVELOP-ECPGT-EOIT): Uma `enum` informando que não há mais variáveis de entrada.

Variáveis de saída [#](#ECPG-DEVELOP-OUTPUT-VARIABLES): Cada variável de saída gera a criação de dez argumentos. (Veja abaixo.) Essas variáveis são preenchidas pela função.

*`ECPGt_EORT`* [#](#ECPG-DEVELOP-ECPGT-EORT): Uma `enum` que indica que não há mais variáveis.

Para cada variável que faz parte do comando SQL, a função recebe dez argumentos:

1. O tipo como um símbolo especial.
2. Um ponteiro para o valor ou um ponteiro para o ponteiro.
3. O tamanho da variável, se for um `char` ou `varchar`.
4. O número de elementos na matriz (para fetches de matriz).
5. O deslocamento para o próximo elemento na matriz (para fetches de matriz).
6. O tipo da variável de indicador como um símbolo especial.
7. Um ponteiro para a variável de indicador.
8. 0
9. O número de elementos na matriz de indicador (para fetches de matriz).
10. O deslocamento para o próximo elemento na matriz de indicador (para fetches de matriz).

Observe que nem todos os comandos SQL são tratados dessa maneira. Por exemplo, uma declaração de cursor aberto como:

```
EXEC SQL OPEN cursor;
```

não é copiada para a saída. Em vez disso, o comando `DECLARE` do cursor é usado na posição do comando `OPEN`, porque ele realmente abre o cursor.

Aqui está um exemplo completo que descreve a saída do pré-processador de um arquivo `foo.pgc` (os detalhes podem mudar com cada versão específica do pré-processador):

```
EXEC SQL BEGIN DECLARE SECTION;
int index;
int result;
EXEC SQL END DECLARE SECTION;
...
EXEC SQL SELECT res INTO :result FROM mytable WHERE index = :index;
```

é traduzido em:

```
/* Processed by ecpg (2.6.0) */
/* These two include files are added by the preprocessor */
#include <ecpgtype.h>;
#include <ecpglib.h>;

/* exec sql begin declare section */

#line 1 "foo.pgc"

 int index;
 int result;
/* exec sql end declare section */
...
ECPGdo(__LINE__, NULL, "SELECT res FROM mytable WHERE index = ?     ",
        ECPGt_int,&(index),1L,1L,sizeof(int),
        ECPGt_NO_INDICATOR, NULL , 0L, 0L, 0L, ECPGt_EOIT,
        ECPGt_int,&(result),1L,1L,sizeof(int),
        ECPGt_NO_INDICATOR, NULL , 0L, 0L, 0L, ECPGt_EORT);
#line 147 "foo.pgc"
```

(A indentação aqui é adicionada para legibilidade e não é algo que o pré-processador faça.)