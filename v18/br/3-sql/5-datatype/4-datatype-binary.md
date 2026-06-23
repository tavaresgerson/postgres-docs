## 8.4. Tipos de dados binários [#](#DATATYPE-BINARY)

* [8.4.1. `bytea` Hex Format](datatype-binary.md#DATATYPE-BINARY-BYTEA-HEX-FORMAT)
* [8.4.2. `bytea` Formato de Escape](datatype-binary.md#DATATYPE-BINARY-BYTEA-ESCAPE-FORMAT)

O tipo de dados `bytea` permite o armazenamento de cadeias binárias; veja [Tabela 8.6](datatype-binary.md#DATATYPE-BINARY-TABLE).

**Tabela 8.6. Tipos de dados binários**



<table border="1" class="table" summary="Binary Data Types">
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
    Tamanho de armazenamento
   </th>
   <th>
    Description
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <code class="type">
     bytea
    </code>
   </td>
   <td>
    1 ou 4 bytes mais a própria string binária
   </td>
   <td>
    variable-length binary string
   </td>
  </tr>
 </tbody>
</table>










Uma string binária é uma sequência de octetos (ou bytes). As strings binárias se distinguem das strings de caracteres em dois modos. Primeiro, as strings binárias permitem especificamente armazenar octetos de valor zero e outros octetos “não imprimíveis” (geralmente, octetos fora do intervalo decimal de 32 a 126). As strings de caracteres não permitem octetos zero e também não permitem quaisquer outros valores de octeto e sequências de valores de octeto que sejam inválidos de acordo com o conjunto de caracteres de codificação selecionado pelo banco de dados. Em segundo lugar, as operações em strings binárias processam os bytes reais, enquanto o processamento de strings de caracteres depende das configurações do local. Em resumo, as strings binárias são apropriadas para armazenar dados que o programador considera como “bytes brutos”, enquanto as strings de caracteres são apropriadas para armazenar texto.

O tipo `bytea` suporta dois formatos para entrada e saída: o formato "hex" e o histórico formato "escape" do PostgreSQL. Ambos são sempre aceitos na entrada. O formato de saída depende do parâmetro de configuração [bytea_output](runtime-config-client.md#GUC-BYTEA-OUTPUT); o padrão é hex. (Observe que o formato hex foi introduzido no PostgreSQL 9.0; versões anteriores e algumas ferramentas não o entendem.)

O padrão SQL define um tipo de string binária diferente, chamado `BLOB` ou `BINARY LARGE OBJECT`. O formato de entrada é diferente do `bytea`, mas as funções e operadores fornecidos são na maioria dos casos os mesmos.

### 8.4.1. `bytea` Hex Format [#](#DATATYPE-BINARY-BYTEA-HEX-FORMAT)

O formato “hex” codifica dados binários como 2 dígitos hexadecimais por byte, com o nibble mais significativo primeiro. A sequência inteira é precedida pela sequência `\x` (para distingui-la do formato de fuga). Em alguns contextos, o traço inicial inicial pode precisar ser escamado dobrando-o (ver [Seção 4.1.2.1](sql-syntax-lexical.md#SQL-SYNTAX-STRINGS)). Para entrada, os dígitos hexadecimais podem ser maiúsculos ou minúsculos, e espaços em branco são permitidos entre pares de dígitos (mas não dentro de um par de dígitos nem na sequência inicial `\x`). O formato hex é compatível com uma ampla gama de aplicações e protocolos externos, e tende a ser mais rápido de converter do que o formato de fuga, portanto, seu uso é preferido.

Exemplo:

```
SET bytea_output = 'hex';

SELECT '\xDEADBEEF'::bytea;
   bytea
------------
 \xdeadbeef
```

### 8.4.2. `bytea` Formato de fuga [#](#DATATYPE-BINARY-BYTEA-ESCAPE-FORMAT)

O formato “escape” é o formato tradicional do PostgreSQL para o tipo `bytea`. Ele adota a abordagem de representar uma string binária como uma sequência de caracteres ASCII, enquanto converte os bytes que não podem ser representados como um caractere ASCII em sequências de escape especiais. Se, do ponto de vista da aplicação, representar bytes como caracteres faz sentido, então essa representação pode ser conveniente. Mas, na prática, geralmente é confuso porque confunde a distinção entre strings binárias e strings de caracteres, e também o mecanismo de escape específico escolhido é um tanto complicado. Portanto, esse formato provavelmente deve ser evitado para a maioria das novas aplicações.

Ao inserir valores de `bytea` em formato de escape, os octetos de certos valores *devem* ser escapados, enquanto todos os valores de octeto *podem* ser escapados. Em geral, para escapar um octeto, converta-o em seu valor octal de três dígitos e preceda-o com uma barra invertida. A própria barra invertida (valor decimal de octeto 92) pode ser representada alternativamente por barras duplas. [Tabela 8.7](datatype-binary.md#DATATYPE-BINARY-SQLESC) mostra os caracteres que devem ser escapados e fornece as sequências de escape alternativas, quando aplicável.

**Tabela 8.7. Octetos Literais Escapados `bytea`**



<table border="1" class="table" summary="bytea Literal Escaped Octets">
 <colgroup>
  <col class="col1"/>
  <col class="col2"/>
  <col class="col3"/>
  <col class="col4"/>
  <col class="col5"/>
 </colgroup>
 <thead>
  <tr>
   <th>
    Valor de oitava decimal
   </th>
   <th>
    Description
   </th>
   <th>
    Escaped Input Representation
   </th>
   <th>
    Example
   </th>
   <th>
    Hex Representation
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    0
   </td>
   <td>
    zero octet
   </td>
   <td>
    <code class="literal">
     '\000'
    </code>
   </td>
   <td>
    <code class="literal">
     '\000'::bytea
    </code>
   </td>
   <td>
    <code class="literal">
     \x00
    </code>
   </td>
  </tr>
  <tr>
   <td>
    39
   </td>
   <td>
    single quote
   </td>
   <td>
    <code class="literal">
     ''''
    </code>
    or
    <code class="literal">
     '\047'
    </code>
   </td>
   <td>
    <code class="literal">
     ''''::bytea
    </code>
   </td>
   <td>
    <code class="literal">
     \x27
    </code>
   </td>
  </tr>
  <tr>
   <td>
    92
   </td>
   <td>
    backslash
   </td>
   <td>
    <code class="literal">
     '\\'
    </code>
    or
    <code class="literal">
     '\134'
    </code>
   </td>
   <td>
    <code class="literal">
     '\\'::bytea
    </code>
   </td>
   <td>
    <code class="literal">
     \x5c
    </code>
   </td>
  </tr>
  <tr>
   <td>
    0 a 31 e 127 a 255
   </td>
   <td>
    <span class="quote">
     “
     <span class="quote">
      non-printable
     </span>
     ”
    </span>
    octets
   </td>
   <td>
    <code class="literal">
     '\
     <em class="replaceable">
      <code>
       xxx'
      </code>
     </em>
    </code>
    (octal value)
   </td>
   <td>
    <code class="literal">
     '\001'::bytea
    </code>
   </td>
   <td>
    <code class="literal">
     \x01
    </code>
   </td>
  </tr>
 </tbody>
</table>










O requisito de escapar de octaltos *não imprimíveis* varia de acordo com as configurações do local. Em alguns casos, você pode ficar com eles sem escapá-los.

A razão pela qual as aspas simples devem ser duplicadas, conforme mostrado em [Tabela 8.7](datatype-binary.md#DATATYPE-BINARY-SQLESC), é que isso é verdade para qualquer literal de string em um comando SQL. O parser genérico de literal de string consome as aspas externas e reduz qualquer par de aspas simples a um caractere de dados. O que a função de entrada `bytea` vê é apenas uma aspas simples, que ela trata como um caractere de dados simples. No entanto, a função de entrada `bytea` trata barras invertidas como especiais, e os outros comportamentos mostrados em [Tabela 8.7](datatype-binary.md#DATATYPE-BINARY-SQLESC) são implementados por essa função.

Em alguns contextos, os traços de retorno devem ser duplicados em comparação com o que é mostrado acima, porque o analisador genérico de caracteres de cadeia também reduzirá pares de traços de retorno a um caractere de dados; veja [Seção 4.1.2.1](sql-syntax-lexical.md#SQL-SYNTAX-STRINGS).

Os `Bytea` octetos são emitidos no formato `hex` por padrão. Se você alterar [bytea_output](runtime-config-client.md#GUC-BYTEA-OUTPUT) para `escape`, os octetos “não imprimíveis” são convertidos em seu valor octal equivalente de três dígitos e precedidos por uma barra invertida. A maioria dos octetos “impressíveis” é emitida por sua representação padrão no conjunto de caracteres do cliente, por exemplo:

```
SET bytea_output = 'escape';

SELECT 'abc \153\154\155 \052\251\124'::bytea;
     bytea
----------------
 abc klm *\251T
```

O octal com valor decimal 92 (barra) é duplicado na saída. Os detalhes estão em [Tabela 8.8](datatype-binary.md#DATATYPE-BINARY-RESESC).

**Tabela 8.8. Octetos de Saída Escapados `bytea`**



<table border="1" class="table" summary="bytea Output Escaped Octets">
 <colgroup>
  <col class="col1"/>
  <col class="col2"/>
  <col class="col3"/>
  <col class="col4"/>
  <col class="col5"/>
 </colgroup>
 <thead>
  <tr>
   <th>
    Valor de oitava decimal
   </th>
   <th>
    Descrição
   </th>
   <th>
    Representação de Saída Escapada
   </th>
   <th>
    Example
   </th>
   <th>
    Output Result
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    92
   </td>
   <td>
    barra invertida
   </td>
   <td>
    <code class="literal">
     \\
    </code>
   </td>
   <td>
    <code class="literal">
     '\134'::bytea
    </code>
   </td>
   <td>
    <code class="literal">
     \\
    </code>
   </td>
  </tr>
  <tr>
   <td>
    0 a 31 e 127 a 255
   </td>
   <td>
    <span class="quote">
     “
     <span class="quote">
      não imprimível
     </span>
     ”
    </span>
    oitos
   </td>
   <td>
    <code class="literal">
     \
     <em class="replaceable">
      <code>
       xxx
      </code>
     </em>
    </code>
    (valor octal)
   </td>
   <td>
    <code class="literal">
     '\001'::bytea
    </code>
   </td>
   <td>
    <code class="literal">
     \001
    </code>
   </td>
  </tr>
  <tr>
   <td>
    32 a 126
   </td>
   <td>
    <span class="quote">
     “
     <span class="quote">
      impressível
     </span>
     ”
    </span>
    oitos
   </td>
   <td>
    representação do conjunto de caracteres do cliente
   </td>
   <td>
    <code class="literal">
     '\176'::bytea
    </code>
   </td>
   <td>
    <code class="literal">
     ~
    </code>
   </td>
  </tr>
 </tbody>
</table>










Dependendo do front-end para PostgreSQL que você usa, você pode ter mais trabalho em termos de escapagem e desescapagem de strings `bytea`. Por exemplo, você também pode precisar escapar de entradas de linha e retornos de carro se sua interface as traduz automaticamente.