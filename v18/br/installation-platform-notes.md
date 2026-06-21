## 17.7. Notas específicas da plataforma [#](#INSTALLATION-PLATFORM-NOTES)

* [17.7.1. Cygwin][(installation-platform-notes.md#INSTALLATION-NOTES-CYGWIN)
* [17.7.2. macOS][(installation-platform-notes.md#INSTALLATION-NOTES-MACOS)
* [17.7.3. MinGW][(installation-platform-notes.md#INSTALLATION-NOTES-MINGW)
* [17.7.4. Solaris][(installation-platform-notes.md#INSTALLATION-NOTES-SOLARIS)
* [17.7.5. Visual Studio][(installation-platform-notes.md#INSTALLATION-NOTES-VISUAL-STUDIO)

Esta seção documenta questões adicionais específicas da plataforma em relação à instalação e configuração do PostgreSQL. Certifique-se de ler as instruções de instalação e, em particular, [Seção 17.1][(install-requirements.md "17.1. Requirements")] também. Além disso, verifique [Capítulo 31][(regress.md "Chapter 31. Regression Tests")] em relação à interpretação dos resultados dos testes de regressão.

As plataformas que não estão aqui mencionadas não apresentam problemas de instalação específicos da plataforma.

### 17.7.1. Cygwin [#](#INSTALLATION-NOTES-CYGWIN)

O PostgreSQL pode ser construído usando o Cygwin, um ambiente semelhante ao Linux para Windows, mas esse método é inferior à versão nativa do Windows e não é mais recomendado executar um servidor sob o Cygwin.

Ao construir a partir de fonte, proceda de acordo com o procedimento de instalação de estilo Unix (ou seja, `./configure; make`; etc.), observando as seguintes diferenças específicas do Cygwin:

* Defina seu caminho para usar o diretório de binários do Cygwin antes das utilidades do Windows. Isso ajudará a evitar problemas com a compilação.
* O comando `adduser` não é suportado; use o aplicativo apropriado de gerenciamento de usuários no Windows. Caso contrário, ignore este passo.
* O comando `su` não é suportado; use o ssh para simular su no Windows. Caso contrário, ignore este passo.
* O OpenSSL não é suportado.
* Inicie `cygserver` para suporte de memória compartilhada. Para fazer isso, insira o comando `/usr/sbin/cygserver &`. Este programa precisa estar em execução sempre que você iniciar o servidor PostgreSQL ou inicializar um clúster de banco de dados (`initdb`). A configuração padrão `cygserver` pode precisar ser alterada (por exemplo, aumentar `SEMMNS`) para evitar que o PostgreSQL falhe devido à falta de recursos do sistema.
* A construção pode falhar em alguns sistemas onde um local diferente de C está em uso. Para corrigir isso, defina o local para C fazendo `export LANG=C.utf8` antes da construção, e depois definindo-o de volta para o ajuste anterior após ter instalado o PostgreSQL.
* Os testes de regressão paralelos (`make check`) podem gerar falhas espúrias nos testes de regressão devido ao esvaziamento da fila de `listen()` de backlog, o que causa erros de conexão recusada ou travamento. Você pode limitar o número de conexões usando a variável make `MAX_CONNECTIONS` assim:

  ```
  make MAX_CONNECTIONS=5 check
  ```

(Em alguns sistemas, você pode ter até cerca de 10 conexões simultâneas.)

É possível instalar o `cygserver` e o servidor PostgreSQL como serviços do Windows NT. Para obter informações sobre como fazer isso, consulte o documento `README` incluído no pacote binário do PostgreSQL no Cygwin. Ele está instalado no diretório `/usr/share/doc/Cygwin`.

### 17.7.2. macOS [#](#INSTALLATION-NOTES-MACOS)

Para construir o PostgreSQL a partir do código-fonte no macOS, você precisará instalar as ferramentas de linha de comando do desenvolvedor da Apple, que podem ser feitas emitindo

```
xcode-select --install
```

(observe que isso abrirá uma janela de diálogo de interface gráfica para confirmação). Você pode ou não desejar instalar o Xcode.

Em versões recentes do macOS, é necessário incorporar o caminho "sysroot" nos switches de inclusão usados para encontrar alguns arquivos de cabeçalho do sistema. Isso resulta em saídas do script de configuração variando dependendo da versão do SDK que foi usada durante a configuração. Isso não deve representar nenhum problema em cenários simples, mas se você está tentando fazer algo como construir uma extensão em uma máquina diferente daquela em que o código do servidor foi construído, você pode precisar forçar o uso de um caminho de sysroot diferente. Para fazer isso, defina `PG_SYSROOT`, por exemplo

```
make PG_SYSROOT=/desired/path all
```

Para descobrir o caminho apropriado na sua máquina, execute

```
xcrun --show-sdk-path
```

Observe que não é realmente recomendado construir uma extensão usando uma versão diferente da sysroot que foi usada para construir o servidor principal; no pior dos casos, isso pode resultar em inconsistências de ABI difíceis de depurar.

Você também pode selecionar um caminho de sysroot não padrão ao configurar, especificando `PG_SYSROOT` para configurar:

```
./configure ... PG_SYSROOT=/desired/path
```

Isso seria útil principalmente para a compilação cruzada para algumas outras versões do macOS. Não há garantia de que os executables resultantes serão executados no host atual.

Para suprimir as opções do `-isysroot` por completo, use

```
./configure ... PG_SYSROOT=none
```

(qualquer caminho não existente funcionará). Isso pode ser útil se você deseja construir com um compilador que não é da Apple, mas tenha cuidado com o fato de que esse caso não é testado ou suportado pelos desenvolvedores do PostgreSQL.

O recurso de Proteção de Integridade do Sistema (SIP) do macOS quebra o `make check`, pois impede a passagem da configuração necessária do `DYLD_LIBRARY_PATH` para os executables que estão sendo testados. Você pode contornar isso fazendo `make install` antes de `make check`. A maioria dos desenvolvedores do PostgreSQL simplesmente desativa o SIP.

### 17.7.3. MinGW [#](#INSTALLATION-NOTES-MINGW)

O PostgreSQL para Windows pode ser construído usando MinGW, um ambiente de construção semelhante ao Unix para Windows. É recomendável usar o ambiente [MSYS2][(https://www.msys2.org/)] para isso e também instalar quaisquer pacotes pré-requisitos.

#### 17.7.3.1. Coleta de Dumps de Acidente [#](#MINGW-CRASH-DUMPS)

Se o PostgreSQL no Windows falhar, ele tem a capacidade de gerar minidumps que podem ser usados para identificar a causa do falhanço, semelhante aos core dumps no Unix. Esses dumps podem ser lidos usando as Ferramentas de depuração do Windows ou usando o Visual Studio. Para habilitar a geração de dumps no Windows, crie um subdiretório chamado `crashdumps` dentro do diretório de dados do cluster. Os dumps serão então escritos neste diretório com um nome único baseado no identificador do processo que falhou e no horário atual do falhanço.

### 17.7.4. Solaris [#](#INSTALLATION-NOTES-SOLARIS)

O PostgreSQL é bem suportado no Solaris. Quanto mais atualizado o seu sistema operacional, menos problemas você terá.

#### 17.7.4.1. Ferramentas necessárias [#](#INSTALLATION-NOTES-SOLARIS-REQ-TOOLS)

Você pode construir com o GCC ou a suite de compiladores da Sun. Para uma melhor otimização do código, a compiladora da Sun é fortemente recomendada na arquitetura SPARC. Se você estiver usando a compiladora da Sun, tenha cuidado para não selecionar `/usr/ucb/cc`; use `/opt/SUNWspro/bin/cc`.

Você pode baixar o Sun Studio em <https://www.oracle.com/technetwork/server-storage/solarisstudio/downloads/>. Muitas ferramentas GNU são integradas ao Solaris 10, ou estão presentes no CD de acompanhamento do Solaris. Se você precisar de pacotes para versões mais antigas do Solaris, você pode encontrar essas ferramentas em <http://www.sunfreeware.com>. Se você prefere fontes, veja <https://www.gnu.org/prep/ftp>.

#### 17.7.4.2. configurar Reclamações sobre um programa de teste falhado [#](#INSTALLATION-NOTES-SOLARIS-CONFIGURE-COMPLAINS)

Se o `configure` reclamar sobre um programa de teste falhado, provavelmente é um caso de o linkador de tempo de execução não conseguir encontrar alguma biblioteca, provavelmente libz, libreadline ou alguma outra biblioteca não padrão, como libssl. Para apontá-la para o local correto, defina a variável de ambiente `LDFLAGS` na linha de comando do comando `configure`, por exemplo:

```
configure ... LDFLAGS="-R /usr/sfw/lib:/opt/sfw/lib:/usr/local/lib"
```

Veja a página de manual para mais informações.

#### 17.7.4.3. Compilação para Desempenho Óptimo [#](#INSTALLATION-NOTES-SOLARIS-COMP-OPT-PERF)

Na arquitetura SPARC, o Sun Studio é fortemente recomendado para compilação. Tente usar a bandeira de otimização `-xO5` para gerar binários significativamente mais rápidos. Não use nenhuma bandeira que modifique o comportamento das operações de ponto flutuante e o processamento `errno` (por exemplo, `-fast`).

Se você não tem uma razão para usar binários de 64 bits no SPARC, prefira a versão de 32 bits. As operações de 64 bits são mais lentas e os binários de 64 bits são mais lentos do que as variantes de 32 bits. Por outro lado, o código de 32 bits na família de CPU AMD64 não é nativo, então o código de 32 bits é significativamente mais lento nessa família de CPU.

#### 17.7.4.4. Usando DTrace para rastrear o PostgreSQL [#](#INSTALLATION-NOTES-SOLARIS-USING-DTRACE)

Sim, é possível usar o DTrace. Consulte a Seção 27.5 [(dynamic-trace.md "27.5. Dynamic Tracing")] para obter mais informações.

Se você ver a ligação do executável `postgres` abortar com uma mensagem de erro como:

```
Undefined                       first referenced
 symbol                             in file
AbortTransaction                    utils/probes.o
CommitTransaction                   utils/probes.o
ld: fatal: Symbol referencing errors. No output written to postgres
collect2: ld returned 1 exit status
make: *** [postgres] Error 1
```

sua instalação DTrace é muito antiga para lidar com sondas em funções estáticas. Você precisa do Solaris 10u4 ou uma versão mais recente para usar o DTrace.

### 17.7.5. Visual Studio [#](#INSTALLATION-NOTES-VISUAL-STUDIO)

Recomenda-se que a maioria dos usuários baixe a distribuição binária para Windows, disponível como um pacote de instalador gráfico no site do PostgreSQL em <https://www.postgresql.org/download/>. A construção a partir de fonte é destinada apenas a pessoas que estão desenvolvendo o PostgreSQL ou extensões.

O PostgreSQL para Windows com o Visual Studio pode ser construído usando o Meson, conforme descrito em [Seção 17.4][(install-meson.md "17.4. Building and Installation with Meson")]. A versão nativa do Windows requer uma versão de 32 ou 64 bits do Windows 10 ou posterior.

As versões nativas do psql não suportam edição de linha de comando. A versão do Cygwin suporta edição de linha de comando, então ela deve ser usada quando o psql é necessário para uso interativo no Windows.

O PostgreSQL pode ser construído usando o conjunto de compiladores Visual C++ da Microsoft. Esses compiladores podem ser obtidos a partir do Visual Studio, do Visual Studio Express ou de algumas versões do SDK do Microsoft Windows. Se você ainda não tem um ambiente do Visual Studio configurado, as maneiras mais fáceis são usar os compiladores do Visual Studio 2022 ou os do SDK do Windows 10, que são ambos downloads gratuitos da Microsoft.

Tanto as versões de 32 bits quanto as de 64 bits são possíveis com o conjunto de compiladores da Microsoft. As versões de PostgreSQL de 32 bits são possíveis com o Visual Studio 2015 ao Visual Studio 2022, bem como versões independentes do Windows SDK 10 e superiores. As versões de PostgreSQL de 64 bits são suportadas com o Windows SDK da Microsoft versão 10 e superior ou o Visual Studio 2015 e superior.

Se o ambiente de construção não vem com uma versão compatível do Microsoft Windows SDK, é recomendável que você atualize para a versão mais recente (atualmente a versão 10), disponível para download em <https://www.microsoft.com/download>.

Você deve sempre incluir a parte de Cabeçalhos e Bibliotecas do Windows do SDK. Se você instalar um SDK do Windows que inclui os compiladores do Visual C++, você não precisa do Visual Studio para a construção. Observe que, a partir da versão 8.0a, o SDK do Windows não vem mais com um ambiente de construção completo de linha de comando.

#### 17.7.5.1. Requisitos [#](#WINDOWS-REQUIREMENTS)

Os seguintes produtos adicionais são necessários para construir o PostgreSQL no Windows.

Strawberry Perl: O Strawberry Perl é necessário para executar os scripts de geração de compilação. MinGW ou o Perl do Cygwin não funcionarão. Ele também deve estar presente no PATH. Os binários podem ser baixados em <https://strawberryperl.com>.

Bison e Flex: Binários para Bison e Flex podem ser baixados em <https://github.com/lexxmark/winflexbison>.

Os seguintes produtos adicionais não são necessários para começar, mas são necessários para montar o pacote completo.

Magicsplat Tcl: Necessário para a construção do PL/Tcl. Os binários podem ser baixados em <https://www.magicsplat.com/tcl-installer/index.html>.

Diff: Diff é necessário para executar os testes de regressão, e pode ser baixado em <http://gnuwin32.sourceforge.net>.

Gettext: É necessário obter Gettext para a construção com suporte a NLS, e ele pode ser baixado a partir de <http://gnuwin32.sourceforge.net>. Note que binários, dependências e arquivos de desenvolvedor são necessários.

MIT Kerberos: Necessário para suporte à autenticação GSSAPI. O MIT Kerberos pode ser baixado em <https://web.mit.edu/Kerberos/dist/index.html>.

libxml2 e libxslt: Necessários para suporte a XML. Os binários podem ser baixados de <https://zlatkovic.com/pub/libxml> ou obtidos em fonte de <http://xmlsoft.org>. Observe que o libxml2 requer iconv, que está disponível na mesma localização de download.

LZ4: Necessário para o suporte à compressão LZ4. Os binários e a fonte podem ser baixados em <https://github.com/lz4/lz4/releases>.

Zstandard: Necessário para suportar a compressão Zstandard. Os binários e a fonte podem ser baixados em <https://github.com/facebook/zstd/releases>.

OpenSSL: Necessário para suporte SSL. Os binários podem ser baixados de <https://slproweb.com/products/Win32OpenSSL.html> ou obtidos de <https://www.openssl.org>.

ossp-uuid: Necessário para suporte UUID-OSSP (apenas para contribuintes). A fonte pode ser baixada em <http://www.ossp.org/pkg/lib/uuid/>.

Python: Necessário para a construção do PL/Python. Os binários podem ser baixados em <https://www.python.org>.

zlib: Necessário para suporte de compressão em pg_dump e pg_restore. Os binários podem ser baixados em <https://www.zlib.net>.

#### 17.7.5.2. Considerações Especiais para o Windows de 64 bits [#](#INSTALL-WINDOWS-FULL-64-BIT)

O PostgreSQL será construído apenas para a arquitetura x64 no Windows de 64 bits.

Misturar versões de 32 e 64 bits na mesma árvore de construção não é suportada. O sistema de construção detectará automaticamente se está sendo executado em um ambiente de 32 ou 64 bits e construirá o PostgreSQL de acordo. Por esse motivo, é importante iniciar o prompt de comando correto antes de construir.

Para usar uma biblioteca de terceiros do lado do servidor, como Python ou OpenSSL, essa biblioteca *deve* também ser de 64 bits. Não há suporte para carregar uma biblioteca de 32 bits em um servidor de 64 bits. Várias das bibliotecas de terceiros que o PostgreSQL suporta podem estar disponíveis apenas em versões de 32 bits, e, nesse caso, não podem ser usadas com o PostgreSQL de 64 bits.

#### 17.7.5.3. Recolher Dumps de Acidente [#](#WINDOWS-CRASH-DUMPS)

Se o PostgreSQL no Windows falhar, ele tem a capacidade de gerar minidumps que podem ser usados para identificar a causa do falhanço, semelhante aos core dumps no Unix. Esses dumps podem ser lidos usando as Ferramentas de depuração do Windows ou usando o Visual Studio. Para habilitar a geração de dumps no Windows, crie um subdiretório chamado `crashdumps` dentro do diretório de dados do cluster. Os dumps serão então escritos neste diretório com um nome único baseado no identificador do processo que falhou e no horário atual do falhanço.