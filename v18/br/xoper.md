## 36.14. Operadores Definidos pelo Usuário [#](#XOPER)

Cada operador é um "açúcar sintático" para uma chamada a uma função subjacente que realiza o trabalho real; portanto, você deve criar primeiro a função subjacente antes de poder criar o operador. No entanto, um operador *não é apenas* açúcar sintático, porque ele carrega informações adicionais que ajudam o planejador de consultas a otimizar consultas que usam o operador. A próxima seção será dedicada a explicar essas informações adicionais.

O PostgreSQL suporta operadores prefixo e infixo. Os operadores podem ser sobrecarregados; ou seja, o mesmo nome de operador pode ser usado para diferentes operadores que têm diferentes números e tipos de operandos. Quando uma consulta é executada, o sistema determina o operador a ser chamado a partir do número e dos tipos dos operandos fornecidos.

Aqui está um exemplo de criação de um operador para adicionar dois números complexos. Suponhamos que já tenhamos criado a definição do tipo `complex` (consulte [Seção 36.13](xtypes.md)). Primeiro, precisamos de uma função que faça o trabalho, e depois podemos definir o operador:

```
CREATE FUNCTION complex_add(complex, complex)
    RETURNS complex
    AS 'filename', 'complex_add'
    LANGUAGE C IMMUTABLE STRICT;

CREATE OPERATOR + (
    leftarg = complex,
    rightarg = complex,
    function = complex_add,
    commutator = +
);
```

Agora, poderíamos executar uma consulta como esta:

```
SELECT (a + b) AS c FROM test_complex;

        c
-----------------
 (5.2,6.05)
 (133.42,144.95)
```

Mostramos como criar um operador binário aqui. Para criar um operador prefixo, basta omitir o `leftarg`. A cláusula `function` e as cláusulas de argumento são os únicos itens obrigatórios em `CREATE OPERATOR`. A cláusula `commutator` mostrada no exemplo é uma dica opcional para o otimizador de consulta. Mais detalhes sobre `commutator` e outras dicas do otimizador aparecem na próxima seção.