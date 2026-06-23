## 27.3. Visualização de bloqueios [#](#MONITORING-LOCKS)

Outra ferramenta útil para monitorar a atividade do banco de dados é a tabela do sistema `pg_locks`. Ela permite que o administrador do banco de dados visualize informações sobre as chaves pendentes no gerenciador de chaves. Por exemplo, essa capacidade pode ser usada para:

* Veja todas as chaves atualmente pendentes, todas as chaves em relações em um banco de dados específico, todas as chaves em uma relação específica ou todas as chaves mantidas por uma sessão específica do PostgreSQL. * Determine a relação no banco de dados atual com as chaves mais não concedidas (que pode ser uma fonte de contenção entre os clientes do banco de dados). * Determine o efeito da contenção de chaves no desempenho geral do banco de dados, bem como a extensão em que a contenção varia com o tráfego geral do banco de dados.

Os detalhes da visualização `pg_locks` aparecem em [Seção 53.13](view-pg-locks.md "53.13. pg_locks"). Para mais informações sobre bloqueio e gerenciamento de concorrência com PostgreSQL, consulte [Capítulo 13](mvcc.md "Chapter 13. Concurrency Control").