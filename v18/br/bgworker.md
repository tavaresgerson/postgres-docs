## Capítulo 46. Processos de Trabalho de Fundo

O PostgreSQL pode ser estendido para executar código fornecido pelo usuário em processos separados. Esses processos são iniciados, interrompidos e monitorados pelo `postgres`, que permite que eles tenham uma vida útil intimamente ligada ao status do servidor. Esses processos estão vinculados à área de memória compartilhada do PostgreSQL e têm a opção de se conectar a bancos de dados internamente; eles também podem executar múltiplas transações em série, assim como um processo de servidor conectado a um cliente regular. Além disso, ao se conectar ao libpq, eles podem se conectar ao servidor e se comportar como um aplicativo de cliente regular.

### Aviso

Há riscos consideráveis de robustez e segurança ao usar processos de trabalhador de segundo plano, porque, sendo escritos na linguagem `C`, eles têm acesso irrestrito aos dados. Os administradores que desejam habilitar módulos que incluem processos de trabalhador de segundo plano devem exercer extrema cautela. Apenas módulos cuidadosamente auditados devem ser permitidos para executar processos de trabalhador de segundo plano.

Os trabalhadores em segundo plano podem ser inicializados no momento em que o PostgreSQL é iniciado, incluindo o nome do módulo no `shared_preload_libraries`. Um módulo que deseja executar um trabalhador em segundo plano pode registrá-lo chamando `RegisterBackgroundWorker(BackgroundWorker *worker)` a partir de sua função `_PG_init()`. Os trabalhadores em segundo plano também podem ser iniciados após o sistema estar operacional, chamando `RegisterDynamicBackgroundWorker(BackgroundWorker *worker, BackgroundWorkerHandle **handle)`. Ao contrário de `RegisterBackgroundWorker`, que só pode ser chamado dentro do processo postmaster, `RegisterDynamicBackgroundWorker` deve ser chamado a partir de um backend regular ou outro trabalhador em segundo plano.

A estrutura `BackgroundWorker` é definida da seguinte forma:

```
typedef void (*bgworker_main_type)(Datum main_arg);
typedef struct BackgroundWorker
{
    char        bgw_name[BGW_MAXLEN];
    char        bgw_type[BGW_MAXLEN];
    int         bgw_flags;
    BgWorkerStartTime bgw_start_time;
    int         bgw_restart_time;       /* in seconds, or BGW_NEVER_RESTART */
    char        bgw_library_name[MAXPGPATH];
    char        bgw_function_name[BGW_MAXLEN];
    Datum       bgw_main_arg;
    char        bgw_extra[BGW_EXTRALEN];
    pid_t       bgw_notify_pid;
} BackgroundWorker;
```

`bgw_name` e `bgw_type` são strings que devem ser usadas em mensagens de log, listas de processos e contextos semelhantes. `bgw_type` deve ser o mesmo para todos os trabalhadores de fundo do mesmo tipo, para que seja possível agrupar esses trabalhadores em uma lista de processos, por exemplo. `bgw_name`, por outro lado, pode conter informações adicionais sobre o processo específico. (Tipicamente, a string para `bgw_name` conterá o tipo de alguma forma, mas isso não é estritamente necessário.)

`bgw_flags` é uma máscara de bits que indica as capacidades que o módulo deseja. Os valores possíveis são:

`BGWORKER_SHMEM_ACCESS`: Solicita acesso à memória compartilhada. Essa bandeira é necessária.

`BGWORKER_BACKEND_DATABASE_CONNECTION`: Solicita a capacidade de estabelecer uma conexão de banco de dados através da qual poderá executar transações e consultas posteriormente. Um trabalhador de segundo plano que utilize `BGWORKER_BACKEND_DATABASE_CONNECTION` para se conectar a um banco de dados também deve anexar memória compartilhada usando `BGWORKER_SHMEM_ACCESS`, ou o arranque do trabalhador falhará.

`bgw_start_time` é o estado do servidor durante o qual `postgres` deve iniciar o processo; pode ser um dos `BgWorkerStart_PostmasterStart` (começar assim que `postgres` próprio tenha terminado sua própria inicialização; os processos que solicitam isso não são elegíveis para conexões com banco de dados), `BgWorkerStart_ConsistentState` (começar assim que um estado consistente tenha sido alcançado em um standby quente, permitindo que os processos se conectem aos bancos de dados e executem consultas de leitura), e `BgWorkerStart_RecoveryFinished` (começar assim que o sistema tenha entrado no estado normal de leitura e escrita). Observe que os dois últimos valores são equivalentes em um servidor que não é um standby quente. Note que este ajuste indica apenas quando os processos devem ser iniciados; eles não param quando é alcançado um estado diferente.

`bgw_restart_time` é o intervalo, em segundos, que `postgres` deve esperar antes de reiniciar o processo no caso de ele falhar. Pode ser qualquer valor positivo, ou `BGW_NEVER_RESTART`, indicando que não deve reiniciar o processo em caso de falha.

`bgw_library_name` é o nome de uma biblioteca na qual o ponto inicial de entrada do trabalhador de fundo deve ser procurado. A biblioteca nomeada será carregada dinamicamente pelo processo do trabalhador e `bgw_function_name` será usado para identificar a função a ser chamada. Se estiver chamando uma função no código principal, isso deve ser definido como `"postgres"`.

`bgw_function_name` é o nome da função a ser usada como ponto de entrada inicial para o novo trabalhador de fundo. Se essa função estiver em uma biblioteca carregada dinamicamente, ela deve ser marcada `PGDLLEXPORT` (e não `static`).

`bgw_main_arg` é o argumento `Datum` para a função principal do trabalhador de fundo. Esta função principal deve receber um único argumento do tipo `Datum` e retornar `void`. `bgw_main_arg` será passado como argumento. Além disso, a variável global `MyBgworkerEntry` aponta para uma cópia da estrutura `BackgroundWorker` passada no momento do registro; o trabalhador pode achar útil examinar essa estrutura.

Em Windows (e em qualquer outro lugar onde `EXEC_BACKEND` é definido) ou em trabalhadores dinâmicos de fundo, não é seguro passar um `Datum` por referência, apenas por valor. Se um argumento for necessário, é mais seguro passar um int32 ou outro valor pequeno e usar esse valor como índice em um array alocado em memória compartilhada. Se um valor como um `cstring` ou `text` for passado, o ponteiro não será válido a partir do novo processo de trabalhador de fundo.

`bgw_extra` pode conter dados adicionais que serão passados para o trabalhador de fundo. Ao contrário de `bgw_main_arg`, esses dados não são passados como argumento para a função principal do trabalhador, mas podem ser acessados via `MyBgworkerEntry`, conforme discutido acima.

`bgw_notify_pid` é o PID de um processo de backend do PostgreSQL para o qual o postmaster deve enviar `SIGUSR1` quando o processo é iniciado ou encerrado. Deve ser 0 para trabalhadores registrados no momento de inicialização do postmaster, ou quando o backend que registra o trabalhador não deseja esperar pelo início do trabalhador. Caso contrário, deve ser inicializado para `MyProcPid`.

Uma vez em execução, o processo pode se conectar a um banco de dados chamando `BackgroundWorkerInitializeConnection(char *dbname, char *username, uint32 flags)` ou `BackgroundWorkerInitializeConnectionByOid(Oid dboid, Oid useroid, uint32 flags)`. Isso permite que o processo execute transações e consultas usando a interface `SPI`. Se `dbname` for NULL ou `dboid` for `InvalidOid`, a sessão não está conectada a nenhum banco de dados específico, mas catálogos compartilhados podem ser acessados. Se `username` for NULL ou `useroid` for `InvalidOid`, o processo será executado como o superusuário criado durante `initdb`. Se `BGWORKER_BYPASS_ALLOWCONN` for especificado como `flags`, é possível contornar a restrição de conexão com bancos de dados que não permitem conexões de usuário. Se `BGWORKER_BYPASS_ROLELOGINCHECK` for especificado como `flags`, é possível contornar a verificação de login para o papel usado para conectar-se a bancos de dados. Um trabalhador em segundo plano pode chamar apenas uma dessas duas funções, e apenas uma vez. Não é possível alternar bancos.

Os sinais são inicialmente bloqueados quando o controle atinge a função principal do trabalhador de fundo, e devem ser desbloqueados por ele; isso permite que o processo personalize seus manipuladores de sinal, se necessário. Os sinais podem ser desbloqueados no novo processo chamando `BackgroundWorkerUnblockSignals` e bloqueados chamando `BackgroundWorkerBlockSignals`.

Se `bgw_restart_time` para um trabalhador de fundo estiver configurado como `BGW_NEVER_RESTART`, ou se ele sair com um código de saída de 0 ou for terminado por `TerminateBackgroundWorker`, ele será automaticamente desregistrado pelo postmaster na saída. Caso contrário, ele será reiniciado após o período de tempo configurado via `bgw_restart_time`, ou imediatamente se o postmaster reiniciar o clúster devido a uma falha no backend. Backends que precisam suspender a execução apenas temporariamente devem usar um sono interrompível em vez de sair; isso pode ser feito chamando `WaitLatch()`. Certifique-se de que a bandeira `WL_POSTMASTER_DEATH` esteja definida ao chamar essa função, e verifique o código de retorno para uma saída rápida no caso de emergência que o próprio `postgres` tenha terminado.

Quando um trabalhador de fundo é registrado usando a função `RegisterDynamicBackgroundWorker`, é possível que o backend que realiza o registro obtenha informações sobre o status do trabalhador. Backends que desejam fazer isso devem passar o endereço de um `BackgroundWorkerHandle *` como o segundo argumento para `RegisterDynamicBackgroundWorker`. Se o trabalhador for registrado com sucesso, este ponteiro será inicializado com um handle opaco que pode ser posteriormente passado para `GetBackgroundWorkerPid(BackgroundWorkerHandle *, pid_t *)` ou `TerminateBackgroundWorker(BackgroundWorkerHandle *)`. `GetBackgroundWorkerPid` pode ser usado para coletar o status do trabalhador: um valor de retorno de `BGWH_NOT_YET_STARTED` indica que o trabalhador ainda não foi iniciado pelo postmaster; `BGWH_STOPPED` indica que foi iniciado, mas não está mais em execução; e `BGWH_STARTED` indica que está atualmente em execução. Neste último caso, o PID também será retornado via o segundo argumento. `TerminateBackgroundWorker` faz com que o postmaster envie `SIGTERM` ao trabalhador se estiver em execução, e o desregistre assim que não estiver.

Em alguns casos, um processo que registra um trabalhador de segundo plano pode querer esperar que o trabalhador seja iniciado. Isso pode ser feito inicializando `bgw_notify_pid` para `MyProcPid` e, em seguida, passando o `BackgroundWorkerHandle *` obtido no momento do registro para a função `WaitForBackgroundWorkerStartup(BackgroundWorkerHandle *handle, pid_t *)`. Esta função bloqueará até que o postmaster tenha tentado iniciar o trabalhador de segundo plano, ou até que o postmaster morra. Se o trabalhador de segundo plano estiver em execução, o valor de retorno será `BGWH_STARTED`, e o PID será escrito no endereço fornecido. Caso contrário, o valor de retorno será `BGWH_STOPPED` ou `BGWH_POSTMASTER_DIED`.

Um processo também pode esperar que um trabalhador de segundo plano seja encerrado, usando a função `WaitForBackgroundWorkerShutdown(BackgroundWorkerHandle *handle)` e passando o `BackgroundWorkerHandle *` obtido no registro. Esta função bloqueará até que o trabalhador de segundo plano saia, ou o postmaster morra. Quando o trabalhador de segundo plano sai, o valor de retorno é `BGWH_STOPPED`, se o postmaster morrer, ele retornará `BGWH_POSTMASTER_DIED`.

Os trabalhadores em segundo plano podem enviar mensagens de notificação assíncrona, utilizando o comando `NOTIFY` via SPI ou diretamente via `Async_Notify()`. Essas notificações serão enviadas no momento do commit da transação. Os trabalhadores em segundo plano não devem se registrar para receber notificações assíncronas com o comando `LISTEN`, pois não há infraestrutura para um trabalhador consumir essas notificações.

O módulo `src/test/modules/worker_spi` contém um exemplo funcional, que demonstra algumas técnicas úteis.

O número máximo de trabalhadores de fundo registrados é limitado por [max_worker_processes][(runtime-config-resource.md#GUC-MAX-WORKER-PROCESSES)].