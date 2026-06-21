## 68.5. Estrutura do arquivo Bootstrap BKI [#](#BKI-STRUCTURE)

O comando `open` não pode ser usado até que as tabelas que ele usa existam e tenham entradas para a tabela que deve ser aberta. (Essas tabelas mínimas são `pg_class`, `pg_attribute`, `pg_proc` e `pg_type`.)] Para permitir que essas tabelas sejam preenchidas, o `create` com a opção `bootstrap` abre implicitamente a tabela criada para inserção de dados.

Além disso, os comandos `declare index` e `declare toast` não podem ser usados até que os catálogos de sistema que eles precisam terem sido criados e preenchidos.

Assim, a estrutura do arquivo `postgres.bki` deve ser:

1. `create bootstrap` uma das tabelas críticas
2. `insert` dados que descrevam pelo menos as tabelas críticas
3. `close`
4. Repita para as outras tabelas críticas.
5. `create` (sem `bootstrap`) uma tabela não crítica
6. `open`
7. `insert` dados desejados
8. `close`
9. Repita para as outras tabelas não críticas.
10. Defina índices e tabelas de toast.
11. `build indices`

Sem dúvida, há outras dependências de ordem não documentadas.