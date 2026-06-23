## ALTER OPERADOR

ALTERAR OPERADOR — alterar a definição de um operador

## Sinopse

```
ALTER OPERATOR name ( { left_type | NONE } , right_type )
    OWNER TO { new_owner | CURRENT_ROLE | CURRENT_USER | SESSION_USER }

ALTER OPERATOR name ( { left_type | NONE } , right_type )
    SET SCHEMA new_schema

ALTER OPERATOR name ( { left_type | NONE } , right_type )
    SET ( {  RESTRICT = { res_proc | NONE }
           | JOIN = { join_proc | NONE }
           | COMMUTATOR = com_op
           | NEGATOR = neg_op
           | HASHES
           | MERGES
          } [, ... ] )
```

## Descrição

`ALTER OPERATOR` altera a definição de um operador.

Você deve ser o operador para usar `ALTER OPERATOR`. Para alterar o proprietário, você deve ser capaz de `SET ROLE` para o novo papel de proprietário, e esse papel deve ter `CREATE` privilégio no esquema do operador. (Essas restrições garantem que alterar o proprietário não faz nada que você não poderia fazer ao descartar e recriar o operador. No entanto, um superusuário pode alterar a propriedade de qualquer operador de qualquer maneira.)

## Parâmetros

*`name`*: O nome (opcionalmente qualificado por esquema) de um operador existente.

*`left_type`*: O tipo de dados do operador do operando esquerdo; escreva `NONE` se o operador não tiver um operando esquerdo.

*`right_type`*: O tipo de dados do operador do operando da direita.

*`new_owner`*: O novo proprietário do operador.

*`new_schema`*: O novo esquema para o operador.

*`res_proc`*: A função de estimativa de seletividade de restrição para este operador; escreva NONE para remover a estimativa de seletividade existente.

*`join_proc`*: A função de estimativa de seletividade de junção para este operador; escreva NONE para remover a estimativa de seletividade existente.

*`com_op`*: O commutator deste operador. Só pode ser alterado se o operador não tiver um commutator existente.

*`neg_op`*: O negador deste operador. Só pode ser alterado se o operador não tiver um negador existente.

`HASHES`: Indica que este operador pode suportar uma junção de hash. Só pode ser habilitado e não desabilitado.

`MERGES`: Indica que este operador pode suportar uma junção de fusão. Só pode ser habilitado e não desabilitado.

## Notas

Consulte a [Seção 36.14](xoper.md) e a [Seção 36.15](xoper-optimization.md) para obter mais informações.

Como os commutatórios vêm em pares que são commutatórios uns dos outros, `ALTER OPERATOR SET COMMUTATOR` também definirá o commutatório do *`com_op`* como o operador alvo. Da mesma forma, `ALTER OPERATOR SET NEGATOR` também definirá o negador do *`neg_op`* como o operador alvo. Portanto, você deve possuir o operador de commutatório ou negador, bem como o operador alvo.

## Exemplos

Altere o proprietário do operador personalizado `a @@ b` para o tipo `text`:

```
ALTER OPERATOR @@ (text, text) OWNER TO joe;
```

Altere a restrição e as funções de estimativa de seletividade de um operador personalizado `a && b` para o tipo `int[]`:

```
ALTER OPERATOR && (int[], int[]) SET (RESTRICT = _int_contsel, JOIN = _int_contjoinsel);
```

Marque o operador `&&` como sendo seu próprio commutator:

```
ALTER OPERATOR && (int[], int[]) SET (COMMUTATOR = &&);
```

## Compatibilidade

Não há nenhuma declaração `ALTER OPERATOR` no padrão SQL.

## Veja também

[Crie Operador](sql-createoperator.md "CREATE OPERATOR"), [Remova Operador](sql-dropoperator.md "DROP OPERATOR")