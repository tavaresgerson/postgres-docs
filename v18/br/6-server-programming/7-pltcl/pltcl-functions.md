## 42.2. Funções e Argumentos PL/Tcl [#](#PLTCL-FUNCTIONS)

Para criar uma função no idioma PL/Tcl, use a sintaxe padrão [CREATE FUNCTION](sql-createfunction.md "CREATE FUNCTION"):

```
CREATE FUNCTION funcname (argument-types) RETURNS return-type AS $$
    # PL/Tcl function body
$$ LANGUAGE pltcl;
```

PL/TclU é o mesmo, exceto que a língua deve ser especificada como `pltclu`.

O corpo da função é simplesmente um trecho de script Tcl. Quando a função é chamada, os valores dos argumentos são passados para o script Tcl como variáveis nomeadas `1`... `n`. O resultado é retornado pelo código Tcl da maneira usual, com uma declaração `return`. Em um procedimento, o valor de retorno do código Tcl é ignorado.

Por exemplo, uma função que retorne o maior de dois valores inteiros pode ser definida da seguinte forma:

```
CREATE FUNCTION tcl_max(integer, integer) RETURNS integer AS $$
    if {$1 > $2} {return $1}
    return $2
$$ LANGUAGE pltcl STRICT;
```

Observe a cláusula `STRICT`, que nos poupa de ter que pensar em valores de entrada nulos: se um valor nulo for passado, a função não será chamada em absoluto, mas apenas retornará um resultado nulo automaticamente.

Em uma função não estrita, se o valor real de um argumento for nulo, a variável correspondente `$n` será definida como uma string vazia. Para detectar se um argumento específico é nulo, use a função `argisnull`. Por exemplo, suponha que quiséssemos que `tcl_max` com um argumento nulo e um não nulo retorne o argumento não nulo, em vez de nulo:

```
CREATE FUNCTION tcl_max(integer, integer) RETURNS integer AS $$
    if {[argisnull 1]} {
        if {[argisnull 2]} { return_null }
        return $2
    }
    if {[argisnull 2]} { return $1 }
    if {$1 > $2} {return $1}
    return $2
$$ LANGUAGE pltcl;
```

Como mostrado acima, para retornar um valor nulo de uma função PL/Tcl, execute `return_null`. Isso pode ser feito independentemente de a função ser estrita ou

Os argumentos do tipo composto são passados para a função como arrays Tcl. Os nomes dos elementos do array são os nomes dos atributos do tipo composto. Se um atributo na linha passada tiver o valor nulo, ele não aparecerá no array. Aqui está um exemplo:

```
CREATE TABLE employee (
    name text,
    salary integer,
    age integer
);

CREATE FUNCTION overpaid(employee) RETURNS boolean AS $$
    if {200000.0 < $1(salary)} {
        return "t"
    }
    if {$1(age) < 30 && 100000.0 < $1(salary)} {
        return "t"
    }
    return "f"
$$ LANGUAGE pltcl;
```

As funções PL/Tcl também podem retornar resultados de tipo composto. Para isso, o código Tcl deve retornar uma lista de pares de nome de coluna/valor que correspondam ao tipo de resultado esperado. Quaisquer nomes de coluna omitidos da lista são retornados como nulos, e um erro é gerado se houver nomes de coluna inesperados. Aqui está um exemplo:

```
CREATE FUNCTION square_cube(in int, out squared int, out cubed int) AS $$
    return [list squared [expr {$1 * $1}] cubed [expr {$1 * $1 * $1}]]
$$ LANGUAGE pltcl;
```

Os argumentos de saída dos procedimentos são devolvidos da mesma maneira, por exemplo:

```
CREATE PROCEDURE tcl_triple(INOUT a integer, INOUT b integer) AS $$
    return [list a [expr {$1 * 3}] b [expr {$2 * 3}]]
$$ LANGUAGE pltcl;

CALL tcl_triple(5, 10);
```

DICA

A lista de resultados pode ser feita a partir de uma representação de matriz do conjunto desejado com o comando Tcl `array get`. Por exemplo:

```
CREATE FUNCTION raise_pay(employee, delta int) RETURNS employee AS $$
    set 1(salary) [expr {$1(salary) + $2}]
    return [array get 1]
$$ LANGUAGE pltcl;
```

As funções PL/Tcl podem retornar conjuntos. Para isso, o código Tcl deve chamar `return_next` uma vez por linha a ser retornada, passando o valor apropriado ao retornar um tipo escalar, ou uma lista de pares de nome/valor de coluna ao retornar um tipo composto. Aqui está um exemplo retornando um tipo escalar:

```
CREATE FUNCTION sequence(int, int) RETURNS SETOF int AS $$
    for {set i $1} {$i < $2} {incr i} {
        return_next $i
    }
$$ LANGUAGE pltcl;
```

e aqui está um retornando um tipo composto:

```
CREATE FUNCTION table_of_squares(int, int) RETURNS TABLE (x int, x2 int) AS $$
    for {set i $1} {$i < $2} {incr i} {
        return_next [list x $i x2 [expr {$i * $i}]]
    }
$$ LANGUAGE pltcl;
```
