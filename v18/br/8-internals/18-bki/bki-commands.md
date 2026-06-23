## 68.4. Comandos do BKI [#](#BKI-COMMANDS)

`create` *`tablename`* *`tableoid`* [`bootstrap`] [`shared_relation`] [`rowtype_oid` *`oid`*] (*`name1`* = *`type1`* [`FORCE NOT NULL` | `FORCE NULL` ] [, *`name2`* = *`type2`* [`FORCE NOT NULL` | `FORCE NULL` ], ...]): Crie uma tabela denominada *`tablename`*, e com o OID *`tableoid`*, com as colunas dadas entre parênteses.

Os seguintes tipos de colunas são suportados diretamente pelo `bootstrap.c`: `bool`, `bytea`, `char` (1 byte), `name`, `int2`, `int4`, `regproc`, `regclass`, `regtype`, `text`, `oid`, `tid`, `xid`, `cid`, `int2vector`, `oidvector`, `_int4` (matriz), `_text` (matriz), `_oid` (matriz), `_char` (matriz), `_aclitem` (matriz). Embora seja possível criar tabelas contendo colunas de outros tipos, isso não pode ser feito até que o `pg_type` tenha sido criado e preenchido com entradas apropriadas. (Isso significa que, efetivamente, apenas esses tipos de colunas podem ser usados em catálogos bootstrap, mas catálogos não bootstrap podem conter qualquer tipo embutido.)

Quando `bootstrap` é especificado, a tabela será criada apenas no disco; nada será inserido em `pg_class`, `pg_attribute`, etc., para ela. Assim, a tabela não será acessível por operações SQL comuns até que essas entradas sejam feitas da maneira tradicional (com comandos `insert`). Esta opção é usada para criar os próprios `pg_class` etc.

A tabela é criada como compartilhada se `shared_relation` for especificado. O tipo de linha da tabela OID (`pg_type` OID) pode ser opcionalmente especificado via cláusula `rowtype_oid`; se não for especificado, um OID é gerado automaticamente para ela. (A cláusula `rowtype_oid` é inútil se `bootstrap` for especificado, mas pode ser fornecida de qualquer maneira para documentação.)

`open` *`tablename`*: Abra a tabela denominada *`tablename`* para inserção de dados. Qualquer tabela aberta atualmente é fechada.

`close` *`tablename`*: Feche a tabela aberta. O nome da tabela deve ser fornecido como um cruzamento.

`insert` `(` [*`oid_value`*] *`value1`* *`value2`* ... `)`: Insira uma nova linha na tabela aberta usando *`value1`*, *`value2`*, etc., para seus valores de coluna.

Os valores nulos podem ser especificados usando a palavra-chave especial `_null_`. Os valores que não parecem ser identificadores ou cadeias de caracteres numéricos devem ser escritos com aspas simples. (Para incluir uma aspa simples em um valor, escreva-a duas vezes. As escamas de estilo de string de barra também são permitidas na string.)

`declare` [`unique`] `index` *`indexname`* *`indexoid`* `on` *`tablename`* `using` *`amname`* `(` *`opclass1`* *`name1`* [, ...] `)`: Crie um índice com o nome *`indexname`*, com OID *`indexoid`*, na tabela denominada *`tablename`*, usando o método de acesso *`amname`*. Os campos a serem indexados são chamados *`name1`*, *`name2`* etc., e as classes de operador a serem usadas são *`opclass1`*, *`opclass2`* etc., respectivamente. O arquivo do índice é criado e entradas de catálogo apropriadas são feitas para ele, mas o conteúdo do índice não é inicializado por este comando.

`declare toast` *`toasttableoid`* *`toastindexoid`* `on` *`tablename`*: Crie uma tabela TOAST para a tabela denominada *`tablename`*. A tabela TOAST é atribuída OID *`toasttableoid`* e seu índice é atribuído OID *`toastindexoid`*. Assim como em `declare index`, o preenchimento do índice é adiado.

`build indices`: Preencha os índices que foram declarados anteriormente.