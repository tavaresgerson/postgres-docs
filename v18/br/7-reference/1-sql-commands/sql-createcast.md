## Crie CAST

CREATE CAST — definir um novo elenco

## Sinopse

```
CREATE CAST (source_type AS target_type)
    WITH FUNCTION function_name [ (argument_type [, ...]) ]
    [ AS ASSIGNMENT | AS IMPLICIT ]

CREATE CAST (source_type AS target_type)
    WITHOUT FUNCTION
    [ AS ASSIGNMENT | AS IMPLICIT ]

CREATE CAST (source_type AS target_type)
    WITH INOUT
    [ AS ASSIGNMENT | AS IMPLICIT ]
```

## Descrição

`CREATE CAST` define um novo cast. Um cast especifica como realizar uma conversão entre dois tipos de dados. Por exemplo,

```
SELECT CAST(42 AS float8);
```

converte a constante inteira 42 para o tipo `float8` invocando uma função especificada anteriormente, neste caso `float8(int4)`. (Se não houver uma transformação adequada definida, a conversão falha.)

Dois tipos podem ser *binários coercíveis*, o que significa que a conversão pode ser realizada “gratuitamente” sem a necessidade de invocar qualquer função. Isso exige que os valores correspondentes utilizem a mesma representação interna. Por exemplo, os tipos `text` e `varchar` são binários coercíveis em ambos os sentidos. A coercibilidade binária não é necessariamente uma relação simétrica. Por exemplo, o cast de `xml` para `text` pode ser realizado gratuitamente na implementação atual, mas a direção inversa requer uma função que realize pelo menos uma verificação de sintaxe. (Dois tipos que são binários coercíveis em ambos os sentidos também são referidos como compatíveis binários.)

Você pode definir uma cast como uma cast de conversão de *I/O* usando a sintaxe `WITH INOUT`. Uma cast de conversão de I/O é realizada invocando a função de saída do tipo de dados de origem e passando a string resultante para a função de entrada do tipo de dados de destino. Em muitos casos comuns, essa característica evita a necessidade de escrever uma função de cast separada para conversão. Uma cast de conversão de I/O age da mesma forma que uma cast regular baseada em função; apenas a implementação é diferente.

Por padrão, uma cast só pode ser invocada por meio de um pedido explícito de cast, ou seja, um `CAST(x AS typename)` explícito ou *`x`*`::`*`typename`* explícito.

Se o conjunto de dados estiver marcado `AS ASSIGNMENT`, ele pode ser invocado implicitamente ao atribuir um valor a uma coluna do tipo de dados de destino. Por exemplo, supondo que `foo.f1` é uma coluna do tipo `text`, então:

```
INSERT INTO foo (f1) VALUES (42);
```

será permitido se o elenco do tipo `integer` para o tipo `text` estiver marcado `AS ASSIGNMENT`, caso contrário, não. (Geralmente usamos o termo *cast de atribuição* para descrever esse tipo de cast.)

Se o cast estiver marcado `AS IMPLICIT`, ele pode ser invocado implicitamente em qualquer contexto, seja em uma atribuição ou internamente em uma expressão. (Geralmente, usamos o termo *cast implícito* para descrever esse tipo de cast.) Por exemplo, considere esta consulta:

```
SELECT 2 + 4.0;
```

O analisador inicialmente marca as constantes como sendo do tipo `integer` e `numeric`, respectivamente. Não há operador `integer` `+` `numeric` nos catálogos do sistema, mas há um operador `numeric` `+` `numeric`. Portanto, a consulta terá sucesso se houver um cast de `integer` para `numeric` disponível e marcado como `AS IMPLICIT` — o que, de fato, é o caso. O analisador aplicará o cast implícito e resolverá a consulta como se tivesse sido escrita

```
SELECT CAST ( 2 AS numeric ) + 4.0;
```

Agora, os catálogos também fornecem um cast de `numeric` para `integer`. Se esse cast fosse marcado `AS IMPLICIT` — o que não é o caso — o analisador seria obrigado a escolher entre a interpretação acima e a alternativa de converter a constante `numeric` para `integer` e aplicar o operador `integer` `+` `integer`. Sem qualquer conhecimento sobre qual escolha preferir, ele desistiria e declararia a consulta ambígua. O fato de que apenas um dos dois casts é implícito é a maneira como ensinamos ao analisador a preferir a resolução de uma expressão misturada de `numeric` e `integer` como `numeric`; não há conhecimento embutido sobre isso.

É prudente ser conservador ao marcar casts como implícitos. Uma abundância excessiva de caminhos de casting implícito pode fazer com que o PostgreSQL escolha interpretações surpreendentes dos comandos, ou que não consiga resolver comandos de todo, porque há múltiplas interpretações possíveis. Uma boa regra é fazer um cast implicitamente invocable apenas para transformações que preservam a informação entre tipos na mesma categoria de tipo geral. Por exemplo, o cast de `int2` para `int4` pode ser razoavelmente implícito, mas o cast de `float8` para `int4` provavelmente deve ser apenas de atribuição. Casts entre categorias de tipo, como `text` para `int4`, devem ser feitos apenas explicitamente.

### Nota

Às vezes, é necessário, por razões de usabilidade ou conformidade com padrões, fornecer múltiplos casts implícitos entre um conjunto de tipos, resultando em ambiguidade que não pode ser evitada como acima. O analisador tem uma heurística de fallback baseada em *categorias de tipo* e *tipos preferidos* que podem ajudar a fornecer o comportamento desejado em tais casos. Consulte [CREATE TYPE](sql-createtype.md) para obter mais informações.

Para poder criar um cast, você deve possuir o tipo de dados fonte ou alvo e ter o privilégio `USAGE` no outro tipo. Para criar um cast binário coerível, você deve ser um superusuário. (Essa restrição é feita porque uma conversão errada de cast binária coerível pode facilmente fazer o servidor falhar.)

## Parâmetros

*`source_type`*: O nome do tipo de dados fonte do cast.

*`target_type`*: O nome do tipo de dados de destino do cast.

`function_name[(argument_type [, ...])]`: A função usada para realizar o cast. O nome da função pode ser qualificado pelo esquema. Se não for, a função será procurada no caminho de pesquisa do esquema. O tipo de dados do resultado da função deve corresponder ao tipo alvo do cast. Seus argumentos são discutidos abaixo. Se nenhuma lista de argumentos for especificada, o nome da função deve ser único em seu esquema.

`WITHOUT FUNCTION`: Indica que o tipo de fonte é binário coerível com o tipo de destino, portanto, não é necessária nenhuma função para realizar o cast.

`WITH INOUT`: Indica que a cast é uma cast de conversão de entrada/saída, realizada invocando a função de saída do tipo de dados de origem e passando a string resultante para a função de entrada do tipo de dados de destino.

`AS ASSIGNMENT`: Indica que o cast pode ser invocado implicitamente em contextos de atribuição.

`AS IMPLICIT`: Indica que o cast pode ser invocado implicitamente em qualquer contexto.

As funções de implementação de cast podem ter de um a três argumentos. O primeiro argumento deve ser idêntico ou binário-coercível com o tipo de origem da cast. O segundo argumento, se presente, deve ser do tipo `integer`; ele recebe o modificador de tipo associado ao tipo de destino, ou `-1` se não houver nenhum. O terceiro argumento, se presente, deve ser do tipo `boolean`; ele recebe `true` se a cast for uma cast explícita, `false` caso contrário. (Bizarramente, o padrão SQL exige comportamentos diferentes para casts explícitos e implícitos em alguns casos. Este argumento é fornecido para funções que devem implementar tais casts. Não é recomendado que você projete seus próprios tipos de dados para que isso seja importante.)

O tipo de retorno de uma função de cast deve ser idêntico ou binário-coercível ao tipo alvo da cast.

Normalmente, uma cast deve ter diferentes tipos de dados de origem e destino. No entanto, é permitido declarar uma cast com tipos de origem e destino idênticos se ela tiver uma função de implementação de cast com mais de um argumento. Isso é usado para representar funções de coerção de comprimento específicas do tipo nos catálogos do sistema. A função nomeada é usada para coercer um valor do tipo para o valor do modificador de tipo dado pelo seu segundo argumento.

Quando um cast tem tipos de origem e destino diferentes e uma função que recebe mais de um argumento, ele suporta a conversão de um tipo para outro e a aplicação de uma coerção de comprimento em um único passo. Quando não há tal entrada disponível, a coerção para um tipo que usa um modificador de tipo envolve duas etapas de cast, uma para converter entre tipos de dados e uma segunda para aplicar o modificador.

Um cast para ou a partir de um tipo de domínio atualmente não tem efeito. O cast para ou a partir de um domínio usa os casts associados ao seu tipo subjacente.

## Notas

Use `DROP CAST`(sql-dropcast.md "DROP CAST") para remover os casts definidos pelo usuário.

Lembre-se de que, se você quiser ser capaz de converter tipos em ambas as direções, você precisa declarar os casts explicitamente em ambas as direções.

Normalmente, não é necessário criar casts entre tipos definidos pelo usuário e os tipos padrão de string (`text`, `varchar` e `char(n)`, bem como tipos definidos pelo usuário que são definidos para estarem na categoria de string). O PostgreSQL oferece conversões automáticas de I/O para isso. As conversões automáticas para tipos de string são tratadas como casts de atribuição, enquanto as conversões automáticas de tipos de string são explícitas apenas. Você pode sobrepor esse comportamento declarando seu próprio cast para substituir um cast automático, mas geralmente a única razão para fazer isso é se você deseja que a conversão seja mais facilmente invocavel do que a configuração padrão de apenas atribuição ou apenas explícita. Outra razão possível é que você deseja que a conversão se comporte de maneira diferente da função de I/O do tipo; mas isso é suficientemente surpreendente para que você pense duas vezes se é uma boa ideia. (Um pequeno número dos tipos embutidos tem, de fato, comportamentos diferentes para conversões, principalmente devido a requisitos do padrão SQL.)

Embora não seja obrigatório, é recomendável que você continue a seguir essa antiga convenção de nomear as funções de implementação de cast após o tipo de dados alvo. Muitos usuários estão acostumados a poder realizar casts de tipos de dados usando uma notação em estilo de função, ou seja, *`typename`*(*`x`*) . Essa notação, na verdade, não é nada mais do que uma chamada da função de implementação de cast; não é tratada especialmente como um cast. Se suas funções de conversão não forem nomeadas para suportar essa convenção, você terá usuários surpresos. Como o PostgreSQL permite a sobrecarga do mesmo nome de função com diferentes tipos de argumentos, não há dificuldade em ter várias funções de conversão de diferentes tipos que usam o nome do tipo alvo.

### Nota

Na verdade, o parágrafo anterior é uma simplificação excessiva: há dois casos em que uma construção de chamada de função será tratada como uma solicitação de cast sem ter sido correspondida a uma função real. Se uma chamada de função *`name`*(*`x`*) não corresponder exatamente a nenhuma função existente, mas *`name`* é o nome de um tipo de dados e `pg_cast` fornece uma cast binária-coercível para este tipo a partir do tipo de *`x`*, então a chamada será interpretada como uma cast binária-coercível. Esta exceção é feita para que casts binária-coercíveis possam ser invocados usando sintaxe funcional, mesmo que não tenham nenhuma função. Da mesma forma, se não houver uma entrada em `pg_cast` mas a cast seria para ou a partir de um tipo de string, a chamada será interpretada como uma cast de conversão de E/S. Esta exceção permite que casts de conversão de E/S sejam invocados usando sintaxe funcional.

### Nota

Há também uma exceção à exceção: as conversões de saída/entrada de tipos compostos para tipos de string não podem ser invocadas usando a sintaxe funcional, mas devem ser escritas em sintaxe de cast explícita (ou seja, a notação `CAST` ou `::`). Essa exceção foi adicionada porque, após a introdução de conversões de saída/entrada fornecidas automaticamente, foi descoberto que era muito fácil invocar acidentalmente tal conversão quando uma referência a uma função ou coluna era pretendida.

## Exemplos

Para criar uma atribuição de tipo `bigint` para o tipo `int4` usando a função `int4(bigint)`:

```
CREATE CAST (bigint AS int4) WITH FUNCTION int4(bigint) AS ASSIGNMENT;
```

(Este elenco já está pré-definido no sistema.)

## Compatibilidade

O comando `CREATE CAST` está de acordo com o padrão SQL, exceto que o SQL não prevê tipos binariamente coercíveis ou argumentos extras para funções de implementação. `AS IMPLICIT` é uma extensão do PostgreSQL também.

## Veja também

[Crie função](sql-createfunction.md "CREATE FUNCTION"), [Crie tipo](sql-createtype.md "CREATE TYPE"), [Remeta tipo](sql-dropcast.md "DROP CAST")