## pg_amcheck

pg_amcheck — verifica a corrupção em um ou mais bancos de dados PostgreSQL

## Sinopse

`pg_amcheck` [*`option`*...] [*`dbname`*]

## Descrição

O pg_amcheck suporta a execução das funções de verificação de corrupção do [amcheck][(amcheck.md "F.1. amcheck — tools to verify table and index consistency")] contra um ou mais bancos de dados, com opções para selecionar quais esquemas, tabelas e índices devem ser verificados, quais tipos de verificação devem ser realizados e se devem realizar as verificações em paralelo, e, se assim for, o número de conexões paralelas a serem estabelecidas e utilizadas.

Atualmente, apenas as relações comuns e de mesa de torradas, visualizações materializadas, sequências e índices btree são suportadas. Outros tipos de relação são silenciosamente ignorados.

Se `dbname` for especificado, ele deve ser o nome de um único banco de dados a ser verificado, e não devem estar presentes outras opções de seleção de banco de dados. Caso contrário, se houver alguma opção de seleção de banco de dados, todos os bancos de dados correspondentes serão verificados. Se não houver tais opções, o banco de dados padrão será verificado. As opções de seleção de banco de dados incluem `--all`, `--database` e `--exclude-database`. Elas também incluem `--relation`, `--exclude-relation`, `--table`, `--exclude-table`, `--index` e `--exclude-index`, mas apenas quando tais opções são usadas com um padrão de três partes (por exemplo, `mydb*.myschema*.myrel*`). Por fim, elas incluem `--schema` e `--exclude-schema` quando tais opções são usadas com um padrão de duas partes (por exemplo, `mydb*.myschema*`).

*`dbname`* também pode ser uma [string de conexão][(libpq-connect.md#LIBPQ-CONNSTRING "32.1.1. Connection Strings")].

## Opções

As opções de linha de comando a seguir controlam o que é verificado:

`-a` `--all`: Verifique todos os bancos de dados, exceto aqueles excluídos por meio de `--exclude-database`.

`-d pattern` `--database=pattern`: Verifique os bancos de dados que correspondem ao especificado [*`pattern`](app-psql.md#APP-PSQL-PATTERNS "Patterns"), exceto aqueles excluídos por `--exclude-database`. Esta opção pode ser especificada mais de uma vez.

`-D pattern` `--exclude-database=pattern`: Exclua bancos de dados que correspondem ao dado [*`pattern`](app-psql.md#APP-PSQL-PATTERNS "Patterns"). Esta opção pode ser especificada mais de uma vez.

`-i pattern` `--index=pattern`: Verifique índices que correspondem ao especificado [*`pattern`](app-psql.md#APP-PSQL-PATTERNS "Patterns"), a menos que eles sejam excluídos de outra forma. Esta opção pode ser especificada mais de uma vez.

Isso é semelhante à opção `--relation`, exceto que ela se aplica apenas a índices, e não a outros tipos de relação.

`-I pattern` `--exclude-index=pattern`: Exclua índices que correspondem ao especificado [*`pattern`*](app-psql.md#APP-PSQL-PATTERNS "Patterns"). Esta opção pode ser especificada mais de uma vez.

Isso é semelhante à opção `--exclude-relation`, exceto que ela se aplica apenas a índices, não a outros tipos de relação.

`-r pattern` `--relation=pattern`: Verifique as relações que correspondem ao [*`pattern`*](app-psql.md#APP-PSQL-PATTERNS "Patterns"), a menos que sejam excluídas de outra forma. Esta opção pode ser especificada mais de uma vez.

Os padrões podem ser não qualificados, por exemplo, `myrel*`, ou podem ser qualificados por esquema, por exemplo, `myschema*.myrel*` ou qualificados para banco de dados e qualificados por esquema, por exemplo, `mydb*.myschema*.myrel*`. Um padrão qualificado para banco de dados adicionará bancos de dados correspondentes à lista de bancos de dados a serem verificados.

`-R pattern` `--exclude-relation=pattern`: Exclua as relações que correspondem ao especificado [*`pattern`](app-psql.md#APP-PSQL-PATTERNS "Patterns"). Esta opção pode ser especificada mais de uma vez.

Assim como no caso de `--relation`, o [*`pattern`*](app-psql.md#APP-PSQL-PATTERNS "Patterns") pode ser não qualificado, qualificado por esquema ou qualificado por banco de dados e esquema.

`-s pattern` `--schema=pattern`: Verifique as tabelas e índices nos esquemas que correspondem ao especificado [*`pattern`](app-psql.md#APP-PSQL-PATTERNS "Patterns"), a menos que eles sejam excluídos de outra forma. Esta opção pode ser especificada mais de uma vez.

Para selecionar apenas as tabelas em esquemas que correspondem a um padrão específico, considere usar algo como `--table=SCHEMAPAT.* --no-dependent-indexes`. Para selecionar apenas índices, considere usar algo como `--index=SCHEMAPAT.*`.

Um padrão de esquema pode ser qualificado para banco de dados. Por exemplo, você pode escrever `--schema=mydb*.myschema*` para selecionar esquemas que correspondem a `myschema*` em bancos que correspondem a `mydb*`.

`-S pattern` `--exclude-schema=pattern`: Exclua tabelas e índices em esquemas que correspondem ao especificado [*`pattern`](app-psql.md#APP-PSQL-PATTERNS "Patterns"). Esta opção pode ser especificada mais de uma vez.

Assim como no caso de `--schema`, o padrão pode ser qualificado por banco de dados.

`-t pattern` `--table=pattern`: Verifique as tabelas que correspondem ao especificado [*`pattern`](app-psql.md#APP-PSQL-PATTERNS "Patterns"), a menos que estejam excluídas de outra forma. Esta opção pode ser especificada mais de uma vez.

Isso é semelhante à opção `--relation`, exceto que ela se aplica apenas a tabelas, visualizações materializadas e sequências, e não a índices.

`-T pattern` `--exclude-table=pattern`: Exclua tabelas que correspondem ao especificado [*`pattern`](app-psql.md#APP-PSQL-PATTERNS "Patterns"). Esta opção pode ser especificada mais de uma vez.

Isso é semelhante à opção `--exclude-relation`, exceto que ela se aplica apenas a tabelas, visualizações materializadas e sequências, e não a índices.

`--no-dependent-indexes`: Por padrão, se uma tabela for marcada, quaisquer índices btree dessa tabela também serão verificados, mesmo que não sejam explicitamente selecionados por uma opção como `--index` ou `--relation`. Esta opção suprime esse comportamento.

`--no-dependent-toast`: Por padrão, se uma tabela for marcada, sua tabela de acompanhamento, se houver, também será marcada, mesmo que não seja explicitamente selecionada por uma opção como `--table` ou `--relation`. Esta opção suprime esse comportamento.

`--no-strict-names`: Por padrão, se um argumento para `--database`, `--table`, `--index` ou `--relation` não corresponder a nenhum objeto, é um erro fatal. Esta opção desvaloriza esse erro para um aviso.

As opções de linha de comando a seguir controlam a verificação de tabelas:

`--exclude-toast-pointers`: Por padrão, sempre que um ponteiro de toast é encontrado em uma tabela, uma pesquisa é realizada para garantir que ele faça referência a entradas aparentemente válidas na tabela de toast. Esses verificações podem ser bastante lentas, e essa opção pode ser usada para ignorá-las.

`--on-error-stop`: Após relatar todas as corrupções na primeira página de uma tabela onde a corrupção é encontrada, pare o processamento dessa relação da tabela e vá para a próxima tabela ou índice.

Observe que a verificação do índice sempre para após a primeira página corrupta. Esta opção só tem significado em relação às relações de tabela.

`--skip=option`: Se `all-frozen` for fornecido, as verificações de corrupção de tabela passarão em páginas em todas as tabelas marcadas como todas congeladas.

Se o `all-visible` for fornecido, os verificadores de corrupção de tabela passarão por páginas em todas as tabelas marcadas como todas visíveis.

Por padrão, nenhuma página é ignorada. Isso pode ser especificado como `none`, mas, como este é o padrão, não precisa ser mencionado.

`--startblock=block`: Comece a verificar no número especificado do bloco. Um erro ocorrerá se a relação da tabela que está sendo verificada tiver menos que esse número de blocos. Esta opção não se aplica a índices e provavelmente só é útil ao verificar uma única relação de tabela. Consulte `--endblock` para mais informações.

`--endblock=block`: Encerrar a verificação no número de bloco especificado. Um erro ocorrerá se a relação de tabela que está sendo verificada tiver menos que este número de blocos. Esta opção não se aplica a índices e provavelmente só é útil ao verificar uma única relação de tabela. Se uma tabela regular e uma tabela de toast forem verificadas, esta opção se aplicará a ambas, mas blocos de toast com números mais altos ainda podem ser acessados durante a validação de ponteiros de toast, a menos que isso seja suprimido usando `--exclude-toast-pointers`.

As opções de linha de comando a seguir controlam a verificação de índices de árvore B:

`--checkunique`: Para cada índice com restrição exclusiva verificada, verifique se não há mais de uma entrada duplicada visível no índice usando a opção (amcheck.md "F.1. amcheck — tools to verify table and index consistency") de `checkunique`.

`--heapallindexed`: Para cada índice verificado, verifique a presença de todos os tuplos de pilha como tuplos de índice no índice usando a opção (amcheck.md "F.1. amcheck — tools to verify table and index consistency") de `heapallindexed`.

`--parent-check`: Para cada índice btree verificado, use a função (amcheck.md "F.1. amcheck — tools to verify table and index consistency") de [amcheck]`bt_index_parent_check`, que realiza verificações adicionais de relações pai/filho durante a verificação do índice.

O padrão é usar a função `bt_index_check` do amcheck, mas observe que o uso da opção `--rootdescend` seleciona implicitamente `bt_index_parent_check`.

`--rootdescend`: Para cada índice verificado, encontre novamente os tuplos no nível de folha, realizando uma nova pesquisa a partir da página raiz para cada tupla usando a opção `rootdescend` do [amcheck](amcheck.md "F.1. amcheck — tools to verify table and index consistency").

O uso desta opção também seleciona implicitamente a opção `--parent-check`.

Essa forma de verificação foi originalmente escrita para ajudar no desenvolvimento de recursos do índice btree. Pode ser de uso limitado ou até mesmo sem utilidade para ajudar a detectar os tipos de corrupção que ocorrem na prática. Também pode fazer com que a verificação de corrupção leve consideravelmente mais tempo e consuma consideravelmente mais recursos no servidor.

### Aviso

Os verificações adicionais realizadas em índices de árvore B quando a opção `--parent-check` ou a opção `--rootdescend` é especificada exigem bloqueios relativamente fortes em nível de relação. Essas verificações são as únicas que bloquearão a modificação de dados concorrente dos comandos `INSERT`, `UPDATE` e `DELETE`.

As opções de linha de comando a seguir controlam a conexão com o servidor:

`-h hostname` `--host=hostname`: Especifica o nome do host da máquina em que o servidor está sendo executado. Se o valor começar com uma barra, ele é usado como o diretório para o socket de domínio Unix.

`-p port` `--port=port`: Especifica a porta TCP ou a extensão de arquivo de soquete de domínio Unix local em que o servidor está ouvindo conexões.

`-U` `--username=username`: Nome do usuário para se conectar como.

`-w` `--no-password`: Nunca emita um prompt de senha. Se o servidor exigir autenticação por senha e uma senha não estiver disponível por outros meios, como um arquivo `.pgpass`, a tentativa de conexão falhará. Esta opção pode ser útil em trabalhos em lote e scripts onde nenhum usuário está presente para inserir uma senha.

`-W` `--password`: Forçar o pg_amcheck a solicitar uma senha antes de se conectar a um banco de dados.

Essa opção nunca é essencial, pois o pg_amcheck solicitará automaticamente uma senha se o servidor exigir autenticação por senha. No entanto, o pg_amcheck desperdiçará uma tentativa de conexão descobrindo que o servidor deseja uma senha. Em alguns casos, vale a pena digitar `-W` para evitar a tentativa extra de conexão.

`--maintenance-db=dbname`: Especifica um banco de dados ou uma [string de conexão](libpq-connect.md#LIBPQ-CONNSTRING "32.1.1. Connection Strings") a ser usado para descobrir a lista de bancos de dados a serem verificados. Se nem `--all` nem qualquer opção que inclua um padrão de banco de dados for usada, nenhuma conexão é necessária e esta opção não faz nada. Caso contrário, quaisquer parâmetros de string de conexão, exceto o nome do banco de dados, que estejam incluídos no valor desta opção, também serão usados ao se conectar aos bancos de dados que estão sendo verificados. Se esta opção for omitida, o padrão é `postgres` ou, se isso falhar, `template1`.

Outras opções também estão disponíveis:

`-e` `--echo`: Eje todos os SQL enviados ao servidor para a saída padrão (stdout).

`-j num` `--jobs=num`: Use *`num`* conexões concorrentes ao servidor, ou uma por objeto a ser verificado, o que for menor.

O padrão é usar uma única conexão.

`-P` `--progress`: Mostrar informações de progresso. As informações de progresso incluem o número de relações para as quais a verificação foi concluída e o tamanho total dessas relações. Também inclui o número total de relações que serão verificadas e o tamanho estimado dessas relações.

`-v` `--verbose`: Imprimir mais mensagens. Em particular, isso imprimirá uma mensagem para cada relação que está sendo verificada e aumentará o nível de detalhe mostrado para erros no servidor.

`-V` `--version`: Imprimir a versão do pg_amcheck e sair.

`--install-missing` `--install-missing=schema`: Instale todas as extensões ausentes que são necessárias para verificar o(s) banco(s) de dados. Se ainda não instaladas, os objetos de cada extensão serão instalados no *`schema`* fornecido, ou, se não especificado, no esquema `pg_catalog`.

Atualmente, a única extensão necessária é [amcheck][(amcheck.md "F.1. amcheck — tools to verify table and index consistency")].

`-?` `--help`: Mostrar ajuda sobre os argumentos da linha de comando do comando pg_amcheck e sair.

## Meio Ambiente

`pg_amcheck`, como a maioria das outras utilidades do PostgreSQL, também utiliza as variáveis de ambiente suportadas pelo libpq (consulte a Seção 32.15 (libpq-envars.md "32.15. Environment Variables")).

A variável de ambiente `PG_COLOR` especifica se a cor deve ser usada nas mensagens de diagnóstico. Os valores possíveis são `always`, `auto` e `never`.

## Notas

O pg_amcheck foi projetado para funcionar com o PostgreSQL 14.0 e versões posteriores.

## Veja também

[amcheck](amcheck.md "F.1. amcheck — tools to verify table and index consistency")
