## COMPROMISSO PREPARADO

COMMIT PREPARADO — realizar uma transação que foi preparada anteriormente para um compromisso em duas fases

## Sinopse

```
COMMIT PREPARED transaction_id
```

## Descrição

`COMMIT PREPARED` realiza uma transação que está em estado preparado.

## Parâmetros

*`transaction_id`*: O identificador de transação da transação que deve ser comprometida.

## Notas

Para realizar uma transação preparada, você deve ser o mesmo usuário que executou a transação originalmente, ou um superusuário. Mas você não precisa estar na mesma sessão que executou a transação.

Este comando não pode ser executado dentro de um bloco de transação. A transação preparada é comprometida imediatamente.

Todas as transações preparadas disponíveis atualmente estão listadas na visualização do sistema `pg_prepared_xacts`(view-pg-prepared-xacts.md "53.17. pg_prepared_xacts").

## Exemplos

Realize a transação identificada pelo identificador de transação `foobar`:

```
COMMIT PREPARED 'foobar';
```

## Compatibilidade

`COMMIT PREPARED` é uma extensão do PostgreSQL. É destinado ao uso por sistemas de gerenciamento de transações externas, alguns dos quais estão cobertos por padrões (como X/Open XA), mas o lado SQL desses sistemas não está padronizado.

## Veja também

[PREPARE TRANSACÃO](sql-prepare-transaction.md "PREPARE TRANSACTION"), [REVERSÃO DA PREPARAÇÃO](sql-rollback-prepared.md "ROLLBACK PREPARED")