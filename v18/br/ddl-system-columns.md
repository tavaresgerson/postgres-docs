## 5.6. Colunas do sistema [#](#DDL-SYSTEM-COLUMNS)

Cada tabela tem várias *colunas do sistema* que são implicitamente definidas pelo sistema. Portanto, esses nomes não podem ser usados como nomes de colunas definidas pelo usuário. (Observe que essas restrições são separadas de acordo com o fato de o nome ser uma palavra-chave ou não; citar um nome não permitirá que você escape dessas restrições.) Você realmente não precisa se preocupar com essas colunas; apenas saiba que elas existem.

`tableoid` [#](#DDL-SYSTEM-COLUMNS-TABLEOID): O OID da tabela que contém esta linha. Esta coluna é particularmente útil para consultas que selecionam de tabelas particionadas (ver [Seção 5.12](ddl-partitioning.md "5.12. Table Partitioning")) ou hierarquias de herança (ver [Seção 5.11](ddl-inherit.md "5.11. Inheritance")), pois, sem ela, é difícil dizer de qual tabela individual uma linha veio. O `tableoid` pode ser associado à coluna `oid` de `pg_class` para obter o nome da tabela.

`xmin` [#](#DDL-SYSTEM-COLUMNS-XMIN): A identidade (ID de transação) da transação inserida para esta versão da linha. (Uma versão de linha é um estado individual de uma linha; cada atualização de uma linha cria uma nova versão de linha para a mesma linha lógica.)

`cmin` [#](#DDL-SYSTEM-COLUMNS-CMIN): O identificador de comando (iniciando em zero) dentro da transação de inserção.

`xmax` [#](#DDL-SYSTEM-COLUMNS-XMAX): A identidade (ID de transação) da transação que está sendo excluída, ou zero para uma versão de linha não excluída. É possível que essa coluna seja não nula em uma versão de linha visível. Isso geralmente indica que a transação que está sendo excluída ainda não foi confirmada, ou que uma tentativa de exclusão foi cancelada.

`cmax` [#](#DDL-SYSTEM-COLUMNS-CMAX): O identificador do comando na transação de exclusão, ou zero.

`ctid` [#](#DDL-SYSTEM-COLUMNS-CTID): A localização física da versão da linha dentro de sua tabela. Note que, embora o `ctid` possa ser usado para localizar a versão da linha muito rapidamente, o `ctid` de uma linha mudará se for atualizado ou movido por `VACUUM FULL`. Portanto, o `ctid` não deve ser usado como um identificador de linha. Uma chave primária deve ser usada para identificar linhas lógicas.

Os identificadores de transação também são quantidades de 32 bits. Em um banco de dados de longa duração, é possível que os IDs de transação se repitam. Isso não é um problema fatal, dado os procedimentos de manutenção adequados; consulte [Capítulo 24][(maintenance.md "Chapter 24. Routine Database Maintenance Tasks")] para detalhes. No entanto, é imprudente depender da unicidade dos IDs de transação a longo prazo (mais de um bilhão de transações).

Os identificadores de comando também são quantidades de 32 bits. Isso cria um limite rígido de 232 (4 bilhões) comandos SQL dentro de uma única transação. Na prática, esse limite não é um problema — observe que o limite está no número de comandos SQL, não no número de linhas processadas. Além disso, apenas os comandos que realmente modificam o conteúdo do banco de dados consumirão um identificador de comando.