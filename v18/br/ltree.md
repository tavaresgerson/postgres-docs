## F.22. ltree — tipo de dados hierárquico semelhante a uma árvore [#](#LTREE)

* [F.22.1. Definições](ltree.md#LTREE-DEFINITIONS)
* [F.22.2. Operadores e Funções](ltree.md#LTREE-OPS-FUNCS)
* [F.22.3. Índices](ltree.md#LTREE-INDEXES)
* [F.22.4. Exemplo](ltree.md#LTREE-EXAMPLE)
* [F.22.5. Transformações](ltree.md#LTREE-TRANSFORMS)
* [F.22.6. Autores](ltree.md#LTREE-AUTHORS)

Este módulo implementa um tipo de dados `ltree` para representar rótulos de dados armazenados em uma estrutura hierárquica semelhante a uma árvore. São fornecidas facilidades extensas para pesquisar em árvores de rótulos.

Este módulo é considerado "confiável", ou seja, pode ser instalado por usuários não superusuários que possuem privilégio `CREATE` no banco de dados atual.

### F.22.1. Definições [#](#LTREE-DEFINITIONS)

Um * rótulo * é uma sequência de caracteres alfanuméricos, sublinhados e hífens. Os intervalos de caracteres alfanuméricos válidos dependem do local do banco de dados. Por exemplo, no local C, os caracteres `A-Za-z0-9_-` são permitidos. Os rótulos não podem ter mais de 1000 caracteres.

Exemplos: `42`, `Personal_Services`

Um *caminho de rótulo* é uma sequência de zero ou mais rótulos separados por pontos, por exemplo, `L1.L2.L3`, representando um caminho a partir da raiz de uma árvore hierárquica até um nó específico. O comprimento de um caminho de rótulo não pode exceder 65535 rótulos.

Exemplo: `Top.Countries.Europe.Russia`

O módulo `ltree` fornece vários tipos de dados:

* `ltree` armazena um caminho de rótulo.
* `lquery` representa um padrão semelhante a uma expressão regular para a correspondência de valores de `ltree`. Uma palavra simples corresponde a esse rótulo dentro de um caminho. Um símbolo estrela (`*`) corresponde a zero ou mais rótulos. Esses podem ser unidos com pontos para formar um padrão que deve corresponder a todo o caminho do rótulo. Por exemplo:

```
foo         Match the exact label path foo
*.foo.*     Match any label path containing the label foo
*.foo       Match any label path whose last label is foo
```

Tanto os símbolos de estrela quanto as palavras simples podem ser quantificados para restringir quantas etiquetas podem corresponder:

```
*{n}        Match exactly n labels
*{n,}       Match at least n labels
*{n,m}      Match at least n but not more than m labels
*{,m}       Match at most m labels — same as *{0,m}
foo{n,m}    Match at least n but not more than m occurrences of foo
foo{,}      Match any number of occurrences of foo, including zero
```

Na ausência de qualquer quantificador explícito, o padrão para um símbolo estrela é corresponder a qualquer número de rótulos (ou seja, `{,}`) enquanto o padrão para um item sem estrela é corresponder exatamente uma vez (ou seja, `{1}`).

Existem vários modificadores que podem ser colocados no final de um item não-estrelado `lquery` para torná-lo mais do que apenas uma correspondência exata:

```
@           Match case-insensitively, for example a@ matches A
*           Match any label with this prefix, for example foo* matches foobar
%           Match initial underscore-separated words
```

O comportamento do `%` é um pouco complicado. Ele tenta corresponder a palavras em vez de toda a etiqueta. Por exemplo, o `foo_bar%` corresponde ao `foo_bar_baz`, mas não ao `foo_barbaz`. Se combinado com o `*`, a correspondência de prefixo se aplica a cada palavra separadamente, por exemplo, o `foo_bar%*` corresponde ao `foo1_bar2_baz`, mas não ao `foo1_br2_baz`.

Além disso, você pode escrever vários itens não-estrelados possivelmente modificados separados por `|` (OU) para corresponder a qualquer um desses itens, e pode colocar `!` (NÃO) no início de um grupo não-estrelado para corresponder a qualquer rótulo que não corresponda a nenhuma das alternativas. Um quantificador, se houver, vai no final do grupo; isso significa um número determinado de correspondências para o grupo como um todo (ou seja, um número determinado de rótulos que correspondem ou não correspondem a nenhuma das alternativas).

Aqui está um exemplo com anotações de `lquery`:

```
Top.*{0,2}.sport*@.!football|tennis{1,}.Russ*|Spain
a.  b.     c.      d.                   e.
```

Essa consulta corresponderá a qualquer caminho de rótulo que:

1. começa com a etiqueta `Top`
2. e, em seguida, tem de zero a dois rótulos antes
3. de um rótulo começando com o prefixo sensível a maiúsculas ou minúsculas `sport`
4. então tem um ou mais rótulos, nenhum dos quais corresponde a `football` nem `tennis`
5. e, em seguida, termina com um rótulo começando com `Russ` ou correspondendo exatamente a `Spain`.
* `ltxtquery` representa um padrão semelhante a pesquisa de texto completo para correspondência a valores de `ltree`. Um valor de `ltxtquery` contém palavras, possivelmente com os modificadores `@`, `*`, `%` no final; os modificadores têm os mesmos significados que em `lquery`. As palavras podem ser combinadas com `&` (E), `|` (OU), `!` (NÃO) e parênteses. A principal diferença de `lquery` é que `ltxtquery` corresponde a palavras sem considerar sua posição no caminho do rótulo.

Aqui está um exemplo `ltxtquery`:

```
Europe & Russia*@ & !Transportation
```

Isso corresponderá a caminhos que contenham a etiqueta `Europe` e qualquer etiqueta que comece com `Russia` (independente da grafia), mas não caminhos que contenham a etiqueta `Transportation`. A localização dessas palavras dentro do caminho não é importante. Além disso, quando `%` é usado, a palavra pode ser correspondida a qualquer palavra separada por sublinhado dentro de uma etiqueta, independentemente da posição.

Nota: `ltxtquery` permite espaço em branco entre os símbolos, mas `ltree` e `lquery`

### F.22.2. Operadores e Funções [#](#LTREE-OPS-FUNCS)

O tipo `ltree` possui os operadores de comparação habituais `=`, `<>`, `<`, `>`, `<=`, `>=`. As ordenações de comparação são realizadas na ordem de uma travessia em árvore, com as crianças de um nó ordenadas pelo texto do rótulo. Além disso, os operadores especializados mostrados em [Tabela F.12](ltree.md#LTREE-OP-TABLE "Table F.12. ltree Operators") estão disponíveis.

**Tabela F.12. Operadores `ltree`**



<table border="1" class="table" summary="ltree Operators">
 <colgroup>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th class="func_table_entry">
    <p class="func_signature">
     Operador
    </p>
    <p>
     Descrição
    </p>
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="type">
      ltree
     </code>
     <code class="literal">
      @&gt;
     </code>
     <code class="type">
      ltree
     </code>
     →
     <code class="returnvalue">
      boolean
     </code>
    </p>
    <p>
     O argumento esquerdo é um antecessor do direito (ou igual)?
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="type">
      ltree
     </code>
     <code class="literal">
      &lt;@
     </code>
     <code class="type">
      ltree
     </code>
     →
     <code class="returnvalue">
      boolean
     </code>
    </p>
    <p>
     O argumento esquerdo é descendente do direito (ou é igual)?
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="type">
      ltree
     </code>
     <code class="literal">
      ~
     </code>
     <code class="type">
      lquery
     </code>
     →
     <code class="returnvalue">
      boolean
     </code>
    </p>
    <p class="func_signature">
     <code class="type">
      lquery
     </code>
     <code class="literal">
      ~
     </code>
     <code class="type">
      ltree
     </code>
     →
     <code class="returnvalue">
      boolean
     </code>
    </p>
    <p>
     Faz
     <code class="type">
      ltree
     </code>
     jogo
     <code class="type">
      lquery
     </code>
     ?
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="type">
      ltree
     </code>
     <code class="literal">
      ?
     </code>
     <code class="type">
      lquery[]
     </code>
     →
     <code class="returnvalue">
      boolean
     </code>
    </p>
    <p class="func_signature">
     <code class="type">
      lquery[]
     </code>
     <code class="literal">
      ?
     </code>
     <code class="type">
      ltree
     </code>
     →
     <code class="returnvalue">
      boolean
     </code>
    </p>
    <p>
     Faz
     <code class="type">
      ltree
     </code>
     corresponda a qualquer
     <code class="type">
      lquery
     </code>
     em linha?
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="type">
      ltree
     </code>
     <code class="literal">
      @
     </code>
     <code class="type">
      ltxtquery
     </code>
     →
     <code class="returnvalue">
      boolean
     </code>
    </p>
    <p class="func_signature">
     <code class="type">
      ltxtquery
     </code>
     <code class="literal">
      @
     </code>
     <code class="type">
      ltree
     </code>
     →
     <code class="returnvalue">
      boolean
     </code>
    </p>
    <p>
     Faz
     <code class="type">
      ltree
     </code>
     jogo
     <code class="type">
      ltxtquery
     </code>
     ?
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="type">
      ltree
     </code>
     <code class="literal">
      ||
     </code>
     <code class="type">
      ltree
     </code>
     →
     <code class="returnvalue">
      ltree
     </code>
    </p>
    <p>
     Concatenam
     <code class="type">
      ltree
     </code>
     paths.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="type">
      ltree
     </code>
     <code class="literal">
      ||
     </code>
     <code class="type">
      text
     </code>
     →
     <code class="returnvalue">
      ltree
     </code>
    </p>
    <p class="func_signature">
     <code class="type">
      text
     </code>
     <code class="literal">
      ||
     </code>
     <code class="type">
      ltree
     </code>
     →
     <code class="returnvalue">
      ltree
     </code>
    </p>
    <p>
     Converte texto em
     <code class="type">
      ltree
     </code>
     e concatenam.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="type">
      ltree[]
     </code>
     <code class="literal">
      @&gt;
     </code>
     <code class="type">
      ltree
     </code>
     →
     <code class="returnvalue">
      boolean
     </code>
    </p>
    <p class="func_signature">
     <code class="type">
      ltree
     </code>
     <code class="literal">
      &lt;@
     </code>
     <code class="type">
      ltree[]
     </code>
     →
     <code class="returnvalue">
      boolean
     </code>
    </p>
    <p>
     A matriz contém um antepassado de
     <code class="type">
      ltree
     </code>
     ?
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="type">
      ltree[]
     </code>
     <code class="literal">
      &lt;@
     </code>
     <code class="type">
      ltree
     </code>
     →
     <code class="returnvalue">
      boolean
     </code>
    </p>
    <p class="func_signature">
     <code class="type">
      ltree
     </code>
     <code class="literal">
      @&gt;
     </code>
     <code class="type">
      ltree[]
     </code>
     →
     <code class="returnvalue">
      boolean
     </code>
    </p>
    <p>
     A matriz contém um descendente de
     <code class="type">
      ltree
     </code>
     ?
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="type">
      ltree[]
     </code>
     <code class="literal">
      ~
     </code>
     <code class="type">
      lquery
     </code>
     →
     <code class="returnvalue">
      boolean
     </code>
    </p>
    <p class="func_signature">
     <code class="type">
      lquery
     </code>
     <code class="literal">
      ~
     </code>
     <code class="type">
      ltree[]
     </code>
     →
     <code class="returnvalue">
      boolean
     </code>
    </p>
    <p>
     O array contém algum caminho correspondente
     <code class="type">
      lquery
     </code>
     ?
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="type">
      ltree[]
     </code>
     <code class="literal">
      ?
     </code>
     <code class="type">
      lquery[]
     </code>
     →
     <code class="returnvalue">
      boolean
     </code>
    </p>
    <p class="func_signature">
     <code class="type">
      lquery[]
     </code>
     <code class="literal">
      ?
     </code>
     <code class="type">
      ltree[]
     </code>
     →
     <code class="returnvalue">
      boolean
     </code>
    </p>
    <p>
     Faz
     <code class="type">
      ltree
     </code>
     um array que contenha qualquer caminho que corresponda a qualquer
     <code class="type">
      lquery
     </code>
     ?
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="type">
      ltree[]
     </code>
     <code class="literal">
      @
     </code>
     <code class="type">
      ltxtquery
     </code>
     →
     <code class="returnvalue">
      boolean
     </code>
    </p>
    <p class="func_signature">
     <code class="type">
      ltxtquery
     </code>
     <code class="literal">
      @
     </code>
     <code class="type">
      ltree[]
     </code>
     →
     <code class="returnvalue">
      boolean
     </code>
    </p>
    <p>
     O array contém algum caminho correspondente
     <code class="type">
      ltxtquery
     </code>
     ?
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="type">
      ltree[]
     </code>
     <code class="literal">
      ?@&gt;
     </code>
     <code class="type">
      ltree
     </code>
     →
     <code class="returnvalue">
      ltree
     </code>
    </p>
    <p>
     Retorna a primeira entrada do array que é um antecessor de
     <code class="type">
      ltree
     </code>
     , ou
     <code class="literal">
      NULL
     </code>
     nenhum.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="type">
      ltree[]
     </code>
     <code class="literal">
      ?&lt;@
     </code>
     <code class="type">
      ltree
     </code>
     →
     <code class="returnvalue">
      ltree
     </code>
    </p>
    <p>
     Retorna a primeira entrada do array que é um descendente de
     <code class="type">
      ltree
     </code>
     , ou
     <code class="literal">
      NULL
     </code>
     nenhum.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="type">
      ltree[]
     </code>
     <code class="literal">
      ?~
     </code>
     <code class="type">
      lquery
     </code>
     →
     <code class="returnvalue">
      ltree
     </code>
    </p>
    <p>
     Retorna a primeira entrada do array que corresponde
     <code class="type">
      lquery
     </code>
     , ou
     <code class="literal">
      NULL
     </code>
     nenhum.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="type">
      ltree[]
     </code>
     <code class="literal">
      ?@
     </code>
     <code class="type">
      ltxtquery
     </code>
     →
     <code class="returnvalue">
      ltree
     </code>
    </p>
    <p>
     Retorna a primeira entrada do array que corresponde
     <code class="type">
      ltxtquery
     </code>
     , ou
     <code class="literal">
      NULL
     </code>
     nenhum.
    </p>
   </td>
  </tr>
 </tbody>
</table>









Os operadores `<@`, `@>`, `@` e `~` têm análogos `^<@`, `^@>`, `^@`, `^~`, que são os mesmos, exceto que não usam índices. Esses são úteis apenas para fins de teste.

As funções disponíveis são mostradas na [Tabela F.13](ltree.md#LTREE-FUNC-TABLE).

**Tabela F.13. `ltree` Funções**



<table border="1" class="table" summary="ltree Functions">
 <colgroup>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th class="func_table_entry">
    <p class="func_signature">
     Função
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
     <code class="function">
      subltree
     </code>
     (
     <code class="type">
      ltree
     </code>
     ,
     <em class="parameter">
      <code>
       start
      </code>
     </em>
     <code class="type">
      integer
     </code>
     ,
     <em class="parameter">
      <code>
       end
      </code>
     </em>
     <code class="type">
      integer
     </code>
     )
     <code class="returnvalue">
      ltree
     </code>
    </p>
    <p>
     Retorna subcaminho de
     <code class="type">
      ltree
     </code>
     da posição
     <em class="parameter">
      <code>
       start
      </code>
     </em>
     posicionar
     <em class="parameter">
      <code>
       end
      </code>
     </em>
     -1 (contando a partir de 0).
    </p>
    <p>
     <code class="literal">
      subltree('Top.Child1.Child2', 1, 2)
     </code>
     →
     <code class="returnvalue">
      Child1
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      subpath
     </code>
     (
     <code class="type">
      ltree
     </code>
     ,
     <em class="parameter">
      <code>
       offset
      </code>
     </em>
     <code class="type">
      integer
     </code>
     ,
     <em class="parameter">
      <code>
       len
      </code>
     </em>
     <code class="type">
      integer
     </code>
     )
     <code class="returnvalue">
      ltree
     </code>
    </p>
    <p>
     Retorna subcaminho de
     <code class="type">
      ltree
     </code>
     a partir da posição
     <em class="parameter">
      <code>
       offset
      </code>
     </em>
     , com comprimento
     <em class="parameter">
      <code>
       len
      </code>
     </em>
     . Se
     <em class="parameter">
      <code>
       offset
      </code>
     </em>
     se for negativo, o subcaminho começa muito longe do final do caminho. Se
     <em class="parameter">
      <code>
       len
      </code>
     </em>
     É negativo, deixa muitas etiquetas no fim do caminho.
    </p>
    <p>
     <code class="literal">
      subpath('Top.Child1.Child2', 0, 2)
     </code>
     →
     <code class="returnvalue">
      Top.Child1
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      subpath
     </code>
     (
     <code class="type">
      ltree
     </code>
     ,
     <em class="parameter">
      <code>
       offset
      </code>
     </em>
     <code class="type">
      integer
     </code>
     )
     <code class="returnvalue">
      ltree
     </code>
    </p>
    <p>
     Retorna subcaminho de
     <code class="type">
      ltree
     </code>
     a partir da posição
     <em class="parameter">
      <code>
       offset
      </code>
     </em>
     , estendendo-se até o final do caminho. Se
     <em class="parameter">
      <code>
       offset
      </code>
     </em>
     se for negativo, o subcaminho começa muito longe do final do caminho.
    </p>
    <p>
     <code class="literal">
      subpath('Top.Child1.Child2', 1)
     </code>
     →
     <code class="returnvalue">
      Child1.Child2
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      nlevel
     </code>
     (
     <code class="type">
      ltree
     </code>
     )
     <code class="returnvalue">
      integer
     </code>
    </p>
    <p>
     Retorna o número de rótulos no caminho.
    </p>
    <p>
     <code class="literal">
      nlevel('Top.Child1.Child2')
     </code>
     →
     <code class="returnvalue">
      3
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      index
     </code>
     (
     <em class="parameter">
      <code>
       a
      </code>
     </em>
     <code class="type">
      ltree
     </code>
     ,
     <em class="parameter">
      <code>
       b
      </code>
     </em>
     <code class="type">
      ltree
     </code>
     )
     <code class="returnvalue">
      integer
     </code>
    </p>
    <p>
     Retorna a posição da primeira ocorrência de
     <em class="parameter">
      <code>
       b
      </code>
     </em>
     em
     <em class="parameter">
      <code>
       a
      </code>
     </em>
     , ou -1 se não for encontrado.
    </p>
    <p>
     <code class="literal">
      index('0.1.2.3.5.4.5.6.8.5.6.8', '5.6')
     </code>
     →
     <code class="returnvalue">
      6
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      index
     </code>
     (
     <em class="parameter">
      <code>
       a
      </code>
     </em>
     <code class="type">
      ltree
     </code>
     ,
     <em class="parameter">
      <code>
       b
      </code>
     </em>
     <code class="type">
      ltree
     </code>
     ,
     <em class="parameter">
      <code>
       offset
      </code>
     </em>
     <code class="type">
      integer
     </code>
     )
     <code class="returnvalue">
      integer
     </code>
    </p>
    <p>
     Retorna a posição da primeira ocorrência de
     <em class="parameter">
      <code>
       b
      </code>
     </em>
     em
     <em class="parameter">
      <code>
       a
      </code>
     </em>
     , ou -1 se não for encontrado. A pesquisa começa na posição
     <em class="parameter">
      <code>
       offset
      </code>
     </em>
     ; negativo
     <em class="parameter">
      <code>
       offset
      </code>
     </em>
     significa começar
     <em class="parameter">
      <code>
       -offset
      </code>
     </em>
     etiquetas do final do caminho.
    </p>
    <p>
     <code class="literal">
      index('0.1.2.3.5.4.5.6.8.5.6.8', '5.6', -4)
     </code>
     →
     <code class="returnvalue">
      9
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      text2ltree
     </code>
     (
     <code class="type">
      text
     </code>
     )
     <code class="returnvalue">
      ltree
     </code>
    </p>
    <p>
     Funduras
     <code class="type">
      text
     </code>
     para
     <code class="type">
      ltree
     </code>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      ltree2text
     </code>
     (
     <code class="type">
      ltree
     </code>
     )
     <code class="returnvalue">
      text
     </code>
    </p>
    <p>
     Funduras
     <code class="type">
      ltree
     </code>
     para
     <code class="type">
      text
     </code>
     .
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      lca
     </code>
     (
     <code class="type">
      ltree
     </code>
     [
     <span class="optional">
      ,
      <code class="type">
       ltree
      </code>
      [
      <span class="optional">
       , ...
      </span>
      ]
     </span>
     ] )
     <code class="returnvalue">
      ltree
     </code>
    </p>
    <p>
     Calcula o antepassado comum mais longo dos caminhos (até 8 argumentos são suportados).
    </p>
    <p>
     <code class="literal">
      lca('1.2.3', '1.2.3.4.5.6')
     </code>
     →
     <code class="returnvalue">
      1.2
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      lca
     </code>
     (
     <code class="type">
      ltree[]
     </code>
     )
     <code class="returnvalue">
      ltree
     </code>
    </p>
    <p>
     Calcula o antepassado comum mais longo dos caminhos no array.
    </p>
    <p>
     <code class="literal">
      lca(array['1.2.3'::ltree,'1.2.3.4'])
     </code>
     →
     <code class="returnvalue">
      1.2
     </code>
    </p>
   </td>
  </tr>
 </tbody>
</table>






### F.22.3. Índices [#](#LTREE-INDEXES)

`ltree` suporta vários tipos de índices que podem acelerar os operadores indicados:

* Índice de árvore B sobre `ltree`: `<`, `<=`, `=`, `>=`, `>`
* Índice de hash sobre `ltree`: `=`
* Índice GiST sobre `ltree` (`gist_ltree_ops` opclass): `<`, `<=`, `=`, `>=`, `>`, `@>`, `<@`, `@`, `~`, `?`

`gist_ltree_ops` O opclass GiST aproxima um conjunto de rótulos de caminho como uma assinatura de bitmap. Seu parâmetro inteiro opcional `siglen` determina o comprimento da assinatura em bytes. O comprimento padrão é de 8 bytes. O comprimento deve ser um múltiplo positivo de `int` (4 bytes na maioria das máquinas) até 2024. assinaturas mais longas levam a uma busca mais precisa (digitalizando uma fração menor do índice e menos páginas de heap), ao custo de um índice maior.

Exemplo de criação de um índice com o comprimento de assinatura padrão de 8 bytes:

```
CREATE INDEX path_gist_idx ON test USING GIST (path);
```

Exemplo de criação de um índice desse tipo com uma extensão de assinatura de 100 bytes:

* Índice GiST sobre `ltree[]` (opclass `gist__ltree_ops`): `ltree[] <@ ltree`, `ltree @> ltree[]`, `@`, `~`, `?`

`gist__ltree_ops` O opclass GiST funciona de forma semelhante ao `gist_ltree_ops` e também recebe o comprimento da assinatura como um parâmetro. O valor padrão de `siglen` em `gist__ltree_ops` é de 28 bytes.

Exemplo de criação de um índice com o comprimento de assinatura padrão de 28 bytes:

```
CREATE INDEX path_gist_idx ON test USING GIST (array_path);
```

Exemplo de criação de um índice desse tipo com uma extensão de assinatura de 100 bytes:

```
CREATE INDEX path_gist_idx ON test USING GIST (array_path gist__ltree_ops(siglen=100));
```

Nota: Este tipo de índice é perda de dados.

### F.22.4. Exemplo [#](#LTREE-EXAMPLE)

Este exemplo utiliza os seguintes dados (também disponíveis no arquivo `contrib/ltree/ltreetest.sql` na distribuição de origem):

```
CREATE TABLE test (path ltree);
INSERT INTO test VALUES ('Top');
INSERT INTO test VALUES ('Top.Science');
INSERT INTO test VALUES ('Top.Science.Astronomy');
INSERT INTO test VALUES ('Top.Science.Astronomy.Astrophysics');
INSERT INTO test VALUES ('Top.Science.Astronomy.Cosmology');
INSERT INTO test VALUES ('Top.Hobbies');
INSERT INTO test VALUES ('Top.Hobbies.Amateurs_Astronomy');
INSERT INTO test VALUES ('Top.Collections');
INSERT INTO test VALUES ('Top.Collections.Pictures');
INSERT INTO test VALUES ('Top.Collections.Pictures.Astronomy');
INSERT INTO test VALUES ('Top.Collections.Pictures.Astronomy.Stars');
INSERT INTO test VALUES ('Top.Collections.Pictures.Astronomy.Galaxies');
INSERT INTO test VALUES ('Top.Collections.Pictures.Astronomy.Astronauts');
CREATE INDEX path_gist_idx ON test USING GIST (path);
CREATE INDEX path_idx ON test USING BTREE (path);
CREATE INDEX path_hash_idx ON test USING HASH (path);
```

Agora, temos uma tabela `test` preenchida com dados que descrevem a hierarquia mostrada abaixo:

```
                        Top
                     /   |  \
             Science Hobbies Collections
                 /       |              \
        Astronomy   Amateurs_Astronomy Pictures
           /  \                            |
Astrophysics  Cosmology                Astronomy
                                        /  |    \
                                 Galaxies Stars Astronauts
```

Podemos fazer herança:

```
ltreetest=> SELECT path FROM test WHERE path <@ 'Top.Science';
                path
------------------------------------
 Top.Science
 Top.Science.Astronomy
 Top.Science.Astronomy.Astrophysics
 Top.Science.Astronomy.Cosmology
(4 rows)
```

Aqui estão alguns exemplos de correspondência de caminho:

```
ltreetest=> SELECT path FROM test WHERE path ~ '*.Astronomy.*';
                     path
-----------------------------------------------
 Top.Science.Astronomy
 Top.Science.Astronomy.Astrophysics
 Top.Science.Astronomy.Cosmology
 Top.Collections.Pictures.Astronomy
 Top.Collections.Pictures.Astronomy.Stars
 Top.Collections.Pictures.Astronomy.Galaxies
 Top.Collections.Pictures.Astronomy.Astronauts
(7 rows)

ltreetest=> SELECT path FROM test WHERE path ~ '*.!pictures@.Astronomy.*';
                path
------------------------------------
 Top.Science.Astronomy
 Top.Science.Astronomy.Astrophysics
 Top.Science.Astronomy.Cosmology
(3 rows)
```

Aqui estão alguns exemplos de busca de texto completo:

```
ltreetest=> SELECT path FROM test WHERE path @ 'Astro*% & !pictures@';
                path
------------------------------------
 Top.Science.Astronomy
 Top.Science.Astronomy.Astrophysics
 Top.Science.Astronomy.Cosmology
 Top.Hobbies.Amateurs_Astronomy
(4 rows)

ltreetest=> SELECT path FROM test WHERE path @ 'Astro* & !pictures@';
                path
------------------------------------
 Top.Science.Astronomy
 Top.Science.Astronomy.Astrophysics
 Top.Science.Astronomy.Cosmology
(3 rows)
```

Construção de caminhos usando funções:

```
ltreetest=> SELECT subpath(path,0,2)||'Space'||subpath(path,2) FROM test WHERE path <@ 'Top.Science.Astronomy';
                 ?column?
------------------------------------------
 Top.Science.Space.Astronomy
 Top.Science.Space.Astronomy.Astrophysics
 Top.Science.Space.Astronomy.Cosmology
(3 rows)
```

Poderíamos simplificar isso criando uma função SQL que insere uma etiqueta em uma posição especificada em um caminho:

```
CREATE FUNCTION ins_label(ltree, int, text) RETURNS ltree
    AS 'select subpath($1,0,$2) || $3 || subpath($1,$2);'
    LANGUAGE SQL IMMUTABLE;

ltreetest=> SELECT ins_label(path,2,'Space') FROM test WHERE path <@ 'Top.Science.Astronomy';
                ins_label
------------------------------------------
 Top.Science.Space.Astronomy
 Top.Science.Space.Astronomy.Astrophysics
 Top.Science.Space.Astronomy.Cosmology
(3 rows)
```

### F.22.5. Transformações [#](#LTREE-TRANSFORMS)

A extensão `ltree_plpython3u` implementa transformações para o tipo `ltree` para PL/Python. Se instalada e especificada ao criar uma função, os valores de `ltree` são mapeados para listas em Python. (O contrário, no entanto, não é atualmente suportado.)

### F.22.6. Autores [#](#LTREE-AUTHORS)

Todo o trabalho foi feito por Teodor Sigaev (`<teodor@stack.net>`) e Oleg Bartunov (`<oleg@sai.msu.su>`). Consulte
<http://www.sai.msu.su/~megera/postgres/gist/> para
informações adicionais. Os autores gostariam de agradecer a Eugeny Rodichev por discussões úteis. Comentários e relatórios de erros são bem-vindos.