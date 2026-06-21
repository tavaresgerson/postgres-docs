## REASSINAR DE ACESSO AO DETENTO

REASSIGN OWNED — altere a propriedade dos objetos de banco de dados detidos por um papel de banco de dados

## Sinopse

```
REASSIGN OWNED BY { old_role | CURRENT_ROLE | CURRENT_USER | SESSION_USER } [, ...]
               TO { new_role | CURRENT_ROLE | CURRENT_USER | SESSION_USER }
```

## Descrição

`REASSIGN OWNED` instrui o sistema a alterar a propriedade dos objetos de banco de dados detidos por qualquer um dos *`old_roles`* para *`new_role`*.

## Parâmetros

*`old_role`*: O nome de um papel. A propriedade de todos os objetos dentro do banco de dados atual, e de todos os objetos compartilhados (bancos de dados, espaços de tabelas), possuídos por este papel, serão reatribuídos a *`new_role`*.

*`new_role`*: O nome do papel que será feito o novo proprietário dos objetos afetados.

## Notas

`REASSIGN OWNED` é frequentemente usado para preparar a remoção de um ou mais papéis. Como `REASSIGN OWNED` não afeta objetos dentro de outros bancos de dados, geralmente é necessário executar este comando em cada banco de dados que contém objetos de propriedade de um papel que será removido.

`REASSIGN OWNED` exige a adesão tanto no(s) papel(es) de origem quanto no papel de destino.

O comando `DROP OWNED`](sql-drop-owned.md "DROP OWNED") é uma alternativa que simplesmente elimina todos os objetos do banco de dados detidos por um ou mais papéis.

O comando `REASSIGN OWNED` não afeta quaisquer privilégios concedidos ao *`old_roles`* em objetos que não sejam de sua propriedade. Da mesma forma, ele não afeta os privilégios padrão criados com `ALTER DEFAULT PRIVILEGES`. Use `DROP OWNED` para revogar tais privilégios.

Veja [Seção 21.4][(role-removal.md "21.4. Dropping Roles")] para mais discussão.

## Compatibilidade

O comando `REASSIGN OWNED` é uma extensão do PostgreSQL.

## Veja também

[DROP OWNED](sql-drop-owned.md "DROP OWNED"), [DROP ROLE](sql-droprole.md "DROP ROLE"), [ALTER DATABASE](sql-alterdatabase.md "ALTER DATABASE")