## DROP DATABASE

DROP DATABASE — remover um banco de dados

## Sinopse

```
DROP DATABASE [ IF EXISTS ] name [ [ WITH ] ( option [, ...] ) ]

where option can be:

    FORCE
```

## Descrição

`DROP DATABASE` descarrega um banco de dados. Ele remove as entradas do catálogo do banco de dados e exclui o diretório que contém os dados. Ele só pode ser executado pelo proprietário do banco de dados. Não pode ser executado enquanto você está conectado ao banco de dados de destino. (Conecte-se a `postgres` ou qualquer outro banco de dados para emitir este comando.) Além disso, se alguém estiver conectado ao banco de dados de destino, este comando falhará, a menos que você use a opção `FORCE` descrita abaixo.

`DROP DATABASE` não pode ser desfeito. Use com cuidado!

## Parâmetros

`IF EXISTS`: Não exija erro se o banco de dados não existir. Um aviso é emitido neste caso.

*`name`*: O nome do banco de dados a ser removido.

`FORCE`: Tente encerrar todas as conexões existentes no banco de dados-alvo. Não é possível encerrar se houver transações preparadas, slots de replicação lógica ativa ou assinaturas presentes no banco de dados-alvo.

Isso interrompe as conexões dos trabalhadores de segundo plano e as conexões que o usuário atual tem permissão para interromper com `pg_terminate_backend`, descrito em [Seção 9.28.2](functions-admin.md#FUNCTIONS-ADMIN-SIGNAL). Se as conexões permanecerem, este comando falhará.

## Notas

`DROP DATABASE` não pode ser executado dentro de um bloco de transação.

Este comando não pode ser executado enquanto estiver conectado ao banco de dados de destino. Assim, pode ser mais conveniente usar o programa [dropdb](app-dropdb.md) em vez disso, que é um wrapper em torno deste comando.

## Compatibilidade

Não há nenhuma declaração `DROP DATABASE` no padrão SQL.

## Veja também

[Crie banco de dados](sql-createdatabase.md "CREATE DATABASE")