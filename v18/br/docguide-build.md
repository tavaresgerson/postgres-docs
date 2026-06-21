## J.3. Construindo a documentação com Make [#](#DOCGUIDE-BUILD)

* [J.3.1. HTML](docguide-build.md#DOCGUIDE-BUILD-HTML)
* [J.3.2. Manpages](docguide-build.md#DOCGUIDE-BUILD-MANPAGES)
* [J.3.3. PDF](docguide-build.md#DOCGUIDE-BUILD-PDF)
* [J.3.4. Verificação de Sintaxe](docguide-build.md#DOCGUIDE-BUILD-SYNTAX-CHECK)

Depois de configurar tudo, mude para o diretório `doc/src/sgml` e execute um dos comandos descritos nas seções a seguir para construir a documentação. (Lembre-se de usar o GNU make.)

### J.3.1. HTML [#](#DOCGUIDE-BUILD-HTML)

Para construir a versão HTML da documentação:

```
doc/src/sgml$ make html
```

Este também é o alvo padrão. A saída aparece no subdiretório `html`.

Para produzir documentação HTML com o conjunto de estilos usado em [postgresql.org][(https://www.postgresql.org/docs/current/)], em vez do estilo simples padrão, use:

```
doc/src/sgml$ make STYLE=website html
```

Se a opção `STYLE=website` for usada, os arquivos HTML gerados incluem referências a folhas de estilo hospedadas em [postgresql.org][(https://www.postgresql.org/docs/current/)] e exigem acesso à rede para visualização.

### J.3.2. Manpages [#](#DOCGUIDE-BUILD-MANPAGES)

Usamos as folhas de estilo DocBook XSL para converter as páginas do DocBook `refentry` em saída *roff adequada para manuais. Para criar os manuais, use o comando:

```
doc/src/sgml$ make man
```

### J.3.3. PDF [#](#DOCGUIDE-BUILD-PDF)

Para produzir uma versão em PDF da documentação usando FOP, você pode usar um dos seguintes comandos, dependendo do formato de papel preferido:

* Para o formato A4:

```
  doc/src/sgml$ make postgres-A4.pdf
  ``` * Para o formato de carta dos EUA:

  ```
  doc/src/sgml$ make postgres-US.pdf
  ```

Como a documentação do PostgreSQL é bastante extensa, o FOP exigirá uma quantidade significativa de memória. Por isso, em alguns sistemas, a compilação falhará com uma mensagem de erro relacionada à memória. Isso geralmente pode ser corrigido configurando as configurações do heap do Java no arquivo de configuração `~/.foprc`, por exemplo:

```
# FOP binary distribution
FOP_OPTS='-Xmx1500m'
# Debian
JAVA_ARGS='-Xmx1500m'
# Red Hat
ADDITIONAL_FLAGS='-Xmx1500m'
```

Há um mínimo de memória que é necessário, e, em certa medida, mais memória parece fazer as coisas um pouco mais rápidas. Em sistemas com muito pouca memória (menos de 1 GB), a construção será muito lenta devido ao swapping ou não funcionará de forma alguma.

Na sua configuração padrão, o FOP emitirá uma mensagem `INFO` para cada página. O nível de log pode ser alterado através de `~/.foprc`:

```
LOGCHOICE=-Dorg.apache.commons.logging.Log=​org.apache.commons.logging.impl.SimpleLog
LOGLEVEL=-Dorg.apache.commons.logging.simplelog.defaultlog=WARN
```

Outros processadores XSL-FO também podem ser usados manualmente, mas o processo de construção automatizado só suporta o FOP.

### J.3.4. Verificação de sintaxe [#](#DOCGUIDE-BUILD-SYNTAX-CHECK)

Construir a documentação pode levar muito tempo. Mas há um método para verificar apenas a sintaxe correta dos arquivos de documentação, que leva apenas alguns segundos:

```
doc/src/sgml$ make check
```
