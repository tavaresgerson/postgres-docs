### Capítulo 8. Tipos de dados

**Índice**

* [8.1. Tipos Numéricos](datatype-numeric.md)
  + [8.1.1. Tipos inteiros](datatype-numeric.md#DATATYPE-INT)
  + [8.1.2. Números de precisão arbitrária](datatype-numeric.md#DATATYPE-NUMERIC-DECIMAL)
  + [8.1.3. Tipos de ponto flutuante](datatype-numeric.md#DATATYPE-FLOAT)
  + [8.1.4. Tipos de série](datatype-numeric.md#DATATYPE-SERIAL)
* [8.2. Tipos Monetários](datatype-money.md)
* [8.3. Tipos de Caracteres](datatype-character.md)
* [8.4. Tipos de Dados Binários](datatype-binary.md)
  + [8.4.1. `bytea` Hex Format](datatype-binary.md#DATATYPE-BINARY-BYTEA-HEX-FORMAT)
  + [8.4.2. `bytea` Formato de Escape](datatype-binary.md#DATATYPE-BINARY-BYTEA-ESCAPE-FORMAT)
* [8.5. Tipos de data/hora](datatype-datetime.md)
  + [8.5.1. Entrada de data/hora](datatype-datetime.md#DATATYPE-DATETIME-INPUT)
  + [8.5.2. Saída de data/hora](datatype-datetime.md#DATATYPE-DATETIME-OUTPUT)
  + [8.5.3. Fuso horário](datatype-datetime.md#DATATYPE-TIMEZONES)
  + [8.5.4. Entrada de intervalo](datatype-datetime.md#DATATYPE-INTERVAL-INPUT)
  + [8.5.5. Saída de intervalo](datatype-datetime.md#DATATYPE-INTERVAL-OUTPUT)
* [8.6. Tipo Booleano](datatype-boolean.md)
* [8.7. Tipos Enumerados](datatype-enum.md)
  + [8.7.1. Declaração de Tipos Enumerados](datatype-enum.md#DATATYPE-ENUM-DECLARATION)
  + [8.7.2. Ordem](datatype-enum.md#DATATYPE-ENUM-ORDERING)
  + [8.7.3. Segurança do Tipo](datatype-enum.md#DATATYPE-ENUM-TYPE-SAFETY)
  + [8.7.4. Detalhes de Implementação](datatype-enum.md#DATATYPE-ENUM-IMPLEMENTATION-DETAILS)
* [8.8. Tipos geométricos](datatype-geometric.md)
  + [8.8.1. Pontos](datatype-geometric.md#DATATYPE-GEOMETRIC-POINTS)
  + [8.8.2. Linhas](datatype-geometric.md#DATATYPE-LINE)
  + [8.8.3. Setores de linha](datatype-geometric.md#DATATYPE-LSEG)
  + [8.8.4. Caixas](datatype-geometric.md#DATATYPE-GEOMETRIC-BOXES)
  + [8.8.5. Caminhos](datatype-geometric.md#DATATYPE-GEOMETRIC-PATHS)
  + [8.8.6. Polígonos](datatype-geometric.md#DATATYPE-POLYGON)
  + [8.8.7. Círculos](datatype-geometric.md#DATATYPE-CIRCLE)
* [8.9. Tipos de Endereços de Rede](datatype-net-types.md)
  + [8.9.1. `inet`](datatype-net-types.md#DATATYPE-INET)
  + [8.9.2. `cidr`](datatype-net-types.md#DATATYPE-CIDR)
  + [8.9.3. `inet` vs. `cidr`](datatype-net-types.md#DATATYPE-INET-VS-CIDR)
  + [8.9.4. `macaddr`](datatype-net-types.md#DATATYPE-MACADDR)
  + [8.9.5. `macaddr8`](datatype-net-types.md#DATATYPE-MACADDR8)
* [8.10. Tipos de String de Bits](datatype-bit.md)
* [8.11. Tipos de Pesquisa de Texto](datatype-textsearch.md)
  + [8.11.1. `tsvector`](datatype-textsearch.md#DATATYPE-TSVECTOR)
  + [8.11.2. `tsquery`](datatype-textsearch.md#DATATYPE-TSQUERY)
* [8.12. Tipo de UUID](datatype-uuid.md)
* [8.13. Tipo de XML](datatype-xml.md)
  + [8.13.1. Criação de Valores XML](datatype-xml.md#DATATYPE-XML-CREATING)
  + [8.13.2. Tratamento de codificação](datatype-xml.md#DATATYPE-XML-ENCODING-HANDLING)
  + [8.13.3. Acesso a Valores XML](datatype-xml.md#DATATYPE-XML-ACCESSING-XML-VALUES)
* [8.14. Tipos JSON](datatype-json.md)
  + [8.14.1. Sintaxe de entrada e saída JSON](datatype-json.md#JSON-KEYS-ELEMENTS)
  + [8.14.2. Projeto de documentos JSON](datatype-json.md#JSON-DOC-DESIGN)
  + [8.14.3. `jsonb` Contenimento e existência](datatype-json.md#JSON-CONTAINMENT)
  + [8.14.4. `jsonb` Indexação](datatype-json.md#JSON-INDEXING)
  + [8.14.5. `jsonb` Subscrito](datatype-json.md#JSONB-SUBSCRIPTING)
  + [8.14.6. Transformações](datatype-json.md#DATATYPE-JSON-TRANSFORMS)
  + [8.14.7. Tipo jsonpath](datatype-json.md#DATATYPE-JSONPATH)
* [8.15. Arrays](arrays.md)
  + [8.15.1. Declaração de Tipos de Array](arrays.md#ARRAYS-DECLARATION)
  + [8.15.2. Entrada de Valor de Array](arrays.md#ARRAYS-INPUT)
  + [8.15.3. Acesso a Arrays](arrays.md#ARRAYS-ACCESSING)
  + [8.15.4. Modificação de Arrays](arrays.md#ARRAYS-MODIFYING)
  + [8.15.5. Pesquisa em Arrays](arrays.md#ARRAYS-SEARCHING)
  + [8.15.6. Sintaxe de Entrada e Saída de Array](arrays.md#ARRAYS-IO)
* [8.16. Tipos compostos](rowtypes.md)
  + [8.16.1. Declaração de Tipos Compostos](rowtypes.md#ROWTYPES-DECLARING)
  + [8.16.2. Construção de Valores Compostos](rowtypes.md#ROWTYPES-CONSTRUCTING)
  + [8.16.3. Acesso a Tipos Compostos](rowtypes.md#ROWTYPES-ACCESSING)
  + [8.16.4. Modificação de Tipos Compostos](rowtypes.md#ROWTYPES-MODIFYING)
  + [8.16.5. Uso de Tipos Compostos em Consultas](rowtypes.md#ROWTYPES-USAGE)
  + [8.16.6. Sintaxe de Entrada e Saída de Tipos Compostos](rowtypes.md#ROWTYPES-IO-SYNTAX)
* [8.17. Tipos de faixa](rangetypes.md)
  + [8.17.1. Tipos de intervalo embutido e multiintervalo](rangetypes.md#RANGETYPES-BUILTIN)
  + [8.17.2. Exemplos](rangetypes.md#RANGETYPES-EXAMPLES)
  + [8.17.3. Limites inclusivos e exclusivos](rangetypes.md#RANGETYPES-INCLUSIVITY)
  + [8.17.4. Intervalos infinitos (sem limites)[(rangetypes.md#RANGETYPES-INFINITE)]
  + [8.17.5. Entrada/saída de intervalo](rangetypes.md#RANGETYPES-IO)
  + [8.17.6. Construção de intervalos e multiintervalos](rangetypes.md#RANGETYPES-CONSTRUCT)
  + [8.17.7. Tipos de intervalo discreto](rangetypes.md#RANGETYPES-DISCRETE)
  + [8.17.8. Definindo novos tipos de intervalo](rangetypes.md#RANGETYPES-DEFINING)
  + [8.17.9. Indexação](rangetypes.md#RANGETYPES-INDEXING)
  + [8.17.10. Restrições em intervalos](rangetypes.md#RANGETYPES-CONSTRAINT)
* [8.18. Tipos de domínio](domains.md)
* [8.19. Tipos de identificador de objeto](datatype-oid.md)
* [8.20. Tipo `pg_lsn`](datatype-pg-lsn.md)
* [8.21. Pseudo-tipos](datatype-pseudo.md)

O PostgreSQL possui um conjunto rico de tipos de dados nativos disponíveis para os usuários. Os usuários podem adicionar novos tipos ao PostgreSQL usando o comando [CREATE TYPE](sql-createtype.md).

[Tabela 8.1](datatype.md#DATATYPE-TABLE) mostra todos os tipos de dados de propósito geral integrados. A maioria dos nomes alternativos listados na coluna “Aliases” são os nomes usados internamente pelo PostgreSQL por razões históricas. Além disso, alguns tipos usados internamente ou descontinuados estão disponíveis, mas não estão listados aqui.

**Tabela 8.1. Tipos de dados**

<table>
 <colgroup>
  <col class="col1"/>
  <col class="col2"/>
  <col class="col3"/>
 </colgroup>
 <thead>
  <tr>
   <th>
    Name
   </th>
   <th>
    Aliases
   </th>
   <th>
    Descrição
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <code>
     bigint
    </code>
   </td>
   <td>
    <code>
     int8
    </code>
   </td>
   <td>
    inteiro de oito bytes
   </td>
  </tr>
  <tr>
   <td>
    <code>
     bigserial
    </code>
   </td>
   <td>
    <code>
     serial8
    </code>
   </td>
   <td>
    autoincrementado inteiro de oito bytes
   </td>
  </tr>
  <tr>
   <td>
    <code>
     bit [ (
     <em class="replaceable">
      <code>
       n
      </code>
     </em>
     ) ]
    </code>
   </td>
   <td>
   </td>
   <td>
    string de bits de comprimento fixo
   </td>
  </tr>
  <tr>
   <td>
    <code>
     bit varying [ (
     <em class="replaceable">
      <code>
       n
      </code>
     </em>
     ) ]
    </code>
   </td>
   <td>
    <code>
     varbit [ (
     <em class="replaceable">
      <code>
       n
      </code>
     </em>
     ) ]
    </code>
   </td>
   <td>
    string de bits de comprimento variável
   </td>
  </tr>
  <tr>
   <td>
    <code>
     boolean
    </code>
   </td>
   <td>
    <code>
     bool
    </code>
   </td>
   <td>
    lógico Booleano (verdadeiro/falso)
   </td>
  </tr>
  <tr>
   <td>
    <code>
     box
    </code>
   </td>
   <td>
   </td>
   <td>
    caixa retangular em um avião
   </td>
  </tr>
  <tr>
   <td>
    <code>
     bytea
    </code>
   </td>
   <td>
   </td>
   <td>
    dados binários (
    <span class="quote">
     “
     <span class="quote">
      matriz de bytes
     </span>
     ”
    </span>
    )
   </td>
  </tr>
  <tr>
   <td>
    <code>
     character [ (
     <em class="replaceable">
      <code>
       n
      </code>
     </em>
     ) ]
    </code>
   </td>
   <td>
    <code>
     char [ (
     <em class="replaceable">
      <code>
       n
      </code>
     </em>
     ) ]
    </code>
   </td>
   <td>
    string de caracteres de comprimento fixo
   </td>
  </tr>
  <tr>
   <td>
    <code>
     character varying [ (
     <em class="replaceable">
      <code>
       n
      </code>
     </em>
     ) ]
    </code>
   </td>
   <td>
    <code>
     varchar [ (
     <em class="replaceable">
      <code>
       n
      </code>
     </em>
     ) ]
    </code>
   </td>
   <td>
    string de caracteres de comprimento variável
   </td>
  </tr>
  <tr>
   <td>
    <code>
     cidr
    </code>
   </td>
   <td>
   </td>
   <td>
    Endereço de rede IPv4 ou IPv6
   </td>
  </tr>
  <tr>
   <td>
    <code>
     circle
    </code>
   </td>
   <td>
   </td>
   <td>
    círculo em um avião
   </td>
  </tr>
  <tr>
   <td>
    <code>
     date
    </code>
   </td>
   <td>
   </td>
   <td>
    data do calendário (ano, mês, dia)
   </td>
  </tr>
  <tr>
   <td>
    <code>
     double precision
    </code>
   </td>
   <td>
    <code>
     float
    </code>
    ,
    <code>
     float8
    </code>
   </td>
   <td>
    número de ponto flutuante de precisão dupla (8 bytes)
   </td>
  </tr>
  <tr>
   <td>
    <code>
     inet
    </code>
   </td>
   <td>
   </td>
   <td>
    Endereço de host IPv4 ou IPv6
   </td>
  </tr>
  <tr>
   <td>
    <code>
     integer
    </code>
   </td>
   <td>
    <code>
     int
    </code>
    ,
    <code>
     int4
    </code>
   </td>
   <td>
    inteiro de quatro bytes
   </td>
  </tr>
  <tr>
   <td>
    <code>
     interval [
     <em class="replaceable">
      <code>
       fields
      </code>
     </em>
     ] [ (
     <em class="replaceable">
      <code>
       p
      </code>
     </em>
     ) ]
    </code>
   </td>
   <td>
   </td>
   <td>
    período de tempo
   </td>
  </tr>
  <tr>
   <td>
    <code>
     json
    </code>
   </td>
   <td>
   </td>
   <td>
    dados JSON textuais
   </td>
  </tr>
  <tr>
   <td>
    <code>
     jsonb
    </code>
   </td>
   <td>
   </td>
   <td>
    dados binários JSON, decompostos
   </td>
  </tr>
  <tr>
   <td>
    <code>
     line
    </code>
   </td>
   <td>
   </td>
   <td>
    linha infinita em um plano
   </td>
  </tr>
  <tr>
   <td>
    <code>
     lseg
    </code>
   </td>
   <td>
   </td>
   <td>
    semente de linha em um plano
   </td>
  </tr>
  <tr>
   <td>
    <code>
     macaddr
    </code>
   </td>
   <td>
   </td>
   <td>
    Endereço MAC (Controle de Acesso à Mídia)
   </td>
  </tr>
  <tr>
   <td>
    <code>
     macaddr8
    </code>
   </td>
   <td>
   </td>
   <td>
    Endereço MAC (Controle de Acesso à Mídia) (formato EUI-64)
   </td>
  </tr>
  <tr>
   <td>
    <code>
     money
    </code>
   </td>
   <td>
   </td>
   <td>
    valor em moeda
   </td>
  </tr>
  <tr>
   <td>
    <code>
     numeric [ (
     <em class="replaceable">
      <code>
       p
      </code>
     </em>
     ,
     <em class="replaceable">
      <code>
       s
      </code>
     </em>
     ) ]
    </code>
   </td>
   <td>
    <code>
     decimal [ (
     <em class="replaceable">
      <code>
       p
      </code>
     </em>
     ,
     <em class="replaceable">
      <code>
       s
      </code>
     </em>
     ) ]
    </code>
   </td>
   <td>
    exato número de precisão selecionável
   </td>
  </tr>
  <tr>
   <td>
    <code>
     path
    </code>
   </td>
   <td>
   </td>
   <td>
    caminho geométrico em um plano
   </td>
  </tr>
  <tr>
   <td>
    <code>
     pg_lsn
    </code>
   </td>
   <td>
   </td>
   <td>
    <span class="productname">
     PostgreSQL
    </span>
    Número de sequência do log
   </td>
  </tr>
  <tr>
   <td>
    <code>
     pg_snapshot
    </code>
   </td>
   <td>
   </td>
   <td>
    instantâneo do ID de transação de nível de usuário
   </td>
  </tr>
  <tr>
   <td>
    <code>
     point
    </code>
   </td>
   <td>
   </td>
   <td>
    ponto geométrico em um plano
   </td>
  </tr>
  <tr>
   <td>
    <code>
     polygon
    </code>
   </td>
   <td>
   </td>
   <td>
    caminho geométrico fechado em um plano
   </td>
  </tr>
  <tr>
   <td>
    <code>
     real
    </code>
   </td>
   <td>
    <code>
     float4
    </code>
   </td>
   <td>
    número de ponto flutuante de precisão única (4 bytes)
   </td>
  </tr>
  <tr>
   <td>
    <code>
     smallint
    </code>
   </td>
   <td>
    <code>
     int2
    </code>
   </td>
   <td>
    inteiro de dois bytes
   </td>
  </tr>
  <tr>
   <td>
    <code>
     smallserial
    </code>
   </td>
   <td>
    <code>
     serial2
    </code>
   </td>
   <td>
    autoincrementado inteiro de dois bytes
   </td>
  </tr>
  <tr>
   <td>
    <code>
     serial
    </code>
   </td>
   <td>
    <code>
     serial4
    </code>
   </td>
   <td>
    autoincrementado inteiro de quatro bytes
   </td>
  </tr>
  <tr>
   <td>
    <code>
     text
    </code>
   </td>
   <td>
   </td>
   <td>
    string de caracteres de comprimento variável
   </td>
  </tr>
  <tr>
   <td>
    <code>
     time [ (
     <em class="replaceable">
      <code>
       p
      </code>
     </em>
     ) ] [ without time zone ]
    </code>
   </td>
   <td>
   </td>
   <td>
    hora do dia (sem fuso horário)
   </td>
  </tr>
  <tr>
   <td>
    <code>
     time [ (
     <em class="replaceable">
      <code>
       p
      </code>
     </em>
     ) ] with time zone
    </code>
   </td>
   <td>
    <code>
     timetz
    </code>
   </td>
   <td>
    hora do dia, incluindo fuso horário
   </td>
  </tr>
  <tr>
   <td>
    <code>
     timestamp [ (
     <em class="replaceable">
      <code>
       p
      </code>
     </em>
     ) ] [ without time zone ]
    </code>
   </td>
   <td>
   </td>
   <td>
    data e hora (sem fuso horário)
   </td>
  </tr>
  <tr>
   <td>
    <code>
     timestamp [ (
     <em class="replaceable">
      <code>
       p
      </code>
     </em>
     ) ] with time zone
    </code>
   </td>
   <td>
    <code>
     timestamptz
    </code>
   </td>
   <td>
    data e hora, incluindo fuso horário
   </td>
  </tr>
  <tr>
   <td>
    <code>
     tsquery
    </code>
   </td>
   <td>
   </td>
   <td>
    consulta de pesquisa de texto
   </td>
  </tr>
  <tr>
   <td>
    <code>
     tsvector
    </code>
   </td>
   <td>
   </td>
   <td>
    texto de busca de documentos
   </td>
  </tr>
  <tr>
   <td>
    <code>
     txid_snapshot
    </code>
   </td>
   <td>
   </td>
   <td>
    instantâneo do ID de transação de nível de usuário (desatualizado; veja
    <code>
     pg_snapshot
    </code>
    )
   </td>
  </tr>
  <tr>
   <td>
    <code>
     uuid
    </code>
   </td>
   <td>
   </td>
   <td>
    identificador universalmente único
   </td>
  </tr>
  <tr>
   <td>
    <code>
     xml
    </code>
   </td>
   <td>
   </td>
   <td>
    Dados XML
   </td>
  </tr>
 </tbody>
</table>

#### Compatibilidade

Os seguintes tipos (ou suas ortografias) são especificados pelo SQL: `bigint`, `bit`, `bit varying`, `boolean`, `char`, `character varying`, `character`, `varchar`, `date`, `double precision`, `integer`, `interval`, `numeric`, `decimal`, `real`, `smallint`, `time` (com ou sem fuso horário), `timestamp` (com ou sem fuso horário), `xml`.

Cada tipo de dado tem uma representação externa determinada por suas funções de entrada e saída. Muitos dos tipos embutidos têm formatos externos óbvios. No entanto, vários tipos são exclusivos do PostgreSQL, como caminhos geométricos, ou têm vários formatos possíveis, como os tipos de data e hora. Algumas das funções de entrada e saída não são inversíveis, ou seja, o resultado de uma função de saída pode perder precisão quando comparado ao input original.