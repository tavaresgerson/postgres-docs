## ALTER GROUP

ALTER GROUP — alterar o nome do papel ou a adesão

## Sinopse

```
ALTER GROUP role_specification ADD USER user_name [, ... ]
ALTER GROUP role_specification DROP USER user_name [, ... ]

where role_specification can be:

    role_name
  | CURRENT_ROLE
  | CURRENT_USER
  | SESSION_USER

ALTER GROUP group_name RENAME TO new_name
```

## Descrição

`ALTER GROUP` altera os atributos de um grupo de usuários. Este é um comando obsoleto, embora ainda aceito para compatibilidade reversa, porque os grupos (e os usuários também) foram substituídos pelo conceito mais geral de papéis.

As duas primeiras variantes adicionam usuários a um grupo ou os removem de um grupo. (Qualquer papel pode desempenhar o papel de “usuário” ou “grupo” para esse propósito.) Essas variantes são efetivamente equivalentes a conceder ou revogar a adesão ao papel denominado como “grupo”; portanto, a maneira preferida de fazer isso é usar `GRANT`(sql-grant.md "GRANT") ou `REVOKE`(sql-revoke.md "REVOKE"). Note que `GRANT` e `REVOKE` têm opções adicionais que não estão disponíveis com este comando, como a capacidade de conceder e revogar `ADMIN OPTION`, e a capacidade de especificar o concedente.

A terceira variante altera o nome do grupo. Isso é exatamente equivalente a renomear o papel com `ALTER ROLE` (sql-alterrole.md "ALTER ROLE").

## Parâmetros

*`group_name`*: O nome do grupo (papel) que você deseja modificar.

*`user_name`*: Usuários (atributos) que devem ser adicionados ao grupo ou removidos dele. Os usuários devem já existir; `ALTER GROUP` não cria ou remove usuários.

*`new_name`*: O novo nome do grupo.

## Exemplos

Adicione usuários a um grupo:

```
ALTER GROUP staff ADD USER karl, john;
```

Remover um usuário de um grupo:

```
ALTER GROUP workers DROP USER beth;
```

## Compatibilidade

Não há nenhuma declaração `ALTER GROUP` no padrão SQL.

## Veja também

[PRESTAÇÃO](sql-grant.md "GRANT"), [REVOGA](sql-revoke.md "REVOKE"), [ALTERAR ROLE](sql-alterrole.md "ALTER ROLE")