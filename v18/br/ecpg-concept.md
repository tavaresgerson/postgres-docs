## 34.1. O Conceito [#](#ECPG-CONCEPT)

Um programa de SQL embutido consiste em código escrito em uma linguagem de programação comum, neste caso C, misturado com comandos SQL em seções especificamente marcadas. Para construir o programa, o código-fonte (`*.pgc`) é primeiro passado pelo pré-processador de SQL embutido, que o converte em um programa comum em C (`*.c`), e, posteriormente, pode ser processado por um compilador C. (Para detalhes sobre a compilação e vinculação, consulte [Seção 34.10][(ecpg-process.md "34.10. Processing Embedded SQL Programs")]. Conforme convertido, as aplicações ECPG chamam funções na biblioteca libpq através da biblioteca de SQL embutida (ecpglib) e comunicam-se com o servidor PostgreSQL usando o protocolo normal de frontend-backend.

O SQL embutido tem vantagens em relação a outros métodos para manipulação de comandos SQL a partir do código C. Primeiro, ele cuida da tediosa passagem de informações para e a partir de variáveis em seu programa C. Segundo, o código SQL no programa é verificado no momento da construção para correção sintática. Terceiro, o SQL embutido em C é especificado no padrão SQL e é suportado por muitos outros sistemas de banco de dados SQL. A implementação do PostgreSQL é projetada para corresponder a este padrão tanto quanto possível, e geralmente é possível portar programas de SQL embutido escritos para outros bancos de dados SQL para o PostgreSQL com relativa facilidade.

Como já mencionado, os programas escritos para a interface SQL embutida são programas normais em C com código especial inserido para realizar ações relacionadas ao banco de dados. Esse código especial sempre tem a forma:

```
EXEC SQL ...;
```

Essas declarações ocupam o lugar de uma declaração C. Dependendo da declaração específica, elas podem aparecer no nível global ou dentro de uma função.

As instruções SQL embutidas seguem as regras de sensibilidade de caso do código SQL normal e não as do C. Além disso, permitem comentários aninhados no estilo C, conforme o padrão SQL. A parte C do programa, no entanto, segue o padrão C de não aceitar comentários aninhados. As instruções SQL embutidas também usam regras SQL, não regras de C, para análise de strings e identificadores com citação. (Veja [Seção 4.1.2.1] e [Seção 4.1.1], respectivamente. Note que o ECPG assume que `standard_conforming_strings` é `on`.). Claro, a parte C do programa segue as regras de citação de C.

As seções a seguir explicam todas as instruções SQL embutidas.