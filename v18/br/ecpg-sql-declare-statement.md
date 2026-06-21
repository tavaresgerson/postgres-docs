## DECLARAÇÃO DE DECLARAR

DECLARAÇÃO DECLARATIVA — identificador de declaração SQL

## Sinopse

```
EXEC SQL [ AT connection_name ] DECLARE statement_name STATEMENT
```

## Descrição

`DECLARE STATEMENT` declara um identificador de declaração SQL. O identificador de declaração SQL pode ser associado à conexão. Quando o identificador é usado por declarações SQL dinâmicas, as declarações são executadas usando a conexão associada. O espaço de nome da declaração é a unidade pré-compilada, e várias declarações para o mesmo identificador de declaração SQL não são permitidas. Note que, se o pré-compilador for executado no modo de compatibilidade Informix e alguma declaração SQL for declarada, "database" não pode ser usado como nome de cursor.

## Parâmetros

*`connection_name`* [#](#ECPG-SQL-DECLARE-STATEMENT-CONNECTION-NAME): Um nome de conexão de banco de dados estabelecido pelo comando `CONNECT`.

A cláusula AT pode ser omitida, mas tal declaração não tem significado.

*`statement_name`* [#](#ECPG-SQL-DECLARE-STATEMENT-STATEMENT-NAME): O nome de um identificador de declaração SQL, seja como um identificador SQL ou uma variável de host.

## Notas

Essa associação é válida apenas se a declaração estiver fisicamente localizada no topo de uma declaração dinâmica.

## Exemplos

```
EXEC SQL CONNECT TO postgres AS con1;
EXEC SQL AT con1 DECLARE sql_stmt STATEMENT;
EXEC SQL DECLARE cursor_name CURSOR FOR sql_stmt;
EXEC SQL PREPARE sql_stmt FROM :dyn_string;
EXEC SQL OPEN cursor_name;
EXEC SQL FETCH cursor_name INTO :column1;
EXEC SQL CLOSE cursor_name;
```

## Compatibilidade

`DECLARE STATEMENT` é uma extensão do padrão SQL, mas pode ser usada em sistemas de gerenciamento de banco de dados famosos.

## Veja também

[CONECTAR](ecpg-sql-connect.md "CONNECT"), [DECLARAÇÃO](ecpg-sql-declare.md "DECLARE"), [ABERTO](ecpg-sql-open.md "OPEN")