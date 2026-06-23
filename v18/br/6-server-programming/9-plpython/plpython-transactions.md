## 44.8. Gerenciamento de Transações [#](#PLPYTHON-TRANSACTIONS)

Em um procedimento chamado a partir do nível superior ou em um bloco de código anônimo (comando `DO`) chamado a partir do nível superior, é possível controlar as transações. Para confirmar a transação atual, chame `plpy.commit()`. Para reverter a transação atual, chame `plpy.rollback()`. (Observe que não é possível executar os comandos SQL `COMMIT` ou `ROLLBACK` via `plpy.execute` ou semelhante. Isso deve ser feito usando essas funções.) Após uma transação ser encerrada, uma nova transação é iniciada automaticamente, portanto, não há uma função separada para isso.

Aqui está um exemplo:

```
CREATE PROCEDURE transaction_test1()
LANGUAGE plpython3u
AS $$
for i in range(0, 10):
    plpy.execute("INSERT INTO test1 (a) VALUES (%d)" % i)
    if i % 2 == 0:
        plpy.commit()
    else:
        plpy.rollback()
$$;

CALL transaction_test1();
```

As transações não podem ser encerradas quando uma subtransação explícita estiver ativa.