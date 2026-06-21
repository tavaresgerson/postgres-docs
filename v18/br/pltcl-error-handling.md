## 42.8. Gerenciamento de Erros em PL/Tcl [#](#PLTCL-ERROR-HANDLING)

O código Tcl dentro ou chamado a partir de uma função PL/Tcl pode gerar um erro, seja executando uma operação inválida ou gerando um erro usando o comando Tcl `error` ou o comando `elog` do PL/Tcl. Esses erros podem ser capturados dentro do Tcl usando o comando Tcl `catch`. Se um erro não for capturado, mas permitido propagar até o nível superior de execução da função PL/Tcl, ele é relatado como um erro SQL na consulta que está chamando a função.

Por outro lado, os erros SQL que ocorrem dentro dos comandos `spi_exec`, `spi_prepare` e `spi_execp` do PL/Tcl são relatados como erros Tcl, portanto, podem ser detectados pelo comando `catch` do Tcl. (Cada um desses comandos PL/Tcl executa sua operação SQL em uma subtransação, que é revertida em caso de erro, de modo que qualquer operação parcialmente concluída é automaticamente limpa.) Novamente, se um erro se propagar até o nível superior sem ser detectado, ele volta a se tornar um erro SQL.

O Tcl fornece uma variável `errorCode` que pode representar informações adicionais sobre um erro em um formulário que é fácil para os programas Tcl interpretar. O conteúdo está no formato de lista Tcl, e a primeira palavra identifica o subsistema ou a biblioteca que relata o erro; além disso, o conteúdo é deixado para o subsistema ou biblioteca individual. Para erros de banco de dados relatados por comandos PL/Tcl, a primeira palavra é `POSTGRES`, a segunda palavra é o número da versão do PostgreSQL, e palavras adicionais são pares de nome/valor de campo fornecendo informações detalhadas sobre o erro. Os campos `SQLSTATE`, `condition` e `message` são sempre fornecidos (os dois primeiros representam o código de erro e o nome da condição conforme mostrado em [Apêndice A][(errcodes-appendix.md "Appendix A. PostgreSQL Error Codes")]). Os campos que podem estar presentes incluem `detail`, `hint`, `context`, `schema`, `table`, `column`, `datatype`, `constraint`, `statement`, `cursor_position`, `filename`, `lineno` e `funcname`.

Uma maneira conveniente de trabalhar com as informações `errorCode` do PL/Tcl é carregá-las em um array, de modo que os nomes dos campos se tornem índices do array. O código para fazer isso pode parecer assim:

```
if {[catch { spi_exec $sql_command }]} {
    if {[lindex $::errorCode 0] == "POSTGRES"} {
        array set errorArray $::errorCode
        if {$errorArray(condition) == "undefined_table"} {
            # deal with missing table
        } else {
            # deal with some other type of SQL error
        }
    }
}
```

(Os dois pontos colchetes especificam explicitamente que `errorCode` é uma variável global.)