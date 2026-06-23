## 33.3. Interfaces do Cliente [#](#LO-INTERFACES)

* [33.3.1. Criando um Objeto Grande](lo-interfaces.md#LO-CREATE)
* [33.3.2. Importando um Objeto Grande](lo-interfaces.md#LO-IMPORT)
* [33.3.3. Exportando um Objeto Grande](lo-interfaces.md#LO-EXPORT)
* [33.3.4. Abrindo um Objeto Grande Existente](lo-interfaces.md#LO-OPEN)
* [33.3.5. Escrevendo Dados em um Objeto Grande](lo-interfaces.md#LO-WRITE)
* [33.3.6. Lendo Dados de um Objeto Grande](lo-interfaces.md#LO-READ)
* [33.3.7. Buscando em um Objeto Grande](lo-interfaces.md#LO-SEEK)
* [33.3.8. Obtendo a Posição de Busca de um Objeto Grande](lo-interfaces.md#LO-TELL)
* [33.3.9. Cortando um Objeto Grande](lo-interfaces.md#LO-TRUNCATE)
* [33.3.10. Fechando um Descritor de Objeto Grande](lo-interfaces.md#LO-CLOSE)
* [33.3.11. Removendo um Objeto Grande](lo-interfaces.md#LO-UNLINK)

Esta seção descreve as facilidades que a biblioteca de interface do cliente libpq do PostgreSQL oferece para acessar objetos grandes. A interface de objeto grande do PostgreSQL é modelada após a interface do sistema de arquivos Unix, com análogos de `open`, `read`, `write`, `lseek`, etc.

Todas as manipulações de objetos grandes que utilizam essas funções *devem* ser realizadas dentro de um bloco de transação SQL, uma vez que os descritores de arquivo de objetos grandes são válidos apenas durante a duração de uma transação. As operações de escrita, incluindo `lo_open` com o modo `INV_WRITE`, não são permitidas em uma transação somente de leitura.

Se ocorrer um erro ao executar uma dessas funções, a função retornará um valor que, de outra forma, seria impossível, tipicamente 0 ou -1. Uma mensagem que descreve o erro é armazenada no objeto de conexão e pode ser recuperada com `PQerrorMessage`(libpq-status.md#LIBPQ-PQERRORMESSAGE).

As aplicações cliente que utilizam essas funções devem incluir o arquivo de cabeçalho `libpq/libpq-fs.h` e vincular com a biblioteca libpq.

Os aplicativos do cliente não podem usar essas funções enquanto uma conexão libpq estiver no modo de pipeline.

### 33.3.1. Criar um Objeto Grande [#](#LO-CREATE)

A função

```
Oid lo_create(PGconn *conn, Oid lobjId);
```

cria um novo objeto grande. O OID a ser atribuído pode ser especificado por *`lobjId`*; se assim for, ocorre falha se esse OID já estiver em uso para algum objeto grande. Se *`lobjId`* for `InvalidOid` (zero) então `lo_create` atribui um OID não utilizado. O valor de retorno é o OID que foi atribuído ao novo objeto grande, ou `InvalidOid` (zero) em caso de falha.

Um exemplo:

```
inv_oid = lo_create(conn, desired_oid);
```

A função mais antiga

```
Oid lo_creat(PGconn *conn, int mode);
```

também cria um novo objeto grande, sempre atribuindo um OID não utilizado. O valor de retorno é o OID que foi atribuído ao novo objeto grande, ou `InvalidOid` (zero) em caso de falha.

Nas versões do PostgreSQL 8.1 e posteriores, o *`mode`* é ignorado, de modo que `lo_creat` é exatamente equivalente a `lo_create` com um argumento de segundo zero. No entanto, há pouca razão para usar `lo_creat`, a menos que você precise trabalhar com servidores mais antigos que 8.1. Para trabalhar com um servidor tão antigo, você deve usar `lo_creat` e não `lo_create`, e deve definir *`mode`* para um dos `INV_READ`, `INV_WRITE`, ou `INV_READ` `|` `INV_WRITE`. (Essas constantes simbólicas são definidas no arquivo de cabeçalho `libpq/libpq-fs.h`.)

Um exemplo:

```
inv_oid = lo_creat(conn, INV_READ|INV_WRITE);
```

### 33.3.2. Impor um Objeto Grande [#](#LO-IMPORT)

Para importar um arquivo de sistema operacional como um objeto grande, chame

```
Oid lo_import(PGconn *conn, const char *filename);
```

*`filename`* especifica o nome do sistema operacional do arquivo a ser importado como um objeto grande. O valor de retorno é o OID que foi atribuído ao novo objeto grande, ou `InvalidOid` (zero) em caso de falha. Note que o arquivo é lido pela biblioteca de interface do cliente, não pelo servidor; portanto, ele deve existir no sistema de arquivos do cliente e ser legível pelo aplicativo do cliente.

A função

```
Oid lo_import_with_oid(PGconn *conn, const char *filename, Oid lobjId);
```

também importa um novo objeto grande. O OID a ser atribuído pode ser especificado por *`lobjId`*; se assim for, ocorre falha se esse OID já estiver em uso para algum objeto grande. Se *`lobjId`* é `InvalidOid` (zero) então `lo_import_with_oid` atribui um OID não utilizado (este é o mesmo comportamento que `lo_import`). O valor de retorno é o OID que foi atribuído ao novo objeto grande, ou `InvalidOid` (zero) em caso de falha.

`lo_import_with_oid` é novo a partir do PostgreSQL 8.4 e usa internamente `lo_create`, que é novo no 8.1; se essa função for executada contra 8.0 ou antes, ela falhará e retornará `InvalidOid`.

### 33.3.3. Expor um Objeto Grande [#](#LO-EXPORT)

Para exportar um objeto grande para um arquivo do sistema operacional, chame

```
int lo_export(PGconn *conn, Oid lobjId, const char *filename);
```

O argumento *`lobjId`* especifica o OID do grande objeto a ser exportado e o argumento *`filename`* especifica o nome do sistema operacional do arquivo. Observe que o arquivo é escrito pela biblioteca de interface do cliente, não pelo servidor. Retorna 1 em caso de sucesso, -1 em caso de falha.

### 33.3.4. Abrir um Objeto Grande Existente [#](#LO-OPEN)

Para abrir um objeto grande existente para leitura ou escrita, chame

```
int lo_open(PGconn *conn, Oid lobjId, int mode);
```

O argumento *`lobjId`* especifica o OID do grande objeto a ser aberto. Os bits *`mode`* controlam se o objeto é aberto para leitura (`INV_READ`), escrita (`INV_WRITE`), ou ambos. (Essas constantes simbólicas são definidas no arquivo de cabeçalho `libpq/libpq-fs.h`.) `lo_open` retorna um descritor de objeto grande (não negativo) para uso posterior em `lo_read`, `lo_write`, `lo_lseek`, `lo_lseek64`, `lo_tell`, `lo_tell64`, `lo_truncate`, `lo_truncate64` e `lo_close`. O descritor é válido apenas durante a duração da transação atual. Em caso de falha, -1 é retornado.

O servidor atualmente não distingue entre os modos `INV_WRITE` e `INV_READ` `|` `INV_WRITE`: você pode ler o descritor em qualquer um desses casos. No entanto, há uma diferença significativa entre esses modos e o modo `INV_READ` sozinho: com `INV_READ`, você não pode escrever no descritor, e os dados lidos a partir dele refletirão o conteúdo do grande objeto no momento do instantâneo de transação que estava ativo quando o `lo_open` foi executado, independentemente de escritas posteriores por essa ou outras transações. Ler de um descritor aberto com `INV_WRITE` retorna dados que refletem todas as escritas de outras transações comprometidas, bem como as escritas da transação atual. Isso é semelhante ao comportamento dos modos de transação `REPEATABLE READ` versus `READ COMMITTED` para comandos ordinários SQL `SELECT`.

`lo_open` falhará se o privilégio `SELECT` não estiver disponível para o objeto grande, ou se `INV_WRITE` for especificado e o privilégio `UPDATE` não estiver disponível. (Antes do PostgreSQL 11, essas verificações de privilégio eram realizadas, em vez disso, na primeira chamada de leitura ou escrita real usando o descritor. Essas verificações de privilégio podem ser desativadas com o parâmetro de runtime [lo_compat_privileges](runtime-config-compatible.md#GUC-LO-COMPAT-PRIVILEGES).

Um exemplo:

```
inv_fd = lo_open(conn, inv_oid, INV_READ|INV_WRITE);
```

### 33.3.5. Escrita de dados em um objeto grande [#](#LO-WRITE)

A função

```
int lo_write(PGconn *conn, int fd, const char *buf, size_t len);
```

escreve *`len`* bytes de *`buf`* (que deve ter tamanho *`len`*) no descritor de objeto grande *`fd`*. O argumento *`fd`* deve ter sido retornado por um `lo_open` anterior. O número de bytes realmente escritos é retornado (na implementação atual, isso sempre será igual a *`len`* a menos que haja um erro). No caso de um erro, o valor de retorno é -1.

Embora o parâmetro *`len`* seja declarado como `size_t`, essa função rejeitará valores de comprimento maiores que `INT_MAX`. Na prática, é melhor transferir dados em lotes de, no máximo, alguns megabytes.

### 33.3.6. Leitura de dados de um objeto grande [#](#LO-READ)

A função

```
int lo_read(PGconn *conn, int fd, char *buf, size_t len);
```

lê até *`len`* bytes do descritor de objeto grande *`fd`* para *`buf`* (que deve ter tamanho *`len`*). O argumento *`fd`* deve ter sido retornado por um `lo_open` anterior. O número de bytes realmente lidos é retornado; este será menor que *`len`* se o fim do objeto grande for alcançado primeiro. No caso de um erro, o valor de retorno é -1.

Embora o parâmetro *`len`* seja declarado como `size_t`, essa função rejeitará valores de comprimento maiores que `INT_MAX`. Na prática, é melhor transferir dados em lotes de, no máximo, alguns megabytes.

### 33.3.7. Buscar em um Objeto Grande [#](#LO-SEEK)

Para alterar a localização atual de leitura ou escrita associada a um descritor de objeto grande, chame

```
int lo_lseek(PGconn *conn, int fd, int offset, int whence);
```

Essa função move o ponteiro de localização atual para o descritor de objeto grande identificado por *`fd`*. Os valores válidos para *`whence`* são `SEEK_SET` (buscar a partir do início do objeto), `SEEK_CUR` (buscar a partir da posição atual) e `SEEK_END` (buscar a partir do fim do objeto). O valor de retorno é o novo ponteiro de localização, ou -1 em caso de erro.

Ao lidar com objetos grandes que possam exceder 2 GB de tamanho, use, em vez disso,

```
int64_t lo_lseek64(PGconn *conn, int fd, int64_t offset, int whence);
```

Essa função tem o mesmo comportamento que `lo_lseek`, mas pode aceitar um *`offset`* maior que 2 GB e/ou fornecer um resultado maior que 2 GB. Note que `lo_lseek` falhará se o novo ponteiro de localização for maior que 2 GB.

`lo_lseek64` é novo a partir do PostgreSQL 9.3. Se essa função for executada em uma versão mais antiga do servidor, ela falhará e retornará -1.

### 33.3.8. Obter a Posição de Busca de um Objeto Grande [#](#LO-TELL)

Para obter a localização atual de leitura ou escrita de um descritor de objeto grande, chame

```
int lo_tell(PGconn *conn, int fd);
```

Se houver um erro, o valor de retorno é -1.

Ao lidar com objetos grandes que possam exceder 2 GB de tamanho, use, em vez disso,

```
int64_t lo_tell64(PGconn *conn, int fd);
```

Essa função tem o mesmo comportamento que `lo_tell`, mas pode fornecer um resultado maior que 2 GB. Observe que `lo_tell` falhará se a localização atual de leitura/escrita for maior que 2 GB.

`lo_tell64` é novo a partir do PostgreSQL 9.3. Se essa função for executada em uma versão mais antiga do servidor, ela falhará e retornará -1.

### 33.3.9. Retornar um objeto grande [#](#LO-TRUNCATE)

Para truncar um objeto grande a uma determinada comprimento, chame

```
int lo_truncate(PGconn *conn, int fd, size_t len);
```

Essa função trunca o descritor do objeto grande *`fd`* para o comprimento *`len`*. O argumento *`fd`* deve ter sido retornado por um `lo_open` anterior. Se *`len`* for maior que o comprimento atual do objeto grande, o objeto grande é estendido para o comprimento especificado com bytes nulos ('\0'). Se for bem-sucedido, `lo_truncate` retorna zero. Se houver erro, o valor de retorno é -1.

A localização de leitura/escrita associada ao descritor *`fd`* não é alterada.

Embora o parâmetro *`len`* seja declarado como `size_t`, `lo_truncate` rejeitará valores de comprimento maiores que `INT_MAX`.

Ao lidar com objetos grandes que possam exceder 2 GB de tamanho, use, em vez disso,

```
int lo_truncate64(PGconn *conn, int fd, int64_t len);
```

Essa função tem o mesmo comportamento que `lo_truncate`, mas pode aceitar um valor de *`len`* que exceda 2 GB.

`lo_truncate` é novo a partir do PostgreSQL 8.3; se essa função for executada em uma versão mais antiga do servidor, ela falhará e retornará -1.

`lo_truncate64` é novo a partir do PostgreSQL 9.3; se essa função for executada em uma versão mais antiga do servidor, ela falhará e retornará -1.

### 33.3.10. Fechamento de um Descritor de Objeto Grande [#](#LO-CLOSE)

Um descritor de objeto grande pode ser fechado chamando

```
int lo_close(PGconn *conn, int fd);
```

onde *`fd`* é um descritor de objeto grande retornado por `lo_open`. Se for bem-sucedido, `lo_close` retorna zero. Se houver erro, o valor de retorno é -1.

Qualquer descritor de objeto grande que permanecer aberto no final de uma transação será fechado automaticamente.

### 33.3.11. Retirada de um Objeto Grande [#](#LO-UNLINK)

Para remover um objeto grande do banco de dados, ligue

```
int lo_unlink(PGconn *conn, Oid lobjId);
```

O argumento *`lobjId`* especifica o OID do grande objeto a ser removido. Retorna 1 se o processo for bem-sucedido, -1 se falhar.