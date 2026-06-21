## 44.1. Funções PL/Python [#](#PLPYTHON-FUNCS)

As funções no PL/Python são declaradas através da sintaxe padrão [CREATE FUNCTION](sql-createfunction.md "CREATE FUNCTION"):

```
CREATE FUNCTION funcname (argument-list)
  RETURNS return-type
AS $$
  # PL/Python function body
$$ LANGUAGE plpython3u;
```

O corpo de uma função é simplesmente um script em Python. Quando a função é chamada, seus argumentos são passados como elementos da lista `args`; argumentos nomeados também são passados como variáveis comuns para o script em Python. O uso de argumentos nomeados geralmente é mais legível. O resultado é retornado do código em Python da maneira usual, com `return` ou `yield` (no caso de uma declaração de conjunto de resultados). Se você não fornecer um valor de retorno, o Python retorna o valor padrão `None`. O PL/Python traduz o `None` do Python no valor nulo do SQL. Em um procedimento, o resultado do código em Python deve ser `None` (tipicamente alcançado terminando o procedimento sem uma declaração de `return` ou usando uma declaração de `return` sem argumento); caso contrário, um erro será exibido.

Por exemplo, uma função para retornar o maior de dois inteiros pode ser definida da seguinte forma:

```
CREATE FUNCTION pymax (a integer, b integer)
  RETURNS integer
AS $$
  if a > b:
    return a
  return b
$$ LANGUAGE plpython3u;
```

O código Python que é fornecido como o corpo da definição da função é transformado em uma função Python. Por exemplo, o acima resulta em:

```
def __plpython_procedure_pymax_23456():
  if a > b:
    return a
  return b
```

assumindo que 23456 é o OID atribuído à função pelo PostgreSQL.

Os argumentos são definidos como variáveis globais. Devido às regras de escopo do Python, isso tem a consequência sutil de que uma variável de argumento não pode ser reatribuída dentro da função ao valor de uma expressão que envolve o próprio nome da variável, a menos que a variável seja redescrevida como global no bloco. Por exemplo, o seguinte não funcionará:

```
CREATE FUNCTION pystrip(x text)
  RETURNS text
AS $$
  x = x.strip()  # error
  return x
$$ LANGUAGE plpython3u;
```

porque atribuir a `x` torna `x` uma variável local para todo o bloco, e assim o `x` do lado direito da atribuição refere-se a uma variável local não atribuída `x`, e não ao parâmetro da função PL/Python. Usando a declaração `global`, isso pode ser feito para funcionar:

```
CREATE FUNCTION pystrip(x text)
  RETURNS text
AS $$
  global x
  x = x.strip()  # ok now
  return x
$$ LANGUAGE plpython3u;
```

Mas é aconselhável não confiar nesse detalhe de implementação do PL/Python. É melhor tratar os parâmetros da função como somente leitura.