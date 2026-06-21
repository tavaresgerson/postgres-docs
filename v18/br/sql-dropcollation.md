## DROP COLLATION

DROP COLLATION — remova uma correção de texto

## Sinopse

```
DROP COLLATION [ IF EXISTS ] name [ CASCADE | RESTRICT ]
```

## Descrição

`DROP COLLATION` remove uma correção previamente definida. Para poder descartar uma correção, você deve possuir a correção.

## Parâmetros

`IF EXISTS`: Não exija erro se a correção não existir. Neste caso, é emitido um aviso.

*`name`*: O nome da correção. O nome da correção pode ser qualificado pelo esquema.

`CASCADE`: Descarte automaticamente os objetos que dependem da correção, e, por sua vez, todos os objetos que dependem desses objetos (consulte [Seção 5.15][(ddl-depend.md "5.15. Dependency Tracking")]).

`RESTRICT`: Rejeitar a eliminação da agregação se quaisquer objetos dependerem dela. Esse é o padrão.

## Exemplos

Para descartar a agregação nomeada `german`:

```
DROP COLLATION german;
```

## Compatibilidade

O comando `DROP COLLATION` está de acordo com o padrão SQL, à exceção da opção `IF EXISTS`, que é uma extensão do PostgreSQL.

## Veja também

[ALTERAR COLUNA DE ORDENAÇÃO](sql-altercollation.md "ALTER COLLATION"), [CADASTRAR COLUNA DE ORDENAÇÃO](sql-createcollation.md "CREATE COLLATION")