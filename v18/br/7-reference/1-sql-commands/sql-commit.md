## COMPROMETIDO

COMMIT — commit a transação atual

## Sinopse

```
COMMIT [ WORK | TRANSACTION ] [ AND [ NO ] CHAIN ]
```

## Descrição

`COMMIT` executa a transação atual. Todas as alterações feitas pela transação tornam-se visíveis para outros e são garantidas como duráveis, caso ocorra um crash.

## Parâmetros

`WORK` `TRANSACTION` [#](#SQL-COMMIT-TRANSACTION): Palavras-chave opcionais. Elas não têm efeito.

`AND CHAIN` [#](#SQL-COMMIT-CHAIN): Se `AND CHAIN` for especificado, uma nova transação é iniciada imediatamente com as mesmas características da transação que acabou de ser concluída (ver [SET TRANSACTION](sql-set-transaction.md "SET TRANSACTION")) . Caso contrário, não é iniciada nenhuma nova transação.

## Notas

Use [ROLLBACK][(sql-rollback.md "ROLLBACK") para abortar uma transação.

Emitir `COMMIT` quando não estiver dentro de uma transação não causa nenhum dano, mas provocará uma mensagem de alerta. `COMMIT AND CHAIN` quando não estiver dentro de uma transação é um erro.

## Exemplos

Para comprometê-se com a transação atual e tornar todas as alterações permanentes:

```
COMMIT;
```

## Compatibilidade

O comando `COMMIT` está de acordo com o padrão SQL. O formulário `COMMIT TRANSACTION` é uma extensão do PostgreSQL.

## Veja também

[INÍCIO](sql-begin.md "BEGIN"), [REVERSÃO](sql-rollback.md "ROLLBACK")