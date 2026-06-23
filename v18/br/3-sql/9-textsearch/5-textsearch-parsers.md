## 12.5. Parsers [#](#TEXTSEARCH-PARSERS)

Os analisadores de busca de texto são responsáveis por dividir o texto de documentos brutos em *tokens* e identificar o tipo de cada token, onde o conjunto de tipos possíveis é definido pelo próprio analisador. Note que um analisador não modifica o texto de forma alguma — ele simplesmente identifica possíveis limites de palavras. Devido a esse escopo limitado, há menos necessidade de analisadores personalizados específicos para aplicativos do que de dicionários personalizados. Atualmente, o PostgreSQL fornece apenas um analisador embutido, que foi encontrado útil para uma ampla gama de aplicações.

O analisador embutido é chamado `pg_catalog.default`. Ele reconhece 23 tipos de tokens, mostrados na [Tabela 12.1](textsearch-parsers.md#TEXTSEARCH-DEFAULT-PARSER).

**Tabela 12.1. Tipos de Tokens Padrão do Parser**



<table border="1" class="table" summary="Default Parser's Token Types">
 <colgroup>
  <col class="col1"/>
  <col class="col2"/>
  <col class="col3"/>
 </colgroup>
 <thead>
  <tr>
   <th>
    Alias
   </th>
   <th>
    Descrição
   </th>
   <th>
    Example
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <code class="literal">
     asciiword
    </code>
   </td>
   <td>
    Palavra, todas as letras ASCII
   </td>
   <td>
    <code class="literal">
     elephant
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     word
    </code>
   </td>
   <td>
    Palavra, todas as letras
   </td>
   <td>
    <code class="literal">
     mañana
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     numword
    </code>
   </td>
   <td>
    Palavras, letras e algarismos
   </td>
   <td>
    <code class="literal">
     beta1
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     asciihword
    </code>
   </td>
   <td>
    Palavra hífena, todo ASCII
   </td>
   <td>
    <code class="literal">
     up-to-date
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     hword
    </code>
   </td>
   <td>
    Palavra hífena, todas as letras
   </td>
   <td>
    <code class="literal">
     lógico-matemática
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     numhword
    </code>
   </td>
   <td>
    Palavras compostas, letras e algarismos
   </td>
   <td>
    <code class="literal">
     postgresql-beta1
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     hword_asciipart
    </code>
   </td>
   <td>
    Parte de palavra com hífen, todo ASCII
   </td>
   <td>
    <code class="literal">
     postgresql
    </code>
    in the context
    <code class="literal">
     postgresql-beta1
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     hword_part
    </code>
   </td>
   <td>
    Parte de palavra com hífen, todas as letras
   </td>
   <td>
    <code class="literal">
     lógico
    </code>
    or
    <code class="literal">
     matemática
    </code>
    in the context
    <code class="literal">
     lógico-matemática
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     hword_numpart
    </code>
   </td>
   <td>
    Parte de palavra com hífen, letras e dígitos
   </td>
   <td>
    <code class="literal">
     beta1
    </code>
    in the context
    <code class="literal">
     postgresql-beta1
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     email
    </code>
   </td>
   <td>
    Endereço de e-mail
   </td>
   <td>
    <code class="literal">
     foo@example.com
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     protocol
    </code>
   </td>
   <td>
    Cabeçalho do protocolo
   </td>
   <td>
    <code class="literal">
     http://
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     url
    </code>
   </td>
   <td>
    URL
   </td>
   <td>
    <code class="literal">
     example.com/stuff/index.html
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     host
    </code>
   </td>
   <td>
    Anfitrião
   </td>
   <td>
    <code class="literal">
     example.com
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     url_path
    </code>
   </td>
   <td>
    Caminho do URL
   </td>
   <td>
    <code class="literal">
     /stuff/index.html
    </code>
    , in the context of a URL
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     file
    </code>
   </td>
   <td>
    Nome do arquivo ou caminho
   </td>
   <td>
    <code class="literal">
     /usr/local/foo.txt
    </code>
    , if not within a URL
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     sfloat
    </code>
   </td>
   <td>
    Notação científica
   </td>
   <td>
    <code class="literal">
     -1.234e56
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     float
    </code>
   </td>
   <td>
    Notação decimal
   </td>
   <td>
    <code class="literal">
     -1.234
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     int
    </code>
   </td>
   <td>
    Inteiro assinado
   </td>
   <td>
    <code class="literal">
     -1234
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     uint
    </code>
   </td>
   <td>
    Inteiro não assinado
   </td>
   <td>
    <code class="literal">
     1234
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     version
    </code>
   </td>
   <td>
    Número da versão
   </td>
   <td>
    <code class="literal">
     8.3.0
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     tag
    </code>
   </td>
   <td>
    etiqueta XML
   </td>
   <td>
    <code class="literal">
     &lt;a href="dictionaries.html"&gt;
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     entity
    </code>
   </td>
   <td>
    entidade XML
   </td>
   <td>
    <code class="literal">
     &amp;amp;
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     blank
    </code>
   </td>
   <td>
    Símbolos espaciais
   </td>
   <td>
    (any whitespace or punctuation not otherwise recognized)
   </td>
  </tr>
 </tbody>
</table>










### Nota

A noção de uma “letra” do analisador é determinada pelo ajuste do local da base de dados, especificamente `lc_ctype`. As palavras que contêm apenas as letras básicas ASCII são relatadas como um tipo de token separado, uma vez que às vezes é útil distingui-las. Na maioria das línguas europeias, os tipos de token `word` e `asciiword` devem ser tratados da mesma forma.

`email` não suporta todos os caracteres de e-mail válidos conforme definido pelo [RFC 5322](https://datatracker.ietf.org/doc/html/rfc5322). Especificamente, os únicos caracteres não alfanuméricos suportados para nomes de usuários de e-mail são ponto, travessão e sublinhado.

`tag` não suporta todos os nomes de marcação válidos conforme definido pela [Recomendação do W3C, XML](https://www.w3.org/TR/xml/). Especificamente, os únicos nomes de marcação suportados são aqueles que começam com uma letra ASCII, sublinhado ou colon, e contêm apenas letras, dígitos, hífens, sublinhado, pontos e colones. `tag` também inclui comentários XML que começam com `<!--` e terminam com `-->`, e declarações XML (mas note que isso inclui qualquer coisa que comece com `<?x` e termine com `>`).

É possível que o analisador produza tokens sobrepostos a partir da mesma parte de texto. Como exemplo, uma palavra com hífen será relatada tanto como a palavra inteira quanto como cada componente:

```
SELECT alias, description, token FROM ts_debug('foo-bar-beta1');
      alias      |               description                |     token
-----------------+------------------------------------------+---------------
 numhword        | Hyphenated word, letters and digits      | foo-bar-beta1
 hword_asciipart | Hyphenated word part, all ASCII          | foo
 blank           | Space symbols                            | -
 hword_asciipart | Hyphenated word part, all ASCII          | bar
 blank           | Space symbols                            | -
 hword_numpart   | Hyphenated word part, letters and digits | beta1
```

Esse comportamento é desejável, pois permite que as pesquisas funcionem tanto para a palavra composta como para os componentes. Aqui está outro exemplo instrutivo:

```
SELECT alias, description, token FROM ts_debug('http://example.com/stuff/index.html');
  alias   |  description  |            token
----------+---------------+------------------------------
 protocol | Protocol head | http://
 url      | URL           | example.com/stuff/index.html
 host     | Host          | example.com
 url_path | URL path      | /stuff/index.html
```
