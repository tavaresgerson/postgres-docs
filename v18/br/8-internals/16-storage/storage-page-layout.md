## 66.6. Layout da página do banco de dados [#](#STORAGE-PAGE-LAYOUT)

* [66.6.1. Layout de linha de tabela](storage-page-layout.md#STORAGE-TUPLE-LAYOUT)

Esta seção fornece uma visão geral do formato da página usado nas tabelas e índices do PostgreSQL. [[19]] (#ftn.id-1.10.18.8.2.2) Sequências e tabelas TOAST são formatadas da mesma forma que uma tabela regular.

Na explicação a seguir, um *byte* é assumido que contém 8 bits. Além disso, o termo *item* se refere a um valor de dados individual que é armazenado em uma página. Em uma tabela, um item é uma linha; em um índice, um item é uma entrada de índice.

Cada tabela e índice são armazenados como um array de *páginas* de tamanho fixo (geralmente 8 kB, embora um tamanho de página diferente possa ser selecionado ao compilar o servidor). Em uma tabela, todas as páginas são logicamente equivalentes, então um item particular (linha) pode ser armazenado em qualquer página. Em índices, a primeira página é geralmente reservada como uma *metapágina* que contém informações de controle, e pode haver diferentes tipos de páginas dentro do índice, dependendo do método de acesso ao índice.

[Tabela 66.2](storage-page-layout.md#PAGE-TABLE) mostra o layout geral de uma página. Há cinco partes em cada página.

**Tabela 66.2. Layout geral da página**



<table border="1" class="table" summary="Overall Page Layout">
 <colgroup>
  <col/>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th>
    Item
   </th>
   <th>
    Descrição
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    PageHeaderData
   </td>
   <td>
    Com 24 bytes de comprimento. Contém informações gerais sobre a página, incluindo ponteiros de espaço livre.
   </td>
  </tr>
  <tr>
   <td>
    ItemIdData
   </td>
   <td>
    Matriz de identificadores de itens que apontam para os itens reais. Cada entrada é um par (deslocamento, comprimento). 4 bytes por item.
   </td>
  </tr>
  <tr>
   <td>
    Free space
   </td>
   <td>
    O espaço não alocado. Novos identificadores de itens são alocados a partir do início desta área, novos itens a partir do final.
   </td>
  </tr>
  <tr>
   <td>
    Items
   </td>
   <td>
    Os próprios itens.
   </td>
  </tr>
  <tr>
   <td>
    Special space
   </td>
   <td>
    Dados específicos do método de acesso ao índice. Diferentes métodos armazenam dados diferentes. Vazio em tabelas comuns.
   </td>
  </tr>
 </tbody>
</table>










Os primeiros 24 bytes de cada página consistem em um cabeçalho de página (`PageHeaderData`). Seu formato é detalhado em [Tabela 66.3](storage-page-layout.md#PAGEHEADERDATA-TABLE "Table 66.3. PageHeaderData Layout"). O primeiro campo acompanha a entrada mais recente do WAL relacionada a esta página. O segundo campo contém o checksum da página se [[`-k`](app-initdb.md#APP-INITDB-DATA-CHECKSUMS)]] estiverem habilitados. A seguir, há um campo de 2 bytes contendo bits de sinalização. Isso é seguido por três campos inteiros de 2 bytes (`pd_lower`, `pd_upper` e `pd_special`). Esses campos contêm offsets de byte do início da página até o início do espaço não alocado, até o fim do espaço não alocado e até o início do espaço especial. Os próximos 2 bytes do cabeçalho de página, `pd_pagesize_version`, armazenam tanto o tamanho da página quanto um indicador de versão. A partir do PostgreSQL 8.3, o número de versão é 4; o PostgreSQL 8.1 e 8.2 utilizaram o número de versão 3; o PostgreSQL 8.0 utilizou o número de versão 2; o PostgreSQL 7.3 e 7.4 utilizaram o número de versão 1; versões anteriores utilizaram o número de versão 0. (O layout básico da página e o formato do cabeçalho não mudaram na maioria dessas versões, mas o layout dos cabeçalhos de linha do heap.) O tamanho da página basicamente só está presente como um cruzamento; não há suporte para ter mais de um tamanho de página em uma instalação. O último campo é um aviso que mostra se a poda da página é provável que seja lucrativa: ele acompanha o XMAX não podado mais antigo na página.

**Tabela 66.3. Layout de PageHeaderData**



<table border="1" class="table" summary="PageHeaderData Layout">
 <colgroup>
  <col/>
  <col/>
  <col/>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th>
    Field
   </th>
   <th>
    Type
   </th>
   <th>
    Length
   </th>
   <th>
    Descrição
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    pd_lsn
   </td>
   <td>
    PageXLogRecPtr
   </td>
   <td>
    8 bytes
   </td>
   <td>
    LSN: próximo byte após o último byte do registro WAL para a última alteração
   </td>
  </tr>
  <tr>
   <td>
    pd_checksum
   </td>
   <td>
    uint16
   </td>
   <td>
    2 bytes
   </td>
   <td>
    Checksum da página
   </td>
  </tr>
  <tr>
   <td>
    pd_flags
   </td>
   <td>
    uint16
   </td>
   <td>
    2 bytes
   </td>
   <td>
    Bits de bandeira
   </td>
  </tr>
  <tr>
   <td>
    pd_lower
   </td>
   <td>
    LocationIndex
   </td>
   <td>
    2 bytes
   </td>
   <td>
    Deslocamento para o início do espaço livre
   </td>
  </tr>
  <tr>
   <td>
    pd_upper
   </td>
   <td>
    LocationIndex
   </td>
   <td>
    2 bytes
   </td>
   <td>
    Deslocamento até o fim do espaço livre
   </td>
  </tr>
  <tr>
   <td>
    pd_special
   </td>
   <td>
    LocationIndex
   </td>
   <td>
    2 bytes
   </td>
   <td>
    Deslocamento para o início do espaço especial
   </td>
  </tr>
  <tr>
   <td>
    pd_pagesize_version
   </td>
   <td>
    uint16
   </td>
   <td>
    2 bytes
   </td>
   <td>
    Tamanho da página e informações sobre o número da versão do layout
   </td>
  </tr>
  <tr>
   <td>
    pd_prune_xid
   </td>
   <td>
    TransactionId
   </td>
   <td>
    4 bytes
   </td>
   <td>
    Mais antigo XMAX não podado na página, ou zero se nenhum
   </td>
  </tr>
 </tbody>
</table>










Todos os detalhes podem ser encontrados em `src/include/storage/bufpage.h`.

Após o cabeçalho da página estão os identificadores de itens (`ItemIdData`), cada um dos quais requer quatro bytes. Um identificador de item contém um deslocamento de byte para o início de um item, sua extensão em bytes e alguns bits de atributo que afetam sua interpretação. Novos identificadores de itens são alocados conforme necessário, a partir do início do espaço não alocado. O número de identificadores de itens presentes pode ser determinado observando `pd_lower`, que é aumentado para alocar um novo identificador. Como um identificador de item nunca é movido até que seja liberado, seu índice pode ser usado de forma a longo prazo para referenciar um item, mesmo quando o próprio item é movido pela página para compactar o espaço livre. De fato, todo o ponteiro para um item (`ItemPointer`, também conhecido como `CTID`) criado pelo PostgreSQL consiste em um número de página e o índice de um identificador de item.

Os próprios itens são armazenados no espaço alocado em ordem inversa do final do espaço não alocado. A estrutura exata varia dependendo do que a tabela deve conter. Tabelas e sequências utilizam uma estrutura denominada `HeapTupleHeaderData`, descrita abaixo.

A seção final é a “seção especial”, que pode conter qualquer coisa que o método de acesso queira armazenar. Por exemplo, os índices de árvore b armazenam links para os irmãos à esquerda e à direita da página, bem como alguns outros dados relevantes para a estrutura do índice. As tabelas comuns não usam uma seção especial (indicada definindo `pd_special` igual ao tamanho da página).

[Figura 66.1] (storage-page-layout.md#STORAGE-PAGE-LAYOUT-FIGURE "Figure 66.1. Page Layout") ilustra como essas partes são dispostas em uma página.

**Figura 66.1. Layout da página**



### 66.6.1. Layout de linha de tabela [#](#STORAGE-TUPLE-LAYOUT)

Todas as linhas da tabela são estruturadas da mesma maneira. Há um cabeçalho de tamanho fixo (ocupando 23 bytes na maioria das máquinas), seguido por um bitmap opcional, um campo de ID de objeto opcional e os dados do usuário. O cabeçalho é detalhado em [Tabela 66.4](storage-page-layout.md#HEAPTUPLEHEADERDATA-TABLE). Os dados reais do usuário (colunas da linha) começam no deslocamento indicado por `t_hoff`, que deve ser sempre um múltiplo da distância MAXALIGN para a plataforma. O bitmap nulo só está presente se o bit *HEAP_HASNULL* estiver definido em `t_infomask`. Se estiver presente, ele começa logo após o cabeçalho fixo e ocupa bytes suficientes para ter um bit por coluna de dados (ou seja, o número de bits que equivale ao número de atributos em `t_infomask2`). Nesta lista de bits, um bit 1 indica não nulo, um bit 0 é nulo. Quando o bitmap não está presente, todas as colunas são assumidas como não nulos. O ID de objeto só está presente se o bit *HEAP_HASOID_OLD* estiver definido em `t_infomask`. Se estiver presente, ele aparece logo antes da fronteira de `t_hoff`. Qualquer preenchimento necessário para fazer `t_hoff` um múltiplo de MAXALIGN aparecerá entre o bitmap nulo e o ID de objeto. (Isso, por sua vez, garante que o ID de objeto esteja adequadamente alinhado.)

**Tabela 66.4. Estrutura de dados HeapTupleHeaderData**



<table border="1" class="table" summary="HeapTupleHeaderData Layout">
 <colgroup>
  <col/>
  <col/>
  <col/>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th>
    Field
   </th>
   <th>
    Type
   </th>
   <th>
    Length
   </th>
   <th>
    Descrição
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    t_xmin
   </td>
   <td>
    TransactionId
   </td>
   <td>
    4 bytes
   </td>
   <td>
    inserir o selo XID
   </td>
  </tr>
  <tr>
   <td>
    t_xmax
   </td>
   <td>
    TransactionId
   </td>
   <td>
    4 bytes
   </td>
   <td>
    excluir o selo XID
   </td>
  </tr>
  <tr>
   <td>
    t_cid
   </td>
   <td>
    CommandId
   </td>
   <td>
    4 bytes
   </td>
   <td>
    inserir e/ou excluir o carimbo CID (sobreposição com t_xvac)
   </td>
  </tr>
  <tr>
   <td>
    t_xvac
   </td>
   <td>
    TransactionId
   </td>
   <td>
    4 bytes
   </td>
   <td>
    XID para operação VACUUM que move uma versão de linha
   </td>
  </tr>
  <tr>
   <td>
    t_ctid
   </td>
   <td>
    ItemPointerData
   </td>
   <td>
    6 bytes
   </td>
   <td>
    TID atual desta ou versão mais nova da linha
   </td>
  </tr>
  <tr>
   <td>
    t_infomask2
   </td>
   <td>
    uint16
   </td>
   <td>
    2 bytes
   </td>
   <td>
    número de atributos, além de vários bits de bandeira
   </td>
  </tr>
  <tr>
   <td>
    t_infomask
   </td>
   <td>
    uint16
   </td>
   <td>
    2 bytes
   </td>
   <td>
    variosos bits de bandeira
   </td>
  </tr>
  <tr>
   <td>
    t_hoff
   </td>
   <td>
    uint8
   </td>
   <td>
    1 byte
   </td>
   <td>
    deslocamento para dados do usuário
   </td>
  </tr>
 </tbody>
</table>










Todos os detalhes podem ser encontrados em `src/include/access/htup_details.h`.

Interpretar os dados reais só pode ser feito com informações obtidas de outras tabelas, principalmente `pg_attribute`. Os valores chave necessários para identificar os locais dos campos são `attlen` e `attalign`. Não é possível obter diretamente um atributo específico, exceto quando há apenas campos de largura fixa e sem valores nulos. Tudo isso é envolto nas funções *heap_getattr*, *fastgetattr* e *heap_getsysattr*.

Para ler os dados, você precisa examinar cada atributo por vez. Primeiro, verifique se o campo está NULL de acordo com a bitmap de nulidade. Se estiver, vá para o próximo. Em seguida, certifique-se de que você tem o alinhamento correto. Se o campo for um campo de largura fixa, então todos os bytes são simplesmente colocados. Se for um campo de comprimento variável (attlen = -1), então é um pouco mais complicado. Todos os tipos de dados de comprimento variável compartilham a estrutura de cabeçalho comum `struct varlena`, que inclui o comprimento total do valor armazenado e alguns bits de sinal. Dependendo das bandeiras, os dados podem ser inline ou em uma tabela TOAST; também pode ser comprimido (consulte [Seção 66.2] (storage-toast.md "66.2. TOAST")).

---

[[19]](#id-1.10.18.8.2.2) De fato, o uso desse formato de página não é necessário para métodos de acesso a tabelas ou índices. O método de acesso à tabela `heap` sempre usa esse formato. Todos os métodos de índice existentes também usam o formato básico, mas os dados mantidos nas metapáginas do índice geralmente não seguem as regras de layout do item.