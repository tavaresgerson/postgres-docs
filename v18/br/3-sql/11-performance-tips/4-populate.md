## 14.4. Populando um Banco de Dados [#](#POPULATE)

* [14.4.1. Desativar o Autocommit](populate.md#DISABLE-AUTOCOMMIT)
* [14.4.2. Usar `COPY`](populate.md#POPULATE-COPY-FROM)
* [14.4.3. Remover Índices](populate.md#POPULATE-RM-INDEXES)
* [14.4.4. Remover Restrições de Chave Estrangeira](populate.md#POPULATE-RM-FKEYS)
* [14.4.5. Aumentar `maintenance_work_mem`](populate.md#POPULATE-WORK-MEM)
* [14.4.6. Aumentar `max_wal_size`](populate.md#POPULATE-MAX-WAL-SIZE)
* [14.4.7. Desativar a Replicação Arquival e em Streaming de WAL](populate.md#POPULATE-PITR)
* [14.4.8. Executar `ANALYZE` Posteriormente](populate.md#POPULATE-ANALYZE)
* [14.4.9. Algumas Notas sobre pg_dump](populate.md#POPULATE-PG-DUMP)

Pode ser necessário inserir uma grande quantidade de dados ao primeiro preenchimento de um banco de dados. Esta seção contém algumas sugestões sobre como tornar esse processo o mais eficiente possível.

### 14.4.1. Desativar o Autocommit [#](#DISABLE-AUTOCOMMIT)

Ao usar vários `INSERT`s, desative o autocommit e faça apenas um commit no final. (Em SQL simples, isso significa emitir `BEGIN` no início e `COMMIT` no final. Algumas bibliotecas de cliente podem fazer isso por trás da sua cortina, nesse caso, você precisa se certificar de que a biblioteca faça isso quando você deseja que isso seja feito.) Se permitir que cada inserção seja realizada separadamente, o PostgreSQL está fazendo muito trabalho para cada linha que é adicionada. Um benefício adicional de realizar todas as inserções em uma transação é que, se a inserção de uma linha falhar, a inserção de todas as linhas inseridas até esse ponto será revertida, então você não ficará preso com dados parcialmente carregados.

### 14.4.2. Use `COPY` [#](#POPULATE-COPY-FROM)

Use `COPY`(sql-copy.md "COPY") para carregar todas as linhas em um comando, em vez de usar uma série de comandos `INSERT`. O comando `COPY` é otimizado para carregar um grande número de linhas; é menos flexível do que `INSERT`, mas incorre em um custo significativamente menor para cargas de dados grandes. Como `COPY` é um único comando, não há necessidade de desabilitar o autocommit se você usar esse método para preencher uma tabela.

Se você não puder usar `COPY`, pode ser útil usar `PREPARE` para criar uma declaração preparada (sql-prepare.md "PREPARE"), e depois usar `EXECUTE` quantas vezes for necessário. Isso evita parte do overhead de analisar e planejar `INSERT` repetidamente. Diferentes interfaces fornecem essa facilidade de maneiras diferentes; procure por “declarações preparadas” na documentação da interface.

Observe que carregar um grande número de linhas usando `COPY` é quase sempre mais rápido do que usar `INSERT`, mesmo se `PREPARE` for usado e várias inserções forem agrupadas em uma única transação.

`COPY` é mais rápido quando usado na mesma transação que um comando anterior `CREATE TABLE` ou `TRUNCATE`. Nesses casos, não é necessário escrever um WAL, porque, em caso de erro, os arquivos que contêm os dados recém-carregados serão removidos de qualquer maneira. No entanto, essa consideração só se aplica quando [wal_level](runtime-config-wal.md#GUC-WAL-LEVEL) é `minimal`, pois todos os comandos devem escrever WAL caso contrário.

### 14.4.3. Remova índices [#](#POPULATE-RM-INDEXES)

Se você está carregando uma tabela recém-criada, o método mais rápido é criar a tabela, carregar os dados da tabela em massa usando `COPY`, e, em seguida, criar quaisquer índices necessários para a tabela. Criar um índice em dados pré-existentes é mais rápido do que atualizá-los incrementalmente à medida que cada linha é carregada.

Se você está adicionando grandes quantidades de dados a uma tabela existente, pode ser uma boa ideia excluir os índices, carregar a tabela e, em seguida, recriar os índices. Claro, o desempenho do banco de dados para outros usuários pode sofrer durante o tempo em que os índices estão ausentes. Também se deve pensar duas vezes antes de excluir um índice único, pois o controle de erro oferecido pela restrição única será perdido enquanto o índice estiver ausente.

### 14.4.4. Remova restrições de chave estrangeira [#](#POPULATE-RM-FKEYS)

Assim como com índices, uma restrição de chave estrangeira pode ser verificada de forma mais eficiente em massa do que linha por linha. Portanto, pode ser útil descartar as restrições de chave estrangeira, carregar os dados e recriar as restrições. Novamente, há um compromisso entre a velocidade de carregamento de dados e a perda de verificação de erros enquanto a restrição está faltando.

Além disso, quando você carrega dados em uma tabela com restrições de chave estrangeira existentes, cada nova linha requer uma entrada na lista de eventos de gatilho pendentes do servidor (já que é o disparo de um gatilho que verifica a restrição de chave estrangeira da linha). Carregar muitos milhões de linhas pode fazer com que a fila de eventos de gatilho transborde a memória disponível, levando a um swap intolerável ou até mesmo ao fracasso total do comando. Portanto, pode ser *necessário*, não apenas desejável, descartar e reaplicar chaves estrangeiras ao carregar grandes quantidades de dados. Se a remoção temporária da restrição não for aceitável, o único outro recurso pode ser dividir a operação de carga em transações menores.

### 14.4.5. Aumentar `maintenance_work_mem` [#](#POPULATE-WORK-MEM)

Aumentar temporariamente a variável de configuração [maintenance_work_mem](runtime-config-resource.md#GUC-MAINTENANCE-WORK-MEM) ao carregar grandes quantidades de dados pode levar a um desempenho melhor. Isso ajudará a acelerar os comandos `CREATE INDEX` e os comandos `ALTER TABLE ADD FOREIGN KEY`. Não fará muito para o próprio `COPY`, então este conselho é útil apenas quando você está usando uma ou ambas as técnicas acima.

### 14.4.6. Aumentar `max_wal_size` [#](#POPULATE-MAX-WAL-SIZE)

Aumentar temporariamente a variável de configuração [max_wal_size](runtime-config-wal.md#GUC-MAX-WAL-SIZE) também pode tornar as cargas de dados grandes mais rápidas. Isso ocorre porque carregar uma grande quantidade de dados no PostgreSQL fará com que os pontos de verificação ocorram com mais frequência do que a frequência normal de verificação (especificada pela variável de configuração `checkpoint_timeout`). Sempre que ocorre um ponto de verificação, todas as páginas sujas devem ser descarregadas no disco. Ao aumentar temporariamente [[`max_wal_size`] durante cargas de dados em massa, o número de pontos de verificação necessários pode ser reduzido.

### 14.4.7. Desativar a Replicação de Arquivo e Streaming WAL [#](#POPULATE-PITR)

Ao carregar grandes quantidades de dados em uma instalação que utiliza arquivamento WAL ou replicação em fluxo, pode ser mais rápido fazer um novo backup de base após o carregamento ter sido concluído do que processar uma grande quantidade de dados WAL incrementais. Para evitar o registro incremental do WAL durante o carregamento, desative o arquivamento e a replicação em fluxo, definindo [wal_level](runtime-config-wal.md#GUC-WAL-LEVEL) para `minimal`, [archive_mode](runtime-config-wal.md#GUC-ARCHIVE-MODE) para `off` e [max_wal_senders](runtime-config-replication.md#GUC-MAX-WAL-SENDERS) para zero. No entanto, observe que alterar esses ajustes requer o reinício do servidor e torna quaisquer backups de base tomados anteriormente indisponíveis para recuperação de arquivo e servidor de espera, o que pode levar à perda de dados.

Além de evitar que o arquivador ou o remetente WAL processe os dados do WAL, fazer isso realmente tornará certos comandos mais rápidos, porque eles não escreverão WAL de forma alguma se `wal_level` for `minimal` e a subtransação atual (ou transação de nível superior) tenha criado ou truncado a tabela ou índice que eles alteram. (Eles podem garantir segurança em caso de falha de forma mais barata ao fazer um `fsync` no final do que escrevendo WAL.)

### 14.4.8. Execute `ANALYZE` Posteriormente [#](#POPULATE-ANALYZE)

Sempre que você tiver alterado significativamente a distribuição dos dados em uma tabela, é altamente recomendável executar `ANALYZE` (sql-analyze.md "ANALYZE"). Isso inclui o carregamento em massa de grandes quantidades de dados na tabela. Executar `ANALYZE` (ou `VACUUM ANALYZE`) garante que o planejador tenha estatísticas atualizadas sobre a tabela. Sem estatísticas ou estatísticas obsoletas, o planejador pode tomar decisões ruins durante o planejamento de consultas, levando a um desempenho ruim em quaisquer tabelas com estatísticas imprecisas ou inexistentes. Note que, se o daemon de autovazamento estiver habilitado, ele pode executar `ANALYZE` automaticamente; consulte [Seção 24.1.3](routine-vacuuming.md#VACUUM-FOR-STATISTICS) e [Seção 24.1.6](routine-vacuuming.md#AUTOVACUUM) para mais informações.

### 14.4.9. Algumas notas sobre pg_dump [#](#POPULATE-PG-DUMP)

Os scripts de exclusão gerados pelo pg_dump aplicam automaticamente várias, mas não todas, das diretrizes acima. Para restaurar um dump do pg_dump o mais rapidamente possível, você precisa fazer algumas coisas extras manualmente. (Observe que esses pontos se aplicam durante a *restauração* de um dump, não durante a *criação* dele. Os mesmos pontos se aplicam ao carregar um dump de texto com o psql ou ao usar o pg_restore para carregar a partir de um arquivo de arquivo pg_dump.)

Por padrão, o pg_dump usa `COPY`, e quando está gerando um dump completo de esquema e dados, ele é cuidadoso em carregar os dados antes de criar índices e chaves estrangeiras. Portanto, neste caso, várias diretrizes são tratadas automaticamente. O que você precisa fazer é:

* Defina valores apropriados (ou seja, maiores que o normal) para `maintenance_work_mem` e `max_wal_size`.
* Se estiver usando arquivamento WAL ou replicação em fluxo, considere desativá-los durante o restabelecimento. Para isso, defina `archive_mode` para `off`, `wal_level` para `minimal` e `max_wal_senders` para zero antes de carregar o dump. Depois, defina-os de volta aos valores corretos e faça um backup de base fresco.
* Experimente os modos de dump e restabelecimento paralelos de pg_dump e pg_restore e encontre o número ótimo de trabalhos concorrentes a usar. O dump e o restabelecimento em paralelo por meio da opção `-j` devem lhe proporcionar um desempenho significativamente maior em relação ao modo serial.
* Considere se o dump inteiro deve ser restaurado como uma única transação. Para isso, passe a opção de linha de comando `-1` ou `--single-transaction` ao psql ou ao pg_restore. Ao usar esse modo, até os menores erros irão fazer o rollback de todo o restabelecimento, possivelmente descartando muitas horas de processamento. Dependendo de quão interligados os dados estão, isso pode parecer preferível à limpeza manual, ou não. Os comandos `COPY` funcionarão mais rápido se você usar uma única transação e tiver arquivamento WAL desativado.
* Se houver vários CPUs disponíveis no servidor de banco de dados, considere usar a opção `--jobs` do pg_restore. Isso permite o carregamento de dados e a criação de índices concorrentes.
* Execute `ANALYZE` depois.

Um dump com apenas dados ainda usará `COPY`, mas ele não exclui ou recria índices e normalmente não toca em chaves estrangeiras. [[14]](#ftn.id-1.5.13.7.11.4.2) Portanto, ao carregar um dump com apenas dados, cabe a você excluir e recriar índices e chaves estrangeiras, se desejar usar essas técnicas. Ainda é útil aumentar `max_wal_size` ao carregar os dados, mas não se preocupe em aumentar `maintenance_work_mem`; em vez disso, você faria isso ao recarregar manualmente os índices e chaves estrangeiras posteriormente. E não se esqueça de `ANALYZE` quando estiver pronto; consulte [Seção 24.1.3](routine-vacuuming.md#VACUUM-FOR-STATISTICS "24.1.3. Updating Planner Statistics") e [Seção 24.1.6](routine-vacuuming.md#AUTOVACUUM "24.1.6. The Autovacuum Daemon") para mais informações.

---

[[14]](#id-1.5.13.7.11.4.2) Você pode obter o efeito de desabilitar chaves estrangeiras usando a opção `--disable-triggers` — mas perceba que isso elimina, em vez de apenas adiar, a validação de chaves estrangeiras, e, portanto, é possível inserir dados ruins se você usá-la.