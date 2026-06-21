## 42.11. Configuração do PL/Tcl [#](#PLTCL-CONFIG)

Esta seção lista os parâmetros de configuração que afetam o PL/Tcl.

`pltcl.start_proc` (`string`) [#](#GUC-PLTCL-START-PROC): Este parâmetro, se definido como uma string não vazia, especifica o nome (possível com qualificação de esquema) de uma função PL/Tcl sem parâmetros que deve ser executada sempre que um novo interpretador Tcl é criado para PL/Tcl. Tal função pode realizar a inicialização por sessão, como carregar código Tcl adicional. Um novo interpretador Tcl é criado quando uma função PL/Tcl é executada pela primeira vez em uma sessão de banco de dados, ou quando um interpretador adicional deve ser criado porque uma função PL/Tcl é chamada por um novo papel SQL.

A função referenciada deve ser escrita na língua `pltcl`, e não deve ser marcada `SECURITY DEFINER`. (Essas restrições garantem que ela seja executada no interpretador que ela deve inicializar. O usuário atual também deve ter permissão para chamá-la.

Se a função falhar com um erro, ela abortará a chamada de função que causou a criação do novo interpretador e propagará para a consulta que fez a chamada, fazendo com que a transação ou subtransação atual seja abortada. Quaisquer ações já realizadas dentro do Tcl não serão desfeitas; no entanto, esse interpretador não será usado novamente. Se a linguagem for usada novamente, a inicialização será realizada novamente dentro de um novo interpretador Tcl.

Somente usuários super podem alterar essa configuração. Embora essa configuração possa ser alterada durante uma sessão, essas alterações não afetarão os interpretadores Tcl que já foram criados.

`pltclu.start_proc` (`string`) [#](#GUC-PLTCLU-START-PROC): Este parâmetro é exatamente igual ao `pltcl.start_proc`, exceto que se aplica ao PL/TclU. A função referenciada deve ser escrita na linguagem `pltclu`.