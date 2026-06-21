## pg_dump

pg_dump — exporta um banco de dados PostgreSQL como um script SQL ou em outros formatos

## Sinopse

`pg_dump` [*`connection-option`*...] [*`option`*...] [*`dbname`*]

## Descrição

pg_dump é uma ferramenta para exportar um banco de dados PostgreSQL. Faz exportações consistentes mesmo se o banco de dados estiver sendo usado simultaneamente. O pg_dump não bloqueia outros usuários que estão acessando o banco de dados (leitores ou escritores). No entanto, observe que, exceto em casos simples, o pg_dump geralmente não é a escolha certa para fazer backups regulares de bancos de produção. Consulte [Capítulo 25][(backup.md "Chapter 25. Backup and Restore")] para uma discussão adicional.

O pg_dump só exibe um único banco de dados. Para exportar um conjunto inteiro ou para exportar objetos globais que são comuns a todos os bancos de dados em um conjunto (como papéis e espaços de tabela), use [pg_dumpall][(app-pg-dumpall.md "pg_dumpall")].

Os backups podem ser exportados em formatos de arquivo ou de script. Os backups de script são arquivos de texto simples que contêm os comandos SQL necessários para reconstruir o banco de dados ao estado em que estava no momento em que foi salvo. Para restaurar a partir de um desses scripts, alimente-o em [psql][(app-psql.md "psql")]. Os arquivos de script podem ser usados para reconstruir o banco de dados mesmo em outras máquinas e em outras arquiteturas; com algumas modificações, até mesmo em outros produtos de banco de dados SQL.

Os formatos de arquivo de arquivo alternativo devem ser usados com [pg_restore][(app-pgrestore.md "pg_restore")] para reconstruir o banco de dados. Eles permitem que o pg_restore seja seletivo sobre o que é restaurado, ou até mesmo reordenar os itens antes de serem restaurados. Os formatos de arquivo de arquivo são projetados para ser portáveis em várias arquiteturas.

Quando usado com um dos formatos de arquivo de arquivo e combinado com o pg_restore, o pg_dump fornece um mecanismo flexível de arquivamento e transferência. O pg_dump pode ser usado para exportar um banco de dados inteiro, então o pg_restore pode ser usado para examinar o arquivo e/ou selecionar quais partes do banco de dados devem ser restauradas. Os formatos de arquivo de saída mais flexíveis são o formato “custom” (`-Fc`) e o formato “directory” (`-Fd`). Eles permitem a seleção e a reordenação de todos os itens arquivados, suportam a restauração paralela e são comprimidos por padrão. O formato “directory” é o único formato que suporta gravações paralelas.

Ao executar o pg_dump, é importante examinar a saída em busca de quaisquer avisos (impressos na saída padrão), especialmente à luz das limitações listadas abaixo.

### Aviso

Restaurar um dump faz com que o destino execute código arbitrário da escolha dos superusuários da fonte. Dumps parciais e restaurações parciais não limitam isso. Se os superusuários da fonte não forem confiáveis, as declarações SQL descartadas devem ser inspecionadas antes da restauração. Dumps que não são em texto plano podem ser inspecionados usando a opção `--file` do pg_restore. Note que o cliente que executa o dump e a restauração não precisa confiar nos superusuários da fonte ou do destino.

## Opções

As opções de linha de comando a seguir controlam o conteúdo e o formato do resultado.

*`dbname`*: Especifica o nome do banco de dados a ser descarregado. Se isso não for especificado, a variável de ambiente `PGDATABASE` é usada. Se isso não for definido, o nome de usuário especificado para a conexão é usado.

`-a` `--data-only`: Exclua apenas os dados, não o esquema (definições de dados) ou estatísticas. Os dados da tabela, objetos grandes e valores de sequência são excluídos.

Esta opção é semelhante, mas por razões históricas, não é idêntica à especificação `--section=data`.

`-b` `--large-objects` `--blobs` (desatualizado): Inclua objetos grandes no dump. Este é o comportamento padrão, exceto quando `--schema`, `--table`, `--schema-only`, `--statistics-only` ou `--no-data` é especificado. O interruptor `-b` é, portanto, útil apenas para adicionar objetos grandes aos dumps onde um esquema ou tabela específica foi solicitado. Note que objetos grandes são considerados dados e, portanto, serão incluídos quando `--data-only` é usado, mas não quando `--schema-only` ou `--statistics-only` é.

`-B` `--no-large-objects` `--no-blobs` (desatualizado): Exclua objetos grandes no dump.

Quando ambos os `-b` e `-B` são fornecidos, o comportamento é emitir objetos grandes, quando os dados estão sendo descarregados, veja a documentação do `-b`.

`-c` `--clean`: Emita comandos para `DROP` todos os objetos do banco de dados descarregados antes de emitir os comandos para criá-los. Esta opção é útil quando o restabelecimento deve sobrescrever um banco de dados existente. Se algum dos objetos não existir no banco de dados de destino, mensagens de erro ignoráveis serão relatadas durante o restabelecimento, a menos que `--if-exists` também seja especificado.

Essa opção é ignorada ao emitir um arquivo de saída de arquivo (não textual). Para os formatos de arquivo, você pode especificar a opção ao chamar `pg_restore`.

`-C` `--create`: Comece a saída com um comando para criar o próprio banco de dados e reconectar-se ao banco de dados criado. (Com um script dessa forma, não importa com qual banco de dados na instalação de destino você se conectar antes de executar o script.) Se `--clean` também for especificado, o script exclui e recria o banco de dados de destino antes de se reconectar a ele.

Com `--create`, a saída também inclui o comentário do banco de dados, se houver, e quaisquer configurações de variáveis específicas para este banco de dados, ou seja, quaisquer comandos `ALTER DATABASE ... SET ...` e `ALTER ROLE ... IN DATABASE ... SET ...` que mencionem este banco de dados. Os privilégios de acesso para o próprio banco de dados também são descarregados, a menos que `--no-acl` seja especificado.

Essa opção é ignorada ao emitir um arquivo de saída de arquivo (não textual). Para os formatos de arquivo, você pode especificar a opção ao chamar `pg_restore`.

`-e pattern` `--extension=pattern`: Exclua apenas as extensões que correspondem a *`pattern`*. Quando esta opção não é especificada, todas as extensões não-sistemáticas no banco de dados de destino serão excluídas. Múltiplas extensões podem ser selecionadas escrevendo vários `-e` switches. O parâmetro *`pattern`* é interpretado como um padrão de acordo com as mesmas regras usadas pelos comandos `\d` do psql (ver [Padrões][(app-psql.md#APP-PSQL-PATTERNS "Patterns")]), então múltiplas extensões também podem ser selecionadas escrevendo caracteres curinga no padrão. Ao usar caracteres curinga, tenha cuidado em citar o padrão, se necessário, para evitar que o shell expanda os caracteres curinga.

Qualquer relação de configuração registrada por `pg_extension_config_dump` é incluída no dump se sua extensão for especificada por `--extension`.

### Nota

Quando `-e` é especificado, o pg_dump não faz qualquer tentativa de drenar quaisquer outros objetos de banco de dados que a(s) extensão(ões) selecionada(s) possa(m) depender. Portanto, não há garantia de que os resultados de um dump de extensão específica possam ser restaurados com sucesso em um banco de dados limpo.

`-E encoding` `--encoding=encoding`: Crie o dump no conjunto de caracteres de codificação especificado. Por padrão, o dump é criado no conjunto de caracteres do banco de dados. (Outra maneira de obter o mesmo resultado é definir a variável de ambiente `PGCLIENTENCODING` para o conjunto de caracteres de dump desejado.) Os conjuntos de caracteres suportados são descritos em [Seção 23.3.1](multibyte.md#MULTIBYTE-CHARSET-SUPPORTED "23.3.1. Supported Character Sets").

`-f file` `--file=file`: Envie a saída para o arquivo especificado. Este parâmetro pode ser omitido para formatos de saída baseados em arquivos, no qual caso, a saída padrão é usada. No entanto, deve ser fornecido para o formato de saída de diretório, onde especifica o diretório de destino em vez de um arquivo. Neste caso, o diretório é criado por `pg_dump` e não deve existir antes.

`-F format` `--format=format`: Seleciona o formato do resultado. *`format`* pode ser um dos seguintes:

`p` `plain` :   Exiba um arquivo de script SQL em texto simples (o padrão).

`c` `custom` :   Emita um arquivo de formato personalizado adequado para entrada no pg_restore. Juntamente com o formato de saída de diretório, este é o formato de saída mais flexível, pois permite a seleção e reordenação manual dos itens arquivados durante a restauração. Este formato também é comprimido por padrão.

`d` `directory` :   Emita um arquivo em formato de diretório adequado para entrada no pg_restore. Isso criará um diretório com um arquivo para cada tabela e objeto grande sendo descartado, além de um chamado arquivo de Índice que descreve os objetos descartados em um formato legível por máquina que o pg_restore pode ler. Um arquivo em formato de diretório pode ser manipulado com ferramentas padrão Unix; por exemplo, os arquivos em um arquivo descompactado podem ser compactados com as ferramentas gzip, lz4 ou zstd. Este formato é comprimido por padrão usando `gzip` e também suporta descargas paralelas.

`t` `tar` :   Emita um arquivo no formato `tar` adequado para entrada no pg_restore. O formato tar é compatível com o formato de diretório: a extração de um arquivo no formato tar produz um arquivo com o formato de diretório válido. No entanto, o formato tar não suporta compressão. Além disso, ao usar o formato tar, o ordem relativa dos itens de dados da tabela não pode ser alterada durante o restabelecimento.

`-j njobs` `--jobs=njobs`: Execute o dump em paralelo, descarregando as tabelas *`njobs`* simultaneamente. Esta opção pode reduzir o tempo necessário para realizar o dump, mas também aumenta a carga no servidor do banco de dados. Você só pode usar esta opção com o formato de saída de diretório, porque este é o único formato de saída onde vários processos podem escrever seus dados ao mesmo tempo.

O pg_dump abrirá *`njobs`* + 1 conexões ao banco de dados, então certifique-se de que sua configuração [max_connections][(runtime-config-connection.md#GUC-MAX-CONNECTIONS)] é alta o suficiente para acomodar todas as conexões.

Solicitar bloqueios exclusivos em objetos de banco de dados enquanto realiza um dump paralelo pode fazer com que o dump falhe. A razão é que o processo líder do pg_dump solicita blocos compartilhados ([ACCESS SHARE][(explicit-locking.md#LOCKING-TABLES "13.3.1. Table-Level Locks")]) nos objetos que os processos de trabalho vão drenar mais tarde, a fim de garantir que ninguém os exclua e os faça desaparecer enquanto o dump está sendo executado. Se outro cliente, em seguida, solicitar um bloqueio exclusivo em uma tabela, esse bloqueio não será concedido, mas será enfileirado esperando que o bloqueio compartilhado do processo líder seja liberado. Consequentemente, qualquer outro acesso à tabela também não será concedido e será enfileirado após a solicitação do bloqueio exclusivo. Isso inclui o processo de trabalho tentando drenar a tabela. Sem quaisquer precauções, isso seria uma situação clássica de deadlock. Para detectar esse conflito, o processo de trabalho do pg_dump solicita outro bloqueio compartilhado usando a opção `NOWAIT`. Se o processo de trabalho não receber esse bloqueio compartilhado, alguém mais deve ter solicitado um bloqueio exclusivo nesse meio tempo e não há como continuar com o dump, então o pg_dump não tem escolha a não ser abortar o dump.

Para realizar um dump paralelo, o servidor de banco de dados precisa suportar instantâneos sincronizados, uma característica que foi introduzida no PostgreSQL 9.2 para servidores primários e 10 para standby. Com essa característica, os clientes do banco de dados podem garantir que vejam o mesmo conjunto de dados, mesmo que usem conexões diferentes. O `pg_dump -j` usa múltiplas conexões de banco de dados; ele se conecta ao banco de dados uma vez com o processo líder e novamente para cada trabalho do trabalhador. Sem a característica de instantâneo sincronizado, os diferentes trabalhos do trabalhador não seriam garantidos para ver os mesmos dados em cada conexão, o que poderia levar a uma cópia inconsistente.

`-n pattern` `--schema=pattern`: Exclua apenas os esquemas que correspondem a *`pattern`*; isso seleciona tanto o próprio esquema quanto todos os objetos contidos nele. Quando esta opção não é especificada, todos os esquemas não-sistemáticos no banco de dados de destino serão excluídos. Múltiplos esquemas podem ser selecionados escrevendo vários `-n` switches. O parâmetro *`pattern`* é interpretado como um padrão de acordo com as mesmas regras usadas pelos comandos `\d` do psql (veja [Padrões](app-psql.md#APP-PSQL-PATTERNS "Patterns")), então múltiplos esquemas também podem ser selecionados escrevendo caracteres curinga no padrão. Ao usar caracteres curinga, tenha cuidado em citar o padrão, se necessário, para evitar que o shell expanda os caracteres curinga; veja [Exemplos](app-pgdump.md#PG-DUMP-EXAMPLES "Examples") abaixo.

### Nota

Quando o `-n` é especificado, o pg_dump não faz qualquer tentativa de drenar quaisquer outros objetos de banco de dados que os esquemas selecionados possam depender. Portanto, não há garantia de que os resultados de um dump de esquema específico possam ser restaurados com sucesso em um banco de dados limpo.

### Nota

Objetos não esquemáticos, como objetos grandes, não são descarregados quando o `-n` é especificado. Você pode adicionar objetos grandes de volta ao descarregamento com o interruptor `--large-objects`.

`-N pattern` `--exclude-schema=pattern`: Não descarte nenhum esquema que corresponda a *`pattern`. O padrão é interpretado de acordo com as mesmas regras que para `-n`. `-N` pode ser dado mais de uma vez para excluir esquemas que correspondam a qualquer um dos vários padrões.

Quando ambos os `-n` e `-N` são fornecidos, o comportamento é descartar apenas os esquemas que correspondem a pelo menos um interruptor `-n`, mas nenhum interruptor `-N`. Se `-N` aparece sem `-n`, então os esquemas que correspondem a `-N` são excluídos do que, de outra forma, seria um descarte normal.

`-O` `--no-owner`: Não emita comandos para definir a propriedade dos objetos de acordo com o banco de dados original. Por padrão, o pg_dump emite as declarações `ALTER OWNER` ou `SET SESSION AUTHORIZATION` para definir a propriedade dos objetos de banco de dados criados. Essas declarações falharão quando o script for executado, a menos que seja iniciado por um superusuário (ou pelo mesmo usuário que possui todos os objetos do script). Para criar um script que possa ser restaurado por qualquer usuário, mas que dê a esse usuário a propriedade de todos os objetos, especifique `-O`.

Essa opção é ignorada ao emitir um arquivo de saída de arquivo (não textual). Para os formatos de arquivo, você pode especificar a opção ao chamar `pg_restore`.

`-R` `--no-reconnect`: Esta opção é obsoleta, mas ainda é aceita para compatibilidade reversa.

`-s` `--schema-only`: Exclua apenas as definições do objeto (esquema), não os dados ou estatísticas.

Esta opção não pode ser usada com `--data-only` ou `--statistics-only`. É semelhante, mas por razões históricas, não é idêntica à especificação de `--section=pre-data --section=post-data`.

(Não confunda isso com a opção `--schema`, que usa a palavra “esquema” em um significado diferente.)

Para excluir dados de tabela apenas para um subconjunto de tabelas no banco de dados, consulte `--exclude-table-data`.

`-S username` `--superuser=username`: Especifique o nome do usuário de superusuário a ser usado ao desabilitar gatilhos. Isso é relevante apenas se `--disable-triggers` for usado. (Normalmente, é melhor deixar isso de fora e, em vez disso, iniciar o script resultante como superusuário.)

`-t pattern` `--table=pattern`: Exclua apenas as tabelas com nomes que correspondem a *`pattern`*. Múltiplas tabelas podem ser selecionadas escrevendo vários `-t` switches. O parâmetro *`pattern`* é interpretado como um padrão de acordo com as mesmas regras usadas pelos comandos `\d` do psql (veja [Padrões][(app-psql.md#APP-PSQL-PATTERNS "Patterns")]), então múltiplas tabelas também podem ser selecionadas escrevendo caracteres curinga no padrão. Ao usar caracteres curinga, tenha cuidado em citar o padrão, se necessário, para evitar que o shell expanda os caracteres curinga; veja [Exemplos][(app-pgdump.md#PG-DUMP-EXAMPLES "Examples")] abaixo.

Além das tabelas, essa opção pode ser usada para descartar a definição de vistas correspondentes, vistas materializadas, tabelas externas e sequências. Não descartará o conteúdo das vistas ou das vistas materializadas, e o conteúdo das tabelas externas será descartado apenas se o servidor externo correspondente for especificado com `--include-foreign-data`.

Os interruptores `-n` e `-N` não têm efeito quando o `-t` é usado, porque as tabelas selecionadas por `-t` serão descarregadas independentemente desses interruptores, e os objetos que não são tabelas não serão descarregados.

### Nota

Quando `-t` é especificado, o pg_dump não faz qualquer tentativa de drenar quaisquer outros objetos de banco de dados que as tabelas selecionadas possam depender. Portanto, não há garantia de que os resultados de um dump de uma tabela específica possam ser restaurados com sucesso em um banco de dados limpo.

`-T pattern` `--exclude-table=pattern`: Não descarte nenhuma tabela que corresponda a *`pattern`. O padrão é interpretado de acordo com as mesmas regras que para `-t`. `-T` pode ser dado mais de uma vez para excluir tabelas que correspondam a qualquer um dos vários padrões.

Quando ambos os `-t` e `-T` são fornecidos, o comportamento é descartar apenas as tabelas que correspondem a pelo menos um `-t` switch, mas nenhum `-T` switch. Se `-T` aparece sem `-t`, então as tabelas que correspondem a `-T` são excluídas do que, de outra forma, seria um dump normal.

`-v` `--verbose`: Especifica o modo verbose. Isso fará com que o pg_dump emita comentários detalhados sobre os objetos e os horários de início/parada no arquivo de dump, além de mensagens de progresso no erro padrão. A repetição da opção fará com que mensagens adicionais de nível de depuração apareçam no erro padrão.

`-V` `--version`: Imprimir a versão do pg_dump e sair.

`-x` `--no-privileges` `--no-acl`: Prevenir o descarte de privilégios de acesso (comandos de concessão/rejeição).

`-Z level` `-Z method`[:*`detail`*] `--compress=level` `--compress=method`[:*`detail`*]: Especifique o método de compressão e/ou o nível de compressão a ser utilizado. O método de compressão pode ser definido como `gzip`, `lz4`, `zstd` ou `none` para sem compressão. Uma string de detalhes de compressão pode ser especificada opcionalmente. Se a string de detalhes for um número inteiro, ela especifica o nível de compressão. Caso contrário, deve ser uma lista de itens separados por vírgula, cada um na forma `keyword` ou `keyword=value`. Atualmente, as palavras-chave suportadas são `level` e `long`.

Se nenhum nível de compressão for especificado, o nível de compressão padrão será utilizado. Se apenas um nível for especificado sem mencionar um algoritmo, a compressão `gzip` será utilizada se o nível for maior que `0`, e não será utilizada compressão se o nível for `0`.

Para os formatos de arquivo de diretório e de arquivo personalizado, isso especifica a compressão de segmentos de dados individuais da tabela, e o padrão é comprimir usando `gzip` em um nível moderado. Para saída de texto simples, definir um nível de compressão não nulo faz com que todo o arquivo de saída seja comprimido, como se tivesse sido alimentado através de gzip, lz4 ou zstd; mas o padrão não é comprimir. Com a compressão zstd, o modo `long` pode melhorar a taxa de compressão, às custas do uso de memória aumentado.

O formato de arquivo tar atualmente não suporta compressão de forma alguma.

`--binary-upgrade`: Esta opção é para uso em utilitários de atualização in-place. Seu uso para outros propósitos não é recomendado ou suportado. O comportamento da opção pode mudar em versões futuras sem aviso prévio.

`--column-inserts` `--attribute-inserts`: Arraste dados como comandos `INSERT` com nomes explícitos de colunas (`INSERT INTO table (column, ...) VALUES ...`). Isso tornará a restauração muito lenta; é principalmente útil para fazer backups que podem ser carregados em bancos de dados que não são do PostgreSQL. Qualquer erro durante a restauração causará a perda apenas das linhas que fazem parte do problema `INSERT`, e não do conteúdo completo da tabela.

`--disable-dollar-quoting`: Esta opção desativa o uso de citação de dólares para corpos de função e obriga-os a serem citados usando a sintaxe de string padrão do SQL.

`--disable-triggers`: Esta opção é relevante apenas ao criar um dump que inclui dados, mas não inclui esquema. Instrui o pg_dump a incluir comandos para desabilitar temporariamente os gatilhos nas tabelas de destino enquanto os dados são restaurados. Use isso se você tiver verificações de integridade referencial ou outros gatilhos nas tabelas que você não deseja invocar durante a restauração dos dados.

Atualmente, os comandos emitidos para `--disable-triggers` devem ser feitos como superusuário. Portanto, você também deve especificar um nome de superusuário com `-S`, ou, de preferência, ter cuidado para iniciar o script resultante como um superusuário.

Essa opção é ignorada ao emitir um arquivo de saída de arquivo (não textual). Para os formatos de arquivo, você pode especificar a opção ao chamar `pg_restore`.

`--enable-row-security`: Esta opção é relevante apenas quando descarregando o conteúdo de uma tabela que tem segurança de linha. Por padrão, o pg_dump definirá [row_security](runtime-config-client.md#GUC-ROW-SECURITY) como desligado, para garantir que todos os dados sejam descarregados da tabela. Se o usuário não tiver privilégios suficientes para contornar a segurança de linha, então um erro é lançado. Este parâmetro instrui o pg_dump a definir [row_security](runtime-config-client.md#GUC-ROW-SECURITY) como ligado, permitindo que o usuário descarregue as partes do conteúdo da tabela nas quais ele tem acesso.

Observe que, se você estiver usando essa opção atualmente, provavelmente também deseja que o dump esteja no formato `INSERT`, pois o `COPY FROM` durante o restabelecimento não suporta segurança de linha.

`--exclude-extension=pattern`: Não descarte quaisquer extensões que correspondam a *`pattern`*. O padrão é interpretado de acordo com as mesmas regras que para `-e`. `--exclude-extension` pode ser dado mais de uma vez para excluir extensões que correspondam a qualquer um dos vários padrões.

Quando ambos os `-e` e `--exclude-extension` são fornecidos, o comportamento é descartar apenas as extensões que correspondem a pelo menos uma chave `-e`, mas nenhuma chave `--exclude-extension`. Se `--exclude-extension` aparece sem `-e`, então as extensões que correspondem a `--exclude-extension` são excluídas do que, de outra forma, seria um dump normal.

`--exclude-table-and-children=pattern`: Isso é o mesmo que a opção `-T`/`--exclude-table`, exceto que também exclui quaisquer partições ou tabelas filhas de herança da(s) tabela(s) que correspondem ao *`pattern`*.

`--exclude-table-data=pattern`: Não descarte dados para quaisquer tabelas que correspondam a *`pattern`*. O padrão é interpretado de acordo com as mesmas regras que para `-t`. `--exclude-table-data` pode ser dado mais de uma vez para excluir tabelas que correspondam a vários padrões. Esta opção é útil quando você precisa da definição de uma tabela específica, mesmo que não precise dos dados nela.

Para excluir dados de todas as tabelas no banco de dados, consulte `--schema-only` ou `--statistics-only`.

`--exclude-table-data-and-children=pattern`: Isso é o mesmo que a opção `--exclude-table-data`, exceto que também exclui dados de quaisquer partições ou tabelas filhas de herança da(s) tabela(s) que correspondem ao *`pattern`*.

`--extra-float-digits=ndigits`: Use o valor especificado de `extra_float_digits` ao descartar dados de ponto flutuante, em vez da máxima precisão disponível. Os descargas de rotina feitas para fins de backup não devem usar essa opção.

`--filter=filename`: Especifique um nome de arquivo a partir do qual ler padrões para objetos a serem incluídos ou excluídos do dump. Os padrões são interpretados de acordo com as mesmas regras que as opções correspondentes: `-t`/`--table`, `--table-and-children`, `-T`/`--exclude-table` e `--exclude-table-and-children` para tabelas, `-n`/`--schema` e `-N`/`--exclude-schema` para esquemas, `--include-foreign-data` para dados em servidores externos, `--exclude-table-data` e `--exclude-table-data-and-children` para dados de tabela, e `-e`/`--extension` e `--exclude-extension` para extensões. Para ler a partir de `STDIN`, use `-` como o nome de arquivo. A opção `--filter` pode ser especificada em conjunto com as opções listadas acima para incluir ou excluir objetos, e também pode ser especificada mais de uma vez para múltiplos arquivos de filtro.

O arquivo lista um padrão de objeto por linha, com o seguinte formato:

``` { include | exclude } { extension | foreign_data | table | table_and_children | table_data | table_data_and_children | schema } PATTERN
    ```

A primeira palavra-chave especifica se os objetos que correspondem ao padrão devem ser incluídos ou excluídos. A segunda palavra-chave especifica o tipo de objeto que deve ser filtrado usando o padrão:

* `extension`: extensões. Funciona como a opção `-e`/`--extension` ou `--exclude-extension`.
    * `foreign_data`: dados em servidores externos. Funciona como a opção `--include-foreign-data`. Este termo só pode ser usado com o termo `include`.
    * `table`: tabelas. Funciona como a opção `-t`/`--table` ou `-T`/`--exclude-table`.
    * `table_and_children`: tabelas, incluindo quaisquer partições ou tabelas filhas de herança. Funciona como a opção `--table-and-children` ou `--exclude-table-and-children`.
    * `table_data`: dados de tabela de quaisquer tabelas que correspondam a *`pattern`*. Funciona como a opção `--exclude-table-data`. Este termo só pode ser usado com o termo `exclude`.
    * `table_data_and_children`: dados de tabela de quaisquer tabelas que correspondam a *`pattern`* bem como quaisquer partições ou filhos de herança da(s) tabela(s). Funciona como a opção `--exclude-table-data-and-children`. Este termo só pode ser usado com o termo `exclude`.
    * `schema`: esquemas. Funciona como a opção `-n`/`--schema` ou `-N`/`--exclude-schema`.

As linhas que começam com `#` são consideradas comentários e ignoradas. Comentários também podem ser colocados após uma linha de padrão de objeto. Linhas em branco também são ignoradas. Veja [Padrões](app-psql.md#APP-PSQL-PATTERNS "Patterns") para saber como realizar citação em padrões.

Os arquivos de exemplo estão listados abaixo na seção [Exemplos][(app-pgdump.md#PG-DUMP-EXAMPLES "Examples")].

`--if-exists`: Use os comandos `DROP ... IF EXISTS` para descartar objetos no modo `--clean`. Isso suprime os erros de "não existe" que, de outra forma, poderiam ser relatados. Esta opção não é válida, a menos que `--clean` também seja especificado.

`--include-foreign-data=foreignserver`: Armazene os dados de qualquer tabela estrangeira com um servidor estrangeiro que corresponda ao padrão *`foreignserver`*. Múltiplos servidores estrangeiros podem ser selecionados escrevendo vários interruptores `--include-foreign-data`. Além disso, o parâmetro *`foreignserver`* é interpretado como um padrão de acordo com as mesmas regras usadas pelos comandos `\d` do psql (ver [Padrões][(app-psql.md#APP-PSQL-PATTERNS "Patterns")]), então múltiplos servidores estrangeiros também podem ser selecionados escrevendo caracteres curinga no padrão. Ao usar caracteres curinga, tenha cuidado em citar o padrão, se necessário, para evitar que o shell expanda os caracteres curinga; veja [Exemplos][(app-pgdump.md#PG-DUMP-EXAMPLES "Examples")] abaixo. A única exceção é que um padrão vazio é proibido.

### Nota

O uso de caracteres especiais em `--include-foreign-data` pode resultar em acesso a servidores estrangeiros inesperados. Além disso, para usar essa opção com segurança, certifique-se de que o servidor nomeado deve ter um proprietário de confiança.

### Nota

Quando `--include-foreign-data` é especificado, o pg_dump não verifica se a tabela externa é legível. Portanto, não há garantia de que os resultados de um dump de tabela externa possam ser restaurados com sucesso.

`--inserts`: Armazene os dados como comandos `INSERT` (em vez de `COPY`). Isso tornará a restauração muito lenta; é principalmente útil para fazer backups que podem ser carregados em bancos de dados que não são do PostgreSQL. Qualquer erro durante a restauração fará com que apenas as linhas que fazem parte do `INSERT` problemático sejam perdidas, em vez do conteúdo completo da tabela. Note que a restauração pode falhar completamente se você tiver reorganizado a ordem dos colunários. A opção `--column-inserts` é segura contra mudanças na ordem dos colunários, embora seja ainda mais lenta.

`--load-via-partition-root`: Ao descartar dados de uma partição de tabela, faça as declarações `COPY` ou `INSERT` direcionarem-se à raiz da hierarquia de partição que a contém, em vez da própria partição. Isso faz com que a partição apropriada seja redefinida para cada linha quando os dados são carregados. Isso pode ser útil ao restaurar dados em um servidor onde as linhas nem sempre caem nas mesmas partições que faziam no servidor original. Isso pode acontecer, por exemplo, se a coluna de partição for do tipo texto e os dois sistemas tenham definições diferentes da collation usada para ordenar a coluna de partição.

`--lock-wait-timeout=timeout`: Não espere para sempre adquirir bloqueios de tabela compartilhada no início do dump. Em vez disso, falhe se não conseguir bloquear uma tabela dentro do especificado *`timeout`*. O tempo de espera pode ser especificado em qualquer um dos formatos aceitos por `SET statement_timeout`. (Os formatos permitidos variam dependendo da versão do servidor da qual está fazendo o dump, mas um número inteiro de milissegundos é aceito por todas as versões.)

`--no-comments`: Não descarte comandos `COMMENT`.

`--no-data`: Não descarte dados.

`--no-policies`: Não descarte políticas de segurança de linha.

`--no-publications`: Não descarte publicações.

`--no-schema`: Não descarte o esquema (definições de dados).

`--no-security-labels`: Não descarte etiquetas de segurança.

`--no-statistics`: Não descarte estatísticas. Este é o padrão.

`--no-subscriptions`: Não descarte assinaturas.

`--no-sync`: Por padrão, `pg_dump` aguardará que todos os arquivos sejam escritos com segurança no disco. Esta opção faz com que `pg_dump` retorne sem aguardar, o que é mais rápido, mas significa que um posterior falha do sistema operacional pode deixar o dump corrompido. Geralmente, esta opção é útil para testes, mas não deve ser usada ao fazer o dumping de dados de uma instalação de produção.

`--no-table-access-method`: Não exiba comandos para selecionar métodos de acesso à tabela. Com esta opção, todos os objetos serão criados com o método de acesso à tabela que é o padrão durante a restauração.

Essa opção é ignorada ao emitir um arquivo de saída de arquivo (não textual). Para os formatos de arquivo, você pode especificar a opção ao chamar `pg_restore`.

`--no-tablespaces`: Não execute comandos para selecionar tablespaces. Com esta opção, todos os objetos serão criados no tablespace padrão durante o restabelecimento.

Essa opção é ignorada ao emitir um arquivo de saída de arquivo (não textual). Para os formatos de arquivo, você pode especificar a opção ao chamar `pg_restore`.

`--no-toast-compression`: Não exiba comandos para definir métodos de compressão TOAST. Com esta opção, todas as colunas serão restauradas com o ajuste de compressão padrão.

`--no-unlogged-table-data`: Não descarte o conteúdo de tabelas e sequências não registradas. Esta opção não afeta se as definições de tabela e sequência (esquema) são descarregadas ou não; ela apenas suprime o descarregamento dos dados da tabela e da sequência. Os dados em tabelas e sequências não registradas são sempre excluídos ao descarregar de um servidor de espera.

`--on-conflict-do-nothing`: Adicione os comandos `ON CONFLICT DO NOTHING` a `INSERT`. Esta opção não é válida a menos que `--inserts`, `--column-inserts` ou `--rows-per-insert` também seja especificado.

`--quote-all-identifiers`: Forçar a citação de todos os identificadores. Esta opção é recomendada quando se está a descarregar um banco de dados de um servidor cuja versão principal do PostgreSQL é diferente da do pg_dump, ou quando a saída está destinada a ser carregada num servidor de uma versão principal diferente. Por predefinição, o pg_dump cita apenas os identificadores que são palavras reservadas na sua própria versão principal. Isso, por vezes, resulta em problemas de compatibilidade ao lidar com servidores de outras versões que podem ter conjuntos de palavras reservadas ligeiramente diferentes. Usar `--quote-all-identifiers` previne tais problemas, ao preço de um script de descarregamento mais difícil de ler.

`--restrict-key=restrict_key`: Use a string fornecida como a chave `\restrict` no psql na saída do dump. Isso só pode ser especificado para dumps de texto plano, ou seja, quando `--format` está definido como `plain` ou a opção `--format` é omitida. Se nenhuma chave de restrição for especificada, o pg_dump gerará uma aleatória conforme necessário. As chaves podem conter apenas caracteres alfanuméricos.

Esta opção é destinada principalmente a fins de teste e outros cenários que exigem saída repetida (por exemplo, comparar arquivos de depuração). Não é recomendada para uso geral, pois um servidor malicioso com conhecimento avançado da chave pode ser capaz de injetar código arbitrário que será executado na máquina que executa o psql com a saída de depuração.

`--rows-per-insert=nrows`: Arraste dados como comandos `INSERT` (em vez de `COPY`). Controla o número máximo de linhas por comando `INSERT`. O valor especificado deve ser um número maior que zero. Qualquer erro durante a restauração fará com que apenas as linhas que fazem parte do `INSERT` problemático sejam perdidas, em vez do conteúdo completo da tabela.

`--section=sectionname`: Apenas descarregue a seção nomeada. O nome da seção pode ser `pre-data`, `data` ou `post-data`. Esta opção pode ser especificada mais de uma vez para selecionar várias seções. O padrão é descarregar todas as seções.

A seção de dados contém dados reais da tabela, conteúdos de objetos grandes, valores de sequência e estatísticas para tabelas, visualizações materializadas e tabelas externas. Os itens pós-dados incluem definições de índices, gatilhos, regras, estatísticas para índices e restrições que não são restrições de verificação validadas e não nulos. Os itens pré-dados incluem todos os outros itens de definição de dados.

`--sequence-data`: Inclua dados de sequência no dump. Este é o comportamento padrão, exceto quando são especificados `--no-data`, `--schema-only` ou `--statistics-only`.

`--serializable-deferrable`: Use uma transação `serializable` para o dump, para garantir que o instantâneo utilizado esteja consistente com os estados posteriores do banco de dados; mas faça isso esperando por um ponto no fluxo de transação em que não possam estar presentes anomalias, para que não haja risco de o dump falhar ou causar o retorno de outras transações com um `serialization_failure`. Consulte o [Capítulo 13][(mvcc.md "Chapter 13. Concurrency Control")] para obter mais informações sobre isolamento de transações e controle de concorrência.

Esta opção não é benéfica para um dump que é destinado apenas para recuperação em caso de desastre. Poderia ser útil para um dump usado para carregar uma cópia do banco de dados para relatórios ou outro compartilhamento de carga apenas de leitura, enquanto o banco de dados original continua sendo atualizado. Sem ela, o dump pode refletir um estado que não é consistente com qualquer execução serial das transações eventualmente comprometidas. Por exemplo, se técnicas de processamento em lote forem usadas, um lote pode ser mostrado como fechado no dump sem que todos os itens que estão no lote apareçam.

Essa opção não fará diferença se não houver transações de leitura e escrita ativas quando o pg_dump for iniciado. Se as transações de leitura e escrita estiverem ativas, o início do dump pode ser adiado por um período indeterminado de tempo. Uma vez em execução, o desempenho com ou sem a chave é o mesmo.

`--snapshot=snapshotname`: Use o instantâneo sincronizado especificado ao fazer um dump do banco de dados (consulte [Tabela 9.100][(functions-admin.md#FUNCTIONS-SNAPSHOT-SYNCHRONIZATION-TABLE "Table 9.100. Snapshot Synchronization Functions")] para mais detalhes).

Essa opção é útil quando é necessário sincronizar o dump com um intervalo de replicação lógica (consulte [Capítulo 47][(logicaldecoding.md "Chapter 47. Logical Decoding")]) ou com uma sessão concorrente.

No caso de uma varredura paralela, o nome do instantâneo definido por esta opção é usado em vez de criar um novo instantâneo.

`--statistics`: Otimizador de dados de descarte.

`--statistics-only`: Descarte apenas as estatísticas, não o esquema (definições de dados) ou os dados. As estatísticas do otimizador para tabelas, visualizações materializadas, tabelas externas e índices são descartadas.

`--strict-names`: Exija que cada extensão (`-e`/`--extension`), esquema (`-n`/`--schema`) e tabela (`-t`/`--table`) correspondam a pelo menos uma extensão/esquema/tabela no banco de dados a ser exportado. Isso também se aplica aos filtros usados com `--filter`. Observe que, se nenhuma das extensões/esquema/tabela encontrar correspondências, o pg_dump gerará um erro mesmo sem `--strict-names`.

Esta opção não afeta `--exclude-extension`, `-N`/`--exclude-schema`, `-T`/`--exclude-table` ou `--exclude-table-data`. Um padrão de exclusão que não consegue corresponder a nenhum objeto não é considerado um erro.

`--sync-method=method`: Quando configurado para `fsync`, que é o padrão, `pg_dump --format=directory` abrirá e sincronizará recursivamente todos os arquivos no diretório do arquivo.

Em Linux, `syncfs` pode ser usado para pedir ao sistema operacional que sincronize todo o sistema de arquivos que contém o diretório do arquivo. Consulte [recovery_init_sync_method][(runtime-config-error-handling.md#GUC-RECOVERY-INIT-SYNC-METHOD)] para obter informações sobre as advertências a serem observadas ao usar `syncfs`.

Esta opção não tem efeito quando o `--no-sync` é usado ou quando o `--format` não está definido como `directory`.

`--table-and-children=pattern`: Isso é o mesmo que a opção `-t`/`--table`, exceto que também inclui quaisquer partições ou tabelas de herança das tabelas que correspondem ao *`pattern`*.

`--use-set-session-authorization`: Edite os comandos padrão SQL `SET SESSION AUTHORIZATION` em vez dos comandos `ALTER OWNER` para determinar a propriedade dos objetos. Isso torna o dump mais compatível com os padrões, mas, dependendo do histórico dos objetos no dump, pode não ser restaurado corretamente. Além disso, um dump usando `SET SESSION AUTHORIZATION` certamente exigirá privilégios de superusuário para ser restaurado corretamente, enquanto `ALTER OWNER` requer privilégios menores.

`-?` `--help`: Mostrar ajuda sobre os argumentos da linha de comando do comando pg_dump e sair.

As opções de linha de comando a seguir controlam os parâmetros de conexão do banco de dados.

`-d dbname` `--dbname=dbname`: Especifica o nome do banco de dados a ser conectado. Isso é equivalente a especificar *`dbname`* como o primeiro argumento não opcional na linha de comando. O *`dbname`* pode ser uma [string de conexão](libpq-connect.md#LIBPQ-CONNSTRING "32.1.1. Connection Strings"). Se assim for, os parâmetros da string de conexão substituirão quaisquer opções de linha de comando conflitantes.

`-h host` `--host=host`: Especifica o nome do host da máquina na qual o servidor está sendo executado. Se o valor começar com uma barra, ele é usado como o diretório para o socket de domínio Unix. O padrão é tomado da variável de ambiente `PGHOST`, se definida, caso contrário, uma conexão de socket de domínio Unix é tentada.

`-p port` `--port=port`: Especifica a porta TCP ou a extensão de arquivo de soquete de domínio Unix local em que o servidor está ouvindo conexões. Tem como padrão a variável de ambiente `PGPORT`, se definida, ou um padrão incorporado.

`-U username` `--username=username`: Nome do usuário para se conectar como.

`-w` `--no-password`: Nunca emita um prompt de senha. Se o servidor exigir autenticação por senha e uma senha não estiver disponível por outros meios, como um arquivo `.pgpass`, a tentativa de conexão falhará. Esta opção pode ser útil em trabalhos em lote e scripts onde nenhum usuário está presente para inserir uma senha.

`-W` `--password`: Forçar o pg_dump a solicitar uma senha antes de se conectar a um banco de dados.

Essa opção nunca é essencial, pois o pg_dump solicitará automaticamente uma senha se o servidor exigir autenticação por senha. No entanto, o pg_dump desperdiçará uma tentativa de conexão descobrindo que o servidor deseja uma senha. Em alguns casos, vale a pena digitar `-W` para evitar a tentativa extra de conexão.

`--role=rolename`: Especifica um nome de papel a ser usado para criar o dump. Esta opção faz com que o pg_dump emita um comando `SET ROLE` *`rolename`* após se conectar ao banco de dados. É útil quando o usuário autenticado (especificado por `-U`) não possui privilégios necessários pelo pg_dump, mas pode alternar para um papel com os direitos necessários. Algumas instalações têm uma política contra a autenticação direta como superusuário, e o uso desta opção permite que os dumps sejam feitos sem violar a política.

## Meio Ambiente

`PGDATABASE` `PGHOST` `PGOPTIONS` `PGPORT` `PGUSER`: Parâmetros de conexão padrão.

`PG_COLOR`: Especifica se a cor deve ser usada em mensagens de diagnóstico. Os valores possíveis são `always`, `auto` e `never`.

Esse utilitário, como a maioria dos outros utilitários do PostgreSQL, também utiliza as variáveis de ambiente suportadas pelo libpq (consulte a Seção 32.15 [(libpq-envars.md "32.15. Environment Variables")]).

## Diagnósticos

O pg_dump executa internamente as instruções `SELECT`. Se você tiver problemas para executar o pg_dump, certifique-se de que você pode selecionar informações do banco de dados usando, por exemplo, [psql][(app-psql.md "psql")]. Além disso, quaisquer configurações de conexão padrão e variáveis de ambiente usadas pela biblioteca de interface libpq se aplicarão.

A atividade do banco de dados do pg_dump é normalmente coletada pelo sistema de estatísticas cumulativas. Se isso não for desejado, você pode definir o parâmetro `track_counts` para false via `PGOPTIONS` ou o comando `ALTER USER`.

## Notas

Se o seu clúster de banco de dados tiver quaisquer adições locais no banco de dados `template1`, tenha cuidado para restaurar a saída do pg_dump em um banco de dados verdadeiramente vazio; caso contrário, é provável que você obtenha erros devido a definições duplicadas dos objetos adicionados. Para criar um banco de dados vazio sem quaisquer adições locais, copie do `template0` e não do `template1`, por exemplo:

```
CREATE DATABASE foo WITH TEMPLATE template0;
```

Quando uma dump sem esquema é escolhida e a opção `--disable-triggers` é usada, o pg_dump emite comandos para desativar os gatilhos em tabelas de usuários antes de inserir os dados, e então comandos para reativá-los após os dados terem sido inseridos. Se o restauro for interrompido no meio do caminho, os catálogos do sistema podem ficar no estado errado.

Quando `--statistics` é especificado, `pg_dump` incluirá a maioria das estatísticas do otimizador no arquivo de dump resultante. Isso não inclui todas as estatísticas, como as criadas explicitamente com [CREATE STATISTICS](sql-createstatistics.md "CREATE STATISTICS"), estatísticas personalizadas adicionadas por uma extensão ou estatísticas coletadas pelo sistema de estatísticas cumulativas. Portanto, ainda pode ser útil executar `ANALYZE` após a restauração de um arquivo de dump para garantir um desempenho ótimo; consulte [Seção 24.1.3](routine-vacuuming.md#VACUUM-FOR-STATISTICS "24.1.3. Updating Planner Statistics") e [Seção 24.1.6](routine-vacuuming.md#AUTOVACUUM "24.1.6. The Autovacuum Daemon") para mais informações.

Como o pg_dump é usado para transferir dados para versões mais recentes do PostgreSQL, espera-se que a saída do pg_dump seja carregada em servidores PostgreSQL mais recentes do que a versão do pg_dump. O pg_dump também pode descartar servidores PostgreSQL mais antigos do que sua própria versão. (Atualmente, os servidores que retornam à versão 9.2 são suportados.) No entanto, o pg_dump não pode descartar servidores PostgreSQL mais recentes do que sua própria versão principal; ele se recusará até mesmo a tentar, em vez de arriscar fazer um dump inválido. Além disso, não é garantido que a saída do pg_dump possa ser carregada em um servidor de uma versão principal mais antiga — mesmo que o dump tenha sido feito de um servidor dessa versão. Carregar um arquivo de dump em um servidor mais antigo pode exigir edição manual do arquivo de dump para remover a sintaxe que não é entendida pelo servidor mais antigo. O uso da opção `--quote-all-identifiers` é recomendado em casos de versões cruzadas, pois pode evitar problemas decorrentes de listas de palavras reservadas variáveis em diferentes versões do PostgreSQL.

Ao descartar assinaturas de replicação lógica, o pg_dump gerará comandos `CREATE SUBSCRIPTION` que utilizam a opção `connect = false`, para que a restauração da assinatura não faça conexões remotas para criar um slot de replicação ou para uma cópia inicial da tabela. Dessa forma, o descarte pode ser restaurado sem exigir acesso à rede aos servidores remotos. Em seguida, cabe ao usuário reativar as assinaturas de maneira adequada. Se os hosts envolvidos tiverem mudado, as informações de conexão podem ter que ser alteradas. Também pode ser apropriado truncar as tabelas de destino antes de iniciar uma nova cópia completa da tabela. Se os usuários pretenderem copiar dados iniciais durante a atualização, eles devem criar o slot com `two_phase = false`. Após a sincronização inicial, a opção `two_phase`(sql-createsubscription.md#SQL-CREATESUBSCRIPTION-PARAMS-WITH-TWO-PHASE) será automaticamente habilitada pelo assinante se a assinatura tivesse sido originalmente criada com a opção `two_phase = true`.

Geralmente, é recomendado usar a opção `-X` (`--no-psqlrc`) ao restaurar um banco de dados a partir de um script de dump de texto plano pg_dump para garantir um processo de restauração limpo e evitar potenciais conflitos com configurações de psql não padrão.

## Exemplos

Para descartar um banco de dados chamado `mydb` em um arquivo de script SQL:

```
$ pg_dump mydb > db.sql
```

Para recarregar um script desse tipo em um banco de dados (criado recentemente) chamado `newdb`:

```
$ psql -X -d newdb -f db.sql
```

Para descartar um banco de dados em um arquivo de arquivo de formato personalizado:

```
$ pg_dump -Fc mydb > db.dump
```

Para descartar um banco de dados em um arquivo em formato de diretório:

```
$ pg_dump -Fd mydb -f dumpdir
```

Para descartar um banco de dados em um arquivo em formato de diretório em paralelo com 5 trabalhos de operador:

```
$ pg_dump -Fd mydb -j 5 -f dumpdir
```

Para recarregar um arquivo de arquivo em um banco de dados (criado recentemente) chamado `newdb`:

```
$ pg_restore -d newdb db.dump
```

Para recarregar um arquivo de arquivo na mesma base de dados de onde foi descartado, descartando o conteúdo atual dessa base de dados:

```
$ pg_restore -d postgres --clean --create db.dump
```

Para descartar uma única tabela chamada `mytab`:

```
$ pg_dump -t mytab mydb > db.sql
```

Para descartar todas as tabelas cujos nomes comecem com `emp` no esquema `detroit`, exceto a tabela denominada `employee_log`:

```
$ pg_dump -t 'detroit.emp*' -T detroit.employee_log mydb > db.sql
```

Para descartar todos os esquemas cujos nomes comecem com `east` ou `west` e terminem em `gsm`, excluindo quaisquer esquemas cujos nomes contenham a palavra `test`:

```
$ pg_dump -n 'east*gsm' -n 'west*gsm' -N '*test*' mydb > db.sql
```

O mesmo, usando notação de expressão regular para consolidar os switches:

```
$ pg_dump -n '(east|west)*gsm' -N '*test*' mydb > db.sql
```

Para descartar todos os objetos do banco de dados, exceto as tabelas cujos nomes comecem com `ts_`:

```
$ pg_dump -T 'ts_*' mydb > db.sql
```

Para especificar um nome em maiúsculas ou minúsculas em `-t` e switches relacionados, você precisa colocar aspas duplas no nome; caso contrário, ele será convertido para minúsculas (consulte [Padrões][(app-psql.md#APP-PSQL-PATTERNS "Patterns")]. Mas aspas são especiais para a concha, então, por sua vez, elas também devem ser citadas. Assim, para descartar uma única tabela com um nome em maiúsculas e minúsculas, você precisa de algo como

```
$ pg_dump -t "\"MixedCaseName\"" mydb > mytab.sql
```

Para descartar todas as tabelas cujos nomes comecem com `mytable`, exceto a tabela `mytable2`, especifique um arquivo de filtro `filter.txt` como:

```
include table mytable* exclude table mytable2
```

```
$ pg_dump --filter=filter.txt mydb > db.sql
```

## Veja também

[pg_dumpall](app-pg-dumpall.md "pg_dumpall"), [pg_restore](app-pgrestore.md "pg_restore"), [psql](app-psql.md "psql")