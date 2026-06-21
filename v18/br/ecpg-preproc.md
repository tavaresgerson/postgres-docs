## 34.9. Diretrizes do pré-processador [#](#ECPG-PREPROC)

* [34.9.1. Incluir arquivos][(ecpg-preproc.md#ECPG-INCLUDE)]
* [34.9.2. As diretivas define e undef][(ecpg-preproc.md#ECPG-DEFINE)]
* [34.9.3. as diretivas ifdef, ifndef, elif, else e endif][(ecpg-preproc.md#ECPG-IFDEF)]

Existem várias diretivas do pré-processador disponíveis que modificam a forma como o pré-processador `ecpg` analisa e processa um arquivo.

### 34.9.1. Incluir arquivos [#](#ECPG-INCLUDE)

Para incluir um arquivo externo em seu programa de SQL incorporado, use:

```
EXEC SQL INCLUDE filename;
EXEC SQL INCLUDE <filename>;
EXEC SQL INCLUDE "filename";
```

O pré-processador de SQL embutido procurará um arquivo chamado `filename.h`, o preprocessará e o incluirá na saída em C resultante. Assim, as declarações de SQL embutidas no arquivo incluído são tratadas corretamente.

O pré-processador `ecpg` procurará um arquivo em vários diretórios na seguinte ordem:

* diretório atual
* `/usr/local/include`
* diretório do PostgreSQL, definido no momento da construção (por exemplo, `/usr/local/pgsql/include`)
* `/usr/include`

Mas quando o `EXEC SQL INCLUDE "filename"` é usado, apenas o diretório atual é pesquisado.

Em cada diretório, o pré-processador primeiro procurará o nome do arquivo conforme especificado e, se não for encontrado, anexará `.h` ao nome do arquivo e tentará novamente (a menos que o nome de arquivo especificado já tenha esse sufixo).

Observe que `EXEC SQL INCLUDE` *não* é o mesmo que:

```
#include <filename.h>
```

porque esse arquivo não seria sujeito à pré-processamento de comandos SQL. Naturalmente, você pode continuar a usar a diretiva C `#include` para incluir outros arquivos de cabeçalho.

### Nota

O nome do arquivo do arquivo de inclusão é sensível ao caso, embora o resto do comando `EXEC SQL INCLUDE` siga as regras normais de sensibilidade ao caso do SQL.

### 34.9.2. As diretivas define e undef [#](#ECPG-DEFINE)

Semelhante à diretiva `#define` que é conhecida em C, a SQL embutida tem um conceito semelhante:

```
EXEC SQL DEFINE name;
EXEC SQL DEFINE name value;
```

Então você pode definir um nome:

```
EXEC SQL DEFINE HAVE_FEATURE;
```

E você também pode definir constantes:

```
EXEC SQL DEFINE MYNUMBER 12;
EXEC SQL DEFINE MYSTRING 'abc';
```

Use `undef` para remover uma definição anterior:

```
EXEC SQL UNDEF MYNUMBER;
```

Claro que você pode continuar a usar as versões C `#define` e `#undef` em seu programa de SQL embutido. A diferença é onde seus valores definidos são avaliados. Se você usar `EXEC SQL DEFINE`, o pré-processador `ecpg` avalia as definições e substitui os valores. Por exemplo, se você escreve:

```
EXEC SQL DEFINE MYNUMBER 12;
...
EXEC SQL UPDATE Tbl SET col = MYNUMBER;
```

então `ecpg` já fará a substituição e seu compilador C nunca verá nenhum nome ou identificador `MYNUMBER`. Note que você não pode usar `#define` para uma constante que você vai usar em uma consulta SQL embutida, porque, neste caso, o pré-compilador SQL embutido não é capaz de ver esta declaração.

Se vários arquivos de entrada forem nomeados na linha de comando do pré-processador `ecpg`, os efeitos de `EXEC SQL DEFINE` e `EXEC SQL UNDEF` não se estendem aos arquivos: cada arquivo começa apenas com os símbolos definidos pelos interruptores `-D` na linha de comando.

### 34.9.3. Diretivas ifdef, ifndef, elif, else e endif [#](#ECPG-IFDEF)

Você pode usar as seguintes diretivas para compilar seções de código condicionalmente:

`EXEC SQL ifdef name;` [#](#ECPG-IFDEF-IFDEF): Verifica um *`name`* e processa as linhas subsequentes se *`name`* foi definido via `EXEC SQL define name`.

`EXEC SQL ifndef name;` [#](#ECPG-IFDEF-IFNDEF): Verifica um *`name`* e processa as linhas subsequentes se *`name`* não tiver sido definido via `EXEC SQL define name`.

`EXEC SQL elif name;` [#](#ECPG-IFDEF-ELIF): Começa uma seção alternativa opcional após uma diretiva `EXEC SQL ifdef name` ou `EXEC SQL ifndef name`. Pode aparecer qualquer número de seções `elif`. As linhas que seguem uma `elif` serão processadas se *`name`* tiver sido definido *e* nenhuma seção anterior do mesmo `ifdef`/`ifndef`...`endif` foi processada.

`EXEC SQL else;` [#](#ECPG-IFDEF-ELSE): Começa uma seção alternativa opcional final após uma diretiva `EXEC SQL ifdef name` ou `EXEC SQL ifndef name`. As linhas subsequentes serão processadas se nenhuma seção anterior do mesmo `ifdef`/`ifndef`...`endif` foi processada.

`EXEC SQL endif;` [#](#ECPG-IFDEF-ENDIF): Finaliza um `ifdef`/`ifndef`...`endif` construído. As linhas subsequentes são processadas normalmente.

Os `ifdef`/`ifndef`...`endif` podem ser aninhados, até 127 níveis de profundidade.

Este exemplo compilará exatamente um dos três comandos `SET TIMEZONE`:

```
EXEC SQL ifdef TZVAR;
EXEC SQL SET TIMEZONE TO TZVAR;
EXEC SQL elif TZNAME;
EXEC SQL SET TIMEZONE TO TZNAME;
EXEC SQL else;
EXEC SQL SET TIMEZONE TO 'GMT';
EXEC SQL endif;
```
