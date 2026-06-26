### 9.5. Funções e operadores de string binária [#](#FUNCTIONS-BINARYSTRING)

Esta seção descreve funções e operadores para examinar e manipular strings binárias, ou seja, valores do tipo `bytea`. Muitas dessas funções são equivalentes, em propósito e sintaxe, às funções de string de texto descritas na seção anterior.

O SQL define algumas funções de string que utilizam palavras-chave, em vez de vírgulas, para separar os argumentos. Os detalhes estão em [Tabela 9.11](functions-binarystring.md#FUNCTIONS-BINARYSTRING-SQL). O PostgreSQL também fornece versões dessas funções que utilizam a sintaxe de invocação de função regular (consulte [Tabela 9.12](functions-binarystring.md#FUNCTIONS-BINARYSTRING-OTHER)).

**Tabela 9.11. Funções e operadores de cadeia binária SQL**

<table>
 <colgroup>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th class="func_table_entry">
    <p class="func_signature">
     Function/Operator
    </p>
    <p>
     Description
    </p>
    <p>
     Example(s)
    </p>
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      bytea
     </code>
     <code>
      ||
     </code>
     <code>
      bytea
     </code>
     →
     <code>
      bytea
     </code>
    </p>
    <p>
     Concatenates the two binary strings.
    </p>
    <p>
     <code>
      '\x123456'::bytea || '\x789a00bcde'::bytea
     </code>
     →
     <code>
      \x123456789a00bcde
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      bit_length
     </code>
     (
     <code>
      bytea
     </code>
     ) →
     <code>
      integer
     </code>
    </p>
    <p>
     Returns number of bits in the binary string (8 times the
     <code>
      octet_length
     </code>
     ).
    </p>
    <p>
     <code>
      bit_length('\x123456'::bytea)
     </code>
     →
     <code>
      24
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      btrim
     </code>
     (
     <em class="parameter">
      <code>
       bytes
      </code>
     </em>
     <code>
      bytea
     </code>
     ,
     <em class="parameter">
      <code>
       bytesremoved
      </code>
     </em>
     <code>
      bytea
     </code>
     ) →
     <code>
      bytea
     </code>
    </p>
    <p>
     Removes the longest string containing only bytes appearing in
     <em class="parameter">
      <code>
       bytesremoved
      </code>
     </em>
     from the start and end of
     <em class="parameter">
      <code>
       bytes
      </code>
     </em>
     .
    </p>
    <p>
     <code>
      btrim('\x1234567890'::bytea, '\x9012'::bytea)
     </code>
     →
     <code>
      \x345678
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      ltrim
     </code>
     (
     <em class="parameter">
      <code>
       bytes
      </code>
     </em>
     <code>
      bytea
     </code>
     ,
     <em class="parameter">
      <code>
       bytesremoved
      </code>
     </em>
     <code>
      bytea
     </code>
     ) →
     <code>
      bytea
     </code>
    </p>
    <p>
     Removes the longest string containing only bytes appearing in
     <em class="parameter">
      <code>
       bytesremoved
      </code>
     </em>
     from the start of
     <em class="parameter">
      <code>
       bytes
      </code>
     </em>
     .
    </p>
    <p>
     <code>
      ltrim('\x1234567890'::bytea, '\x9012'::bytea)
     </code>
     →
     <code>
      \x34567890
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      octet_length
     </code>
     (
     <code>
      bytea
     </code>
     ) →
     <code>
      integer
     </code>
    </p>
    <p>
     Returns number of bytes in the binary string.
    </p>
    <p>
     <code>
      octet_length('\x123456'::bytea)
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
      overlay
     </code>
     (
     <em class="parameter">
      <code>
       bytes
      </code>
     </em>
     <code>
      bytea
     </code>
     <code>
      PLACING
     </code>
     <em class="parameter">
      <code>
       newsubstring
      </code>
     </em>
     <code>
      bytea
     </code>
     <code>
      FROM
     </code>
     <em class="parameter">
      <code>
       start
      </code>
     </em>
     <code>
      integer
     </code>
     [
     <span class="optional">
      <code>
       FOR
      </code>
      <em class="parameter">
       <code>
        count
       </code>
      </em>
      <code>
       integer
      </code>
     </span>
     ] ) →
     <code>
      bytea
     </code>
    </p>
    <p>
     Replaces the substring of
     <em class="parameter">
      <code>
       bytes
      </code>
     </em>
     that starts at the
     <em class="parameter">
      <code>
       start
      </code>
     </em>
     'th byte and extends for
     <em class="parameter">
      <code>
       count
      </code>
     </em>
     bytes with
     <em class="parameter">
      <code>
       newsubstring
      </code>
     </em>
     . If
     <em class="parameter">
      <code>
       count
      </code>
     </em>
     is omitted, it defaults to the length of
     <em class="parameter">
      <code>
       newsubstring
      </code>
     </em>
     .
    </p>
    <p>
     <code>
      overlay('\x1234567890'::bytea placing '\002\003'::bytea from 2 for 3)
     </code>
     →
     <code>
      \x12020390
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      position
     </code>
     (
     <em class="parameter">
      <code>
       substring
      </code>
     </em>
     <code>
      bytea
     </code>
     <code>
      IN
     </code>
     <em class="parameter">
      <code>
       bytes
      </code>
     </em>
     <code>
      bytea
     </code>
     ) →
     <code>
      integer
     </code>
    </p>
    <p>
     Returns first starting index of the specified
     <em class="parameter">
      <code>
       substring
      </code>
     </em>
     within
     <em class="parameter">
      <code>
       bytes
      </code>
     </em>
     , or zero if it's not present.
    </p>
    <p>
     <code>
      position('\x5678'::bytea in '\x1234567890'::bytea)
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
      rtrim
     </code>
     (
     <em class="parameter">
      <code>
       bytes
      </code>
     </em>
     <code>
      bytea
     </code>
     ,
     <em class="parameter">
      <code>
       bytesremoved
      </code>
     </em>
     <code>
      bytea
     </code>
     ) →
     <code>
      bytea
     </code>
    </p>
    <p>
     Removes the longest string containing only bytes appearing in
     <em class="parameter">
      <code>
       bytesremoved
      </code>
     </em>
     from the end of
     <em class="parameter">
      <code>
       bytes
      </code>
     </em>
     .
    </p>
    <p>
     <code>
      rtrim('\x1234567890'::bytea, '\x9012'::bytea)
     </code>
     →
     <code>
      \x12345678
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      substring
     </code>
     (
     <em class="parameter">
      <code>
       bytes
      </code>
     </em>
     <code>
      bytea
     </code>
     [
     <span class="optional">
      <code>
       FROM
      </code>
      <em class="parameter">
       <code>
        start
       </code>
      </em>
      <code>
       integer
      </code>
     </span>
     ] [
     <span class="optional">
      <code>
       FOR
      </code>
      <em class="parameter">
       <code>
        count
       </code>
      </em>
      <code>
       integer
      </code>
     </span>
     ] ) →
     <code>
      bytea
     </code>
    </p>
    <p>
     Extracts the substring of
     <em class="parameter">
      <code>
       bytes
      </code>
     </em>
     starting at the
     <em class="parameter">
      <code>
       start
      </code>
     </em>
     'th byte if that is specified, and stopping after
     <em class="parameter">
      <code>
       count
      </code>
     </em>
     bytes if that is specified.  Provide at least one of
     <em class="parameter">
      <code>
       start
      </code>
     </em>
     and
     <em class="parameter">
      <code>
       count
      </code>
     </em>
     .
    </p>
    <p>
     <code>
      substring('\x1234567890'::bytea from 3 for 2)
     </code>
     →
     <code>
      \x5678
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      trim
     </code>
     ( [
     <span class="optional">
      <code>
       LEADING
      </code>
      |
      <code>
       TRAILING
      </code>
      |
      <code>
       BOTH
      </code>
     </span>
     ]
     <em class="parameter">
      <code>
       bytesremoved
      </code>
     </em>
     <code>
      bytea
     </code>
     <code>
      FROM
     </code>
     <em class="parameter">
      <code>
       bytes
      </code>
     </em>
     <code>
      bytea
     </code>
     ) →
     <code>
      bytea
     </code>
    </p>
    <p>
     Removes the longest string containing only bytes appearing in
     <em class="parameter">
      <code>
       bytesremoved
      </code>
     </em>
     from the start, end, or both ends (
     <code>
      BOTH
     </code>
     is the default) of
     <em class="parameter">
      <code>
       bytes
      </code>
     </em>
     .
    </p>
    <p>
     <code>
      trim('\x9012'::bytea from '\x1234567890'::bytea)
     </code>
     →
     <code>
      \x345678
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      trim
     </code>
     ( [
     <span class="optional">
      <code>
       LEADING
      </code>
      |
      <code>
       TRAILING
      </code>
      |
      <code>
       BOTH
      </code>
     </span>
     ] [
     <span class="optional">
      <code>
       FROM
      </code>
     </span>
     ]
     <em class="parameter">
      <code>
       bytes
      </code>
     </em>
     <code>
      bytea
     </code>
     ,
     <em class="parameter">
      <code>
       bytesremoved
      </code>
     </em>
     <code>
      bytea
     </code>
     ) →
     <code>
      bytea
     </code>
    </p>
    <p>
     This is a non-standard syntax for
     <code>
      trim()
     </code>
     .
    </p>
    <p>
     <code>
      trim(both from '\x1234567890'::bytea, '\x9012'::bytea)
     </code>
     →
     <code>
      \x345678
     </code>
    </p>
   </td>
  </tr>
 </tbody>
</table>

Funções adicionais de manipulação de strings binárias estão disponíveis e estão listadas em [Tabela 9.12](functions-binarystring.md#FUNCTIONS-BINARYSTRING-OTHER). Algumas delas são usadas internamente para implementar as funções de string padrão do SQL listadas em [Tabela 9.11](functions-binarystring.md#FUNCTIONS-BINARYSTRING-SQL).

**Tabela 9.12. Outras funções de string binária**

<table>
 <colgroup>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th class="func_table_entry">
    <p class="func_signature">
     Function
    </p>
    <p>
     Description
    </p>
    <p>
     Example(s)
    </p>
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      bit_count
     </code>
     (
     <em class="parameter">
      <code>
       bytes
      </code>
     </em>
     <code>
      bytea
     </code>
     ) →
     <code>
      bigint
     </code>
    </p>
    <p>
     Returns the number of bits set in the binary string (also known as
     <span class="quote">
      “
      <span class="quote">
       popcount
      </span>
      ”
     </span>
     ).
    </p>
    <p>
     <code>
      bit_count('\x1234567890'::bytea)
     </code>
     →
     <code>
      15
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      crc32
     </code>
     (
     <code>
      bytea
     </code>
     ) →
     <code>
      bigint
     </code>
    </p>
    <p>
     Computes the CRC-32 value of the binary string.
    </p>
    <p>
     <code>
      crc32('abc'::bytea)
     </code>
     →
     <code>
      891568578
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      crc32c
     </code>
     (
     <code>
      bytea
     </code>
     ) →
     <code>
      bigint
     </code>
    </p>
    <p>
     Computes the CRC-32C value of the binary string.
    </p>
    <p>
     <code>
      crc32c('abc'::bytea)
     </code>
     →
     <code>
      910901175
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      get_bit
     </code>
     (
     <em class="parameter">
      <code>
       bytes
      </code>
     </em>
     <code>
      bytea
     </code>
     ,
     <em class="parameter">
      <code>
       n
      </code>
     </em>
     <code>
      bigint
     </code>
     ) →
     <code>
      integer
     </code>
    </p>
    <p>
     Extracts
     <a class="link" href="functions-binarystring.md#FUNCTIONS-ZEROBASED-NOTE">
      n'th
     </a>
     bit from binary string.
    </p>
    <p>
     <code>
      get_bit('\x1234567890'::bytea, 30)
     </code>
     →
     <code>
      1
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      get_byte
     </code>
     (
     <em class="parameter">
      <code>
       bytes
      </code>
     </em>
     <code>
      bytea
     </code>
     ,
     <em class="parameter">
      <code>
       n
      </code>
     </em>
     <code>
      integer
     </code>
     ) →
     <code>
      integer
     </code>
    </p>
    <p>
     Extracts
     <a class="link" href="functions-binarystring.md#FUNCTIONS-ZEROBASED-NOTE">
      n'th
     </a>
     byte from binary string.
    </p>
    <p>
     <code>
      get_byte('\x1234567890'::bytea, 4)
     </code>
     →
     <code>
      144
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      length
     </code>
     (
     <code>
      bytea
     </code>
     ) →
     <code>
      integer
     </code>
    </p>
    <p>
     Returns the number of bytes in the binary string.
    </p>
    <p>
     <code>
      length('\x1234567890'::bytea)
     </code>
     →
     <code>
      5
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      length
     </code>
     (
     <em class="parameter">
      <code>
       bytes
      </code>
     </em>
     <code>
      bytea
     </code>
     ,
     <em class="parameter">
      <code>
       encoding
      </code>
     </em>
     <code>
      name
     </code>
     ) →
     <code>
      integer
     </code>
    </p>
    <p>
     Returns the number of characters in the binary string, assuming that it is text in the given
     <em class="parameter">
      <code>
       encoding
      </code>
     </em>
     .
    </p>
    <p>
     <code>
      length('jose'::bytea, 'UTF8')
     </code>
     →
     <code>
      4
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      md5
     </code>
     (
     <code>
      bytea
     </code>
     ) →
     <code>
      text
     </code>
    </p>
    <p>
     Computes the MD5
     <a class="link" href="functions-binarystring.md#FUNCTIONS-HASH-NOTE">
      hash
     </a>
     of the binary string, with the result written in hexadecimal.
    </p>
    <p>
     <code>
      md5('Th\000omas'::bytea)
     </code>
     →
     <code>
      8ab2d3c9689aaf18​b4958c334c82d8b1
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      reverse
     </code>
     (
     <code>
      bytea
     </code>
     ) →
     <code>
      bytea
     </code>
    </p>
    <p>
     Reverses the order of the bytes in the binary string.
    </p>
    <p>
     <code>
      reverse('\xabcd'::bytea)
     </code>
     →
     <code>
      \xcdab
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      set_bit
     </code>
     (
     <em class="parameter">
      <code>
       bytes
      </code>
     </em>
     <code>
      bytea
     </code>
     ,
     <em class="parameter">
      <code>
       n
      </code>
     </em>
     <code>
      bigint
     </code>
     ,
     <em class="parameter">
      <code>
       newvalue
      </code>
     </em>
     <code>
      integer
     </code>
     ) →
     <code>
      bytea
     </code>
    </p>
    <p>
     Sets
     <a class="link" href="functions-binarystring.md#FUNCTIONS-ZEROBASED-NOTE">
      n'th
     </a>
     bit in binary string to
     <em class="parameter">
      <code>
       newvalue
      </code>
     </em>
     .
    </p>
    <p>
     <code>
      set_bit('\x1234567890'::bytea, 30, 0)
     </code>
     →
     <code>
      \x1234563890
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      set_byte
     </code>
     (
     <em class="parameter">
      <code>
       bytes
      </code>
     </em>
     <code>
      bytea
     </code>
     ,
     <em class="parameter">
      <code>
       n
      </code>
     </em>
     <code>
      integer
     </code>
     ,
     <em class="parameter">
      <code>
       newvalue
      </code>
     </em>
     <code>
      integer
     </code>
     ) →
     <code>
      bytea
     </code>
    </p>
    <p>
     Sets
     <a class="link" href="functions-binarystring.md#FUNCTIONS-ZEROBASED-NOTE">
      n'th
     </a>
     byte in binary string to
     <em class="parameter">
      <code>
       newvalue
      </code>
     </em>
     .
    </p>
    <p>
     <code>
      set_byte('\x1234567890'::bytea, 4, 64)
     </code>
     →
     <code>
      \x1234567840
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      sha224
     </code>
     (
     <code>
      bytea
     </code>
     ) →
     <code>
      bytea
     </code>
    </p>
    <p>
     Computes the SHA-224
     <a class="link" href="functions-binarystring.md#FUNCTIONS-HASH-NOTE">
      hash
     </a>
     of the binary string.
    </p>
    <p>
     <code>
      sha224('abc'::bytea)
     </code>
     →
     <code>
      \x23097d223405d8228642a477bda2​55b32aadbce4bda0b3f7e36c9da7
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      sha256
     </code>
     (
     <code>
      bytea
     </code>
     ) →
     <code>
      bytea
     </code>
    </p>
    <p>
     Computes the SHA-256
     <a class="link" href="functions-binarystring.md#FUNCTIONS-HASH-NOTE">
      hash
     </a>
     of the binary string.
    </p>
    <p>
     <code>
      sha256('abc'::bytea)
     </code>
     →
     <code>
      \xba7816bf8f01cfea414140de5dae2223​b00361a396177a9cb410ff61f20015ad
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      sha384
     </code>
     (
     <code>
      bytea
     </code>
     ) →
     <code>
      bytea
     </code>
    </p>
    <p>
     Computes the SHA-384
     <a class="link" href="functions-binarystring.md#FUNCTIONS-HASH-NOTE">
      hash
     </a>
     of the binary string.
    </p>
    <p>
     <code>
      sha384('abc'::bytea)
     </code>
     →
     <code>
      \xcb00753f45a35e8bb5a03d699ac65007​272c32ab0eded1631a8b605a43ff5bed​8086072ba1e7cc2358baeca134c825a7
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      sha512
     </code>
     (
     <code>
      bytea
     </code>
     ) →
     <code>
      bytea
     </code>
    </p>
    <p>
     Computes the SHA-512
     <a class="link" href="functions-binarystring.md#FUNCTIONS-HASH-NOTE">
      hash
     </a>
     of the binary string.
    </p>
    <p>
     <code>
      sha512('abc'::bytea)
     </code>
     →
     <code>
      \xddaf35a193617abacc417349ae204131​12e6fa4e89a97ea20a9eeee64b55d39a​2192992a274fc1a836ba3c23a3feebbd​454d4423643ce80e2a9ac94fa54ca49f
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      substr
     </code>
     (
     <em class="parameter">
      <code>
       bytes
      </code>
     </em>
     <code>
      bytea
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
     [
     <span class="optional">
      ,
      <em class="parameter">
       <code>
        count
       </code>
      </em>
      <code>
       integer
      </code>
     </span>
     ] ) →
     <code>
      bytea
     </code>
    </p>
    <p>
     Extracts the substring of
     <em class="parameter">
      <code>
       bytes
      </code>
     </em>
     starting at the
     <em class="parameter">
      <code>
       start
      </code>
     </em>
     'th byte, and extending for
     <em class="parameter">
      <code>
       count
      </code>
     </em>
     bytes if that is specified.  (Same as
     <code>
      substring(
      <em class="parameter">
       <code>
        bytes
       </code>
      </em>
      from
      <em class="parameter">
       <code>
        start
       </code>
      </em>
      for
      <em class="parameter">
       <code>
        count
       </code>
      </em>
      )
     </code>
     .)
    </p>
    <p>
     <code>
      substr('\x1234567890'::bytea, 3, 2)
     </code>
     →
     <code>
      \x5678
     </code>
    </p>
   </td>
  </tr>
 </tbody>
</table>

As funções `get_byte` e `set_byte` numeram o primeiro byte de uma string binária como byte 0. As funções `get_bit` e `set_bit` numeram bits da direita para a esquerda em cada byte; por exemplo, o bit 0 é o bit menos significativo do primeiro byte, e o bit 15 é o bit mais significativo do segundo byte.

Por razões históricas, a função `md5` retorna um valor codificado em hexadecimal do tipo `text`, enquanto as funções SHA-2 retornam do tipo `bytea`. Use as funções `encode`(functions-binarystring.md#FUNCTION-ENCODE) e `decode`(functions-binarystring.md#FUNCTION-DECODE) para converter entre os dois. Por exemplo, escreva `encode(sha256('abc'), 'hex')` para obter uma representação de texto codificada em hexadecimal, ou `decode(md5('abc'), 'hex')` para obter um valor de `bytea`.

As funções para converter strings entre diferentes conjuntos de caracteres (códigos de codificação) e para representar dados binários arbitrários em forma textual são mostradas em [Tabela 9.13](functions-binarystring.md#FUNCTIONS-BINARYSTRING-CONVERSIONS). Para essas funções, um argumento ou resultado do tipo `text` é expresso no codificação padrão do banco de dados, enquanto argumentos ou resultados do tipo `bytea` estão em um codificação nomeada por outro argumento.

**Tabela 9.13. Funções de conversão de string de texto/binária**

<table>
 <colgroup>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th class="func_table_entry">
    <p class="func_signature">
     Function
    </p>
    <p>
     Description
    </p>
    <p>
     Example(s)
    </p>
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      convert
     </code>
     (
     <em class="parameter">
      <code>
       bytes
      </code>
     </em>
     <code>
      bytea
     </code>
     ,
     <em class="parameter">
      <code>
       src_encoding
      </code>
     </em>
     <code>
      name
     </code>
     ,
     <em class="parameter">
      <code>
       dest_encoding
      </code>
     </em>
     <code>
      name
     </code>
     ) →
     <code>
      bytea
     </code>
    </p>
    <p>
     Converts a binary string representing text in encoding
     <em class="parameter">
      <code>
       src_encoding
      </code>
     </em>
     to a binary string in encoding
     <em class="parameter">
      <code>
       dest_encoding
      </code>
     </em>
     (see
     <a class="xref" href="multibyte.md#MULTIBYTE-CONVERSIONS-SUPPORTED" title="23.3.4. Available Character Set Conversions">
      Section 23.3.4
     </a>
     for available conversions).
    </p>
    <p>
     <code>
      convert('text_in_utf8', 'UTF8', 'LATIN1')
     </code>
     →
     <code>
      \x746578745f696e5f75746638
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      convert_from
     </code>
     (
     <em class="parameter">
      <code>
       bytes
      </code>
     </em>
     <code>
      bytea
     </code>
     ,
     <em class="parameter">
      <code>
       src_encoding
      </code>
     </em>
     <code>
      name
     </code>
     ) →
     <code>
      text
     </code>
    </p>
    <p>
     Converts a binary string representing text in encoding
     <em class="parameter">
      <code>
       src_encoding
      </code>
     </em>
     to
     <code>
      text
     </code>
     in the database encoding (see
     <a class="xref" href="multibyte.md#MULTIBYTE-CONVERSIONS-SUPPORTED" title="23.3.4. Available Character Set Conversions">
      Section 23.3.4
     </a>
     for available conversions).
    </p>
    <p>
     <code>
      convert_from('text_in_utf8', 'UTF8')
     </code>
     →
     <code>
      text_in_utf8
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      convert_to
     </code>
     (
     <em class="parameter">
      <code>
       string
      </code>
     </em>
     <code>
      text
     </code>
     ,
     <em class="parameter">
      <code>
       dest_encoding
      </code>
     </em>
     <code>
      name
     </code>
     ) →
     <code>
      bytea
     </code>
    </p>
    <p>
     Converts a
     <code>
      text
     </code>
     string (in the database encoding) to a binary string encoded in encoding
     <em class="parameter">
      <code>
       dest_encoding
      </code>
     </em>
     (see
     <a class="xref" href="multibyte.md#MULTIBYTE-CONVERSIONS-SUPPORTED" title="23.3.4. Available Character Set Conversions">
      Section 23.3.4
     </a>
     for available conversions).
    </p>
    <p>
     <code>
      convert_to('some_text', 'UTF8')
     </code>
     →
     <code>
      \x736f6d655f74657874
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      encode
     </code>
     (
     <em class="parameter">
      <code>
       bytes
      </code>
     </em>
     <code>
      bytea
     </code>
     ,
     <em class="parameter">
      <code>
       format
      </code>
     </em>
     <code>
      text
     </code>
     ) →
     <code>
      text
     </code>
    </p>
    <p>
     Encodes binary data into a textual representation; supported
     <em class="parameter">
      <code>
       format
      </code>
     </em>
     values are:
     <a class="link" href="functions-binarystring.md#ENCODE-FORMAT-BASE64">
      <code>
       base64
      </code>
     </a>
     ,
     <a class="link" href="functions-binarystring.md#ENCODE-FORMAT-ESCAPE">
      <code>
       escape
      </code>
     </a>
     ,
     <a class="link" href="functions-binarystring.md#ENCODE-FORMAT-HEX">
      <code>
       hex
      </code>
     </a>
     .
    </p>
    <p>
     <code>
      encode('123\000\001', 'base64')
     </code>
     →
     <code>
      MTIzAAE=
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      decode
     </code>
     (
     <em class="parameter">
      <code>
       string
      </code>
     </em>
     <code>
      text
     </code>
     ,
     <em class="parameter">
      <code>
       format
      </code>
     </em>
     <code>
      text
     </code>
     ) →
     <code>
      bytea
     </code>
    </p>
    <p>
     Decodes binary data from a textual representation; supported
     <em class="parameter">
      <code>
       format
      </code>
     </em>
     values are the same as for
     <code>
      encode
     </code>
     .
    </p>
    <p>
     <code>
      decode('MTIzAAE=', 'base64')
     </code>
     →
     <code>
      \x3132330001
     </code>
    </p>
   </td>
  </tr>
 </tbody>
</table>

As funções `encode` e `decode` suportam os seguintes formatos textuais:

base64 [#](#ENCODE-FORMAT-BASE64): O formato `base64` é o da [RFC 2045 Seção 6.8](https://datatracker.ietf.org/doc/html/rfc2045#section-6.8). De acordo com o RFC, as linhas codificadas são quebradas em 76 caracteres. No entanto, em vez do marcador de fim de linha MIME CRLF, apenas uma nova linha é usada para o fim de linha. A função `decode` ignora os caracteres de retorno de carro, nova linha, espaço e tabulação. Caso contrário, um erro é exibido quando o `decode` é fornecido dados inválidos de base64 — incluindo quando o preenchimento final é incorreto.

escape [#](#ENCODE-FORMAT-ESCAPE): O formato `escape` converte bytes nulos e bytes com o bit alto definido em sequências de escape octal (`\`*`nnn`*), e duplica barras invertidas. Outros valores de byte são representados literalmente. A função `decode` levantará um erro se uma barra invertida não for seguida por uma segunda barra invertida ou três dígitos octal; ela aceita outros valores de byte inalterados.

hex [#](#ENCODE-FORMAT-HEX): O formato `hex` representa cada 4 bits de dados como um dígito hexadecimal, `0` a `f`, escrevendo primeiro o dígito de ordem superior de cada byte. A função `encode` emite os dígitos hex `a`-`f` em minúsculas. Como a menor unidade de dados é de 8 bits, sempre há um número par de caracteres retornados por `encode`. A função `decode` aceita os caracteres `a`-`f` em maiúsculas ou minúsculas. Um erro é exibido quando `decode` é fornecido dados hex inválidos — incluindo quando fornecido um número ímpar de caracteres.

Além disso, é possível converter valores inteiros para e a partir do tipo `bytea`. A conversão de um inteiro para `bytea` produz 2, 4 ou 8 bytes, dependendo da largura do tipo de inteiro. O resultado é a representação de complemento de dois do inteiro, com o byte mais significativo primeiro. Alguns exemplos:

```sql
1234::smallint::bytea          \x04d2
cast(1234 as bytea)            \x000004d2
cast(-1234 as bytea)           \xfffffb2e
'\x8000'::bytea::smallint      -32768
'\x8000'::bytea::integer       32768
```

A conversão de um `bytea` para um inteiro gerará um erro se o comprimento do `bytea` exceder a largura do tipo inteiro.

Veja também a função agregada `string_agg` em [Seção 9.21](functions-aggregate.md "9.21. Aggregate Functions") e as funções de grande objeto em [Seção 33.4](lo-funcs.md "33.4. Server-Side Functions").