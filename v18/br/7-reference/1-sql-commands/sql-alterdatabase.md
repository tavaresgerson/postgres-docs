## ALTER DATABASE

ALTER DATABASE — alterar um banco de dados

## Sinopse

```
ALTER DATABASE name [ [ WITH ] option [ ... ] ]

where option can be:

    ALLOW_CONNECTIONS allowconn
    CONNECTION LIMIT connlimit
    IS_TEMPLATE istemplate

ALTER DATABASE name RENAME TO new_name

ALTER DATABASE name OWNER TO { new_owner | CURRENT_ROLE | CURRENT_USER | SESSION_USER }

ALTER DATABASE name SET TABLESPACE new_tablespace

ALTER DATABASE name REFRESH COLLATION VERSION

ALTER DATABASE name SET configuration_parameter { TO | = } { value | DEFAULT }
ALTER DATABASE name SET configuration_parameter FROM CURRENT
ALTER DATABASE name RESET configuration_parameter
ALTER DATABASE name RESET ALL
```

## Descrição

`ALTER DATABASE` altera os atributos de um banco de dados.

O primeiro formulário altera certas configurações por banco de dados. (Veja abaixo para detalhes.) Apenas o proprietário do banco de dados ou um superusuário pode alterar essas configurações.

A segunda forma altera o nome do banco de dados. Apenas o proprietário do banco de dados ou um superusuário pode renomear um banco de dados; os proprietários que não são superusuários também devem ter o privilégio `CREATEDB`. O banco de dados atual não pode ser renomeado. (Conecte-se a um banco de dados diferente se precisar fazer isso.)

A terceira forma altera o proprietário do banco de dados. Para alterar o proprietário, você deve ser capaz de `SET ROLE` para o novo papel de proprietário e deve ter o privilégio `CREATEDB`. (Observe que os superusuários têm todos esses privilégios automaticamente.)

A quarta forma altera o espaço de tabela padrão do banco de dados. Apenas o proprietário do banco de dados ou um superusuário pode fazer isso; você também deve ter privilégio de criar para o novo espaço de tabela. Este comando move fisicamente quaisquer tabelas ou índices no espaço de tabela padrão antigo do banco de dados para o novo espaço de tabela. O novo espaço de tabela padrão deve estar vazio para este banco de dados, e ninguém pode estar conectado ao banco de dados. As tabelas e índices em espaços de tabela não padrão não são afetados. O método usado para copiar arquivos para o novo espaço de tabela é afetado pelo ajuste [file_copy_method](runtime-config-resource.md#GUC-FILE-COPY-METHOD).

Os formulários restantes alteram o valor padrão da sessão para uma variável de configuração de execução para um banco de dados PostgreSQL. Sempre que uma nova sessão é subsequentemente iniciada nesse banco de dados, o valor especificado torna-se o valor padrão da sessão. O valor padrão específico do banco de dados substitui qualquer configuração presente em `postgresql.conf` ou que tenha sido recebida a partir do comando `postgres`. Apenas o proprietário do banco de dados ou um superusuário pode alterar os valores padrão da sessão para um banco de dados. Algumas variáveis não podem ser definidas dessa maneira, ou só podem ser definidas por um superusuário.

## Parâmetros

*`name`*: O nome do banco de dados cujos atributos devem ser alterados.

*`allowconn`*: Se falso, ninguém pode se conectar a este banco de dados.

*`connlimit`*: Quantos conexões concorrentes podem ser feitas com este banco de dados. -1 significa sem limite.

*`istemplate`*: Se verdadeiro, então este banco de dados pode ser clonado por qualquer usuário com privilégios de `CREATEDB`; se falso, então apenas superusuários ou o proprietário do banco de dados podem cloná-lo.

*`new_name`*: O novo nome do banco de dados.

*`new_owner`*: O novo proprietário do banco de dados.

*`new_tablespace`*: O novo espaço de tabela padrão do banco de dados.

Essa forma do comando não pode ser executada dentro de um bloco de transação.

`REFRESH COLLATION VERSION`: Atualize a versão da collation do banco de dados. Consulte [Notas](sql-altercollation.md#SQL-ALTERCOLLATION-NOTES) para informações adicionais.

*`configuration_parameter`* *`value`*: Defina o valor padrão da sessão deste banco de dados para o parâmetro de configuração especificado no valor fornecido. Se *`value`* for `DEFAULT` ou, de forma equivalente, `RESET` for usado, o ajuste específico do banco de dados será removido, de modo que o ajuste padrão para todo o sistema será herdado em novas sessões. Use `RESET ALL` para limpar todos os ajustes específicos do banco de dados. `SET FROM CURRENT` salva o valor atual da sessão do parâmetro como o valor específico do banco de dados.

Veja [SET](sql-set.md "SET") e [Capítulo 19](runtime-config.md "Chapter 19. Server Configuration") para mais informações sobre os nomes e valores permitidos dos parâmetros.

## Notas

Também é possível vincular um padrão de sessão a um papel específico, em vez de a um banco de dados; veja [ALTER ROLE](sql-alterrole.md). As configurações específicas do papel substituem as específicas do banco de dados, se houver um conflito.

## Exemplos

Para desabilitar a varredura de índice por padrão no banco de dados `test`:

```
ALTER DATABASE test SET enable_indexscan TO off;
```

## Compatibilidade

A declaração `ALTER DATABASE` é uma extensão do PostgreSQL.

## Veja também

[CREATE DATABASE](sql-createdatabase.md "CREATE DATABASE"), [DROP DATABASE](sql-dropdatabase.md "DROP DATABASE"), [SET](sql-set.md "SET"), [CREATE TABLESPACE](sql-createtablespace.md "CREATE TABLESPACE")