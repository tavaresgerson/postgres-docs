## 52.11. `pg_class` [#](#CATALOG-PG-CLASS)

O catálogo `pg_class` descreve tabelas e outros objetos que possuem colunas ou são de outra forma semelhantes a uma tabela. Isso inclui índices (mas veja também [`pg_index`](catalog-pg-index.md "52.26. pg_index")), sequências (mas veja também [`pg_sequence`](catalog-pg-sequence.md "52.47. pg_sequence")), visualizações, visualizações materializadas, tipos compostos e tabelas TOAST; veja `relkind`. Abaixo, quando nos referimos a todos esses tipos de objetos, falamos de “relações”. Nem todas as colunas do `pg_class` são significativas para todos os tipos de relação.

**Tabela 52.11. Colunas `pg_class`**



<table border="1" class="table" summary="pg_class Columns">
 <colgroup>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th class="catalog_table_entry">
    <p class="column_definition">
     Tipo de coluna
    </p>
    <p>
     Descrição
    </p>
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      oid
     </code>
     <code class="type">
      oid
     </code>
    </p>
    <p>
     Identificador da linha
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      relname
     </code>
     <code class="type">
      name
     </code>
    </p>
    <p>
     Nome da tabela, índice, visualização, etc.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      relnamespace
     </code>
     <code class="type">
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-namespace.md" title="52.32. pg_namespace">
      <code class="structname">
       pg_namespace
      </code>
     </a>
     .
     <code class="structfield">
      oid
     </code>
     )
    </p>
    <p>
     O OID do espaço de nomes que contém essa relação
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      reltype
     </code>
     <code class="type">
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-type.md" title="52.64. pg_type">
      <code class="structname">
       pg_type
      </code>
     </a>
     .
     <code class="structfield">
      oid
     </code>
     )
    </p>
    <p>
     O OID do tipo de dados que corresponde ao tipo de linha desta tabela, se houver; zero para índices, sequências e tabelas de toast, que não têm
     <code class="structname">
      pg_type
     </code>
     entrada
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      reloftype
     </code>
     <code class="type">
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-type.md" title="52.64. pg_type">
      <code class="structname">
       pg_type
      </code>
     </a>
     .
     <code class="structfield">
      oid
     </code>
     )
    </p>
    <p>
     Para tabelas digitadas, o OID do tipo composto subjacente; zero para todas as outras relações
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      relowner
     </code>
     <code class="type">
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-authid.md" title="52.8. pg_authid">
      <code class="structname">
       pg_authid
      </code>
     </a>
     .
     <code class="structfield">
      oid
     </code>
     )
    </p>
    <p>
     Proprietário da relação
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      relam
     </code>
     <code class="type">
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-am.md" title="52.3. pg_am">
      <code class="structname">
       pg_am
      </code>
     </a>
     .
     <code class="structfield">
      oid
     </code>
     )
    </p>
    <p>
     O método de acesso usado para acessar esta tabela ou índice. Não é significativo se a relação for uma sequência ou não tiver um arquivo no disco, exceto para tabelas particionadas, onde, se definido, ele tem precedência sobre
     <code class="varname">
      default_table_access_method
     </code>
     ao determinar o método de acesso a ser utilizado para partições criadas quando não é especificado no comando de criação.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      relfilenode
     </code>
     <code class="type">
      oid
     </code>
    </p>
    <p>
     Nome do arquivo em disco desta relação; zero significa que esta é uma
     <span class="quote">
      “
      <span class="quote">
       mapeado
      </span>
      ”
     </span>
     relação cujo nome do arquivo de disco é determinado pelo estado de baixo nível
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      reltablespace
     </code>
     <code class="type">
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-tablespace.md" title="52.56. pg_tablespace">
      <code class="structname">
       pg_tablespace
      </code>
     </a>
     .
     <code class="structfield">
      oid
     </code>
     )
    </p>
    <p>
     O tablespace no qual essa relação é armazenada. Se zero, o tablespace padrão do banco de dados é implícito. Não é significativo se a relação não tiver um arquivo no disco, exceto para tabelas particionadas, onde este é o tablespace no qual as partições serão criadas quando não for especificado no comando de criação.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      relpages
     </code>
     <code class="type">
      int4
     </code>
    </p>
    <p>
     Tamanho da representação em disco desta tabela em páginas (do tamanho de
     <code class="symbol">
      BLCKSZ
     </code>
     ). Esse é apenas uma estimativa usada pelo planejador. Ela é atualizada por
     <a class="link" href="sql-vacuum.md" title="VACUUM">
      <code class="command">
       VACUUM
      </code>
     </a>
     ,
     <a class="link" href="sql-analyze.md" title="ANALYZE">
      <code class="command">
       ANALYZE
      </code>
     </a>
     , e alguns comandos DDL, como
     <a class="link" href="sql-createindex.md" title="CREATE INDEX">
      <code class="command">
       CREATE INDEX
      </code>
     </a>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      reltuples
     </code>
     <code class="type">
      float4
     </code>
    </p>
    <p>
     Número de linhas vivas na tabela. Isso é apenas uma estimativa usada pelo planejador. É atualizado por
     <a class="link" href="sql-vacuum.md" title="VACUUM">
      <code class="command">
       VACUUM
      </code>
     </a>
     ,
     <a class="link" href="sql-analyze.md" title="ANALYZE">
      <code class="command">
       ANALYZE
      </code>
     </a>
     , e alguns comandos DDL, como
     <a class="link" href="sql-createindex.md" title="CREATE INDEX">
      <code class="command">
       CREATE INDEX
      </code>
     </a>
     Se a tabela ainda não tiver sido aspirada ou analisada,
     <code class="structfield">
      reltuples
     </code>
     contem
     <code class="literal">
      -1
     </code>
     indicando que o número de linhas é desconhecido.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      relallvisible
     </code>
     <code class="type">
      int4
     </code>
    </p>
    <p>
     Número de páginas marcadas como totalmente visíveis no mapa de visibilidade da tabela. Esse é apenas uma estimativa usada pelo planejador. É atualizado por
     <a class="link" href="sql-vacuum.md" title="VACUUM">
      <code class="command">
       VACUUM
      </code>
     </a>
     ,
     <a class="link" href="sql-analyze.md" title="ANALYZE">
      <code class="command">
       ANALYZE
      </code>
     </a>
     , e alguns comandos DDL, como
     <a class="link" href="sql-createindex.md" title="CREATE INDEX">
      <code class="command">
       CREATE INDEX
      </code>
     </a>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      relallfrozen
     </code>
     <code class="type">
      int4
     </code>
    </p>
    <p>
     Número de páginas marcadas como totalmente congeladas no mapa de visibilidade da tabela. Esse é apenas uma estimativa usada para acionar autovacuos. Também pode ser usado juntamente com
     <code class="structfield">
      relallvisible
     </code>
     para agendamento de aspiradores manuais e ajuste
     <a class="link" href="runtime-config-vacuum.md#RUNTIME-CONFIG-VACUUM-FREEZING" title="19.10.4. Freezing">
      comportamento de congelamento do vácuo
     </a>
     . É atualizado por
     <a class="link" href="sql-vacuum.md" title="VACUUM">
      <code class="command">
       VACUUM
      </code>
     </a>
     ,
     <a class="link" href="sql-analyze.md" title="ANALYZE">
      <code class="command">
       ANALYZE
      </code>
     </a>
     , e alguns comandos DDL, como
     <a class="link" href="sql-createindex.md" title="CREATE INDEX">
      <code class="command">
       CREATE INDEX
      </code>
     </a>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      reltoastrelid
     </code>
     <code class="type">
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-class.md" title="52.11. pg_class">
      <code class="structname">
       pg_class
      </code>
     </a>
     .
     <code class="structfield">
      oid
     </code>
     )
    </p>
    <p>
     OID da tabela TOAST associada a esta tabela, zero se nenhuma. A tabela TOAST armazena atributos grandes
     <span class="quote">
      “
      <span class="quote">
       fora de linha
      </span>
      ”
     </span>
     em uma tabela secundária.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      relhasindex
     </code>
     <code class="type">
      bool
     </code>
    </p>
    <p>
     Verdadeiro se esta é uma tabela e ela tem (ou teve recentemente) algum índice
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      relisshared
     </code>
     <code class="type">
      bool
     </code>
    </p>
    <p>
     Verdadeiro se esta tabela for compartilhada em todos os bancos de dados do clúster. Apenas certos catálogos do sistema (como
     <a class="link" href="catalog-pg-database.md" title="52.15. pg_database">
      <code class="structname">
       pg_database
      </code>
     </a>
     ) são compartilhadas.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      relpersistence
     </code>
     <code class="type">
      char
     </code>
    </p>
    <p>
     <code class="literal">
      p
     </code>
     = tabela/sequência permanente
     <code class="literal">
      u
     </code>
     = tabela/sequência não registrada,
     <code class="literal">
      t
     </code>
     = tabela/sequência temporária
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      relkind
     </code>
     <code class="type">
      char
     </code>
    </p>
    <p>
     <code class="literal">
      r
     </code>
     = mesa comum,
     <code class="literal">
      i
     </code>
     = índice,
     <code class="literal">
      S
     </code>
     = sequência,
     <code class="literal">
      t
     </code>
     mesa TOAST
     <code class="literal">
      v
     </code>
     = visualizar,
     <code class="literal">
      m
     </code>
     = visão materializada,
     <code class="literal">
      c
     </code>
     = tipo composto,
     <code class="literal">
      f
     </code>
     = mesa estrangeira,
     <code class="literal">
      p
     </code>
     = tabela dividida
     <code class="literal">
      I
     </code>
     = índice particionado
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      relnatts
     </code>
     <code class="type">
      int2
     </code>
    </p>
    <p>
     Número de colunas de usuário na relação (colunas do sistema não contadas). Deve haver tantas entradas correspondentes quanto o número de colunas de usuário na relação.
     <a class="link" href="catalog-pg-attribute.md" title="52.7. pg_attribute">
      <code class="structname">
       pg_attribute
      </code>
     </a>
     Veja também
     <code class="structname">
      pg_attribute
     </code>
     .
     <code class="structfield">
      attnum
     </code>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      relchecks
     </code>
     <code class="type">
      int2
     </code>
    </p>
    <p>
     Número de
     <code class="literal">
      CHECK
     </code>
     restrições na tabela; veja
     <a class="link" href="catalog-pg-constraint.md" title="52.13. pg_constraint">
      <code class="structname">
       pg_constraint
      </code>
     </a>
     catálogo
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      relhasrules
     </code>
     <code class="type">
      bool
     </code>
    </p>
    <p>
     Verdadeiro se a tabela tem (ou teve) regras; veja
     <a class="link" href="catalog-pg-rewrite.md" title="52.45. pg_rewrite">
      <code class="structname">
       pg_rewrite
      </code>
     </a>
     catálogo
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      relhastriggers
     </code>
     <code class="type">
      bool
     </code>
    </p>
    <p>
     Verdadeiro se a tabela tiver (ou tiver tido) gatilhos; veja
     <a class="link" href="catalog-pg-trigger.md" title="52.58. pg_trigger">
      <code class="structname">
       pg_trigger
      </code>
     </a>
     catálogo
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      relhassubclass
     </code>
     <code class="type">
      bool
     </code>
    </p>
    <p>
     Verdadeiro se a tabela ou o índice tiver (ou tiver tido) qualquer filho ou partição de herança
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      relrowsecurity
     </code>
     <code class="type">
      bool
     </code>
    </p>
    <p>
     Verdadeiro se a tabela tiver segurança de nível de linha habilitada; veja
     <a class="link" href="catalog-pg-policy.md" title="52.38. pg_policy">
      <code class="structname">
       pg_policy
      </code>
     </a>
     catálogo
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      relforcerowsecurity
     </code>
     <code class="type">
      bool
     </code>
    </p>
    <p>
     Verdadeiro se a segurança de nível de linha (quando habilitada) também se aplicará ao proprietário da tabela; veja
     <a class="link" href="catalog-pg-policy.md" title="52.38. pg_policy">
      <code class="structname">
       pg_policy
      </code>
     </a>
     catálogo
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      relispopulated
     </code>
     <code class="type">
      bool
     </code>
    </p>
    <p>
     Verdadeiro se a relação estiver preenchida (isso é verdadeiro para todas as relações, exceto algumas visualizações materializadas)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      relreplident
     </code>
     <code class="type">
      char
     </code>
    </p>
    <p>
     Colunas utilizadas para formar
     <span class="quote">
      “
      <span class="quote">
       identidade replicada
      </span>
      ”
     </span>
     para linhas:
     <code class="literal">
      d
     </code>
     = padrão (chave primária, se houver),
     <code class="literal">
      n
     </code>
     = nada,
     <code class="literal">
      f
     </code>
     = todas as colunas,
     <code class="literal">
      i
     </code>
     = índice com
     <code class="structfield">
      indisreplident
     </code>
     set (mesmo que nada se o índice usado tenha sido descartado)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      relispartition
     </code>
     <code class="type">
      bool
     </code>
    </p>
    <p>
     Verdadeiro se a tabela ou o índice é uma partição
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      relrewrite
     </code>
     <code class="type">
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-class.md" title="52.11. pg_class">
      <code class="structname">
       pg_class
      </code>
     </a>
     .
     <code class="structfield">
      oid
     </code>
     )
    </p>
    <p>
     Para novas relações que são escritas durante uma operação de DDL que requer uma reescrita de uma tabela, este contém o OID da relação original; caso contrário, zero. Esse estado é visível apenas internamente; este campo nunca deve conter nada além de zero para uma relação visível pelo usuário.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      relfrozenxid
     </code>
     <code class="type">
      xid
     </code>
    </p>
    <p>
     Todos os IDs de transação antes deste foram substituídos por um permanente (
     <span class="quote">
      “
      <span class="quote">
       congelado
      </span>
      ”
     </span>
     ) ID de transação nesta tabela. Isso é usado para rastrear se a tabela precisa ser limpa para evitar o enrolamento do ID de transação ou para permitir
     <code class="literal">
      pg_xact
     </code>
     para ser reduzido. Zero (
     <code class="symbol">
      InvalidTransactionId
     </code>
     ) se a relação não for uma tabela.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      relminmxid
     </code>
     <code class="type">
      xid
     </code>
    </p>
    <p>
     Todos os IDs multixact anteriores a este foram substituídos por um ID de transação nesta tabela. Isso é usado para rastrear se a tabela precisa ser limpa para evitar o envolvimento de IDs multixact ou para permitir
     <code class="literal">
      pg_multixact
     </code>
     para ser reduzido. Zero (
     <code class="symbol">
      InvalidMultiXactId
     </code>
     ) se a relação não for uma tabela.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      relacl
     </code>
     <code class="type">
      aclitem[]
     </code>
    </p>
    <p>
     Privilegios de acesso; veja
     <a class="xref" href="ddl-priv.md" title="5.8. Privileges">
      Seção 5.8
     </a>
     para detalhes
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      reloptions
     </code>
     <code class="type">
      text[]
     </code>
    </p>
    <p>
     Opções específicas para métodos de acesso, como
     <span class="quote">
      “
      <span class="quote">
       palavra-chave=valor
      </span>
      ”
     </span>
     cordas
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      relpartbound
     </code>
     <code class="type">
      pg_node_tree
     </code>
    </p>
    <p>
     Se a tabela for uma partição (consulte
     <code class="structfield">
      relispartition
     </code>
     ), representação interna do limite da partição
    </p>
   </td>
  </tr>
 </tbody>
</table>










Vários dos indicadores lógicos em `pg_class` são mantidos preguiçosamente: eles são garantidos como verdadeiros se esse for o estado correto, mas podem não ser redefinidos como falsos imediatamente quando a condição não é mais verdadeira. Por exemplo, `relhasindex` é definido por [`CREATE INDEX`](sql-createindex.md "CREATE INDEX"), mas nunca é limpo por [`DROP INDEX`](sql-dropindex.md "DROP INDEX"). Em vez disso, [`VACUUM`](sql-vacuum.md "VACUUM") limpa `relhasindex` se encontrar que a tabela não tem índices. Esse arranjo evita condições de corrida e melhora a concorrência.