## DECLARA-SE

DECLARE — definir um cursor

## Sinopse

```
DECLARE cursor_name [ BINARY ] [ ASENSITIVE | INSENSITIVE ] [ [ NO ] SCROLL ] CURSOR [ { WITH | WITHOUT } HOLD ] FOR prepared_name
DECLARE cursor_name [ BINARY ] [ ASENSITIVE | INSENSITIVE ] [ [ NO ] SCROLL ] CURSOR [ { WITH | WITHOUT } HOLD ] FOR query
```

## Descrição

`DECLARE` declara um cursor para iterar sobre o conjunto de resultados de uma declaração preparada. Este comando tem uma semântica ligeiramente diferente do comando SQL direto `DECLARE`: Enquanto este último executa uma consulta e prepara o conjunto de resultados para recuperação, este comando SQL incorporado apenas declara um nome como uma “variável de loop” para iterar sobre o conjunto de resultados de uma consulta; a execução real acontece quando o cursor é aberto com o comando `OPEN`.

## Parâmetros

*`cursor_name`* [#](#ECPG-SQL-DECLARE-CURSOR-NAME): Um nome de cursor, sensível a maiúsculas e minúsculas. Isso pode ser um identificador SQL ou uma variável de host.

*`prepared_name`* [#](#ECPG-SQL-DECLARE-PREPARED-NAME): O nome de uma consulta preparada, seja como um identificador SQL ou uma variável de host.

*`query`* [#](#ECPG-SQL-DECLARE-QUERY): Um comando de [SELECT](sql-select.md "SELECT") ou [VALUES](sql-values.md "VALUES") que fornecerá as linhas que serão devolvidas pelo cursor.

Para o significado das opções do cursor, consulte [DECLARE](sql-declare.md "DECLARE").

## Exemplos

Exemplos declarando um cursor para uma consulta:

```
EXEC SQL DECLARE C CURSOR FOR SELECT * FROM My_Table;
EXEC SQL DECLARE C CURSOR FOR SELECT Item1 FROM T;
EXEC SQL DECLARE cur1 CURSOR FOR SELECT version();
```

Um exemplo declarando um cursor para uma declaração preparada:

```
EXEC SQL PREPARE stmt1 AS SELECT version();
EXEC SQL DECLARE cur1 CURSOR FOR stmt1;
```

## Compatibilidade

`DECLARE` é especificado no padrão SQL.

## Veja também

[ABERTO](ecpg-sql-open.md "OPEN"), [FECHO](sql-close.md "CLOSE"), [DECLARAÇÃO](sql-declare.md "DECLARE")