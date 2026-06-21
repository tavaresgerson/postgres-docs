## 36.4. Procedimentos Definidos pelo Usuário [#](#XPROC)

Um procedimento é um objeto de banco de dados semelhante a uma função. As principais diferenças são:

* Os procedimentos são definidos com o comando `CREATE PROCEDURE` (sql-createprocedure.md "CREATE PROCEDURE"), não `CREATE FUNCTION`.
* Os procedimentos não retornam um valor de função; portanto, o `CREATE PROCEDURE` não possui uma cláusula `RETURNS`. No entanto, os procedimentos podem, em vez disso, retornar dados para seus chamados por meio de parâmetros de saída.
* Enquanto uma função é chamada como parte de uma consulta ou comando DML, um procedimento é chamado em isolamento usando o comando [`CALL` (sql-call.md "CALL").
* Um procedimento pode confirmar ou reverter transações durante sua execução (então iniciando automaticamente uma nova transação), desde que o comando `CALL` invocante não faça parte de um bloco de transação explícito. Uma função não pode fazer isso.
* Certos atributos de função, como a estrícção, não se aplicam a procedimentos. Esses atributos controlam como a função é usada em uma consulta, o que não é relevante para os procedimentos.

As explicações nas seções a seguir sobre como definir funções definidas pelo usuário se aplicam também a procedimentos, exceto pelos pontos mencionados acima.

Coletivamente, funções e procedimentos também são conhecidos como *rotinas*. Existem comandos como `ALTER ROUTINE`(sql-alterroutine.md "ALTER ROUTINE") e `DROP ROUTINE`(sql-droproutine.md "DROP ROUTINE") que podem operar em funções e procedimentos sem precisar saber qual tipo é. No entanto, observe que não há comando `CREATE ROUTINE`.