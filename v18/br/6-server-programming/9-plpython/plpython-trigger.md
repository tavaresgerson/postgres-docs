## 44.5. Funções de disparo [#](#PLPYTHON-TRIGGER)

Quando uma função é usada como um gatilho, o dicionário `TD` contém valores relacionados ao gatilho:

`TD["event"]`: contém o evento como uma string: `INSERT`, `UPDATE`, `DELETE` ou `TRUNCATE`.

`TD["when"]`: contém um dos `BEFORE`, `AFTER` ou `INSTEAD OF`.

`TD["level"]`: contém `ROW` ou `STATEMENT`.

`TD["new"]` `TD["old"]`: Para um gatilho de nível de linha, um ou ambos desses campos contêm as respectivas linhas do gatilho, dependendo do evento do gatilho.

`TD["name"]`: contém o nome do gatilho.

`TD["table_name"]`: contém o nome da tabela em que o gatilho ocorreu.

`TD["table_schema"]`: contém o esquema da tabela em que o gatilho ocorreu.

`TD["relid"]`: contém o OID da tabela em que o gatilho ocorreu.

`TD["args"]`: Se o comando `CREATE TRIGGER` incluísse argumentos, eles estão disponíveis em `TD["args"][0]` para `TD["args"][n-1]`.

Se `TD["when"]` for `BEFORE` ou `INSTEAD OF` e `TD["level"]` for `ROW`, você pode retornar `None` ou `"OK"` da função Python para indicar que a linha não foi modificada, `"SKIP"` para abortar o evento, ou se `TD["event"]` for `INSERT` ou `UPDATE`, você pode retornar `"MODIFY"` para indicar que você modificou a nova linha. Caso contrário, o valor de retorno é ignorado.