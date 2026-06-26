## 52.64. `pg_type` [#](#CATALOG-PG-TYPE)

O catálogo `pg_type` armazena informações sobre os tipos de dados. Os tipos básicos e os tipos enum (tipos escalares) são criados com [`CREATE TYPE`](sql-createtype.md "CREATE TYPE"), e os domínios com [`CREATE DOMAIN`](sql-createdomain.md "CREATE DOMAIN"). Um tipo composto é criado automaticamente para cada tabela no banco de dados, para representar a estrutura da linha da tabela. Também é possível criar tipos compostos com `CREATE TYPE AS`.

**Tabela 52.64. Colunas `pg_type`**



<table>
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
     <code>
      oid
     </code>
     <code>
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
     <code>
      typname
     </code>
     <code>
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
     <code>
      typnamespace
     </code>
     <code>
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-namespace.md" title="52.32. pg_namespace">
      <code>
       pg_namespace
      </code>
     </a>
     .
     <code>
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
     <code>
      typowner
     </code>
     <code>
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-authid.md" title="52.8. pg_authid">
      <code>
       pg_authid
      </code>
     </a>
     .
     <code>
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
     <code>
      typlen
     </code>
     <code>
      int2
     </code>
    </p>
    <p>
     Para um tipo de tamanho fixo,
     <code>
      typlen
     </code>
     é o número de bytes na representação interna do tipo. Mas, para um tipo de comprimento variável,
     <code>
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
     <code>
      typbyval
     </code>
     <code>
      bool
     </code>
    </p>
    <p>
     <code>
      typbyval
     </code>
     determina se as rotinas internas passam um valor desse tipo por valor ou por referência.
     <code>
      typbyval
     </code>
     teria que ser falsa se
     <code>
      typlen
     </code>
     não é 1, 2 ou 4 (ou 8 em máquinas onde o Datum é de 8 bytes). Os tipos de comprimento variável são sempre passados por referência. Note que
     <code>
      typbyval
     </code>
     pode ser falsa mesmo que a comprimento permita a passagem por valor.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      typtype
     </code>
     <code>
      char
     </code>
    </p>
    <p>
     <code>
      typtype
     </code>
     é
     <code>
      b
     </code>
     para um tipo de base,
     <code>
      c
     </code>
     para um tipo composto (por exemplo, o tipo de linha de uma tabela),
     <code>
      d
     </code>
     para um domínio,
     <code>
      e
     </code>
     para um tipo de enum,
     <code>
      p
     </code>
     para um pseudo-tipo,
     <code>
      r
     </code>
     para um tipo de gama, ou
     <code>
      m
     </code>
     para um tipo multiranged.
     <code>
      typrelid
     </code>
     e
     <code>
      typbasetype
     </code>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      typcategory
     </code>
     <code>
      char
     </code>
    </p>
    <p>
     <code>
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
     <code>
      typispreferred
     </code>
     <code>
      bool
     </code>
    </p>
    <p>
     Verdadeiro se o tipo é um alvo de cast preferido dentro de seu
     <code>
      typcategory
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      typisdefined
     </code>
     <code>
      bool
     </code>
    </p>
    <p>
     Verdadeiro se o tipo estiver definido, falso se esta for uma entrada de marcador para um tipo ainda não definido. Quando
     <code>
      typisdefined
     </code>
     É falso, nada, exceto o nome do tipo, o espaço de nomeação e o OID podem ser confiáveis.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      typdelim
     </code>
     <code>
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
     <code>
      typrelid
     </code>
     <code>
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-class.md" title="52.11. pg_class">
      <code>
       pg_class
      </code>
     </a>
     .
     <code>
      oid
     </code>
     )
    </p>
    <p>
     Se este for um tipo composto (veja
     <code>
      typtype
     </code>
     ), então esta coluna aponta para
     <a class="link" href="catalog-pg-class.md" title="52.11. pg_class">
      <code>
       pg_class
      </code>
     </a>
     entrada que define a tabela correspondente. (Para um tipo de composto independente, o
     <a class="link" href="catalog-pg-class.md" title="52.11. pg_class">
      <code>
       pg_class
      </code>
     </a>
     A entrada não representa realmente uma tabela, mas é necessária de qualquer forma para o tipo
     <a class="link" href="catalog-pg-attribute.md" title="52.7. pg_attribute">
      <code>
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
     <code>
      typsubscript
     </code>
     <code>
      regproc
     </code>
     (referências
     <a class="link" href="catalog-pg-proc.md" title="52.39. pg_proc">
      <code>
       pg_proc
      </code>
     </a>
     .
     <code>
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
     <code>
      typsubscript
     </code>
     =
     <code>
      array_subscript_handler
     </code>
     , mas outros tipos podem ter outras funções de manipulador para implementar comportamentos de subscrito especializados.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      typelem
     </code>
     <code>
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-type.md" title="52.64. pg_type">
      <code>
       pg_type
      </code>
     </a>
     .
     <code>
      oid
     </code>
     )
    </p>
    <p>
     Se
     <code>
      typelem
     </code>
     Se não for zero, então ele identifica outra linha
     <code>
      pg_type
     </code>
     , definindo o tipo gerado por subscrito. Isso deve ser zero se
     <code>
      typsubscript
     </code>
     é zero. No entanto, pode ser zero quando
     <code>
      typsubscript
     </code>
     não é zero, se o manipulador não precisa
     <code>
      typelem
     </code>
     para determinar o tipo do resultado de subscrita. Observe que
     <code>
      typelem
     </code>
     A dependência é considerada para implicar contenção física do tipo de elemento neste tipo; portanto, as alterações no DDL no tipo de elemento podem ser restringidas pela presença deste tipo.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      typarray
     </code>
     <code>
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-type.md" title="52.64. pg_type">
      <code>
       pg_type
      </code>
     </a>
     .
     <code>
      oid
     </code>
     )
    </p>
    <p>
     Se
     <code>
      typarray
     </code>
     Se não for zero, então ele identifica outra linha
     <code>
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
     <code>
      typinput
     </code>
     <code>
      regproc
     </code>
     (referências
     <a class="link" href="catalog-pg-proc.md" title="52.39. pg_proc">
      <code>
       pg_proc
      </code>
     </a>
     .
     <code>
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
     <code>
      typoutput
     </code>
     <code>
      regproc
     </code>
     (referências
     <a class="link" href="catalog-pg-proc.md" title="52.39. pg_proc">
      <code>
       pg_proc
      </code>
     </a>
     .
     <code>
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
     <code>
      typreceive
     </code>
     <code>
      regproc
     </code>
     (referências
     <a class="link" href="catalog-pg-proc.md" title="52.39. pg_proc">
      <code>
       pg_proc
      </code>
     </a>
     .
     <code>
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
     <code>
      typsend
     </code>
     <code>
      regproc
     </code>
     (referências
     <a class="link" href="catalog-pg-proc.md" title="52.39. pg_proc">
      <code>
       pg_proc
      </code>
     </a>
     .
     <code>
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
     <code>
      typmodin
     </code>
     <code>
      regproc
     </code>
     (referências
     <a class="link" href="catalog-pg-proc.md" title="52.39. pg_proc">
      <code>
       pg_proc
      </code>
     </a>
     .
     <code>
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
     <code>
      typmodout
     </code>
     <code>
      regproc
     </code>
     (referências
     <a class="link" href="catalog-pg-proc.md" title="52.39. pg_proc">
      <code>
       pg_proc
      </code>
     </a>
     .
     <code>
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
     <code>
      typanalyze
     </code>
     <code>
      regproc
     </code>
     (referências
     <a class="link" href="catalog-pg-proc.md" title="52.39. pg_proc">
      <code>
       pg_proc
      </code>
     </a>
     .
     <code>
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
     <code>
      typalign
     </code>
     <code>
      char
     </code>
    </p>
    <p>
     <code>
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
        <code>
         c
        </code>
        =
        <code>
         char
        </code>
        alinhamento, ou seja, não há necessidade de alinhamento.
       </p>
      </li>
      <li class="listitem">
       <p>
        <code>
         s
        </code>
        =
        <code>
         short
        </code>
        alinhamento (2 bytes na maioria das máquinas).
       </p>
      </li>
      <li class="listitem">
       <p>
        <code>
         i
        </code>
        =
        <code>
         int
        </code>
        alinhamento (4 bytes na maioria das máquinas).
       </p>
      </li>
      <li class="listitem">
       <p>
        <code>
         d
        </code>
        =
        <code>
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
     <code>
      typstorage
     </code>
     <code>
      char
     </code>
    </p>
    <p>
     <code>
      typstorage
     </code>
     conta para varlena tipos (aqueles com
     <code>
      typlen
     </code>
     = -1) se o tipo estiver preparado para torrar e qual a estratégia padrão para os atributos desse tipo deve ser. Os valores possíveis são:
    </p>
    <div class="itemizedlist">
     <ul class="itemizedlist" style="list-style-type: disc; ">
      <li class="listitem">
       <p>
        <code>
         p
        </code>
        (simples): Os valores devem ser sempre armazenados simples
       </p>
      </li>
      <li class="listitem">
       <p>
        <code>
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
        <code>
         pg_class.reltoastrelid
        </code>
        ).
       </p>
      </li>
      <li class="listitem">
       <p>
        <code>
         m
        </code>
        (principal): Os valores podem ser comprimidos e armazenados inline.
       </p>
      </li>
      <li class="listitem">
       <p>
        <code>
         x
        </code>
        (ampliado): Os valores podem ser comprimidos e/ou movidos para uma relação secundária.
       </p>
      </li>
     </ul>
    </div>
    <p>
     <code>
      x
     </code>
     é a escolha usual para tipos que podem ser torrados.
     <code>
      m
     </code>
     Os valores também podem ser transferidos para armazenamento secundário, mas apenas como último recurso (
     <code>
      e
     </code>
     e
     <code>
      x
     </code>
     Os valores são movidos primeiro).
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      typnotnull
     </code>
     <code>
      bool
     </code>
    </p>
    <p>
     <code>
      typnotnull
     </code>
     representa uma restrição não nula em um tipo. Usada apenas para domínios.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      typbasetype
     </code>
     <code>
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-type.md" title="52.64. pg_type">
      <code>
       pg_type
      </code>
     </a>
     .
     <code>
      oid
     </code>
     )
    </p>
    <p>
     Se este for um domínio (veja
     <code>
      typtype
     </code>
     ), então
     <code>
      typbasetype
     </code>
     identifica o tipo sobre o qual este se baseia. Zero se este tipo não for um domínio.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      typtypmod
     </code>
     <code>
      int4
     </code>
    </p>
    <p>
     Domínios de uso
     <code>
      typtypmod
     </code>
     para registrar
     <code>
      typmod
     </code>
     devem ser aplicados ao seu tipo base (-1 se o tipo base não utiliza um
     <code>
      typmod
     </code>
     ). -1 se este tipo não for um domínio.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      typndims
     </code>
     <code>
      int4
     </code>
    </p>
    <p>
     <code>
      typndims
     </code>
     é o número de dimensões de um domínio sobre um array (ou seja,
     <code>
      typbasetype
     </code>
     é um tipo de matriz). Zero para outros tipos, exceto domínios sobre tipos de matriz.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      typcollation
     </code>
     <code>
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-collation.md" title="52.12. pg_collation">
      <code>
       pg_collation
      </code>
     </a>
     .
     <code>
      oid
     </code>
     )
    </p>
    <p>
     <code>
      typcollation
     </code>
     especifica a ordenação do tipo. Se o tipo não suportar ordenações, este será zero. Um tipo de base que suporte ordenações terá um valor não nulo aqui, tipicamente
     <code>
      DEFAULT_COLLATION_OID
     </code>
     Um domínio sobre um tipo colidível pode ter um OID de codificação diferente do seu tipo de base, se um foi especificado para o domínio.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      typdefaultbin
     </code>
     <code>
      pg_node_tree
     </code>
    </p>
    <p>
     Se
     <code>
      typdefaultbin
     </code>
     se não for nulo, é o
     <code>
      nodeToString()
     </code>
     representação de uma expressão padrão para o tipo. Isso é usado apenas para domínios.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      typdefault
     </code>
     <code>
      text
     </code>
    </p>
    <p>
     <code>
      typdefault
     </code>
     é nulo se o tipo não tiver um valor padrão associado. Se
     <code>
      typdefaultbin
     </code>
     não é nulo,
     <code>
      typdefault
     </code>
     deve conter uma versão legível pelo ser humano da expressão padrão representada por
     <code>
      typdefaultbin
     </code>
     . Se
     <code>
      typdefaultbin
     </code>
     é nulo e
     <code>
      typdefault
     </code>
     não é, então
     <code>
      typdefault
     </code>
     é a representação externa do valor padrão do tipo, que pode ser alimentada no conversor de entrada do tipo para produzir uma constante.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      typacl
     </code>
     <code>
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



<table>
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
    <code>
     A
    </code>
   </td>
   <td>
    Array types
   </td>
  </tr>
  <tr>
   <td>
    <code>
     B
    </code>
   </td>
   <td>
    Boolean types
   </td>
  </tr>
  <tr>
   <td>
    <code>
     C
    </code>
   </td>
   <td>
    Composite types
   </td>
  </tr>
  <tr>
   <td>
    <code>
     D
    </code>
   </td>
   <td>
    Date/time types
   </td>
  </tr>
  <tr>
   <td>
    <code>
     E
    </code>
   </td>
   <td>
    Enum types
   </td>
  </tr>
  <tr>
   <td>
    <code>
     G
    </code>
   </td>
   <td>
    Geometric types
   </td>
  </tr>
  <tr>
   <td>
    <code>
     I
    </code>
   </td>
   <td>
    Network address types
   </td>
  </tr>
  <tr>
   <td>
    <code>
     N
    </code>
   </td>
   <td>
    Numeric types
   </td>
  </tr>
  <tr>
   <td>
    <code>
     P
    </code>
   </td>
   <td>
    Pseudo-types
   </td>
  </tr>
  <tr>
   <td>
    <code>
     R
    </code>
   </td>
   <td>
    Range types
   </td>
  </tr>
  <tr>
   <td>
    <code>
     S
    </code>
   </td>
   <td>
    String types
   </td>
  </tr>
  <tr>
   <td>
    <code>
     T
    </code>
   </td>
   <td>
    Timespan types
   </td>
  </tr>
  <tr>
   <td>
    <code>
     U
    </code>
   </td>
   <td>
    User-defined types
   </td>
  </tr>
  <tr>
   <td>
    <code>
     V
    </code>
   </td>
   <td>
    Bit-string types
   </td>
  </tr>
  <tr>
   <td>
    <code>
     X
    </code>
   </td>
   <td>
    <code>
     unknown
    </code>
    type
   </td>
  </tr>
  <tr>
   <td>
    <code>
     Z
    </code>
   </td>
   <td>
    Internal-use types
   </td>
  </tr>
 </tbody>
</table>





