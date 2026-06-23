## pg_restore

pg_restore — restaurar um banco de dados PostgreSQL a partir de um arquivo de arquivo criado por pg_dump

## Sinopse

`pg_restore` [*`connection-option`*...] [*`option`*...] [*`filename`*]

## Descrição

O pg_restore é um utilitário para restaurar um banco de dados PostgreSQL a partir de um arquivo criado pelo [pg_dump](app-pgdump.md) em um dos formatos que não são de texto plano. Ele emitirá os comandos necessários para reconstruir o banco de dados ao estado em que estava no momento em que foi salvo. Os arquivos do arquivo também permitem que o pg_restore seja seletivo sobre o que é restaurado, ou até mesmo para reorganizar os itens antes de serem restaurados. Os arquivos do arquivo são projetados para ser portáveis em várias arquiteturas.

O pg_restore pode operar em dois modos. Se um nome de banco de dados for especificado, o pg_restore se conecta a esse banco de dados e restaura o conteúdo do arquivo diretamente no banco de dados. Caso contrário, um script que contém os comandos SQL necessários para reconstruir o banco de dados é criado e escrito em um arquivo ou saída padrão. A saída desse script é equivalente ao formato de saída de texto simples do pg_dump. Algumas das opções que controlam a saída são, portanto, análogas às opções do pg_dump.

Obviamente, o pg_restore não pode restaurar informações que não estão presentes no arquivo de arquivo. Por exemplo, se o arquivo foi criado usando a opção "dumpar dados como comandos `INSERT`", o pg_restore não poderá carregar os dados usando as instruções `COPY`.

### Aviso

Restaurar um dump faz com que o destino execute código arbitrário da escolha dos superusuários da fonte. Dumps parciais e restaurações parciais não limitam isso. Se os superusuários da fonte não forem confiáveis, as declarações SQL descartadas devem ser inspecionadas antes da restauração. Dumps que não são em texto plano podem ser inspecionados usando a opção `--file` do pg_restore. Note que o cliente que executa o dump e a restauração não precisa confiar nos superusuários da fonte ou do destino.

## Opções

pg_restore aceita os seguintes argumentos de linha de comando.

*`filename`*: Especifica o local do arquivo de arquivo (ou diretório, para um arquivo de formato de diretório) a ser restaurado. Se não especificado, o padrão de entrada é usado.

`-a` `--data-only`: Restaure apenas os dados, não o esquema (definições de dados) ou estatísticas. Os dados da tabela, grandes objetos e valores de sequência são restaurados, se estiverem presentes no arquivo.

Esta opção é semelhante, mas por razões históricas, não é idêntica à especificação `--section=data`.

`-c` `--clean`: Antes de restaurar objetos do banco de dados, emita comandos para `DROP` todos os objetos que serão restaurados. Esta opção é útil para sobrescrever um banco de dados existente. Se algum dos objetos não existir no banco de dados de destino, mensagens de erro ignoráveis serão relatadas, a menos que `--if-exists` também seja especificado.

`-C` `--create`: Crie o banco de dados antes de restaurá-lo nele. Se `--clean` também for especificado, elimine e recree o banco de dados de destino antes de se conectar a ele.

Com `--create`, o pg_restore também restaura o comentário do banco de dados, se houver, e quaisquer configurações de variáveis específicas para este banco de dados, ou seja, quaisquer comandos `ALTER DATABASE ... SET ...` e `ALTER ROLE ... IN DATABASE ... SET ...` que mencionem este banco de dados. Os privilégios de acesso para o próprio banco de dados também são restaurados, a menos que `--no-acl` seja especificado.

Quando esta opção é usada, o banco de dados denominado com `-d` é usado apenas para emitir os comandos iniciais `DROP DATABASE` e `CREATE DATABASE`. Todos os dados são restaurados no nome do banco de dados que aparece no arquivo.

`-d dbname` `--dbname=dbname`: Conecte-se ao banco de dados *`dbname`* e restaure diretamente no banco de dados. O *`dbname`* pode ser uma [string de conexão](libpq-connect.md#LIBPQ-CONNSTRING "32.1.1. Connection Strings"). Se assim for, os parâmetros da string de conexão substituirão quaisquer opções de linha de comando conflitantes.

`-e` `--exit-on-error`: Saia se um erro for encontrado ao enviar comandos SQL para o banco de dados. O padrão é continuar e exibir um número de erros no final da restauração.

`-f filename` `--file=filename`: Especifique o arquivo de saída para o script gerado, ou para a listagem quando usado com `-l`. Use `-` para stdout.

`-F format` `--format=format`: Especifique o formato do arquivo. Não é necessário especificar o formato, uma vez que o pg_restore determinará o formato automaticamente. Se especificado, pode ser um dos seguintes:

`c` `custom` :   O arquivo está no formato personalizado do pg_dump.

`d` `directory` :   O arquivo é um arquivo de diretório.

`t` `tar` :   O arquivo é um arquivo `tar`.

`-I index` `--index=index`: Restaurar a definição do índice nomeado apenas. Múltiplos índices podem ser especificados com múltiplos `-I` switches.

`-j number-of-jobs` `--jobs=number-of-jobs`: Execute as etapas mais demoradas do pg_restore — aquelas que carregam dados, criam índices ou criam restrições — de forma concorrente, usando até *`number-of-jobs`* sessões concorrentes. Esta opção pode reduzir drasticamente o tempo para restaurar um grande banco de dados em um servidor que está em uma máquina multiprocessadora. Esta opção é ignorada ao emitir um script em vez de se conectar diretamente a um servidor de banco de dados.

Cada trabalho é um processo ou um fio, dependendo do sistema operacional, e utiliza uma conexão separada com o servidor.

O valor ótimo para essa opção depende da configuração do hardware do servidor, do cliente e da rede. Os fatores incluem o número de núcleos da CPU e a configuração do disco. Um bom ponto de partida é o número de núcleos da CPU no servidor, mas valores maiores que esse também podem levar a tempos de restauração mais rápidos em muitos casos. Claro, valores que são muito altos levarão a um desempenho diminuído devido ao thrashing.

Apenas os formatos de arquivo de diretório e de arquivo personalizado são suportados com esta opção. O input deve ser um arquivo ou diretório regular (não, por exemplo, um pipe ou entrada padrão). Além disso, múltiplos trabalhos não podem ser usados juntos com a opção `--single-transaction`.

`-l` `--list`: Liste o índice do arquivo. A saída desta operação pode ser usada como entrada para a opção `-L`. Note que, se switches de filtragem como `-n` ou `-t` forem usados com `-l`, eles restringirão os itens listados.

`-L list-file` `--use-list=list-file`: Restaure apenas os elementos do arquivo que estão listados em *`list-file`*, e restaure-os na ordem em que aparecem no arquivo. Observe que, se switches de filtragem como `-n` ou `-t` forem usados com `-L`, eles restringirão ainda mais os itens restaurados.

*`list-file`* é normalmente criado editando a saída de uma operação anterior `-l`. As linhas podem ser movidas ou removidas, e também podem ser comentadas, colocando um ponto e vírgula (`;`) no início da linha. Veja abaixo exemplos.

`-n schema` `--schema=schema`: Restaure apenas os objetos que estão no esquema nomeado. Múltiplos esquemas podem ser especificados com múltiplos interruptores `-n`. Isso pode ser combinado com a opção `-t` para restaurar apenas uma tabela específica.

`-N schema` `--exclude-schema=schema`: Não restaure objetos que estejam no esquema nomeado. Múltiplos esquemas a serem excluídos podem ser especificados com múltiplos interruptores `-N`.

Quando tanto o `-n` quanto o `-N` são fornecidos para o mesmo nome do esquema, o interruptor `-N` vence e o esquema é excluído.

`-O` `--no-owner`: Não emita comandos para definir a propriedade dos objetos de acordo com o banco de dados original. Por padrão, o pg_restore emite as declarações `ALTER OWNER` ou `SET SESSION AUTHORIZATION` para definir a propriedade dos elementos do esquema criados. Essas declarações falharão, a menos que a conexão inicial com o banco de dados seja feita por um superusuário (ou pelo mesmo usuário que possui todos os objetos do script). Com `-O`, qualquer nome de usuário pode ser usado para a conexão inicial, e esse usuário possuirá todos os objetos criados.

`-P function-name(argtype [, ...])` `--function=function-name(argtype [, ...])`: Restaure apenas a função designada. Tenha cuidado para digitar o nome da função e os argumentos exatamente como aparecem na tabela de conteúdo do arquivo de depuração. Múltiplas funções podem ser especificadas com múltiplos interruptores `-P`.

`-R` `--no-reconnect`: Esta opção é obsoleta, mas ainda é aceita para compatibilidade reversa.

`-s` `--schema-only`: Restaure apenas o esquema (definições de dados), não os dados, na medida em que as entradas do esquema estejam presentes no arquivo.

Esta opção não pode ser usada com `--data-only` ou `--statistics-only`. É semelhante, mas por razões históricas, não é idêntica à especificação de `--section=pre-data --section=post-data --no-statistics`.

(Não confunda isso com a opção `--schema`, que usa a palavra “esquema” em um significado diferente.)

`-S username` `--superuser=username`: Especifique o nome do usuário superusuário a ser usado ao desabilitar gatilhos. Isso é relevante apenas se `--disable-triggers` for usado.

`-t table` `--table=table`: Restaure a definição e/ou os dados apenas da tabela especificada. Para este propósito, “tabela” inclui visualizações, visualizações materializadas, sequências e tabelas externas. Múltiplas tabelas podem ser selecionadas escrevendo vários interruptores `-t`. Esta opção pode ser combinada com a opção `-n` para especificar(es) a(s) tabela(s) em um esquema específico.

Nota

Quando o `-t` é especificado, o pg_restore não faz qualquer tentativa de restaurar quaisquer outros objetos do banco de dados que as tabelas selecionadas possam depender. Portanto, não há garantia de que um restauro específico em uma base de dados limpa terá sucesso.

Nota

Essa bandeira não se comporta de maneira idêntica à bandeira `-t` do pg_dump. Atualmente, não há nenhuma disposição para correspondência de wildcard no pg_restore, e você também não pode incluir um nome de esquema em seu `-t`. E, embora a bandeira `-t` do pg_dump também descarregue objetos subsidiários (como índices) da(s) tabela(s) selecionada(s), a bandeira `-t` do pg_restore não inclui tais objetos subsidiários.

Nota

Em versões anteriores ao PostgreSQL 9.6, essa bandeira correspondia apenas a tabelas, e não a qualquer outro tipo de relação.

`-T trigger` `--trigger=trigger`: Restaurar o gatilho nomeado apenas. Múltiplos gatilhos podem ser especificados com múltiplos interruptores `-T`.

`-v` `--verbose`: Especifica o modo verbose. Isso fará com que o pg_restore emita comentários detalhados sobre os objetos e os tempos de início/parada no arquivo de saída, além de mensagens de progresso no erro padrão. A repetição da opção fará com que mensagens adicionais de nível de depuração apareçam no erro padrão.

`-V` `--version`: Imprimir a versão do pg_restore e sair.

`-x` `--no-privileges` `--no-acl`: Prevenir a restauração de privilégios de acesso (comandos de concessão/rejeição).

`-1` `--single-transaction`: Execute o restabelecimento como uma única transação (ou seja, envolva os comandos emitidos em `BEGIN`/`COMMIT`). Isso garante que todos os comandos sejam concluídos com sucesso ou que nenhuma alteração seja aplicada. Esta opção implica em `--exit-on-error`.

`--disable-triggers`: Esta opção é relevante apenas ao realizar um restabelecimento sem esquema. Instrui o pg_restore a executar comandos para desabilitar temporariamente os gatilhos nas tabelas de destino enquanto os dados são restaurados. Use essa opção se você tiver verificações de integridade referencial ou outros gatilhos nas tabelas que você não deseja invocar durante o restabelecimento de dados.

Atualmente, os comandos emitidos para `--disable-triggers` devem ser feitos como superusuário. Portanto, você também deve especificar um nome de superusuário com `-S` ou, de preferência, executar o pg_restore como um superusuário do PostgreSQL.

`--enable-row-security`: Esta opção é relevante apenas ao restaurar o conteúdo de uma tabela que possui segurança de linha. Por padrão, o pg_restore definirá [row_security](runtime-config-client.md#GUC-ROW-SECURITY) como desligado, para garantir que todos os dados sejam restaurados na tabela. Se o usuário não tiver privilégios suficientes para contornar a segurança de linha, então um erro será lançado. Este parâmetro instrui o pg_restore a definir [row_security](runtime-config-client.md#GUC-ROW-SECURITY) como ligado, permitindo que o usuário tente restaurar o conteúdo da tabela com segurança de linha habilitada. Isso ainda pode falhar se o usuário não tiver o direito de inserir as linhas do dump na tabela.

Observe que essa opção atualmente também exige que o dump esteja no formato `INSERT`, pois o `COPY FROM` não suporta segurança de linha.

`--filter=filename`: Especifique um nome de arquivo a partir do qual ler padrões para objetos excluídos ou incluídos na restauração. Os padrões são interpretados de acordo com as mesmas regras que `-n`/`--schema` para incluir objetos em esquemas, `-N`/`--exclude-schema` para excluir objetos em esquemas, `-P`/`--function` para restaurar funções nomeadas, `-I`/`--index` para restaurar índices nomeados, `-t`/`--table` para restaurar tabelas nomeadas ou `-T`/`--trigger` para restaurar gatilhos. Para ler a partir de `STDIN`, use `-` como o nome do arquivo. A opção `--filter` pode ser especificada em conjunto com as opções listadas acima para incluir ou excluir objetos, e também pode ser especificada mais de uma vez para múltiplos arquivos de filtro.

O arquivo lista um padrão de banco de dados por linha, com o seguinte formato:

```
{ include | exclude } { function | index | schema | table | trigger } PATTERN
```

A primeira palavra-chave especifica se os objetos que correspondem ao padrão devem ser incluídos ou excluídos. A segunda palavra-chave especifica o tipo de objeto que deve ser filtrado usando o padrão:

* `function`: funções, funciona como a opção `-P`/`--function`. Este termo só pode ser usado com o termo `include`.
* `index`: índices, funciona como a opção `-I`/`--indexes`. Este termo só pode ser usado com o termo `include`.
* `schema`: esquemas, funciona como as opções `-n`/`--schema` e `-N`/`--exclude-schema`.
* `table`: tabelas, funciona como a opção `-t`/`--table`. Este termo só pode ser usado com o termo `include`.
* `trigger`: gatilhos, funciona como a opção `-T`/`--trigger`. Este termo só pode ser usado com o termo `include`.

As linhas que começam com `#` são consideradas comentários e ignoradas. Comentários também podem ser colocados após uma linha de padrão de objeto. Linhas em branco também são ignoradas. Veja [Padrões](app-psql.md#APP-PSQL-PATTERNS "Patterns") para saber como realizar citação em padrões.

`--if-exists`: Use os comandos `DROP ... IF EXISTS` para descartar objetos no modo `--clean`. Isso suprime os erros de "não existe" que, de outra forma, poderiam ser relatados. Esta opção não é válida, a menos que `--clean` também seja especificado.

`--no-comments`: Não exiba comandos para restaurar comentários, mesmo que o arquivo os contenha.

`--no-data`: Não emita comandos para restaurar dados, mesmo que o arquivo os contenha.

`--no-data-for-failed-tables`: Por padrão, os dados da tabela são restaurados mesmo se o comando de criação da tabela falhar (por exemplo, porque ela já existe). Com esta opção, os dados de uma tabela desse tipo são ignorados. Esse comportamento é útil se o banco de dados de destino já contiver o conteúdo desejado da tabela. Por exemplo, as tabelas auxiliares para extensões do PostgreSQL, como PostGIS, podem já estar carregadas no banco de dados de destino; especificar esta opção evita que dados duplicados ou obsoletos sejam carregados nelas.

Essa opção é eficaz apenas ao restaurar diretamente em um banco de dados, não quando produzindo saída de script SQL.

`--no-policies`: Não execute comandos para restaurar as políticas de segurança de linha, mesmo que o arquivo as contenha.

`--no-publications`: Não emita comandos para restaurar publicações, mesmo que o arquivo as contenha.

`--no-schema`: Não exiba comandos para restaurar o esquema (definições de dados), mesmo que o arquivo os contenha.

`--no-security-labels`: Não emita comandos para restaurar etiquetas de segurança, mesmo que o arquivo as contenha.

`--no-statistics`: Não emita comandos para restaurar estatísticas, mesmo que o arquivo as contenha.

`--no-subscriptions`: Não emita comandos para restaurar assinaturas, mesmo que o arquivo as contenha.

`--no-table-access-method`: Não exiba comandos para selecionar métodos de acesso à tabela. Com esta opção, todos os objetos serão criados com o método de acesso à tabela que é o padrão durante a restauração.

`--no-tablespaces`: Não execute comandos para selecionar tablespaces. Com esta opção, todos os objetos serão criados no tablespace padrão durante o restabelecimento.

`--restrict-key=restrict_key`: Use a string fornecida como a chave `\restrict` no psql na saída do dump. Isso só pode ser especificado para saída de script SQL, ou seja, quando a opção `--file` é usada. Se nenhuma chave restrita for especificada, o pg_restore gerará uma aleatória conforme necessário. As chaves podem conter apenas caracteres alfanuméricos.

Esta opção é destinada principalmente a fins de teste e outros cenários que exigem saída repetida (por exemplo, comparar arquivos de depuração). Não é recomendada para uso geral, pois um servidor malicioso com conhecimento avançado da chave pode ser capaz de injetar código arbitrário que será executado na máquina que executa o psql com a saída de depuração.

`--section=sectionname`: Restaure apenas a seção nomeada. O nome da seção pode ser `pre-data`, `data` ou `post-data`. Esta opção pode ser especificada mais de uma vez para selecionar várias seções. O padrão é restaurar todas as seções.

A seção de dados contém dados reais da tabela, bem como definições de objetos grandes. Os itens pós-dados consistem em definições de índices, gatilhos, regras e restrições que não são restrições de verificação validadas. Os itens pré-dados consistem em todos os outros itens de definição de dados.

`--statistics`: Comandos de saída para restaurar estatísticas, se o arquivo as contiver. Isso é o padrão.

`--statistics-only`: Restaure apenas as estatísticas, não o esquema (definições de dados) ou os dados.

`--strict-names`: Exigir que cada qualificador de esquema (`-n`/`--schema`) e tabela (`-t`/`--table`) corresponda a pelo menos um esquema/tabela no arquivo a ser restaurado.

`--transaction-size=N`: Execute o restauro como uma série de transações, processando cada uma até *`N`* objetos de banco de dados. Esta opção implica em `--exit-on-error`.

`--transaction-size` oferece uma opção intermediária entre o comportamento padrão (uma transação por comando SQL) e `-1`/`--single-transaction` (uma transação para todos os objetos restaurados). Embora `--single-transaction` tenha o menor custo, pode ser impraticável para grandes bancos de dados, pois a transação assumirá um bloqueio em cada objeto restaurado, possivelmente esgotando o espaço de tabela de bloqueio do servidor. Usando `--transaction-size` com um tamanho de alguns milhares de objetos, oferece benefícios de desempenho quase iguais, ao mesmo tempo em que limita a quantidade de espaço de tabela de bloqueio necessária.

`--use-set-session-authorization`: Em vez de comandos padrão SQL `SET SESSION AUTHORIZATION`, execute comandos padrão SQL `ALTER OWNER` para determinar a propriedade dos objetos. Isso torna o dump mais compatível com os padrões, mas, dependendo do histórico dos objetos no dump, pode não ser restaurado corretamente.

`-?` `--help`: Mostrar ajuda sobre os argumentos da linha de comando do comando pg_restore e sair.

O pg_restore também aceita os seguintes argumentos de linha de comando para parâmetros de conexão:

`-h host` `--host=host`: Especifica o nome do host da máquina na qual o servidor está sendo executado. Se o valor começar com uma barra, ele é usado como o diretório para o socket de domínio Unix. O padrão é tomado da variável de ambiente `PGHOST`, se definida, caso contrário, uma conexão de socket de domínio Unix é tentada.

`-p port` `--port=port`: Especifica a porta TCP ou a extensão de arquivo de soquete de domínio Unix local em que o servidor está ouvindo conexões. Tem como padrão a variável de ambiente `PGPORT`, se definida, ou um padrão incorporado.

`-U username` `--username=username`: Nome do usuário para se conectar como.

`-w` `--no-password`: Nunca emita um prompt de senha. Se o servidor exigir autenticação por senha e uma senha não estiver disponível por outros meios, como um arquivo `.pgpass`, a tentativa de conexão falhará. Esta opção pode ser útil em trabalhos em lote e scripts onde nenhum usuário está presente para inserir uma senha.

`-W` `--password`: Forçar o pg_restore a solicitar uma senha antes de se conectar a um banco de dados.

Essa opção nunca é essencial, pois o pg_restore solicitará automaticamente uma senha se o servidor exigir autenticação por senha. No entanto, o pg_restore desperdiçará uma tentativa de conexão descobrindo que o servidor deseja uma senha. Em alguns casos, vale a pena digitar `-W` para evitar a tentativa extra de conexão.

`--role=rolename`: Especifica um nome de papel a ser usado para realizar o restabelecimento. Esta opção faz com que o pg_restore emita um comando `SET ROLE` *`rolename`* após se conectar ao banco de dados. É útil quando o usuário autenticado (especificado por `-U`) não possui privilégios necessários pelo pg_restore, mas pode alternar para um papel com os direitos necessários. Algumas instalações têm uma política contra a conexão direta como superusuário, e o uso desta opção permite que os restabelecimentos sejam realizados sem violar a política.

## Meio Ambiente

`PGHOST` `PGOPTIONS` `PGPORT` `PGUSER`: Parâmetros de conexão padrão

`PG_COLOR`: Especifica se a cor deve ser usada em mensagens de diagnóstico. Os valores possíveis são `always`, `auto` e `never`.

Esse utilitário, como a maioria dos outros utilitários do PostgreSQL, também utiliza as variáveis de ambiente suportadas pelo libpq (consulte [Seção 32.15](libpq-envars.md)). No entanto, ele não lê `PGDATABASE` quando o nome do banco de dados não é fornecido.

## Diagnósticos

Quando uma conexão direta com o banco de dados é especificada usando a opção `-d`, o pg_restore executa internamente instruções SQL. Se você tiver problemas para executar o pg_restore, certifique-se de que você pode selecionar informações do banco de dados usando, por exemplo, [psql](app-psql.md). Além disso, quaisquer configurações de conexão padrão e variáveis de ambiente usadas pela biblioteca de interface libpq se aplicarão.

## Notas

Se a sua instalação tiver alguma adição local no banco de dados `template1`, tenha cuidado para carregar a saída do pg_restore em um banco de dados verdadeiramente vazio; caso contrário, você provavelmente obterá erros devido a definições duplicadas dos objetos adicionados. Para criar um banco de dados vazio sem quaisquer adições locais, copie de `template0` e não de `template1`, por exemplo:

```
CREATE DATABASE foo WITH TEMPLATE template0;
```

As limitações do pg_restore são detalhadas abaixo.

* Ao restaurar dados para uma tabela pré-existente e a opção `--disable-triggers` for usada, o pg_restore emite comandos para desativar gatilhos em tabelas de usuários antes de inserir os dados, e em seguida emite comandos para reativá-los após os dados terem sido inseridos. Se o restauro for interrompido no meio do caminho, os catálogos do sistema podem ficar no estado errado.
* O pg_restore não pode restaurar objetos grandes seletivamente; por exemplo, apenas aqueles para uma tabela específica. Se um arquivo contiver objetos grandes, todos os objetos grandes serão restaurados, ou nenhum deles se forem excluídos via `-L`, `-t` ou outras opções.

Veja também a documentação do [pg_dump](app-pgdump.md) para obter detalhes sobre as limitações do pg_dump.

Por padrão, `pg_restore` restaurará as estatísticas do otimizador se estiver incluído no arquivo de dump. Se todas as estatísticas não tiverem sido restauradas, pode ser útil executar `ANALYZE` em cada tabela restaurada para que o otimizador tenha estatísticas úteis; consulte [Seção 24.1.3](routine-vacuuming.md#VACUUM-FOR-STATISTICS) e [Seção 24.1.6](routine-vacuuming.md#AUTOVACUUM) para obter mais informações.

## Exemplos

Suponha que tenhamos descarregado um banco de dados chamado `mydb` em um arquivo de dump de formato personalizado:

```
$ pg_dump -Fc mydb > db.dump
```

Para descartar o banco de dados e recriá-lo a partir do dump:

```
$ dropdb mydb $ pg_restore -C -d postgres db.dump
```

O banco de dados denominado no interruptor `-d` pode ser qualquer banco de dados existente no clúster; o pg_restore só o usa para emitir o comando `CREATE DATABASE` para `mydb`. Com `-C`, os dados são sempre restaurados no nome do banco de dados que aparece no arquivo de dump.

Para restaurar o dump em um novo banco de dados chamado `newdb`:

```
$ createdb -T template0 newdb $ pg_restore -d newdb db.dump
```

Observe que não usamos `-C`, e, em vez disso, conectamos diretamente ao banco de dados que será restaurado. Além disso, observe que clonamos o novo banco de dados a partir de `template0` e não de `template1`, para garantir que ele esteja inicialmente vazio.

Para reorganizar os itens do banco de dados, é necessário, em primeiro lugar, fazer uma cópia da tabela de conteúdo do arquivo:

```
$ pg_restore -l db.dump > db.list
```

O arquivo de listagem consiste em um cabeçalho e uma linha para cada item, por exemplo:

```
; ; Archive created at Mon Sep 14 13:55:39 2009 ;     dbname: DBDEMOS ;     TOC Entries: 81 ;     Compression: 9 ;     Dump Version: 1.10-0 ;     Format: CUSTOM ;     Integer: 4 bytes ;     Offset: 8 bytes ;     Dumped from database version: 8.3.5 ;     Dumped by pg_dump version: 8.3.8 ; ; ; Selected TOC Entries: ; 3; 2615 2200 SCHEMA - public pasha 1861; 0 0 COMMENT - SCHEMA public pasha 1862; 0 0 ACL - public pasha 317; 1247 17715 TYPE public composite pasha 319; 1247 25899 DOMAIN public domain0 pasha
```

Os pontos e vírgulas iniciam um comentário, e os números no início das linhas se referem à ID do arquivo interno atribuída a cada item.

As linhas no arquivo podem ser comentadas, excluídas e reorganizadas. Por exemplo:

```
10; 145433 TABLE map_resolutions postgres ;2; 145344 TABLE species postgres ;4; 145359 TABLE nt_header postgres 6; 145402 TABLE species_records postgres ;8; 145416 TABLE ss_old postgres
```

poderia ser usado como entrada para o pg_restore e restauraria apenas os itens 10 e 6, nessa ordem:

```
$ pg_restore -L db.list db.dump
```

## Veja também

[pg_dump](app-pgdump.md "pg_dump"), [pg_dumpall](app-pg-dumpall.md "pg_dumpall"), [psql](app-psql.md "psql")