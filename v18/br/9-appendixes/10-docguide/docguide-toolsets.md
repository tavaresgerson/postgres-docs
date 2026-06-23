## J.2. Conjuntos de Ferramentas [#](#DOCGUIDE-TOOLSETS)

* [J.2.1. Instalação no Fedora, RHEL e Derivados](docguide-toolsets.md#DOCGUIDE-TOOLSETS-INST-FEDORA-ET-AL)
* [J.2.2. Instalação no FreeBSD](docguide-toolsets.md#DOCGUIDE-TOOLSETS-INST-FREEBSD)
* [J.2.3. Pacotes do Debian](docguide-toolsets.md#DOCGUIDE-TOOLSETS-INST-DEBIAN)
* [J.2.4. macOS](docguide-toolsets.md#DOCGUIDE-TOOLSETS-INST-MACOS)
* [J.2.5. Detecção pelo `configure`[(docguide-toolsets.md#DOCGUIDE-TOOLSETS-CONFIGURE)]

Os seguintes instrumentos são utilizados para processar a documentação. Alguns podem ser opcionais, conforme indicado.

[DocBook DTD](https://www.oasis-open.org/docbook/) [#](#DOCGUIDE-TOOLSETS-DOCBOOK-DTD): Esta é a definição do próprio DocBook. Atualmente, usamos a versão 4.5; você não pode usar versões posteriores ou anteriores. Você precisa da variante XML do DTD do DocBook, não da variante SGML.

[DocBook XSL Stylesheets](https://github.com/docbook/wiki/wiki/DocBookXslStylesheets) [#](#DOCGUIDE-TOOLSETS-DOCBOOK-XSL): Estes contêm as instruções de processamento para a conversão das fontes DocBook para outros formatos, como HTML.

A versão mínima exigida é atualmente 1.77.0, mas é recomendável usar a versão mais recente disponível para obter os melhores resultados.

[Libxml2](http://xmlsoft.org/) para `xmllint` [#](#DOCGUIDE-TOOLSETS-LIBXML2): Esta biblioteca e a ferramenta `xmllint` que ela contém são usadas para processar XML. Muitos desenvolvedores já terão o Libxml2 instalado, pois ele também é usado ao construir o código do PostgreSQL. No entanto, note que `xmllint` pode precisar ser instalada a partir de um subpacote separado.

[Libxslt](http://xmlsoft.org/XSLT/) para `xsltproc` [#](#DOCGUIDE-TOOLSETS-LIBXSLT): `xsltproc` é um processador XSLT, ou seja, um programa para converter XML para outros formatos usando folhas de estilo XSLT.

[FOP](https://xmlgraphics.apache.org/fop/) [#](#DOCGUIDE-TOOLSETS-FOP): Este é um programa para converter, entre outras coisas, XML para PDF. É necessário apenas se você deseja construir a documentação em formato PDF.

Temos experiência documentada com vários métodos de instalação para as várias ferramentas necessárias para processar a documentação. Essas serão descritas abaixo. Pode haver algumas outras distribuições empacotadas para essas ferramentas. Por favor, informe o status do pacote para a lista de correio da documentação, e incluiremos essa informação aqui.

### J.2.1. Instalação no Fedora, RHEL e derivados [#](#DOCGUIDE-TOOLSETS-INST-FEDORA-ET-AL)

Para instalar os pacotes necessários, use:

```
yum install docbook-dtds docbook-style-xsl libxslt fop
```

### J.2.2. Instalação no FreeBSD [#](#DOCGUIDE-TOOLSETS-INST-FREEBSD)

Para instalar os pacotes necessários com `pkg`, use:

```
pkg install docbook-xml docbook-xsl libxslt fop
```

Ao construir a documentação a partir do diretório `doc`, você precisará usar `gmake`, porque o makefile fornecido não é adequado para o FreeBSD `make`.

### J.2.3. Pacotes Debian [#](#DOCGUIDE-TOOLSETS-INST-DEBIAN)

Há um conjunto completo de pacotes de ferramentas de documentação disponíveis para o Debian GNU/Linux. Para instalar, basta usar:

```
apt-get install docbook-xml docbook-xsl libxml2-utils xsltproc fop
```

### J.2.4. macOS [#](#DOCGUIDE-TOOLSETS-INST-MACOS)

Se você usa o MacPorts, o seguinte lhe dará as configurações necessárias:

```
sudo port install docbook-xml docbook-xsl-nons libxslt fop
```

Se você usa Homebrew, use este:

```
brew install docbook docbook-xsl libxslt fop
```

Os programas fornecidos pelo Homebrew exigem que a seguinte variável de ambiente seja definida. Para máquinas baseadas em Intel, use o seguinte:

```
export XML_CATALOG_FILES=/usr/local/etc/xml/catalog
```

Em máquinas com base em Apple Silicon, use o seguinte:

```
export XML_CATALOG_FILES=/opt/homebrew/etc/xml/catalog
```

Sem ela, `xsltproc` lançará erros como este:

```
I/O error : Attempt to load network entity http://www.oasis-open.org/docbook/xml/4.5/docbookx.dtd
postgres.sgml:21: warning: failed to load external entity "http://www.oasis-open.org/docbook/xml/4.5/docbookx.dtd"
...
```

Embora seja possível usar as versões fornecidas pela Apple dos `xmllint` e `xsltproc`, em vez das versões do MacPorts ou Homebrew, você ainda precisará instalar o DTD e as folhas de estilo do DocBook, e configurar um arquivo de catálogo que os aponte.

### J.2.5. Detecção por `configure` [#](#DOCGUIDE-TOOLSETS-CONFIGURE)

Antes de poder construir a documentação que você precisa para executar o script `configure`, como faria ao construir os próprios programas do PostgreSQL. Verifique a saída perto do final da execução; ela deve parecer algo assim:

```
checking for xmllint... xmllint
checking for xsltproc... xsltproc
checking for fop... fop
checking for dbtoepub... dbtoepub
```

Se `xmllint` ou `xsltproc` não for encontrado, você não poderá construir nenhuma das documentações. `fop` é necessário apenas para construir a documentação em formato PDF. `dbtoepub` é necessário apenas para construir a documentação em formato EPUB.

Se necessário, você pode dizer a `configure` onde encontrar esses programas, por exemplo

```
./configure ... XMLLINT=/opt/local/bin/xmllint ...
```

Se você preferir construir o PostgreSQL usando Meson, em vez disso, execute `meson setup` conforme descrito em [Seção 17.4](install-meson.md "17.4. Building and Installation with Meson"), e depois veja [Seção J.4](docguide-build-meson.md "J.4. Building the Documentation with Meson").