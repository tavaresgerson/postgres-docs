## 24.3. Manutenção de arquivos de registro [#](#LOGFILE-MAINTENANCE)

É uma boa ideia salvar a saída do log do servidor de banco de dados em algum lugar, em vez de simplesmente descartá-la via `/dev/null`. A saída do log é inestimável ao diagnosticar problemas.

Nota

O log do servidor pode conter informações sensíveis e precisa ser protegido, independentemente de como ou onde ele é armazenado, ou do destino para o qual ele é encaminhado. Por exemplo, algumas declarações DDL podem conter senhas em texto plano ou outros detalhes de autenticação. Declarações registradas no nível `ERROR` podem mostrar o código-fonte do SQL para aplicativos e também podem conter algumas partes das linhas de dados. O registro de dados, eventos e informações relacionadas é a função pretendida desta facilidade, então isso não é uma vazamento ou um bug. Por favor, garanta que os logs do servidor sejam visíveis apenas para pessoas apropriadamente autorizadas.

A saída do log tende a ser volumosa (especialmente em níveis mais altos de depuração), então você não vai querer salvá-la indefinidamente. Você precisa *rotular* os arquivos de log para que novos arquivos de log sejam iniciados e os antigos sejam removidos após um período razoável de tempo.

Se você simplesmente redirecionar o stderr do `postgres` para um arquivo, você terá saída de log, mas a única maneira de truncar o arquivo de log é parar e reiniciar o servidor. Isso pode ser aceitável se você estiver usando o PostgreSQL em um ambiente de desenvolvimento, mas poucos servidores de produção acharão esse comportamento aceitável.

Uma abordagem melhor é enviar a saída do stderr do servidor para algum tipo de programa de rotação de log. Há uma facilidade de rotação de log embutida, que você pode usar definindo o parâmetro de configuração `logging_collector` para `true` em `postgresql.conf`. Os parâmetros de controle para este programa são descritos em [Seção 19.8.1](runtime-config-logging.md#RUNTIME-CONFIG-LOGGING-WHERE "19.8.1. Where to Log"). Você também pode usar essa abordagem para capturar os dados do log no formato CSV (valores separados por vírgula) legível por máquina.

Como alternativa, você pode preferir usar um programa de rotação de registro externo, se você tiver um que já está usando com outro software do servidor. Por exemplo, a ferramenta rotatelogs incluída na distribuição do Apache pode ser usada com o PostgreSQL. Uma maneira de fazer isso é canalizar a saída stderr do servidor para o programa desejado. Se você iniciar o servidor com `pg_ctl`, então o stderr já está redirecionado para stdout, então você só precisa de um comando de canal, por exemplo:

```
pg_ctl start | rotatelogs /var/log/pgsql_log 86400
```

Você pode combinar essas abordagens configurando o logrotate para coletar os arquivos de registro produzidos pelo coletor de registro integrado do PostgreSQL. Neste caso, o coletor de registro define os nomes e a localização dos arquivos de registro, enquanto o logrotate arquivia periodicamente esses arquivos. Ao iniciar a rotação de log, o logrotate deve garantir que o aplicativo envie mais saída para o novo arquivo. Isso é comumente feito com um script `postrotate` que envia um sinal `SIGHUP` ao aplicativo, que então reabre o arquivo de log. No PostgreSQL, você pode executar `pg_ctl` com a opção `logrotate`. Quando o servidor recebe esse comando, o servidor ou troca para um novo arquivo de log ou reabre o arquivo existente, dependendo da configuração de registro (veja [Seção 19.8.1] (runtime-config-logging.md#RUNTIME-CONFIG-LOGGING-WHERE "19.8.1. Where to Log")).

Nota

Ao usar nomes estáticos de arquivos de registro, o servidor pode falhar ao reabrir o arquivo de registro se o limite máximo de arquivos abertos for atingido ou ocorrer um overflow na tabela de arquivos. Neste caso, as mensagens de log são enviadas para o arquivo de log antigo até que ocorra uma rotação de log bem-sucedida. Se o logrotate for configurado para comprimir o arquivo de log e excluí-lo, o servidor pode perder as mensagens registradas nesse período. Para evitar esse problema, você pode configurar o coletor de registro para atribuir dinamicamente nomes de arquivos de registro e usar um script `prerotate` para ignorar arquivos de log abertos.

Outra abordagem de nível de produção para gerenciar a saída de registro é enviá-la para o syslog e deixar o syslog lidar com a rotação de arquivos. Para fazer isso, defina o parâmetro de configuração `log_destination` para `syslog` (para registrar no syslog apenas) em `postgresql.conf`. Em seguida, você pode enviar um sinal `SIGHUP` ao daemon syslog sempre que quiser forçar-o a começar a escrever um novo arquivo de registro. Se você deseja automatizar a rotação de registro, o programa logrotate pode ser configurado para trabalhar com arquivos de registro do syslog.

Em muitos sistemas, no entanto, o syslog não é muito confiável, especialmente com mensagens de log grandes; ele pode truncar ou descartar mensagens justamente quando você mais precisa delas. Além disso, no Linux, o syslog esvazia cada mensagem no disco, resultando em um desempenho ruim. (Você pode usar um “`-`” no início do nome do arquivo no arquivo de configuração do syslog para desabilitar a sincronização.)

Observe que todas as soluções descritas acima cuidam de iniciar novos arquivos de registro em intervalos configuráveis, mas elas não lidam com a exclusão de arquivos de registro antigos que não são mais úteis. Provavelmente, você vai querer configurar um trabalho em lote para excluir periodicamente os arquivos de registro antigos. Outra possibilidade é configurar o programa de rotação para que os arquivos de registro antigos sejam sobrescritos cíclicamente.

[pgBadger](https://pgbadger.darold.net/) é um projeto externo que realiza uma análise sofisticada de arquivos de registro. [check_postgres](https://bucardo.org/check_postgres/) fornece alertas do Nagios quando mensagens importantes aparecem nos arquivos de registro, além da detecção de muitas outras condições extraordinárias.