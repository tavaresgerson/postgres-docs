## DROP TABLESPACE

DROP TABLESPACE — remova um tablespace

## Sinopse

```
DROP TABLESPACE [ IF EXISTS ] name
```

## Descrição

`DROP TABLESPACE` remove um espaço de tabela do sistema.

Um espaço de tabelas só pode ser descartado pelo seu proprietário ou por um superusuário. O espaço de tabelas deve estar vazio de todos os objetos do banco de dados antes de poder ser descartado. É possível que objetos em outros bancos de dados ainda residam no espaço de tabelas, mesmo que nenhum objeto no banco de dados atual esteja usando o espaço de tabelas. Além disso, se o espaço de tabelas estiver listado na configuração [temp_tablespaces][(runtime-config-client.md#GUC-TEMP-TABLESPACES)] de qualquer sessão ativa, o `DROP` pode falhar devido a arquivos temporários que residem no espaço de tabelas.

## Parâmetros

`IF EXISTS`: Não exija erro se o tablespace não existir. Um aviso é emitido neste caso.

*`name`*: O nome de um espaço de tabela.

## Notas

`DROP TABLESPACE` não pode ser executado dentro de um bloco de transação.

## Exemplos

Para remover o tablespace `mystuff` do sistema:

```
DROP TABLESPACE mystuff;
```

## Compatibilidade

`DROP TABLESPACE` é uma extensão do PostgreSQL.

## Veja também

[CREATE TABLESPACE](sql-createtablespace.md "CREATE TABLESPACE"), [ALTER TABLESPACE](sql-altertablespace.md "ALTER TABLESPACE")