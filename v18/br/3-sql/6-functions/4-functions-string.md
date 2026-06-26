### 9.4. Funções e operadores de strings [#](#FUNCTIONS-STRING)

* [9.4.1. `format`](functions-string.md#FUNCTIONS-STRING-FORMAT)

Esta seção descreve funções e operadores para examinar e manipular valores de cadeia. As cadeias neste contexto incluem valores dos tipos `character`, `character varying` e `text`. Salvo indicação em contrário, estas funções e operadores são declarados para aceitar e retornar o tipo `text`. Eles aceitarão, de forma intercambiável, argumentos `character varying`. Os valores do tipo `character` serão convertidos em `text` antes da função ou operador ser aplicada, resultando na remoção de quaisquer espaços finais no valor `character`.

O SQL define algumas funções de cadeia que utilizam palavras-chave, em vez de vírgulas, para separar os argumentos. Os detalhes estão em [Tabela 9.9](functions-string.md#FUNCTIONS-STRING-SQL). O PostgreSQL também fornece versões dessas funções que utilizam a sintaxe de invocação de função regular (consulte [Tabela 9.10](functions-string.md#FUNCTIONS-STRING-OTHER)).

Nota

O operador de concatenação de strings (`||`) aceitará entrada não de tipo de string, desde que pelo menos uma entrada seja de tipo de string, conforme mostrado em [Tabela 9.9](functions-string.md#FUNCTIONS-STRING-SQL). Para outros casos, pode-se inserir uma coerção explícita para `text` para aceitar entrada não de tipo de string.

**Tabela 9.9. Funções e operadores de cadeia de caracteres SQL**

<table>
 <colgroup>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th class="func_table_entry">
    <p class="func_signature">
     Função/Operador
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
      text
     </code>
     <code>
      ||
     </code>
     <code>
      text
     </code>
     →
     <code>
      text
     </code>
    </p>
    <p>
     Concatenia as duas strings.
    </p>
    <p>
     <code>
      'Post' || 'greSQL'
     </code>
     →
     <code>
      PostgreSQL
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      text
     </code>
     <code>
      ||
     </code>
     <code>
      anynonarray
     </code>
     →
     <code>
      text
     </code>
    </p>
    <p class="func_signature">
     <code>
      anynonarray
     </code>
     <code>
      ||
     </code>
     <code>
      text
     </code>
     →
     <code>
      text
     </code>
    </p>
    <p>
     Converte a entrada não-string para texto e, em seguida, concatenia as duas strings. (A entrada não-string não pode ser de um tipo de matriz, porque isso criaria ambiguidade com a matriz
     <code>
      ||
     </code>
     operadores. Se você quiser concatenar o equivalente textual de um array, faça-o com a função cast.
     <code>
      text
     </code>
     explicitly.)
    </p>
    <p>
     <code>
      'Value: ' || 42
     </code>
     →
     <code>
      Value: 42
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
       string
      </code>
     </em>
     <code>
      text
     </code>
     [
     <span class="optional">
      ,
      <em class="parameter">
       <code>
        characters
       </code>
      </em>
      <code>
       text
      </code>
     </span>
     ] ) →
     <code>
      text
     </code>
    </p>
    <p>
     Remove a cadeia mais longa que contenha apenas caracteres
     <em class="parameter">
      <code>
       characters
      </code>
     </em>
     (um espaço por padrão) do início e do fim
     <em class="parameter">
      <code>
       string
      </code>
     </em>
     .
    </p>
    <p>
     <code>
      btrim('xyxtrimyyx', 'xyz')
     </code>
     →
     <code>
      trim
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      text
     </code>
     <code>
      IS
     </code>
     [
     <span class="optional">
      <code>
       NOT
      </code>
     </span>
     ] [
     <span class="optional">
      <em class="parameter">
       <code>
        form
       </code>
      </em>
     </span>
     ]
     <code>
      NORMALIZED
     </code>
     →
     <code>
      boolean
     </code>
    </p>
    <p>
     Verifica se a string está na forma de normalização Unicode especificada. A opção
     <em class="parameter">
      <code>
       form
      </code>
     </em>
     palavra-chave especifica o formulário:
     <code>
      NFC
     </code>
     (o padrão),
     <code>
      NFD
     </code>
     ,
     <code>
      NFKC
     </code>
     , ou
     <code>
      NFKD
     </code>
     Essa expressão só pode ser usada quando o codificação do servidor é
     <code>
      UTF8
     </code>
     Observe que verificar a normalização usando essa expressão é, muitas vezes, mais rápido do que normalizar strings que já podem estar normalizadas.
    </p>
    <p>
     <code>
      U&amp;'\0061\0308bc' IS NFD NORMALIZED
     </code>
     →
     <code>
      t
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
      text
     </code>
     )
     <code>
      integer
     </code>
    </p>
    <p>
     Retorna o número de bits na string (8 vezes o
     <code>
      octet_length
     </code>
     ).
    </p>
    <p>
     <code>
      bit_length('jose')
     </code>
     →
     <code>
      32
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      char_length
     </code>
     (
     <code>
      text
     </code>
     )
     <code>
      integer
     </code>
    </p>
    <p class="func_signature">
     <code>
      character_length
     </code>
     (
     <code>
      text
     </code>
     )
     <code>
      integer
     </code>
    </p>
    <p>
     Retorna o número de caracteres na string.
    </p>
    <p>
     <code>
      char_length('josé')
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
      lower
     </code>
     (
     <code>
      text
     </code>
     )
     <code>
      text
     </code>
    </p>
    <p>
     Converte a string para maiúsculas, de acordo com as regras do local do banco de dados.
    </p>
    <p>
     <code>
      lower('TOM')
     </code>
     →
     <code>
      tom
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      lpad
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
       length
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
        fill
       </code>
      </em>
      <code>
       text
      </code>
     </span>
     ] ) →
     <code>
      text
     </code>
    </p>
    <p>
     Amplia o
     <em class="parameter">
      <code>
       string
      </code>
     </em>
     até o comprimento
     <em class="parameter">
      <code>
       length
      </code>
     </em>
     preenchendo os caracteres no início
     <em class="parameter">
      <code>
       fill
      </code>
     </em>
     (um espaço por padrão). Se o
     <em class="parameter">
      <code>
       string
      </code>
     </em>
     já é mais longo do que
     <em class="parameter">
      <code>
       length
      </code>
     </em>
     então, ele é truncado (à direita).
    </p>
    <p>
     <code>
      lpad('hi', 5, 'xy')
     </code>
     →
     <code>
      xyxhi
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
       string
      </code>
     </em>
     <code>
      text
     </code>
     [
     <span class="optional">
      ,
      <em class="parameter">
       <code>
        characters
       </code>
      </em>
      <code>
       text
      </code>
     </span>
     ] ) →
     <code>
      text
     </code>
    </p>
    <p>
     Remove a cadeia mais longa que contenha apenas caracteres
     <em class="parameter">
      <code>
       characters
      </code>
     </em>
     (um espaço por padrão) desde o início
     <em class="parameter">
      <code>
       string
      </code>
     </em>
     .
    </p>
    <p>
     <code>
      ltrim('zzzytest', 'xyz')
     </code>
     →
     <code>
      test
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      normalize
     </code>
     (
     <code>
      text
     </code>
     [
     <span class="optional">
      ,
      <em class="parameter">
       <code>
        form
       </code>
      </em>
     </span>
     ] ) →
     <code>
      text
     </code>
    </p>
    <p>
     Converte a cadeia de caracteres para a forma de normalização Unicode especificada. A opção
     <em class="parameter">
      <code>
       form
      </code>
     </em>
     palavra-chave especifica o formulário:
     <code>
      NFC
     </code>
     (o padrão),
     <code>
      NFD
     </code>
     ,
     <code>
      NFKC
     </code>
     , ou
     <code>
      NFKD
     </code>
     Essa função só pode ser usada quando o codificação do servidor é
     <code>
      UTF8
     </code>
     .
    </p>
    <p>
     <code>
      normalize(U&amp;'\0061\0308bc', NFC)
     </code>
     →
     <code>
      U&amp;'\00E4bc'
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
      text
     </code>
     )
     <code>
      integer
     </code>
    </p>
    <p>
     Retorna o número de bytes na string.
    </p>
    <p>
     <code>
      octet_length('josé')
     </code>
     →
     <code>
      5
     </code>
     (se o codificação do servidor for UTF8)
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
      character
     </code>
     )
     <code>
      integer
     </code>
    </p>
    <p>
     Retorna o número de bytes na string. Como esta versão da função aceita o tipo
     <code>
      character
     </code>
     diretamente, não removerá espaços finais.
    </p>
    <p>
     <code>
      octet_length('abc '::character(4))
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
      overlay
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
     <code>
      PLACING
     </code>
     <em class="parameter">
      <code>
       newsubstring
      </code>
     </em>
     <code>
      text
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
     ] )
     <code>
      text
     </code>
    </p>
    <p>
     Substitui a subdivisão de
     <em class="parameter">
      <code>
       string
      </code>
     </em>
     que começa em
     <em class="parameter">
      <code>
       start
      </code>
     </em>
     'o personagem e se estende por
     <em class="parameter">
      <code>
       count
      </code>
     </em>
     personagens com
     <em class="parameter">
      <code>
       newsubstring
      </code>
     </em>
     . Se
     <em class="parameter">
      <code>
       count
      </code>
     </em>
     Se for omitido, ele tem como padrão o comprimento de
     <em class="parameter">
      <code>
       newsubstring
      </code>
     </em>
     .
    </p>
    <p>
     <code>
      overlay('Txxxxas' placing 'hom' from 2 for 4)
     </code>
     →
     <code>
      Thomas
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
      text
     </code>
     <code>
      IN
     </code>
     <em class="parameter">
      <code>
       string
      </code>
     </em>
     <code>
      text
     </code>
     )
     <code>
      integer
     </code>
    </p>
    <p>
     Retorna o primeiro índice de início do especificado
     <em class="parameter">
      <code>
       substring
      </code>
     </em>
     dentro
     <em class="parameter">
      <code>
       string
      </code>
     </em>
     , ou zero se não estiver presente.
    </p>
    <p>
     <code>
      position('om' in 'Thomas')
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
      rpad
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
       length
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
        fill
       </code>
      </em>
      <code>
       text
      </code>
     </span>
     ] ) →
     <code>
      text
     </code>
    </p>
    <p>
     Amplia o
     <em class="parameter">
      <code>
       string
      </code>
     </em>
     até o comprimento
     <em class="parameter">
      <code>
       length
      </code>
     </em>
     ao anexar os caracteres
     <em class="parameter">
      <code>
       fill
      </code>
     </em>
     (um espaço por padrão). Se o
     <em class="parameter">
      <code>
       string
      </code>
     </em>
     já é mais longo do que
     <em class="parameter">
      <code>
       length
      </code>
     </em>
     então, ela é truncada.
    </p>
    <p>
     <code>
      rpad('hi', 5, 'xy')
     </code>
     →
     <code>
      hixyx
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
       string
      </code>
     </em>
     <code>
      text
     </code>
     [
     <span class="optional">
      ,
      <em class="parameter">
       <code>
        characters
       </code>
      </em>
      <code>
       text
      </code>
     </span>
     ] ) →
     <code>
      text
     </code>
    </p>
    <p>
     Remove a cadeia mais longa que contenha apenas caracteres
     <em class="parameter">
      <code>
       characters
      </code>
     </em>
     (um espaço por padrão) a partir do final de
     <em class="parameter">
      <code>
       string
      </code>
     </em>
     .
    </p>
    <p>
     <code>
      rtrim('testxxzx', 'xyz')
     </code>
     →
     <code>
      test
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
       string
      </code>
     </em>
     <code>
      text
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
     ] )
     <code>
      text
     </code>
    </p>
    <p>
     Extrai a subcadeia de
     <em class="parameter">
      <code>
       string
      </code>
     </em>
     a partir do
     <em class="parameter">
      <code>
       start
      </code>
     </em>
     'se o personagem for especificado, e parar após
     <em class="parameter">
      <code>
       count
      </code>
     </em>
     caracteres, se isso for especificado. Forneça pelo menos um
     <em class="parameter">
      <code>
       start
      </code>
     </em>
     e
     <em class="parameter">
      <code>
       count
      </code>
     </em>
     .
    </p>
    <p>
     <code>
      substring('Thomas' from 2 for 3)
     </code>
     →
     <code>
      hom
     </code>
    </p>
    <p>
     <code>
      substring('Thomas' from 3)
     </code>
     →
     <code>
      omas
     </code>
    </p>
    <p>
     <code>
      substring('Thomas' for 2)
     </code>
     →
     <code>
      Th
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
       string
      </code>
     </em>
     <code>
      text
     </code>
     <code>
      FROM
     </code>
     <em class="parameter">
      <code>
       pattern
      </code>
     </em>
     <code>
      text
     </code>
     )
     <code>
      text
     </code>
    </p>
    <p>
     Extrai a primeira subcadeia que corresponde à expressão regular POSIX; veja
     <a class="xref" href="functions-matching.md#FUNCTIONS-POSIX-REGEXP" title="9.7.3. POSIX Regular Expressions">
      Seção 9.7.3
     </a>
     .
    </p>
    <p>
     <code>
      substring('Thomas' from '...$')
     </code>
     →
     <code>
      mas
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
       string
      </code>
     </em>
     <code>
      text
     </code>
     <code>
      SIMILAR
     </code>
     <em class="parameter">
      <code>
       pattern
      </code>
     </em>
     <code>
      text
     </code>
     <code>
      ESCAPE
     </code>
     <em class="parameter">
      <code>
       escape
      </code>
     </em>
     <code>
      text
     </code>
     )
     <code>
      text
     </code>
    </p>
    <p class="func_signature">
     <code>
      substring
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
     <code>
      FROM
     </code>
     <em class="parameter">
      <code>
       pattern
      </code>
     </em>
     <code>
      text
     </code>
     <code>
      FOR
     </code>
     <em class="parameter">
      <code>
       escape
      </code>
     </em>
     <code>
      text
     </code>
     )
     <code>
      text
     </code>
    </p>
    <p>
     Extrai a primeira subcadeia de caracteres que corresponde
     <acronym class="acronym">
      SQL
     </acronym>
     expressão regular; veja
     <a class="xref" href="functions-matching.md#FUNCTIONS-SIMILARTO-REGEXP" title="9.7.2. SIMILAR TO Regular Expressions">
      Seção 9.7.2
     </a>
     A primeira forma foi especificada desde SQL:2003; a segunda forma só estava presente no SQL:1999 e deve ser considerada obsoleta.
    </p>
    <p>
     <code>
      substring('Thomas' similar '%#"o_a#"_' escape '#')
     </code>
     →
     <code>
      oma
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
     <span class="optional">
      <em class="parameter">
       <code>
        characters
       </code>
      </em>
      <code>
       text
      </code>
     </span>
     ]
     <code>
      FROM
     </code>
     <em class="parameter">
      <code>
       string
      </code>
     </em>
     <code>
      text
     </code>
     )
     <code>
      text
     </code>
    </p>
    <p>
     Remove a cadeia mais longa que contenha apenas caracteres
     <em class="parameter">
      <code>
       characters
      </code>
     </em>
     (um espaço por padrão) a partir do início, do fim ou de ambos os extremos (
     <code>
      BOTH
     </code>
     é o padrão) de
     <em class="parameter">
      <code>
       string
      </code>
     </em>
     .
    </p>
    <p>
     <code>
      trim(both 'xyz' from 'yxTomxx')
     </code>
     →
     <code>
      Tom
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
       string
      </code>
     </em>
     <code>
      text
     </code>
     [
     <span class="optional">
      ,
      <em class="parameter">
       <code>
        characters
       </code>
      </em>
      <code>
       text
      </code>
     </span>
     ] )
     <code>
      text
     </code>
    </p>
    <p>
     Esta é uma sintaxe não padrão para
     <code>
      trim()
     </code>
     .
    </p>
    <p>
     <code>
      trim(both from 'yxTomxx', 'xyz')
     </code>
     →
     <code>
      Tom
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      unicode_assigned
     </code>
     (
     <code>
      text
     </code>
     )
     <code>
      boolean
     </code>
    </p>
    <p>
     Retornos
     <code>
      true
     </code>
     se todos os caracteres na string forem atribuídos a pontos de código Unicode;
     <code>
      false
     </code>
     caso contrário. Essa função só pode ser usada quando o codificação do servidor é
     <code>
      UTF8
     </code>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      upper
     </code>
     (
     <code>
      text
     </code>
     )
     <code>
      text
     </code>
    </p>
    <p>
     Converte a string para maiúsculas, de acordo com as regras do local do banco de dados.
    </p>
    <p>
     <code>
      upper('tom')
     </code>
     →
     <code>
      TOM
     </code>
    </p>
   </td>
  </tr>
 </tbody>
</table>

Funções e operadores adicionais de manipulação de strings estão disponíveis e estão listados em [Tabela 9.10] ((functions-string.md#FUNCTIONS-STRING-OTHER "Table 9.10. Other String Functions and Operators")). (Algumas dessas funções são usadas internamente para implementar as funções de string padrão do SQL listadas em [Tabela 9.9] ((functions-string.md#FUNCTIONS-STRING-SQL "Table 9.9. SQL String Functions and Operators")). Além disso, há operadores de correspondência de padrões, que são descritos em [Seção 9.7] ((functions-matching.md "9.7. Pattern Matching")), e operadores para pesquisa de texto completo, que são descritos em [Capítulo 12] ((textsearch.md "Chapter 12. Full Text Search")).

**Tabela 9.10. Outras funções e operadores de cadeia**

<table>
 <colgroup>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th class="func_table_entry">
    <p class="func_signature">
     Função/Operador
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
      text
     </code>
     <code>
      ^@
     </code>
     <code>
      text
     </code>
     →
     <code>
      boolean
     </code>
    </p>
    <p>
     Retorna verdadeiro se a primeira string começar com a segunda string (equivalente a o
     <code>
      starts_with()
     </code>
     function).
    </p>
    <p>
     <code>
      'alphabet' ^@ 'alph'
     </code>
     →
     <code>
      t
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      ascii
     </code>
     (
     <code>
      text
     </code>
     )
     <code>
      integer
     </code>
    </p>
    <p>
     Retorna o código numérico do primeiro caractere do argumento. Em
     <acronym class="acronym">
      UTF8
     </acronym>
     encoding, retorna o ponto de código Unicode do caractere. Em outros codificações multilínguas, o argumento deve ser
     <acronym class="acronym">
      ASCII
     </acronym>
     character.
    </p>
    <p>
     <code>
      ascii('x')
     </code>
     →
     <code>
      120
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      chr
     </code>
     (
     <code>
      integer
     </code>
     )
     <code>
      text
     </code>
    </p>
    <p>
     Retorna o caractere com o código fornecido. Em
     <acronym class="acronym">
      UTF8
     </acronym>
     O argumento é codificado como um ponto de código Unicode. Em outros tipos de codificação multilíngue, o argumento deve designar
     <acronym class="acronym">
      ASCII
     </acronym>
     character.
     <code>
      chr(0)
     </code>
     é desaconselhável, pois os tipos de dados de texto não podem armazenar esse caractere.
    </p>
    <p>
     <code>
      chr(65)
     </code>
     →
     <code>
      A
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      concat
     </code>
     (
     <em class="parameter">
      <code>
       val1
      </code>
     </em>
     <code>
      "any"
     </code>
     [
     <span class="optional">
      ,
      <em class="parameter">
       <code>
        val2
       </code>
      </em>
      <code>
       "any"
      </code>
      [
      <span class="optional">
       , ...
      </span>
      ]
     </span>
     ] ) →
     <code>
      text
     </code>
    </p>
    <p>
     Concatenia as representações de texto de todos os argumentos. Argumentos NULL são ignorados.
    </p>
    <p>
     <code>
      concat('abcde', 2, NULL, 22)
     </code>
     →
     <code>
      abcde222
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      concat_ws
     </code>
     (
     <em class="parameter">
      <code>
       sep
      </code>
     </em>
     <code>
      text
     </code>
     ,
     <em class="parameter">
      <code>
       val1
      </code>
     </em>
     <code>
      "any"
     </code>
     [
     <span class="optional">
      ,
      <em class="parameter">
       <code>
        val2
       </code>
      </em>
      <code>
       "any"
      </code>
      [
      <span class="optional">
       , ...
      </span>
      ]
     </span>
     ] ) →
     <code>
      text
     </code>
    </p>
    <p>
     Concatenia todos, exceto o primeiro argumento, com separadores. O primeiro argumento é usado como a string de separador e não deve ser NULL. Outros argumentos NULL são ignorados.
    </p>
    <p>
     <code>
      concat_ws(',', 'abcde', 2, NULL, 22)
     </code>
     →
     <code>
      abcde,2,22
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      format
     </code>
     (
     <em class="parameter">
      <code>
       formatstr
      </code>
     </em>
     <code>
      text
     </code>
     [
     <span class="optional">
      ,
      <em class="parameter">
       <code>
        formatarg
       </code>
      </em>
      <code>
       "any"
      </code>
      [
      <span class="optional">
       , ...
      </span>
      ]
     </span>
     ] ) →
     <code>
      text
     </code>
    </p>
    <p>
     Formata argumentos de acordo com uma string de formato; veja
     <a class="xref" href="functions-string.md#FUNCTIONS-STRING-FORMAT" title="9.4.1. format">
      Seção 9.4.1
     </a>
     Essa função é semelhante à função C
     <code>
      sprintf
     </code>
     .
    </p>
    <p>
     <code>
      format('Hello %s, %1$s', 'World')
     </code>
     →
     <code>
      Hello World, World
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      initcap
     </code>
     (
     <code>
      text
     </code>
     )
     <code>
      text
     </code>
    </p>
    <p>
     Converte a primeira letra de cada palavra para maiúscula e o resto para minúscula. As palavras são sequências de caracteres alfanuméricos separados por caracteres não alfanuméricos.
    </p>
    <p>
     <code>
      initcap('hi THOMAS')
     </code>
     →
     <code>
      Hi Thomas
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      casefold
     </code>
     (
     <code>
      text
     </code>
     )
     <code>
      text
     </code>
    </p>
    <p>
     Realiza a compactação de maiúsculas da string de entrada de acordo com a correção de texto. A compactação de maiúsculas é semelhante à conversão de maiúsculas, mas o propósito da compactação de maiúsculas é facilitar a correspondência não sensível à maiúscula das strings, enquanto o propósito da conversão de maiúsculas é converter para uma forma específica de maiúsculas. Esta função só pode ser usada quando o codificação do servidor é
     <code>
      UTF8
     </code>
     .
    </p>
    <p>
     Normalmente, a dobragem de caso simplesmente converte para minúsculas, mas pode haver exceções, dependendo da ordenação. Por exemplo, alguns caracteres têm mais de duas variantes em minúsculas, ou dobra para maiúsculas.
    </p>
    <p>
     A dobragem do caso pode alterar o comprimento da corda. Por exemplo, no
     <code>
      PG_UNICODE_FAST
     </code>
     colação,
     <code>
      ß
     </code>
     (U+00DF) dobra para
     <code>
      ss
     </code>
     .
    </p>
    <p>
     <code>
      casefold
     </code>
     pode ser usado para correspondência de caso não maiúsculo padrão Unicode. Ele não preserva sempre a forma normalizada da string de entrada (veja a seção "Notas de rodapé").
     <a class="xref" href="functions-string.md#FUNCTION-NORMALIZE">
      normalizar
     </a>
     ).
    </p>
    <p>
     O
     <code>
      libc
     </code>
     o fornecedor não suporta dobramento de caso, então
     <code>
      casefold
     </code>
     é idêntico a
     <a class="xref" href="functions-string.md#FUNCTION-LOWER">
      inferior
     </a>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      left
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
       n
      </code>
     </em>
     <code>
      integer
     </code>
     )
     <code>
      text
     </code>
    </p>
    <p>
     Retorna o primeiro
     <em class="parameter">
      <code>
       n
      </code>
     </em>
     caracteres na string, ou quando
     <em class="parameter">
      <code>
       n
      </code>
     </em>
     se for negativo, retorna todos, exceto o último |
     <em class="parameter">
      <code>
       n
      </code>
     </em>
     | personagens.
    </p>
    <p>
     <code>
      left('abcde', 2)
     </code>
     →
     <code>
      ab
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
      text
     </code>
     )
     <code>
      integer
     </code>
    </p>
    <p>
     Retorna o número de caracteres na string.
    </p>
    <p>
     <code>
      length('jose')
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
      text
     </code>
     )
     <code>
      text
     </code>
    </p>
    <p>
     Calcula o MD5
     <a class="link" href="functions-binarystring.md#FUNCTIONS-HASH-NOTE">
      hash
     </a>
     do argumento, com o resultado escrito em hexadecimal.
    </p>
    <p>
     <code>
      md5('abc')
     </code>
     →
     <code>
      900150983cd24fb0​d6963f7d28e17f72
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      parse_ident
     </code>
     (
     <em class="parameter">
      <code>
       qualified_identifier
      </code>
     </em>
     <code>
      text
     </code>
     [
     <span class="optional">
      ,
      <em class="parameter">
       <code>
        strict_mode
       </code>
      </em>
      <code>
       boolean
      </code>
      <code>
       DEFAULT
      </code>
      <code>
       true
      </code>
     </span>
     ] ) →
     <code>
      text[]
     </code>
    </p>
    <p>
     Divisões
     <em class="parameter">
      <code>
       qualified_identifier
      </code>
     </em>
     em um conjunto de identificadores, removendo qualquer citação de identificadores individuais. Por padrão, caracteres extras após o último identificador são considerados um erro; mas se o segundo parâmetro for
     <code>
      false
     </code>
     , então esses caracteres extras são ignorados. (Esse comportamento é útil para a análise de nomes para objetos como funções.) Observe que essa função não corta identificadores de comprimento excessivo. Se você deseja uma redução, pode-se converter o resultado em
     <code>
      name[]
     </code>
     .
    </p>
    <p>
     <code>
      parse_ident('"SomeSchema".someTable')
     </code>
     →
     <code>
      {SomeSchema,sometable}
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pg_client_encoding
     </code>
     ( )
     <code>
      name
     </code>
    </p>
    <p>
     Retorna o nome atual do codificador do cliente.
    </p>
    <p>
     <code>
      pg_client_encoding()
     </code>
     →
     <code>
      UTF8
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      quote_ident
     </code>
     (
     <code>
      text
     </code>
     )
     <code>
      text
     </code>
    </p>
    <p>
     Retorna a string fornecida devidamente citada para ser usada como um identificador em
     <acronym class="acronym">
      SQL
     </acronym>
     string de declaração. As citações são adicionadas apenas quando necessário (ou seja, se a string contiver caracteres não identificadores ou que seriam compactados em maiúsculas). As citações embutidas são duplicadas corretamente. Veja também
     <a class="xref" href="plpgsql-statements.md#PLPGSQL-QUOTE-LITERAL-EXAMPLE" title="Example 41.1. Quoting Values in Dynamic Queries">
      Exemplo 41.1
     </a>
     .
    </p>
    <p>
     <code>
      quote_ident('Foo bar')
     </code>
     →
     <code>
      "Foo bar"
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      quote_literal
     </code>
     (
     <code>
      text
     </code>
     )
     <code>
      text
     </code>
    </p>
    <p>
     Retorna a string fornecida devidamente citada para ser usada como uma literal de string em um
     <acronym class="acronym">
      SQL
     </acronym>
     string de declaração. As aspas embutidas e barras invertidas são duplicadas corretamente. Observe que
     <code>
      quote_literal
     </code>
     retorna nulo em entrada nulo; se o argumento pode ser nulo,
     <code>
      quote_nullable
     </code>
     é muitas vezes mais adequada. Veja também
     <a class="xref" href="plpgsql-statements.md#PLPGSQL-QUOTE-LITERAL-EXAMPLE" title="Example 41.1. Quoting Values in Dynamic Queries">
      Exemplo 41.1
     </a>
     .
    </p>
    <p>
     <code>
      quote_literal(E'O\'Reilly')
     </code>
     →
     <code>
      'O''Reilly'
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      quote_literal
     </code>
     (
     <code>
      anyelement
     </code>
     )
     <code>
      text
     </code>
    </p>
    <p>
     Converte o valor fornecido em texto e, em seguida, o cita como literal. As aspas embutidas e barras invertidas são duplicadas corretamente.
    </p>
    <p>
     <code>
      quote_literal(42.5)
     </code>
     →
     <code>
      '42.5'
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      quote_nullable
     </code>
     (
     <code>
      text
     </code>
     )
     <code>
      text
     </code>
    </p>
    <p>
     Retorna a string fornecida devidamente citada para ser usada como uma literal de string em um
     <acronym class="acronym">
      SQL
     </acronym>
     string; ou, se o argumento for nulo, retorna
     <code>
      NULL
     </code>
     As aspas embutidas e barras invertidas são duplicadas corretamente. Veja também
     <a class="xref" href="plpgsql-statements.md#PLPGSQL-QUOTE-LITERAL-EXAMPLE" title="Example 41.1. Quoting Values in Dynamic Queries">
      Exemplo 41.1
     </a>
     .
    </p>
    <p>
     <code>
      quote_nullable(NULL)
     </code>
     →
     <code>
      NULL
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      quote_nullable
     </code>
     (
     <code>
      anyelement
     </code>
     )
     <code>
      text
     </code>
    </p>
    <p>
     Converte o valor fornecido em texto e, em seguida, o cita como literal; ou, se o argumento for nulo, retorna
     <code>
      NULL
     </code>
     As aspas embutidas e barras invertidas são duplicadas corretamente.
    </p>
    <p>
     <code>
      quote_nullable(42.5)
     </code>
     →
     <code>
      '42.5'
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      regexp_count
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
       pattern
      </code>
     </em>
     <code>
      text
     </code>
     [
     <span class="optional">
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
         flags
        </code>
       </em>
       <code>
        text
       </code>
      </span>
      ]
     </span>
     ] ) →
     <code>
      integer
     </code>
    </p>
    <p>
     Retorna o número de vezes que a expressão regular POSIX é encontrada.
     <em class="parameter">
      <code>
       pattern
      </code>
     </em>
     jogos na
     <em class="parameter">
      <code>
       string
      </code>
     </em>
     ; veja
     <a class="xref" href="functions-matching.md#FUNCTIONS-POSIX-REGEXP" title="9.7.3. POSIX Regular Expressions">
      Seção 9.7.3
     </a>
     .
    </p>
    <p>
     <code>
      regexp_count('123456789012', '\d\d\d', 2)
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
      regexp_instr
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
       pattern
      </code>
     </em>
     <code>
      text
     </code>
     [
     <span class="optional">
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
         N
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
          endoption
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
           flags
          </code>
         </em>
         <code>
          text
         </code>
         [
         <span class="optional">
          ,
          <em class="parameter">
           <code>
            subexpr
           </code>
          </em>
          <code>
           integer
          </code>
         </span>
         ]
        </span>
        ]
       </span>
       ]
      </span>
      ]
     </span>
     ] ) →
     <code>
      integer
     </code>
    </p>
    <p>
     Retorna a posição dentro
     <em class="parameter">
      <code>
       string
      </code>
     </em>
     onde o
     <em class="parameter">
      <code>
       N
      </code>
     </em>
     'o jogo da expressão regular POSIX padrão
     <em class="parameter">
      <code>
       pattern
      </code>
     </em>
     ocorre, ou zero se não houver tal correspondência; veja
     <a class="xref" href="functions-matching.md#FUNCTIONS-POSIX-REGEXP" title="9.7.3. POSIX Regular Expressions">
      Seção 9.7.3
     </a>
     .
    </p>
    <p>
     <code>
      regexp_instr('ABCDEF', 'c(.)(..)', 1, 1, 0, 'i')
     </code>
     →
     <code>
      3
     </code>
    </p>
    <p>
     <code>
      regexp_instr('ABCDEF', 'c(.)(..)', 1, 1, 0, 'i', 2)
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
      regexp_like
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
       pattern
      </code>
     </em>
     <code>
      text
     </code>
     [
     <span class="optional">
      ,
      <em class="parameter">
       <code>
        flags
       </code>
      </em>
      <code>
       text
      </code>
     </span>
     ] ) →
     <code>
      boolean
     </code>
    </p>
    <p>
     Verifica se há uma correspondência da expressão regular POSIX
     <em class="parameter">
      <code>
       pattern
      </code>
     </em>
     acontece dentro
     <em class="parameter">
      <code>
       string
      </code>
     </em>
     ; veja
     <a class="xref" href="functions-matching.md#FUNCTIONS-POSIX-REGEXP" title="9.7.3. POSIX Regular Expressions">
      Seção 9.7.3
     </a>
     .
    </p>
    <p>
     <code>
      regexp_like('Hello World', 'world$', 'i')
     </code>
     →
     <code>
      t
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      regexp_match
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
       pattern
      </code>
     </em>
     <code>
      text
     </code>
     [
     <span class="optional">
      ,
      <em class="parameter">
       <code>
        flags
       </code>
      </em>
      <code>
       text
      </code>
     </span>
     ] )
     <code>
      text[]
     </code>
    </p>
    <p>
     Retorna substratos dentro da primeira correspondência da expressão regular POSIX
     <em class="parameter">
      <code>
       pattern
      </code>
     </em>
     para o
     <em class="parameter">
      <code>
       string
      </code>
     </em>
     ; veja
     <a class="xref" href="functions-matching.md#FUNCTIONS-POSIX-REGEXP" title="9.7.3. POSIX Regular Expressions">
      Seção 9.7.3
     </a>
     .
    </p>
    <p>
     <code>
      regexp_match('foobarbequebaz', '(bar)(beque)')
     </code>
     →
     <code>
      {bar,beque}
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      regexp_matches
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
       pattern
      </code>
     </em>
     <code>
      text
     </code>
     [
     <span class="optional">
      ,
      <em class="parameter">
       <code>
        flags
       </code>
      </em>
      <code>
       text
      </code>
     </span>
     ] )
     <code>
      setof text[]
     </code>
    </p>
    <p>
     Retorna substratos dentro da primeira correspondência da expressão regular POSIX
     <em class="parameter">
      <code>
       pattern
      </code>
     </em>
     para o
     <em class="parameter">
      <code>
       string
      </code>
     </em>
     , ou substratos em todas essas correspondências, se o
     <code>
      g
     </code>
     é usada a bandeira; veja
     <a class="xref" href="functions-matching.md#FUNCTIONS-POSIX-REGEXP" title="9.7.3. POSIX Regular Expressions">
      Seção 9.7.3
     </a>
     .
    </p>
    <p>
     <code>
      regexp_matches('foobarbequebaz', 'ba.', 'g')
     </code>
     →
     <code>
     </code>
    </p>
    <pre class="programlisting">
 {bar} {baz}
</pre>
    <p>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      regexp_replace
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
       pattern
      </code>
     </em>
     <code>
      text
     </code>
     ,
     <em class="parameter">
      <code>
       replacement
      </code>
     </em>
     <code>
      text
     </code>
     [
     <span class="optional">
      ,
      <em class="parameter">
       <code>
        flags
       </code>
      </em>
      <code>
       text
      </code>
     </span>
     ] ) →
     <code>
      text
     </code>
    </p>
    <p>
     Substitui a substring que é a primeira correspondência à expressão regular POSIX
     <em class="parameter">
      <code>
       pattern
      </code>
     </em>
     , ou todos esses jogos, se o
     <code>
      g
     </code>
     é usada a bandeira; veja
     <a class="xref" href="functions-matching.md#FUNCTIONS-POSIX-REGEXP" title="9.7.3. POSIX Regular Expressions">
      Seção 9.7.3
     </a>
     .
    </p>
    <p>
     <code>
      regexp_replace('Thomas', '.[mN]a.', 'M')
     </code>
     →
     <code>
      ThM
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      regexp_replace
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
       pattern
      </code>
     </em>
     <code>
      text
     </code>
     ,
     <em class="parameter">
      <code>
       replacement
      </code>
     </em>
     <code>
      text
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
        N
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
         flags
        </code>
       </em>
       <code>
        text
       </code>
      </span>
      ]
     </span>
     ] ) →
     <code>
      text
     </code>
    </p>
    <p>
     Substitui a substring que é
     <em class="parameter">
      <code>
       N
      </code>
     </em>
     'o correspondente à expressão regular POSIX
     <em class="parameter">
      <code>
       pattern
      </code>
     </em>
     , ou todos esses jogos, se
     <em class="parameter">
      <code>
       N
      </code>
     </em>
     é zero, com a busca começando na
     <em class="parameter">
      <code>
       start
      </code>
     </em>
     'o caráter de
     <em class="parameter">
      <code>
       string
      </code>
     </em>
     . Se
     <em class="parameter">
      <code>
       N
      </code>
     </em>
     Se for omitido, ele tem como padrão 1. Veja
     <a class="xref" href="functions-matching.md#FUNCTIONS-POSIX-REGEXP" title="9.7.3. POSIX Regular Expressions">
      Seção 9.7.3
     </a>
     .
    </p>
    <p>
     <code>
      regexp_replace('Thomas', '.', 'X', 3, 2)
     </code>
     →
     <code>
      ThoXas
     </code>
    </p>
    <p>
     <code>
      regexp_replace(string=&gt;'hello world', pattern=&gt;'l', replacement=&gt;'XX', start=&gt;1, "N"=&gt;2)
     </code>
     →
     <code>
      helXXo world
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      regexp_split_to_array
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
       pattern
      </code>
     </em>
     <code>
      text
     </code>
     [
     <span class="optional">
      ,
      <em class="parameter">
       <code>
        flags
       </code>
      </em>
      <code>
       text
      </code>
     </span>
     ] )
     <code>
      text[]
     </code>
    </p>
    <p>
     Divisões
     <em class="parameter">
      <code>
       string
      </code>
     </em>
     usando uma expressão regular POSIX como delimitador, produzindo um array de resultados; veja
     <a class="xref" href="functions-matching.md#FUNCTIONS-POSIX-REGEXP" title="9.7.3. POSIX Regular Expressions">
      Seção 9.7.3
     </a>
     .
    </p>
    <p>
     <code>
      regexp_split_to_array('hello world', '\s+')
     </code>
     →
     <code>
      {hello,world}
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      regexp_split_to_table
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
       pattern
      </code>
     </em>
     <code>
      text
     </code>
     [
     <span class="optional">
      ,
      <em class="parameter">
       <code>
        flags
       </code>
      </em>
      <code>
       text
      </code>
     </span>
     ] )
     <code>
      setof text
     </code>
    </p>
    <p>
     Divisões
     <em class="parameter">
      <code>
       string
      </code>
     </em>
     usando uma expressão regular POSIX como delimitador, produzindo um conjunto de resultados; veja
     <a class="xref" href="functions-matching.md#FUNCTIONS-POSIX-REGEXP" title="9.7.3. POSIX Regular Expressions">
      Seção 9.7.3
     </a>
     .
    </p>
    <p>
     <code>
      regexp_split_to_table('hello world', '\s+')
     </code>
     →
     <code>
     </code>
    </p>
    <pre class="programlisting">
 hello world
</pre>
    <p>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      regexp_substr
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
       pattern
      </code>
     </em>
     <code>
      text
     </code>
     [
     <span class="optional">
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
         N
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
          flags
         </code>
        </em>
        <code>
         text
        </code>
        [
        <span class="optional">
         ,
         <em class="parameter">
          <code>
           subexpr
          </code>
         </em>
         <code>
          integer
         </code>
        </span>
        ]
       </span>
       ]
      </span>
      ]
     </span>
     ] ) →
     <code>
      text
     </code>
    </p>
    <p>
     Retorna a subcadeia dentro de
     <em class="parameter">
      <code>
       string
      </code>
     </em>
     que correspondem a
     <em class="parameter">
      <code>
       N
      </code>
     </em>
     'a ocorrência da expressão regular POSIX
     <em class="parameter">
      <code>
       pattern
      </code>
     </em>
     , ou
     <code>
      NULL
     </code>
     se não houver tal correspondência; veja
     <a class="xref" href="functions-matching.md#FUNCTIONS-POSIX-REGEXP" title="9.7.3. POSIX Regular Expressions">
      Seção 9.7.3
     </a>
     .
    </p>
    <p>
     <code>
      regexp_substr('ABCDEF', 'c(.)(..)', 1, 1, 'i')
     </code>
     →
     <code>
      CDEF
     </code>
    </p>
    <p>
     <code>
      regexp_substr('ABCDEF', 'c(.)(..)', 1, 1, 'i', 2)
     </code>
     →
     <code>
      EF
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      repeat
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
       number
      </code>
     </em>
     <code>
      integer
     </code>
     )
     <code>
      text
     </code>
    </p>
    <p>
     Repetições
     <em class="parameter">
      <code>
       string
      </code>
     </em>
     o especificado
     <em class="parameter">
      <code>
       number
      </code>
     </em>
     das vezes.
    </p>
    <p>
     <code>
      repeat('Pg', 4)
     </code>
     →
     <code>
      PgPgPgPg
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      replace
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
       from
      </code>
     </em>
     <code>
      text
     </code>
     ,
     <em class="parameter">
      <code>
       to
      </code>
     </em>
     <code>
      text
     </code>
     )
     <code>
      text
     </code>
    </p>
    <p>
     Substitui todas as ocorrências em
     <em class="parameter">
      <code>
       string
      </code>
     </em>
     de subdivisão
     <em class="parameter">
      <code>
       from
      </code>
     </em>
     com subdivisão
     <em class="parameter">
      <code>
       to
      </code>
     </em>
     .
    </p>
    <p>
     <code>
      replace('abcdefabcdef', 'cd', 'XX')
     </code>
     →
     <code>
      abXXefabXXef
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
      text
     </code>
     )
     <code>
      text
     </code>
    </p>
    <p>
     Reverte a ordem dos caracteres na string.
    </p>
    <p>
     <code>
      reverse('abcde')
     </code>
     →
     <code>
      edcba
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      right
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
       n
      </code>
     </em>
     <code>
      integer
     </code>
     )
     <code>
      text
     </code>
    </p>
    <p>
     Retorna o último
     <em class="parameter">
      <code>
       n
      </code>
     </em>
     caracteres na string, ou quando
     <em class="parameter">
      <code>
       n
      </code>
     </em>
     se for negativo, retorna tudo, exceto o primeiro |
     <em class="parameter">
      <code>
       n
      </code>
     </em>
     | personagens.
    </p>
    <p>
     <code>
      right('abcde', 2)
     </code>
     →
     <code>
      de
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      split_part
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
       delimiter
      </code>
     </em>
     <code>
      text
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
     )
     <code>
      text
     </code>
    </p>
    <p>
     Divisões
     <em class="parameter">
      <code>
       string
      </code>
     </em>
     em ocorrências de
     <em class="parameter">
      <code>
       delimiter
      </code>
     </em>
     e retorna o
     <em class="parameter">
      <code>
       n
      </code>
     </em>
     'campo (contando de um), ou quando
     <em class="parameter">
      <code>
       n
      </code>
     </em>
     se for negativo, retorna |
     <em class="parameter">
      <code>
       n
      </code>
     </em>
     campo 'th-from-last.
    </p>
    <p>
     <code>
      split_part('abc~@~def~@~ghi', '~@~', 2)
     </code>
     →
     <code>
      def
     </code>
    </p>
    <p>
     <code>
      split_part('abc,def,ghi,jkl', ',', -2)
     </code>
     →
     <code>
      ghi
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      starts_with
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
       prefix
      </code>
     </em>
     <code>
      text
     </code>
     )
     <code>
      boolean
     </code>
    </p>
    <p>
     Retorna verdadeiro se
     <em class="parameter">
      <code>
       string
      </code>
     </em>
     começa com
     <em class="parameter">
      <code>
       prefix
      </code>
     </em>
     .
    </p>
    <p>
     <code>
      starts_with('alphabet', 'alph')
     </code>
     →
     <code>
      t
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      string_to_array
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
       delimiter
      </code>
     </em>
     <code>
      text
     </code>
     [
     <span class="optional">
      ,
      <em class="parameter">
       <code>
        null_string
       </code>
      </em>
      <code>
       text
      </code>
     </span>
     ] )
     <code>
      text[]
     </code>
    </p>
    <p>
     Separa os
     <em class="parameter">
      <code>
       string
      </code>
     </em>
     em ocorrências de
     <em class="parameter">
      <code>
       delimiter
      </code>
     </em>
     e forma os campos resultantes em um
     <code>
      text
     </code>
     matriz. Se
     <em class="parameter">
      <code>
       delimiter
      </code>
     </em>
     é
     <code>
      NULL
     </code>
     , cada personagem no
     <em class="parameter">
      <code>
       string
      </code>
     </em>
     tornará um elemento separado na matriz. Se
     <em class="parameter">
      <code>
       delimiter
      </code>
     </em>
     se for uma string vazia, então
     <em class="parameter">
      <code>
       string
      </code>
     </em>
     é tratado como um único campo. Se
     <em class="parameter">
      <code>
       null_string
      </code>
     </em>
     é fornecida e não
     <code>
      NULL
     </code>
     , campos que correspondem a essa string são substituídos por
     <code>
      NULL
     </code>
     Veja também
     <a class="link" href="functions-array.md#FUNCTION-ARRAY-TO-STRING">
      <code>
       array_to_string
      </code>
     </a>
     .
    </p>
    <p>
     <code>
      string_to_array('xx~~yy~~zz', '~~', 'yy')
     </code>
     →
     <code>
      {xx,NULL,zz}
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      string_to_table
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
       delimiter
      </code>
     </em>
     <code>
      text
     </code>
     [
     <span class="optional">
      ,
      <em class="parameter">
       <code>
        null_string
       </code>
      </em>
      <code>
       text
      </code>
     </span>
     ] )
     <code>
      setof text
     </code>
    </p>
    <p>
     Separa os
     <em class="parameter">
      <code>
       string
      </code>
     </em>
     em ocorrências de
     <em class="parameter">
      <code>
       delimiter
      </code>
     </em>
     e retorna os campos resultantes como um conjunto de
     <code>
      text
     </code>
     linhas. Se
     <em class="parameter">
      <code>
       delimiter
      </code>
     </em>
     é
     <code>
      NULL
     </code>
     , cada personagem no
     <em class="parameter">
      <code>
       string
      </code>
     </em>
     tornará uma linha separada do resultado. Se
     <em class="parameter">
      <code>
       delimiter
      </code>
     </em>
     se for uma string vazia, então
     <em class="parameter">
      <code>
       string
      </code>
     </em>
     é tratado como um único campo. Se
     <em class="parameter">
      <code>
       null_string
      </code>
     </em>
     é fornecida e não
     <code>
      NULL
     </code>
     , campos que correspondem a essa string são substituídos por
     <code>
      NULL
     </code>
     .
    </p>
    <p>
     <code>
      string_to_table('xx~^~yy~^~zz', '~^~', 'yy')
     </code>
     →
     <code>
     </code>
    </p>
    <pre class="programlisting">
 xx NULL zz
</pre>
    <p>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      strpos
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
       substring
      </code>
     </em>
     <code>
      text
     </code>
     )
     <code>
      integer
     </code>
    </p>
    <p>
     Retorna o primeiro índice de início do especificado
     <em class="parameter">
      <code>
       substring
      </code>
     </em>
     dentro
     <em class="parameter">
      <code>
       string
      </code>
     </em>
     , ou zero se não estiver presente. (O mesmo que
     <code>
      position(
      <em class="parameter">
       <code>
        substring
       </code>
      </em>
      in
      <em class="parameter">
       <code>
        string
       </code>
      </em>
      )
     </code>
     , mas observe a ordem de argumento invertida.)
    </p>
    <p>
     <code>
      strpos('high', 'ig')
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
      substr
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
     ] )
     <code>
      text
     </code>
    </p>
    <p>
     Extrai a subcadeia de
     <em class="parameter">
      <code>
       string
      </code>
     </em>
     a partir do
     <em class="parameter">
      <code>
       start
      </code>
     </em>
     'o personagem, e estendendo-se por
     <em class="parameter">
      <code>
       count
      </code>
     </em>
     caracteres, se isso for especificado. (O mesmo que
     <code>
      substring(
      <em class="parameter">
       <code>
        string
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
      substr('alphabet', 3)
     </code>
     →
     <code>
      phabet
     </code>
    </p>
    <p>
     <code>
      substr('alphabet', 3, 2)
     </code>
     →
     <code>
      ph
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      to_ascii
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
     )
     <code>
      text
     </code>
    </p>
    <p class="func_signature">
     <code>
      to_ascii
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
       encoding
      </code>
     </em>
     <code>
      name
     </code>
     )
     <code>
      text
     </code>
    </p>
    <p class="func_signature">
     <code>
      to_ascii
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
       encoding
      </code>
     </em>
     <code>
      integer
     </code>
     )
     <code>
      text
     </code>
    </p>
    <p>
     Convertidos
     <em class="parameter">
      <code>
       string
      </code>
     </em>
     para
     <acronym class="acronym">
      ASCII
     </acronym>
     de outro codificação, que pode ser identificado pelo nome ou número. Se
     <em class="parameter">
      <code>
       encoding
      </code>
     </em>
     Se omite o codificação do banco de dados, presume-se que ela está presente (o que, na prática, é o único caso útil). A conversão consiste principalmente na eliminação de acentos. A conversão é suportada apenas a partir
     <code>
      LATIN1
     </code>
     ,
     <code>
      LATIN2
     </code>
     ,
     <code>
      LATIN9
     </code>
     , e
     <code>
      WIN1250
     </code>
     códigos de codificação.
     <a class="xref" href="unaccent.md" title="F.48. unaccent — a text search dictionary which removes diacritics">
      unaccent
     </a>
     um módulo para outra solução mais flexível.)
    </p>
    <p>
     <code>
      to_ascii('Karél')
     </code>
     →
     <code>
      Karel
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      to_bin
     </code>
     (
     <code>
      integer
     </code>
     )
     <code>
      text
     </code>
    </p>
    <p class="func_signature">
     <code>
      to_bin
     </code>
     (
     <code>
      bigint
     </code>
     )
     <code>
      text
     </code>
    </p>
    <p>
     Converte o número para sua representação binária equivalente ao complemento de dois.
    </p>
    <p>
     <code>
      to_bin(2147483647)
     </code>
     →
     <code>
      1111111111111111111111111111111
     </code>
    </p>
    <p>
     <code>
      to_bin(-1234)
     </code>
     →
     <code>
      11111111111111111111101100101110
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      to_hex
     </code>
     (
     <code>
      integer
     </code>
     )
     <code>
      text
     </code>
    </p>
    <p class="func_signature">
     <code>
      to_hex
     </code>
     (
     <code>
      bigint
     </code>
     )
     <code>
      text
     </code>
    </p>
    <p>
     Converte o número para sua representação hexadecimal equivalente em complemento de dois.
    </p>
    <p>
     <code>
      to_hex(2147483647)
     </code>
     →
     <code>
      7fffffff
     </code>
    </p>
    <p>
     <code>
      to_hex(-1234)
     </code>
     →
     <code>
      fffffb2e
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      to_oct
     </code>
     (
     <code>
      integer
     </code>
     )
     <code>
      text
     </code>
    </p>
    <p class="func_signature">
     <code>
      to_oct
     </code>
     (
     <code>
      bigint
     </code>
     )
     <code>
      text
     </code>
    </p>
    <p>
     Converte o número para sua representação equivalente octal de complemento de dois.
    </p>
    <p>
     <code>
      to_oct(2147483647)
     </code>
     →
     <code>
      17777777777
     </code>
    </p>
    <p>
     <code>
      to_oct(-1234)
     </code>
     →
     <code>
      37777775456
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      translate
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
       from
      </code>
     </em>
     <code>
      text
     </code>
     ,
     <em class="parameter">
      <code>
       to
      </code>
     </em>
     <code>
      text
     </code>
     )
     <code>
      text
     </code>
    </p>
    <p>
     Substitui cada caractere em
     <em class="parameter">
      <code>
       string
      </code>
     </em>
     que corresponde a um personagem no
     <em class="parameter">
      <code>
       from
      </code>
     </em>
     conjunto com o personagem correspondente no
     <em class="parameter">
      <code>
       to
      </code>
     </em>
     se o conjunto estiver definido.
     <em class="parameter">
      <code>
       from
      </code>
     </em>
     é mais longo do que
     <em class="parameter">
      <code>
       to
      </code>
     </em>
     , ocorrem os caracteres extras em
     <em class="parameter">
      <code>
       from
      </code>
     </em>
     são excluídos.
    </p>
    <p>
     <code>
      translate('12345', '143', 'ax')
     </code>
     →
     <code>
      a2x5
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      unistr
     </code>
     (
     <code>
      text
     </code>
     )
     <code>
      text
     </code>
    </p>
    <p>
     Avalie caracteres Unicode escapados no argumento. Caracteres Unicode podem ser especificados como
     <code>
      \
      <em class="replaceable">
       <code>
        XXXX
       </code>
      </em>
     </code>
     (4 dígitos hexadecimais),
     <code>
      \+
      <em class="replaceable">
       <code>
        XXXXXX
       </code>
      </em>
     </code>
     (6 dígitos hexadecimais),
     <code>
      \u
      <em class="replaceable">
       <code>
        XXXX
       </code>
      </em>
     </code>
     (4 dígitos hexadecimais), ou
     <code>
      \U
      <em class="replaceable">
       <code>
        XXXXXXXX
       </code>
      </em>
     </code>
     (8 dígitos hexadecimais). Para especificar uma barra invertida, escreva duas barras invertidas. Todos os outros caracteres são tomados literalmente.
    </p>
    <p>
     Se o codificação do servidor não for UTF-8, o ponto de código Unicode identificado por uma dessas sequências de escape é convertido para a codificação real do servidor; um erro é relatado se isso não for possível.
    </p>
    <p>
     Essa função oferece uma alternativa (não padrão) para constantes de cadeia com escapamentos de Unicode (consulte
     <a class="xref" href="sql-syntax-lexical.md#SQL-SYNTAX-STRINGS-UESCAPE" title="4.1.2.3. String Constants with Unicode Escapes">
      Seção 4.1.2.3
     </a>
     ).
    </p>
    <p>
     <code>
      unistr('d\0061t\+000061')
     </code>
     →
     <code>
      data
     </code>
    </p>
    <p>
     <code>
      unistr('d\u0061t\U00000061')
     </code>
     →
     <code>
      data
     </code>
    </p>
   </td>
  </tr>
 </tbody>
</table>

As funções `concat`, `concat_ws` e `format` são variáveis, portanto é possível passar os valores a serem concatenados ou formatados como um array marcado com a palavra-chave `VARIADIC` (ver [Seção 36.5.6](xfunc-sql.md#XFUNC-SQL-VARIADIC-FUNCTIONS "36.5.6. SQL Functions with Variable Numbers of Arguments")). Os elementos do array são tratados como se fossem argumentos comuns separados da função. Se o argumento do array variável for NULL, `concat` e `concat_ws` retornam NULL, mas `format` trata um NULL como um array de elemento zero.

Veja também a função agregada `string_agg` em [Seção 9.21](functions-aggregate.md "9.21. Aggregate Functions"), e as funções para conversão entre strings e o tipo `bytea` em [Tabela 9.13](functions-binarystring.md#FUNCTIONS-BINARYSTRING-CONVERSIONS "Table 9.13. Text/Binary String Conversion Functions").

#### 9.4.1. `format` [#](#FUNCTIONS-STRING-FORMAT)

A função `format` produz saída formatada de acordo com uma string de formato, em um estilo semelhante à função C `sprintf`.

```sql
format(formatstr text [, formatarg "any" [, ...] ])
```

*`formatstr`* é uma string de formato que especifica como o resultado deve ser formatado. O texto na string de formato é copiado diretamente para o resultado, exceto onde *especificadores de formato* são usados. Os especificadores de formato atuam como marcadores de posição na string, definindo como os argumentos subsequentes da função devem ser formatados e inseridos no resultado. Cada argumento *`formatarg`* é convertido em texto de acordo com as regras de saída usuais para seu tipo de dados, e então formatado e inserido na string de resultado de acordo com o(s) especificador(es) de formato.

Os especificadores de formato são introduzidos por um caractere `%` e têm a forma

```sql
%[position][flags][width]type
```

onde os campos componentes são:

*`position`* (opcional): Uma string na forma `n$` onde *`n`* é o índice do argumento a ser impresso. O índice 1 significa o primeiro argumento após *`formatstr`*. Se o *`position`* for omitido, o padrão é usar o próximo argumento na sequência.

*`flags`* (opcional): Opções adicionais que controlam a formatação da saída do especificador de formato. Atualmente, a única bandeira suportada é um sinal de menos (`-`) que fará com que a saída do especificador de formato seja alinhada à esquerda. Isso não tem efeito a menos que o campo *`width`* também seja especificado.

*`width`* (opcional): Especifica o *mínimo* número de caracteres a serem usados para exibir a saída do especificador de formato. A saída é preenchida à esquerda ou à direita (dependendo da bandeira `-`) com espaços conforme necessário para preencher a largura. Uma largura muito pequena não causa a redução da saída, mas é simplesmente ignorada. A largura pode ser especificada usando qualquer um dos seguintes: um número inteiro positivo; um asterisco (`*`) para usar o próximo argumento de função como a largura; ou uma string na forma `*n$` para usar o *`n`*º argumento de função como a largura.

Se a largura vier de um argumento de função, esse argumento é consumido antes do argumento que é usado para o valor do especificado de formato. Se o argumento de largura for negativo, o resultado é alinhado à esquerda (como se a bandeira `-` tivesse sido especificada) dentro de um campo de comprimento `abs`(*`width`*).

*`type`* (obrigatório): O tipo de conversão de formato a ser usado para produzir a saída do especificador de formato. Os seguintes tipos são suportados:

* `s` formata o valor do argumento como uma string simples. Um valor nulo é tratado como uma string vazia. * `I` trata o valor do argumento como um identificador SQL, colocando-o em aspas duplas, se necessário. É um erro que o valor seja nulo (equivalente a `quote_ident`). * `L` cita o valor do argumento como um literal SQL. Um valor nulo é exibido como a string `NULL`, sem aspas (equivalente a `quote_nullable`).

Além dos especificadores de formato descritos acima, a sequência especial `%%` pode ser usada para exibir um caractere literal `%`.

Aqui estão alguns exemplos das conversões de formato básico:

```sql
SELECT format('Hello %s', 'World');
Result: Hello World

SELECT format('Testing %s, %s, %s, %%', 'one', 'two', 'three');
Result: Testing one, two, three, %

SELECT format('INSERT INTO %I VALUES(%L)', 'Foo bar', E'O\'Reilly');
Result: INSERT INTO "Foo bar" VALUES('O''Reilly')

SELECT format('INSERT INTO %I VALUES(%L)', 'locations', 'C:\Program Files');
Result: INSERT INTO locations VALUES('C:\Program Files')
```

Aqui estão exemplos usando os campos *`width`* e a bandeira `-`:

```sql
SELECT format('|%10s|', 'foo');
Result: |       foo|

SELECT format('|%-10s|', 'foo');
Result: |foo       |

SELECT format('|%*s|', 10, 'foo');
Result: |       foo|

SELECT format('|%*s|', -10, 'foo');
Result: |foo       |

SELECT format('|%-*s|', 10, 'foo');
Result: |foo       |

SELECT format('|%-*s|', -10, 'foo');
Result: |foo       |
```

Esses exemplos mostram o uso dos campos *`position`*:

```sql
SELECT format('Testing %3$s, %2$s, %1$s', 'one', 'two', 'three');
Result: Testing three, two, one

SELECT format('|%*2$s|', 'foo', 10, 'bar');
Result: |       bar|

SELECT format('|%1$*2$s|', 'foo', 10, 'bar');
Result: |       foo|
```

Ao contrário da função padrão C `sprintf`, a função `format` do PostgreSQL permite que os especificadores de formato com e sem campos *`position`* sejam misturados na mesma string de formato. Um especificador de formato sem um campo *`position`* sempre usa o próximo argumento após o último argumento consumido. Além disso, a função `format` não exige que todos os argumentos da função sejam usados na string de formato. Por exemplo:

```sql
SELECT format('Testing %3$s, %2$s, %s', 'one', 'two', 'three');
Result: Testing three, two, three
```

Os especificadores de formato `%I` e `%L` são particularmente úteis para a construção segura de declarações SQL dinâmicas. Veja [Exemplo 41.1](plpgsql-statements.md#PLPGSQL-QUOTE-LITERAL-EXAMPLE).