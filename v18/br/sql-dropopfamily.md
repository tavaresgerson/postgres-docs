## FAMÍLIA DE OPERADORES DE DROGAS

DROP OPERATOR FAMILY — remover uma família de operadores

## Sinopse

```
DROP OPERATOR FAMILY [ IF EXISTS ] name USING index_method [ CASCADE | RESTRICT ]
```

## Descrição

`DROP OPERATOR FAMILY` elimina uma família de operadores existente. Para executar este comando, você deve ser o proprietário da família de operadores.

`DROP OPERATOR FAMILY` inclui a eliminação de quaisquer classes de operador contidas na família, mas não elimina nenhum dos operadores ou funções referenciados pela família. Se houver algum índice dependente de classes de operador dentro da família, você precisará especificar `CASCADE` para que a eliminação seja concluída.

## Parâmetros

`IF EXISTS`: Não exija erro se a família de operadores não existir. Neste caso, é emitido um aviso.

*`name`*: O nome (opcionalmente qualificado por esquema) de uma família de operadores existente.

*`index_method`*: O nome do método de acesso ao índice para o qual a família de operadores é destinada.

`CASCADE`: Descarte automaticamente os objetos que dependem da família de operadores e, por sua vez, todos os objetos que dependem desses objetos (consulte [Seção 5.15][(ddl-depend.md "5.15. Dependency Tracking")]).

`RESTRICT`: Rejeitar a eliminação da família de operadores se algum objeto depender dela. Este é o padrão.

## Exemplos

Remova a família de operadores de árvore B `float_ops`:

```
DROP OPERATOR FAMILY float_ops USING btree;
```

Este comando não terá sucesso se houver algum índice existente que utilize classes de operador dentro da família. Adicione `CASCADE` para descartar tais índices juntamente com a família de operadores.

## Compatibilidade

Não há nenhuma declaração `DROP OPERATOR FAMILY` no padrão SQL.

## Veja também

[ALTERAR FAMÍLIA DE OPERADORES](sql-alteropfamily.md "ALTER OPERATOR FAMILY"), [CADASTRAR FAMÍLIA DE OPERADORES](sql-createopfamily.md "CREATE OPERATOR FAMILY"), [ALTERAR CLASSE DE OPERADOR](sql-alteropclass.md "ALTER OPERATOR CLASS"), [CADASTRAR CLASSE DE OPERADOR](sql-createopclass.md "CREATE OPERATOR CLASS"), [CANCELAR CLASSE DE OPERADOR](sql-dropopclass.md "DROP OPERATOR CLASS")