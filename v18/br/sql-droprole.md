## DROP ROLE

DROP ROLE — remover um papel de banco de dados

## Sinopse

```
DROP ROLE [ IF EXISTS ] name [, ...]
```

## Descrição

`DROP ROLE` remove o(s) papel(es) especificado(s). Para descartar um papel de superusuário, você deve ser um superusuário; para descartar papéis que não são de superusuário, você deve ter o privilégio `CREATEROLE` e ter sido concedido `ADMIN OPTION` no papel.

Um papel não pode ser removido se ainda estiver sendo referenciado em qualquer banco de dados do clúster; um erro será exibido se isso ocorrer. Antes de descartar o papel, você deve descartar todos os objetos que ele possui (ou reatribuir sua propriedade) e revogar quaisquer privilégios que o papel tenha sido concedido em outros objetos. Os comandos `REASSIGN OWNED` e (sql-reassign-owned.md "REASSIGN OWNED") e `DROP OWNED` e (sql-drop-owned.md "DROP OWNED") podem ser úteis para esse propósito; consulte [Seção 21.4] para mais discussão.

No entanto, não é necessário remover as associações de papéis que envolvem o papel; `DROP ROLE` revoga automaticamente quaisquer associações do papel alvo em outros papéis e de outros papéis no papel alvo. Os outros papéis não são eliminados nem afetados de outra forma.

## Parâmetros

`IF EXISTS`: Não exija erro se o papel não existir. Um aviso é emitido neste caso.

*`name`*: O nome do papel a ser removido.

## Notas

O PostgreSQL inclui um programa [dropuser](app-dropuser.md) que tem a mesma funcionalidade que este comando (de fato, ele chama este comando) mas pode ser executado a partir do shell de comando.

## Exemplos

Para abandonar um papel:

```
DROP ROLE jonathan;
```

## Compatibilidade

O padrão SQL define `DROP ROLE`, mas permite que apenas um papel seja excluído de cada vez e especifica requisitos de privilégio diferentes dos usados pelo PostgreSQL.

## Veja também

[Crie um papel](sql-createrole.md "CREATE ROLE"), [Alterar papel](sql-alterrole.md "ALTER ROLE"), [Definir papel](sql-set-role.md "SET ROLE")