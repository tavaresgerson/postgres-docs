## F.19. intarray — manipular arrays de inteiros [#](#INTARRAY)

* [F.19.1. `intarray` Funções e Operadores](intarray.md#INTARRAY-FUNCS-OPS)
* [F.19.2. Suporte de Índice](intarray.md#INTARRAY-INDEX)
* [F.19.3. Exemplo](intarray.md#INTARRAY-EXAMPLE)
* [F.19.4. Benchmark](intarray.md#INTARRAY-BENCHMARK)
* [F.19.5. Autores](intarray.md#INTARRAY-AUTHORS)

O módulo `intarray` oferece uma série de funções e operadores úteis para manipular arrays de inteiros livres de nulos. Há também suporte para pesquisas indexadas usando alguns dos operadores.

Todas essas operações irão lançar um erro se um array fornecido contiver quaisquer elementos NULL.

Muitas dessas operações são sensíveis apenas para matrizes unidimensionais. Embora elas aceitem matrizes de entrada com mais dimensões, os dados são tratados como se fossem uma matriz linear na ordem de armazenamento.

Este módulo é considerado "confiável", ou seja, pode ser instalado por usuários não superusuários que possuem privilégio `CREATE` no banco de dados atual.

### F.19.1. `intarray` Funções e Operadores [#](#INTARRAY-FUNCS-OPS)

As funções fornecidas pelo módulo `intarray` são mostradas na [Tabela F.8](intarray.md#INTARRAY-FUNC-TABLE "Table F.8. intarray Functions"), os operadores na [Tabela F.9](intarray.md#INTARRAY-OP-TABLE "Table F.9. intarray Operators").

**Tabela F.8. `intarray` Funções**



<table>
 <colgroup>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th class="func_table_entry">
    <p class="func_signature">
     Função
    </p>
    <p>
     Descrição
    </p>
    <p>
     Exemplo(s)
    </p>
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      icount
     </code>
     (
     <code>
      integer[]
     </code>
     )
     <code>
      integer
     </code>
    </p>
    <p>
     Retorna o número de elementos na matriz.
    </p>
    <p>
     <code>
      icount('{1,2,3}'::integer[])
     </code>
     →
     <code>
      3
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      sort
     </code>
     (
     <code>
      integer[]
     </code>
     ,
     <em class="parameter">
      <code>
       dir
      </code>
     </em>
     <code>
      text
     </code>
     )
     <code>
      integer[]
     </code>
    </p>
    <p>
     Ordena o array em ordem crescente ou decrescente.
     <em class="parameter">
      <code>
       dir
      </code>
     </em>
     devem ser
     <code>
      asc
     </code>
     ou
     <code>
      desc
     </code>
     .
    </p>
    <p>
     <code>
      sort('{1,3,2}'::integer[], 'desc')
     </code>
     →
     <code>
      {3,2,1}
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      sort
     </code>
     (
     <code>
      integer[]
     </code>
     )
     <code>
      integer[]
     </code>
    </p>
    <p class="func_signature">
     <code>
      sort_asc
     </code>
     (
     <code>
      integer[]
     </code>
     )
     <code>
      integer[]
     </code>
    </p>
    <p>
     Ordena em ordem ascendente.
    </p>
    <p>
     <code>
      sort(array[11,77,44])
     </code>
     →
     <code>
      {11,44,77}
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      sort_desc
     </code>
     (
     <code>
      integer[]
     </code>
     )
     <code>
      integer[]
     </code>
    </p>
    <p>
     Ordena em ordem decrescente.
    </p>
    <p>
     <code>
      sort_desc(array[11,77,44])
     </code>
     →
     <code>
      {77,44,11}
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      uniq
     </code>
     (
     <code>
      integer[]
     </code>
     )
     <code>
      integer[]
     </code>
    </p>
    <p>
     Remove duplicatas adjacentes. Frequentemente usado com
     <code>
      sort
     </code>
     para remover todas as duplicatas.
    </p>
    <p>
     <code>
      uniq('{1,2,2,3,1,1}'::integer[])
     </code>
     →
     <code>
      {1,2,3,1}
     </code>
    </p>
    <p>
     <code>
      uniq(sort('{1,2,3,2,1}'::integer[]))
     </code>
     →
     <code>
      {1,2,3}
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      idx
     </code>
     (
     <code>
      integer[]
     </code>
     ,
     <em class="parameter">
      <code>
       item
      </code>
     </em>
     <code>
      integer
     </code>
     )
     <code>
      integer
     </code>
    </p>
    <p>
     Retorna o índice do primeiro elemento da matriz que corresponde a
     <em class="parameter">
      <code>
       item
      </code>
     </em>
     , ou 0 se não houver correspondência.
    </p>
    <p>
     <code>
      idx(array[11,22,33,22,11], 22)
     </code>
     →
     <code>
      2
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      subarray
     </code>
     (
     <code>
      integer[]
     </code>
     ,
     <em class="parameter">
      <code>
       start
      </code>
     </em>
     <code>
      integer
     </code>
     ,
     <em class="parameter">
      <code>
       len
      </code>
     </em>
     <code>
      integer
     </code>
     )
     <code>
      integer[]
     </code>
    </p>
    <p>
     Extrai a porção do array que começa na posição
     <em class="parameter">
      <code>
       start
      </code>
     </em>
     , com
     <em class="parameter">
      <code>
       len
      </code>
     </em>
     elements.
    </p>
    <p>
     <code>
      subarray('{1,2,3,2,1}'::integer[], 2, 3)
     </code>
     →
     <code>
      {2,3,2}
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      subarray
     </code>
     (
     <code>
      integer[]
     </code>
     ,
     <em class="parameter">
      <code>
       start
      </code>
     </em>
     <code>
      integer
     </code>
     )
     <code>
      integer[]
     </code>
    </p>
    <p>
     Extrai a porção do array que começa na posição
     <em class="parameter">
      <code>
       start
      </code>
     </em>
     .
    </p>
    <p>
     <code>
      subarray('{1,2,3,2,1}'::integer[], 2)
     </code>
     →
     <code>
      {2,3,2,1}
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      intset
     </code>
     (
     <code>
      integer
     </code>
     )
     <code>
      integer[]
     </code>
    </p>
    <p>
     Faz um array de um único elemento.
    </p>
    <p>
     <code>
      intset(42)
     </code>
     →
     <code>
      {42}
     </code>
    </p>
   </td>
  </tr>
 </tbody>
</table>










**Tabela F.9. Operadores `intarray`**



<table>
 <colgroup>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th class="func_table_entry">
    <p class="func_signature">
     Operador
    </p>
    <p>
     Descrição
    </p>
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      integer[]
     </code>
     <code>
      &amp;&amp;
     </code>
     <code>
      integer[]
     </code>
     →
     <code>
      boolean
     </code>
    </p>
    <p>
     Os arrays se sobrepõem (têm pelo menos um elemento em comum)?
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      integer[]
     </code>
     <code>
      @&gt;
     </code>
     <code>
      integer[]
     </code>
     →
     <code>
      boolean
     </code>
    </p>
    <p>
     A matriz esquerda contém a matriz direita?
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      integer[]
     </code>
     <code>
      &lt;@
     </code>
     <code>
      integer[]
     </code>
     →
     <code>
      boolean
     </code>
    </p>
    <p>
     A matriz esquerda está contida na matriz direita?
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
     </code>
     <code>
      #
     </code>
     <code>
      integer[]
     </code>
     →
     <code>
      integer
     </code>
    </p>
    <p>
     Retorna o número de elementos na matriz.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      integer[]
     </code>
     <code>
      #
     </code>
     <code>
      integer
     </code>
     →
     <code>
      integer
     </code>
    </p>
    <p>
     Retorna o índice do primeiro elemento da matriz que corresponde ao argumento correto, ou 0 se não houver correspondência. (O mesmo que
     <code>
      idx
     </code>
     function.)
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      integer[]
     </code>
     <code>
      +
     </code>
     <code>
      integer
     </code>
     →
     <code>
      integer[]
     </code>
    </p>
    <p>
     Adiciona um elemento ao final do array.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      integer[]
     </code>
     <code>
      +
     </code>
     <code>
      integer[]
     </code>
     →
     <code>
      integer[]
     </code>
    </p>
    <p>
     Concatenia os arrays.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      integer[]
     </code>
     <code>
      -
     </code>
     <code>
      integer
     </code>
     →
     <code>
      integer[]
     </code>
    </p>
    <p>
     Remove entradas que correspondem ao argumento correto do array.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      integer[]
     </code>
     <code>
      -
     </code>
     <code>
      integer[]
     </code>
     →
     <code>
      integer[]
     </code>
    </p>
    <p>
     Remove elementos da matriz da direita da matriz da esquerda.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      integer[]
     </code>
     <code>
      |
     </code>
     <code>
      integer
     </code>
     →
     <code>
      integer[]
     </code>
    </p>
    <p>
     Calcula a união dos argumentos.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      integer[]
     </code>
     <code>
      |
     </code>
     <code>
      integer[]
     </code>
     →
     <code>
      integer[]
     </code>
    </p>
    <p>
     Calcula a união dos argumentos.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      integer[]
     </code>
     <code>
      &amp;
     </code>
     <code>
      integer[]
     </code>
     →
     <code>
      integer[]
     </code>
    </p>
    <p>
     Calcula a interseção dos argumentos.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      integer[]
     </code>
     <code>
      @@
     </code>
     <code>
      query_int
     </code>
     →
     <code>
      boolean
     </code>
    </p>
    <p>
     A matriz satisfaz a consulta? (veja abaixo)
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      query_int
     </code>
     <code>
      ~~
     </code>
     <code>
      integer[]
     </code>
     →
     <code>
      boolean
     </code>
    </p>
    <p>
     A matriz satisfaz a consulta? (comutativo de
     <code>
      @@
     </code>
     )
    </p>
   </td>
  </tr>
 </tbody>
</table>










Os operadores `&&`, `@>` e `<@` são equivalentes aos operadores internos do PostgreSQL com os mesmos nomes, exceto que eles funcionam apenas em matrizes inteiras que não contêm nulos, enquanto os operadores internos funcionam para qualquer tipo de matriz. Essa restrição os torna mais rápidos que os operadores internos em muitos casos.

Os operadores `@@` e `~~` testam se uma matriz satisfaz uma *consulta*, que é expressa como um valor de um tipo de dados especializado `query_int`. Uma *consulta* consiste em valores inteiros que são verificados contra os elementos da matriz, possivelmente combinados usando os operadores `&` (E), `|` (OU) e `!` (NÃO). Fechetes podem ser usados conforme necessário. Por exemplo, a consulta `1&(2|3)` corresponde a matrizes que contêm 1 e também contêm 2 ou 3.

### F.19.2. Suporte ao índice [#](#INTARRAY-INDEX)

O `intarray` oferece suporte a índices para os operadores `&&`, `@>` e `@@`, além da igualdade regular de arrays.

São fornecidas duas classes de operadores de índice GiST parametrizadas: `gist__int_ops` (usada por padrão) é adequada para conjuntos de dados de pequeno a médio porte, enquanto `gist__intbig_ops` utiliza uma assinatura maior e é mais adequada para indexação de grandes conjuntos de dados (ou seja, colunas que contêm um grande número de valores distintos em matriz). A implementação utiliza uma estrutura de dados RD-tree com compressão perda embutida.

`gist__int_ops` aproxima um conjunto de inteiros como um array de intervalos de inteiros. Seu parâmetro opcional inteiro `numranges` determina o número máximo de intervalos em uma chave de índice. O valor padrão de `numranges` é 100. Os valores válidos estão entre 1 e 253. O uso de arrays maiores como chaves de índice GiST leva a uma pesquisa mais precisa (digitalizando uma fração menor do índice e menos páginas de heap), ao custo de um índice maior.

`gist__intbig_ops` aproxima um conjunto de inteiros como uma assinatura em formato de bitmap. Seu parâmetro opcional inteiro `siglen` determina o comprimento da assinatura em bytes. O comprimento padrão da assinatura é de 16 bytes. Os valores válidos do comprimento da assinatura estão entre 1 e 2024 bytes. assinaturas mais longas levam a uma busca mais precisa (digitalizando uma fração menor do índice e menos páginas de heap), ao custo de um índice maior.

Existe também uma classe de operador GIN não padrão `gin__int_ops`, que suporta esses operadores, assim como `<@`.

A escolha entre a indexação GiST e GIN depende das características de desempenho relativas de GiST e GIN, que são discutidas em outros lugares.

### F.19.3. Exemplo [#](#INTARRAY-EXAMPLE)

```
-- a message can be in one or more “sections”
CREATE TABLE message (mid INT PRIMARY KEY, sections INT[], ...);

-- create specialized index with signature length of 32 bytes
CREATE INDEX message_rdtree_idx ON message USING GIST (sections gist__intbig_ops (siglen = 32));

-- select messages in section 1 OR 2 - OVERLAP operator
SELECT message.mid FROM message WHERE message.sections && '{1,2}';

-- select messages in sections 1 AND 2 - CONTAINS operator
SELECT message.mid FROM message WHERE message.sections @> '{1,2}';

-- the same, using QUERY operator
SELECT message.mid FROM message WHERE message.sections @@ '1&2'::query_int;
```

### F.19.4. Benchmark [#](#INTARRAY-BENCHMARK)

O diretório de origem `contrib/intarray/bench` contém um conjunto de testes de referência, que pode ser executado contra um servidor PostgreSQL instalado. (Também é necessário instalar `DBD::Pg`. Para executar:

```
cd .../contrib/intarray/bench
createdb TEST
psql -c "CREATE EXTENSION intarray" TEST
./create_test.pl | psql TEST
./bench.pl
```

O script `bench.pl` tem várias opções, que são exibidas quando é executado sem quaisquer argumentos.

### F.19.5. Autores [#](#INTARRAY-AUTHORS)

Todo o trabalho foi feito por Teodor Sigaev (`<teodor@sigaev.ru>`) e Oleg Bartunov (`<oleg@sai.msu.su>`). Consulte
<http://www.sai.msu.su/~megera/postgres/gist/> para informações adicionais. Andrey Oktyabrski fez um ótimo trabalho ao adicionar novas funções e operações.