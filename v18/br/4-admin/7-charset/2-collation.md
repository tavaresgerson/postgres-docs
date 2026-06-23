## 23.2. Suporte de Colaboração [#](#COLLATION)

* [23.2.1. Conceitos](collation.md#COLLATION-CONCEPTS)
* [23.2.2. Gerenciamento de Colagens](collation.md#COLLATION-MANAGING)
* [23.2.3. Colagens Personalizadas do ICU](collation.md#ICU-CUSTOM-COLLATIONS)

O recurso de agregação permite especificar a ordem de classificação e o comportamento de classificação de caracteres dos dados por coluna, ou até mesmo por operação. Isso alivia a restrição de que as configurações `LC_COLLATE` e `LC_CTYPE` de um banco de dados não podem ser alteradas após sua criação.

### 23.2.1. Conceitos [#](#COLLATION-CONCEPTS)

Conceitualmente, toda expressão de um tipo de dados colidível tem uma colagem. (Os tipos de dados colidíveis pré-definidos são `text`, `varchar` e `char`. Tipos de base definidos pelo usuário também podem ser marcados como colidíveis, e, claro, um [*[domain](glossary.md#GLOSSARY-DOMAIN "Domain")*](glossário.md#GLOSSARY-DOMAIN) sobre um tipo de dados colidível é colidível.) Se a expressão for uma referência de coluna, a colagem da expressão é a colagem definida da coluna. Se a expressão for uma constante, a colagem é a colagem padrão do tipo de dados da constante. A colagem de uma expressão mais complexa é derivada das colégias de suas entradas, conforme descrito abaixo.

A agregação de uma expressão pode ser a agregação "padrão", o que significa que as configurações de localização definidas para o banco de dados. Também é possível que a agregação de uma expressão seja indeterminada. Nesses casos, operações de ordenação e outras operações que precisam saber a agregação falharão.

Quando o sistema de banco de dados precisa realizar uma ordenação ou uma classificação de caracteres, ele utiliza a collation da expressão de entrada. Isso acontece, por exemplo, com cláusulas `ORDER BY` e chamadas de função ou operador, como `<`. A collation a ser aplicada para uma cláusula `ORDER BY` é simplesmente a collation da chave de ordenação. A collation a ser aplicada para uma chamada de função ou operador é derivada dos argumentos, conforme descrito abaixo. Além dos operadores de comparação, as collations são consideradas por funções que convertem entre letras maiúsculas e minúsculas, como `lower`, `upper` e `initcap`; por operadores de correspondência de padrões; e por `to_char` e funções relacionadas.

Para uma chamada de função ou operador, a collation que é derivada ao examinar as collation dos argumentos é usada no momento da execução para realizar a operação especificada. Se o resultado da chamada de função ou operador for de um tipo de dados collationável, a collation também é usada no momento da análise, como a collation definida da expressão da função ou operador, no caso de haver uma expressão envolvente que exija conhecimento de sua collation.

A *derivada da coligação* de uma expressão pode ser explícita ou implícita. Essa distinção afeta a forma como as coligações são combinadas quando várias coligações diferentes aparecem em uma expressão. Uma derivação explícita da coligação ocorre quando uma cláusula `COLLATE` é usada; todas as outras derivações de coligação são implícitas. Quando várias coligações precisam ser combinadas, por exemplo, em uma chamada de função, as seguintes regras são usadas:

1. Se qualquer expressão de entrada tiver uma derivação explícita de cotação, então todas as cotações derivadas explicitamente entre as expressões de entrada devem ser as mesmas, caso contrário, um erro é gerado. Se houver alguma cotação derivada explicitamente presente, esse é o resultado da combinação de cotação.
2. Caso contrário, todas as expressões de entrada devem ter a mesma derivação de cotação implícita ou a cotação padrão. Se houver alguma cotação não padrão presente, esse é o resultado da combinação de cotação. Caso contrário, o resultado é a cotação padrão.
3. Se houver cotações implícitas não padrão em conflito entre as expressões de entrada, então a combinação é considerada ter uma cotação indeterminada. Isso não é uma condição de erro, a menos que a função específica que está sendo invocada exija conhecimento da cotação que deve ser aplicada. Se isso acontecer, um erro será gerado no tempo de execução.

Por exemplo, considere esta definição de tabela:

```
CREATE TABLE test1 (
    a text COLLATE "de_DE",
    b text COLLATE "es_ES",
    ...
);
```

Então, em

```
SELECT a < 'foo' FROM test1;
```

a comparação `<` é realizada de acordo com as regras `de_DE`, porque a expressão combina uma ordenação derivada implicitamente com a ordenação padrão. Mas em

```
SELECT a < ('foo' COLLATE "fr_FR") FROM test1;
```

a comparação é realizada usando as regras do `fr_FR`, porque a derivação explícita da correção substitui a implícita. Além disso, dado

```
SELECT a < b FROM test1;
```

o analisador não pode determinar qual collation aplicar, uma vez que as colunas `a` e `b` têm collation implícita conflitante. Como o operador `<` precisa saber qual collation usar, isso resultará em um erro. O erro pode ser resolvido ao anexar um especificador explícito de collation a qualquer expressão de entrada, assim:

```
SELECT a < b COLLATE "de_DE" FROM test1;
```

ou, como equivalente

```
SELECT a COLLATE "de_DE" < b FROM test1;
```

Por outro lado, o caso estruturalmente semelhante

```
SELECT a || b FROM test1;
```

não resulta em um erro, porque o operador `||` não se importa com as codificações: seu resultado é o mesmo, independentemente da codificação.

A combinação de expressões de entrada de uma função ou expressão de operador também é considerada aplicável ao resultado da função ou do operador, se a função ou o operador fornecer um resultado de um tipo de dados combinável. Portanto, em

```
SELECT * FROM test1 ORDER BY a || 'foo';
```

a encomenda será feita de acordo com as regras do `de_DE`. Mas esta consulta:

```
SELECT * FROM test1 ORDER BY a || b;
```

resulta em um erro, porque, embora o operador `||` não precise conhecer uma codificação, a cláusula `ORDER BY` precisa. Como antes, o conflito pode ser resolvido com um especificador explícito de codificação:

```
SELECT * FROM test1 ORDER BY a || b COLLATE "fr_FR";
```

### 23.2.2. Gerenciamento de collation [#](#COLLATION-MANAGING)

Uma correção é um objeto do esquema SQL que mapeia um nome SQL para locais fornecidos por bibliotecas instaladas no sistema operacional. Uma definição de correção tem um * provedor * que especifica qual biblioteca fornece os dados do local. Um nome padrão do provedor é `libc`, que usa os locais fornecidos pela biblioteca C do sistema operacional. Estes são os locais usados pela maioria das ferramentas fornecidas pelo sistema operacional. Outro provedor é `icu`, que usa a biblioteca ICU externa. Os locais ICU só podem ser usados se o suporte para ICU foi configurado quando o PostgreSQL foi construído.

Um objeto de correspondência fornecido por `libc` corresponde a uma combinação de configurações de `LC_COLLATE` e `LC_CTYPE`, conforme aceito pela chamada de biblioteca do sistema `setlocale()`. (Como o nome sugere, o principal propósito de uma correspondência é definir `LC_COLLATE`, que controla a ordem de classificação. Mas raramente é necessário, na prática, ter uma configuração de `LC_CTYPE` diferente de `LC_COLLATE`, então é mais conveniente coletar essas configurações sob um único conceito do que criar outra infraestrutura para definir `LC_CTYPE` por expressão.) Além disso, uma correspondência de `libc` está vinculada a um conjunto de codificação de caracteres (veja [Seção 23.3](multibyte.md)). O mesmo nome de correspondência pode existir para diferentes codificações.

Um objeto de correspondência fornecido por `icu` corresponde a um coletor nomeado fornecido pela biblioteca ICU. O ICU não suporta configurações separadas de “collate” e “ctype”, então elas são sempre as mesmas. Além disso, as codificações do ICU são independentes da codificação, então sempre há apenas uma codificação ICU de um nome dado em um banco de dados.

#### 23.2.2.1. Colagens Padrão [#](#COLLATION-MANAGING-STANDARD)

Em todas as plataformas, as seguintes codificações são suportadas:

`unicode`: Este padrão de ordenação SQL ordena usando o Algoritmo de Ordenação Unicode com a Tabela de Elemento de Ordenação Unicode Padrão. Está disponível em todas as codificações. O suporte do ICU é necessário para usar essa ordenação, e o comportamento pode mudar se o PostgreSQL for construído com uma versão diferente do ICU. (Essa ordenação tem o mesmo comportamento que o local raiz do ICU; veja `und-x-icu` (para “definido”) (collation.md#COLLATION-MANAGING-PREDEFINED-ICU-UND-X-ICU).)

`ucs_basic`: Este padrão de codificação SQL ordena usando os valores dos pontos de código Unicode, em vez da ordem do idioma natural, e apenas as letras ASCII “`A`” a “`Z`” são tratadas como letras. O comportamento é eficiente e estável em todas as versões. Disponível apenas para codificação `UTF8`. (Este padrão de codificação tem o mesmo comportamento que a especificação de localidade libc `C` na codificação `UTF8`.

`pg_unicode_fast`: Esta ordenação classifica por valores de pontos de código Unicode, em vez de ordem de linguagem natural. Para as funções `lower`, `initcap` e `upper`, utiliza mapeamento de caso completo Unicode. Para o correspondência de padrões (incluindo expressões regulares), utiliza a variante padrão do Unicode [Propriedades de compatibilidade](https://www.unicode.org/reports/tr18/#Compatibility_Properties). O comportamento é eficiente e estável dentro de uma versão principal do Postgres. Está disponível apenas para codificação `UTF8`.

`pg_c_utf8`: Esta ordenação ordena por valores de pontos de código Unicode, em vez de ordem de linguagem natural. Para as funções `lower`, `initcap` e `upper`, utiliza mapeamento de caso simples Unicode. Para o correspondência de padrões (incluindo expressões regulares), utiliza a variante compatível com POSIX de Unicode [Propriedades de compatibilidade](https://www.unicode.org/reports/tr18/#Compatibility_Properties). O comportamento é eficiente e estável dentro de uma versão principal do PostgreSQL. Esta ordenação está disponível apenas para codificação `UTF8`.

`C` (equivalente a `POSIX`): As codificações `C` e `POSIX` são baseadas no comportamento do "C tradicional". Elas ordenam por valores de byte em vez da ordem do idioma natural, e apenas as letras ASCII “`A`” a “`Z`” são tratadas como letras. O comportamento é eficiente e estável em todas as versões para um determinado codificação de banco de dados, mas o comportamento pode variar entre diferentes codificações de banco de dados.

`default`: A agregação `default` seleciona o local especificado no momento da criação do banco de dados.

Outras colatões podem estar disponíveis, dependendo do suporte do sistema operacional. A eficiência e a estabilidade dessas colatões dependem do fornecedor de colatões, da versão do fornecedor e do local.

#### 23.2.2.2. Colagens pré-definidas [#](#COLLATION-MANAGING-PREDEFINED)

Se o sistema operacional fornecer suporte para o uso de múltiplos locais em um único programa (`newlocale` e funções relacionadas), ou se o suporte para ICU for configurado, então, quando um clúster de banco de dados é inicializado, `initdb` preenche o catálogo do sistema `pg_collation` com colunas baseadas em todos os locais que ele encontrar no sistema operacional no momento.

Para inspecionar as localidades disponíveis atualmente, use a consulta `SELECT
* FROM pg_collation`, ou o comando `\dOS+` no psql.

##### 23.2.2.2.1. Colagens do libc [#](#COLLATION-MANAGING-PREDEFINED-LIBC)

Por exemplo, o sistema operacional pode fornecer um local denominado `de_DE.utf8`. `initdb` criaria então uma codificação denominada `de_DE.utf8` para codificar `UTF8` que tem tanto `LC_COLLATE` quanto `LC_CTYPE` definidos como `de_DE.utf8`. Também criaria uma codificação com a tag `.utf8` removida do nome. Assim, você também poderia usar a codificação sob o nome `de_DE`, que é menos trabalhoso de escrever e torna o nome menos dependente da codificação. Note, no entanto, que o conjunto inicial de nomes de codificação é dependente da plataforma.

O conjunto padrão de codificações fornecido por `libc` é mapeado diretamente para os locais instalados no sistema operacional, que podem ser listados usando o comando `locale -a`. Caso seja necessário uma codificação `libc` que tenha valores diferentes para `LC_COLLATE` e `LC_CTYPE`, ou se novos locais forem instalados no sistema operacional após o sistema de banco de dados ter sido inicializado, então uma nova codificação pode ser criada usando o comando [CREATE COLLATION](sql-createcollation.md "CREATE COLLATION"). Novos locais do sistema operacional também podem ser importados em massa usando a função [`pg_import_system_collations()`(functions-admin.md#FUNCTIONS-ADMIN-COLLATION "Table 9.104. Collation Management Functions").

Dentro de qualquer banco de dados específico, apenas as codificações que utilizam a codificação do banco de dados em questão são de interesse. Outras entradas em `pg_collation` são ignoradas. Assim, um nome de codificação simplificado, como `de_DE`, pode ser considerado único dentro de um banco de dados dado, mesmo que não seja único globalmente. O uso dos nomes de codificação simplificados é recomendado, pois isso fará uma coisa a menos que você precise mudar se decidir mudar para outra codificação de banco de dados. No entanto, é importante notar que as codificações `default`, `C` e `POSIX` podem ser usadas independentemente da codificação do banco de dados.

O PostgreSQL considera que objetos de collation distintos são incompatíveis, mesmo quando possuem propriedades idênticas. Assim, por exemplo,

```
SELECT a COLLATE "C" < b COLLATE "POSIX" FROM test1;
```

irá gerar um erro, mesmo que as colatações `C` e `POSIX` tenham comportamentos idênticos. Portanto, não é recomendado misturar nomes de colatação descascados e não descascados.

##### 23.2.2.2.2. Colagens do ICU [#](#COLLATION-MANAGING-PREDEFINED-ICU)

Com o ICU, não é sensato enumerar todos os nomes possíveis de locais. O ICU usa um sistema de nomeação particular para locais, mas há muitas outras maneiras de nomear um local do que realmente há locais distintos. `initdb` usa as APIs do ICU para extrair um conjunto de locais distintos para preencher o conjunto inicial de coligações. As coligações fornecidas pelo ICU são criadas no ambiente SQL com nomes no formato de tag de idioma BCP 47, com uma extensão de “uso privado” `-x-icu` anexada, para distingui-las dos locais da libc.

Aqui estão alguns exemplos de colatações que podem ser criadas:

`de-x-icu` [#](#COLLATION-MANAGING-PREDEFINED-ICU-DE-X-ICU): Coleta alemã, variante padrão

`de-AT-x-icu` [#](#COLLATION-MANAGING-PREDEFINED-ICU-DE-AT-X-ICU): Coleta alemã para a Áustria, variante padrão

(Existem também, por exemplo, `de-DE-x-icu` ou `de-CH-x-icu`, mas, conforme este texto, eles são equivalentes a `de-x-icu`.)

`und-x-icu` (para “definido”) [#](#COLLATION-MANAGING-PREDEFINED-ICU-UND-X-ICU): Cotação “raiz” da ICU. Use isso para obter uma ordem de classificação razoável, independente do idioma.

Algumas (menos frequentemente usadas) codificações não são suportadas pelo ICU. Quando o código de banco de dados é uma dessas, as entradas de ordenação do ICU em `pg_collation` são ignoradas. Tentar usar uma delas resultará em um erro do tipo “a ordenação 'de-x-icu' para a codificação 'WIN874' não existe”.

#### 23.2.2.3. Criando novos objetos de coligação [#](#COLLATION-CREATE)

Se as colatões padrão e predefinidos não forem suficientes, os usuários podem criar seus próprios objetos de colatão usando o comando SQL [CREATE COLLATION](sql-createcollation.md "CREATE COLLATION").

As colatões padrão e predefinidas estão no esquema `pg_catalog`, assim como todos os objetos predefinidos. Colatões definidos pelo usuário devem ser criados em esquemas de usuário. Isso também garante que eles sejam salvos por `pg_dump`.

##### 23.2.2.3.1. Colagens do libc [#](#COLLATION-MANAGING-CREATE-LIBC)

Novas colatações do libc podem ser criadas da seguinte forma:

```
CREATE COLLATION german (provider = libc, locale = 'de_DE');
```

Os valores exatos que são aceitáveis para a cláusula `locale` neste comando dependem do sistema operacional. Em sistemas semelhantes ao Unix, o comando `locale -a` mostrará uma lista.

Como as colatações pré-definidas da libc já incluem todas as colatações definidas no sistema operacional quando a instância do banco de dados é inicializada, muitas vezes não é necessário criar manualmente novas colatações. As razões podem ser se um sistema de nomenclatura diferente é desejado (neste caso, veja também [Seção 23.2.2.3.3](collation.md#COLLATION-COPY)) ou se o sistema operacional foi atualizado para fornecer novas definições de local (neste caso, veja também [`pg_import_system_collations()`](functions-admin.md#FUNCTIONS-ADMIN-COLLATION)).

##### 23.2.2.3.2. Colagens do ICU [#](#COLLATION-MANAGING-CREATE-ICU)

As colas de ICU podem ser criadas como:

```
CREATE COLLATION german (provider = icu, locale = 'de-DE');
```

As localizações de ICU são especificadas como um BCP 47 (locale.md#ICU-LANGUAGE-TAG "23.1.5.3. Language Tag"), mas também podem aceitar a maioria dos nomes de localidade estilo libc. Se possível, os nomes de localidade estilo libc são transformados em tags de idioma.

Novas colatações de UTI podem personalizar extensivamente o comportamento da colatação, incluindo atributos de colatação no identificador de idioma. Consulte [Seção 23.2.3](collation.md#ICU-CUSTOM-COLLATIONS) para obter detalhes e exemplos.

##### 23.2.2.3.3. Copiar colligações [#](#COLLATION-COPY)

O comando [CREATE COLLATION](sql-createcollation.md "CREATE COLLATION") também pode ser usado para criar uma nova correção de texto a partir de uma correção de texto existente, o que pode ser útil para poder usar nomes de correção de texto independentes do sistema operacional em aplicativos, criar nomes de compatibilidade ou usar uma correção de texto fornecida pelo ICU sob um nome mais legível. Por exemplo:

```
CREATE COLLATION german FROM "de_DE";
CREATE COLLATION french FROM "fr-x-icu";
```

#### 23.2.2.4. Colagens não determinísticas [#](#COLLATION-NONDETERMINISTIC)

Uma ordenação é *determinística* ou *não determinística*. Uma ordenação determinística utiliza comparações determinísticas, o que significa que ela considera que as cadeias são iguais apenas se consistirem na mesma sequência de bytes. A comparação não determinística pode determinar que as cadeias são iguais mesmo que consistirem em bytes diferentes. Situações típicas incluem a comparação não sensível ao caso, a comparação não sensível ao acento, bem como a comparação de cadeias em diferentes formas normais do Unicode. Cabe ao provedor da ordenação implementar essas comparações não sensíveis; a bandeira determinística apenas determina se os empates devem ser quebrados usando comparação byte a byte. Consulte também [Padrão Técnico de Unicode 10](https://www.unicode.org/reports/tr10) para obter mais informações sobre a terminologia.

Para criar uma ordenação não determinística, especifique a propriedade `deterministic = false` para `CREATE COLLATION`, por exemplo:

```
CREATE COLLATION ndcoll (provider = icu, locale = 'und', deterministic = false);
```

Este exemplo usaria a cotação Unicode padrão de uma maneira não determinística. Em particular, isso permitiria que as cadeias em diferentes formas normais fossem comparadas corretamente. Exemplos mais interessantes utilizam as facilidades de personalização do ICU explicadas acima. Por exemplo:

```
CREATE COLLATION case_insensitive (provider = icu, locale = 'und-u-ks-level2', deterministic = false);
CREATE COLLATION ignore_accents (provider = icu, locale = 'und-u-ks-level1-kc-true', deterministic = false);
```

Todas as colatões padrão e pré-definidas são determinísticas, todas as colatões definidas pelo usuário são determinísticas por padrão. Embora as colatões não determinísticas ofereçam um comportamento mais “correto”, especialmente quando se considera o poder total do Unicode e seus muitos casos especiais, elas também têm algumas desvantagens. Em primeiro lugar, seu uso leva a uma penalização de desempenho. Note, em particular, que a árvore B não pode usar a deduplicação com índices que utilizam uma colatão não determinística. Além disso, certas operações não são possíveis com colatões não determinísticas, como algumas operações de correspondência de padrões. Portanto, elas devem ser usadas apenas em casos em que sejam especificamente desejadas.

### DICA

Para lidar com texto em diferentes formas de normalização Unicode, também é uma opção usar as funções/expressões `normalize` e `is normalized` para pré-processar ou verificar as strings, em vez de usar colunas não determinísticas. Há diferentes compromissos para cada abordagem.

### 23.2.3. Colagens personalizadas do ICU [#](#ICU-CUSTOM-COLLATIONS)

A ICU permite um controle extenso sobre o comportamento de ordenação, definindo novas ordenações com configurações de ordenação como parte da tag de idioma. Essas configurações podem modificar a ordem de ordenação para atender a uma variedade de necessidades. Por exemplo:

```
-- ignore differences in accents and case
CREATE COLLATION ignore_accent_case (provider = icu, deterministic = false, locale = 'und-u-ks-level1');
SELECT 'Å' = 'A' COLLATE ignore_accent_case; -- true
SELECT 'z' = 'Z' COLLATE ignore_accent_case; -- true

-- upper case letters sort before lower case.
CREATE COLLATION upper_first (provider = icu, locale = 'und-u-kf-upper');
SELECT 'B' < 'b' COLLATE upper_first; -- true

-- treat digits numerically and ignore punctuation
CREATE COLLATION num_ignore_punct (provider = icu, deterministic = false, locale = 'und-u-ka-shifted-kn');
SELECT 'id-45' < 'id-123' COLLATE num_ignore_punct; -- true
SELECT 'w;x*y-z' = 'wxyz' COLLATE num_ignore_punct; -- true
```

Muitas das opções disponíveis são descritas em [Seção 23.2.3.2](collation.md#ICU-COLLATION-SETTINGS), ou consulte [Seção 23.2.3.5](collation.md#ICU-EXTERNAL-REFERENCES) para mais detalhes.

#### 23.2.3.1. Níveis de comparação de UTI [#](#ICU-COLLATION-COMPARISON-LEVELS)

A comparação de duas cadeias de caracteres (colação) no ICU é determinada por um processo de vários níveis, onde as características textuais são agrupadas em "níveis". O tratamento de cada nível é controlado pelas configurações de [colação](collation.md#ICU-COLLATION-SETTINGS-TABLE). Níveis mais altos correspondem a características textuais mais refinadas.

[Tabela 23.1](collation.md#ICU-COLLATION-LEVELS) mostra quais diferenças de características textuais são consideradas significativas ao determinar a igualdade no nível dado. O caractere Unicode `U+2063` é um separador invisível e, como visto na tabela, é ignorado em todos os níveis de comparação menos que `identic`.

**Tabela 23.1. Níveis de Colaboração de UTI**



<table border="1" class="table" summary="ICU Collation Levels">
 <colgroup>
  <col class="col1"/>
  <col class="col2"/>
  <col class="col3"/>
  <col class="col4"/>
  <col class="col5"/>
  <col class="col6"/>
  <col class="col7"/>
  <col class="col8"/>
 </colgroup>
 <thead>
  <tr>
   <th>
    Level
   </th>
   <th>
    Description
   </th>
   <th>
    <code class="literal">
     'f' = 'f'
    </code>
   </th>
   <th>
    <code class="literal">
     'ab' = U&amp;'a\2063b'
    </code>
   </th>
   <th>
    <code class="literal">
     'x-y' = 'x_y'
    </code>
   </th>
   <th>
    <code class="literal">
     'g' = 'G'
    </code>
   </th>
   <th>
    <code class="literal">
     'n' = 'ñ'
    </code>
   </th>
   <th>
    <code class="literal">
     'y' = 'z'
    </code>
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    level1
   </td>
   <td>
    Base Character
   </td>
   <td>
    <code class="literal">
     true
    </code>
   </td>
   <td>
    <code class="literal">
     true
    </code>
   </td>
   <td>
    <code class="literal">
     true
    </code>
   </td>
   <td>
    <code class="literal">
     true
    </code>
   </td>
   <td>
    <code class="literal">
     true
    </code>
   </td>
   <td>
    <code class="literal">
     false
    </code>
   </td>
  </tr>
  <tr>
   <td>
    level2
   </td>
   <td>
    Accents
   </td>
   <td>
    <code class="literal">
     true
    </code>
   </td>
   <td>
    <code class="literal">
     true
    </code>
   </td>
   <td>
    <code class="literal">
     true
    </code>
   </td>
   <td>
    <code class="literal">
     true
    </code>
   </td>
   <td>
    <code class="literal">
     false
    </code>
   </td>
   <td>
    <code class="literal">
     false
    </code>
   </td>
  </tr>
  <tr>
   <td>
    level3
   </td>
   <td>
    Case/Variants
   </td>
   <td>
    <code class="literal">
     true
    </code>
   </td>
   <td>
    <code class="literal">
     true
    </code>
   </td>
   <td>
    <code class="literal">
     true
    </code>
   </td>
   <td>
    <code class="literal">
     false
    </code>
   </td>
   <td>
    <code class="literal">
     false
    </code>
   </td>
   <td>
    <code class="literal">
     false
    </code>
   </td>
  </tr>
  <tr>
   <td>
    level4
   </td>
   <td>
    Punctuation
    <a class="footnote" href="#ftn.id-1.6.10.4.6.3.4.2.10.4.2.1">
     <sup class="footnote" id="id-1.6.10.4.6.3.4.2.10.4.2.1">
      [a]
     </sup>
    </a>
   </td>
   <td>
    <code class="literal">
     true
    </code>
   </td>
   <td>
    <code class="literal">
     true
    </code>
   </td>
   <td>
    <code class="literal">
     false
    </code>
   </td>
   <td>
    <code class="literal">
     false
    </code>
   </td>
   <td>
    <code class="literal">
     false
    </code>
   </td>
   <td>
    <code class="literal">
     false
    </code>
   </td>
  </tr>
  <tr>
   <td>
    identic
   </td>
   <td>
    All
   </td>
   <td>
    <code class="literal">
     true
    </code>
   </td>
   <td>
    <code class="literal">
     false
    </code>
   </td>
   <td>
    <code class="literal">
     false
    </code>
   </td>
   <td>
    <code class="literal">
     false
    </code>
   </td>
   <td>
    <code class="literal">
     false
    </code>
   </td>
   <td>
    <code class="literal">
     false
    </code>
   </td>
  </tr>
 </tbody>
 <tbody class="footnotes">
  <tr>
   <td colspan="8">
    <div class="footnote" id="ftn.id-1.6.10.4.6.3.4.2.10.4.2.1">
     <p>
      <a class="para" href="#id-1.6.10.4.6.3.4.2.10.4.2.1">
       <sup class="para">
        [a]
       </sup>
      </a>
      only with
      <code class="literal">
       ka-shifted
      </code>
      ; see
      <a class="xref" href="collation.md#ICU-COLLATION-SETTINGS-TABLE" title="Table 23.2. ICU Collation Settings">
       Table 23.2
      </a>
     </p>
    </div>
   </td>
  </tr>
 </tbody>
</table>










Em todos os níveis, mesmo com a normalização completa desativada, a normalização básica é realizada. Por exemplo, `'á'` pode ser composto pelos pontos de código `U&'\0061\0301'` ou pelo único ponto de código `U&'\00E1'`, e essas sequências serão consideradas iguais mesmo no nível `identic`. Para tratar qualquer diferença na representação dos pontos de código como distintos, use uma ordenação criada com `deterministic` definida como `true`.

##### 23.2.3.1.1. Exemplos de nível de cotação [#](#ICU-COLLATION-LEVEL-EXAMPLES)

```
CREATE COLLATION level3 (provider = icu, deterministic = false, locale = 'und-u-ka-shifted-ks-level3');
CREATE COLLATION level4 (provider = icu, deterministic = false, locale = 'und-u-ka-shifted-ks-level4');
CREATE COLLATION identic (provider = icu, deterministic = false, locale = 'und-u-ka-shifted-ks-identic');

-- invisible separator ignored at all levels except identic
SELECT 'ab' = U&'a\2063b' COLLATE level4; -- true
SELECT 'ab' = U&'a\2063b' COLLATE identic; -- false

-- punctuation ignored at level3 but not at level 4
SELECT 'x-y' = 'x_y' COLLATE level3; -- true
SELECT 'x-y' = 'x_y' COLLATE level4; -- false
```

#### 23.2.3.2. Configurações de Colaboração para um Local de ICU [#](#ICU-COLLATION-SETTINGS)

[Tabela 23.2](collation.md#ICU-COLLATION-SETTINGS-TABLE) mostra as configurações de ordenação disponíveis, que podem ser usadas como parte de uma tag de idioma para personalizar uma ordenação.

**Tabela 23.2. Configurações de ordenação do ICU**



<table border="1" class="table" summary="ICU Collation Settings">
 <colgroup>
  <col class="col1"/>
  <col class="col2"/>
  <col class="col3"/>
  <col class="col4"/>
 </colgroup>
 <thead>
  <tr>
   <th>
    Key
   </th>
   <th>
    Valores
   </th>
   <th>
    Default
   </th>
   <th>
    Descrição
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <code class="literal">
     co
    </code>
   </td>
   <td>
    <code class="literal">
     emoji
    </code>
    ,
    <code class="literal">
     phonebk
    </code>
    ,
    <code class="literal">
     standard
    </code>
    ,
    <em class="replaceable">
     <code>
      ...
     </code>
    </em>
   </td>
   <td>
    <code class="literal">
     standard
    </code>
   </td>
   <td>
    Tipo de cotação. Veja
    <a class="xref" href="collation.md#ICU-EXTERNAL-REFERENCES" title="23.2.3.5. External References for ICU">
     Seção 23.2.3.5
    </a>
    para obter opções adicionais e detalhes.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     ka
    </code>
   </td>
   <td>
    <code class="literal">
     noignore
    </code>
    ,
    <code class="literal">
     shifted
    </code>
   </td>
   <td>
    <code class="literal">
     noignore
    </code>
   </td>
   <td>
    Se definido como
    <code class="literal">
     shifted
    </code>
    , faz com que alguns caracteres (por exemplo, pontuação ou espaço) sejam ignorados na comparação. Chave
    <code class="literal">
     ks
    </code>
    deve ser ajustado para
    <code class="literal">
     level3
    </code>
    ou reduza-o para entrar em vigor. Defina a chave
    <code class="literal">
     kv
    </code>
    para controlar quais classes de caracteres são ignoradas.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     kb
    </code>
   </td>
   <td>
    <code class="literal">
     true
    </code>
    ,
    <code class="literal">
     false
    </code>
   </td>
   <td>
    <code class="literal">
     false
    </code>
   </td>
   <td>
    Comparação reversa para as diferenças do nível 2. Por exemplo, local
    <code class="literal">
     und-u-kb
    </code>
    selecione
    <code class="literal">
     'àe'
    </code>
    antes
    <code class="literal">
     'aé'
    </code>
    .
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     kc
    </code>
   </td>
   <td>
    <code class="literal">
     true
    </code>
    ,
    <code class="literal">
     false
    </code>
   </td>
   <td>
    <code class="literal">
     false
    </code>
   </td>
   <td>
    <p>
     Separa o caso em um "nível 2.5" que fica entre acentos e outras características do nível 3.
    </p>
    <p>
     Se definido como
     <code class="literal">
      true
     </code>
     e
     <code class="literal">
      ks
     </code>
     está previsto
     <code class="literal">
      level1
     </code>
     , ignorará acentos, mas levará em conta a grafia.
    </p>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     kf
    </code>
   </td>
   <td>
    <code class="literal">
     upper
    </code>
    ,
    <code class="literal">
     lower
    </code>
    ,
    <code class="literal">
     false
    </code>
   </td>
   <td>
    <code class="literal">
     false
    </code>
   </td>
   <td>
    Se definido como
    <code class="literal">
     upper
    </code>
    , as letras maiúsculas são ordenadas antes das minúsculas. Se definido como
    <code class="literal">
     lower
    </code>
    , as letras minúsculas são ordenadas antes das maiúsculas. Se definido como
    <code class="literal">
     false
    </code>
    , o tipo depende das regras do local.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     kn
    </code>
   </td>
   <td>
    <code class="literal">
     true
    </code>
    ,
    <code class="literal">
     false
    </code>
   </td>
   <td>
    <code class="literal">
     false
    </code>
   </td>
   <td>
    Se definido como
    <code class="literal">
     true
    </code>
    , os números dentro de uma string são tratados como um único valor numérico, e não como uma sequência de dígitos. Por exemplo,
    <code class="literal">
     'id-45'
    </code>
    separam antes
    <code class="literal">
     'id-123'
    </code>
    .
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     kk
    </code>
   </td>
   <td>
    <code class="literal">
     true
    </code>
    ,
    <code class="literal">
     false
    </code>
   </td>
   <td>
    <code class="literal">
     false
    </code>
   </td>
   <td>
    <p>
     Ative a normalização completa; pode afetar o desempenho. A normalização básica é realizada mesmo quando configurada para
     <code class="literal">
      false
     </code>
     . Os locais para idiomas que exigem normalização completa geralmente permitem isso por padrão.
    </p>
    <p>
     A normalização completa é importante em alguns casos, como quando múltiplos acentos são aplicados a um único caractere. Por exemplo, as sequências de pontos de código
     <code class="literal">
      U&amp;'\0065\0323\0302'
     </code>
     e
     <code class="literal">
      U&amp;'\0065\0302\0323'
     </code>
     representam
     <code class="literal">
      e
     </code>
     com acentos circunflexos e pontos abaixo aplicados em diferentes ordens. Com a normalização completa ativada, essas sequências de pontos de código são tratadas como iguais; caso contrário, são desiguais.
    </p>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     kr
    </code>
   </td>
   <td>
    <code class="literal">
     space
    </code>
    ,
    <code class="literal">
     punct
    </code>
    ,
    <code class="literal">
     symbol
    </code>
    ,
    <code class="literal">
     currency
    </code>
    ,
    <code class="literal">
     digit
    </code>
    ,
    <em class="replaceable">
     <code>
      script-id
     </code>
    </em>
   </td>
   <td>
   </td>
   <td>
    <p>
     Definido para um ou mais dos valores válidos, ou qualquer BCP 47
     <em class="replaceable">
      <code>
       script-id
      </code>
     </em>
     , por exemplo.
     <code class="literal">
      latn
     </code>
     ("Latino") ou
     <code class="literal">
      grek
     </code>
     ("Grego"). Múltiplos valores são separados por "
     <code class="literal">
      -
     </code>
     ".
    </p>
    <p>
     Redefine a ordem das classes de caracteres; os caracteres que pertencem a uma classe mais cedo na lista são ordenados antes dos caracteres que pertencem a uma classe mais tarde na lista. Por exemplo, o valor
     <code class="literal">
      digit-currency-space
     </code>
     (como parte de uma tag de idioma como
     <code class="literal">
      und-u-kr-digit-currency-space
     </code>
     ) ordena a pontuação antes dos dígitos e dos espaços.
    </p>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     ks
    </code>
   </td>
   <td>
    <code class="literal">
     level1
    </code>
    ,
    <code class="literal">
     level2
    </code>
    ,
    <code class="literal">
     level3
    </code>
    ,
    <code class="literal">
     level4
    </code>
    ,
    <code class="literal">
     identic
    </code>
   </td>
   <td>
    <code class="literal">
     level3
    </code>
   </td>
   <td>
    Sensibilidade (ou "força") ao determinar a igualdade, com
    <code class="literal">
     level1
    </code>
    menos sensíveis às diferenças e
    <code class="literal">
     identic
    </code>
    os mais sensíveis às diferenças. Veja
    <a class="xref" href="collation.md#ICU-COLLATION-LEVELS" title="Table 23.1. ICU Collation Levels">
     Tabela 23.1
    </a>
    para obter mais informações.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     kv
    </code>
   </td>
   <td>
    <code class="literal">
     space
    </code>
    ,
    <code class="literal">
     punct
    </code>
    ,
    <code class="literal">
     symbol
    </code>
    ,
    <code class="literal">
     currency
    </code>
   </td>
   <td>
    <code class="literal">
     punct
    </code>
   </td>
   <td>
    Classes de caracteres ignoradas durante a comparação no nível 3. Definir um valor posterior inclui valores anteriores; por exemplo,
    <code class="literal">
     symbol
    </code>
    também inclui
    <code class="literal">
     punct
    </code>
    e
    <code class="literal">
     space
    </code>
    em os caracteres a serem ignorados. Chave
    <code class="literal">
     ka
    </code>
    deve ser ajustado para
    <code class="literal">
     shifted
    </code>
    e chave
    <code class="literal">
     ks
    </code>
    deve ser definido
    <code class="literal">
     level3
    </code>
    ou inferior para entrar em vigor.
   </td>
  </tr>
 </tbody>
</table>










Os padrões podem depender do local. O quadro acima não pretende ser completo. Consulte [Seção 23.2.3.5](collation.md#ICU-EXTERNAL-REFERENCES) para obter opções e detalhes adicionais.

### Nota

Para muitas configurações de collation, você deve criar a collation com `deterministic` definida como `false` para que a configuração tenha o efeito desejado (consulte [Seção 23.2.2.4](collation.md#COLLATION-NONDETERMINISTIC)). Além disso, algumas configurações só têm efeito quando a chave `ka` é definida como `shifted` (consulte [Tabela 23.2](collation.md#ICU-COLLATION-SETTINGS-TABLE)).

#### 23.2.3.3. Configurações de Colaboração Exemplos [#](#ICU-LOCALE-EXAMPLES)

`CREATE COLLATION "de-u-co-phonebk-x-icu" (provider = icu, locale = 'de-u-co-phonebk');` [#](#COLLATION-MANAGING-CREATE-ICU-DE-U-CO-PHONEBK-X-ICU): Coleta alemã com tipo de coleta de livro telefônico

`CREATE COLLATION "und-u-co-emoji-x-icu" (provider = icu, locale = 'und-u-co-emoji');` [#](#COLLATION-MANAGING-CREATE-ICU-UND-U-CO-EMOJI-X-ICU): Colagem de raiz com tipo de colagem Emoji, de acordo com o Padrão Técnico Unicode #51

`CREATE COLLATION latinlast (provider = icu, locale = 'en-u-kr-grek-latn');` [#](#COLLATION-MANAGING-CREATE-ICU-EN-U-KR-GREK-LATN): Ordene as letras gregas antes das letras latinas. (O padrão é latim antes de grego.)

`CREATE COLLATION upperfirst (provider = icu, locale = 'en-u-kf-upper');` [#](#COLLATION-MANAGING-CREATE-ICU-EN-U-KF-UPPER): Ordene as letras maiúsculas antes das letras minúsculas. (O padrão é as letras minúsculas primeiro.)

`CREATE COLLATION special (provider = icu, locale = 'en-u-kf-upper-kr-grek-latn');` [#](#COLLATION-MANAGING-CREATE-ICU-EN-U-KF-UPPER-KR-GREK-LATN): Combina ambas as opções acima.

#### 23.2.3.4. Regras de personalização do ICU [#](#ICU-TAILORING-RULES)

Se as opções fornecidas pelas configurações de ordenação mostradas acima não forem suficientes, a ordem dos elementos de ordenação pode ser alterada com regras de personalização, cuja sintaxe é detalhada em <https://unicode-org.github.io/icu/userguide/collation/customization/>.

Este pequeno exemplo cria uma ordenação baseada no idioma raiz com uma regra de personalização:

```
CREATE COLLATION custom (provider = icu, locale = 'und', rules = '&V << w <<< W');
```

Com essa regra, a letra “W” é classificada após “V”, mas é tratada como uma diferença secundária semelhante a um acento. Regras como essa estão contidas nas definições do local de alguns idiomas. (Claro, se uma definição de local já contiver as regras desejadas, então elas não precisam ser especificadas explicitamente novamente.)

Aqui está um exemplo mais complexo. A seguinte declaração configura uma correção chamada `ebcdic` com regras para ordenar caracteres US-ASCII na ordem da codificação EBCDIC.

```
CREATE COLLATION ebcdic (provider = icu, locale = 'und',
rules = $$
& ' ' < '.' < '<' < '(' < '+' < \|
< '&' < '!' < '$' < '*' < ')' < ';'
< '-' < '/' < ',' < '%' < '_' < '>' < '?'
< '`' < ':' < '#' < '@' < \' < '=' < '"'
<*a-r < '~' <*s-z < '^' < '[' < ']'
< '{' <*A-I < '}' <*J-R < '\' <*S-Z <*0-9
$$);

SELECT c
FROM (VALUES ('a'), ('b'), ('A'), ('B'), ('1'), ('2'), ('!'), ('^')) AS x(c)
ORDER BY c COLLATE ebcdic;
 c
---
 !
 a
 b
 ^
 A
 B
 1
 2
```

#### 23.2.3.5. Referências externas para UTI [#](#ICU-EXTERNAL-REFERENCES)

Esta seção ([Seção 23.2.3](collation.md#ICU-CUSTOM-COLLATIONS)) é apenas uma breve visão geral do comportamento e das etiquetas de linguagem do ICU. Consulte os seguintes documentos para obter detalhes técnicos, opções adicionais e novo comportamento:

* [Padrão Técnico Unicode #35](https://www.unicode.org/reports/tr35/tr35-collation.html)
* [BCP 47](https://www.rfc-editor.org/info/bcp47)
* [Repositório CLDR](https://github.com/unicode-org/cldr/blob/master/common/bcp47/collation.xml)
* <https://unicode-org.github.io/icu/userguide/locale/>
* <https://unicode-org.github.io/icu/userguide/collation/>