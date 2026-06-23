## 34.5. SQL dinâmico [#](#ECPG-DYNAMIC)

* [34.5.1. Executar declarações sem um conjunto de resultados](ecpg-dynamic.md#ECPG-DYNAMIC-WITHOUT-RESULT)
* [34.5.2. Executar uma declaração com parâmetros de entrada](ecpg-dynamic.md#ECPG-DYNAMIC-INPUT)
* [34.5.3. Executar uma declaração com um conjunto de resultados](ecpg-dynamic.md#ECPG-DYNAMIC-WITH-RESULT)

Em muitos casos, as instruções SQL específicas que uma aplicação precisa executar são conhecidas no momento em que a aplicação é escrita. Em alguns casos, no entanto, as instruções SQL são compostas em tempo de execução ou fornecidas por uma fonte externa. Nesses casos, você não pode incorporar as instruções SQL diretamente no código-fonte C, mas há uma facilidade que permite que você chame instruções SQL arbitrárias que você fornece em uma variável de string.

### 34.5.1. Executar declarações sem um conjunto de resultados [#](#ECPG-DYNAMIC-WITHOUT-RESULT)

A maneira mais simples de executar uma declaração SQL arbitrária é usar o comando `EXECUTE IMMEDIATE`. Por exemplo:

```
EXEC SQL BEGIN DECLARE SECTION;
const char *stmt = "CREATE TABLE test1 (...);";
EXEC SQL END DECLARE SECTION;

EXEC SQL EXECUTE IMMEDIATE :stmt;
```

`EXECUTE IMMEDIATE` pode ser usado para declarações SQL que não retornam um conjunto de resultados (por exemplo, DDL, `INSERT`, `UPDATE`, `DELETE`). Você não pode executar declarações que recuperam dados (por exemplo, `SELECT`) dessa maneira. A próxima seção descreve como fazer isso.

### 34.5.2. Executar uma declaração com parâmetros de entrada [#](#ECPG-DYNAMIC-INPUT)

Uma maneira mais poderosa de executar instruções SQL arbitrárias é prepará-las uma vez e executar a declaração preparada quantas vezes você quiser. Também é possível preparar uma versão generalizada de uma declaração e, em seguida, executar versões específicas dela substituindo os parâmetros. Ao preparar a declaração, escreva pontos de interrogação onde você deseja substituir os parâmetros mais tarde. Por exemplo:

```
EXEC SQL BEGIN DECLARE SECTION;
const char *stmt = "INSERT INTO test1 VALUES(?, ?);";
EXEC SQL END DECLARE SECTION;

EXEC SQL PREPARE mystmt FROM :stmt;
 ...
EXEC SQL EXECUTE mystmt USING 42, 'foobar';
```

Quando você não precisa mais da declaração preparada, você deve liberar o espaço ocupado por ela:

```
EXEC SQL DEALLOCATE PREPARE name;
```

### 34.5.3. Executar uma declaração com um conjunto de resultados [#](#ECPG-DYNAMIC-WITH-RESULT)

Para executar uma declaração SQL com uma única linha de resultado, pode-se usar `EXECUTE`. Para salvar o resultado, adicione uma cláusula `INTO`.

```
EXEC SQL BEGIN DECLARE SECTION;
const char *stmt = "SELECT a, b, c FROM test1 WHERE a > ?";
int v1, v2;
VARCHAR v3[50];
EXEC SQL END DECLARE SECTION;

EXEC SQL PREPARE mystmt FROM :stmt;
 ...
EXEC SQL EXECUTE mystmt INTO :v1, :v2, :v3 USING 37;
```

Um comando `EXECUTE` pode ter uma cláusula `INTO`, uma cláusula `USING`, ambas ou nenhuma.

Se uma consulta for esperada para retornar mais de uma linha de resultado, deve-se usar um cursor, como no exemplo a seguir. (Consulte [Seção 34.3.2] para mais detalhes sobre o cursor.)

```
EXEC SQL BEGIN DECLARE SECTION;
char dbaname[128];
char datname[128];
char *stmt = "SELECT u.usename as dbaname, d.datname "
             "  FROM pg_database d, pg_user u "
             "  WHERE d.datdba = u.usesysid";
EXEC SQL END DECLARE SECTION;

EXEC SQL CONNECT TO testdb AS con1 USER testuser;
EXEC SQL SELECT pg_catalog.set_config('search_path', '', false); EXEC SQL COMMIT;

EXEC SQL PREPARE stmt1 FROM :stmt;

EXEC SQL DECLARE cursor1 CURSOR FOR stmt1;
EXEC SQL OPEN cursor1;

EXEC SQL WHENEVER NOT FOUND DO BREAK;

while (1)
{
    EXEC SQL FETCH cursor1 INTO :dbaname,:datname;
    printf("dbaname=%s, datname=%s\n", dbaname, datname);
}

EXEC SQL CLOSE cursor1;

EXEC SQL COMMIT;
EXEC SQL DISCONNECT ALL;
```
