## 18.4. Gerenciamento de Recursos do Kernel [#](#KERNEL-RESOURCES)

* [18.4.1. Memória compartilhada e semaforos](kernel-resources.md#SYSVIPC)
* [18.4.2. RemoveIPC do systemd](kernel-resources.md#SYSTEMD-REMOVEIPC)
* [18.4.3. Limites de recursos](kernel-resources.md#KERNEL-RESOURCES-LIMITS)
* [18.4.4. Sobrecommit de memória no Linux](kernel-resources.md#LINUX-MEMORY-OVERCOMMIT)
* [18.4.5. Páginas enormes no Linux](kernel-resources.md#LINUX-HUGE-PAGES)

O PostgreSQL pode, às vezes, esgotar vários limites de recursos do sistema operacional, especialmente quando várias cópias do servidor estão em execução no mesmo sistema ou em instalações muito grandes. Esta seção explica os recursos do kernel utilizados pelo PostgreSQL e os passos que você pode tomar para resolver problemas relacionados ao consumo de recursos do kernel.

### 18.4.1. Memória compartilhada e semaforos [#](#SYSVIPC)

O PostgreSQL exige que o sistema operacional forneça recursos de comunicação entre processos (IPC), especificamente memória compartilhada e semaforos. Sistemas derivados do Unix geralmente fornecem IPC do tipo “System V”, IPC “POSIX” ou ambos. O Windows tem sua própria implementação desses recursos e não é discutido aqui.

Por padrão, o PostgreSQL aloca uma quantidade muito pequena de memória compartilhada do Sistema V, além de uma quantidade muito maior de memória compartilhada anônima `mmap`. Alternativamente, uma única região grande de memória compartilhada do Sistema V pode ser usada (consulte [shared_memory_type](runtime-config-resource.md#GUC-SHARED-MEMORY-TYPE)). Além disso, um número significativo de semaforos, que podem ser do tipo Sistema V ou POSIX, são criados no início do servidor. Atualmente, os semaforos POSIX são usados em sistemas Linux e FreeBSD, enquanto outras plataformas usam semaforos do Sistema V.

As características do Sistema V IPC são tipicamente limitadas por limites de alocação em todo o sistema. Quando o PostgreSQL excede um desses limites, o servidor se recusará a iniciar e deverá deixar uma mensagem de erro instrutiva descrevendo o problema e o que fazer a respeito. (Veja também [Seção 18.3.1] (server-start.md#SERVER-START-FAILURES "18.3.1. Server Start-up Failures"). Os parâmetros relevantes do kernel são nomeados de forma consistente em diferentes sistemas; [Tabela 18.1] (kernel-resources.md#SYSVIPC-PARAMETERS "Table 18.1. System V IPC Parameters") dá uma visão geral. Os métodos para configurá-los, no entanto, variam. Sugestões para algumas plataformas são dadas abaixo.

**Tabela 18.1. Parâmetros do sistema V IPC**



<table border="1" class="table" summary="System V IPC Parameters">
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
    Descrição
   </th>
   <th>
    Valores necessários para executar um
    <span class="productname">
     PostgreSQL
    </span>
    exemplo
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <code class="varname">
     SHMMAX
    </code>
   </td>
   <td>
    Tamanho máximo do segmento de memória compartilhada (bytes)
   </td>
   <td>
    pelo menos 1 kB, mas o padrão geralmente é muito maior
   </td>
  </tr>
  <tr>
   <td>
    <code class="varname">
     SHMMIN
    </code>
   </td>
   <td>
    Tamanho mínimo do segmento de memória compartilhada (bytes)
   </td>
   <td>
    1
   </td>
  </tr>
  <tr>
   <td>
    <code class="varname">
     SHMALL
    </code>
   </td>
   <td>
    Quantidade total de memória compartilhada disponível (bytes ou páginas)
   </td>
   <td>
    mesmo que
    <code class="varname">
     SHMMAX
    </code>
    se são bytes,
    <code class="literal">
     ceil(SHMMAX/PAGE_SIZE)
    </code>
    se páginas, além de espaço para outras aplicações
   </td>
  </tr>
  <tr>
   <td>
    <code class="varname">
     SHMSEG
    </code>
   </td>
   <td>
    Número máximo de segmentos de memória compartilhada por processo
   </td>
   <td>
    só é necessário um segmento, mas o padrão é muito maior
   </td>
  </tr>
  <tr>
   <td>
    <code class="varname">
     SHMMNI
    </code>
   </td>
   <td>
    Número máximo de segmentos de memória compartilhada em todo o sistema
   </td>
   <td>
    como
    <code class="varname">
     SHMSEG
    </code>
    mais espaço para outras aplicações
   </td>
  </tr>
  <tr>
   <td>
    <code class="varname">
     SEMMNI
    </code>
   </td>
   <td>
    Número máximo de identificadores de semaforos (ou seja, conjuntos)
   </td>
   <td>
    pelo menos
    <code class="literal">
     ceil(num_os_semaphores / 16)
    </code>
    mais espaço para outras aplicações
   </td>
  </tr>
  <tr>
   <td>
    <code class="varname">
     SEMMNS
    </code>
   </td>
   <td>
    Número máximo de semaforos em todo o sistema
   </td>
   <td>
    <code class="literal">
     ceil(num_os_semaphores / 16) * 17
    </code>
    mais espaço para outras aplicações
   </td>
  </tr>
  <tr>
   <td>
    <code class="varname">
     SEMMSL
    </code>
   </td>
   <td>
    Número máximo de semaforos por conjunto
   </td>
   <td>
    pelo menos 17
   </td>
  </tr>
  <tr>
   <td>
    <code class="varname">
     SEMMAP
    </code>
   </td>
   <td>
    Número de entradas no mapa do semaforo
   </td>
   <td>
    ver texto
   </td>
  </tr>
  <tr>
   <td>
    <code class="varname">
     SEMVMX
    </code>
   </td>
   <td>
    Valor máximo do semaforo
   </td>
   <td>
    pelo menos 1000 (o padrão é geralmente 32767; não altere a menos que seja necessário)
   </td>
  </tr>
 </tbody>
</table>









O PostgreSQL requer alguns bytes de memória compartilhada do Sistema V (tipicamente 48 bytes, em plataformas de 64 bits) para cada cópia do servidor. Na maioria dos sistemas operacionais modernos, essa quantidade pode ser facilmente alocada. No entanto, se você estiver executando muitas cópias do servidor ou se estiver explicitamente configurando o servidor para usar grandes quantidades de memória compartilhada do Sistema V (consulte [shared_memory_type](runtime-config-resource.md#GUC-SHARED-MEMORY-TYPE) e [dynamic_shared_memory_type](runtime-config-resource.md#GUC-DYNAMIC-SHARED-MEMORY-TYPE)), pode ser necessário aumentar `SHMALL`, que é a quantidade total de memória compartilhada do Sistema V em todo o sistema. Note que `SHMALL` é medido em páginas, em vez de bytes, em muitos sistemas.

Menos provável de causar problemas é o tamanho mínimo para segmentos de memória compartilhada (`SHMMIN`), que deve ser no máximo aproximadamente 32 bytes para o PostgreSQL (geralmente é apenas 1). O número máximo de segmentos em todo o sistema (`SHMMNI`) ou por processo (`SHMSEG`) é improvável de causar um problema, a menos que seu sistema os tenha configurados como zero.

Ao usar semaforos do Sistema V, o PostgreSQL usa um semaforo por conexão permitida ([max_connections](runtime-config-connection.md#GUC-MAX-CONNECTIONS)), processo de trabalhador de autoajuste permitido ([autovacuum_worker_slots](runtime-config-vacuum.md#GUC-AUTOVACUUM-WORKER-SLOTS)), processo de emissor de WAL permitido ([max_wal_senders](runtime-config-replication.md#GUC-MAX-WAL-SENDERS)), processo de fundo permitido ([max_worker_processes](runtime-config-resource.md#GUC-MAX-WORKER-PROCESSES)), etc., em conjuntos de 16. O parâmetro calculado em tempo de execução [num_os_semaphores](runtime-config-preset.md#GUC-NUM-OS-SEMAPHORES) relata o número de semaforos necessários. Esse parâmetro pode ser visualizado antes de iniciar o servidor com um comando como:

```
$ postgres -D $PGDATA -C num_os_semaphores
```

Cada conjunto de 16 semaforos também conterá um sétimo semaforo que contém um “número mágico”, para detectar colisões com conjuntos de semaforos utilizados por outras aplicações. O número máximo de semaforos no sistema é definido por `SEMMNS`, que, consequentemente, deve ser pelo menos tão alto quanto `num_os_semaphores` mais um adicional para cada conjunto de 16 semaforos necessários (ver a fórmula em [Tabela 18.1](kernel-resources.md#SYSVIPC-PARAMETERS)). O parâmetro `SEMMNI` determina o limite do número de conjuntos de semaforos que podem existir no sistema de uma só vez. Portanto, esse parâmetro deve ser pelo menos `ceil(num_os_semaphores / 16)`. Reduzir o número de conexões permitidas é uma solução temporária para falhas, que geralmente são formuladas de forma confusa como “Não há espaço disponível no dispositivo”, da função `semget`.

Em alguns casos, também pode ser necessário aumentar `SEMMAP` para pelo menos o valor de `SEMMNS`. Se o sistema tiver esse parâmetro (muitos não o têm), ele define o tamanho do mapa de recursos de semaforos, no qual cada bloco contíguo de semaforos disponíveis precisa de uma entrada. Quando um conjunto de semaforos é liberado, ele é adicionado a uma entrada existente que é adjacente ao bloco liberado ou é registrado sob uma nova entrada do mapa. Se o mapa estiver cheio, os semaforos liberados são perdidos (até o reinício). A fragmentação do espaço de semaforos pode, com o tempo, levar a menos semaforos disponíveis do que o necessário.

Outros vários ajustes relacionados a “undo de semaforo”, como `SEMMNU` e `SEMUME`, não afetam o PostgreSQL.

Ao usar semaforos POSIX, o número de semaforos necessários é o mesmo que para o System V, ou seja, um semaforo por conexão permitida ([max_connections](runtime-config-connection.md#GUC-MAX-CONNECTIONS)), processo de trabalhador de autovacuum permitido ([autovacuum_worker_slots](runtime-config-vacuum.md#GUC-AUTOVACUUM-WORKER-SLOTS)), processo de emissor de WAL permitido ([max_wal_senders](runtime-config-replication.md#GUC-MAX-WAL-SENDERS)), processo de fundo permitido ([max_worker_processes](runtime-config-resource.md#GUC-MAX-WORKER-PROCESSES)), etc. Nas plataformas onde essa opção é preferida, não há um limite específico do kernel sobre o número de semaforos POSIX.

FreeBSD: As configurações padrão de memória compartilhada geralmente são suficientes, a menos que você tenha definido `shared_memory_type` para `sysv`. Semaforos do System V não são usados nesta plataforma.

As configurações padrão do IPC podem ser alteradas usando as interfaces `sysctl` ou `loader`. Os seguintes parâmetros podem ser definidos usando `sysctl`:

```
# sysctl kern.ipc.shmall=32768 # sysctl kern.ipc.shmmax=134217728
```

Para que essas configurações persistem após as reinicializações, modifique `/etc/sysctl.conf`.

Se você configurou `shared_memory_type` para `sysv`, talvez queira também configurar seu kernel para bloquear a memória compartilhada do System V na RAM e impedir que ela seja mapeada para o swap. Isso pode ser feito usando a configuração `sysctl` `kern.ipc.shm_use_phys`.

Se você estiver executando em um jail do FreeBSD, você deve definir o parâmetro `sysvshm` para `new`, para que ele tenha seu próprio namespace de memória compartilhada do Sistema V separado. (Antes do FreeBSD 11.0, era necessário habilitar o acesso compartilhado ao namespace de IPC do host a partir de jails e tomar medidas para evitar colisões.)

NetBSD: As configurações padrão de memória compartilhada geralmente são suficientes, a menos que você tenha definido `shared_memory_type` para `sysv`. No entanto, você precisará aumentar `kern.ipc.semmni` e `kern.ipc.semmns`, pois as configurações padrão do NetBSD para essas opções são ineficazes.

Os parâmetros do IPC podem ser ajustados usando `sysctl`, por exemplo:

```
# sysctl -w kern.ipc.semmni=100
```

Para que essas configurações persistem após as reinicializações, modifique `/etc/sysctl.conf`.

Se você definiu `shared_memory_type` para `sysv`, talvez queira também configurar seu kernel para bloquear a memória compartilhada do System V na RAM e impedir que ela seja mapeada para o swap. Isso pode ser feito usando o ajuste `sysctl` `kern.ipc.shm_use_phys`.

OpenBSD:   Os ajustes padrão de memória compartilhada geralmente são suficientes, a menos que você tenha definido `shared_memory_type` para `sysv`. No entanto, você precisará aumentar `kern.seminfo.semmni` e `kern.seminfo.semmns`, pois os ajustes padrão do OpenBSD para esses são inoperáveis.

Os parâmetros do IPC podem ser ajustados usando `sysctl`, por exemplo:

```
# sysctl kern.seminfo.semmni=100
```

Para que essas configurações persistem após as reinicializações, modifique `/etc/sysctl.conf`.

Os ajustes padrão de memória compartilhada geralmente são suficientes, a menos que você tenha definido `shared_memory_type` para `sysv`, e mesmo assim, apenas em versões mais antigas do kernel que foram entregues com configurações padrão baixas. Semaforos do System V não são usados nesta plataforma.

Os ajustes de tamanho da memória compartilhada podem ser alterados através da interface `sysctl`. Por exemplo, para permitir 16 GB:

```
$ sysctl -w kernel.shmmax=17179869184 $ sysctl -w kernel.shmall=4194304
```

Para que essas configurações persistem após as reinicializações, consulte `/etc/sysctl.conf`.

macOS: As configurações padrão de memória compartilhada e semaforos geralmente são suficientes, a menos que você tenha definido `shared_memory_type` para `sysv`.

O método recomendado para configurar a memória compartilhada no macOS é criar um arquivo chamado `/etc/sysctl.conf`, contendo atribuições de variáveis, como:

```
kern.sysv.shmmax=4194304 kern.sysv.shmmin=1 kern.sysv.shmmni=32 kern.sysv.shmseg=8 kern.sysv.shmall=1024
```

Observe que, em algumas versões do macOS, *todos os cinco* parâmetros de memória compartilhada devem ser definidos em `/etc/sysctl.conf`, caso contrário, os valores serão ignorados.

`SHMMAX` só pode ser definido em múltiplos de 4096.

`SHMALL` é medido em páginas de 4 kB nesta plataforma.

É possível alterar tudo, exceto `SHMMNI`, em tempo real, usando sysctl. No entanto, ainda é melhor configurar os valores preferidos através de `/etc/sysctl.conf`, para que os valores sejam mantidos após as reinicializações.

Solaris illumos:   Os valores padrão de memória compartilhada e semaforos geralmente são suficientes para a maioria das aplicações do PostgreSQL. O padrão do Solaris é um `SHMMAX` de um quarto da RAM do sistema. Para ajustar ainda mais esse ajuste, use um ajuste de projeto associado ao usuário `postgres`. Por exemplo, execute o seguinte como `root`:

```
projadd -c "PostgreSQL DB User" -K "project.max-shm-memory=(privileged,8GB,deny)" -U postgres -G postgres user.postgres
```

Este comando adiciona o projeto `user.postgres` e define o máximo de memória compartilhada para o usuário `postgres` para 8 GB, e entra em vigor na próxima vez que o usuário iniciar sessão, ou quando você reiniciar o PostgreSQL (não recarregar). O acima assume que o PostgreSQL é executado pelo usuário `postgres` no grupo `postgres`. Não é necessário reiniciar o servidor.

Outras alterações recomendadas nas configurações do kernel para servidores de banco de dados que terão um grande número de conexões são:

```
project.max-shm-ids=(priv,32768,deny) project.max-sem-ids=(priv,4096,deny) project.max-msg-ids=(priv,4096,deny)
```

Além disso, se você estiver executando o PostgreSQL dentro de uma zona, talvez seja necessário aumentar os limites de uso do recurso da zona. Consulte o "Capítulo 2: Projetos e Tarefas" no *Guia do Administrador do Sistema* para mais informações sobre `projects` e `prctl`.

### 18.4.2. systemd RemoveIPC [#](#SYSTEMD-REMOVEIPC)

Se o systemd estiver em uso, é preciso ter cuidado para que os recursos IPC (incluindo memória compartilhada) não sejam removidos prematuramente pelo sistema operacional. Isso é especialmente preocupante ao instalar o PostgreSQL a partir de fonte. Os usuários de pacotes de distribuição do PostgreSQL têm menos probabilidade de serem afetados, pois o usuário `postgres` é então normalmente criado como um usuário do sistema.

O parâmetro `RemoveIPC` em `logind.conf` controla se os objetos do IPC são removidos quando um usuário faz o logout completo. Os usuários do sistema estão isentos. Este parâmetro tem o valor padrão ativado no sistema stock systemd, mas algumas distribuições do sistema operacional o têm como padrão desativado.

Um efeito observado com frequência quando essa configuração está ativada é que os objetos de memória compartilhada usados para execução de consultas paralelas são removidos em momentos aparentemente aleatórios, o que resulta em erros e avisos ao tentar abri-los e removê-los, como:

```
WARNING:  could not remove shared memory segment "/PostgreSQL.1450751626": No such file or directory
```

Diferentes tipos de objetos IPC (memória compartilhada vs. semaforos, System V vs. POSIX) são tratados de maneira ligeiramente diferente pelo systemd, então é possível observar que alguns recursos de IPC não são removidos da mesma maneira que outros. Mas não é recomendável confiar nessas diferenças sutis.

Uma "sessão de desconexão do usuário" pode ocorrer como parte de uma tarefa de manutenção ou manualmente quando um administrador se conecta como o usuário `postgres` ou algo semelhante, portanto é difícil de prevenir em geral.

O que é um "usuário do sistema" é determinado no momento da compilação do systemd a partir do ajuste `SYS_UID_MAX` em `/etc/login.defs`.

Os scripts de embalagem e implantação devem ter cuidado ao criar o usuário `postgres` como um usuário do sistema usando `useradd -r`, `adduser --system`, ou equivalente.

Como alternativa, se a conta do usuário foi criada incorretamente ou não pode ser alterada, é recomendável definir

```
RemoveIPC=no
```

em `/etc/systemd/logind.conf` ou outro arquivo de configuração apropriado.

### Atenção

Pelo menos uma dessas duas coisas precisa ser assegurada, ou o servidor PostgreSQL será muito pouco confiável.

### 18.4.3. Limites de recursos [#](#KERNEL-RESOURCES-LIMITS)

Sistemas operacionais semelhantes ao Unix importam vários tipos de limites de recursos que podem interferir no funcionamento do seu servidor PostgreSQL. De particular importância são os limites do número de processos por usuário, o número de arquivos abertos por processo e a quantidade de memória disponível para cada processo. Cada um desses tem um limite "duro" e um limite "suave". O limite suave é o que realmente conta, mas pode ser alterado pelo usuário até o limite duro. O limite duro só pode ser alterado pelo usuário root. A chamada do sistema `setrlimit` é responsável por definir esses parâmetros. O comando embutido da concha `ulimit` (conchas Bourne) ou `limit` (csh) é usado para controlar os limites de recursos a partir da linha de comando. Em sistemas derivados de BSD, o arquivo `/etc/login.conf` controla os vários limites de recursos definidos durante o login. Consulte a documentação do sistema operacional para detalhes. Os parâmetros relevantes são `maxproc`, `openfiles` e `datasize`. Por exemplo:

```
default:\ ... :datasize-cur=256M:\ :maxproc-cur=256:\ :openfiles-cur=256:\ ...
```

(`-cur` é o limite flexível. Adicione `-max` para definir o limite rígido.)

Os kernels também podem ter limites em todo o sistema em relação a alguns recursos.

* No Linux, o parâmetro do kernel `fs.file-max` determina o número máximo de arquivos abertos que o kernel suportará. Ele pode ser alterado com `sysctl -w fs.file-max=N`. Para fazer o ajuste persistir após reinicializações, adicione uma atribuição em `/etc/sysctl.conf`. O limite máximo de arquivos por processo é fixado no momento em que o kernel é compilado; veja `/usr/src/linux/Documentation/proc.txt` para mais informações.

O servidor PostgreSQL usa um processo por conexão, portanto, você deve fornecer pelo menos tantos processos quanto conexões permitidas, além do que você precisa para o resto do seu sistema. Geralmente, isso não é um problema, mas se você executar vários servidores em uma máquina, as coisas podem ficar apertadas.

O limite padrão da fábrica para arquivos abertos é frequentemente definido para valores "socialmente amigáveis" que permitem que muitos usuários coexistissem em uma máquina sem usar uma fração inadequada dos recursos do sistema. Se você executar muitos servidores em uma máquina, talvez seja o que você queira, mas em servidores dedicados, você pode querer aumentar esse limite.

Do outro lado da moeda, alguns sistemas permitem que processos individuais abram um grande número de arquivos; se mais de alguns processos o fizerem, o limite do sistema pode ser facilmente excedido. Se você encontrar isso acontecendo e não quiser alterar o limite do sistema, pode definir o parâmetro de configuração [max_files_per_process](runtime-config-resource.md#GUC-MAX-FILES-PER-PROCESS) do PostgreSQL para limitar o consumo de arquivos abertos.

Outro limite do kernel que pode ser preocupante ao suportar um grande número de conexões de clientes é o comprimento máximo da fila de conexões de socket. Se mais do que esse número de solicitações de conexão chegarem em um período muito curto, algumas podem ser rejeitadas antes que o servidor PostgreSQL possa atender às solicitações, com esses clientes recebendo erros de falha de conexão inúteis, como “Recurso temporariamente indisponível” ou “Conexão recusada”. O limite padrão do comprimento da fila é de 128 em muitas plataformas. Para aumentá-lo, ajuste o parâmetro apropriado do kernel via sysctl e, em seguida, reinicie o servidor PostgreSQL. O parâmetro é denominado de várias maneiras, como `net.core.somaxconn` no Linux, `kern.ipc.soacceptqueue` no FreeBSD mais recente, e `kern.ipc.somaxconn` no macOS e outros variantes BSD.

### 18.4.4. Sobrecommit de memória no Linux [#](#LINUX-MEMORY-OVERCOMMIT)

O comportamento padrão de memória virtual no Linux não é ótimo para o PostgreSQL. Devido à maneira como o kernel implementa o sobrecommit de memória, o kernel pode terminar o postmaster do PostgreSQL (o processo do servidor supervisor) se as demandas de memória de qualquer um dos PostgreSQL ou outro processo causarem o esgotamento da memória virtual do sistema.

Se isso acontecer, você verá uma mensagem do kernel que parece com esta (consulte a documentação e a configuração do seu sistema para saber onde procurar tal mensagem):

```
Out of Memory: Killed process 12345 (postgres).
```

Isso indica que o processo `postgres` foi encerrado devido à pressão de memória. Embora as conexões de banco de dados existentes continuem a funcionar normalmente, nenhuma nova conexão será aceita. Para se recuperar, o PostgreSQL precisará ser reiniciado.

Uma maneira de evitar esse problema é executar o PostgreSQL em uma máquina onde você pode ter certeza de que outros processos não esgotarão a memória da máquina. Se a memória estiver apertada, aumentar o espaço de troca do sistema operacional pode ajudar a evitar o problema, porque o assassino de memória insuficiente (OOM) é invocado apenas quando a memória física e o espaço de troca são esgotados.

Se o PostgreSQL em si for a causa do sistema ficar sem memória, você pode evitar o problema alterando sua configuração. Em alguns casos, pode ajudar a diminuir os parâmetros de configuração relacionados à memória, particularmente `shared_buffers` (runtime-config-resource.md#GUC-SHARED-BUFFERS), `work_mem` (runtime-config-resource.md#GUC-WORK-MEM) e `hash_mem_multiplier` (runtime-config-resource.md#GUC-HASH-MEM-MULTIPLIER). Noutros casos, o problema pode ser causado por permitir muitas conexões ao próprio servidor de banco de dados. Em muitos casos, pode ser melhor reduzir `max_connections` (runtime-config-connection.md#GUC-MAX-CONNECTIONS) e, em vez disso, utilizar software de pool de conexões externas.

É possível modificar o comportamento do kernel para que ele não "sobrecarregue" a memória. Embora essa configuração não impeça que o [OOM killer](https://lwn.net/Articles/104179/) seja invocado completamente, ela reduzirá significativamente as chances e, portanto, levará a um comportamento de sistema mais robusto. Isso é feito selecionando o modo de sobrecarregamento estrito via `sysctl`:

```
sysctl -w vm.overcommit_memory=2
```

ou colocando uma entrada equivalente em `/etc/sysctl.conf`. Você também pode desejar modificar o ajuste relacionado `vm.overcommit_ratio`. Para detalhes, consulte o arquivo de documentação do kernel
<https://www.kernel.org/doc/Documentation/vm/overcommit-accounting>.

Outra abordagem, que pode ser usada com ou sem alteração, é definir o valor do ajuste do *score de ajuste específico do processo* para o processo postmaster para `-1000`, garantindo assim que ele não será alvo do OOM killer. A maneira mais simples de fazer isso é executar

```
echo -1000 > /proc/self/oom_score_adj
```

no script de inicialização do PostgreSQL, logo antes de invocar `postgres`. Observe que essa ação deve ser feita como root, ou não terá efeito; assim, um script de inicialização de propriedade de root é o lugar mais fácil para fazer isso. Se você fazer isso, também deve definir essas variáveis de ambiente no script de inicialização antes de invocar `postgres`:

```
export PG_OOM_ADJUST_FILE=/proc/self/oom_score_adj export PG_OOM_ADJUST_VALUE=0
```

Essas configurações farão com que os processos filhos do postmaster sejam executados com o ajuste normal do score OOM de zero, para que o assassino OOM ainda possa direcioná-los quando necessário. Você pode usar outro valor para `PG_OOM_ADJUST_VALUE` se quiser que os processos filhos sejam executados com algum outro ajuste do score OOM. (`PG_OOM_ADJUST_VALUE` também pode ser omitido, no caso, ele tem como padrão zero.) Se você não definir `PG_OOM_ADJUST_FILE`, os processos filhos serão executados com o mesmo ajuste do score OOM que o postmaster, o que não é prudente, uma vez que o objetivo é garantir que o postmaster tenha um ajuste preferencial.

### 18.4.5. Páginas enormes do Linux [#](#LINUX-HUGE-PAGES)

Usar páginas enormes reduz o overhead ao usar grandes pedaços contínuos de memória, como o PostgreSQL, especialmente quando se usam grandes valores de [shared_buffers](runtime-config-resource.md#GUC-SHARED-BUFFERS). Para usar essa característica no PostgreSQL, você precisa de um kernel com `CONFIG_HUGETLBFS=y` e `CONFIG_HUGETLB_PAGE=y`. Você também precisará configurar o sistema operacional para fornecer páginas enormes suficientes do tamanho desejado. O parâmetro calculado em tempo de execução [shared_memory_size_in_huge_pages](runtime-config-preset.md#GUC-SHARED-MEMORY-SIZE-IN-HUGE-PAGES) relata o número de páginas enormes necessárias. Esse parâmetro pode ser visualizado antes de iniciar o servidor com um comando como:

```
$ postgres -D $PGDATA -C shared_memory_size_in_huge_pages 3170 $ grep ^Hugepagesize /proc/meminfo Hugepagesize:       2048 kB $ ls /sys/kernel/mm/hugepages hugepages-1048576kB  hugepages-2048kB
```

Neste exemplo, o padrão é de 2 MB, mas você também pode solicitar explicitamente 2 MB ou 1 GB com [huge_page_size](runtime-config-resource.md#GUC-HUGE-PAGE-SIZE) para adaptar o número de páginas calculadas por `shared_memory_size_in_huge_pages`. Embora precisemos de pelo menos `3170` páginas enormes neste exemplo, um ajuste maior seria apropriado se outros programas na máquina também precisem de páginas enormes. Podemos definir isso com:

```
# sysctl -w vm.nr_hugepages=3170
```

Não se esqueça de adicionar essa configuração ao `/etc/sysctl.conf` para que ela seja reaplicada após as reinicializações. Para tamanhos de página grandes que não são padrão, podemos usar em vez disso:

```
# echo 3170 > /sys/kernel/mm/hugepages/hugepages-2048kB/nr_hugepages
```

É também possível fornecer esses ajustes no momento do boot, usando parâmetros do kernel, como `hugepagesz=2M hugepages=3170`.

Às vezes, o kernel não consegue alocar o número desejado de páginas enormes imediatamente devido à fragmentação, então pode ser necessário repetir o comando ou reiniciar. (Imediatamente após um reinício, a maioria da memória da máquina deve estar disponível para ser convertida em páginas enormes.) Para verificar a situação de alocação de páginas enormes para um tamanho dado, use:

```
$ cat /sys/kernel/mm/hugepages/hugepages-2048kB/nr_hugepages
```

Também pode ser necessário conceder permissão ao sistema operacional do servidor de banco de dados para usar páginas enormes, configurando `vm.hugetlb_shm_group` via sysctl, e/ou conceder permissão para bloquear a memória com `ulimit -l`.

O comportamento padrão para páginas enormes no PostgreSQL é usá-las quando possível, com o tamanho de página enorme padrão do sistema, e recorrer a páginas normais em caso de falha. Para impor o uso de páginas enormes, você pode definir [huge_pages](runtime-config-resource.md#GUC-HUGE-PAGES) para `on` em `postgresql.conf`. Observe que, com essa configuração, o PostgreSQL não conseguirá iniciar se não houver páginas enormes suficientes disponíveis.

Para uma descrição detalhada da característica de páginas enormes do Linux, consulte <https://www.kernel.org/doc/Documentation/vm/hugetlbpage.txt>.