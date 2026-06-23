## 43.1. Funções e Argumentos PL/Perl [#](#PLPERL-FUNCS)

Para criar uma função no idioma PL/Perl, use a sintaxe padrão [CREATE FUNCTION](sql-createfunction.md):

```
CREATE FUNCTION funcname (argument-types)
RETURNS return-type
-- function attributes can go here
AS $$
    # PL/Perl function body goes here
$$ LANGUAGE plperl;
```

O corpo da função é código Perl comum. Na verdade, o código de cola PL/Perl o envolve dentro de uma subrotina Perl. Uma função PL/Perl é chamada em um contexto escalar, então ela não pode retornar uma lista. Você pode retornar valores não escalares (arrays, registros e conjuntos) retornando uma referência, conforme discutido abaixo.

Em um procedimento PL/Perl, qualquer valor de retorno do código Perl é ignorado.

O PL/Perl também suporta blocos de código anônimo que são chamados com a declaração [DO](sql-do.md "DO"):

```
DO $$
    # PL/Perl code
$$ LANGUAGE plperl;
```

Um bloco de código anônimo não recebe argumentos e qualquer valor que ele possa retornar é descartado. Caso contrário, ele se comporta exatamente como uma função.

Nota

O uso de subrotinas aninhadas nomeadas é perigoso em Perl, especialmente se elas se referirem a variáveis lexicais no escopo interno. Como uma função PL/Perl é envolvida em uma subrotina, qualquer subrotina nomeada que você colocar dentro de uma será aninhada. Em geral, é muito mais seguro criar subrotinas anônimas que você chame via um coderef. Para mais informações, consulte as entradas para `Variable "%s" will not stay shared` e `Variable "%s" is not available` na página do manual perldiag, ou pesquise na Internet por “subrotina aninhada nomeada em perl”.

A sintaxe do comando `CREATE FUNCTION` exige que o corpo da função seja escrito como uma constante de string. Geralmente, é mais conveniente usar a citação em dólar (ver [Seção 4.1.2.4](sql-syntax-lexical.md#SQL-SYNTAX-DOLLAR-QUOTING)) para a constante de string. Se você optar por usar a sintaxe de string de escape `E''`, deve duplicar quaisquer aspas simples (`'`) e barras invertidas (`\`) usadas no corpo da função (ver [Seção 4.1.2.1](sql-syntax-lexical.md#SQL-SYNTAX-STRINGS)).

Os argumentos e os resultados são tratados como em qualquer outra subrotina do Perl: os argumentos são passados em `@_`, e um valor de resultado é retornado com `return` ou como a última expressão avaliada na função.

Por exemplo, uma função que retorne o maior de dois valores inteiros pode ser definida da seguinte forma:

```
CREATE FUNCTION perl_max (integer, integer) RETURNS integer AS $$
    if ($_[0] > $_[1]) { return $_[0]; }
    return $_[1];
$$ LANGUAGE plperl;
```

Nota

Os argumentos serão convertidos do codificação do banco de dados para UTF-8 para uso dentro do PL/Perl, e então convertidos de UTF-8 de volta para a codificação do banco de dados ao retornar.

Se um valor nulo do SQL for passado para uma função, o valor do argumento aparecerá como “definido” em Perl. A definição de função acima não se comportará de maneira muito agradável com entradas nulos (de fato, ela agirá como se fossem zeros). Podíamos adicionar `STRICT` à definição da função para fazer com que o PostgreSQL faça algo mais razoável: se um valor nulo for passado, a função não será chamada em absoluto, mas apenas retornará um resultado nulo automaticamente. Alternativamente, podemos verificar entradas indefinidas no corpo da função. Por exemplo, suponha que quiséssemos `perl_max` com um argumento nulo e um argumento não nulo para retornar o argumento não nulo, em vez de um valor nulo:

```
CREATE FUNCTION perl_max (integer, integer) RETURNS integer AS $$
    my ($x, $y) = @_;
    if (not defined $x) {
        return undef if not defined $y;
        return $y;
    }
    return $x if not defined $y;
    return $x if $x > $y;
    return $y;
$$ LANGUAGE plperl;
```

Como mostrado acima, para retornar um valor nulo do SQL de uma função PL/Perl, retorne um valor indefinido. Isso pode ser feito, independentemente de a função ser estrita ou

Qualquer coisa em um argumento de função que não seja uma referência é uma string, que é a representação de texto externo padrão do PostgreSQL para o tipo de dados relevante. No caso de tipos numéricos ou de texto comuns, o Perl fará a coisa certa e, normalmente, o programador não precisará se preocupar com isso. No entanto, em outros casos, o argumento precisará ser convertido em uma forma mais utilizável no Perl. Por exemplo, a função `decode_bytea` pode ser usada para converter um argumento do tipo `bytea` em binário não escapado.

Da mesma forma, os valores passados de volta ao PostgreSQL devem estar no formato de representação de texto externo. Por exemplo, a função `encode_bytea` pode ser usada para escapar dados binários para um valor de retorno do tipo `bytea`.

Um caso que é particularmente importante são os valores booleanos. Como acabou de ser dito, o comportamento padrão para os valores de `bool` é que eles são passados para o Perl como texto, ou seja, `'t'` ou `'f'`. Isso é problemático, pois o Perl não tratará `'f'` como falso! É possível melhorar a situação usando uma "transformação" (consulte [CREATE TRANSFORM](sql-createtransform.md "CREATE TRANSFORM")). Transformações adequadas são fornecidas pela extensão `bool_plperl`. Para usá-la, instale a extensão:

```
CREATE EXTENSION bool_plperl;  -- or bool_plperlu for PL/PerlU
```

Em seguida, use o atributo de função `TRANSFORM` para uma função PL/Perl que recebe ou retorna `bool`, por exemplo:

```
CREATE FUNCTION perl_and(bool, bool) RETURNS bool
TRANSFORM FOR TYPE bool
AS $$
  my ($a, $b) = @_;
  return $a && $b;
$$ LANGUAGE plperl;
```

Quando essa transformação for aplicada, os argumentos `bool` serão vistos pelo Perl como sendo `1` ou vazios, portanto, verdadeiros ou falsos, respectivamente. Se o resultado da função for do tipo `bool`, ele será verdadeiro ou falso de acordo com o fato de o Perl avaliar o valor retornado como verdadeiro. Transformações semelhantes também são realizadas para argumentos e resultados de consultas booleanas realizadas dentro da função ([Seção 43.3.1](plperl-builtins.md#PLPERL-DATABASE)).

O Perl pode retornar arrays do PostgreSQL como referências para arrays do Perl. Aqui está um exemplo:

```
CREATE OR REPLACE function returns_array()
RETURNS text[][] AS $$
    return [['a"b','c,d'],['e\\f','g']];
$$ LANGUAGE plperl;

select returns_array();
```

Perl passa arrays do PostgreSQL como um objeto `PostgreSQL::InServer::ARRAY` abençoado. Esse objeto pode ser tratado como uma referência de matriz ou uma string, permitindo compatibilidade reversa com código Perl escrito para versões do PostgreSQL inferiores a 9.1. Por exemplo:

```
CREATE OR REPLACE FUNCTION concat_array_elements(text[]) RETURNS TEXT AS $$
    my $arg = shift;
    my $result = "";
    return undef if (!defined $arg);

    # as an array reference
    for (@$arg) {
        $result .= $_;
    }

    # also works as a string
    $result .= $arg;

    return $result;
$$ LANGUAGE plperl;

SELECT concat_array_elements(ARRAY['PL','/','Perl']);
```

Nota

Matrizes multidimensionais são representadas como referências a matrizes de dimensão inferior, de forma comum a todos os programadores Perl.

Os argumentos do tipo composto são passados para a função como referências a hashes. As chaves do hash são os nomes de atributo do tipo composto. Aqui está um exemplo:

```
CREATE TABLE employee (
    name text,
    basesalary integer,
    bonus integer
);

CREATE FUNCTION empcomp(employee) RETURNS integer AS $$
    my ($emp) = @_;
    return $emp->{basesalary} + $emp->{bonus};
$$ LANGUAGE plperl;

SELECT name, empcomp(employee.*) FROM employee;
```

Uma função PL/Perl pode retornar um resultado de tipo composto usando a mesma abordagem: retornar uma referência a um hash que tenha os atributos necessários. Por exemplo:

```
CREATE TYPE testrowperl AS (f1 integer, f2 text, f3 text);

CREATE OR REPLACE FUNCTION perl_row() RETURNS testrowperl AS $$
    return {f2 => 'hello', f1 => 1, f3 => 'world'};
$$ LANGUAGE plperl;

SELECT * FROM perl_row();
```

Quaisquer colunas no tipo de dados do resultado declarado que não estão presentes no hash serão devolvidas como valores nulos.

Da mesma forma, os argumentos de saída dos procedimentos podem ser retornados como uma referência de hash:

```
CREATE PROCEDURE perl_triple(INOUT a integer, INOUT b integer) AS $$
    my ($a, $b) = @_;
    return {a => $a * 3, b => $b * 3};
$$ LANGUAGE plperl;

CALL perl_triple(5, 10);
```

As funções PL/Perl também podem retornar conjuntos de tipos escalares ou compostos. Geralmente, você deseja retornar linhas uma de cada vez, tanto para acelerar o tempo de inicialização quanto para evitar agrupar todo o conjunto de resultados na memória. Você pode fazer isso com `return_next`, como ilustrado abaixo. Note que, após o último `return_next`, você deve colocar `return` ou (melhor) `return undef`.

```
CREATE OR REPLACE FUNCTION perl_set_int(int)
RETURNS SETOF INTEGER AS $$
    foreach (0..$_[0]) {
        return_next($_);
    }
    return undef;
$$ LANGUAGE plperl;

SELECT * FROM perl_set_int(5);

CREATE OR REPLACE FUNCTION perl_set()
RETURNS SETOF testrowperl AS $$
    return_next({ f1 => 1, f2 => 'Hello', f3 => 'World' });
    return_next({ f1 => 2, f2 => 'Hello', f3 => 'PostgreSQL' });
    return_next({ f1 => 3, f2 => 'Hello', f3 => 'PL/Perl' });
    return undef;
$$ LANGUAGE plperl;
```

Para conjuntos de resultados pequenos, você pode retornar uma referência a um array que contenha escalares, referências a arrays ou referências a hashes para tipos simples, tipos de array e tipos compostos, respectivamente. Aqui estão alguns exemplos simples de retornar todo o conjunto de resultados como uma referência a um array:

```
CREATE OR REPLACE FUNCTION perl_set_int(int) RETURNS SETOF INTEGER AS $$
    return [0..$_[0]];
$$ LANGUAGE plperl;

SELECT * FROM perl_set_int(5);

CREATE OR REPLACE FUNCTION perl_set() RETURNS SETOF testrowperl AS $$
    return [
        { f1 => 1, f2 => 'Hello', f3 => 'World' },
        { f1 => 2, f2 => 'Hello', f3 => 'PostgreSQL' },
        { f1 => 3, f2 => 'Hello', f3 => 'PL/Perl' }
    ];
$$ LANGUAGE plperl;

SELECT * FROM perl_set();
```

Se você deseja usar o `strict` pragma com seu código, você tem algumas opções. Para uso global temporário, você pode `SET` `plperl.use_strict` para true. Isso afetará as compilações subsequentes das funções PL/Perl, mas não as funções já compiladas na sessão atual. Para uso global permanente, você pode definir `plperl.use_strict` para true no arquivo `postgresql.conf`.

Para uso permanente em funções específicas, você pode simplesmente colocar:

```
use strict;
```

no topo do corpo da função.

O `feature` pragma também está disponível para `use` se o seu Perl for versão 5.10.0 ou superior.