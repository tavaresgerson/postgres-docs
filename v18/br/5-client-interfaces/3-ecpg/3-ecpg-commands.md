## 34.3. Executar comandos SQL [#](#ECPG-COMMANDS)

* [34.3.1. Elaboração de instruções SQL](ecpg-commands.md#ECPG-EXECUTING)
* [34.3.2. Uso de cursor](ecpg-commands.md#ECPG-CURSORS)
* [34.3.3. Gerenciamento de transações](ecpg-commands.md#ECPG-TRANSACTIONS)
* [34.3.4. Elaboração preparada](ecpg-commands.md#ECPG-PREPARED)

Qualquer comando SQL pode ser executado dentro de uma aplicação de SQL integrada. Abaixo estão alguns exemplos de como fazer isso.

### 34.3.1. Executando instruções SQL [#](#ECPG-EXECUTING)

Criando uma tabela:

```
EXEC SQL CREATE TABLE foo (number integer, ascii char(16));
EXEC SQL CREATE UNIQUE INDEX num1 ON foo(number);
EXEC SQL COMMIT;
```

Inserindo linhas:

```
EXEC SQL INSERT INTO foo (number, ascii) VALUES (9999, 'doodad');
EXEC SQL COMMIT;
```

Excluindo linhas:

```
EXEC SQL DELETE FROM foo WHERE number = 9999;
EXEC SQL COMMIT;
```

Atualizações:

```
EXEC SQL UPDATE foo
    SET ascii = 'foobar'
    WHERE number = 9999;
EXEC SQL COMMIT;
```

As declarações `SELECT` que retornam uma única linha de resultado também podem ser executadas usando `EXEC SQL` diretamente. Para lidar com conjuntos de resultados com várias linhas, uma aplicação deve usar um cursor; veja [Seção 34.3.2](ecpg-commands.md#ECPG-CURSORS) abaixo. (Como um caso especial, uma aplicação pode obter várias linhas de uma vez em uma variável hospedeira de matriz; veja [Seção 34.4.4.3.1](ecpg-variables.md#ECPG-VARIABLES-ARRAYS).

Seleção de linha única:

```
EXEC SQL SELECT foo INTO :FooBar FROM table1 WHERE ascii = 'doodad';
```

Além disso, um parâmetro de configuração pode ser recuperado com o comando `SHOW`:

```
EXEC SQL SHOW search_path INTO :var;
```

Os tokens da forma `:something` são *variáveis hospedeira*, ou seja, eles se referem a variáveis no programa C. Eles são explicados em [Seção 34.4](ecpg-variables.md).

### 34.3.2. Uso de cursor [#](#ECPG-CURSORS)

Para recuperar um conjunto de resultados que contém várias linhas, uma aplicação deve declarar um cursor e obter cada linha do cursor. Os passos para usar um cursor são os seguintes: declarar um cursor, abri-lo, obter uma linha do cursor, repetir e, finalmente, fechá-lo.

Selecionar usando cursor:

```
EXEC SQL DECLARE foo_bar CURSOR FOR
    SELECT number, ascii FROM foo
    ORDER BY ascii;
EXEC SQL OPEN foo_bar;
EXEC SQL FETCH foo_bar INTO :FooBar, DooDad;
...
EXEC SQL CLOSE foo_bar;
EXEC SQL COMMIT;
```

Para mais detalhes sobre a declaração de um cursor, consulte [DECLARE](ecpg-sql-declare.md "DECLARE"); para mais detalhes sobre a obtenção de linhas de um cursor, consulte [FETCH](sql-fetch.md "FETCH").

### Nota

O comando ECPG `DECLARE` não realmente faz com que uma declaração seja enviada ao backend do PostgreSQL. O cursor é aberto no backend (usando o comando `DECLARE` do backend) no ponto em que o comando `OPEN` é executado.

### 34.3.3. Gerenciamento de Transações [#](#ECPG-TRANSACTIONS)

No modo padrão, as declarações são realizadas apenas quando o `EXEC SQL COMMIT` é emitido. A interface de SQL integrada também suporta o autocommit de transações (semelhante ao comportamento padrão do psql) via a opção de linha de comando `-t` para `ecpg` (ver [ecpg](app-ecpg.md)) ou via a declaração `EXEC SQL SET AUTOCOMMIT TO ON`. No modo autocommit, cada comando é automaticamente realizado, a menos que esteja dentro de um bloco de transação explícito. Esse modo pode ser desligado explicitamente usando `EXEC SQL SET AUTOCOMMIT TO OFF`.

Os seguintes comandos de gerenciamento de transações estão disponíveis:

`EXEC SQL COMMIT` [#](#ECPG-TRANSACTIONS-EXEC-SQL-COMMIT): Realizar uma transação em andamento.

`EXEC SQL ROLLBACK` [#](#ECPG-TRANSACTIONS-EXEC-SQL-ROLLBACK): Reverter uma transação em andamento.

`EXEC SQL PREPARE TRANSACTION` *`transaction_id`* [#](#ECPG-TRANSACTIONS-EXEC-SQL-PREPARE-TRANSACTION): Prepare a transação atual para o compromisso de duas fases.

`EXEC SQL COMMIT PREPARED` *`transaction_id`* [#](#ECPG-TRANSACTIONS-EXEC-SQL-COMMIT-PREPARED): Realizar uma transação que esteja em estado preparado.

`EXEC SQL ROLLBACK PREPARED` *`transaction_id`* [#](#ECPG-TRANSACTIONS-EXEC-SQL-ROLLBACK-PREPARED): Reverter uma transação que está em estado preparado.

`EXEC SQL SET AUTOCOMMIT TO ON` [#](#ECPG-TRANSACTIONS-EXEC-SQL-AUTOCOMMIT-ON): Habilitar o modo de autocommit.

`EXEC SQL SET AUTOCOMMIT TO OFF` [#](#ECPG-TRANSACTIONS-EXEC-SQL-AUTOCOMMIT-OFF): Desative o modo de autocommit. Este é o padrão.

### 34.3.4. Declarações preparadas [#](#ECPG-PREPARED)

Quando os valores a serem passados para uma declaração SQL não são conhecidos no momento da compilação, ou se a mesma declaração será usada muitas vezes, então as declarações preparadas podem ser úteis.

A declaração é preparada usando o comando `PREPARE`. Para os valores que ainda não são conhecidos, use o marcador de posição “`?`”:

```
EXEC SQL PREPARE stmt1 FROM "SELECT oid, datname FROM pg_database WHERE oid = ?";
```

Se uma declaração retornar uma única linha, o aplicativo pode chamar `EXECUTE` após `PREPARE` para executar a declaração, fornecendo os valores reais para os marcadores com uma cláusula `USING`:

```
EXEC SQL EXECUTE stmt1 INTO :dboid, :dbname USING 1;
```

Se uma declaração retornar várias linhas, o aplicativo pode usar um cursor declarado com base na declaração preparada. Para vincular parâmetros de entrada, o cursor deve ser aberto com uma cláusula `USING`:

```
EXEC SQL PREPARE stmt1 FROM "SELECT oid,datname FROM pg_database WHERE oid > ?";
EXEC SQL DECLARE foo_bar CURSOR FOR stmt1;

/* when end of result set reached, break out of while loop */
EXEC SQL WHENEVER NOT FOUND DO BREAK;

EXEC SQL OPEN foo_bar USING 100;
...
while (1)
{
    EXEC SQL FETCH NEXT FROM foo_bar INTO :dboid, :dbname;
    ...
}
EXEC SQL CLOSE foo_bar;
```

Quando você não precisa mais da declaração preparada, você deve liberar o espaço ocupado por ela:

```
EXEC SQL DEALLOCATE PREPARE name;
```

Para mais detalhes sobre `PREPARE`, consulte [PREPARE](ecpg-sql-prepare.md "PREPARE"). Veja também [Seção 34.5](ecpg-dynamic.md "34.5. Dynamic SQL") para mais detalhes sobre o uso de marcadores e parâmetros de entrada.