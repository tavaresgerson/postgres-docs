## 8.3. Tipos de Personagem [#](#DATATYPE-CHARACTER)

**Tabela 8.4. Tipos de Caracteres**



<table border="1" class="table" summary="Character Types">
<colgroup>
<col/>
<col/>
</colgroup>
<thead>
<tr>
<th>Nome</th>
<th>Descrição</th>
</tr>
</thead>
<tbody>
<tr>
<td>
<code class="type">
     character varying(
     <em class="replaceable">
<code>
       n
      </code>
</em>
     )
    </code>,<code class="type">
     varchar(
     <em class="replaceable">
<code>
       n
      </code>
</em>
     )
    </code>
</td>
<td>com comprimento variável e limite</td>
</tr>
<tr>
<td>
<code class="type">
     character(
     <em class="replaceable">
<code>
       n
      </code>
</em>
     )
    </code>,<code class="type">
     char(
     <em class="replaceable">
<code>
       n
      </code>
</em>
     )
    </code>,<code class="type">
     bpchar(
     <em class="replaceable">
<code>
       n
      </code>
</em>
     )
    </code>
</td>
<td>de comprimento fixo, com revestimento em branco</td>
</tr>
<tr>
<td>
<code class="type">
     bpchar
    </code>
</td>
<td>variável de comprimento ilimitado, com recorte em branco</td>
</tr>
<tr>
<td>
<code class="type">
     text
    </code>
</td>
<td>variável de comprimento ilimitado</td>
</tr>
</tbody>
</table>




  

[Tabela 8.4][(datatype-character.md#DATATYPE-CHARACTER-TABLE "Table 8.4. Character Types")] mostra os tipos de caracteres de propósito geral disponíveis no PostgreSQL.

O SQL define dois tipos de caracteres principais: `character varying(n)` e `character(n)`, onde *`n`* é um inteiro positivo. Ambos esses tipos podem armazenar strings com até *`n`* caracteres (não bytes) de comprimento. Uma tentativa de armazenar uma string mais longa em uma coluna desses tipos resultará em um erro, a menos que os excessos de caracteres sejam todos espaços, no qual caso a string será truncada até o comprimento máximo. (Essa exceção um tanto bizarra é exigida pelo padrão SQL.) No entanto, se uma pessoa explicitamente converter um valor para `character varying(n)` ou `character(n)`, então um valor de comprimento excessivo será truncado para *`n`* caracteres sem levantar um erro. (Isso também é exigido pelo padrão SQL.) Se a string a ser armazenada for mais curta que o comprimento declarado, os valores do tipo `character` serão preenchidos com espaços; os valores do tipo `character varying` simplesmente armazenarão a string mais curta.

Além disso, o PostgreSQL fornece o tipo `text`, que armazena cadeias de qualquer comprimento. Embora o tipo `text` não esteja no padrão SQL, vários outros sistemas de gerenciamento de banco de dados SQL também o possuem. `text` é o tipo de dados nativo de cadeia do PostgreSQL, pois a maioria das funções embutidas que operam em cadeias é declarada para receber ou retornar `text` e não `character varying`. Para muitos propósitos, `character varying` age como se fosse um [domínio](domains.md "8.18. Domain Types") sobre `text`.

O nome do tipo `varchar` é um alias para `character varying`, enquanto `bpchar` (com especificador de comprimento) e `char` são aliases para `character`. Os aliases `varchar` e `char` são definidos no padrão SQL; `bpchar` é uma extensão do PostgreSQL.

Se especificado, o comprimento *`n`* deve ser maior que zero e não pode exceder 10.485.760. Se `character varying` (ou `varchar`) é usado sem especificar comprimento, o tipo aceita cadeias de qualquer comprimento. Se `bpchar` não tem um especificador de comprimento, ele também aceita cadeias de qualquer comprimento, mas espaços finais são semanticamente insignificantes. Se `character` (ou `char`) não tem um especificador, é equivalente a `character(1)`.

Os valores do tipo `character` são preenchidos fisicamente com espaços até a largura especificada *`n`*, e são armazenados e exibidos dessa forma. No entanto, os espaços finais são tratados como semanticamente insignificantes e ignorados ao comparar dois valores do tipo `character`. Em colas onde o espaço em branco é significativo, esse comportamento pode produzir resultados inesperados; por exemplo, `SELECT 'a '::CHAR(2) collate "C" < E'a\n'::CHAR(2)` retorna verdadeiro, mesmo que o local `C` considere um espaço maior que uma nova linha. Os espaços finais são removidos ao converter um valor de `character` para um dos outros tipos de string. Note que os espaços finais *são* semanticamente significativos nos valores de `character varying` e `text`, e ao usar correspondência de padrões, ou seja, `LIKE` e expressões regulares.

Os caracteres que podem ser armazenados em qualquer um desses tipos de dados são determinados pelo conjunto de caracteres do banco de dados, que é selecionado quando o banco de dados é criado. Independentemente do conjunto de caracteres específico, o caractere com código zero (às vezes chamado de NUL) não pode ser armazenado. Para mais informações, consulte [Seção 23.3][(multibyte.md "23.3. Character Set Support")].

O requisito de armazenamento para uma string curta (até 126 bytes) é de 1 byte mais a própria string, o que inclui o preenchimento de espaço no caso de `character`. Strings mais longas têm 4 bytes de sobrecarga em vez de 1. As strings longas são comprimidas automaticamente pelo sistema, então o requisito físico no disco pode ser menor. Valores muito longos também são armazenados em tabelas de segundo plano para que não interfiram no acesso rápido a valores de colunas mais curtas. Em qualquer caso, a string de caracteres mais longa possível que pode ser armazenada é de cerca de 1 GB. (O valor máximo que será permitido para *`n`* na declaração do tipo de dados é menor que esse. Não seria útil mudar isso porque, com codificações de caracteres multibyte, o número de caracteres e bytes pode ser bastante diferente. Se você deseja armazenar strings longas sem um limite superior específico, use `text` ou `character varying` sem um especificado de comprimento, em vez de criar um limite de comprimento arbitrário.)

### DICA

Não há diferença de desempenho entre esses três tipos, exceto pelo aumento do espaço de armazenamento ao usar o tipo preenchido com branco, e alguns ciclos de CPU adicionais para verificar o comprimento ao armazenar em uma coluna com comprimento limitado. Embora o `character(n)` tenha vantagens de desempenho em alguns outros sistemas de banco de dados, não há tal vantagem no PostgreSQL; de fato, o `character(n)` é geralmente o mais lento dos três devido aos seus custos de armazenamento adicionais. Na maioria das situações, o `text` ou o `character varying` deve ser usado em vez disso.

Consulte a [Seção 4.1.2.1][(sql-syntax-lexical.md#SQL-SYNTAX-STRINGS "4.1.2.1. String Constants")] para obter informações sobre a sintaxe de literais de cadeia, e consulte o [Capítulo 9][(functions.md "Chapter 9. Functions and Operators")] para obter informações sobre os operadores e funções disponíveis.

**Exemplo 8.1. Usando os Tipos de Caracteres**

```
CREATE TABLE test1 (a character(4));
INSERT INTO test1 VALUES ('ok');
SELECT a, char_length(a) FROM test1; -- (1)

  a   | char_length
------+-------------
 ok   |           2


CREATE TABLE test2 (b varchar(5));
INSERT INTO test2 VALUES ('ok');
INSERT INTO test2 VALUES ('good      ');
INSERT INTO test2 VALUES ('too long');
ERROR:  value too long for type character varying(5)
INSERT INTO test2 VALUES ('too long'::varchar(5)); -- explicit truncation
SELECT b, char_length(b) FROM test2;

   b   | char_length
-------+-------------
 ok    |           2
 good  |           5
 too l |           5
```



<table border="0" summary="Callout list">
<tr>
<td align="left" valign="top" width="5%">
<p>
<a href="#co.datatype-char">
     (1)
    </a>
</p>
</td>
<td align="left" valign="top">
<p>
    The
    <code class="function">
     char_length
    </code>
    function is discussed in
    <a class="xref" href="functions-string.md" title="9.4. String Functions and Operators">
     Section 9.4
    </a>
    .
   </p>
</td>
</tr>
</table>




  

Existem outros dois tipos de caracteres de comprimento fixo no PostgreSQL, mostrados em [Tabela 8.5][(datatype-character.md#DATATYPE-CHARACTER-SPECIAL-TABLE "Table 8.5. Special Character Types")]. Estes não são destinados ao uso geral, apenas para uso nos catálogos internos do sistema. O tipo `name` é usado para armazenar identificadores. Seu comprimento é atualmente definido como 64 bytes (63 caracteres utilizáveis mais o terminador) mas deve ser referenciado usando a constante `NAMEDATALEN` no código-fonte `C`. O comprimento é definido no momento da compilação (e, portanto, é ajustável para usos especiais); o comprimento máximo padrão pode mudar em uma versão futura. O tipo `"char"` (note as aspas) é diferente de `char(1)` na medida em que ele usa apenas um byte de armazenamento, e, portanto, pode armazenar apenas um único caractere ASCII. Ele é usado nos catálogos do sistema como um tipo de enumeração simplista.

**Tabela 8.5. Tipos de Caracteres Especiais**



<table border="1" class="table" summary="Special Character Types">
<colgroup>
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
    Storage Size
   </th>
<th>Descrição</th>
</tr>
</thead>
<tbody>
<tr>
<td>
<code class="type">
     "char"
    </code>
</td>
<td>
    1 byte
   </td>
<td>tipo interno de byte único</td>
</tr>
<tr>
<td>
<code class="type">
     name
    </code>
</td>
<td>
    64 bytes
   </td>
<td>tipo interno para nomes de objetos</td>
</tr>
</tbody>
</table>

