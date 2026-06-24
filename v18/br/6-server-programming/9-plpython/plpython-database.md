## 44.6. Acesso ao banco de dados [#](#PLPYTHON-DATABASE)

* [44.6.1. Funções de Acesso a Banco de Dados](plpython-database.md#PLPYTHON-DATABASE-ACCESS-FUNCS)
* [44.6.2. Captura de Erros](plpython-database.md#PLPYTHON-TRAPPING)

O módulo de linguagem PL/Python importa automaticamente um módulo Python chamado `plpy`. As funções e constantes neste módulo estão disponíveis para você no código Python como `plpy.foo`.

### 44.6.1. Funções de Acesso ao Banco de Dados [#](#PLPYTHON-DATABASE-ACCESS-FUNCS)

O módulo `plpy` oferece várias funções para executar comandos de banco de dados:

`plpy.execute(query [, limit])`: Chamar `plpy.execute` com uma string de consulta e um argumento opcional de limite de linha faz com que a consulta seja executada e o resultado seja retornado em um objeto de resultado.

Se *`limit`* for especificado e for maior que zero, então `plpy.execute` recupera no máximo *`limit`* linhas, assim como se a consulta incluísse uma cláusula `LIMIT`. O omitindo *`limit`* ou especificando-o como zero resulta em nenhum limite de linha.

O objeto resultado emula um objeto de lista ou dicionário. O objeto resultado pode ser acessado pelo número da linha e pelo nome da coluna. Por exemplo:

```
rv = plpy.execute("SELECT * FROM my_table", 5)
```

retorna até 5 linhas de `my_table`. Se `my_table` tiver uma coluna `my_column`, ela seria acessada da seguinte forma:

```
foo = rv[i]["my_column"]
```

O número de linhas retornadas pode ser obtido usando a função embutida `len`.

O objeto de resultado tem esses métodos adicionais:

`nrows()` : Retorna o número de linhas processadas pelo comando. Note que isso não é necessariamente o mesmo número de linhas retornadas. Por exemplo, um comando `UPDATE` definirá esse valor, mas não retornará nenhuma linha (a menos que `RETURNING` seja usado).

`status()` :   O valor de retorno do `SPI_execute()`.

`colnames()` `coltypes()` `coltypmods()` :   Retorne uma lista de nomes de colunas, uma lista de tipos de OIDs de colunas e uma lista de modificadores de tipo específicos para o tipo de colunas, respectivamente.

Esses métodos geram uma exceção quando chamados em um objeto de resultado de um comando que não produziu um conjunto de resultados, por exemplo, `UPDATE` sem `RETURNING`, ou `DROP TABLE`. Mas é permitido usar esses métodos em um conjunto de resultados contendo zero linhas.

`__str__()` :   O método padrão `__str__` é definido de forma que seja possível, por exemplo, depurar os resultados da execução de consultas usando `plpy.debug(rv)`.

O objeto de resultado pode ser modificado.

Observe que chamar `plpy.execute` fará com que todo o conjunto de resultados seja lido na memória. Use essa função apenas quando tiver certeza de que o conjunto de resultados será relativamente pequeno. Se você não quiser arriscar o uso excessivo de memória ao buscar resultados grandes, use `plpy.cursor` em vez de `plpy.execute`.

`plpy.prepare(query [, argtypes])` `plpy.execute(plan [, arguments [, limit]])`: `plpy.prepare` prepara o plano de execução para uma consulta. É chamado com uma string de consulta e uma lista de tipos de parâmetros, se você tiver referências de parâmetros na consulta. Por exemplo:

```
plan = plpy.prepare("SELECT last_name FROM my_users WHERE first_name = $1", ["text"])
```

`text` é o tipo da variável que você vai passar para `$1`. O segundo argumento é opcional se você não quiser passar nenhum parâmetro para a consulta.

Depois de preparar uma declaração, você usa uma variante da função `plpy.execute` para executá-la:

```
rv = plpy.execute(plan, ["name"], 5)
```

Passe o plano como o primeiro argumento (em vez da string de consulta), e uma lista de valores para substituir na consulta como o segundo argumento. O segundo argumento é opcional se a consulta não esperar nenhum parâmetro. O terceiro argumento é o limite de linha opcional como antes.

Como alternativa, você pode chamar o método `execute` no objeto de plano:

```
rv = plan.execute(["name"], 5)
```

Os parâmetros de consulta e os campos das linhas de resultado são convertidos entre os tipos de dados do PostgreSQL e Python conforme descrito em [Seção 44.2](plpython-data.md).

Quando você prepara um plano usando o módulo PL/Python, ele é automaticamente salvo. Leia a documentação do SPI ([Capítulo 45](spi.md)) para uma descrição do que isso significa. Para fazer uso eficaz disso em chamadas de função, é necessário usar um dos dicionários de armazenamento persistente `SD` ou `GD` (consulte [Seção 44.3](plpython-sharing.md)). Por exemplo:

```
CREATE FUNCTION usesavedplan() RETURNS trigger AS $$ if "plan" in SD: plan = SD["plan"] else: plan = plpy.prepare("SELECT 1") SD["plan"] = plan
    # rest of function
$$ LANGUAGE plpython3u;
```

`plpy.cursor(query)` `plpy.cursor(plan [, arguments])`: A função `plpy.cursor` aceita os mesmos argumentos que `plpy.execute` (exceto pelo limite de linha) e retorna um objeto cursor, que permite processar grandes conjuntos de resultados em partes menores. Assim como em `plpy.execute`, pode-se usar uma string de consulta ou um objeto de plano, juntamente com uma lista de argumentos, ou a função `cursor` pode ser chamada como um método do objeto de plano.

O objeto cursor fornece um método `fetch` que aceita um parâmetro inteiro e retorna um objeto de resultado. Toda vez que você chama `fetch`, o objeto retornado conterá o próximo lote de linhas, nunca maior que o valor do parâmetro. Uma vez que todas as linhas são esgotadas, `fetch` começa a retornar um objeto de resultado vazio. Os objetos cursor também fornecem uma [interface de iterador](https://docs.python.org/library/stdtypes.html#iterator-types), produzindo uma linha de cada vez até que todas as linhas sejam esgotadas. Os dados obtidos dessa maneira não são retornados como objetos de resultado, mas sim como dicionários, cada dicionário correspondendo a uma única linha de resultado.

Um exemplo de duas maneiras de processar dados de uma tabela grande é:

```
CREATE FUNCTION count_odd_iterator() RETURNS integer AS $$ odd = 0 for row in plpy.cursor("select num from largetable"): if row['num'] % 2: odd += 1 return odd $$ LANGUAGE plpython3u;

CREATE FUNCTION count_odd_fetch(batch_size integer) RETURNS integer AS $$ odd = 0 cursor = plpy.cursor("select num from largetable") while True: rows = cursor.fetch(batch_size) if not rows: break for row in rows: if row['num'] % 2: odd += 1 return odd $$ LANGUAGE plpython3u;

CREATE FUNCTION count_odd_prepared() RETURNS integer AS $$ odd = 0 plan = plpy.prepare("select num from largetable where num % $1 <> 0", ["integer"]) rows = list(plpy.cursor(plan, [2]))  # or: = list(plan.cursor([2]))

return len(rows) $$ LANGUAGE plpython3u;
```

Os ponteiros são automaticamente descartados. Mas se você quiser liberar explicitamente todos os recursos mantidos por um ponteiro, use o método `close`. Uma vez fechado, um ponteiro não pode ser recuperado mais.

DICA

Não confunda objetos criados por `plpy.cursor` com cursor da DB-API conforme definido pela especificação da [API de banco de dados do Python](https://www.python.org/dev/peps/pep-0249/). Eles não têm nada em comum, exceto pelo nome.

### 44.6.2. Erros de captura [#](#PLPYTHON-TRAPPING)

As funções que acessam o banco de dados podem encontrar erros, o que as fará abortar e gerar uma exceção. Tanto `plpy.execute` quanto `plpy.prepare` podem gerar uma instância de uma subclasse de `plpy.SPIError`, que, por padrão, terminará a função. Esse erro pode ser tratado da mesma forma que qualquer outra exceção do Python, usando o `try/except` construção. Por exemplo:

```
CREATE FUNCTION try_adding_joe() RETURNS text AS $$ try: plpy.execute("INSERT INTO users(username) VALUES ('joe')") except plpy.SPIError: return "something went wrong" else: return "Joe added" $$ LANGUAGE plpython3u;
```

A classe real da exceção que está sendo levantada corresponde à condição específica que causou o erro. Consulte [Tabela A.1] para obter uma lista de condições possíveis. O módulo (errcodes-appendix.md#ERRCODES-TABLE "Table A.1. PostgreSQL Error Codes") define uma classe de exceção para cada condição do PostgreSQL, derivando seus nomes do nome da condição. Por exemplo, `division_by_zero` se torna `DivisionByZero`, `unique_violation` se torna `UniqueViolation`, `fdw_error` se torna `FdwError`, e assim por diante. Cada uma dessas classes de exceção herda de `SPIError`. Essa separação facilita o tratamento de erros específicos, por exemplo:

```
CREATE FUNCTION insert_fraction(numerator int, denominator int) RETURNS text AS $$ from plpy import spiexceptions try: plan = plpy.prepare("INSERT INTO fractions (frac) VALUES ($1 / $2)", ["int", "int"]) plpy.execute(plan, [numerator, denominator]) except spiexceptions.DivisionByZero: return "denominator cannot equal zero" except spiexceptions.UniqueViolation: return "already have that fraction" except plpy.SPIError as e: return "other error, SQLSTATE %s" % e.sqlstate else: return "fraction inserted" $$ LANGUAGE plpython3u;
```

Observe que, como todas as exceções do módulo `plpy.spiexceptions` herdam de `SPIError`, uma cláusula de tratamento de `except` que a abranja irá capturar qualquer erro de acesso ao banco de dados.

Como uma alternativa para lidar com diferentes condições de erro, você pode capturar a exceção `SPIError` e determinar a condição de erro específica dentro do bloco `except` olhando para o atributo `sqlstate` do objeto da exceção. Esse atributo é um valor de string que contém o código de erro "SQLSTATE". Essa abordagem oferece aproximadamente a mesma funcionalidade