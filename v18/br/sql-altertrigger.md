## ALTER TRIGGER

ALTER TRIGGER — alterar a definição de um gatilho

## Sinopse

```
ALTER TRIGGER name ON table_name RENAME TO new_name
ALTER TRIGGER name ON table_name [ NO ] DEPENDS ON EXTENSION extension_name
```

## Descrição

`ALTER TRIGGER` altera as propriedades de um gatilho existente.

A cláusula `RENAME` muda o nome do gatilho fornecido sem alterar, de outra forma, a definição do gatilho. Se a tabela em que o gatilho está inserida for uma tabela particionada, os gatilhos clonados correspondentes nas partições também serão renomeados.

A cláusula `DEPENDS ON EXTENSION` marca o gatilho como dependente de uma extensão, de modo que, se a extensão for removida, o gatilho será automaticamente removido também.

Você deve possuir a tabela na qual o gatilho atua para poder alterar suas propriedades.

## Parâmetros

*`name`*: O nome de um gatilho existente para alterar.

*`table_name`*: O nome da tabela sobre a qual este gatilho atua.

*`new_name`*: O novo nome para o gatilho.

*`extension_name`*: O nome da extensão da qual o gatilho deve depender (ou que não deve mais depender, se `NO` for especificado). Um gatilho marcado como dependente de uma extensão é automaticamente descartado quando a extensão é descartada.

## Notas

A capacidade de habilitar ou desabilitar temporariamente um gatilho é fornecida por `ALTER TABLE`(sql-altertable.md "ALTER TABLE"), não por `ALTER TRIGGER`, porque `ALTER TRIGGER` não tem uma maneira conveniente de expressar a opção de habilitar ou desabilitar todos os gatilhos de uma tabela de uma só vez.

## Exemplos

Para renomear um gatilho existente:

```
ALTER TRIGGER emp_stamp ON emp RENAME TO emp_track_chgs;
```

Para marcar um gatilho como dependente de uma extensão:

```
ALTER TRIGGER emp_stamp ON emp DEPENDS ON EXTENSION emplib;
```

## Compatibilidade

`ALTER TRIGGER` é uma extensão do PostgreSQL do padrão SQL.

## Veja também

[ALTER TABLE](sql-altertable.md "ALTER TABLE")