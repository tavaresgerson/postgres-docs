## 36.18. Edifício de extensão de infraestrutura [#](#EXTEND-PGXS)

Se você está pensando em distribuir seus módulos de extensão do PostgreSQL, configurar um sistema de compilação portátil para eles pode ser bastante difícil. Portanto, a instalação do PostgreSQL fornece uma infraestrutura de compilação para extensões, chamada PGXS, para que módulos de extensão simples possam ser compilados simplesmente contra um servidor já instalado. O PGXS é principalmente destinado a extensões que incluem código C, embora possa ser usado para extensões SQL puras também. Note que o PGXS não é destinado a ser um sistema de construção universal que pode ser usado para construir qualquer software que interaja com o PostgreSQL; ele simplesmente automatiza as regras de compilação comuns para módulos de extensão de servidor simples. Para pacotes mais complicados, você pode precisar escrever seu próprio sistema de construção.

Para usar a infraestrutura PGXS para sua extensão, você deve escrever um simples makefile. No makefile, você precisa definir algumas variáveis e incluir o makefile global PGXS. Aqui está um exemplo que constrói um módulo de extensão chamado `isbn_issn`, composto por uma biblioteca compartilhada contendo algum código C, um arquivo de controle de extensão, um script SQL, um arquivo de inclusão (necessário apenas se outros módulos possam precisar acessar as funções da extensão sem passar pelo SQL) e um arquivo de texto de documentação:

```
MODULES = isbn_issn
EXTENSION = isbn_issn
DATA = isbn_issn--1.0.sql
DOCS = README.isbn_issn
HEADERS_isbn_issn = isbn_issn.h

PG_CONFIG = pg_config
PGXS := $(shell $(PG_CONFIG) --pgxs)
include $(PGXS)
```

As três últimas linhas devem ser sempre as mesmas. Mais cedo no arquivo, você atribui variáveis ou adiciona regras de fazer personalizadas.

Defina uma dessas três variáveis para especificar o que é construído:

`MODULES` [#](#EXTEND-PGXS-MODULES): lista de objetos de biblioteca compartilhada a serem construídos a partir de arquivos de fonte com o mesmo tronco (não inclua sufixos de biblioteca nesta lista)

`MODULE_big` [#](#EXTEND-PGXS-MODULE-BIG): uma biblioteca compartilhada para ser construída a partir de vários arquivos de origem (liste os arquivos de objeto em `OBJS`)

`PROGRAM` [#](#EXTEND-PGXS-PROGRAM): um programa executável para construir (lista arquivos de objeto em `OBJS`)

As seguintes variáveis também podem ser definidas:

`EXTENSION` [#](#EXTEND-PGXS-EXTENSION): nome(s) do(s) extensão(ões); para cada nome, você deve fornecer um arquivo `extension.control`, que será instalado em `prefix/share/extension`

`MODULEDIR` [#](#EXTEND-PGXS-MODULEDIR): subdiretório de `prefix/share` no qual os arquivos DATA e DOCS devem ser instalados (se não definido, o padrão é `extension` se `EXTENSION` estiver definido, ou `contrib` se não estiver)

`DATA` [#](#EXTEND-PGXS-DATA): arquivos aleatórios para instalar no `prefix/share/$MODULEDIR`

`DATA_built` [#](#EXTEND-PGXS-DATA-BUILT): arquivos aleatórios para instalar no `prefix/share/$MODULEDIR`, que precisam ser compilados primeiro

`DATA_TSEARCH` [#](#EXTEND-PGXS-DATA-TSEARCH): arquivos aleatórios para instalar sob `prefix/share/tsearch_data`

`DOCS` [#](#EXTEND-PGXS-DOCS): arquivos aleatórios para instalar sob `prefix/doc/$MODULEDIR`

`HEADERS` `HEADERS_built` [#](#EXTEND-PGXS-HEADERS): Arquivos para (opcionalmente construir e) instalar em `prefix/include/server/$MODULEDIR/$MODULE_big`.

Ao contrário de `DATA_built`, os arquivos em `HEADERS_built` não são removidos pelo alvo [[`clean`]; se você deseja que eles sejam removidos, também adicione-os a `EXTRA_CLEAN` ou adicione suas próprias regras para fazer isso.

`HEADERS_$MODULE` `HEADERS_built_$MODULE` [#](#EXTEND-PGXS-HEADERS-MODULE): Arquivos para instalação (após a construção, se especificado) em `prefix/include/server/$MODULEDIR/$MODULE`, onde `$MODULE` deve ser um nome de módulo usado em `MODULES` ou `MODULE_big`.

Ao contrário de `DATA_built`, os arquivos em `HEADERS_built_$MODULE` não são removidos pelo alvo `clean`; se você deseja que eles sejam removidos, também adicione-os a `EXTRA_CLEAN` ou adicione suas próprias regras para fazer isso.

É legal usar ambas as variáveis para o mesmo módulo, ou qualquer combinação, a menos que você tenha dois nomes de módulo na lista `MODULES` que diferem apenas pela presença de um prefixo `built_`, o que causaria ambiguidade. Nesse caso (espera-se que improvável), você deve usar apenas as variáveis `HEADERS_built_$MODULE`.

`SCRIPTS` [#](#EXTEND-PGXS-SCRIPTS): arquivos de script (não binários) para instalar no `prefix/bin`

`SCRIPTS_built` [#](#EXTEND-PGXS-SCRIPTS-BUILT): arquivos de script (não binários) para instalar no `prefix/bin`, que precisam ser compilados primeiro

`REGRESS` [#](#EXTEND-PGXS-REGRESS): lista de casos de testes de regressão (sem sufixo), veja abaixo

`REGRESS_OPTS` [#](#EXTEND-PGXS-REGRESS-OPTS): interruptores adicionais para passar ao pg_regress

`ISOLATION` [#](#EXTEND-PGXS-ISOLATION): lista de casos de teste de isolamento, consulte abaixo para mais detalhes

`ISOLATION_OPTS` [#](#EXTEND-PGXS-ISOLATION-OPTS): interruptores adicionais para passar ao pg_isolation_regress

`TAP_TESTS` [#](#EXTEND-PGXS-TAP-TESTS): interruptor que define se os testes TAP precisam ser executados, veja abaixo

`NO_INSTALL` [#](#EXTEND-PGXS-NO-INSTALL): não defina um alvo `install`, útil para módulos de teste que não precisam que seus produtos de construção sejam instalados

`NO_INSTALLCHECK` [#](#EXTEND-PGXS-NO-INSTALLCHECK): não defina um alvo `installcheck`, útil, por exemplo, se os testes exigem configuração especial, ou não use o pg_regress

`EXTRA_CLEAN` [#](#EXTEND-PGXS-EXTRA-CLEAN): arquivos extras a serem removidos em `make clean`

`PG_CPPFLAGS` [#](#EXTEND-PGXS-PG-CPPFLAGS): será prependido a `CPPFLAGS`

`PG_CFLAGS` [#](#EXTEND-PGXS-PG-CFLAGS): será anexado a `CFLAGS`

`PG_CXXFLAGS` [#](#EXTEND-PGXS-PG-CXXFLAGS): será anexado a `CXXFLAGS`

`PG_LDFLAGS` [#](#EXTEND-PGXS-PG-LDFLAGS): será prependido a `LDFLAGS`

`PG_LIBS` [#](#EXTEND-PGXS-PG-LIBS): será adicionada à linha de link `PROGRAM`

`SHLIB_LINK` [#](#EXTEND-PGXS-SHLIB-LINK): será adicionado à linha de link `MODULE_big`

`PG_CONFIG` [#](#EXTEND-PGXS-PG-CONFIG): caminho para o programa pg_config para a instalação do PostgreSQL a ser utilizado (normalmente apenas `pg_config` para usar o primeiro no seu `PATH`)

Coloque este makefile como `Makefile` no diretório que contém sua extensão. Em seguida, você pode fazer `make` para compilar e, em seguida, `make install` para instalar seu módulo. Por padrão, a extensão é compilada e instalada para a instalação do PostgreSQL que corresponde ao primeiro programa `pg_config` encontrado em seu `PATH`. Você pode usar uma instalação diferente, definindo `PG_CONFIG` para apontar para seu programa `pg_config`, seja dentro do makefile ou na linha de comando `make`.

Você pode selecionar um prefixo de diretório separado para instalar os arquivos de sua extensão, definindo a variável `make` `prefix` ao executar `make install` da seguinte forma:

```
make install prefix=/usr/local/postgresql
```

Isso instalará o controle de extensão e os arquivos SQL em `/usr/local/postgresql/share` e os módulos compartilhados em `/usr/local/postgresql/lib`. Se o prefixo não incluir as strings `postgres` ou `pgsql`, como

```
make install prefix=/usr/local/extras
```

então `postgresql` será anexado aos nomes dos diretórios, instalando os arquivos de controle e SQL em `/usr/local/extras/share/postgresql/extension` e os módulos compartilhados em `/usr/local/extras/lib/postgresql`. De qualquer forma, você precisará definir [extension_control_path](runtime-config-client.md#GUC-EXTENSION-CONTROL-PATH) e [dynamic_library_path](runtime-config-client.md#GUC-DYNAMIC-LIBRARY-PATH) para permitir que o servidor PostgreSQL encontre os arquivos:

```
extension_control_path = '/usr/local/extras/share/postgresql:$system'
dynamic_library_path = '/usr/local/extras/lib/postgresql:$libdir'
```

Você também pode executar `make` em um diretório fora da árvore de origem da sua extensão, se quiser manter o diretório de construção separado. Esse procedimento também é chamado de *VPATH* build. Veja como:

```
mkdir build_dir
cd build_dir
make -f /path/to/extension/source/tree/Makefile
make -f /path/to/extension/source/tree/Makefile install
```

Como alternativa, você pode configurar um diretório para uma construção VPATH de maneira semelhante àquela realizada para o código principal. Uma maneira de fazer isso é usando o script principal `config/prep_buildtree`. Uma vez que isso tenha sido feito, você pode construir definindo a variável `make` `VPATH` da seguinte maneira:

```
make VPATH=/path/to/extension/source/tree
make VPATH=/path/to/extension/source/tree install
```

Esse procedimento pode funcionar com uma maior variedade de layouts de diretório.

Os scripts listados na variável `REGRESS` são usados para testes de regressão do seu módulo, que pode ser invocado por `make installcheck` após fazer `make install`. Para que isso funcione, você deve ter um servidor PostgreSQL em execução. Os arquivos de script listados em `REGRESS` devem aparecer em um subdiretório chamado `sql/` no diretório da extensão. Esses arquivos devem ter a extensão `.sql`, que não deve ser incluída na lista `REGRESS` no makefile. Para cada teste, também deve haver um arquivo contendo a saída esperada em um subdiretório chamado `expected/`, com o mesmo radical e extensão `.out`. `make installcheck` executa cada script de teste com psql e compara a saída resultante com o arquivo esperado correspondente. Quaisquer diferenças serão escritas no arquivo `regression.diffs` no formato `diff -c`. Note que tentar executar um teste que está faltando seu arquivo esperado será relatado como “problema”, então certifique-se de ter todos os arquivos esperados.

Os scripts listados na variável `ISOLATION` são usados para testes que enfatizam o comportamento de sessão concorrente com seu módulo, que pode ser invocado por `make installcheck` após fazer `make install`. Para que isso funcione, você deve ter um servidor PostgreSQL em execução. Os arquivos de script listados em `ISOLATION` devem aparecer em um subdiretório chamado `specs/` no diretório da extensão. Esses arquivos devem ter a extensão `.spec`, que não deve ser incluída na lista `ISOLATION` no makefile. Para cada teste, também deve haver um arquivo contendo a saída esperada em um subdiretório chamado `expected/`, com o mesmo tronco e extensão `.out`. `make installcheck` executa cada script de teste e compara a saída resultante com o arquivo esperado correspondente. Quaisquer diferenças serão escritas no arquivo `output_iso/regression.diffs` no formato `diff -c`. Note que tentar executar um teste que está faltando seu arquivo esperado será relatado como “problema”, então certifique-se de ter todos os arquivos esperados.

`TAP_TESTS` permite o uso de testes TAP. Os dados de cada execução estão presentes em um subdiretório denominado `tmp_check/`. Consulte também [Seção 31.4](regress-tap.md "31.4. TAP Tests") para mais detalhes.

### DICA

A maneira mais fácil de criar os arquivos esperados é criar arquivos vazios, depois realizar uma execução de teste (que, claro, reportará diferenças). Inspecione os arquivos de resultado reais encontrados no diretório `results/` (para testes em `REGRESS`), ou no diretório `output_iso/results/` (para testes em `ISOLATION`), e depois copie-os para `expected/` se eles corresponderem ao que você espera do teste.