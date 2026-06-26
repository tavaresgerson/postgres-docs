## Apêndice K. Limites do PostgreSQL

[Tabela K.1](limits.md#LIMITS-TABLE) descreve vários limites rígidos do PostgreSQL. No entanto, limites práticos, como limitações de desempenho ou espaço em disco disponível, podem ser aplicados antes que os limites rígidos absolutos sejam alcançados.

**Tabela K.1. Limitações do PostgreSQL**



<table>
 <colgroup>
  <col/>
  <col/>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th>
    Item
   </th>
   <th>
    Upper Limit
   </th>
   <th>
    Comentário
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    tamanho do banco de dados
   </td>
   <td>
    unlimited
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>
    número de bancos de dados
   </td>
   <td>
    4,294,950,911
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>
    relações por banco de dados
   </td>
   <td>
    1,431,650,303
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>
    tamanho da relação
   </td>
   <td>
    32 TB
   </td>
   <td>
    com o padrão
    <code>
     BLCKSZ
    </code>
    de 8192 bytes
   </td>
  </tr>
  <tr>
   <td>
    linhas por tabela
   </td>
   <td>
    limited by the number of tuples that can fit onto 4,294,967,295 pages
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>
    colunas por tabela
   </td>
   <td>
    1,600
   </td>
   <td>
    mais limitada pela adequação do tamanho do tuple em uma única página; veja a nota abaixo
   </td>
  </tr>
  <tr>
   <td>
    colunas em um conjunto de resultados
   </td>
   <td>
    1,664
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>
    tamanho do campo
   </td>
   <td>
    1 GB
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>
    índice por tabela
   </td>
   <td>
    unlimited
   </td>
   <td>
    limitado por relações máximas por banco de dados
   </td>
  </tr>
  <tr>
   <td>
    colunas por índice
   </td>
   <td>
    32
   </td>
   <td>
    pode ser aumentada recompilando
    <span class="productname">
     PostgreSQL
    </span>
   </td>
  </tr>
  <tr>
   <td>
    chaves de partição
   </td>
   <td>
    32
   </td>
   <td>
    pode ser aumentada recompilando
    <span class="productname">
     PostgreSQL
    </span>
   </td>
  </tr>
  <tr>
   <td>
    comprimento do identificador
   </td>
   <td>
    63 bytes
   </td>
   <td>
    pode ser aumentada recompilando
    <span class="productname">
     PostgreSQL
    </span>
   </td>
  </tr>
  <tr>
   <td>
    argumentos de função
   </td>
   <td>
    100
   </td>
   <td>
    pode ser aumentada recompilando
    <span class="productname">
     PostgreSQL
    </span>
   </td>
  </tr>
  <tr>
   <td>
    parâmetros de consulta
   </td>
   <td>
    65,535
   </td>
   <td>
   </td>
  </tr>
 </tbody>
</table>










O número máximo de colunas para uma tabela é reduzido ainda mais, pois o tuplo que está sendo armazenado deve caber em uma única página de heap de 8192 bytes. Por exemplo, excluindo o cabeçalho do tuplo, um tuplo composto por 1.600 colunas `int` consumiria 6400 bytes e poderia ser armazenado em uma página de heap, mas um tuplo de 1.600 colunas `bigint` consumiria 12800 bytes e, portanto, não caberia dentro de uma página de heap. Campos de comprimento variável de tipos como `text`, `varchar` e `char` podem ter seus valores armazenados fora da linha na tabela TOAST quando os valores forem grandes o suficiente para exigir isso. Apenas um ponteiro de 18 bytes deve permanecer dentro do tuplo na heap da tabela. Para campos de comprimento variável de menor comprimento, ou seja, um cabeçalho de campo de 4 bytes ou 1 byte é usado e o valor é armazenado dentro do tuplo de heap.

As colunas que foram excluídas da tabela também contribuem para o limite máximo de colunas. Além disso, embora os valores das colunas excluídas para tuplas recém-criadas sejam marcados internamente como nulos na bitmap de nulidade da tupla, a bitmap de nulidade também ocupa espaço.

Cada tabela pode armazenar um máximo teórico de 2^32 valores fora da linha; consulte [Seção 66.2](storage-toast.md) para uma discussão detalhada sobre o armazenamento fora da linha. Esse limite decorre do uso de um OID de 32 bits para identificar cada valor desse tipo. O limite prático é significativamente menor que o limite teórico, porque, à medida que o espaço do OID se enche, encontrar um OID que ainda esteja disponível pode se tornar caro, o que, por sua vez, desacelera as declarações INSERT/UPDATE. Normalmente, esse é apenas um problema para tabelas que contêm muitos terabytes de dados; a partição é uma solução possível.