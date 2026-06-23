## Capítulo 17. Instalação a partir do Código-fonte

**Índice**

* [17.1. Requisitos](install-requirements.md)
* [17.2. Obter a Fonte](install-getsource.md)
* [17.3. Construção e Instalação com Autoconf e Make](install-make.md)

+ [17.3.1. Versão Curta](install-make.md#INSTALL-SHORT-MAKE)
+ [17.3.2. Procedimento de Instalação](install-make.md#INSTALL-PROCEDURE-MAKE)
+ [17.3.3. Opções de `configure`](install-make.md#CONFIGURE-OPTIONS)
+ [17.3.4. Variáveis de Ambiente `configure`](install-make.md#CONFIGURE-ENVVARS)

* [17.4. Construção e Instalação com Meson](install-meson.md)

+ [17.4.1. Versão Breve](install-meson.md#INSTALL-SHORT-MESON)
+ [17.4.2. Procedimento de Instalação](install-meson.md#INSTALL-PROCEDURE-MESON)
+ [17.4.3. Opções de ](install-meson.md#MESON-OPTIONS) ICD-14]]
+ [17.4.4. ](install-meson.md#TARGETS-MESON) Alvos de Construção de ICD-15]]

* [17.5. Configuração pós-instalação](install-post.md)

+ [17.5.1. Bibliotecas Compartilhadas](install-post.md#INSTALL-POST-SHLIBS)
+ [17.5.2. Variáveis Ambientais](install-post.md#INSTALL-POST-ENV-VARS)

* [17.6. Plataformas suportadas](supported-platforms.md)
* [17.7. Notas específicas da plataforma](installation-platform-notes.md)

+ [17.7.1. Cygwin][(installation-platform-notes.md#INSTALLATION-NOTES-CYGWIN)
+ [17.7.2. macOS][(installation-platform-notes.md#INSTALLATION-NOTES-MACOS)
+ [17.7.3. MinGW][(installation-platform-notes.md#INSTALLATION-NOTES-MINGW)
+ [17.7.4. Solaris][(installation-platform-notes.md#INSTALLATION-NOTES-SOLARIS)
+ [17.7.5. Visual Studio][(installation-platform-notes.md#INSTALLATION-NOTES-VISUAL-STUDIO)

Este capítulo descreve a instalação do PostgreSQL usando a distribuição de código-fonte. Se você estiver instalando uma distribuição pré-embalada, como um pacote RPM ou Debian, ignore este capítulo e veja [Capítulo 16](install-binaries.md) em vez disso.