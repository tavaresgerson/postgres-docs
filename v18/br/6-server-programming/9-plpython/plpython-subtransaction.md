## 44.7. Subtransações explícitas [#](#PLPYTHON-SUBTRANSACTION)

* [44.7.1. Geradores de contexto de subtransação](plpython-subtransaction.md#PLPYTHON-SUBTRANSACTION-CONTEXT-MANAGERS)

Recuperar erros causados pelo acesso ao banco de dados, conforme descrito em [Seção 44.6.2](plpython-database.md#PLPYTHON-TRAPPING) pode levar a uma situação indesejável em que algumas operações têm sucesso antes de uma delas falhar, e, após a recuperação desse erro, os dados permanecem em um estado inconsistente. O PL/Python oferece uma solução para esse problema na forma de subtransações explícitas.

### 44.7.1. Geradores de contexto de subtransação [#](#PLPYTHON-SUBTRANSACTION-CONTEXT-MANAGERS)

Considere uma função que implemente uma transferência entre duas contas:

```
CREATE FUNCTION transfer_funds() RETURNS void AS $$
try:
    plpy.execute("UPDATE accounts SET balance = balance - 100 WHERE account_name = 'joe'")
    plpy.execute("UPDATE accounts SET balance = balance + 100 WHERE account_name = 'mary'")
except plpy.SPIError as e:
    result = "error transferring funds: %s" % e.args
else:
    result = "funds transferred correctly"
plan = plpy.prepare("INSERT INTO operations (result) VALUES ($1)", ["text"])
plpy.execute(plan, [result])
$$ LANGUAGE plpython3u;
```

Se a segunda declaração `UPDATE` resultar em uma exceção ser levantada, esta função informará o erro, mas o resultado da primeira declaração `UPDATE` será, no entanto, comprometido. Em outras palavras, os fundos serão retirados da conta de Joe, mas não serão transferidos para a conta de Mary.

Para evitar tais problemas, você pode envolver suas chamadas de `plpy.execute` em uma subtransação explícita. O módulo `plpy` fornece um objeto auxiliar para gerenciar subtransações explícitas que são criadas com a função `plpy.subtransaction()`. Os objetos criados por essa função implementam a interface de gerenciador de contexto [context manager interface](https://docs.python.org/library/stdtypes.html#context-manager-types)]. Usando subtransações explícitas, podemos reescrever nossa função como:

```
CREATE FUNCTION transfer_funds2() RETURNS void AS $$
try:
    with plpy.subtransaction():
        plpy.execute("UPDATE accounts SET balance = balance - 100 WHERE account_name = 'joe'")
        plpy.execute("UPDATE accounts SET balance = balance + 100 WHERE account_name = 'mary'")
except plpy.SPIError as e:
    result = "error transferring funds: %s" % e.args
else:
    result = "funds transferred correctly"
plan = plpy.prepare("INSERT INTO operations (result) VALUES ($1)", ["text"])
plpy.execute(plan, [result])
$$ LANGUAGE plpython3u;
```

Observe que o uso de `try`/`except` ainda é necessário. Caso contrário, a exceção se propagaria até o topo da pilha do Python e causaria o abandono de toda a função com um erro do PostgreSQL, de modo que a tabela `operations` não teria nenhuma linha inserida nela. O gerenciador de contexto de subtransação não arrinca erros, apenas assegura que todas as operações de banco de dados executadas dentro de seu escopo sejam comprometidas ou revertidas atomicamente. Um retorno do bloco de subtransação ocorre em qualquer tipo de saída de exceção, não apenas aquelas causadas por erros originados do acesso ao banco de dados. Uma exceção regular de Python lançada dentro de um bloco de subtransação explícito também causaria o retorno da subtransação.