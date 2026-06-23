## 42.10. Gestão de Transações [#](#PLTCL-TRANSACTIONS)

Em um procedimento chamado a partir do nível superior ou em um bloco de código anônimo (comando `DO`), chamado a partir do nível superior, é possível controlar as transações. Para confirmar a transação atual, chame o comando `commit`. Para reverter a transação atual, chame o comando `rollback`. (Observe que não é possível executar os comandos SQL `COMMIT` ou `ROLLBACK` via `spi_exec` ou semelhante. Isso deve ser feito usando essas funções.) Após uma transação ser concluída, uma nova transação é iniciada automaticamente, portanto, não há um comando separado para isso.

Aqui está um exemplo:

```
CREATE PROCEDURE transaction_test1()
LANGUAGE pltcl
AS $$
for {set i 0} {$i < 10} {incr i} {
    spi_exec "INSERT INTO test1 (a) VALUES ($i)"
    if {$i % 2 == 0} {
        commit
    } else {
        rollback
    }
}
$$;

CALL transaction_test1();
```

As transações não podem ser encerradas quando uma subtransação explícita estiver ativa.