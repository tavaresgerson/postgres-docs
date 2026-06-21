## OPERADOR DROP

DROP OPERATOR — remova um operador

## Sinopse

```
DROP OPERATOR [ IF EXISTS ] name ( { left_type | NONE } , right_type ) [, ...] [ CASCADE | RESTRICT ]
```

## Descrição

`DROP OPERATOR` remove um operador existente do sistema de banco de dados. Para executar este comando, você deve ser o proprietário do operador.

## Parâmetros

`IF EXISTS`: Não exija erro se o operador não existir. Neste caso, é emitido um aviso.

*`name`*: O nome (opcionalmente qualificado por esquema) de um operador existente.

*`left_type`*: O tipo de dados do operador do operando esquerdo; escreva `NONE` se o operador não tiver um operando esquerdo.

*`right_type`*: O tipo de dados do operador do operando da direita.

`CASCADE`: Descarte automaticamente os objetos que dependem do operador (como as visualizações que o utilizam), e, por sua vez, todos os objetos que dependem desses objetos (consulte [Seção 5.15](ddl-depend.md)).

`RESTRICT`: Não se recusar a descartar o operador se algum objeto depender dele. Esse é o padrão.

## Exemplos

Remova o operador de energia `a^b` para o tipo `integer`:

```
DROP OPERATOR ^ (integer, integer);
```

Remova o operador de prefixo de complemento bit a bit `~b` para o tipo `bit`:

```
DROP OPERATOR ~ (none, bit);
```

Remova vários operadores em um comando:

```
DROP OPERATOR ~ (none, bit), ^ (integer, integer);
```

## Compatibilidade

Não há nenhuma declaração `DROP OPERATOR` no padrão SQL.

## Veja também

[Crie Operador](sql-createoperator.md "CREATE OPERATOR"), [Altere Operador](sql-alteroperator.md "ALTER OPERATOR")