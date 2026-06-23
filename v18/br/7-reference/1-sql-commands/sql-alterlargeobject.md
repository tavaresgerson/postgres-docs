## ALTER LARGE OBJECT

ALTERAR OBJETO GRANDE — alterar a definição de um objeto grande

## Sinopse

```
ALTER LARGE OBJECT large_object_oid OWNER TO { new_owner | CURRENT_ROLE | CURRENT_USER | SESSION_USER }
```

## Descrição

`ALTER LARGE OBJECT` altera a definição de um objeto grande.

Você deve ser o proprietário do grande objeto para usar `ALTER LARGE OBJECT`. Para alterar o proprietário, você também deve ser capaz de `SET ROLE` para o novo papel de proprietário. (No entanto, um superusuário pode alterar qualquer grande objeto de qualquer maneira.) Atualmente, a única funcionalidade é atribuir um novo proprietário, então ambas as restrições sempre se aplicam.

## Parâmetros

*`large_object_oid`*: OID do grande objeto que será alterado

*`new_owner`*: O novo proprietário do grande objeto

## Compatibilidade

Não há nenhuma declaração `ALTER LARGE OBJECT` no padrão SQL.

## Veja também

[Capítulo 33](largeobjects.md "Chapter 33. Large Objects")