## F.20. isn — tipos de dados para números padrão internacional (ISBN, EAN, UPC, etc.) [#](#ISN)

* [F.20.1. Tipos de Dados](isn.md#ISN-DATA-TYPES)
* [F.20.2. Casts](isn.md#ISN-CASTS)
* [F.20.3. Funções e Operadores](isn.md#ISN-FUNCS-OPS)
* [F.20.4. Parâmetros de Configuração](isn.md#ISN-CONFIGURATION-PARAMETERS)
* [F.20.5. Exemplos](isn.md#ISN-EXAMPLES)
* [F.20.6. Bibliografia](isn.md#ISN-BIBLIOGRAPHY)
* [F.20.7. Autor](isn.md#ISN-AUTHOR)

O módulo `isn` fornece tipos de dados para os seguintes padrões de numeração de produtos internacionais: EAN13, UPC, ISBN (livros) e ISSN (revistas). Os números são validados na entrada de acordo com uma lista de prefixos codificada; essa lista de prefixos também é usada para separar os números na saída. Como novos prefixos são atribuídos de tempos em tempos, a lista de prefixos pode estar desatualizada. Espera-se que uma versão futura deste módulo obtenha a lista de prefixos de uma ou mais tabelas que podem ser facilmente atualizadas pelos usuários conforme necessário; no entanto, atualmente, a lista só pode ser atualizada modificando o código-fonte e recompilando. Alternativamente, o suporte à validação e separação de prefixos pode ser eliminado de uma versão futura deste módulo.

Este módulo é considerado "confiável", ou seja, pode ser instalado por usuários não superusuários que possuem privilégio `CREATE` no banco de dados atual.

### F.20.1. Tipos de dados [#](#ISN-DATA-TYPES)

[Tabela F.10](isn.md#ISN-DATATYPES "Table F.10. isn Data Types") mostra os tipos de dados fornecidos pelo módulo `isn`.

**Tabela F.10. Tipos de dados `isn`**



<table>
 <colgroup>
  <col class="col1"/>
  <col class="col2"/>
 </colgroup>
 <thead>
  <tr>
   <th>
    Data Type
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
     EAN13
    </code>
   </td>
   <td>
    Números de artigos europeus, sempre exibidos no formato de exibição EAN13
   </td>
  </tr>
  <tr>
   <td>
    <code>
     ISBN13
    </code>
   </td>
   <td>
    Números internacionais padrão de livro a serem exibidos no novo formato de exibição EAN13
   </td>
  </tr>
  <tr>
   <td>
    <code>
     ISMN13
    </code>
   </td>
   <td>
    Números internacionais padrão de música serão exibidos no novo formato de exibição EAN13
   </td>
  </tr>
  <tr>
   <td>
    <code>
     ISSN13
    </code>
   </td>
   <td>
    Números de série serial internacional a serem exibidos no novo formato de exibição EAN13
   </td>
  </tr>
  <tr>
   <td>
    <code>
     ISBN
    </code>
   </td>
   <td>
    Números internacionais padrão de livro a serem exibidos no antigo formato de exibição curta
   </td>
  </tr>
  <tr>
   <td>
    <code>
     ISMN
    </code>
   </td>
   <td>
    Números internacionais de música padrão serão exibidos no antigo formato de exibição curta
   </td>
  </tr>
  <tr>
   <td>
    <code>
     ISSN
    </code>
   </td>
   <td>
    Números de série serial internacional a serem exibidos no antigo formato de exibição curta
   </td>
  </tr>
  <tr>
   <td>
    <code>
     UPC
    </code>
   </td>
   <td>
    Códigos de Produto Universal
   </td>
  </tr>
 </tbody>
</table>










Algumas notas:

Os números ISBN13, ISMN13 e ISSN13 são todos números EAN13. Os números EAN13 nem sempre são ISBN13, ISMN13 ou ISSN13 (alguns são). Alguns números ISBN13 podem ser exibidos como ISBN. Alguns números ISMN13 podem ser exibidos como ISMN. Alguns números ISSN13 podem ser exibidos como ISSN. Os números UPC são um subconjunto dos números EAN13 (eles são basicamente EAN13 sem o primeiro dígito `0`). Todos os números UPC, ISBN, ISMN e ISSN podem ser representados como números EAN13.

Internamente, todos esses tipos utilizam a mesma representação (um inteiro de 64 bits) e todos são intercambiáveis. Múltiplos tipos são fornecidos para controlar a formatação de exibição e para permitir uma verificação mais rigorosa da validade da entrada que deve denotar um tipo particular de número.

Os tipos `ISBN`, `ISMN` e `ISSN` exibirão a versão curta do número (ISxN 10) sempre que possível e mostrarão o formato ISxN 13 para números que não se encaixam na versão curta. Os tipos `EAN13`, `ISBN13`, `ISMN13` e `ISSN13` sempre exibirão a versão longa do ISxN (EAN13).

### F.20.2. Fundições [#](#ISN-CASTS)

O módulo `isn` fornece os seguintes pares de tipos de conversão:

* ISBN13 <=> EAN13
* ISMN13 <=> EAN13
* ISSN13 <=> EAN13
* ISBN <=> EAN13
* ISMN <=> EAN13
* ISSN <=> EAN13
* UPC <=> EAN13
* ISBN <=> ISBN13
* ISMN <=> ISMN13
* ISSN <=> ISSN13

Ao fazer uma conversão de `EAN13` para outro tipo, há uma verificação de tempo de execução de que o valor está dentro do domínio do outro tipo, e um erro é lançado se não estiver. Os outros tipos de conversão são simplesmente redefinições que sempre terão sucesso.

### F.20.3. Funções e Operadores [#](#ISN-FUNCS-OPS)

O módulo `isn` fornece os operadores de comparação padrão, além do suporte a índice B-tree e hash para todos esses tipos de dados. Além disso, há várias funções especializadas, mostradas na [Tabela F.11](isn.md#ISN-FUNCTIONS). Nesta tabela, `isn` significa qualquer um dos tipos de dados do módulo.

**Tabela F.11. `isn` Funções**



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
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      make_valid
     </code>
     (
     <code>
      isn
     </code>
     ) →
     <code>
      isn
     </code>
    </p>
    <p>
     Clears the invalid-check-digit flag of the value.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      is_valid
     </code>
     (
     <code>
      isn
     </code>
     ) →
     <code>
      boolean
     </code>
    </p>
    <p>
     Checks for the presence of the invalid-check-digit flag.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      isn_weak
     </code>
     (
     <code>
      boolean
     </code>
     ) →
     <code>
      boolean
     </code>
    </p>
    <p>
     Sets the weak input mode, and returns the new setting. This function is retained for backward compatibility. The recommended way to set weak mode is via the
     <code>
      isn.weak
     </code>
     configuration parameter.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      isn_weak
     </code>
     () →
     <code>
      boolean
     </code>
    </p>
    <p>
     Returns the current status of the weak mode. This function is retained for backward compatibility. The recommended way to check weak mode is via the
     <code>
      isn.weak
     </code>
     configuration parameter.
    </p>
   </td>
  </tr>
 </tbody>
</table>







### F.20.4. Parâmetros de Configuração [#](#ISN-CONFIGURATION-PARAMETERS)

`isn.weak` (`boolean`) [#](#ISN-CONFIGURATION-PARAMETERS-WEAK): `isn.weak` habilita o modo de entrada fraca, que permite que os valores de entrada do ISN sejam aceitos mesmo quando seu dígito de verificação está errado. O padrão é `false`, que rejeita dígitos de verificação inválidos.

Por que você gostaria de usar o modo fraco? Bem, pode ser que você tenha uma enorme coleção de números ISBN, e que haja tantos deles que, por razões estranhas, alguns têm o dígito de verificação errado (talvez os números tenham sido digitalizados de uma lista impressa e o OCR tenha errado os números, talvez os números tenham sido capturados manualmente... quem sabe). De qualquer forma, o ponto é que você pode querer limpar a confusão, mas ainda quer ser capaz de ter todos os números em seu banco de dados e, talvez, usar uma ferramenta externa para localizar os números inválidos no banco de dados, para que você possa verificar as informações e validá-las mais facilmente; por exemplo, você gostaria de selecionar todos os números inválidos na tabela.

Quando você inserir números inválidos em uma tabela usando o modo fraco, o número será inserido com o dígito de verificação corrigido, mas será exibido com um ponto de exclamação (`!`) no final, por exemplo, `0-11-000322-5!`. Esse marcador inválido pode ser verificado com a função `is_valid` e apagado com a função `make_valid`.

Você também pode forçar a inserção de números marcados como inválidos, mesmo quando não estiver no modo fraco, anexando o caractere `!` no final do número.

Outra característica especial é que, durante a digitação, você pode escrever `?` no lugar do algarismo de verificação, e o algarismo de verificação correto será inserido automaticamente.

### F.20.5. Exemplos [#](#ISN-EXAMPLES)

```
--Using the types directly:
SELECT isbn('978-0-393-04002-9');
SELECT isbn13('0901690546');
SELECT issn('1436-4522');

--Casting types:
-- note that you can only cast from ean13 to another type when the
-- number would be valid in the realm of the target type;
-- thus, the following will NOT work: select isbn(ean13('0220356483481'));
-- but these will:
SELECT upc(ean13('0220356483481'));
SELECT ean13(upc('220356483481'));

--Create a table with a single column to hold ISBN numbers:
CREATE TABLE test (id isbn);
INSERT INTO test VALUES('9780393040029');

--Automatically calculate check digits (observe the '?'):
INSERT INTO test VALUES('220500896?');
INSERT INTO test VALUES('978055215372?');

SELECT issn('3251231?');
SELECT ismn('979047213542?');

--Using the weak mode:
SET isn.weak TO true;
INSERT INTO test VALUES('978-0-11-000533-4');
INSERT INTO test VALUES('9780141219307');
INSERT INTO test VALUES('2-205-00876-X');
SET isn.weak TO false;

SELECT id FROM test WHERE NOT is_valid(id);
UPDATE test SET id = make_valid(id) WHERE id = '2-205-00876-X!';

SELECT * FROM test;

SELECT isbn13(id) FROM test;
```

### F.20.6. Bibliografia [#](#ISN-BIBLIOGRAPHY)

As informações para implementar este módulo foram coletadas de vários sites, incluindo:

* <https://www.isbn-international.org/>
* <https://www.issn.org/>
* <https://www.ismn-international.org/>
* <https://www.wikipedia.org/>

Os prefixos utilizados para a ligação por hífen também foram compilados a partir de:

* <https://www.gs1.org/standards/id-keys>
* <https://en.wikipedia.org/wiki/List_of_ISBN_registration_groups>
* <https://www.isbn-international.org/content/isbn-users-manual/29>
* <https://en.wikipedia.org/wiki/International_Standard_Music_Number>
* <https://www.ismn-international.org/ranges/tools>

Foi dada atenção durante a criação dos algoritmos e eles foram meticulosamente verificados em relação aos algoritmos sugeridos nos manuais oficiais do ISBN, ISMN e ISSN.

### F.20.7. Autor [#](#ISN-AUTHOR)

Germán Méndez Bravo (Kronuz), 2004–2006

Este módulo foi inspirado no código `isbn_issn` de Garrett A. Wollman.