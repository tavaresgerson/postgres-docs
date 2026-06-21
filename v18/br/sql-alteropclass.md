## ALTER CLASS OPERATOR

ALTERAR CLASSE OPERADOR — alterar a definição de uma classe de operador

## Sinopse

```
ALTER OPERATOR CLASS name USING index_method
    RENAME TO new_name

ALTER OPERATOR CLASS name USING index_method
    OWNER TO { new_owner | CURRENT_ROLE | CURRENT_USER | SESSION_USER }

ALTER OPERATOR CLASS name USING index_method
    SET SCHEMA new_schema
```

## Descrição

`ALTER OPERATOR CLASS` altera a definição de uma classe de operador.

Você deve possuir a classe do operador para usar `ALTER OPERATOR CLASS`. Para alterar o proprietário, você deve ser capaz de `SET ROLE` para o novo papel de proprietário, e esse papel deve ter `CREATE` privilégio no esquema da classe do operador. (Essas restrições garantem que alterar o proprietário não faz nada que você não pudesse fazer ao descartar e recriar a classe do operador. No entanto, um superusuário pode alterar a propriedade de qualquer classe do operador de qualquer maneira.)

## Parâmetros

*`name`*: O nome (opcionalmente qualificado por esquema) de uma classe de operador existente.

*`index_method`*: O nome do método de índice para o qual essa classe de operador é destinada.

*`new_name`*: O novo nome da classe do operador.

*`new_owner`*: O novo proprietário da classe de operador.

*`new_schema`*: O novo esquema para a classe de operador.

## Compatibilidade

Não há nenhuma declaração `ALTER OPERATOR CLASS` no padrão SQL.

## Veja também

[CRIAR CLASSE DE OPERADOR](sql-createopclass.md "CREATE OPERATOR CLASS"), [DROP CLASSE DE OPERADOR](sql-dropopclass.md "DROP OPERATOR CLASS"), [ALTERAR FAMÍLIA DE OPERADORES](sql-alteropfamily.md "ALTER OPERATOR FAMILY")