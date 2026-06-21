## 19.11. Definições padrão de conexão do cliente [#](#RUNTIME-CONFIG-CLIENT)

* [19.11.1. Declaração de comportamento](runtime-config-client.md#RUNTIME-CONFIG-CLIENT-STATEMENT)
* [19.11.2. Local e formatação](runtime-config-client.md#RUNTIME-CONFIG-CLIENT-FORMAT)
* [19.11.3. Pré-carga de biblioteca compartilhada](runtime-config-client.md#RUNTIME-CONFIG-CLIENT-PRELOAD)
* [19.11.4. Outros padrões](runtime-config-client.md#RUNTIME-CONFIG-CLIENT-OTHER)

### 19.11.1. Declaração de comportamento [#](#RUNTIME-CONFIG-CLIENT-STATEMENT)

`client_min_messages` (`enum`) [#](#GUC-CLIENT-MIN-MESSAGES): Controla quais níveis de [mensagens](runtime-config-logging.md#RUNTIME-CONFIG-SEVERITY-LEVELS "Table 19.2. Message Severity Levels") são enviados ao cliente. Os valores válidos são `DEBUG5`, `DEBUG4`, `DEBUG3`, `DEBUG2`, `DEBUG1`, `LOG`, `NOTICE`, `WARNING` e `ERROR`. Cada nível inclui todos os níveis que o seguem. Quanto mais recente o nível, menos mensagens são enviadas. O padrão é `NOTICE`. Note que `LOG` tem um rank diferente aqui do que em [mensagens_mínimas](runtime-config-logging.md#GUC-LOG-MIN-MESSAGES).

Mensagens de nível `INFO` são sempre enviadas ao cliente.

`search_path` (`string`) [#](#GUC-SEARCH-PATH): Esta variável especifica a ordem em que os esquemas são pesquisados quando um objeto (tabela, tipo de dados, função, etc.) é referenciado por um nome simples sem esquema especificado. Quando existem objetos com nomes idênticos em diferentes esquemas, o primeiro encontrado no caminho de pesquisa é usado. Um objeto que não está em nenhum dos esquemas no caminho de pesquisa só pode ser referenciado especificando seu esquema contendo um nome qualificado (com pontos).

O valor para `search_path` deve ser uma lista de nomes de esquema separados por vírgula. Qualquer nome que não seja um esquema existente ou que seja um esquema para o qual o usuário não tenha permissão `USAGE` é ignorado silenciosamente.

Se um dos itens da lista for o nome especial `$user`, o esquema que tem o nome retornado por `CURRENT_USER` é substituído, se houver um esquema desse e o usuário tenha permissão `USAGE` para ele. (Se não, `$user` é ignorado.)

O esquema do catálogo do sistema, `pg_catalog`, é sempre pesquisado, independentemente de ser mencionado no caminho ou não. Se for mencionado no caminho, ele será pesquisado na ordem especificada. Se `pg_catalog` não estiver no caminho, ele será pesquisado *antes* de pesquisar qualquer um dos itens do caminho.

Da mesma forma, o esquema de tabela temporária da sessão atual, `pg_temp_nnn`, é sempre procurado se ele existir. Pode ser explicitamente listado no caminho usando o alias `pg_temp`. Se não estiver listado no caminho, ele é procurado primeiro (mesmo antes de `pg_catalog`). No entanto, o esquema temporário é procurado apenas para nomes de relação (tabela, visão, sequência, etc.) e nomes de tipos de dados. Nunca é procurado para nomes de função ou operadores.

Quando os objetos são criados sem especificar um esquema de destino particular, eles serão colocados no primeiro esquema válido nomeado em `search_path`. Um erro é relatado se o caminho de busca estiver vazio.

O valor padrão para este parâmetro é `"$user", public`. Esta configuração suporta o uso compartilhado de um banco de dados (onde nenhum usuário tem esquemas privados e todos compartilham o uso de `public`), esquemas privados por usuário e combinações desses. Outros efeitos podem ser obtidos alterando o ajuste do caminho de busca padrão, seja globalmente ou por usuário.

Para mais informações sobre o manuseio de esquemas, consulte [Seção 5.10][(ddl-schemas.md "5.10. Schemas")]. Em particular, a configuração padrão é adequada apenas quando o banco de dados tem um único usuário ou alguns usuários que se confiam mutuamente.

O valor efetivo atual do caminho de busca pode ser examinado através da função SQL `current_schemas` (ver [Seção 9.27] (functions-info.md "9.27. System Information Functions and Operators")). Isso não é exatamente o mesmo que examinar o valor de `search_path`, pois `current_schemas` mostra como os itens que aparecem em `search_path` foram resolvidos.

`row_security` (`boolean`) [#](#GUC-ROW-SECURITY): Esta variável controla se deve gerar um erro em vez de aplicar uma política de segurança de linha. Quando definida como `on`, as políticas são aplicadas normalmente. Quando definida como `off`, as consultas falham, o que de outra forma aplicaria pelo menos uma política. A opção padrão é `on`. Altere para `off` quando a visibilidade limitada da linha pode causar resultados incorretos; por exemplo, o pg_dump faz essa alteração por padrão. Esta variável não tem efeito em papéis que contornam toda a política de segurança de linha, ou seja, superusuários e papéis com o atributo `BYPASSRLS`.

Para mais informações sobre políticas de segurança de linha, consulte [CREATE POLICY](sql-createpolicy.md "CREATE POLICY").

`default_table_access_method` (`string`) [#](#GUC-DEFAULT-TABLE-ACCESS-METHOD): Este parâmetro especifica o método de acesso à tabela padrão a ser usado ao criar tabelas ou visualizações materializadas, se o comando `CREATE` não especificar explicitamente um método de acesso, ou quando `SELECT ... INTO` é usado, o que não permite especificar um método de acesso à tabela. O padrão é `heap`.

`default_tablespace` (`string`) [#](#GUC-DEFAULT-TABLESPACE): Esta variável especifica o espaço de tabela padrão no qual os objetos (tabelas e índices) serão criados quando um comando `CREATE` não especificar explicitamente um espaço de tabela.

O valor é o nome de um espaço de tabela, ou uma string vazia para especificar o uso do espaço de tabela padrão do banco de dados atual. Se o valor não corresponder ao nome de qualquer espaço de tabela existente, o PostgreSQL usará automaticamente o espaço de tabela padrão do banco de dados atual. Se um espaço de tabela não padrão for especificado, o usuário deve ter o privilégio `CREATE`, ou as tentativas de criação falharão.

Essa variável não é usada para tabelas temporárias; para elas, [temp_tablespaces][(runtime-config-client.md#GUC-TEMP-TABLESPACES)] é consultado em vez disso.

Essa variável também não é usada ao criar bancos de dados. Por padrão, um novo banco de dados herda sua configuração de espaço de tabela do banco de dados de modelo do qual é copiado.

Se este parâmetro for definido com um valor diferente da string vazia quando uma tabela dividida for criada, o espaço de tabela da tabela dividida será definido com esse valor, que será usado como o espaço de tabela padrão para as partições criadas no futuro, mesmo que `default_tablespace` tenha sido alterado desde então.

Para mais informações sobre tablespaces, consulte [Seção 22.6][(manage-ag-tablespaces.md "22.6. Tablespaces")].

`default_toast_compression` (`enum`) [#](#GUC-DEFAULT-TOAST-COMPRESSION): Esta variável define o método de compressão padrão para valores de colunas compressivas. (Isso pode ser sobrescrito para colunas individuais definindo a opção de coluna `COMPRESSION` em `CREATE TABLE` ou `ALTER TABLE`.). Os métodos de compressão suportados são `pglz` e (se o PostgreSQL foi compilado com `--with-lz4`) `lz4`. O padrão é `pglz`.

`temp_tablespaces` (`string`) [#](#GUC-TEMP-TABLESPACES): Esta variável especifica os tablespaces nos quais criar objetos temporários (mesas temporárias e índices em mesas temporárias) quando um comando `CREATE` não especifica explicitamente um tablespace. Arquivos temporários para fins, como classificação de grandes conjuntos de dados, também são criados nesses tablespaces.

O valor é uma lista de nomes de espaços de tabela. Quando há mais de um nome na lista, o PostgreSQL escolhe um membro aleatório da lista cada vez que um objeto temporário deve ser criado; exceto que, dentro de uma transação, os objetos temporários sucessivamente criados são colocados em espaços de tabela sucessivos da lista. Se o elemento selecionado da lista for uma string vazia, o PostgreSQL usará automaticamente o espaço de tabela padrão do banco de dados atual.

Quando `temp_tablespaces` é definido interativamente, especificar um espaço de tabela inexistente é um erro, assim como especificar um espaço de tabela para o qual o usuário não tem privilégio `CREATE`. No entanto, ao usar um valor previamente definido, espaços de tabela inexistentes são ignorados, assim como espaços de tabela para os quais o usuário não tem privilégio `CREATE`. Em particular, esta regra se aplica ao usar um valor definido em `postgresql.conf`.

O valor padrão é uma string vazia, o que resulta na criação de todos os objetos temporários nos espaços de tabela padrão do banco de dados atual.

Veja também [default_tablespace][(runtime-config-client.md#GUC-DEFAULT-TABLESPACE)].

`check_function_bodies` (`boolean`) [#](#GUC-CHECK-FUNCTION-BODIES): Este parâmetro está normalmente ativado. Quando definido como `off`, desativa a validação da string do corpo da rotina durante [CREATE FUNCTION](sql-createfunction.md "CREATE FUNCTION") e [CREATE PROCEDURE](sql-createprocedure.md "CREATE PROCEDURE"). Desativar a validação evita efeitos colaterais do processo de validação, em particular, impedindo falsos positivos devido a problemas como referências diretas. Defina este parâmetro como `off` antes de carregar funções em nome de outros usuários; o pg_dump faz isso automaticamente.

`default_transaction_isolation` (`enum`) [#](#GUC-DEFAULT-TRANSACTION-ISOLATION): Cada transação SQL tem um nível de isolamento, que pode ser “não comprometido”, “comprometido”, “leitura repetida” ou “serializável”. Este parâmetro controla o nível de isolamento padrão de cada nova transação. O padrão é “não comprometido”.

Consulte o [Capítulo 13](mvcc.md "Chapter 13. Concurrency Control") e [SET TRANSACTION](sql-set-transaction.md "SET TRANSACTION") para obter mais informações.

`default_transaction_read_only` (`boolean`) [#](#GUC-DEFAULT-TRANSACTION-READ-ONLY): Uma transação SQL somente leitura não pode alterar tabelas não temporárias. Este parâmetro controla o status padrão somente leitura de cada nova transação. O padrão é `off` (leitura/escrita).

Consulte [SET TRANSACTION](sql-set-transaction.md "SET TRANSACTION") para obter mais informações.

`default_transaction_deferrable` (`boolean`) [#](#GUC-DEFAULT-TRANSACTION-DEFERRABLE): Quando executada no nível de isolamento `serializable`, uma transação SQL somente de leitura deferível pode ser adiada antes de ser permitida para prosseguir. No entanto, uma vez que ela começa a ser executada, não incorre em nenhum dos custos necessários para garantir a serializabilidade; portanto, o código de serialização não terá motivos para forçá-la a abortar devido a atualizações concorrentes, tornando essa opção adequada para transações somente de leitura de longa duração.

Este parâmetro controla o status padrão deferível de cada nova transação. Atualmente, ele não tem efeito em transações de leitura e escrita ou aquelas que operam em níveis de isolamento inferiores a `serializable`. O padrão é `off`.

Consulte [SET TRANSACTION](sql-set-transaction.md "SET TRANSACTION") para obter mais informações.

`transaction_isolation` (`enum`) [#](#GUC-TRANSACTION-ISOLATION): Este parâmetro reflete o nível de isolamento da transação atual. No início de cada transação, ele é definido pelo valor atual de [default_transaction_isolation](runtime-config-client.md#GUC-DEFAULT-TRANSACTION-ISOLATION). Qualquer tentativa subsequente de alterá-lo é equivalente a um comando [SET TRANSACTION](sql-set-transaction.md "SET TRANSACTION").

`transaction_read_only` (`boolean`) [#](#GUC-TRANSACTION-READ-ONLY): Este parâmetro reflete o status de leitura somente do transação atual. No início de cada transação, ele é definido pelo valor atual de [default_transaction_read_only](runtime-config-client.md#GUC-DEFAULT-TRANSACTION-READ-ONLY). Qualquer tentativa subsequente de alterá-lo é equivalente a um comando de [SET TRANSACTION](sql-set-transaction.md "SET TRANSACTION").

`transaction_deferrable` (`boolean`) [#](#GUC-TRANSACTION-DEFERRABLE): Este parâmetro reflete o status de deferibilidade da transação atual. No início de cada transação, ele é definido pelo valor atual de [default_transaction_deferrable](runtime-config-client.md#GUC-DEFAULT-TRANSACTION-DEFERRABLE). Qualquer tentativa subsequente de alterá-lo é equivalente a um comando de [SET TRANSACTION](sql-set-transaction.md "SET TRANSACTION").

`session_replication_role` (`enum`) [#](#GUC-SESSION-REPLICATION-ROLE): Controla o disparo de gatilhos relacionados à replicação e as regras para a sessão atual. Os valores possíveis são `origin` (o padrão), `replica` e `local`. Definir este parâmetro resulta no descarte de quaisquer planos de consulta previamente armazenados na cache. Somente usuários super e usuários com o privilégio apropriado `SET` podem alterar esta configuração.

O uso pretendido deste ajuste é que os sistemas de replicação lógica o definam como `replica` quando estão aplicando mudanças replicadas. O efeito disso será que os gatilhos e as regras (que não tenham sido alteradas de sua configuração padrão) não serão acionados na replica. Consulte as cláusulas `ALTER TABLE`(sql-altertable.md "ALTER TABLE") `ENABLE TRIGGER` e `ENABLE RULE` para mais informações.

O PostgreSQL trata os parâmetros `origin` e `local` da mesma forma internamente. Sistemas de replicação de terceiros podem usar esses dois valores para seus propósitos internos, por exemplo, usando `local` para designar uma sessão cujas mudanças não devem ser replicadas.

Como as chaves estrangeiras são implementadas como gatilhos, definir este parâmetro para `replica` também desativa todas as verificações de chave estrangeira, o que pode deixar os dados em um estado inconsistente se usado de forma inadequada.

`statement_timeout` (`integer`) [#](#GUC-STATEMENT-TIMEOUT): Aborde qualquer declaração que leve mais do que o tempo especificado. Se `log_min_error_statement` estiver definido como `ERROR` ou menor, a declaração que expirou também será registrada. Se este valor for especificado sem unidades, ele será considerado em milissegundos. Um valor de zero (padrão) desativa o tempo de espera.

O tempo de espera é medido a partir do momento em que um comando chega ao servidor até que ele seja completado pelo servidor. Se várias instruções SQL aparecem em uma única mensagem de consulta simples, o tempo de espera é aplicado a cada declaração separadamente. (As versões do PostgreSQL anteriores a 13 geralmente tratavam o tempo de espera como aplicável a todo o conjunto de consulta.) No protocolo de consulta estendida, o tempo de espera começa a ser executado quando qualquer mensagem relacionada à consulta (Parse, Bind, Execute, Describe) chega e é cancelada pela conclusão de uma mensagem Execute ou Sync.

Não é recomendado definir `statement_timeout` em `postgresql.conf`, pois isso afetaria todas as sessões.

`transaction_timeout` (`integer`) [#](#GUC-TRANSACTION-TIMEOUT): Finalize qualquer sessão que ultrapasse o período especificado em uma transação. O limite se aplica tanto a transações explícitas (iniciadas com `BEGIN`) quanto a uma transação implicitamente iniciada correspondente a uma única declaração. Se este valor for especificado sem unidades, ele é considerado em milissegundos. Um valor de zero (padrão) desativa o tempo de espera.

Se `transaction_timeout` for mais curto ou igual a `idle_in_transaction_session_timeout` ou `statement_timeout`, o tempo de espera mais longo é ignorado.

Não é recomendado definir `transaction_timeout` em `postgresql.conf`, pois isso afetaria todas as sessões.

### Nota

As transações preparadas não estão sujeitas a esse limite de tempo.

`lock_timeout` (`integer`) [#](#GUC-LOCK-TIMEOUT): Aborta qualquer declaração que espere mais tempo do que o período especificado ao tentar adquirir um bloqueio em uma tabela, índice, linha ou outro objeto do banco de dados. O limite de tempo se aplica separadamente a cada tentativa de aquisição de bloqueio. O limite se aplica tanto a solicitações de bloqueio explícitas (como `LOCK TABLE`, ou `SELECT FOR UPDATE` sem `NOWAIT`) quanto a bloqueios adquiridos implicitamente. Se este valor for especificado sem unidades, ele é considerado em milissegundos. Um valor de zero (o padrão) desativa o tempo limite.

Ao contrário de `statement_timeout`, esse tempo de espera só pode ocorrer enquanto se está aguardando por bloqueios. Observe que, se `statement_timeout` não for nulo, não faz muito sentido definir `lock_timeout` com o mesmo valor ou um valor maior, uma vez que o tempo de espera da declaração sempre será ativado primeiro. Se `log_min_error_statement` estiver definido como `ERROR` ou menor, a declaração que expirou será registrada.

Não é recomendado definir `lock_timeout` em `postgresql.conf`, pois isso afetaria todas as sessões.

`idle_in_transaction_session_timeout` (`integer`) [#](#GUC-IDLE-IN-TRANSACTION-SESSION-TIMEOUT): Finalize qualquer sessão que esteja inativa (ou seja, esperando uma consulta do cliente) dentro de uma transação aberta por mais tempo do que o período especificado. Se este valor for especificado sem unidades, ele será considerado em milissegundos. Um valor de zero (o padrão) desativa o tempo de espera.

Essa opção pode ser usada para garantir que as sessões ociosas não mantenham bloqueios por um período indevido. Mesmo quando não há bloqueios significativos, uma transação aberta impede a limpeza de tuplas recentemente mortas que podem ser visíveis apenas para essa transação; portanto, permanecer ocioso por um longo período pode contribuir para o bloat da tabela. Consulte [Seção 24.1] para obter mais detalhes.

`idle_session_timeout` (`integer`) [#](#GUC-IDLE-SESSION-TIMEOUT): Finalize qualquer sessão que esteja inativa (ou seja, esperando uma consulta do cliente), mas não dentro de uma transação aberta, por mais tempo do que o período especificado. Se este valor for especificado sem unidades, ele é considerado em milissegundos. Um valor de zero (o padrão) desativa o tempo de espera.

Ao contrário do caso de uma transação aberta, uma sessão inativa sem uma transação não impõe grandes custos ao servidor, portanto, há menos necessidade de habilitar esse tempo de espera do que `idle_in_transaction_session_timeout`.

Cuidado ao aplicar esse tempo limite em conexões feitas por meio de software de pool de conexões ou outro middleware, pois essa camada pode não reagir bem a fechamento inesperado de conexão. Pode ser útil habilitar esse tempo limite apenas para sessões interativas, talvez aplicando-o apenas a usuários específicos.

`bytea_output` (`enum`) [#](#GUC-BYTEA-OUTPUT): Define o formato de saída para valores do tipo `bytea`. Os valores válidos são `hex` (o padrão) e `escape` (o formato tradicional do PostgreSQL). Consulte [Seção 8.4](datatype-binary.md "8.4. Binary Data Types") para obter mais informações. O tipo `bytea` sempre aceita ambos os formatos na entrada, independentemente desta configuração.

`xmlbinary` (`enum`) [#](#GUC-XMLBINARY): Define como os valores binários devem ser codificados no XML. Isso se aplica, por exemplo, quando os valores de `bytea` são convertidos para XML pelas funções `xmlelement` ou `xmlforest`. Os valores possíveis são `base64` e `hex`, que são ambos definidos no padrão do XML Schema. O padrão é `base64`. Para obter mais informações sobre funções relacionadas ao XML, consulte [Seção 9.15](functions-xml.md "9.15. XML Functions").

A escolha real aqui é, na maioria das vezes, uma questão de gosto, limitada apenas por possíveis restrições em aplicações de clientes. Ambos os métodos suportam todos os valores possíveis, embora a codificação hexadecimal seja um pouco maior do que a codificação base64.

`xmloption` (`enum`) [#](#GUC-XMLOPTION): Define se `DOCUMENT` ou `CONTENT` é implícito ao converter entre valores de XML e cadeia de caracteres. Consulte [Seção 8.13](datatype-xml.md "8.13. XML Type") para uma descrição disso. Os valores válidos são `DOCUMENT` e `CONTENT`. O padrão é `CONTENT`.

De acordo com o padrão SQL, o comando para definir essa opção é

``` SET XML OPTION { DOCUMENT | CONTENT };
    ```

Essa sintaxe também está disponível no PostgreSQL.

`gin_pending_list_limit` (`integer`) [#](#GUC-GIN-PENDING-LIST-LIMIT): Define o tamanho máximo da lista pendente de um índice GIN, que é usado quando o `fastupdate` está habilitado. Se a lista crescer para um tamanho maior que este máximo, ela é limpa movendo as entradas nela para a estrutura de dados principal do GIN do índice em massa. Se este valor for especificado sem unidades, ele é considerado em kilobytes. O padrão é quatro megabytes (`4MB`). Este ajuste pode ser sobrescrito para índices GIN individuais alterando os parâmetros de armazenamento do índice. Consulte [Seção 65.4.4.1](gin.md#GIN-FAST-UPDATE "65.4.4.1. GIN Fast Update Technique") e [Seção 65.4.5](gin.md#GIN-TIPS "65.4.5. GIN Tips and Tricks") para mais informações.

`createrole_self_grant` (`string`) [#](#GUC-CREATEROLE-SELF-GRANT): Se um usuário que tem `CREATEROLE`, mas não `SUPERUSER`, criar um papel, e se este for definido com um valor não vazio, o papel recém-criado será concedido ao usuário criador com as opções especificadas. O valor deve ser `set`, `inherit`, ou uma lista de vírgulas separadas desses. O valor padrão é uma string vazia, que desativa o recurso.

O propósito desta opção é permitir que um usuário `CREATEROLE` que não é um superusuário herde automaticamente ou adquira automaticamente a capacidade de `SET ROLE` para quaisquer usuários criados. Como um usuário `CREATEROLE` sempre é implicitamente concedido `ADMIN OPTION` em papéis criados, esse usuário pode sempre executar uma declaração `GRANT` que alcançaria o mesmo efeito que esta configuração. No entanto, por razões de usabilidade, pode ser conveniente que a concessão aconteça automaticamente. Um superusuário herda automaticamente os privilégios de todos os papéis e pode sempre `SET ROLE` para qualquer papel, e esta configuração pode ser usada para produzir um comportamento semelhante para usuários `CREATEROLE` para usuários que eles criam.

`event_triggers` (`boolean`) [#](#GUC-EVENT-TRIGGERS): Permitir a desativação temporária da execução de gatilhos de eventos para solucionar e reparar gatilhos de eventos defeituosos. Todos os gatilhos de eventos serão desativados ao definir o valor para `false`. Definir o valor para `true` permite que todos os gatilhos de eventos sejam acionados, este é o valor padrão. Somente usuários super e usuários com o privilégio apropriado `SET` podem alterar esta configuração.

`restrict_nonsystem_relation_kind` (`string`) [#](#GUC-RESTRICT-NONSYSTEM-RELATION-KIND): Defina os tipos de relação para os quais o acesso às relações não-sistemáticas é proibido. O valor assume a forma de uma lista de tipos de relação separados por vírgula. Atualmente, os tipos de relação suportados são `view` e `foreign-table`.

### 19.11.2. Local e formatação [#](#RUNTIME-CONFIG-CLIENT-FORMAT)

`DateStyle` (`string`) [#](#GUC-DATESTYLE): Define o formato de exibição para valores de data e hora, bem como as regras para a interpretação de valores de entrada de data ambíguos. Por razões históricas, esta variável contém dois componentes independentes: a especificação do formato de saída (`ISO`, `Postgres`, `SQL` ou `German`) e a especificação de entrada/saída para ordenação de ano/mês/dia (`DMY`, `MDY` ou `YMD`). Estes podem ser definidos separadamente ou juntos. As palavras-chave `Euro` e `European` são sinônimos de `DMY`; as palavras-chave `US`, `NonEuro` e `NonEuropean` são sinônimos de `MDY`. Consulte [Seção 8.5](datatype-datetime.md "8.5. Date/Time Types") para mais informações. O padrão embutido é `ISO, MDY`, mas o initdb inicializará o arquivo de configuração com uma configuração que corresponde ao comportamento do `lc_time` local escolhido.

`IntervalStyle` (`enum`) [#](#GUC-INTERVALSTYLE): Define o formato de exibição para valores de intervalo. O valor `sql_standard` produzirá saída que corresponda aos literais de intervalo padrão do SQL. O valor `postgres` (que é o padrão) produzirá saída que corresponda às versões do PostgreSQL anteriores a 8.4 quando o parâmetro `ISO` de [DateStyle] foi definido como `postgres_verbose`. O valor `postgres_verbose` produzirá saída que corresponda às versões do PostgreSQL anteriores a 8.4 quando o parâmetro `DateStyle` foi definido para saída que não seja `ISO`. O valor `iso_8601` produzirá saída que corresponda ao formato de intervalo de tempo “com designadores” definido na seção 4.4.3.2 do ISO 8601.

O parâmetro `IntervalStyle` também afeta a interpretação de entradas de intervalo ambíguas. Consulte [Seção 8.5.4][(datatype-datetime.md#DATATYPE-INTERVAL-INPUT "8.5.4. Interval Input")] para obter mais informações.

`TimeZone` (`string`) [#](#GUC-TIMEZONE): Define o fuso horário para exibir e interpretar marcas de tempo. O padrão embutido é `GMT`, mas isso é normalmente substituído em `postgresql.conf`; o initdb instalará um ajuste correspondente ao seu ambiente de sistema. Consulte [Seção 8.5.3](datatype-datetime.md#DATATYPE-TIMEZONES "8.5.3. Time Zones") para mais informações.

`timezone_abbreviations` (`string`) [#](#GUC-TIMEZONE-ABBREVIATIONS): Define a coleção de abreviações adicionais de fuso horário que serão aceitas pelo servidor para entrada de datas e horários (além de quaisquer abreviações definidas pela configuração atual do `TimeZone`). O padrão é `'Default'`, que é uma coleção que funciona na maioria do mundo; também existem `'Australia'` e `'India'`, e outras coleções podem ser definidas para uma instalação específica. Consulte [Seção B.4](datetime-config-files.md "B.4. Date/Time Configuration Files") para obter mais informações.

`extra_float_digits` (`integer`) [#](#GUC-EXTRA-FLOAT-DIGITS): Este parâmetro ajusta o número de dígitos utilizados para a saída textual de valores de ponto flutuante, incluindo os tipos de dados `float4`, `float8` e geométricos.

Se o valor for 1 (padrão) ou superior, os valores flutuantes são exibidos no formato mais curto e preciso; veja [Seção 8.1.3][(datatype-numeric.md#DATATYPE-FLOAT "8.1.3. Floating-Point Types")]. O número real de dígitos gerados depende apenas do valor que está sendo exibido, não do valor deste parâmetro. No máximo, são necessários 17 dígitos para os valores de `float8`, e 9 para os valores de `float4`. Este formato é rápido e preciso, preservando o valor binário original do float exatamente quando corretamente lido. Por compatibilidade histórica, valores de até 3 são permitidos.

Se o valor for zero ou negativo, a saída será arredondada para uma precisão decimal dada. A precisão usada é o número padrão de dígitos para o tipo (`FLT_DIG` ou `DBL_DIG`, conforme apropriado) reduzido de acordo com o valor deste parâmetro. (Por exemplo, especificar -1 fará com que os valores de `float4` sejam exibidos arredondados a 5 dígitos significativos, e os valores de `float8` arredondados a 14 dígitos.) Este formato é mais lento e não preserva todos os bits do valor binário do float, mas pode ser mais legível para humanos.

### Nota

O significado deste parâmetro e seu valor padrão foram alterados no PostgreSQL 12; consulte [Seção 8.1.3][(datatype-numeric.md#DATATYPE-FLOAT "8.1.3. Floating-Point Types")] para uma discussão adicional.

`client_encoding` (`string`) [#](#GUC-CLIENT-ENCODING): Define o codificação do lado do cliente (conjunto de caracteres). O padrão é usar a codificação do banco de dados. Os conjuntos de caracteres suportados pelo servidor PostgreSQL são descritos em [Seção 23.3.1](multibyte.md#MULTIBYTE-CHARSET-SUPPORTED "23.3.1. Supported Character Sets").

`lc_messages` (`string`) [#](#GUC-LC-MESSAGES): Define o idioma em que as mensagens são exibidas. Os valores aceitáveis dependem do sistema; consulte [Seção 23.1](locale.md "23.1. Locale Support") para obter mais informações. Se essa variável for definida como uma string vazia (que é o padrão), o valor é herdado do ambiente de execução do servidor de uma maneira dependente do sistema.

Em alguns sistemas, essa categoria de localização não existe. Definir essa variável ainda funcionará, mas não haverá efeito. Além disso, há uma chance de não existir mensagens traduzidas para o idioma desejado. Nesse caso, você continuará a ver as mensagens em inglês.

Somente superusuários e usuários com o privilégio apropriado `SET` podem alterar essa configuração.

`lc_monetary` (`string`) [#](#GUC-LC-MONETARY): Define o idioma a ser usado para formatar valores monetários, por exemplo, com a família de funções `to_char`. Os valores aceitáveis dependem do sistema; consulte [Seção 23.1](locale.md "23.1. Locale Support") para mais informações. Se essa variável for definida como uma string vazia (que é a opção padrão), o valor será herdado do ambiente de execução do servidor de uma maneira dependente do sistema.

`lc_numeric` (`string`) [#](#GUC-LC-NUMERIC): Define o local a ser utilizado para formatação de números, por exemplo, com a família de funções `to_char`. Os valores aceitáveis dependem do sistema; consulte [Seção 23.1](locale.md "23.1. Locale Support") para obter mais informações. Se essa variável for definida como uma string vazia (que é a opção padrão), o valor será herdado do ambiente de execução do servidor de uma maneira dependente do sistema.

`lc_time` (`string`) [#](#GUC-LC-TIME): Define o local a ser usado para formatação de datas e horários, por exemplo, com a família de funções `to_char`. Os valores aceitáveis dependem do sistema; consulte [Seção 23.1](locale.md "23.1. Locale Support") para mais informações. Se essa variável for definida como uma string vazia (que é o padrão), o valor é herdado do ambiente de execução do servidor de maneira dependente do sistema.

`icu_validation_level` (`enum`) [#](#GUC-ICU-VALIDATION-LEVEL): Quando problemas de validação do local do ICU são encontrados, controla qual [nível de mensagem](runtime-config-logging.md#RUNTIME-CONFIG-SEVERITY-LEVELS "Table 19.2. Message Severity Levels") é usado para relatar o problema. Os valores válidos são `DISABLED`, `DEBUG5`, `DEBUG4`, `DEBUG3`, `DEBUG2`, `DEBUG1`, `INFO`, `NOTICE`, `WARNING`, `ERROR` e `LOG`.

Se configurado em `DISABLED`, não reporta problemas de validação de forma alguma. Caso contrário, reporta problemas no nível da mensagem fornecida. O padrão é `WARNING`.

`default_text_search_config` (`string`) [#](#GUC-DEFAULT-TEXT-SEARCH-CONFIG): Seleciona a configuração de pesquisa de texto que é usada por essas variantes das funções de pesquisa de texto que não têm um argumento explícito que especifique a configuração. Consulte [Capítulo 12](textsearch.md "Chapter 12. Full Text Search") para obter mais informações. O padrão embutido é `pg_catalog.simple`, mas o initdb inicializará o arquivo de configuração com um ajuste que corresponde ao `lc_ctype` local escolhido, se uma configuração que corresponda a esse local pode ser identificada.

### 19.11.3. Pré-carregamento da Biblioteca Partilhada [#](#RUNTIME-CONFIG-CLIENT-PRELOAD)

Vários ajustes estão disponíveis para pré-carregar bibliotecas compartilhadas no servidor, a fim de carregar funcionalidades adicionais ou obter benefícios de desempenho. Por exemplo, um ajuste de `'$libdir/mylib'` faria com que `mylib.so` (ou em algumas plataformas, `mylib.sl`) fosse pré-carregado a partir do diretório da biblioteca padrão da instalação. As diferenças entre os ajustes são quando eles entram em vigor e quais privilégios são necessários para as alterar.

As bibliotecas de linguagem procedural do PostgreSQL podem ser pré-carregadas dessa maneira, tipicamente usando a sintaxe `'$libdir/plXXX'` onde `XXX` é `pgsql`, `perl`, `tcl` ou `python`.

Apenas bibliotecas compartilhadas especificamente destinadas a serem usadas com PostgreSQL podem ser carregadas dessa maneira. Cada biblioteca compatível com PostgreSQL tem um “bloco mágico” que é verificado para garantir a compatibilidade. Por esse motivo, bibliotecas que não são compatíveis com PostgreSQL não podem ser carregadas dessa maneira. Você pode ser capaz de usar recursos do sistema operacional, como `LD_PRELOAD`, para isso.

Em geral, consulte a documentação de um módulo específico para a maneira recomendada de carregar esse módulo.

`local_preload_libraries` (`string`) [#](#GUC-LOCAL-PRELOAD-LIBRARIES): Esta variável especifica uma ou mais bibliotecas compartilhadas que devem ser pré-carregadas no início da conexão. Ela contém uma lista de nomes de bibliotecas separados por vírgula, onde cada nome é interpretado como para o comando [`LOAD`](sql-load.md "LOAD"). Espaços em branco entre as entradas são ignorados; rode um nome de biblioteca com aspas duplas se você precisar incluir espaços em branco ou vírgulas no nome. O valor do parâmetro só tem efeito no início da conexão. Alterações subsequentes não têm efeito. Se uma biblioteca especificada não for encontrada, a tentativa de conexão falhará.

Essa opção pode ser definida por qualquer usuário. Por isso, as bibliotecas que podem ser carregadas são restritas àquelas que aparecem no subdiretório `plugins` do diretório da biblioteca padrão da instalação. (É responsabilidade do administrador do banco de dados garantir que apenas bibliotecas "seguras" sejam instaladas lá.) As entradas em `local_preload_libraries` podem especificar esse diretório explicitamente, por exemplo, `$libdir/plugins/mylib`, ou apenas especificar o nome da biblioteca — `mylib` teria o mesmo efeito que `$libdir/plugins/mylib`.

A intenção deste recurso é permitir que usuários não privilegiados carreguem bibliotecas de depuração ou de medição de desempenho em sessões específicas, sem exigir um comando explícito `LOAD`. Para esse fim, seria típico definir este parâmetro usando a variável de ambiente `PGOPTIONS` no cliente ou usando `ALTER ROLE SET`.

No entanto, a menos que um módulo seja projetado especificamente para ser usado dessa maneira por não-superusuários, esse geralmente não é o ajuste correto a ser usado. Veja [session_preload_libraries][(runtime-config-client.md#GUC-SESSION-PRELOAD-LIBRARIES)] em vez disso.

`session_preload_libraries` (`string`) [#](#GUC-SESSION-PRELOAD-LIBRARIES): Esta variável especifica uma ou mais bibliotecas compartilhadas que devem ser pré-carregadas no início da conexão. Ela contém uma lista de nomes de bibliotecas separados por vírgula, onde cada nome é interpretado como para o comando [`LOAD`(sql-load.md "LOAD")]. Espaços em branco entre as entradas são ignorados; rode um nome de biblioteca com aspas duplas se você precisar incluir espaços em branco ou vírgulas no nome. O valor do parâmetro só tem efeito no início da conexão. Alterações subsequentes não têm efeito. Se uma biblioteca especificada não for encontrada, a tentativa de conexão falhará. Somente superusuários e usuários com o privilégio apropriado `SET` podem alterar esta configuração.

A intenção deste recurso é permitir que bibliotecas de depuração ou de medição de desempenho sejam carregadas em sessões específicas sem que um comando explícito `LOAD` seja dado. Por exemplo, [auto_explain][(auto-explain.md "F.3. auto_explain — log execution plans of slow queries")] pode ser habilitado para todas as sessões sob um nome de usuário dado, definindo este parâmetro com `ALTER ROLE SET`. Além disso, este parâmetro pode ser alterado sem reiniciar o servidor (mas as alterações só se tornam eficazes quando uma nova sessão é iniciada), portanto, é mais fácil adicionar novos módulos dessa maneira, mesmo que eles devam ser aplicados a todas as sessões.

Ao contrário de [shared_preload_libraries][(runtime-config-client.md#GUC-SHARED-PRELOAD-LIBRARIES)], não há uma grande vantagem de desempenho ao carregar uma biblioteca no início da sessão em vez de quando ela é usada pela primeira vez. Há, no entanto, uma vantagem quando o pooling de conexão é usado.

`shared_preload_libraries` (`string`) [#](#GUC-SHARED-PRELOAD-LIBRARIES): Esta variável especifica uma ou mais bibliotecas compartilhadas a serem pré-carregadas no início do servidor. Ela contém uma lista de nomes de bibliotecas separados por vírgula, onde cada nome é interpretado como para o comando [`LOAD`](sql-load.md "LOAD"). Espaços em branco entre as entradas são ignorados; envolva o nome de uma biblioteca com aspas duplas se você precisar incluir espaços em branco ou vírgulas no nome. Este parâmetro só pode ser definido no início do servidor. Se uma biblioteca especificada não for encontrada, o servidor falhará no início.

Algumas bibliotecas precisam realizar certas operações que só podem ocorrer no início do postmaster, como alocar memória compartilhada, reservar bloqueios leves ou iniciar trabalhadores em segundo plano. Essas bibliotecas devem ser carregadas no início do servidor por meio deste parâmetro. Consulte a documentação de cada biblioteca para obter detalhes.

Outras bibliotecas também podem ser pré-carregadas. Ao pré-carregar uma biblioteca compartilhada, o tempo de inicialização da biblioteca é evitado quando a biblioteca é usada pela primeira vez. No entanto, o tempo para iniciar cada novo processo do servidor pode aumentar ligeiramente, mesmo que esse processo nunca use a biblioteca. Portanto, este parâmetro é recomendado apenas para bibliotecas que serão usadas na maioria das sessões. Além disso, alterar este parâmetro requer um reinício do servidor, então este não é o ajuste certo para usar em tarefas de depuração de curto prazo, por exemplo. Use [session_preload_libraries][(runtime-config-client.md#GUC-SESSION-PRELOAD-LIBRARIES)] para isso, em vez disso.

### Nota

Em hosts Windows, o pré-carregamento de uma biblioteca no início do servidor não reduzirá o tempo necessário para iniciar cada novo processo do servidor; cada processo do servidor recarregará todas as bibliotecas pré-carregadas. No entanto, `shared_preload_libraries` ainda é útil em hosts Windows para bibliotecas que precisam realizar operações no momento do início do postmaster.

`jit_provider` (`string`) [#](#GUC-JIT-PROVIDER): Esta variável é o nome da biblioteca do provedor JIT a ser utilizada (ver [Seção 30.4.2](jit-extensibility.md#JIT-PLUGGABLE "30.4.2. Pluggable JIT Providers")). O padrão é `llvmjit`. Este parâmetro só pode ser definido no início do servidor.

Se configurada para uma biblioteca não existente, o JIT não estará disponível, mas não será gerado nenhum erro. Isso permite que o suporte JIT seja instalado separadamente do pacote principal do PostgreSQL.

### 19.11.4. Outros Defeitos [#](#RUNTIME-CONFIG-CLIENT-OTHER)

`dynamic_library_path` (`string`) [#](#GUC-DYNAMIC-LIBRARY-PATH): Se um módulo dinamicamente carregável precisar ser aberto e o nome do arquivo especificado no comando `CREATE FUNCTION` ou `LOAD` não tiver um componente de diretório (ou seja, o nome não contenha uma barra), o sistema buscará esse caminho para o arquivo necessário.

O valor para `dynamic_library_path` deve ser uma lista de caminhos de diretório absolutos separados por colchetes (ou pontos e vírgulas no Windows). Se um elemento da lista começar com a string especial `$libdir`, o diretório da biblioteca de pacotes do PostgreSQL integrado é substituído por `$libdir`; é onde os módulos fornecidos pela distribuição padrão do PostgreSQL são instalados. (Use `pg_config --pkglibdir` para descobrir o nome desse diretório. Por exemplo:

``` dynamic_library_path = '/usr/local/lib/postgresql:/home/my_project/lib:$libdir'
    ```

ou, em um ambiente Windows:

    ```
    dynamic_library_path = 'C:\tools\postgresql;H:\my_project\lib;$libdir'
    ```

O valor padrão para este parâmetro é `'$libdir'`. Se o valor for definido como uma string vazia, a busca automática de caminho é desativada.

Este parâmetro pode ser alterado em tempo real por superusuários e usuários com o privilégio apropriado `SET`, mas uma configuração feita dessa forma só persistirá até o final da conexão do cliente, portanto, esse método deve ser reservado para fins de desenvolvimento. A maneira recomendada para definir este parâmetro é no arquivo de configuração `postgresql.conf`.

`extension_control_path` (`string`) [#](#GUC-EXTENSION-CONTROL-PATH)
:   Um caminho para procurar extensões, especificamente arquivos de controle de extensão
    (`name.control`). O restante do script de extensão e os arquivos de controle secundários são então carregados
    do mesmo diretório onde o arquivo de controle primário foi encontrado.
    Veja [Seção 36.17.1](extend-extensions.md#EXTEND-EXTENSIONS-FILES "36.17.1. Extension Files") para detalhes.

O valor para `extension_control_path` deve ser uma lista de caminhos de diretório absolutos separados por colchetes (ou pontos e vírgulas em Windows). Se um elemento da lista começar com a string especial `$system`, o diretório da extensão PostgreSQL incorporada é substituído por `$system`; é aqui que as extensões fornecidas pela distribuição padrão do PostgreSQL são instaladas. (Use `pg_config --sharedir` para descobrir o nome desse diretório.) Por exemplo:

    ```
    extension_control_path = '/usr/local/share/postgresql:/home/my_project/share:$system'
    ```

ou, em um ambiente Windows:

    ```
    extension_control_path = 'C:\tools\postgresql;H:\my_project\share;$system'
    ```

Observe que os elementos de caminho especificados devem ter um subdiretório `extension` que conterá os arquivos `.control` e `.sql`; o sufixo `extension` é automaticamente anexado a cada elemento de caminho.

O valor padrão para este parâmetro é `'$system'`. Se o valor for definido como uma string vazia, também é assumido o valor padrão `'$system'`.

Se houver extensões com nomes iguais em vários diretórios no caminho configurado, apenas a instância encontrada primeiro no caminho será usada.

Este parâmetro pode ser alterado em tempo real por superusuários e usuários com o privilégio apropriado `SET`, mas uma configuração feita dessa forma só persistirá até o final da conexão do cliente, portanto, esse método deve ser reservado para fins de desenvolvimento. A maneira recomendada para definir este parâmetro é no arquivo de configuração `postgresql.conf`.

Observe que, se você definir esse parâmetro para poder carregar extensões de locais não padrão, você provavelmente também precisará definir [dynamic_library_path][(runtime-config-client.md#GUC-DYNAMIC-LIBRARY-PATH)] para um local correspondente, por exemplo,

    ```
    extension_control_path = '/usr/local/share/postgresql:$system' dynamic_library_path = '/usr/local/lib/postgresql:$libdir'
    ```

`gin_fuzzy_search_limit` (`integer`) [#](#GUC-GIN-FUZZY-SEARCH-LIMIT)
:   Limite suave do tamanho do conjunto retornado por varreduras de índice GIN. Para mais informações, consulte [Seção 65.4.5](gin.md#GIN-TIPS "65.4.5. GIN Tips and Tricks").