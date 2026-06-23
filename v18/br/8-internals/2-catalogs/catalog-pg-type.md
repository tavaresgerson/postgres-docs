## 52.64. `pg_type` [#](#CATALOG-PG-TYPE)

O catálogo `pg_type` armazena informações sobre os tipos de dados. Os tipos básicos e os tipos enum (tipos escalares) são criados com [`CREATE TYPE`](sql-createtype.md "CREATE TYPE"), e os domínios com [`CREATE DOMAIN`](sql-createdomain.md "CREATE DOMAIN"). Um tipo composto é criado automaticamente para cada tabela no banco de dados, para representar a estrutura da linha da tabela. Também é possível criar tipos compostos com `CREATE TYPE AS`.

**Tabela 52.64. Colunas `pg_type`**



<table border="1" class="table" summary="pg_type Columns">
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
      typname
     </code>
     <code class="type">
      name
     </code>
    </p>
    <p>
     Nome do tipo de dados
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      typnamespace
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
     O OID do espaço de nomes que contém este tipo
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      typowner
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
     Proprietário do tipo
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      typlen
     </code>
     <code class="type">
      int2
     </code>
    </p>
    <p>
     Para um tipo de tamanho fixo,
     <code class="structfield">
      typlen
     </code>
     é o número de bytes na representação interna do tipo. Mas, para um tipo de comprimento variável,
     <code class="structfield">
      typlen
     </code>
     é negativa. -1 indica uma
     <span class="quote">
      “
      <span class="quote">
       varlena
      </span>
      ”
     </span>
     tipo (um que tem uma palavra de comprimento), -2 indica uma cadeia de caracteres C terminada por nulo.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      typbyval
     </code>
     <code class="type">
      bool
     </code>
    </p>
    <p>
     <code class="structfield">
      typbyval
     </code>
     determina se as rotinas internas passam um valor desse tipo por valor ou por referência.
     <code class="structfield">
      typbyval
     </code>
     teria que ser falsa se
     <code class="structfield">
      typlen
     </code>
     não é 1, 2 ou 4 (ou 8 em máquinas onde o Datum é de 8 bytes). Os tipos de comprimento variável são sempre passados por referência. Note que
     <code class="structfield">
      typbyval
     </code>
     pode ser falsa mesmo que a comprimento permita a passagem por valor.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      typtype
     </code>
     <code class="type">
      char
     </code>
    </p>
    <p>
     <code class="structfield">
      typtype
     </code>
     é
     <code class="literal">
      b
     </code>
     para um tipo de base,
     <code class="literal">
      c
     </code>
     para um tipo composto (por exemplo, o tipo de linha de uma tabela),
     <code class="literal">
      d
     </code>
     para um domínio,
     <code class="literal">
      e
     </code>
     para um tipo de enum,
     <code class="literal">
      p
     </code>
     para um pseudo-tipo,
     <code class="literal">
      r
     </code>
     para um tipo de gama, ou
     <code class="literal">
      m
     </code>
     para um tipo multiranged.
     <code class="structfield">
      typrelid
     </code>
     e
     <code class="structfield">
      typbasetype
     </code>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      typcategory
     </code>
     <code class="type">
      char
     </code>
    </p>
    <p>
     <code class="structfield">
      typcategory
     </code>
     é uma classificação arbitrária de tipos de dados que é usada pelo analisador para determinar quais casts implícitos devem ser
     <span class="quote">
      “
      <span class="quote">
       preferido
      </span>
      ”
     </span>
     Veja
     <a class="xref" href="catalog-pg-type.md#CATALOG-TYPCATEGORY-TABLE" title="Table 52.65. typcategory Codes">
      Tabela 52.65
     </a>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      typispreferred
     </code>
     <code class="type">
      bool
     </code>
    </p>
    <p>
     Verdadeiro se o tipo é um alvo de cast preferido dentro de seu
     <code class="structfield">
      typcategory
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      typisdefined
     </code>
     <code class="type">
      bool
     </code>
    </p>
    <p>
     Verdadeiro se o tipo estiver definido, falso se esta for uma entrada de marcador para um tipo ainda não definido. Quando
     <code class="structfield">
      typisdefined
     </code>
     É falso, nada, exceto o nome do tipo, o espaço de nomeação e o OID podem ser confiáveis.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      typdelim
     </code>
     <code class="type">
      char
     </code>
    </p>
    <p>
     Caractere que separa dois valores desse tipo ao analisar a entrada de matriz. Observe que o delimitador está associado ao tipo de dados do elemento da matriz, não ao tipo de dados da matriz.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      typrelid
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
     Se este for um tipo composto (veja
     <code class="structfield">
      typtype
     </code>
     ), então esta coluna aponta para
     <a class="link" href="catalog-pg-class.md" title="52.11. pg_class">
      <code class="structname">
       pg_class
      </code>
     </a>
     entrada que define a tabela correspondente. (Para um tipo de composto independente, o
     <a class="link" href="catalog-pg-class.md" title="52.11. pg_class">
      <code class="structname">
       pg_class
      </code>
     </a>
     A entrada não representa realmente uma tabela, mas é necessária de qualquer forma para o tipo
     <a class="link" href="catalog-pg-attribute.md" title="52.7. pg_attribute">
      <code class="structname">
       pg_attribute
      </code>
     </a>
     entradas para vincular.) Zero para tipos não compostos.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      typsubscript
     </code>
     <code class="type">
      regproc
     </code>
     (referências
     <a class="link" href="catalog-pg-proc.md" title="52.39. pg_proc">
      <code class="structname">
       pg_proc
      </code>
     </a>
     .
     <code class="structfield">
      oid
     </code>
     )
    </p>
    <p>
     O OID da função de manipulação de subscrito, ou zero, se esse tipo não suportar subscrito. Os tipos que são
     <span class="quote">
      “
      <span class="quote">
       verdadeiro
      </span>
      ”
     </span>
     tipos de arrays têm
     <code class="structfield">
      typsubscript
     </code>
     =
     <code class="function">
      array_subscript_handler
     </code>
     , mas outros tipos podem ter outras funções de manipulador para implementar comportamentos de subscrito especializados.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      typelem
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
     Se
     <code class="structfield">
      typelem
     </code>
     Se não for zero, então ele identifica outra linha
     <code class="structname">
      pg_type
     </code>
     , definindo o tipo gerado por subscrito. Isso deve ser zero se
     <code class="structfield">
      typsubscript
     </code>
     é zero. No entanto, pode ser zero quando
     <code class="structfield">
      typsubscript
     </code>
     não é zero, se o manipulador não precisa
     <code class="structfield">
      typelem
     </code>
     para determinar o tipo do resultado de subscrita. Observe que
     <code class="structfield">
      typelem
     </code>
     A dependência é considerada para implicar contenção física do tipo de elemento neste tipo; portanto, as alterações no DDL no tipo de elemento podem ser restringidas pela presença deste tipo.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      typarray
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
     Se
     <code class="structfield">
      typarray
     </code>
     Se não for zero, então ele identifica outra linha
     <code class="structname">
      pg_type
     </code>
     , que é a
     <span class="quote">
      “
      <span class="quote">
       verdadeiro
      </span>
      ”
     </span>
     tipo de matriz que tem esse tipo como elemento
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      typinput
     </code>
     <code class="type">
      regproc
     </code>
     (referências
     <a class="link" href="catalog-pg-proc.md" title="52.39. pg_proc">
      <code class="structname">
       pg_proc
      </code>
     </a>
     .
     <code class="structfield">
      oid
     </code>
     )
    </p>
    <p>
     Função de conversão de entrada (formato de texto)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      typoutput
     </code>
     <code class="type">
      regproc
     </code>
     (referências
     <a class="link" href="catalog-pg-proc.md" title="52.39. pg_proc">
      <code class="structname">
       pg_proc
      </code>
     </a>
     .
     <code class="structfield">
      oid
     </code>
     )
    </p>
    <p>
     Função de conversão de saída (formato de texto)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      typreceive
     </code>
     <code class="type">
      regproc
     </code>
     (referências
     <a class="link" href="catalog-pg-proc.md" title="52.39. pg_proc">
      <code class="structname">
       pg_proc
      </code>
     </a>
     .
     <code class="structfield">
      oid
     </code>
     )
    </p>
    <p>
     Função de conversão de entrada (formato binário), ou zero se não houver
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      typsend
     </code>
     <code class="type">
      regproc
     </code>
     (referências
     <a class="link" href="catalog-pg-proc.md" title="52.39. pg_proc">
      <code class="structname">
       pg_proc
      </code>
     </a>
     .
     <code class="structfield">
      oid
     </code>
     )
    </p>
    <p>
     Função de conversão de saída (formato binário), ou zero se não houver
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      typmodin
     </code>
     <code class="type">
      regproc
     </code>
     (referências
     <a class="link" href="catalog-pg-proc.md" title="52.39. pg_proc">
      <code class="structname">
       pg_proc
      </code>
     </a>
     .
     <code class="structfield">
      oid
     </code>
     )
    </p>
    <p>
     Função de entrada de modificadores de tipo, ou zero se o tipo não suportar modificadores
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      typmodout
     </code>
     <code class="type">
      regproc
     </code>
     (referências
     <a class="link" href="catalog-pg-proc.md" title="52.39. pg_proc">
      <code class="structname">
       pg_proc
      </code>
     </a>
     .
     <code class="structfield">
      oid
     </code>
     )
    </p>
    <p>
     Função de saída do modificador de tipo, ou zero para usar o formato padrão
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      typanalyze
     </code>
     <code class="type">
      regproc
     </code>
     (referências
     <a class="link" href="catalog-pg-proc.md" title="52.39. pg_proc">
      <code class="structname">
       pg_proc
      </code>
     </a>
     .
     <code class="structfield">
      oid
     </code>
     )
    </p>
    <p>
     Personalizado
     <a class="xref" href="sql-analyze.md" title="ANALYZE">
      <span class="refentrytitle">
       ANALISE
      </span>
     </a>
     função, ou zero para usar a função padrão
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      typalign
     </code>
     <code class="type">
      char
     </code>
    </p>
    <p>
     <code class="structfield">
      typalign
     </code>
     é o alinhamento necessário ao armazenar um valor desse tipo. Isso se aplica ao armazenamento em disco, bem como à maioria das representações do valor dentro
     <span class="productname">
      PostgreSQL
     </span>
     . Quando vários valores são armazenados consecutivamente, como na representação de uma linha completa no disco, um preenchimento é inserido antes de um dado desse tipo, para que ele comece no limite especificado. A referência de alinhamento é o início do primeiro dado na sequência. Os valores possíveis são:
    </p>
    <div class="itemizedlist">
     <ul class="itemizedlist" style="list-style-type: disc; ">
      <li class="listitem">
       <p>
        <code class="literal">
         c
        </code>
        =
        <code class="type">
         char
        </code>
        alinhamento, ou seja, não há necessidade de alinhamento.
       </p>
      </li>
      <li class="listitem">
       <p>
        <code class="literal">
         s
        </code>
        =
        <code class="type">
         short
        </code>
        alinhamento (2 bytes na maioria das máquinas).
       </p>
      </li>
      <li class="listitem">
       <p>
        <code class="literal">
         i
        </code>
        =
        <code class="type">
         int
        </code>
        alinhamento (4 bytes na maioria das máquinas).
       </p>
      </li>
      <li class="listitem">
       <p>
        <code class="literal">
         d
        </code>
        =
        <code class="type">
         double
        </code>
        alinhamento (8 bytes em muitas máquinas, mas de forma alguma todos).
       </p>
      </li>
     </ul>
    </div>
    <p>
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      typstorage
     </code>
     <code class="type">
      char
     </code>
    </p>
    <p>
     <code class="structfield">
      typstorage
     </code>
     conta para varlena tipos (aqueles com
     <code class="structfield">
      typlen
     </code>
     = -1) se o tipo estiver preparado para torrar e qual a estratégia padrão para os atributos desse tipo deve ser. Os valores possíveis são:
    </p>
    <div class="itemizedlist">
     <ul class="itemizedlist" style="list-style-type: disc; ">
      <li class="listitem">
       <p>
        <code class="literal">
         p
        </code>
        (simples): Os valores devem ser sempre armazenados simples
       </p>
      </li>
      <li class="listitem">
       <p>
        <code class="literal">
         e
        </code>
        (externo): Os valores podem ser armazenados em um secundário
        <span class="quote">
         “
         <span class="quote">
          TOAST
         </span>
         ”
        </span>
        relação (se a relação tiver uma, veja
        <code class="literal">
         pg_class.reltoastrelid
        </code>
        ).
       </p>
      </li>
      <li class="listitem">
       <p>
        <code class="literal">
         m
        </code>
        (principal): Os valores podem ser comprimidos e armazenados inline.
       </p>
      </li>
      <li class="listitem">
       <p>
        <code class="literal">
         x
        </code>
        (ampliado): Os valores podem ser comprimidos e/ou movidos para uma relação secundária.
       </p>
      </li>
     </ul>
    </div>
    <p>
     <code class="literal">
      x
     </code>
     é a escolha usual para tipos que podem ser torrados.
     <code class="literal">
      m
     </code>
     Os valores também podem ser transferidos para armazenamento secundário, mas apenas como último recurso (
     <code class="literal">
      e
     </code>
     e
     <code class="literal">
      x
     </code>
     Os valores são movidos primeiro).
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      typnotnull
     </code>
     <code class="type">
      bool
     </code>
    </p>
    <p>
     <code class="structfield">
      typnotnull
     </code>
     representa uma restrição não nula em um tipo. Usada apenas para domínios.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      typbasetype
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
     Se este for um domínio (veja
     <code class="structfield">
      typtype
     </code>
     ), então
     <code class="structfield">
      typbasetype
     </code>
     identifica o tipo sobre o qual este se baseia. Zero se este tipo não for um domínio.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      typtypmod
     </code>
     <code class="type">
      int4
     </code>
    </p>
    <p>
     Domínios de uso
     <code class="structfield">
      typtypmod
     </code>
     para registrar
     <code class="literal">
      typmod
     </code>
     devem ser aplicados ao seu tipo base (-1 se o tipo base não utiliza um
     <code class="literal">
      typmod
     </code>
     ). -1 se este tipo não for um domínio.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      typndims
     </code>
     <code class="type">
      int4
     </code>
    </p>
    <p>
     <code class="structfield">
      typndims
     </code>
     é o número de dimensões de um domínio sobre um array (ou seja,
     <code class="structfield">
      typbasetype
     </code>
     é um tipo de matriz). Zero para outros tipos, exceto domínios sobre tipos de matriz.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      typcollation
     </code>
     <code class="type">
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-collation.md" title="52.12. pg_collation">
      <code class="structname">
       pg_collation
      </code>
     </a>
     .
     <code class="structfield">
      oid
     </code>
     )
    </p>
    <p>
     <code class="structfield">
      typcollation
     </code>
     especifica a ordenação do tipo. Se o tipo não suportar ordenações, este será zero. Um tipo de base que suporte ordenações terá um valor não nulo aqui, tipicamente
     <code class="symbol">
      DEFAULT_COLLATION_OID
     </code>
     Um domínio sobre um tipo colidível pode ter um OID de codificação diferente do seu tipo de base, se um foi especificado para o domínio.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      typdefaultbin
     </code>
     <code class="type">
      pg_node_tree
     </code>
    </p>
    <p>
     Se
     <code class="structfield">
      typdefaultbin
     </code>
     se não for nulo, é o
     <code class="function">
      nodeToString()
     </code>
     representação de uma expressão padrão para o tipo. Isso é usado apenas para domínios.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      typdefault
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     <code class="structfield">
      typdefault
     </code>
     é nulo se o tipo não tiver um valor padrão associado. Se
     <code class="structfield">
      typdefaultbin
     </code>
     não é nulo,
     <code class="structfield">
      typdefault
     </code>
     deve conter uma versão legível pelo ser humano da expressão padrão representada por
     <code class="structfield">
      typdefaultbin
     </code>
     . Se
     <code class="structfield">
      typdefaultbin
     </code>
     é nulo e
     <code class="structfield">
      typdefault
     </code>
     não é, então
     <code class="structfield">
      typdefault
     </code>
     é a representação externa do valor padrão do tipo, que pode ser alimentada no conversor de entrada do tipo para produzir uma constante.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      typacl
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
 </tbody>
</table>










Nota

Para tipos de largura fixa usados em tabelas de sistema, é fundamental que o tamanho e o alinhamento definidos em `pg_type` estejam de acordo com a forma como o compilador irá organizar a coluna em uma estrutura que representa uma linha de tabela.

[Tabela 52.65](catalog-pg-type.md#CATALOG-TYPCATEGORY-TABLE "Table 52.65. typcategory Codes") lista os valores definidos pelo sistema de `typcategory`. Quaisquer adições futuras a esta lista também serão letras maiúsculas ASCII. Todos os outros caracteres ASCII são reservados para categorias definidas pelo usuário.

**Tabela 52.65. Códigos `typcategory`**



<table border="1" class="table" summary="typcategory Codes">
 <colgroup>
  <col/>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th>
    Code
   </th>
   <th>
    Category
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <code class="literal">
     A
    </code>
   </td>
   <td>
    Array types
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     B
    </code>
   </td>
   <td>
    Boolean types
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     C
    </code>
   </td>
   <td>
    Composite types
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     D
    </code>
   </td>
   <td>
    Date/time types
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     E
    </code>
   </td>
   <td>
    Enum types
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     G
    </code>
   </td>
   <td>
    Geometric types
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     I
    </code>
   </td>
   <td>
    Network address types
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     N
    </code>
   </td>
   <td>
    Numeric types
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     P
    </code>
   </td>
   <td>
    Pseudo-types
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     R
    </code>
   </td>
   <td>
    Range types
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     S
    </code>
   </td>
   <td>
    String types
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     T
    </code>
   </td>
   <td>
    Timespan types
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     U
    </code>
   </td>
   <td>
    User-defined types
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     V
    </code>
   </td>
   <td>
    Bit-string types
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     X
    </code>
   </td>
   <td>
    <code class="type">
     unknown
    </code>
    type
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     Z
    </code>
   </td>
   <td>
    Internal-use types
   </td>
  </tr>
 </tbody>
</table>





