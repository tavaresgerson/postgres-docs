## F.17. hstore — tipo de dados chave/valor hstore [#](#HSTORE)

* [F.17.1. `hstore` Representação Externa](hstore.md#HSTORE-EXTERNAL-REP)
* [F.17.2. `hstore` Operadores e Funções](hstore.md#HSTORE-OPS-FUNCS)
* [F.17.3. Índices](hstore.md#HSTORE-INDEXES)
* [F.17.4. Exemplos](hstore.md#HSTORE-EXAMPLES)
* [F.17.5. Estatísticas](hstore.md#HSTORE-STATISTICS)
* [F.17.6. Compatibilidade](hstore.md#HSTORE-COMPATIBILITY)
* [F.17.7. Transformações](hstore.md#HSTORE-TRANSFORMS)
* [F.17.8. Autores](hstore.md#HSTORE-AUTHORS)

Este módulo implementa o tipo de dados `hstore` para armazenar conjuntos de pares chave/valor dentro de um único valor do PostgreSQL. Isso pode ser útil em vários cenários, como linhas com muitos atributos que são raramente examinados ou dados semi-estruturados. As chaves e os valores são simplesmente strings de texto.

Este módulo é considerado "confiável", ou seja, pode ser instalado por usuários não superusuários que possuem privilégio `CREATE` no banco de dados atual.

### F.17.1. `hstore` Representação Externa [#](#HSTORE-EXTERNAL-REP)

A representação textual de um `hstore`, usada para entrada e saída, inclui zero ou mais pares *`key`* *`=>`* *`value`* separados por vírgulas. Alguns exemplos:

```
k => v
foo => bar, baz => whatever
"1-a" => "anything at all"
```

A ordem dos pares não é significativa (e pode não ser reproduzida na saída). Espaços em branco entre pares ou ao redor do sinal `=>` são ignorados. Chaves e valores com espaços em branco, vírgulas, `=`s ou `>`s são ignorados. Para incluir uma citação dupla ou uma barra insira-a com uma barra invertida.

Cada chave em um `hstore` é única. Se você declarar um `hstore` com chaves duplicadas, apenas uma será armazenada no `hstore` e não há garantia de qual será mantida:

```
SELECT 'a=>1,a=>2'::hstore;
  hstore
----------
 "a"=>"1"
```

Um valor (mas não uma chave) pode ser um SQL `NULL`. Por exemplo:

```
key => NULL
```

A palavra-chave `NULL` é sensível a maiúsculas e minúsculas. Double-quote o `NULL` para tratá-lo como a string comum “NULL”.

### Nota

Tenha em mente que o formato de texto `hstore` aplicado ao inserir, aplica-se *antes* de qualquer citação ou escapagem necessária. Se você estiver passando um literal `hstore` por meio de um parâmetro, então nenhum processamento adicional é necessário. Mas se você está passando como uma constante literal citada, então quaisquer caracteres de aspas simples e (dependendo da configuração do parâmetro de configuração `standard_conforming_strings`), caracteres de barra invertida precisam ser escaçados corretamente. Consulte [Seção 4.1.2.1][(sql-syntax-lexical.md#SQL-SYNTAX-STRINGS "4.1.2.1. String Constants")] para mais informações sobre o manuseio de constantes de string.

Em saída, as aspas duplas sempre cercam as chaves e os valores, mesmo quando isso não é estritamente necessário.

### F.17.2. `hstore` Operadores e Funções [#](#HSTORE-OPS-FUNCS)

Os operadores fornecidos pelo módulo `hstore` são mostrados na [Tabela F.6](hstore.md#HSTORE-OP-TABLE "Table F.6. hstore Operators"), as funções na [Tabela F.7](hstore.md#HSTORE-FUNC-TABLE "Table F.7. hstore Functions").

**Tabela F.6. Operadores `hstore`**



<table border="1" class="table" summary="hstore Operators">
<colgroup>
<col/>
</colgroup>
<thead>
<tr>
<th class="func_table_entry">
<p class="func_signature">Operador</p>
<p>Descrição</p>
<p>Exemplo(s)</p>
</th>
</tr>
</thead>
<tbody>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="type">
      hstore
     </code>
<code class="literal">
      -&gt;
     </code>
<code class="type">
      text
     </code>→<code class="returnvalue">
      text
     </code>
</p>
<p>Retorna o valor associado à chave fornecida, ou<code class="literal">
      NULL
     </code>se não estiver presente.</p>
<p>
<code class="literal">
      'a=&gt;x, b=&gt;y'::hstore -&gt; 'a'
     </code>→<code class="returnvalue">
      x
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="type">
      hstore
     </code>
<code class="literal">
      -&gt;
     </code>
<code class="type">
      text[]
     </code>→<code class="returnvalue">
      text[]
     </code>
</p>
<p>Retorna valores associados a chaves específicas, ou<code class="literal">
      NULL
     </code>se não estiver presente.</p>
<p>
<code class="literal">
      'a=&gt;x, b=&gt;y, c=&gt;z'::hstore -&gt; ARRAY['c','a']
     </code>→<code class="returnvalue">
      {"z","x"}
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="type">
      hstore
     </code>
<code class="literal">
      ||
     </code>
<code class="type">
      hstore
     </code>→<code class="returnvalue">
      hstore
     </code>
</p>
<p>Concatenam dois<code class="type">
      hstore
     </code>
     s.
    </p>
<p>
<code class="literal">
      'a=&gt;b, c=&gt;d'::hstore || 'c=&gt;x, d=&gt;q'::hstore
     </code>→<code class="returnvalue">
      "a"=&gt;"b", "c"=&gt;"x", "d"=&gt;"q"
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="type">
      hstore
     </code>
<code class="literal">
      ?
     </code>
<code class="type">
      text
     </code>→<code class="returnvalue">
      boolean
     </code>
</p>
<p>Faz<code class="type">
      hstore
     </code>contêm chave?</p>
<p>
<code class="literal">
      'a=&gt;1'::hstore ? 'a'
     </code>→<code class="returnvalue">
      t
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="type">
      hstore
     </code>
<code class="literal">
      ?&amp;
     </code>
<code class="type">
      text[]
     </code>→<code class="returnvalue">
      boolean
     </code>
</p>
<p>Faz<code class="type">
      hstore
     </code>contêm todas as chaves especificadas?</p>
<p>
<code class="literal">
      'a=&gt;1,b=&gt;2'::hstore ?&amp; ARRAY['a','b']
     </code>→<code class="returnvalue">
      t
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="type">
      hstore
     </code>
<code class="literal">
      ?|
     </code>
<code class="type">
      text[]
     </code>→<code class="returnvalue">
      boolean
     </code>
</p>
<p>Faz<code class="type">
      hstore
     </code>contêm alguma das chaves especificadas?</p>
<p>
<code class="literal">
      'a=&gt;1,b=&gt;2'::hstore ?| ARRAY['b','c']
     </code>→<code class="returnvalue">
      t
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="type">
      hstore
     </code>
<code class="literal">
      @&gt;
     </code>
<code class="type">
      hstore
     </code>→<code class="returnvalue">
      boolean
     </code>
</p>
<p>O lado esquerdo do operador contém o lado direito?</p>
<p>
<code class="literal">
      'a=&gt;b, b=&gt;1, c=&gt;NULL'::hstore @&gt; 'b=&gt;1'
     </code>→<code class="returnvalue">
      t
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="type">
      hstore
     </code>
<code class="literal">
      &lt;@
     </code>
<code class="type">
      hstore
     </code>→<code class="returnvalue">
      boolean
     </code>
</p>
<p>O operador esquerdo está contido no direito?</p>
<p>
<code class="literal">
      'a=&gt;c'::hstore &lt;@ 'a=&gt;b, b=&gt;1, c=&gt;NULL'
     </code>→<code class="returnvalue">
      f
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="type">
      hstore
     </code>
<code class="literal">
      -
     </code>
<code class="type">
      text
     </code>→<code class="returnvalue">
      hstore
     </code>
</p>
<p>Exclui a chave do operando esquerdo.</p>
<p>
<code class="literal">
      'a=&gt;1, b=&gt;2, c=&gt;3'::hstore - 'b'::text
     </code>→<code class="returnvalue">
      "a"=&gt;"1", "c"=&gt;"3"
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="type">
      hstore
     </code>
<code class="literal">
      -
     </code>
<code class="type">
      text[]
     </code>→<code class="returnvalue">
      hstore
     </code>
</p>
<p>Exclui as chaves do operando esquerdo.</p>
<p>
<code class="literal">
      'a=&gt;1, b=&gt;2, c=&gt;3'::hstore - ARRAY['a','b']
     </code>→<code class="returnvalue">
      "c"=&gt;"3"
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="type">
      hstore
     </code>
<code class="literal">
      -
     </code>
<code class="type">
      hstore
     </code>→<code class="returnvalue">
      hstore
     </code>
</p>
<p>Exclui pares do operador esquerdo que correspondem aos pares do operador direito.</p>
<p>
<code class="literal">
      'a=&gt;1, b=&gt;2, c=&gt;3'::hstore - 'a=&gt;4, b=&gt;2'::hstore
     </code>→<code class="returnvalue">
      "a"=&gt;"1", "c"=&gt;"3"
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="type">
      anyelement
     </code>
<code class="literal">
      #=
     </code>
<code class="type">
      hstore
     </code>→<code class="returnvalue">
      anyelement
     </code>
</p>
<p>Substitui os campos no operando esquerdo (que deve ser um tipo composto) com valores correspondentes de<code class="type">
      hstore
     </code>
     .
    </p>
<p>
<code class="literal">
      ROW(1,3) #= 'f1=&gt;11'::hstore
     </code>→<code class="returnvalue">
      (11,3)
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="literal">
      %%
     </code>
<code class="type">
      hstore
     </code>→<code class="returnvalue">
      text[]
     </code>
</p>
<p>Convertidos<code class="type">
      hstore
     </code>para um array de chaves e valores alternados.</p>
<p>
<code class="literal">
      %% 'a=&gt;foo, b=&gt;bar'::hstore
     </code>→<code class="returnvalue">
      {a,foo,b,bar}
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="literal">
      %#
     </code>
<code class="type">
      hstore
     </code>→<code class="returnvalue">
      text[]
     </code>
</p>
<p>Convertidos<code class="type">
      hstore
     </code>para um array de chave/valor bidimensional.</p>
<p>
<code class="literal">
      %# 'a=&gt;foo, b=&gt;bar'::hstore
     </code>→<code class="returnvalue">
      {{a,foo},{b,bar}}
     </code>
</p>
</td>
</tr>
</tbody>
</table>




  

**Tabela F.7. `hstore` Funções**



<table border="1" class="table" summary="hstore Functions">
<colgroup>
<col/>
</colgroup>
<thead>
<tr>
<th class="func_table_entry">
<p class="func_signature">Função</p>
<p>Descrição</p>
<p>Exemplo(s)</p>
</th>
</tr>
</thead>
<tbody>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      hstore
     </code>(<code class="type">
      record
     </code>)<code class="returnvalue">
      hstore
     </code>
</p>
<p>constrói<code class="type">
      hstore
     </code>de um registro ou linha.</p>
<p>
<code class="literal">
      hstore(ROW(1,2))
     </code>→<code class="returnvalue">
      "f1"=&gt;"1", "f2"=&gt;"2"
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      hstore
     </code>(<code class="type">
      text[]
     </code>)<code class="returnvalue">
      hstore
     </code>
</p>
<p>constrói<code class="type">
      hstore
     </code>de uma matriz, que pode ser uma matriz chave/valor ou uma matriz bidimensional.</p>
<p>
<code class="literal">
      hstore(ARRAY['a','1','b','2'])
     </code>→<code class="returnvalue">
      "a"=&gt;"1", "b"=&gt;"2"
     </code>
</p>
<p>
<code class="literal">
      hstore(ARRAY[['c','3'],['d','4']])
     </code>→<code class="returnvalue">
      "c"=&gt;"3", "d"=&gt;"4"
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      hstore
     </code>(<code class="type">
      text[]
     </code>,<code class="type">
      text[]
     </code>)<code class="returnvalue">
      hstore
     </code>
</p>
<p>constrói<code class="type">
      hstore
     </code>de arrays de chave e valor separados.</p>
<p>
<code class="literal">
      hstore(ARRAY['a','b'], ARRAY['1','2'])
     </code>→<code class="returnvalue">
      "a"=&gt;"1", "b"=&gt;"2"
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      hstore
     </code>(<code class="type">
      text
     </code>,<code class="type">
      text
     </code>)<code class="returnvalue">
      hstore
     </code>
</p>
<p>Faz um único item<code class="type">
      hstore
     </code>
     .
    </p>
<p>
<code class="literal">
      hstore('a', 'b')
     </code>→<code class="returnvalue">
      "a"=&gt;"b"
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      akeys
     </code>(<code class="type">
      hstore
     </code>)<code class="returnvalue">
      text[]
     </code>
</p>
<p>Extrai extratos<code class="type">
      hstore
     </code>As chaves como um array.</p>
<p>
<code class="literal">
      akeys('a=&gt;1,b=&gt;2')
     </code>→<code class="returnvalue">
      {a,b}
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      skeys
     </code>(<code class="type">
      hstore
     </code>)<code class="returnvalue">
      setof text
     </code>
</p>
<p>Extrai extratos<code class="type">
      hstore
     </code>As chaves do 's como um conjunto.</p>
<p>
<code class="literal">
      skeys('a=&gt;1,b=&gt;2')
     </code>→<code class="returnvalue">
</code>
</p>
<pre class="programlisting">
a b
</pre>
<p>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      avals
     </code>(<code class="type">
      hstore
     </code>)<code class="returnvalue">
      text[]
     </code>
</p>
<p>Extrai extratos<code class="type">
      hstore
     </code>Os valores de 's como um array.</p>
<p>
<code class="literal">
      avals('a=&gt;1,b=&gt;2')
     </code>→<code class="returnvalue">
      {1,2}
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      svals
     </code>(<code class="type">
      hstore
     </code>)<code class="returnvalue">
      setof text
     </code>
</p>
<p>Extrai extratos<code class="type">
      hstore
     </code>valores do 's como um conjunto.</p>
<p>
<code class="literal">
      svals('a=&gt;1,b=&gt;2')
     </code>→<code class="returnvalue">
</code>
</p>
<pre class="programlisting">
1 2
</pre>
<p>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      hstore_to_array
     </code>(<code class="type">
      hstore
     </code>)<code class="returnvalue">
      text[]
     </code>
</p>
<p>Extrai extratos<code class="type">
      hstore
     </code>As chaves e seus valores como um array de chaves e valores alternados.</p>
<p>
<code class="literal">
      hstore_to_array('a=&gt;1,b=&gt;2')
     </code>→<code class="returnvalue">
      {a,1,b,2}
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      hstore_to_matrix
     </code>(<code class="type">
      hstore
     </code>)<code class="returnvalue">
      text[]
     </code>
</p>
<p>Extrai extratos<code class="type">
      hstore
     </code>As chaves e valores são apresentados como uma matriz bidimensional.</p>
<p>
<code class="literal">
      hstore_to_matrix('a=&gt;1,b=&gt;2')
     </code>→<code class="returnvalue">
      {{a,1},{b,2}}
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      hstore_to_json
     </code>(<code class="type">
      hstore
     </code>)<code class="returnvalue">
      json
     </code>
</p>
<p>Converte um<code class="type">
      hstore
     </code>para<code class="type">
      json
     </code>valor, convertendo todos os valores não nulos em strings JSON.</p>
<p>Essa função é usada implicitamente quando um<code class="type">
      hstore
     </code>o valor é lançado<code class="type">
      json
     </code>
     .
    </p>
<p>
<code class="literal">
      hstore_to_json('"a key"=&gt;1, b=&gt;t, c=&gt;null, d=&gt;12345, e=&gt;012345, f=&gt;1.234, g=&gt;2.345e+4')
     </code>→<code class="returnvalue">
      {"a key": "1", "b": "t", "c": null, "d": "12345", "e": "012345", "f": "1.234", "g": "2.345e+4"}
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      hstore_to_jsonb
     </code>(<code class="type">
      hstore
     </code>)<code class="returnvalue">
      jsonb
     </code>
</p>
<p>Converte um<code class="type">
      hstore
     </code>para<code class="type">
      jsonb
     </code>valor, convertendo todos os valores não nulos em strings JSON.</p>
<p>Essa função é usada implicitamente quando um<code class="type">
      hstore
     </code>o valor é lançado<code class="type">
      jsonb
     </code>
     .
    </p>
<p>
<code class="literal">
      hstore_to_jsonb('"a key"=&gt;1, b=&gt;t, c=&gt;null, d=&gt;12345, e=&gt;012345, f=&gt;1.234, g=&gt;2.345e+4')
     </code>→<code class="returnvalue">
      {"a key": "1", "b": "t", "c": null, "d": "12345", "e": "012345", "f": "1.234", "g": "2.345e+4"}
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      hstore_to_json_loose
     </code>(<code class="type">
      hstore
     </code>)<code class="returnvalue">
      json
     </code>
</p>
<p>Converte um<code class="type">
      hstore
     </code>para<code class="type">
      json
     </code>O valor, mas tenta distinguir valores numéricos e booleanos para que não sejam citados no JSON.</p>
<p>
<code class="literal">
      hstore_to_json_loose('"a key"=&gt;1, b=&gt;t, c=&gt;null, d=&gt;12345, e=&gt;012345, f=&gt;1.234, g=&gt;2.345e+4')
     </code>→<code class="returnvalue">
      {"a key": 1, "b": true, "c": null, "d": 12345, "e": "012345", "f": 1.234, "g": 2.345e+4}
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      hstore_to_jsonb_loose
     </code>(<code class="type">
      hstore
     </code>)<code class="returnvalue">
      jsonb
     </code>
</p>
<p>Converte um<code class="type">
      hstore
     </code>para<code class="type">
      jsonb
     </code>O valor, mas tenta distinguir valores numéricos e booleanos para que não sejam citados no JSON.</p>
<p>
<code class="literal">
      hstore_to_jsonb_loose('"a key"=&gt;1, b=&gt;t, c=&gt;null, d=&gt;12345, e=&gt;012345, f=&gt;1.234, g=&gt;2.345e+4')
     </code>→<code class="returnvalue">
      {"a key": 1, "b": true, "c": null, "d": 12345, "e": "012345", "f": 1.234, "g": 2.345e+4}
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      slice
     </code>(<code class="type">
      hstore
     </code>,<code class="type">
      text[]
     </code>)<code class="returnvalue">
      hstore
     </code>
</p>
<p>Extrai um subconjunto de um<code class="type">
      hstore
     </code>contendo apenas as chaves especificadas.</p>
<p>
<code class="literal">
      slice('a=&gt;1,b=&gt;2,c=&gt;3'::hstore, ARRAY['b','c','x'])
     </code>→<code class="returnvalue">
      "b"=&gt;"2", "c"=&gt;"3"
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      each
     </code>(<code class="type">
      hstore
     </code>)<code class="returnvalue">
      setof record
     </code>(<em class="parameter">
<code>
       key
      </code>
</em>
<code class="type">
      text
     </code>,<em class="parameter">
<code>
       value
      </code>
</em>
<code class="type">
      text
     </code>)</p>
<p>Extrai extratos<code class="type">
      hstore
     </code>As chaves e valores como um conjunto de registros.</p>
<p>
<code class="literal">
      select * from each('a=&gt;1,b=&gt;2')
     </code>→<code class="returnvalue">
</code>
</p>
<pre class="programlisting">
 key | value -----+------- a   | 1 b   | 2
</pre>
<p>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      exist
     </code>(<code class="type">
      hstore
     </code>,<code class="type">
      text
     </code>)<code class="returnvalue">
      boolean
     </code>
</p>
<p>Faz<code class="type">
      hstore
     </code>contêm chave?</p>
<p>
<code class="literal">
      exist('a=&gt;1', 'a')
     </code>→<code class="returnvalue">
      t
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      defined
     </code>(<code class="type">
      hstore
     </code>,<code class="type">
      text
     </code>)<code class="returnvalue">
      boolean
     </code>
</p>
<p>Faz<code class="type">
      hstore
     </code>contenham um não<code class="literal">
      NULL
     </code>valor para chave?</p>
<p>
<code class="literal">
      defined('a=&gt;NULL', 'a')
     </code>→<code class="returnvalue">
      f
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      delete
     </code>(<code class="type">
      hstore
     </code>,<code class="type">
      text
     </code>)<code class="returnvalue">
      hstore
     </code>
</p>
<p>Exclui o par com a chave correspondente.</p>
<p>
<code class="literal">
      delete('a=&gt;1,b=&gt;2', 'b')
     </code>→<code class="returnvalue">
      "a"=&gt;"1"
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      delete
     </code>(<code class="type">
      hstore
     </code>,<code class="type">
      text[]
     </code>)<code class="returnvalue">
      hstore
     </code>
</p>
<p>Exclui pares com chaves correspondentes.</p>
<p>
<code class="literal">
      delete('a=&gt;1,b=&gt;2,c=&gt;3', ARRAY['a','b'])
     </code>→<code class="returnvalue">
      "c"=&gt;"3"
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      delete
     </code>(<code class="type">
      hstore
     </code>,<code class="type">
      hstore
     </code>)<code class="returnvalue">
      hstore
     </code>
</p>
<p>Exclui pares que correspondem aos do segundo argumento.</p>
<p>
<code class="literal">
      delete('a=&gt;1,b=&gt;2', 'a=&gt;4,b=&gt;2'::hstore)
     </code>→<code class="returnvalue">
      "a"=&gt;"1"
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      populate_record
     </code>(<code class="type">
      anyelement
     </code>,<code class="type">
      hstore
     </code>)<code class="returnvalue">
      anyelement
     </code>
</p>
<p>Substitui os campos no operando esquerdo (que deve ser um tipo composto) com valores correspondentes de<code class="type">
      hstore
     </code>
     .
    </p>
<p>
<code class="literal">
      populate_record(ROW(1,2), 'f1=&gt;42'::hstore)
     </code>→<code class="returnvalue">
      (42,2)
     </code>
</p>
</td>
</tr>
</tbody>
</table>




  

Além desses operadores e funções, os valores do tipo `hstore` podem ser subscritos, permitindo que atuem como matrizes associativas. Apenas um único subscript do tipo `text` pode ser especificado; ele é interpretado como uma chave e o valor correspondente é obtido ou armazenado. Por exemplo,

```
CREATE TABLE mytable (h hstore);
INSERT INTO mytable VALUES ('a=>b, c=>d');
SELECT h['a'] FROM mytable;
 h
---
 b
(1 row)

UPDATE mytable SET h['c'] = 'new';
SELECT h FROM mytable;
          h
----------------------
 "a"=>"b", "c"=>"new"
(1 row)
```

Uma consulta com índice retorna `NULL` se o índice for `NULL` ou se a chave não existir no `hstore`. (Assim, uma consulta com índice não é muito diferente do operador `->`.) Uma atualização com índice falha se o índice for `NULL`; caso contrário, ela substitui o valor para essa chave, adicionando uma entrada no `hstore` se a chave não existir já.

### F.17.3. Índices [#](#HSTORE-INDEXES)

`hstore` tem suporte para os índices GiST e GIN para os operadores `@>`, `?`, `?&` e `?|`. Por exemplo:

```
CREATE INDEX hidx ON testhstore USING GIST (h);

CREATE INDEX hidx ON testhstore USING GIN (h);
```

`gist_hstore_ops` O opclass GiST aproxima um conjunto de pares chave/valor como uma assinatura de bitmap. Seu parâmetro inteiro opcional `siglen` determina o comprimento da assinatura em bytes. O comprimento padrão é de 16 bytes. Os valores válidos do comprimento da assinatura estão entre 1 e 2024 bytes. assinaturas mais longas levam a uma pesquisa mais precisa (digitalizando uma fração menor do índice e menos páginas de heap), ao custo de um índice maior.

Exemplo de criação de um índice desse tipo com uma extensão de assinatura de 32 bytes:

```
CREATE INDEX hidx ON testhstore USING GIST (h gist_hstore_ops(siglen=32));
```

`hstore` também suporta índices `btree` ou `hash` para o operador `=`. Isso permite que as colunas `hstore` sejam declaradas como `UNIQUE`, ou sejam usadas em expressões `GROUP BY`, `ORDER BY` ou `DISTINCT`. A ordem de classificação para os valores de `hstore` não é particularmente útil, mas esses índices podem ser úteis para buscas de equivalência. Crie índices para comparações `=` da seguinte forma:

```
CREATE INDEX hidx ON testhstore USING BTREE (h);

CREATE INDEX hidx ON testhstore USING HASH (h);
```

### F.17.4. Exemplos [#](#HSTORE-EXAMPLES)

Adicione uma chave ou atualize uma chave existente com um novo valor:

```
UPDATE tab SET h['c'] = '3';
```

Outra maneira de fazer a mesma coisa é:

```
UPDATE tab SET h = h || hstore('c', '3');
```

Se várias chaves devem ser adicionadas ou alteradas em uma operação, a abordagem de concatenação é mais eficiente do que o subscripting:

```
UPDATE tab SET h = h || hstore(array['q', 'w'], array['11', '12']);
```

Excluir uma chave:

```
UPDATE tab SET h = delete(h, 'k1');
```

Converte um `record` em um `hstore`:

```
CREATE TABLE test (col1 integer, col2 text, col3 text);
INSERT INTO test VALUES (123, 'foo', 'bar');

SELECT hstore(t) FROM test AS t;
                   hstore
---------------------------------------------
 "col1"=>"123", "col2"=>"foo", "col3"=>"bar"
(1 row)
```

Converte um `hstore` para um tipo pré-definido de `record`:

```
CREATE TABLE test (col1 integer, col2 text, col3 text);

SELECT * FROM populate_record(null::test,
                              '"col1"=>"456", "col2"=>"zzz"');
 col1 | col2 | col3
------+------+------
  456 | zzz  |
(1 row)
```

Modifique um registro existente usando os valores de um `hstore`:

```
CREATE TABLE test (col1 integer, col2 text, col3 text);
INSERT INTO test VALUES (123, 'foo', 'bar');

SELECT (r).* FROM (SELECT t #= '"col3"=>"baz"' AS r FROM test t) s;
 col1 | col2 | col3
------+------+------
  123 | foo  | baz
(1 row)
```

### F.17.5. Estatísticas [#](#HSTORE-STATISTICS)

O tipo `hstore`, devido à sua liberalidade intrínseca, pode conter muitas chaves diferentes. Verificar chaves válidas é a tarefa da aplicação. Os exemplos a seguir demonstram várias técnicas para verificar chaves e obter estatísticas.

Exemplo simples:

```
SELECT * FROM each('aaa=>bq, b=>NULL, ""=>1');
```

Usando uma tabela:

```
CREATE TABLE stat AS SELECT (each(h)).key, (each(h)).value FROM testhstore;
```

Estatísticas online:

```
SELECT key, count(*) FROM
  (SELECT (each(h)).key FROM testhstore) AS stat
  GROUP BY key
  ORDER BY count DESC, key;
    key    | count
-----------+-------
 line      |   883
 query     |   207
 pos       |   203
 node      |   202
 space     |   197
 status    |   195
 public    |   194
 title     |   190
 org       |   189
...................
```

### F.17.6. Compatibilidade [#](#HSTORE-COMPATIBILITY)

A partir do PostgreSQL 9.0, `hstore` usa uma representação interna diferente das versões anteriores. Isso não apresenta nenhum obstáculo para atualizações de dump/restore, uma vez que a representação de texto (usada no dump) não é alterada.

No caso de uma atualização binária, a compatibilidade ascendente é mantida ao fazer com que o novo código reconheça dados de formato antigo. Isso implicará uma pequena penalidade de desempenho ao processar dados que ainda não foram modificados pelo novo código. É possível forçar uma atualização de todos os valores em uma coluna de tabela fazendo uma declaração `UPDATE` da seguinte forma:

```
UPDATE tablename SET hstorecol = hstorecol || '';
```

Outra maneira de fazer isso é:

```
ALTER TABLE tablename ALTER hstorecol TYPE hstore USING hstorecol || '';
```

O método `ALTER TABLE` exige um bloqueio `ACCESS EXCLUSIVE` na tabela, mas não resulta no aumento do tamanho da tabela com versões de linhas antigas.

### F.17.7. Transformações [#](#HSTORE-TRANSFORMS)

Extensões adicionais estão disponíveis que implementam transformações para o tipo `hstore` para os idiomas PL/Perl e PL/Python. As extensões para PL/Perl são chamadas de `hstore_plperl` e `hstore_plperlu`, para PL/Perl confiável e não confiável. Se você instalar essas transformações e especiá-las ao criar uma função, os valores de `hstore` são mapeados para hashes Perl. A extensão para PL/Python é chamada de `hstore_plpython3u`. Se você usá-la, os valores de `hstore` são mapeados para dicionários Python.

### F.17.8. Autores [#](#HSTORE-AUTHORS)

Oleg Bartunov `<oleg@sai.msu.su>`, Moscou, Universidade de Moscou, Rússia

Teodor Sigaev `<teodor@sigaev.ru>`, Moscou, Delta-Soft Ltd., Rússia

Melhorias adicionais por Andrew Gierth `<andrew@tao11.riddles.org.uk>`, Reino Unido