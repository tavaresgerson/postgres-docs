## 27.6. Monitoramento do uso do disco [#](#DISKUSAGE)

* [27.6.1. Determinação do uso do disco](diskusage.md#DISK-USAGE)
* [27.6.2. Falha de esgotamento do disco](diskusage.md#DISK-FULL)

Esta seção discute como monitorar o uso do disco de um sistema de banco de dados PostgreSQL.

### 27.6.1. Determinação do uso do disco [#](#DISK-USAGE)

Cada tabela tem um arquivo principal de disco de pilha onde a maioria dos dados é armazenada. Se a tabela tiver quaisquer colunas com valores potencialmente amplos, também pode haver um arquivo TOAST associado à tabela, que é usado para armazenar valores que são muito amplos para caber confortavelmente na tabela principal (ver [Seção 66.2](storage-toast.md)). Haverá um índice válido na tabela TOAST, se estiver presente. Também pode haver índices associados à tabela de base. Cada tabela e índice são armazenados em um arquivo de disco separado — possivelmente mais de um arquivo, se o arquivo exceder um gigabyte. As convenções de nomeação para esses arquivos são descritas em [Seção 66.1](storage-file-layout.md).

Você pode monitorar o espaço em disco de três maneiras: usando as funções SQL listadas em [Tabela 9.102](functions-admin.md#FUNCTIONS-ADMIN-DBSIZE), usando o módulo [oid2name](oid2name.md) ou usando inspeção manual dos catálogos do sistema. As funções SQL são as mais fáceis de usar e geralmente são recomendadas. O restante desta seção mostra como fazer isso por inspeção dos catálogos do sistema.

Usando o psql em um banco de dados recentemente aspirado ou analisado, você pode emitir consultas para ver o uso do disco de qualquer tabela:

```
SELECT pg_relation_filepath(oid), relpages FROM pg_class WHERE relname = 'customer';

 pg_relation_filepath | relpages
----------------------+----------
 base/16384/16806     |       60
(1 row)
```

Cada página é tipicamente de 8 kilobytes. (Lembre-se de que `relpages` é atualizado apenas por `VACUUM`, `ANALYZE` e alguns comandos DDL, como `CREATE INDEX`.]) O nome do caminho do arquivo é de interesse se você quiser examinar o arquivo do disco da tabela diretamente.

Para mostrar o espaço usado pelas tabelas TOAST, use uma consulta como a seguinte:

```
SELECT relname, relpages
FROM pg_class,
     (SELECT reltoastrelid
      FROM pg_class
      WHERE relname = 'customer') AS ss
WHERE oid = ss.reltoastrelid OR
      oid = (SELECT indexrelid
             FROM pg_index
             WHERE indrelid = ss.reltoastrelid)
ORDER BY relname;

       relname        | relpages
----------------------+----------
 pg_toast_16806       |        0
 pg_toast_16806_index |        1
```

Você pode facilmente exibir os tamanhos dos índices também:

```
SELECT c2.relname, c2.relpages
FROM pg_class c, pg_class c2, pg_index i
WHERE c.relname = 'customer' AND
      c.oid = i.indrelid AND
      c2.oid = i.indexrelid
ORDER BY c2.relname;

      relname      | relpages
-------------------+----------
 customer_id_index |       26
```

É fácil encontrar suas tabelas e índices maiores usando essas informações:

```
SELECT relname, relpages
FROM pg_class
ORDER BY relpages DESC;

       relname        | relpages
----------------------+----------
 bigtable             |     3290
 customer             |     3144
```

### 27.6.2. Falha de disco cheio [#](#DISK-FULL)

A tarefa mais importante de monitoramento de disco de um administrador de banco de dados é garantir que o disco não fique cheio. Um disco de dados cheio não resultará em corrupção de dados, mas pode impedir que atividades úteis ocorram. Se o disco que contém os arquivos WAL ficar cheio, o servidor de banco de dados pode entrar em pânico e sofrer um desligamento consequente.

Se você não conseguir liberar espaço adicional no disco, excluindo outras coisas, pode mover alguns dos arquivos do banco de dados para outros sistemas de arquivos, utilizando tablespaces. Consulte [Seção 22.6](manage-ag-tablespaces.md) para obter mais informações sobre isso.

### DICA

Alguns sistemas de arquivos apresentam desempenho ruim quando estão quase cheios, então não espere até que o disco esteja completamente cheio para tomar medidas.

Se o seu sistema suportar quotas de disco por usuário, então o banco de dados naturalmente estará sujeito à quota colocada no usuário pelo qual o servidor é executado. Exceder a quota terá os mesmos efeitos negativos que ficar sem espaço em disco.