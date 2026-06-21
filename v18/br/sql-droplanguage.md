## DROP LANGUAGE

DROP LANGUAGE — remover uma linguagem procedural

## Sinopse

```
DROP [ PROCEDURAL ] LANGUAGE [ IF EXISTS ] name [ CASCADE | RESTRICT ]
```

## Descrição

`DROP LANGUAGE` remove a definição de um idioma de procedimento previamente registrado. Você deve ser um superusuário ou o proprietário do idioma para usar `DROP LANGUAGE`.

### Nota

A partir do PostgreSQL 9.1, a maioria dos linguagens procedimentais foi transformada em “extensões” e, portanto, deve ser removida com `DROP EXTENSION` não (sql-dropextension.md "DROP EXTENSION") `DROP LANGUAGE`.

## Parâmetros

`IF EXISTS`: Não exija erro se a língua não existir. Um aviso é emitido neste caso.

*`name`*: O nome de uma linguagem procedural existente.

`CASCADE`: Descarte automaticamente os objetos que dependem da linguagem (como funções na linguagem), e, por sua vez, todos os objetos que dependem desses objetos (consulte [Seção 5.15][(ddl-depend.md "5.15. Dependency Tracking")]).

`RESTRICT`: Não se afaste do idioma se algum objeto depender dele. Esse é o padrão.

## Exemplos

Este comando remove a linguagem procedural `plsample`:

```
DROP LANGUAGE plsample;
```

## Compatibilidade

Não há nenhuma declaração `DROP LANGUAGE` no padrão SQL.

## Veja também

[ALTERAR LINGUAGEM](sql-alterlanguage.md "ALTER LANGUAGE"), [CADASTRAR LINGUAGEM](sql-createlanguage.md "CREATE LANGUAGE")