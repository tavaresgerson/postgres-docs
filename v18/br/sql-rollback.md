## REVERTIMENTO

REVERT — interrompa a transação atual

## Sinopse

```
ROLLBACK [ WORK | TRANSACTION ] [ AND [ NO ] CHAIN ]
```

## Descrição

`ROLLBACK` desfaz a transação atual e faz com que todas as atualizações feitas pela transação sejam descartadas.

## Parâmetros

`WORK` `TRANSACTION` [#](#SQL-ROLLBACK-TRANSACTION): Palavras-chave opcionais. Elas não têm efeito.

`AND CHAIN` [#](#SQL-ROLLBACK-CHAIN): Se `AND CHAIN` for especificado, uma nova (não interrompida) transação é iniciada imediatamente com as mesmas características da transação (ver [SET TRANSACTION](sql-set-transaction.md "SET TRANSACTION")) que foi concluída. Caso contrário, não é iniciada nenhuma nova transação.

## Notas

Use `COMMIT`(sql-commit.md "COMMIT") para encerrar com sucesso uma transação.

Emitir `ROLLBACK` fora de um bloco de transação emite um aviso e, de outra forma, não tem efeito. `ROLLBACK AND CHAIN` fora de um bloco de transação é um erro.

## Exemplos

Para abortar todas as alterações:

```
ROLLBACK;
```

## Compatibilidade

O comando `ROLLBACK` está de acordo com o padrão SQL. O formulário `ROLLBACK TRANSACTION` é uma extensão do PostgreSQL.

## Veja também

[INÍCIO](sql-begin.md "BEGIN"), [COMITAMENTO](sql-commit.md "COMMIT"), [REVERT PARA SAVEPOINT](sql-rollback-to.md "ROLLBACK TO SAVEPOINT")