## 17.1. Requisitos [#](#INSTALL-REQUIREMENTS)

Em geral, uma plataforma moderna compatível com Unix deve ser capaz de executar o PostgreSQL. As plataformas que receberam testes específicos no momento do lançamento estão descritas em [Seção 17.6](supported-platforms.md) abaixo.

Os seguintes pacotes de software são necessários para a construção do PostgreSQL:

* É necessário o uso da versão 3.81 ou superior do GNU make; outros programas do make ou versões mais antigas do GNU make *não* funcionarão. (O GNU make é, às vezes, instalado sob o nome `gmake`.). Para testar o GNU make, digite:

* Alternativamente, o PostgreSQL pode ser construído usando [Meson](https://mesonbuild.com/). Esta é a única opção para construir o PostgreSQL no Windows usando o Visual Studio. Para outras plataformas, o uso do Meson é atualmente experimental. Se você optar por usar o Meson, então não precisa do GNU make, mas os outros requisitos abaixo ainda se aplicam.

A versão mínima necessária do Meson é 0.54.
* Você precisa de um compilador ISO/ANSI C (pelo menos compatível com C99). Versões recentes do GCC são recomendadas, mas o PostgreSQL é conhecido por ser construído usando uma ampla variedade de compiladores de diferentes fornecedores.
* O tar é necessário para desempacotar a distribuição de código-fonte, além de gzip ou bzip2.
* Flex e Bison são necessários. Outros programas lex e yacc não podem ser usados. Bison precisa estar na versão mínima 2.3.
* Perl 5.14 ou posterior é necessário durante o processo de construção e para executar algumas suítes de teste. (Essa exigência é separada das exigências para a construção do PL/Perl; veja abaixo.)
* A biblioteca GNU Readline é usada por padrão. Ela permite que o psql (o interpretador de SQL da linha de comando do PostgreSQL) lembre cada comando que você digita e permite que você use as teclas seta para lembrar e editar comandos anteriores. Isso é muito útil e é fortemente recomendado. Se você não quiser usá-lo, então você deve especificar a opção `--without-readline` para `configure`. Como alternativa, você pode frequentemente usar a biblioteca `libedit`, originalmente desenvolvida no NetBSD, licenciada sob BSD. A biblioteca `libedit` é compatível com GNU Readline e é usada se `libreadline` não for encontrada, ou se `--with-libedit-preferred` for usada como uma opção para `configure`. Se você está usando uma distribuição Linux baseada em pacotes, esteja ciente de que você precisa tanto dos pacotes `readline` quanto `readline-devel`, se esses forem separados em sua distribuição.
* A biblioteca de compressão zlib é usada por padrão. Se você não quiser usá-la, então você deve especificar a opção `--without-zlib` para `configure`. Usar essa opção desativa o suporte para arquivos comprimidos em pg_dump e pg_restore.
* A biblioteca ICU é usada por padrão. Se você não quiser usá-la, então você deve especificar a opção `--without-icu` para `configure`. Usar essa opção desativa o suporte para recursos de ordenação ICU (veja [Seção 23.2](collation.md)).

O suporte do ICU requer que o pacote ICU4C seja instalado. A versão mínima necessária do ICU4C é atualmente 4.2.

Por padrão, o pkg-config será usado para encontrar as opções de compilação necessárias. Isso é suportado para a versão ICU4C 4.6 e posterior. Para versões mais antigas, ou se o pkg-config não estiver disponível, as variáveis `ICU_CFLAGS` e `ICU_LIBS` podem ser especificadas para `configure`, como neste exemplo:

```
./configure ... ICU_CFLAGS='-I/some/where/include' ICU_LIBS='-L/some/where/lib -licui18n -licuuc -licudata'
```

(Se o ICU4C estiver no caminho de busca padrão do compilador, ainda é necessário especificar strings não vazias para evitar o uso do pkg-config, por exemplo, `ICU_CFLAGS=' '`.)

Os pacotes a seguir são opcionais. Eles não são necessários na configuração padrão, mas são necessários quando certas opções de compilação são habilitadas, conforme explicado abaixo:

* Para construir o PL/Perl, o idioma de programação do servidor, você precisa de uma instalação completa do Perl, incluindo a biblioteca `libperl` e os arquivos de cabeçalho. A versão mínima necessária é o Perl 5.14. Como o PL/Perl será uma biblioteca compartilhada, a biblioteca `libperl` também deve ser uma biblioteca compartilhada na maioria das plataformas. Isso parece ser o padrão nas versões recentes do Perl, mas não estava presente nas versões anteriores, e, de qualquer forma, é a escolha de quem instalou o Perl em seu site. `configure` falhará se a opção de construção do PL/Perl for selecionada, mas não conseguirá encontrar uma biblioteca compartilhada `libperl`. Nesse caso, você terá que reconstruir e instalar o Perl manualmente para poder construir o PL/Perl. Durante o processo de configuração do Perl, solicite uma biblioteca compartilhada.

Se você pretende fazer uso mais do que incidental do PL/Perl, você deve garantir que a instalação do Perl foi construída com a opção `usemultiplicity` habilitada (`perl -V` mostrará se isso é o caso). * Para construir a linguagem de programação do servidor PL/Python, você precisa de uma instalação do Python com os arquivos de cabeçalho e o módulo sysconfig. A versão mínima compatível é o Python 3.6.8.

Como o PL/Python será uma biblioteca compartilhada, a biblioteca `libpython` também deve ser uma biblioteca compartilhada na maioria das plataformas. Esse não é o caso em uma instalação padrão do Python construída a partir do código fonte, mas uma biblioteca compartilhada está disponível em muitas distribuições de sistemas operacionais. `configure` falhará se a opção de construção do PL/Python for selecionada, mas não consegue encontrar uma biblioteca compartilhada `libpython`. Isso pode significar que você precisa instalar pacotes adicionais ou reconstruir (parte de) sua instalação do Python para fornecer essa biblioteca compartilhada. Ao construir a partir do código fonte, execute o configure do Python com a bandeira `--enable-shared`.
* Para construir a linguagem procedural PL/Tcl, você, claro, precisa de uma instalação Tcl. A versão mínima necessária é Tcl 8.4.
* Para habilitar o Suporte de Idioma Nativo (NLS), ou seja, a capacidade de exibir as mensagens de um programa em uma língua diferente do inglês, você precisa de uma implementação da API Gettext. Alguns sistemas operacionais têm isso embutido (por exemplo, Linux, NetBSD, Solaris), para outros sistemas, você pode baixar um pacote de adição de <https://www.gnu.org/software/gettext/>. Se você estiver usando a implementação Gettext na biblioteca C do GNU, então você precisará adicionalmente do pacote GNU Gettext para alguns programas utilitários. Para qualquer uma das outras implementações, você não precisará.
* Você precisa do OpenSSL, se quiser suportar conexões de cliente criptografadas. O OpenSSL também é necessário para geração de números aleatórios em plataformas que não têm `/dev/urandom` (exceto Windows). A versão mínima necessária é 1.1.1.

Além disso, o LibreSSL é suportado usando a camada de compatibilidade OpenSSL. A versão mínima necessária é 3.4 (a partir da versão 7.0 do OpenBSD).
* Você precisa do MIT Kerberos (para GSSAPI), OpenLDAP e/ou PAM, se quiser suportar autenticação usando esses serviços.
* Você precisa do Curl para construir um módulo opcional que implemente o fluxo de [Autenticação de Dispositivo OAuth](libpq-oauth.md) para aplicativos de cliente.
* Você precisa do LZ4, se quiser suportar compressão de dados com esse método; veja [compressão_default_toast](runtime-config-client.md#GUC-DEFAULT-TOAST-COMPRESSION) e [compressão_wal](runtime-config-wal.md#GUC-WAL-COMPRESSION).
* Você precisa do Zstandard, se quiser suportar compressão de dados com esse método; veja [compressão_wal](runtime-config-wal.md#GUC-WAL-COMPRESSION). A versão mínima necessária é 1.4.0.
* Para construir a documentação do PostgreSQL, há um conjunto separado de requisitos; veja [Seção J.2](docguide-toolsets.md).

Se você precisa obter um pacote GNU, pode encontrá-lo em seu site local de espelho GNU (consulte <https://www.gnu.org/prep/ftp> para uma lista) ou em <ftp://ftp.gnu.org/gnu/>.