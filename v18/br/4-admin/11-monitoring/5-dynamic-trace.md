## 27.5. Rastreamento Dinâmico [#](#DYNAMIC-TRACE)

* [27.5.1. Compilando para Rastreamento Dinâmico][(dynamic-trace.md#COMPILING-FOR-TRACE)
* [27.5.2. Sondas Integradas][(dynamic-trace.md#TRACE-POINTS)
* [27.5.3. Usando Sondas][(dynamic-trace.md#USING-TRACE-POINTS)
* [27.5.4. Definindo Novas Sondas][(dynamic-trace.md#DEFINING-TRACE-POINTS)

O PostgreSQL oferece recursos para suportar o rastreamento dinâmico do servidor de banco de dados. Isso permite que uma ferramenta externa seja chamada em pontos específicos do código e, assim, rastreie a execução.

Vários pontos de sondagem ou pontos de rastreamento já estão inseridos no código-fonte. Esses pontos de sondagem são destinados a serem utilizados por desenvolvedores e administradores de banco de dados. Por padrão, os pontos de sondagem não são compilados no PostgreSQL; o usuário precisa informar explicitamente ao script de configuração para tornar os pontos de sondagem disponíveis.

Atualmente, o utilitário [DTrace](https://en.wikipedia.org/wiki/DTrace) é suportado, que, no momento da escrita deste texto, está disponível em Solaris, macOS, FreeBSD, NetBSD e Oracle Linux. O projeto [SystemTap](https://sourceware.org/systemtap/) para Linux fornece um equivalente ao DTrace e também pode ser usado. Supor a outros utilitários de rastreamento dinâmico é teoricamente possível, alterando as definições para as macros em `src/include/utils/probes.h`.

### 27.5.1. Compilação para Rastreamento Dinâmico [#](#COMPILING-FOR-TRACE)

Por padrão, as sondas não estão disponíveis, então você precisará informar explicitamente ao script de configuração para tornar as sondas disponíveis no PostgreSQL. Para incluir o suporte ao DTrace, especifique `--enable-dtrace` para configurar. Consulte [Seção 17.3.3.6](install-make.md#CONFIGURE-OPTIONS-DEVEL) para obter mais informações.

### 27.5.2. Sensores integrados [#](#TRACE-POINTS)

Vários sondas padrão são fornecidos no código-fonte, conforme mostrado em [Tabela 27.49](dynamic-trace.md#DTRACE-PROBE-POINT-TABLE); [Tabela 27.50](dynamic-trace.md#TYPEDEFS-TABLE) mostra os tipos utilizados nas sondas. Mais sondas podem certamente ser adicionadas para melhorar a observabilidade do PostgreSQL.

**Tabela 27.49. Sondas DTrace integradas**



<table>
 <colgroup>
  <col class="col1"/>
  <col class="col2"/>
  <col class="col3"/>
 </colgroup>
 <thead>
  <tr>
   <th>
    Name
   </th>
   <th>
    Parâmetros
   </th>
   <th>
    Descrição
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <code>
     transaction-start
    </code>
   </td>
   <td>
    <code>
     (LocalTransactionId)
    </code>
   </td>
   <td>
    Probe que é acionada no início de uma nova transação.  arg0 é o ID da transação.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     transaction-commit
    </code>
   </td>
   <td>
    <code>
     (LocalTransactionId)
    </code>
   </td>
   <td>
    Probe que acende quando uma transação é concluída com sucesso. arg0 é o ID da transação.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     transaction-abort
    </code>
   </td>
   <td>
    <code>
     (LocalTransactionId)
    </code>
   </td>
   <td>
    Prova que acende quando uma transação é concluída com sucesso. arg0 é o ID da transação.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     query-start
    </code>
   </td>
   <td>
    <code>
     (const char *)
    </code>
   </td>
   <td>
    Probe que acende quando o processamento de uma consulta é iniciado. arg0 é a string de consulta.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     query-done
    </code>
   </td>
   <td>
    <code>
     (const char *)
    </code>
   </td>
   <td>
    Probe que acende quando o processamento de uma consulta está concluído. arg0 é a string de consulta.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     query-parse-start
    </code>
   </td>
   <td>
    <code>
     (const char *)
    </code>
   </td>
   <td>
    Probe que acende quando a análise de uma consulta é iniciada. arg0 é a string de consulta.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     query-parse-done
    </code>
   </td>
   <td>
    <code>
     (const char *)
    </code>
   </td>
   <td>
    Probe que acende quando a análise de uma consulta está completa. arg0 é a string de consulta.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     query-rewrite-start
    </code>
   </td>
   <td>
    <code>
     (const char *)
    </code>
   </td>
   <td>
    Probe que acende quando a reescrita de uma consulta é iniciada. arg0 é a string de consulta.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     query-rewrite-done
    </code>
   </td>
   <td>
    <code>
     (const char *)
    </code>
   </td>
   <td>
    Probe que acende quando a reescrita de uma consulta está completa. arg0 é a string de consulta.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     query-plan-start
    </code>
   </td>
   <td>
    <code>
     ()
    </code>
   </td>
   <td>
    Probe que acende quando o planejamento de uma consulta é iniciado.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     query-plan-done
    </code>
   </td>
   <td>
    <code>
     ()
    </code>
   </td>
   <td>
    Probe que acende quando o planejamento de uma consulta está completo.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     query-execute-start
    </code>
   </td>
   <td>
    <code>
     ()
    </code>
   </td>
   <td>
    Probe que acende quando a execução de uma consulta é iniciada.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     query-execute-done
    </code>
   </td>
   <td>
    <code>
     ()
    </code>
   </td>
   <td>
    Probe que acende quando a execução de uma consulta é concluída.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     statement-status
    </code>
   </td>
   <td>
    <code>
     (const char *)
    </code>
   </td>
   <td>
    Probe que acende sempre que o processo do servidor atualiza
    <code>
     pg_stat_activity
    </code>
    .
    <code>
     status
    </code>
    .  arg0 é a nova string de status.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     checkpoint-start
    </code>
   </td>
   <td>
    <code>
     (int)
    </code>
   </td>
   <td>
    Prova que acende quando um ponto de verificação é iniciado. arg0 contém as flags binárias usadas para distinguir diferentes tipos de ponto de verificação, como desligamento, imediato ou força.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     checkpoint-done
    </code>
   </td>
   <td>
    <code>
     (int, int, int, int, int)
    </code>
   </td>
   <td>
    Sensores que acendem quando um ponto de verificação é concluído. (Os sensores listados a seguir acendem em sequência durante o processamento do ponto de verificação.) arg0 é o número de buffers escritos. arg1 é o número total de buffers. arg2, arg3 e arg4 contêm o número de arquivos WAL adicionados, removidos e reciclados, respectivamente.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     clog-checkpoint-start
    </code>
   </td>
   <td>
    <code>
     (bool)
    </code>
   </td>
   <td>
    Prova que acende quando a porção CLOG de um ponto de verificação é iniciada. arg0 é verdadeiro para o ponto de verificação normal, falso para o ponto de verificação de desligamento.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     clog-checkpoint-done
    </code>
   </td>
   <td>
    <code>
     (bool)
    </code>
   </td>
   <td>
    Prova que acende quando a porção CLOG de um ponto de verificação é concluída. arg0 tem o mesmo significado que para
    <code>
     clog-checkpoint-start
    </code>
    .
   </td>
  </tr>
  <tr>
   <td>
    <code>
     subtrans-checkpoint-start
    </code>
   </td>
   <td>
    <code>
     (bool)
    </code>
   </td>
   <td>
    Prova que acende quando a porção SUBTRANS de um ponto de verificação é iniciada. arg0 é verdadeiro para o ponto de verificação normal, falso para o ponto de verificação de desligamento.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     subtrans-checkpoint-done
    </code>
   </td>
   <td>
    <code>
     (bool)
    </code>
   </td>
   <td>
    Prova que acende quando a parte SUBTRANS de um ponto de verificação é concluída. arg0 tem o mesmo significado que para
    <code>
     subtrans-checkpoint-start
    </code>
    .
   </td>
  </tr>
  <tr>
   <td>
    <code>
     multixact-checkpoint-start
    </code>
   </td>
   <td>
    <code>
     (bool)
    </code>
   </td>
   <td>
    Prova que acende quando a porção MultiXact de um ponto de verificação é iniciada. arg0 é verdadeiro para o ponto de verificação normal, falso para o ponto de verificação de desligamento.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     multixact-checkpoint-done
    </code>
   </td>
   <td>
    <code>
     (bool)
    </code>
   </td>
   <td>
    Prova que acende quando a porção MultiXact de um ponto de verificação é concluída. arg0 tem o mesmo significado que para
    <code>
     multixact-checkpoint-start
    </code>
    .
   </td>
  </tr>
  <tr>
   <td>
    <code>
     buffer-checkpoint-start
    </code>
   </td>
   <td>
    <code>
     (int)
    </code>
   </td>
   <td>
    Probe que acende quando a parte de escrita de buffer de um ponto de verificação é iniciada. arg0 contém as flags binárias usadas para distinguir diferentes tipos de ponto de verificação, como desligamento, imediato ou força.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     buffer-sync-start
    </code>
   </td>
   <td>
    <code>
     (int, int)
    </code>
   </td>
   <td>
    Probe que acende quando começamos a escrever buffers sujos durante o ponto de verificação (após identificar quais buffers devem ser escritos). arg0 é o número total de buffers. arg1 é o número que atualmente está sujo e precisa ser escrito.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     buffer-sync-written
    </code>
   </td>
   <td>
    <code>
     (int)
    </code>
   </td>
   <td>
    Probe que acende após cada buffer ser escrito durante o ponto de verificação. arg0 é o número de identificação do buffer.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     buffer-sync-done
    </code>
   </td>
   <td>
    <code>
     (int, int, int)
    </code>
   </td>
   <td>
    Prova que acende quando todos os buffers sujos foram escritos. arg0 é o número total de buffers. arg1 é o número de buffers que realmente foram escritos pelo processo de verificação. arg2 é o número que se esperava que fossem escritos (arg1 de
    <code>
     buffer-sync-start
    </code>
    ); qualquer diferença reflete outros processos que limpem os buffers durante o ponto de verificação.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     buffer-checkpoint-sync-start
    </code>
   </td>
   <td>
    <code>
     ()
    </code>
   </td>
   <td>
    Prova que é acionada após buffers sujos terem sido escritos no kernel e antes de começar a emitir solicitações de fsync.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     buffer-checkpoint-done
    </code>
   </td>
   <td>
    <code>
     ()
    </code>
   </td>
   <td>
    Prova que acende quando a sincronização dos buffers no disco é concluída.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     twophase-checkpoint-start
    </code>
   </td>
   <td>
    <code>
     ()
    </code>
   </td>
   <td>
    Prova que acende quando a porção bifásica de um ponto de verificação é iniciada.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     twophase-checkpoint-done
    </code>
   </td>
   <td>
    <code>
     ()
    </code>
   </td>
   <td>
    Prova que acende quando a porção bifásica de um ponto de verificação está completa.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     buffer-extend-start
    </code>
   </td>
   <td>
    <code>
     (ForkNumber, BlockNumber, Oid, Oid, Oid, int, unsigned int)
    </code>
   </td>
   <td>
    A sonda que acende quando uma extensão de relação é iniciada. arg0 contém o fork a ser estendido. arg1, arg2 e arg3 contêm os OIDs do espaço de tabela, banco de dados e relação que identificam a relação. arg4 é o ID do backend que criou a relação temporária para um buffer local, ou
    <code>
     INVALID_PROC_NUMBER
    </code>
    (-1) para um buffer compartilhado. arg5 é o número de blocos que o chamador gostaria de estender.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     buffer-extend-done
    </code>
   </td>
   <td>
    <code>
     (ForkNumber, BlockNumber, Oid, Oid, Oid, int, unsigned int, BlockNumber)
    </code>
   </td>
   <td>
    Probe que acende quando uma extensão de relação é concluída. arg0 contém o fork a ser estendido. arg1, arg2 e arg3 contêm os OIDs do espaço de tabela, banco de dados e relação que identificam a relação. arg4 é o ID do backend que criou a relação temporária para um buffer local, ou
    <code>
     INVALID_PROC_NUMBER
    </code>
    (-1) para um buffer compartilhado. arg5 é o número de blocos pelo qual a relação foi estendida, que pode ser menor que o número no
    <code>
     buffer-extend-start
    </code>
    devido a restrições de recursos. arg6 contém o número de bloco do primeiro novo bloco.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     buffer-read-start
    </code>
   </td>
   <td>
    <code>
     (ForkNumber, BlockNumber, Oid, Oid, Oid, int)
    </code>
   </td>
   <td>
    Probe que acende quando uma leitura de buffer é iniciada. arg0 e arg1 contêm os números de bifurcação e bloqueio da página. arg2, arg3 e arg4 contêm os OIDs do tablespace, banco de dados e relação que identificam a relação. arg5 é o ID do backend que criou a relação temporária para um buffer local, ou
    <code>
     INVALID_PROC_NUMBER
    </code>
    (-1) para um buffer compartilhado.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     buffer-read-done
    </code>
   </td>
   <td>
    <code>
     (ForkNumber, BlockNumber, Oid, Oid, Oid, int, bool)
    </code>
   </td>
   <td>
    Probe que acende quando uma leitura de buffer é concluída.  arg0 e arg1 contêm os números de bifurcação e bloqueio da página. arg2, arg3 e arg4 contêm os OIDs do tablespace, banco de dados e relação que identificam a relação. arg5 é o ID do backend que criou a relação temporária para um buffer local, ou
    <code>
     INVALID_PROC_NUMBER
    </code>
    (-1) para um buffer compartilhado. arg6 é verdadeiro se o buffer foi encontrado no pool, falso se
   </td>
  </tr>
  <tr>
   <td>
    <code>
     buffer-flush-start
    </code>
   </td>
   <td>
    <code>
     (ForkNumber, BlockNumber, Oid, Oid, Oid)
    </code>
   </td>
   <td>
    Probe que acende antes de emitir qualquer solicitação de escrita para um buffer compartilhado. arg0 e arg1 contêm os números de bifurcação e bloqueio da página. arg2, arg3 e arg4 contêm as tabelaspace, banco de dados e OIDs de relação que identificam a relação.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     buffer-flush-done
    </code>
   </td>
   <td>
    <code>
     (ForkNumber, BlockNumber, Oid, Oid, Oid)
    </code>
   </td>
   <td>
    Probe que acende quando um pedido de escrita está concluído. (Observe que isso apenas reflete o tempo para passar os dados para o kernel; normalmente, eles ainda não foram escritos no disco.) Os argumentos são os mesmos que para
    <code>
     buffer-flush-start
    </code>
    .
   </td>
  </tr>
  <tr>
   <td>
    <code>
     wal-buffer-write-dirty-start
    </code>
   </td>
   <td>
    <code>
     ()
    </code>
   </td>
   <td>
    Probe que acende quando um processo do servidor começa a escrever um buffer WAL sujo, porque não há mais espaço disponível para o buffer WAL. (Se isso acontece com frequência, isso implica que
    <a class="xref" href="runtime-config-wal.md#GUC-WAL-BUFFERS">
     wal_buffers
    </a>
    é muito pequeno.)
   </td>
  </tr>
  <tr>
   <td>
    <code>
     wal-buffer-write-dirty-done
    </code>
   </td>
   <td>
    <code>
     ()
    </code>
   </td>
   <td>
    Probe que acende quando uma escrita de buffer WAL sujo é concluída.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     wal-insert
    </code>
   </td>
   <td>
    <code>
     (unsigned char, unsigned char)
    </code>
   </td>
   <td>
    Probe que acende quando um registro WAL é inserido.  arg0 é o gerenciador de recursos (rmid) para o registro. arg1 contém as flags de informação.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     wal-switch
    </code>
   </td>
   <td>
    <code>
     ()
    </code>
   </td>
   <td>
    Probe que acende quando é solicitado um interruptor de segmento WAL.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     smgr-md-read-start
    </code>
   </td>
   <td>
    <code>
     (ForkNumber, BlockNumber, Oid, Oid, Oid, int)
    </code>
   </td>
   <td>
    Probe que acende quando começa a ler um bloco de uma relação. arg0 e arg1 contêm os números de bifurcação e bloco da página. arg2, arg3 e arg4 contêm os OIDs do tablespace, banco de dados e relação que identificam a relação. arg5 é o ID do backend que criou a relação temporária para um buffer local, ou
    <code>
     INVALID_PROC_NUMBER
    </code>
    (-1) para um buffer compartilhado.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     smgr-md-read-done
    </code>
   </td>
   <td>
    <code>
     (ForkNumber, BlockNumber, Oid, Oid, Oid, int, int, int)
    </code>
   </td>
   <td>
    Probe que acende quando uma leitura de bloco é concluída. arg0 e arg1 contêm os números de bifurcação e bloco da página. arg2, arg3 e arg4 contêm os OIDs do tablespace, banco de dados e relação que identificam a relação. arg5 é o ID do backend que criou a relação temporária para um buffer local, ou
    <code>
     INVALID_PROC_NUMBER
    </code>
    (-1) para um buffer compartilhado. arg6 é o número de bytes realmente lidos, enquanto arg7 é o número solicitado (se esses forem diferentes, isso indica uma leitura curta).
   </td>
  </tr>
  <tr>
   <td>
    <code>
     smgr-md-write-start
    </code>
   </td>
   <td>
    <code>
     (ForkNumber, BlockNumber, Oid, Oid, Oid, int)
    </code>
   </td>
   <td>
    Probe que acende quando começa a escrever um bloco em uma relação. arg0 e arg1 contêm os números de bifurcação e bloqueio da página. arg2, arg3 e arg4 contêm os OIDs do tablespace, banco de dados e relação que identificam a relação. arg5 é o ID do backend que criou a relação temporária para um buffer local, ou
    <code>
     INVALID_PROC_NUMBER
    </code>
    (-1) para um buffer compartilhado.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     smgr-md-write-done
    </code>
   </td>
   <td>
    <code>
     (ForkNumber, BlockNumber, Oid, Oid, Oid, int, int, int)
    </code>
   </td>
   <td>
    Probe que acende quando uma escrita de bloco é concluída. arg0 e arg1 contêm os números de bifurcação e bloco da página. arg2, arg3 e arg4 contêm os OIDs do tablespace, banco de dados e relação que identificam a relação. arg5 é o ID do backend que criou a relação temporária para um buffer local, ou
    <code>
     INVALID_PROC_NUMBER
    </code>
    (-1) para um buffer compartilhado. arg6 é o número de bytes realmente escritos, enquanto arg7 é o número solicitado (se esses forem diferentes, isso indica uma escrita curta).
   </td>
  </tr>
  <tr>
   <td>
    <code>
     sort-start
    </code>
   </td>
   <td>
    <code>
     (int, bool, int, int, bool, int)
    </code>
   </td>
   <td>
    Probe que acende quando uma operação de classificação é iniciada. arg0 indica heap, índice ou classificação de dados. arg1 é verdadeiro para a aplicação de valores únicos. arg2 é o número de colunas chave. arg3 é o número de kilobytes de memória de trabalho permitidos. arg4 é verdadeiro se o acesso aleatório ao resultado da classificação é necessário. arg5 indica serial quando
    <code>
     0
    </code>
    , trabalhador paralelo quando
    <code>
     1
    </code>
    , ou líder paralelo quando
    <code>
     2
    </code>
    .
   </td>
  </tr>
  <tr>
   <td>
    <code>
     sort-done
    </code>
   </td>
   <td>
    <code>
     (bool, long)
    </code>
   </td>
   <td>
    Probe que acende quando uma classificação está completa.  arg0 é verdadeiro para classificação externa, falso para classificação interna. arg1 é o número de blocos de disco utilizados para uma classificação externa, ou kilobytes de memória utilizados para uma classificação interna.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     lwlock-acquire
    </code>
   </td>
   <td>
    <code>
     (char *, LWLockMode)
    </code>
   </td>
   <td>
    Probe que acende quando uma LWLock foi adquirida. arg0 é a fração da LWLock. arg1 é o modo de bloqueio solicitado, exclusivo ou compartilhado.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     lwlock-release
    </code>
   </td>
   <td>
    <code>
     (char *)
    </code>
   </td>
   <td>
    Probe que acende quando um LWLock é liberado (mas observe que quaisquer atendentes liberados ainda não foram despertados). arg0 é a faixa do LWLock.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     lwlock-wait-start
    </code>
   </td>
   <td>
    <code>
     (char *, LWLockMode)
    </code>
   </td>
   <td>
    Probe que acende quando um LWLock não estava imediatamente disponível e um processo do servidor começou a esperar que o bloqueio se tornasse disponível. arg0 é a fração do LWLock. arg1 é o modo de bloqueio solicitado, exclusivo ou compartilhado.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     lwlock-wait-done
    </code>
   </td>
   <td>
    <code>
     (char *, LWLockMode)
    </code>
   </td>
   <td>
    Probe que acende quando um processo do servidor é liberado de sua espera por um LWLock (na verdade, ele não possui o bloqueio ainda). arg0 é a fração do LWLock. arg1 é o modo de bloqueio solicitado, exclusivo ou compartilhado.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     lwlock-condacquire
    </code>
   </td>
   <td>
    <code>
     (char *, LWLockMode)
    </code>
   </td>
   <td>
    Probe que acende quando uma LWLock é adquirida com sucesso quando o chamador não especificou espera. arg0 é a fração da LWLock. arg1 é o modo de bloqueio solicitado, exclusivo ou compartilhado.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     lwlock-condacquire-fail
    </code>
   </td>
   <td>
    <code>
     (char *, LWLockMode)
    </code>
   </td>
   <td>
    Probe que acende quando um LWLock não foi adquirido com sucesso quando o chamador não especificou espera. arg0 é a fração do LWLock. arg1 é o modo de bloqueio solicitado, exclusivo ou compartilhado.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     lock-wait-start
    </code>
   </td>
   <td>
    <code>
     (unsigned int, unsigned int, unsigned int, unsigned int, unsigned int, LOCKMODE)
    </code>
   </td>
   <td>
    O probe que acende quando um pedido de bloqueio de peso pesado (bloqueio lmgr) começa a esperar porque o bloqueio não está disponível. arg0 a arg3 são os campos de identificação da etiqueta do objeto que está sendo bloqueado. arg4 indica o tipo de objeto que está sendo bloqueado. arg5 indica o tipo de bloqueio solicitado.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     lock-wait-done
    </code>
   </td>
   <td>
    <code>
     (unsigned int, unsigned int, unsigned int, unsigned int, unsigned int, LOCKMODE)
    </code>
   </td>
   <td>
    Probe que acende quando um pedido de bloqueio de peso pesado (bloqueio lmgr) termina de esperar (ou seja, adquiriu o bloqueio). Os argumentos são os mesmos que para
    <code>
     lock-wait-start
    </code>
    .
   </td>
  </tr>
  <tr>
   <td>
    <code>
     deadlock-found
    </code>
   </td>
   <td>
    <code>
     ()
    </code>
   </td>
   <td>
    Probe que acende quando um bloqueio é encontrado pelo detector de bloqueio.
   </td>
  </tr>
 </tbody>
</table>










**Tabela 27.50. Tipos Definidos Usados nos Parâmetros de Sondagem**



<table>
 <thead>
  <tr>
   <th>
    Type
   </th>
   <th>
    Definition
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <code>
     LocalTransactionId
    </code>
   </td>
   <td>
    <code>
     unsigned int
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     LWLockMode
    </code>
   </td>
   <td>
    <code>
     int
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     LOCKMODE
    </code>
   </td>
   <td>
    <code>
     int
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     BlockNumber
    </code>
   </td>
   <td>
    <code>
     unsigned int
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     Oid
    </code>
   </td>
   <td>
    <code>
     unsigned int
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     ForkNumber
    </code>
   </td>
   <td>
    <code>
     int
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     bool
    </code>
   </td>
   <td>
    <code>
     unsigned char
    </code>
   </td>
  </tr>
 </tbody>
</table>







### 27.5.3. Uso de sondas [#](#USING-TRACE-POINTS)

O exemplo abaixo mostra um script DTrace para analisar o número de transações no sistema, como alternativa ao uso do snapshot `pg_stat_database` antes e depois de um teste de desempenho:

```
#!/usr/sbin/dtrace -qs

postgresql$1:::transaction-start
{
      @start["Start"] = count();
      self->ts  = timestamp;
}

postgresql$1:::transaction-abort
{
      @abort["Abort"] = count();
}

postgresql$1:::transaction-commit
/self->ts/
{
      @commit["Commit"] = count();
      @time["Total time (ns)"] = sum(timestamp - self->ts);
      self->ts=0;
}
```

Quando executado, o script exemplo D gera uma saída como:

```
# ./txn_count.d `pgrep -n postgres` or ./txn_count.d <PID>
^C

Start                                          71
Commit                                         70
Total time (ns)                        2312105013
```

Nota

O SystemTap utiliza uma notação diferente para scripts de rastreamento em comparação com o DTrace, embora os pontos de rastreamento subjacentes sejam compatíveis. Um ponto que vale a pena notar é que, neste texto, os scripts do SystemTap devem referenciar os nomes dos sondas usando dois underscores em vez de hífens. Espera-se que isso seja corrigido em futuras versões do SystemTap.

Você deve lembrar que os scripts do DTrace precisam ser cuidadosamente escritos e depurados, caso contrário, as informações coletadas podem não ter significado. Na maioria dos casos em que problemas são encontrados, é a instrumentação que está errada, não o sistema subjacente. Ao discutir as informações encontradas usando o rastreamento dinâmico, certifique-se de incluir o script usado para permitir que isso também seja verificado e discutido.

### 27.5.4. Definindo Novas Sensores [#](#DEFINING-TRACE-POINTS)

Novos sensores podem ser definidos dentro do código onde o desenvolvedor desejar, embora isso exija uma recompilação. Abaixo estão os passos para inserir novos sensores:

1. Decida sobre os nomes dos sensores e os dados que serão disponibilizados através dos sensores.
2. Adicione as definições dos sensores ao `src/backend/utils/probes.d`
3. Inclua `pg_trace.h` se não estiver já presente no módulo (s) que contém os pontos de sensor, e insira as macros dos sensores `TRACE_POSTGRESQL` nos locais desejados no código-fonte.
4. Reconecte e verifique se os novos sensores estão disponíveis.

**Exemplo:** Aqui está um exemplo de como você adicionaria uma sonda para rastrear todas as novas transações pelo ID de transação.

1. Decidir que a sonda será chamada de `transaction-start` e requer um parâmetro do tipo `LocalTransactionId`
2. Adicionar a definição da sonda a `src/backend/utils/probes.d`:

```
probe transaction__start(LocalTransactionId);
```

Observe o uso do duplo underline no nome da sonda. Em um script DTrace que utiliza a sonda, o duplo underline precisa ser substituído por um hífen, então `transaction-start` é o nome a ser documentado para os usuários.
3. No momento da compilação, `transaction__start` é convertido em uma macro chamada `TRACE_POSTGRESQL_TRANSACTION_START` (observe que os underscores são únicos aqui), que está disponível incluindo `pg_trace.h`. Adicione a chamada de macro ao local apropriado no código-fonte. Neste caso, parece o seguinte:

4. Após recompilar e executar o novo binário, verifique se a sonda recém-adicionada está disponível, executando o seguinte comando DTrace. Você deve ver uma saída semelhante:

```
# dtrace -ln transaction-start
   ID    PROVIDER          MODULE           FUNCTION NAME
18705 postgresql49878     postgres     StartTransactionCommand transaction-start
18755 postgresql49877     postgres     StartTransactionCommand transaction-start
18805 postgresql49876     postgres     StartTransactionCommand transaction-start
18855 postgresql49875     postgres     StartTransactionCommand transaction-start
18986 postgresql49873     postgres     StartTransactionCommand transaction-start
```

Há algumas coisas a serem cuidadas ao adicionar macros de rastreamento ao código C:

* Você deve se certificar de que os tipos de dados especificados para os parâmetros de uma sonda correspondem aos tipos de dados das variáveis usadas na macro. Caso contrário, você receberá erros de compilação.
* Na maioria das plataformas, se o PostgreSQL for construído com `--enable-dtrace`, os argumentos de uma macro de rastreamento serão avaliados sempre que o controle passar pela macro, * mesmo que não esteja sendo feito rastreamento *. Isso geralmente não vale a pena se você está apenas relatando os valores de algumas variáveis locais. Mas cuidado ao colocar chamadas de função caras nos argumentos. Se você precisar fazer isso, considere proteger a macro com uma verificação para ver se o rastreamento está realmente habilitado:

```
if (TRACE_POSTGRESQL_TRANSACTION_START_ENABLED())
    TRACE_POSTGRESQL_TRANSACTION_START(some_function(...));
```

Cada macro de rastreamento tem uma macro correspondente `ENABLED`.