## 4.3. Chamando funções [#](#SQL-SYNTAX-CALLING-FUNCS)

* [4.3.1. Usando notação posicional](sql-syntax-calling-funcs.md#SQL-SYNTAX-CALLING-FUNCS-POSITIONAL)
* [4.3.2. Usando notação nomeada](sql-syntax-calling-funcs.md#SQL-SYNTAX-CALLING-FUNCS-NAMED)
* [4.3.3. Usando notação mista](sql-syntax-calling-funcs.md#SQL-SYNTAX-CALLING-FUNCS-MIXED)

O PostgreSQL permite que funções com parâmetros nomeados sejam chamadas usando notação *posicionada* ou *nomeada*. A notação nomeada é especialmente útil para funções que têm um grande número de parâmetros, pois torna as associações entre os parâmetros e os argumentos reais mais explícitas e confiáveis. Na notação posicionada, uma chamada de função é escrita com seus valores de argumento na mesma ordem em que são definidos na declaração da função. Na notação nomeada, os argumentos são correspondidos aos parâmetros da função pelo nome e podem ser escritos em qualquer ordem. Para cada notação, também considere o efeito dos tipos de argumentos da função, documentado em [Seção 10.3][(typeconv-func.md "10.3. Functions")].

Em qualquer notação, os parâmetros que têm valores padrão definidos na declaração da função não precisam ser escritos na chamada. Mas isso é particularmente útil na notação nomeada, pois qualquer combinação de parâmetros pode ser omitida; enquanto que na notação posicional, os parâmetros só podem ser omitidos de direita para esquerda.

O PostgreSQL também suporta a notação *misturada*, que combina a notação posicional e a nomeada. Neste caso, os parâmetros posicionais são escritos primeiro e os parâmetros nomeados aparecem depois deles.

Os exemplos a seguir ilustrarão o uso de todas as três notações, utilizando a seguinte definição de função:

```
CREATE FUNCTION concat_lower_or_upper(a text, b text, uppercase boolean DEFAULT false)
RETURNS text
AS
$$
 SELECT CASE
        WHEN $3 THEN UPPER($1 || ' ' || $2)
        ELSE LOWER($1 || ' ' || $2)
        END;
$$
LANGUAGE SQL IMMUTABLE STRICT;
```

A função `concat_lower_or_upper` tem dois parâmetros obrigatórios, `a` e `b`. Além disso, há um parâmetro opcional `uppercase`, que tem como padrão `false`. As entradas `a` e `b` serão concatenadas e forçadas a maiúsculas ou minúsculas, dependendo do parâmetro `uppercase`. Os detalhes restantes desta definição da função não são importantes aqui (consulte [Capítulo 36][(extend.md "Chapter 36. Extending SQL")] para mais informações).

### 4.3.1. Uso da notação posicional [#](#SQL-SYNTAX-CALLING-FUNCS-POSITIONAL)

A notação posicional é o mecanismo tradicional para passar argumentos para funções no PostgreSQL. Um exemplo é:

```
SELECT concat_lower_or_upper('Hello', 'World', true);
 concat_lower_or_upper
-----------------------
 HELLO WORLD
(1 row)
```

Todos os argumentos são especificados em ordem. O resultado é maiúsculo, pois `uppercase` é especificado como `true`. Outro exemplo é:

```
SELECT concat_lower_or_upper('Hello', 'World');
 concat_lower_or_upper
-----------------------
 hello world
(1 row)
```

Aqui, o parâmetro `uppercase` é omitido, então ele recebe seu valor padrão de `false`, resultando em saída em minúsculas. Na notação posicional, os argumentos podem ser omitidos de direita para esquerda, desde que tenham valores padrão.

### 4.3.2. Uso de notação nomeada [#](#SQL-SYNTAX-CALLING-FUNCS-NAMED)

Na notação nomeada, o nome de cada argumento é especificado usando `=>` para separá-lo da expressão do argumento. Por exemplo:

```
SELECT concat_lower_or_upper(a => 'Hello', b => 'World');
 concat_lower_or_upper
-----------------------
 hello world
(1 row)
```

Novamente, o argumento `uppercase` foi omitido, então ele é definido implicitamente como `false`. Uma vantagem de usar notação nomeada é que os argumentos podem ser especificados em qualquer ordem, por exemplo:

```
SELECT concat_lower_or_upper(a => 'Hello', b => 'World', uppercase => true);
 concat_lower_or_upper
-----------------------
 HELLO WORLD
(1 row)

SELECT concat_lower_or_upper(a => 'Hello', uppercase => true, b => 'World');
 concat_lower_or_upper
-----------------------
 HELLO WORLD
(1 row)
```

Uma sintaxe mais antiga baseada em ":=" é suportada para compatibilidade reversa:

```
SELECT concat_lower_or_upper(a := 'Hello', uppercase := true, b := 'World');
 concat_lower_or_upper
-----------------------
 HELLO WORLD
(1 row)
```

### 4.3.3. Uso de notação mista [#](#SQL-SYNTAX-CALLING-FUNCS-MIXED)

A notação mista combina a notação posicional e a notação por nome. No entanto, como já mencionado, os argumentos por nome não podem preceder os argumentos posicionais. Por exemplo:

```
SELECT concat_lower_or_upper('Hello', 'World', uppercase => true);
 concat_lower_or_upper
-----------------------
 HELLO WORLD
(1 row)
```

Na consulta acima, os argumentos `a` e `b` são especificados positivamente, enquanto `uppercase` é especificado pelo nome. Neste exemplo, isso adiciona pouco, exceto documentação. Com uma função mais complexa que tem vários parâmetros que têm valores padrão, a notação nomeada ou mista pode economizar uma grande quantidade de escrita e reduzir as chances de erro.

### Nota

As notações de chamada nomeadas e misturadas atualmente não podem ser usadas ao chamar uma função agregada (mas elas funcionam quando uma função agregada é usada como uma função de janela).