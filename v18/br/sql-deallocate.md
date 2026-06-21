## DESLOCUE

REDESLOCAR — deslocar uma declaração preparada

## Sinopse

```
DEALLOCATE [ PREPARE ] { name | ALL }
```

## Descrição

`DEALLOCATE` é usado para realocar uma declaração SQL previamente preparada. Se você não realocar explicitamente uma declaração preparada, ela é realocada quando a sessão termina.

Para mais informações sobre declarações preparadas, consulte [PREPARE](sql-prepare.md "PREPARE").

## Parâmetros

`PREPARE`: Esta palavra-chave é ignorada.

*`name`*: O nome da declaração preparada para realocar.

`ALL`: Desfazer todas as declarações preparadas.

## Compatibilidade

O padrão SQL inclui uma declaração `DEALLOCATE`, mas ela é apenas para uso em SQL embutido.

## Veja também

[EXECUTAR](sql-execute.md "EXECUTE"), [PREPARAR](sql-prepare.md "PREPARE")