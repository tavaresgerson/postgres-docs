## Capítulo 24. Tarefas rotineiras de manutenção de banco de dados

**Índice**

* [24.1. Aspiração de rotina](routine-vacuuming.md)

+ [24.1.1. Básico de Aspiração](routine-vacuuming.md#VACUUM-BASICS)
+ [24.1.2. Recuperação de Espaço em Disco](routine-vacuuming.md#VACUUM-FOR-SPACE-RECOVERY)
+ [24.1.3. Atualização das Estatísticas do Planejador](routine-vacuuming.md#VACUUM-FOR-STATISTICS)
+ [24.1.4. Atualização do Mapa de Visibilidade](routine-vacuuming.md#VACUUM-FOR-VISIBILITY-MAP)
+ [24.1.5. Prevenção de Falhas no Envoltório de ID de Transação](routine-vacuuming.md#VACUUM-FOR-WRAPAROUND)
+ [24.1.6. O Daemon de Autoaspiração](routine-vacuuming.md#AUTOVACUUM)

* [24.2. Reindexação de rotina](routine-reindex.md)
* [24.3. Manutenção de arquivo de registro](logfile-maintenance.md)

O PostgreSQL, como qualquer software de banco de dados, exige que certas tarefas sejam realizadas regularmente para alcançar o desempenho ótimo. As tarefas discutidas aqui são *requeridas*, mas são de natureza repetitiva e podem ser facilmente automatizadas usando ferramentas padrão, como scripts cron ou o Cron Scheduler do Windows. É responsabilidade do administrador do banco de dados configurar os scripts apropriados e verificar se eles são executados com sucesso.

Uma tarefa de manutenção óbvia é a criação de cópias de segurança dos dados em um cronograma regular. Sem uma cópia de segurança recente, você não tem chance de recuperação após uma catástrofe (falha de disco, incêndio, deixar acidentalmente uma tabela crítica, etc.). Os mecanismos de backup e recuperação disponíveis no PostgreSQL são discutidos em detalhes no [Capítulo 25][(backup.md "Chapter 25. Backup and Restore")].

A outra categoria principal de tarefa de manutenção é o "limpeza" periódica do banco de dados. Esta atividade é discutida em [Seção 24.1][(routine-vacuuming.md "24.1. Routine Vacuuming")]. Está intimamente relacionada a isso a atualização das estatísticas que serão usadas pelo planejador de consultas, conforme discutido em [Seção 24.1.3][(routine-vacuuming.md#VACUUM-FOR-STATISTICS "24.1.3. Updating Planner Statistics")].

Outra tarefa que pode exigir atenção periódica é a gestão de arquivos de registro. Isso é discutido em [Seção 24.3][(logfile-maintenance.md "24.3. Log File Maintenance")].

[check_postgres][(https://bucardo.org/check_postgres/)] está disponível para monitorar a saúde do banco de dados e relatar condições incomuns. O check_postgres se integra com o Nagios e o MRTG, mas também pode ser executado de forma independente.

O PostgreSQL é de baixa manutenção em comparação com alguns outros sistemas de gerenciamento de banco de dados. No entanto, a atenção adequada a essas tarefas contribuirá muito para garantir uma experiência agradável e produtiva com o sistema.