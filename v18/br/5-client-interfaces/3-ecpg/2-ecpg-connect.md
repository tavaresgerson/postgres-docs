## 34.2. Gerenciamento de Conexões de Banco de Dados [#](#ECPG-CONNECT)

* [34.2.1. Conectando ao servidor de banco de dados](ecpg-connect.md#ECPG-CONNECTING)
* [34.2.2. Escolhendo uma conexão](ecpg-connect.md#ECPG-SET-CONNECTION)
* [34.2.3. Fechar uma conexão](ecpg-connect.md#ECPG-DISCONNECT)

Esta seção descreve como abrir, fechar e alternar conexões de banco de dados.

### 34.2.1. Conectar ao servidor de banco de dados [#](#ECPG-CONNECTING)

Um se conecta a um banco de dados usando a seguinte declaração:

```
EXEC SQL CONNECT TO target [AS connection-name] [USER user-name];
```

O *`target`* pode ser especificado das seguintes maneiras:

* `dbname[@hostname][:port]`
* `tcp:postgresql://hostname[:port][/dbname][?options]`
* `unix:postgresql://localhost[:port][/dbname][?options]`
* uma literal de string SQL contendo uma das formas acima
* uma referência a uma variável de caractere contendo uma das formas acima (ver exemplos)
* `DEFAULT`

O alvo de conexão `DEFAULT` inicia uma conexão com o banco de dados padrão sob o nome de usuário padrão. Nesse caso, não é possível especificar um nome de usuário ou nome de conexão separado.

Se você especificar o alvo da conexão diretamente (ou seja, não como uma literal de string ou referência de variável), então os componentes do alvo são passados através da análise SQL normal; isso significa que, por exemplo, o *`hostname`* deve parecer um ou mais identificadores SQL separados por pontos, e esses identificadores serão maiúsculos a menos que sejam citados em duplicado. Os valores de qualquer *`options`* devem ser identificadores SQL, inteiros ou referências de variáveis. Claro, você pode colocar quase qualquer coisa em um identificador SQL citando-a em duplicado. Na prática, provavelmente é menos propenso a erros usar uma literal de string (com uma única citação) ou uma referência de variável do que escrever o alvo da conexão diretamente.

Há também diferentes maneiras de especificar o nome do usuário:

* `username`
* `username/password`
* `username IDENTIFIED BY password`
* `username USING password`

Como acima, os parâmetros *`username`* e *`password`* podem ser um identificador SQL, uma literal de string SQL ou uma referência a uma variável de caracteres.

Se o alvo da conexão incluir qualquer *`options`*, esses consistem em especificações de `keyword=value` separadas por e (`&`). As palavras-chave permitidas são as mesmas reconhecidas pelo libpq (veja [Seção 32.1.2](libpq-connect.md#LIBPQ-PARAMKEYWORDS "32.1.2. Parameter Key Words")). Espaços são ignorados antes de qualquer *`keyword`* ou *`value`*, embora não dentro ou após um. Note que não é possível escrever `&` dentro de um *`value`*.

Observe que, ao especificar uma conexão de soquete (com o prefixo `unix:`, o nome do host deve ser exatamente `localhost`. Para selecionar um diretório de soquete não padrão, escreva o caminho do diretório como o valor de uma opção `host` na parte *`options`* do alvo.

O *`connection-name` é usado para lidar com múltiplas conexões em um único programa. Ele pode ser omitido se um programa utilizar apenas uma conexão. A conexão mais recentemente aberta se torna a conexão atual, que é usada por padrão quando uma declaração SQL deve ser executada (veja mais adiante neste capítulo).

Aqui estão alguns exemplos de declarações `CONNECT`:

```
EXEC SQL CONNECT TO mydb@sql.mydomain.com;

EXEC SQL CONNECT TO tcp:postgresql://sql.mydomain.com/mydb AS myconnection USER john;

EXEC SQL BEGIN DECLARE SECTION;
const char *target = "mydb@sql.mydomain.com";
const char *user = "john";
const char *passwd = "secret";
EXEC SQL END DECLARE SECTION;
 ...
EXEC SQL CONNECT TO :target USER :user USING :passwd;
/* or EXEC SQL CONNECT TO :target USER :user/:passwd; */
```

O último exemplo utiliza a característica mencionada acima como referências de variáveis de caracteres. Você verá em seções posteriores como as variáveis C podem ser usadas em declarações SQL quando você as prefixa com um colon.

Por favor, note que o formato do alvo de conexão não é especificado no padrão SQL. Portanto, se você deseja desenvolver aplicativos portáteis, talvez queira usar algo baseado no último exemplo acima para encapsular a string do alvo de conexão em algum lugar.

Se usuários não confiáveis tiverem acesso a um banco de dados que não adotou um padrão de uso de esquema seguro (ddl-schemas.md#DDL-SCHEMAS-PATTERNS "5.10.6. Usage Patterns"), comece cada sessão removendo esquemas que podem ser escritos publicamente de `search_path`. Por exemplo, adicione `options=-c search_path=` a `options`, ou emita `EXEC SQL SELECT pg_catalog.set_config('search_path', '', false);` após a conexão. Esta consideração não é específica do ECPG; ela se aplica a todas as interfaces para executar comandos SQL arbitrários.

### 34.2.2. Escolhendo uma conexão [#](#ECPG-SET-CONNECTION)

As instruções SQL em programas de SQL embutido são, por padrão, executadas na conexão atual, ou seja, na mais recentemente aberta. Se uma aplicação precisar gerenciar múltiplas conexões, existem três maneiras de lidar com isso.

A primeira opção é escolher explicitamente uma conexão para cada declaração SQL, por exemplo:

```
EXEC SQL AT connection-name SELECT ...;
```

Essa opção é particularmente adequada se a aplicação precisar usar várias conexões em ordem mista.

Se sua aplicação usa múltiplos threads de execução, eles não podem compartilhar uma conexão simultaneamente. Você deve controlar explicitamente o acesso à conexão (usando mutantes) ou usar uma conexão para cada thread.

A segunda opção é executar uma declaração para alternar a conexão atual. Essa declaração é:

```
EXEC SQL SET CONNECTION connection-name;
```

Essa opção é particularmente conveniente se muitas declarações devem ser executadas na mesma conexão.

Aqui está um exemplo de programa que gerencia múltiplas conexões de banco de dados:

```
#include <stdio.h>

EXEC SQL BEGIN DECLARE SECTION;
    char dbname[1024];
EXEC SQL END DECLARE SECTION;

int
main()
{
    EXEC SQL CONNECT TO testdb1 AS con1 USER testuser;
    EXEC SQL SELECT pg_catalog.set_config('search_path', '', false); EXEC SQL COMMIT;
    EXEC SQL CONNECT TO testdb2 AS con2 USER testuser;
    EXEC SQL SELECT pg_catalog.set_config('search_path', '', false); EXEC SQL COMMIT;
    EXEC SQL CONNECT TO testdb3 AS con3 USER testuser;
    EXEC SQL SELECT pg_catalog.set_config('search_path', '', false); EXEC SQL COMMIT;

    /* This query would be executed in the last opened database "testdb3". */
    EXEC SQL SELECT current_database() INTO :dbname;
    printf("current=%s (should be testdb3)\n", dbname);

    /* Using "AT" to run a query in "testdb2" */
    EXEC SQL AT con2 SELECT current_database() INTO :dbname;
    printf("current=%s (should be testdb2)\n", dbname);

    /* Switch the current connection to "testdb1". */
    EXEC SQL SET CONNECTION con1;

    EXEC SQL SELECT current_database() INTO :dbname;
    printf("current=%s (should be testdb1)\n", dbname);

    EXEC SQL DISCONNECT ALL;
    return 0;
}
```

Esse exemplo produziria essa saída:

```
current=testdb3 (should be testdb3)
current=testdb2 (should be testdb2)
current=testdb1 (should be testdb1)
```

A terceira opção é declarar um identificador SQL vinculado à conexão, por exemplo:

```
EXEC SQL AT connection-name DECLARE statement-name STATEMENT;
EXEC SQL PREPARE statement-name FROM :dyn-string;
```

Uma vez que você vincule um identificador SQL a uma conexão, execute SQL dinâmico sem uma cláusula AT. Observe que essa opção se comporta como diretivas de pré-processador, portanto, o link é habilitado apenas no arquivo.

Aqui está um exemplo de programa que usa essa opção:

```
#include <stdio.h>

EXEC SQL BEGIN DECLARE SECTION;
char dbname[128];
char *dyn_sql = "SELECT current_database()";
EXEC SQL END DECLARE SECTION;

int main(){
  EXEC SQL CONNECT TO postgres AS con1;
  EXEC SQL CONNECT TO testdb AS con2;
  EXEC SQL AT con1 DECLARE stmt STATEMENT;
  EXEC SQL PREPARE stmt FROM :dyn_sql;
  EXEC SQL EXECUTE stmt INTO :dbname;
  printf("%s\n", dbname);

  EXEC SQL DISCONNECT ALL;
  return 0;
}
```

Esse exemplo produziria essa saída, mesmo que a conexão padrão seja testdb:

```
postgres
```

### 34.2.3. Fechar uma conexão [#](#ECPG-DISCONNECT)

Para fechar uma conexão, use a seguinte declaração:

```
EXEC SQL DISCONNECT [connection];
```

O *`connection`* pode ser especificado das seguintes maneiras:

* `connection-name`
* `CURRENT`
* `ALL`

Se não for especificado um nome de conexão, a conexão atual é fechada.

É bom estilo que um aplicativo sempre se desconecte explicitamente de todas as conexões que abriu.