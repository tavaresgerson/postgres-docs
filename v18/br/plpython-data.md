## 44.2. Valores dos dados [#](#PLPYTHON-DATA)

* [44.2.1. Mapeamento do Tipo de Dados](plpython-data.md#PLPYTHON-DATA-TYPE-MAPPING)
* [44.2.2. Nulo, Nenhum](plpython-data.md#PLPYTHON-DATA-NULL)
* [44.2.3. Arrays, Listas](plpython-data.md#PLPYTHON-ARRAYS)
* [44.2.4. Tipos Compostos](plpython-data.md#PLPYTHON-DATA-COMPOSITE-TYPES)
* [44.2.5. Funções de Conjunto que Retornam Conjuntos](plpython-data.md#PLPYTHON-DATA-SET-RETURNING-FUNCS)

De modo geral, o objetivo do PL/Python é fornecer uma mapeia “natural” entre os mundos PostgreSQL e Python. Isso informa as regras de mapeia de dados descritas abaixo.

### 44.2.1. Mapeamento do tipo de dados [#](#PLPYTHON-DATA-TYPE-MAPPING)

Quando uma função PL/Python é chamada, seus argumentos são convertidos de seu tipo de dados PostgreSQL para um tipo correspondente em Python:

* PostgreSQL `boolean` é convertido para Python `bool`.
* PostgreSQL `smallint`, `int`, `bigint` e `oid` são convertidos para Python `int`.
* PostgreSQL `real` e `double` são convertidos para Python `float`.
* PostgreSQL `numeric` é convertido para Python `Decimal`. Esse tipo é importado do pacote `cdecimal` se estiver disponível. Caso contrário, `decimal.Decimal` da biblioteca padrão será usado. `cdecimal` é significativamente mais rápido que `decimal`. No Python 3.3 e superior, no entanto, `cdecimal` foi integrado à biblioteca padrão sob o nome `decimal`, então não há mais nenhuma diferença.
* PostgreSQL `bytea` é convertido para Python `bytes`.
* Todos os outros tipos de dados, incluindo os tipos de string de caracteres de PostgreSQL, são convertidos para um Python `str` (em Unicode como todas as strings em Python).
* Para tipos de dados não escalares, veja abaixo.

Quando uma função PL/Python retorna, seu valor de retorno é convertido para o tipo de dados de retorno declarado da função no PostgreSQL da seguinte forma:

* Quando o tipo de retorno do PostgreSQL é `boolean`, o valor de retorno será avaliado como verdadeiro de acordo com as regras do *Python*. Isso significa que 0 e a string vazia são falsos, mas notavelmente `'f'` é verdadeiro.
* Quando o tipo de retorno do PostgreSQL é `bytea`, o valor de retorno será convertido para `bytes` do Python usando os respectivos construtores Python, com o resultado sendo convertido para `bytea`.
* Para todos os outros tipos de retorno do PostgreSQL, o valor de retorno é convertido para uma string usando o construtor Python `str`, e o resultado é passado para a função de entrada do tipo de dados do PostgreSQL. (Se o valor do Python é um `float`, ele é convertido usando o construtor `repr` em vez de `str`, para evitar perda de precisão.)

As strings são automaticamente convertidas para o codificação do servidor PostgreSQL quando são passadas para o PostgreSQL. * Para tipos de dados que não são escalares, veja abaixo.

Observe que os desalinhamentos lógicos entre o tipo de retorno declarado do PostgreSQL e o tipo de dados Python do objeto de retorno real não são sinalizados; o valor será convertido de qualquer forma.

### 44.2.2. Nulo, Nenhum [#](#PLPYTHON-DATA-NULL)

Se um valor nulo do SQL for passado para uma função, o valor do argumento aparecerá como `None` no Python. Por exemplo, a definição da função de `pymax` mostrada em [Seção 44.1][(plpython-funcs.md "44.1. PL/Python Functions")] retornará a resposta errada para entradas nulos. Podíamos adicionar `STRICT` à definição da função para fazer com que o PostgreSQL faça algo mais razoável: se um valor nulo for passado, a função não será chamada em absoluto, mas apenas retornará um resultado nulo automaticamente. Alternativamente, podemos verificar entradas nulos no corpo da função:

```
CREATE FUNCTION pymax (a integer, b integer)
  RETURNS integer
AS $$
  if (a is None) or (b is None):
    return None
  if a > b:
    return a
  return b
$$ LANGUAGE plpython3u;
```

Como mostrado acima, para retornar um valor nulo do SQL de uma função PL/Python, retorne o valor `None`. Isso pode ser feito, independentemente de a função ser estrita ou

### 44.2.3. Arrays, Listas [#](#PLPYTHON-ARRAYS)

Os valores de matriz SQL são passados para o PL/Python como uma lista Python. Para retornar um valor de matriz SQL de uma função PL/Python, retorne uma lista Python:

```
CREATE FUNCTION return_arr()
  RETURNS int[]
AS $$
return [1, 2, 3, 4, 5]
$$ LANGUAGE plpython3u;

SELECT return_arr();
 return_arr
-------------
 {1,2,3,4,5}
(1 row)
```

Os arrays multidimensionais são passados para o PL/Python como listas Python aninhadas. Um array 2-dimensional, por exemplo, é uma lista de listas. Ao retornar um array SQL multidimensional a partir de uma função PL/Python, as listas internas em cada nível devem ter o mesmo tamanho. Por exemplo:

```
CREATE FUNCTION test_type_conversion_array_int4(x int4[]) RETURNS int4[] AS $$
plpy.info(x, type(x))
return x
$$ LANGUAGE plpython3u;

SELECT * FROM test_type_conversion_array_int4(ARRAY[[1,2,3],[4,5,6]]);
INFO:  ([[1, 2, 3], [4, 5, 6]], <type 'list'>)
 test_type_conversion_array_int4
---------------------------------
 {{1,2,3},{4,5,6}}
(1 row)
```

Outras sequências do Python, como tuplas, também são aceitas para compatibilidade reversa com versões do PostgreSQL 9.6 e versões anteriores, quando matrizes multidimensionais não eram suportadas. No entanto, elas são sempre tratadas como matrizes unidimensionais, porque são ambíguas com tipos compostos. Por esse mesmo motivo, quando um tipo composto é usado em uma matriz multidimensional, ele deve ser representado por uma tupla, em vez de uma lista.

Observe que, em Python, as strings são sequências, o que pode ter efeitos indesejáveis que podem ser familiares aos programadores do Python:

```
CREATE FUNCTION return_str_arr()
  RETURNS varchar[]
AS $$
return "hello"
$$ LANGUAGE plpython3u;

SELECT return_str_arr();
 return_str_arr
----------------
 {h,e,l,l,o}
(1 row)
```

### 44.2.4. Tipos compostos [#](#PLPYTHON-DATA-COMPOSITE-TYPES)

Os argumentos do tipo composto são passados para a função como mapeamentos em Python. Os nomes dos elementos do mapeamento são os nomes dos atributos do tipo composto. Se um atributo na linha passada tiver o valor nulo, ele terá o valor [[`None`] ] no mapeamento. Aqui está um exemplo:

```
CREATE TABLE employee (
  name text,
  salary integer,
  age integer
);

CREATE FUNCTION overpaid (e employee)
  RETURNS boolean
AS $$
  if e["salary"] > 200000:
    return True
  if (e["age"] < 30) and (e["salary"] > 100000):
    return True
  return False
$$ LANGUAGE plpython3u;
```

Existem várias maneiras de retornar tipos de linha ou compostos de uma função Python. Os exemplos a seguir assumem que temos:

```
CREATE TYPE named_value AS (
  name   text,
  value  integer
);
```

Um resultado composto pode ser retornado como:

Tipo de sequência (uma tupla ou uma lista, mas não um conjunto, pois não é indexável): Os objetos de sequência retornados devem ter o mesmo número de itens que o tipo de resultado composto tem campos. O item com índice 0 é atribuído ao primeiro campo do tipo composto, 1 ao segundo e assim por diante. Por exemplo:

``` CREATE FUNCTION make_pair (name text, value integer) RETURNS named_value AS $$ return ( name, value ) # or alternatively, as list: return [ name, value ] $$ LANGUAGE plpython3u;
    ```

Para retornar um SQL nulo para qualquer coluna, insira `None` na posição correspondente.

Quando um array de tipos compostos é retornado, ele não pode ser retornado como uma lista, porque é ambíguo se a lista Python representa um tipo composto ou outra dimensão do array.

Mapeamento (dicionário): O valor para cada coluna do tipo de resultado é recuperado do mapeamento com o nome da coluna como chave. Exemplo:

``` CREATE FUNCTION make_pair (name text, value integer) RETURNS named_value AS $$ return { "name": name, "value": value } $$ LANGUAGE plpython3u;
    ```

Qualquer par chave/valor adicional do dicionário é ignorado. Chaves ausentes são tratadas como erros. Para retornar um valor nulo do SQL para qualquer coluna, insira `None` com o nome da coluna correspondente como chave.

Objeto (qualquer objeto que forneça o método `__getattr__`)
:   Funciona da mesma forma que um mapeamento.
    Exemplo:

    ```
    CREATE FUNCTION make_pair (name text, value integer) RETURNS named_value AS $$ class named_value: def __init__ (self, n, v): self.name = n self.value = v return named_value(name, value)

      # or simply
      class nv: pass nv.name = name nv.value = value return nv $$ LANGUAGE plpython3u;
    ```

Também são suportadas funções com parâmetros `OUT`. Por exemplo:

```
CREATE FUNCTION multiout_simple(OUT i integer, OUT j integer) AS $$ return (1, 2) $$ LANGUAGE plpython3u;

SELECT * FROM multiout_simple();
```

Os parâmetros de saída dos procedimentos são passados de volta da mesma maneira. Por exemplo:

```
CREATE PROCEDURE python_triple(INOUT a integer, INOUT b integer) AS $$ return (a * 3, b * 3) $$ LANGUAGE plpython3u;

CALL python_triple(5, 10);
```

### 44.2.5. Funções de retorno de configuração [#](#PLPYTHON-DATA-SET-RETURNING-FUNCS)

Uma função PL/Python também pode retornar conjuntos de tipos escalares ou compostos. Há várias maneiras de alcançar isso, pois o objeto retornado é convertido internamente em um iterador. Os exemplos a seguir assumem que temos um tipo composto:

```
CREATE TYPE greeting AS ( how text, who text );
```

Um resultado definido pode ser retornado a partir de:

Tipo de sequência (tupla, lista, conjunto)
```
    CREATE FUNCTION greet (how text)
      RETURNS SETOF greeting
    AS $$
      # return tuple containing lists as composite types
      # all other combinations work also
      return ( [ how, "World" ], [ how, "PostgreSQL" ], [ how, "PL/Python" ] )
    $$ LANGUAGE plpython3u;
    ```

Iterador (qualquer objeto que forneça os métodos `__iter__` e `__next__`): ``` CREATE FUNCTION greet (how text) RETURNS SETOF greeting AS $$ class producer: def __init__ (self, how, who): self.how = how self.who = who self.ndx = -1

def __iter__ (self): return self

def __next__(self): self.ndx += 1 if self.ndx == len(self.who): raise StopIteration return ( self.how, self.who[self.ndx] )

return producer(how, [ "World", "PostgreSQL", "PL/Python" ]) $$ LANGUAGE plpython3u;
    ```

Gerador (`yield`)
:   ```
    CREATE FUNCTION greet (how text)
      RETURNS SETOF greeting
    AS $$
      for who in [ "World", "PostgreSQL", "PL/Python" ]:
        yield ( how, who )
    $$ LANGUAGE plpython3u;
    ```

Também são suportadas funções de retorno de conjunto com parâmetros `OUT` (usando `RETURNS SETOF record`). Por exemplo:

```
CREATE FUNCTION multiout_simple_setof(n integer, OUT integer, OUT integer) RETURNS SETOF record AS $$
return [(1, 2)] * n
$$ LANGUAGE plpython3u;

SELECT * FROM multiout_simple_setof(3);
```
