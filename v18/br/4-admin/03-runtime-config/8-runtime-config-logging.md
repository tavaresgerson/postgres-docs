## 19.8. Relatório e registro de erros [#](#RUNTIME-CONFIG-LOGGING)

* [19.8.1. Onde registrar](runtime-config-logging.md#RUNTIME-CONFIG-LOGGING-WHERE)
* [19.8.2. Quando registrar](runtime-config-logging.md#RUNTIME-CONFIG-LOGGING-WHEN)
* [19.8.3. O que registrar](runtime-config-logging.md#RUNTIME-CONFIG-LOGGING-WHAT)
* [19.8.4. Usando saída de registro no formato CSV](runtime-config-logging.md#RUNTIME-CONFIG-LOGGING-CSVLOG)
* [19.8.5. Usando saída de registro no formato JSON](runtime-config-logging.md#RUNTIME-CONFIG-LOGGING-JSONLOG)
* [19.8.6. Título do processo](runtime-config-logging.md#RUNTIME-CONFIG-LOGGING-PROC-TITLE)

### 19.8.1. Onde fazer o registro [#](#RUNTIME-CONFIG-LOGGING-WHERE)

`log_destination` (`string`) [#](#GUC-LOG-DESTINATION): O PostgreSQL suporta vários métodos para registrar mensagens do servidor, incluindo stderr, csvlog, jsonlog e syslog. No Windows, o eventlog também é suportado. Defina este parâmetro em uma lista de destinos de registro desejados separados por vírgulas. O padrão é registrar apenas no stderr. Este parâmetro só pode ser definido no arquivo `postgresql.conf` ou na linha de comando do servidor.

Se o csvlog estiver incluído em `log_destination`, as entradas de log são exibidas no formato de valor separado por vírgula (CSV), o que é conveniente para carregar logs em programas. Consulte [Seção 19.8.4](runtime-config-logging.md#RUNTIME-CONFIG-LOGGING-CSVLOG) para obter detalhes. [logging_collector](runtime-config-logging.md#GUC-LOGGING-COLLECTOR) deve ser habilitado para gerar saída de log no formato CSV.

Se o jsonlog estiver incluído em `log_destination`, as entradas de log são exibidas em formato JSON, o que é conveniente para carregar logs em programas. Consulte [Seção 19.8.5](runtime-config-logging.md#RUNTIME-CONFIG-LOGGING-JSONLOG) para obter detalhes. [logging_collector](runtime-config-logging.md#GUC-LOGGING-COLLECTOR) deve ser habilitado para gerar saída de log em formato JSON.

Quando o stderr, csvlog ou jsonlog são incluídos, o arquivo `current_logfiles` é criado para registrar a localização do(s) arquivo(s) de log atualmente utilizado(s) pelo coletor de registro e o destino de registro associado. Isso fornece uma maneira conveniente de encontrar os logs atualmente utilizados pela instância. Aqui está um exemplo do conteúdo desse arquivo:

```
stderr log/postgresql.log csvlog log/postgresql.csv jsonlog log/postgresql.json
```

`current_logfiles` é recriado quando um novo arquivo de registro é criado como efeito da rotação e quando `log_destination` é recarregado. Ele é removido quando nenhum dos arquivos stderr, csvlog ou jsonlog estão incluídos em `log_destination`, e quando o coletor de registro é desativado.

Nota

Na maioria dos sistemas Unix, você precisará alterar a configuração do daemon syslog do seu sistema para poder utilizar a opção syslog para `log_destination`. O PostgreSQL pode registrar em instalações syslog `LOCAL0` através de `LOCAL7` (consulte [syslog_facility](runtime-config-logging.md#GUC-SYSLOG-FACILITY)), mas a configuração padrão de syslog na maioria das plataformas descartará todas essas mensagens. Você precisará adicionar algo como:

```
local0.*    /var/log/postgresql
```

para o arquivo de configuração do daemon syslog para que ele funcione.

Em Windows, quando você usa a opção `eventlog` para `log_destination`, você deve registrar uma fonte de evento e sua biblioteca com o sistema operacional para que o Visualizador de Eventos do Windows possa exibir mensagens do registro de eventos de forma limpa. Consulte [Seção 18.12](event-log-registration.md) para obter detalhes.

`logging_collector` (`boolean`) [#](#GUC-LOGGING-COLLECTOR): Este parâmetro habilita o *coletador de logs*, que é um processo em segundo plano que captura mensagens de log enviadas para o stderr e as redireciona para arquivos de log. Essa abordagem é frequentemente mais útil do que fazer log no syslog, pois alguns tipos de mensagens podem não aparecer na saída do syslog. (Um exemplo comum são as mensagens de falha de dinâmica de ligação; outro são as mensagens de erro produzidas por scripts como `archive_command`.) Este parâmetro só pode ser definido no início do servidor.

Nota

É possível fazer log no stderr sem usar o coletor de log; as mensagens de log irão para onde o stderr do servidor está direcionado. No entanto, esse método é adequado apenas para volumes de log baixos, pois não oferece nenhuma maneira conveniente de rotação de arquivos de log. Além disso, em algumas plataformas que não usam o coletor de log, pode resultar em saída de log perdida ou distorcida, porque vários processos escrevendo simultaneamente no mesmo arquivo de log podem sobrepor a saída dos outros.

Nota

O coletor de registro é projetado para nunca perder mensagens. Isso significa que, em caso de carga extremamente alta, os processos do servidor podem ser bloqueados enquanto tenta enviar mensagens de registro adicionais quando o coletor fica para trás. Em contraste, o syslog prefere descartar mensagens se não conseguir escrevê-las, o que significa que pode falhar em registrar algumas mensagens nesses casos, mas não bloqueará o resto do sistema.

`log_directory` (`string`) [#](#GUC-LOG-DIRECTORY): Quando o `logging_collector` está habilitado, este parâmetro determina o diretório em que os arquivos de registro serão criados. Pode ser especificado como um caminho absoluto ou relativo ao diretório de dados do cluster. Este parâmetro só pode ser definido no arquivo `postgresql.conf` ou na linha de comando do servidor. O padrão é `log`.

`log_filename` (`string`) [#](#GUC-LOG-FILENAME): Quando o `logging_collector` está habilitado, este parâmetro define os nomes dos arquivos dos arquivos de registro criados. O valor é tratado como um padrão `strftime`, portanto, `%`-escapes podem ser usados para especificar nomes de arquivos variáveis no tempo. (Observe que, se houver `%`-escapes dependentes do fuso horário, o cálculo é feito na zona especificada por [log_timezone](runtime-config-logging.md#GUC-LOG-TIMEZONE).]) Os `%`-escapes suportados são semelhantes aos listados na especificação do Open Group [strftime](https://pubs.opengroup.org/onlinepubs/009695399/functions/strftime.html). Note que o `strftime` do sistema não é usado diretamente, portanto, extensões específicas da plataforma (não padronizadas) não funcionam. O padrão é `postgresql-%Y-%m-%d_%H%M%S.log`.

Se você especificar um nome de arquivo sem escapamentos, você deve planejar usar um utilitário de rotação de log para evitar acabar preenchendo todo o disco. Em versões anteriores à 8.4, se não houvesse `%` escapamentos, o PostgreSQL anexaria a época do tempo de criação do novo arquivo de log, mas isso não é mais o caso.

Se a saída em formato CSV estiver habilitada em `log_destination`, `.csv` será anexado ao nome do arquivo de registro com marcação de tempo para criar o nome do arquivo para a saída em formato CSV. (Se `log_filename` terminar em `.log`, o sufixo é substituído em vez disso.)

Se a saída em formato JSON estiver habilitada em `log_destination`, `.json` será anexado ao nome do arquivo de registro com marcação de tempo para criar o nome do arquivo para a saída em formato JSON. (Se `log_filename` terminar em `.log`, o sufixo é substituído em vez disso.)

Este parâmetro só pode ser definido no arquivo `postgresql.conf` ou na linha de comando do servidor.

`log_file_mode` (`integer`) [#](#GUC-LOG-FILE-MODE): Nos sistemas Unix, este parâmetro define as permissões para os arquivos de registro quando o `logging_collector` está habilitado. (Nos sistemas Microsoft Windows, este parâmetro é ignorado.) O valor do parâmetro deve ser um modo numérico especificado no formato aceito pelas chamadas de sistema `chmod` e `umask`. (Para usar o formato octal comum, o número deve começar com um `0` (zero).)

Os permissões padrão são `0600`, o que significa que apenas o proprietário do servidor pode ler ou escrever os arquivos de registro. O outro ajuste comumente útil é `0640`, permitindo que membros do grupo do proprietário leiam os arquivos. No entanto, observe que, para utilizar esse ajuste, você precisará alterar [log_directory](runtime-config-logging.md#GUC-LOG-DIRECTORY) para armazenar os arquivos em algum lugar fora do diretório de dados do cluster. Em qualquer caso, não é prudente tornar os arquivos de registro mundialmente legíveis, pois eles podem conter dados sensíveis.

Este parâmetro só pode ser definido no arquivo `postgresql.conf` ou na linha de comando do servidor.

`log_rotation_age` (`integer`) [#](#GUC-LOG-ROTATION-AGE): Quando o `logging_collector` está habilitado, este parâmetro determina o tempo máximo a ser usado em um arquivo de registro individual, após o qual um novo arquivo de registro será criado. Se este valor for especificado sem unidades, ele será considerado em minutos. O padrão é de 24 horas. Defina como zero para desabilitar a criação de novos arquivos de registro baseada no tempo. Este parâmetro só pode ser definido no arquivo `postgresql.conf` ou na linha de comando do servidor.

`log_rotation_size` (`integer`) [#](#GUC-LOG-ROTATION-SIZE): Quando o `logging_collector` está habilitado, este parâmetro determina o tamanho máximo de um arquivo de registro individual. Após essa quantidade de dados ter sido emitida em um arquivo de registro, um novo arquivo de registro será criado. Se este valor for especificado sem unidades, ele será considerado em kilobytes. O padrão é de 10 megabytes. Defina como zero para desabilitar a criação de novos arquivos de registro com base no tamanho. Este parâmetro só pode ser definido no arquivo `postgresql.conf` ou na linha de comando do servidor.

`log_truncate_on_rotation` (`boolean`) [#](#GUC-LOG-TRUNCATE-ON-ROTATION): Quando o `logging_collector` está habilitado, este parâmetro fará com que o PostgreSQL trunque (escreva sobre) em vez de anexar, qualquer arquivo de registro existente com o mesmo nome. No entanto, o truncamento ocorrerá apenas quando um novo arquivo estiver sendo aberto devido à rotação baseada no tempo, não durante o inicialização do servidor ou rotação baseada no tamanho. Quando desativado, os arquivos pré-existentes serão anexados em todos os casos. Por exemplo, usando este ajuste em combinação com um `log_filename` como `postgresql-%H.log`, resultaria na geração de arquivos de registro horários de vinte e quatro horas e, em seguida, sobrescritos cíclicamente. Este parâmetro só pode ser definido no arquivo `postgresql.conf` ou na linha de comando do servidor.

Exemplo: Para manter 7 dias de registros, um arquivo de registro por dia com o nome `server_log.Mon`, `server_log.Tue`, etc., e sobrescrever automaticamente o registro da semana passada com o registro desta semana, defina `log_filename` para `server_log.%a`, `log_truncate_on_rotation` para `on`, e `log_rotation_age` para `1440`.

Exemplo: Para manter 24 horas de registros, um arquivo de registro por hora, mas também rotular mais cedo se o tamanho do arquivo de registro exceder 1 GB, defina `log_filename` para `server_log.%H%M`, `log_truncate_on_rotation` para `on`, `log_rotation_age` para `60` e `log_rotation_size` para `1000000`. Incluir `%M` em `log_filename` permite que quaisquer rotações baseadas no tamanho que possam ocorrer selecionem um nome de arquivo diferente do nome inicial do arquivo da hora.

`syslog_facility` (`enum`) [#](#GUC-SYSLOG-FACILITY): Quando o registro no syslog está habilitado, este parâmetro determina o "facilidade" do syslog a ser utilizado. Você pode escolher entre `LOCAL0`, `LOCAL1`, `LOCAL2`, `LOCAL3`, `LOCAL4`, `LOCAL5`, `LOCAL6`, `LOCAL7`; o padrão é `LOCAL0`. Veja também a documentação do daemon de syslog do seu sistema. Este parâmetro só pode ser definido no arquivo `postgresql.conf` ou na linha de comando do servidor.

`syslog_ident` (`string`) [#](#GUC-SYSLOG-IDENT): Quando o registro no syslog está habilitado, este parâmetro determina o nome do programa usado para identificar as mensagens do PostgreSQL nos registros do syslog. O padrão é `postgres`. Este parâmetro só pode ser definido no arquivo `postgresql.conf` ou na linha de comando do servidor.

`syslog_sequence_numbers` (`boolean`) [#](#GUC-SYSLOG-SEQUENCE-NUMBERS): Ao fazer log no syslog e este estar ativado (o padrão), cada mensagem será prefixada por um número de sequência crescente (como `[2]`). Isso evita a supressão de "--- última mensagem repetida N vezes ---" que muitas implementações de syslog realizam por padrão. Em implementações de syslog mais modernas, a supressão de mensagens repetidas pode ser configurada (por exemplo, `$RepeatedMsgReduction` no rsyslog), então isso pode não ser necessário. Além disso, você pode desativá-lo se realmente quiser suprimir mensagens repetidas.

Este parâmetro só pode ser definido no arquivo `postgresql.conf` ou na linha de comando do servidor.

`syslog_split_messages` (`boolean`) [#](#GUC-SYSLOG-SPLIT-MESSAGES): Quando o registro no syslog está habilitado, este parâmetro determina como as mensagens são entregues ao syslog. Quando ativado (o padrão), as mensagens são divididas por linhas e as longas linhas são divididas para que se encaixem em 1024 bytes, que é um limite de tamanho típico para implementações tradicionais de syslog. Quando desativado, as mensagens de log do servidor PostgreSQL são entregues ao serviço syslog como está, e cabe ao serviço syslog lidar com as mensagens potencialmente volumosas.

Se o syslog estiver registrando mensagens em um arquivo de texto, o efeito será o mesmo em qualquer caso, e é melhor deixar a configuração ativada, pois a maioria das implementações de syslog não consegue lidar com mensagens grandes ou precisaria ser configurada especialmente para lidar com elas. Mas se o syslog estiver escrevendo mensagens em algum outro meio, pode ser necessário ou mais útil manter as mensagens logicamente juntas.

Este parâmetro só pode ser definido no arquivo `postgresql.conf` ou na linha de comando do servidor.

`event_source` (`string`) [#](#GUC-EVENT-SOURCE): Quando o registro no log de eventos está habilitado, este parâmetro determina o nome do programa usado para identificar as mensagens do PostgreSQL no log. O padrão é `PostgreSQL`. Este parâmetro só pode ser definido na inicialização do servidor.

### 19.8.2. Quando fazer o registro [#](#RUNTIME-CONFIG-LOGGING-WHEN)

`log_min_messages` (`enum`) [#](#GUC-LOG-MIN-MESSAGES): Controla quais níveis de [mensagens](runtime-config-logging.md#RUNTIME-CONFIG-SEVERITY-LEVELS "Table 19.2. Message Severity Levels") são escritos no log do servidor. Os valores válidos são `DEBUG5`, `DEBUG4`, `DEBUG3`, `DEBUG2`, `DEBUG1`, `INFO`, `NOTICE`, `WARNING`, `ERROR`, `LOG`, `FATAL` e `PANIC`. Cada nível inclui todos os níveis que o seguem. Quanto mais recente o nível, menos mensagens são enviadas para o log. O padrão é `WARNING`. Note que `LOG` tem um rank diferente aqui do que em [client_min_messages](runtime-config-client.md#GUC-CLIENT-MIN-MESSAGES). Apenas usuários super e usuários com o privilégio apropriado `SET` podem alterar esta configuração.

`log_min_error_statement` (`enum`) [#](#GUC-LOG-MIN-ERROR-STATEMENT): Controla quais instruções SQL que causam uma condição de erro são registradas no log do servidor. A instrução SQL atual é incluída na entrada do log para qualquer mensagem do [severidade](runtime-config-logging.md#RUNTIME-CONFIG-SEVERITY-LEVELS) ou superior. Os valores válidos são `DEBUG5`, `DEBUG4`, `DEBUG3`, `DEBUG2`, `DEBUG1`, `INFO`, `NOTICE`, `WARNING`, `ERROR`, `LOG`, `FATAL` e `PANIC`. O padrão é `ERROR`, o que significa que instruções que causam erros, mensagens de log, erros fatais ou pânico serão registradas. Para efetivamente desativar o registro de instruções que falham, defina este parâmetro para `PANIC`. Somente usuários superusuários e usuários com o privilégio apropriado `SET` podem alterar esta configuração.

`log_min_duration_statement` (`integer`) [#](#GUC-LOG-MIN-DURATION-STATEMENT): Faz com que a duração de cada declaração concluída seja registrada se a declaração tiver sido executada por pelo menos o tempo especificado. Por exemplo, se você defini-lo como `250ms`, todas as declarações SQL que executam 250 ms ou mais serão registradas. Habilitar este parâmetro pode ser útil para localizar consultas não otimizadas em seus aplicativos. Se este valor for especificado sem unidades, ele é considerado em milissegundos. Definir este valor como zero imprime todas as durações das declarações. `-1` (o padrão) desabilita a registro das durações das declarações. Somente usuários super e usuários com o privilégio apropriado `SET` podem alterar esta configuração.

Isso substitui [log_min_duration_sample](runtime-config-logging.md#GUC-LOG-MIN-DURATION-SAMPLE), o que significa que as consultas com duração que excederem essa configuração não são sujeitas a amostragem e são sempre registradas.

Para clientes que utilizam o protocolo de consulta estendida, as durações das etapas de Parse, Bind e Execute são registradas de forma independente.

Nota

Ao usar esta opção juntamente com [log_statement](runtime-config-logging.md#GUC-LOG-STATEMENT), o texto das declarações que são registradas devido a `log_statement` não será repetido na mensagem do log de duração. Se você não estiver usando syslog, é recomendável que você registre o PID ou o ID de sessão usando [log_line_prefix](runtime-config-logging.md#GUC-LOG-LINE-PREFIX) para que você possa vincular a mensagem da declaração à mensagem de duração posterior usando o ID de processo ou o ID de sessão.

`log_min_duration_sample` (`integer`) [#](#GUC-LOG-MIN-DURATION-SAMPLE): Permite a amostragem da duração das declarações concluídas que foram executadas por pelo menos o período especificado. Isso produz o mesmo tipo de entradas de log que [log_min_duration_statement](runtime-config-logging.md#GUC-LOG-MIN-DURATION-STATEMENT), mas apenas para um subconjunto das declarações executadas, com a taxa de amostragem controlada por [log_statement_sample_rate](runtime-config-logging.md#GUC-LOG-STATEMENT-SAMPLE-RATE). Por exemplo, se você defini-lo como `100ms`, todas as declarações SQL que executam 100ms ou mais serão consideradas para amostragem. Ativação deste parâmetro pode ser útil quando o tráfego é muito alto para registrar todas as consultas. Se este valor for especificado sem unidades, ele é considerado em milissegundos. Definir isso como zero amostra todas as durações das declarações. `-1` (o padrão) desativa a amostragem das durações das declarações. Apenas usuários super e usuários com o privilégio apropriado `SET` podem alterar este ajuste.

Essa configuração tem prioridade menor que `log_min_duration_statement`, o que significa que as declarações com durações que excedem `log_min_duration_statement` não são sujeitas a amostragem e são sempre registradas.

Outras notas para `log_min_duration_statement` também se aplicam a este ajuste.

`log_statement_sample_rate` (`floating point`) [#](#GUC-LOG-STATEMENT-SAMPLE-RATE): Determina a fração de declarações com duração superior a [log_min_duration_sample](runtime-config-logging.md#GUC-LOG-MIN-DURATION-SAMPLE) que serão registradas. A amostragem é estocástica, por exemplo, `0.5` significa que há estatisticamente uma chance em dois de que qualquer declaração dada seja registrada. O padrão é `1.0`, o que significa registrar todas as declarações amostradas. Definir isso como zero desativa o registro da duração das declarações amostradas, o mesmo que definir `log_min_duration_sample` para `-1`. Somente superusuários e usuários com o privilégio apropriado `SET` podem alterar essa configuração.

`log_transaction_sample_rate` (`floating point`) [#](#GUC-LOG-TRANSACTION-SAMPLE-RATE): Define a fração de transações cujas declarações estão todas registradas, além das declarações registradas por outros motivos. Aplica-se a cada nova transação, independentemente da duração de suas declarações. A amostragem é estocástica, por exemplo, `0.1` significa que há estatisticamente uma chance em dez de que qualquer transação dada seja registrada. `log_transaction_sample_rate` pode ser útil para construir uma amostra de transações. O padrão é `0`, o que significa não registrar declarações de quaisquer transações adicionais. Definir isso para `1` registra todas as declarações de todas as transações. Apenas superusuários e usuários com o privilégio apropriado `SET` podem alterar essa configuração.

Nota

Como todas as opções de registro de declarações, esta opção pode adicionar um custo significativo.

`log_startup_progress_interval` (`integer`) [#](#GUC-LOG-STARTUP-PROGRESS-INTERVAL): Define o tempo após o qual o processo de inicialização registrará uma mensagem sobre uma operação de longa duração que ainda está em progresso, bem como o intervalo entre as próximas mensagens de progresso para essa operação. O padrão é de 10 segundos. Uma configuração de `0` desativa o recurso. Se esse valor for especificado sem unidades, ele é considerado em milissegundos. Este ajuste é aplicado separadamente para cada operação. Este parâmetro só pode ser definido no arquivo `postgresql.conf` ou na linha de comando do servidor.

Por exemplo, se a sincronização do diretório de dados leva 25 segundos e, posteriormente, o restabelecimento de relações não registradas leva 8 segundos, e se essa configuração tiver o valor padrão de 10 segundos, então mensagens serão registradas para a sincronização do diretório de dados após ele ter ocorrido por 10 segundos e novamente após ter ocorrido por 20 segundos, mas nada será registrado para o restabelecimento de relações não registradas.

[Tabela 19.2](runtime-config-logging.md#RUNTIME-CONFIG-SEVERITY-LEVELS) explica os níveis de gravidade da mensagem usados pelo PostgreSQL. Se a saída de registro for enviada para o syslog ou o registro de eventos do Windows, os níveis de gravidade são traduzidos conforme mostrado na tabela.

**Tabela 19.2. Níveis de gravidade da mensagem**



<table>
 <colgroup>
  <col class="col1"/>
  <col class="col2"/>
  <col class="col3"/>
  <col class="col4"/>
 </colgroup>
 <thead>
  <tr>
   <th>
    Severity
   </th>
   <th>
    Uso
   </th>
   <th>
    <span class="systemitem">
     syslog
    </span>
   </th>
   <th>
    <span class="systemitem">
     eventlog
    </span>
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <code>
     DEBUG1 .. DEBUG5
    </code>
   </td>
   <td>
    Fornece informações sucessivamente mais detalhadas para uso por desenvolvedores.
   </td>
   <td>
    <code>
     DEBUG
    </code>
   </td>
   <td>
    <code>
     INFORMATION
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     INFO
    </code>
   </td>
   <td>
    Fornece informações implicitamente solicitadas pelo usuário, por exemplo, saída de
    <code>
     VACUUM VERBOSE
    </code>
    .
   </td>
   <td>
    <code>
     INFO
    </code>
   </td>
   <td>
    <code>
     INFORMATION
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     NOTICE
    </code>
   </td>
   <td>
    Fornece informações que podem ser úteis para os usuários, como aviso sobre a redução de identificadores longos.
   </td>
   <td>
    <code>
     NOTICE
    </code>
   </td>
   <td>
    <code>
     INFORMATION
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     WARNING
    </code>
   </td>
   <td>
    Fornece avisos sobre problemas prováveis, por exemplo,
    <code>
     COMMIT
    </code>
    fora de um bloco de transação.
   </td>
   <td>
    <code>
     NOTICE
    </code>
   </td>
   <td>
    <code>
     WARNING
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     ERROR
    </code>
   </td>
   <td>
    Relata um erro que causou o cancelamento do comando atual.
   </td>
   <td>
    <code>
     WARNING
    </code>
   </td>
   <td>
    <code>
     ERROR
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     LOG
    </code>
   </td>
   <td>
    Relata informações de interesse para os administradores, como a atividade do ponto de controle.
   </td>
   <td>
    <code>
     INFO
    </code>
   </td>
   <td>
    <code>
     INFORMATION
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     FATAL
    </code>
   </td>
   <td>
    Relata um erro que causou o cancelamento da sessão atual.
   </td>
   <td>
    <code>
     ERR
    </code>
   </td>
   <td>
    <code>
     ERROR
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code>
     PANIC
    </code>
   </td>
   <td>
    Relata um erro que fez com que todas as sessões do banco de dados sejam interrompidas.
   </td>
   <td>
    <code>
     CRIT
    </code>
   </td>
   <td>
    <code>
     ERROR
    </code>
   </td>
  </tr>
 </tbody>
</table>







### 19.8.3. O que registrar [#](#RUNTIME-CONFIG-LOGGING-WHAT)

Nota

O que você escolhe registrar pode ter implicações de segurança; veja [Seção 24.3](logfile-maintenance.md).

`application_name` (`string`) [#](#GUC-APPLICATION-NAME): O `application_name` pode ser qualquer string com menos de `NAMEDATALEN` caracteres (64 caracteres em uma compilação padrão). Normalmente, é definido por uma aplicação ao se conectar ao servidor. O nome será exibido na exibição `pg_stat_activity` e incluído nas entradas de registro CSV. Também pode ser incluído em entradas de registro regulares via o parâmetro [log_line_prefix](runtime-config-logging.md#GUC-LOG-LINE-PREFIX). Apenas caracteres ASCII imprimíveis podem ser usados no valor `application_name`. Outros caracteres são substituídos por escapes hexadecimais em estilo C (sql-syntax-lexical.md#SQL-SYNTAX-STRINGS-ESCAPE "4.1.2.2. String Constants with C-Style Escapes").

`debug_print_parse` (`boolean`) `debug_print_rewritten` (`boolean`) `debug_print_plan` (`boolean`) [#](#GUC-DEBUG-PRINT-PARSE): Esses parâmetros permitem que várias saídas de depuração sejam emitidas. Quando definidos, eles imprimem a árvore de parse resultante, a saída do reescritor de consulta ou o plano de execução para cada consulta executada. Essas mensagens são emitidas no nível de mensagem `LOG`, então, por padrão, elas aparecerão no log do servidor, mas não serão enviadas ao cliente. Você pode alterar isso ajustando [client_min_messages](runtime-config-client.md#GUC-CLIENT-MIN-MESSAGES) e/ou [log_min_messages](runtime-config-logging.md#GUC-LOG-MIN-MESSAGES). Esses parâmetros estão desativados por padrão.

`debug_pretty_print` (`boolean`) [#](#GUC-DEBUG-PRETTY-PRINT): Quando definido, `debug_pretty_print` indenta as mensagens produzidas por `debug_print_parse`, `debug_print_rewritten` ou `debug_print_plan`. Isso resulta em uma saída mais legível, mas muito mais longa do que o formato "compacto" usado quando está desligado. Está ativado por padrão.

`log_autovacuum_min_duration` (`integer`) [#](#GUC-LOG-AUTOVACUUM-MIN-DURATION): Registra cada ação executada pelo autovacuum se ela foi executada por pelo menos o tempo especificado. Definindo esse valor como zero, todas as ações do autovacuum são registradas. `-1` desabilita o registro das ações do autovacuum. Se esse valor for especificado sem unidades, ele é considerado em milissegundos. Por exemplo, se você definir isso para `250ms`, todos os vazamentos e análises automáticos que duram 250 ms ou mais serão registrados. Além disso, quando esse parâmetro é definido para qualquer valor diferente de `-1`, uma mensagem será registrada se uma ação do autovacuum for ignorada devido a um bloqueio conflitante ou a uma relação descartada simultaneamente. O padrão é `10min`. Habilitar esse parâmetro pode ser útil para acompanhar a atividade do autovacuum. Esse parâmetro só pode ser definido no arquivo `postgresql.conf` ou na linha de comando do servidor; mas o ajuste pode ser sobrescrito para tabelas individuais alterando os parâmetros de armazenamento da tabela.

`log_checkpoints` (`boolean`) [#](#GUC-LOG-CHECKPOINTS): Faça com que os pontos de verificação e os pontos de reinício sejam registrados no log do servidor. Algumas estatísticas são incluídas nas mensagens de log, incluindo o número de buffers escritos e o tempo gasto escrevendo-os. Este parâmetro só pode ser definido no arquivo `postgresql.conf` ou na linha de comando do servidor. O padrão é ativado.

`log_connections` (`string`) [#](#GUC-LOG-CONNECTIONS): Faz com que os aspectos de cada conexão com o servidor sejam registrados. O padrão é a string vazia, `''`, que desativa todo o registro de conexão. As seguintes opções podem ser especificadas sozinhas ou em uma lista separada por vírgula:

**Tabela 19.3. Opções de Conexão de Log**



<table>
 <colgroup>
  <col class="col1"/>
  <col class="col2"/>
 </colgroup>
 <thead>
  <tr>
   <th>
    Name
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
     receipt
    </code>
   </td>
   <td>
    Registra o recebimento de uma conexão.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     authentication
    </code>
   </td>
   <td>
    Registra a identidade original usada por um método de autenticação para identificar um usuário. Na maioria dos casos, a string de identidade corresponde à
    <span class="productname">
     PostgreSQL
    </span>
    nome de usuário, mas alguns métodos de autenticação de terceiros podem alterar o identificador original do usuário antes de o servidor armazená-lo. A autenticação falha é sempre registrada, independentemente do valor desta configuração.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     authorization
    </code>
   </td>
   <td>
    Registra o sucesso da conclusão da autorização. Neste ponto, a conexão foi estabelecida, mas o backend ainda não está totalmente configurado. A mensagem de log inclui o nome de usuário autorizado, bem como o nome do banco de dados e o nome da aplicação, se aplicável.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     setup_durations
    </code>
   </td>
   <td>
    Registra o tempo gasto para estabelecer a conexão e configurar o backend até que a conexão esteja pronta para executar sua primeira consulta. A mensagem de log inclui três durações: a duração total de configuração (iniciando quando o postmaster aceita a conexão recebida e terminando quando a conexão está pronta para consulta), o tempo que levou para bifurcar o novo backend e o tempo que levou para autenticar o usuário.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     all
    </code>
   </td>
   <td>
    Um alias de conveniência equivalente a especificar todas as opções. Se
    <code>
     all
    </code>
    Se estiver especificado em uma lista de outras opções, todos os aspectos da conexão serão registrados.
   </td>
  </tr>
 </tbody>
</table>










O registro de desconexões é controlado separadamente por [log_disconnections](runtime-config-logging.md#GUC-LOG-DISCONNECTIONS).

Para fins de compatibilidade reversa, `on`, `off`, `true`, `false`, `yes`, `no`, `1` e `0` ainda são suportados. Os valores positivos são equivalentes ao especificar as opções de `receipt`, `authentication` e `authorization`.

Apenas superusuários e usuários com o privilégio apropriado `SET` podem alterar este parâmetro no início da sessão, e não pode ser alterado em nenhuma hipótese dentro de uma sessão.

Nota

Alguns programas de cliente, como o psql, tentam se conectar duas vezes para determinar se é necessária uma senha, portanto, mensagens duplicadas de "conexão recebida" não indicam necessariamente um problema.

`log_disconnections` (`boolean`) [#](#GUC-LOG-DISCONNECTIONS): Faz com que as terminações de sessão sejam registradas. A saída do log fornece informações semelhantes a `log_connections`, além da duração da sessão. Apenas usuários super e usuários com o privilégio apropriado `SET` podem alterar este parâmetro no início da sessão, e não pode ser alterado em nenhuma sessão. O padrão é `off`.

`log_duration` (`boolean`) [#](#GUC-LOG-DURATION): Faz com que a duração de cada declaração concluída seja registrada. O padrão é `off`. Somente usuários superusuários e usuários com o privilégio apropriado `SET` podem alterar essa configuração.

Para clientes que utilizam o protocolo de consulta estendida, as durações das etapas de Parse, Bind e Execute são registradas de forma independente.

Nota

A diferença entre habilitar `log_duration` e definir [log_min_duration_statement](runtime-config-logging.md#GUC-LOG-MIN-DURATION-STATEMENT) como zero é que exceder `log_min_duration_statement` obriga o texto da consulta a ser registrado, mas essa opção não faz isso. Assim, se `log_duration` for `on` e `log_min_duration_statement` tiver um valor positivo, todas as durações são registradas, mas o texto da consulta é incluído apenas para declarações que excedem o limite. Esse comportamento pode ser útil para coletar estatísticas em instalações com alto tráfego.

`log_error_verbosity` (`enum`) [#](#GUC-LOG-ERROR-VERBOSITY): Controla a quantidade de detalhes escritos no log do servidor para cada mensagem que é registrada. Os valores válidos são `TERSE`, `DEFAULT` e `VERBOSE`, cada um adicionando mais campos aos mensagens exibidas. `TERSE` exclui o registro de informações de erro de `DETAIL`, `HINT`, `QUERY` e `CONTEXT`. A saída de `VERBOSE` inclui o código de erro `SQLSTATE` (consulte também [Apêndice A](errcodes-appendix.md "Appendix A. PostgreSQL Error Codes")) e o nome do arquivo de código-fonte, o nome da função e o número da linha que gerou o erro. Apenas usuários superusuários e usuários com o privilégio apropriado de `SET` podem alterar esta configuração.

`log_hostname` (`boolean`) [#](#GUC-LOG-HOSTNAME): Por padrão, as mensagens de registro de conexão mostram apenas o endereço IP do host que está se conectando. Ao ativar este parâmetro, o nome do host também é registrado. Observe que, dependendo da configuração de resolução do nome do host, isso pode impor uma penalidade de desempenho que não é desprezível. Este parâmetro só pode ser definido no arquivo `postgresql.conf` ou na linha de comando do servidor.

`log_line_prefix` (`string`) [#](#GUC-LOG-LINE-PREFIX): Esta é uma cadeia de caracteres do estilo `printf` que é emitida no início de cada linha de registro. Os caracteres `%` começam com "sequências de escape" que são substituídas com informações de status conforme descrito abaixo. Escapes não reconhecidos são ignorados. Outros caracteres são copiados diretamente para a linha de registro. Alguns escapes são reconhecidos apenas por processos de sessão, e serão tratados como vazios por processos de fundo, como o processo do servidor principal. As informações de status podem ser alinhadas à esquerda ou à direita, especificando um literal numérico após o % e antes da opção. Um valor negativo fará com que as informações de status sejam preenchidas à direita com espaços para dar a ela uma largura mínima, enquanto um valor positivo preencherá à esquerda. O preenchimento pode ser útil para auxiliar a legibilidade humana em arquivos de registro.

Este parâmetro só pode ser definido no arquivo `postgresql.conf` ou na linha de comando do servidor. O padrão é `'%m [%p] '`, que registra um rótulo de tempo e o ID do processo.



<table>
 <colgroup>
  <col/>
  <col/>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th>
    Escape
   </th>
   <th>
    Efeito
   </th>
   <th>
    Session only
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <code>
     %a
    </code>
   </td>
   <td>
    Nome do aplicativo
   </td>
   <td>
    yes
   </td>
  </tr>
  <tr>
   <td>
    <code>
     %u
    </code>
   </td>
   <td>
    Nome do usuário
   </td>
   <td>
    yes
   </td>
  </tr>
  <tr>
   <td>
    <code>
     %d
    </code>
   </td>
   <td>
    Nome do banco de dados
   </td>
   <td>
    yes
   </td>
  </tr>
  <tr>
   <td>
    <code>
     %r
    </code>
   </td>
   <td>
    Nome de host remoto ou endereço IP, e porta remota
   </td>
   <td>
    yes
   </td>
  </tr>
  <tr>
   <td>
    <code>
     %h
    </code>
   </td>
   <td>
    Nome de host remoto ou endereço IP
   </td>
   <td>
    yes
   </td>
  </tr>
  <tr>
   <td>
    <code>
     %L
    </code>
   </td>
   <td>
    Endereço local (o endereço IP no servidor ao qual o cliente se conectou)
   </td>
   <td>
    yes
   </td>
  </tr>
  <tr>
   <td>
    <code>
     %b
    </code>
   </td>
   <td>
    Tipo de backend
   </td>
   <td>
    no
   </td>
  </tr>
  <tr>
   <td>
    <code>
     %p
    </code>
   </td>
   <td>
    ID do processo
   </td>
   <td>
    no
   </td>
  </tr>
  <tr>
   <td>
    <code>
     %P
    </code>
   </td>
   <td>
    ID do processo do líder do grupo paralelo, se este processo for um trabalhador de consulta paralela
   </td>
   <td>
    no
   </td>
  </tr>
  <tr>
   <td>
    <code>
     %t
    </code>
   </td>
   <td>
    Carimbo de tempo sem milissegundos
   </td>
   <td>
    no
   </td>
  </tr>
  <tr>
   <td>
    <code>
     %m
    </code>
   </td>
   <td>
    Marcador de tempo com milissegundos
   </td>
   <td>
    no
   </td>
  </tr>
  <tr>
   <td>
    <code>
     %n
    </code>
   </td>
   <td>
    Marca-data com milissegundos (como uma época Unix)
   </td>
   <td>
    no
   </td>
  </tr>
  <tr>
   <td>
    <code>
     %i
    </code>
   </td>
   <td>
    Tag de comando: tipo de comando atual da sessão
   </td>
   <td>
    yes
   </td>
  </tr>
  <tr>
   <td>
    <code>
     %e
    </code>
   </td>
   <td>
    Código de erro SQLSTATE
   </td>
   <td>
    no
   </td>
  </tr>
  <tr>
   <td>
    <code>
     %c
    </code>
   </td>
   <td>
    ID de sessão: veja abaixo
   </td>
   <td>
    no
   </td>
  </tr>
  <tr>
   <td>
    <code>
     %l
    </code>
   </td>
   <td>
    Número da linha de registro para cada sessão ou processo, começando em 1
   </td>
   <td>
    no
   </td>
  </tr>
  <tr>
   <td>
    <code>
     %s
    </code>
   </td>
   <td>
    Marcadores de hora de início do processo
   </td>
   <td>
    no
   </td>
  </tr>
  <tr>
   <td>
    <code>
     %v
    </code>
   </td>
   <td>
    ID de transação virtual (procNumber/localXID); veja
    <a class="xref" href="transaction-id.md" title="67.1. Transactions and Identifiers">
     Seção 67.1
    </a>
   </td>
   <td>
    no
   </td>
  </tr>
  <tr>
   <td>
    <code>
     %x
    </code>
   </td>
   <td>
    ID da transação (0 se nenhum for atribuído); veja
    <a class="xref" href="transaction-id.md" title="67.1. Transactions and Identifiers">
     Seção 67.1
    </a>
   </td>
   <td>
    no
   </td>
  </tr>
  <tr>
   <td>
    <code>
     %q
    </code>
   </td>
   <td>
    Não produz saída, mas informa aos processos não de sessão que devem parar neste ponto da cadeia; ignorado pelos processos de sessão
   </td>
   <td>
    no
   </td>
  </tr>
  <tr>
   <td>
    <code>
     %Q
    </code>
   </td>
   <td>
    Identificador da consulta atual. Os identificadores de consulta não são calculados por padrão, portanto, este campo será zero a menos que
    <a class="xref" href="runtime-config-statistics.md#GUC-COMPUTE-QUERY-ID">
     compute_query_id
    </a>
    O parâmetro está habilitado ou um módulo de terceiros que calcula identificadores de consulta está configurado.
   </td>
   <td>
    yes
   </td>
  </tr>
  <tr>
   <td>
    <code>
     %%
    </code>
   </td>
   <td>
    Literal
    <code>
     %
    </code>
   </td>
   <td>
    no
   </td>
  </tr>
 </tbody>
</table>







O tipo de backend corresponde à coluna `backend_type` na visualização `pg_stat_activity`(monitoring-stats.md#MONITORING-PG-STAT-ACTIVITY-VIEW "27.2.3. pg_stat_activity"), mas tipos adicionais podem aparecer no log que não aparecem nessa visualização.

O `%c` escape imprime um identificador de sessão quase único, composto por dois números hexadecimais de 4 bytes (sem zeros no início) separados por um ponto. Os números são o horário de início do processo e o ID do processo, então o `%c` também pode ser usado como uma maneira de economizar espaço ao imprimir esses itens. Por exemplo, para gerar o identificador de sessão a partir do `pg_stat_activity`, use esta consulta:

```
SELECT to_hex(trunc(EXTRACT(EPOCH FROM backend_start))::integer) || '.' || to_hex(pid) FROM pg_stat_activity;
```

DICA

Se você definir um valor não vazio para `log_line_prefix`, geralmente deve deixar seu último caractere como um espaço, para fornecer uma separação visual do resto da linha de registro. Um caractere de pontuação também pode ser usado.

DICA

O Syslog produz seu próprio rótulo de tempo e informações de ID de processo, então você provavelmente não quer incluir essas escapadas se estiver registrando no syslog.

DICA

O escape `%q` é útil ao incluir informações que estão disponíveis apenas no contexto da sessão (backend), como o nome do usuário ou do banco de dados. Por exemplo:

```
log_line_prefix = '%m [%p] %q%u@%d/%a '
```

Nota

O escape `%Q` sempre reporta um identificador zero para as linhas geradas por [log_statement](runtime-config-logging.md#GUC-LOG-STATEMENT) porque `log_statement` gera a saída antes que um identificador possa ser calculado, incluindo declarações inválidas para as quais não pode ser calculado um identificador.

`log_lock_waits` (`boolean`) [#](#GUC-LOG-LOCK-WAITS): Controla se uma mensagem de log é produzida quando uma sessão espera mais tempo do que [deadlock_timeout](runtime-config-locks.md#GUC-DEADLOCK-TIMEOUT) para adquirir um bloqueio. Isso é útil para determinar se as esperas de bloqueio estão causando um desempenho ruim. O padrão é `off`. Somente usuários super e usuários com o privilégio apropriado `SET` podem alterar essa configuração.

`log_lock_failures` (`boolean`) [#](#GUC-LOG-LOCK-FAILURES): Controla se uma mensagem de log detalhada é produzida quando uma aquisição de bloqueio falha. Isso é útil para analisar as causas das falhas de bloqueio. Atualmente, apenas as falhas de bloqueio devido a `SELECT NOWAIT` são suportadas. O padrão é `off`. Somente superusuários e usuários com o privilégio apropriado `SET` podem alterar essa configuração.

`log_recovery_conflict_waits` (`boolean`) [#](#GUC-LOG-RECOVERY-CONFLICT-WAITS): Controla se uma mensagem de log é produzida quando o processo de inicialização espera mais tempo do que `deadlock_timeout` para resolver conflitos de recuperação. Isso é útil para determinar se os conflitos de recuperação impedem que a recuperação aplique o WAL.

O padrão é `off`. Este parâmetro só pode ser definido no arquivo `postgresql.conf` ou na linha de comando do servidor.

`log_parameter_max_length` (`integer`) [#](#GUC-LOG-PARAMETER-MAX-LENGTH): Se maior que zero, cada valor do parâmetro de vinculação registrado com uma mensagem de registro de log sem erro é limitado a este número de bytes. Zero desativa o registro de parâmetros de vinculação para logs de declarações sem erro. `-1` (o padrão) permite que os parâmetros de vinculação sejam registrados na íntegra. Se este valor for especificado sem unidades, ele é considerado em bytes. Somente superusuários e usuários com o privilégio apropriado `SET` podem alterar esta configuração.

Essa configuração afeta apenas as mensagens de log impressas como resultado de [log_statement](runtime-config-logging.md#GUC-LOG-STATEMENT), [log_duration](runtime-config-logging.md#GUC-LOG-DURATION) e configurações relacionadas. Valores não nulos dessa configuração adicionam algum overhead, especialmente se os parâmetros forem enviados em formato binário, pois, nesse caso, é necessária a conversão para texto.

`log_parameter_max_length_on_error` (`integer`) [#](#GUC-LOG-PARAMETER-MAX-LENGTH-ON-ERROR): Se maior que zero, cada valor do parâmetro de vinculação relatado em mensagens de erro é limitado a quantos bytes. Zero (o padrão) desativa a inclusão de parâmetros de vinculação em mensagens de erro. `-1` permite que os parâmetros de vinculação sejam impressos na íntegra. Se este valor for especificado sem unidades, ele é considerado em bytes.

Valores não nulos deste ajuste adicionam sobrecarga, pois o PostgreSQL precisará armazenar representações textuais dos valores dos parâmetros na memória no início de cada declaração, independentemente de ocorrer ou não um erro eventualmente. A sobrecarga é maior quando os parâmetros de vinculação são enviados em forma binária do que quando são enviados como texto, pois o primeiro caso requer conversão de dados, enquanto o último apenas requer a cópia da string.

`log_statement` (`enum`) [#](#GUC-LOG-STATEMENT): Controla quais declarações SQL são registradas. Os valores válidos são `none` (desativado), `ddl`, `mod` e `all` (todas as declarações). `ddl` registra todas as declarações de definição de dados, como as declarações de `CREATE`, `ALTER` e `DROP`. `mod` registra todas as declarações de `ddl`, além de declarações que modificam dados, como `INSERT`, `UPDATE`, `DELETE`, `TRUNCATE` e `COPY FROM`. As declarações de `PREPARE`, `EXECUTE` e `EXPLAIN ANALYZE` também são registradas se o comando contido tiver um tipo apropriado. Para clientes que usam o protocolo de consulta estendida, o registro ocorre quando uma mensagem de Execute é recebida e os valores dos parâmetros Bind são incluídos (com quaisquer aspas embutidas duplicadas).

O padrão é `none`. Somente usuários superusuários e usuários com o privilégio apropriado `SET` podem alterar essa configuração.

Nota

As declarações que contêm erros de sintaxe simples não são registradas, mesmo com a configuração `log_statement` = `all`, porque a mensagem de log é emitida apenas após a análise básica ter sido realizada para determinar o tipo de declaração. No caso do protocolo de consulta estendida, essa configuração também não registra declarações que falham antes da fase Execute (ou seja, durante a análise ou planejamento de análise). Defina `log_min_error_statement` para `ERROR` (ou menor) para registrar tais declarações.

As declarações registradas podem revelar dados sensíveis e até conter senhas em texto plano.

`log_replication_commands` (`boolean`) [#](#GUC-LOG-REPLICATION-COMMANDS): Cada comando de replicação e a aquisição/liberação do slot de replicação do processo `walsender` são registrados no log do servidor. Consulte [Seção 54.4](protocol-replication.md "54.4. Streaming Replication Protocol") para obter mais informações sobre o comando de replicação. O valor padrão é `off`. Somente usuários superusuários e usuários com o privilégio apropriado `SET` podem alterar essa configuração.

`log_temp_files` (`integer`) [#](#GUC-LOG-TEMP-FILES): Controla o registro de nomes e tamanhos de arquivos temporários. Arquivos temporários podem ser criados para ordenamentos, hashes e resultados temporários de consultas. Se habilitado por esta configuração, uma entrada de registro é emitida para cada arquivo temporário, com o tamanho do arquivo especificado em bytes, quando é excluído. Um valor de zero registra todas as informações dos arquivos temporários, enquanto valores positivos registram apenas arquivos cujos tamanhos são maiores ou iguais ao valor especificado de dados. Se este valor for especificado sem unidades, ele é considerado em kilobytes. A configuração padrão é -1, que desativa tal registro. Somente superusuários e usuários com o privilégio apropriado `SET` podem alterar esta configuração.

`log_timezone` (`string`) [#](#GUC-LOG-TIMEZONE): Define o fuso horário usado para marcações de tempo escritas no log do servidor. Ao contrário de [TimeZone](runtime-config-client.md#GUC-TIMEZONE), este valor é válido para todo o clúster, de modo que todas as sessões irão relatar marcações de tempo de forma consistente. O valor padrão embutido é `GMT`, mas isso é tipicamente substituído em `postgresql.conf`; o initdb instalará um ajuste correspondente ao seu ambiente de sistema. Consulte [Seção 8.5.3](datatype-datetime.md#DATATYPE-TIMEZONES "8.5.3. Time Zones") para obter mais informações. Este parâmetro só pode ser definido no arquivo `postgresql.conf` ou na linha de comando do servidor.

### 19.8.4. Saída de registro no formato CSV [#](#RUNTIME-CONFIG-LOGGING-CSVLOG)

Incluir `csvlog` na lista `log_destination` fornece uma maneira conveniente de importar arquivos de registro em uma tabela de banco de dados. Esta opção emite linhas de registro no formato de valores separados por vírgula (CSV), com essas colunas: marca-horário com milissegundos, nome do usuário, nome do banco de dados, ID do processo, número do host:porta do cliente, ID de sessão, número de linha de sessão, tag de comando, hora de início da sessão, ID de transação virtual, ID de transação regular, gravidade do erro, código SQLSTATE, mensagem de erro, detalhe da mensagem de erro, dica, consulta interna que levou ao erro (se houver), contagem de caracteres da posição do erro, contexto do erro, consulta do usuário que levou ao erro (se houver e habilitada por `log_min_error_statement`), contagem de caracteres da posição do erro, localização do erro no código-fonte do PostgreSQL (se `log_error_verbosity` estiver definido como `verbose`), nome do aplicativo, tipo de backend, ID de processo do líder do grupo paralelo e ID da consulta. Aqui está uma definição de tabela de amostra para armazenar a saída de registro no formato CSV:

```
CREATE TABLE postgres_log ( log_time timestamp(3) with time zone, user_name text, database_name text, process_id integer, connection_from text, session_id text, session_line_num bigint, command_tag text, session_start_time timestamp with time zone, virtual_transaction_id text, transaction_id bigint, error_severity text, sql_state_code text, message text, detail text, hint text, internal_query text, internal_query_pos integer, context text, query text, query_pos integer, location text, application_name text, backend_type text, leader_pid integer, query_id bigint, PRIMARY KEY (session_id, session_line_num) );
```

Para importar um arquivo de registro nesta tabela, use o comando `COPY FROM`:

```
COPY postgres_log FROM '/full/path/to/logfile.csv' WITH csv;
```

É também possível acessar o arquivo como uma tabela estrangeira, usando o módulo fornecido [file_fdw](file-fdw.md).

Há algumas coisas que você precisa fazer para simplificar a importação de arquivos de registro CSV:

1. Defina `log_filename` e `log_rotation_age` para fornecer um esquema de nomeação consistente e previsível para seus arquivos de registro. Isso permite que você preveja qual será o nome do arquivo e saiba quando um arquivo de registro individual está completo e, portanto, pronto para ser importado.
2. Defina `log_rotation_size` para 0 para desativar a rotação de log baseada no tamanho, pois isso dificulta a previsão do nome do arquivo de registro.
3. Defina `log_truncate_on_rotation` para `on` para que os dados de log antigos não sejam misturados com os novos no mesmo arquivo.
4. A definição da tabela acima inclui uma especificação de chave primária. Isso é útil para proteger contra a importação acidental da mesma informação duas vezes. O comando `COPY` compromete todos os dados que importa de uma só vez, então qualquer erro causará o fracasso de toda a importação. Se você importar um arquivo de log parcial e depois importar o arquivo novamente quando ele estiver completo, a violação da chave primária causará o fracasso da importação. Aguarde até que o log esteja completo e fechado antes de importar. Esse procedimento também protegerá contra a importação acidental de uma linha parcial que não foi completamente escrita, o que também causaria o fracasso do `COPY`.

### 19.8.5. Uso de saída de registro em formato JSON [#](#RUNTIME-CONFIG-LOGGING-JSONLOG)

Incluir `jsonlog` na lista `log_destination` fornece uma maneira conveniente de importar arquivos de registro em muitos programas diferentes. Esta opção emite linhas de registro no formato JSON.

Campos de texto com valores nulos são excluídos da saída. Campos adicionais podem ser adicionados no futuro. Aplicações de usuário que processam a saída `jsonlog` devem ignorar campos desconhecidos.

Cada linha de registro é serializada como um objeto JSON com o conjunto de chaves e seus valores associados mostrados em [Tabela 19.4](runtime-config-logging.md#RUNTIME-CONFIG-LOGGING-JSONLOG-KEYS-VALUES).

**Tabela 19.4. Chaves e valores das entradas de registro JSON**



<table>
 <colgroup>
  <col/>
  <col/>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th>
    Key name
   </th>
   <th>
    Type
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
     timestamp
    </code>
   </td>
   <td>
    string
   </td>
   <td>
    Marcador de tempo com milissegundos
   </td>
  </tr>
  <tr>
   <td>
    <code>
     user
    </code>
   </td>
   <td>
    string
   </td>
   <td>
    Nome do usuário
   </td>
  </tr>
  <tr>
   <td>
    <code>
     dbname
    </code>
   </td>
   <td>
    string
   </td>
   <td>
    Nome do banco de dados
   </td>
  </tr>
  <tr>
   <td>
    <code>
     pid
    </code>
   </td>
   <td>
    number
   </td>
   <td>
    ID do processo
   </td>
  </tr>
  <tr>
   <td>
    <code>
     remote_host
    </code>
   </td>
   <td>
    string
   </td>
   <td>
    anfitrião do cliente
   </td>
  </tr>
  <tr>
   <td>
    <code>
     remote_port
    </code>
   </td>
   <td>
    number
   </td>
   <td>
    Porto do cliente
   </td>
  </tr>
  <tr>
   <td>
    <code>
     session_id
    </code>
   </td>
   <td>
    string
   </td>
   <td>
    ID de sessão
   </td>
  </tr>
  <tr>
   <td>
    <code>
     line_num
    </code>
   </td>
   <td>
    number
   </td>
   <td>
    Número de linha por sessão
   </td>
  </tr>
  <tr>
   <td>
    <code>
     ps
    </code>
   </td>
   <td>
    string
   </td>
   <td>
    Atual ps display
   </td>
  </tr>
  <tr>
   <td>
    <code>
     session_start
    </code>
   </td>
   <td>
    string
   </td>
   <td>
    Horário de início da sessão
   </td>
  </tr>
  <tr>
   <td>
    <code>
     vxid
    </code>
   </td>
   <td>
    string
   </td>
   <td>
    ID de transação virtual
   </td>
  </tr>
  <tr>
   <td>
    <code>
     txid
    </code>
   </td>
   <td>
    string
   </td>
   <td>
    ID de transação regular
   </td>
  </tr>
  <tr>
   <td>
    <code>
     error_severity
    </code>
   </td>
   <td>
    string
   </td>
   <td>
    Gravidade do erro
   </td>
  </tr>
  <tr>
   <td>
    <code>
     state_code
    </code>
   </td>
   <td>
    string
   </td>
   <td>
    Código SQLSTATE
   </td>
  </tr>
  <tr>
   <td>
    <code>
     message
    </code>
   </td>
   <td>
    string
   </td>
   <td>
    Mensagem de erro
   </td>
  </tr>
  <tr>
   <td>
    <code>
     detail
    </code>
   </td>
   <td>
    string
   </td>
   <td>
    Detalhamento da mensagem de erro
   </td>
  </tr>
  <tr>
   <td>
    <code>
     hint
    </code>
   </td>
   <td>
    string
   </td>
   <td>
    Sugestão de mensagem de erro
   </td>
  </tr>
  <tr>
   <td>
    <code>
     internal_query
    </code>
   </td>
   <td>
    string
   </td>
   <td>
    Consulta interna que levou ao erro
   </td>
  </tr>
  <tr>
   <td>
    <code>
     internal_position
    </code>
   </td>
   <td>
    number
   </td>
   <td>
    Índice do cursor em consulta interna
   </td>
  </tr>
  <tr>
   <td>
    <code>
     context
    </code>
   </td>
   <td>
    string
   </td>
   <td>
    Contexto do erro
   </td>
  </tr>
  <tr>
   <td>
    <code>
     statement
    </code>
   </td>
   <td>
    string
   </td>
   <td>
    string de consulta fornecida pelo cliente
   </td>
  </tr>
  <tr>
   <td>
    <code>
     cursor_position
    </code>
   </td>
   <td>
    number
   </td>
   <td>
    Índice do cursor na string de consulta
   </td>
  </tr>
  <tr>
   <td>
    <code>
     func_name
    </code>
   </td>
   <td>
    string
   </td>
   <td>
    Nome da função de localização de erro
   </td>
  </tr>
  <tr>
   <td>
    <code>
     file_name
    </code>
   </td>
   <td>
    string
   </td>
   <td>
    Nome do arquivo da localização do erro
   </td>
  </tr>
  <tr>
   <td>
    <code>
     file_line_num
    </code>
   </td>
   <td>
    number
   </td>
   <td>
    Número de linha do arquivo do local da localização do erro
   </td>
  </tr>
  <tr>
   <td>
    <code>
     application_name
    </code>
   </td>
   <td>
    string
   </td>
   <td>
    Nome do aplicativo do cliente
   </td>
  </tr>
  <tr>
   <td>
    <code>
     backend_type
    </code>
   </td>
   <td>
    string
   </td>
   <td>
    Tipo de backend
   </td>
  </tr>
  <tr>
   <td>
    <code>
     leader_pid
    </code>
   </td>
   <td>
    number
   </td>
   <td>
    ID de processo do líder para trabalhadores paralelos ativos
   </td>
  </tr>
  <tr>
   <td>
    <code>
     query_id
    </code>
   </td>
   <td>
    number
   </td>
   <td>
    ID da consulta
   </td>
  </tr>
 </tbody>
</table>







### 19.8.6. Título do processo [#](#RUNTIME-CONFIG-LOGGING-PROC-TITLE)

Estes ajustes controlam como os títulos dos processos do servidor são modificados. Os títulos dos processos são normalmente visualizados usando programas como o ps ou, no Windows, o Process Explorer. Consulte [Seção 27.1] para obter detalhes.

`cluster_name` (`string`) [#](#GUC-CLUSTER-NAME): Define um nome que identifica este grupo de bancos de dados (instância) para vários propósitos. O nome do grupo aparece no título do processo para todos os processos do servidor neste grupo. Além disso, é o nome de aplicativo padrão para uma conexão de espera (consulte [synchronous_standby_names](runtime-config-replication.md#GUC-SYNCHRONOUS-STANDBY-NAMES)).

O nome pode ser qualquer cadeia de menos de `NAMEDATALEN` caracteres (64 caracteres em uma versão padrão). Apenas caracteres ASCII imprimíveis podem ser usados no valor `cluster_name`. Outros caracteres são substituídos por escapes hexadecimais em estilo C (sql-syntax-lexical.md#SQL-SYNTAX-STRINGS-ESCAPE "4.1.2.2. String Constants with C-Style Escapes"). Não é exibido nenhum nome se este parâmetro for definido como a cadeia vazia `''` (que é a opção padrão). Este parâmetro só pode ser definido na inicialização do servidor.

`update_process_title` (`boolean`) [#](#GUC-UPDATE-PROCESS-TITLE): Habilita a atualização do título do processo toda vez que um novo comando SQL é recebido pelo servidor. Esta configuração tem como padrão `on` na maioria das plataformas, mas tem como padrão `off` no Windows devido ao maior overhead dessa plataforma para a atualização do título do processo. Somente usuários superusuários e usuários com o privilégio apropriado `SET` podem alterar esta configuração.