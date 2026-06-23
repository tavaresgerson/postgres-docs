## 17.4. Construção e Instalação com Meson [#](#INSTALL-MESON)

* [17.4.1. Versão Breve](install-meson.md#INSTALL-SHORT-MESON)
* [17.4.2. Procedimento de Instalação](install-meson.md#INSTALL-PROCEDURE-MESON)
* [17.4.3. Opções de `meson setup`](install-meson.md#MESON-OPTIONS)
* [17.4.4. `meson` Alvos de Construção](install-meson.md#TARGETS-MESON)

### 17.4.1. Versão Breve [#](#INSTALL-SHORT-MESON)

```
meson setup build --prefix=/usr/local/pgsql
cd build
ninja
su
ninja install
adduser postgres
mkdir -p /usr/local/pgsql/data
chown postgres /usr/local/pgsql/data
su - postgres
/usr/local/pgsql/bin/initdb -D /usr/local/pgsql/data
/usr/local/pgsql/bin/pg_ctl -D /usr/local/pgsql/data -l logfile start
/usr/local/pgsql/bin/createdb test
/usr/local/pgsql/bin/psql test
```

A versão longa é o restante desta seção.

### 17.4.2. Procedimento de instalação [#](#INSTALL-PROCEDURE-MESON)

1. **Configuração**

O primeiro passo do procedimento de instalação é configurar a árvore de compilação para o seu sistema e escolher as opções que você gostaria. Para criar e configurar o diretório de compilação, você pode começar com o comando `meson setup`.

```
meson setup build
```

O comando de configuração aceita os argumentos `builddir` e `srcdir`. Se não for fornecido `srcdir`, o Meson deduzirá o `srcdir` com base no diretório atual e na localização de `meson.build`. O `builddir` é obrigatório.

Executando `meson setup` carrega o arquivo de configuração de compilação e configura o diretório de compilação. Além disso, você também pode passar várias opções de compilação para o Meson. Algumas opções comumente usadas são mencionadas nas seções subsequentes. Por exemplo:

```
# configure with a different installation prefix
meson setup build --prefix=/home/user/pg-install

# configure to generate a debug build
meson setup build --buildtype=debug

# configure to build with OpenSSL support
meson setup build -Dssl=openssl
```

Configurar o diretório de compilação é uma etapa única. Para reconfigurar antes de uma nova compilação, você pode simplesmente usar o comando `meson configure`

```
meson configure -Dcassert=true
```

As opções de linha de comando comumente usadas do `meson configure` são explicadas em [Seção 17.4.3](install-meson.md#MESON-OPTIONS).

Por padrão, o Meson usa a ferramenta de compilação [Ninja](https://ninja-build.org/). Para construir o PostgreSQL a partir de fonte usando o Meson, você pode simplesmente usar o comando `ninja` no diretório de compilação.

```
ninja
```

O Ninja detectará automaticamente o número de CPUs no seu computador e se paralelizará conforme necessário. Você pode substituir o número de processos paralelos usados com o argumento de linha de comando `-j`.

Deve-se notar que, após a etapa inicial de configuração, `ninja` é o único comando que você precisa digitar para compilar. Não importa como você altere sua árvore de origem (a menos que a mova para um local completamente novo), o Meson detectará as alterações e se regenerará conforme necessário. Isso é especialmente útil se você tiver vários diretórios de compilação. Muitas vezes, um deles é usado para desenvolvimento (a compilação "de depuração") e outros apenas de vez em quando (como a compilação de "análise estática"). Qualquer configuração pode ser compilada apenas indo para o diretório correspondente e executando o Ninja.

Se você deseja construir com um backend diferente do ninja, pode usar configure com a opção `--backend` para selecionar o que você deseja usar e, em seguida, construir usando `meson compile`. Para saber mais sobre esses backends e outros argumentos que você pode fornecer ao ninja, você pode consultar a documentação do Meson [(https://mesonbuild.com/Running-Meson.html#building-from-the-source)].

Se você quiser testar o servidor recém-construído antes de instalá-lo, pode executar os testes de regressão neste ponto. Os testes de regressão são um conjunto de testes para verificar se o PostgreSQL funciona na sua máquina da maneira que os desenvolvedores esperavam. Tipo:

```
meson test
```

(Isso não funcionará como root; faça isso como um usuário não privilegiado.) Consulte o [Capítulo 31](regress.md) para obter informações detalhadas sobre a interpretação dos resultados do teste. Você pode repetir este teste em qualquer momento posterior, emitindo o mesmo comando.

Para executar os testes pg_regress e pg_isolation_regress contra uma instância de postgres em execução, especifique **`--setup running`** como um argumento para **`meson test`**.

Nota

Se você está atualizando um sistema existente, não se esqueça de ler [Seção 18.6](upgrading.md), que tem instruções sobre atualização de um cluster.

Uma vez que o PostgreSQL seja construído, você pode instalá-lo simplesmente executando o comando `ninja install`.

```
ninja install
```

Isso instalará os arquivos nos diretórios que foram especificados em [Passo 1] (install-meson.md#MESON-CONFIGURE "Configuration"). Certifique-se de que você tem permissões apropriadas para escrever nessa área. Você pode precisar fazer esse passo como root. Alternativamente, você pode criar os diretórios de destino com antecedência e organizar para que as permissões apropriadas sejam concedidas. A instalação padrão fornece todos os arquivos de cabeçalho necessários para o desenvolvimento de aplicativos cliente, bem como para o desenvolvimento de programas do lado do servidor, como funções personalizadas ou tipos de dados escritos em C.

`ninja install` deve funcionar na maioria dos casos, mas se você quiser usar mais opções (como `--quiet` para suprimir saída extra), também pode usar `meson install`. Você pode aprender mais sobre [meson install](https://mesonbuild.com/Commands.html#install) e suas opções na documentação do Meson.

**Desinstalação:** Para desfazer a instalação, você pode usar o comando `ninja uninstall`.

**Limpeza:** Após a instalação, você pode liberar espaço em disco removendo os arquivos construídos da árvore de origem com o comando `ninja clean`.

### 17.4.3. `meson setup` Opções [#](#MESON-OPTIONS)

As opções de linha de comando do `meson setup` são explicadas abaixo. Esta lista não é exaustiva (use `meson configure --help` para obter uma que o seja). As opções não cobertas aqui são destinadas a casos de uso avançados, e estão documentadas na documentação padrão do [Meson](https://mesonbuild.com/Commands.html#configure). Esses argumentos também podem ser usados com `meson setup`.

#### 17.4.3.1. Locais de instalação [#](#MESON-OPTIONS-LOCATIONS)

Essas opções controlam onde o `ninja install` (ou `meson install`) colocará os arquivos. A opção `--prefix` (exemplo [Seção 17.4.1](install-meson.md#INSTALL-SHORT-MESON "17.4.1. Short Version")) é suficiente para a maioria dos casos. Se você tiver necessidades especiais, pode personalizar os subdiretórios de instalação com as outras opções descritas nesta seção. No entanto, tenha cuidado para não alterar as localizações relativas dos diferentes subdiretórios, pois isso pode tornar a instalação não relocável, ou seja, você não poderá movê-la após a instalação. (As localizações `man` e `doc` não são afetadas por essa restrição). Para instalações relocáveis, você pode querer usar a opção `-Drpath=false` descrita mais adiante.

`--prefix=PREFIX` [#](#CONFIGURE-PREFIX-MESON): Instale todos os arquivos sob o diretório *`PREFIX`* em vez de `/usr/local/pgsql` (em sistemas baseados em Unix) ou `current drive letter:/usr/local/pgsql` (em Windows). Os arquivos reais serão instalados em vários subdiretórios; nenhum arquivo será instalado diretamente no diretório *`PREFIX`*.

`--bindir=DIRECTORY` [#](#CONFIGURE-BINDIR-MESON): Especifica o diretório para programas executáveis. O padrão é `PREFIX/bin`.

`--sysconfdir=DIRECTORY` [#](#CONFIGURE-SYSCONFDIR-MESON): Define o diretório para vários arquivos de configuração, `PREFIX/etc` por padrão.

`--libdir=DIRECTORY` [#](#CONFIGURE-LIBDIR-MESON): Define a localização para instalar bibliotecas e módulos dinamicamente carregáveis. O padrão é `PREFIX/lib`.

`--includedir=DIRECTORY` [#](#CONFIGURE-INCLUDEDIR-MESON): Define o diretório para a instalação de arquivos de cabeçalho C e C++. O padrão é `PREFIX/include`.

`--datadir=DIRECTORY` [#](#CONFIGURE-DATADIR-MESON): Define o diretório para arquivos de dados somente de leitura usados pelos programas instalados. O padrão é `PREFIX/share`. Observe que isso não tem nada a ver com o local onde seus arquivos de banco de dados serão colocados.

`--localedir=DIRECTORY` [#](#CONFIGURE-LOCALEDIR-MESON): Define o diretório para a instalação de dados de localização, em particular os arquivos de catálogo de tradução de mensagens. O padrão é `DATADIR/locale`.

`--mandir=DIRECTORY` [#](#CONFIGURE-MANDIR-MESON): As páginas do manual que vêm com o PostgreSQL serão instaladas neste diretório, em suas respectivas subdiretórios `manx`. O padrão é `DATADIR/man`.

Nota

Preocupamo-nos em tornar possível instalar o PostgreSQL em locais de instalação compartilhados (como `/usr/local/include`) sem interferir no espaço de nomes do resto do sistema. Primeiro, a string “`/postgresql`” é automaticamente anexada a `datadir`, `sysconfdir` e `docdir`, a menos que o nome de diretório totalmente expandido já contenha a string “`postgres`” ou “`pgsql`”. Por exemplo, se você escolher `/usr/local` como prefixo, a documentação será instalada em `/usr/local/doc/postgresql`, mas se o prefixo for `/opt/postgres`, então ela estará em `/opt/postgres/doc`. Os arquivos de cabeçalho C públicos das interfaces do cliente são instalados em `includedir` e são limpos em termos de espaço de nomes. Os arquivos de cabeçalho internos e os arquivos de cabeçalho do servidor são instalados em diretórios privados sob `includedir`. Consulte a documentação de cada interface para obter informações sobre como acessar seus arquivos de cabeçalho. Finalmente, se apropriado, um subdiretório privado também será criado sob [[`libdir`] para módulos carregáveis dinamicamente.

#### 17.4.3.2. Características do PostgreSQL [#](#MESON-OPTIONS-FEATURES)

As opções descritas nesta seção permitem a construção de várias funcionalidades opcionais do PostgreSQL. A maioria dessas funcionalidades requer software adicional, conforme descrito em [Seção 17.1](install-requirements.md), e serão habilitadas automaticamente se o software necessário for encontrado. Você pode alterar esse comportamento definindo manualmente essas funcionalidades para `enabled` para exigí-las ou `disabled` para não serem construídas com elas.

Para especificar opções específicas do PostgreSQL, o nome da opção deve ser precedido por `-D`.

`-Dnls={ auto | enabled | disabled }` [#](#CONFIGURE-WITH-NLS-MESON): Habilita ou desabilita o Suporte de Idioma Nativo (NLS), ou seja, a capacidade de exibir as mensagens de um programa em um idioma diferente do inglês. O padrão é automático e será ativado automaticamente se uma implementação da API Gettext for encontrada.

`-Dplperl={ auto | enabled | disabled }` [#](#CONFIGURE-WITH-PLPERL-MESON): Construa o PL/Perl, o idioma do lado do servidor. O padrão é auto.

`-Dplpython={ auto | enabled | disabled }` [#](#CONFIGURE-WITH-PLPYTHON-MESON): Construa o PL/Python, o idioma do lado do servidor. O padrão é auto.

`-Dpltcl={ auto | enabled | disabled }` [#](#CONFIGURE-WITH-PLTCL-MESON): Construa o PL/Tcl, o idioma do lado do servidor. O padrão é auto.

`-Dtcl_version=TCL_VERSION` [#](#CONFIGURE-WITH-TCL-VERSION-MESON): Especifica a versão do Tcl a ser usada ao construir o PL/Tcl.

`-Dicu={ auto | enabled | disabled }` [#](#CONFIGURE-WITH-ICU-MESON): Construa com suporte para a biblioteca ICU, permitindo o uso das características de ordenação ICU (consulte [Seção 23.2](collation.md "23.2. Collation Support")). Os valores padrão são automáticos e exigem que o pacote ICU4C seja instalado. A versão mínima necessária do ICU4C é atualmente 4.2.

`-Dllvm={ auto | enabled | disabled }` [#](#CONFIGURE-WITH-LLVM-MESON): Construa com suporte para compilação JIT (JIT) baseada em LLVM (consulte o [Capítulo 30](jit.md)). Isso requer que a biblioteca LLVM seja instalada. A versão mínima necessária do LLVM é atualmente 14. Desabilitada por padrão.

`llvm-config` será usado para encontrar as opções de compilação necessárias. `llvm-config`, e, em seguida, `llvm-config-$version` para todas as versões suportadas, serão pesquisados em seu `PATH`. Se isso não resultar no programa desejado, use `LLVM_CONFIG` para especificar um caminho para o `llvm-config` correto.

`-Dlz4={ auto | enabled | disabled }` [#](#CONFIGURE-WITH-LZ4-MESON): Construa com suporte à compressão LZ4. Padrão: auto.

`-Dzstd={ auto | enabled | disabled }` [#](#CONFIGURE-WITH-ZSTD-MESON): Construa com suporte à compressão Zstandard. Padrão: auto.

`-Dssl={ auto | LIBRARY }` [#](#CONFIGURE-WITH-SSL-MESON): Construa com suporte para conexões SSL (encriptadas). O único *`LIBRARY`* suportado é `openssl`. Isso requer que o pacote OpenSSL seja instalado. Ao construir com essa opção, o programa verificará os arquivos de cabeçalho e as bibliotecas necessárias para garantir que sua instalação do OpenSSL seja suficiente antes de prosseguir. A opção padrão para essa opção é auto.

`-Dgssapi={ auto | enabled | disabled }` [#](#CONFIGURE-WITH-GSSAPI-MESON): Construa com suporte para autenticação GSSAPI. O MIT Kerberos é necessário para o GSSAPI. Em muitos sistemas, o sistema GSSAPI (uma parte da instalação do MIT Kerberos) não está instalado em um local que é pesquisado por padrão (por exemplo, `/usr/include`, `/usr/lib`). Nesses casos, o PostgreSQL consultará `pkg-config` para detectar as opções de compilador e encadeamento necessárias. O padrão é auto. `meson configure` verificará os arquivos de cabeçalho e as bibliotecas necessárias para garantir que sua instalação GSSAPI seja suficiente antes de prosseguir.

`-Dldap={ auto | enabled | disabled }` [#](#CONFIGURE-WITH-LDAP-MESON): Construa com suporte LDAP para busca de parâmetros de autenticação e conexão (consulte [Seção 32.18](libpq-ldap.md "32.18. LDAP Lookup of Connection Parameters") e [Seção 20.10](auth-ldap.md "20.10. LDAP Authentication") para mais informações). Em Unix, isso requer que o pacote OpenLDAP seja instalado. Em Windows, a biblioteca WinLDAP padrão é usada. A configuração padrão é auto. `meson configure` verificará os arquivos e bibliotecas de cabeçalho necessários para garantir que sua instalação do OpenLDAP seja suficiente antes de prosseguir.

`-Dpam={ auto | enabled | disabled }` [#](#CONFIGURE-WITH-PAM-MESON): Construa com suporte a PAM (Módulos de Autenticação Conectam-se). Definição padrão: auto.

`-Dbsd_auth={ auto | enabled | disabled }` [#](#CONFIGURE-WITH-BSD-AUTH-MESON): Construa com suporte de autenticação BSD. (O framework de autenticação BSD está atualmente disponível apenas no OpenBSD.) O padrão é auto.

`-Dsystemd={ auto | enabled | disabled }` [#](#CONFIGURE-WITH-SYSTEMD-MESON): Construa com suporte para notificações de serviço systemd. Isso melhora a integração se o servidor for iniciado sob o systemd, mas não tem impacto caso contrário; consulte [Seção 18.3](server-start.md "18.3. Starting the Database Server") para mais informações. O padrão é auto. libsystemd e os arquivos de cabeçalho associados precisam ser instalados para usar essa opção.

`-Dbonjour={ auto | enabled | disabled }` [#](#CONFIGURE-WITH-BONJOUR-MESON): Construa com suporte para detecção automática de serviços Bonjour. Tem como padrão auto e requer suporte Bonjour em seu sistema operacional. Recomendado em macOS.

`-Duuid=LIBRARY` [#](#CONFIGURE-WITH-UUID-MESON): Construa o módulo [uuid-ossp](uuid-ossp.md "F.49. uuid-ossp — a UUID generator") (que fornece funções para gerar UUIDs), usando a biblioteca de UUID especificada. *`LIBRARY`* deve ser um dos:

* `none` para não construir o módulo uuid. Este é o padrão. * `bsd` para usar as funções UUID encontradas no FreeBSD e em outros sistemas derivados do BSD * `e2fs` para usar a biblioteca UUID criada pelo projeto `e2fsprogs`; esta biblioteca está presente na maioria dos sistemas Linux e no macOS, e também pode ser obtida para outras plataformas * `ossp` para usar a biblioteca [OSSP UUID](http://www.ossp.org/pkg/lib/uuid/)

`-Dlibcurl={ auto | enabled | disabled }` [#](#CONFIGURE-WITH-LIBCURL-MESON): Construa com suporte ao libcurl para fluxos de cliente OAuth 2.0. A versão 7.61.0 ou posterior do Libcurl é necessária para essa funcionalidade. Ao construir com essa opção, o programa verificará os arquivos de cabeçalho e as bibliotecas necessárias para garantir que a instalação do Curl seja suficiente antes de prosseguir. A opção padrão é auto.

`-Dliburing={ auto | enabled | disabled }` [#](#CONFIGURE-WITH-LIBURING-MESON): Construa com liburing, habilitando o suporte io_uring para I/O assíncrono. Padrão: auto.

Para usar uma instalação de liburing em um local incomum, você pode definir variáveis de ambiente relacionadas ao `pkg-config` (consulte a documentação).

`-Dlibnuma={ auto | enabled | disabled }` [#](#CONFIGURE-WITH-LIBNUMA-MESON): Construa com suporte à libnuma para suporte básico NUMA. Apenas suportado em plataformas para as quais a biblioteca libnuma é implementada. A opção padrão é auto.

`-Dlibxml={ auto | enabled | disabled }` [#](#CONFIGURE-WITH-LIBXML-MESON): Construa com libxml2, habilitando o suporte SQL/XML. Padrão para auto. É necessária a versão 2.6.23 ou posterior do Libxml2 para este recurso.

Para usar uma instalação do libxml2 em um local incomum, você pode definir variáveis de ambiente relacionadas ao `pkg-config` (consulte a documentação).

`-Dlibxslt={ auto | enabled | disabled }` [#](#CONFIGURE-WITH-LIBXSLT-MESON): Construa com libxslt, habilitando o módulo [xml2](xml2.md "F.50. xml2 — XPath querying and XSLT functionality") para realizar transformações XSL de XML. `-Dlibxml` também deve ser especificado. O padrão é auto.

`-Dselinux={ auto | enabled | disabled }` [#](#CONFIGURE-WITH-SEPGSQL-MESON): Construa com suporte SElinux, habilitando o módulo de segurança [sepgsql](sepgsql.md "F.40. sepgsql — SELinux-, label-based mandatory access control (MAC)") e defina como padrão auto.

#### 17.4.3.3. Funções anti [#](#MESON-OPTIONS-ANTI-FEATURES)

`-Dreadline={ auto | enabled | disabled }` [#](#CONFIGURE-READLINE-MESON): Permite o uso da biblioteca Readline (e também do libedit). Esta opção é predefinida como auto e habilita a edição de linha de comando e histórico no psql e é fortemente recomendada.

`-Dlibedit_preferred={ true | false }` [#](#CONFIGURE-LIBEDIT-PREFERRED-MESON): Definir essa opção como verdadeira favorece o uso da biblioteca libedit licenciada pela BSD em vez da Readline licenciada pela GPL. Esta opção é significativa apenas se você tiver ambas as bibliotecas instaladas; o padrão é false, ou seja, usar a Readline.

`-Dzlib={ auto | enabled | disabled }` [#](#CONFIGURE-ZLIB-MESON): Habilita o uso da biblioteca Zlib. O padrão é auto e habilita o suporte para arquivos comprimidos em pg_dump, pg_restore e pg_basebackup e é recomendado.

#### 17.4.3.4. Detalhes do processo de construção [#](#MESON-OPTIONS-BUILD-PROCESS)

`--auto-features={ auto | enabled | disabled }` [#](#CONFIGURE-AUTO-FEATURES-MESON): Definir esta opção permite que você substitua o valor de todas as características "automáticas" (características que são ativadas automaticamente se o software necessário for encontrado). Isso pode ser útil quando você deseja desabilitar ou habilitar todas as características "opcionais" de uma vez, sem precisar definir cada uma delas manualmente. O valor padrão para este parâmetro é auto.

`--backend=BACKEND` [#](#CONFIGURE-BACKEND-MESON): O backend padrão que o Meson usa é o ninja e isso deve ser suficiente para a maioria dos casos de uso. No entanto, se você deseja integrá-lo totalmente ao Visual Studio, pode definir o *`BACKEND`* para `vs`.

`-Dc_args=OPTIONS` [#](#CONFIGURE-C-ARGS-MESON): Esta opção pode ser usada para passar opções adicionais ao compilador C.

`-Dc_link_args=OPTIONS` [#](#CONFIGURE-C-LINK-ARGS-MESON): Esta opção pode ser usada para passar opções adicionais ao encadeador C.

`-Dextra_include_dirs=DIRECTORIES` [#](#CONFIGURE-EXTRA-INCLUDE-DIRS-MESON): *`DIRECTORIES`* é uma lista de diretórios separados por vírgula que serão adicionados à lista em que o compilador busca arquivos de cabeçalho. Se você tiver pacotes opcionais (como GNU Readline) instalados em um local não padrão, você deve usar essa opção e, provavelmente, também a opção correspondente `-Dextra_lib_dirs`.

Exemplo: `-Dextra_include_dirs=/opt/gnu/include,/usr/sup/include`.

`-Dextra_lib_dirs=DIRECTORIES` [#](#CONFIGURE-EXTRA-LIB-DIRS-MESON): *`DIRECTORIES`* é uma lista de diretórios separados por vírgula para procurar bibliotecas. Você provavelmente terá que usar essa opção (e a opção correspondente `-Dextra_include_dirs`), se tiver pacotes instalados em locais não padrão.

Exemplo: `-Dextra_lib_dirs=/opt/gnu/lib,/usr/sup/lib`.

`-Dsystem_tzdata=DIRECTORY` [#](#CONFIGURE-SYSTEM-TZDATA-MESON): O PostgreSQL inclui seu próprio banco de dados de fuso horário, que ele exige para operações de data e hora. Esse banco de dados de fuso horário é, de fato, compatível com o banco de dados de fuso horário IANA fornecido por muitos sistemas operacionais, como FreeBSD, Linux e Solaris, portanto, seria redundante instalá-lo novamente. Quando esta opção é usada, o banco de dados de fuso horário fornecido pelo sistema em *`DIRECTORY`* é usado em vez do que está incluído na distribuição de fonte do PostgreSQL. *`DIRECTORY`* deve ser especificado como um caminho absoluto. `/usr/share/zoneinfo` é um diretório provável em alguns sistemas operacionais. Note que a rotina de instalação não detectará dados de fuso horário incompatíveis ou errados. Se você usar esta opção, é aconselhável executar os testes de regressão para verificar se os dados de fuso horário que você apontou funcionam corretamente com o PostgreSQL.

Esta opção é destinada principalmente a distribuidores de pacotes binários que conhecem bem o seu sistema operacional alvo. A principal vantagem de usar esta opção é que o pacote PostgreSQL não precisará ser atualizado sempre que alguma das muitas regras locais de horário de verão mudar. Outra vantagem é que o PostgreSQL pode ser compilado de forma mais direta se os arquivos do banco de dados de fuso horário não precisarem ser construídos durante a instalação.

`-Dextra_version=STRING` [#](#CONFIGURE-EXTRA-VERSION-MESON): Adicione *`STRING`* ao número da versão do PostgreSQL. Você pode usar isso, por exemplo, para marcar binários construídos a partir de snapshots do Git não lançados ou que contenham patches personalizados com uma string de versão extra, como um identificador `git describe` ou um número de lançamento de pacote de distribuição.

`-Drpath={ true | false }` [#](#CONFIGURE-RPATH-MESON): Esta opção é definida como verdadeira por padrão. Se definida como falsa, não marque os executáveis do PostgreSQL para indicar que eles devem procurar bibliotecas compartilhadas no diretório de bibliotecas da instalação (consulte `--libdir`). Na maioria das plataformas, essa marcação usa um caminho absoluto para o diretório de bibliotecas, de modo que não será útil se você relocar a instalação posteriormente. No entanto, você precisará fornecer outra maneira para os executáveis encontrarem as bibliotecas compartilhadas. Normalmente, isso requer a configuração do link dinâmico do sistema operacional para procurar o diretório de bibliotecas; consulte [Seção 17.5.1](install-post.md#INSTALL-POST-SHLIBS "17.5.1. Shared Libraries") para mais detalhes.

`-DBINARY_NAME=PATH` [#](#CONFIGURE-BINARY-NAME-MESON): Se um programa que precisa ser instalado para construir o PostgreSQL (com ou sem opções opcionais) estiver armazenado em um caminho não padrão, você pode especiá-lo manualmente em `meson configure`. A lista completa dos programas para os quais isso é suportado pode ser encontrada executando `meson configure`. Exemplo:

```
meson configure -DBISON=PATH_TO_BISON
```

#### 17.4.3.5. Documentação [#](#MESON-OPTIONS-DOCS)

Consulte a [Seção J.2](docguide-toolsets.md) para obter as ferramentas necessárias para a construção da documentação.

`-Ddocs={ auto | enabled | disabled }` [#](#CONFIGURE-DOCS-MESON): Permite a construção da documentação em HTML e formato man. O padrão é auto.

`-Ddocs_pdf={ auto | enabled | disabled }` [#](#CONFIGURE-DOCS-PDF-MESON): Permite a construção da documentação em formato PDF. O padrão é automático.

`-Ddocs_html_style={ simple | website }` [#](#CONFIGURE-DOCS-HTML-STYLE): Controla qual folha de estilo CSS é usada. O padrão é `simple`. Se definido como `website`, a documentação HTML fará referência à folha de estilo para [postgresql.org](https://www.postgresql.org/docs/current/).

#### 17.4.3.6. Diversos [#](#MESON-OPTIONS-MISC)

`-Dpgport=NUMBER` [#](#CONFIGURE-PGPORT-MESON): Configure *`NUMBER`* como o número de porta padrão para o servidor e os clientes. O padrão é 5432. A porta pode ser alterada posteriormente, mas se você especificar aqui, o servidor e os clientes terão o mesmo valor padrão compilado, o que pode ser muito conveniente. Geralmente, a única boa razão para selecionar um valor não padrão é se você pretende executar vários servidores PostgreSQL na mesma máquina.

`-Dkrb_srvnam=NAME` [#](#CONFIGURE-KRB-SRVNAM-MESON): O nome padrão do principal do serviço Kerberos usado pelo GSSAPI. `postgres` é o padrão. Geralmente, não há motivo para alterar isso, a menos que você esteja construindo para um ambiente Windows, no qual caso, ele deve ser definido em maiúsculas `POSTGRES`.

`-Dsegsize=SEGSIZE` [#](#CONFIGURE-SEGSIZE-MESON): Defina o *tamanho do segmento*, em gigabytes. As tabelas grandes são divididas em vários arquivos do sistema operacional, cada um com tamanho igual ao tamanho do segmento. Isso evita problemas com limites de tamanho de arquivo que existem em muitas plataformas. O tamanho de segmento padrão, 1 gigabyte, é seguro em todas as plataformas suportadas. Se o seu sistema operacional tiver suporte para "largefile" (o que a maioria tem, atualmente), você pode usar um tamanho de segmento maior. Isso pode ser útil para reduzir o número de descritores de arquivo consumidos ao trabalhar com tabelas muito grandes. Mas tenha cuidado para não selecionar um valor maior do que o suportado pela sua plataforma e pelos sistemas de arquivos que você pretende usar. Outras ferramentas que você pode querer usar, como o tar, também podem definir limites no tamanho de arquivo utilizável. É recomendado, embora não seja absolutamente necessário, que esse valor seja um poder de 2.

`-Dblocksize=BLOCKSIZE` [#](#CONFIGURE-BLOCKSIZE-MESON): Defina o *tamanho do bloco*, em kilobytes. Essa é a unidade de armazenamento e I/O dentro das tabelas. O padrão, de 8 kilobytes, é adequado para a maioria das situações; mas outros valores podem ser úteis em casos especiais. O valor deve ser um expoente de 2 entre 1 e 32 (kilobytes).

`-Dwal_blocksize=BLOCKSIZE` [#](#CONFIGURE-WAL-BLOCKSIZE-MESON): Defina o tamanho do bloco *WAL*, em kilobytes. Essa é a unidade de armazenamento e de entrada/saída dentro do log WAL. O padrão, de 8 kilobytes, é adequado para a maioria das situações; mas outros valores podem ser úteis em casos especiais. O valor deve ser um expoente de 2 entre 1 e 64 (kilobytes).

#### 17.4.3.7. Opções do desenvolvedor [#](#MESON-OPTIONS-DEVEL)

A maioria das opções desta seção é de interesse apenas para o desenvolvimento ou depuração do PostgreSQL. Não são recomendadas para edições de produção, exceto `--debug`, que pode ser útil para habilitar relatórios de bugs detalhados no caso improvável de você encontrar um bug. Em plataformas que suportam DTrace, `-Ddtrace` também pode ser razoável para uso em produção.

Ao construir uma instalação que será usada para desenvolver código dentro do servidor, é recomendável usar pelo menos as opções `--buildtype=debug` e `-Dcassert`.

`--buildtype=BUILDTYPE` [#](#CONFIGURE-BUILDTYPE-MESON): Esta opção pode ser usada para especificar o tipo de compilação a ser utilizado; o padrão é `debugoptimized`. Se você deseja um controle mais preciso sobre os símbolos de depuração e os níveis de otimização do que esta opção oferece, você pode consultar as bandeiras `--debug` e `--optimization`.

Os seguintes tipos de construção são geralmente utilizados: `plain`, `debug`, `debugoptimized` e `release`. Mais informações sobre eles podem ser encontradas na documentação do Meson [Meson documentation](https://mesonbuild.com/Running-Meson.html#configuring-the-build-directory).

`--debug` [#](#CONFIGURE-DEBUG-MESON): Compila todos os programas e bibliotecas com símbolos de depuração. Isso significa que você pode executar os programas em um depurador para analisar problemas. Isso aumenta consideravelmente o tamanho dos executables instalados, e em compiladores que não são do GCC, geralmente também desabilita a otimização do compilador, causando lentidão. No entanto, ter os símbolos disponíveis é extremamente útil para lidar com quaisquer problemas que possam surgir. Atualmente, essa opção é recomendada apenas para instalações de produção se você usar o GCC. Mas você deve sempre tê-la se estiver fazendo trabalho de desenvolvimento ou executando uma versão beta.

`--optimization`=*`LEVEL`* [#](#CONFIGURE-OPTIMIZATION-MESON): Especifique o nível de otimização. `LEVEL` pode ser definido em qualquer um dos valores {0, g, 1, 2, 3, s}.

`--werror` [#](#CONFIGURE-WERROR-MESON): Definir esta opção pede ao compilador que trate as advertências como erros. Isso pode ser útil para o desenvolvimento de código.

`-Dcassert={ true | false }` [#](#CONFIGURE-CASSERT-MESON): Habilita verificações de *afirmação* no servidor, que testam muitas condições de "não pode acontecer". Isso é inestimável para fins de desenvolvimento de código, mas os testes desaceleram significativamente o servidor. Além disso, ter as verificações ativadas não necessariamente melhora a estabilidade do seu servidor! As verificações de afirmação não são categorizadas por gravidade, e assim o que pode ser um bug relativamente inofensivo ainda levará a reinicializações do servidor se ele desencadear uma falha de afirmação. Esta opção não é recomendada para uso em produção, mas você deve tê-la para trabalho de desenvolvimento ou ao executar uma versão beta.

`-Dtap_tests={ auto | enabled | disabled }` [#](#CONFIGURE-TAP-TESTS-MESON): Habilitar testes usando as ferramentas Perl TAP. O padrão é automático e requer uma instalação do Perl e o módulo Perl `IPC::Run`. Consulte [Seção 31.4](regress-tap.md "31.4. TAP Tests") para obter mais informações.

`-DPG_TEST_EXTRA=TEST_SUITES` [#](#CONFIGURE-PG-TEST-EXTRA-MESON): Habilitar suportes de teste adicionais, que não são executados por padrão porque não são seguros para executar em um sistema multiusuário, requerem software especial para executar ou são intensivos em recursos. O argumento é uma lista de testes separados por espaços em branco para habilitar. Consulte [Seção 31.1.3](regress-run.md#REGRESS-ADDITIONAL "31.1.3. Additional Test Suites") para detalhes. Se a variável de ambiente `PG_TEST_EXTRA` estiver definida quando os testes forem executados, ela substituirá esta opção de tempo de configuração.

`-Db_coverage={ true | false }` [#](#CONFIGURE-B-COVERAGE-MESON): Se estiver usando o GCC, todos os programas e bibliotecas são compilados com instrumentação de teste de cobertura de código. Quando executados, eles geram arquivos no diretório de construção com métricas de cobertura de código. Consulte [Seção 31.5](regress-coverage.md "31.5. Test Coverage Examination") para obter mais informações. Esta opção é para uso apenas com o GCC e quando estiver realizando trabalho de desenvolvimento.

`-Ddtrace={ auto | enabled | disabled }` [#](#CONFIGURE-DTRACE-MESON): Ativação desta compilação do PostgreSQL com suporte para a ferramenta de rastreamento dinâmico DTrace. Consulte [Seção 27.5](dynamic-trace.md "27.5. Dynamic Tracing") para mais informações.

Para apontar para o programa `dtrace`, a opção `DTRACE` pode ser definida. Isso geralmente será necessário, pois o `dtrace` é instalado normalmente sob `/usr/sbin`, que pode não estar em seu `PATH`.

`-Dinjection_points={ true | false }` [#](#CONFIGURE-INJECTION-POINTS-MESON): Compila o PostgreSQL com suporte para pontos de injeção no servidor. Os pontos de injeção permitem executar código definido pelo usuário dentro do servidor em caminhos de código pré-definidos. Isso ajuda a testar e investigar cenários de concorrência de maneira controlada. Esta opção é desativada por padrão. Consulte [Seção 36.10.14](xfunc-c.md#XFUNC-ADDIN-INJECTION-POINTS) para mais detalhes. Esta opção é destinada a ser usada apenas por desenvolvedores para testes.

`-Dsegsize_blocks=SEGSIZE_BLOCKS` [#](#CONFIGURE-SEGSIZE-BLOCKS-MESON): Especifique o tamanho do segmento de relação em blocos. Se ambos `-Dsegsize` e esta opção forem especificados, esta opção vence. Esta opção é apenas para desenvolvedores, para testar código relacionado ao segmento.

### 17.4.4. `meson` Metas de construção [#](#TARGETS-MESON)

Os objetivos de compilação individuais podem ser compilados usando `ninja` *`target`*. Quando não é especificado um alvo, tudo, exceto a documentação, é compilado. Os produtos de compilação individuais podem ser compilados usando o caminho/nome do arquivo como *`target`*.

#### 17.4.4.1. Alvos do código [#](#TARGETS-MESON-CODE)

`all` [#](#MESON-TARGET-ALL): Construa tudo, exceto documentação

`backend` [#](#MESON-TARGET-BACKEND): Construa o backend e módulos relacionados

`bin` [#](#MESON-TARGET-BIN): Construa binários do frontend

`contrib` [#](#MESON-TARGET-CONTRIB): Construa módulos contrib

`pl` [#](#MESON-TARGET-PL): Construa linguagens processuais

#### 17.4.4.2. Alvos do Desenvolvedor [#](#TARGETS-MESON-DEVELOPER)

`reformat-dat-files` [#](#MESON-TARGET-REFORMAT-DAT-FILES): Reescreva os arquivos de dados do catálogo no formato padrão

`expand-dat-files` [#](#MESON-TARGET-EXPAND-DAT-FILES): Expanda todos os arquivos de dados para incluir os padrões

`update-unicode` [#](#MESON-TARGET-UPDATE-UNICODE): Atualize os dados unicode para a nova versão

#### 17.4.4.3. **Documentação de alvos [#](#TARGETS-MESON-DOCUMENTATION)

`html` [#](#MESON-TARGET-HTML): Construa documentação em formato HTML de várias páginas

`man` [#](#MESON-TARGET-MAN): Construa documentação em formato de página do manual

`docs` [#](#MESON-TARGET-DOCS): Construa documentação em formato HTML de várias páginas e página do manual

`doc/src/sgml/postgres-A4.pdf` [#](#MESON-TARGET-DOC-SRC-SGML-POSTGRES-A4.PDF): Construa documentação em formato PDF, com páginas A4

`doc/src/sgml/postgres-US.pdf` [#](#MESON-TARGET-DOC-SRC-SGML-POSTGRES-US.PDF): Construa documentação em formato PDF, com páginas em letra de tamanho americano

`doc/src/sgml/postgres.html` [#](#MESON-TARGET-DOC-SRC-SGML-POSTGRES.HTML): Construa documentação em formato HTML de página única

`alldocs` [#](#MESON-TARGET-ALLDOCS): Construa documentação em todos os formatos suportados

#### 17.4.4.4. Alvos de instalação [#](#TARGETS-MESON-INSTALLATION)

`install` [#](#MESON-TARGET-INSTALL): Instale postgres, excluindo a documentação

`install-docs` [#](#MESON-TARGET-INSTALL-DOCS): Instale a documentação em formatos de HTML de várias páginas e páginas do manual

`install-html` [#](#MESON-TARGET-INSTALL-HTML): Instale a documentação em formato HTML de várias páginas

`install-man` [#](#MESON-TARGET-INSTALL-MAN): Instale a documentação no formato da página do manual

`install-quiet` [#](#MESON-TARGET-INSTALL-QUIET): Como "instalar", mas os arquivos instalados não são exibidos

`install-world` [#](#MESON-TARGET-INSTALL-WORLD): Instale o postgres, incluindo documentação de HTML multipágina e página do manual

`uninstall` [#](#MESON-TARGET-UNINSTALL): Remova os arquivos instalados

#### 17.4.4.5. Outros Alvos [#](#TARGETS-MESON-OTHER)

`clean` [#](#MESON-TARGET-CLEAN): Remova todos os produtos de construção

`test` [#](#MESON-TARGET-TEST): Execute todos os testes habilitados (incluindo contrib)

`world` [#](#MESON-TARGET-WORLD): Construa tudo, incluindo documentação

`help` [#](#MESON-TARGET-HELP): Lista de alvos importantes