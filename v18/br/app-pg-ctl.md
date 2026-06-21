## pg_ctl

pg_ctl — inicializar, iniciar, parar ou controlar um servidor PostgreSQL

## Sinopse

`pg_ctl` `init[db]` [`-D` *`datadir`* [`-s`] [`-o` *`initdb-options`*

`pg_ctl` `start` [`-D` *`datadir`* [`-l` *`filename`* [`-W`] [`-t` *`seconds`* [`-s`] [`-o` *`options`* [`-p` *`path`* [`-c`]

`pg_ctl` `stop` [`-D` *`datadir`* [`-m` `s[mart]` | `f[ast]` | `i[mmediate]` ] [`-W`] [`-t` *`seconds`* [`-s`]

`pg_ctl` `restart` [`-D` *`datadir`*] [`-m` `s[mart]` | `f[ast]` | `i[mmediate]` ] [`-W`] [`-t` *`seconds`*] [`-s`] [`-o` *`options`*] [`-c`]

`pg_ctl` `reload` [`-D` *`datadir`*] [`-s`]

`pg_ctl` `status` [`-D` *`datadir`*]

`pg_ctl` `promote` [`-D` *`datadir`*] [`-W`] [`-t` *`seconds`*] [`-s`]

`pg_ctl` `logrotate` [`-D` *`datadir`*] [`-s`]

`pg_ctl` `kill` *`signal_name`* *`process_id`*

Em Microsoft Windows, também:

`pg_ctl` `register` [`-D` *`datadir`*] [`-N` *`servicename`*] [`-U` *`username`*] [`-P` *`password`*] [`-S` `a[uto]` | `d[emand]` ] [`-e` *`source`*] [`-W`] [`-t` *`seconds`*] [`-s`] [`-o` *`options`*]

`pg_ctl` `unregister` [`-N` *`servicename`*]

## Descrição

pg_ctl é uma ferramenta para inicializar um clúster de banco de dados PostgreSQL, iniciar, parar ou reiniciar o servidor de banco de dados PostgreSQL ([postgres](app-postgres.md "postgres")), ou exibir o status de um servidor em execução. Embora o servidor possa ser iniciado manualmente, o pg_ctl encapsula tarefas como redirecionar a saída de log e desligar corretamente do terminal e do grupo de processos. Também oferece opções convenientes para desligamento controlado.

O modo `init` ou `initdb` cria um novo clúster de bancos de dados PostgreSQL, ou seja, uma coleção de bancos de dados que serão gerenciados por uma única instância do servidor. Esse modo invoca o comando `initdb`. Consulte [initdb](app-initdb.md "initdb") para obter detalhes.

O modo `start` inicia um novo servidor. O servidor é iniciado em segundo plano, e sua entrada padrão é anexada ao `/dev/null` (ou ao `nul` no Windows). Em sistemas semelhantes ao Unix, por padrão, a saída padrão e o erro padrão do servidor são enviados para a saída padrão do pg_ctl (não para o erro padrão). A saída padrão do pg_ctl deve então ser redirecionada para um arquivo ou canalizada para outro processo, como um programa de rotação de logs, como rotatelogs; caso contrário, o `postgres` escreverá sua saída para o terminal de controle (do segundo plano) e não deixará o grupo de processos do shell. No Windows, por padrão, a saída padrão e o erro padrão do servidor são enviados para o terminal. Esses comportamentos padrão podem ser alterados usando `-l` para anexar a saída do servidor a um arquivo de log. O uso de `-l` ou redirecionamento de saída é recomendado.

O modo `stop` desativa o servidor que está em execução no diretório de dados especificado. Três métodos diferentes de desligamento podem ser selecionados com a opção `-m`. O modo “Inteligente” impede novas conexões e, em seguida, espera que todos os clientes existentes se desconectem. Se o servidor estiver em modo de standby quente, a recuperação e a replicação em streaming serão terminadas assim que todos os clientes se desconectarem. O modo “Rápido” (o padrão) não espera que os clientes se desconectem. Todas as transações ativas são revertidas e os clientes são desconectados à força, e então o servidor é desligado. O modo “Imediato” abortará todos os processos do servidor imediatamente, sem um desligamento limpo. Essa escolha levará a um ciclo de recuperação em caso de falha durante a próxima inicialização do servidor.

O modo `restart` executa efetivamente um stop seguido de um start. Isso permite alterar as opções de linha de comando do comando `postgres`, ou alterar as opções do arquivo de configuração que não podem ser alteradas sem reiniciar o servidor. Se caminhos relativos foram usados na linha de comando durante o início do servidor, `restart` pode falhar, a menos que o pg_ctl seja executado no mesmo diretório atual em que foi durante o início do servidor.

O modo `reload` simplesmente envia ao servidor do processo `postgres` um sinal SIGHUP, fazendo com que ele leia novamente seus arquivos de configuração (`postgresql.conf`, `pg_hba.conf`, etc.). Isso permite que as opções dos arquivos de configuração que não exigem um reinício completo do servidor sejam aplicadas.

O modo `status` verifica se um servidor está em execução no diretório de dados especificado. Se estiver, o PID do servidor e as opções de linha de comando que foram usadas para invocá-lo são exibidos. Se o servidor não estiver em execução, o pg_ctl retorna um status de saída de 3. Se um diretório de dados acessível não for especificado, o pg_ctl retorna um status de saída de 4.

Os comandos do modo `promote` controlam o servidor de espera que está em execução no diretório de dados especificado para encerrar o modo de espera e iniciar operações de leitura e escrita.

O modo `logrotate` roda o arquivo de registro do servidor. Para obter detalhes sobre como usar esse modo com ferramentas de rotação de registro externas, consulte [Seção 24.3](logfile-maintenance.md).

O modo `kill` envia um sinal para um processo especificado. Isso é principalmente útil no Microsoft Windows, que não possui um comando de kill integrado. Use `--help` para ver uma lista dos nomes de sinal suportados.

O modo `register` registra o servidor PostgreSQL como um serviço do sistema no Microsoft Windows. A opção `-S` permite a seleção do tipo de início do serviço, ou seja, “auto” (comece o serviço automaticamente na inicialização do sistema) ou “demand” (comece o serviço sob demanda).

O modo `unregister` desregistra um serviço do sistema no Microsoft Windows. Isso anula os efeitos do comando `register`.

## Opções

`-c` `--core-files`: Tente permitir que as falhas do servidor produzam arquivos de núcleo, em plataformas onde isso é possível, levantando qualquer limite de recursos suaves colocado em arquivos de núcleo. Isso é útil na depuração ou diagnóstico de problemas, permitindo que uma traçada de pilha seja obtida de um processo de servidor falhado.

`-D datadir` `--pgdata=datadir`: Especifica a localização do sistema de arquivos dos arquivos de configuração do banco de dados. Se esta opção for omitida, a variável de ambiente `PGDATA` é usada.

`-l filename` `--log=filename`: Adicione a saída do log do servidor ao *`filename`*. Se o arquivo não existir, ele será criado. Por padrão, apenas o proprietário do clúster pode acessar o arquivo de log. Se o acesso por grupo estiver habilitado no clúster, os usuários do mesmo grupo que o proprietário do clúster também podem lê-lo.

`-m mode` `--mode=mode`: Especifica o modo de desligamento. *`mode`* pode ser `smart`, `fast`, ou `immediate`, ou a primeira letra de um desses três. Se esta opção for omitida, `fast` é a opção padrão.

`-o options` `--options=options`: Especifica as opções a serem passadas diretamente para o comando `postgres`. `-o` pode ser especificado várias vezes, com todas as opções fornecidas sendo passadas.

O *`options`* geralmente deve ser rodeado por aspas simples ou duplas para garantir que sejam passadas como um grupo.

`-o initdb-options` `--options=initdb-options`: Especifica as opções a serem passadas diretamente para o comando `initdb`. `-o` pode ser especificado várias vezes, com todas as opções fornecidas sendo passadas.

O *`initdb-options`* geralmente deve ser rodeado por aspas simples ou duplas para garantir que sejam passadas como um grupo.

`-p path`: Especifica o local do executável `postgres`. Por padrão, o executável `postgres` é retirado do mesmo diretório que `pg_ctl`, ou, caso contrário, do diretório de instalação pré-configurado. Não é necessário usar essa opção, a menos que você esteja fazendo algo incomum e obtenha erros de que o executável `postgres` não foi encontrado.

No modo `init`, esta opção especifica, de forma análoga, a localização do executável `initdb`.

`-s` `--silent`: Imprimir apenas erros, sem mensagens informativas.

`-t seconds` `--timeout=seconds`: Especifica o número máximo de segundos para esperar quando esperando uma operação completar (veja a opção `-w`). Tem como padrão o valor da variável de ambiente `PGCTLTIMEOUT` ou, se não definida, 60 segundos.

`-V` `--version`: Imprimir a versão do pg_ctl e sair.

`-w` `--wait`: Aguarde a operação ser concluída. Isso é suportado para os modos `start`, `stop`, `restart`, `promote` e `register`, e é o padrão para esses modos.

Ao esperar, `pg_ctl` verifica repetidamente o arquivo PID do servidor, dormindo por um curto período de tempo entre as verificações. O arranque é considerado completo quando o arquivo PID indica que o servidor está pronto para aceitar conexões. O desligamento é considerado completo quando o servidor remove o arquivo PID. `pg_ctl` retorna um código de saída com base no sucesso do arranque ou desligamento.

Se a operação não for concluída dentro do limite de tempo (consulte a opção `-t`), então `pg_ctl` sai com um status de saída não nulo. Mas observe que a operação pode continuar em segundo plano e, eventualmente, ter sucesso.

`-W` `--no-wait`: Não espere a operação ser concluída. Isso é o oposto da opção `-w`.

Se a espera estiver desativada, a ação solicitada é acionada, mas não há feedback sobre seu sucesso. Nesse caso, o arquivo de registro do servidor ou um sistema de monitoramento externo teria que ser usado para verificar o progresso e o sucesso da operação.

Em versões anteriores do PostgreSQL, isso era o padrão, exceto para o modo `stop`.

`-?` `--help`: Mostrar ajuda sobre os argumentos da linha de comando do comando pg_ctl e sair.

Se uma opção for especificada que é válida, mas não relevante para o modo operacional selecionado, o pg_ctl a ignora.

### Opções para Windows

`-e source`: Nome da fonte de eventos para o pg_ctl usar para registrar no log de eventos ao ser executado como um serviço do Windows. O padrão é `PostgreSQL`. Observe que isso controla apenas as mensagens enviadas pelo próprio pg_ctl; uma vez iniciado, o servidor usará a fonte de eventos especificada pelo seu parâmetro [event_source](runtime-config-logging.md#GUC-EVENT-SOURCE). Se o servidor falhar muito cedo no início, antes que esse parâmetro tenha sido definido, ele também pode registrar usando o nome padrão da fonte de eventos `PostgreSQL`.

`-N servicename`: Nome do serviço do sistema a registrar. Esse nome será usado tanto como nome do serviço quanto como nome de exibição. O padrão é `PostgreSQL`.

`-P password`: Senha para o usuário executar o serviço como.

`-S start-type`: Tipo de início do serviço do sistema. *`start-type`* pode ser `auto`, ou `demand`, ou a primeira letra de um desses dois. Se esta opção for omitida, `auto` é a opção padrão.

`-U username`: Nome do usuário para o usuário executar o serviço. Para usuários de domínio, use o formato `DOMAIN\username`.

## Meio Ambiente

`PGCTLTIMEOUT`: Limite padrão no número de segundos a esperar quando esperando que o arranque ou o desligamento sejam concluídos. Se não definido, o padrão é de 60 segundos.

`PGDATA`: Local padrão do diretório de dados.

A maioria dos modos do `pg_ctl` exige o conhecimento da localização do diretório de dados; portanto, a opção `-D` é necessária, a menos que o `PGDATA` esteja definido.

Para variáveis adicionais que afetam o servidor, consulte [postgres](app-postgres.md).

## Arquivos

`postmaster.pid`: O pg_ctl examina este arquivo no diretório de dados para determinar se o servidor está em execução atualmente.

`postmaster.opts`: Se este arquivo existir no diretório de dados, o pg_ctl (no modo `restart`) passará o conteúdo do arquivo como opções para o postgres, a menos que a opção `-o` seja sobrescrita. O conteúdo deste arquivo também é exibido no modo `status`.

## Exemplos

### Iniciando o servidor

Para iniciar o servidor, espere até que o servidor esteja aceitando conexões:

```
$ pg_ctl start
```

Para iniciar o servidor usando a porta 5433 e executando sem `fsync`, use:

```
$ pg_ctl -o "-F -p 5433" start
```

### Parar o servidor

Para parar o servidor, use:

```
$ pg_ctl stop
```

A opção `-m` permite o controle de *como* o servidor é desligado:

```
$ pg_ctl stop -m smart
```

### Reiniciando o servidor

Reiniciar o servidor é quase equivalente a parar o servidor e iniciá-lo novamente, exceto que, por padrão, `pg_ctl` salva e reutiliza as opções de linha de comando que foram passadas para a instância anteriormente em execução. Para reiniciar o servidor usando as mesmas opções do que antes, use:

```
$ pg_ctl restart
```

Mas se `-o` for especificado, ele substituirá todas as opções anteriores. Para reiniciar o uso da porta 5433, desative `fsync` após o reinício:

```
$ pg_ctl -o "-F -p 5433" restart
```

### Mostrar o status do servidor

Aqui está uma amostra de saída de status do pg_ctl:

```
$ pg_ctl status

pg_ctl: server is running (PID: 13718)
/usr/local/pgsql/bin/postgres "-D" "/usr/local/pgsql/data" "-p" "5433" "-B" "128"
```

A segunda linha é o comando que seria invocado no modo de reinício.

## Veja também

[initdb](app-initdb.md "initdb"), [postgres](app-postgres.md "postgres")