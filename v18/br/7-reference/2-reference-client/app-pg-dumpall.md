## pg_dumpall

pg_dumpall — extrair um cluster de banco de dados PostgreSQL em um arquivo de script

## Sinopse

`pg_dumpall` [*`connection-option`*...] [*`option`*...]

## Descrição

O pg_dumpall é um utilitário para escrever todos os bancos de dados do PostgreSQL de um clúster em um arquivo de script. O arquivo de script contém comandos SQL que podem ser usados como entrada para [psql](app-psql.md) para restaurar os bancos de dados. Isso é feito chamando [pg_dump](app-pgdump.md) para cada banco de dados no clúster. O pg_dumpall também grava objetos globais que são comuns a todos os bancos de dados, a saber, papéis de banco, espaços de tabela e concessões de privilégio para parâmetros de configuração. (O pg_dump não salva esses objetos.)

Como o pg_dumpall lê as tabelas de todos os bancos de dados, você provavelmente terá que se conectar como um superusuário do banco de dados para produzir um dump completo. Além disso, você precisará de privilégios de superusuário para executar o script salvo, a fim de poder adicionar funções e criar bancos de dados.

O script SQL será escrito na saída padrão. Use a opção `-f`/`--file` ou operadores de shell para redirecioná-lo para um arquivo.

O pg_dumpall precisa se conectar várias vezes ao servidor PostgreSQL (uma vez por banco de dados). Se você usar autenticação por senha, ele solicitará uma senha a cada vez. É conveniente ter um arquivo `~/.pgpass` nesses casos. Consulte [Seção 32.16](libpq-pgpass.md) para obter mais informações.

### Aviso

Restaurar um dump faz com que o destino execute código arbitrário da escolha dos superusuários da fonte. Dumps parciais e restaurações parciais não limitam isso. Se os superusuários da fonte não forem confiáveis, as declarações SQL descarregadas devem ser inspecionadas antes da restauração. Note que o cliente que executa o dump e a restauração não precisa confiar nos superusuários da fonte ou do destino.

## Opções

As opções de linha de comando a seguir controlam o conteúdo e o formato do resultado.

`-a` `--data-only`: Exclua apenas os dados, não o esquema (definições de dados) ou estatísticas.

`-c` `--clean`: Emitir comandos SQL para `DROP` todas as bases de dados, papéis e espaços de tabela descarregados antes de as recriar. Esta opção é útil quando o restabelecimento for sobrepor um cluster existente. Se algum dos objetos não existir no cluster de destino, mensagens de erro ignoráveis serão relatadas durante o restabelecimento, a menos que `--if-exists` também seja especificado.

`-E encoding` `--encoding=encoding`: Crie o dump no conjunto de caracteres de codificação especificado. Por padrão, o dump é criado no conjunto de caracteres da base de dados. (Outra maneira de obter o mesmo resultado é definir a variável de ambiente `PGCLIENTENCODING` para o conjunto de caracteres de codificação desejado.)

`-f filename` `--file=filename`: Envie a saída para o arquivo especificado. Se isso for omitido, a saída padrão é usada.

`-g` `--globals-only`: Exclua apenas objetos globais (roles e espaços de tabela), não bancos de dados.

`-O` `--no-owner`: Não emita comandos para definir a propriedade dos objetos de acordo com o banco de dados original. Por padrão, o pg_dumpall emite as declarações `ALTER OWNER` ou `SET SESSION AUTHORIZATION` para definir a propriedade dos elementos do esquema criados. Essas declarações falharão quando o script for executado, a menos que seja iniciado por um superusuário (ou pelo mesmo usuário que possui todos os objetos do script). Para criar um script que possa ser restaurado por qualquer usuário, mas que dê a esse usuário a propriedade de todos os objetos, especifique `-O`.

`-r` `--roles-only`: Exporte apenas os papéis, sem bancos de dados ou espaços de tabela.

`-s` `--schema-only`: Descarte apenas as definições do objeto (esquema), não os dados.

`-S username` `--superuser=username`: Especifique o nome do usuário superusuário a ser usado ao desabilitar gatilhos. Isso é relevante apenas se `--disable-triggers` for usado. (Normalmente, é melhor deixar isso de fora e, em vez disso, iniciar o script resultante como superusuário.)

`-t` `--tablespaces-only`: Exclua apenas os espaços de tabela, sem bancos de dados ou papéis.

`-v` `--verbose`: Especifica o modo verbose. Isso fará com que o pg_dumpall exiba os horários de início/parada no arquivo de dump e mensagens de progresso no erro padrão. A repetição da opção fará com que mensagens adicionais de nível de depuração apareçam no erro padrão. A opção também é passada para o pg_dump.

`-V` `--version`: Imprimir a versão do pg_dumpall e sair.

`-x` `--no-privileges` `--no-acl`: Prevenir o descarte de privilégios de acesso (comandos de concessão/rejeição).

`--binary-upgrade`: Esta opção é para uso em utilitários de atualização in-place. Seu uso para outros propósitos não é recomendado ou suportado. O comportamento da opção pode mudar em versões futuras sem aviso prévio.

`--column-inserts` `--attribute-inserts`: Arraste dados como comandos `INSERT` com nomes explícitos de colunas (`INSERT INTO table (column, ...) VALUES ...`). Isso tornará a restauração muito lenta; é principalmente útil para fazer backups que podem ser carregados em bancos de dados que não são do PostgreSQL.

`--disable-dollar-quoting`: Esta opção desativa o uso de citação de dólares para corpos de função e obriga-os a serem citados usando a sintaxe de string padrão do SQL.

`--disable-triggers`: Esta opção é relevante apenas ao criar um dump com dados e sem esquema. Instrui o pg_dumpall a incluir comandos para desabilitar temporariamente os gatilhos nas tabelas de destino enquanto os dados são restaurados. Use isso se você tiver verificações de integridade referencial ou outros gatilhos nas tabelas que você não deseja invocar durante a restauração dos dados.

Atualmente, os comandos emitidos para `--disable-triggers` devem ser feitos como superusuário. Portanto, você também deve especificar um nome de superusuário com `-S`, ou, de preferência, ter cuidado para iniciar o script resultante como um superusuário.

`--exclude-database=pattern`: Não descarte bancos de dados cujo nome corresponda a *`pattern`*. Múltiplos padrões podem ser excluídos escrevendo múltiplos interruptores `--exclude-database`. O parâmetro *`pattern` é interpretado como um padrão de acordo com as mesmas regras usadas pelos comandos `\d` do psql (ver [Padrões](app-psql.md#APP-PSQL-PATTERNS "Patterns")), então múltiplos bancos de dados também podem ser excluídos escrevendo caracteres curinga no padrão. Ao usar caracteres curinga, tenha cuidado em citar o padrão, se necessário, para evitar a expansão de caracteres curinga do shell.

`--extra-float-digits=ndigits`: Use o valor especificado de extra_float_digits ao descartar dados de ponto flutuante, em vez da precisão máxima disponível. Os descargas de rotina feitas para fins de backup não devem usar essa opção.

`--filter=filename`: Especifique um nome de arquivo a partir do qual ler padrões para bancos de dados excluídos do dump. Os padrões são interpretados de acordo com as mesmas regras que `--exclude-database`. Para ler a partir de `STDIN`, use `-` como o nome de arquivo. A opção `--filter` pode ser especificada em conjunto com `--exclude-database` para excluir bancos de dados, e também pode ser especificada mais de uma vez para vários arquivos de filtro.

O arquivo lista um padrão de banco de dados por linha, com o seguinte formato:

```
exclude database PATTERN
```

As linhas que começam com `#` são consideradas comentários e ignoradas. Comentários também podem ser colocados após uma linha de padrão de objeto. Linhas em branco também são ignoradas. Veja [Padrões](app-psql.md#APP-PSQL-PATTERNS) para saber como realizar citação em padrões.

`--if-exists`: Use os comandos `DROP ... IF EXISTS` para descartar objetos no modo `--clean`. Isso suprime os erros de "não existe" que, de outra forma, poderiam ser relatados. Esta opção não é válida, a menos que `--clean` também seja especificado.

`--inserts`: Armazene os dados como comandos `INSERT` (em vez de `COPY`). Isso tornará a restauração muito lenta; é principalmente útil para fazer backups que podem ser carregados em bancos de dados que não são do PostgreSQL. Observe que a restauração pode falhar completamente se você tiver reorganizado a ordem dos colunários. A opção `--column-inserts` é mais segura, embora ainda mais lenta.

`--load-via-partition-root`: Ao descartar dados de uma partição de tabela, faça as declarações `COPY` ou `INSERT` direcionarem-se à raiz da hierarquia de partição que a contém, em vez da própria partição. Isso faz com que a partição apropriada seja redefinida para cada linha quando os dados são carregados. Isso pode ser útil ao restaurar dados em um servidor onde as linhas nem sempre caem nas mesmas partições que faziam no servidor original. Isso pode acontecer, por exemplo, se a coluna de partição for do tipo texto e os dois sistemas tiverem definições diferentes da collation usada para ordenar a coluna de partição.

`--lock-wait-timeout=timeout`: Não espere para sempre adquirir bloqueios de tabela compartilhada no início do dump. Em vez disso, falhe se não conseguir bloquear uma tabela dentro do especificado *`timeout`*. O tempo de espera pode ser especificado em qualquer um dos formatos aceitos por `SET statement_timeout`.

`--no-comments`: Não descarte comandos `COMMENT`.

`--no-data`: Não descarte dados.

`--no-policies`: Não descarte as políticas de segurança de linha.

`--no-publications`: Não descarte publicações.

`--no-role-passwords`: Não descarte senhas para papéis. Quando restaurado, os papéis terão uma senha nula, e a autenticação por senha falhará sempre até que a senha seja definida. Como os valores da senha não são necessários quando esta opção é especificada, as informações do papel são lidas a partir da visualização do catálogo `pg_roles` em vez de `pg_authid`. Portanto, esta opção também ajuda se o acesso a `pg_authid` for restrito por alguma política de segurança.

`--no-schema`: Não descarte o esquema (definições de dados).

`--no-security-labels`: Não descarte etiquetas de segurança.

`--no-statistics`: Não descarte estatísticas. Este é o padrão.

`--no-subscriptions`: Não descarte assinaturas.

`--no-sync`: Por padrão, o `pg_dumpall` aguarda que todos os arquivos sejam escritos com segurança no disco. Esta opção faz com que o `pg_dumpall` retorne sem aguardar, o que é mais rápido, mas significa que um posterior travamento do sistema operacional pode deixar o dump corrompido. Geralmente, esta opção é útil para testes, mas não deve ser usada ao fazer o dumping de dados de uma instalação em produção.

`--no-table-access-method`: Não exiba comandos para selecionar métodos de acesso à tabela. Com esta opção, todos os objetos serão criados com o método de acesso à tabela que é o padrão durante o restabelecimento.

`--no-tablespaces`: Não execute comandos para criar tablespaces nem selecione tablespaces para objetos. Com esta opção, todos os objetos serão criados no tablespace padrão durante o restabelecimento.

`--no-toast-compression`: Não exiba comandos para definir métodos de compressão TOAST. Com esta opção, todas as colunas serão restauradas com o ajuste de compressão padrão.

`--no-unlogged-table-data`: Não descarte o conteúdo de tabelas não registradas. Esta opção não afeta se as definições de tabela (esquema) são descarregadas ou não; ela apenas suprime o descarregamento dos dados da tabela.

`--on-conflict-do-nothing`: Adicione os comandos `ON CONFLICT DO NOTHING` a `INSERT`. Esta opção não é válida a menos que `--inserts` ou `--column-inserts` também seja especificado.

`--quote-all-identifiers`: Forçar a citação de todos os identificadores. Esta opção é recomendada quando se está a descarregar um banco de dados de um servidor cuja versão principal do PostgreSQL é diferente da do pg_dumpall, ou quando a saída está destinada a ser carregada num servidor de uma versão principal diferente. Por predefinição, o pg_dumpall cita apenas os identificadores que são palavras reservadas na sua própria versão principal. Isso, por vezes, resulta em problemas de compatibilidade ao lidar com servidores de outras versões que podem ter conjuntos ligeiramente diferentes de palavras reservadas. Usar `--quote-all-identifiers` previne tais problemas, ao preço de um script de descarregamento mais difícil de ler.

`--restrict-key=restrict_key`: Use a string fornecida como a chave `\restrict` do psql na saída do dump. Se nenhuma chave restrita for especificada, o pg_dumpall gerará uma chave aleatória conforme necessário. As chaves podem conter apenas caracteres alfanuméricos.

Esta opção é destinada principalmente a fins de teste e outros cenários que exigem saída repetida (por exemplo, comparar arquivos de depuração). Não é recomendada para uso geral, pois um servidor malicioso com conhecimento avançado da chave pode ser capaz de injetar código arbitrário que será executado na máquina que executa o psql com a saída de depuração.

`--rows-per-insert=nrows`: Arraste dados como comandos `INSERT` (em vez de `COPY`). Controla o número máximo de linhas por comando `INSERT`. O valor especificado deve ser um número maior que zero. Qualquer erro durante a restauração fará com que apenas as linhas que fazem parte do `INSERT` problemático sejam perdidas, em vez do conteúdo completo da tabela.

`--statistics`: Otimizador de dados de descarte.

`--statistics-only`: Exclua apenas as estatísticas, não o esquema (definições de dados) ou os dados. As estatísticas do otimizador para tabelas, visualizações materializadas, tabelas externas e índices são excluídas.

`--sequence-data`: Inclua dados de sequência no dump. Este é o comportamento padrão, exceto quando são especificados `--no-data`, `--schema-only` ou `--statistics-only`.

`--use-set-session-authorization`: Em vez de comandos padrão SQL `SET SESSION AUTHORIZATION`, execute comandos `ALTER OWNER` para determinar a propriedade dos objetos. Isso torna o dump mais compatível com os padrões, mas, dependendo do histórico dos objetos no dump, pode não ser restaurado corretamente.

`-?` `--help`: Mostrar ajuda sobre os argumentos da linha de comando do comando pg_dumpall e sair.

As opções de linha de comando a seguir controlam os parâmetros de conexão do banco de dados.

`-d connstr` `--dbname=connstr`: Especifica os parâmetros usados para se conectar ao servidor, como uma [string de conexão](libpq-connect.md#LIBPQ-CONNSTRING "32.1.1. Connection Strings"); esses parâmetros substituirão quaisquer opções de linha de comando conflitantes.

A opção é chamada `--dbname` para garantir a consistência com outras aplicações do cliente, mas, como o pg_dumpall precisa se conectar a muitas bases de dados, o nome da base de dados na string de conexão será ignorado. Use a opção `-l` para especificar o nome da base de dados usada para a conexão inicial, que irá descartar objetos globais e descobrir quais outras bases de dados devem ser descartadas.

`-h host` `--host=host`: Especifica o nome do host da máquina na qual o servidor de banco de dados está sendo executado. Se o valor começar com uma barra, ele é usado como o diretório para o socket de domínio Unix. O padrão é tomado da variável de ambiente `PGHOST`, se definida, caso contrário, uma conexão de socket de domínio Unix é tentada.

`-l dbname` `--database=dbname`: Especifica o nome do banco de dados a ser conectado para drenar objetos globais e descobrir quais outros bancos de dados devem ser drenados. Se não for especificado, o banco de dados `postgres` será usado, e se este não existir, `template1` será usado.

`-p port` `--port=port`: Especifica a porta TCP ou a extensão de arquivo de soquete de domínio Unix local em que o servidor está ouvindo conexões. Tem como padrão a variável de ambiente `PGPORT`, se definida, ou um padrão incorporado.

`-U username` `--username=username`: Nome do usuário para se conectar como.

`-w` `--no-password`: Nunca emita um prompt de senha. Se o servidor exigir autenticação por senha e uma senha não estiver disponível por outros meios, como um arquivo `.pgpass`, a tentativa de conexão falhará. Esta opção pode ser útil em trabalhos em lote e scripts onde nenhum usuário está presente para inserir uma senha.

`-W` `--password`: Forçar o pg_dumpall a solicitar uma senha antes de se conectar a um banco de dados.

Essa opção nunca é essencial, pois o pg_dumpall solicitará automaticamente uma senha se o servidor exigir autenticação por senha. No entanto, o pg_dumpall desperdiçará uma tentativa de conexão descobrindo que o servidor deseja uma senha. Em alguns casos, vale a pena digitar `-W` para evitar a tentativa extra de conexão.

Observe que o prompt de senha ocorrerá novamente para cada banco de dados que será descarregado. Geralmente, é melhor configurar um arquivo `~/.pgpass` do que confiar na entrada manual da senha.

`--role=rolename`: Especifica um nome de papel a ser usado para criar o dump. Esta opção faz com que o pg_dumpall emita um comando `SET ROLE` *`rolename`* após se conectar ao banco de dados. É útil quando o usuário autenticado (especificado por `-U`) não possui privilégios necessários pelo pg_dumpall, mas pode alternar para um papel com os direitos necessários. Algumas instalações têm uma política contra a autenticação direta como superusuário, e o uso desta opção permite que os dumps sejam feitos sem violar a política.

## Meio Ambiente

`PGHOST` `PGOPTIONS` `PGPORT` `PGUSER`: Parâmetros de conexão padrão

`PG_COLOR`: Especifica se a cor deve ser usada nas mensagens de diagnóstico. Os valores possíveis são `always`, `auto` e `never`.

Esse utilitário, como a maioria dos outros utilitários do PostgreSQL, também utiliza as variáveis de ambiente suportadas pelo libpq (consulte a [Seção 32.15](libpq-envars.md)).

## Notas

Como o pg_dumpall chama o pg_dump internamente, algumas mensagens de diagnóstico se referirão ao pg_dump.

A opção `--clean` pode ser útil mesmo quando a sua intenção é restaurar o script de implantação em um novo clúster. O uso de `--clean` autoriza o script a descartar e recriar os bancos de dados internos `postgres` e `template1`, garantindo que esses bancos de dados manterão as mesmas propriedades (por exemplo, idioma e codificação) que tinham no clúster de origem. Sem a opção, esses bancos de dados manterão suas propriedades de nível de banco de dados existentes, bem como qualquer conteúdo pré-existente.

Quando `--statistics` é especificado, `pg_dumpall` incluirá a maioria das estatísticas do otimizador no arquivo de dump resultante. Isso não inclui todas as estatísticas, como as criadas explicitamente com [CREATE STATISTICS](sql-createstatistics.md "CREATE STATISTICS"), estatísticas personalizadas adicionadas por uma extensão ou estatísticas coletadas pelo sistema de estatísticas cumulativas. Portanto, ainda pode ser útil executar `ANALYZE` em cada banco de dados após a restauração de um arquivo de dump para garantir um desempenho ótimo. Você também pode executar `vacuumdb -a -z` para analisar todos os bancos de dados.

Não se espera que o script de implantação seja executado completamente sem erros. Em particular, porque o script emitirá `CREATE ROLE` para cada papel existente no clúster de origem, é certo que receberá um erro de “papel já existe” para o superusuário de bootstrap, a menos que o clúster de destino tenha sido inicializado com um nome de superusuário de bootstrap diferente. Esse erro é inofensivo e deve ser ignorado. O uso da opção `--clean` provavelmente produzirá mensagens de erro adicionais inofensivas sobre objetos não existentes, embora você possa minimizar esses erros adicionando `--if-exists`.

O pg_dumpall exige que todos os diretórios do espaço de tabela necessários existam antes do restabelecimento; caso contrário, a criação do banco de dados falhará para bancos em locais que não são padrão.

Geralmente, é recomendado usar a opção `-X` (`--no-psqlrc`) ao restaurar um banco de dados a partir de um script pg_dumpall para garantir um processo de restauração limpo e evitar potenciais conflitos com configurações de psql não padrão. Além disso, como o script pg_dumpall pode incluir meta-comandos do psql, ele pode ser incompatível com clientes que não são o psql.

## Exemplos

Para descartar todos os bancos de dados:

```
$ pg_dumpall > db.out
```

Para restaurar o(s) banco(s) de dados a partir deste arquivo, você pode usar:

```
$ psql -X -f db.out -d postgres
```

Não é importante qual banco de dados você se conecta aqui, uma vez que o arquivo de script criado pelo pg_dumpall conterá os comandos apropriados para criar e se conectar aos bancos de dados salvos. Uma exceção é que, se você especificou `--clean`, você deve se conectar ao banco de dados `postgres` inicialmente; o script tentará descartar outros bancos de dados imediatamente, e isso falhará para o banco de dados ao qual você está conectado.

## Veja também

Consulte [pg_dump](app-pgdump.md) para obter detalhes sobre as possíveis condições de erro.