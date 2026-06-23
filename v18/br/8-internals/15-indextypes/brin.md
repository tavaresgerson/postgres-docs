## 65.5. Índices BRIN [#](#BRIN)

* [65.5.1. Introdução](brin.md#BRIN-INTRO)
* [65.5.2. Classes de Operadores Integradas](brin.md#BRIN-BUILTIN-OPCLASSES)
* [65.5.3. Extensibilidade](brin.md#BRIN-EXTENSIBILITY)

### 65.5.1. Introdução [#](#BRIN-INTRO)

BRIN significa Índice de Alcance de Bloco. O BRIN foi projetado para lidar com tabelas muito grandes, nas quais certas colunas têm alguma correlação natural com sua localização física dentro da tabela.

O BRIN trabalha em termos de *intervalos de blocos* (ou "intervalos de páginas"). Um intervalo de bloco é um grupo de páginas que estão fisicamente adjacentes na tabela; para cada intervalo de bloco, algumas informações resumidas são armazenadas pelo índice. Por exemplo, uma tabela que armazena as ordens de venda de uma loja pode ter uma coluna de data na qual cada ordem foi colocada, e na maioria das vezes as entradas para ordens anteriores aparecerão mais cedo na tabela também; uma tabela que armazena uma coluna de código postal pode ter todos os códigos para uma cidade agrupados naturalmente.

Os índices BRIN podem atender a consultas por meio de varreduras regulares de índice de bitmap, e retornar todos os tuplos em todas as páginas dentro de cada intervalo, se as informações resumidas armazenadas pelo índice forem *consistentes* com as condições da consulta. O executor da consulta é responsável por reverificar esses tuplos e descartar aqueles que não correspondem às condições da consulta — em outras palavras, esses índices são perdas. Como um índice BRIN é muito pequeno, a varredura do índice adiciona pouco sobrecarga em comparação com uma varredura sequencial, mas pode evitar a varredura de grandes partes da tabela que são conhecidas por não conter tuplos correspondentes.

Os dados específicos que um índice BRIN armazenará, bem como as consultas específicas que o índice poderá satisfazer, dependem da classe do operador selecionada para cada coluna do índice. Os tipos de dados que possuem uma ordem de classificação linear podem ter classes de operador que armazenam o valor mínimo e máximo dentro de cada intervalo de bloco, por exemplo; os tipos geométricos podem armazenar a caixa de delimitação para todos os objetos no intervalo de bloco.

O tamanho da faixa do bloco é determinado no momento da criação do índice pelo parâmetro de armazenamento `pages_per_range`. O número de entradas do índice será igual ao tamanho da relação em páginas dividido pelo valor selecionado para `pages_per_range`. Portanto, quanto menor o número, maior o índice se torna (devido à necessidade de armazenar mais entradas de índice), mas, ao mesmo tempo, os dados resumidos armazenados podem ser mais precisos e mais blocos de dados podem ser ignorados durante uma varredura do índice.

#### 65.5.1.1. Manutenção do índice [#](#BRIN-OPERATION)

No momento da criação, todas as páginas de pilha existentes são verificadas e um índice resumido é criado para cada intervalo, incluindo o intervalo possivelmente incompleto no final. À medida que novas páginas são preenchidas com dados, os intervalos de página que já foram resumidos farão com que as informações resumidas sejam atualizadas com dados dos novos tuplos. Quando uma nova página é criada e não pertence ao último intervalo resumido, o intervalo ao qual a nova página pertence não adquire automaticamente um tuplo resumido; esses tuplos permanecem não resumidos até que uma execução de resumido seja invocada posteriormente, criando o resumo inicial para esse intervalo.

Existem várias maneiras de iniciar a síntese inicial de um intervalo de página. Se a tabela for aspirada, manualmente ou pelo [autovacuum](routine-vacuuming.md#AUTOVACUUM), todos os intervalos de página não resumidos existentes serão resumidos. Além disso, se o parâmetro [autosummarize](sql-createindex.md#INDEX-RELOPTION-AUTOSUMMARIZE) do índice estiver habilitado, o que não é o caso por padrão, sempre que o autovacuum for executado nesse banco de dados, a síntese ocorrerá para todos os intervalos de página não resumidos que tenham sido preenchidos, independentemente de a própria tabela ser processada pelo autovacuum; veja abaixo.

Por último, as seguintes funções podem ser utilizadas (enquanto essas funções estão em execução, [search_path](runtime-config-client.md#GUC-SEARCH-PATH) é temporariamente alterado para `pg_catalog, pg_temp`):

<table border="0" class="simplelist" summary="Simple list">
 <tr>
  <td>
   <code class="function">
    brin_summarize_new_values(regclass)
   </code>
   which summarizes all unsummarized ranges;
  </td>
 </tr>
 <tr>
  <td>
   <code class="function">
    brin_summarize_range(regclass, bigint)
   </code>
   which summarizes only the range containing the given page, if it is unsummarized.
  </td>
 </tr>
</table>

Quando a auto-resumo é habilitada, um pedido é enviado para `autovacuum` para executar uma resumo direcionado para uma faixa de blocos quando uma inserção é detectada para o primeiro item da primeira página da próxima faixa de blocos, para ser cumprido na próxima vez que um trabalhador de auto-vazamento termina de executar no mesmo banco de dados. Se a fila de pedidos estiver cheia, o pedido não é registrado e uma mensagem é enviada para o log do servidor:

```
LOG:  request for BRIN range summarization for index "brin_wi_idx" page 128 was not recorded
```

Quando isso acontecer, a faixa permanecerá não resumida até a próxima sessão regular de vácuo na mesa, ou até que uma das funções mencionadas acima seja invocada.

Por outro lado, uma faixa pode ser desconsiderada usando a função `brin_desummarize_range(regclass, bigint)`, que é útil quando o conjunto de índices não é mais uma representação muito boa, porque os valores existentes mudaram. Veja [Seção 9.28.8](functions-admin.md#FUNCTIONS-ADMIN-INDEX) para detalhes.

### 65.5.2. Classes de operador embutidas [#](#BRIN-BUILTIN-OPCLASSES)

A distribuição principal do PostgreSQL inclui as classes de operadores BRIN mostradas na [Tabela 65.4](brin.md#BRIN-BUILTIN-OPCLASSES-TABLE).

As classes do operador *minmax* armazenam os valores mínimo e máximo que aparecem na coluna indexada dentro do intervalo. As classes do operador *inclusion* armazenam um valor que inclui os valores na coluna indexada dentro do intervalo. As classes do operador *bloom* constroem um filtro Bloom para todos os valores dentro do intervalo. As classes do operador *minmax-multi* armazenam múltiplos valores mínimo e máximo, representando valores que aparecem na coluna indexada dentro do intervalo.

**Tabela 65.4. Classes de operadores BRIN integrados**

<table border="1" class="table" summary="Built-in BRIN Operator Classes">
 <colgroup>
  <col/>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th>
    Name
   </th>
   <th>
    Indexable Operators
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td rowspan="5" valign="middle">
    <code class="literal">
     bit_minmax_ops
    </code>
   </td>
   <td>
    <code class="literal">
     = (bit,bit)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt; (bit,bit)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt; (bit,bit)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt;= (bit,bit)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt;= (bit,bit)
    </code>
   </td>
  </tr>
  <tr>
   <td rowspan="13" valign="middle">
    <code class="literal">
     box_inclusion_ops
    </code>
   </td>
   <td>
    <code class="literal">
     @&gt; (box,point)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt;&lt; (box,box)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &amp;&lt; (box,box)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &amp;&gt; (box,box)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt;&gt; (box,box)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt;@ (box,box)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     @&gt; (box,box)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     ~= (box,box)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &amp;&amp; (box,box)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt;&lt;| (box,box)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &amp;&lt;| (box,box)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     |&amp;&gt; (box,box)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     |&gt;&gt; (box,box)
    </code>
   </td>
  </tr>
  <tr>
   <td valign="middle">
    <code class="literal">
     bpchar_bloom_ops
    </code>
   </td>
   <td>
    <code class="literal">
     = (character,character)
    </code>
   </td>
  </tr>
  <tr>
   <td rowspan="5" valign="middle">
    <code class="literal">
     bpchar_minmax_ops
    </code>
   </td>
   <td>
    <code class="literal">
     = (character,character)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt; (character,character)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt;= (character,character)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt; (character,character)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt;= (character,character)
    </code>
   </td>
  </tr>
  <tr>
   <td valign="middle">
    <code class="literal">
     bytea_bloom_ops
    </code>
   </td>
   <td>
    <code class="literal">
     = (bytea,bytea)
    </code>
   </td>
  </tr>
  <tr>
   <td rowspan="5" valign="middle">
    <code class="literal">
     bytea_minmax_ops
    </code>
   </td>
   <td>
    <code class="literal">
     = (bytea,bytea)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt; (bytea,bytea)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt;= (bytea,bytea)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt; (bytea,bytea)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt;= (bytea,bytea)
    </code>
   </td>
  </tr>
  <tr>
   <td valign="middle">
    <code class="literal">
     char_bloom_ops
    </code>
   </td>
   <td>
    <code class="literal">
     = ("char","char")
    </code>
   </td>
  </tr>
  <tr>
   <td rowspan="5" valign="middle">
    <code class="literal">
     char_minmax_ops
    </code>
   </td>
   <td>
    <code class="literal">
     = ("char","char")
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt; ("char","char")
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt;= ("char","char")
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt; ("char","char")
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt;= ("char","char")
    </code>
   </td>
  </tr>
  <tr>
   <td valign="middle">
    <code class="literal">
     date_bloom_ops
    </code>
   </td>
   <td>
    <code class="literal">
     = (date,date)
    </code>
   </td>
  </tr>
  <tr>
   <td rowspan="5" valign="middle">
    <code class="literal">
     date_minmax_ops
    </code>
   </td>
   <td>
    <code class="literal">
     = (date,date)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt; (date,date)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt;= (date,date)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt; (date,date)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt;= (date,date)
    </code>
   </td>
  </tr>
  <tr>
   <td rowspan="5" valign="middle">
    <code class="literal">
     date_minmax_multi_ops
    </code>
   </td>
   <td>
    <code class="literal">
     = (date,date)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt; (date,date)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt;= (date,date)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt; (date,date)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt;= (date,date)
    </code>
   </td>
  </tr>
  <tr>
   <td valign="middle">
    <code class="literal">
     float4_bloom_ops
    </code>
   </td>
   <td>
    <code class="literal">
     = (float4,float4)
    </code>
   </td>
  </tr>
  <tr>
   <td rowspan="5" valign="middle">
    <code class="literal">
     float4_minmax_ops
    </code>
   </td>
   <td>
    <code class="literal">
     = (float4,float4)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt; (float4,float4)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt; (float4,float4)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt;= (float4,float4)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt;= (float4,float4)
    </code>
   </td>
  </tr>
  <tr>
   <td rowspan="5" valign="middle">
    <code class="literal">
     float4_minmax_multi_ops
    </code>
   </td>
   <td>
    <code class="literal">
     = (float4,float4)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt; (float4,float4)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt; (float4,float4)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt;= (float4,float4)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt;= (float4,float4)
    </code>
   </td>
  </tr>
  <tr>
   <td valign="middle">
    <code class="literal">
     float8_bloom_ops
    </code>
   </td>
   <td>
    <code class="literal">
     = (float8,float8)
    </code>
   </td>
  </tr>
  <tr>
   <td rowspan="5" valign="middle">
    <code class="literal">
     float8_minmax_ops
    </code>
   </td>
   <td>
    <code class="literal">
     = (float8,float8)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt; (float8,float8)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt;= (float8,float8)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt; (float8,float8)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt;= (float8,float8)
    </code>
   </td>
  </tr>
  <tr>
   <td rowspan="5" valign="middle">
    <code class="literal">
     float8_minmax_multi_ops
    </code>
   </td>
   <td>
    <code class="literal">
     = (float8,float8)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt; (float8,float8)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt;= (float8,float8)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt; (float8,float8)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt;= (float8,float8)
    </code>
   </td>
  </tr>
  <tr>
   <td rowspan="6" valign="middle">
    <code class="literal">
     inet_inclusion_ops
    </code>
   </td>
   <td>
    <code class="literal">
     &lt;&lt; (inet,inet)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt;&lt;= (inet,inet)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt;&gt; (inet,inet)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt;&gt;= (inet,inet)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     = (inet,inet)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &amp;&amp; (inet,inet)
    </code>
   </td>
  </tr>
  <tr>
   <td valign="middle">
    <code class="literal">
     inet_bloom_ops
    </code>
   </td>
   <td>
    <code class="literal">
     = (inet,inet)
    </code>
   </td>
  </tr>
  <tr>
   <td rowspan="5" valign="middle">
    <code class="literal">
     inet_minmax_ops
    </code>
   </td>
   <td>
    <code class="literal">
     = (inet,inet)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt; (inet,inet)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt;= (inet,inet)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt; (inet,inet)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt;= (inet,inet)
    </code>
   </td>
  </tr>
  <tr>
   <td rowspan="5" valign="middle">
    <code class="literal">
     inet_minmax_multi_ops
    </code>
   </td>
   <td>
    <code class="literal">
     = (inet,inet)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt; (inet,inet)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt;= (inet,inet)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt; (inet,inet)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt;= (inet,inet)
    </code>
   </td>
  </tr>
  <tr>
   <td valign="middle">
    <code class="literal">
     int2_bloom_ops
    </code>
   </td>
   <td>
    <code class="literal">
     = (int2,int2)
    </code>
   </td>
  </tr>
  <tr>
   <td rowspan="5" valign="middle">
    <code class="literal">
     int2_minmax_ops
    </code>
   </td>
   <td>
    <code class="literal">
     = (int2,int2)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt; (int2,int2)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt; (int2,int2)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt;= (int2,int2)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt;= (int2,int2)
    </code>
   </td>
  </tr>
  <tr>
   <td rowspan="5" valign="middle">
    <code class="literal">
     int2_minmax_multi_ops
    </code>
   </td>
   <td>
    <code class="literal">
     = (int2,int2)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt; (int2,int2)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt; (int2,int2)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt;= (int2,int2)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt;= (int2,int2)
    </code>
   </td>
  </tr>
  <tr>
   <td valign="middle">
    <code class="literal">
     int4_bloom_ops
    </code>
   </td>
   <td>
    <code class="literal">
     = (int4,int4)
    </code>
   </td>
  </tr>
  <tr>
   <td rowspan="5" valign="middle">
    <code class="literal">
     int4_minmax_ops
    </code>
   </td>
   <td>
    <code class="literal">
     = (int4,int4)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt; (int4,int4)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt; (int4,int4)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt;= (int4,int4)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt;= (int4,int4)
    </code>
   </td>
  </tr>
  <tr>
   <td rowspan="5" valign="middle">
    <code class="literal">
     int4_minmax_multi_ops
    </code>
   </td>
   <td>
    <code class="literal">
     = (int4,int4)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt; (int4,int4)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt; (int4,int4)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt;= (int4,int4)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt;= (int4,int4)
    </code>
   </td>
  </tr>
  <tr>
   <td valign="middle">
    <code class="literal">
     int8_bloom_ops
    </code>
   </td>
   <td>
    <code class="literal">
     = (bigint,bigint)
    </code>
   </td>
  </tr>
  <tr>
   <td rowspan="5" valign="middle">
    <code class="literal">
     int8_minmax_ops
    </code>
   </td>
   <td>
    <code class="literal">
     = (bigint,bigint)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt; (bigint,bigint)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt; (bigint,bigint)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt;= (bigint,bigint)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt;= (bigint,bigint)
    </code>
   </td>
  </tr>
  <tr>
   <td rowspan="5" valign="middle">
    <code class="literal">
     int8_minmax_multi_ops
    </code>
   </td>
   <td>
    <code class="literal">
     = (bigint,bigint)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt; (bigint,bigint)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt; (bigint,bigint)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt;= (bigint,bigint)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt;= (bigint,bigint)
    </code>
   </td>
  </tr>
  <tr>
   <td valign="middle">
    <code class="literal">
     interval_bloom_ops
    </code>
   </td>
   <td>
    <code class="literal">
     = (interval,interval)
    </code>
   </td>
  </tr>
  <tr>
   <td rowspan="5" valign="middle">
    <code class="literal">
     interval_minmax_ops
    </code>
   </td>
   <td>
    <code class="literal">
     = (interval,interval)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt; (interval,interval)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt;= (interval,interval)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt; (interval,interval)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt;= (interval,interval)
    </code>
   </td>
  </tr>
  <tr>
   <td rowspan="5" valign="middle">
    <code class="literal">
     interval_minmax_multi_ops
    </code>
   </td>
   <td>
    <code class="literal">
     = (interval,interval)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt; (interval,interval)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt;= (interval,interval)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt; (interval,interval)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt;= (interval,interval)
    </code>
   </td>
  </tr>
  <tr>
   <td valign="middle">
    <code class="literal">
     macaddr_bloom_ops
    </code>
   </td>
   <td>
    <code class="literal">
     = (macaddr,macaddr)
    </code>
   </td>
  </tr>
  <tr>
   <td rowspan="5" valign="middle">
    <code class="literal">
     macaddr_minmax_ops
    </code>
   </td>
   <td>
    <code class="literal">
     = (macaddr,macaddr)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt; (macaddr,macaddr)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt;= (macaddr,macaddr)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt; (macaddr,macaddr)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt;= (macaddr,macaddr)
    </code>
   </td>
  </tr>
  <tr>
   <td rowspan="5" valign="middle">
    <code class="literal">
     macaddr_minmax_multi_ops
    </code>
   </td>
   <td>
    <code class="literal">
     = (macaddr,macaddr)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt; (macaddr,macaddr)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt;= (macaddr,macaddr)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt; (macaddr,macaddr)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt;= (macaddr,macaddr)
    </code>
   </td>
  </tr>
  <tr>
   <td valign="middle">
    <code class="literal">
     macaddr8_bloom_ops
    </code>
   </td>
   <td>
    <code class="literal">
     = (macaddr8,macaddr8)
    </code>
   </td>
  </tr>
  <tr>
   <td rowspan="5" valign="middle">
    <code class="literal">
     macaddr8_minmax_ops
    </code>
   </td>
   <td>
    <code class="literal">
     = (macaddr8,macaddr8)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt; (macaddr8,macaddr8)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt;= (macaddr8,macaddr8)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt; (macaddr8,macaddr8)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt;= (macaddr8,macaddr8)
    </code>
   </td>
  </tr>
  <tr>
   <td rowspan="5" valign="middle">
    <code class="literal">
     macaddr8_minmax_multi_ops
    </code>
   </td>
   <td>
    <code class="literal">
     = (macaddr8,macaddr8)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt; (macaddr8,macaddr8)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt;= (macaddr8,macaddr8)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt; (macaddr8,macaddr8)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt;= (macaddr8,macaddr8)
    </code>
   </td>
  </tr>
  <tr>
   <td valign="middle">
    <code class="literal">
     name_bloom_ops
    </code>
   </td>
   <td>
    <code class="literal">
     = (name,name)
    </code>
   </td>
  </tr>
  <tr>
   <td rowspan="5" valign="middle">
    <code class="literal">
     name_minmax_ops
    </code>
   </td>
   <td>
    <code class="literal">
     = (name,name)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt; (name,name)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt;= (name,name)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt; (name,name)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt;= (name,name)
    </code>
   </td>
  </tr>
  <tr>
   <td valign="middle">
    <code class="literal">
     numeric_bloom_ops
    </code>
   </td>
   <td>
    <code class="literal">
     = (numeric,numeric)
    </code>
   </td>
  </tr>
  <tr>
   <td rowspan="5" valign="middle">
    <code class="literal">
     numeric_minmax_ops
    </code>
   </td>
   <td>
    <code class="literal">
     = (numeric,numeric)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt; (numeric,numeric)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt;= (numeric,numeric)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt; (numeric,numeric)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt;= (numeric,numeric)
    </code>
   </td>
  </tr>
  <tr>
   <td rowspan="5" valign="middle">
    <code class="literal">
     numeric_minmax_multi_ops
    </code>
   </td>
   <td>
    <code class="literal">
     = (numeric,numeric)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt; (numeric,numeric)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt;= (numeric,numeric)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt; (numeric,numeric)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt;= (numeric,numeric)
    </code>
   </td>
  </tr>
  <tr>
   <td valign="middle">
    <code class="literal">
     oid_bloom_ops
    </code>
   </td>
   <td>
    <code class="literal">
     = (oid,oid)
    </code>
   </td>
  </tr>
  <tr>
   <td rowspan="5" valign="middle">
    <code class="literal">
     oid_minmax_ops
    </code>
   </td>
   <td>
    <code class="literal">
     = (oid,oid)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt; (oid,oid)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt; (oid,oid)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt;= (oid,oid)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt;= (oid,oid)
    </code>
   </td>
  </tr>
  <tr>
   <td rowspan="5" valign="middle">
    <code class="literal">
     oid_minmax_multi_ops
    </code>
   </td>
   <td>
    <code class="literal">
     = (oid,oid)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt; (oid,oid)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt; (oid,oid)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt;= (oid,oid)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt;= (oid,oid)
    </code>
   </td>
  </tr>
  <tr>
   <td valign="middle">
    <code class="literal">
     pg_lsn_bloom_ops
    </code>
   </td>
   <td>
    <code class="literal">
     = (pg_lsn,pg_lsn)
    </code>
   </td>
  </tr>
  <tr>
   <td rowspan="5" valign="middle">
    <code class="literal">
     pg_lsn_minmax_ops
    </code>
   </td>
   <td>
    <code class="literal">
     = (pg_lsn,pg_lsn)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt; (pg_lsn,pg_lsn)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt; (pg_lsn,pg_lsn)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt;= (pg_lsn,pg_lsn)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt;= (pg_lsn,pg_lsn)
    </code>
   </td>
  </tr>
  <tr>
   <td rowspan="5" valign="middle">
    <code class="literal">
     pg_lsn_minmax_multi_ops
    </code>
   </td>
   <td>
    <code class="literal">
     = (pg_lsn,pg_lsn)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt; (pg_lsn,pg_lsn)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt; (pg_lsn,pg_lsn)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt;= (pg_lsn,pg_lsn)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt;= (pg_lsn,pg_lsn)
    </code>
   </td>
  </tr>
  <tr>
   <td rowspan="14" valign="middle">
    <code class="literal">
     range_inclusion_ops
    </code>
   </td>
   <td>
    <code class="literal">
     = (anyrange,anyrange)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt; (anyrange,anyrange)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt;= (anyrange,anyrange)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt;= (anyrange,anyrange)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt; (anyrange,anyrange)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &amp;&amp; (anyrange,anyrange)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     @&gt; (anyrange,anyelement)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     @&gt; (anyrange,anyrange)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt;@ (anyrange,anyrange)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt;&lt; (anyrange,anyrange)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt;&gt; (anyrange,anyrange)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &amp;&lt; (anyrange,anyrange)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &amp;&gt; (anyrange,anyrange)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     -|- (anyrange,anyrange)
    </code>
   </td>
  </tr>
  <tr>
   <td valign="middle">
    <code class="literal">
     text_bloom_ops
    </code>
   </td>
   <td>
    <code class="literal">
     = (text,text)
    </code>
   </td>
  </tr>
  <tr>
   <td rowspan="5" valign="middle">
    <code class="literal">
     text_minmax_ops
    </code>
   </td>
   <td>
    <code class="literal">
     = (text,text)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt; (text,text)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt;= (text,text)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt; (text,text)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt;= (text,text)
    </code>
   </td>
  </tr>
  <tr>
   <td valign="middle">
    <code class="literal">
     tid_bloom_ops
    </code>
   </td>
   <td>
    <code class="literal">
     = (tid,tid)
    </code>
   </td>
  </tr>
  <tr>
   <td rowspan="5" valign="middle">
    <code class="literal">
     tid_minmax_ops
    </code>
   </td>
   <td>
    <code class="literal">
     = (tid,tid)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt; (tid,tid)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt; (tid,tid)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt;= (tid,tid)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt;= (tid,tid)
    </code>
   </td>
  </tr>
  <tr>
   <td rowspan="5" valign="middle">
    <code class="literal">
     tid_minmax_multi_ops
    </code>
   </td>
   <td>
    <code class="literal">
     = (tid,tid)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt; (tid,tid)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt; (tid,tid)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt;= (tid,tid)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt;= (tid,tid)
    </code>
   </td>
  </tr>
  <tr>
   <td valign="middle">
    <code class="literal">
     timestamp_bloom_ops
    </code>
   </td>
   <td>
    <code class="literal">
     = (timestamp,timestamp)
    </code>
   </td>
  </tr>
  <tr>
   <td rowspan="5" valign="middle">
    <code class="literal">
     timestamp_minmax_ops
    </code>
   </td>
   <td>
    <code class="literal">
     = (timestamp,timestamp)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt; (timestamp,timestamp)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt;= (timestamp,timestamp)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt; (timestamp,timestamp)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt;= (timestamp,timestamp)
    </code>
   </td>
  </tr>
  <tr>
   <td rowspan="5" valign="middle">
    <code class="literal">
     timestamp_minmax_multi_ops
    </code>
   </td>
   <td>
    <code class="literal">
     = (timestamp,timestamp)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt; (timestamp,timestamp)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt;= (timestamp,timestamp)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt; (timestamp,timestamp)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt;= (timestamp,timestamp)
    </code>
   </td>
  </tr>
  <tr>
   <td valign="middle">
    <code class="literal">
     timestamptz_bloom_ops
    </code>
   </td>
   <td>
    <code class="literal">
     = (timestamptz,timestamptz)
    </code>
   </td>
  </tr>
  <tr>
   <td rowspan="5" valign="middle">
    <code class="literal">
     timestamptz_minmax_ops
    </code>
   </td>
   <td>
    <code class="literal">
     = (timestamptz,timestamptz)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt; (timestamptz,timestamptz)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt;= (timestamptz,timestamptz)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt; (timestamptz,timestamptz)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt;= (timestamptz,timestamptz)
    </code>
   </td>
  </tr>
  <tr>
   <td rowspan="5" valign="middle">
    <code class="literal">
     timestamptz_minmax_multi_ops
    </code>
   </td>
   <td>
    <code class="literal">
     = (timestamptz,timestamptz)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt; (timestamptz,timestamptz)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt;= (timestamptz,timestamptz)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt; (timestamptz,timestamptz)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt;= (timestamptz,timestamptz)
    </code>
   </td>
  </tr>
  <tr>
   <td valign="middle">
    <code class="literal">
     time_bloom_ops
    </code>
   </td>
   <td>
    <code class="literal">
     = (time,time)
    </code>
   </td>
  </tr>
  <tr>
   <td rowspan="5" valign="middle">
    <code class="literal">
     time_minmax_ops
    </code>
   </td>
   <td>
    <code class="literal">
     = (time,time)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt; (time,time)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt;= (time,time)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt; (time,time)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt;= (time,time)
    </code>
   </td>
  </tr>
  <tr>
   <td rowspan="5" valign="middle">
    <code class="literal">
     time_minmax_multi_ops
    </code>
   </td>
   <td>
    <code class="literal">
     = (time,time)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt; (time,time)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt;= (time,time)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt; (time,time)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt;= (time,time)
    </code>
   </td>
  </tr>
  <tr>
   <td valign="middle">
    <code class="literal">
     timetz_bloom_ops
    </code>
   </td>
   <td>
    <code class="literal">
     = (timetz,timetz)
    </code>
   </td>
  </tr>
  <tr>
   <td rowspan="5" valign="middle">
    <code class="literal">
     timetz_minmax_ops
    </code>
   </td>
   <td>
    <code class="literal">
     = (timetz,timetz)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt; (timetz,timetz)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt;= (timetz,timetz)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt; (timetz,timetz)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt;= (timetz,timetz)
    </code>
   </td>
  </tr>
  <tr>
   <td rowspan="5" valign="middle">
    <code class="literal">
     timetz_minmax_multi_ops
    </code>
   </td>
   <td>
    <code class="literal">
     = (timetz,timetz)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt; (timetz,timetz)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt;= (timetz,timetz)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt; (timetz,timetz)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt;= (timetz,timetz)
    </code>
   </td>
  </tr>
  <tr>
   <td valign="middle">
    <code class="literal">
     uuid_bloom_ops
    </code>
   </td>
   <td>
    <code class="literal">
     = (uuid,uuid)
    </code>
   </td>
  </tr>
  <tr>
   <td rowspan="5" valign="middle">
    <code class="literal">
     uuid_minmax_ops
    </code>
   </td>
   <td>
    <code class="literal">
     = (uuid,uuid)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt; (uuid,uuid)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt; (uuid,uuid)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt;= (uuid,uuid)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt;= (uuid,uuid)
    </code>
   </td>
  </tr>
  <tr>
   <td rowspan="5" valign="middle">
    <code class="literal">
     uuid_minmax_multi_ops
    </code>
   </td>
   <td>
    <code class="literal">
     = (uuid,uuid)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt; (uuid,uuid)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt; (uuid,uuid)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt;= (uuid,uuid)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt;= (uuid,uuid)
    </code>
   </td>
  </tr>
  <tr>
   <td rowspan="5" valign="middle">
    <code class="literal">
     varbit_minmax_ops
    </code>
   </td>
   <td>
    <code class="literal">
     = (varbit,varbit)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt; (varbit,varbit)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt; (varbit,varbit)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &lt;= (varbit,varbit)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     &gt;= (varbit,varbit)
    </code>
   </td>
  </tr>
 </tbody>
</table>










#### 65.5.2.1. Parâmetros da Classe do Operador [#](#BRIN-BUILTIN-OPCLASSES--PARAMETERS)

Algumas das classes de operadores embutidas permitem especificar parâmetros que afetam o comportamento da classe de operador. Cada classe de operador tem seu próprio conjunto de parâmetros permitidos. Apenas as classes de operadores `bloom` e `minmax-multi` permitem especificar parâmetros:

As classes do operador bloom aceitam esses parâmetros:

`n_distinct_per_range`: Define o número estimado de valores distintos não nulos na faixa do bloco, utilizado pelos índices de floração BRIN para dimensionamento do filtro de Bloom. Comporta-se de forma semelhante à opção `n_distinct` para [ALTER TABLE](sql-altertable.md "ALTER TABLE"). Quando definido para um valor positivo, cada faixa do bloco é assumida para conter esse número de valores distintos não nulos. Quando definido para um valor negativo, que deve ser maior ou igual a -1, o número de valores distintos não nulos é assumido para crescer linearmente com o número máximo possível de tuplas na faixa do bloco (cerca de 290 linhas por bloco). O valor padrão é `-0.1`, e o número mínimo de valores distintos não nulos é `16`.

`false_positive_rate`: Define a taxa de falso positivo desejada usada pelo índice de Bloom BRIN para o dimensionamento do filtro Bloom. Os valores devem estar entre 0,0001 e 0,25. O valor padrão é 0,01, que é uma taxa de falso positivo de 1%.

As classes de operadores minmax-multi aceitam esses parâmetros:

`values_per_range`: Define o número máximo de valores armazenados por índices minmax BRIN para resumir um intervalo de bloco. Cada valor pode representar um ponto ou uma fronteira de um intervalo. Os valores devem estar entre 8 e 256, e o valor padrão é 32.

### 65.5.3. Extensibilidade [#](#BRIN-EXTENSIBILITY)

A interface BRIN possui um alto nível de abstração, exigindo que o implementador do método de acesso implemente apenas a semântica do tipo de dados a ser acessado. A própria camada BRIN cuida da concorrência, do registro e da busca na estrutura do índice.

Tudo o que é necessário para fazer um método de acesso BRIN funcionar é implementar alguns métodos definidos pelo usuário, que definem o comportamento dos valores resumidos armazenados no índice e a maneira como eles interagem com as chaves de varredura. Em suma, o BRIN combina extensibilidade com generalidade, reutilização de código e uma interface limpa.

Existem quatro métodos que uma classe de operador para BRIN deve fornecer:

`BrinOpcInfo *opcInfo(Oid type_oid)`: Retorna informações internas sobre os dados resumidos das colunas indexadas. O valor de retorno deve apontar para um `BrinOpcInfo` palloc, que tem esta definição:

```
typedef struct BrinOpcInfo { /* Number of columns stored in an index column of this opclass */ uint16      oi_nstored;

/* Opaque pointer for the opclass' private use */ void       *oi_opaque;

/* Type cache entries of the stored columns */ TypeCacheEntry *oi_typcache[FLEXIBLE_ARRAY_MEMBER]; } BrinOpcInfo;
```

`BrinOpcInfo`.`oi_opaque` pode ser usado pelas rotinas da classe de operador para passar informações entre funções de suporte durante uma varredura de índice.

`bool consistent(BrinDesc *bdesc, BrinValues *column, ScanKey *keys, int nkeys)`: Retorna se todas as entradas do ScanKey são consistentes com os valores indexados fornecidos para uma faixa. O número de atributo a ser usado é passado como parte da chave de varredura. Múltiplas chaves de varredura para o mesmo atributo podem ser passadas de uma só vez; o número de entradas é determinado pelo parâmetro `nkeys`.

`bool consistent(BrinDesc *bdesc, BrinValues *column, ScanKey key)`: Retorna se o ScanKey é consistente com os valores indexados fornecidos para uma faixa. O número do atributo a ser usado é passado como parte da chave de varredura. Esta é uma versão mais antiga e compatível com versões anteriores da função consistente.

`bool addValue(BrinDesc *bdesc, BrinValues *column, Datum newval, bool isnull)`: Dado um tuplo de índice e um valor indexado, modifica o atributo indicado da tupla de modo que ele represente adicionalmente o novo valor. Se alguma modificação foi feita na tupla, `true` é retornado.

`bool unionTuples(BrinDesc *bdesc, BrinValues *a, BrinValues *b)`: Consolida dois tuplos de índice. Dado dois tuplos de índice, modifica o atributo indicado do primeiro deles de modo que ele represente ambos os tuplos. O segundo tuplo não é modificado.

Uma classe de operador para BRIN pode especificar opcionalmente o seguinte método:

`void options(local_relopts *relopts)`: Define um conjunto de parâmetros visíveis pelo usuário que controlam o comportamento da classe do operador.

A função `options` é passada um ponteiro para uma estrutura `local_relopts`, que precisa ser preenchida com um conjunto de opções específicas da classe do operador. As opções podem ser acessadas a partir de outras funções de suporte usando as macros `PG_HAS_OPCLASS_OPTIONS()` e `PG_GET_OPCLASS_OPTIONS()`.

Como a extração de chaves de valores indexados e a representação da chave no BRIN são flexíveis, elas podem depender de parâmetros especificados pelo usuário.

A distribuição principal inclui suporte para quatro tipos de classes de operador: minmax, minmax-multi, inclusão e bloom. As definições das classes de operador que as utilizam são fornecidas para tipos de dados em núcleo conforme apropriado. Classes de operador adicionais podem ser definidas pelo usuário para outros tipos de dados usando definições equivalentes, sem precisar escrever código fonte; declarações de entradas de catálogo apropriadas são suficientes. Note que as suposições sobre a semântica das estratégias de operador estão incorporadas no código-fonte das funções de suporte.

Classes de operador que implementam semânticas completamente diferentes também são possíveis, desde que sejam escritas implementações das quatro funções de suporte principais descritas acima. Observe que a compatibilidade reversa entre as principais versões não é garantida: por exemplo, funções de suporte adicionais podem ser necessárias em versões posteriores.

Para escrever uma classe de operador para um tipo de dados que implementa um conjunto totalmente ordenado, é possível usar as funções de suporte minmax juntamente com os operadores correspondentes, conforme mostrado em [Tabela 65.5] (brin.md#BRIN-EXTENSIBILITY-MINMAX-TABLE "Table 65.5. Function and Support Numbers for Minmax Operator Classes"). Todos os membros da classe de operador (funções e operadores) são obrigatórios.

**Tabela 65.5. Números de função e suporte para as classes do operador Minmax**



<table border="1" class="table" summary="Function and Support Numbers for Minmax Operator Classes">
 <colgroup>
  <col class="col1"/>
  <col class="col2"/>
 </colgroup>
 <thead>
  <tr>
   <th>
    Membro da classe do operador
   </th>
   <th>
    Object
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    Função de Suporte 1
   </td>
   <td>
    internal function
    <code class="function">
     brin_minmax_opcinfo()
    </code>
   </td>
  </tr>
  <tr>
   <td>
    Função de Suporte 2
   </td>
   <td>
    internal function
    <code class="function">
     brin_minmax_add_value()
    </code>
   </td>
  </tr>
  <tr>
   <td>
    Função de Suporte 3
   </td>
   <td>
    internal function
    <code class="function">
     brin_minmax_consistent()
    </code>
   </td>
  </tr>
  <tr>
   <td>
    Função de Suporte 4
   </td>
   <td>
    internal function
    <code class="function">
     brin_minmax_union()
    </code>
   </td>
  </tr>
  <tr>
   <td>
    Estratégia do Operador 1
   </td>
   <td>
    operator less-than
   </td>
  </tr>
  <tr>
   <td>
    Estratégia do Operador 2
   </td>
   <td>
    operator less-than-or-equal-to
   </td>
  </tr>
  <tr>
   <td>
    Estratégia do Operador 3
   </td>
   <td>
    operator equal-to
   </td>
  </tr>
  <tr>
   <td>
    Estratégia do Operador 4
   </td>
   <td>
    operator greater-than-or-equal-to
   </td>
  </tr>
  <tr>
   <td>
    Estratégia do Operador 5
   </td>
   <td>
    operator greater-than
   </td>
  </tr>
 </tbody>
</table>










Para escrever uma classe de operador para um tipo de dados complexo que tem valores incluídos dentro de outro tipo, é possível usar as funções de suporte à inclusão juntamente com os operadores correspondentes, conforme mostrado em [Tabela 65.6] (brin.md#BRIN-EXTENSIBILITY-INCLUSION-TABLE "Table 65.6. Function and Support Numbers for Inclusion Operator Classes"). Requer apenas uma única função adicional, que pode ser escrita em qualquer idioma. Mais funções podem ser definidas para funcionalidades adicionais. Todos os operadores são opcionais. Alguns operadores requerem outros operadores, conforme mostrado como dependências na tabela.

**Tabela 65.6. Números de Função e Suporte para Classes de Operador de Inclusão**



<table border="1" class="table" summary="Function and Support Numbers for Inclusion Operator Classes">
 <colgroup>
  <col class="col1"/>
  <col class="col2"/>
  <col class="col3"/>
 </colgroup>
 <thead>
  <tr>
   <th>
    Membro da classe do operador
   </th>
   <th>
    Object
   </th>
   <th>
    Dependência
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    Função de Suporte 1
   </td>
   <td>
    função interna
    <code class="function">
     brin_inclusion_opcinfo()
    </code>
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>
    Função de Suporte 2
   </td>
   <td>
    função interna
    <code class="function">
     brin_inclusion_add_value()
    </code>
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>
    Função de Suporte 3
   </td>
   <td>
    função interna
    <code class="function">
     brin_inclusion_consistent()
    </code>
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>
    Função de Suporte 4
   </td>
   <td>
    função interna
    <code class="function">
     brin_inclusion_union()
    </code>
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>
    Função de Suporte 11
   </td>
   <td>
    função para combinar dois elementos
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>
    Função de Suporte 12
   </td>
   <td>
    função opcional para verificar se dois elementos são mescíveis
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>
    Função de Suporte 13
   </td>
   <td>
    função opcional para verificar se um elemento está contido em outro
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>
    Função de Suporte 14
   </td>
   <td>
    função opcional para verificar se um elemento está vazio
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>
    Estratégia do Operador 1
   </td>
   <td>
    operador à esquerda
   </td>
   <td>
    Estratégia do Operador 4
   </td>
  </tr>
  <tr>
   <td>
    Estratégia do Operador 2
   </td>
   <td>
    operador não se estende à direita
   </td>
   <td>
    Estratégia do Operador 5
   </td>
  </tr>
  <tr>
   <td>
    Estratégia do Operador 3
   </td>
   <td>
    sobreposição de operadores
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>
    Estratégia do Operador 4
   </td>
   <td>
    operador não se estende à esquerda
   </td>
   <td>
    Estratégia do Operador 1
   </td>
  </tr>
  <tr>
   <td>
    Estratégia do Operador 5
   </td>
   <td>
    direito de operador
   </td>
   <td>
    Estratégia do Operador 2
   </td>
  </tr>
  <tr>
   <td>
    Estratégia do Operador 6, 18
   </td>
   <td>
    operador igual a ou igual ou superior a
   </td>
   <td>
    Estratégia do Operador 7
   </td>
  </tr>
  <tr>
   <td>
    Estratégia do Operador 7, 16, 24, 25
   </td>
   <td>
    operador contém-ou-igual-a
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>
    Estratégia do Operador 8, 26, 27
   </td>
   <td>
    operador é contido por ou igual a
   </td>
   <td>
    Estratégia do Operador 3
   </td>
  </tr>
  <tr>
   <td>
    Estratégia do Operador 9
   </td>
   <td>
    operador não se estende acima
   </td>
   <td>
    Estratégia do Operador 11
   </td>
  </tr>
  <tr>
   <td>
    Estratégia do Operador 10
   </td>
   <td>
    operador é-de-baixo
   </td>
   <td>
    Estratégia do Operador 12
   </td>
  </tr>
  <tr>
   <td>
    Estratégia do Operador 11
   </td>
   <td>
    operador é-superior
   </td>
   <td>
    Estratégia do Operador 9
   </td>
  </tr>
  <tr>
   <td>
    Estratégia do Operador 12
   </td>
   <td>
    operador não estende abaixo
   </td>
   <td>
    Estratégia do Operador 10
   </td>
  </tr>
  <tr>
   <td>
    Estratégia do Operador 20
   </td>
   <td>
    operador menos-que
   </td>
   <td>
    Estratégia do Operador 5
   </td>
  </tr>
  <tr>
   <td>
    Estratégia do Operador 21
   </td>
   <td>
    operador menor ou igual a
   </td>
   <td>
    Estratégia do Operador 5
   </td>
  </tr>
  <tr>
   <td>
    Estratégia do Operador 22
   </td>
   <td>
    operador maior que
   </td>
   <td>
    Estratégia do Operador 1
   </td>
  </tr>
  <tr>
   <td>
    Estratégia do Operador 23
   </td>
   <td>
    operador maior que ou igual a
   </td>
   <td>
    Estratégia do Operador 1
   </td>
  </tr>
 </tbody>
</table>










Os números de função de suporte de 1 a 10 são reservados para as funções internas do BRIN, então as funções do nível SQL começam com o número 11. O número de função de suporte 11 é a função principal necessária para construir o índice. Ele deve aceitar dois argumentos com o mesmo tipo de dados que a classe de operador, e retornar a união deles. A classe de operador de inclusão pode armazenar valores de união com diferentes tipos de dados se for definida com o parâmetro `STORAGE`. O valor de retorno da função de união deve corresponder ao tipo de dados `STORAGE`.

Os números de suporte 12 e 14 são fornecidos para suportar irregularidades de tipos de dados embutidos. O número de função 12 é usado para suportar endereços de rede de diferentes famílias que não podem ser mesclados. O número de função 14 é usado para suportar intervalos vazios. O número de função 13 é um opcional, mas recomendado, que permite que o novo valor seja verificado antes de ser passado para a função de união. Como o quadro BRIN pode agilizar algumas operações quando a união não é alterada, usar essa função pode melhorar o desempenho do índice.

Para escrever uma classe de operador para um tipo de dados que implemente apenas um operador de igualdade e suporte a agregação, é possível usar os procedimentos de suporte a blocos juntamente com os operadores correspondentes, conforme mostrado em [Tabela 65.7](brin.md#BRIN-EXTENSIBILITY-BLOOM-TABLE). Todos os membros da classe de operador (procedimentos e operadores) são obrigatórios.

**Tabela 65.7. Procedimento e números de suporte para as classes do operador Bloom**



<table border="1" class="table" summary="Procedure and Support Numbers for Bloom Operator Classes">
 <colgroup>
  <col/>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th>
    Membro da classe do operador
   </th>
   <th>
    Object
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    Procedimento de Suporte 1
   </td>
   <td>
    internal function
    <code class="function">
     brin_bloom_opcinfo()
    </code>
   </td>
  </tr>
  <tr>
   <td>
    Procedimento de Suporte 2
   </td>
   <td>
    internal function
    <code class="function">
     brin_bloom_add_value()
    </code>
   </td>
  </tr>
  <tr>
   <td>
    Procedimento de Suporte 3
   </td>
   <td>
    internal function
    <code class="function">
     brin_bloom_consistent()
    </code>
   </td>
  </tr>
  <tr>
   <td>
    Procedimento de Suporte 4
   </td>
   <td>
    internal function
    <code class="function">
     brin_bloom_union()
    </code>
   </td>
  </tr>
  <tr>
   <td>
    Procedimento de Suporte 5
   </td>
   <td>
    internal function
    <code class="function">
     brin_bloom_options()
    </code>
   </td>
  </tr>
  <tr>
   <td>
    Procedimento de Suporte 11
   </td>
   <td>
    function to compute hash of an element
   </td>
  </tr>
  <tr>
   <td>
    Estratégia do Operador 1
   </td>
   <td>
    operator equal-to
   </td>
  </tr>
 </tbody>
</table>










Os números de procedimento de suporte 1-10 são reservados para as funções internas do BRIN, então as funções de nível SQL começam com o número 11. O número de função de suporte 11 é a função principal necessária para construir o índice. Ele deve aceitar um argumento com o mesmo tipo de dados que a classe de operador e retornar um hash do valor.

A classe do operador minmax-multi também é destinada a tipos de dados que implementam um conjunto totalmente ordenado e pode ser vista como uma simples extensão da classe do operador minmax. Enquanto a classe do operador minmax resume os valores de cada intervalo de bloco em um único intervalo contínuo, o minmax-multi permite a resumo em múltiplos intervalos menores para melhorar o tratamento de valores atípicos. É possível usar os procedimentos de suporte do minmax-multi juntamente com os operadores correspondentes, conforme mostrado em [Tabela 65.8](brin.md#BRIN-EXTENSIBILITY-MINMAX-MULTI-TABLE). Todos os membros da classe do operador (procedimentos e operadores) são obrigatórios.

**Tabela 65.8. Procedimentos e números de suporte para as classes de operadores minmax-multi**



<table border="1" class="table" summary="Procedure and Support Numbers for minmax-multi Operator Classes">
 <colgroup>
  <col/>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th>
    Membro da classe do operador
   </th>
   <th>
    Object
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    Procedimento de Suporte 1
   </td>
   <td>
    função interna
    <code class="function">
     brin_minmax_multi_opcinfo()
    </code>
   </td>
  </tr>
  <tr>
   <td>
    Procedimento de Suporte 2
   </td>
   <td>
    função interna
    <code class="function">
     brin_minmax_multi_add_value()
    </code>
   </td>
  </tr>
  <tr>
   <td>
    Procedimento de Suporte 3
   </td>
   <td>
    função interna
    <code class="function">
     brin_minmax_multi_consistent()
    </code>
   </td>
  </tr>
  <tr>
   <td>
    Procedimento de Suporte 4
   </td>
   <td>
    função interna
    <code class="function">
     brin_minmax_multi_union()
    </code>
   </td>
  </tr>
  <tr>
   <td>
    Procedimento de Suporte 5
   </td>
   <td>
    função interna
    <code class="function">
     brin_minmax_multi_options()
    </code>
   </td>
  </tr>
  <tr>
   <td>
    Procedimento de Suporte 11
   </td>
   <td>
    função para calcular a distância entre dois valores (comprimento de uma faixa)
   </td>
  </tr>
  <tr>
   <td>
    Estratégia do Operador 1
   </td>
   <td>
    operador menos-que
   </td>
  </tr>
  <tr>
   <td>
    Estratégia do Operador 2
   </td>
   <td>
    operador menor ou igual a
   </td>
  </tr>
  <tr>
   <td>
    Estratégia do Operador 3
   </td>
   <td>
    operador igual a
   </td>
  </tr>
  <tr>
   <td>
    Estratégia do Operador 4
   </td>
   <td>
    operador maior que ou igual a
   </td>
  </tr>
  <tr>
   <td>
    Estratégia do Operador 5
   </td>
   <td>
    operador maior que
   </td>
  </tr>
 </tbody>
</table>










As classes de operadores minmax e de inclusão suportam operadores cruzados entre tipos de dados, embora, com essas, as dependências se tornem mais complicadas. A classe de operadores minmax requer um conjunto completo de operadores para serem definidos, com ambos os argumentos tendo o mesmo tipo de dados. Ela permite que outros tipos de dados sejam suportados definindo conjuntos adicionais de operadores. As estratégias de operadores de classe de inclusão dependem de outra estratégia de operador, conforme mostrado em [Tabela 65.6] (brin.md#BRIN-EXTENSIBILITY-INCLUSION-TABLE "Table 65.6. Function and Support Numbers for Inclusion Operator Classes"), ou da mesma estratégia de operador que elas mesmas. Elas requerem que o operador de dependência seja definido com o tipo de dados `STORAGE` como argumento do lado esquerdo e o outro tipo de dados suportado ser o argumento do lado direito do operador suportado. Veja `float4_minmax_ops` como um exemplo de minmax, e `box_inclusion_ops` como um exemplo de inclusão.