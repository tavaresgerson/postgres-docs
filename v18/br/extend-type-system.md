## 36.2. O sistema de tipos do PostgreSQL [#](#EXTEND-TYPE-SYSTEM)

* [36.2.1. Tipos de Base][(extend-type-system.md#EXTEND-TYPE-SYSTEM-BASE)
* [36.2.2. Tipos de Contêiner][(extend-type-system.md#EXTEND-TYPE-SYSTEM-CONTAINER)
* [36.2.3. Domínios][(extend-type-system.md#EXTEND-TYPE-SYSTEM-DOMAINS)
* [36.2.4. Pseudo-Tipos][(extend-type-system.md#EXTEND-TYPE-SYSTEM-PSEUDO)
* [36.2.5. Tipos Polimorficos][(extend-type-system.md#EXTEND-TYPES-POLYMORPHIC)

Os tipos de dados do PostgreSQL podem ser divididos em tipos básicos, tipos de contenção, domínios e pseudotipos.

### 36.2.1. Tipos de base [#](#EXTEND-TYPE-SYSTEM-BASE)

Os tipos de base são aqueles, como `integer`, que são implementados abaixo do nível da linguagem SQL (tipicamente em uma linguagem de baixo nível, como C). Eles geralmente correspondem ao que é frequentemente conhecido como tipos de dados abstratos. O PostgreSQL só pode operar com esses tipos por meio de funções fornecidas pelo usuário e só entende o comportamento desses tipos na medida em que o usuário os descreve. Os tipos de base embutidos são descritos em [Capítulo 8][(datatype.md "Chapter 8. Data Types")].

Os tipos enumerados (enum) podem ser considerados uma subcategoria dos tipos básicos. A principal diferença é que eles podem ser criados usando apenas comandos SQL, sem qualquer programação de nível baixo. Consulte [Seção 8.7][(datatype-enum.md "8.7. Enumerated Types")] para mais informações.

### 36.2.2. Tipos de contêineres [#](#EXTEND-TYPE-SYSTEM-CONTAINER)

O PostgreSQL tem três tipos de "contêiner", que são tipos que contêm múltiplos valores de outros tipos. São eles: arrays, compostos e intervalos.

Os arrays podem conter múltiplos valores que são todos do mesmo tipo. Um tipo de array é criado automaticamente para cada tipo de base, tipo composto, tipo de intervalo e tipo de domínio. Mas não existem arrays de arrays. No que diz respeito ao sistema de tipos, arrays multidimensionais são os mesmos que arrays unidimensionais. Consulte [Seção 8.15][(arrays.md "8.15. Arrays")] para mais informações.

Os tipos compostos, ou tipos de linha, são criados sempre que o usuário cria uma tabela. Também é possível usar [CREATE TYPE][(sql-createtype.md "CREATE TYPE")] para definir um tipo composto "autônomo" sem uma tabela associada. Um tipo composto é simplesmente uma lista de tipos com nomes de campos associados. Um valor de um tipo composto é uma linha ou registro de valores de campo. Consulte [Seção 8.16][(rowtypes.md "8.16. Composite Types")] para obter mais informações.

Um tipo de intervalo pode conter dois valores do mesmo tipo, que são os limites inferior e superior do intervalo. Os tipos de intervalo são criados pelo usuário, embora existam alguns pré-definidos. Consulte [Seção 8.17][(rangetypes.md "8.17. Range Types")] para obter mais informações.

### 36.2.3. Domínios [#](#EXTEND-TYPE-SYSTEM-DOMAINS)

Um domínio é baseado em um tipo subjacente específico e, para muitos propósitos, é intercambiável com seu tipo subjacente. No entanto, um domínio pode ter restrições que restringem seus valores válidos a um subconjunto do que o tipo subjacente permitiria. Domínios são criados usando o comando SQL [CREATE DOMAIN](sql-createdomain.md "CREATE DOMAIN"). Consulte [Seção 8.18](domains.md "8.18. Domain Types") para mais informações.

### 36.2.4. Pseudotípicos [#](#EXTEND-TYPE-SYSTEM-PSEUDO)

Existem alguns “pseudotipos” para fins especiais. Pseudotipos não podem aparecer como colunas de tabelas ou componentes de tipos de contêiner, mas podem ser usados para declarar os tipos de argumento e resultado de funções. Isso fornece um mecanismo dentro do sistema de tipos para identificar classes especiais de funções. A Tabela 8.27 (datatype-pseudo.md#DATATYPE-PSEUDOTYPES-TABLE "Table 8.27. Pseudo-Types") lista os pseudotipos existentes.

### 36.2.5. Tipos polimórficos [#](#EXTEND-TYPES-POLYMORPHIC)

Alguns pseudotipos de interesse especial são os *tipos polimórficos*, que são usados para declarar *funções polimórficas*. Este recurso poderoso permite que uma única definição de função opere em muitos tipos de dados diferentes, com o(s) tipo(s) de dados específico(s) sendo determinado(s) pelos tipos de dados que são realmente passados para ele em uma chamada particular. Os tipos polimórficos são mostrados em [Tabela 36.1][(extend-type-system.md#EXTEND-TYPES-POLYMORPHIC-TABLE "Table 36.1. Polymorphic Types")]. Alguns exemplos de seu uso aparecem em [Seção 36.5.11][(xfunc-sql.md#XFUNC-SQL-POLYMORPHIC-FUNCTIONS "36.5.11. Polymorphic SQL Functions")].

**Tabela 36.1. Tipos polimórficos**



<table border="1" class="table" summary="Polymorphic Types">
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
    Family
   </th>
<th>Descrição</th>
</tr>
</thead>
<tbody>
<tr>
<td>
<code class="type">
     anyelement
    </code>
</td>
<td>
    Simple
   </td>
<td>Indica que uma função aceita qualquer tipo de dados</td>
</tr>
<tr>
<td>
<code class="type">
     anyarray
    </code>
</td>
<td>
    Simple
   </td>
<td>Indica que uma função aceita qualquer tipo de dados de matriz</td>
</tr>
<tr>
<td>
<code class="type">
     anynonarray
    </code>
</td>
<td>
    Simple
   </td>
<td>Indica que uma função aceita qualquer tipo de dados que não seja um array</td>
</tr>
<tr>
<td>
<code class="type">
     anyenum
    </code>
</td>
<td>
    Simple
   </td>
<td>Indica que uma função aceita qualquer tipo de dados enum<a class="xref" href="datatype-enum.md" title="8.7. Enumerated Types">Seção 8.7</a>)</td>
</tr>
<tr>
<td>
<code class="type">
     anyrange
    </code>
</td>
<td>
    Simple
   </td>
<td>Indica que uma função aceita qualquer tipo de dados de intervalo<a class="xref" href="rangetypes.md" title="8.17. Range Types">Seção 8.17</a>)</td>
</tr>
<tr>
<td>
<code class="type">
     anymultirange
    </code>
</td>
<td>
    Simple
   </td>
<td>Indica que uma função aceita qualquer tipo de dados multirange (consulte<a class="xref" href="rangetypes.md" title="8.17. Range Types">Seção 8.17</a>)</td>
</tr>
<tr>
<td>
<code class="type">
     anycompatible
    </code>
</td>
<td>
    Common
   </td>
<td>Indica que uma função aceita qualquer tipo de dados, com promoção automática de múltiplos argumentos para um tipo de dados comum</td>
</tr>
<tr>
<td>
<code class="type">
     anycompatiblearray
    </code>
</td>
<td>
    Common
   </td>
<td>Indica que uma função aceita qualquer tipo de dados de matriz,
com promoção automática de múltiplos argumentos para um tipo de dados comum</td>
</tr>
<tr>
<td>
<code class="type">
     anycompatiblenonarray
    </code>
</td>
<td>
    Common
   </td>
<td>Indica que uma função aceita qualquer tipo de dados que não seja um array,
com promoção automática de múltiplos argumentos para um tipo de dados comum</td>
</tr>
<tr>
<td>
<code class="type">
     anycompatiblerange
    </code>
</td>
<td>
    Common
   </td>
<td>Indica que uma função aceita qualquer tipo de dados de intervalo,
com promoção automática de múltiplos argumentos para um tipo de dados comum</td>
</tr>
<tr>
<td>
<code class="type">
     anycompatiblemultirange
    </code>
</td>
<td>
    Common
   </td>
<td>Indica que uma função aceita qualquer tipo de dados multirange,
com promoção automática de múltiplos argumentos para um tipo de dados comum</td>
</tr>
</tbody>
</table>




  

Os argumentos e resultados polimórficos estão ligados entre si e são resolvidos para tipos de dados específicos quando uma consulta que chama uma função polimórfica é analisada. Quando há mais de um argumento polimórfico, os tipos de dados reais dos valores de entrada devem corresponder conforme descrito abaixo. Se o tipo de resultado do resultado da função é polimórfico, ou tem parâmetros de saída de tipos polimórficos, os tipos desses resultados são deduzidos dos tipos reais dos inputs polimórficos conforme descrito abaixo.

Para a “simples” família de tipos polimórficos, as regras de correspondência e dedução funcionam da seguinte forma:

Cada posição (seja argumento ou valor de retorno) declarada como `anyelement` pode ter qualquer tipo de dado específico, mas em qualquer chamada, todos eles devem ser o *mesmo* tipo de dado. Cada posição declarada como `anyarray` pode ter qualquer tipo de dados de matriz, mas de forma semelhante, todos eles devem ser o mesmo tipo. E, de forma semelhante, as posições declaradas como `anyrange` devem ser todos do mesmo tipo de intervalo. Da mesma forma para `anymultirange`.

Além disso, se houver posições declaradas `anyarray` e outras declaradas `anyelement`, o tipo de matriz real nas posições `anyarray` deve ser uma matriz cujos elementos sejam do mesmo tipo que aparece nas posições `anyelement`. `anynonarray` é tratado exatamente da mesma forma que `anyelement`, mas adiciona a restrição adicional de que o tipo real não deve ser um tipo de matriz. `anyenum` é tratado exatamente da mesma forma que `anyelement`, mas adiciona a restrição adicional de que o tipo real deve ser um tipo de enum.

Da mesma forma, se houver posições declaradas `anyrange` e outras declaradas `anyelement` ou `anyarray`, o tipo de intervalo real nas posições `anyrange` deve ser um intervalo cujo subtipo seja o mesmo tipo que aparece nas posições `anyelement` e o mesmo que o tipo de elemento das posições `anyarray`. Se houver posições declaradas `anymultirange`, seu tipo de multiintervalo real deve conter intervalos que correspondam aos parâmetros declarados `anyrange` e elementos básicos que correspondam aos parâmetros declarados `anyelement` e `anyarray`.

Assim, quando mais de uma posição de argumento é declarada com um tipo polimórfico, o efeito líquido é que apenas certas combinações de tipos de argumento reais são permitidas. Por exemplo, uma função declarada como `equal(anyelement, anyelement)` receberá quaisquer dois valores de entrada, desde que sejam do mesmo tipo de dados.

Quando o valor de retorno de uma função é declarado como um tipo polimórfico, deve haver pelo menos uma posição de argumento que também seja polimórfica, e os tipos de dados reais fornecidos para os argumentos polimórficos determinam o tipo de resultado real para essa chamada. Por exemplo, se não houvesse já um mecanismo de subscrito de matriz, poderia-se definir uma função que implemente o subscrito como `subscript(anyarray, integer) returns anyelement`. Essa declaração restringe o argumento real inicial a ser um tipo de matriz e permite que o analisador infira o tipo de resultado correto a partir do tipo do argumento inicial real. Outro exemplo é que uma função declarada como `f(anyarray) returns anyenum` só aceitará matrizes de tipos enum.

Na maioria dos casos, o analisador pode inferir o tipo de dado real para um tipo de resultado polimórfico a partir de argumentos que são de um tipo polimórfico diferente na mesma família; por exemplo, `anyarray` pode ser deduzido de `anyelement` ou vice-versa. Uma exceção é que um resultado polimórfico do tipo `anyrange` requer um argumento do tipo `anyrange`; ele não pode ser deduzido de argumentos de `anyarray` ou `anyelement`. Isso ocorre porque pode haver vários tipos de intervalo com o mesmo subtipo.

Observe que `anynonarray` e `anyenum` não representam variáveis de tipo separadas; eles são o mesmo tipo que `anyelement`, apenas com uma restrição adicional. Por exemplo, declarar uma função como `f(anyelement, anyenum)` é equivalente a declará-la como `f(anyenum, anyenum)`: ambos os argumentos reais devem ser do mesmo tipo de enum.

Para a família "comum" de tipos polimórficos, as regras de correspondência e dedução funcionam aproximadamente da mesma forma que para a família "simples", com uma grande diferença: os tipos reais dos argumentos não precisam ser idênticos, desde que possam ser implicitamente convertidos em um único tipo comum. O tipo comum é selecionado seguindo as mesmas regras que para `UNION` e construções relacionadas (ver [Seção 10.5][(typeconv-union-case.md "10.5. UNION, CASE, and Related Constructs")]). A seleção do tipo comum considera os tipos reais dos `anycompatible` e `anycompatiblenonarray` entradas, os tipos de elemento de matriz dos `anycompatiblearray` entradas, os subtipos de intervalo dos `anycompatiblerange` entradas e os subtipos de multiintervalo dos `anycompatiblemultirange` entradas. Se `anycompatiblenonarray` estiver presente, então o tipo comum deve ser um tipo não de matriz. Uma vez que um tipo comum é identificado, os argumentos nas posições de `anycompatible` e `anycompatiblenonarray` são automaticamente convertidos nesse tipo, e os argumentos nas posições de `anycompatiblearray` são automaticamente convertidos para o tipo de matriz desse tipo.

Como não é possível selecionar um tipo de intervalo conhecendo apenas seu subtipo, o uso de `anycompatiblerange` e/ou `anycompatiblemultirange` exige que todos os argumentos declarados com esse tipo tenham o mesmo intervalo real e/ou tipo multiintervalo, e que o subtipo desse tipo concorde com o tipo comum selecionado, para que não seja necessária nenhuma conversão dos valores do intervalo. Assim como com `anyrange` e `anymultirange`, o uso de `anycompatiblerange` e `anymultirange` como tipo de resultado de função exige que haja um argumento `anycompatiblerange` ou `anycompatiblemultirange`.

Observe que não há um tipo `anycompatibleenum`. Esse tipo não seria muito útil, pois normalmente não há nenhum cast implícito para tipos de enum, o que significa que não haveria nenhuma maneira de resolver um tipo comum para entradas de enum diferentes.

As famílias polimórficas "simples" e "comuns" representam dois conjuntos independentes de variáveis de tipo. Considere, por exemplo:

```
CREATE FUNCTION myfunc(a anyelement, b anyelement,
                       c anycompatible, d anycompatible)
RETURNS anycompatible AS ...
```

Em uma chamada real desta função, os dois primeiros inputs devem ter exatamente o mesmo tipo. Os dois últimos inputs devem ser promovíveis para um tipo comum, mas este tipo não precisa ter nada a ver com o tipo dos dois primeiros inputs. O resultado terá o tipo comum dos dois últimos inputs.

Uma função variável (aquela que aceita um número variável de argumentos, como na [Seção 36.5.6][(xfunc-sql.md#XFUNC-SQL-VARIADIC-FUNCTIONS "36.5.6. SQL Functions with Variable Numbers of Arguments")]) pode ser polimórfica: isso é feito declarando seu último parâmetro como `VARIADIC` `anyarray` ou `VARIADIC` `anycompatiblearray`. Para fins de correspondência de argumentos e determinação do tipo de resultado real, essa função se comporta da mesma forma como se tivesse escrito o número apropriado de parâmetros `anynonarray` ou `anycompatiblenonarray`.