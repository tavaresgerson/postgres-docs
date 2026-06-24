## 25.3. Arquivamento Contínuo e Recuperação em Ponto no Tempo (PITR) [#](#CONTINUOUS-ARCHIVING)

* [25.3.1. Configuração do arquivamento WAL][(continuous-archiving.md#BACKUP-ARCHIVING-WAL)
* [25.3.2. Fazer um backup de base][(continuous-archiving.md#BACKUP-BASE-BACKUP)
* [25.3.3. Fazer um backup incremental][(continuous-archiving.md#BACKUP-INCREMENTAL-BACKUP)
* [25.3.4. Fazer um backup de base usando a API de baixo nível][(continuous-archiving.md#BACKUP-LOWLEVEL-BASE-BACKUP)
* [25.3.5. Recuperação usando um backup de arquivo contínuo][(continuous-archiving.md#BACKUP-PITR-RECOVERY)
* [25.3.6. Linhas do tempo][(continuous-archiving.md#BACKUP-TIMELINES)
* [25.3.7. Dicas e exemplos][(continuous-archiving.md#BACKUP-TIPS)
* [25.3.8. Considerações][(continuous-archiving.md#CONTINUOUS-ARCHIVING-CAVEATS)

Em todos os momentos, o PostgreSQL mantém um *registro de escrita antecipada* (WAL) no subdiretório `pg_wal/` do diretório de dados do clúster. O registro registra todas as alterações feitas nos arquivos de dados do banco de dados. Esse registro existe principalmente para fins de segurança em caso de falha: se o sistema falhar, o banco de dados pode ser restaurado à consistência "rejogando" as entradas do registro feitas desde o último ponto de verificação. No entanto, a existência do registro permite a utilização de uma terceira estratégia para fazer backups de bancos de dados: podemos combinar um backup em nível de sistema de arquivos com o backup dos arquivos WAL. Se a recuperação for necessária, restauramos o backup do sistema de arquivos e, em seguida, rejogamos a partir dos arquivos WAL de backup para trazer o sistema a um estado atual. Essa abordagem é mais complexa de administrar do que qualquer uma das abordagens anteriores, mas tem alguns benefícios significativos:

* Não precisamos de um backup de sistema de arquivos perfeitamente consistente como ponto de partida. Qualquer inconsistência interna no backup será corrigida pelo replay de log (isso não é significativamente diferente do que acontece durante a recuperação em caso de falha). Portanto, não precisamos de uma capacidade de instantâneo do sistema de arquivos, apenas tar ou uma ferramenta de arquivamento semelhante.
* Como podemos combinar uma sequência indefinidamente longa de arquivos WAL para replay, o backup contínuo pode ser alcançado simplesmente continuando a arquivar os arquivos WAL. Isso é particularmente valioso para grandes bancos de dados, onde pode não ser conveniente fazer um backup completo com frequência.
* Não é necessário replayar as entradas do WAL até o final. Podemos parar o replay em qualquer ponto e ter um instantâneo consistente do banco de dados como estava naquela época. Assim, essa técnica suporta a *recuperação em um ponto no tempo*: é possível restaurar o banco de dados ao seu estado em qualquer momento desde que seu backup de base foi feito.
* Se alimentarmos continuamente a série de arquivos WAL em outra máquina que tenha sido carregada com o mesmo arquivo de backup de base, temos um sistema de *standby quente*: em qualquer ponto, podemos colocar a segunda máquina e ela terá uma cópia quase atual do banco de dados.

Nota

pg_dump e pg_dumpall não produzem backups em nível de sistema de arquivos e não podem ser usados como parte de uma solução de arquivamento contínuo. Esses backups são *lógicos* e não contêm informações suficientes para serem usados pelo replay do WAL.

Assim como a técnica de backup simples com sistema de arquivos, este método só pode suportar a restauração de um conjunto de bancos de dados inteiros, não de um subconjunto. Além disso, ele exige um grande armazenamento de arquivamento: o backup básico pode ser volumoso, e um sistema ocupado gerará muitos megabytes de tráfego WAL que precisam ser arquivados. Ainda assim, é a técnica de backup preferida em muitas situações onde é necessária alta confiabilidade.

Para recuperar com sucesso usando arquivamento contínuo (também chamado de "backup online" por muitos fornecedores de bancos de dados), você precisa de uma sequência contínua de arquivos WAL arquivados que se estenda pelo menos até o horário de início do seu backup. Portanto, para começar, você deve configurar e testar seu procedimento para arquivamento de arquivos WAL * antes * de fazer seu primeiro backup de base. Assim, primeiro discutimos a mecânica do arquivamento de arquivos WAL.

### 25.3.1. Configuração do arquivamento WAL [#](#BACKUP-ARCHIVING-WAL)

Em um sentido abstrato, um sistema PostgreSQL em execução produz uma sequência indefinidamente longa de registros WAL. O sistema divide fisicamente essa sequência em arquivos de *segmento WAL*, que normalmente são de 16 MB cada (embora o tamanho do segmento possa ser alterado durante o initdb). Os arquivos de segmento recebem nomes numéricos que refletem sua posição na sequência abstrata WAL. Quando não está usando a arquivamento WAL, o sistema normalmente cria apenas alguns arquivos de segmento e depois os "recicla" renomeando os arquivos de segmento que não são mais necessários para números de segmento mais altos. Assume-se que os arquivos de segmento cujo conteúdo precede o último ponto de verificação não são mais de interesse e podem ser reciclados.

Ao arquivar dados WAL, precisamos capturar o conteúdo de cada arquivo de segmento assim que ele for preenchido e salvar esses dados em algum lugar antes de o arquivo de segmento ser reciclado para uso. Dependendo da aplicação e do hardware disponível, pode haver muitas maneiras diferentes de “salvar os dados em algum lugar”: podemos copiar os arquivos de segmento para um diretório montado em NFS em outra máquina, escrevê-los em uma unidade de fita (assegurando que você tenha uma maneira de identificar o nome original de cada arquivo) ou agrupá-los e gravá-los em CDs, ou algo completamente diferente. Para fornecer flexibilidade ao administrador do banco de dados, o PostgreSQL tenta não fazer suposições sobre como o arquivamento será feito. Em vez disso, o PostgreSQL permite que o administrador especifique um comando de shell ou uma biblioteca de arquivo a ser executado para copiar um arquivo de segmento concluído para onde ele precisa ir. Isso pode ser tão simples quanto um comando de shell que usa `cp`, ou pode invocar uma função C complexa — tudo depende de você.

Para habilitar o arquivamento WAL, defina o parâmetro de configuração [wal_level](runtime-config-wal.md#GUC-WAL-LEVEL) para `replica` ou superior, [archive_mode](runtime-config-wal.md#GUC-ARCHIVE-MODE) para `on`, especifique o comando de shell a ser usado no parâmetro de configuração [archive_command](runtime-config-wal.md#GUC-ARCHIVE-COMMAND) ou especifique a biblioteca a ser usada no parâmetro de configuração [archive_library](runtime-config-wal.md#GUC-ARCHIVE-LIBRARY). Na prática, esses ajustes serão sempre colocados no arquivo `postgresql.conf`.

Em `archive_command`, `%p` é substituído pelo nome do caminho do arquivo a ser arquivado, enquanto `%f` é substituído apenas pelo nome do arquivo. (O nome do caminho é relativo ao diretório de trabalho atual, ou seja, ao diretório de dados do cluster.) Use `%%` se você precisar incorporar um caractere real `%` no comando. O comando mais simples e útil é algo como:

```
archive_command = 'test ! -f /mnt/server/archivedir/%f && cp %p /mnt/server/archivedir/%f'  # Unix
archive_command = 'copy "%p" "C:\\server\\archivedir\\%f"'  # Windows
```

que copiará os segmentos WAL arquiváveis para o diretório `/mnt/server/archivedir`. (Este é um exemplo, não uma recomendação, e pode não funcionar em todas as plataformas.) Após os parâmetros `%p` e `%f` terem sido substituídos, o comando executado efetivamente pode parecer assim:

```
test ! -f /mnt/server/archivedir/00000001000000A900000065 && cp pg_wal/00000001000000A900000065 /mnt/server/archivedir/00000001000000A900000065
```

Um comando semelhante será gerado para cada novo arquivo que será arquivado.

O comando de arquivamento será executado sob a propriedade do mesmo usuário em que o servidor PostgreSQL está sendo executado. Como a série de arquivos WAL que está sendo arquivada contém efetivamente tudo no seu banco de dados, você vai querer ter certeza de que os dados arquivados estão protegidos de olhares indiscretos; por exemplo, armazene em um diretório que não tenha acesso de leitura de grupo ou mundo.

É importante que o comando de arquivo retorne um status de saída de zero se e somente se ele tiver sucesso. Ao obter um resultado nulo, o PostgreSQL assumirá que o arquivo foi arquivado com sucesso e o removerá ou reciclará. No entanto, um status não nulo informa ao PostgreSQL que o arquivo não foi arquivado; ele tentará novamente periodicamente até obter sucesso.

Outra maneira de arquivar é usar um módulo de arquivo personalizado como o `archive_library`. Como esses módulos são escritos em `C`, criar o seu próprio pode exigir um esforço consideravelmente maior do que escrever um comando de shell. No entanto, os módulos de arquivo podem ser mais eficientes do que arquivar via shell, e eles terão acesso a muitos recursos úteis do servidor. Para mais informações sobre módulos de arquivo, consulte [Capítulo 49](archive-modules.md).

Quando o comando de arquivamento é interrompido por um sinal (diferente de SIGTERM, que é usado como parte de uma interrupção do servidor) ou por um erro da shell com um status de saída maior que 125 (como comando não encontrado), ou se a função de arquivamento emite `ERROR` ou `FATAL`, o processo de arquivamento é abortado e reiniciado pelo postmaster. Nesses casos, a falha não é relatada em [pg_stat_archiver](monitoring-stats.md#PG-STAT-ARCHIVER-VIEW "Table 27.22. pg_stat_archiver View").

Os comandos e bibliotecas de arquivo devem, em geral, ser projetados para se recusar a sobrescrever qualquer arquivo de arquivo pré-existente. Esse é um recurso de segurança importante para preservar a integridade do seu arquivo em caso de erro do administrador (como enviar a saída de dois servidores diferentes para o mesmo diretório de arquivo). É aconselhável testar a biblioteca de arquivo proposta para garantir que ela não sobrescreva um arquivo existente.

Em casos raros, o PostgreSQL pode tentar re-arquivar um arquivo WAL que já foi arquivado. Por exemplo, se o sistema falhar antes de o servidor fazer um registro durável de sucesso de arquivamento, o servidor tentará arquivar o arquivo novamente após o reinício (desde que o arquivamento ainda esteja habilitado). Quando um comando ou biblioteca de arquivamento encontra um arquivo pré-existente, deve retornar um status de zero ou `true`, respectivamente, se o arquivo WAL tiver conteúdos idênticos ao arquivo pré-existente e o arquivo pré-existente esteja totalmente persistido no armazenamento. Se um arquivo pré-existente contiver conteúdos diferentes dos do arquivo WAL que está sendo arquivado, o comando ou biblioteca de arquivamento *deve* retornar um status não nulo ou `false`, respectivamente.

O exemplo de comando acima para Unix evita sobrescrever um arquivo pré-existente, incluindo uma etapa separada `test`. Em algumas plataformas Unix, `cp` tem opções como `-i` que podem ser usadas para fazer a mesma coisa de forma menos verbose, mas você não deve confiar nelas sem verificar se o status de saída correto é retornado. (Em particular, o GNU `cp` retornará status zero quando `-i` é usado e o arquivo de destino já existe, o que *não* é o comportamento desejado.)

Ao projetar sua configuração de arquivamento, considere o que acontecerá se o comando ou a biblioteca de arquivamento falharem repetidamente, porque algum aspecto requer intervenção do operador ou o arquivo fica sem espaço. Por exemplo, isso pode ocorrer se você escrever em fita sem um autotrocador; quando a fita se enche, nada mais pode ser arquivado até que a fita seja trocada. Você deve garantir que qualquer condição de erro ou solicitação a um operador humano seja relatada adequadamente para que a situação possa ser resolvida de forma razoavelmente rápida. O diretório `pg_wal/` continuará a se preencher com arquivos de segmento WAL até que a situação seja resolvida. (Se o sistema de arquivos contendo `pg_wal/` ficar cheio, o PostgreSQL fará um desligamento PANIC. Nenhuma transação comprometida será perdida, mas o banco de dados permanecerá offline até que você libere algum espaço.)

A velocidade do comando ou biblioteca de arquivamento não é importante, desde que possa acompanhar a taxa média na qual seu servidor gera dados WAL. O funcionamento normal continua mesmo se o processo de arquivamento ficar um pouco atrasado. Se o arquivamento ficar significativamente atrasado, isso aumentará a quantidade de dados que seriam perdidos em caso de desastre. Isso também significará que o diretório `pg_wal/` conterá um grande número de arquivos de segmento ainda não arquivados, que eventualmente poderão exceder o espaço disponível no disco. Você é aconselhado a monitorar o processo de arquivamento para garantir que ele esteja funcionando conforme o que você pretende.

Ao escrever seu comando de arquivo ou biblioteca, você deve assumir que os nomes dos arquivos que serão arquivados podem ter até 64 caracteres e podem conter qualquer combinação de letras ASCII, dígitos e pontos. Não é necessário preservar o caminho relativo original (`%p`) mas é necessário preservar o nome do arquivo (`%f`).

Observe que, embora o arquivamento WAL permita restaurar quaisquer modificações feitas nos dados do seu banco de dados PostgreSQL, ele não restaurará as alterações feitas nos arquivos de configuração (ou seja, `postgresql.conf`, `pg_hba.conf` e `pg_ident.conf`) porque esses são editados manualmente e não por meio de operações SQL. Você pode querer manter os arquivos de configuração em um local que será respaldado pelos procedimentos regulares de backup do seu sistema de arquivos. Veja [Seção 19.2] para saber como reposicionar os arquivos de configuração.

O comando ou a função de arquivo é invocado apenas em segmentos WAL completos. Portanto, se o seu servidor gera pouco tráfego WAL (ou tem períodos de folga em que o faz), pode haver um longo atraso entre a conclusão de uma transação e sua gravação segura no armazenamento de arquivo. Para limitar a idade dos dados não arquivados, você pode definir [archive_timeout](runtime-config-wal.md#GUC-ARCHIVE-TIMEOUT) para forçar o servidor a alternar para um novo arquivo de segmento WAL pelo menos com essa frequência. Note que os arquivos arquivados que são arquivados precocemente devido a uma mudança forçada ainda têm o mesmo comprimento dos arquivos completamente cheios. Portanto, não é prudente definir um `archive_timeout` muito curto — isso fará com que seu armazenamento de arquivo se infla. As configurações de `archive_timeout` de cerca de um minuto são geralmente razoáveis.

Além disso, você pode forçar uma troca de segmento manualmente com `pg_switch_wal` se quiser garantir que uma transação recém-finalizada seja arquivada o mais rápido possível. Outras funções utilitárias relacionadas à gestão do WAL estão listadas em [Tabela 9.97](functions-admin.md#FUNCTIONS-ADMIN-BACKUP-TABLE).

Quando `wal_level` é `minimal`, alguns comandos SQL são otimizados para evitar o registro no WAL, conforme descrito em [Seção 14.4.7](populate.md#POPULATE-PITR). Se a arquivamento ou replicação em fluxo estiverem ativadas durante a execução de uma dessas declarações, o WAL não conterá informações suficientes para a recuperação do arquivo de arquivação. (A recuperação em caso de falha não é afetada). Por essa razão, `wal_level` só pode ser alterado no início do servidor. No entanto, `archive_command` e `archive_library` podem ser alterados com uma recarga do arquivo de configuração. Se você está arquivando via shell e deseja interromper temporariamente o arquivamento, uma maneira de fazer isso é definir `archive_command` como a string vazia (`''`). Isso fará com que os arquivos do WAL se acumulem em `pg_wal/` até que um `archive_command` funcional seja reestabelecido.

### 25.3.2. Fazer um backup de base [#](#BACKUP-BASE-BACKUP)

A maneira mais fácil de realizar um backup básico é usar a ferramenta [pg_basebackup](app-pgbasebackup.md). Ela pode criar um backup básico, seja em arquivos regulares ou em um arquivo tar. Se for necessário mais flexibilidade do que o [pg_basebackup](app-pgbasebackup.md) pode oferecer, você também pode fazer um backup básico usando a API de baixo nível (consulte [Seção 25.3.4](continuous-archiving.md#BACKUP-LOWLEVEL-BASE-BACKUP)).

Não é necessário se preocupar com o tempo que leva para fazer um backup básico. No entanto, se você normalmente executa o servidor com o `full_page_writes` desativado, você pode notar uma queda no desempenho enquanto o backup é executado, pois o `full_page_writes` é efetivamente forçado durante o modo de backup.

Para fazer uso do backup, você precisará manter todos os arquivos de segmento WAL gerados durante e após o backup do sistema de arquivos. Para ajudá-lo a fazer isso, o processo de backup de base cria um *arquivo de histórico de backup* que é armazenado imediatamente na área de arquivo WAL. Este arquivo é nomeado com base no primeiro arquivo de segmento WAL que você precisa para o backup do sistema de arquivos. Por exemplo, se o arquivo WAL inicial é `0000000100001234000055CD`, o arquivo de histórico de backup será nomeado algo como `0000000100001234000055CD.007C9330.backup`. (A segunda parte do nome do arquivo representa uma posição exata dentro do arquivo WAL, e normalmente pode ser ignorada.) Uma vez que você tenha arquivado com segurança o backup do sistema de arquivos e os arquivos de segmento WAL usados durante o backup (conforme especificado no arquivo de histórico de backup), todos os segmentos WAL arquivados com nomes numericamente menores não são mais necessários para recuperar o backup do sistema de arquivos e podem ser excluídos. No entanto, você deve considerar manter vários conjuntos de backup para ter certeza de que pode recuperar seus dados.

O arquivo de histórico de backup é apenas um pequeno arquivo de texto. Ele contém a string de rótulo que você deu para [pg_basebackup](app-pgbasebackup.md), além dos tempos de início e término e dos segmentos WAL do backup. Se você usou o rótulo para identificar o arquivo de dump associado, então o arquivo de histórico arquivado é suficiente para lhe dizer qual arquivo de dump deve ser restaurado.

Como você precisa manter todos os arquivos WAL arquivados até o seu último backup de base, o intervalo entre os backups de base geralmente deve ser escolhido com base no quanto de armazenamento você deseja gastar em arquivos WAL arquivados. Você também deve considerar quanto tempo está preparado para gastar na recuperação, se a recuperação for necessária — o sistema terá que reproduzir todos esses segmentos WAL, e isso pode levar algum tempo, se há muito tempo desde o último backup de base.

### 25.3.3. Fazer um backup incremental [#](#BACKUP-INCREMENTAL-BACKUP)

Você pode usar [pg_basebackup](app-pgbasebackup.md) para fazer um backup incremental, especificando a opção `--incremental`. Você deve fornecer, como argumento para `--incremental`, o manifesto de backup de um backup anterior do mesmo servidor. No backup resultante, os arquivos não relacionados serão incluídos na íntegra, mas alguns arquivos relacionados podem ser substituídos por arquivos incrementais menores que contêm apenas os blocos que foram alterados desde o backup anterior e metadados suficientes para reconstruir a versão atual do arquivo.

Para descobrir quais blocos precisam ser feitos backups, o servidor usa resumos WAL, que são armazenados no diretório de dados, dentro do diretório `pg_wal/summaries`. Se os arquivos de resumo necessários não estiverem presentes, uma tentativa de fazer um backup incremental falhará. Os resumos presentes neste diretório devem cobrir todos os LSNs do LSN inicial do backup anterior ao LSN inicial do backup atual. Como o servidor busca resumos WAL logo após estabelecer o LSN inicial do backup atual, os arquivos de resumo necessários provavelmente não estarão instantaneamente presentes no disco, mas o servidor aguardará a aparição de quaisquer arquivos ausentes. Isso também ajuda se o processo de sumarização WAL estiver atrasado. No entanto, se os arquivos necessários já tiverem sido removidos ou se o sumarizador WAL não estiver cumprindo o ritmo necessário, o backup incremental falhará.

Ao restaurar uma cópia incremental, será necessário ter não apenas a própria cópia incremental, mas também todos os backups anteriores que são necessários para fornecer os blocos omitidos da cópia incremental. Consulte [pg_combinebackup](app-pgcombinebackup.md) para obter mais informações sobre essa exigência. Observe que há restrições no uso de `pg_combinebackup` quando o status do checksum do clúster foi alterado; consulte [pg_combinebackup limitations](app-pgcombinebackup.md#APP-PGCOMBINEBACKUP-LIMITATIONS).

Observe que todos os requisitos para fazer uso de um backup completo também se aplicam a um backup incremental. Por exemplo, você ainda precisa de todos os arquivos de segmento WAL gerados durante e após o backup do sistema de arquivos, e quaisquer arquivos de histórico WAL relevantes. E você ainda precisa criar um `recovery.signal` (ou `standby.signal`) e realizar a recuperação, conforme descrito em [Seção 25.3.5](continuous-archiving.md#BACKUP-PITR-RECOVERY). O requisito de ter backups anteriores disponíveis no momento da restauração e de usar `pg_combinebackup` é um requisito adicional além de tudo o resto. Tenha em mente que o PostgreSQL não tem um mecanismo embutido para descobrir quais backups ainda são necessários como base para restaurar backups incrementais posteriores. Você deve acompanhar as relações entre seus backups completos e incrementais por conta própria e ter certeza de não remover backups anteriores se eles possam ser necessários ao restaurar backups incrementais posteriores.

Os backups incrementais geralmente só fazem sentido para bancos de dados relativamente grandes, onde uma parte significativa dos dados não muda ou muda apenas lentamente. Para um banco de dados pequeno, é mais simples ignorar a existência de backups incrementais e simplesmente fazer backups completos, que são mais fáceis de gerenciar. Para um grande banco de dados que é fortemente modificado, os backups incrementais não serão muito menores do que os backups completos.

Um backup incremental só é possível se a reprodução começar a partir de um ponto de verificação posterior do que o backup anterior do qual depende. Se você fizer o backup incremental no primário, essa condição é sempre satisfeita, porque cada backup desencadeia um novo ponto de verificação. Em um estado de espera, a reprodução começa a partir do ponto de reinício mais recente. Portanto, um backup incremental de um servidor em espera pode falhar se houver havido muito pouca atividade desde o backup anterior, pois pode não ter sido criado nenhum novo ponto de reinício.

### 25.3.4. Fazer um backup de base usando a API de nível baixo [#](#BACKUP-LOWLEVEL-BASE-BACKUP)

Em vez de fazer um backup completo ou incremental usando [pg_basebackup](app-pgbasebackup.md), você pode fazer um backup de base usando a API de nível baixo. Esse procedimento contém alguns passos adicionais em relação ao método pg_basebackup, mas é relativamente simples. É muito importante que esses passos sejam executados em sequência e que o sucesso de um passo seja verificado antes de prosseguir para o próximo passo.

É possível executar múltiplos backups simultaneamente (tanto os iniciados usando essa API de backup quanto os iniciados usando [pg_basebackup](app-pgbasebackup.md)).

1. Certifique-se de que o arquivamento WAL esteja habilitado e funcionando.
2. Conecte-se ao servidor (não importa qual banco de dados) como um usuário com direitos para executar `pg_backup_start` (superusuário ou um usuário que tenha sido concedido `EXECUTE` na função) e emita o comando:

```
SELECT pg_backup_start(label => 'label', fast => false);
```

onde `label` é qualquer string que você deseja usar para identificar de forma única essa operação de backup. A conexão que chama `pg_backup_start` deve ser mantida até o final do backup, ou o backup será automaticamente abortado.

Os backups online são sempre iniciados no início de um ponto de verificação. Por padrão, `pg_backup_start` aguardará o próximo ponto de verificação regularmente agendado para ser concluído, o que pode levar um longo tempo (consulte os parâmetros de configuração [checkpoint_timeout](runtime-config-wal.md#GUC-CHECKPOINT-TIMEOUT) e [checkpoint_completion_target](runtime-config-wal.md#GUC-CHECKPOINT-COMPLETION-TARGET)). Isso geralmente é preferível, pois minimiza o impacto no sistema em execução. Se você deseja iniciar o backup o mais rápido possível, passe `true` como o segundo parâmetro para `pg_backup_start` e ele solicitará um ponto de verificação imediato, que será concluído o mais rápido possível, usando o máximo de I/O possível.
3. Realize o backup, usando qualquer ferramenta de backup de sistema de arquivos conveniente, como tar ou cpio (não pg_dump ou pg_dumpall). Não é necessário nem desejável interromper a operação normal do banco de dados enquanto isso. Consulte [Seção 25.3.4.1](continuous-archiving.md#BACKUP-LOWLEVEL-BASE-BACKUP-DATA) para as coisas a considerar durante este backup.
4. Na mesma conexão do antes, emita o comando:

```
SELECT * FROM pg_backup_stop(wait_for_archive => true);
```

Isso termina o modo de backup. Em um primário, também realiza uma mudança automática para o próximo segmento WAL. Em um de espera, não é possível mudar automaticamente os segmentos WAL, então você pode querer executar `pg_switch_wal` no primário para realizar uma mudança manual. A razão para a mudança é para garantir que o último arquivo do segmento WAL escrito durante o intervalo de backup esteja pronto para arquivar.

`pg_backup_stop` retornará uma linha com três valores. O segundo desses campos deve ser escrito em um arquivo chamado `backup_label` no diretório raiz do backup. O terceiro campo deve ser escrito em um arquivo chamado `tablespace_map`, a menos que o campo esteja vazio. Esses arquivos são vitais para o funcionamento do backup e devem ser escritos caracter a caractere, sem modificações, o que pode exigir a abertura do arquivo no modo binário.

Se o processo de backup monitorar e garantir que todos os arquivos de segmento WAL necessários para o backup sejam arquivados com sucesso, o parâmetro `wait_for_archive` (que tem o valor padrão verdadeiro) pode ser definido como falso para que `pg_backup_stop` seja retornado assim que o registro de parada do backup for escrito no WAL. Por padrão, `pg_backup_stop` aguardará até que todo o WAL seja arquivado, o que pode levar algum tempo. Esta opção deve ser usada com cautela: se o arquivamento do WAL não for monitorado corretamente, o backup pode não incluir todos os arquivos do WAL e, portanto, será incompleto e não poderá ser restaurado.

#### 25.3.4.1. Fazer backup do diretório de dados [#](#BACKUP-LOWLEVEL-BASE-BACKUP-DATA)

Algumas ferramentas de backup de sistemas de arquivos emitem avisos ou erros se os arquivos que estão tentando copiar mudarem enquanto a cópia prossegue. Ao fazer um backup de base de um banco de dados ativo, essa situação é normal e não um erro. No entanto, você precisa garantir que possa distinguir queixas desse tipo de erros reais. Por exemplo, algumas versões do rsync retornam um código de saída separado para "arquivos de origem desaparecidos", e você pode escrever um script de driver para aceitar esse código de saída como um caso sem erro. Além disso, algumas versões do GNU tar retornam um código de erro indistinguível de um erro fatal se um arquivo foi truncado enquanto o tar estava copiando-o. Felizmente, as versões do GNU tar 1.16 e posteriores saem com 1 se um arquivo foi alterado durante o backup, e 2 para outros erros. Com a versão do GNU tar 1.23 e posterior, você pode usar as opções de aviso [[`--warning=no-file-changed --warning=no-file-removed`] para ocultar as mensagens de aviso relacionadas.

Certifique-se de que seu backup inclui todos os arquivos sob o diretório do clúster de banco de dados (por exemplo, `/usr/local/pgsql/data`). Se você estiver usando espaços de tabela que não estejam sob este diretório, tenha cuidado para incluí-los também (e certifique-se de que seus arquivos de backup criem links simbólicos como links, caso contrário, o restabelecimento corromperá seus espaços de tabela).

No entanto, você deve omitir os arquivos dentro do subdiretório `pg_wal/` do cluster. Esse pequeno ajuste é importante porque reduz o risco de erros durante a restauração. Isso é fácil de organizar se `pg_wal/` for um link simbólico apontando para algum lugar fora do diretório do cluster, o que é uma configuração comum de qualquer forma por razões de desempenho. Você também pode querer excluir `postmaster.pid` e `postmaster.opts`, que registram informações sobre o postmaster em execução, não sobre o postmaster que eventualmente usará este backup. (Esses arquivos podem confundir o pg_ctl.)

Muitas vezes, também é uma boa ideia omitir dos backups os arquivos dentro do diretório `pg_replslot/` do clúster, para que as faixas de replicação que existem no primário não se tornem parte do backup. Caso contrário, o uso subsequente do backup para criar um standby pode resultar na retenção indefinida dos arquivos WAL no standby, e possivelmente no aumento do tamanho do primário se o feedback de standby quente estiver habilitado, porque os clientes que estão usando essas faixas de replicação ainda estarão se conectando e atualizando as faixas no primário, não no standby. Mesmo que o backup seja destinado apenas para uso na criação de um novo primário, espera-se que a cópia das faixas de replicação não seja particularmente útil, uma vez que o conteúdo dessas faixas provavelmente estará muito desatualizado no momento em que o novo primário entrar em operação.

Os conteúdos dos diretórios `pg_dynshmem/`, `pg_notify/`, `pg_serial/`, `pg_snapshots/`, `pg_stat_tmp/` e `pg_subtrans/` (mas não os próprios diretórios) podem ser omitidos do backup, pois serão inicializados na inicialização do postmaster.

Qualquer arquivo ou diretório que comece com `pgsql_tmp` pode ser omitido do backup. Esses arquivos são removidos no início do postmaster e os diretórios serão recriados conforme necessário.

Os arquivos `pg_internal.init` podem ser omitidos do backup sempre que um arquivo com esse nome for encontrado. Esses arquivos contêm dados de cache de relação que são sempre reconstruídos durante a recuperação.

O arquivo de rótulo de backup inclui a string de rótulo que você forneceu para `pg_backup_start`, além do horário em que `pg_backup_start` foi executado e o nome do arquivo WAL inicial. Em caso de confusão, é possível, portanto, examinar um arquivo de backup e determinar exatamente de qual sessão de backup o arquivo de dump veio. O arquivo de mapa de tablespace inclui os nomes dos links simbólicos conforme eles existem no diretório [[`pg_tblspc/`] e o caminho completo de cada link simbólico. Esses arquivos não são apenas para sua informação; sua presença e conteúdo são críticos para o funcionamento adequado do processo de recuperação do sistema.

Também é possível fazer um backup enquanto o servidor está parado. Nesse caso, você obviamente não pode usar `pg_backup_start` ou `pg_backup_stop`, e, portanto, você será obrigado a usar seus próprios dispositivos para acompanhar qual backup é qual e até onde os arquivos WAL associados vão. Geralmente é melhor seguir o procedimento de arquivamento contínuo acima.

### 25.3.5. Recuperação usando um backup de arquivo contínuo [#](#BACKUP-PITR-RECOVERY)

Tudo bem, o pior já aconteceu e você precisa se recuperar de seu backup. Aqui está o procedimento:

1. Parta o servidor, se ele estiver em execução.
2. Se tiver espaço para fazê-lo, copie todo o diretório de dados do cluster e quaisquer espaços de tabelas para um local temporário, caso precise deles mais tarde. Note que essa precaução exigirá que você tenha espaço livre suficiente no seu sistema para manter duas cópias do seu banco de dados existente. Se não tiver espaço suficiente, você deve, pelo menos, salvar o conteúdo do subdiretório `pg_wal` do cluster, pois ele pode conter arquivos WAL que não foram arquivados antes do sistema falhar.
3. Remova todos os arquivos e subdiretórios existentes sob o diretório de dados do cluster e sob os diretórios raiz de quaisquer espaços de tabelas que você está usando.
4. Se estiver restaurando um backup completo, você pode restaurar os arquivos do banco de dados diretamente nos diretórios de destino. Certifique-se de que eles sejam restaurados com a propriedade correta (o usuário do sistema do banco de dados, não `root`!) e com as permissões corretas. Se estiver usando espaços de tabelas, você deve verificar se os links simbólicos em `pg_tblspc/` foram restaurados corretamente.
5. Se estiver restaurando um backup incremental, você precisará restaurar o backup incremental e todos os backups anteriores sobre os quais ele depende diretamente ou indiretamente para a máquina onde você está realizando a restauração. Esses backups precisarão ser colocados em diretórios separados, não nos diretórios de destino onde você deseja que o servidor em execução termine. Uma vez feito isso, use [pg_combinebackup](app-pgcombinebackup.md "pg_combinebackup") para extrair dados do backup completo e de todos os backups incrementais subsequentes e escreva um backup sintético completo nos diretórios de destino. Como acima, verifique se as permissões e os links de espaço de tabela estão corretos.
6. Remova quaisquer arquivos presentes em `pg_wal/`; esses vieram do backup do sistema de arquivos e, portanto, provavelmente são obsoletos em vez de atuais. Se não arquivar `pg_wal/` de forma alguma, então recriá-lo com as permissões adequadas, sendo cuidadoso para garantir que o reestabeleça como um link simbólico se o configurou dessa maneira antes.
7. Se tiver arquivos de segmento WAL não arquivados que você salvou no passo 2, copie-os em `pg_wal/`. (É melhor copiá-los, não movê-los, para que você ainda tenha os arquivos não modificados se ocorrer um problema e você tiver que começar novamente.)
8. Defina as configurações de configuração de recuperação em `postgresql.conf` (veja [Seção 19.5.5](runtime-config-wal.md#RUNTIME-CONFIG-WAL-ARCHIVE-RECOVERY "19.5.5. Archive Recovery")) e crie um arquivo `recovery.signal` no diretório de dados do cluster. Você também pode querer modificar temporariamente `pg_hba.conf` para impedir que usuários comuns se conectem até que você esteja certo de que a recuperação foi bem-sucedida.
9. Inicie o servidor. O servidor entrará no modo de recuperação e prosseguirá lendo os arquivos WAL arquivados que precisa. Se a recuperação for terminada por um erro externo, o servidor pode simplesmente ser reiniciado e continuará a recuperação. Após a conclusão do processo de recuperação, o servidor removerá `recovery.signal` (para evitar reentrar acidentalmente no modo de recuperação mais tarde) e então começará as operações normais do banco de dados.
10. Inspecione o conteúdo do banco de dados para garantir que você tenha recuperado para o estado desejado. Se não, retorne ao passo 1. Se tudo estiver bem, permita que seus usuários se conectem restaurando `pg_hba.conf` para o normal.

A parte fundamental de tudo isso é configurar uma configuração de recuperação que descreva como você deseja recuperar e até onde a recuperação deve ser realizada. A única coisa que você deve especificar absolutamente é o `restore_command`, que informa ao PostgreSQL como recuperar segmentos de arquivos WAL arquivados. Assim como o `archive_command`, este é uma string de comando de shell. Ele pode conter `%f`, que é substituído pelo nome do arquivo WAL desejado, e `%p`, que é substituído pelo nome do caminho para copiar o arquivo WAL. (O nome do caminho é relativo ao diretório de trabalho atual, ou seja, o diretório de dados do cluster.) Escreva `%%` se você precisar incorporar um caractere real `%` no comando. O comando mais simples e útil é algo como:

```
restore_command = 'cp /mnt/server/archivedir/%f %p'
```

que copiará os segmentos WAL arquivados anteriormente do diretório `/mnt/server/archivedir`. Claro, você pode usar algo muito mais complicado, talvez até um script de shell que peça ao operador para montar uma fita apropriada.

É importante que o comando retorne um status de saída não nulo em caso de falha. O comando *deverá* ser chamado solicitando arquivos que não estão presentes no arquivo; ele deve retornar não nulo quando assim solicitado. Isso não é uma condição de erro. Uma exceção é que, se o comando foi encerrado por um sinal (diferente de SIGTERM, que é usado como parte de um desligamento do servidor de banco de dados) ou por um erro pelo shell (como comando não encontrado), então a recuperação será interrompida e o servidor não será iniciado.

Nem todos os arquivos solicitados serão arquivos de segmento WAL; você também deve esperar solicitações para arquivos com um sufixo de `.history`. Além disso, esteja ciente de que o nome base do caminho `%p` será diferente de `%f`; não espere que eles sejam intercambiáveis.

Os segmentos que não podem ser encontrados no arquivo serão procurados em `pg_wal/`; isso permite o uso de segmentos recentes não arquivados. No entanto, os segmentos disponíveis no arquivo serão usados em preferência aos arquivos em `pg_wal/`.

Normalmente, a recuperação prosseguirá por todos os segmentos WAL disponíveis, restaurando o banco de dados ao ponto atual (ou o mais próximo possível, dado os segmentos WAL disponíveis). Portanto, uma recuperação normal terminará com uma mensagem de “arquivo não encontrado”, o texto exato da mensagem de erro, dependendo da sua escolha de `restore_command`. Você também pode ver uma mensagem de erro no início da recuperação para um arquivo com um nome como `00000001.history`. Isso também é normal e não indica um problema em situações de recuperação simples; consulte [Seção 25.3.6](continuous-archiving.md#BACKUP-TIMELINES) para discussão.

Se você deseja recuperar a um ponto anterior (digamos, logo antes de o DBA júnior ter descartado sua tabela de transação principal), basta especificar o ponto de parada necessário (runtime-config-wal.md#RUNTIME-CONFIG-WAL-RECOVERY-TARGET "19.5.6. Recovery Target"). Você pode especificar o ponto de parada, conhecido como "ponto de recuperação", por data/hora, ponto de restauração nomeado ou pelo término de um ID de transação específico. A partir deste texto, as opções de data/hora e ponto de restauração nomeado são muito úteis, pois não há ferramentas que ajudem a identificar com precisão qual ID de transação deve ser usado.

Nota

O ponto de parada deve ser após o horário de término do backup básico, ou seja, o horário de término de `pg_backup_stop`. Você não pode usar um backup básico para recuperar um momento em que esse backup estava em andamento. (Para recuperar para esse momento, você deve voltar ao seu backup básico anterior e avançar a partir daí.)

Se a recuperação encontrar dados WAL corrompidos, a recuperação será interrompida nesse ponto e o servidor não será iniciado. Nesse caso, o processo de recuperação pode ser executado novamente do início, especificando um "alvo de recuperação" antes do ponto de corrupção, para que a recuperação possa ser completada normalmente. Se a recuperação falhar por um motivo externo, como um travamento do sistema ou se o arquivo WAL se tornar inacessível, a recuperação pode ser simplesmente reiniciada e será reiniciada quase onde falhou. O reinício da recuperação funciona de maneira muito semelhante ao checkpointing em operação normal: o servidor força periodicamente todo seu estado no disco e, em seguida, atualiza o arquivo `pg_control` para indicar que os dados WAL já processados não precisam ser verificados novamente.

### 25.3.6. Cronogramas [#](#BACKUP-TIMELINES)

A capacidade de restaurar o banco de dados a um ponto anterior do tempo cria algumas complexidades que se assemelham a histórias de ficção científica sobre viagens no tempo e universos paralelos. Por exemplo, na história original do banco de dados, suponha que você tenha perdido uma tabela crítica às 17:15 do dia de terça-feira à noite, mas não tenha percebido seu erro até o meio-dia de quarta-feira. Sem se importar, você pega seu backup, restaura ao ponto no tempo das 17:14 da terça-feira à noite e está pronto. Neste *histórico* do universo do banco de dados, você nunca perdeu a tabela. Mas suponha que você perceba mais tarde que essa não foi uma ótima ideia e que gostaria de retornar a algum momento da manhã de quarta-feira na história original. Você não poderá fazer isso, pois, enquanto seu banco de dados estava funcionando, ele sobrescreveu alguns dos arquivos dos segmentos WAL que levaram até o momento em que agora gostaria de poder voltar. Assim, para evitar isso, você precisa distinguir a série de registros WAL gerados após ter feito uma recuperação no ponto no tempo daquela data.

Para lidar com esse problema, o PostgreSQL tem uma noção de *cronogramas*. Sempre que uma recuperação de arquivo é concluída, um novo cronograma é criado para identificar a série de registros WAL gerados após essa recuperação. O número de ID do cronograma faz parte dos nomes dos arquivos de segmento WAL, então um novo cronograma não sobrescreve os dados WAL gerados por cronogramas anteriores. Por exemplo, no nome do arquivo WAL `0000000100001234000055CD`, o prefixo `00000001` é o ID do cronograma em hexadecimal. (Observe que, em outros contextos, como mensagens de log do servidor, os IDs do cronograma geralmente são impressos em decimal.)

De fato, é possível arquivar muitas diferentes linhas do tempo. Embora isso possa parecer uma característica inútil, muitas vezes é uma salvação. Considere a situação em que você não tem certeza de qual ponto no tempo deve recuperar, e, portanto, precisa fazer várias recuperações em pontos no tempo por tentativa e erro até encontrar o melhor lugar para se ramificar a partir da história antiga. Sem linhas do tempo, esse processo logo geraria uma confusão incontrolável. Com linhas do tempo, você pode recuperar *qualquer* estado anterior, incluindo estados em ramos de linha do tempo que você abandonou anteriormente.

Toda vez que uma nova linha cronológica é criada, o PostgreSQL cria um arquivo de "histórico de linha cronológica" que mostra de qual linha cronológica ela se ramificou e quando. Esses arquivos de histórico são necessários para permitir que o sistema escolha os arquivos de segmento WAL corretos ao recuperar de um arquivo que contém várias linhas cronológicas. Portanto, eles são arquivados na área de arquivo WAL, assim como os arquivos de segmento WAL. Os arquivos de histórico são apenas pequenos arquivos de texto, então é barato e apropriado mantê-los indefinidamente (ao contrário dos arquivos de segmento, que são grandes). Você pode, se desejar, adicionar comentários a um arquivo de histórico para registrar suas próprias notas sobre como e por que essa linha cronológica específica foi criada. Tais comentários serão especialmente valiosos quando você tiver uma densa rede de diferentes linhas cronológicas como resultado de experimentação.

O comportamento padrão de recuperação é recuperar para o cronograma mais recente encontrado no arquivo. Se você deseja recuperar para o cronograma que estava em vigor quando o backup de base foi feito ou para um cronograma específico (ou seja, você deseja retornar a algum estado que foi gerado após uma tentativa de recuperação), você precisa especificar `current` ou o ID do cronograma de destino em [recovery_target_timeline](runtime-config-wal.md#GUC-RECOVERY-TARGET-TIMELINE). Não é possível recuperar para cronogramas que se ramificaram anteriormente que o backup de base.

### 25.3.7. Dicas e exemplos [#](#BACKUP-TIPS)

Aqui estão algumas dicas para configurar a arquivamento contínuo.

#### 25.3.7.1. Resgate quente independente [#](#BACKUP-STANDALONE)

É possível usar as facilidades de backup do PostgreSQL para produzir backups quentes independentes. Estes são backups que não podem ser usados para recuperação em um ponto no tempo, mas geralmente são muito mais rápidos de fazer backup e restaurar do que os backups do pg_dump. (Eles também são muito maiores do que os backups do pg_dump, então, em alguns casos, a vantagem de velocidade pode ser negada.)

Assim como os backups básicos, a maneira mais fácil de produzir um backup quente independente é usar a ferramenta [pg_basebackup](app-pgbasebackup.md). Se você incluir o parâmetro `-X` ao chamá-la, todos os registros de pré-escrita necessários para usar o backup serão incluídos automaticamente no backup, e não é necessária nenhuma ação especial para restaurar o backup.

#### 25.3.7.2. Registros de Arquivo Compactado [#](#COMPRESSED-ARCHIVE-LOGS)

Se o tamanho do armazenamento do arquivo é uma preocupação, você pode usar gzip para comprimir os arquivos do arquivo:

```
archive_command = 'gzip < %p > /mnt/server/archivedir/%f.gz'
```

Você precisará, então, usar gunzip durante a recuperação:

```
restore_command = 'gunzip < /mnt/server/archivedir/%f.gz > %p'
```

#### 25.3.7.3. `archive_command` Scripts [#](#BACKUP-SCRIPTS)

Muitas pessoas optam por usar scripts para definir seu `archive_command`, de modo que sua entrada no `postgresql.conf` pareça muito simples:

```
archive_command = 'local_backup_script.sh "%p" "%f"'
```

É aconselhável usar um arquivo de script separado sempre que você quiser usar mais de um comando no processo de arquivamento. Isso permite que toda a complexidade seja gerenciada dentro do script, que pode ser escrito em um idioma de script popular, como bash ou perl.

Exemplos de requisitos que podem ser resolvidos dentro de um script incluem:

* Copiar dados para armazenamento de dados fora do local
* Agrupar arquivos WAL para que sejam transferidos a cada três horas, em vez de um de cada vez
* Interagir com outros softwares de backup e recuperação
* Interagir com software de monitoramento para relatar erros

DICA

Ao usar um script `archive_command`, é desejável habilitar [logging_collector](runtime-config-logging.md#GUC-LOGGING-COLLECTOR). Quaisquer mensagens escritas no stderr do script aparecerão, então, no log do servidor de banco de dados, permitindo que configurações complexas sejam diagnosticadas facilmente se elas falharem.

### 25.3.8. Avisos [#](#CONTINUOUS-ARCHIVING-CAVEATS)

Neste momento, há várias limitações da técnica de arquivamento contínuo. Essas limitações provavelmente serão corrigidas em versões futuras:

* Se um comando `CREATE DATABASE`](sql-createdatabase.md "CREATE DATABASE") for executado enquanto uma cópia de segurança de base está sendo feita, e depois o banco de dados de modelo que o `CREATE DATABASE` copiou for modificado enquanto a cópia de segurança de base ainda está em andamento, é possível que a recuperação cause essas modificações a serem propagadas também no banco de dados criado. Isso, é claro, é indesejável. Para evitar esse risco, é melhor não modificar quaisquer bancos de dados de modelo enquanto está sendo feita uma cópia de segurança de base.
* Os comandos `CREATE TABLESPACE`](sql-createtablespace.md "CREATE TABLESPACE") são registrados no WAL com o caminho absoluto literal e, portanto, serão regravados como criações de espaço de tabela com o mesmo caminho absoluto. Isso pode ser indesejável se o WAL estiver sendo regravado em uma máquina diferente. Pode ser perigoso mesmo se o WAL estiver sendo regravado na mesma máquina, mas em um novo diretório de dados: a regra ainda sobrescreverá o conteúdo do espaço de tabela original. Para evitar possíveis armadilhas desse tipo, a melhor prática é fazer uma nova cópia de segurança de base após criar ou descartar espaços de tabela.

Também deve ser observado que o formato WAL padrão é bastante volumoso, pois inclui muitos snapshots de página de disco. Esses snapshots de página são projetados para suportar a recuperação em caso de falha, uma vez que podemos precisar corrigir páginas de disco parcialmente escritas. Dependendo do hardware e do software do seu sistema, o risco de escritas parciais pode ser pequeno o suficiente para ser ignorado, caso em que você pode reduzir significativamente o volume total dos arquivos WAL arquivados, desligando os snapshots de página usando o parâmetro [full_page_writes](runtime-config-wal.md#GUC-FULL-PAGE-WRITES). (Leia as notas e avisos em [Capítulo 28](wal.md) antes de fazer isso.) Desligar os snapshots de página não impede o uso do WAL para operações PITR. Uma área para desenvolvimento futuro é comprimir os dados WAL arquivados, removendo cópias de página desnecessárias, mesmo quando `full_page_writes` está ativado. Enquanto isso, os administradores podem desejar reduzir o número de snapshots de página incluídos no WAL, aumentando os parâmetros do intervalo de verificação o máximo possível.