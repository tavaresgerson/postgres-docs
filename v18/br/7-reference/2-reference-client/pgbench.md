## pgbench

pgbench — execute um teste de referência no PostgreSQL

## Sinopse

`pgbench` `-i` [*`option`*...] [*`dbname`*]

`pgbench` [*`option`*...] [*`dbname`*]

## Descrição

pgbench é um programa simples para executar testes de benchmark no PostgreSQL. Ele executa a mesma sequência de comandos SQL várias vezes, possivelmente em várias sessões de banco de dados concorrentes, e depois calcula a taxa média de transações (transações por segundo). Por padrão, o pgbench testa um cenário que é vagamente baseado em TPC-B, envolvendo cinco comandos `SELECT`, `UPDATE` e `INSERT` por transação. No entanto, é fácil testar outros casos escrevendo seus próprios arquivos de script de transação.

A saída típica do pgbench parece assim:

```
transaction type: <builtin: TPC-B (sort of)>
scaling factor: 10
query mode: simple
number of clients: 10
number of threads: 1
maximum number of tries: 1
number of transactions per client: 1000
number of transactions actually processed: 10000/10000
number of failed transactions: 0 (0.000%)
latency average = 11.013 ms
latency stddev = 7.351 ms
initial connection time = 45.758 ms
tps = 896.967014 (without initial connection time)
```

As primeiras sete linhas relatam algumas das configurações de parâmetros mais importantes. A sexta linha relata o número máximo de tentativas para transações com erros de serialização ou bloqueio (consulte [Falhas e Retries de Serialização/Bloqueio](pgbench.md#FAILURES-AND-RETRIES) para mais informações). A oitava linha relata o número de transações concluídas e pretendidas (estes sendo apenas o produto do número de clientes e o número de transações por cliente); estes serão iguais a menos que a execução falhou antes da conclusão ou alguns comandos SQL falharam. (No modo `-T`, apenas o número real de transações é impresso.) A próxima linha relata o número de transações falhadas devido a erros de serialização ou bloqueio (consulte [Falhas e Retries de Serialização/Bloqueio](pgbench.md#FAILURES-AND-RETRIES) para mais informações). A última linha relata o número de transações por segundo.

O teste de transação padrão semelhante ao TPC-B requer que tabelas específicas sejam configuradas previamente. O pgbench deve ser invocado com a opção `-i` (inicializar) para criar e preencher essas tabelas. (Quando você está testando um script personalizado, você não precisa desse passo, mas, em vez disso, precisará fazer qualquer configuração que seu teste precise.) A inicialização parece assim:

```
pgbench -i [ other-options ] dbname
```

onde *`dbname`* é o nome do banco de dados já criado para testar. (Você também pode precisar das opções `-h`, `-p` e/ou `-U` para especificar como se conectar ao servidor do banco de dados.)

### Atenção

`pgbench -i` cria quatro tabelas `pgbench_accounts`, `pgbench_branches`, `pgbench_history` e `pgbench_tellers`, destruindo quaisquer tabelas existentes com esses nomes. Tenha muito cuidado ao usar outro banco de dados se você tiver tabelas com esses nomes!

Na escala padrão de 1, as tabelas inicialmente contêm tantas linhas quanto:

```
table                   # of rows
---------------------------------
pgbench_branches        1
pgbench_tellers         10
pgbench_accounts        100000
pgbench_history         0
```

Você pode (e, para a maioria dos casos, provavelmente deve) aumentar o número de linhas usando a opção `-s` (fator de escala). A opção `-F` (fillfactor) também pode ser usada neste ponto.

Depois de fazer a configuração necessária, você pode executar seu benchmark com um comando que não inclua `-i`, ou seja,

```
pgbench [ options ] dbname
```

Na maioria dos casos, você precisará de algumas opções para fazer um teste útil. As opções mais importantes são `-c` (número de clientes), `-t` (número de transações), `-T` (limite de tempo) e `-f` (especificar um arquivo de script personalizado). Veja abaixo uma lista completa.

## Opções

O que segue é dividido em três subseções. Diferentes opções são usadas durante a inicialização do banco de dados e durante a execução de benchmarks, mas algumas opções são úteis em ambos os casos.

### Opções de Inicialização

pgbench aceita os seguintes argumentos de inicialização na linha de comando:

`[-d] dbname` `[--dbname=]dbname` [#](#PGBENCH-OPTION-DBNAME): Especifica o nome do banco de dados a ser testado. Se não for especificado, a variável de ambiente `PGDATABASE` é usada. Se essa não for definida, o nome de usuário especificado para a conexão é usado.

`-i` `--initialize` [#](#PGBENCH-OPTION-INITIALIZE): Requerida para invocar o modo de inicialização.

`-I init_steps` `--init-steps=init_steps` [#](#PGBENCH-OPTION-INIT-STEPS): Realize apenas um conjunto selecionado das etapas de inicialização normal. *`init_steps`* especifica as etapas de inicialização a serem realizadas, usando um caractere por etapa. Cada etapa é invocada na ordem especificada. O padrão é `dtgvp`. Os passos disponíveis são:

`d` (Drop) [#](#PGBENCH-OPTION-INIT-STEPS-D) :   Remova quaisquer tabelas existentes do pgbench.

`t` (criar tabelas) [#](#PGBENCH-OPTION-INIT-STEPS-T) :   Crie as tabelas utilizadas pelo cenário padrão do pgbench, a saber, `pgbench_accounts`, `pgbench_branches`, `pgbench_history` e `pgbench_tellers`.

`g` ou `G` (Gerar dados, de lado do cliente ou de lado do servidor) [#](#PGBENCH-OPTION-INIT-STEPS-G) :   Gerar dados e carregá-los nas tabelas padrão, substituindo quaisquer dados já presentes.

Com `g` (geração de dados no lado do cliente), os dados são gerados no cliente `pgbench` e, em seguida, enviados para o servidor. Isso utiliza a largura de banda cliente/servidor extensivamente através de um `COPY`. O `pgbench` utiliza a opção `FREEZE` para carregar dados em tabelas comuns (não particionadas) com a versão 14 ou posterior do PostgreSQL para acelerar o subsequente `VACUUM`. O uso de `g` faz com que o registro imprima uma mensagem a cada 100.000 linhas enquanto gera dados para todas as tabelas.

Com `G` (geração de dados no lado do servidor), apenas pequenas consultas são enviadas do cliente `pgbench` e, em seguida, os dados são realmente gerados no servidor. Não é necessária largura de banda significativa para essa variante, mas o servidor fará mais trabalho. O uso de `G` faz com que o registro não imprima nenhuma mensagem de progresso durante a geração de dados.

O comportamento de inicialização padrão usa geração de dados do lado do cliente (equivalente a `g`).

`v` (Vácuo) [#](#PGBENCH-OPTION-INIT-STEPS-V) :  Invoque `VACUUM` nas tabelas padrão.

`p` (criar chaves primárias) [#](#PGBENCH-OPTION-INIT-STEPS-P) :   Crie índices de chave primária nas tabelas padrão.

`f` (criar Chaves Estrangeiras) [#](#PGBENCH-OPTION-INIT-STEPS-F) :   Criar restrições de chave estrangeira entre as tabelas padrão. (Observe que este passo não é realizado por padrão.)

`-F` *`fillfactor`* `--fillfactor=`*`fillfactor`* [#](#PGBENCH-OPTION-FILLFACTOR): Crie as tabelas `pgbench_accounts`, `pgbench_tellers` e `pgbench_branches` com o fator de preenchimento fornecido. O padrão é 100.

`-n` `--no-vacuum` [#](#PGBENCH-OPTION-NO-VACUUM-INIT): Não realize a aspiração durante a inicialização. (Essa opção suprime a etapa de inicialização `v`, mesmo que tenha sido especificada em `-I`.)

`-q` `--quiet` [#](#PGBENCH-OPTION-QUIET): Alterar o registro para o modo silencioso, produzindo apenas uma mensagem de progresso a cada 5 segundos. O registro padrão imprime uma mensagem a cada 100.000 linhas, o que geralmente produz muitas linhas por segundo (especialmente em hardware de boa qualidade).

Essa configuração não tem efeito se `G` for especificado em `-I`.

`-s` *`scale_factor`* `--scale=`*`scale_factor`* [#](#PGBENCH-OPTION-SCALE-INIT): Multiplique o número de linhas geradas pelo fator de escala. Por exemplo, `-s 100` criará 10.000.000 de linhas na tabela `pgbench_accounts`. O padrão é 1. Quando a escala é de 20.000 ou maior, as colunas usadas para armazenar identificadores de conta (colunas `aid`) mudarão para usar inteiros maiores (`bigint`), para serem grandes o suficiente para armazenar a faixa de identificadores de conta.

`--foreign-keys` [#](#PGBENCH-OPTION-FOREIGN-KEYS): Crie restrições de chave estrangeira entre as tabelas padrão. (Esta opção adiciona a etapa `f` à sequência de etapas de inicialização, se ainda não estiver presente.)

`--index-tablespace=index_tablespace` [#](#PGBENCH-OPTION-INDEX-TABLESPACE): Crie índices nos espaços de tabelas especificados, em vez do espaço de tabelas padrão.

`--partition-method=NAME` [#](#PGBENCH-OPTION-PARTITION-METHOD): Crie uma tabela particionada `pgbench_accounts` com o método *`NAME`*. Os valores esperados são `range` ou `hash`. Esta opção exige que `--partitions` esteja definido como não nulo. Se não especificado, o padrão é `range`.

`--partitions=NUM` [#](#PGBENCH-OPTION-PARTITIONS): Crie uma tabela particionada `pgbench_accounts` com *`NUM`* particionamentos de tamanho quase igual para o número escalado de contas. O padrão é `0`, o que significa que não há particionamento.

`--tablespace=tablespace` [#](#PGBENCH-OPTION-TABLESPACE): Crie tabelas no espaço de tabelas especificado, em vez do espaço de tabelas padrão.

`--unlogged-tables` [#](#PGBENCH-OPTION-UNLOGGED-TABLES): Crie todas as tabelas como tabelas não registradas, em vez de tabelas permanentes.

### Opções de Benchmarking

pgbench aceita os seguintes argumentos de benchmarking de linha de comando:

`-b` *`scriptname[@weight]`* `--builtin`=*`scriptname[@weight]`* [#](#PGBENCH-OPTION-BUILTIN): Adicione o script interno especificado à lista de scripts a serem executados. Os scripts internos disponíveis são: `tpcb-like`, `simple-update` e `select-only`. Prefixo não ambíguo de nomes internos é aceito. Com o nome especial `list`, mostre a lista de scripts internos e saia imediatamente.

Opcionalmente, escreva um peso inteiro após `@` para ajustar a probabilidade de seleção deste script em relação a outros. O peso padrão é 1. Veja abaixo para detalhes.

`-c` *`clients`* `--client=`*`clients`* [#](#PGBENCH-OPTION-CLIENT): Número de clientes simulados, ou seja, número de sessões de banco de dados concorrentes. O padrão é 1.

`-C` `--connect` [#](#PGBENCH-OPTION-CONNECT): Estabeleça uma nova conexão para cada transação, em vez de fazer isso apenas uma vez por sessão do cliente. Isso é útil para medir o custo da conexão.

`-D` *`varname`*`=`*`value`* `--define=`*`varname`*`=`*`value`* [#](#PGBENCH-OPTION-DEFINE): Define uma variável para uso por um script personalizado (consulte abaixo). Múltiplas opções de `-D` são permitidas.

`-f` *`filename[@weight]`* `--file=`*`filename[@weight]`* [#](#PGBENCH-OPTION-FILE): Adicione um script de transação lido de *`filename`* à lista de scripts a serem executados.

Opcionalmente, escreva um peso inteiro após `@` para ajustar a probabilidade de seleção deste script em relação a outros. O peso padrão é 1. (Para usar um nome de arquivo de script que inclua um caractere `@`, adicione um peso para que não haja ambiguidade, por exemplo, `filen@me@1`). Veja abaixo para obter detalhes.

`-j` *`threads`* `--jobs=`*`threads`* [#](#PGBENCH-OPTION-JOBS): Número de threads de trabalhador dentro do pgbench. Usar mais de uma thread pode ser útil em máquinas com vários processadores. Os clientes são distribuídos o mais uniformemente possível entre as threads disponíveis. O padrão é 1.

`-l` `--log` [#](#PGBENCH-OPTION-LOG): Escreva informações sobre cada transação em um arquivo de registro. Veja abaixo para obter detalhes.

`-L` *`limit`* `--latency-limit=`*`limit`* [#](#PGBENCH-OPTION-LATENCY-LIMIT): As transações que duram mais de *`limit`* milissegundos são contadas e relatadas separadamente, como *tardias*.

Quando o controle de tráfego é usado (`--rate=...`), as transações que ficam para trás no cronograma em mais de *`limit`* ms, e, portanto, não têm esperança de atender ao limite de latência, não são enviadas para o servidor. Elas são contadas e relatadas separadamente como *descartáveis*.

Quando a opção `--max-tries` é usada, uma transação que falha devido a uma anomalia de serialização ou por um bloqueio não será retente se o tempo total de todas as suas tentativas for maior que *`limit`* ms. Para limitar apenas o tempo das tentativas e não seu número, use `--max-tries=0`. Por padrão, a opção `--max-tries` é definida para 1 e as transações com erros de serialização/bloqueio não são retente. Consulte [Falhas e Retentes de Serialização/Bloqueio](pgbench.md#FAILURES-AND-RETRIES "Failures and Serialization/Deadlock Retries") para obter mais informações sobre a retente de tais transações.

`-M` *`querymode`* `--protocol=`*`querymode`* [#](#PGBENCH-OPTION-PROTOCOL): Protocolo para enviar consultas ao servidor:

* `simple`: use o protocolo de consulta simples. * `extended`: use o protocolo de consulta estendida. * `prepared`: use o protocolo de consulta estendida com declarações preparadas.

No modo `prepared`, o pgbench reutiliza o resultado da análise de análise a partir da segunda iteração da consulta, portanto, o pgbench é mais rápido do que em outros modos.

O protocolo de consulta padrão é simples. (Consulte o [Capítulo 54](protocol.md) para obter mais informações.)

`-n` `--no-vacuum` [#](#PGBENCH-OPTION-NO-VACUUM-RUN): Não realize a aspiração antes de executar o teste. Esta opção é *necessária* se você estiver executando um cenário de teste personalizado que não inclui as tabelas padrão `pgbench_accounts`, `pgbench_branches`, `pgbench_history` e `pgbench_tellers`.

`-N` `--skip-some-updates` [#](#PGBENCH-OPTION-SKIP-SOME-UPDATES): Execute o script de atualização simples integrado. Abreviação para `-b simple-update`.

`-P` *`sec`* `--progress=`*`sec`* [#](#PGBENCH-OPTION-PROGRESS): Mostrar relatório de progresso a cada *`sec`* segundos. O relatório inclui o tempo desde o início da execução, o TPS desde o último relatório e a latência média da transação, desvio padrão e o número de transações falhadas desde o último relatório. Sob o controle de tráfego (`-R`), a latência é calculada em relação ao horário de início da transação agendada, e não ao horário real de início da transação, portanto, também inclui o tempo médio de atraso na programação. Quando `--max-tries` é usado para habilitar tentativas de retransmissão de transações após erros de serialização/bloqueio, o relatório inclui o número de transações retransmitidas e a soma de todas as tentativas.

`-r` `--report-per-command` [#](#PGBENCH-OPTION-REPORT-LATENCIES): Relate as seguintes estatísticas para cada comando após o término do benchmark: a latência média por declaração (tempo de execução sob a perspectiva do cliente), o número de falhas e o número de tentativas após erros de serialização ou bloqueio em este comando. O relatório exibe as estatísticas de tentativas apenas se a opção `--max-tries` não for igual a 1.

`-R` *`rate`* `--rate=`*`rate`* [#](#PGBENCH-OPTION-RATE): Execute transações com o objetivo da taxa especificada em vez de executar o mais rápido possível (o padrão). A taxa é dada em transações por segundo. Se a taxa alvo estiver acima da taxa máxima possível, o limite da taxa não afetará os resultados.

A taxa é direcionada, iniciando transações em uma linha de tempo cronológica distribuída de Poisson. O cronograma de tempo de início esperado avança com base em quando o cliente iniciou pela primeira vez, e não quando a transação anterior terminou. Essa abordagem significa que, quando as transações passam pelo seu horário de término original, é possível que as posteriores recuperem o atraso.

Quando o controle de tráfego está ativo, a latência da transação relatada no final da execução é calculada a partir dos horários de início agendados, portanto, inclui o tempo que cada transação teve que esperar para que a transação anterior terminasse. O tempo de espera é chamado de tempo de atraso de cronograma, e sua média e máxima também são relatadas separadamente. A latência da transação em relação ao horário real de início da transação, ou seja, o tempo gasto executando a transação no banco de dados, pode ser calculada subtraindo o tempo de atraso de cronograma da latência relatada.

Se `--latency-limit` for usado juntamente com `--rate`, uma transação pode ficar tão atrasada que já ultrapassa o limite de latência quando a transação anterior termina, porque a latência é calculada a partir do horário de início agendado. Tais transações não são enviadas ao servidor, mas são ignoradas completamente e contadas separadamente.

Um longo atraso no cronograma é uma indicação de que o sistema não pode processar transações na taxa especificada, com o número escolhido de clientes e threads. Quando o tempo médio de execução da transação é maior que o intervalo agendado entre cada transação, cada transação sucessiva ficará ainda mais atrasada, e o atraso no cronograma continuará aumentando quanto mais tempo a execução do teste durar. Quando isso acontece, você terá que reduzir a taxa de transação especificada.

`-s` *`scale_factor`* `--scale=`*`scale_factor`* [#](#PGBENCH-OPTION-SCALE-RUN): Reporte o fator de escala especificado na saída do pgbench. Com os testes internos, isso não é necessário; o fator de escala correto será detectado contando o número de linhas na tabela `pgbench_branches`. No entanto, ao testar apenas benchmarks personalizados (opção `-f`), o fator de escala será relatado como 1 a menos que essa opção seja usada.

`-S` `--select-only` [#](#PGBENCH-OPTION-SELECT-ONLY): Execute o script de seleção integrado. Abreviação para `-b select-only`.

`-t` *`transactions`* `--transactions=`*`transactions`* [#](#PGBENCH-OPTION-TRANSACTIONS): Número de transações que cada cliente executa. O padrão é 10.

`-T` *`seconds`* `--time=`*`seconds`* [#](#PGBENCH-OPTION-TIME): Realize o teste por tantos segundos, em vez de um número fixo de transações por cliente. `-t` e `-T` são mutuamente exclusivos.

`-v` `--vacuum-all` [#](#PGBENCH-OPTION-VACUUM-ALL): Vácume todas as quatro tabelas padrão antes de executar o teste. Com nem `-n` nem `-v`, o pgbench vácumeará as tabelas `pgbench_tellers` e `pgbench_branches`, e truncará `pgbench_history`.

`--aggregate-interval=seconds` [#](#PGBENCH-OPTION-AGGREGATE-INTERVAL): Comprimento do intervalo de agregação (em segundos). Pode ser usado apenas com a opção `-l`. Com esta opção, o log contém dados resumidos por intervalo, conforme descrito abaixo.

`--exit-on-abort` [#](#PGBENCH-OPTION-EXIT-ON-ABORT): Saia imediatamente quando qualquer cliente for interrompido devido a algum erro. Sem essa opção, mesmo quando um cliente for interrompido, outros clientes podem continuar sua execução conforme especificado na opção `-t` ou `-T`, e o pgbench imprimirá resultados incompletos neste caso.

Observe que as falhas de serialização ou as falhas de bloqueio não abortam o cliente, portanto, não são afetadas por essa opção. Consulte [Falhas e Repetições de Serialização/Bloqueio](pgbench.md#FAILURES-AND-RETRIES) para obter mais informações.

`--failures-detailed` [#](#PGBENCH-OPTION-FAILURES-DETAILED): Relatar falhas nos logs de per-transação e agregação, bem como nos relatórios principais e por script, agrupados pelos seguintes tipos:

* falhas de serialização; * falhas de bloqueio;

Veja [Falhas e Serialização/Reintentos de Deadlock](pgbench.md#FAILURES-AND-RETRIES) para mais informações.

`--log-prefix=prefix` [#](#PGBENCH-OPTION-LOG-PREFIX): Defina o prefixo do nome do arquivo para os arquivos de registro criados por `--log`. O padrão é `pgbench_log`.

`--max-tries=number_of_tries` [#](#PGBENCH-OPTION-MAX-TRIES): Ative as tentativas para transações com erros de serialização/bloqueio de dados e defina o número máximo dessas tentativas. Esta opção pode ser combinada com a opção `--latency-limit`, que limita o tempo total de todas as tentativas de transação; além disso, não é possível usar um número ilimitado de tentativas (`--max-tries=0`) sem `--latency-limit` ou `--time`. O valor padrão é 1 e as transações com erros de serialização/bloqueio de dados não são reatletas. Consulte [Falhas e tentativas de reatletas de serialização/bloqueio de dados](pgbench.md#FAILURES-AND-RETRIES "Failures and Serialization/Deadlock Retries") para obter mais informações sobre a reatletas de tais transações.

`--progress-timestamp` [#](#PGBENCH-OPTION-PROGRESS-TIMESTAMP): Ao mostrar o progresso (opção `-P`), use um timestamp (epocas Unix) em vez do número de segundos desde o início da execução. A unidade é em segundos, com precisão de milissegundo após o ponto. Isso ajuda a comparar logs gerados por várias ferramentas.

`--random-seed=`*`seed`* [#](#PGBENCH-OPTION-RANDOM-SEED): Definir a semente do gerador aleatório. Gera a semente do gerador aleatório do sistema, que então produz uma sequência de estados iniciais do gerador, um para cada thread. Os valores para *`seed`* podem ser: `time` (o padrão, a semente é baseada na hora atual), `rand` (use uma fonte aleatória forte, caso nenhuma esteja disponível), ou um valor inteiro decimal não assinado. O gerador aleatório é invocado explicitamente a partir de um script do pgbench (funções `random...`) ou implicitamente (por exemplo, a opção `--rate` usa isso para agendar transações). Quando definido explicitamente, o valor usado para a semente é mostrado no terminal. Qualquer valor permitido para *`seed`* também pode ser fornecido através da variável de ambiente `PGBENCH_RANDOM_SEED`. Para garantir que a semente fornecida afete todos os usos possíveis, coloque esta opção primeiro ou use a variável de ambiente.

Definir explicitamente a semente permite reproduzir exatamente uma execução de `pgbench`, no que diz respeito a números aleatórios. Como o estado aleatório é gerenciado por thread, isso significa que a mesma execução de `pgbench` para uma invocação idêntica, se houver um cliente por thread e não houver dependências externas ou de dados, é exatamente a mesma. Do ponto de vista estatístico, reproduzir execuções exatamente é uma má ideia, pois pode esconder a variabilidade de desempenho ou melhorar o desempenho indevidamente, por exemplo, ao acessar as mesmas páginas que uma execução anterior. No entanto, também pode ser muito útil para depuração, por exemplo, reexecutando um caso complicado que leva a um erro. Use com sabedoria.

`--sampling-rate=rate` [#](#PGBENCH-OPTION-SAMPLING-RATE): Taxa de amostragem, usada ao escrever dados no log, para reduzir a quantidade de log gerado. Se esta opção for dada, apenas a fração especificada de transações será registrada. 1,0 significa que todas as transações serão registradas, 0,05 significa que apenas 5% das transações serão registradas.

Lembre-se de levar em consideração a taxa de amostragem ao processar o arquivo de registro. Por exemplo, ao calcular os valores de TPS, você precisa multiplicar os números de acordo (por exemplo, com uma taxa de amostragem de 0,01, você obterá apenas 1/100 do TPS real).

`--show-script=`*`scriptname`* [#](#PGBENCH-OPTION-SHOW-SCRIPT): Mostre o código real do script embutido *`scriptname`* no stderr e saia imediatamente.

`--verbose-errors` [#](#PGBENCH-OPTION-VERBOSE-ERRORS): Imprimir mensagens sobre todos os erros e falhas (erros sem tentativa de reposição), incluindo qual limite para tentativas foi excedido e até que ponto foi excedido para as falhas de serialização/bloqueio de acesso. (Observe que, neste caso, a saída pode ser significativamente aumentada.) Consulte [Falhas e tentativas de reposição de serialização/bloqueio de acesso](pgbench.md#FAILURES-AND-RETRIES "Failures and Serialization/Deadlock Retries") para obter mais informações.

### Opções Comuns

O pgbench também aceita os seguintes argumentos comuns de linha de comando para parâmetros de conexão e outras configurações comuns:

`--debug` [#](#PGBENCH-OPTION-DEBUG): Imprimir a saída de depuração.

`-h` *`hostname`* `--host=`*`hostname`* [#](#PGBENCH-OPTION-HOST): Nome do servidor de banco de dados

`-p` *`port`* `--port=`*`port`* [#](#PGBENCH-OPTION-PORT): Número da porta do servidor de banco de dados

`-U` *`login`* `--username=`*`login`* [#](#PGBENCH-OPTION-USERNAME): O nome do usuário para se conectar

`-V` `--version` [#](#PGBENCH-OPTION-VERSION): Imprimir a versão do pgbench e sair.

`-?` `--help` [#](#PGBENCH-OPTION-HELP): Mostrar ajuda sobre os argumentos da linha de comando do comando pgbench e sair.

## Status de saída

Uma execução bem-sucedida sairá com o status 0. O status de saída 1 indica problemas estáticos, como opções inválidas de linha de comando ou erros internos que não deveriam ocorrer. Erros iniciais que ocorrem ao iniciar benchmarks, como falhas na conexão inicial, também saem com o status 1. Erros durante a execução, como erros de banco de dados ou problemas no script, resultarão em status de saída 2. No último caso, o pgbench imprimirá resultados parciais se a opção `--exit-on-abort` não for especificada.

## Meio Ambiente

`PGDATABASE` `PGHOST` `PGPORT` `PGUSER` [#](#PGBENCH-ENVIRONMENT-PGDATABASE): Parâmetros de conexão padrão.

Esse utilitário, como a maioria dos outros utilitários do PostgreSQL, utiliza as variáveis de ambiente suportadas pelo libpq (consulte a [Seção 32.15](libpq-envars.md)).

A variável de ambiente `PG_COLOR` especifica se a cor deve ser usada nas mensagens de diagnóstico. Os valores possíveis são `always`, `auto` e `never`.

## Notas

### O que é realmente realizado na “transação” no pgbench?

O pgbench executa scripts de teste escolhidos aleatoriamente a partir de uma lista especificada. Os scripts podem incluir scripts embutidos especificados com `-b` e scripts fornecidos pelo usuário especificados com `-f`. Cada script pode receber um peso relativo especificado após um `@` para alterar sua probabilidade de seleção. O peso padrão é `1`. Scripts com um peso de `0` são ignorados.

O script de transação pré-definido (também invocado com `-b tpcb-like`) emite sete comandos por transação sobre `aid`, `tid`, `bid` e `delta` escolhidos aleatoriamente. O cenário é inspirado no benchmark TPC-B, mas não é realmente TPC-B, daí o nome.

1. `BEGIN;`
2. `UPDATE pgbench_accounts SET abalance = abalance + :delta WHERE aid = :aid;`
3. `SELECT abalance FROM pgbench_accounts WHERE aid = :aid;`
4. `UPDATE pgbench_tellers SET tbalance = tbalance + :delta WHERE tid = :tid;`
5. `UPDATE pgbench_branches SET bbalance = bbalance + :delta WHERE bid = :bid;`
6. `INSERT INTO pgbench_history (tid, bid, aid, delta, mtime) VALUES (:tid, :bid, :aid, :delta, CURRENT_TIMESTAMP);`
7. `END;`

Se você selecionar o embutido `simple-update` (também `-N`), os passos 4 e 5 não são incluídos na transação. Isso evitará a concorrência de atualização nessas tabelas, mas torna o caso de teste ainda menos semelhante ao TPC-B.

Se você selecionar o embutido `select-only` (também `-S`), apenas o `SELECT` é emitido.

### Scripts Personalizados

O pgbench tem suporte para executar cenários de benchmark personalizados, substituindo o script de transação padrão (descrito acima) por um script de transação lido a partir de um arquivo (opção `-f`). Neste caso, uma “transação” é contada como uma execução de um arquivo de script.

Um arquivo de script contém um ou mais comandos SQL terminados por pontos e vírgulas. Linhas vazias e linhas que começam com `--` são ignoradas. Arquivos de script também podem conter “comandos meta”, que são interpretados pelo próprio pgbench, conforme descrito abaixo.

Nota

Antes do PostgreSQL 9.6, os comandos SQL em arquivos de script eram terminados por novas linhas, e, portanto, não podiam ser continuados em várias linhas. Agora, um ponto e vírgula é *requisitado* para separar comandos SQL consecutivos (embora um comando SQL não precise de um se for seguido por um comando meta). Se você precisa criar um arquivo de script que funcione tanto com versões antigas quanto com novas do pgbench, certifique-se de escrever cada comando SQL em uma única linha que termine com um ponto e vírgula.

Assume-se que os scripts do pgbench não contenham blocos incompletos de transações SQL. Se, durante a execução, o cliente atingir o final do script sem completar o último bloco de transação, ele será abortado.

Existe uma função simples de substituição de variáveis para arquivos de script. Os nomes das variáveis devem consistir em letras (incluindo letras não latinas), dígitos e sublinhados, com o primeiro caractere não sendo um dígito. As variáveis podem ser definidas pelo comando `-D` da opção de linha de comando, explicada acima, ou pelos comandos meta explicados abaixo. Além das variáveis pré-definidas por `-D` opções de linha de comando, há algumas variáveis que são pré-definidas automaticamente, listadas em [Tabela 301](pgbench.md#PGBENCH-AUTOMATIC-VARIABLES). Um valor especificado para essas variáveis usando `-D` tem precedência sobre os pré-definidos automaticamente. Uma vez definida, o valor de uma variável pode ser inserido em um comando SQL escrevendo [[`:`]*`variablename`*. Ao executar mais de uma sessão de cliente, cada sessão tem seu próprio conjunto de variáveis. O pgbench suporta até 255 usos de variáveis em uma declaração.

**Tabela 301. Variáveis automáticas do pgbench**



<table>
 <colgroup>
  <col class="col1"/>
  <col class="col2"/>
 </colgroup>
 <thead>
  <tr>
   <th>
    Variable
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
     client_id
    </code>
   </td>
   <td>
    número único que identifica a sessão do cliente (começa de zero)
   </td>
  </tr>
  <tr>
   <td>
    <code>
     default_seed
    </code>
   </td>
   <td>
    semente usada em funções de permutação hash e pseudorandom por padrão
   </td>
  </tr>
  <tr>
   <td>
    <code>
     random_seed
    </code>
   </td>
   <td>
    semente do gerador aleatório (a menos que seja sobrescrita
    <code>
     -D
    </code>
    )
   </td>
  </tr>
  <tr>
   <td>
    <code>
     scale
    </code>
   </td>
   <td>
    fator atual de escala
   </td>
  </tr>
 </tbody>
</table>










Os comandos meta de arquivo de script começam com uma barra invertida (`\`) e normalmente se estendem até o final da linha, embora possam ser continuados para linhas adicionais escrevendo barra invertida-retorno. Os argumentos de um comando meta são separados por espaço em branco. Esses comandos meta são suportados:

`\gset [prefix]` `\aset [prefix]` [#](#PGBENCH-METACOMMAND-GSET): Esses comandos podem ser usados para encerrar consultas SQL, ocupando o lugar do ponto e vírgula final (`;`).

Quando o comando `\gset` é usado, espera-se que a consulta SQL anterior retorne uma única linha, cujos campos são armazenados em variáveis com nomes baseados nos nomes dos campos, e prefixados com *`prefix`* se fornecidos.

Quando o comando `\aset` é usado, todas as consultas SQL combinadas (separadas por `\;`) têm suas colunas armazenadas em variáveis com nomes baseados nos nomes das colunas, e prefixadas com *`prefix`* se fornecidas. Se uma consulta não retornar nenhuma linha, não é feita nenhuma atribuição e a variável pode ser testada para existência para detectar isso. Se uma consulta retornar mais de uma linha, o último valor é mantido.

`\gset` e `\aset` não podem ser usados no modo de pipeline, uma vez que os resultados da consulta ainda não estão disponíveis no momento em que os comandos os necessitam.

O exemplo a seguir coloca o saldo final da conta da primeira consulta na variável *`abalance`*, e preenche as variáveis *`p_two`* e *`p_three`* com inteiros da terceira consulta. O resultado da segunda consulta é descartado. O resultado das duas últimas consultas combinadas é armazenado nas variáveis *`four`* e *`five`*.

```
UPDATE pgbench_accounts SET abalance = abalance + :delta WHERE aid = :aid RETURNING abalance \gset -- compound of two queries SELECT 1 \; SELECT 2 AS two, 3 AS three \gset p_ SELECT 4 AS four \; SELECT 5 AS five \aset
```

`\if` *`expression`* `\elif` *`expression`* `\else` `\endif` [#](#PGBENCH-METACOMMAND-IF-ELSE): Este grupo de comandos implementa blocos condicionais nestables, de forma semelhante ao `psql` de `\if` *`expression`](app-psql.md#PSQL-METACOMMAND-IF). As expressões condicionais são idênticas às de `\set`, com valores não nulos interpretados como verdadeiros.

`\set varname expression` [#](#PGBENCH-METACOMMAND-SET): Define a variável *`varname`* com um valor calculado a partir de *`expression`*. A expressão pode conter a constante `NULL`, constantes booleanas `TRUE` e `FALSE`, constantes inteiras como `5432`, constantes duplas como `3.14159`, referências a variáveis [[`:`]*`variablename`*, [operadores](pgbench.md#PGBENCH-BUILTIN-OPERATORS "Built-in Operators") com a precedência e a associatividade SQL usual, [chamadas de função](pgbench.md#PGBENCH-BUILTIN-FUNCTIONS "Built-In Functions"), expressões condicionais genéricas SQL [`CASE`](functions-conditional.md#FUNCTIONS-CASE "9.18.1. CASE") e parênteses.

As funções e a maioria dos operadores retornam `NULL` na entrada `NULL`.

Para fins condicionados, os valores numéricos não nulos são `TRUE`, os valores numéricos zero e `NULL` são `FALSE`.

As constantes inteiras e decimais muito grandes ou pequenas, bem como os operadores aritméticos inteiros (`+`, `-`, `*` e `/`) geram erros por excesso.

Quando não é fornecida uma cláusula final `ELSE` para um `CASE`, o valor padrão é `NULL`.

Exemplos:

```
\set ntellers 10 * :scale \set aid (1021 * random(1, 100000 * :scale)) % \ (100000 * :scale) + 1 \set divx CASE WHEN :x <> 0 THEN :y/:x ELSE NULL END
```

`\sleep number [ us | ms | s ]` [#](#PGBENCH-METACOMMAND-SLEEP): Faz com que a execução do script durma por a duração especificada em microsegundos (`us`), milissegundos (`ms`) ou segundos (`s`). Se a unidade for omitida, então segundos são os padrões. *`number`* pode ser uma constante inteira ou uma `:`*`variablename`* referência a uma variável que tenha um valor inteiro.

Exemplo:

```
\sleep 10 ms
```

`\setshell varname command [ argument ... ]` [#](#PGBENCH-METACOMMAND-SETSHELL): Define a variável *`varname`* como o resultado do comando de shell *`command`* com os *`argument`*(s) fornecidos. O comando deve retornar um valor inteiro através de sua saída padrão.

*`command`* e cada *`argument`* pode ser uma constante de texto ou uma referência *`:`*`variablename`* para uma variável. Se você deseja usar um *`argument`* começando com um colon, escreva um colon adicional no início de *`argument`*.

Exemplo:

```
\setshell variable_to_be_assigned command literal_argument :variable ::literal_starting_with_colon
```

`\shell command [ argument ... ]` [#](#PGBENCH-METACOMMAND-SHELL): O mesmo que `\setshell`, mas o resultado do comando é descartado.

Exemplo:

```
\shell command literal_argument :variable ::literal_starting_with_colon
```

`\startpipeline` `\syncpipeline` `\endpipeline` [#](#PGBENCH-METACOMMAND-PIPELINE): Este grupo de comandos implementa a encadernação de instruções SQL. Um pipeline deve começar com um `\startpipeline` e terminar com um `\endpipeline`. Entre eles, pode haver qualquer número de comandos `\syncpipeline`, que envia uma mensagem de sincronização (protocol-flow.md#PROTOCOL-FLOW-EXT-QUERY "54.2.3. Extended Query") sem encerrar o pipeline em andamento e limpar o buffer de envio. No modo pipeline, as instruções são enviadas ao servidor sem esperar pelos resultados das instruções anteriores. Veja [Seção 32.5](libpq-pipeline-mode.md "32.5. Pipeline Mode") para mais detalhes. O modo pipeline requer o uso do protocolo de consulta estendido.

### Operadores embutidos

Os operadores aritméticos, de comparação de bits, lógicos e listados na [Tabela 302](pgbench.md#PGBENCH-OPERATORS "Table 302. pgbench Operators") são integrados ao pgbench e podem ser usados em expressões que aparecem em [`\set`](pgbench.md#PGBENCH-METACOMMAND-SET). Os operadores são listados em ordem de precedência crescente. Exceto conforme indicado, os operadores que recebem duas entradas numéricas produzirão um valor duplo se qualquer uma das entradas for dupla, caso contrário, eles produzirão um resultado inteiro.

**Tabela 302. Operadores pgbench**



<table>
 <colgroup>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th class="func_table_entry">
    <p class="func_signature">
     Operador
    </p>
    <p>
     Descrição
    </p>
    <p>
     Exemplo(s)
    </p>
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <em class="replaceable">
      <code>
       boolean
      </code>
     </em>
     <code>
      OR
     </code>
     <em class="replaceable">
      <code>
       boolean
      </code>
     </em>
     →
     <code>
      <em class="replaceable">
       <code>
        boolean
       </code>
      </em>
     </code>
    </p>
    <p>
     OU lógico
    </p>
    <p>
     <code>
      5 or 0
     </code>
     →
     <code>
      TRUE
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <em class="replaceable">
      <code>
       boolean
      </code>
     </em>
     <code>
      AND
     </code>
     <em class="replaceable">
      <code>
       boolean
      </code>
     </em>
     →
     <code>
      <em class="replaceable">
       <code>
        boolean
       </code>
      </em>
     </code>
    </p>
    <p>
     E lógico e
    </p>
    <p>
     <code>
      3 and 0
     </code>
     →
     <code>
      FALSE
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      NOT
     </code>
     <em class="replaceable">
      <code>
       boolean
      </code>
     </em>
     →
     <code>
      <em class="replaceable">
       <code>
        boolean
       </code>
      </em>
     </code>
    </p>
    <p>
     Lógico NÃO
    </p>
    <p>
     <code>
      not false
     </code>
     →
     <code>
      TRUE
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <em class="replaceable">
      <code>
       boolean
      </code>
     </em>
     <code>
      IS [NOT] (NULL|TRUE|FALSE)
     </code>
     →
     <code>
      <em class="replaceable">
       <code>
        boolean
       </code>
      </em>
     </code>
    </p>
    <p>
     Testes de valor booleano
    </p>
    <p>
     <code>
      1 is null
     </code>
     →
     <code>
      FALSE
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <em class="replaceable">
      <code>
       value
      </code>
     </em>
     <code>
      ISNULL|NOTNULL
     </code>
     →
     <code>
      <em class="replaceable">
       <code>
        boolean
       </code>
      </em>
     </code>
    </p>
    <p>
     Testes de nulidade
    </p>
    <p>
     <code>
      1 notnull
     </code>
     →
     <code>
      TRUE
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <em class="replaceable">
      <code>
       number
      </code>
     </em>
     <code>
      =
     </code>
     <em class="replaceable">
      <code>
       number
      </code>
     </em>
     →
     <code>
      <em class="replaceable">
       <code>
        boolean
       </code>
      </em>
     </code>
    </p>
    <p>
     Igual
    </p>
    <p>
     <code>
      5 = 4
     </code>
     →
     <code>
      FALSE
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <em class="replaceable">
      <code>
       number
      </code>
     </em>
     <code>
      &lt;&gt;
     </code>
     <em class="replaceable">
      <code>
       number
      </code>
     </em>
     →
     <code>
      <em class="replaceable">
       <code>
        boolean
       </code>
      </em>
     </code>
    </p>
    <p>
     Não igual
    </p>
    <p>
     <code>
      5 &lt;&gt; 4
     </code>
     →
     <code>
      TRUE
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <em class="replaceable">
      <code>
       number
      </code>
     </em>
     <code>
      !=
     </code>
     <em class="replaceable">
      <code>
       number
      </code>
     </em>
     →
     <code>
      <em class="replaceable">
       <code>
        boolean
       </code>
      </em>
     </code>
    </p>
    <p>
     Não igual
    </p>
    <p>
     <code>
      5 != 5
     </code>
     →
     <code>
      FALSE
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <em class="replaceable">
      <code>
       number
      </code>
     </em>
     <code>
      &lt;
     </code>
     <em class="replaceable">
      <code>
       number
      </code>
     </em>
     →
     <code>
      <em class="replaceable">
       <code>
        boolean
       </code>
      </em>
     </code>
    </p>
    <p>
     Menos de
    </p>
    <p>
     <code>
      5 &lt; 4
     </code>
     →
     <code>
      FALSE
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <em class="replaceable">
      <code>
       number
      </code>
     </em>
     <code>
      &lt;=
     </code>
     <em class="replaceable">
      <code>
       number
      </code>
     </em>
     →
     <code>
      <em class="replaceable">
       <code>
        boolean
       </code>
      </em>
     </code>
    </p>
    <p>
     Menos ou igual a
    </p>
    <p>
     <code>
      5 &lt;= 4
     </code>
     →
     <code>
      FALSE
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <em class="replaceable">
      <code>
       number
      </code>
     </em>
     <code>
      &gt;
     </code>
     <em class="replaceable">
      <code>
       number
      </code>
     </em>
     →
     <code>
      <em class="replaceable">
       <code>
        boolean
       </code>
      </em>
     </code>
    </p>
    <p>
     Superior a
    </p>
    <p>
     <code>
      5 &gt; 4
     </code>
     →
     <code>
      TRUE
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <em class="replaceable">
      <code>
       number
      </code>
     </em>
     <code>
      &gt;=
     </code>
     <em class="replaceable">
      <code>
       number
      </code>
     </em>
     →
     <code>
      <em class="replaceable">
       <code>
        boolean
       </code>
      </em>
     </code>
    </p>
    <p>
     Maior que ou igual a
    </p>
    <p>
     <code>
      5 &gt;= 4
     </code>
     →
     <code>
      TRUE
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <em class="replaceable">
      <code>
       integer
      </code>
     </em>
     <code>
      |
     </code>
     <em class="replaceable">
      <code>
       integer
      </code>
     </em>
     →
     <code>
      <em class="replaceable">
       <code>
        integer
       </code>
      </em>
     </code>
    </p>
    <p>
     XOR (Bitwise OU)
    </p>
    <p>
     <code>
      1 | 2
     </code>
     →
     <code>
      3
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <em class="replaceable">
      <code>
       integer
      </code>
     </em>
     <code>
      #
     </code>
     <em class="replaceable">
      <code>
       integer
      </code>
     </em>
     →
     <code>
      <em class="replaceable">
       <code>
        integer
       </code>
      </em>
     </code>
    </p>
    <p>
     XOR bit a bit
    </p>
    <p>
     <code>
      1 # 3
     </code>
     →
     <code>
      2
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <em class="replaceable">
      <code>
       integer
      </code>
     </em>
     <code>
      &amp;
     </code>
     <em class="replaceable">
      <code>
       integer
      </code>
     </em>
     →
     <code>
      <em class="replaceable">
       <code>
        integer
       </code>
      </em>
     </code>
    </p>
    <p>
     E AND bit a bit
    </p>
    <p>
     <code>
      1 &amp; 3
     </code>
     →
     <code>
      1
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      ~
     </code>
     <em class="replaceable">
      <code>
       integer
      </code>
     </em>
     →
     <code>
      <em class="replaceable">
       <code>
        integer
       </code>
      </em>
     </code>
    </p>
    <p>
     Bitwise NOT
    </p>
    <p>
     <code>
      ~ 1
     </code>
     →
     <code>
      -2
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <em class="replaceable">
      <code>
       integer
      </code>
     </em>
     <code>
      &lt;&lt;
     </code>
     <em class="replaceable">
      <code>
       integer
      </code>
     </em>
     →
     <code>
      <em class="replaceable">
       <code>
        integer
       </code>
      </em>
     </code>
    </p>
    <p>
     Deslocamento à esquerda bit a bit
    </p>
    <p>
     <code>
      1 &lt;&lt; 2
     </code>
     →
     <code>
      4
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <em class="replaceable">
      <code>
       integer
      </code>
     </em>
     <code>
      &gt;&gt;
     </code>
     <em class="replaceable">
      <code>
       integer
      </code>
     </em>
     →
     <code>
      <em class="replaceable">
       <code>
        integer
       </code>
      </em>
     </code>
    </p>
    <p>
     Deslocamento à direita bit a bit
    </p>
    <p>
     <code>
      8 &gt;&gt; 2
     </code>
     →
     <code>
      2
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <em class="replaceable">
      <code>
       number
      </code>
     </em>
     <code>
      +
     </code>
     <em class="replaceable">
      <code>
       number
      </code>
     </em>
     →
     <code>
      <em class="replaceable">
       <code>
        number
       </code>
      </em>
     </code>
    </p>
    <p>
     Adição
    </p>
    <p>
     <code>
      5 + 4
     </code>
     →
     <code>
      9
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <em class="replaceable">
      <code>
       number
      </code>
     </em>
     <code>
      -
     </code>
     <em class="replaceable">
      <code>
       number
      </code>
     </em>
     →
     <code>
      <em class="replaceable">
       <code>
        number
       </code>
      </em>
     </code>
    </p>
    <p>
     Subtração
    </p>
    <p>
     <code>
      3 - 2.0
     </code>
     →
     <code>
      1.0
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <em class="replaceable">
      <code>
       number
      </code>
     </em>
     <code>
      *
     </code>
     <em class="replaceable">
      <code>
       number
      </code>
     </em>
     →
     <code>
      <em class="replaceable">
       <code>
        number
       </code>
      </em>
     </code>
    </p>
    <p>
     Multiplicação
    </p>
    <p>
     <code>
      5 * 4
     </code>
     →
     <code>
      20
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <em class="replaceable">
      <code>
       number
      </code>
     </em>
     <code>
      /
     </code>
     <em class="replaceable">
      <code>
       number
      </code>
     </em>
     →
     <code>
      <em class="replaceable">
       <code>
        number
       </code>
      </em>
     </code>
    </p>
    <p>
     Divisão (truncando o resultado para zero se ambos os inputs forem inteiros)
    </p>
    <p>
     <code>
      5 / 3
     </code>
     →
     <code>
      1
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <em class="replaceable">
      <code>
       integer
      </code>
     </em>
     <code>
      %
     </code>
     <em class="replaceable">
      <code>
       integer
      </code>
     </em>
     →
     <code>
      <em class="replaceable">
       <code>
        integer
       </code>
      </em>
     </code>
    </p>
    <p>
     Modulo (resto)
    </p>
    <p>
     <code>
      3 % 2
     </code>
     →
     <code>
      1
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      -
     </code>
     <em class="replaceable">
      <code>
       number
      </code>
     </em>
     →
     <code>
      <em class="replaceable">
       <code>
        number
       </code>
      </em>
     </code>
    </p>
    <p>
     Negação
    </p>
    <p>
     <code>
      - 2.0
     </code>
     →
     <code>
      -2.0
     </code>
    </p>
   </td>
  </tr>
 </tbody>
</table>







### Funções embutidas

As funções listadas na [Tabela 303](pgbench.md#PGBENCH-FUNCTIONS) são incorporadas ao pgbench e podem ser usadas em expressões que aparecem em [[`\set`](pgbench.md#PGBENCH-METACOMMAND-SET)].

**Tabela 303. Funções pgbench**



<table>
 <colgroup>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th class="func_table_entry">
    <p class="func_signature">
     Função
    </p>
    <p>
     Descrição
    </p>
    <p>
     Exemplo(s)
    </p>
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      abs
     </code>
     (
     <em class="replaceable">
      <code>
       number
      </code>
     </em>
     )
     <code>
     </code>
     mesmo tipo que a entrada
    </p>
    <p>
     Valor absoluto
    </p>
    <p>
     <code>
      abs(-17)
     </code>
     →
     <code>
      17
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      debug
     </code>
     (
     <em class="replaceable">
      <code>
       number
      </code>
     </em>
     )
     <code>
     </code>
     mesmo tipo que a entrada
    </p>
    <p>
     Imprime o argumento para
     <span class="systemitem">
      stderr
     </span>
     , e retorna o argumento.
    </p>
    <p>
     <code>
      debug(5432.1)
     </code>
     →
     <code>
      5432.1
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      double
     </code>
     (
     <em class="replaceable">
      <code>
       number
      </code>
     </em>
     )
     <code>
      double
     </code>
    </p>
    <p>
     Jogos para duplicar.
    </p>
    <p>
     <code>
      double(5432)
     </code>
     →
     <code>
      5432.0
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      exp
     </code>
     (
     <em class="replaceable">
      <code>
       number
      </code>
     </em>
     )
     <code>
      double
     </code>
    </p>
    <p>
     Explicativa (
     <code>
      e
     </code>
     elevado à potência dada)
    </p>
    <p>
     <code>
      exp(1.0)
     </code>
     →
     <code>
      2.718281828459045
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      greatest
     </code>
     (
     <em class="replaceable">
      <code>
       number
      </code>
     </em>
     [
     <span class="optional">
      ,
      <code>
       ...
      </code>
     </span>
     ] )
     <code>
     </code>
     <code>
      double
     </code>
     se algum argumento for duplo, senão
     <code>
      integer
     </code>
    </p>
    <p>
     Seleciona o maior valor entre os argumentos.
    </p>
    <p>
     <code>
      greatest(5, 4, 3, 2)
     </code>
     →
     <code>
      5
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      hash
     </code>
     (
     <em class="parameter">
      <code>
       value
      </code>
     </em>
     [
     <span class="optional">
      ,
      <em class="parameter">
       <code>
        seed
       </code>
      </em>
     </span>
     ] )
     <code>
      integer
     </code>
    </p>
    <p>
     Este é um alias para
     <code>
      hash_murmur2
     </code>
     .
    </p>
    <p>
     <code>
      hash(10, 5432)
     </code>
     →
     <code>
      -5817877081768721676
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      hash_fnv1a
     </code>
     (
     <em class="parameter">
      <code>
       value
      </code>
     </em>
     [
     <span class="optional">
      ,
      <em class="parameter">
       <code>
        seed
       </code>
      </em>
     </span>
     ] )
     <code>
      integer
     </code>
    </p>
    <p>
     Calcula
     <a class="ulink" href="https://en.wikipedia.org/wiki/Fowler%E2%80%93Noll%E2%80%93Vo_hash_function" target="_top">
      Hash FNV-1a
     </a>
     .
    </p>
    <p>
     <code>
      hash_fnv1a(10, 5432)
     </code>
     →
     <code>
      -7793829335365542153
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      hash_murmur2
     </code>
     (
     <em class="parameter">
      <code>
       value
      </code>
     </em>
     [
     <span class="optional">
      ,
      <em class="parameter">
       <code>
        seed
       </code>
      </em>
     </span>
     ] )
     <code>
      integer
     </code>
    </p>
    <p>
     Calcula
     <a class="ulink" href="https://en.wikipedia.org/wiki/MurmurHash" target="_top">
      MurmurHash2 hash
     </a>
     .
    </p>
    <p>
     <code>
      hash_murmur2(10, 5432)
     </code>
     →
     <code>
      -5817877081768721676
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      int
     </code>
     (
     <em class="replaceable">
      <code>
       number
      </code>
     </em>
     )
     <code>
      integer
     </code>
    </p>
    <p>
     Arranjos para inteiro.
    </p>
    <p>
     <code>
      int(5.4 + 3.8)
     </code>
     →
     <code>
      9
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      least
     </code>
     (
     <em class="replaceable">
      <code>
       number
      </code>
     </em>
     [
     <span class="optional">
      ,
      <code>
       ...
      </code>
     </span>
     ] )
     <code>
     </code>
     <code>
      double
     </code>
     se algum argumento for duplo, senão
     <code>
      integer
     </code>
    </p>
    <p>
     Seleciona o menor valor entre os argumentos.
    </p>
    <p>
     <code>
      least(5, 4, 3, 2.1)
     </code>
     →
     <code>
      2.1
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      ln
     </code>
     (
     <em class="replaceable">
      <code>
       number
      </code>
     </em>
     )
     <code>
      double
     </code>
    </p>
    <p>
     Logarítmico natural
    </p>
    <p>
     <code>
      ln(2.718281828459045)
     </code>
     →
     <code>
      1.0
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      mod
     </code>
     (
     <em class="replaceable">
      <code>
       integer
      </code>
     </em>
     ,
     <em class="replaceable">
      <code>
       integer
      </code>
     </em>
     )
     <code>
      integer
     </code>
    </p>
    <p>
     Modulo (resto)
    </p>
    <p>
     <code>
      mod(54, 32)
     </code>
     →
     <code>
      22
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      permute
     </code>
     (
     <em class="parameter">
      <code>
       i
      </code>
     </em>
     ,
     <em class="parameter">
      <code>
       size
      </code>
     </em>
     [,
     <em class="parameter">
      <code>
       seed
      </code>
     </em>
     ] )
     <code>
      integer
     </code>
    </p>
    <p>
     Valor permutado de
     <em class="parameter">
      <code>
       i
      </code>
     </em>
     , na faixa
     <code>
      [0, size)
     </code>
     . Esta é a nova posição de
     <em class="parameter">
      <code>
       i
      </code>
     </em>
     (modulo
     <em class="parameter">
      <code>
       size
      </code>
     </em>
     ) em uma permutação pseudorandom de inteiros
     <code>
      0...size-1
     </code>
     , parametrizado por
     <em class="parameter">
      <code>
       seed
      </code>
     </em>
     , veja abaixo.
    </p>
    <p>
     <code>
      permute(0, 4)
     </code>
     →
     <code>
      an integer between 0 and 3
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pi
     </code>
     ()
     <code>
      double
     </code>
    </p>
    <p>
     Valor aproximado de
     <span class="symbol_font">
      π
     </span>
    </p>
    <p>
     <code>
      pi()
     </code>
     →
     <code>
      3.14159265358979323846
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      pow
     </code>
     (
     <em class="parameter">
      <code>
       x
      </code>
     </em>
     ,
     <em class="parameter">
      <code>
       y
      </code>
     </em>
     )
     <code>
      double
     </code>
    </p>
    <p class="func_signature">
     <code>
      power
     </code>
     (
     <em class="parameter">
      <code>
       x
      </code>
     </em>
     ,
     <em class="parameter">
      <code>
       y
      </code>
     </em>
     )
     <code>
      double
     </code>
    </p>
    <p>
     <em class="parameter">
      <code>
       x
      </code>
     </em>
     elevado à potência de
     <em class="parameter">
      <code>
       y
      </code>
     </em>
    </p>
    <p>
     <code>
      pow(2.0, 10)
     </code>
     →
     <code>
      1024.0
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      random
     </code>
     (
     <em class="parameter">
      <code>
       lb
      </code>
     </em>
     ,
     <em class="parameter">
      <code>
       ub
      </code>
     </em>
     )
     <code>
      integer
     </code>
    </p>
    <p>
     Calcula um número inteiro aleatório distribuído uniformemente em
     <code>
      [lb, ub]
     </code>
     .
    </p>
    <p>
     <code>
      random(1, 10)
     </code>
     →
     <code>
      an integer between 1 and 10
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      random_exponential
     </code>
     (
     <em class="parameter">
      <code>
       lb
      </code>
     </em>
     ,
     <em class="parameter">
      <code>
       ub
      </code>
     </em>
     ,
     <em class="parameter">
      <code>
       parameter
      </code>
     </em>
     )
     <code>
      integer
     </code>
    </p>
    <p>
     Calcula um número inteiro aleatório distribuído exponencialmente
     <code>
      [lb, ub]
     </code>
     , veja abaixo.
    </p>
    <p>
     <code>
      random_exponential(1, 10, 3.0)
     </code>
     →
     <code>
      an integer between 1 and 10
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      random_gaussian
     </code>
     (
     <em class="parameter">
      <code>
       lb
      </code>
     </em>
     ,
     <em class="parameter">
      <code>
       ub
      </code>
     </em>
     ,
     <em class="parameter">
      <code>
       parameter
      </code>
     </em>
     )
     <code>
      integer
     </code>
    </p>
    <p>
     Calcula um número inteiro aleatório distribuído de forma gaussiana
     <code>
      [lb, ub]
     </code>
     , veja abaixo.
    </p>
    <p>
     <code>
      random_gaussian(1, 10, 2.5)
     </code>
     →
     <code>
      an integer between 1 and 10
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      random_zipfian
     </code>
     (
     <em class="parameter">
      <code>
       lb
      </code>
     </em>
     ,
     <em class="parameter">
      <code>
       ub
      </code>
     </em>
     ,
     <em class="parameter">
      <code>
       parameter
      </code>
     </em>
     )
     <code>
      integer
     </code>
    </p>
    <p>
     Calcula um número inteiro aleatório distribuído de acordo com a Zipf,
     <code>
      [lb, ub]
     </code>
     , veja abaixo.
    </p>
    <p>
     <code>
      random_zipfian(1, 10, 1.5)
     </code>
     →
     <code>
      an integer between 1 and 10
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      sqrt
     </code>
     (
     <em class="replaceable">
      <code>
       number
      </code>
     </em>
     )
     <code>
      double
     </code>
    </p>
    <p>
     raiz quadrada
    </p>
    <p>
     <code>
      sqrt(2.0)
     </code>
     →
     <code>
      1.414213562
     </code>
    </p>
   </td>
  </tr>
 </tbody>
</table>










A função `random` gera valores usando uma distribuição uniforme, ou seja, todos os valores são extraídos dentro do intervalo especificado com probabilidade igual. As funções `random_exponential`, `random_gaussian` e `random_zipfian` requerem um parâmetro duplo adicional que determina a forma precisa da distribuição.

* Para uma distribuição exponencial, *`parameter`* controla a distribuição truncando uma distribuição exponencial que diminui rapidamente em *`parameter`*, e depois projetando-a em inteiros entre os limites. Para ser preciso, com

f(x) = exp(-parâmetro * (x - min) / (max - min + 1)) / (1 - exp(-parâmetro))

Então o valor *`i`* entre *`min`* e *`max`* inclusive é traçado com probabilidade de: `f(i) - f(i + 1)`.

Intuitivamente, quanto maior o *`parameter`*, mais frequentemente valores próximos a *`min`* são acessados, e menos frequentemente valores próximos a *`max`* são acessados. Quanto mais próximo de 0 *`parameter`* estiver, mais plana (mais uniforme) será a distribuição de acesso. Uma aproximação grosseira da distribuição é que os valores mais frequentes no intervalo, próximos a *`min`*, são drawn *`parameter`% das vezes. O valor de *`parameter`* deve ser estritamente positivo.
* Para uma distribuição gaussiana, o intervalo é mapeado para uma distribuição normal padrão (a curva gaussiana clássica em forma de sino) truncada em `-parameter` à esquerda e `+parameter` à direita. Valores no meio do intervalo têm mais probabilidade de serem drawn. Para ser preciso, se `PHI(x)` é a função de distribuição cumulativa da distribuição normal padrão, com média `mu` definida como `(max + min) / 2.0`, com *

f(x) = PHI(2,0 * parâmetro * (x - μ) / (max - min + 1)) / (2,0 * PHI(parâmetro) - 1)

O valor *`i`* entre *`min`* e *`max`* inclusive é extraído com probabilidade de: *`f(i + 0.5) - f(i - 0.5)`. Intuitivamente, quanto maior o *`parameter`*, mais frequentemente valores próximos ao meio do intervalo são extraídos, e menos frequentemente valores próximos aos limites *`min`* e *`max`*. Aproximadamente 67% dos valores são extraídos do meio *`1.0 / parameter`, ou seja, um relativo *`0.5 / parameter` em torno da média, e 95% no meio *`2.0 / parameter`, ou seja, um relativo *`1.0 / parameter` em torno da média; por exemplo, se *`parameter`* é 4,0, 67% dos valores são extraídos do quarto médio (1,0 / 4,0) do intervalo (ou seja, de *`3.0 / 8.0` a *`5.0 / 8.0`) e 95% da metade meio *`2.0 / 4.0` do intervalo (segundo e terceiro quartis). O valor mínimo permitido de *`parameter`* é 2,0.
* `random_zipfian` gera uma distribuição Zipfiana limitada. *`parameter` define como enviesada a distribuição. Quanto maior o *`parameter`*, mais frequentemente valores próximos ao início do intervalo são extraídos. A distribuição é tal que, assumindo que a faixa começa em 1, a razão da probabilidade de extrair *`k`* em comparação com extrair *`k+1`* é *`((k+1)/k)**parameter`. Por exemplo, *`random_zipfian(1, ..., 2.5)` produz o valor *`1` aproximadamente *`(2/1)**2.5 = 5.66` vezes mais frequente do que *`2`, que por sua vez é produzido *`(3/2)**2.5 = 2.76` vezes mais frequente do que *`3`, e assim por diante.

A implementação do pgbench é baseada na "Geração de Variáveis Aleatórias Não Uniformes", Luc Devroye, p. 550-551, Springer 1986. Devido às limitações desse algoritmo, o valor *`parameter`* é restrito ao intervalo [1,001, 1000].

Nota

Ao projetar um benchmark que seleciona linhas de forma não uniforme, esteja ciente de que as linhas escolhidas podem estar correlacionadas com outros dados, como IDs de uma sequência ou a ordem física das linhas, o que pode distorcer as medições de desempenho.

Para evitar isso, você pode querer usar a função `permute` ou algum outro passo adicional com efeito semelhante, para embaralhar as linhas selecionadas e remover tais correlações.

As funções de hash `hash`, `hash_murmur2` e `hash_fnv1a` aceitam um valor de entrada e um parâmetro de semente opcional. Caso a semente não seja fornecida, o valor de `:default_seed` é usado, que é inicializado aleatoriamente, a menos que seja definido pela opção de linha de comando `-D`.

`permute` aceita um valor de entrada, um tamanho e um parâmetro opcional seed. Ele gera uma permutação pseudorandom de inteiros no intervalo `[0, size)`, e retorna o índice do valor de entrada nos valores permutados. A permutação escolhida é parametrizada pelo seed, que é padrão em `:default_seed`, se não for especificado. Ao contrário das funções de hash, `permute` garante que não haja colisões ou lacunas nos valores de saída. Os valores de entrada fora do intervalo são interpretados módulo o tamanho. A função gera um erro se o tamanho não for positivo. `permute` pode ser usado para espalhar a distribuição de funções aleatórias não uniformes, como `random_zipfian` ou `random_exponential` para que os valores tirados com mais frequência não estejam trivialmente correlacionados. Por exemplo, o seguinte script pgbench simula um possível trabalho real típico de plataformas de mídia social e blog, onde algumas contas geram carga excessiva:

```
\set size 1000000 \set r random_zipfian(1, :size, 1.07) \set k 1 + permute(:r, :size)
```

Em alguns casos, são necessárias várias distribuições distintas que não se correlacionam entre si, e é aí que o parâmetro de semente opcional se torna útil:

```
\set k1 1 + permute(:r, :size, :default_seed + 123) \set k2 1 + permute(:r, :size, :default_seed + 321)
```

Um comportamento semelhante também pode ser aproximado com `hash`:

```
\set size 1000000 \set r random_zipfian(1, 100 * :size, 1.07) \set k 1 + abs(hash(:r)) % :size
```

No entanto, uma vez que `hash` gera colisões, alguns valores não serão acessíveis e outros serão mais frequentes do que o esperado a partir da distribuição original.

Como exemplo, a definição completa da transação embutida semelhante ao TPC-B é:

```
\set aid random(1, 100000 * :scale) \set bid random(1, 1 * :scale) \set tid random(1, 10 * :scale) \set delta random(-5000, 5000) BEGIN; UPDATE pgbench_accounts SET abalance = abalance + :delta WHERE aid = :aid; SELECT abalance FROM pgbench_accounts WHERE aid = :aid; UPDATE pgbench_tellers SET tbalance = tbalance + :delta WHERE tid = :tid; UPDATE pgbench_branches SET bbalance = bbalance + :delta WHERE bid = :bid; INSERT INTO pgbench_history (tid, bid, aid, delta, mtime) VALUES (:tid, :bid, :aid, :delta, CURRENT_TIMESTAMP); END;
```

Este script permite que cada iteração da transação faça referência a linhas diferentes, escolhidas aleatoriamente. (Este exemplo também mostra por que é importante que cada sessão do cliente tenha suas próprias variáveis — caso contrário, elas não estariam tocando independentemente em diferentes linhas.)

### Registro por Transação

Com a opção `-l` (mas sem a opção `--aggregate-interval`), pgbench escreve informações sobre cada transação em um arquivo de registro. O arquivo de registro será nomeado `prefix.nnn`, onde *`prefix`* por padrão será `pgbench_log`, e *`nnn`* é o PID do pgbench. O prefixo pode ser alterado usando a opção `--log-prefix`. Se a opção `-j` for 2 ou superior, de modo que haja vários threads de trabalhador, cada um terá seu próprio arquivo de registro. O primeiro trabalhador usará o mesmo nome para seu arquivo de registro que no caso padrão de um trabalhador único. Os arquivos de registro adicionais para os outros trabalhadores serão nomeados `prefix.nnn.mmm`, onde *`mmm`* é um número sequencial para cada trabalhador começando com 1.

Cada linha em um arquivo de registro descreve uma transação. Ele contém os seguintes campos separados por espaço:

*`client_id`*   identifica a sessão do cliente que executou a transação

*`transaction_no`*   conta quantas transações foram realizadas por aquela sessão

*`time`* *tempo transcorrido da transação, em microsegundos

*`script_no`*   identifica o arquivo de script que foi utilizado para a transação (útil quando vários scripts são especificados com `-f` ou `-b`)

*`time_epoch`*  *tempo de conclusão da transação, como um rótulo de data e hora em Unix*

*`time_us`*: fração — parte da segunda parte do tempo de conclusão da transação, em microsegundos

*`schedule_lag`*: delay do início da transação, ou seja, a diferença entre o horário de início programado da transação e o horário em que ela realmente começou, em microsegundos (apenas presente se `--rate` for especificado)

*`retries`*: número de tentativas após erros de serialização ou bloqueio durante a transação (apresentado apenas se `--max-tries` não for igual a um)

Quando ambos os `--rate` e `--latency-limit` são utilizados, o *`time`* para uma transação ignorada será relatado como `skipped`. Se a transação terminar com um erro, seu *`time`* será relatado como `failed`. Se você usar a `--failures-detailed` opção, o *`time`* da transação falha será relatado como `serialization` ou `deadlock` dependendo do tipo de falha (consulte [Falhas e Serialização/Reintentos de Engano](pgbench.md#FAILURES-AND-RETRIES "Failures and Serialization/Deadlock Retries") para mais informações).

Aqui está um trecho de um arquivo de registro gerado em uma execução com um único cliente:

```
0 199 2241 0 1175850568 995598 0 200 2465 0 1175850568 998079 0 201 2513 0 1175850569 608 0 202 2038 0 1175850569 2663
```

Outro exemplo com `--rate=100` e `--latency-limit=5` (note a coluna adicional *`schedule_lag`*):

```
0 81 4621 0 1412881037 912698 3005 0 82 6173 0 1412881037 914578 4304 0 83 skipped 0 1412881037 914578 5217 0 83 skipped 0 1412881037 914578 5099 0 83 4722 0 1412881037 916203 3108 0 84 4142 0 1412881037 918023 2333 0 85 2465 0 1412881037 919759 740
```

Neste exemplo, a transação 82 foi atrasada, porque sua latência (6.173 ms) estava acima do limite de 5 ms. As duas transações seguintes foram ignoradas, porque já estavam atrasadas antes mesmo de serem iniciadas.

O exemplo a seguir mostra um trecho de um arquivo de registro com falhas e tentativas de recuperação, com o número máximo de tentativas definido em 10 (note a coluna adicional *`retries`*):

```
3 0 47423 0 1499414498 34501 3 3 1 8333 0 1499414498 42848 0 3 2 8358 0 1499414498 51219 0 4 0 72345 0 1499414498 59433 6 1 3 41718 0 1499414498 67879 4 1 4 8416 0 1499414498 76311 0 3 3 33235 0 1499414498 84469 3 0 0 failed 0 1499414498 84905 9 2 0 failed 0 1499414498 86248 9 3 4 8307 0 1499414498 92788 0
```

Se a opção `--failures-detailed` for usada, o tipo de falha é relatado no *`time`* da seguinte forma:

```
3 0 47423 0 1499414498 34501 3 3 1 8333 0 1499414498 42848 0 3 2 8358 0 1499414498 51219 0 4 0 72345 0 1499414498 59433 6 1 3 41718 0 1499414498 67879 4 1 4 8416 0 1499414498 76311 0 3 3 33235 0 1499414498 84469 3 0 0 serialization 0 1499414498 84905 9 2 0 serialization 0 1499414498 86248 9 3 4 8307 0 1499414498 92788 0
```

Ao executar um teste longo em um hardware que pode lidar com muitas transações, os arquivos de registro podem se tornar muito grandes. A opção `--sampling-rate` pode ser usada para registrar apenas uma amostra aleatória de transações.

### Registro Agregado

Com a opção `--aggregate-interval`, um formato diferente é usado para os arquivos de registro. Cada linha de registro descreve um intervalo de agregação. Ela contém os seguintes campos separados por espaço:

*`interval_start`*  *hora de início do intervalo, como um rótulo de marcação de tempo em época Unix

*`num_transactions`*   número de transações dentro do intervalo

*`sum_latency`*: soma das latências das transações

*`sum_latency_2`*: soma dos quadrados das latências das transações

*`min_latency`*: latência mínima da transação

*`max_latency`*: latência máxima da transação

*`sum_lag`*: soma dos atrasos no início da transação (zero, a menos que `--rate` seja especificado)

*`sum_lag_2`*: soma dos quadrados dos atrasos no início da transação (zero, a menos que `--rate` seja especificado)

*`min_lag`*: delay mínimo para início da transação (zero, a menos que `--rate` seja especificado)

*`max_lag`*: delay máximo de início da transação (zero, a menos que `--rate` seja especificado)

*`skipped`*: número de transações ignoradas porque teriam começado muito tarde (zero a menos que `--rate` e `--latency-limit` sejam especificados)

*`retried`*: número de transações repetidas (zero, a menos que `--max-tries` não seja igual a um)

*`retries`*: número de tentativas após erros de serialização ou bloqueio (zero, a menos que `--max-tries` não seja igual a um)

*`serialization_failures`*: número de transações que tiveram um erro de serialização e não foram repostas posteriormente (zero, a menos que `--failures-detailed` seja especificado)

*`deadlock_failures`*: número de transações que obtiveram um erro de deadlock e não foram repostas posteriormente (zero, a menos que `--failures-detailed` seja especificado)

Aqui está uma saída de exemplo gerada com essa opção:

```
pgbench --aggregate-interval=10 --time=20 --client=10 --log --rate=1000 --latency-limit=10 --failures-detailed --max-tries=10 test

1650260552 5178 26171317 177284491527 1136 44462 2647617 7321113867 0 9866 64 7564 28340 4148 0 1650260562 4808 25573984 220121792172 1171 62083 3037380 9666800914 0 9998 598 7392 26621 4527 0
```

Observe que, embora o formato de registro simples (não agregada) mostre qual script foi usado para cada transação, o formato agregado não o faz. Portanto, se você precisa de dados por script, você precisa agregar os dados por conta própria.

### Relatório por Pedido de Pagamento

Com a opção `-r`, o pgbench coleta as seguintes estatísticas para cada declaração:

* `latency` — tempo de transação concluído para cada declaração. O pgbench reporta um valor médio de todas as execuções bem-sucedidas da declaração.
* O número de falhas nesta declaração. Consulte [Falhas e Repetições de Serialização/Retritos de Engano de Conquista](pgbench.md#FAILURES-AND-RETRIES "Failures and Serialization/Deadlock Retries") para mais informações.
* O número de repetições após um erro de serialização ou de bloqueio de acesso nesta declaração. Consulte [Falhas e Repetições de Serialização/Retritos de Engano de Conquista](pgbench.md#FAILURES-AND-RETRIES "Failures and Serialization/Deadlock Retries") para mais informações.

O relatório exibe as estatísticas de tentativa de recuperação apenas se a opção `--max-tries` não for igual a 1.

Todos os valores são calculados para cada declaração executada por cada cliente e são relatados após o benchmark ter terminado.

Para o script padrão, a saída será semelhante a esta:

```
starting vacuum...end. transaction type: <builtin: TPC-B (sort of)> scaling factor: 1 query mode: simple number of clients: 10 number of threads: 1 maximum number of tries: 1 number of transactions per client: 1000 number of transactions actually processed: 10000/10000 number of failed transactions: 0 (0.000%) number of transactions above the 50.0 ms latency limit: 1311/10000 (13.110 %) latency average = 28.488 ms latency stddev = 21.009 ms initial connection time = 69.068 ms tps = 346.224794 (without initial connection time) statement latencies in milliseconds and failures: 0.012  0  \set aid random(1, 100000 * :scale) 0.002  0  \set bid random(1, 1 * :scale) 0.002  0  \set tid random(1, 10 * :scale) 0.002  0  \set delta random(-5000, 5000) 0.319  0  BEGIN; 0.834  0  UPDATE pgbench_accounts SET abalance = abalance + :delta WHERE aid = :aid; 0.641  0  SELECT abalance FROM pgbench_accounts WHERE aid = :aid; 11.126  0  UPDATE pgbench_tellers SET tbalance = tbalance + :delta WHERE tid = :tid; 12.961  0  UPDATE pgbench_branches SET bbalance = bbalance + :delta WHERE bid = :bid; 0.634  0  INSERT INTO pgbench_history (tid, bid, aid, delta, mtime) VALUES (:tid, :bid, :aid, :delta, CURRENT_TIMESTAMP); 1.957  0  END;
```

Outro exemplo de saída para o script padrão usando o nível de isolamento de transação padrão serializável (`PGOPTIONS='-c default_transaction_isolation=serializable' pgbench ...`):

```
starting vacuum...end. transaction type: <builtin: TPC-B (sort of)> scaling factor: 1 query mode: simple number of clients: 10 number of threads: 1 maximum number of tries: 10 number of transactions per client: 1000 number of transactions actually processed: 6317/10000 number of failed transactions: 3683 (36.830%) number of transactions retried: 7667 (76.670%) total number of retries: 45339 number of transactions above the 50.0 ms latency limit: 106/6317 (1.678 %) latency average = 17.016 ms latency stddev = 13.283 ms initial connection time = 45.017 ms tps = 186.792667 (without initial connection time) statement latencies in milliseconds, failures and retries: 0.006     0      0  \set aid random(1, 100000 * :scale) 0.001     0      0  \set bid random(1, 1 * :scale) 0.001     0      0  \set tid random(1, 10 * :scale) 0.001     0      0  \set delta random(-5000, 5000) 0.385     0      0  BEGIN; 0.773     0      1  UPDATE pgbench_accounts SET abalance = abalance + :delta WHERE aid = :aid; 0.624     0      0  SELECT abalance FROM pgbench_accounts WHERE aid = :aid; 1.098   320   3762  UPDATE pgbench_tellers SET tbalance = tbalance + :delta WHERE tid = :tid; 0.582  3363  41576  UPDATE pgbench_branches SET bbalance = bbalance + :delta WHERE bid = :bid; 0.465     0      0  INSERT INTO pgbench_history (tid, bid, aid, delta, mtime) VALUES (:tid, :bid, :aid, :delta, CURRENT_TIMESTAMP); 1.933     0      0  END;
```

Se vários arquivos de script forem especificados, todas as estatísticas serão relatadas separadamente para cada arquivo de script.

Observe que a coleta das informações de tempo adicionais necessárias para o cálculo da latência por declaração adiciona algum custo. Isso diminuirá a velocidade de execução média e reduzirá o TPS calculado. A quantidade de redução de velocidade varia significativamente dependendo da plataforma e do hardware. Comparar os valores de TPS médios com e sem o relatório de latência ativado é uma boa maneira de medir se o custo de tempo é significativo.

### Falhas e Retrias de Serialização/Bloqueio em Série

Ao executar o pgbench, existem três tipos principais de erros:

* Erros do programa principal. Eles são os mais graves e sempre resultam em uma saída imediata do pgbench com a mensagem de erro correspondente. Eles incluem:

+ erros no início do pgbench (por exemplo, um valor de opção inválido);
+ erros no modo de inicialização (por exemplo, a consulta para criar tabelas para scripts embutidos falha);
+ erros antes de iniciar os threads (por exemplo, não conseguiu se conectar ao servidor de banco de dados, erro de sintaxe no comando meta, falha na criação de threads);
+ erros internos do pgbench (que supostamente nunca ocorrem...).
* Erros quando o thread gerencia seus clientes (por exemplo, o cliente não conseguiu iniciar uma conexão com o servidor de banco de dados / o socket para conectar o cliente ao servidor de banco de dados se tornou inválido). Nesses casos, todos os clientes deste thread param enquanto outros threads continuam a funcionar. No entanto, `--exit-on-abort` é especificado, todos os threads param imediatamente neste caso.
* Erros diretos do cliente. Levam à saída imediata do pgbench com a mensagem de erro correspondente no caso de um erro interno do pgbench (que supostamente nunca ocorrem...) ou quando `--exit-on-abort` é especificado. Caso contrário, no pior dos casos, apenas levam ao aborto do cliente falhado enquanto outros clientes continuam sua execução (mas alguns erros de cliente são tratados sem aborto do cliente e relatados separadamente, veja abaixo). Mais tarde, nesta seção, assume-se que os erros discutidos são apenas os erros diretos do cliente e não são erros internos do pgbench.

O rodízio de um cliente é interrompido em caso de um erro grave; por exemplo, a conexão com o servidor de banco de dados foi perdida ou o fim do script foi alcançado sem completar a última transação. Além disso, se a execução de um comando SQL ou meta falhar por razões que não sejam erros de serialização ou bloqueio, o cliente é interrompido. Caso contrário, se um comando SQL falhar com erros de serialização ou bloqueio, o cliente não é interrompido. Nesses casos, a transação atual é revertida, o que também inclui a definição das variáveis do cliente como estavam antes do rodízio dessa transação (se assume-se que um script de transação contém apenas uma transação; consulte [O que é realmente realizado a "Transação" no pgbench?](pgbench.md#TRANSACTIONS-AND-SCRIPTS) para mais informações). As transações com erros de serialização ou bloqueio são repetidas após os recuos até que sejam concluídas com sucesso ou atinjam o número máximo de tentativas (especificado pela opção `--max-tries`)/o tempo máximo de tentativas (especificado pela opção `--latency-limit`)/o fim do benchmark (especificado pela opção `--time`). Se o último ensaio falhar, essa transação será relatada como falha, mas o cliente não é interrompido e continua a funcionar.

Nota

Sem especificar a opção `--max-tries`, uma transação nunca será retente após um erro de serialização ou bloqueio, porque seu valor padrão é 1. Use um número ilimitado de tentativas (`--max-tries=0`) e a opção `--latency-limit` para limitar apenas o tempo máximo de tentativas. Você também pode usar a opção `--time` para limitar a duração do benchmark sob um número ilimitado de tentativas.

Tenha cuidado ao repetir scripts que contenham várias transações: o script é sempre repetido completamente, então as transações bem-sucedidas podem ser realizadas várias vezes.

Tenha cuidado ao repetir transações com comandos de shell. Ao contrário dos resultados dos comandos SQL, os resultados dos comandos de shell não são revertidos, exceto pelo valor variável do comando `\setshell`.

A latência de uma transação bem-sucedida inclui todo o tempo de execução da transação com rollback e tentativas. A latência é medida apenas para transações e comandos bem-sucedidos, mas não para transações ou comandos falháveis.

O relatório principal contém o número de transações não concluídas. Se a opção `--max-tries` não for igual a 1, o relatório principal também contém estatísticas relacionadas aos retentes: o número total de transações repetidas e o número total de repetições. O relatório por script herda todos esses campos do relatório principal. O relatório por declaração exibe estatísticas de repetição apenas se a opção `--max-tries` não for igual a 1.

Se você deseja agrupar falhas por tipos básicos em logs de per-transação e agregados, bem como nos relatórios principais e por script, use a opção `--failures-detailed`. Se você também deseja distinguir todos os erros e falhas (erros sem tentativa de refazer) por tipo, incluindo qual limite para tentativas foi excedido e quanto foi excedido para as falhas de serialização/bloqueio, use a opção `--verbose-errors`.

### Métodos de Acesso à Tabela

Você pode especificar o [Método de Acesso à Tabela](tableam.md) para as tabelas do pgbench. A variável de ambiente `PGOPTIONS` especifica opções de configuração do banco de dados que são passadas ao PostgreSQL via linha de comando (Veja [Seção 19.1.4](config-setting.md#CONFIG-SETTING-SHELL)). Por exemplo, um método hipotético de Acesso à Tabela padrão para as tabelas que o pgbench cria chamado `wuzza` pode ser especificado com:

```
PGOPTIONS='-c default_table_access_method=wuzza'
```

### Boas Práticas

É muito fácil usar o pgbench para gerar números completamente sem sentido. Aqui estão algumas orientações para ajudá-lo a obter resultados úteis.

Em primeiro lugar, *nunca* acredite em qualquer teste que dure apenas alguns segundos. Use a opção `-t` ou `-T` para fazer a execução durar pelo menos alguns minutos, a fim de calcular a média do ruído. Em alguns casos, você pode precisar de horas para obter números que sejam reproduzíveis. É uma boa ideia tentar executar o teste algumas vezes, para descobrir se seus números são reproduzíveis ou

Para o cenário de teste padrão semelhante ao TPC-B, o fator de escala de inicialização (`-s`) deve ser pelo menos tão grande quanto o maior número de clientes que você pretende testar (`-c`); caso contrário, você estará medindo principalmente a concorrência de atualização. Existem apenas `-s` linhas na tabela `pgbench_branches`, e cada transação quer atualizar uma delas, então os valores de `-c` em excesso de `-s` resultarão, sem dúvida, em muitas transações bloqueadas esperando outras transações.

O cenário de teste padrão também é bastante sensível quanto ao tempo que se passou desde que as tabelas foram inicializadas: a acumulação de linhas mortas e espaço morto nas tabelas altera os resultados. Para entender os resultados, você deve acompanhar o número total de atualizações e quando o vacúmen ocorre. Se o autovacúmen estiver habilitado, pode resultar em mudanças imprevisíveis no desempenho medido.

Uma limitação do pgbench é que ele pode se tornar o gargalo quando se tenta testar um grande número de sessões de clientes. Isso pode ser aliviado ao executar o pgbench em uma máquina diferente do servidor de banco de dados, embora a baixa latência de rede seja essencial. Pode até ser útil executar várias instâncias do pgbench simultaneamente, em várias máquinas de clientes, contra o mesmo servidor de banco de dados.

### Segurança

Se usuários não confiáveis tiverem acesso a um banco de dados que não adotou um [esquema de uso seguro de esquema](ddl-schemas.md#DDL-SCHEMAS-PATTERNS), não execute o pgbench nesse banco de dados. O pgbench usa nomes não qualificados e não manipula o caminho de busca.