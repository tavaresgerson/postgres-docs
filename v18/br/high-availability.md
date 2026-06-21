## Capítulo 26. Alta disponibilidade, balanceamento de carga e replicação

**Índice**

* [26.1. Comparação de diferentes soluções](different-replication-solutions.md)
* [26.2. Servidores de espera de envio de logs](warm-standby.md)

+ [26.2.1. Planejamento](warm-standby.md#STANDBY-PLANNING)
+ [26.2.2. Operação de servidor em espera](warm-standby.md#STANDBY-SERVER-OPERATION)
+ [26.2.3. Preparação do primário para servidores em espera](warm-standby.md#PREPARING-PRIMARY-FOR-STANDBY)
+ [26.2.4. Configuração de um servidor em espera](warm-standby.md#STANDBY-SERVER-SETUP)
+ [26.2.5. Replicação em fluxo](warm-standby.md#STREAMING-REPLICATION)
+ [26.2.6. Fissuras de replicação](warm-standby.md#STREAMING-REPLICATION-SLOTS)
+ [26.2.7. Replicação em cascata](warm-standby.md#CASCADING-REPLICATION)
+ [26.2.8. Replicação síncrona](warm-standby.md#SYNCHRONOUS-REPLICATION)
+ [26.2.9. Arquivamento contínuo em espera](warm-standby.md#CONTINUOUS-ARCHIVING-IN-STANDBY)

* [26.3. Failover](warm-standby-failover.md)
* [26.4. Hot Standby](hot-standby.md)

+ [26.4.1. Visão Geral do Usuário](hot-standby.md#HOT-STANDBY-USERS)
+ [26.4.2. Tratamento de Conflitos de Consulta](hot-standby.md#HOT-STANDBY-CONFLICT)
+ [26.4.3. Visão Geral do Administrador](hot-standby.md#HOT-STANDBY-ADMIN)
+ [26.4.4. Referência do Parâmetro de Standby Quente](hot-standby.md#HOT-STANDBY-PARAMETERS)
+ [26.4.5. Observações](hot-standby.md#HOT-STANDBY-CAVEATS)

Os servidores de banco de dados podem trabalhar juntos para permitir que um segundo servidor assuma rapidamente se o servidor principal falhar (alta disponibilidade), ou para permitir que vários computadores sirvam os mesmos dados (balanceamento de carga). Idealmente, os servidores de banco de dados poderiam trabalhar juntos sem problemas. Servidores da web que servem páginas da web estáticas podem ser combinados facilmente, simplesmente balanceando as solicitações da web em várias máquinas. De fato, servidores de banco de dados que só podem ser lidos também podem ser combinados relativamente facilmente. Infelizmente, a maioria dos servidores de banco de dados tem uma mistura de solicitações de leitura/escrita, e servidores de leitura/escrita são muito mais difíceis de combinar. Isso ocorre porque, embora os dados que só podem ser lidos precisem ser colocados em cada servidor apenas uma vez, uma escrita em qualquer servidor precisa ser propagada para todos os servidores para que as solicitações de leitura futuras desses servidores retorne resultados consistentes.

Esse problema de sincronização é a dificuldade fundamental para servidores que trabalham juntos. Como não há uma única solução que elimine o impacto do problema de sincronização para todos os casos de uso, existem várias soluções. Cada solução aborda esse problema de uma maneira diferente e minimiza seu impacto para uma carga de trabalho específica.

Algumas soluções tratam a sincronização permitindo que apenas um servidor modifique os dados. Servidores que podem modificar dados são chamados de servidores de leitura/escrita, *mestre* ou *primárias*. Servidores que acompanham as mudanças no primário são chamados de *de standby* ou *secundários*. Um servidor de standby que não pode ser conectado até ser promovido a um servidor primário é chamado de servidor de *standby quente*, e aquele que pode aceitar conexões e atender consultas apenas de leitura é chamado de servidor de *standby quente*.

Algumas soluções são síncronas, o que significa que uma transação que modifica dados não é considerada comprometida até que todos os servidores tenham comprometido a transação. Isso garante que uma falha não perca nenhum dado e que todos os servidores balanceados de carga retornem resultados consistentes, independentemente de qual servidor seja consultado. Em contraste, as soluções assíncronas permitem algum atraso entre o momento de um compromisso e sua propagação para os outros servidores, abrindo a possibilidade de que algumas transações possam ser perdidas na mudança para um servidor de backup, e que servidores balanceados de carga possam retornar resultados ligeiramente desatualizados. A comunicação assíncrona é usada quando a sincrona seria muito lenta.

As soluções também podem ser categorizadas por sua granularidade. Algumas soluções podem lidar apenas com um servidor de banco de dados inteiro, enquanto outras permitem o controle no nível de tabela ou de banco de dados.

O desempenho deve ser considerado em qualquer escolha. Geralmente, há um compromisso entre funcionalidade e desempenho. Por exemplo, uma solução totalmente sincronizada em uma rede lenta pode reduzir o desempenho em mais de metade, enquanto uma solução assíncrona pode ter um impacto mínimo no desempenho.

O restante desta seção descreve várias soluções de falha, replicação e balanceamento de carga.