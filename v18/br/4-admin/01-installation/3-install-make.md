## 17.3. Construção e Instalação com Autoconf e Make [#](#INSTALL-MAKE)

* [17.3.1. Versão Breve](install-make.md#INSTALL-SHORT-MAKE)
* [17.3.2. Procedimento de Instalação](install-make.md#INSTALL-PROCEDURE-MAKE)
* [17.3.3. Opções de `configure`](install-make.md#CONFIGURE-OPTIONS)
* [17.3.4. Variáveis Ambientais de `configure`](install-make.md#CONFIGURE-ENVVARS)

### 17.3.1. Versão Breve [#](#INSTALL-SHORT-MAKE)

```
./configure
make
su
make install
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

### 17.3.2. Procedimento de instalação [#](#INSTALL-PROCEDURE-MAKE)

1. **Configuração**

O primeiro passo do procedimento de instalação é configurar a árvore de origem do seu sistema e escolher as opções que você deseja. Isso é feito executando o script `configure`. Para uma instalação padrão, basta digitar:

```
./configure
```

Este script executará uma série de testes para determinar os valores de várias variáveis dependentes do sistema e detectará quaisquer peculiaridades do seu sistema operacional. Por fim, criará vários arquivos na árvore de construção para registrar o que encontrou.

Você também pode executar `configure` em um diretório fora da árvore de origem e, em seguida, construir lá, se quiser manter o diretório de construção separado dos arquivos de origem originais. Esse procedimento é chamado de *VPATH* build. Aqui está como fazer:

```
mkdir build_dir
cd build_dir
/path/to/source/tree/configure [options go here]
make
```

A configuração padrão irá construir o servidor e as ferramentas, bem como todas as aplicações e interfaces de cliente que requerem apenas um compilador C. Todos os arquivos serão instalados por padrão em `/usr/local/pgsql`.

Você pode personalizar o processo de construção e instalação fornecendo uma ou mais opções de linha de comando para `configure`. Normalmente, você deve personalizar a localização de instalação ou o conjunto de recursos opcionais que são construídos. `configure` tem um grande número de opções, que são descritas em [Seção 17.3.3](install-make.md#CONFIGURE-OPTIONS "17.3.3. configure Options").

Além disso, `configure` responde a determinadas variáveis de ambiente, conforme descrito na [Seção 17.3.4](install-make.md#CONFIGURE-ENVVARS). Essas variáveis oferecem maneiras adicionais de personalizar a configuração.

Para iniciar a construção, digite qualquer uma das seguintes opções:

```
make
make all
```

(Lembre-se de usar o GNU make.) A construção levará alguns minutos, dependendo do seu hardware.

Se você quer construir tudo o que pode ser construído, incluindo a documentação (HTML e páginas do manual) e os módulos adicionais (`contrib`), digite em vez disso:

```
make world
```

Se você quer construir tudo o que pode ser construído, incluindo os módulos adicionais (`contrib`), mas sem a documentação, digite em vez disso:

```
make world-bin
```

Se você deseja invocar a compilação a partir de outro makefile em vez de manualmente, você deve desativar `MAKELEVEL` ou configurá-lo como zero, por exemplo, da seguinte forma:

```
build-postgresql:
        $(MAKE) -C postgresql MAKELEVEL=0 all
```

A falha em fazer isso pode levar a mensagens de erro estranhas, geralmente sobre arquivos de cabeçalho ausentes. 3. **Testes de Regressão**

Se você quiser testar o servidor recém-construído antes de instalá-lo, pode executar os testes de regressão neste ponto. Os testes de regressão são um conjunto de testes para verificar se o PostgreSQL funciona na sua máquina da maneira que os desenvolvedores esperavam. Tipo:

```
make check
```

(Isso não funcionará como root; faça isso como um usuário não privilegiado.) Consulte o [Capítulo 31](regress.md) para obter informações detalhadas sobre a interpretação dos resultados do teste. Você pode repetir este teste em qualquer momento posterior, emitindo o mesmo comando.

Nota

Se você está atualizando um sistema existente, não se esqueça de ler [Seção 18.6](upgrading.md), que tem instruções sobre atualização de um cluster.

Para instalar o PostgreSQL, digite:

```
make install
```

Isso instalará os arquivos nos diretórios que foram especificados em [Passo 1](install-make.md#CONFIGURE). Certifique-se de que você tem permissões apropriadas para escrever nessa área. Normalmente, você precisa fazer esse passo como root. Alternativamente, você pode criar os diretórios de destino com antecedência e organizar para que as permissões apropriadas sejam concedidas.

Para instalar a documentação (HTML e páginas do manual), digite:

```
make install-docs
```

Se você construiu o mundo acima, digite em vez disso:

```
make install-world
```

Isso também instala a documentação.

Se você construiu o mundo sem a documentação acima, digite em vez disso:

```
make install-world-bin
```

Você pode usar `make install-strip` em vez de `make install` para remover os arquivos executáveis e as bibliotecas conforme eles são instalados. Isso economizará algum espaço. Se você construiu com suporte de depuração, a remoção efetivamente removerá o suporte de depuração, então isso deve ser feito apenas se a depuração não for mais necessária. `install-strip` tenta fazer um trabalho razoável para economizar espaço, mas não tem conhecimento perfeito sobre como remover todos os bytes desnecessários de um arquivo executável, então se você quiser economizar todo o espaço em disco que puder, terá que fazer trabalho manual.

A instalação padrão fornece todos os arquivos de cabeçalho necessários para o desenvolvimento de aplicativos cliente, bem como para o desenvolvimento de programas do lado do servidor, como funções personalizadas ou tipos de dados escritos em C.

**Instalação exclusiva para cliente:** Se você deseja instalar apenas as aplicações do cliente e as bibliotecas de interface, então você pode usar esses comandos:

```
make -C src/bin install
make -C src/include install
make -C src/interfaces install
make -C doc install
```

`src/bin` tem alguns binários para uso exclusivo de servidor, mas eles são pequenos.

**Desinstalação:** Para desfazer a instalação, use o comando `make uninstall`. No entanto, isso não removerá nenhum diretório criado.

**Limpeza:** Após a instalação, você pode liberar espaço em disco removendo os arquivos construídos da árvore de origem com o comando `make clean`. Isso preservará os arquivos criados pelo programa `configure`, para que você possa reconstruir tudo com `make` mais tarde. Para redefinir a árvore de origem ao estado em que foi distribuída, use `make distclean`. Se você vai construir para várias plataformas na mesma árvore de origem, você deve fazer isso e reconfigurar para cada plataforma. (Alternativamente, use uma árvore de construção separada para cada plataforma, para que a árvore de origem permaneça sem modificações.)

Se você realizar uma construção e depois descobrir que suas opções de `configure` estavam erradas, ou se você alterar algo que o `configure` investiga (por exemplo, atualizações de software), é uma boa ideia realizar o `make distclean` antes de reconfigurar e reconstruir. Sem isso, suas alterações nas escolhas de configuração podem não se propagar por todas as áreas onde precisam.

### 17.3.3. `configure` Opções [#](#CONFIGURE-OPTIONS)

As opções de linha de comando do `configure` são explicadas abaixo. Esta lista não é exaustiva (use `./configure --help` para obter uma que o seja). As opções não cobertas aqui são destinadas a casos de uso avançados, como a compilação cruzada, e estão documentadas na documentação padrão do Autoconf.

#### 17.3.3.1. Locais de instalação [#](#CONFIGURE-OPTIONS-LOCATIONS)

Essas opções controlam onde o `make install` colocará os arquivos. A opção `--prefix` é suficiente para a maioria dos casos. Se você tiver necessidades especiais, pode personalizar os subdiretórios de instalação com as outras opções descritas nesta seção. No entanto, tenha cuidado para não alterar as localizações relativas dos diferentes subdiretórios, pois isso pode tornar a instalação não relocável, ou seja, você não poderá movê-la após a instalação. (As localizações `man` e `doc` não são afetadas por essa restrição). Para instalações relocáveis, você pode querer usar a opção `--disable-rpath` descrita mais adiante.

`--prefix=PREFIX` [#](#CONFIGURE-OPTION-PREFIX): Instale todos os arquivos sob o diretório *`PREFIX`* em vez de `/usr/local/pgsql`. Os arquivos reais serão instalados em vários subdiretórios; nenhum arquivo será instalado diretamente no diretório *`PREFIX`*.

`--exec-prefix=EXEC-PREFIX` [#](#CONFIGURE-OPTION-EXEC-PREFIX): Você pode instalar arquivos dependentes da arquitetura sob um prefixo diferente, *`EXEC-PREFIX`*, do que o que *`PREFIX`* foi definido. Isso pode ser útil para compartilhar arquivos independentes da arquitetura entre os hosts. Se você omitir isso, então *`EXEC-PREFIX`* é definido igual a *`PREFIX`* e tanto os arquivos dependentes quanto independentes da arquitetura serão instalados sob a mesma árvore, o que provavelmente é o que você quer.

`--bindir=DIRECTORY` [#](#CONFIGURE-OPTION-BINDIR): Especifica o diretório para programas executáveis. O padrão é `EXEC-PREFIX/bin`, que normalmente significa `/usr/local/pgsql/bin`.

`--sysconfdir=DIRECTORY` [#](#CONFIGURE-OPTION-SYSCONFDIR): Define o diretório para vários arquivos de configuração, `PREFIX/etc`, por padrão.

`--libdir=DIRECTORY` [#](#CONFIGURE-OPTION-LIBDIR): Define a localização para instalar bibliotecas e módulos dinamicamente carregáveis. O padrão é `EXEC-PREFIX/lib`.

`--includedir=DIRECTORY` [#](#CONFIGURE-OPTION-INCLUDEDIR): Define o diretório para a instalação de arquivos de cabeçalho de C e C++. O padrão é `PREFIX/include`.

`--datarootdir=DIRECTORY` [#](#CONFIGURE-OPTION-DATAROOTDIR): Define o diretório raiz para vários tipos de arquivos de dados somente de leitura. Isso define apenas o padrão para algumas das seguintes opções. O padrão é `PREFIX/share`.

`--datadir=DIRECTORY` [#](#CONFIGURE-OPTION-DATADIR): Define o diretório para arquivos de dados somente de leitura usados pelos programas instalados. O padrão é `DATAROOTDIR`. Observe que isso não tem nada a ver com o local onde seus arquivos de banco de dados serão colocados.

`--localedir=DIRECTORY` [#](#CONFIGURE-OPTION-LOCALEDIR): Define o diretório para a instalação de dados de localização, em particular os arquivos de catálogo de tradução de mensagens. O padrão é `DATAROOTDIR/locale`.

`--mandir=DIRECTORY` [#](#CONFIGURE-OPTION-MANDIR): As páginas do manual que vêm com o PostgreSQL serão instaladas neste diretório, em suas respectivas subdiretórios `manx`. O padrão é `DATAROOTDIR/man`.

`--docdir=DIRECTORY` [#](#CONFIGURE-OPTION-DOCDIR): Define o diretório raiz para a instalação de arquivos de documentação, exceto as páginas do tipo “man”. Este valor apenas define o padrão para as opções a seguir. O valor padrão para esta opção é `DATAROOTDIR/doc/postgresql`.

`--htmldir=DIRECTORY` [#](#CONFIGURE-OPTION-HTMLDIR): A documentação formatada em HTML para PostgreSQL será instalada neste diretório. O padrão é `DATAROOTDIR`.

Nota

Preocupamo-nos em tornar possível instalar o PostgreSQL em locais de instalação compartilhados (como `/usr/local/include`) sem interferir no espaço de nomes do resto do sistema. Primeiro, a string “`/postgresql`” é automaticamente anexada a `datadir`, `sysconfdir` e `docdir`, a menos que o nome de diretório totalmente expandido já contenha a string “`postgres`” ou “`pgsql`”. Por exemplo, se você escolher `/usr/local` como prefixo, a documentação será instalada em `/usr/local/doc/postgresql`, mas se o prefixo for `/opt/postgres`, então ela estará em `/opt/postgres/doc`. Os arquivos de cabeçalho C públicos das interfaces do cliente são instalados em `includedir` e são limpos em termos de espaço de nomes. Os arquivos de cabeçalho internos e os arquivos de cabeçalho do servidor são instalados em diretórios privados sob `includedir`. Consulte a documentação de cada interface para obter informações sobre como acessar seus arquivos de cabeçalho. Finalmente, se apropriado, um subdiretório privado também será criado sob `libdir` para módulos carregáveis dinamicamente.

#### 17.3.3.2. Características do PostgreSQL [#](#CONFIGURE-OPTIONS-FEATURES)

As opções descritas nesta seção permitem a construção de várias funcionalidades do PostgreSQL que não são construídas por padrão. A maioria dessas opções não são padrão apenas porque requerem software adicional, conforme descrito em [Seção 17.1](install-requirements.md).

`--enable-nls[=LANGUAGES]` [#](#CONFIGURE-OPTION-ENABLE-NLS): Habilita o suporte a idioma nativo (NLS), ou seja, a capacidade de exibir as mensagens de um programa em um idioma diferente do inglês. *`LANGUAGES`* é uma lista opcional de códigos separados por espaço das línguas que você deseja que sejam suportados, por exemplo, `--enable-nls='de fr'`. (A interseção entre sua lista e o conjunto de traduções fornecidas automaticamente será calculada automaticamente.) Se você não especificar uma lista, todas as traduções disponíveis serão instaladas.

Para usar essa opção, você precisará de uma implementação da API Gettext.

`--with-perl` [#](#CONFIGURE-OPTION-WITH-PERL): Construa o PL/Perl, o idioma do lado do servidor.

`--with-python` [#](#CONFIGURE-OPTION-WITH-PYTHON): Construa o PL/Python, a linguagem de servidor.

`--with-tcl` [#](#CONFIGURE-OPTION-WITH-TCL): Construa o PL/Tcl, o idioma do lado do servidor.

`--with-tclconfig=DIRECTORY` [#](#CONFIGURE-OPTION-WITH-TCLCONFIG): O Tcl instala o arquivo `tclConfig.sh`, que contém informações de configuração necessárias para construir módulos que interagem com o Tcl. Esse arquivo é normalmente encontrado automaticamente em um local bem conhecido, mas se você deseja usar uma versão diferente do Tcl, pode especificar o diretório em que procurar `tclConfig.sh`.

`--with-llvm` [#](#CONFIGURE-WITH-LLVM): Construa com suporte para compilação JIT (Just-In-Time) baseada em LLVM (consulte o [Capítulo 30](jit.md)). Isso requer que a biblioteca LLVM seja instalada. A versão mínima necessária do LLVM é atualmente 14.

`llvm-config` será usado para encontrar as opções de compilação necessárias. `llvm-config` será procurado em seu `PATH`. Se isso não resultar no programa desejado, use `LLVM_CONFIG` para especificar um caminho para o `llvm-config` correto. Por exemplo

```
./configure ... --with-llvm LLVM_CONFIG='/path/to/llvm/bin/llvm-config'
```

O suporte ao LLVM requer um compilador compatível `clang` (especificado, se necessário, usando a variável de ambiente `CLANG`, e) e um compilador C++ em funcionamento (especificado, se necessário, usando a variável de ambiente `CXX`).

`--with-lz4` [#](#CONFIGURE-OPTION-WITH-LZ4): Construa com suporte à compressão LZ4.

`--with-zstd` [#](#CONFIGURE-OPTION-WITH-ZSTD): Construa com suporte à compressão Zstandard.

`--with-ssl=LIBRARY` [#](#CONFIGURE-OPTION-WITH-SSL): Construa com suporte para conexões SSL (encriptadas). O único *`LIBRARY`* suportado é `openssl`, que é usado tanto para OpenSSL quanto para LibreSSL. Isso requer que o pacote OpenSSL esteja instalado. `configure` verificará os arquivos de cabeçalho e as bibliotecas necessárias para garantir que sua instalação OpenSSL seja suficiente antes de prosseguir.

`--with-openssl` [#](#CONFIGURE-OPTION-WITH-OPENSSL): Equivalente obsoleto de `--with-ssl=openssl`.

`--with-gssapi` [#](#CONFIGURE-OPTION-WITH-GSSAPI): Construa com suporte para autenticação GSSAPI. O MIT Kerberos é necessário para ser instalado para GSSAPI. Em muitos sistemas, o sistema GSSAPI (uma parte da instalação MIT Kerberos) não está instalado em um local que é pesquisado por padrão (por exemplo, `/usr/include`, `/usr/lib`), então você deve usar as opções `--with-includes` e `--with-libraries` além desta opção. `configure` verificará os arquivos de cabeçalho e bibliotecas necessários para garantir que sua instalação GSSAPI seja suficiente antes de prosseguir.

`--with-ldap` [#](#CONFIGURE-OPTION-WITH-LDAP): Construa com suporte LDAP para busca de parâmetros de autenticação e conexão (consulte [Seção 32.18](libpq-ldap.md "32.18. LDAP Lookup of Connection Parameters") e [Seção 20.10](auth-ldap.md "20.10. LDAP Authentication") para mais informações). Em Unix, isso requer que o pacote OpenLDAP seja instalado. Em Windows, a biblioteca WinLDAP padrão é usada. `configure` verificará os arquivos de cabeçalho e bibliotecas necessários para garantir que sua instalação OpenLDAP seja suficiente antes de prosseguir.

`--with-pam` [#](#CONFIGURE-OPTION-WITH-PAM): Construa com suporte a PAM (Módulos de Autenticação Conectam-se).

`--with-bsd-auth` [#](#CONFIGURE-OPTION-WITH-BSD-AUTH): Construa com suporte à Autenticação BSD. (O framework de Autenticação BSD está atualmente disponível apenas no OpenBSD.)

`--with-systemd` [#](#CONFIGURE-OPTION-WITH-SYSTEMD): Construa com suporte para notificações de serviço systemd. Isso melhora a integração se o servidor for iniciado sob o systemd, mas não tem impacto caso contrário; consulte [Seção 18.3](server-start.md "18.3. Starting the Database Server") para mais informações. As bibliotecas libsystemd e os arquivos de cabeçalho associados precisam ser instalados para usar essa opção.

`--with-bonjour` [#](#CONFIGURE-OPTION-WITH-BONJOUR): Construa com suporte para detecção automática de serviços Bonjour. Isso requer suporte Bonjour em seu sistema operacional. Recomendado em macOS.

`--with-uuid=LIBRARY` [#](#CONFIGURE-OPTION-WITH-UUID): Construa o módulo [uuid-ossp](uuid-ossp.md "F.49. uuid-ossp — a UUID generator") (que fornece funções para gerar UUIDs), usando a biblioteca de UUID especificada. *`LIBRARY`* deve ser um dos:

* `bsd` para usar as funções UUID encontradas no FreeBSD e em alguns outros sistemas derivados do BSD * `e2fs` para usar a biblioteca UUID criada pelo projeto `e2fsprogs`; essa biblioteca está presente na maioria dos sistemas Linux e no macOS, e também pode ser obtida para outras plataformas * `ossp` para usar a biblioteca [OSSP UUID](http://www.ossp.org/pkg/lib/uuid/)

`--with-ossp-uuid` [#](#CONFIGURE-OPTION-WITH-OSSP-UUID): Equivalente obsoleto de `--with-uuid=ossp`.

`--with-libcurl` [#](#CONFIGURE-OPTION-WITH-LIBCURL): Construa com suporte ao libcurl para fluxos de cliente OAuth 2.0. A versão 7.61.0 ou posterior do Libcurl é necessária para essa funcionalidade. Ao construir com isso, ele verificará os arquivos de cabeçalho e as bibliotecas necessárias para garantir que sua instalação do curl seja suficiente antes de prosseguir.

`--with-libnuma` [#](#CONFIGURE-OPTION-WITH-LIBNUMA): Construa com suporte à libnuma para suporte básico NUMA. Apenas suportado em plataformas para as quais a biblioteca libnuma é implementada.

`--with-liburing` [#](#CONFIGURE-OPTION-WITH-LIBURING): Construa com liburing, habilitando o suporte io_uring para I/O assíncrono.

Para detectar as opções de compilador e encadeador necessárias, o PostgreSQL consultará `pkg-config`.

Para usar uma instalação de liburing em um local incomum, você pode definir variáveis de ambiente relacionadas ao `pkg-config` (consulte a documentação).

`--with-libxml` [#](#CONFIGURE-OPTION-WITH-LIBXML): Construa com libxml2, habilitando o suporte SQL/XML. É necessária a versão 2.6.23 ou posterior do Libxml2 para essa funcionalidade.

Para detectar as opções necessárias do compilador e do encadeador, o PostgreSQL consultará `pkg-config`, se estiver instalado e saiba sobre o libxml2. Caso contrário, o programa `xml2-config`, que é instalado pelo libxml2, será usado se for encontrado. O uso de `pkg-config` é preferido, pois pode lidar melhor com instalações multi-arquitetura.

Para usar uma instalação do libxml2 em um local incomum, você pode definir variáveis de ambiente relacionadas ao `pkg-config` (consulte sua documentação) ou definir a variável de ambiente `XML2_CONFIG` para apontar para o programa `xml2-config` pertencente à instalação do libxml2, ou definir as variáveis `XML2_CFLAGS` e `XML2_LIBS`. (Se o `pkg-config` estiver instalado, então, para substituir sua ideia de onde está o libxml2, você deve definir `XML2_CONFIG` ou definir tanto `XML2_CFLAGS` quanto `XML2_LIBS` como strings não vazias.)

`--with-libxslt` [#](#CONFIGURE-OPTION-WITH-LIBXSLT): Construa com libxslt, habilitando o módulo [xml2](xml2.md "F.50. xml2 — XPath querying and XSLT functionality") para realizar transformações XSL de XML. `--with-libxml` também deve ser especificado.

`--with-selinux` [#](#CONFIGURE-OPTION-WITH-SEPGSQL): Construa com suporte SElinux, habilitando a extensão do módulo de segurança [sepgsql](sepgsql.md "F.40. sepgsql — SELinux-, label-based mandatory access control (MAC)).

#### 17.3.3.3. Funções anti [#](#CONFIGURE-OPTIONS-ANTI-FEATURES)

As opções descritas nesta seção permitem desabilitar certos recursos do PostgreSQL que são construídos por padrão, mas que podem precisar ser desativados se os recursos de software ou sistema necessários não estiverem disponíveis. Não é recomendado usar essas opções, a menos que seja realmente necessário.

`--without-icu` [#](#CONFIGURE-OPTION-WITHOUT-ICU): Construa sem suporte para a biblioteca ICU, desativando o uso das características de ordenação ICU (consulte [Seção 23.2](collation.md "23.2. Collation Support")).

`--without-readline` [#](#CONFIGURE-OPTION-WITHOUT-READLINE): Previne o uso da biblioteca Readline (e também do libedit). Esta opção desativa a edição de linha de comando e o histórico no psql.

`--with-libedit-preferred` [#](#CONFIGURE-OPTION-WITH-LIBEDIT-PREFERRED): Favorece o uso da biblioteca libedit licenciada pela BSD em vez da Readline licenciada pela GPL. Esta opção é significativa apenas se você tiver ambas as bibliotecas instaladas; o padrão nesse caso é usar a Readline.

`--without-zlib` [#](#CONFIGURE-OPTION-WITHOUT-ZLIB): Previne o uso da biblioteca Zlib. Isso desativa o suporte para arquivos comprimidos em pg_dump e pg_restore.

#### 17.3.3.4. Detalhes do processo de construção [#](#CONFIGURE-OPTIONS-BUILD-PROCESS)

`--with-includes=DIRECTORIES` [#](#CONFIGURE-OPTION-WITH-INCLUDES): *`DIRECTORIES`* é uma lista de diretórios separados por vírgula que será adicionada à lista em que o compilador busca arquivos de cabeçalho. Se você tiver pacotes opcionais (como GNU Readline) instalados em um local não padrão, você deve usar essa opção e, provavelmente, também a opção correspondente `--with-libraries`.

Exemplo: `--with-includes=/opt/gnu/include:/usr/sup/include`.

`--with-libraries=DIRECTORIES` [#](#CONFIGURE-OPTION-WITH-LIBRARIES): *`DIRECTORIES`* é uma lista de diretórios separados por vírgula para procurar bibliotecas. Você provavelmente terá que usar essa opção (e a opção correspondente `--with-includes`), se tiver pacotes instalados em locais não padrão.

Exemplo: `--with-libraries=/opt/gnu/lib:/usr/sup/lib`.

`--with-system-tzdata=DIRECTORY` [#](#CONFIGURE-OPTION-WITH-SYSTEM-TZDATA): O PostgreSQL inclui seu próprio banco de dados de fuso horário, que ele exige para operações de data e hora. Esse banco de dados de fuso horário é, de fato, compatível com o banco de dados de fuso horário IANA fornecido por muitos sistemas operacionais, como FreeBSD, Linux e Solaris, portanto, seria redundante instalá-lo novamente. Quando esta opção é usada, o banco de dados de fuso horário fornecido pelo sistema em *`DIRECTORY`* é usado em vez do que está incluído na distribuição de fonte do PostgreSQL. *`DIRECTORY`* deve ser especificado como um caminho absoluto. `/usr/share/zoneinfo` é um diretório provável em alguns sistemas operacionais. Note que a rotina de instalação não detectará dados de fuso horário incompatíveis ou errados. Se você usar esta opção, é aconselhável executar os testes de regressão para verificar se os dados de fuso horário que você apontou funcionam corretamente com o PostgreSQL.

Esta opção é destinada principalmente a distribuidores de pacotes binários que conhecem bem o seu sistema operacional alvo. A principal vantagem de usar esta opção é que o pacote PostgreSQL não precisará ser atualizado sempre que alguma das muitas regras locais de horário de verão mudar. Outra vantagem é que o PostgreSQL pode ser compilado de forma mais direta se os arquivos do banco de dados de fuso horário não precisarem ser construídos durante a instalação.

`--with-extra-version=STRING` [#](#CONFIGURE-OPTION-WITH-EXTRA-VERSION): Adicione *`STRING`* ao número da versão do PostgreSQL. Você pode usar isso, por exemplo, para marcar binários construídos a partir de snapshots do Git não lançados ou que contenham patches personalizados com uma string de versão extra, como um identificador `git describe` ou um número de lançamento de pacote de distribuição.

`--disable-rpath` [#](#CONFIGURE-OPTION-DISABLE-RPATH): Não marque os executáveis do PostgreSQL para indicar que eles devem procurar bibliotecas compartilhadas no diretório de bibliotecas da instalação (consulte `--libdir`). Na maioria das plataformas, essa marcação usa um caminho absoluto para o diretório de bibliotecas, para que não seja útil se você relocar a instalação posteriormente. No entanto, você precisará fornecer outra maneira para os executáveis encontrarem as bibliotecas compartilhadas. Normalmente, isso requer configurar o link dinâmico do sistema operacional para procurar o diretório de bibliotecas; consulte [Seção 17.5.1](install-post.md#INSTALL-POST-SHLIBS "17.5.1. Shared Libraries") para mais detalhes.

#### 17.3.3.5. Diversos [#](#CONFIGURE-OPTIONS-MISC)

É bastante comum, especialmente em builds de teste, ajustar o número de porta padrão com `--with-pgport`. As outras opções nesta seção são recomendadas apenas para usuários avançados.

`--with-pgport=NUMBER` [#](#CONFIGURE-OPTION-WITH-PGPORT): Configure *`NUMBER`* como o número de porta padrão para o servidor e os clientes. O padrão é 5432. A porta pode ser alterada posteriormente, mas se você especificar aqui, o servidor e os clientes terão o mesmo valor padrão compilado, o que pode ser muito conveniente. Geralmente, a única boa razão para selecionar um valor não padrão é se você pretende executar vários servidores PostgreSQL na mesma máquina.

`--with-krb-srvnam=NAME` [#](#CONFIGURE-OPTION-WITH-KRB-SRVNAM): O nome padrão do principal do serviço Kerberos usado pelo GSSAPI. `postgres` é o padrão. Geralmente, não há motivo para alterar isso, a menos que você esteja construindo para um ambiente Windows, no qual caso, ele deve ser definido em maiúsculas `POSTGRES`.

`--with-segsize=SEGSIZE` [#](#CONFIGURE-OPTION-WITH-SEGSIZE): Defina o *tamanho do segmento*, em gigabytes. As tabelas grandes são divididas em vários arquivos do sistema operacional, cada um com um tamanho igual ao tamanho do segmento. Isso evita problemas com limites de tamanho de arquivo que existem em muitas plataformas. O tamanho de segmento padrão, 1 gigabyte, é seguro em todas as plataformas suportadas. Se o seu sistema operacional tiver suporte para "largefile" (o que a maioria tem, atualmente), você pode usar um tamanho de segmento maior. Isso pode ser útil para reduzir o número de descritores de arquivo consumidos ao trabalhar com tabelas muito grandes. Mas tenha cuidado para não selecionar um valor maior do que o suportado pela sua plataforma e pelos sistemas de arquivos que você pretende usar. Outras ferramentas que você pode querer usar, como tar, também podem definir limites no tamanho de arquivo utilizável. É recomendado, embora não seja absolutamente necessário, que esse valor seja um poder de 2. Note que alterar esse valor quebra a compatibilidade do banco de dados em disco, o que significa que você não pode usar `pg_upgrade` para fazer uma atualização para uma compilação com um tamanho de segmento diferente.

`--with-blocksize=BLOCKSIZE` [#](#CONFIGURE-OPTION-WITH-BLOCKSIZE): Defina o *tamanho do bloco*, em kilobytes. Essa é a unidade de armazenamento e de entrada/saída dentro das tabelas. O padrão, de 8 kilobytes, é adequado para a maioria das situações; mas outros valores podem ser úteis em casos especiais. O valor deve ser um expoente de 2 entre 1 e 32 (kilobytes). Observe que alterar esse valor quebra a compatibilidade do banco de dados no disco, o que significa que você não pode usar `pg_upgrade` para atualizar para uma compilação com um tamanho de bloco diferente.

`--with-wal-blocksize=BLOCKSIZE` [#](#CONFIGURE-OPTION-WITH-WAL-BLOCKSIZE): Defina o *tamanho do bloco WAL*, em kilobytes. Essa é a unidade de armazenamento e de entrada/saída dentro do log WAL. O padrão, de 8 kilobytes, é adequado para a maioria das situações; mas outros valores podem ser úteis em casos especiais. O valor deve ser um expoente de 2 entre 1 e 64 (kilobytes). Observe que alterar esse valor quebra a compatibilidade do banco de dados em disco, o que significa que você não pode usar `pg_upgrade` para atualizar para uma versão com um tamanho de bloco WAL diferente.

#### 17.3.3.6. Opções do Desenvolvedor [#](#CONFIGURE-OPTIONS-DEVEL)

A maioria das opções desta seção é de interesse apenas para o desenvolvimento ou depuração do PostgreSQL. Não são recomendadas para edições de produção, exceto para `--enable-debug`, que pode ser útil para habilitar relatórios de bugs detalhados no caso improvável de você encontrar um bug. Em plataformas que suportam DTrace, `--enable-dtrace` também pode ser razoável para uso em produção.

Ao construir uma instalação que será usada para desenvolver código dentro do servidor, é recomendável usar pelo menos as opções `--enable-debug` e `--enable-cassert`.

`--enable-debug` [#](#CONFIGURE-OPTION-ENABLE-DEBUG): Compila todos os programas e bibliotecas com símbolos de depuração. Isso significa que você pode executar os programas em um depurador para analisar problemas. Isso aumenta consideravelmente o tamanho dos executables instalados, e em compiladores que não são do GCC, geralmente também desabilita a otimização do compilador, causando lentidão. No entanto, ter os símbolos disponíveis é extremamente útil para lidar com quaisquer problemas que possam surgir. Atualmente, essa opção é recomendada apenas para instalações de produção se você usar o GCC. Mas você deve sempre tê-la se estiver fazendo trabalho de desenvolvimento ou executando uma versão beta.

`--enable-cassert` [#](#CONFIGURE-OPTION-ENABLE-CASSERT): Habilita verificações de *afirmação* no servidor, que testam muitas condições de "não pode acontecer". Isso é inestimável para fins de desenvolvimento de código, mas os testes podem desacelerar significativamente o servidor. Além disso, ter os testes ativados não necessariamente melhora a estabilidade do seu servidor! As verificações de afirmação não são categorizadas por gravidade, e o que pode ser um bug relativamente inofensivo ainda levará a reinicializações do servidor se ele desencadear uma falha de afirmação. Esta opção não é recomendada para uso em produção, mas você deve tê-la ativada para trabalho de desenvolvimento ou ao executar uma versão beta.

`--enable-tap-tests` [#](#CONFIGURE-OPTION-ENABLE-TAP-TESTS): Habilite os testes usando as ferramentas Perl TAP. Isso requer uma instalação do Perl e o módulo Perl `IPC::Run`. Consulte [Seção 31.4](regress-tap.md "31.4. TAP Tests") para obter mais informações.

`--enable-depend` [#](#CONFIGURE-OPTION-ENABLE-DEPEND): Habilita o rastreamento automático de dependências. Com esta opção, os makefiles são configurados para que todos os arquivos de objeto afetados sejam reconstruídos quando qualquer arquivo de cabeçalho for alterado. Isso é útil se você estiver fazendo trabalho de desenvolvimento, mas é apenas um desperdício se você pretender apenas compilar uma vez e instalar. Atualmente, esta opção só funciona com o GCC.

`--enable-coverage` [#](#CONFIGURE-OPTION-ENABLE-COVERAGE): Se estiver usando o GCC, todos os programas e bibliotecas são compilados com instrumentação de teste de cobertura de código. Quando executados, eles geram arquivos no diretório de construção com métricas de cobertura de código. Consulte [Seção 31.5](regress-coverage.md "31.5. Test Coverage Examination") para obter mais informações. Esta opção é para uso apenas com o GCC e quando estiver realizando trabalho de desenvolvimento.

`--enable-profiling` [#](#CONFIGURE-OPTION-ENABLE-PROFILING): Se estiver usando o GCC, todos os programas e bibliotecas são compilados para que possam ser analisados. Na saída do backend, será criado um subdiretório que contém o arquivo `gmon.out` contendo os dados do perfil. Esta opção é para uso apenas com o GCC e quando estiver fazendo trabalho de desenvolvimento.

`--enable-dtrace` [#](#CONFIGURE-OPTION-ENABLE-DTRACE): Compila o PostgreSQL com suporte para a ferramenta de rastreamento dinâmico DTrace. Consulte [Seção 27.5](dynamic-trace.md "27.5. Dynamic Tracing") para mais informações.

Para apontar para o programa `dtrace`, a variável de ambiente `DTRACE` pode ser definida. Isso geralmente será necessário, pois o `dtrace` é tipicamente instalado sob `/usr/sbin`, que pode não estar em seu `PATH`.

Opções adicionais de linha de comando para o programa `dtrace` podem ser especificadas na variável de ambiente `DTRACEFLAGS`. Em Solaris, para incluir suporte ao DTrace em um binário de 64 bits, você deve especificar `DTRACEFLAGS="-64"`. Por exemplo, usando o compilador GCC:

```
./configure CC='gcc -m64' --enable-dtrace DTRACEFLAGS='-64' ...
```

Usando o compilador da Sun:

```
./configure CC='/opt/SUNWspro/bin/cc -xtarget=native64' --enable-dtrace DTRACEFLAGS='-64' ...
```

`--enable-injection-points` [#](#CONFIGURE-OPTION-ENABLE-INJECTION-POINTS): Compila o PostgreSQL com suporte para pontos de injeção no servidor. Os pontos de injeção permitem executar código definido pelo usuário dentro do servidor em caminhos de código pré-definidos. Isso ajuda a testar e investigar cenários de concorrência de maneira controlada. Esta opção é desativada por padrão. Consulte [Seção 36.10.14](xfunc-c.md#XFUNC-ADDIN-INJECTION-POINTS "36.10.14. Injection Points") para mais detalhes. Esta opção é destinada a ser usada apenas por desenvolvedores para testes.

`--with-segsize-blocks=SEGSIZE_BLOCKS` [#](#CONFIGURE-OPTION-WITH-SEGSIZE-BLOCKS): Especifique o tamanho do segmento de relação em blocos. Se ambos `--with-segsize` e esta opção forem especificados, esta opção vence. Esta opção é apenas para desenvolvedores, para testar código relacionado ao segmento.

### 17.3.4. `configure` Variáveis de ambiente [#](#CONFIGURE-ENVVARS)

Além das opções comuns de linha de comando descritas acima, o `configure` responde a uma série de variáveis de ambiente. Você pode especificar variáveis de ambiente na linha de comando do comando `configure`, por exemplo:

```
./configure CC=/opt/bin/gcc CFLAGS='-O2 -pipe'
```

Nesse caso, uma variável de ambiente é pouco diferente de uma opção de linha de comando. Você também pode definir essas variáveis previamente:

```
export CC=/opt/bin/gcc export CFLAGS='-O2 -pipe' ./configure
```

Essa utilização pode ser conveniente, pois muitos scripts de configuração de programas respondem a essas variáveis de maneira semelhante.

Os mais comumente utilizados dessas variáveis de ambiente são `CC` e `CFLAGS`. Se você prefere um compilador C diferente do que o `configure` escolhe, pode definir a `CC` como o programa de sua escolha. Por padrão, `configure` escolherá `gcc` se disponível, caso contrário, a padrão da plataforma (geralmente `cc`). Da mesma forma, você pode substituir as marcas de compilação padrão, se necessário, com a `CFLAGS` variável.

Aqui está uma lista das variáveis significativas que podem ser definidas dessa maneira:

`BISON` [#](#CONFIGURE-ENVVARS-BISON): Programa de bisão

`CC` [#](#CONFIGURE-ENVVARS-CC): Compilador C

`CFLAGS` [#](#CONFIGURE-ENVVARS-CFLAGS): opções para passar ao compilador C

`CLANG` [#](#CONFIGURE-ENVVARS-CLANG): caminho para o programa `clang` usado para processar código-fonte para inlining ao compilar com `--with-llvm`

`CPP` [#](#CONFIGURE-ENVVARS-CPP) : pré-processador C

`CPPFLAGS` [#](#CONFIGURE-ENVVARS-CPPFLAGS): opções para passar ao pré-processador C

`CXX` [#](#CONFIGURE-ENVVARS-CXX): Compilador de C++

`CXXFLAGS` [#](#CONFIGURE-ENVVARS-CXXFLAGS): opções para passar ao compilador C++

`DTRACE` [#](#CONFIGURE-ENVVARS-DTRACE): localização do programa `dtrace`

`DTRACEFLAGS` [#](#CONFIGURE-ENVVARS-DTRACEFLAGS): opções para passar para o programa `dtrace`

`FLEX` [#](#CONFIGURE-ENVVARS-FLEX): Programa Flex

`LDFLAGS` [#](#CONFIGURE-ENVVARS-LDFLAGS): opções a serem usadas ao vincular execuções ou bibliotecas compartilhadas

`LDFLAGS_EX` [#](#CONFIGURE-ENVVARS-LDFLAGS-EX): opções adicionais para vincular executaveis apenas

`LDFLAGS_SL` [#](#CONFIGURE-ENVVARS-LDFLAGS-SL): opções adicionais para vincular bibliotecas compartilhadas apenas

`LLVM_CONFIG` [#](#CONFIGURE-ENVVARS-LLVM-CONFIG): programa usado para localizar a instalação do LLVM `llvm-config`

`MSGFMT` [#](#CONFIGURE-ENVVARS-MSGFMT): `msgfmt` programa de suporte ao idioma nativo

`PERL` [#](#CONFIGURE-ENVVARS-PERL): Programa do interpretador Perl. Este será usado para determinar as dependências para a construção do PL/Perl. O padrão é `perl`.

`PYTHON` [#](#CONFIGURE-ENVVARS-PYTHON): Programa do interpretador Python. Este será usado para determinar as dependências para a construção do PL/Python. Se não for definido, o seguinte será verificado nesta ordem: `python3 python`.

`TCLSH` [#](#CONFIGURE-ENVVARS-TCLSH): programa do interpretador Tcl. Este será usado para determinar as dependências para a construção do PL/Tcl. Se não for definido, o seguinte será verificado nesta ordem: `tclsh tcl tclsh8.6 tclsh86 tclsh8.5 tclsh85 tclsh8.4 tclsh84`.

`XML2_CONFIG` [#](#CONFIGURE-ENVVARS-XML2-CONFIG): programa usado para localizar a instalação do libxml2

Às vezes, é útil adicionar marcas do compilador após o fato ao conjunto que foi escolhido por `configure`. Um exemplo importante é que a opção `-Werror` do gcc não pode ser incluída no `CFLAGS` passado para `configure`, porque isso quebrará muitos dos testes internos do `configure`. Para adicionar tais marcas, inclua-as na variável de ambiente `COPT` enquanto executa `make`. O conteúdo de `COPT` é adicionado aos conjuntos de opções `CFLAGS`, `CXXFLAGS` e `LDFLAGS` configurados por `configure`. Por exemplo, você pode fazer

```
make COPT='-Werror'
```

ou

```
export COPT='-Werror' make
```

Nota

Se estiver usando o GCC, é melhor compilar com um nível de otimização de pelo menos `-O1`, porque usar nenhum nível de otimização (`-O0`) desativa algumas advertências importantes do compilador (como o uso de variáveis não inicializadas). No entanto, níveis de otimização não nulos podem complicar a depuração, porque a execução de código compilado geralmente não corresponderá de forma direta com as linhas do código-fonte. Se você ficar confuso ao tentar depurar código otimizado, recomponha os arquivos específicos de interesse com `-O0`. Uma maneira fácil de fazer isso é passando uma opção para o make: `make PROFILE=-O0 file.o`.

As variáveis de ambiente `COPT` e `PROFILE` são, na verdade, manipuladas de maneira idêntica pelos makefiles do PostgreSQL. A escolha de qual usar é uma questão de preferência, mas um hábito comum entre os desenvolvedores é usar `PROFILE` para ajustes de bandeira temporários, enquanto `COPT` pode ser mantido configurado o tempo todo.