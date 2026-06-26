## F.38. postgres_fdw — acesso a dados armazenados em servidores externos PostgreSQL [#](#POSTGRES-FDW)

* [F.38.1. Opções de FDW de postgres_fdw](postgres-fdw.md#POSTGRES-FDW-OPTIONS)
* [F.38.2. Funções](postgres-fdw.md#POSTGRES-FDW-FUNCTIONS)
* [F.38.3. Gerenciamento de Conexão](postgres-fdw.md#POSTGRES-FDW-CONNECTION-MANAGEMENT)
* [F.38.4. Gerenciamento de Transação](postgres-fdw.md#POSTGRES-FDW-TRANSACTION-MANAGEMENT)
* [F.38.5. Otimização de Consulta Remota](postgres-fdw.md#POSTGRES-FDW-REMOTE-QUERY-OPTIMIZATION)
* [F.38.6. Ambiente de Execução de Consulta Remota](postgres-fdw.md#POSTGRES-FDW-REMOTE-QUERY-EXECUTION-ENVIRONMENT)
* [F.38.7. Compatibilidade entre Versões Cruzadas](postgres-fdw.md#POSTGRES-FDW-CROSS-VERSION-COMPATIBILITY)
* [F.38.8. Eventos de Aguardar](postgres-fdw.md#POSTGRES-FDW-WAIT-EVENTS)
* [F.38.9. Parâmetros de Configuração](postgres-fdw.md#POSTGRES-FDW-CONFIGURATION-PARAMETERS)
* [F.38.10. Exemplos](postgres-fdw.md#POSTGRES-FDW-EXAMPLES)
* [F.38.11. Autor](postgres-fdw.md#POSTGRES-FDW-AUTHOR)

O módulo `postgres_fdw` fornece o wrapper de dados externos `postgres_fdw`, que pode ser usado para acessar dados armazenados em servidores externos PostgreSQL.

A funcionalidade fornecida por este módulo sobrepõe-se substancialmente à funcionalidade do módulo anterior [dblink](dblink.md). Mas o `postgres_fdw` oferece uma sintaxe mais transparente e conforme com os padrões para acessar tabelas remotas e pode oferecer melhor desempenho em muitos casos.

Para se preparar para o acesso remoto usando `postgres_fdw`:

1. Instale a extensão `postgres_fdw` usando [CREATE EXTENSION](sql-createextension.md "CREATE EXTENSION").
2. Crie um objeto de servidor externo, usando [CREATE SERVER](sql-createserver.md "CREATE SERVER"), para representar cada banco de dados remoto que você deseja conectar. Especifique as informações de conexão, exceto `user` e `password`, como opções do objeto do servidor.
3. Crie um mapeamento de usuário, usando [CREATE USER MAPPING](sql-createusermapping.md "CREATE USER MAPPING"), para cada usuário do banco de dados que você deseja permitir acessar cada servidor externo. Especifique o nome do usuário remoto e a senha a serem usados como opções de `user` e `password` do mapeamento de usuário.
4. Crie uma tabela externa, usando [CREATE FOREIGN TABLE](sql-createforeigntable.md "CREATE FOREIGN TABLE") ou [IMPORT FOREIGN SCHEMA](sql-importforeignschema.md "IMPORT FOREIGN SCHEMA"), para cada tabela remota que você deseja acessar. As colunas da tabela externa devem corresponder à tabela remota referenciada. No entanto, você pode usar nomes de tabela e/ou colunas diferentes da tabela remota, se especificar os nomes remotos corretos como opções do objeto da tabela externa.

Agora, você só precisa de `SELECT` de uma tabela estrangeira para acessar os dados armazenados em sua tabela remota subjacente. Você também pode modificar a tabela remota usando `INSERT`, `UPDATE`, `DELETE`, `COPY` ou `TRUNCATE`. (Claro, o usuário remoto que você especificou em sua mapeamento de usuário deve ter privilégios para fazer essas coisas.)

Observe que a opção `ONLY` especificada em `SELECT`, `UPDATE`, `DELETE` ou `TRUNCATE` não tem efeito ao acessar ou modificar a tabela remota.

Observe que o `postgres_fdw` atualmente não oferece suporte para declarações `INSERT` com uma cláusula `ON CONFLICT DO UPDATE`. No entanto, a cláusula `ON CONFLICT DO NOTHING` é suportada, desde que uma especificação de inferência de índice única seja omitida. Observe também que o `postgres_fdw` suporta o movimento de linha invocado por declarações `UPDATE` executadas em tabelas particionadas, mas atualmente não lida com o caso em que uma partição remota escolhida para inserir uma linha movida também é uma partição `UPDATE` alvo que será atualizada em outro lugar no mesmo comando.

Geralmente, é recomendado que as colunas de uma tabela estrangeira sejam declaradas com exatamente os mesmos tipos de dados e, se aplicável, as mesmas colas de ordenação que as colunas referenciadas da tabela remota. Embora o `postgres_fdw` esteja atualmente bastante tolerante em relação à realização de conversões de tipos de dados conforme necessário, podem surgir anomalias semânticas surpreendentes quando os tipos ou colas de ordenação não correspondem, devido ao servidor remoto interpretar as condições da consulta de maneira diferente do servidor local.

Observe que uma tabela estrangeira pode ser declarada com menos colunas ou com uma ordem de coluna diferente do que a tabela remota subjacente. A correspondência das colunas com a tabela remota é por nome, não por posição.

### F.38.1. Opções de FDW do postgres_fdw [#](#POSTGRES-FDW-OPTIONS)

#### F.38.1.1. Opções de conexão [#](#POSTGRES-FDW-OPTIONS-CONNECTION)

Um servidor estrangeiro que utiliza o wrapper de dados estrangeiro `postgres_fdw` pode ter as mesmas opções que a libpq aceita nas configurações de conexão, conforme descrito em [Seção 32.1.2](libpq-connect.md#LIBPQ-PARAMKEYWORDS), exceto que essas opções não são permitidas ou têm tratamento especial:

* `user`, `password` e `sslpassword` (especifique esses em um mapeamento de usuário em vez disso, ou use um arquivo de serviço)
* `client_encoding` (este é definido automaticamente a partir da codificação do servidor local)
* `application_name` - isso pode aparecer em *ou ambos* um mapeamento de conexão e [postgres_fdw.application_name](postgres-fdw.md#GUC-PGFDW-APPLICATION-NAME). Se ambos estiverem presentes, `postgres_fdw.application_name` substitui o ajuste de conexão. Ao contrário do libpq, `postgres_fdw` permite que `application_name` inclua "sequências de escape". Veja [postgres_fdw.application_name](postgres-fdw.md#GUC-PGFDW-APPLICATION-NAME) para detalhes.
* `fallback_application_name` (sempre definido como `postgres_fdw`)
* `sslkey` e `sslcert` - esses podem aparecer em *ou ambos* um mapeamento de conexão e um mapeamento de usuário. Se ambos estiverem presentes, o ajuste do mapeamento de usuário substitui o ajuste de conexão.

Apenas usuários superusuários podem criar ou modificar mapeamentos de usuários com as configurações `sslcert` ou `sslkey`.

Os não superusuários podem se conectar a servidores estrangeiros usando autenticação por senha ou com credenciais delegadas GSSAPI, portanto, especifique a opção `password` para mapeamentos de usuário pertencentes a não superusuários onde a autenticação por senha é necessária.

Um superusuário pode ignorar essa verificação em uma base por mapeamento de usuário, definindo a opção de mapeamento de usuário `password_required 'false'`, por exemplo:

```
ALTER USER MAPPING FOR some_non_superuser SERVER loopback_nopw
OPTIONS (ADD password_required 'false');
```

Para impedir que usuários não privilegiados explorem os direitos de autenticação do usuário Unix que o servidor postgres está executando para escalar para direitos de superusuário, apenas o superusuário pode definir essa opção em um mapeamento de usuário.

É necessário ter cuidado para garantir que isso não permita que o usuário mapeado conecte-se como usuário superutilizador ao banco de dados mapeado, conforme CVE-2007-3278 e CVE-2007-6601. Não defina `password_required=false` no papel `public`. Tenha em mente que o usuário mapeado pode potencialmente usar quaisquer certificados de cliente, `.pgpass`, `.pg_service.conf` etc., no diretório de casa do sistema do usuário do servidor postgres. (Para detalhes sobre como os diretórios de casa são encontrados, consulte [Seção 32.16](libpq-pgpass.md). Eles também podem usar qualquer relação de confiança concedida por modos de autenticação como `peer` ou `ident` autenticação.

#### F.38.1.2. Opções de Nome do Objeto [#](#POSTGRES-FDW-OPTIONS-OBJECT-NAME)

Essas opções podem ser usadas para controlar os nomes utilizados em declarações SQL enviadas ao servidor remoto PostgreSQL. Essas opções são necessárias quando uma tabela externa é criada com nomes diferentes dos nomes da tabela remota subjacente.

`schema_name` (`string`): Esta opção, que pode ser especificada para uma tabela estrangeira, fornece o nome do esquema a ser usado para a tabela estrangeira no servidor remoto. Se esta opção for omitida, o nome do esquema da tabela estrangeira é usado.

`table_name` (`string`): Esta opção, que pode ser especificada para uma tabela estrangeira, fornece o nome da tabela a ser usada para a tabela estrangeira no servidor remoto. Se esta opção for omitida, o nome da tabela estrangeira é usado.

`column_name` (`string`): Esta opção, que pode ser especificada para uma coluna de uma tabela estrangeira, fornece o nome da coluna a ser usada para a coluna no servidor remoto. Se esta opção for omitida, o nome da coluna é usado.

#### F.38.1.3. Opções de Estimativa de Custos [#](#POSTGRES-FDW-OPTIONS-COST-ESTIMATION)

`postgres_fdw` recupera dados remotos executando consultas em servidores remotos, portanto, idealmente, o custo estimado para digitalizar uma tabela estrangeira deve ser o que custa para ser feito no servidor remoto, mais algum custo de overhead para comunicação. A maneira mais confiável de obter tal estimativa é perguntar ao servidor remoto e, em seguida, adicionar algo para overhead — mas para consultas simples, pode não valer o custo de uma consulta remota adicional para obter uma estimativa de custo. Portanto, `postgres_fdw` fornece as seguintes opções para controlar como a estimativa de custo é feita:

`use_remote_estimate` (`boolean`): Esta opção, que pode ser especificada para uma tabela estrangeira ou um servidor estrangeiro, controla se os `postgres_fdw` emite comandos remotos `EXPLAIN` para obter estimativas de custo. Uma configuração para uma tabela estrangeira substitui qualquer configuração para seu servidor, mas apenas para essa tabela. O padrão é `false`.

`fdw_startup_cost` (`floating point`): Esta opção, que pode ser especificada para um servidor estrangeiro, é um valor em ponto flutuante que é adicionado ao custo estimado de inicialização de qualquer varredura de tabela estrangeira nesse servidor. Isso representa o custo adicional de estabelecer uma conexão, analisar e planejar a consulta no lado remoto, etc. O valor padrão é `100`.

`fdw_tuple_cost` (`floating point`): Esta opção, que pode ser especificada para um servidor estrangeiro, é um valor em ponto flutuante que é usado como custo adicional por tupla para varreduras de tabela estrangeira nesse servidor. Isso representa o sobrecarga adicional da transferência de dados entre servidores. Você pode aumentar ou diminuir esse número para refletir um atraso de rede mais alto ou mais baixo para o servidor remoto. O valor padrão é `0.2`.

Quando `use_remote_estimate` é verdadeiro, `postgres_fdw` obtém o número de linhas e as estimativas de custo do servidor remoto e, em seguida, adiciona `fdw_startup_cost` e `fdw_tuple_cost` às estimativas de custo. Quando `use_remote_estimate` é falso, `postgres_fdw` realiza a contagem de linhas e a estimativa de custo local e, em seguida, adiciona `fdw_startup_cost` e `fdw_tuple_cost` às estimativas de custo. Essa estimativa local é improvável que seja muito precisa, a menos que cópias locais das estatísticas da tabela remota estejam disponíveis. Executar [ANALYZE](sql-analyze.md "ANALYZE") na tabela estrangeira é a maneira de atualizar as estatísticas locais; isso realizará uma varredura da tabela remota e, em seguida, calculará e armazenará estatísticas como se a tabela fosse local. Manter estatísticas locais pode ser uma maneira útil de reduzir o overhead de planejamento por consulta para uma tabela remota — mas se a tabela remota for frequentemente atualizada, as estatísticas locais logo se tornarão obsoletas.

A opção a seguir controla como uma operação do tipo `ANALYZE` se comporta:

`analyze_sampling` (`string`): Esta opção, que pode ser especificada para uma tabela estrangeira ou um servidor estrangeiro, determina se `ANALYZE` em uma tabela estrangeira amostra os dados do lado remoto, ou lê e transfere todos os dados e realiza a amostragem localmente. Os valores suportados são `off`, `random`, `system`, `bernoulli` e `auto`. `off` desativa a amostragem remota, de modo que todos os dados são transferidos e amostrados localmente. `random` realiza a amostragem remota usando a função `random()` para escolher as linhas devolvidas, enquanto `system` e `bernoulli` dependem dos métodos internos `TABLESAMPLE` desses nomes. `random` funciona em todas as versões de servidor remoto, enquanto `TABLESAMPLE` é suportado apenas a partir do 9.5. `auto` (o padrão) escolhe o método de amostragem recomendado automaticamente; atualmente, isso significa `bernoulli` ou `random`, dependendo da versão do servidor remoto.

#### F.38.1.4. Opções de execução remota [#](#POSTGRES-FDW-OPTIONS-REMOTE-EXECUTION)

Por padrão, apenas as cláusulas `WHERE` que utilizam operadores e funções embutidos serão consideradas para execução no servidor remoto. As cláusulas que envolvem funções não embutidas são verificadas localmente após a obtenção das linhas. Se tais funções estiverem disponíveis no servidor remoto e puderem ser confiáveis para produzir os mesmos resultados que produzem localmente, o desempenho pode ser melhorado enviando tais cláusulas `WHERE` para execução remota. Esse comportamento pode ser controlado usando a seguinte opção:

`extensions` (`string`): Esta opção é uma lista de nomes de extensões do PostgreSQL que estão instaladas, em versões compatíveis, tanto nos servidores locais quanto remotos. As funções e operadores que são imutáveis e pertencem a uma extensão listada serão considerados para envio para o servidor remoto. Esta opção só pode ser especificada para servidores externos, não por tabela.

Ao usar a opção `extensions`, *é responsabilidade do usuário* que as extensões listadas existam e se comportem da mesma maneira nos servidores locais e remotos. Caso contrário, as consultas remotas podem falhar ou se comportar de forma inesperada.

`fetch_size` (`integer`): Esta opção especifica o número de linhas que a tabela `postgres_fdw` deve obter em cada operação de busca. Pode ser especificado para uma tabela estrangeira ou um servidor estrangeiro. A opção especificada em uma tabela substitui uma opção especificada para o servidor. O padrão é `100`.

`batch_size` (`integer`): Esta opção especifica o número de linhas que o `postgres_fdw` deve inserir em cada operação de inserção. Pode ser especificado para uma tabela estrangeira ou um servidor estrangeiro. A opção especificada em uma tabela substitui uma opção especificada para o servidor. O padrão é `1`.

Observe que o número real de inserções `postgres_fdw` das linhas depende do número de colunas e do valor fornecido `batch_size`. O lote é executado como uma única consulta, e o protocolo libpq (que `postgres_fdw` usa para se conectar a um servidor remoto) limita o número de parâmetros em uma única consulta a 65535. Quando o número de colunas * `batch_size` excede o limite, o `batch_size` será ajustado para evitar um erro.

Essa opção também se aplica ao copiar em tabelas estrangeiras. Nesse caso, o número real de cópias da linha `postgres_fdw` é determinado de maneira semelhante ao caso de inserção, mas é limitado a no máximo 1000 devido às restrições de implementação do comando `COPY`.

#### F.38.1.5. Opções de execução assíncrona [#](#POSTGRES-FDW-OPTIONS-ASYNCHRONOUS-EXECUTION)

`postgres_fdw` suporta a execução assíncrona, que executa várias partes de um nó `Append` de forma concorrente, em vez de serial, para melhorar o desempenho. Essa execução pode ser controlada usando a seguinte opção:

`async_capable` (`boolean`): Esta opção controla se `postgres_fdw` permite que tabelas estrangeiras sejam verificadas simultaneamente para execução assíncrona. Pode ser especificada para uma tabela estrangeira ou um servidor estrangeiro. Uma opção de nível de tabela substitui uma opção de nível de servidor. O padrão é `false`.

Para garantir que os dados retornados de um servidor estrangeiro sejam consistentes, o `postgres_fdw` abrirá apenas uma conexão para um servidor estrangeiro específico e executará todas as consultas nesse servidor sequencialmente, mesmo que haja várias tabelas estrangeiras envolvidas, a menos que essas tabelas sejam sujeitas a diferentes mapeamentos de usuário. Nesse caso, pode ser mais eficiente desabilitar essa opção para eliminar o custo associado à execução de consultas de forma assíncrona.

A execução assíncrona é aplicada mesmo quando um nó `Append` contém subplano(s) executado(s) de forma síncrona, bem como subplano(s) executado(s) de forma assíncrona. Nesse caso, se os subplanos assíncronos forem processados usando `postgres_fdw`, os tuplos dos subplanos assíncronos não serão retornados até que pelo menos um subplano síncrono retorne todos os tuplos, pois esse subplano é executado enquanto os subplanos assíncronos estão aguardando os resultados de consultas assíncronas enviadas para servidores externos. Esse comportamento pode mudar em uma versão futura.

#### F.38.1.6. Opções de Gestão de Transações [#](#POSTGRES-FDW-OPTIONS-TRANSACTION-MANAGEMENT)

Como descrito na seção de Gestão de Transações, nas transações `postgres_fdw`, as transações são gerenciadas criando as transações correspondentes remotamente, e as subtransações são gerenciadas criando as subtransações correspondentes remotamente. Quando várias transações remotamente envolvidas na transação local atual, por padrão, `postgres_fdw` compromete ou abortam essas transações remotamente em série quando a transação local é comprometida ou abortada. Quando várias subtransações remotamente envolvidas na subtransação local atual, por padrão, `postgres_fdw` compromete ou abortam essas subtransações remotamente em série quando a subtransação local é comprometida ou abortada. O desempenho pode ser melhorado com as seguintes opções:

`parallel_commit` (`boolean`): Esta opção controla se `postgres_fdw` realiza, em paralelo, transações remotas abertas em um servidor estrangeiro em uma transação local quando a transação local é realizada. Esta configuração também se aplica a subtransações remotas e locais. Esta opção só pode ser especificada para servidores estrangeiros, não por tabela. O padrão é `false`.

`parallel_abort` (`boolean`): Esta opção controla se `postgres_fdw` interrompe, em paralelo, transações remotas abertas em um servidor estrangeiro em uma transação local quando a transação local é interrompida. Esta configuração também se aplica a subtransações remotas e locais. Esta opção só pode ser especificada para servidores estrangeiros, não por tabela. O padrão é `false`.

Se vários servidores estrangeiros com essas opções ativadas estiverem envolvidos em uma transação local, múltiplas transações remotas nesses servidores estrangeiros são comprometidas ou abortadas em paralelo em todos esses servidores estrangeiros quando a transação local é comprometida ou abortada.

Quando essas opções estão habilitadas, um servidor estrangeiro com muitas transações remotas pode observar um impacto negativo no desempenho quando a transação local é comprometida ou abortada.

#### F.38.1.7. Opções de atualização [#](#POSTGRES-FDW-OPTIONS-UPDATABILITY)

Por padrão, todas as tabelas estrangeiras que utilizam `postgres_fdw` são consideradas atualizáveis. Isso pode ser ignorado usando a opção a seguir:

`updatable` (`boolean`): Esta opção controla se `postgres_fdw` permite que tabelas estrangeiras sejam modificadas usando os comandos `INSERT`, `UPDATE` e `DELETE`. Pode ser especificada para uma tabela estrangeira ou um servidor estrangeiro. Uma opção de nível de tabela substitui uma opção de nível de servidor. O padrão é `true`.

Claro, se a tabela remota não for de fato atualizável, um erro ocorreria de qualquer forma. O uso desta opção permite principalmente que o erro seja lançado localmente sem consultar o servidor remoto. No entanto, observe que as vistas `information_schema` irão relatar que uma tabela estrangeira `postgres_fdw` é atualizável (ou não) de acordo com a configuração desta opção, sem qualquer verificação do servidor remoto.

#### F.38.1.8. Opções de truncatura [#](#POSTGRES-FDW-OPTIONS-TRUNCATABILITY)

Por padrão, todas as tabelas estrangeiras que utilizam `postgres_fdw` são consideradas truncatíveis. Isso pode ser ignorado usando a opção a seguir:

`truncatable` (`boolean`): Esta opção controla se `postgres_fdw` permite que tabelas estrangeiras sejam truncadas usando o comando `TRUNCATE`. Pode ser especificada para uma tabela estrangeira ou um servidor estrangeiro. Uma opção de nível de tabela substitui uma opção de nível de servidor. O padrão é `true`.

Claro, se a tabela remota não for, de fato, truncal, ocorrerá um erro de qualquer forma. O uso desta opção permite, principalmente, que o erro seja lançado localmente sem consultar o servidor remoto.

#### F.38.1.9. Opções de importação [#](#POSTGRES-FDW-OPTIONS-IMPORTING)

`postgres_fdw` é capaz de importar definições de tabela estrangeira usando [IMPORTAR SCHEMA ESTRANGEIRO](sql-importforeignschema.md "IMPORT FOREIGN SCHEMA"). Este comando cria definições de tabela estrangeira no servidor local que correspondem a tabelas ou visualizações presentes no servidor remoto. Se as tabelas remotas a serem importadas tiverem colunas de tipos de dados definidos pelo usuário, o servidor local deve ter tipos compatíveis com os mesmos nomes.

O comportamento de importação pode ser personalizado com as seguintes opções (oferecidas no comando `IMPORT FOREIGN SCHEMA`):

`import_collate` (`boolean`): Esta opção controla se as opções da coluna `COLLATE` são incluídas nas definições de tabelas externas importadas de um servidor externo. O padrão é `true`. Você pode precisar desativá-la se o servidor remoto tiver um conjunto diferente de nomes de collation do que o servidor local, o que provavelmente será o caso se estiver rodando em um sistema operacional diferente. No entanto, se você fizer isso, há um risco muito grave de que as collation das colunas da tabela importada não correspondam aos dados subjacentes, resultando em comportamento de consulta anômalo.

Mesmo quando este parâmetro é definido como `true`, importar colunas cuja correção seja a padrão do servidor remoto pode ser arriscado. Elas serão importadas com `COLLATE "default"`, que selecionará a correção padrão do servidor local, que pode ser diferente.

`import_default` (`boolean`): Esta opção controla se as expressões da coluna `DEFAULT` devem ser incluídas nas definições de tabelas estrangeiras importadas de um servidor remoto. O padrão é `false`. Se você ativar esta opção, esteja atento aos padrões que podem ser calculados de maneira diferente no servidor local do que no servidor remoto; `nextval()` é uma fonte comum de problemas. O `IMPORT` falhará completamente se uma expressão padrão importada usar uma função ou operador que não exista localmente.

`import_generated` (`boolean`): Esta opção controla se as expressões da coluna `GENERATED` são incluídas nas definições de tabelas estrangeiras importadas de um servidor estrangeiro. O padrão é `true`. O `IMPORT` falhará completamente se uma expressão gerada importada usar uma função ou operador que não existe localmente.

`import_not_null` (`boolean`): Esta opção controla se as restrições da coluna `NOT NULL` são incluídas nas definições de tabelas externas importadas de um servidor externo. O padrão é `true`.

Observe que restrições que não sejam `NOT NULL` nunca serão importadas das tabelas remotas. Embora o PostgreSQL suporte restrições de verificação em tabelas externas, não há disposição para importá-las automaticamente, devido ao risco de que uma expressão de restrição possa ser avaliada de maneira diferente nos servidores local e remoto. Qualquer inconsistência desse tipo no comportamento de uma restrição de verificação pode levar a erros difíceis de detectar na otimização de consultas. Portanto, se você deseja importar restrições de verificação, deve fazê-lo manualmente e deve verificar cuidadosamente a semântica de cada uma delas. Para mais detalhes sobre o tratamento de restrições de verificação em tabelas externas, consulte [CREATE FOREIGN TABLE](sql-createforeigntable.md).

Tabelas ou tabelas estrangeiras que são divisões de outras tabelas são importadas apenas quando especificadas explicitamente na cláusula `LIMIT TO`. Caso contrário, elas são automaticamente excluídas de [IMPORTAR SCHEMA ESTRANGEIRO](sql-importforeignschema.md "IMPORT FOREIGN SCHEMA"). Como todos os dados podem ser acessados através da tabela dividida, que é a raiz da hierarquia de divisão, a importação de apenas tabelas divididas deve permitir o acesso a todos os dados sem criar objetos extras.

#### F.38.1.10. Opções de Gerenciamento de Conexão [#](#POSTGRES-FDW-OPTIONS-CONNECTION-MANAGEMENT)

Por padrão, todas as conexões que o `postgres_fdw` estabelece com servidores estrangeiros são mantidas abertas na sessão local para reutilização.

`keep_connections` (`boolean`) [#](#POSTGRES-FDW-OPTION-KEEP-CONNECTIONS): Esta opção controla se o `postgres_fdw` mantém as conexões com o servidor estrangeiro abertas para que consultas subsequentes possam reutilizá-las. Só pode ser especificado para um servidor estrangeiro. O padrão é `on`. Se definido como `off`, todas as conexões com este servidor estrangeiro serão descartadas no final de cada transação.

`use_scram_passthrough` (`boolean`) [#](#POSTGRES-FDW-OPTION-USE-SCRAM-PASSTHROUGH): Esta opção controla se o `postgres_fdw` usará a autenticação de passagem SCRAM para se conectar ao servidor externo. Com a autenticação de passagem SCRAM, o `postgres_fdw` usa segredos criptografados SCRAM em vez de senhas de usuário em texto plano para se conectar ao servidor remoto. Isso evita o armazenamento de senhas de usuário em texto plano nos catálogos do sistema PostgreSQL.

Para usar a autenticação de passagem SCRAM:

* O servidor remoto deve solicitar o método de autenticação `scram-sha-256`; caso contrário, a conexão falhará. * O servidor remoto pode ser de qualquer versão do PostgreSQL que suporte SCRAM. O suporte ao `use_scram_passthrough` é necessário apenas no lado do cliente (lado FDW). * A senha de mapeamento do usuário não é usada. * O servidor que executa `postgres_fdw` e o servidor remoto devem ter segredos SCRAM idênticos (senhas criptografadas) para o usuário que está sendo usado em `postgres_fdw` para autenticação no servidor estrangeiro (mesmo sal e iterações, não apenas a mesma senha).

Como consequência, se as conexões FDW a múltiplos hosts devem ser feitas, por exemplo, para tabelas estrangeiras particionadas ou fragmentação, então todos os hosts devem ter segredos SCRAM idênticos para os usuários envolvidos. * A sessão atual na instância PostgreSQL que faz as conexões FDW saídas também deve usar autenticação SCRAM para sua conexão de cliente de entrada. (Portanto, "pass-through": SCRAM deve ser usado entrando e saindo.) Esse é um requisito técnico do protocolo SCRAM.

### F.38.2. Funções [#](#POSTGRES-FDW-FUNCTIONS)

`postgres_fdw_get_connections( IN check_conn boolean DEFAULT false, OUT server_name text, OUT user_name text, OUT valid boolean, OUT used_in_xact boolean, OUT closed boolean, OUT remote_backend_pid int4) returns setof record`: Esta função retorna informações sobre todas as conexões abertas que o postgres_fdw estabeleceu a partir da sessão local para servidores externos. Se não houver conexões abertas, nenhum registro é retornado.

Se `check_conn` estiver definido como `true`, a função verifica o estado de cada conexão e exibe o resultado na coluna `closed`. Esse recurso atualmente está disponível apenas em sistemas que suportam a extensão não padrão `POLLRDHUP` da chamada de sistema `poll`, incluindo o Linux. Isso é útil para verificar se todas as conexões usadas dentro de uma transação ainda estão abertas. Se alguma conexão for fechada, a transação não pode ser comprometida com sucesso, então é melhor reverter assim que uma conexão fechada for detectada, em vez de continuar até o final. Os usuários podem reverter a transação imediatamente se a função relatar conexões onde tanto `used_in_xact` quanto `closed` estiverem em `true`.

Exemplo de uso da função:

```
postgres=# SELECT * FROM postgres_fdw_get_connections(true); server_name | user_name | valid | used_in_xact | closed | remote_backend_pid -------------+-----------+-------+--------------+----------------------------- loopback1   | postgres  | t     | t            | f      |            1353340 loopback2   | public    | t     | t            | f      |            1353120 loopback3   |           | f     | t            | f      |            1353156
```

As colunas de saída são descritas em [Tabela F.28](postgres-fdw.md#POSTGRES-FDW-GET-CONNECTIONS-COLUMNS).

**Tabela F.28. Colunas de Saída `postgres_fdw_get_connections`**



<table>
 <colgroup>
  <col/>
  <col/>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th>
    Column
   </th>
   <th>
    Type
   </th>
   <th>
    Descrição
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <code>
     server_name
    </code>
   </td>
   <td>
    <code>
     text
    </code>
   </td>
   <td>
    O nome do servidor estrangeiro desta conexão. Se o servidor for descartado, mas a conexão permanecer aberta (ou seja, marcada como inválida), isso será
    <code>
     NULL
    </code>
    .
   </td>
  </tr>
  <tr>
   <td>
    <code>
     user_name
    </code>
   </td>
   <td>
    <code>
     text
    </code>
   </td>
   <td>
    Nome do usuário local mapeado para o servidor estrangeiro desta conexão, ou
    <code>
     public
    </code>
    se uma mapear público for usada. Se a mapear do usuário for descartada, mas a conexão permanecer aberta (ou seja, marcada como inválida), isso será
    <code>
     NULL
    </code>
    .
   </td>
  </tr>
  <tr>
   <td>
    <code>
     valid
    </code>
   </td>
   <td>
    <code>
     boolean
    </code>
   </td>
   <td>
    Falso se essa conexão for inválida, ou seja, ela é usada na transação atual, mas seu mapeamento de servidor ou usuário estrangeiro foi alterado ou excluído. A conexão inválida será fechada no final da transação. Verdadeiro é retornado caso contrário.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     used_in_xact
    </code>
   </td>
   <td>
    <code>
     boolean
    </code>
   </td>
   <td>
    Verdadeiro se essa conexão for usada na transação atual.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     closed
    </code>
   </td>
   <td>
    <code>
     boolean
    </code>
   </td>
   <td>
    Verdadeiro se essa conexão for fechada, falso caso contrário.
    <code>
     NULL
    </code>
    é devolvida se
    <code>
     check_conn
    </code>
    está previsto
    <code>
     false
    </code>
    ou se o controle de status de conexão não estiver disponível nesta plataforma.
   </td>
  </tr>
  <tr>
   <td>
    <code>
     remote_backend_pid
    </code>
   </td>
   <td>
    <code>
     int4
    </code>
   </td>
   <td>
    ID do processo do backend remoto, no servidor estrangeiro, que lida com a conexão. Se o backend remoto for encerrado e a conexão for fechada (com
    <code>
     closed
    </code>
    prontos para
    <code>
     true
    </code>
    ), isso ainda mostra o ID do processo do backend terminado.
   </td>
  </tr>
 </tbody>
</table>







`postgres_fdw_disconnect(server_name text) returns boolean`: Esta função descarta as conexões abertas que são estabelecidas por `postgres_fdw` da sessão local para o servidor estrangeiro com o nome dado. Note que pode haver múltiplas conexões ao servidor dado usando diferentes mapeamentos de usuário. Se as conexões forem usadas na transação local atual, elas não serão desconectadas e mensagens de aviso serão relatadas. Esta função retorna `true` se desconectar pelo menos uma conexão, caso contrário, `false`. Se não for encontrado nenhum servidor estrangeiro com o nome dado, um erro será relatado. Exemplo de uso da função:

```
postgres=# SELECT postgres_fdw_disconnect('loopback1'); postgres_fdw_disconnect ------------------------- t
```

`postgres_fdw_disconnect_all() returns boolean`: Esta função descarta todas as conexões abertas que são estabelecidas por `postgres_fdw` da sessão local para servidores externos. Se as conexões forem usadas na transação local atual, elas não serão desconectadas e mensagens de aviso serão relatadas. Esta função retorna `true` se desconectar pelo menos uma conexão, caso contrário `false`. Exemplo de uso da função:

```
postgres=# SELECT postgres_fdw_disconnect_all(); postgres_fdw_disconnect_all ----------------------------- t
```

### F.38.3. Gerenciamento de Conexão [#](#POSTGRES-FDW-CONNECTION-MANAGEMENT)

`postgres_fdw` estabelece uma conexão com um servidor estrangeiro durante a primeira consulta que utiliza uma tabela estrangeira associada ao servidor estrangeiro. Por padrão, essa conexão é mantida e reutilizada para consultas subsequentes na mesma sessão. Esse comportamento pode ser controlado usando a opção `keep_connections` para um servidor estrangeiro. Se várias identidades de usuário (mapeamentos de usuário) forem usadas para acessar o servidor estrangeiro, uma conexão é estabelecida para cada mapeamento de usuário.

Quando alterar a definição de um servidor estrangeiro ou remover uma mapeia de usuário, as conexões associadas são fechadas. Mas observe que, se houver conexões em uso na transação local atual, elas serão mantidas até o final da transação. As conexões fechadas serão restabelecidas quando forem necessárias por consultas futuras que utilizem uma tabela estrangeira.

Uma vez que uma conexão com um servidor estrangeiro tenha sido estabelecida, ela é mantida por padrão até que a sessão local ou remota correspondente seja encerrada. Para desconectar uma conexão explicitamente, a opção `keep_connections` para um servidor estrangeiro pode ser desativada, ou as funções `postgres_fdw_disconnect` e `postgres_fdw_disconnect_all` podem ser usadas. Por exemplo, essas funções são úteis para fechar conexões que não são mais necessárias, liberando assim as conexões no servidor estrangeiro.

### F.38.4. Gestão de Transações [#](#POSTGRES-FDW-TRANSACTION-MANAGEMENT)

Durante uma consulta que faz referência a quaisquer tabelas remotas em um servidor externo, `postgres_fdw` abre uma transação no servidor remoto, se uma não estiver já aberta correspondente à transação local atual. A transação remota é comprometida ou abortada quando a transação local compromete ou abor de. Os pontos de salvamento são gerenciados de maneira semelhante, criando pontos de salvamento remotos correspondentes.

A transação remota usa o nível de isolamento `SERIALIZABLE` quando a transação local tem o nível de isolamento `SERIALIZABLE`; caso contrário, usa o nível de isolamento `REPEATABLE READ`. Essa escolha garante que, se uma consulta realizar múltiplos varreduras em uma tabela no servidor remoto, ela obterá resultados consistentes com instantâneo para todas as varreduras. Uma consequência é que consultas consecutivas dentro de uma única transação verão os mesmos dados do servidor remoto, mesmo que atualizações concorrentes estejam ocorrendo no servidor remoto devido a outras atividades. Esse comportamento seria esperado de qualquer maneira se a transação local usasse o nível de isolamento `SERIALIZABLE` ou `REPEATABLE READ`, mas pode ser surpreendente para uma transação local `READ COMMITTED`. Uma futura versão do PostgreSQL pode modificar essas regras.

Observe que, atualmente, não é suportado pelo `postgres_fdw` para preparar a transação remota para o commit de duas fases.

### F.38.5. Otimização de consultas remotas [#](#POSTGRES-FDW-REMOTE-QUERY-OPTIMIZATION)

`postgres_fdw` tenta otimizar consultas remotas para reduzir a quantidade de dados transferidos de servidores estrangeiros. Isso é feito enviando cláusulas de consulta `WHERE` ao servidor remoto para execução e não recuperando colunas de tabela que não são necessárias para a consulta atual. Para reduzir o risco de execução incorreta de consultas, as cláusulas de `WHERE` não são enviadas ao servidor remoto, a menos que utilizem apenas tipos de dados, operadores e funções que são embutidos ou pertencem a uma extensão que está listada na opção `extensions` do servidor estrangeiro. Operadores e funções nessas cláusulas também devem ser `IMMUTABLE`. Para uma consulta `UPDATE` ou `DELETE`, `postgres_fdw` tenta otimizar a execução da consulta enviando toda a consulta ao servidor remoto se não houver cláusulas de consulta `WHERE` que não possam ser enviadas ao servidor remoto, sem junções locais para a consulta, sem gatilhos locais de nível de linha `BEFORE` ou `AFTER` ou colunas geradas armazenadas na tabela de destino e sem restrições `CHECK OPTION` de visualizações parentais. Em `UPDATE`, expressões para atribuir às colunas de destino devem usar apenas tipos de dados embutidos, `IMMUTABLE` operadores ou funções `IMMUTABLE`, para reduzir o risco de execução incorreta da consulta.

Quando o `postgres_fdw` encontra uma junção entre tabelas estrangeiras no mesmo servidor estrangeiro, ele envia toda a junção para o servidor estrangeiro, a menos que, por algum motivo, ele acredite que será mais eficiente buscar linhas de cada tabela individualmente, ou a menos que as tabelas referenciadas envolvidas estejam sujeitas a diferentes mapeamentos de usuário. Ao enviar as cláusulas `JOIN`, ele toma as mesmas precauções mencionadas acima para as cláusulas `WHERE`.

A consulta que é realmente enviada ao servidor remoto para execução pode ser examinada usando `EXPLAIN VERBOSE`.

### F.38.6. Ambiente de execução de consultas remotas [#](#POSTGRES-FDW-REMOTE-QUERY-EXECUTION-ENVIRONMENT)

Nas sessões remotas abertas por `postgres_fdw`, o parâmetro [search_path](runtime-config-client.md#GUC-SEARCH-PATH) é definido apenas para `pg_catalog`, para que apenas os objetos embutidos sejam visíveis sem qualificação de esquema. Isso não é um problema para consultas geradas pelo próprio `postgres_fdw`, porque ele sempre fornece tal qualificação. No entanto, isso pode representar um perigo para funções que são executadas no servidor remoto por meio de gatilhos ou regras em tabelas remotas. Por exemplo, se uma tabela remota é realmente uma visão, qualquer função usada nessa visão será executada com o caminho de busca restritivo. Recomenda-se qualificar todos os nomes nessas funções, ou então anexar as opções `SET search_path` (veja [CREATE FUNCTION](sql-createfunction.md "CREATE FUNCTION")) a essas funções para estabelecer seu ambiente de caminho de busca esperado.

`postgres_fdw` estabelece, igualmente, configurações de sessão remota para vários parâmetros:

* [TimeZone](runtime-config-client.md#GUC-TIMEZONE) está definido para `UTC`
* [DateStyle](runtime-config-client.md#GUC-DATESTYLE) está definido para `ISO`
* [IntervalStyle](runtime-config-client.md#GUC-INTERVALSTYLE) está definido para `postgres`
* [extra_float_digits](runtime-config-client.md#GUC-EXTRA-FLOAT-DIGITS) está definido para `3` para servidores remotos 9.0 e versões mais recentes e está definido para `2` para versões mais antigas

Esses são menos propensos a serem problemáticos do que `search_path`, mas podem ser tratados com as opções da função `SET` se necessário.

Não é recomendado que você sobrecarregue esse comportamento ao alterar as configurações de nível de sessão desses parâmetros; isso provavelmente fará com que o `postgres_fdw` funcione mal.

### F.38.7. Compatibilidade entre versões cruzadas [#](#POSTGRES-FDW-CROSS-VERSION-COMPATIBILITY)

`postgres_fdw` pode ser usado com servidores remotos que remontam a `postgres_fdw` pode ser usado com servidores remotos que remontam a PostgreSQL 8.3. A capacidade de leitura somente está disponível a partir de 8.1.

Uma limitação, no entanto, é que `postgres_fdw` geralmente assume que funções e operadores embutidos imutáveis são seguros para serem enviados ao servidor remoto para execução, se eles aparecerem em uma cláusula `WHERE` para uma tabela estrangeira. Assim, uma função embutida que foi adicionada desde o lançamento do servidor remoto pode ser enviada para ele para execução, resultando em “função não existe” ou um erro semelhante. Esse tipo de falha pode ser contornado reescrevendo a consulta, por exemplo, incorporando a referência da tabela estrangeira em um sub-`SELECT` com `OFFSET 0` como uma cerca de otimização, e colocando a função ou operador problemático fora do sub-`SELECT`.

Outra limitação é que, ao executar as instruções `INSERT` com uma cláusula `ON CONFLICT DO NOTHING` em uma tabela estrangeira, o servidor remoto deve estar executando o PostgreSQL 9.5 ou uma versão posterior, pois as versões anteriores não suportam essa funcionalidade.

### F.38.8. Eventos de espera [#](#POSTGRES-FDW-WAIT-EVENTS)

`postgres_fdw` pode relatar os seguintes eventos de espera sob o tipo de evento de espera `Extension`:

`PostgresFdwCleanupResult`: Esperando pelo cancelamento da transação no servidor remoto.

`PostgresFdwConnect`: Esperando estabelecer uma conexão com um servidor remoto.

`PostgresFdwGetResult`  : Esperando receber os resultados de uma consulta de um servidor remoto.

### F.38.9. Parâmetros de configuração [#](#POSTGRES-FDW-CONFIGURATION-PARAMETERS)

`postgres_fdw.application_name` (`string`) [#](#GUC-PGFDW-APPLICATION-NAME): Especifica um valor para o parâmetro de configuração de [application_name](runtime-config-logging.md#GUC-APPLICATION-NAME) usado quando `postgres_fdw` estabelece uma conexão com um servidor externo. Isso substitui a opção `application_name` do objeto do servidor. Observe que a alteração deste parâmetro não afeta quaisquer conexões existentes até que sejam restabelecidas.

`postgres_fdw.application_name` pode ser qualquer string de qualquer comprimento e conter caracteres não ASCII. No entanto, quando é passado e usado como `application_name` em um servidor estrangeiro, observe que ele será truncado para menos de caracteres `NAMEDATALEN`. Qualquer coisa que não seja caracteres ASCII imprimíveis é substituída por escapamentos hexadecimais estilo C (sql-syntax-lexical.md#SQL-SYNTAX-STRINGS-ESCAPE "4.1.2.2. String Constants with C-Style Escapes"). Consulte [application_name](runtime-config-logging.md#GUC-APPLICATION-NAME) para obter detalhes.

`%` caracteres começam com "sequências de escape" que são substituídas por informações de status conforme descrito abaixo. Escape não reconhecido é ignorado. Outros caracteres são copiados diretamente para o nome da aplicação. Note que não é permitido especificar um sinal de mais/menos ou um literal numérico após o `%` e antes da opção, para alinhamento e preenchimento.



<table>
 <thead>
  <tr>
   <th>
    Escape
   </th>
   <th>
    Efeito
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <code>
     %a
    </code>
   </td>
   <td>
    Nome do aplicativo no servidor local
   </td>
  </tr>
  <tr>
   <td>
    <code>
     %c
    </code>
   </td>
   <td>
    ID de sessão no servidor local
    <a class="xref" href="runtime-config-logging.md#GUC-LOG-LINE-PREFIX">
     log_line_prefix
    </a>
    para detalhes)
   </td>
  </tr>
  <tr>
   <td>
    <code>
     %C
    </code>
   </td>
   <td>
    Nome do cluster no servidor local
    <a class="xref" href="runtime-config-logging.md#GUC-CLUSTER-NAME">
     cluster_name
    </a>
    para detalhes)
   </td>
  </tr>
  <tr>
   <td>
    <code>
     %u
    </code>
   </td>
   <td>
    Nome do usuário no servidor local
   </td>
  </tr>
  <tr>
   <td>
    <code>
     %d
    </code>
   </td>
   <td>
    Nome do banco de dados no servidor local
   </td>
  </tr>
  <tr>
   <td>
    <code>
     %p
    </code>
   </td>
   <td>
    ID de processo do backend no servidor local
   </td>
  </tr>
  <tr>
   <td>
    <code>
     %%
    </code>
   </td>
   <td>
    Literalmente %
   </td>
  </tr>
 </tbody>
</table>







Por exemplo, se o usuário `local_user` estabelece uma conexão da base de dados `local_db` para `foreign_db` como o usuário `foreign_user`, o ajuste `'db=%d, user=%u'` é substituído por `'db=local_db, user=local_user'`.

### F.38.10. Exemplos [#](#POSTGRES-FDW-EXAMPLES)

Aqui está um exemplo de criação de uma tabela estrangeira com `postgres_fdw`. Primeiro, instale a extensão:

```
CREATE EXTENSION postgres_fdw;
```

Em seguida, crie um servidor remoto usando [CREATE SERVER](sql-createserver.md). Neste exemplo, desejamos conectar-se a um servidor PostgreSQL no host `192.83.123.89` que está ouvindo na porta `5432`. O banco de dados ao qual a conexão é feita é chamado `foreign_db` no servidor remoto:

```
CREATE SERVER foreign_server FOREIGN DATA WRAPPER postgres_fdw OPTIONS (host '192.83.123.89', port '5432', dbname 'foreign_db');
```

É necessário um mapeamento de usuário, definido com [CREATE USER MAPPING](sql-createusermapping.md), para identificar o papel que será usado no servidor remoto:

```
CREATE USER MAPPING FOR local_user SERVER foreign_server OPTIONS (user 'foreign_user', password 'password');
```

Agora é possível criar uma tabela estrangeira com [CREATE FOREIGN TABLE] (sql-createforeigntable.md "CREATE FOREIGN TABLE"). Neste exemplo, desejamos acessar a tabela denominada `some_schema.some_table` no servidor remoto. O nome local para ela será `foreign_table`:

```
CREATE FOREIGN TABLE foreign_table ( id integer NOT NULL, data text ) SERVER foreign_server OPTIONS (schema_name 'some_schema', table_name 'some_table');
```

É essencial que os tipos de dados e outras propriedades das colunas declaradas em `CREATE FOREIGN TABLE` correspondam à tabela remota real. Os nomes das colunas também devem corresponder, a menos que você adicione as opções `column_name` às colunas individuais para mostrar como elas são nomeadas na tabela remota. Em muitos casos, o uso de [`IMPORT FOREIGN SCHEMA`](sql-importforeignschema.md) é preferível à construção manual de definições de tabela externa.

### F.38.11. Autor [#](#POSTGRES-FDW-AUTHOR)

Shigeru Hanada `<shigeru.hanada@gmail.com>`