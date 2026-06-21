## postgres

postgres — servidor de banco de dados PostgreSQL

## Sinopse

`postgres` [*`option`*...]

## Descrição

`postgres` é o servidor de banco de dados PostgreSQL. Para que um aplicativo de cliente acesse um banco de dados, ele se conecta (via rede ou localmente) a uma instância em execução de `postgres`. A instância `postgres` então inicia um processo de servidor separado para lidar com a conexão.

Uma instância `postgres` sempre gerencia os dados de exatamente um conjunto de bancos de dados. Um conjunto de bancos de dados é uma coleção de bancos de dados que é armazenada em um local de sistema de arquivos comum (a “área de dados”). Mais de uma instância `postgres` pode rodar em um sistema ao mesmo tempo, desde que usem diferentes áreas de dados e diferentes portas de comunicação (veja abaixo). Quando o `postgres` começa, ele precisa saber a localização da área de dados. A localização deve ser especificada pela opção `-D` ou pela variável de ambiente `PGDATA`; não há um padrão. Tipicamente, `-D` ou `PGDATA` aponta diretamente para o diretório da área de dados criado por [initdb](app-initdb.md "initdb"). Outros possíveis layouts de arquivo são discutidos em [Seção 19.2](runtime-config-file-locations.md "19.2. File Locations").

Por padrão, `postgres` começa em primeiro plano e imprime mensagens de log no fluxo de erro padrão. Em aplicações práticas, `postgres` deve ser iniciado como um processo em segundo plano, talvez no momento do boot.

O comando `postgres` também pode ser chamado no modo de usuário único. O uso principal para este modo é durante o arranque pelo [initdb][(app-initdb.md "initdb")]. Às vezes, é usado para depuração ou recuperação em caso de desastre; observe que executar um servidor de usuário único não é realmente adequado para depuração do servidor, uma vez que não ocorrerá comunicação e bloqueio de processos realistas. Quando invocado no modo de usuário único a partir da linha de comando, o usuário pode inserir consultas e os resultados serão impressos na tela, mas de uma forma que é mais útil para desenvolvedores do que para usuários finais. No modo de usuário único, o usuário da sessão será definido para o usuário com ID 1, e poderes de superusuário implícitos serão concedidos a este usuário. Este usuário não precisa realmente existir, portanto, o modo de usuário único pode ser usado para recuperar manualmente certos tipos de danos acidentais aos catálogos do sistema.

## Opções

`postgres` aceita os seguintes argumentos de linha de comando. Para uma discussão detalhada das opções, consulte o [Capítulo 19][(runtime-config.md "Chapter 19. Server Configuration")]. Você pode economizar a digitação da maioria dessas opções configurando um arquivo de configuração. Algumas (seguras) opções também podem ser definidas a partir do cliente de conexão de uma maneira dependente da aplicação para aplicar apenas para essa sessão. Por exemplo, se a variável de ambiente `PGOPTIONS` estiver definida, os clientes baseados em libpq passarão essa string para o servidor, que a interpretará como opções de linha de comando `postgres`.

### Propósito Geral

`-B nbuffers`: Define o número de buffers compartilhados para uso pelos processos do servidor. O valor padrão deste parâmetro é escolhido automaticamente pelo initdb. Especificar esta opção é equivalente a definir o parâmetro de configuração [shared_buffers][(runtime-config-resource.md#GUC-SHARED-BUFFERS)].

`-c name=value`: Define um parâmetro de execução com nome. Os parâmetros de configuração suportados pelo PostgreSQL são descritos em [Capítulo 19][(runtime-config.md "Chapter 19. Server Configuration")]. A maioria das outras opções de linha de comando são, na verdade, formas abreviadas de uma atribuição de parâmetros. `-c` pode aparecer várias vezes para definir vários parâmetros.

`-C name`: Imprime o valor do parâmetro de execução nomeado e sai. (Consulte a opção `-c` acima para obter detalhes.) Isso retorna valores de `postgresql.conf`, modificados por quaisquer parâmetros fornecidos nesta invocação. Não reflete os parâmetros fornecidos quando o clúster foi iniciado.

Isso pode ser usado em um servidor em execução para a maioria dos parâmetros. No entanto, o servidor deve ser desligado para alguns parâmetros calculados durante a execução (por exemplo, [shared_memory_size](runtime-config-preset.md#GUC-SHARED-MEMORY-SIZE), [shared_memory_size_in_huge_pages](runtime-config-preset.md#GUC-SHARED-MEMORY-SIZE-IN-HUGE-PAGES) e [wal_segment_size](runtime-config-preset.md#GUC-WAL-SEGMENT-SIZE)).

Esta opção é destinada a outros programas que interagem com uma instância do servidor, como [pg_ctl][(app-pg-ctl.md "pg_ctl")], para consultar os valores dos parâmetros de configuração. As aplicações voltadas para o usuário devem, em vez disso, usar [`SHOW`][(sql-show.md "SHOW")] ou a visualização `pg_settings`.

`-d debug-level`: Define o nível de depuração. Quanto maior o valor definido, mais saída de depuração é escrita no log do servidor. Os valores variam de 1 a 5. É também possível passar `-d 0` para uma sessão específica, o que impedirá que o nível de log do servidor do processo pai `postgres` seja propagado para esta sessão.

`-D datadir`: Especifica a localização do sistema de arquivos dos arquivos de configuração do banco de dados. Consulte [Seção 19.2][(runtime-config-file-locations.md "19.2. File Locations")] para obter detalhes.

`-e`: Define o estilo de data padrão como “Europeu”, ou seja, a `DMY` ordenação dos campos de data de entrada. Isso também faz com que o dia seja impresso antes do mês em certos formatos de saída de data. Consulte [Seção 8.5][(datatype-datetime.md "8.5. Date/Time Types")] para obter mais informações.

`-F`: Desabilita as chamadas para melhoria do desempenho, arriscando a corrupção dos dados no caso de um travamento do sistema. Especificar esta opção é equivalente a desabilitar o parâmetro de configuração [fsync](runtime-config-wal.md#GUC-FSYNC). Leia a documentação detalhada antes de usar isso!

`-h hostname`: Especifica o nome de host IP ou endereço IP no qual o `postgres` deve ouvir conexões TCP/IP de aplicações de cliente. O valor também pode ser uma lista de endereços separados por vírgula, ou `*` para especificar a escuta em todas as interfaces disponíveis. Um valor vazio especifica não ouvir em nenhum endereço IP, no caso em que apenas soquetes de domínio Unix podem ser usados para se conectar ao servidor. O padrão é ouvir apenas em localhost. Especificar esta opção é equivalente a definir o parâmetro de configuração [listen_addresses](runtime-config-connection.md#GUC-LISTEN-ADDRESSES).

`-i`: Permite que clientes remotos se conectem por meio de conexões TCP/IP (domínio de Internet). Sem essa opção, apenas conexões locais são aceitas. Essa opção é equivalente a definir `listen_addresses` como `*` em `postgresql.conf` ou por meio de `-h`.

Essa opção é desaconselhada, pois não permite o acesso à funcionalidade completa de [listen_addresses][(runtime-config-connection.md#GUC-LISTEN-ADDRESSES)]. Geralmente é melhor definir diretamente `listen_addresses`.

`-k directory`: Especifica o diretório do socket de domínio Unix no qual `postgres` deve ouvir conexões de aplicativos cliente. O valor também pode ser uma lista de diretórios separados por vírgula. Um valor vazio especifica não ouvir em nenhum socket de domínio Unix, nesse caso, apenas soquetes TCP/IP podem ser usados para se conectar ao servidor. O valor padrão é normalmente `/tmp`, mas isso pode ser alterado na hora da construção. Especificar esta opção é equivalente a definir o parâmetro de configuração [unix_socket_directories](runtime-config-connection.md#GUC-UNIX-SOCKET-DIRECTORIES).

`-l`: Habilita conexões seguras usando SSL. O PostgreSQL deve ter sido compilado com suporte para SSL para que essa opção esteja disponível. Para mais informações sobre o uso do SSL, consulte [Seção 18.9][(ssl-tcp.md "18.9. Secure TCP/IP Connections with SSL")].

`-N max-connections`: Define o número máximo de conexões de cliente que este servidor aceitará. O valor padrão deste parâmetro é escolhido automaticamente pelo initdb. Especificar esta opção é equivalente a definir o parâmetro de configuração [max_connections][(runtime-config-connection.md#GUC-MAX-CONNECTIONS)].

`-p port`: Especifica a porta TCP/IP ou a extensão de arquivo de soquete de domínio Unix local na qual o `postgres` deve ouvir conexões de aplicações cliente. O padrão é o valor da variável de ambiente `PGPORT`, ou, se `PGPORT` não for definido, o padrão é o valor estabelecido durante a compilação (normalmente 5432). Se você especificar uma porta diferente da porta padrão, todas as aplicações cliente devem especificar a mesma porta usando opções de linha de comando ou `PGPORT`.

`-s`: Imprima informações de tempo e outras estatísticas no final de cada comando. Isso é útil para fazer comparações ou para uso na regulagem do número de buffers.

`-S` *`work-mem`*: Especifica o valor base de memória a ser utilizado por ordenamentos e tabelas de hash antes de recorrer a arquivos temporários em disco. Consulte a descrição do parâmetro de configuração `work_mem` na [Seção 19.4.1](runtime-config-resource.md#RUNTIME-CONFIG-RESOURCE-MEMORY "19.4.1. Memory").

`-V` `--version`: Imprimir a versão do postgres e sair.

`--name=value`: Define um parâmetro de execução com nome; uma forma mais curta de `-c`.

`--describe-config`: Esta opção descarrega as variáveis de configuração internas do servidor, descrições e configurações padrão no formato delimitado por tabulação `COPY`. É projetada principalmente para uso por ferramentas de administração.

`-?` `--help`: Mostrar ajuda sobre os argumentos da linha de comando do postgres e sair.

### Opções Semi-Internas

As opções descritas aqui são usadas principalmente para fins de depuração e, em alguns casos, para auxiliar na recuperação de bancos de dados gravemente danificados. Não deve haver motivo para usá-las em uma configuração de banco de dados de produção. Elas são listadas aqui apenas para uso por desenvolvedores do sistema PostgreSQL. Além disso, essas opções podem ser alteradas ou removidas em uma versão futura sem aviso prévio.

`-f` `{ s | i | o | b | t | n | m | h }`: Proíbe o uso de métodos de varredura e junção específicos: `s` e `i` desativam varreduras sequenciais e de índice, respectivamente, `o`, `b` e `t` desativam varreduras de índice, varreduras de índice em bitmap e varreduras TID, respectivamente, enquanto `n`, `m` e `h` desativam junções de laço aninhado, junção de fusão e junção de hash, respectivamente.

Nem as varreduras sequenciais nem as junções de laço aninhado podem ser desativadas completamente; as opções `-fs` e `-fn` simplesmente desencorajam o otimizador de usar esses tipos de plano se ele tiver alguma outra alternativa.

`-O`: Permite a modificação da estrutura das tabelas do sistema. Isso é utilizado por `initdb`.

`-P`: Ignorar índices do sistema ao ler tabelas do sistema, mas ainda atualizar os índices ao modificar as tabelas. Isso é útil ao recuperar de índices do sistema danificados.

`-t` `pa[rser] | pl[anner] | e[xecutor]`: Imprimir estatísticas de tempo de impressão para cada consulta relativa a cada um dos principais módulos do sistema. Esta opção não pode ser usada em conjunto com a opção `-s`.

`-T`: Esta opção é para depuração de problemas que fazem com que um processo do servidor morra de forma anormal. A estratégia comum nesta situação é notificar todos os outros processos do servidor que devem ser terminados, enviando-lhes sinais SIGQUIT. Com esta opção, SIGABRT será enviado em vez disso, resultando na produção de arquivos de depuração de núcleo.

`-v` *`protocol`*: Especifica o número de versão do protocolo de frontend/backend a ser utilizado para uma sessão específica. Esta opção é para uso interno apenas.

`-W` *`seconds`*: Um atraso de tantos segundos ocorre quando um novo processo do servidor é iniciado, após ele realizar o procedimento de autenticação. Isso visa dar uma oportunidade para se conectar ao processo do servidor com um depurador.

### Opções para Modo de Usuário Único

As opções a seguir só se aplicam ao modo de usuário único (consulte [Modo de usuário único][(app-postgres.md#APP-POSTGRES-SINGLE-USER "Single-User Mode")] abaixo).

`--single`: Seleciona o modo de usuário único. Este deve ser o primeiro argumento na linha de comando.

*`database`*: Especifica o nome do banco de dados a ser acessado. Isso deve ser o último argumento na linha de comando. Se omitido, ele é predefinido com o nome do usuário.

`-E`: Repita todos os comandos para a saída padrão antes de executá-los.

`-j`: Use ponto e vírgula seguido por duas novas linhas, em vez de apenas uma nova linha, como o terminador de entrada do comando.

`-r` *`filename`*: Envie todas as saídas do log do servidor para *`filename`*. Esta opção é respeitada apenas quando fornecida como uma opção de linha de comando.

## Meio Ambiente

`PGCLIENTENCODING`: Codificação de caracteres padrão usada pelos clientes. (Os clientes podem sobrepor isso individualmente.) Esse valor também pode ser definido no arquivo de configuração.

`PGDATA`: Local padrão do diretório de dados

`PGDATESTYLE`: Valor padrão do parâmetro de tempo de execução [DateStyle](runtime-config-client.md#GUC-DATESTYLE). (O uso desta variável de ambiente é desaconselhado.)

`PGPORT`: Número de porta padrão (de preferência definido no arquivo de configuração)

## Diagnósticos

Uma mensagem de falha que menciona `semget` ou `shmget` provavelmente indica que você precisa configurar seu kernel para fornecer memória compartilhada e semaforos adequados. Para mais discussão, consulte [Seção 18.4][(kernel-resources.md "18.4. Managing Kernel Resources")]. Você pode ser capaz de adiar a recarga do seu kernel, diminuindo [shared_buffers][(runtime-config-resource.md#GUC-SHARED-BUFFERS)] para reduzir o consumo de memória compartilhada do PostgreSQL, e/ou reduzindo [max_connections][(runtime-config-connection.md#GUC-MAX-CONNECTIONS)] para reduzir o consumo de semaforos.

Uma mensagem de falha que sugere que outro servidor já está em execução deve ser verificada cuidadosamente, por exemplo, usando o comando

```
$ ps ax | grep postgres
```

ou

```
$ ps -ef | grep postgres
```

dependendo do seu sistema. Se você tem certeza de que nenhum servidor em conflito está em execução, pode remover o arquivo de bloqueio mencionado na mensagem e tentar novamente.

Uma mensagem de falha indicando a incapacidade de se conectar a um porto pode indicar que esse porto já está sendo usado por algum processo que não é o PostgreSQL. Você também pode obter esse erro se encerrar o `postgres` e reiniciá-lo imediatamente usando o mesmo porto; nesse caso, você deve simplesmente esperar alguns segundos até que o sistema operacional feche o porto antes de tentar novamente. Por fim, você pode obter esse erro se especificar um número de porta que o seu sistema operacional considera reservado. Por exemplo, muitas versões do Unix consideram números de porta menores que 1024 como "confiáveis" e permitem apenas que o superusuário do Unix os acesse.

## Notas

O comando utilitário [pg_ctl](app-pg-ctl.md "pg_ctl") pode ser usado para iniciar e desligar o servidor `postgres` de forma segura e confortável.

Se possível, **não** use `SIGKILL` para matar o servidor principal `postgres`. Isso impedirá que o `postgres` libere os recursos do sistema (por exemplo, memória compartilhada e semaforos) que ele mantém antes de terminar. Isso pode causar problemas para iniciar uma nova execução do `postgres`.

Para encerrar o servidor `postgres` normalmente, os sinais `SIGTERM`, `SIGINT` ou `SIGQUIT` podem ser usados. O primeiro aguarda que todos os clientes sejam encerrados antes de encerrar, o segundo desconecta todas as conexões de forma forçada e o terceiro é encerrado imediatamente sem desligamento adequado, resultando em uma execução de recuperação durante o reinício.

O sinal `SIGHUP` recarregará os arquivos de configuração do servidor. É também possível enviar `SIGHUP` para um processo de servidor individual, mas isso geralmente não é sensível.

Para cancelar uma consulta em execução, envie o sinal `SIGINT` ao processo que está executando esse comando. Para encerrar um processo de backend de forma limpa, envie `SIGTERM` a esse processo. Veja também `pg_cancel_backend` e `pg_terminate_backend` em [Seção 9.28.2](functions-admin.md#FUNCTIONS-ADMIN-SIGNAL "9.28.2. Server Signaling Functions") para os equivalentes que podem ser chamados por SQL dessas duas ações.

O servidor `postgres` usa `SIGQUIT` para dizer aos processos de servidor subordinados que terminem sem limpeza normal. Este sinal *não* deve ser usado por usuários. Também não é aconselhável enviar `SIGKILL` para um processo de servidor — o processo principal `postgres` interpretará isso como um crash e forçará todos os processos irmãos a sair como parte de seu procedimento padrão de recuperação de crash.

## Bugs

As opções `--` não funcionarão no FreeBSD ou no OpenBSD. Use `-c` em vez disso. Esse é um bug nos sistemas operacionais afetados; uma futura versão do PostgreSQL fornecerá uma solução alternativa se isso não for corrigido.

Modo de Usuário Único

Para iniciar um servidor em modo de usuário único, use um comando como

```
postgres --single -D /usr/local/pgsql/data other-options my_database
```

Forneça o caminho correto para o diretório do banco de dados com `-D`, ou certifique-se de que a variável de ambiente `PGDATA` esteja definida. Especifique também o nome do banco de dados específico no qual deseja trabalhar.

Normalmente, o servidor no modo de usuário único trata a linha de nova como o terminador de entrada do comando; não há inteligência sobre os pontos e virgulas, como no psql. Para continuar um comando em várias linhas, você deve digitar barra invertida logo antes de cada nova linha, exceto a última. A barra invertida e a nova linha adjacente são ambas descartadas do comando de entrada. Note que isso acontecerá mesmo quando estiver dentro de uma literal de string ou comentário.

Mas se você usar o interruptor de linha de comando `-j`, uma única linha nova não termina a entrada do comando; em vez disso, a sequência ponto-vírgula-linha-nova a faz. Ou seja, digite um ponto e depois uma linha completamente vazia. O barra invertida-linha não é tratada especialmente nesse modo. Novamente, não há inteligência sobre a ocorrência de uma sequência desse tipo em um literal de string ou comentário.

Em qualquer modo de entrada, se você digitar um ponto e vírgula que não esteja antes ou faça parte de um terminador de entrada de comando, ele é considerado um separador de comando. Quando você digita um terminador de entrada de comando, as várias declarações que você inseriu serão executadas como uma única transação.

Para encerrar a sessão, digite EOF (**Control**+**D**, geralmente). Se você tiver digitado algum texto desde o último delimitador de entrada de comando, o EOF será considerado um delimitador de entrada de comando e será necessário outro EOF para sair.

Observe que o servidor no modo de usuário único não oferece recursos sofisticados de edição de linha (sem histórico de comandos, por exemplo). O modo de usuário único também não realiza nenhum processamento em segundo plano, como verificações automáticas ou replicação.

## Exemplos

Para iniciar `postgres` em segundo plano usando valores padrão, digite:

```
$ nohup postgres >logfile 2>&1 </dev/null &
```

Para iniciar o `postgres` com uma porta específica, por exemplo, 1234:

```
$ postgres -p 1234
```

Para se conectar a este servidor usando psql, especifique esta porta com a opção -p:

```
$ psql -p 1234
```

ou defina a variável de ambiente `PGPORT`:

```
$ export PGPORT=1234
$ psql
```

Os parâmetros de tempo de execução podem ser definidos em qualquer um desses estilos:

```
$ postgres -c work_mem=1234
$ postgres --work-mem=1234
```

Qualquer uma das formas substitui qualquer configuração que possa existir para `work_mem` em `postgresql.conf`. Observe que os underscores nos nomes dos parâmetros podem ser escritos como underscore ou hífen na linha de comando. Exceto para experimentos de curto prazo, é provavelmente melhor prática editar a configuração em `postgresql.conf` do que confiar em um interruptor de linha de comando para definir um parâmetro.

## Veja também

[initdb](app-initdb.md "initdb"), [pg_ctl](app-pg-ctl.md "pg_ctl")