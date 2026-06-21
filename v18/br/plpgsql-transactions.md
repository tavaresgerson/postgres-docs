## 41.8. Gerenciamento de Transações [#](#PLPGSQL-TRANSACTIONS)

Nos procedimentos invocados pelo comando `CALL`, bem como nos blocos de código anônimos (comando `DO`, é possível encerrar transações usando os comandos `COMMIT` e `ROLLBACK`. Uma nova transação é iniciada automaticamente após a conclusão de uma transação usando esses comandos, portanto, não há um comando separado `START TRANSACTION`. (Observe que `BEGIN` e `END` têm significados diferentes em PL/pgSQL.)

Aqui está um exemplo simples:

```
CREATE PROCEDURE transaction_test1()
LANGUAGE plpgsql
AS $$
BEGIN
    FOR i IN 0..9 LOOP
        INSERT INTO test1 (a) VALUES (i);
        IF i % 2 = 0 THEN
            COMMIT;
        ELSE
            ROLLBACK;
        END IF;
    END LOOP;
END;
$$;

CALL transaction_test1();
```

Uma nova transação começa com características de transação padrão, como o nível de isolamento de transação. Nos casos em que as transações são comprometidas em um loop, pode ser desejável iniciar novas transações automaticamente com as mesmas características da anterior. Os comandos `COMMIT AND CHAIN` e `ROLLBACK AND CHAIN` realizam isso.

O controle de transação só é possível em invocações de `CALL` ou `DO` a partir do nível superior ou invocações aninhadas de `CALL` ou `DO` sem qualquer outro comando intermediário. Por exemplo, se o pilha de chamadas for `CALL proc1()` → `CALL proc2()` → `CALL proc3()`, então os segundo e terceiro procedimentos podem realizar ações de controle de transação. Mas se o pilha de chamadas for `CALL proc1()` → `SELECT func2()` → `CALL proc3()`, então o último procedimento não pode fazer controle de transação, devido ao `SELECT` entre eles.

O PL/pgSQL não suporta comandos de savepoints (os comandos `SAVEPOINT`/`ROLLBACK TO SAVEPOINT`/`RELEASE SAVEPOINT`). Padrões típicos de uso para savepoints podem ser substituídos por blocos com manipuladores de exceções (consulte [Seção 41.6.8][(plpgsql-control-structures.md#PLPGSQL-ERROR-TRAPPING "41.6.8. Trapping Errors")]). Sob o capô, um bloco com manipuladores de exceções forma uma subtransação, o que significa que as transações não podem ser encerradas dentro de tal bloco.

Considerações especiais se aplicam aos loops do cursor. Considere este exemplo:

```
CREATE PROCEDURE transaction_test2()
LANGUAGE plpgsql
AS $$
DECLARE
    r RECORD;
BEGIN
    FOR r IN SELECT * FROM test2 ORDER BY x LOOP
        INSERT INTO test1 (a) VALUES (r.x);
        COMMIT;
    END LOOP;
END;
$$;

CALL transaction_test2();
```

Normalmente, os cursors são fechados automaticamente ao confirmar a transação. No entanto, um cursor criado como parte de um loop como este é automaticamente convertido em um cursor que pode ser mantido pelo primeiro `COMMIT` ou `ROLLBACK`. Isso significa que o cursor é totalmente avaliado no primeiro `COMMIT` ou `ROLLBACK`, em vez de linha por linha. O cursor ainda é removido automaticamente após o loop, portanto, isso é praticamente invisível para o usuário. Mas é importante lembrar que quaisquer bloqueios de tabela ou linha tomados pela consulta do cursor não serão mais mantidos após o primeiro `COMMIT` ou `ROLLBACK`.

Os comandos de transação não são permitidos em loops de cursor movidos por comandos que não são de leitura somente (por exemplo, `UPDATE ... RETURNING`).