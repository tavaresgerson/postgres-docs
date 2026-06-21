## 8.19. Tipos de Identificador de Objeto [#](#DATATYPE-OID)

Os identificadores de objeto (OIDs) são utilizados internamente pelo PostgreSQL como chaves primárias para várias tabelas do sistema. O tipo `oid` representa um identificador de objeto. Há também vários tipos de alias para `oid`, cada um com o nome `regsomething`. A [Tabela 8.26](datatype-oid.md#DATATYPE-OID-TABLE) mostra uma visão geral.

O tipo `oid` é atualmente implementado como um inteiro de quatro bytes não assinado. Portanto, não é grande o suficiente para fornecer unicidade em todo o banco de dados em grandes bancos de dados, ou até mesmo em grandes tabelas individuais.

O próprio tipo `oid` tem poucas operações além da comparação. No entanto, ele pode ser convertido para inteiro e, em seguida, manipulado usando os operadores padrão de inteiros. (Cuidado com a possível confusão entre sinalizado e não sinalizado se você fizer isso.)

Os tipos de alias OID não possuem operações próprias, exceto para rotinas de entrada e saída especializadas. Essas rotinas são capazes de aceitar e exibir nomes simbólicos para objetos do sistema, em vez do valor numérico bruto que o tipo `oid` usaria. Os tipos de alias permitem uma busca simplificada dos valores OID para objetos. Por exemplo, para examinar as linhas `pg_attribute` relacionadas a uma tabela `mytable`, é possível escrever:

```
SELECT * FROM pg_attribute WHERE attrelid = 'mytable'::regclass;
```

em vez de:

```
SELECT * FROM pg_attribute
  WHERE attrelid = (SELECT oid FROM pg_class WHERE relname = 'mytable');
```

Embora isso não pareça muito ruim por si só, ainda é bastante simplificado. Seria necessário um subconjunto muito mais complicado para selecionar o OID correto se houver várias tabelas com o nome `mytable` em diferentes esquemas. O conversor de entrada `regclass` lida com a pesquisa de tabela de acordo com a configuração do caminho do esquema, e assim faz o "coisa certa" automaticamente. Da mesma forma, a conversão do OID de uma tabela para `regclass` é útil para a exibição simbólica de um OID numérico.

**Tabela 8.26. Tipos de Identificador de Objeto**



<table border="1" class="table" summary="Object Identifier Types">
 <colgroup>
  <col/>
  <col/>
  <col/>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th>
    Name
   </th>
   <th>
    References
   </th>
   <th>
    Descrição
   </th>
   <th>
    Value Example
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <code class="type">
     oid
    </code>
   </td>
   <td>
    any
   </td>
   <td>
    identificador de objeto numérico
   </td>
   <td>
    <code class="literal">
     564182
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     regclass
    </code>
   </td>
   <td>
    <code class="structname">
     pg_class
    </code>
   </td>
   <td>
    nome da relação
   </td>
   <td>
    <code class="literal">
     pg_type
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     regcollation
    </code>
   </td>
   <td>
    <code class="structname">
     pg_collation
    </code>
   </td>
   <td>
    nome da agregação
   </td>
   <td>
    <code class="literal">
     "POSIX"
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     regconfig
    </code>
   </td>
   <td>
    <code class="structname">
     pg_ts_config
    </code>
   </td>
   <td>
    configuração de pesquisa de texto
   </td>
   <td>
    <code class="literal">
     english
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     regdictionary
    </code>
   </td>
   <td>
    <code class="structname">
     pg_ts_dict
    </code>
   </td>
   <td>
    dicionário de busca de texto
   </td>
   <td>
    <code class="literal">
     simple
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     regnamespace
    </code>
   </td>
   <td>
    <code class="structname">
     pg_namespace
    </code>
   </td>
   <td>
    nome do espaço de nomeação
   </td>
   <td>
    <code class="literal">
     pg_catalog
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     regoper
    </code>
   </td>
   <td>
    <code class="structname">
     pg_operator
    </code>
   </td>
   <td>
    nome do operador
   </td>
   <td>
    <code class="literal">
     +
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     regoperator
    </code>
   </td>
   <td>
    <code class="structname">
     pg_operator
    </code>
   </td>
   <td>
    operador com tipos de argumento
   </td>
   <td>
    <code class="literal">
     *(integer,​integer)
    </code>
    or
    <code class="literal">
     -(NONE,​integer)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     regproc
    </code>
   </td>
   <td>
    <code class="structname">
     pg_proc
    </code>
   </td>
   <td>
    nome da função
   </td>
   <td>
    <code class="literal">
     sum
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     regprocedure
    </code>
   </td>
   <td>
    <code class="structname">
     pg_proc
    </code>
   </td>
   <td>
    função com tipos de argumentos
   </td>
   <td>
    <code class="literal">
     sum(int4)
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     regrole
    </code>
   </td>
   <td>
    <code class="structname">
     pg_authid
    </code>
   </td>
   <td>
    nome do papel
   </td>
   <td>
    <code class="literal">
     smithee
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     regtype
    </code>
   </td>
   <td>
    <code class="structname">
     pg_type
    </code>
   </td>
   <td>
    nome do tipo de dados
   </td>
   <td>
    <code class="literal">
     integer
    </code>
   </td>
  </tr>
 </tbody>
</table>









Todos os tipos de alias OID para objetos que são agrupados por namespace aceitam nomes qualificados por esquema e exibirão nomes qualificados por esquema na saída se o objeto não for encontrado no caminho de pesquisa atual sem ser qualificado. Por exemplo, `myschema.mytable` é uma entrada aceitável para `regclass` (se houver uma tabela assim). Esse valor pode ser exibido como `myschema.mytable`, ou apenas `mytable`, dependendo do caminho de pesquisa atual. Os tipos de alias `regproc` e `regoper` só aceitam nomes de entrada que são únicos (não sobrecarregados), portanto, são de uso limitado; para a maioria dos usos, `regprocedure` ou `regoperator` são mais apropriados. Para `regoperator`, os operadores unários são identificados escrevendo `NONE` para o operador não utilizado.

As funções de entrada para esses tipos permitem espaço em branco entre os tokens e transformarão as letras maiúsculas em minúsculas, exceto dentro de aspas duplas; isso é feito para tornar as regras de sintaxe semelhantes à maneira como os nomes dos objetos são escritos em SQL. Por outro lado, as funções de saída usarão aspas duplas, se necessário, para que a saída seja um identificador SQL válido. Por exemplo, o OID de uma função chamada `Foo` (com a letra maiúscula `F`) que leva dois argumentos inteiros pode ser inserido como `' "Foo" ( int, integer ) '::regprocedure`. A saída ficaria como `"Foo"(integer,integer)`. Tanto o nome da função quanto os nomes dos tipos de argumento também poderiam ser qualificados pelo esquema.

Muitas funções incorporadas do PostgreSQL aceitam o OID de uma tabela ou outro tipo de objeto de banco de dados, e, por conveniência, são declaradas como aceitando `regclass` (ou o tipo de alias OID apropriado). Isso significa que você não precisa procurar o OID do objeto manualmente, mas pode simplesmente inserir seu nome como uma literal de string. Por exemplo, a função `nextval(regclass)` aceita o OID de uma relação de sequência, então você poderia chamá-la assim:

```
nextval('foo')              operates on sequence foo
nextval('FOO')              same as above
nextval('"Foo"')            operates on sequence Foo
nextval('myschema.foo')     operates on myschema.foo
nextval('"myschema".foo')   same as above
nextval('foo')              searches search path for foo
```

### Nota

Quando você escreve o argumento de uma função como uma string literal não ornamentada, ela se torna uma constante do tipo `regclass` (ou o tipo apropriado). Como essa é realmente apenas um OID, ela rastreará o objeto originalmente identificado, apesar de posterior renomeação, reatribuição de esquema, etc. Esse comportamento de "ligação precoce" é geralmente desejável para referências de objetos em padrões de coluna e visualizações. Mas, às vezes, você pode querer "ligação tardia" onde a referência do objeto é resolvida no tempo de execução. Para obter comportamento de ligação tardia, force a constante a ser armazenada como uma constante `text` em vez de `regclass`:

```
nextval('foo'::text)      foo is looked up at runtime
```

A função `to_regclass()` e seus irmãos também podem ser usados para realizar pesquisas em tempo de execução. Veja [Tabela 9.76](functions-info.md#FUNCTIONS-INFO-CATALOG-TABLE).

Outro exemplo prático de uso do `regclass` é procurar o OID de uma tabela listada nas visualizações do `information_schema`, que não fornecem esses OIDs diretamente. Por exemplo, pode-se desejar chamar a função `pg_relation_size()`, que requer o OID da tabela. Tendo em conta as regras acima, a maneira correta de fazer isso é

```
SELECT table_schema, table_name,
       pg_relation_size((quote_ident(table_schema) || '.' ||
                         quote_ident(table_name))::regclass)
FROM information_schema.tables
WHERE ...
```

A função `quote_ident()` cuidará da citação dupla dos identificadores, quando necessário. Aparenta ser mais fácil

```
SELECT pg_relation_size(table_name)
FROM information_schema.tables
WHERE ...
```

não é *recomendado*, porque falhará para tabelas que estão fora do seu caminho de pesquisa ou que têm nomes que exigem citação.

Uma propriedade adicional da maioria dos tipos de alias de OID é a criação de dependências. Se uma constante de um desses tipos aparecer em uma expressão armazenada (como uma expressão padrão de coluna ou uma visão), ela cria uma dependência sobre o objeto referenciado. Por exemplo, se uma coluna tiver uma expressão padrão `nextval('my_seq'::regclass)`, o PostgreSQL entende que a expressão padrão depende da sequência `my_seq`, então o sistema não permitirá que a sequência seja removida sem primeiro remover a expressão padrão. A alternativa de `nextval('my_seq'::text)` não cria uma dependência. (`regrole` é uma exceção a essa propriedade. Constantes desse tipo não são permitidas em expressões armazenadas.)

Outro tipo de identificador utilizado pelo sistema é o identificador de transação (abreviado como xact), que é o tipo de dados das colunas do sistema `xid`. Os identificadores de transação são quantidades de 32 bits. Em alguns contextos, é usada uma variante de 64 bits `xid8`. Ao contrário dos valores de `xid`, os valores de `xid8` aumentam de forma estritamente monotônica e não podem ser reutilizados durante a vida útil de um grupo de bancos de dados. Consulte [Seção 67.1] para obter mais detalhes. [(transaction-id.md "67.1. Transactions and Identifiers")]

Um terceiro tipo de identificador utilizado pelo sistema é `cid`, ou identificador de comando. Este é o tipo de dados das colunas do sistema `cmin` e `cmax`. Os identificadores de comando também são quantidades de 32 bits.

Um tipo de identificador final utilizado pelo sistema é `tid`, ou identificador de tupla (identificador de linha). Este é o tipo de dados da coluna do sistema `ctid`. Um ID de tupla é um par (número de bloco, índice de tupla dentro do bloco) que identifica a localização física da linha dentro de sua tabela.

(As colunas do sistema são explicadas mais detalhadamente em [Seção 5.6](ddl-system-columns.md).