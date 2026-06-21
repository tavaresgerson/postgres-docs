## ALTER VIEW

ALTER VIEW — alterar a definição de uma visão

## Sinopse

```
ALTER VIEW [ IF EXISTS ] name ALTER [ COLUMN ] column_name SET DEFAULT expression
ALTER VIEW [ IF EXISTS ] name ALTER [ COLUMN ] column_name DROP DEFAULT
ALTER VIEW [ IF EXISTS ] name OWNER TO { new_owner | CURRENT_ROLE | CURRENT_USER | SESSION_USER }
ALTER VIEW [ IF EXISTS ] name RENAME [ COLUMN ] column_name TO new_column_name
ALTER VIEW [ IF EXISTS ] name RENAME TO new_name
ALTER VIEW [ IF EXISTS ] name SET SCHEMA new_schema
ALTER VIEW [ IF EXISTS ] name SET ( view_option_name [= view_option_value] [, ... ] )
ALTER VIEW [ IF EXISTS ] name RESET ( view_option_name [, ... ] )
```

## Descrição

`ALTER VIEW` altera várias propriedades auxiliares de uma visão. (Se você deseja modificar a consulta que define a visão, use `CREATE OR REPLACE VIEW`.

Você deve possuir a visão para usar `ALTER VIEW`. Para alterar o esquema de uma visão, você também deve ter privilégio `CREATE` no novo esquema. Para alterar o proprietário, você deve ser capaz de `SET ROLE` para o novo papel de proprietário, e esse papel deve ter privilégio `CREATE` no esquema da visão. (Essas restrições garantem que alterar o proprietário não faz nada que você não poderia fazer ao descartar e recriar a visão. No entanto, um superusuário pode alterar a propriedade de qualquer visão de qualquer maneira.)

## Parâmetros

*`name`*: O nome (opcionalmente qualificado por esquema) de uma visão existente.

*`column_name`*: Nome de uma coluna existente.

*`new_column_name`*: Novo nome para uma coluna existente.

`IF EXISTS`: Não exija erro se a visualização não existir. Um aviso é emitido neste caso.

`SET`/`DROP DEFAULT`: Esses formulários definem ou removem o valor padrão para uma coluna. O valor padrão de uma coluna de visualização é substituído em qualquer comando `INSERT` ou `UPDATE` cujo alvo é a visualização, antes de aplicar quaisquer regras ou gatilhos para a visualização. O padrão da visualização, portanto, terá precedência sobre quaisquer valores padrão de relações subjacentes.

*`new_owner`*: O nome do usuário do novo proprietário da visualização.

*`new_name`*: O novo nome para a visualização.

*`new_schema`*: O novo esquema para a visualização.

`SET ( view_option_name [= view_option_value] [, ... ] )` `RESET ( view_option_name [, ... ] )`: Define ou redefine uma opção de visualização. As opções atualmente suportadas são:

`check_option` (`enum`) :   Altera a opção de verificação da visualização. O valor deve ser `local` ou `cascaded`.

`security_barrier` (`boolean`) : Altera a propriedade de barreira de segurança da visualização. O valor deve ser um valor booleano, como `true` ou `false`.

`security_invoker` (`boolean`) :   Altera a propriedade de invocante de segurança da visualização. O valor deve ser um valor booleano, como `true` ou `false`.

## Notas

Por razões históricas, `ALTER TABLE` também pode ser usado com vistas; mas as únicas variantes de `ALTER TABLE` que são permitidas com vistas são equivalentes às mostradas acima.

## Exemplos

Para renomear a visual `foo` para `bar`:

```
ALTER VIEW foo RENAME TO bar;
```

Para associar um valor padrão de coluna a uma visualização atualizável:

```
CREATE TABLE base_table (id int, ts timestamptz);
CREATE VIEW a_view AS SELECT * FROM base_table;
ALTER VIEW a_view ALTER COLUMN ts SET DEFAULT now();
INSERT INTO base_table(id) VALUES(1);  -- ts will receive a NULL
INSERT INTO a_view(id) VALUES(2);  -- ts will receive the current time
```

## Compatibilidade

`ALTER VIEW` é uma extensão do PostgreSQL do padrão SQL.

## Veja também

[Crie a visualização](sql-createview.md "CREATE VIEW"), [Exclua a visualização](sql-dropview.md "DROP VIEW")