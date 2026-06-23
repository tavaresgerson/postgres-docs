## 26.1. Comparação de diferentes soluções [#](#DIFFERENT-REPLICATION-SOLUTIONS)

Failover de disco compartilhado: O failover de disco compartilhado evita o overhead de sincronização, pois possui apenas uma cópia do banco de dados. Ele utiliza um único array de disco que é compartilhado por vários servidores. Se o servidor principal do banco de dados falhar, o servidor de espera é capaz de montar e iniciar o banco de dados como se estivesse se recuperando de um acidente de banco de dados. Isso permite um failover rápido sem perda de dados.

A funcionalidade de hardware compartilhada é comum em dispositivos de armazenamento em rede. É também possível usar um sistema de arquivos de rede, embora se deva ter cuidado para que o sistema de arquivos tenha comportamento completo POSIX (ver [Seção 18.2.2.1](creating-cluster.md#CREATING-CLUSTER-NFS)). Uma limitação significativa desse método é que, se o array de disco compartilhado falhar ou se tornar corrompido, os servidores primário e de reserva também ficam inoperantes. Outro problema é que o servidor de reserva nunca deve acessar o armazenamento compartilhado enquanto o servidor primário estiver em funcionamento.

Replicação do Sistema de Arquivo (Dispositivo Bloco): Uma versão modificada da funcionalidade de hardware compartilhado é a replicação do sistema de arquivos, onde todas as alterações em um sistema de arquivos são espelhadas para um sistema de arquivos que reside em outro computador. A única restrição é que o espelhamento deve ser feito de uma maneira que garanta que o servidor de espera tenha uma cópia consistente do sistema de arquivos — especificamente, as escritas no standby devem ser feitas na mesma ordem que as do primário. O DRBD é uma solução popular de replicação de sistema de arquivos para Linux.

Envio de registro pré-escrita: Servidores de espera quentes e quentes podem ser mantidos atualizados lendo um fluxo de registros de registro pré-escrita (WAL). Se o servidor principal falhar, o standby contém quase todos os dados do servidor principal e pode ser rapidamente convertido no novo servidor de banco de dados primário. Isso pode ser sincronizado ou assíncrono e só pode ser feito para o servidor de banco de dados inteiro.

Um servidor de espera pode ser implementado usando o envio de registros baseado em arquivos (ver [Seção 26.2](warm-standby.md)) ou replicação por fluxo (ver [Seção 26.2.5](warm-standby.md#STREAMING-REPLICATION)), ou uma combinação de ambos. Para informações sobre o modo de espera quente, consulte [Seção 26.4](hot-standby.md).

Replicação lógica: A replicação lógica permite que um servidor de banco de dados envie um fluxo de modificações de dados para outro servidor. A replicação lógica do PostgreSQL constrói um fluxo de modificações lógicas de dados a partir do WAL. A replicação lógica permite a replicação de alterações de dados em uma base por tabela. Além disso, um servidor que está publicando suas próprias alterações também pode se inscrever em alterações de outro servidor, permitindo que os dados fluam em várias direções. Para mais informações sobre replicação lógica, consulte [Capítulo 29](logical-replication.md). Através da interface de decodificação lógica ([Capítulo 47](logicaldecoding.md)), extensões de terceiros também podem fornecer funcionalidades semelhantes.

Replicação primária com base em gatilho: Uma configuração de replicação com base em gatilho geralmente direciona consultas de modificação de dados para um servidor primário designado. Operando em uma base por tabela, o servidor primário envia as alterações de dados (tipicamente) de forma assíncrona para os servidores de espera. Os servidores de espera podem responder a consultas enquanto o primário está em execução e podem permitir algumas alterações de dados locais ou atividade de escrita. Esta forma de replicação é frequentemente usada para descarregar grandes consultas de análise ou de data warehouse.

Slony-I é um exemplo desse tipo de replicação, com granularidade por tabela e suporte para múltiplos servidores de espera. Como ele atualiza o servidor de espera de forma assíncrona (em lotes), é possível ocorrer perda de dados durante a transição.

Meio-termo de replicação baseado em SQL: Com o meio-termo de replicação baseado em SQL, um programa intercepta cada consulta SQL e a envia para um ou todos os servidores. Cada servidor opera de forma independente. As consultas de leitura e escrita devem ser enviadas para todos os servidores, para que cada servidor receba quaisquer alterações. Mas as consultas de leitura apenas podem ser enviadas para um único servidor, permitindo que a carga de trabalho de leitura seja distribuída entre eles.

Se as consultas são simplesmente transmitidas sem modificação, funções como `random()`, `CURRENT_TIMESTAMP` e sequências podem ter valores diferentes em diferentes servidores. Isso ocorre porque cada servidor opera de forma independente e porque as consultas SQL são transmitidas em vez de mudanças de dados reais. Se isso não for aceitável, o middleware ou a aplicação deve determinar esses valores a partir de uma única fonte e, em seguida, usar esses valores em consultas de escrita. Também é necessário garantir que todas as transações sejam confirmadas ou aborridas em todos os servidores, talvez usando um compromisso de duas fases ([PREPARE TRANSACTION](sql-prepare-transaction.md) e [COMMIT PREPARED](sql-commit-prepared.md)). Pgpool-II e Continuent Tungsten são exemplos desse tipo de replicação.

Replicação Multimestre Asíncrona: Para servidores que não estão regularmente conectados ou que têm links de comunicação lentos, como laptops ou servidores remotos, manter os dados consistentes entre os servidores é um desafio. Usando a replicação multimestre assíncrona, cada servidor trabalha de forma independente e, periodicamente, comunica-se com os outros servidores para identificar transações conflitantes. Os conflitos podem ser resolvidos por usuários ou por regras de resolução de conflitos. O Bucardo é um exemplo desse tipo de replicação.

Replicação Multimestre Síncrona: Na replicação multimestre síncrona, cada servidor pode aceitar solicitações de escrita, e os dados modificados são transmitidos do servidor original para todos os outros servidores antes de cada transação ser confirmada. A atividade de escrita pesada pode causar bloqueios e atrasos excessivos de confirmação, levando a um desempenho ruim. As solicitações de leitura podem ser enviadas para qualquer servidor. Algumas implementações usam disco compartilhado para reduzir o overhead de comunicação. A replicação multimestre síncrona é a melhor para cargas de trabalho principalmente de leitura, embora sua grande vantagem seja que qualquer servidor pode aceitar solicitações de escrita — não há necessidade de particionar as cargas de trabalho entre servidores primário e de espera, e, como as alterações de dados são enviadas de um servidor para outro, não há problema com funções não determinísticas como `random()`.

PostgreSQL não oferece esse tipo de replicação, embora o PostgreSQL com dois estágios de compromisso ([PREPARE TRANSACTION](sql-prepare-transaction.md) e [COMMIT PREPARED](sql-commit-prepared.md)) possa ser usado para implementar isso no código de aplicativo ou no middleware.

[Tabela 26.1](different-replication-solutions.md#HIGH-AVAILABILITY-MATRIX) resume as capacidades das várias soluções listadas acima.

**Tabela 26.1. Matriz de recursos de alta disponibilidade, balanceamento de carga e replicação**



<table border="1" class="table" summary="High Availability, Load Balancing, and Replication Feature Matrix">
 <colgroup>
  <col class="col1"/>
  <col class="col2"/>
  <col class="col3"/>
  <col class="col4"/>
  <col class="col5"/>
  <col class="col6"/>
  <col class="col7"/>
  <col class="col8"/>
  <col class="col9"/>
 </colgroup>
 <thead>
  <tr>
   <th>
    Característica
   </th>
   <th>
    Shared Disk
   </th>
   <th>
    File System Repl.
   </th>
   <th>
    Write-Ahead Log Shipping
   </th>
   <th>
    Logical Repl.
   </th>
   <th>
    Trigger-​Based Repl.
   </th>
   <th>
    SQL Repl. Middle-ware
   </th>
   <th>
    Async. MM Repl.
   </th>
   <th>
    Sync. MM Repl.
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    Exemplos populares
   </td>
   <td align="center">
    NAS
   </td>
   <td align="center">
    DRBD
   </td>
   <td align="center">
    built-in streaming repl.
   </td>
   <td align="center">
    built-in logical repl., pglogical
   </td>
   <td align="center">
    Londiste, Slony
   </td>
   <td align="center">
    pgpool-II
   </td>
   <td align="center">
    Bucardo
   </td>
   <td align="center">
   </td>
  </tr>
  <tr>
   <td>
    Método de comunicação
   </td>
   <td align="center">
    shared disk
   </td>
   <td align="center">
    disk blocks
   </td>
   <td align="center">
    WAL
   </td>
   <td align="center">
    logical decoding
   </td>
   <td align="center">
    table rows
   </td>
   <td align="center">
    SQL
   </td>
   <td align="center">
    table rows
   </td>
   <td align="center">
    table rows and row locks
   </td>
  </tr>
  <tr>
   <td>
    Não é necessário hardware especial
   </td>
   <td align="center">
   </td>
   <td align="center">
    •
   </td>
   <td align="center">
    •
   </td>
   <td align="center">
    •
   </td>
   <td align="center">
    •
   </td>
   <td align="center">
    •
   </td>
   <td align="center">
    •
   </td>
   <td align="center">
    •
   </td>
  </tr>
  <tr>
   <td>
    Permite múltiplos servidores primários
   </td>
   <td align="center">
   </td>
   <td align="center">
   </td>
   <td align="center">
   </td>
   <td align="center">
    •
   </td>
   <td align="center">
   </td>
   <td align="center">
    •
   </td>
   <td align="center">
    •
   </td>
   <td align="center">
    •
   </td>
  </tr>
  <tr>
   <td>
    Sem sobrecarga no primário
   </td>
   <td align="center">
    •
   </td>
   <td align="center">
   </td>
   <td align="center">
    •
   </td>
   <td align="center">
    •
   </td>
   <td align="center">
   </td>
   <td align="center">
    •
   </td>
   <td align="center">
   </td>
   <td align="center">
   </td>
  </tr>
  <tr>
   <td>
    Sem esperar por vários servidores
   </td>
   <td align="center">
    •
   </td>
   <td align="center">
   </td>
   <td align="center">
    with sync off
   </td>
   <td align="center">
    with sync off
   </td>
   <td align="center">
    •
   </td>
   <td align="center">
   </td>
   <td align="center">
    •
   </td>
   <td align="center">
   </td>
  </tr>
  <tr>
   <td>
    A falha primária nunca perderá dados
   </td>
   <td align="center">
    •
   </td>
   <td align="center">
    •
   </td>
   <td align="center">
    with sync on
   </td>
   <td align="center">
    with sync on
   </td>
   <td align="center">
   </td>
   <td align="center">
    •
   </td>
   <td align="center">
   </td>
   <td align="center">
    •
   </td>
  </tr>
  <tr>
   <td>
    As réplicas aceitam consultas somente de leitura
   </td>
   <td align="center">
   </td>
   <td align="center">
   </td>
   <td align="center">
    with hot standby
   </td>
   <td align="center">
    •
   </td>
   <td align="center">
    •
   </td>
   <td align="center">
    •
   </td>
   <td align="center">
    •
   </td>
   <td align="center">
    •
   </td>
  </tr>
  <tr>
   <td>
    Granularidade por tabela
   </td>
   <td align="center">
   </td>
   <td align="center">
   </td>
   <td align="center">
   </td>
   <td align="center">
    •
   </td>
   <td align="center">
    •
   </td>
   <td align="center">
   </td>
   <td align="center">
    •
   </td>
   <td align="center">
    •
   </td>
  </tr>
  <tr>
   <td>
    Nenhuma resolução de conflito necessária
   </td>
   <td align="center">
    •
   </td>
   <td align="center">
    •
   </td>
   <td align="center">
    •
   </td>
   <td align="center">
   </td>
   <td align="center">
    •
   </td>
   <td align="center">
    •
   </td>
   <td align="center">
   </td>
   <td align="center">
    •
   </td>
  </tr>
 </tbody>
</table>










Há algumas soluções que não se encaixam nas categorias acima:

Particionamento de dados: O particionamento de dados divide as tabelas em conjuntos de dados. Cada conjunto pode ser modificado por apenas um servidor. Por exemplo, os dados podem ser particionados por escritórios, como Londres e Paris, com um servidor em cada escritório. Se forem necessárias consultas que combinem dados de Londres e Paris, uma aplicação pode consultar ambos os servidores, ou a replicação primária/de reserva pode ser usada para manter uma cópia somente de leitura dos dados do outro escritório em cada servidor.

Execução de consultas paralelas em múltiplos servidores: Muitas das soluções acima permitem que vários servidores gerenciem várias consultas, mas nenhuma permite que uma única consulta use vários servidores para ser concluída mais rapidamente. Esta solução permite que vários servidores trabalhem simultaneamente em uma única consulta. Geralmente, isso é feito dividindo os dados entre os servidores e fazendo com que cada servidor execute sua parte da consulta e retorne resultados a um servidor central, onde eles são combinados e retornados ao usuário. Isso pode ser implementado usando o conjunto de ferramentas PL/Proxy.

Também deve ser observado que, como o PostgreSQL é de código aberto e facilmente extensível, várias empresas pegaram o PostgreSQL e criaram soluções comerciais de código fechado com capacidades exclusivas de falha, replicação e balanceamento de carga. Isso não é discutido aqui.