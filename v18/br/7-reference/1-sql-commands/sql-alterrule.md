## ALTERAR REGRA

ALTERAR REGRA — alterar a definição de uma regra

## Sinopse

```
ALTER RULE name ON table_name RENAME TO new_name
```

## Descrição

`ALTER RULE` altera as propriedades de uma regra existente. Atualmente, a única ação disponível é alterar o nome da regra.

Para usar `ALTER RULE`, você deve possuir a tabela ou a visão para a qual a regra se aplica.

## Parâmetros

*`name`*: O nome de uma regra existente para alterar.

*`table_name`*: O nome (opcionalmente qualificado por esquema) da tabela ou visão a que a regra se aplica.

*`new_name`*: O novo nome para a regra.

## Exemplos

Para renomear uma regra existente:

```
ALTER RULE notify_all ON emp RENAME TO notify_me;
```

## Compatibilidade

`ALTER RULE` é uma extensão de linguagem do PostgreSQL, assim como todo o sistema de reescrita de consultas.

## Veja também

[CREEAR REGRA](sql-createrule.md "CREATE RULE"), [DROP REGRA](sql-droprule.md "DROP RULE")