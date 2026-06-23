## FIM

FINALIZAR — comprometer a transação atual

## Sinopse

```
END [ WORK | TRANSACTION ] [ AND [ NO ] CHAIN ]
```

## Descrição

`END` executa a transação atual. Todas as alterações feitas pela transação tornam-se visíveis para outros e são garantidas como duráveis, caso ocorra um crash. Este comando é uma extensão do PostgreSQL que é equivalente a `COMMIT`(sql-commit.md "COMMIT").

## Parâmetros

`WORK` `TRANSACTION`: Palavras-chave opcionais. Elas não têm efeito.

`AND CHAIN`: Se `AND CHAIN` for especificado, uma nova transação é iniciada imediatamente com as mesmas características da transação que acabou de ser concluída (ver [SET TRANSACTION](sql-set-transaction.md "SET TRANSACTION")). Caso contrário, não é iniciada nenhuma nova transação.

## Notas

Use `ROLLBACK`(sql-rollback.md "ROLLBACK") para abortar uma transação.

Emitir `END` quando não estiver dentro de uma transação não causa nenhum dano, mas provocará uma mensagem de alerta.

## Exemplos

Para comprometê-se com a transação atual e tornar todas as alterações permanentes:

```
END;
```

## Compatibilidade

`END` é uma extensão do PostgreSQL que oferece funcionalidades equivalentes a `COMMIT` (sql-commit.md "COMMIT"), conforme especificado no padrão SQL.

## Veja também

[INÍCIO](sql-begin.md "BEGIN"), [COMITAMENTO](sql-commit.md "COMMIT"), [RETRAÇÃO](sql-rollback.md "ROLLBACK")