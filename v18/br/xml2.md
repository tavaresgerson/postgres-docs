## F.50. xml2 — Consulta XPath e funcionalidades XSLT [#](#XML2)

* [F.50.1. Aviso de Depreciação](xml2.md#XML2-DEPRECATION)
* [F.50.2. Descrição das Funções](xml2.md#XML2-FUNCTIONS)
* [F.50.3. `xpath_table`](xml2.md#XML2-XPATH-TABLE)
* [F.50.4. Funções XSLT](xml2.md#XML2-XSLT)
* [F.50.5. Autor](xml2.md#XML2-AUTHOR)

O módulo `xml2` oferece consulta XPath e funcionalidades XSLT.

### F.50.1. Aviso de depreciação [#](#XML2-DEPRECATION)

A partir do PostgreSQL 8.3, há funcionalidades relacionadas a XML baseadas no padrão SQL/XML no servidor principal. Essas funcionalidades incluem verificação de sintaxe XML e consultas XPath, o que é o que este módulo faz, e mais, mas a API não é compatível. Está planejado que este módulo será removido em uma versão futura do PostgreSQL em favor da API do novo padrão, portanto, é incentivado a tentar converter suas aplicações. Se você encontrar que alguma das funcionalidades deste módulo não está disponível de forma adequada com a nova API, explique seu problema para `<pgsql-hackers@lists.postgresql.org>` para que a deficiência possa ser abordada.

### F.50.2. Descrição das Funções [#](#XML2-FUNCTIONS)

[Tabela F.37](xml2.md#XML2-FUNCTIONS-TABLE "Table F.37. xml2 Functions") mostra as funções fornecidas por este módulo. Essas funções oferecem uma análise XML direta e consultas XPath.

**Tabela F.37. `xml2` Funções**



<table border="1" class="table" summary="xml2 Functions">
<colgroup>
<col/>
</colgroup>
<thead>
<tr>
<th class="func_table_entry">
<p class="func_signature">
     Function
    </p>
<p>
     Description
    </p>
</th>
</tr>
</thead>
<tbody>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      xml_valid
     </code>
     (
     <em class="parameter">
<code>
       document
      </code>
</em>
<code class="type">
      text
     </code>
     )
        →
     <code class="returnvalue">
      boolean
     </code>
</p>
<p>
     Parses the given document and returns true if the document is well-formed XML.  (Note: this is an alias for the standard PostgreSQL function
     <code class="function">
      xml_is_well_formed()
     </code>
     .  The name
     <code class="function">
      xml_valid()
     </code>
     is technically incorrect since validity and well-formedness have different meanings in XML.)
    </p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      xpath_string
     </code>
     (
     <em class="parameter">
<code>
       document
      </code>
</em>
<code class="type">
      text
     </code>
     ,
     <em class="parameter">
<code>
       query
      </code>
</em>
<code class="type">
      text
     </code>
     )
        →
     <code class="returnvalue">
      text
     </code>
</p>
<p>
     Evaluates the XPath query on the supplied document, and casts the result to
     <code class="type">
      text
     </code>
     .
    </p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      xpath_number
     </code>
     (
     <em class="parameter">
<code>
       document
      </code>
</em>
<code class="type">
      text
     </code>
     ,
     <em class="parameter">
<code>
       query
      </code>
</em>
<code class="type">
      text
     </code>
     )
        →
     <code class="returnvalue">
      real
     </code>
</p>
<p>
     Evaluates the XPath query on the supplied document, and casts the result to
     <code class="type">
      real
     </code>
     .
    </p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      xpath_bool
     </code>
     (
     <em class="parameter">
<code>
       document
      </code>
</em>
<code class="type">
      text
     </code>
     ,
     <em class="parameter">
<code>
       query
      </code>
</em>
<code class="type">
      text
     </code>
     )
        →
     <code class="returnvalue">
      boolean
     </code>
</p>
<p>
     Evaluates the XPath query on the supplied document, and casts the result to
     <code class="type">
      boolean
     </code>
     .
    </p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      xpath_nodeset
     </code>
     (
     <em class="parameter">
<code>
       document
      </code>
</em>
<code class="type">
      text
     </code>
     ,
     <em class="parameter">
<code>
       query
      </code>
</em>
<code class="type">
      text
     </code>
     ,
     <em class="parameter">
<code>
       toptag
      </code>
</em>
<code class="type">
      text
     </code>
     ,
     <em class="parameter">
<code>
       itemtag
      </code>
</em>
<code class="type">
      text
     </code>
     )
        →
     <code class="returnvalue">
      text
     </code>
</p>
<p>
     Evaluates the query on the document and wraps the result in XML tags. If the result is multivalued, the output will look like:
    </p>
<pre class="synopsis">
&lt;toptag&gt; &lt;itemtag&gt;Value 1 which could be an XML fragment&lt;/itemtag&gt; &lt;itemtag&gt;Value 2....&lt;/itemtag&gt; &lt;/toptag&gt;
</pre>
<p>
     If either
     <em class="parameter">
<code>
       toptag
      </code>
</em>
     or
     <em class="parameter">
<code>
       itemtag
      </code>
</em>
     is an empty string, the relevant tag is omitted.
    </p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      xpath_nodeset
     </code>
     (
     <em class="parameter">
<code>
       document
      </code>
</em>
<code class="type">
      text
     </code>
     ,
     <em class="parameter">
<code>
       query
      </code>
</em>
<code class="type">
      text
     </code>
     ,
     <em class="parameter">
<code>
       itemtag
      </code>
</em>
<code class="type">
      text
     </code>
     )
        →
     <code class="returnvalue">
      text
     </code>
</p>
<p>
     Like
     <code class="function">
      xpath_nodeset(document, query, toptag, itemtag)
     </code>
     but result omits
     <em class="parameter">
<code>
       toptag
      </code>
</em>
     .
    </p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      xpath_nodeset
     </code>
     (
     <em class="parameter">
<code>
       document
      </code>
</em>
<code class="type">
      text
     </code>
     ,
     <em class="parameter">
<code>
       query
      </code>
</em>
<code class="type">
      text
     </code>
     )
        →
     <code class="returnvalue">
      text
     </code>
</p>
<p>
     Like
     <code class="function">
      xpath_nodeset(document, query, toptag, itemtag)
     </code>
     but result omits both tags.
    </p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      xpath_list
     </code>
     (
     <em class="parameter">
<code>
       document
      </code>
</em>
<code class="type">
      text
     </code>
     ,
     <em class="parameter">
<code>
       query
      </code>
</em>
<code class="type">
      text
     </code>
     ,
     <em class="parameter">
<code>
       separator
      </code>
</em>
<code class="type">
      text
     </code>
     )
        →
     <code class="returnvalue">
      text
     </code>
</p>
<p>
     Evaluates the query on the document and returns multiple values separated by the specified separator, for example
     <code class="literal">
      Value 1,Value 2,Value 3
     </code>
     if
     <em class="parameter">
<code>
       separator
      </code>
</em>
     is
     <code class="literal">
      ,
     </code>
     .
    </p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      xpath_list
     </code>
     (
     <em class="parameter">
<code>
       document
      </code>
</em>
<code class="type">
      text
     </code>
     ,
     <em class="parameter">
<code>
       query
      </code>
</em>
<code class="type">
      text
     </code>
     )
        →
     <code class="returnvalue">
      text
     </code>
</p>
<p>
     This is a wrapper for the above function that uses
     <code class="literal">
      ,
     </code>
     as the separator.
    </p>
</td>
</tr>
</tbody>
</table>



### F.50.3. `xpath_table` [#](#XML2-XPATH-TABLE)

```
xpath_table(text key, text document, text relation, text xpaths, text criteria) returns setof record
```

`xpath_table` é uma função de tabela que avalia um conjunto de consultas XPath em cada um de um conjunto de documentos e retorna os resultados como uma tabela. O campo chave primária do documento original é retornado como a primeira coluna do resultado, para que o conjunto de resultados possa ser facilmente usado em junções. Os parâmetros são descritos em [Tabela F.38][(xml2.md#XML2-XPATH-TABLE-PARAMETERS "Table F.38. xpath_table Parameters")].

**Tabela F.38. Parâmetros `xpath_table`**



<table border="1" class="table" summary="xpath_table Parameters">
<colgroup>
<col class="col1"/>
<col class="col2"/>
</colgroup>
<thead>
<tr>
<th>
    Parameter
   </th>
<th>Descrição</th>
</tr>
</thead>
<tbody>
<tr>
<td>
<em class="parameter">
<code>
      key
     </code>
</em>
</td>
<td>
<p>o nome do<span class="quote">“<span class="quote">chave</span>”</span>campo — este é apenas um campo que será usado como a primeira coluna da tabela de saída, ou seja, ele identifica o registro de onde cada linha de saída veio (veja a nota abaixo sobre múltiplos valores)</p>
</td>
</tr>
<tr>
<td>
<em class="parameter">
<code>
      document
     </code>
</em>
</td>
<td>
<p>o nome do campo que contém o documento XML</p>
</td>
</tr>
<tr>
<td>
<em class="parameter">
<code>
      relation
     </code>
</em>
</td>
<td>
<p>o nome da tabela ou visão que contém os documentos</p>
</td>
</tr>
<tr>
<td>
<em class="parameter">
<code>
      xpaths
     </code>
</em>
</td>
<td>
<p>uma ou mais expressões XPath, separadas por<code class="literal">
      |
     </code>
</p>
</td>
</tr>
<tr>
<td>
<em class="parameter">
<code>
      criteria
     </code>
</em>
</td>
<td>
<p>os conteúdos da cláusula WHERE. Isso não pode ser omitido, então use<code class="literal">
      true
     </code>ou<code class="literal">
      1=1
     </code>se você quiser processar todas as linhas na relação</p>
</td>
</tr>
</tbody>
</table>




  

Esses parâmetros (exceto as cadeias de XPath) são apenas substituídos em uma declaração SQL SELECT simples, então você tem alguma flexibilidade — a declaração é

`SELECT <key>, <document> FROM <relation> WHERE <criteria>`

Portanto, esses parâmetros podem ser *qualquer coisa* válida nesses locais específicos. O resultado desse SELECT precisa retornar exatamente duas colunas (o que ele fará, a menos que você tente listar vários campos para chave ou documento). Esteja ciente de que essa abordagem simplista exige que você valide quaisquer valores fornecidos pelo usuário para evitar ataques de injeção SQL.

A função deve ser usada em uma expressão `FROM`, com uma cláusula `AS` para especificar as colunas de saída, por exemplo:

```
SELECT * FROM
xpath_table('article_id',
            'article_xml',
            'articles',
            '/article/author|/article/pages|/article/title',
            'date_entered > ''2003-01-01'' ')
AS t(article_id integer, author text, page_count integer, title text);
```

A cláusula `AS` define os nomes e os tipos das colunas na tabela de saída. O primeiro é o campo “chave” e o restante corresponde às consultas XPath. Se houver mais consultas XPath do que colunas de resultado, as consultas extras serão ignoradas. Se houver mais colunas de resultado do que consultas XPath, as colunas extras serão NULL.

Observe que este exemplo define a coluna de resultado `page_count` como um inteiro. A função lida internamente com representações de string, então quando você diz que deseja um inteiro no resultado de saída, ela pegará a representação de string do resultado do XPath e usará as funções de entrada do PostgreSQL para transformá-lo em um inteiro (ou qualquer tipo que a cláusula `AS` solicite). Um erro resultará se não conseguir fazer isso — por exemplo, se o resultado estiver vazio — então você pode optar por simplesmente usar `text` como o tipo de coluna se você achar que seus dados têm algum problema.

A declaração de chamada `SELECT` não precisa necessariamente ser apenas `SELECT *` — ela pode referenciar as colunas de saída pelo nome ou combiná-las com outras tabelas. A função produz uma tabela virtual com a qual você pode realizar qualquer operação que desejar (por exemplo, agregação, junção, ordenação, etc.). Portanto, também poderíamos ter:

```
SELECT t.title, p.fullname, p.email
FROM xpath_table('article_id', 'article_xml', 'articles',
                 '/article/title|/article/author/@id',
                 'xpath_string(article_xml,''/article/@date'') > ''2003-03-20'' ')
       AS t(article_id integer, title text, author_id integer),
     tblPeopleInfo AS p
WHERE t.author_id = p.person_id;
```

Como um exemplo mais complicado. Claro, você poderia embrulhar tudo isso em uma visão para conveniência.

#### F.50.3.1. Resultados multivalorados [#](#XML2-XPATH-TABLE-MULTIVALUED-RESULTS)

A função `xpath_table` assume que os resultados de cada consulta XPath podem ser multivalorados, portanto, o número de linhas devolvidas pela função pode não ser o mesmo que o número de documentos de entrada. A primeira linha devolvida contém o primeiro resultado de cada consulta, a segunda linha o segundo resultado de cada consulta. Se uma das consultas tiver menos valores do que as outras, valores nulos serão devolvidos em vez disso.

Em alguns casos, um usuário saberá que uma consulta XPath dada retornará apenas um único resultado (talvez um identificador único de documento) — se usada juntamente com uma consulta XPath que retorna vários resultados, o resultado de valor único aparecerá apenas na primeira linha do resultado. A solução para isso é usar o campo chave como parte de uma junção contra uma consulta XPath mais simples. Como exemplo:

```
CREATE TABLE test (
    id int PRIMARY KEY,
    xml text
);

INSERT INTO test VALUES (1, '<doc num="C1">
<line num="L1"><a>1</a><b>2</b><c>3</c></line>
<line num="L2"><a>11</a><b>22</b><c>33</c></line>
</doc>');

INSERT INTO test VALUES (2, '<doc num="C2">
<line num="L1"><a>111</a><b>222</b><c>333</c></line>
<line num="L2"><a>111</a><b>222</b><c>333</c></line>
</doc>');

SELECT * FROM
  xpath_table('id','xml','test',
              '/doc/@num|/doc/line/@num|/doc/line/a|/doc/line/b|/doc/line/c',
              'true')
  AS t(id int, doc_num varchar(10), line_num varchar(10), val1 int, val2 int, val3 int)
WHERE id = 1 ORDER BY doc_num, line_num

 id | doc_num | line_num | val1 | val2 | val3
----+---------+----------+------+------+------
  1 | C1      | L1       |    1 |    2 |    3
  1 |         | L2       |   11 |   22 |   33
```

Para obter `doc_num` em cada linha, a solução é usar duas invocações de `xpath_table` e unir os resultados:

```
SELECT t.*,i.doc_num FROM
  xpath_table('id', 'xml', 'test',
              '/doc/line/@num|/doc/line/a|/doc/line/b|/doc/line/c',
              'true')
    AS t(id int, line_num varchar(10), val1 int, val2 int, val3 int),
  xpath_table('id', 'xml', 'test', '/doc/@num', 'true')
    AS i(id int, doc_num varchar(10))
WHERE i.id=t.id AND i.id=1
ORDER BY doc_num, line_num;

 id | line_num | val1 | val2 | val3 | doc_num
----+----------+------+------+------+---------
  1 | L1       |    1 |    2 |    3 | C1
  1 | L2       |   11 |   22 |   33 | C1
(2 rows)
```

### F.50.4. Funções XSLT [#](#XML2-XSLT)

As seguintes funções estão disponíveis se a libxslt estiver instalada:

#### F.50.4.1. `xslt_process` [#](#XML2-XSLT-XSLT-PROCESS)

```
xslt_process(text document, text stylesheet, text paramlist) returns text
```

Essa função aplica o folha de estilo XSL ao documento e retorna o resultado transformado. O `paramlist` é uma lista de atribuições de parâmetros a serem usadas na transformação, especificada na forma `a=1,b=2`. Note que a análise de parâmetros é muito simples: os valores dos parâmetros não podem conter vírgulas!

Existe também uma versão de dois parâmetros de `xslt_process` que não passa nenhum parâmetro para a transformação.

### F.50.5. Autor [#](#XML2-AUTHOR)

John Gray `<jgray@azuli.co.uk>`

O desenvolvimento deste módulo foi patrocinado pela Torchbox Ltd. (www.torchbox.com). Ele tem a mesma licença BSD que o PostgreSQL.