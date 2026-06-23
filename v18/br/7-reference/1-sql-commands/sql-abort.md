## ABORTAR

ABORT — interrompa a transação atual

## Sinopse

```
ABORT [ WORK | TRANSACTION ] [ AND [ NO ] CHAIN ]
```

## Descrição

`ABORT` desfaz a transação atual e faz com que todas as atualizações feitas pela transação sejam descartadas. Este comando é idêntico em comportamento ao comando SQL padrão `ROLLBACK`(sql-rollback.md "ROLLBACK"), e está presente apenas por razões históricas.

## Parâmetros

`WORK` `TRANSACTION`: Palavras-chave opcionais. Elas não têm efeito.

`AND CHAIN`: Se `AND CHAIN` for especificado, uma nova transação é iniciada imediatamente com as mesmas características da transação que acabou de ser concluída (ver [`SET TRANSACTION`](sql-set-transaction.md "SET TRANSACTION")) . Caso contrário, não é iniciada nenhuma nova transação.

## Notas

Use `COMMIT`(sql-commit.md "COMMIT") para encerrar com sucesso uma transação.

A emissão de `ABORT` fora de um bloco de transação emite um aviso e, de outra forma, não tem efeito.

## Exemplos

Para abortar todas as alterações:

```
ABORT;
```

## Compatibilidade

Este comando é uma extensão do PostgreSQL presente por razões históricas. `ROLLBACK` é o comando SQL padrão equivalente.

## Veja também

[INÍCIO](sql-begin.md "BEGIN"), [COMITAMENTO](sql-commit.md "COMMIT"), [RETRATO](sql-rollback.md "ROLLBACK")