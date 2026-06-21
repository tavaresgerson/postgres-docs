## DROP PROCEDURE

DROP PROCEDURE — remover um procedimento

## Sinopse

```
DROP PROCEDURE [ IF EXISTS ] name [ ( [ [ argmode ] [ argname ] argtype [, ...] ] ) ] [, ...]
    [ CASCADE | RESTRICT ]
```

## Descrição

`DROP PROCEDURE` remove a definição de um ou mais procedimentos existentes. Para executar este comando, o usuário deve ser o proprietário do(s) procedimento(s). Os tipos de argumentos para o(s) procedimento(s) geralmente devem ser especificados, uma vez que vários procedimentos diferentes podem existir com o mesmo nome e listas de argumentos diferentes.

## Parâmetros

`IF EXISTS`: Não exija erro se o procedimento não existir. Neste caso, é emitido um aviso.

*`name`*: O nome (opcionalmente qualificado por esquema) de um procedimento existente.

*`argmode`*: O modo de um argumento: `IN`, `OUT`, `INOUT` ou `VARIADIC`. Se omitido, o padrão é `IN` (mas veja abaixo).

*`argname`*: O nome de um argumento. Observe que `DROP PROCEDURE` não presta atenção na verdade aos nomes dos argumentos, uma vez que apenas os tipos de dados dos argumentos são usados para determinar a identidade do procedimento.

*`argtype`*: O(s) tipo(s) de dados dos argumentos do procedimento (opcionalmente qualificados por esquema), se houver. Consulte os detalhes abaixo.

`CASCADE`: Descarte automaticamente os objetos que dependem do procedimento e, por sua vez, todos os objetos que dependem desses objetos (consulte [Seção 5.15][(ddl-depend.md "5.15. Dependency Tracking")]).

`RESTRICT`: Não se recusar a descartar o procedimento se algum objeto depender dele. Esse é o padrão.

## Notas

Se houver apenas um procedimento com esse nome, a lista de argumentos pode ser omitida. Nesse caso, também omita as chaves.

Em PostgreSQL, é suficiente listar os argumentos de entrada (incluindo `INOUT`) porque não é permitido que duas rotinas com o mesmo nome compartilhem a mesma lista de argumentos de entrada. Além disso, o comando `DROP` não verificará se você escreveu os tipos de argumentos `OUT` corretamente; portanto, quaisquer argumentos que sejam explicitamente marcados `OUT` são apenas ruídos. Mas escrevê-los é recomendável para consistência com o comando correspondente `CREATE`.

Para compatibilidade com o padrão SQL, também é permitido escrever todos os tipos de dados dos argumentos (incluindo os dos argumentos `OUT`) sem quaisquer marcadores *`argmode`*. Quando isso é feito, os tipos dos argumentos `OUT` do procedimento *irão* ser verificados em relação ao comando. Esta disposição cria uma ambiguidade, pois, quando a lista de argumentos não contém marcadores *`argmode`*, não está claro qual regra é pretendida. O comando `DROP` tentará a busca em ambas as direções e lançará um erro se forem encontrados dois procedimentos diferentes. Para evitar o risco de tal ambiguidade, é recomendável escrever marcadores `IN` explicitamente, em vez de deixá-los por padrão, forçando assim a interpretação tradicional do PostgreSQL a ser usada.

As regras de busca que acabamos de explicar também são usadas por outros comandos que atuam em procedimentos existentes, como `ALTER PROCEDURE` e `COMMENT ON PROCEDURE`.

## Exemplos

Se houver apenas um procedimento `do_db_maintenance`, este comando é suficiente para descartá-lo:

```
DROP PROCEDURE do_db_maintenance;
```

Dado esta definição do procedimento:

```
CREATE PROCEDURE do_db_maintenance(IN target_schema text, OUT results text) ...
```

qualquer um desses comandos funcionaria para descartá-lo:

```
DROP PROCEDURE do_db_maintenance(IN target_schema text, OUT results text);
DROP PROCEDURE do_db_maintenance(IN text, OUT text);
DROP PROCEDURE do_db_maintenance(IN text);
DROP PROCEDURE do_db_maintenance(text);
DROP PROCEDURE do_db_maintenance(text, text);  -- potentially ambiguous
```

No entanto, o último exemplo seria ambíguo se, por exemplo,

```
CREATE PROCEDURE do_db_maintenance(IN target_schema text, IN options text) ...
```

## Compatibilidade

Este comando está de acordo com o padrão SQL, com essas extensões do PostgreSQL:

* O padrão permite que apenas um procedimento seja excluído por comando. * A opção `IF EXISTS` é uma extensão. * A capacidade de especificar modos e nomes de argumentos é uma extensão, e as regras de busca diferem quando os modos são fornecidos.

## Veja também

[Crie procedimento](sql-createprocedure.md "CREATE PROCEDURE"), [Altere procedimento](sql-alterprocedure.md "ALTER PROCEDURE"), [Exclua função](sql-dropfunction.md "DROP FUNCTION"), [Exclua rotina](sql-droproutine.md "DROP ROUTINE")