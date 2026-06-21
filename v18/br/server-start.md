## 18.3. Iniciar o servidor de banco de dados [#](#SERVER-START)

* [18.3.1. Falhas no início do servidor](server-start.md#SERVER-START-FAILURES)
* [18.3.2. Problemas com a conexão do cliente](server-start.md#CLIENT-CONNECTION-PROBLEMS)

Antes que alguém possa acessar o banco de dados, você deve iniciar o servidor de banco de dados. O programa do servidor de banco de dados é chamado `postgres`.

Se você estiver usando uma versão pré-embalada do PostgreSQL, quase certamente ela inclui disposições para executar o servidor como uma tarefa em segundo plano de acordo com as convenções do seu sistema operacional. Usar a infraestrutura do pacote para iniciar o servidor será muito menos trabalho do que descobrir como fazer isso você mesmo. Consulte a documentação do nível do pacote para obter detalhes.

A maneira básica de iniciar o servidor manualmente é simplesmente invocar `postgres` diretamente, especificando a localização do diretório de dados com a opção `-D`, por exemplo:

```
$ postgres -D /usr/local/pgsql/data
```

que deixará o servidor rodando em primeiro plano. Isso deve ser feito enquanto você está conectado à conta de usuário do PostgreSQL. Sem `-D`, o servidor tentará usar o diretório de dados nomeado pela variável de ambiente `PGDATA`. Se essa variável também não for fornecida, falhará.

Normalmente, é melhor iniciar `postgres` em segundo plano. Para isso, use a sintaxe usual do shell Unix:

```
$ postgres -D /usr/local/pgsql/data >logfile 2>&1 &
```

É importante armazenar a saída de stdout e stderr do servidor em algum lugar, como mostrado acima. Isso ajudará para fins de auditoria e para diagnosticar problemas. (Consulte [Seção 24.3] para uma discussão mais detalhada sobre o manuseio de arquivos de registro.)

O programa `postgres` também aceita uma série de outras opções de linha de comando. Para mais informações, consulte a página de referência [postgres][(app-postgres.md "postgres")] e [Capítulo 19][(runtime-config.md "Chapter 19. Server Configuration")] abaixo.

Essa sintaxe de shell pode se tornar entediante rapidamente. Portanto, o programa wrapper [pg_ctl](app-pg-ctl.md "pg_ctl") é fornecido para simplificar algumas tarefas. Por exemplo:

```
pg_ctl start -l logfile
```

O servidor será iniciado em segundo plano e o resultado será colocado no arquivo de registro nomeado. A opção `-D` tem o mesmo significado aqui que para `postgres`. `pg_ctl` também é capaz de parar o servidor.

Normalmente, você vai querer iniciar o servidor de banco de dados quando o computador é iniciado. Os scripts de autoinicialização são específicos para o sistema operacional. Existem alguns scripts de exemplo distribuídos com o PostgreSQL no diretório `contrib/start-scripts`. A instalação de um deles exigirá privilégios de root.

Diferentes sistemas têm convenções diferentes para iniciar os demônios no momento do boot. Muitos sistemas têm um arquivo `/etc/rc.local` ou `/etc/rc.d/rc.local`. Outros usam diretórios `init.d` ou `rc.d`. O que quer que você faça, o servidor deve ser executado pela conta de usuário do PostgreSQL *e não pelo root* ou qualquer outro usuário. Portanto, você provavelmente deve formar seus comandos usando `su postgres -c '...'`. Por exemplo:

```
su postgres -c 'pg_ctl start -D /usr/local/pgsql/data -l serverlog'
```

Aqui estão algumas sugestões específicas para cada sistema operacional. (Em cada caso, certifique-se de usar o diretório de instalação e o nome de usuário apropriados, onde mostramos valores genéricos.)

* Para o FreeBSD, veja o arquivo `contrib/start-scripts/freebsd` na distribuição de código-fonte do PostgreSQL.
* No OpenBSD, adicione as seguintes linhas ao arquivo `/etc/rc.local`:

* Em sistemas Linux, adicione

  ```
  /usr/local/pgsql/bin/pg_ctl start -l logfile -D /usr/local/pgsql/data
  ```

para `/etc/rc.d/rc.local` ou `/etc/rc.local` ou veja o arquivo `contrib/start-scripts/linux` na distribuição de fonte do PostgreSQL.

Ao usar o systemd, você pode usar o seguinte arquivo de unidade de serviço (por exemplo, em `/etc/systemd/system/postgresql.service`):

  ```
  [Unit]
  Description=PostgreSQL database server
  Documentation=man:postgres(1)
  After=network-online.target
  Wants=network-online.target

  [Service]
  Type=notify
  User=postgres
  ExecStart=/usr/local/pgsql/bin/postgres -D /usr/local/pgsql/data
  ExecReload=/bin/kill -HUP $MAINPID
  KillMode=mixed
  KillSignal=SIGINT
  TimeoutSec=infinity

  [Install]
  WantedBy=multi-user.target
  ```

Para usar `Type=notify`, é necessário que o binário do servidor tenha sido construído com `configure --with-systemd`.

Considere cuidadosamente a configuração do tempo de espera. O systemd tem um tempo de espera padrão de 90 segundos, conforme este texto, e irá matar um processo que não informe prontidão dentro desse tempo. Mas um servidor PostgreSQL que pode precisar realizar recuperação em caso de falha no início do sistema pode levar muito mais tempo para se tornar pronto. O valor sugerido de `infinity` desativa a lógica de tempo de espera.
* Em NetBSD, use os scripts de inicialização do FreeBSD ou Linux, dependendo da preferência.
* Em Solaris, crie um arquivo chamado `/etc/init.d/postgresql` que contenha a seguinte linha:

  ```
  su - postgres -c "/usr/local/pgsql/bin/pg_ctl start -l logfile -D /usr/local/pgsql/data"
  ```

Em seguida, crie um link simbólico para ele em `/etc/rc3.d` como `S99postgresql`.

Enquanto o servidor estiver em execução, seu PID será armazenado no arquivo `postmaster.pid` no diretório de dados. Isso é usado para evitar que múltiplas instâncias do servidor sejam executadas no mesmo diretório de dados e também pode ser usado para desligar o servidor.

### 18.3.1. Falhas no início do servidor [#](#SERVER-START-FAILURES)

Existem várias razões comuns pelas quais o servidor pode não iniciar. Verifique o arquivo de log do servidor ou inicie-o manualmente (sem redirecionar a saída padrão ou o erro padrão) e veja quais mensagens de erro aparecem. Abaixo, explicamos algumas das mensagens de erro mais comuns em detalhes.

```
LOG:  could not bind IPv4 address "127.0.0.1": Address already in use
HINT:  Is another postmaster already running on port 5432? If not, wait a few seconds and retry.
FATAL:  could not create any TCP/IP sockets
```

Isso geralmente significa exatamente o que sugere: você tentou iniciar outro servidor na mesma porta onde um já está em execução. No entanto, se a mensagem de erro do kernel não for `Address already in use` ou alguma variação disso, pode haver um problema diferente. Por exemplo, tentar iniciar um servidor em um número de porta reservado pode gerar algo como:

```
$ postgres -p 666
LOG:  could not bind IPv4 address "127.0.0.1": Permission denied
HINT:  Is another postmaster already running on port 666? If not, wait a few seconds and retry.
FATAL:  could not create any TCP/IP sockets
```

Uma mensagem como:

```
FATAL:  could not create shared memory segment: Invalid argument
DETAIL:  Failed system call was shmget(key=5440001, size=4011376640, 03600).
```

provavelmente significa que o limite do seu kernel no tamanho da memória compartilhada é menor que a área de trabalho que o PostgreSQL está tentando criar (4011376640 bytes neste exemplo). Isso provavelmente só acontece se você definiu `shared_memory_type` para `sysv`. Nesse caso, você pode tentar iniciar o servidor com um número de buffers menor que o normal ([shared_buffers](runtime-config-resource.md#GUC-SHARED-BUFFERS)) ou reconfigurar seu kernel para aumentar o tamanho da memória compartilhada permitido. Você também pode ver esta mensagem ao tentar iniciar vários servidores na mesma máquina, se o espaço total solicitado deles exceder o limite do kernel.

Um erro como:

```
FATAL:  could not create semaphores: No space left on device
DETAIL:  Failed system call was semget(5440126, 17, 03600).
```

*não* significa que você esgotou o espaço em disco. Isso significa que o limite do kernel sobre o número de semaforos System V é menor que o número que o PostgreSQL quer criar. Como mencionado acima, você pode resolver o problema iniciando o servidor com um número reduzido de conexões permitidas ([max_connections](runtime-config-connection.md#GUC-MAX-CONNECTIONS)), mas você acabará querendo aumentar o limite do kernel.

Detalhes sobre a configuração das facilidades do System V IPC estão fornecidos em [Seção 18.4.1][(kernel-resources.md#SYSVIPC "18.4.1. Shared Memory and Semaphores")].

### 18.3.2. Problemas com a conexão do cliente [#](#CLIENT-CONNECTION-PROBLEMS)

Embora as condições de erro possíveis do lado do cliente sejam bastante variadas e dependentes da aplicação, algumas delas podem estar diretamente relacionadas à forma como o servidor foi iniciado. Condições que não as mostradas abaixo devem ser documentadas com a respectiva aplicação do cliente.

```
psql: error: connection to server at "server.joe.com" (123.123.123.123), port 5432 failed: Connection refused
        Is the server running on that host and accepting TCP/IP connections?
```

Essa é a falha genérica de "não consegui encontrar um servidor para conversar". Parece o acima quando a comunicação TCP/IP é tentada. Um erro comum é esquecer de configurar [listen_addresses][(runtime-config-connection.md#GUC-LISTEN-ADDRESSES)] para que o servidor aceite conexões TCP remotas.

Como alternativa, você pode receber isso ao tentar comunicação de soquete de domínio Unix em um servidor local:

```
psql: error: connection to server on socket "/tmp/.s.PGSQL.5432" failed: No such file or directory
        Is the server running locally and accepting connections on that socket?
```

Se o servidor realmente estiver em execução, verifique se a ideia do cliente sobre o caminho do socket (aqui `/tmp`) está de acordo com a configuração do servidor do diretório de socket [unix_socket_directories](runtime-config-connection.md#GUC-UNIX-SOCKET-DIRECTORIES).

Uma mensagem de falha de conexão sempre exibe o endereço do servidor ou o nome do caminho de soquete, o que é útil para verificar se o cliente está tentando se conectar ao local correto. Se, de fato, não houver servidor ouvindo lá, a mensagem de erro do kernel geralmente será `Connection refused` ou `No such file or directory`, como ilustrado. (É importante perceber que `Connection refused` neste contexto *não* significa que o servidor recebeu a solicitação de conexão e a rejeitou. Esse caso produzirá uma mensagem diferente, conforme mostrado em [Seção 20.16][(client-authentication-problems.md "20.16. Authentication Problems")]). Outras mensagens de erro, como `Connection timed out`, podem indicar problemas mais fundamentais, como falta de conectividade de rede ou um firewall bloqueando a conexão.