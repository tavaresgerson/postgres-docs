## TIPO DE RETIREMENTO

DROP TYPE — remova um tipo de dados

## Sinopse

```
DROP TYPE [ IF EXISTS ] name [, ...] [ CASCADE | RESTRICT ]
```

## Descrição

`DROP TYPE` remove um tipo de dados definido pelo usuário. Apenas o proprietário de um tipo pode removê-lo.

## Parâmetros

`IF EXISTS`: Não exija erro se o tipo não existir. Neste caso, é emitido um aviso.

*`name`*: O nome (opcionalmente qualificado por esquema) do tipo de dados a ser removido.

`CASCADE`: Descarte automaticamente os objetos que dependem do tipo (como colunas de tabela, funções e operadores), e, por sua vez, todos os objetos que dependem desses objetos (consulte [Seção 5.15](ddl-depend.md)).

`RESTRICT`: Rejeitar a eliminação do tipo se houver objetos que dependem dele. Esse é o padrão.

## Exemplos

Para remover o tipo de dados `box`:

```
DROP TYPE box;
```

## Compatibilidade

Este comando é semelhante ao comando correspondente no padrão SQL, à exceção da opção `IF EXISTS`, que é uma extensão do PostgreSQL. Mas observe que grande parte do comando `CREATE TYPE` e os mecanismos de extensão do tipo de dados no PostgreSQL diferem do padrão SQL.

## Veja também

[ALTER TYPE](sql-altertype.md "ALTER TYPE"), [CREATE TYPE](sql-createtype.md "CREATE TYPE")