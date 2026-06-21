## 32.22. Construção de programas libpq [#](#LIBPQ-BUILD)

Para construir (ou seja, compilar e vincular) um programa usando o libpq, você precisa fazer todas as seguintes coisas:

* Inclua o arquivo de cabeçalho `libpq-fe.h`:

  ```
  #include <libpq-fe.h>
  ```

Se você não tiver feito isso, normalmente receberá mensagens de erro do seu compilador, semelhantes às seguintes:

* Indique ao seu compilador o diretório onde os arquivos de cabeçalho do PostgreSQL foram instalados, fornecendo a opção `-Idirectory` ao seu compilador. (Em alguns casos, o compilador analisará o diretório em questão por padrão, então você pode omitir essa opção. Por exemplo, sua linha de comando de compilação pode parecer assim:

  ```
  cc -c -I/usr/local/pgsql/include testprog.c
  ```

Se você está usando makefiles, adicione a opção à variável `CPPFLAGS`:

  ```
  CPPFLAGS += -I/usr/local/pgsql/include
  ```

Se houver alguma possibilidade de que seu programa possa ser compilado por outros usuários, você não deve codificar a localização do diretório dessa forma. Em vez disso, você pode executar o utilitário `pg_config` para descobrir onde os arquivos de cabeçalho estão no sistema local:

  ```
  $ pg_config --includedir
  /usr/local/include
  ```

Se você tiver `pkg-config` instalado, pode executar em vez disso:

  ```
  $ pkg-config --cflags libpq
  -I/usr/local/include
  ```

Observe que isso já incluirá o `-I` na frente do caminho.

A falha em especificar a opção correta ao compilador resultará em uma mensagem de erro, como:

* Ao vincular o programa final, especifique a opção `-lpq` para que a biblioteca libpq seja puxada, bem como a opção `-Ldirectory` para apontar o compilador para o diretório onde reside a biblioteca libpq. (Novamente, o compilador buscará alguns diretórios por padrão.) Para máxima portabilidade, coloque a opção `-L` antes da opção `-lpq`. Por exemplo:

  ```
  cc -o testprog testprog1.o testprog2.o -L/usr/local/pgsql/lib -lpq
  ```

Você pode descobrir o diretório da biblioteca usando `pg_config` também:

  ```
  $ pg_config --libdir
  /usr/local/pgsql/lib
  ```

Ou, novamente, use `pkg-config`:

  ```
  $ pkg-config --libs libpq
  -L/usr/local/pgsql/lib -lpq
  ```

Observe novamente que isso imprime todas as opções, não apenas o caminho.

Mensagens de erro que apontam para problemas nessa área podem parecer as seguintes:

  ```
  testlibpq.o: In function `main':
  testlibpq.o(.text+0x60): undefined reference to `PQsetdbLogin'
  testlibpq.o(.text+0x71): undefined reference to `PQstatus'
  testlibpq.o(.text+0xa4): undefined reference to `PQerrorMessage'
  ```

Isso significa que você esqueceu `-lpq`.

  ```
  /usr/bin/ld: cannot find -lpq
  ```

Isso significa que você esqueceu a opção `-L` ou não especificou o diretório correto.