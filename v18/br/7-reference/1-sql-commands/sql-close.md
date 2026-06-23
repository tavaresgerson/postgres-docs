## FECHAR

FECHAR — fechar um cursor

## Sinopse

```
CLOSE { name | ALL }
```

## Descrição

`CLOSE` libera os recursos associados a um cursor aberto. Após o cursor ser fechado, não são permitidas operações subsequentes nele. Um cursor deve ser fechado quando não for mais necessário.

Todo cursor aberto não mantido implicitamente é fechado quando uma transação é terminada por `COMMIT` ou `ROLLBACK`. Um cursor mantido implicitamente é fechado se a transação que o criou abortar via `ROLLBACK`. Se a transação que a criou for concluída com sucesso, o cursor mantido permanece aberto até que um `CLOSE` explícito seja executado, ou o cliente se desconecte.

## Parâmetros

*`name`*: O nome de um cursor aberto a ser fechado.

`ALL`: Feche todos os cursors abertos.

## Notas

O PostgreSQL não tem uma declaração explícita de cursor `OPEN`; um cursor é considerado aberto quando é declarado. Use a declaração `DECLARE`(sql-declare.md "DECLARE") para declarar um cursor.

Você pode ver todos os cursors disponíveis consultando a visão do sistema `pg_cursors`(view-pg-cursors.md "53.7. pg_cursors").

Se um cursor for fechado após um ponto de salvamento que é posteriormente desfeito, o `CLOSE` não é desfeito; ou seja, o cursor permanece fechado.

## Exemplos

Feche o cursor `liahona`:

```
CLOSE liahona;
```

## Compatibilidade

`CLOSE` está totalmente em conformidade com o padrão SQL. `CLOSE ALL` é uma extensão do PostgreSQL.

## Veja também

[DECLARE](sql-declare.md "DECLARE"), [FETCH](sql-fetch.md "FETCH"), [MOVE](sql-move.md "MOVE")