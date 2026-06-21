## SPI_execute

SPI_execute — executar um comando

## Sinopse

```
int SPI_execute(const char * command, bool read_only, long count)
```

## Descrição

`SPI_execute` executa o comando SQL especificado para *`count`* linhas. Se *`read_only`* é `true`, o comando deve ser de leitura somente, e o custo de execução é reduzido um pouco.

Essa função só pode ser chamada a partir de uma função C conectada.

Se *`count`* for zero, o comando é executado para todas as linhas que ele se aplica. Se *`count`* for maior que zero, então não mais que *`count`* linhas serão recuperadas; a execução para quando o contador é alcançado, muito como adicionar uma cláusula *`LIMIT`* à consulta. Por exemplo,

```
SPI_execute("SELECT * FROM foo", true, 5);
```

recuperará no máximo 5 linhas da tabela. Observe que esse limite só é eficaz quando o comando realmente retorna linhas. Por exemplo,

```
SPI_execute("INSERT INTO foo SELECT * FROM bar", false, 5);
```

insere todas as linhas de `bar`, ignorando o parâmetro *`count`*. No entanto, com

```
SPI_execute("INSERT INTO foo SELECT * FROM bar RETURNING *", false, 5);
```

máximo de 5 linhas seriam inseridas, uma vez que a execução pararia após a quinta linha do resultado do `RETURNING` ser recuperada.

Você pode passar vários comandos em uma única string; `SPI_execute` retorna o resultado do comando executado por último. O *`count`* limita-se a cada comando separadamente (embora apenas o último resultado seja realmente retornado). O limite não é aplicado a quaisquer comandos ocultos gerados por regras.

Quando *`read_only`* é `false`, `SPI_execute` incrementa o contador de comandos e calcula um novo *instantâneo* antes de executar cada comando na string. O instantâneo não muda na verdade se o nível de isolamento de transação atual é `SERIALIZABLE` ou `REPEATABLE READ`, mas no modo `READ COMMITTED` a atualização do instantâneo permite que cada comando veja os resultados de transações recém-comprometidas de outras sessões. Isso é essencial para um comportamento consistente quando os comandos estão modificando o banco de dados.

Quando *`read_only`* é `true`, `SPI_execute` não atualiza nem o instantâneo nem o contador de comandos, e permite que apenas comandos `SELECT` comuns apareçam na string de comandos. Os comandos são executados usando o instantâneo previamente estabelecido para a consulta envolvente. Esse modo de execução é um pouco mais rápido que o modo de leitura/escrita, pois elimina o overhead por comando. Também permite que funções verdadeiramente *estáveis* sejam construídas: uma vez que as execuções sucessivas usarão todos os mesmos instantâneos, não haverá nenhuma mudança nos resultados.

Geralmente, não é prudente misturar comandos de leitura e de escrita em uma única função usando SPI; isso pode resultar em um comportamento muito confuso, uma vez que as consultas de leitura não veriam os resultados de quaisquer atualizações de banco de dados feitas pelas consultas de leitura e escrita.

O número real de linhas para as quais o (último) comando foi executado é retornado na variável global `SPI_processed`. Se o valor de retorno da função for `SPI_OK_SELECT`, `SPI_OK_INSERT_RETURNING`, `SPI_OK_DELETE_RETURNING`, `SPI_OK_UPDATE_RETURNING` ou `SPI_OK_MERGE_RETURNING`, então você pode usar o ponteiro global `SPITupleTable *SPI_tuptable` para acessar as linhas de resultado. Alguns comandos de utilidade (como `EXPLAIN`) também retornam conjuntos de linhas, e `SPI_tuptable` conterá o resultado nesses casos também. Alguns comandos de utilidade (`COPY`, `CREATE TABLE AS`) não retornam um conjunto de linhas, então `SPI_tuptable` é NULL, mas ainda assim retornam o número de linhas processadas em `SPI_processed`.

A estrutura `SPITupleTable` é definida da seguinte forma:

```
typedef struct SPITupleTable
{
    /* Public members */
    TupleDesc   tupdesc;        /* tuple descriptor */
    HeapTuple  *vals;           /* array of tuples */
    uint64      numvals;        /* number of valid tuples */

    /* Private members, not intended for external callers */
    uint64      alloced;        /* allocated length of vals array */
    MemoryContext tuptabcxt;    /* memory context of result table */
    slist_node  next;           /* link for internal bookkeeping */
    SubTransactionId subid;     /* subxact in which tuptable was created */
} SPITupleTable;
```

Os campos `tupdesc`, `vals` e `numvals` podem ser utilizados por chamados do SPI; os campos restantes são internos. `vals` é um array de ponteiros para linhas. O número de linhas é dado por `numvals` (por razões um tanto históricas, esse contagem também é retornado em `SPI_processed`). `tupdesc` é um descritor de linha que você pode passar para funções do SPI que lidam com linhas.

`SPI_finish` libera todos os `SPITupleTable`s alocados durante a função atual C. Você pode liberar uma tabela de resultado específica anteriormente, se já estiver pronta para isso, chamando `SPI_freetuptable`.

## Argumentos

`const char * command`: string contendo o comando a ser executado

`bool read_only`: `true` para execução somente de leitura

`long count`: número máximo de linhas a serem devolvidas, ou `0` para sem limite

## Valor de retorno

Se a execução do comando foi bem-sucedida, então um dos seguintes valores (não negativo) será retornado:

`SPI_OK_SELECT`: se um `SELECT` (mas não `SELECT INTO`) foi executado

`SPI_OK_SELINTO`: se um `SELECT INTO` foi executado

`SPI_OK_INSERT`: se um `INSERT` foi executado

`SPI_OK_DELETE`: se um `DELETE` foi executado

`SPI_OK_UPDATE`: se um `UPDATE` foi executado

`SPI_OK_MERGE`: se um `MERGE` foi executado

`SPI_OK_INSERT_RETURNING`: se um `INSERT RETURNING` foi executado

`SPI_OK_DELETE_RETURNING`: se um `DELETE RETURNING` foi executado

`SPI_OK_UPDATE_RETURNING`: se uma `UPDATE RETURNING` foi executada

`SPI_OK_MERGE_RETURNING`: se um `MERGE RETURNING` foi executado

`SPI_OK_UTILITY`: se um comando de utilidade (por exemplo, `CREATE TABLE`) foi executado

`SPI_OK_REWRITTEN`: se o comando foi reescrito em outro tipo de comando (por exemplo, `UPDATE` tornou-se um `INSERT`) por uma [regra][(rules.md "Chapter 39. The Rule System")].

Em caso de erro, um dos seguintes valores negativos é retornado:

`SPI_ERROR_ARGUMENT`: se *`command`* é `NULL` ou *`count`* é menor que 0

`SPI_ERROR_COPY`: se `COPY TO stdout` ou `COPY FROM stdin` foi tentado

`SPI_ERROR_TRANSACTION`: se um comando de manipulação de transação foi tentado (`BEGIN`, `COMMIT`, `ROLLBACK`, `SAVEPOINT`, `PREPARE TRANSACTION`, `COMMIT PREPARED`, `ROLLBACK PREPARED` ou qualquer uma de suas variantes)

`SPI_ERROR_OPUNKNOWN`: se o tipo de comando é desconhecido (não deveria acontecer)

`SPI_ERROR_UNCONNECTED`: se chamado a partir de uma função C não conectada

## Notas

Todas as funções de execução de consultas do SPI definem tanto `SPI_processed` quanto `SPI_tuptable` (apenas o ponteiro, não o conteúdo da estrutura). Guarde essas duas variáveis globais em variáveis locais de funções em C se precisar acessar a tabela de resultados de `SPI_execute` ou outra função de execução de consulta em chamadas subsequentes.