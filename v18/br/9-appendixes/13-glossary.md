## Apêndice M. Glossário

Esta é uma lista de termos e seus significados no contexto do PostgreSQL e dos sistemas de banco de dados relacionais em geral.

ACID: [*[Atomicity](glossary.md#GLOSSARY-ATOMICITY "Atomicity")*](glossário.md#GLÓSSICA-ATOMICIDADE), [*[Consistency](glossary.md#GLOSSARY-CONSISTENCY "Consistency")*](glossário.md#GLÓSSICA-CONSISTÊNCIA), [*[Isolation](glossary.md#GLOSSARY-ISOLATION "Isolation")*](glossário.md#GLÓSSICA-ISOLAÇÃO) e [*[Durability](glossary.md#GLOSSARY-DURABILITY "Durability")*](glossário.md#GLÓSSICA-DURABILIDADE). Este conjunto de propriedades das transações de banco de dados destina-se a garantir a validade em operação concorrente e mesmo em caso de erros, falhas de energia, etc.

Função agregada (rotina): Uma [*[function](glossary.md#GLOSSARY-FUNCTION "Function (routine)")*](glossary.md#GLOSSARY-FUNCTION) que combina (*agrupa*) múltiplos valores de entrada, por exemplo, contando, calculando a média ou adicionando, resultando em um único valor de saída.

Para mais informações, consulte [Seção 9.21](functions-aggregate.md).

Veja também [Função de janela (routine)](glossary.md#GLOSSARY-WINDOW-FUNCTION).

Método de acesso: Interfaces que o PostgreSQL utiliza para acessar dados em tabelas e índices. Essa abstração permite adicionar suporte para novos tipos de armazenamento de dados.

Para mais informações, consulte o [Capítulo 62](tableam.md) e o [Capítulo 63](indexam.md).

Função analítica: Veja [Função de janela (routine)](glossary.md#GLOSSARY-WINDOW-FUNCTION).

Analisar (operação): O ato de coletar estatísticas dos dados em [*[tabelas](glossary.md#GLOSSARY-TABLE)]*(glossário.md#GLOSSARY-TABLE) e outras [*[relações](glossary.md#GLOSSARY-RELATION)]*(glossário.md#GLOSSARY-RELATION) para ajudar o [*[planificador de consultas](glossary.md#GLOSSARY-PLANNER)*]*(glossário.md#GLOSSARY-PLANNER) a tomar decisões sobre como executar [*[consultas](glossary.md#GLOSSARY-QUERY)*]*(glossário.md#GLOSSARY-QUERY).

(Não confunda este termo com a opção `ANALYZE` para o comando [EXPLAIN](sql-explain.md "EXPLAIN").)

Para mais informações, consulte [ANALYZE](sql-analyze.md "ANALYZE").

E/S assíncrona (AIO): A E/S assíncrona (AIO) descreve a realização de E/S de uma maneira não bloqueante (assíncrona), em contraste com a E/S síncrona, que bloqueia durante toda a duração da E/S.

Com o AIO, iniciar uma operação de E/S é separado da espera pelo resultado da operação, permitindo que múltiplas operações de E/S sejam iniciadas simultaneamente, bem como a realização de operações pesadas de CPU simultaneamente com a E/S. O preço dessa maior concorrência é a complexidade aumentada.

Veja também [Entrada/Saída](glossary.md#GLOSSARY-IO).

Atômico: Em referência a um [*[data](glossary.md#GLOSSARY-DATUM "Datum")*](glossário.md#GLÓSSOLA-DATA): o fato de que seu valor não pode ser decomposto em componentes menores. Em referência a uma [*[transação de banco de dados](glossary.md#GLOSSARY-TRANSACTION "Transaction")*](glossário.md#GLÓSSOLA-TRANSACÃO): veja [*[atitude](glossary.md#GLOSSARY-ATOMICITY "Atomicity")*](glossário.md#GLÓSSOLA-ATITUDINAL).

Atomismo: A propriedade de uma [*[transação](glossary.md#GLOSSARY-TRANSACTION)]*(glossário.md#GLÓSSOLArio-TRANSACÃO) que ou todas as suas operações são concluídas como uma única unidade ou nenhuma delas. Além disso, se uma falha no sistema ocorrer durante a execução de uma transação, nenhum resultado parcial é visível após a recuperação. Esta é uma das propriedades ACID.

Atributo: Um elemento com um determinado nome e tipo de dados encontrado dentro de um [*[tuple][(glossary.md#GLOSSARY-TUPLE "Tuple")*]](glossário.md#GLÓSSICA-TUPLE).

Autovacuum (processo): Um conjunto de processos de fundo que realizam rotineiramente as operações [*[vacuum](glossary.md#GLOSSARY-VACUUM)*](glossary.md#GLOSSARY-VACUUM) e [*[analyze](glossary.md#GLOSSARY-ANALYZE)*](glossary.md#GLOSSARY-ANALYZE) (*). O [*[auxiliary process](glossary.md#GLOSSARY-AUXILIARY-PROC)*](glossary.md#GLOSSARY-AUXILIARY-PROC) que coordena o trabalho e está sempre presente (a menos que o autovacuum seja desativado) é conhecido como o *autovacuum launcher*, e os processos que realizam as tarefas são conhecidos como os *autovacuum workers*.

Para mais informações, consulte [Seção 24.1.6](routine-vacuuming.md#AUTOVACUUM).

Processo auxiliar: Um processo dentro de um [*[instância](glossary.md#GLOSSARY-INSTANCE "Instance")*](glossary.md#GLOSSARY-INSTANCE) que é responsável por alguma tarefa de fundo específica para a instância. Os processos auxiliares consistem no [*[lançador de autovacuum](glossary.md#GLOSSARY-AUTOVACUUM "Autovacuum (process)"]*(glossary.md#GLOSSARY-AUTOVACUUM) (mas não os trabalhadores de autovacuum), o [*[escritor de fundo](glossary.md#GLOSSARY-BACKGROUND-WRITER "Background writer (process)"]*(glossary.md#GLOSSARY-BACKGROUND-WRITER), o [*[checkpointer](glossary.md#GLOSSARY-CHECKPOINTER "Checkpointer (process)"]*(glossary.md#GLOSSARY-CHECKPOINTER), o [*[logger](glossary.md#GLOSSARY-LOGGER "Logger (process)"]*(glossary.md#GLOSSARY-LOGGER), o [*[processo de inicialização](glossary.md#GLOSSARY-STARTUP-PROCESS "Startup process")*]*(glossary.md#GLOSSARY-STARTUP-PROCESS), o [*[arquivador de WAL](glossary.md#GLOSSARY-WAL-ARCHIVER "WAL archiver (process)"]*(glossary.md#GLOSSARY-WAL-ARCHIVER), o [*[receptor de WAL](glossary.md#GLOSSARY-WAL-RECEIVER "WAL receiver (process)"]*(glossary.md#GLOSSARY-WAL-RECEIVER) (mas não os [*[emendas de WAL](glossary.md#GLOSSARY-WAL-SENDER "WAL sender (process)"]*(glossary.md#GLOSSARY-WAL-SENDER)), o [*[resumidor de WAL](glossary.md#GLOSSARY-WAL-SUMMARIZER "WAL summarizer (process)"]*(glossary.md#GLOSSARY-WAL-SUMMARIZER), e o [*[escritor de WAL](glossary.md#GLOSSARY-WAL-WRITER "WAL writer (process)"]*(glossary.md#GLOSSARY-WAL-WRITER).

Backend (processo): Processo de um [*[instância](glossary.md#GLOSSARY-INSTANCE "Instance")*](glossário.md#GLOSSÁRIO-INSTÂNCIA) que age em nome de uma [*[sessão do cliente](glossary.md#GLOSSARY-SESSION "Session")*](glossário.md#GLOSSÁRIO-SESSÃO) e lida com suas solicitações.

(Não confunda este termo com os termos semelhantes [*[Background Worker](glossary.md#GLOSSARY-BACKGROUND-WORKER "Background worker (process)"]*) (glossary.md#GLOSSARY-BACKGROUND-WORKER) ou [*[Background Writer](glossary.md#GLOSSARY-BACKGROUND-WRITER "Background writer (process)"]*) (glossary.md#GLOSSARY-BACKGROUND-WRITER)).

Trabalhador de fundo (processo): Processo dentro de um [*[instância][(glossary.md#GLOSSARY-INSTANCE "Instance")*]](glossary.md#GLOSSARY-INSTANCIA), que executa código fornecido pelo sistema ou pelo usuário. Serve como infraestrutura para várias funcionalidades no PostgreSQL, como [*[replicação lógica][(glossary.md#GLOSSARY-REPLICATION "Replication")*]](glossary.md#GLOSSARY-REPLICATION) e [*[consultas paralelas][(glossary.md#GLOSSARY-PARALLEL-QUERY "Parallel query")*]](glossary.md#GLOSSARY-PARALLEL-QUERY]. Além disso, [*[extensões][(glossary.md#GLOSSARY-EXTENSION "Extension")*]](glossary.md#GLOSSARY-EXTENSION) pode adicionar processos de trabalhador de fundo personalizados.

Para mais informações, consulte o [Capítulo 46](bgworker.md).

Escritor de segundo plano (processo): Um [*[processo auxiliar][(glossary.md#GLOSSARY-AUXILIARY-PROC "Auxiliary process")*]](glossário.md#GLÓSSICO-AUXILIAR-PROC) que escreve páginas de dados sujas ([*[paginas de dados][(glossary.md#GLOSSARY-DATA-PAGE "Data page")*]](glossário.md#GLÓSSICO-DATA-PAGE) a partir de [*[memória compartilhada][(glossary.md#GLOSSARY-SHARED-MEMORY "Shared memory")*]](glossário.md#GLÓSSICO-MEMÓRIA-PARTEADA) para o sistema de arquivos. Ele acorda periodicamente, mas trabalha apenas por um curto período para distribuir sua atividade de E/S cara ao longo do tempo, evitando gerar picos maiores de E/S que poderiam bloquear outros processos.

Para mais informações, consulte [Seção 19.4.4](runtime-config-resource.md#RUNTIME-CONFIG-RESOURCE-BACKGROUND-WRITER).

Backup de base: Uma cópia binária de todos os arquivos [*[database cluster][(glossary.md#GLOSSARY-DB-CLUSTER "Database cluster")*]](glossário.md#GLOSSARY-DB-CLUSTER). É gerado pela ferramenta [pg_basebackup](app-pgbasebackup.md). Em combinação com os arquivos WAL, pode ser usado como ponto de partida para recuperação, envio de logs ou replicação em streaming.

Bloat: Espaço em páginas de dados que não contém versões atuais de linha, como espaço não utilizado (livre) ou versões de linha desatualizadas.

Superusuário do Bootstrap: O primeiro [*[user][(glossary.md#GLOSSARY-USER "User")*]](glossary.md#GLOSSARY-USER) inicializado em um [*[database cluster][(glossary.md#GLOSSARY-DB-CLUSTER "Database cluster")*]](glossary.md#GLOSSARY-DB-CLUSTER).

Este usuário possui todas as tabelas de catálogo do sistema em cada banco de dados. É também o papel a partir do qual todos os permissões concedidas se originam. Por causa dessas coisas, este papel pode não ser eliminado.

Esse papel também se comporta como um usuário super do [*[database superuser](glossary.md#GLOSSARY-DATABASE-SUPERUSER)]*(glossário.md#GLOSSARY-DATABASE-SUPERUSER), e seu status de usuário super não pode ser removido.

Estratégia de Acesso ao Buffer: Algumas operações acessam um grande número de [*[pages](glossary.md#GLOSSARY-DATA-PAGE)]*(glossário.md#GLOSSARY-DATA-PAGE). Uma *Estratégia de Acesso ao Buffer* ajuda a evitar que essas operações removam muitas páginas de [*[buffers compartilhados](glossary.md#GLOSSARY-SHARED-MEMORY)]*(glossário.md#GLOSSARY-SHARED-MEMORY).

Uma Estratégia de Acesso a Buffer configura referências para um número limitado de [*[buffers compartilhados][(glossary.md#GLOSSARY-SHARED-MEMORY "Shared memory")*]](glossário.md#GLOSSARY-SHARED-MEMORY) e os reutiliza de forma circular. Quando a operação requer uma nova página, um buffer vítima é escolhido entre os buffers da estratégia, o que pode exigir o esvaziamento dos dados sujos da página e, possivelmente, também o descarte do [*[WAL][(glossary.md#GLOSSARY-WAL "Write-ahead log")*]](glossário.md#GLOSSARY-WAL) para armazenamento permanente.

As estratégias de acesso ao buffer são utilizadas para várias operações, como varreduras sequenciais de grandes tabelas, `VACUUM`, `COPY`, `CREATE TABLE AS SELECT`, `ALTER TABLE`, `CREATE DATABASE`, `CREATE INDEX` e `CLUSTER`.

Cast: Uma conversão de um [*[data](glossary.md#GLOSSARY-DATUM)]*(glossário.md#GLÓSSICO-DATA) do seu tipo de dados atual para outro tipo de dados.

Para mais informações, consulte [CREATE CAST](sql-createcast.md "CREATE CAST").

Catálogo: O padrão SQL usa esse termo para indicar o que é chamado de [*[database](glossary.md#GLOSSARY-DATABASE)*](glossário.md#GLOSSARY-DATABASE) na terminologia do PostgreSQL.

(Não confunda este termo com [*[catálogo do sistema][*[(glossary.md#GLOSSARY-SYSTEM-CATALOG "System catalog")]]*](glossário.md#GLÓSSICA-CATÁLOGO-SISTEMA)).

Para mais informações, consulte [Seção 22.1](manage-ag-overview.md).

Restrição de verificação: Um tipo de [*[constraint](glossary.md#GLOSSARY-CONSTRAINT "Constraint")*](glossary.md#GLOSSARY-CONSTRAINT) definido em uma [*[relation](glossary.md#GLOSSARY-RELATION "Relation")*](glossary.md#GLOSSARY-RELATION) que restringe os valores permitidos em um ou mais [*[attributes](glossary.md#GLOSSARY-ATTRIBUTE "Attribute")*](glossary.md#GLOSSARY-ATTRIBUTE). A restrição de verificação pode fazer referência a qualquer atributo da mesma linha na relação, mas não pode fazer referência a outras linhas da mesma relação ou outras relações.

Para mais informações, consulte [Seção 5.5](ddl-constraints.md).

Ponto de verificação: um ponto na sequência [*[WAL](glossary.md#GLOSSARY-WAL "Write-ahead log")*](glossary.md#GLOSSARY-WAL) em que é garantido que os arquivos de dados de heap e índice foram atualizados com todas as informações da [*[memória compartilhada](glossary.md#GLOSSARY-SHARED-MEMORY "Shared memory")*](glossary.md#GLOSSARY-SHARED-MEMORY) modificados antes desse ponto de verificação; um *registro de verificação* é escrito e esvaziado para o WAL para marcar esse ponto.

Um ponto de verificação também é o ato de realizar todas as ações necessárias para alcançar um ponto de verificação conforme definido acima. Esse processo é iniciado quando as condições predefinidas são atendidas, como um período de tempo especificado ter passado ou um certo volume de registros terem sido escritos; ou ele pode ser invocado pelo usuário com o comando `CHECKPOINT`.

Para mais informações, consulte [Seção 28.5](wal-configuration.md).

Checkpointer (processo): Um [*[processo auxiliar][(glossary.md#GLOSSARY-AUXILIARY-PROC "Auxiliary process")*]](glossário.md#GLÓSSICO-AUXILIAR-PROC) que é responsável por executar [*[pontos de verificação][(glossary.md#GLOSSARY-CHECKPOINT "Checkpoint")*]](glossário.md#GLÓSSICO-CHECKPOINT).

Classe (arquéu): Veja [Relação](glossary.md#GLOSSARY-RELATION).

Cliente (processo): Qualquer processo, possivelmente remoto, que estabeleça uma sessão [*[(glossary.md#GLOSSARY-SESSION "Session")]*](glossário.md#GLOSSARY-SESSION) por [*[(glossary.md#GLOSSARY-CONNECTION "Connection")]*](glossário.md#GLOSSARY-CONNECTION) a uma [*[(glossary.md#GLOSSARY-INSTANCE "Instance")]*](glossário.md#GLOSSARY-INSTANCE) para interagir com um [*[(glossary.md#GLOSSARY-DATABASE "Database")]*](glossário.md#GLOSSARY-DATABASE] (banco de dados).

Proprietário do cluster: O usuário do sistema operacional que possui o [*[data directory](glossary.md#GLOSSARY-DATA-DIRECTORY)]*(glossary.md#GLOSSARY-DATA-DIRECTORY) e sob o qual o processo `postgres` é executado. É necessário que esse usuário exista antes de criar um novo [*[database cluster](glossary.md#GLOSSARY-DB-CLUSTER)]*(glossary.md#GLOSSARY-DB-CLUSTER).

Em sistemas operacionais com um usuário `root`, dito usuário não pode ser o proprietário do grupo.

Coluna: Um [*[atributo](glossary.md#GLOSSARY-ATTRIBUTE "Attribute")*](glossário.md#GLÓSSICO-ATributo) encontrado em uma [*[tabela](glossary.md#GLOSSARY-TABLE "Table")*](glossário.md#GLÓSSARIO-TABELA) ou [*[visualização](glossary.md#GLOSSARY-VIEW "View")*](glossário.md#GLÓSSARIO-VISUALIZAÇÃO).

Compromisso: O ato de finalizar uma [*[transação](glossary.md#GLOSSARY-TRANSACTION "Transaction")*](glossary.md#GLOSSARY-TRANSACTION) dentro da [*[base de dados](glossary.md#GLOSSARY-DATABASE "Database")*](glossary.md#GLOSSARY-DATABASE), que a torna visível para outras transações e garante sua [*[durabilidade](glossary.md#GLOSSARY-DURABILITY "Durability")*](glossary.md#GLOSSARY-DURABILITY).

Para mais informações, consulte [COMMIT](sql-commit.md "COMMIT").

Concorrência: O conceito de que múltiplas operações independentes ocorrem ao mesmo tempo dentro do [*[database](glossary.md#GLOSSARY-DATABASE)*](glossary.md#GLOSSARY-DATABASE) no PostgreSQL. A concorrência é controlada pelo mecanismo [*[multiversion concurrency control](glossary.md#GLOSSARY-MVCC)*](glossary.md#GLOSSARY-MVCC).

Conexão: Uma linha de comunicação estabelecida entre um processo cliente e um processo [*[backend](glossary.md#GLOSSARY-BACKEND "Backend (process)*](glossary.md#GLOSSARY-BACKEND), geralmente através de uma rede, que suporta uma [*[session](glossary.md#GLOSSARY-SESSION "Session")*](glossary.md#GLOSSARY-SESSION). Este termo é, por vezes, usado como sinónimo de sessão.

Para mais informações, consulte [Seção 19.3](runtime-config-connection.md).

Consistência: A propriedade de que os dados no [*[database](glossary.md#GLOSSARY-DATABASE)]*](glossary.md#GLOSSARY-DATABASE) estão sempre em conformidade com [*[constraints de integridade](glossary.md#GLOSSARY-CONSTRAINT)]*](glossary.md#GLOSSARY-CONSTRAINT). As transações podem ser permitidas para violar algumas das restrições de forma transitória antes de serem confirmadas, mas se tais violações não forem resolvidas até o momento da confirmação, uma transação é automaticamente [*[revertida](glossary.md#GLOSSARY-ROLLBACK)]*](glossary.md#GLOSSARY-ROLLBACK). Isso é uma das propriedades ACID.

Restrição: Uma restrição sobre os valores de dados permitidos em uma tabela [*[table](glossary.md#GLOSSARY-TABLE "Table")*](glossary.md#GLOSSARY-TABLE), ou em atributos de um domínio [*[domain](glossary.md#GLOSSARY-DOMAIN "Domain")*](glossary.md#GLOSSARY-DOMAIN).

Para mais informações, consulte [Seção 5.5](ddl-constraints.md).

Sistema de Estatísticas Cumulativas: Um sistema que, se ativado, acumula informações estatísticas sobre as atividades do [*[instance][(glossary.md#GLOSSARY-INSTANCE "Instance")*]](glossário.md#GLÓSSICO-INSTÂNCIA).

Para mais informações, consulte [Seção 27.2](monitoring-stats.md).

Área de dados: Veja [Diretório de dados](glossary.md#GLOSSARY-DATA-DIRECTORY).

Banco de dados: uma coleção nomeada de [*[objetos SQL locais][(glossary.md#GLOSSARY-SQL-OBJECT "SQL object")*]](glossário.md#GLÓSSARIO-OBJETO-SQL).

Para mais informações, consulte [Seção 22.1](manage-ag-overview.md).

Grupo de bancos de dados: Uma coleção de bancos de dados e objetos SQL globais, e seus metadados estáticos e dinâmicos comuns. Às vezes referido como um *cluster*. Um grupo de bancos de dados é criado usando o programa [initdb](app-initdb.md).

Em PostgreSQL, o termo *cluster* também é usado às vezes para se referir a uma instância. (Não confunda este termo com o comando SQL `CLUSTER`.)

Veja também [*[cluster owner](glossary.md#GLOSSARY-CLUSTER-OWNER "Cluster owner")*](glossary.md#GLOSSARY-CLUSTER-OWNER), o proprietário do sistema operacional de um cluster, e [*[bootstrap superuser](glossary.md#GLOSSARY-BOOTSTRAP-SUPERUSER "Bootstrap superuser")*](glossary.md#GLOSSARY-BOOTSTRAP-SUPERUSER), o proprietário do PostgreSQL de um cluster.

Servidor de banco de dados: Veja [Instância](glossary.md#GLOSSARY-INSTANCE).

Superusuário do banco de dados: um papel que possui *status de superusuário* (consulte [Seção 21.2](role-attributes.md)).

Frequentemente referido como *superusuário*.

Diretório de dados: O diretório base no sistema de arquivos de um [*[server](glossary.md#GLOSSARY-SERVER "Server")*](glossary.md#GLOSSARY-SERVER) (glossário.md#GLOSSARY-SERVER) que contém todos os arquivos de dados e subdiretórios associados a um [*[cluster de banco de dados](glossary.md#GLOSSARY-DB-CLUSTER "Database cluster")*](glossary.md#GLOSSARY-DB-CLUSTER) (com exceção de [*[tablespaces](glossary.md#GLOSSARY-TABLESPACE "Tablespace")*](glossary.md#GLOSSARY-TABLESPACE), e opcionalmente [*[WAL](glossary.md#GLOSSARY-WAL "Write-ahead log")*](glossary.md#GLOSSARY-WAL)). A variável de ambiente `PGDATA` é comumente usada para se referir ao diretório de dados.

O espaço de armazenamento de um [*[cluster](glossary.md#GLOSSARY-DB-CLUSTER "Database cluster")*] (glossário.md#GLOSSARY-DB-CLUSTER) compreende o diretório de dados mais quaisquer espaços de tabelas adicionais.

Para mais informações, consulte [Seção 66.1](storage-file-layout.md).

Página de dados: A estrutura básica usada para armazenar dados de relação. Todas as páginas têm o mesmo tamanho. As páginas de dados são tipicamente armazenadas em disco, cada uma em um arquivo específico, e podem ser lidas em [*[buffers compartilhados][(glossary.md#GLOSSARY-SHARED-MEMORY "Shared memory")*]](glossário.md#GLOSSARY-SHARED-MEMORY) onde podem ser modificadas, tornando-se *sujas*. Elas se tornam limpas quando escritas em disco. Novas páginas, que inicialmente existem apenas na memória, também são sujas até serem escritas.

Data: A representação interna de um valor de um tipo de dados SQL.

Exclua: Um comando SQL que remove [*[rows](glossary.md#GLOSSARY-TUPLE "Tuple")*](glossary.md#GLOSSARY-TUPLE) de uma [*[table](glossary.md#GLOSSARY-TABLE "Table")*](glossary.md#GLOSSARY-TABLE) ou [*[relation](glossary.md#GLOSSARY-RELATION "Relation")*](glossary.md#GLOSSARY-RELATION) específica.

Para mais informações, consulte [DELETE](sql-delete.md).

Domínio: Um tipo de dados definido pelo usuário que é baseado em outro tipo de dados subjacente. Ele age da mesma forma que o tipo subjacente, exceto por possivelmente restringir o conjunto de valores permitidos.

Para mais informações, consulte [Seção 8.18](domains.md).

Durabilidade: A garantia de que, uma vez que uma [*[transação](glossary.md#GLOSSARY-TRANSACTION)(glossary.md#GLOSSARY-TRANSACTION)](transação) tenha sido [*[comprometida](glossary.md#GLOSSARY-COMMIT)(glossary.md#GLOSSARY-COMMIT)](comprometida), as alterações permanecem mesmo após uma falha ou travamento do sistema. Esta é uma das propriedades ACID.

Época: Veja [ID da transação](glossary.md#GLOSSARY-XID).

Extensão: Um pacote de complementos de software que pode ser instalado em uma instância [*[instance](glossary.md#GLOSSARY-INSTANCE)]*(glossário.md#GLÓSSARIO-INSTÂNCIA) para obter recursos adicionais.

Para mais informações, consulte [Seção 36.17](extend-extensions.md).

Segmento de arquivo: Um arquivo físico que armazena dados para um dado [*[relação](glossary.md#GLOSSARY-RELATION "Relation")*] (glossário.md#GLOSSARY-RELATION). Os segmentos de arquivo são limitados em tamanho por um valor de configuração (tipicamente 1 gigabyte), portanto, se uma relação exceder esse tamanho, ela é dividida em vários segmentos.

Para mais informações, consulte [Seção 66.1](storage-file-layout.md).

(Não confunda este termo com o termo semelhante [*[WAL segment](glossary.md#GLOSSARY-WAL-FILE "WAL file")*](glossário.md#GLÓSSICA-FILE-WAL)).

Agente de dados estrangeiro: Um meio de representar dados que não estão contidos no [*[database](glossary.md#GLOSSARY-DATABASE)]*(glossary.md#GLOSSARY-DATABASE) local, de modo que pareçam estar no [*[table(s)](glossary.md#GLOSSARY-TABLE)]*(glossary.md#GLOSSARY-TABLE) local. Com um agente de dados estrangeiro, é possível definir um [*[foreign server](glossary.md#GLOSSARY-FOREIGN-SERVER)]*(glossary.md#GLOSSARY-FOREIGN-SERVER) e [*[foreign tables](glossary.md#GLOSSARY-FOREIGN-TABLE)*](glossary.md#GLOSSARY-FOREIGN-TABLE).

Para mais informações, consulte [CREATE FOREIGN DATA WRAPPER](sql-createforeigndatawrapper.md).

Chave estrangeira: Um tipo de [*[constraint](glossary.md#GLOSSARY-CONSTRAINT)]*(glossary.md#GLOSSARY-CONSTRAINT) definido em um ou mais [*[columns](glossary.md#GLOSSARY-COLUMN)]*(glossary.md#GLOSSARY-COLUMN) em uma [*[table](glossary.md#GLOSSARY-TABLE)]*(glossary.md#GLOSSARY-TABLE) que exige que os valores nessas [*[columns](glossary.md#GLOSSARY-COLUMN)]*(glossary.md#GLOSSARY-COLUMN) identifiquem zero ou um [*[row](glossary.md#GLOSSARY-TUPLE)]*(glossary.md#GLOSSARY-TUPLE) em outra (ou, raramente, a mesma) [*[table](glossary.md#GLOSSARY-TABLE)]*(glossary.md#GLOSSARY-TABLE).

Servidor estrangeiro: Uma coleção nomeada de [*[tabelas estrangeiras](glossary.md#GLOSSARY-FOREIGN-TABLE "Foreign table (relation)]")*(glossary.md#GLÓSSICA-TABELA-ESTRANGEIRA) que utilizam todas o mesmo [*[envolvente de dados estrangeiro](glossary.md#GLOSSARY-FOREIGN-DATA-WRAPPER "Foreign data wrapper")*](glossary.md#GLÓSSICA-ENVOLVENTE-DE-DADOS-ESTRANGEIRO) e têm outros valores de configuração em comum.

Para mais informações, consulte [CREATE SERVER](sql-createserver.md "CREATE SERVER").

Tabela estrangeira (relação): Um [*[rows](glossary.md#GLOSSARY-TUPLE "Tuple")*](glossary.md#GLOSSARY-TUPLE) que parece ter [*[columns](glossary.md#GLOSSARY-COLUMN "Column")*](glossary.md#GLOSSARY-COLUMN) semelhante a uma tabela regular [*[table](glossary.md#GLOSSARY-TABLE "Table")*](glossary.md#GLOSSARY-TABLE), mas que encaminhará solicitações de dados por meio de seu [*[foreign data wrapper](glossary.md#GLOSSARY-FOREIGN-DATA-WRAPPER "Foreign data wrapper")*](glossary.md#GLOSSARY-FOREIGN-DATA-WRAPPER), que retornará [*[result sets](glossary.md#GLOSSARY-RESULT-SET "Result set")*](glossary.md#GLOSSARY-RESULT-SET) estruturados de acordo com a definição da [*[foreign table](glossary.md#GLOSSARY-FOREIGN-TABLE "Foreign table (relation)")*](glossary.md#GLOSSARY-FOREIGN-TABLE).

Para mais informações, consulte [Criação de tabela estrangeira](sql-createforeigntable.md).

Espécie: Cada um dos conjuntos de arquivos segmentados separados nos quais uma relação é armazenada. O *main fork* é onde os dados reais residem. Também existem dois forks secundários para metadados: o [*[free space map](glossary.md#GLOSSARY-FSM "Free space map (fork)*](glossary.md#GLOSSARY-FSM) e o [*[visibility map](glossary.md#GLOSSARY-VM "Visibility map (fork)*](glossary.md#GLOSSARY-VM). [*[Unlogged relations](glossary.md#GLOSSARY-UNLOGGED "Unlogged")*](glossary.md#GLOSSARY-UNLOGGED) também têm um *fork init*.

Mapa de espaço livre (esponja): Uma estrutura de armazenamento que mantém metadados sobre cada página de dados de uma esponja principal de uma tabela. A entrada do mapa de espaço livre para cada página armazena a quantidade de espaço livre disponível para futuros tuplos e é estruturada para ser pesquisada de forma eficiente em busca de espaço disponível para um novo tuplo de determinado tamanho.

Para mais informações, consulte [Seção 66.3](storage-fsm.md).

Função (rotina): Um tipo de rotina que recebe zero ou mais argumentos, retorna zero ou mais valores de saída e é obrigada a ser executada dentro de uma transação. As funções são invocadas como parte de uma consulta, por exemplo, via `SELECT`. Algumas funções podem retornar [*[sets](glossary.md#GLOSSARY-RESULT-SET "Result set")*](glossário.md#GLOSSARY-RESULT-SET); essas são chamadas de funções que retornam conjuntos.

As funções também podem ser usadas para [*[triggers](glossary.md#GLOSSARY-TRIGGER "Trigger")*](glossário.md#GLÓSSICO-TRIGUEIRO) para serem invocadas.

Para mais informações, consulte [CREATE FUNCTION](sql-createfunction.md "CREATE FUNCTION").

GMT: Veja [UTC](glossary.md#GLOSSARY-UTC).

Permissão: Um comando SQL que é usado para permitir que um [*[usuário](glossary.md#GLOSSARY-USER "User")*](glossary.md#GLOSSARY-USER) ou [*[papel](glossary.md#GLOSSARY-ROLE "Role")*](glossary.md#GLOSSARY-ROLE) acesse objetos específicos dentro do [*[banco de dados](glossary.md#GLOSSARY-DATABASE "Database")*](glossary.md#GLOSSARY-DATABASE).

Para mais informações, consulte [GRANT](sql-grant.md).

Heap: Contém os valores dos atributos [*[row][(glossary.md#GLOSSARY-TUPLE "Tuple")*]](glossary.md#GLOSSARY-TUPLE) (ou seja, os dados) para uma [*[relação][(glossary.md#GLOSSARY-RELATION "Relation")*]](glossary.md#GLOSSARY-RELATION). O heap é realizado dentro de um ou mais [*[segmentos de arquivo][(glossary.md#GLOSSARY-FILE-SEGMENT "File segment")*]](glossary.md#GLOSSARY-FILE-SEGMENT) no [*[principal bifurcação][(glossary.md#GLOSSARY-FORK "Fork")*]](glossary.md#GLOSSARY-FORK] da relação.

Anfitrião: Um computador que se comunica com outros computadores através de uma rede. Isso é, por vezes, usado como sinônimo de [*[server](glossary.md#GLOSSARY-SERVER)*](glossário.md#GLOSSARY-SERVER). Também é usado para se referir a um computador onde os [*[client processes](glossary.md#GLOSSARY-CLIENT)*](glossário.md#GLOSSARY-CLIENT) são executados.

Índice (relação): Um [*[relação](glossary.md#GLOSSARY-RELATION "Relation")*](glossário.md#GLÓSSICA-RELATÓRIO) que contém dados derivados de uma [*[tabela](glossary.md#GLOSSARY-TABLE "Table")*](glossário.md#GLÓSSÁRIO-TABELA) ou [*[visualização materializada](glossary.md#GLOSSARY-MATERIALIZED-VIEW "Materialized view (relation)*](glossário.md#GLÓSSÁRIO-VISUALIZAÇÃO-MATERIALIZADA). Sua estrutura interna suporta a recuperação rápida dos dados originais e o acesso a eles.

Para mais informações, consulte [CREATE INDEX](sql-createindex.md "CREATE INDEX").

Backup incremental: Um backup especial [*[base backup](glossary.md#GLOSSARY-BASEBACKUP)]*(glossário.md#GLOSSARY-BASEBACKUP) que, para alguns arquivos, pode conter apenas as páginas que foram modificadas desde um backup anterior, ao contrário do conteúdo completo de todos os arquivos. Assim como os backups básicos, ele é gerado pela ferramenta [pg_basebackup](app-pgbasebackup.md).

Para restaurar backups incrementais, a ferramenta [pg_combinebackup](app-pgcombinebackup.md) é usada, que combina backups incrementais com um backup de base. Posteriormente, a recuperação pode usar [*[WAL](glossary.md#GLOSSARY-WAL)*](glossário.md#GLOSSARY-WAL) para levar o [*[grupo de bancos de dados](glossary.md#GLOSSARY-DB-CLUSTER)*](glossário.md#GLOSSARY-DB-CLUSTER) a um estado consistente.

Para mais informações, consulte [Seção 25.3.3](continuous-archiving.md#BACKUP-INCREMENTAL-BACKUP).

Entrada/Saída (I/O): Entrada/Saída (I/O) descreve a comunicação entre um programa e dispositivos periféricos. No contexto de sistemas de banco de dados, I/O geralmente, mas não exclusivamente, se refere à interação com dispositivos de armazenamento ou com a rede.

Veja também [E/S assíncrona](glossary.md#GLOSSARY-AIO).

Inserir: Um comando SQL usado para adicionar novos dados em uma tabela [*[(glossary.md#GLOSSARY-TABLE "Table")]*](glossário.md#GLOSSARY-TABLE).

Para mais informações, consulte [INSERT](sql-insert.md "INSERT").

Um grupo de [*[backend](glossary.md#GLOSSARY-BACKEND "Backend (process)]")*(glossary.md#GLOSSARY-BACKEND) e [*[processos auxiliares](glossary.md#GLOSSARY-AUXILIARY-PROC "Auxiliary process")*](glossary.md#GLOSSARY-AUXILIARY-PROC) que se comunicam usando uma área de memória compartilhada comum. Um [*[processo do postmaster](glossary.md#GLOSSARY-POSTMASTER "Postmaster (process)]")*(glossary.md#GLOSSARY-POSTMASTER) gerencia a instância; uma instância gerencia exatamente um [*[grupo de bancos de dados](glossary.md#GLOSSARY-DB-CLUSTER "Database cluster")*](glossary.md#GLOSSARY-DB-CLUSTER) com todas as suas bases de dados. Muitas instâncias podem rodar no mesmo [*[servidor](glossary.md#GLOSSARY-SERVER "Server")*](glossary.md#GLOSSARY-SERVER), desde que suas portas TCP não conflitem.

A instância lida com todas as principais características de um DBMS: acesso de leitura e escrita a arquivos e memória compartilhada, garantia das propriedades ACID, [*[conexões](glossary.md#GLOSSARY-CONNECTION)(glossário.md#GLOSSARY-CONNECTION)](glossário.md#GLOSSARY-CONNECTION) a [*[processos de cliente](glossary.md#GLOSSARY-CLIENT)(glossário.md#GLOSSARY-CLIENT)](glossário.md#GLOSSARY-CLIENT)], verificação de privilégios, recuperação em caso de falha, replicação, etc.

Isolamento: A propriedade de que os efeitos de uma transação não são visíveis para [*[transações concorrentes](glossary.md#GLOSSARY-CONCURRENCY)]*](glossário.md#GLOSSARY-CONCURRENCY) antes de ela ser confirmada. Esta é uma das propriedades ACID.

Para mais informações, consulte [Seção 13.2](transaction-iso.md).

Join: Uma operação e uma palavra-chave SQL usada em [*[queries][(glossary.md#GLOSSARY-QUERY "Query")*]](glossary.md#GLOSSARY-QUERY) para combinar dados de múltiplas [*[relations][(glossary.md#GLOSSARY-RELATION "Relation")*]](glossary.md#GLOSSARY-RELATION).

Chave: Um meio de identificar um [*[row](glossary.md#GLOSSARY-TUPLE "Tuple")*](glossário.md#GLOSSARY-TUPLE) dentro de uma [*[table](glossary.md#GLOSSARY-TABLE "Table")*](glossário.md#GLOSSARY-TABLE) ou outra [*[relation](glossary.md#GLOSSARY-RELATION "Relation")*](glossário.md#GLOSSARY-RELATION) por valores contidos em uma ou mais [*[attributes](glossary.md#GLOSSARY-ATTRIBUTE "Attribute")*](glossário.md#GLOSSARY-ATTRIBUTE) nessa relação.

Bloqueio: Um mecanismo que permite que um processo limite ou impeça o acesso simultâneo a um recurso.

Arquivo de registro: Arquivos de registro contêm linhas de texto legíveis por humanos sobre eventos. Exemplos incluem falhas de login, consultas de longa duração, etc.

Para mais informações, consulte [Seção 24.3](logfile-maintenance.md).

Registrada: Uma tabela [*[table](glossary.md#GLOSSARY-TABLE "Table")*](glossary.md#GLOSSARY-TABLE) é considerada [*[logged](glossary.md#GLOSSARY-LOGGED "Logged")*](glossary.md#GLOSSARY-LOGGED) se alterações nela forem enviadas para o [*[WAL](glossary.md#GLOSSARY-WAL "Write-ahead log")*](glossary.md#GLOSSARY-WAL). Por padrão, todas as tabelas regulares são registradas. Uma tabela pode ser especificada como [*[unlogged](glossary.md#GLOSSARY-UNLOGGED "Unlogged")*](glossary.md#GLOSSARY-UNLOGGED) tanto no momento da criação quanto através do comando `ALTER TABLE`(glossary.md#GLOSSARY-ICD).

Logger (processo): Um [*[processo auxiliar][(glossary.md#GLOSSARY-AUXILIARY-PROC "Auxiliary process")*]](glossário.md#GLOSSÁRIO-AUXILIAR-PROC) que, se habilitado, escreve informações sobre eventos do banco de dados no arquivo de registro atual [*[arquivo de registro][(glossary.md#GLOSSARY-LOG-FILE "Log file")*]](glossário.md#GLOSSÁRIO-LOG-FILE). Quando atinge certos critérios dependentes do tempo ou do volume, um novo arquivo de registro é criado. Também chamado de *syslogger*.

Para mais informações, consulte [Seção 19.8](runtime-config-logging.md).

Clúster de replicação lógica: Um conjunto de instâncias de publicador e assinante, onde a instância de publicador replica as alterações para a instância de assinante.

Registro de registro: termo arcaico para um [*[WAL record](glossary.md#GLOSSARY-WAL-RECORD "WAL record")*](glossário.md#GLOSSARY-WAL-RECORD).

Número de sequência de registro (LSN): Deslocamento de byte no [*[WAL](glossary.md#GLOSSARY-WAL)]*(glossary.md#GLOSSARY-WAL), aumentando de forma monótona com cada novo [*[WAL record](glossary.md#GLOSSARY-WAL-RECORD)]*(glossary.md#GLOSSARY-WAL-RECORD).

Para mais informações, consulte `pg_lsn`(datatype-pg-lsn.md "8.20. pg_lsn Type") e [Seção 28.6](wal-internals.md "28.6. WAL Internals").

LSN: Veja [Número da sequência do log](glossary.md#GLOSSARY-LOG-SEQUENCE-NUMBER).

Mestre (servidor): Veja [Primaria (servidor)](glossary.md#GLOSSARY-PRIMARY-SERVER).

Materializado: A propriedade de que algumas informações foram pré-computadas e armazenadas para uso posterior, em vez de serem computadas em tempo real.

Este termo é usado em [*[materialized view](glossary.md#GLOSSARY-MATERIALIZED-VIEW "Materialized view (relation)](glossary.md#GLOSSARY-MATERIALIZED-VIEW) para indicar que os dados derivados da consulta da visão são armazenados em disco separadamente das fontes desses dados.

Esse termo também é usado para se referir a algumas consultas de vários passos, indicando que os dados resultantes da execução de um determinado passo são armazenados na memória (com a possibilidade de spill para o disco), para que possam ser lidos várias vezes por outro passo.

Visão materializada (relação): Um [*[relation](glossary.md#GLOSSARY-RELATION "Relation")*](glossary.md#GLOSSARY-RELATION) que é definido por uma declaração `SELECT` (assim como uma [*[view](glossary.md#GLOSSARY-VIEW "View")*](glossary.md#GLOSSARY-VIEW)), mas armazena dados da mesma maneira que uma [*[table](glossary.md#GLOSSARY-TABLE "Table")*](glossary.md#GLOSSARY-TABLE). Não pode ser modificada por meio das operações `INSERT`, `UPDATE`, `DELETE` ou `MERGE`.

Para mais informações, consulte [CREATE MATERIALIZED VIEW](sql-creatematerializedview.md "CREATE MATERIALIZED VIEW").

Merge: Um comando SQL usado para adicionar, modificar ou remover condicionalmente [*[rows][(glossary.md#GLOSSARY-TUPLE "Tuple")*]](glossário.md#GLOSSARY-TUPLE) em uma [*[table][(glossary.md#GLOSSARY-TABLE "Table")*]](glossário.md#GLOSSARY-TABLE] dada, usando dados de uma fonte [*[relation][(glossary.md#GLOSSARY-RELATION "Relation")*]](glossário.md#GLOSSARY-RELATION).

Para mais informações, consulte [MERGE](sql-merge.md).

Controle de concorrência de múltiplas versões (MVCC): Um mecanismo projetado para permitir que várias [*[transações](glossary.md#GLOSSARY-TRANSACTION)]*(glossary.md#GLOSSARY-TRANSACTION) leiam e escrevam as mesmas linhas sem que um processo cause o bloqueio de outros processos. No PostgreSQL, o MVCC é implementado criando cópias (*versões*) de [*[tuplas](glossary.md#GLOSSARY-TUPLE)]*(glossary.md#GLOSSARY-TUPLE) à medida que são modificadas; após as transações que podem ver as versões antigas terminarem, essas versões antigas precisam ser removidas.

Nulo: Um conceito de não existência que é um princípio central da teoria de banco de dados relacional. Representa a ausência de um valor definido.

Otimizador: Veja [Planejador de consulta](glossary.md#GLOSSARY-PLANNER).

Pergunta paralela: A capacidade de lidar com partes da execução de uma [*[query](glossary.md#GLOSSARY-QUERY "Query")*] (glossário.md#GLOSSARY-QUERY) para aproveitar processos paralelos em servidores com múltiplos CPUs.

Particionamento: Um dos vários subconjuntos disjuntos (não sobrepostos) de um conjunto maior. Em referência a uma tabela [*[particionada](glossary.md#GLOSSARY-PARTITIONED-TABLE)(glossary.md#GLOSSARY-PARTITIONED-TABLE)]: Uma das tabelas que cada uma contém parte dos dados da tabela particionada, que é chamada de *padrão*. A partição é, por si só, uma tabela, portanto, também pode ser consultada diretamente; ao mesmo tempo, uma partição pode, às vezes, ser uma tabela particionada, permitindo a criação de hierarquias. Em referência a uma [*[função de janela](glossary.md#GLOSSARY-WINDOW-FUNCTION)(glossary.md#GLOSSARY-WINDOW-FUNCTION) em uma [*[consulta](glossary.md#GLOSSARY-QUERY)(glossary.md#GLOSSARY-QUERY)], a partição é um critério definido pelo usuário que identifica quais [*[linhas](glossary.md#GLOSSARY-TUPLE)(glossary.md#GLOSSARY-TUPLE] vizinhas do [*[conjunto de resultados da consulta](glossary.md#GLOSSARY-RESULT-SET)(glossary.md#GLOSSARY-RESULT-SET) da função podem ser consideradas.

Tabela particionada (relação): Um [*[relation](glossary.md#GLOSSARY-RELATION "Relation")*](glossary.md#GLOSSARY-RELATION) que, em termos semânticos, é o mesmo que uma [*[table](glossary.md#GLOSSARY-TABLE "Table")*](glossary.md#GLOSSARY-TABLE), mas cuja armazenagem é distribuída em várias [*[partitions](glossary.md#GLOSSARY-PARTITION "Partition")*](glossary.md#GLOSSARY-PARTITION).

Correio-postal (processo): O primeiro processo de um [*[instância](glossary.md#GLOSSARY-INSTANCE "Instance")*](glossary.md#GLOSSARY-INSTANCIA). Ele inicia e gerencia os [*[processos auxiliares](glossary.md#GLOSSARY-AUXILIARY-PROC "Auxiliary process")*](glossary.md#GLOSSARY-AUXILIARY-PROC) e cria [*[processos de backend](glossary.md#GLOSSARY-BACKEND "Backend (process)"]*(glossary.md#GLOSSARY-BACKEND) sob demanda.

Para mais informações, consulte [Seção 18.3](server-start.md).

Chave primária: Um caso especial de uma [*[constrangimento único](glossary.md#GLOSSARY-UNIQUE-CONSTRAINT "Unique constraint")*](glossary.md#GLOSSARY-UNIQUE-CONSTRAINT) definida em uma [*[tabela](glossary.md#GLOSSARY-TABLE "Table")*](glossary.md#GLOSSARY-TABLE) ou outra [*[relação](glossary.md#GLOSSARY-RELATION "Relation")*](glossary.md#GLOSSARY-RELATION) que também garante que todos os [*[atributos](glossary.md#GLOSSARY-ATTRIBUTE "Attribute")*](glossary.md#GLOSSARY-ATTRIBUTE) dentro da [*[chave primária](glossary.md#GLOSSARY-PRIMARY-KEY "Primary key")*](glossary.md#GLOSSARY-PRIMARY-KEY) não tenham valores de [*[nulo](glossary.md#GLOSSARY-NULL "Null")*](glossary.md#GLOSSARY-NULL). Como o nome sugere, pode haver apenas uma chave primária por tabela, embora seja possível ter múltiplos constrangimentos únicos que também não têm atributos capazes de conter nulos.

Primaria (servidor): Quando dois ou mais [*[databases][(glossary.md#GLOSSARY-DATABASE "Database")*]](glossary.md#GLOSSARY-DATABASE) são vinculados por meio de [*[replication][(glossary.md#GLOSSARY-REPLICATION "Replication")*]](glossary.md#GLOSSARY-REPLICATION], o [*[server][(glossary.md#GLOSSARY-SERVER "Server")*]](glossary.md#GLOSSARY-SERVER] que é considerado a fonte de informação autoritária é chamado de *primario*, também conhecido como *mestre*.

Procedimento (rotineiro): Um tipo de procedimento rotineiro. Suas qualidades distintas são que eles não retornam valores e que é permitido fazer declarações transacionais, como `COMMIT` e `ROLLBACK`. Eles são invocados através do comando `CALL`.

Para mais informações, consulte [CREATE PROCEDURE](sql-createprocedure.md "CREATE PROCEDURE").

Pergunta: Um pedido enviado por um cliente para um [*[backend](glossary.md#GLOSSARY-BACKEND "Backend (process)]")*](glossary.md#GLOSSARY-BACKEND), geralmente para retornar resultados ou modificar dados no banco de dados.

Planificador de consultas: A parte do PostgreSQL que se dedica a determinar (* planejar *) a maneira mais eficiente de executar [*[consultas](glossary.md#GLOSSARY-QUERY "Query")*] (glossário.md#GLOSSARY-QUERY). Também conhecida como * otimizador de consultas */, * otimizador * ou simplesmente * planejador *.

Registro: Ver [Tubo](glossary.md#GLOSSARY-TUPLE).

Reciclagem: Veja o arquivo [WAL](glossary.md#GLOSSARY-WAL-FILE).

Integridade referencial: Um meio de restringir dados em uma [*[relação](glossary.md#GLOSSARY-RELATION "Relation")*](glossary.md#GLOSSARY-RELATION) por meio de uma [*[chave estrangeira](glossary.md#GLOSSARY-FOREIGN-KEY "Foreign key")*](glossary.md#GLOSSARY-FOREIGN-KEY) para que ela deva ter dados correspondentes em outra [*[relação](glossary.md#GLOSSARY-RELATION "Relation")*](glossary.md#GLOSSARY-RELATION).

Relação: O termo genérico para todos os objetos em um [*[database](glossary.md#GLOSSARY-DATABASE "Database")*](glossary.md#GLOSSARY-DATABASE) que têm um nome e uma lista de [*[attributes](glossary.md#GLOSSARY-ATTRIBUTE "Attribute")*](glossary.md#GLOSSARY-ATTRIBUTE) definidos em uma ordem específica. [*[Tables](glossary.md#GLOSSARY-TABLE "Table")*](glossary.md#GLOSSARY-TABLE), [*[sequences](glossary.md#GLOSSARY-SEQUENCE "Sequence (relation)")*](glossary.md#GLOSSARY-SEQUENCE), [*[views](glossary.md#GLOSSARY-VIEW "View")*](glossary.md#GLOSSARY-VIEW), [*[foreign tables](glossary.md#GLOSSARY-FOREIGN-TABLE "Foreign table (relation)")*](glossary.md#GLOSSARY-FOREIGN-TABLE), [*[materialized views](glossary.md#GLOSSARY-MATERIALIZED-VIEW "Materialized view (relation)")*](glossary.md#GLOSSARY-MATERIALIZED-VIEW), tipos compostos e [*[indexes](glossary.md#GLOSSARY-INDEX "Index (relation)")*](glossary.md#GLOSSARY-INDEX) são todas relações.

Mais genericamente, uma relação é um conjunto de tuplas; por exemplo, o resultado de uma consulta também é uma relação.

Em PostgreSQL, *Class* é um sinônimo arcaico para *relação*.

Replica (servidor): Um [*[database](glossary.md#GLOSSARY-DATABASE)*](glossary.md#GLOSSARY-DATABASE) que está emparelhado com um [*[primary](glossary.md#GLOSSARY-PRIMARY-SERVER)*]](glossary.md#GLOSSARY-PRIMARY-SERVER) banco de dados e está mantendo uma cópia de alguns ou todos os dados do banco de dados principal. As principais razões para fazer isso são permitir um maior acesso a esses dados e manter a disponibilidade dos dados no caso de o [*[primary](glossary.md#GLOSSARY-PRIMARY-SERVER)*]](glossary.md#GLOSSARY-PRIMARY-SERVER) se tornar indisponível.

Replicação: O ato de reproduzir dados em um [*[server](glossary.md#GLOSSARY-SERVER)]*(glossário.md#GLOSSARY-SERVER) em outro servidor chamado [*[replica](glossary.md#GLOSSARY-REPLICA)"]*(glossário.md#GLOSSARY-REPLICA). Isso pode assumir a forma de *replicação física*, onde todas as alterações de arquivo de um servidor são copiadas literalmente, ou *replicação lógica*, onde um subconjunto definido de alterações de dados é transmitido usando uma representação de nível superior.

Ponto de reinício: Uma variante de um [*[checkpoint][(glossary.md#GLOSSARY-CHECKPOINT "Checkpoint")*]](glossário.md#GLÓSSICA-CHECKPOINT) realizada em um [*[replica][(glossary.md#GLOSSARY-REPLICA "Replica (server)*]](glossário.md#GLÓSSICA-REPLICA).

Para mais informações, consulte [Seção 28.5](wal-configuration.md).

Conjunto de resultados: Um [*[processo de backend](glossary.md#GLOSSARY-BACKEND "Backend (process)*](glossary.md#GLOSSARY-BACKEND) transmitido de um [*[processo de backend][(glossary.md#GLOSSARY-BACKEND "Backend (process)*]](glossary.md#GLOSSARY-BACKEND) para um [*[cliente][(glossary.md#GLOSSARY-CLIENT "Client (process)*]](glossary.md#GLOSSARY-CLIENT] após a conclusão de um comando SQL, geralmente um `SELECT`, mas pode ser um comando `INSERT`, `UPDATE`, `DELETE`, ou `MERGE` se a cláusula `RETURNING` for especificada.

O fato de que um conjunto de resultados é uma relação significa que uma consulta pode ser usada na definição de outra consulta, tornando-se uma *subconsulta*.

Revocar: Um comando para impedir o acesso a um conjunto nomeado de objetos de [*[database](glossary.md#GLOSSARY-DATABASE)(glossary.md#GLOSSARY-DATABASE)](glossary.md#GLOSSARY-DATABASE) para uma lista nomeada de [*[roles](glossary.md#GLOSSARY-ROLE)(glossary.md#GLOSSARY-ROLE)](glossary.md#GLOSSARY-ROLE].

Para mais informações, consulte [REVOKE](sql-revoke.md "REVOKE").

Papel: Uma coleção de privilégios de acesso ao [*[instância](glossary.md#GLOSSARY-DATABASE)]*(glossary.md#GLOSSARY-DATABASE). Os papéis são, por si mesmos, um privilégio que pode ser concedido a outros papéis. Isso é frequentemente feito por conveniência ou para garantir a integridade quando vários [*[usuários](glossary.md#GLOSSARY-USER)]*(glossary.md#GLOSSARY-USER) precisam dos mesmos privilégios.

Para mais informações, consulte [Crie um papel](sql-createrole.md).

Reverter: Um comando para desfazer todas as operações realizadas desde o início de uma [*[transação](glossary.md#GLOSSARY-TRANSACTION "Transaction")*](glossário.md#GLÓSSICA-TRANSACÃO).

Para mais informações, consulte [ROLLBACK](sql-rollback.md).

Rotina: Um conjunto definido de instruções armazenadas no sistema de banco de dados que podem ser invocadas para execução. Uma rotina pode ser escrita em uma variedade de linguagens de programação. As rotinas podem ser [*[funções](glossary.md#GLOSSARY-FUNCTION "Function (routine)]")*](glossary.md#GLOSSARY-FUNCTION) (incluindo funções que retornam conjuntos e [*[funções de disparo](glossary.md#GLOSSARY-TRIGGER "Trigger")*]")*](glossary.md#GLOSSARY-TRIGGER)), [*[funções agregadas](glossary.md#GLOSSARY-AGGREGATE "Aggregate function (routine)]")*](glossary.md#GLOSSARY-AGGREGATE) e [*[procedimentos](glossary.md#GLOSSARY-PROCEDURE "Procedure (routine)]")*](glossary.md#GLOSSARY-PROCEDURE).

Muitas rotinas já estão definidas dentro do PostgreSQL em si, mas também é possível adicionar rotinas definidas pelo usuário.

Linha: Veja [Tubo](glossary.md#GLOSSARY-TUPLE).

Ponto de salvamento: Uma marca especial na sequência de etapas em uma [*[transação](glossary.md#GLOSSARY-TRANSACTION)]*] (glossário.md#GLOSSARY-TRANSACTION). As modificações de dados após este ponto no tempo podem ser revertidas para o momento do ponto de salvamento.

Para mais informações, consulte [SAVEPOINT](sql-savepoint.md).

Esquema: Um esquema é um espaço de nomes para [*[objetos SQL][(glossary.md#GLOSSARY-SQL-OBJECT "SQL object")*]](glossário.md#GLÓSSICO-OBJETO-SQL), que todos residem no mesmo [*[banco de dados][(glossary.md#GLOSSARY-DATABASE "Database")*]](glossário.md#GLÓSSICO-BANCO-DE-DADOS). Cada objeto SQL deve residir exatamente em um esquema.

Todos os objetos SQL definidos pelo sistema residem no esquema `pg_catalog`.: Mais genericamente, o termo *esquema* é usado para significar todas as descrições de dados ([*[tabela](glossary.md#GLOSSARY-TABLE "Table")*](glossary.md#GLOSSARY-TABLE) definições, [*[restrições](glossary.md#GLOSSARY-CONSTRAINT "Constraint")*](glossary.md#GLOSSARY-CONSTRAINT), comentários, etc.) para um dado [*[banco de dados](glossary.md#GLOSSARY-DATABASE "Database")*](glossary.md#GLOSSARY-DATABASE) ou subconjunto do mesmo.

Para mais informações, consulte [Seção 5.10](ddl-schemas.md).

Segmento: Veja [Segmento de arquivo](glossary.md#GLOSSARY-FILE-SEGMENT).

Selecione: O comando SQL usado para solicitar dados de um [*[database](glossary.md#GLOSSARY-DATABASE "Database")*](glossary.md#GLOSSARY-DATABASE). Normalmente, não se espera que os comandos `SELECT` modifiquem o [*[database](glossary.md#GLOSSARY-DATABASE "Database")*](glossary.md#GLOSSARY-DATABASE) de qualquer maneira, mas é possível que as funções [*[(glossary.md#GLOSSARY-FUNCTION "Function (routine)]]")[*](glossary.md#GLOSSARY-FUNCTION) invocadas dentro da consulta possam ter efeitos colaterais que modifiquem os dados.

Para mais informações, consulte [SELECT](sql-select.md "SELECT").

Sequência (relação): Um tipo de relação que é usado para gerar valores. Tipicamente, os valores gerados são números não repetitivos sequenciais. Eles são comumente usados para gerar valores de surogate [*[chave primária](glossary.md#GLOSSARY-PRIMARY-KEY "Primary key")*](glossário.md#GLOSSARY-PRIMARY-KEY) (glossário.md#GLOSSARY-PRIMARY-KEY).

Servidor: Um computador no qual o PostgreSQL [*[instances][(glossary.md#GLOSSARY-INSTANCE "Instance")*]](glossário.md#GLÓSSIO-INSTÂNCIA) é executado. O termo *servidor* denota hardware real, um contêiner ou uma *máquina virtual*.

Esse termo é usado às vezes para se referir a uma instância ou a um hospedeiro.

Sessão: Um estado que permite que um cliente e um backend interajam, comunicando-se através de uma [*[conexão](glossary.md#GLOSSARY-CONNECTION)*]](glossário.md#GLÓSSARIO-CONEXÃO).

Memória compartilhada: RAM que é usada pelos processos comuns a uma [*[instância](glossary.md#GLOSSARY-INSTANCE "Instance")*](glossary.md#GLOSSARY-INSTANCE). Ela espelha partes dos arquivos de [*[banco de dados](glossary.md#GLOSSARY-DATABASE "Database")*](glossary.md#GLOSSARY-DATABASE), fornece uma área transitória para [*[registros WAL](glossary.md#GLOSSARY-WAL-RECORD "WAL record")*](glossary.md#GLOSSARY-WAL-RECORD) e armazena informações adicionais comuns. Note que a memória compartilhada pertence à instância completa, não a um único banco de dados.

A maior parte da memória compartilhada é conhecida como *tampões compartilhados* e é usada para espelhar parte dos arquivos de dados, organizados em páginas. Quando uma página é modificada, ela é chamada de página suja até que seja escrita de volta ao sistema de arquivos.

Para mais informações, consulte [Seção 19.4.1](runtime-config-resource.md#RUNTIME-CONFIG-RESOURCE-MEMORY).

Objeto SQL: Qualquer objeto que pode ser criado com um comando `CREATE`. A maioria dos objetos é específica para um banco de dados e é comumente conhecida como *objetos locais*.

A maioria dos objetos locais reside em um [*[schema](glossary.md#GLOSSARY-SCHEMA "Schema")*](glossary.md#GLOSSARY-SCHEMA) específico em seu banco de dados de conteúdo, como [*[relations](glossary.md#GLOSSARY-RELATION "Relation")*](glossary.md#GLOSSARY-RELATION) (todos os tipos), [*[routines](glossary.md#GLOSSARY-FUNCTION "Function (routine)"]*(glossary.md#GLOSSARY-FUNCTION) (todos os tipos), tipos de dados, etc. Os nomes desses objetos do mesmo tipo no mesmo esquema são obrigatoriamente únicos.

Existem também objetos locais que não residem em esquemas; alguns exemplos são [*[extensions](glossary.md#GLOSSARY-EXTENSION)*](glossary.md#GLOSSARY-EXTENSION), [*[data type casts](glossary.md#GLOSSARY-CAST)*](glossary.md#GLOSSARY-CAST) e [*[foreign data wrappers](glossary.md#GLOSSARY-FOREIGN-DATA-WRAPPER)*](glossary.md#GLOSSARY-FOREIGN-DATA-WRAPPER). Os nomes desses objetos do mesmo tipo são obrigatoriamente únicos dentro do banco de dados.

Outros tipos de objetos, como [*[roles](glossary.md#GLOSSARY-ROLE "Role")*](glossary.md#GLOSSARY-ROLE), [*[tablespaces](glossary.md#GLOSSARY-TABLESPACE "Tablespace")*](glossary.md#GLOSSARY-TABLESPACE), origens de replicação, assinaturas para replicação lógica e os próprios bancos de dados não são objetos SQL locais, pois existem inteiramente fora de qualquer banco de dados específico; eles são chamados de *objetos globais*. Os nomes desses objetos são obrigatórios a serem únicos dentro de todo o clúster de bancos de dados.

Para mais informações, consulte [Seção 22.1](manage-ag-overview.md).

Padrão SQL: Uma série de documentos que definem a linguagem SQL.

Estacionamento (servidor): Veja [Replica (servidor)](glossary.md#GLOSSARY-REPLICA).

Processo de inicialização: Um [*[processo auxiliar][(glossary.md#GLOSSARY-AUXILIARY-PROC "Auxiliary process")*]](glossário.md#GLOSSÁRIO-AUXILIAR-PROC) que retransmite o WAL durante a recuperação em caso de falha e em um [*[replica física][(glossary.md#GLOSSARY-REPLICATION "Replication")*]](glossário.md#GLOSSÁRIO-REPLICAÇÃO).

(O nome é histórico: o processo de inicialização foi nomeado antes da implementação da replicação; o nome se refere à sua tarefa, pois se relaciona com a inicialização do servidor após um acidente.)

Superusuário: Como usado nesta documentação, é sinônimo de [*[database superuser](glossary.md#GLOSSARY-DATABASE-SUPERUSER)*]](glossário.md#GLÓSSICA-SUPERUSUÁRIO).

Catálogo do sistema: Uma coleção de [*[tabelas](glossary.md#GLOSSARY-TABLE)]*(glossary.md#GLOSSARY-TABLE) que descrevem a estrutura de todos os [*[objetos SQL](glossary.md#GLOSSARY-SQL-OBJECT)]*(glossary.md#GLOSSARY-SQL-OBJECT) da instância. O catálogo do sistema reside no esquema `pg_catalog`. Essas tabelas contêm dados em representação interna e geralmente não são consideradas úteis para exame do usuário; vários [*[visões](glossary.md#GLOSSARY-VIEW)]*(glossary.md#GLOSSARY-VIEW), também no esquema `pg_catalog`, oferecem acesso mais conveniente a algumas dessas informações, enquanto tabelas e visões adicionais existem no esquema `information_schema` (ver [Capítulo 35](information-schema.md)) que expõem algumas das mesmas e informações adicionais conforme exigido pelo [*[padrão SQL](glossary.md#GLOSSARY-SQL-STANDARD)]*(glossary.md#GLOSSARY-SQL-STANDARD).

Para mais informações, consulte [Seção 5.10](ddl-schemas.md).

Tabela: Uma coleção de [*[tuples](glossary.md#GLOSSARY-TUPLE "Tuple")*](glossary.md#GLOSSARY-TUPLE) com uma estrutura de dados comum (o mesmo número de [*[attributes](glossary.md#GLOSSARY-ATTRIBUTE "Attribute")*](glossary.md#GLOSSARY-ATTRIBUTE), na mesma ordem, com o mesmo nome e tipo por posição). Uma tabela é a forma mais comum de [*[relation](glossary.md#GLOSSARY-RELATION "Relation")*](glossary.md#GLOSSARY-RELATION) em PostgreSQL.

Para mais informações, consulte [CREATE TABLE](sql-createtable.md "CREATE TABLE").

Tablespace: Um local nomeado no sistema de arquivos do servidor. Todos os [*[objetos SQL][(glossary.md#GLOSSARY-SQL-OBJECT "SQL object")*]](glossário.md#GLÓSSICO-SQL-OBJETO) que requerem armazenamento além de sua definição no [*[catálogo do sistema][(glossary.md#GLOSSARY-SYSTEM-CATALOG "System catalog")*]](glossário.md#GLÓSSICO-CATÁLOGO-SISTEMA) devem pertencer a um único tablespace. Inicialmente, um grupo de bancos de dados contém um único tablespace utilizável que é usado como padrão para todos os objetos SQL, chamado `pg_default`.

Para mais informações, consulte [Seção 22.6](manage-ag-tablespaces.md).

Tabela temporária: [*[Tables](glossary.md#GLOSSARY-TABLE "Table")*](glossary.md#GLOSSARY-TABLE) que existem para a vida útil de uma [*[session](glossary.md#GLOSSARY-SESSION "Session")*](glossary.md#GLOSSARY-SESSION) ou uma [*[transaction](glossary.md#GLOSSARY-TRANSACTION "Transaction")*](glossary.md#GLOSSARY-TRANSACTION), conforme especificado no momento da criação. Os dados nelas não são visíveis para outras sessões e não são [*[logged](glossary.md#GLOSSARY-LOGGED "Logged")*](glossary.md#GLOSSARY-LOGGED). As tabelas temporárias são frequentemente usadas para armazenar dados intermediários para uma operação em várias etapas.

Para mais informações, consulte [CREATE TABLE](sql-createtable.md "CREATE TABLE").

TOAST: Um mecanismo pelo qual grandes atributos das linhas da tabela são divididos e armazenados em uma tabela secundária, chamada de *tabela TOAST*. Cada relação com atributos grandes tem sua própria tabela TOAST.

Para mais informações, consulte [Seção 66.2](storage-toast.md).

Transação: Uma combinação de comandos que devem agir como um único comando [*[atomic](glossary.md#GLOSSARY-ATOMIC "Atomic")*](glossary.md#GLOSSARY-ATOMIC) (glossário.md#GLOSSARY-ATOMIC): todos eles têm sucesso ou falham como uma única unidade, e seus efeitos não são visíveis para outros [*[sessions](glossary.md#GLOSSARY-SESSION "Session")*](glossary.md#GLOSSARY-SESSION) até que a transação esteja completa, e possivelmente até depois, dependendo do nível de isolamento.

Para mais informações, consulte [Seção 13.2](transaction-iso.md).

ID da transação: O identificador numérico, único e sequencialmente atribuído que cada transação recebe quando causa pela primeira vez uma modificação no banco de dados. Frequentemente abreviado como *xid*. Quando armazenado em disco, os xids têm apenas 32 bits de largura, portanto, apenas aproximadamente quatro bilhões de IDs de transação de escrita podem ser gerados; para permitir que o sistema funcione por mais tempo do que isso, *épocas* são usadas, também de 32 bits de largura. Quando o contador atinge o valor máximo do xid, ele começa novamente em `3` (os valores abaixo disso são reservados) e o valor da época é incrementado em um. Em alguns contextos, os valores da época e do xid são considerados juntos como um único valor de 64 bits; consulte [Seção 67.1](transaction-id.md) para mais detalhes.

Para mais informações, consulte [Seção 8.19](datatype-oid.md).

Transações por segundo (TPS): Número médio de transações executadas por segundo, totalizadas em todas as sessões ativas para uma execução medida. Isso é usado como uma medida das características de desempenho de uma instância.

Trigger: Um [*[function](glossary.md#GLOSSARY-FUNCTION "Function (routine)")*](glossary.md#GLOSSARY-FUNCTION) que pode ser definido para ser executado sempre que uma certa operação (`INSERT`, `UPDATE`, `DELETE`, `TRUNCATE`) é aplicada a uma [*[relation](glossary.md#GLOSSARY-RELATION "Relation")*](glossary.md#GLOSSARY-RELATION). Um trigger é executado dentro da mesma [*[transaction](glossary.md#GLOSSARY-TRANSACTION "Transaction")*](glossary.md#GLOSSARY-TRANSACTION) que a declaração que o invocou, e se a função falhar, então a declaração que a invocou também falha.

Para mais informações, consulte [CREATE TRIGGER](sql-createtrigger.md "CREATE TRIGGER").

Tuples: Uma coleção de [*[atributos][(glossary.md#GLOSSARY-ATTRIBUTE "Attribute")*]](glossary.md#GLOSSARY-ATTRIBUTE) em uma ordem fixa. Essa ordem pode ser definida pela [*[tabela][(glossary.md#GLOSSARY-TABLE "Table")*]](glossary.md#GLOSSARY-TABLE) (ou outra [*[relação][(glossary.md#GLOSSARY-RELATION "Relation")*]](glossary.md#GLOSSARY-RELATION)) onde o tuplo está contido, no caso, o tuplo é frequentemente chamado de *linha*. Também pode ser definido pela estrutura de um conjunto de resultados, no caso, é às vezes chamado de *registro*.

Restrição exclusiva: Um tipo de [*[constraint](glossary.md#GLOSSARY-CONSTRAINT "Constraint")*](glossary.md#GLOSSARY-CONSTRAINT) definido em uma [*[relation](glossary.md#GLOSSARY-RELATION "Relation")*](glossary.md#GLOSSARY-RELATION) que restringe os valores permitidos em uma ou uma combinação de colunas, de modo que cada valor ou combinação de valores só pode aparecer uma vez na relação — ou seja, nenhuma outra linha na relação contém valores iguais a esses.

Como [*[null values](glossary.md#GLOSSARY-NULL "Null")*](glossário.md#GLOSSARY-NULL) não são considerados iguais entre si, é permitido que existam várias linhas com valores nulos sem violar a restrição de unicidade.

Não registrada: A propriedade de certas relações [*[relations][(glossary.md#GLOSSARY-RELATION "Relation")*]](glossary.md#GLOSSARY-RELATION) de que as alterações nelas não são refletidas no [*[WAL][(glossary.md#GLOSSARY-WAL "Write-ahead log")*]](glossary.md#GLOSSARY-WAL). Isso desabilita a replicação e a recuperação em caso de falha para essas relações.

O uso principal das tabelas não registradas é armazenar dados de trabalho transitórios que devem ser compartilhados entre os processos.

[*[Tabelas temporárias](glossary.md#GLOSSARY-TEMPORARY-TABLE "Temporary table")*](glossário.md#GLOSSARY-TEMPORARY-TABLE) são sempre não registradas.

Atualização: Um comando SQL usado para modificar [*[rows](glossary.md#GLOSSARY-TUPLE "Tuple")*](glossary.md#GLOSSARY-TUPLE) que já pode existir em uma [*[table](glossary.md#GLOSSARY-TABLE "Table")*](glossary.md#GLOSSARY-TABLE) especificada. Não pode criar ou remover linhas.

Para mais informações, consulte [ATUALIZAÇÃO](sql-update.md "UPDATE").

Usuário: Um [*[role](glossary.md#GLOSSARY-ROLE "Role")*] (glossário.md#GLOSSARY-ROLE) que possui o *privilegio de login* (consulte [Seção 21.2](role-attributes.md "21.2. Role Attributes")).

Mapeamento do usuário: A tradução das credenciais de login no banco local [*[database](glossary.md#GLOSSARY-DATABASE)]*(glossary.md#GLOSSARY-DATABASE) para as credenciais em um sistema de dados remoto definido por um [*[foreign data wrapper](glossary.md#GLOSSARY-FOREIGN-DATA-WRAPPER)]*(glossary.md#GLOSSARY-FOREIGN-DATA-WRAPPER).

Para mais informações, consulte [CREATE USER MAPPING](sql-createusermapping.md "CREATE USER MAPPING").

UTC: Hora Universal Coordenada, a principal referência de tempo global, aproximadamente a hora que prevalece no meridiano zero de longitude. Frequentemente, mas incorretamente, referido como GMT (Hora Média de Greenwich).

Vacuamento: O processo de remoção de versões desatualizadas de [*[tuple versions](glossary.md#GLOSSARY-TUPLE "Tuple")*](glossary.md#GLOSSARY-TUPLE) de tabelas ou visualizações materializadas, e outros processos relacionados, exigidos pela implementação do [*[MVCC](glossary.md#GLOSSARY-MVCC "Multi-version concurrency control (MVCC)")*](glossary.md#GLOSSARY-MVCC] do PostgreSQL. Isso pode ser iniciado através do uso do comando `VACUUM` , mas também pode ser gerenciado automaticamente através dos processos de [*[autovacuum](glossary.md#GLOSSARY-AUTOVACUUM "Autovacuum (process)")*](glossary.md#GLOSSARY-AUTOVACUUM).

Para mais informações, consulte [Seção 24.1](routine-vacuuming.md).

Exibição: Um [*[relation](glossary.md#GLOSSARY-RELATION "Relation")*](glossário.md#GLOSSARY-RELATION) que é definido por uma declaração `SELECT`, mas não tem armazenamento próprio. Toda vez que uma consulta faz referência a uma exibição, a definição da exibição é substituída na consulta como se o usuário tivesse digitado como uma subconsulta em vez do nome da exibição.

Para mais informações, consulte [CREATE VIEW](sql-createview.md "CREATE VIEW").

Mapa de visibilidade (escada): Uma estrutura de armazenamento que mantém metadados sobre cada página de dados de um principal de uma tabela. A entrada do mapa de visibilidade para cada página armazena dois bits: o primeiro (`all-visible`) indica que todos os tuplos na página são visíveis para todas as transações. O segundo (`all-frozen`) indica que todos os tuplos na página estão marcados como congelados.

WAL: Veja [Registro prévio](glossary.md#GLOSSARY-WAL).

Arquivador WAL (processo): Um [*[processo auxiliar][(glossary.md#GLOSSARY-AUXILIARY-PROC "Auxiliary process")*]](glossary.md#GLOSSARY-AUXILIARY-PROC) que, se habilitado, salva cópias dos [*[arquivos WAL][(glossary.md#GLOSSARY-WAL-FILE "WAL file")*]](glossary.md#GLOSSARY-WAL-FILE) para a criação de backups ou para manter as [*[replicas][(glossary.md#GLOSSARY-REPLICA "Replica (server)*]](glossary.md#GLOSSARY-REPLICA) atualizadas.

Para mais informações, consulte [Seção 25.3](continuous-archiving.md)").

Arquivo WAL: Também conhecido como *segmento WAL* ou *arquivo de segmento WAL*. Cada um dos arquivos numerados sequencialmente que fornecem espaço de armazenamento para [*[WAL][(glossary.md#GLOSSARY-WAL "Write-ahead log")*]](glossário.md#GLÓSSARIO-WAL). Todos os arquivos têm o mesmo tamanho pré-definido e são escritos em ordem sequencial, intercalando as alterações conforme elas ocorrem em múltiplas sessões simultâneas. Se o sistema falhar, os arquivos são lidos em ordem e cada uma das alterações é reinterpretada para restaurar o sistema ao estado em que estava antes do crash.

Cada arquivo WAL pode ser liberado após o [*[checkpoint](glossary.md#GLOSSARY-CHECKPOINT)*](glossário.md#GLÓSSICO-CHECKPOINT) escrever todas as alterações nele nos arquivos de dados correspondentes. A liberação do arquivo pode ser feita por meio da sua exclusão ou da alteração de seu nome para que ele seja usado no futuro, o que é chamado de *reciclagem*.

Para mais informações, consulte [Seção 28.6](wal-internals.md).

Registro WAL: Uma descrição de baixo nível de uma alteração de dados individual. Ele contém informações suficientes para que a alteração de dados seja reexecutada (*replayed*) no caso de uma falha no sistema causar a perda da alteração. Os registros WAL utilizam um formato binário não imprimível.

Para mais informações, consulte [Seção 28.6](wal-internals.md).

Receptor WAL (processo): Um [*[processo auxiliar][(glossary.md#GLOSSARY-AUXILIARY-PROC "Auxiliary process")*]](glossário.md#GLÓSSIO-AUXILIAR-PROC) que funciona em um [*[replica][(glossary.md#GLOSSARY-REPLICA "Replica (server)*]](glossário.md#GLÓSSIO-REPLICA) para receber o WAL do [*[servidor principal][(glossary.md#GLOSSARY-PRIMARY-SERVER "Primary (server)*]](glossário.md#GLÓSSIO-PRINCIPAL-SERVIDOR) para rejogo pelo [*[processo de inicialização][(glossary.md#GLOSSARY-STARTUP-PROCESS "Startup process")*]](glossário.md#GLÓSSIO-PROCESSO-DE-INICIALIZAÇÃO).

Para mais informações, consulte [Seção 26.2](warm-standby.md).

Segmento WAL: Veja [arquivo WAL](glossary.md#GLOSSARY-WAL-FILE).

O remetente WAL (processo): Um processo especial [*[backend process](glossary.md#GLOSSARY-BACKEND "Backend (process)]")*](glossary.md#GLOSSARY-BACKEND) que transmite WAL por uma rede. O terminal receptor pode ser um [*[receptor WAL](glossary.md#GLOSSARY-WAL-RECEIVER "WAL receiver (process)]")*](glossary.md#GLOSSARY-WAL-RECEIVER) em um [*[replica](glossary.md#GLOSSARY-REPLICA "Replica (server)]")*](glossary.md#GLOSSARY-REPLICA], [pg_receivewal](app-pgreceivewal.md "pg_receivewal"), ou qualquer outro programa cliente que fale o protocolo de replicação.

Resumo do WAL (processo): Um [*[processo auxiliar](glossary.md#GLOSSARY-AUXILIARY-PROC "Auxiliary process")*](glossário.md#GLOSSÁRIO-AUXILIAR-PROC) que resume os dados do WAL para [*[backup incremental](glossary.md#GLOSSARY-INCREMENTAL-BACKUP "Incremental backup")*](glossário.md#GLOSSÁRIO-BACKUP-INCREMENTAL).

Para mais informações, consulte [Seção 19.5.7](runtime-config-wal.md#RUNTIME-CONFIG-WAL-SUMMARIZATION).

escritor WAL (processo): Um [*[processo auxiliar](glossary.md#GLOSSARY-AUXILIARY-PROC "Auxiliary process")*](glossary.md#GLOSSARY-AUXILIARY-PROC) que escreve [*[registros WAL](glossary.md#GLOSSARY-WAL-RECORD "WAL record")*](glossary.md#GLOSSARY-WAL-RECORD) a partir de [*[memória compartilhada](glossary.md#GLOSSARY-SHARED-MEMORY "Shared memory")*](glossary.md#GLOSSARY-SHARED-MEMORY) para [*[arquivos WAL](glossary.md#GLOSSARY-WAL-FILE "WAL file")*](glossary.md#GLOSSARY-WAL-FILE).

Para mais informações, consulte [Seção 19.5](runtime-config-wal.md).

Função de janela (routine): Um tipo de [*[função](glossary.md#GLOSSARY-FUNCTION "Function (routine)]")*(glossary.md#GLOSSARY-FUNCTION) utilizada em uma [*[consulta](glossary.md#GLOSSARY-QUERY "Query")*](glossary.md#GLOSSARY-QUERY) que se aplica a uma [*[partição](glossary.md#GLOSSARY-PARTITION "Partition")*](glossary.md#GLOSSARY-PARTITION) do conjunto de resultados da consulta; o resultado da função é baseado em valores encontrados em [*[linhas](glossary.md#GLOSSARY-TUPLE "Tuple")*](glossary.md#GLOSSARY-TUPLE) da mesma partição ou quadro.

Todas as funções agregadas [*[aggregate functions](glossary.md#GLOSSARY-AGGREGATE))*](glossary.md#GLOSSARY-AGGREGATE) podem ser usadas como funções de janela, mas as funções de janela também podem ser usadas, por exemplo, para atribuir classificações a cada uma das linhas na partição. Também conhecidas como *funções analíticas*.

Para mais informações, consulte [Seção 3.5](tutorial-window.md).

Diário de escrita antecipada: O diário que acompanha as alterações nas operações invocadas pelo usuário e pelo sistema no [*[cluster de banco de dados][(glossary.md#GLOSSARY-DB-CLUSTER "Database cluster")*]](glossary.md#GLOSSARY-DB-CLUSTER). Ele compreende muitos [*[registros WAL][(glossary.md#GLOSSARY-WAL-RECORD "WAL record")*]](glossary.md#GLOSSARY-WAL-RECORD) escritos sequencialmente em [*[arquivos WAL][(glossary.md#GLOSSARY-WAL-FILE "WAL file")*]](glossary.md#GLOSSARY-WAL-FILE).