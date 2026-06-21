## oid2name

oid2name — resolva OIDs e nós de arquivos em um diretório de dados do PostgreSQL

## Sinopse

`oid2name` [*`option`*...]

## Descrição

oid2name é um programa utilitário que ajuda os administradores a examinar a estrutura de arquivo usada pelo PostgreSQL. Para usá-lo, você precisa estar familiarizado com a estrutura de arquivo do banco de dados, que é descrita em [Capítulo 66][(storage.md "Chapter 66. Database Physical Storage")].

### Nota

O nome “oid2name” é histórico e, na verdade, é bastante enganoso, pois, na maioria das vezes, quando você o usa, você realmente estará preocupado com os números de filenode das tabelas (que são os nomes de arquivo visíveis nos diretórios do banco de dados). Certifique-se de entender a diferença entre OIDs de tabela e filenodes de tabela!

oid2name se conecta a um banco de dados de destino e extrai informações sobre OID, filenode e/ou nome de tabela. Você também pode fazer com que ele mostre OIDs do banco de dados ou OIDs do espaço de tabela.

## Opções

oid2name aceita os seguintes argumentos de linha de comando:

`-f filenode`: mostre informações para a tabela com filenode *`filenode`*.

`-i` `--indexes`: inclua índices e sequências na lista.

`-o oid` `--oid=oid`: mostre informações para a tabela com OID *`oid`*.

`-q` `--quiet`: omit headers (útil para scripts).

`-s` `--tablespaces`: mostre os IDs de espaço de tabela.

`-S` `--system-objects`: inclua objetos do sistema (aqueles nos esquemas de `information_schema`, `pg_toast` e `pg_catalog`).

`-t tablename_pattern` `--table=tablename_pattern`: mostre informações para a(s) tabela(s) que correspondem a *`tablename_pattern`*.

`-V` `--version`: Imprimir a versão oid2name e sair.

`-x` `--extended`: exiba mais informações sobre cada objeto exibido: nome do espaço de tabela, nome do esquema e OID.

`-?` `--help`: Mostrar ajuda sobre os argumentos de linha de comando do comando oid2name e sair.

oid2name também aceita os seguintes argumentos de linha de comando para os parâmetros de conexão:

`-d database` `--dbname=database`: banco de dados para se conectar.

`-h host` `--host=host`: host do servidor de banco de dados.

`-H host`: servidor de banco de dados host. O uso deste parâmetro é *descontinuado* a partir do PostgreSQL 12.

`-p port` `--port=port`: porta do servidor de banco de dados.

`-U username` `--username=username`: nome do usuário para se conectar como.

Para exibir tabelas específicas, selecione quais tabelas devem ser exibidas usando `-o`, `-f` e/ou `-t`. `-o` recebe um OID, `-f` recebe um filenode, e `-t` recebe um nome de tabela (na verdade, é um padrão de `LIKE`, então você pode usar coisas como `foo%`). Você pode usar tantas dessas opções quanto desejar, e a lista incluirá todos os objetos correspondidos por qualquer uma das opções. Mas observe que essas opções só podem mostrar objetos no banco de dados dado por `-d`.

Se você não fornecer nenhum dos `-o`, `-f` ou `-t`, mas fornecer `-d`, ele listará todas as tabelas no banco de dados nomeado por `-d`. Nesse modo, as opções `-S` e `-i` controlam o que é listado.

Se você não fornecer também o `-d`, ele exibirá uma lista de OIDs do banco de dados. Alternativamente, você pode fornecer o `-s` para obter uma lista de espaços de tabela.

## Meio Ambiente

`PGHOST` `PGPORT` `PGUSER`: Parâmetros de conexão padrão.

Esse utilitário, como a maioria dos outros utilitários do PostgreSQL, também utiliza as variáveis de ambiente suportadas pelo libpq (consulte a Seção 32.15 [(libpq-envars.md "32.15. Environment Variables")]).

A variável de ambiente `PG_COLOR` especifica se a cor deve ser usada nas mensagens de diagnóstico. Os valores possíveis são `always`, `auto` e `never`.

## Notas

oid2name requer um servidor de banco de dados em execução com catálogos de sistema não corrompidos. Portanto, é de uso apenas limitado para recuperação de situações catastróficas de corrupção de banco de dados.

## Exemplos

```
$ # what's in this database server, anyway?
$ oid2name
All databases:
    Oid  Database Name  Tablespace
----------------------------------
  17228       alvherre  pg_default
  17255     regression  pg_default
  17227      template0  pg_default
      1      template1  pg_default

$ oid2name -s
All tablespaces:
     Oid  Tablespace Name
-------------------------
    1663       pg_default
    1664        pg_global
  155151         fastdisk
  155152          bigdisk

$ # OK, let's look into database alvherre
$ cd $PGDATA/base/17228

$ # get top 10 db objects in the default tablespace, ordered by size
$ ls -lS * | head -10
-rw-------  1 alvherre alvherre 136536064 sep 14 09:51 155173
-rw-------  1 alvherre alvherre  17965056 sep 14 09:51 1155291
-rw-------  1 alvherre alvherre   1204224 sep 14 09:51 16717
-rw-------  1 alvherre alvherre    581632 sep  6 17:51 1255
-rw-------  1 alvherre alvherre    237568 sep 14 09:50 16674
-rw-------  1 alvherre alvherre    212992 sep 14 09:51 1249
-rw-------  1 alvherre alvherre    204800 sep 14 09:51 16684
-rw-------  1 alvherre alvherre    196608 sep 14 09:50 16700
-rw-------  1 alvherre alvherre    163840 sep 14 09:50 16699
-rw-------  1 alvherre alvherre    122880 sep  6 17:51 16751

$ # What file is 155173?
$ oid2name -d alvherre -f 155173
From database "alvherre":
  Filenode  Table Name
----------------------
    155173    accounts

$ # you can ask for more than one object
$ oid2name -d alvherre -f 155173 -f 1155291
From database "alvherre":
  Filenode     Table Name
-------------------------
    155173       accounts
   1155291  accounts_pkey

$ # you can mix the options, and get more details with -x
$ oid2name -d alvherre -t accounts -f 1155291 -x
From database "alvherre":
  Filenode     Table Name      Oid  Schema  Tablespace
------------------------------------------------------
    155173       accounts   155173  public  pg_default
   1155291  accounts_pkey  1155291  public  pg_default

$ # show disk space for every db object
$ du [0-9]* |
> while read SIZE FILENODE
> do
>   echo "$SIZE       `oid2name -q -d alvherre -i -f $FILENODE`"
> done
16            1155287  branches_pkey
16            1155289  tellers_pkey
17561            1155291  accounts_pkey
...

$ # same, but sort by size
$ du [0-9]* | sort -rn | while read SIZE FN
> do
>   echo "$SIZE   `oid2name -q -d alvherre -f $FN`"
> done
133466             155173    accounts
17561            1155291  accounts_pkey
1177              16717  pg_proc_proname_args_nsp_index
...

$ # If you want to see what's in tablespaces, use the pg_tblspc directory
$ cd $PGDATA/pg_tblspc
$ oid2name -s
All tablespaces:
     Oid  Tablespace Name
-------------------------
    1663       pg_default
    1664        pg_global
  155151         fastdisk
  155152          bigdisk

$ # what databases have objects in tablespace "fastdisk"?
$ ls -d 155151/*
155151/17228/  155151/PG_VERSION

$ # Oh, what was database 17228 again?
$ oid2name
All databases:
    Oid  Database Name  Tablespace
----------------------------------
  17228       alvherre  pg_default
  17255     regression  pg_default
  17227      template0  pg_default
      1      template1  pg_default

$ # Let's see what objects does this database have in the tablespace.
$ cd 155151/17228
$ ls -l
total 0
-rw-------  1 postgres postgres 0 sep 13 23:20 155156

$ # OK, this is a pretty small table ... but which one is it?
$ oid2name -d alvherre -f 155156
From database "alvherre":
  Filenode  Table Name
----------------------
    155156         foo
```

## Autor

B. Palmer `<bpalmer@crimelabs.net>`