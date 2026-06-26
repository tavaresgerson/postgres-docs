## 19.5. Registro de escrita antecipada [#](#RUNTIME-CONFIG-WAL)

* [19.5.1. Configurações](runtime-config-wal.md#RUNTIME-CONFIG-WAL-SETTINGS)
* [19.5.2. Pontos de verificação](runtime-config-wal.md#RUNTIME-CONFIG-WAL-CHECKPOINTS)
* [19.5.3. Arquivamento](runtime-config-wal.md#RUNTIME-CONFIG-WAL-ARCHIVING)
* [19.5.4. Recuperação](runtime-config-wal.md#RUNTIME-CONFIG-WAL-RECOVERY)
* [19.5.5. Recuperação de arquivo](runtime-config-wal.md#RUNTIME-CONFIG-WAL-ARCHIVE-RECOVERY)
* [19.5.6. Alvo de recuperação](runtime-config-wal.md#RUNTIME-CONFIG-WAL-RECOVERY-TARGET)
* [19.5.7. Resumo WAL](runtime-config-wal.md#RUNTIME-CONFIG-WAL-SUMMARIZATION)

Para informações adicionais sobre o ajuste dessas configurações, consulte [Seção 28.5](wal-configuration.md).

### 19.5.1. Configurações [#](#RUNTIME-CONFIG-WAL-SETTINGS)

`wal_level` (`enum`) [#](#GUC-WAL-LEVEL): `wal_level` determina quanto de informação é escrito para o WAL. O valor padrão é `replica`, que escreve dados suficientes para suportar a arquivamento e replicação do WAL, incluindo a execução de consultas somente de leitura em um servidor de espera. `minimal` remove toda a logagem, exceto as informações necessárias para recuperar de um acidente ou desligamento imediato. Finalmente, `logical` adiciona informações necessárias para suportar a decodificação lógica. Cada nível inclui as informações registradas em todos os níveis inferiores. Este parâmetro só pode ser definido no início do servidor.

O nível `minimal` gera o menor volume de WAL. Ele não registra nenhuma informação de linha para relações permanentes em transações que as criam ou as reescrevem. Isso pode tornar as operações muito mais rápidas (consulte [Seção 14.4.7](populate.md#POPULATE-PITR)). As operações que iniciam essa otimização incluem:



<table>
 <tr>
  <td>
   <code>
    ALTER ... SET TABLESPACE
   </code>
  </td>
 </tr>
 <tr>
  <td>
   <code>
    CLUSTER
   </code>
  </td>
 </tr>
 <tr>
  <td>
   <code>
    CREATE TABLE
   </code>
  </td>
 </tr>
 <tr>
  <td>
   <code>
    REFRESH MATERIALIZED VIEW
   </code>
   (sem
   <code>
    CONCURRENTLY
   </code>
   )
  </td>
 </tr>
 <tr>
  <td>
   <code>
    REINDEX
   </code>
  </td>
 </tr>
 <tr>
  <td>
   <code>
    TRUNCATE
   </code>
  </td>
 </tr>
</table>







No entanto, o WAL mínimo não contém informações suficientes para recuperação em ponto no tempo, então `replica` ou superior deve ser usado para habilitar o arquivamento contínuo ([archive_mode](runtime-config-wal.md#GUC-ARCHIVE-MODE)) e a replicação binária em streaming. De fato, o servidor não iniciará sequer nesse modo se `max_wal_senders` não for zero. Note que alterar `wal_level` para `minimal` torna os backups anteriores da base inutilizáveis para recuperação em ponto no tempo e servidores de standby.

No nível `logical`, as mesmas informações são registradas como com `replica`, além das informações necessárias para extrair conjuntos de alterações lógicas do WAL. O uso de um nível de `logical` aumentará o volume do WAL, especialmente se muitas tabelas forem configuradas para `REPLICA IDENTITY FULL` e muitas declarações de `UPDATE` e `DELETE` forem executadas.

Em versões anteriores à 9.6, este parâmetro também permitia os valores `archive` e `hot_standby`. Esses valores ainda são aceitos, mas são mapeados para `replica`.

`fsync` (`boolean`) [#](#GUC-FSYNC): Se este parâmetro estiver ativado, o servidor PostgreSQL tentará garantir que as atualizações sejam escritas fisicamente no disco, emitindo chamadas de sistema `fsync()` ou vários métodos equivalentes (consulte [wal_sync_method](runtime-config-wal.md#GUC-WAL-SYNC-METHOD)). Isso garante que o grupo de bancos de dados possa se recuperar a um estado consistente após um acidente no sistema operacional ou no hardware.

Embora a desativação de `fsync` seja frequentemente uma vantagem em termos de desempenho, isso pode resultar em corrupção de dados irrecuperável em caso de falha de energia ou falha do sistema. Assim, só é aconselhável desativar `fsync` se você puder facilmente recriar todo o seu banco de dados a partir de dados externos.

Exemplos de circunstâncias seguras para desativar `fsync` incluem o carregamento inicial de um novo grupo de bancos de dados a partir de um arquivo de backup, usando um grupo de bancos de dados para processar um lote de dados, após o qual o banco de dados será descartado e recriado, ou para um clone de banco de dados somente de leitura que é frequentemente recriado e não é usado para falha de sobrevivência. O hardware de alta qualidade por si só não é uma justificativa suficiente para desativar `fsync`.

Para uma recuperação confiável ao mudar `fsync` de desligado para ligado, é necessário forçar todos os buffers modificados no kernel para armazenamento durável. Isso pode ser feito enquanto o clúster está desligado ou enquanto `fsync` está ligado, executando `initdb --sync-only`, executando `sync`, desmontando o sistema de arquivos ou reiniciando o servidor.

Em muitas situações, desligar [synchronous_commit](runtime-config-wal.md#GUC-SYNCHRONOUS-COMMIT) para transações não críticas pode oferecer muitos dos benefícios de desempenho potencial de desligar [`fsync`], sem os riscos associados à corrupção de dados.

`fsync` só pode ser definido no arquivo `postgresql.conf` ou na linha de comando do servidor. Se você desativar este parâmetro, também considere desativar [full_page_writes](runtime-config-wal.md#GUC-FULL-PAGE-WRITES).

`synchronous_commit` (`enum`) [#](#GUC-SYNCHRONOUS-COMMIT): Especifica quanto processamento do WAL deve ser concluído antes que o servidor de banco de dados retorne uma indicação de “sucesso” ao cliente. Os valores válidos são `remote_apply`, `on` (o padrão), `remote_write`, `local` e `off`.

Se `synchronous_standby_names` estiver vazio, os únicos ajustes significativos são `on` e `off`; `remote_apply`, `remote_write` e `local` fornecem o mesmo nível de sincronização local que `on`. O comportamento local de todos os modos que não são `off` é esperar pelo apagamento local do WAL no disco. No modo `off`, não há espera, então pode haver um atraso entre o momento em que o sucesso é relatado ao cliente e quando a transação é posteriormente garantida como segura contra um crash do servidor. (O atraso máximo é três vezes [wal_writer_delay](runtime-config-wal.md#GUC-WAL-WRITER-DELAY).). Ao contrário de [fsync](runtime-config-wal.md#GUC-FSYNC), definir este parâmetro para `off` não cria nenhum risco de inconsistência no banco de dados: um crash do sistema operacional ou do banco de dados pode resultar na perda de algumas transações supostamente comprometidas, mas o estado do banco de dados será exatamente o mesmo como se essas transações tivessem sido abortadas de forma limpa. Portanto, desativar `synchronous_commit` pode ser uma alternativa útil quando o desempenho é mais importante do que a certeza exata sobre a durabilidade de uma transação. Para mais discussão, veja [Seção 28.4](wal-async-commit.md).

Se [synchronous_standby_names](runtime-config-replication.md#GUC-SYNCHRONOUS-STANDBY-NAMES) não estiver vazio, `synchronous_commit` também controla se os commits de transação irão esperar que seus registros WAL sejam processados no(s) servidor(es) de standby.

Quando configurado em `remote_apply`, os compromissos aguardam até que as respostas dos standby(s) síncronos atuais indiquem que receberam o registro de compromisso da transação e o aplicaram, de modo que ele se torne visível para consultas nos(s) standby(s), e também escrito em armazenamento durável nos(s) standby(s). Isso causará atrasos muito maiores nos compromissos do que as configurações anteriores, pois espera pela reprodução da WAL. Quando configurado em `on`, os compromissos aguardam até que as respostas dos standby(s) síncronos atuais indiquem que receberam o registro de compromisso da transação e o descarregaram em armazenamento durável. Isso garante que a transação não será perdida, a menos que tanto o principal quanto todos os standby(s) síncronos sofram corrupção de seu armazenamento de banco de dados. Quando configurado em `remote_write`, os compromissos aguardam até que as respostas dos standby(s) síncronos atuais indiquem que receberam o registro de compromisso da transação e o escreveram em seus sistemas de arquivos. Esta configuração garante a preservação dos dados se uma instância de standby do PostgreSQL falhar, mas não se a instância de standby sofrer um falha de nível operacional porque os dados não necessariamente atingiram o armazenamento durável no standby. A configuração `local` faz com que os compromissos esperem pelo descarregamento local no disco, mas não para replicação. Isso geralmente não é desejável quando a replicação síncrona está em uso, mas é fornecido por completo.

Este parâmetro pode ser alterado a qualquer momento; o comportamento de qualquer transação é determinado pelo ajuste em vigor quando ela é confirmada. Portanto, é possível e útil ter algumas transações confirmadas de forma sincrona e outras de forma assíncrona. Por exemplo, para fazer com que uma única transação com múltiplos comandos seja confirmada de forma assíncrona quando o padrão é o oposto, emita `SET LOCAL synchronous_commit TO OFF` dentro da transação.

[Tabela 19.1](runtime-config-wal.md#SYNCHRONOUS-COMMIT-MATRIX "Table 19.1. synchronous_commit Modes") resume as capacidades das configurações do `synchronous_commit`.

**Tabela 19.1. Modos de sincronização_commit**



<table>
 <colgroup>
  <col class="col1"/>
  <col class="col2"/>
  <col class="col3"/>
  <col class="col4"/>
  <col class="col5"/>
 </colgroup>
 <thead>
  <tr>
   <th>
    synchronous_commit setting
   </th>
   <th>
    local durable commit
   </th>
   <th>
    standby durable commit after PG crash
   </th>
   <th>
    commit durável de espera após o crash do sistema operacional
   </th>
   <th>
    standby query consistency
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    remote_apply
   </td>
   <td align="center">
    •
   </td>
   <td align="center">
    •
   </td>
   <td align="center">
    •
   </td>
   <td align="center">
    •
   </td>
  </tr>
  <tr>
   <td>
    on
   </td>
   <td align="center">
    •
   </td>
   <td align="center">
    •
   </td>
   <td align="center">
    •
   </td>
   <td align="center">
   </td>
  </tr>
  <tr>
   <td>
    remote_write
   </td>
   <td align="center">
    •
   </td>
   <td align="center">
    •
   </td>
   <td align="center">
   </td>
   <td align="center">
   </td>
  </tr>
  <tr>
   <td>
    local
   </td>
   <td align="center">
    •
   </td>
   <td align="center">
   </td>
   <td align="center">
   </td>
   <td align="center">
   </td>
  </tr>
  <tr>
   <td>
    off
   </td>
   <td align="center">
   </td>
   <td align="center">
   </td>
   <td align="center">
   </td>
   <td align="center">
   </td>
  </tr>
 </tbody>
</table>







`wal_sync_method` (`enum`) [#](#GUC-WAL-SYNC-METHOD): Método utilizado para forçar as atualizações do WAL para o disco. Se `fsync` estiver desativado, este ajuste é irrelevante, uma vez que as atualizações do arquivo WAL não serão forçadas para o disco. Os valores possíveis são:

* `open_datasync` (escreva arquivos WAL com a opção `open()` `O_DSYNC`) * `fdatasync` (chame `fdatasync()` em cada commit) * `fsync` (chame `fsync()` em cada commit) * `fsync_writethrough` (chame `fsync()` em cada commit, forçando a escrita direta de qualquer cache de escrita em disco) * `open_sync` (escreva arquivos WAL com a opção `open()` `O_SYNC`)

Nem todas essas opções estão disponíveis em todas as plataformas. O padrão é o primeiro método na lista acima que é suportado pela plataforma, exceto que `fdatasync` é o padrão no Linux e no FreeBSD. O padrão não é necessariamente ideal; pode ser necessário alterar este ajuste ou outros aspectos da configuração do seu sistema para criar uma configuração segura contra falhas ou alcançar o desempenho ótimo. Esses aspectos são discutidos em [Seção 28.1](wal-reliability.md). Este parâmetro só pode ser definido no arquivo `postgresql.conf` ou na linha de comando do servidor.

`full_page_writes` (`boolean`) [#](#GUC-FULL-PAGE-WRITES): Quando este parâmetro está ativado, o servidor PostgreSQL escreve todo o conteúdo de cada página do disco no WAL durante a primeira modificação dessa página após um ponto de verificação. Isso é necessário porque uma escrita de página que está em processo durante um acidente do sistema operacional pode ser apenas parcialmente concluída, levando a uma página em disco que contém uma mistura de dados antigos e novos. Os dados de mudança de nível de linha normalmente armazenados no WAL não serão suficientes para restaurar completamente tal página durante a recuperação pós-acidente. Armazenar a imagem completa da página garante que a página possa ser restaurada corretamente, mas ao preço de aumentar a quantidade de dados que deve ser escrita no WAL. (Como o replay do WAL sempre começa a partir de um ponto de verificação, é suficiente fazer isso durante a primeira mudança de cada página após um ponto de verificação. Portanto, uma maneira de reduzir o custo das escritas de página completa é aumentar os parâmetros do intervalo do ponto de verificação.)

Desligar este parâmetro acelera o funcionamento normal, mas pode levar à corrupção dos dados irrecuperável ou à corrupção silenciosa dos dados após uma falha no sistema. Os riscos são semelhantes aos de desligar `fsync`, embora menores, e deve ser desligado apenas com base nas mesmas circunstâncias recomendadas para esse parâmetro.

Desativar este parâmetro não afeta o uso do arquivamento WAL para recuperação em ponto no tempo (PITR) (consulte [Seção 25.3](continuous-archiving.md)).

Este parâmetro só pode ser definido no arquivo `postgresql.conf` ou na linha de comando do servidor. O padrão é `on`.

`wal_log_hints` (`boolean`) [#](#GUC-WAL-LOG-HINTS): Quando este parâmetro é `on`, o servidor PostgreSQL escreve todo o conteúdo de cada página do disco no WAL durante a primeira modificação daquela página após um ponto de verificação, mesmo para modificações não críticas dos chamados bits de dica.

Se os checksums de dados estiverem habilitados, as atualizações do bit de dica são sempre registradas no WAL e essa configuração é ignorada. Você pode usar essa configuração para testar quanto registro adicional no WAL ocorreria se seus dados tivessem checksums habilitados.

Este parâmetro só pode ser definido no início do servidor. O valor padrão é `off`.

`wal_compression` (`enum`) [#](#GUC-WAL-COMPRESSION): Este parâmetro permite a compressão do WAL usando o método de compressão especificado. Quando habilitado, o servidor PostgreSQL comprime imagens de página completa escritas no WAL (por exemplo, quando [full_page_writes](runtime-config-wal.md#GUC-FULL-PAGE-WRITES) está ativado, durante um backup básico, etc.). Uma imagem de página comprimida será descomprimida durante a reprodução do WAL. Os métodos suportados são `pglz`, `lz4` (se o PostgreSQL foi compilado com `--with-lz4`) e `zstd` (se o PostgreSQL foi compilado com `--with-zstd`). O valor padrão é `off`. Somente usuários superusuários e usuários com o privilégio apropriado `SET` podem alterar esta configuração.

A ativação da compressão pode reduzir o volume do WAL sem aumentar o risco de corrupção de dados irrecuperáveis, mas com o custo de um pouco de CPU extra gasto na compressão durante o registro do WAL e na descomprimagem durante a reprodução do WAL.

`wal_init_zero` (`boolean`) [#](#GUC-WAL-INIT-ZERO): Se configurada para `on` (padrão), esta opção faz com que novos arquivos WAL sejam preenchidos com zeros. Em alguns sistemas de arquivos, isso garante que o espaço seja alocado antes de precisarmos escrever registros WAL. No entanto, sistemas de arquivos *Copy-On-Write* (COW) podem não se beneficiar dessa técnica, portanto, a opção é dada para ignorar o trabalho desnecessário. Se configurada para `off`, apenas o byte final é escrito quando o arquivo é criado, para que ele tenha o tamanho esperado.

`wal_recycle` (`boolean`) [#](#GUC-WAL-RECYCLE): Se configurada para `on` (padrão), esta opção faz com que os arquivos WAL sejam reciclados renomeando-os, evitando a necessidade de criar novos. Em sistemas de arquivos COW, pode ser mais rápido criar novos, então a opção é dada para desabilitar esse comportamento.

`wal_buffers` (`integer`) [#](#GUC-WAL-BUFFERS): O volume de memória compartilhada usado para dados WAL que ainda não foram escritos em disco. O ajuste padrão de -1 seleciona um tamanho igual a 1/32 (cerca de 3%) de [shared_buffers](runtime-config-resource.md#GUC-SHARED-BUFFERS), mas não menos que `64kB` nem mais do que o tamanho de um segmento WAL, tipicamente `16MB`. Este valor pode ser definido manualmente se a escolha automática for muito grande ou muito pequena, mas qualquer valor positivo menor que `32kB` será tratado como `32kB`. Se este valor for especificado sem unidades, ele é considerado blocos WAL, ou seja, `XLOG_BLCKSZ` bytes, tipicamente 8kB. Este parâmetro só pode ser definido no início do servidor.

O conteúdo dos buffers WAL é escrito em disco em cada commit de transação, portanto, valores extremamente grandes provavelmente não proporcionarão um benefício significativo. No entanto, definir esse valor em pelo menos alguns megabytes pode melhorar o desempenho de escrita em um servidor ocupado, onde muitos clientes estão commitando ao mesmo tempo. O autoajuste selecionado pelo ajuste padrão de -1 deve fornecer resultados razoáveis na maioria dos casos.

`wal_writer_delay` (`integer`) [#](#GUC-WAL-WRITER-DELAY): Especifica quantas vezes o escritor WAL esvazia o WAL, em termos de tempo. Após a esvaziamento do WAL, o escritor adormece por o tempo dado por `wal_writer_delay`, a menos que seja acordado mais cedo por uma transação que está sendo comprometida de forma assíncrona. Se o último esvaziamento aconteceu há menos de `wal_writer_delay` e menos de `wal_writer_flush_after` de WAL foi produzido desde então, então o WAL é apenas escrito no sistema operacional, não esvaziado no disco. Se este valor é especificado sem unidades, ele é considerado em milissegundos. O valor padrão é de 200 milissegundos (`200ms`). Note que em alguns sistemas, a resolução efetiva dos atrasos de sono é de 10 milissegundos; definir `wal_writer_delay` para um valor que não é um múltiplo de 10 pode ter os mesmos resultados que definir para o próximo múltiplo de 10 mais alto. Este parâmetro só pode ser definido no arquivo `postgresql.conf` ou na linha de comando do servidor.

`wal_writer_flush_after` (`integer`) [#](#GUC-WAL-WRITER-FLUSH-AFTER): Especifica quantas vezes o escritor WAL esvazia o WAL, em termos de volume. Se o último esvaziamento ocorreu há menos de `wal_writer_delay` e menos de `wal_writer_flush_after` de WAL foi produzido desde então, então os dados do WAL são escritos apenas no sistema operacional, não esvaziados para o disco. Se `wal_writer_flush_after` estiver definido como `0`, os dados do WAL são sempre esvaziados imediatamente. Se este valor for especificado sem unidades, ele é considerado blocos de WAL, ou seja, `XLOG_BLCKSZ` bytes, tipicamente 8 kB. O padrão é `1MB`. Este parâmetro só pode ser definido no arquivo `postgresql.conf` ou na linha de comando do servidor.

`wal_skip_threshold` (`integer`) [#](#GUC-WAL-SKIP-THRESHOLD): Quando `wal_level` é `minimal` e uma transação é confirmada após a criação ou reescrita de uma relação permanente, este ajuste determina como persistir os novos dados. Se os dados forem menores que este ajuste, escreva-os no log WAL; caso contrário, use um fsync de arquivos afetados. Dependendo das propriedades do seu armazenamento, aumentar ou diminuir este valor pode ajudar se tais confirmações estiverem atrasando transações concorrentes. Se este valor for especificado sem unidades, ele é considerado em kilobytes. O padrão é de dois megabytes (`2MB`).

`commit_delay` (`integer`) [#](#GUC-COMMIT-DELAY): A configuração de `commit_delay` adiciona um atraso de tempo antes que um esvaziamento WAL seja iniciado. Isso pode melhorar o desempenho do grupo de commit ao permitir que um número maior de transações sejam confirmadas por meio de um único esvaziamento WAL, se a carga do sistema for alta o suficiente para que transações adicionais estejam prontas para serem confirmadas dentro do intervalo dado. No entanto, também aumenta a latência em até `commit_delay` para cada esvaziamento WAL. Como o atraso é apenas desperdiçado se nenhuma outra transação estiver pronta para ser confirmada, um atraso é realizado apenas se pelo menos `commit_siblings` outras transações estiverem ativas quando um esvaziamento está prestes a ser iniciado. Além disso, não são realizados atrasos se `fsync` estiver desativado. Se este valor for especificado sem unidades, ele é considerado em microsegundos. O valor padrão de `commit_delay` é zero (sem atraso). Somente usuários super e usuários com o privilégio apropriado de `SET` podem alterar essa configuração.

Em versões do PostgreSQL anteriores a 9.3, `commit_delay` se comportava de maneira diferente e era muito menos eficaz: afetava apenas os commits, em vez de todos os limpos do WAL, e esperava pelo atraso configurado inteiro, mesmo que o limpe do WAL fosse concluído mais cedo. A partir do PostgreSQL 9.3, o primeiro processo que fica pronto para limpar espera pelo intervalo configurado, enquanto os processos subsequentes esperam apenas até que o líder complete a operação de limpeza.

`commit_siblings` (`integer`) [#](#GUC-COMMIT-SIBLINGS): Número mínimo de transações abertas simultâneas a serem exigidas antes de realizar o atraso `commit_delay`. Um valor maior torna mais provável que pelo menos uma outra transação esteja pronta para ser comprometida durante o intervalo de atraso. O padrão é de cinco transações.

### 19.5.2. Postos de controle [#](#RUNTIME-CONFIG-WAL-CHECKPOINTS)

`checkpoint_timeout` (`integer`) [#](#GUC-CHECKPOINT-TIMEOUT): Tempo máximo entre os pontos de verificação WAL automática. Se este valor for especificado sem unidades, ele é considerado em segundos. A faixa válida é entre 30 segundos e um dia. O padrão é de cinco minutos (`5min`). Aumentar este parâmetro pode aumentar o tempo necessário para a recuperação em caso de falha. Este parâmetro só pode ser definido no arquivo `postgresql.conf` ou na linha de comando do servidor.

`checkpoint_completion_target` (`floating point`) [#](#GUC-CHECKPOINT-COMPLETION-TARGET): Especifica o alvo da conclusão do ponto de verificação, como uma fração do tempo total entre os pontos de verificação. O padrão é 0,9, que distribui o ponto de verificação em quase todo o intervalo disponível, proporcionando uma carga de I/O bastante consistente, ao mesmo tempo em que deixa algum tempo para a sobrecarga da conclusão do ponto de verificação. Reduzir este parâmetro não é recomendado, pois isso faz com que o ponto de verificação seja concluído mais rápido. Isso resulta em uma taxa de I/O mais alta durante o ponto de verificação, seguida por um período de menos I/O entre a conclusão do ponto de verificação e o próximo ponto de verificação agendado. Este parâmetro só pode ser definido no arquivo `postgresql.conf` ou na linha de comando do servidor.

`checkpoint_flush_after` (`integer`) [#](#GUC-CHECKPOINT-FLUSH-AFTER): Sempre que mais do que essa quantidade de dados tiver sido escrita durante a realização de um ponto de verificação, tente forçar o SO a emitir essas escritas no armazenamento subjacente. Fazer isso limitará a quantidade de dados sujos no cache de páginas do kernel, reduzindo a probabilidade de travamentos quando um `fsync` é emitido no final do ponto de verificação, ou quando o SO escreve dados de volta em lotes maiores no segundo plano. Muitas vezes isso resultará em uma latência de transação muito reduzida, mas também há alguns casos, especialmente com cargas de trabalho que são maiores que [shared_buffers](runtime-config-resource.md#GUC-SHARED-BUFFERS), mas menores que o cache de páginas do SO, onde o desempenho pode degradar. Este parâmetro pode não ter efeito em algumas plataformas. Se este valor for especificado sem unidades, ele é considerado em blocos, ou seja, `BLCKSZ` bytes, tipicamente 8kB. A faixa válida está entre `0`, que desativa a escrita forçada de volta, e `2MB`. O padrão é `256kB` no Linux, `0` em outros lugares. (Se `BLCKSZ` não for 8kB, os valores padrão e máximos escalam proporcionalmente a ele.) Este parâmetro só pode ser definido no arquivo `postgresql.conf` ou na linha de comando do servidor.

`checkpoint_warning` (`integer`) [#](#GUC-CHECKPOINT-WARNING): Escreva uma mensagem no log do servidor se os pontos de verificação causados pelo preenchimento dos arquivos de segmentos WAL ocorrerem mais próximos do que esse período de tempo (o que sugere que `max_wal_size` deve ser aumentado). Se esse valor for especificado sem unidades, ele é considerado em segundos. O padrão é de 30 segundos (`30s`). Zero desativa o aviso. Não serão gerados avisos se `checkpoint_timeout` for menor que `checkpoint_warning`. Este parâmetro só pode ser definido no arquivo `postgresql.conf` ou na linha de comando do servidor.

`max_wal_size` (`integer`) [#](#GUC-MAX-WAL-SIZE): Tamanho máximo para permitir que o WAL cresça durante os pontos de verificação automáticos. Esse é um limite flexível; o tamanho do WAL pode exceder `max_wal_size` em circunstâncias especiais, como carga pesada, um `archive_command` ou `archive_library` falhando, ou um alto `wal_keep_size` definido. Se esse valor for especificado sem unidades, ele é considerado em megabytes. O padrão é 1 GB. Aumentar esse parâmetro pode aumentar o tempo necessário para a recuperação em caso de falha. Esse parâmetro só pode ser definido no arquivo `postgresql.conf` ou na linha de comando do servidor.

`min_wal_size` (`integer`) [#](#GUC-MIN-WAL-SIZE): Enquanto o uso do disco WAL permanecer abaixo deste ajuste, os arquivos antigos do WAL são sempre reciclados para uso futuro em um ponto de verificação, em vez de serem removidos. Isso pode ser usado para garantir que espaço suficiente do WAL seja reservado para lidar com picos no uso do WAL, por exemplo, ao executar grandes trabalhos em lote. Se este valor for especificado sem unidades, ele é considerado em megabytes. O padrão é 80 MB. Este parâmetro só pode ser definido no arquivo `postgresql.conf` ou na linha de comando do servidor.

### 19.5.3. Arquivamento [#](#RUNTIME-CONFIG-WAL-ARCHIVING)

`archive_mode` (`enum`) [#](#GUC-ARCHIVE-MODE): Quando o `archive_mode` está habilitado, segmentos WAL completos são enviados para o armazenamento de arquivo definindo [archive_command](runtime-config-wal.md#GUC-ARCHIVE-COMMAND) ou [archive_library](runtime-config-wal.md#GUC-ARCHIVE-LIBRARY). Além do `off`, para desabilitar, existem dois modos: `on`, e `always`. Durante o funcionamento normal, não há diferença entre os dois modos, mas quando definido como `always`, o arquivador WAL é habilitado também durante a recuperação de arquivo ou modo standby. No modo `always`, todos os arquivos restaurados do arquivo ou transmitidos com replicação em fluxo serão arquivados (novamente). Veja [Seção 26.2.9](warm-standby.md#CONTINUOUS-ARCHIVING-IN-STANDBY "26.2.9. Continuous Archiving in Standby") para detalhes.

`archive_mode` é um ajuste separado de `archive_command` e `archive_library`, para que `archive_command` e `archive_library` possam ser alterados sem sair do modo de arquivamento. Este parâmetro só pode ser definido no início do servidor. `archive_mode` não pode ser habilitado quando `wal_level` está definido como `minimal`.

`archive_command` (`string`) [#](#GUC-ARCHIVE-COMMAND): O comando de linha de comando local a ser executado para arquivar um segmento de arquivo WAL concluído. Qualquer `%p` na string é substituído pelo nome do caminho do arquivo a ser arquivado, e qualquer `%f` é substituído apenas pelo nome do arquivo. (O nome do caminho é relativo ao diretório de trabalho do servidor, ou seja, o diretório de dados do clúster.) Use `%%` para incorporar um caractere de `%` real no comando. É importante que o comando retorne um status de saída zero apenas se for bem-sucedido. Para mais informações, consulte [Seção 25.3.1](continuous-archiving.md#BACKUP-ARCHIVING-WAL "25.3.1. Setting Up WAL Archiving").

Este parâmetro só pode ser definido no arquivo `postgresql.conf` ou na linha de comando do servidor. Ele só é usado se `archive_mode` foi habilitado no início do servidor e `archive_library` está definido como uma string vazia. Se tanto `archive_command` quanto `archive_library` estiverem definidos, um erro será exibido. Se `archive_command` for uma string vazia (o padrão) enquanto `archive_mode` está habilitado (e `archive_library` está definido como uma string vazia), o arquivamento WAL é temporariamente desativado, mas o servidor continua a acumular arquivos de segmento WAL na expectativa de que um comando seja fornecido em breve. Definir `archive_command` para um comando que não faça nada além de retornar true, por exemplo, `/bin/true` (`REM` no Windows), desativa efetivamente o arquivamento, mas também quebra a cadeia de arquivos WAL necessários para a recuperação do arquivo de armazém, portanto, só deve ser usado em circunstâncias incomuns.

`archive_library` (`string`) [#](#GUC-ARCHIVE-LIBRARY): A biblioteca a ser usada para arquivar segmentos de arquivo WAL concluídos. Se definida como uma string vazia (o padrão), o arquivamento via shell é habilitado e [archive_command](runtime-config-wal.md#GUC-ARCHIVE-COMMAND) é usado. Se `archive_command` e `archive_library` estiverem definidos, um erro será gerado. Caso contrário, a biblioteca compartilhada especificada é usada para arquivamento. O processo de arquivamento WAL é reiniciado pelo postmaster quando este parâmetro muda. Para mais informações, consulte [Seção 25.3.1](continuous-archiving.md#BACKUP-ARCHIVING-WAL "25.3.1. Setting Up WAL Archiving") e [Capítulo 49](archive-modules.md "Chapter 49. Archive Modules").

Este parâmetro só pode ser definido no arquivo `postgresql.conf` ou na linha de comando do servidor.

`archive_timeout` (`integer`) [#](#GUC-ARCHIVE-TIMEOUT): O [archive_command](runtime-config-wal.md#GUC-ARCHIVE-COMMAND) ou [archive_library](runtime-config-wal.md#GUC-ARCHIVE-LIBRARY) é invocado apenas para segmentos WAL completos. Portanto, se o seu servidor gera pouco tráfego WAL (ou tem períodos de folga em que o faz), pode haver um longo atraso entre a conclusão de uma transação e sua gravação segura no armazenamento de arquivo. Para limitar quão antigo pode ser o dado não arquivado, você pode configurar `archive_timeout` para forçar o servidor a alternar para um novo arquivo de segmento WAL periodicamente. Quando esse parâmetro for maior que zero, o servidor alternará para um novo arquivo de segmento sempre que esse período de tempo tiver se passado desde a última alternância de arquivo de segmento, e houver alguma atividade de banco de dados, incluindo um único ponto de verificação (os pontos de verificação são ignorados se não houver atividade de banco de dados). Note que os arquivos arquivados que são fechados precocemente devido a uma alternância forçada ainda têm o mesmo tamanho dos arquivos completamente cheios. Portanto, não é aconselhável usar um `archive_timeout` muito curto — isso fará com que seu armazenamento de arquivo fique inchado. As configurações de `archive_timeout` de cerca de um minuto são geralmente razoáveis. Você deve considerar usar replicação em fluxo, em vez de arquivamento, se deseja que os dados sejam copiados do servidor principal mais rapidamente. Se esse valor for especificado sem unidades, ele é considerado em segundos. Esse parâmetro só pode ser configurado no arquivo `postgresql.conf` ou na linha de comando do servidor.

### 19.5.4. Recuperação [#](#RUNTIME-CONFIG-WAL-RECOVERY)

Esta seção descreve as configurações que se aplicam à recuperação em geral, afetando a recuperação de falhas, a replicação em streaming e a replicação baseada em arquivos de registro.

`recovery_prefetch` (`enum`) [#](#GUC-RECOVERY-PREFETCH): Se deve tentar pré-carregar blocos que são referenciados no WAL e que ainda não estão no buffer pool, durante a recuperação. Os valores válidos são `off`, `on` e `try` (o padrão). A configuração `try` permite pré-carregar apenas se o sistema operacional fornecer suporte para emitir conselhos de leitura à frente.

Prefetchar blocos que serão necessários em breve pode reduzir os tempos de espera de I/O durante a recuperação com algumas cargas de trabalho. Veja também as configurações [wal_decode_buffer_size](runtime-config-wal.md#GUC-WAL-DECODE-BUFFER-SIZE) e [maintenance_io_concurrency](runtime-config-resource.md#GUC-MAINTENANCE-IO-CONCURRENCY), que limitam a atividade de preenchimento.

`wal_decode_buffer_size` (`integer`) [#](#GUC-WAL-DECODE-BUFFER-SIZE): Um limite de quão longe o servidor pode olhar para a WAL, para encontrar blocos a pré-visualizar. Se este valor for especificado sem unidades, ele é considerado em bytes. O padrão é 512 kB. Este parâmetro só pode ser definido no início do servidor.

### 19.5.5. Recuperação de Arquivo [#](#RUNTIME-CONFIG-WAL-ARCHIVE-RECOVERY)

Esta seção descreve as configurações que se aplicam apenas durante a duração da recuperação. Elas devem ser redefinidas para qualquer recuperação subsequente que você deseje realizar.

“Recuperação” abrange o uso do servidor como um standby ou para executar uma recuperação direcionada. Normalmente, o modo standby seria usado para fornecer alta disponibilidade e/ou escalabilidade de leitura, enquanto uma recuperação direcionada é usada para recuperar a perda de dados.

Para iniciar o servidor no modo standby, crie um arquivo chamado `standby.signal` no diretório de dados. O servidor entrará em recuperação e não parará a recuperação quando o fim do WAL arquivado for alcançado, mas continuará tentando continuar a recuperação conectando-se ao servidor de envio conforme especificado pela configuração `primary_conninfo` e/ou obtendo novos segmentos WAL usando `restore_command`. Para este modo, os parâmetros desta seção e [Seção 19.6.3](runtime-config-replication.md#RUNTIME-CONFIG-REPLICATION-STANDBY "19.6.3. Standby Servers") são de interesse. Os parâmetros de [Seção 19.5.6](runtime-config-wal.md#RUNTIME-CONFIG-WAL-RECOVERY-TARGET "19.5.6. Recovery Target") também serão aplicados, mas normalmente não são úteis neste modo.

Para iniciar o servidor no modo de recuperação direcionado, crie um arquivo chamado `recovery.signal` no diretório de dados. Se os arquivos `standby.signal` e `recovery.signal` forem criados, o modo de espera tem precedência. O modo de recuperação direcionado termina quando o WAL arquivado é totalmente reinterpretado ou quando o `recovery_target` é alcançado. Neste modo, os parâmetros desta seção e do [Seção 19.5.6](runtime-config-wal.md#RUNTIME-CONFIG-WAL-RECOVERY-TARGET "19.5.6. Recovery Target") serão usados.

`restore_command` (`string`) [#](#GUC-RESTORE-COMMAND): O comando de linha de comando local a ser executado para recuperar um segmento arquivado da série de arquivos WAL. Este parâmetro é necessário para a recuperação de arquivos de arquivamento, mas opcional para replicação em fluxo. Qualquer `%f` na string é substituído pelo nome do arquivo a ser recuperado do arquivo, e qualquer `%p` é substituído pelo nome do caminho de destino da cópia no servidor. (O nome do caminho é relativo ao diretório de trabalho atual, ou seja, o diretório de dados do clúster.) Qualquer `%r` é substituído pelo nome do arquivo que contém o último ponto de reinício válido. Esse é o arquivo mais antigo que deve ser mantido para permitir que uma restauração possa ser reiniciada, então essas informações podem ser usadas para truncar o arquivo apenas no mínimo necessário para suportar o reinício a partir da restauração atual. `%r` é tipicamente usado apenas em configurações de standby quente (ver [Seção 26.2](warm-standby.md)). Escreva `%%` para incorporar um caractere de `%` real.

É importante que o comando retorne um status de saída zero apenas se for bem-sucedido. O comando *será* solicitado para nomes de arquivos que não estão presentes no arquivo; ele deve retornar um valor não nulo quando solicitado. Exemplos:

```
restore_command = 'cp /mnt/server/archivedir/%f "%p"' restore_command = 'copy "C:\\server\\archivedir\\%f" "%p"'  # Windows
```

Uma exceção é que, se o comando foi encerrado por um sinal (diferente de SIGTERM, que é usado como parte de um desligamento do servidor de banco de dados) ou por um erro do shell (como comando não encontrado), então a recuperação será interrompida e o servidor não será iniciado.

Este parâmetro só pode ser definido no arquivo `postgresql.conf` ou na linha de comando do servidor.

`archive_cleanup_command` (`string`) [#](#GUC-ARCHIVE-CLEANUP-COMMAND): Este parâmetro opcional especifica um comando de shell que será executado em cada ponto de reinício. O propósito de `archive_cleanup_command` é fornecer um mecanismo para limpar arquivos WAL arquivados antigos que não são mais necessários pelo servidor de espera. Qualquer `%r` é substituído pelo nome do arquivo que contém o último ponto de reinício válido. Esse é o arquivo mais antigo que deve ser *mantido* para permitir que um restabelecimento seja restabelecido, e, portanto, todos os arquivos anteriores a `%r` podem ser removidos com segurança. Esta informação pode ser usada para truncar o arquivo apenas no mínimo necessário para suportar o reinício a partir do restabelecimento atual. O módulo [pg_archivecleanup](pgarchivecleanup.md "pg_archivecleanup") é frequentemente usado em `archive_cleanup_command` para configurações de único servidor de espera, por exemplo:

```
archive_cleanup_command = 'pg_archivecleanup /mnt/server/archivedir %r'
```

Observe, no entanto, que se vários servidores de espera estarem restaurando a partir do mesmo diretório de arquivo, você precisará garantir que não delete os arquivos WAL até que eles não sejam mais necessários por nenhum dos servidores. `archive_cleanup_command` seria tipicamente usado em uma configuração de standby quente (consulte [Seção 26.2] (warm-standby.md "26.2. Log-Shipping Standby Servers")). Escreva `%%` para incorporar um caractere real `%` no comando.

Se o comando retornar um estado de saída não nulo, uma mensagem de log de alerta será escrita. Uma exceção é que, se o comando foi terminado por um sinal ou um erro pelo shell (como comando não encontrado), um erro fatal será gerado.

Este parâmetro só pode ser definido no arquivo `postgresql.conf` ou na linha de comando do servidor.

`recovery_end_command` (`string`) [#](#GUC-RECOVERY-END-COMMAND): Este parâmetro especifica um comando de shell que será executado apenas no final da recuperação. Este parâmetro é opcional. O propósito do `recovery_end_command` é fornecer um mecanismo para limpeza seguindo a replicação ou recuperação. Qualquer `%r` é substituído pelo nome do arquivo que contém o último ponto de reinício válido, como em [archive_cleanup_command](runtime-config-wal.md#GUC-ARCHIVE-CLEANUP-COMMAND).

Se o comando retornar um estado de saída não nulo, uma mensagem de log de alerta será escrita e o banco de dados prosseguirá com o início. Uma exceção é que, se o comando foi terminado por um sinal ou um erro pelo shell (como comando não encontrado), o banco de dados não prosseguirá com o início.

Este parâmetro só pode ser definido no arquivo `postgresql.conf` ou na linha de comando do servidor.

### 19.5.6. Objetivo de recuperação [#](#RUNTIME-CONFIG-WAL-RECOVERY-TARGET)

Por padrão, a recuperação será feita até o final do log WAL. Os seguintes parâmetros podem ser usados para especificar um ponto de parada anterior. No máximo, um dos seguintes `recovery_target`, `recovery_target_lsn`, `recovery_target_name`, `recovery_target_time` ou `recovery_target_xid` pode ser usado; se mais de um desses forem especificados no arquivo de configuração, um erro será gerado. Esses parâmetros só podem ser definidos no início do servidor.

`recovery_target` `= 'immediate'` [#](#GUC-RECOVERY-TARGET): Este parâmetro especifica que a recuperação deve terminar assim que um estado consistente for alcançado, ou seja, o mais cedo possível. Ao restaurar a partir de um backup online, isso significa o ponto em que a tomada do backup terminou.

Tecnicamente, este é um parâmetro de cadeia, mas `'immediate'` é atualmente o único valor permitido.

`recovery_target_name` (`string`) [#](#GUC-RECOVERY-TARGET-NAME): Este parâmetro especifica o ponto de restauração nomeado (criado com `pg_create_restore_point()`) para o qual a recuperação prosseguirá.

`recovery_target_time` (`timestamp`) [#](#GUC-RECOVERY-TARGET-TIME): Este parâmetro especifica o rótulo de tempo até o qual a recuperação procurará prosseguir. O ponto de parada preciso também é influenciado por [recovery_target_inclusive](runtime-config-wal.md#GUC-RECOVERY-TARGET-INCLUSIVE).

O valor deste parâmetro é um rótulo de tempo no mesmo formato aceito pelo tipo de dados `timestamp with time zone`, exceto que você não pode usar uma abreviação de fuso horário (a menos que a variável [timezone_abbreviations](runtime-config-client.md#GUC-TIMEZONE-ABBREVIATIONS) tenha sido definida anteriormente no arquivo de configuração). O estilo preferido é usar um deslocamento numérico em relação ao UTC, ou você pode escrever um nome completo de fuso horário, por exemplo, `Europe/Helsinki` não `EEST`.

`recovery_target_xid` (`string`) [#](#GUC-RECOVERY-TARGET-XID): Este parâmetro especifica o ID de transação até o qual a recuperação procurará prosseguir. Tenha em mente que, embora os IDs de transação sejam atribuídos sequencialmente no início da transação, as transações podem ser concluídas em um ordem numérica diferente. As transações que serão recuperadas são aquelas que foram comprometidas antes (e opcionalmente incluindo) a uma especificada. O ponto de parada preciso também é influenciado por [recovery_target_inclusive](runtime-config-wal.md#GUC-RECOVERY-TARGET-INCLUSIVE).

`recovery_target_lsn` (`pg_lsn`) [#](#GUC-RECOVERY-TARGET-LSN): Este parâmetro especifica o LSN (Local Storage Number) do local de log de pré-escrita até o qual a recuperação prosseguirá. O ponto de parada preciso também é influenciado por [recovery_target_inclusive](runtime-config-wal.md#GUC-RECOVERY-TARGET-INCLUSIVE). Este parâmetro é analisado usando o tipo de dados do sistema [`pg_lsn`](datatype-pg-lsn.md "8.20. pg_lsn Type").

As opções a seguir especificam ainda mais o objetivo de recuperação e afetam o que acontece quando o objetivo é alcançado:

`recovery_target_inclusive` (`boolean`) [#](#GUC-RECOVERY-TARGET-INCLUSIVE): Especifica se deve parar logo após o alvo de recuperação especificado (`on`), ou logo antes do alvo de recuperação (`off`). Aplica-se quando [recovery_target_lsn](runtime-config-wal.md#GUC-RECOVERY-TARGET-LSN), [recovery_target_time](runtime-config-wal.md#GUC-RECOVERY-TARGET-TIME), ou [recovery_target_xid](runtime-config-wal.md#GUC-RECOVERY-TARGET-XID) é especificado. Este ajuste controla se as transações que têm exatamente a localização do WAL alvo (LSN), tempo de compromisso ou ID de transação, respectivamente, serão incluídas na recuperação. O padrão é `on`.

`recovery_target_timeline` (`string`) [#](#GUC-RECOVERY-TARGET-TIMELINE): Especifica a recuperação em um determinado período de tempo. O valor pode ser um ID de linha de tempo numérico ou um valor especial. O valor `current` recupera ao longo do mesmo período de tempo que estava em uso quando o backup de base foi feito. O valor `latest` recupera para o último período de tempo encontrado no arquivo, o que é útil em um servidor de espera. `latest` é o padrão.

Para especificar um ID de linha de tempo em hexadecimal (por exemplo, se extraído de um nome de arquivo WAL ou arquivo de histórico), prefixe-o com `0x`. Por exemplo, se o nome do arquivo WAL for `00000011000000A10000004F`, então o ID de linha de tempo é `0x11` (ou 17 decimal).

Normalmente, você só precisa definir esse parâmetro em situações de re-recuperação complexas, onde você precisa retornar a um estado que foi alcançado após uma recuperação ponto-no-tempo. Consulte [Seção 25.3.6](continuous-archiving.md#BACKUP-TIMELINES) para discussão.

`recovery_target_action` (`enum`) [#](#GUC-RECOVERY-TARGET-ACTION): Especifica a ação que o servidor deve tomar uma vez que o alvo de recuperação é atendido. O padrão é `pause`, o que significa que a recuperação será pausada. `promote` significa que o processo de recuperação terminará e o servidor começará a aceitar conexões. Finalmente, `shutdown` parará o servidor após atingir o alvo de recuperação.

O uso pretendido do ajuste `pause` é permitir que consultas sejam executadas no banco de dados para verificar se este alvo de recuperação é o ponto mais desejável para a recuperação. O estado parado pode ser retomado usando `pg_wal_replay_resume()` (consulte [Tabela 9.99](functions-admin.md#FUNCTIONS-RECOVERY-CONTROL-TABLE)), o que, em seguida, faz com que a recuperação termine. Se este alvo de recuperação não for o ponto de parada desejado, então desligue o servidor, mude as configurações do alvo de recuperação para um alvo posterior e reinicie para continuar a recuperação.

A configuração `shutdown` é útil para ter a instância pronta no ponto de reprodução exato desejado. A instância ainda poderá reproduzir mais registros WAL (e, de fato, terá que reproduzir registros WAL da próxima vez que for iniciada).

Observe que, porque o `recovery.signal` não será removido quando o `recovery_target_action` estiver configurado como `shutdown`, qualquer início subsequente terminará com desligamento imediato, a menos que a configuração seja alterada ou o arquivo `recovery.signal` seja removido manualmente.

Este ajuste não tem efeito se não for definido um alvo de recuperação. Se [hot_standby](runtime-config-replication.md#GUC-HOT-STANDBY) não estiver habilitado, um ajuste de `pause` atuará da mesma forma que `shutdown`. Se o alvo de recuperação for atingido enquanto uma promoção está em andamento, um ajuste de `pause` atuará da mesma forma que `promote`.

Em qualquer caso, se um objetivo de recuperação for configurado, mas a recuperação do arquivo terminar antes de o objetivo ser atingido, o servidor será desligado com um erro fatal.

### 19.5.7. Resumo do WAL [#](#RUNTIME-CONFIG-WAL-SUMMARIZATION)

Esses ajustes controlam a sumarização WAL, uma funcionalidade que deve ser habilitada para realizar um [backup incremental] (continuous-archiving.md#BACKUP-INCREMENTAL-BACKUP "25.3.3. Making an Incremental Backup").

`summarize_wal` (`boolean`) [#](#GUC-SUMMARIZE-WAL): Habilita o processo de sumarizador WAL. Observe que a sumarização WAL pode ser habilitada em um primário ou em um de reserva. Este parâmetro só pode ser definido no arquivo `postgresql.conf` ou na linha de comando do servidor. O padrão é `off`.

O servidor não pode ser iniciado com `summarize_wal=on` se `wal_level` estiver configurado como `minimal`. Se `summarize_wal=on` for configurado após a inicialização do servidor enquanto `wal_level=minimal` estiver ativo, o resumidor será executado, mas se recusará a gerar arquivos de resumo para qualquer WAL gerado com `wal_level=minimal`.

`wal_summary_keep_time` (`integer`) [#](#GUC-WAL-SUMMARY-KEEP-TIME): Configura o tempo após o qual o sumarizador WAL remove automaticamente os resumos antigos do WAL. O timestamp do arquivo é usado para determinar quais arquivos são antigos o suficiente para serem removidos. Normalmente, você deve definir esse valor de forma confortávelmente maior do que o tempo que pode passar entre um backup e um backup incremental posterior que dependa dele. Os resumos WAL devem estar disponíveis para toda a faixa de registros WAL entre o backup anterior e o novo que está sendo realizado; caso contrário, o backup incremental falhará. Se este parâmetro for definido como zero, os resumos WAL não serão removidos automaticamente, mas é seguro remover manualmente os arquivos que você sabe que não serão necessários para backups incrementais futuros. Este parâmetro só pode ser definido no arquivo `postgresql.conf` ou na linha de comando do servidor. Se este valor for especificado sem unidades, ele é considerado em minutos. O padrão é 10 dias. Se `summarize_wal = off`, os resumos WAL existentes não serão removidos, independentemente do valor deste parâmetro, porque o sumarizador WAL não será executado.