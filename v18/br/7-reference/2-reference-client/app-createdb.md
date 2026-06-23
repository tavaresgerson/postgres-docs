## createdb

createdb — criar um novo banco de dados PostgreSQL

## Sinopse

`createdb` [*`connection-option`*...] [*`option`*...] [*`dbname`* [*`description`*]]

## Descrição

createdb cria um novo banco de dados PostgreSQL.

Normalmente, o usuário do banco de dados que executa este comando se torna o proprietário do novo banco de dados. No entanto, um proprietário diferente pode ser especificado via a opção `-O`, se o usuário que executa tiver os privilégios apropriados.

createdb é um wrapper em torno do comando SQL `CREATE DATABASE`(sql-createdatabase.md "CREATE DATABASE"). Não há diferença efetiva entre a criação de bancos de dados por meio deste utilitário e por meio de outros métodos para acessar o servidor.

## Opções

createdb aceita os seguintes argumentos de linha de comando:

*`dbname`*: Especifica o nome do banco de dados a ser criado. O nome deve ser único entre todos os bancos de dados PostgreSQL neste clúster. O padrão é criar um banco de dados com o mesmo nome do usuário atual do sistema.

*`description`*: Especifica um comentário a ser associado ao banco de dados recém-criado.

`-D tablespace` `--tablespace=tablespace`: Especifica o espaço de tabela padrão para o banco de dados. (Esse nome é processado como um identificador com aspas duplas.)

`-e` `--echo`: Repita os comandos que o createb gera e envia para o servidor.

`-E encoding`: Especifica o esquema de codificação de caracteres a ser utilizado neste banco de dados. Os conjuntos de caracteres suportados pelo servidor PostgreSQL são descritos em [Seção 23.3.1](multibyte.md#MULTIBYTE-CHARSET-SUPPORTED).

`-l locale` `--locale=locale`: Especifica o local a ser utilizado neste banco de dados. Isso é equivalente a especificar `--lc-collate`, `--lc-ctype` e `--icu-locale` com o mesmo valor. Alguns locais são válidos apenas para ICU e devem ser definidos com `--icu-locale`.

`--lc-collate=locale`: Especifica o ajuste LC_COLLATE a ser utilizado neste banco de dados.

`--lc-ctype=locale`: Especifica o ajuste LC_CTYPE a ser utilizado neste banco de dados.

`--builtin-locale=locale`: Especifica o nome do local quando o provedor incorporado é usado. O suporte ao local é descrito em [Seção 23.1](locale.md).

`--icu-locale=locale`: Especifica o ID do local do ICU a ser utilizado neste banco de dados, se o provedor de localização do ICU for selecionado.

`--icu-rules=rules`: Especifica regras de ordenação adicionais para personalizar o comportamento da ordenação padrão deste banco de dados. Isso é suportado apenas para ICU.

`--locale-provider={builtin|libc|icu}`: Especifica o provedor de localização para a collation padrão do banco de dados.

`-O owner` `--owner=owner`: Especifica o usuário do banco de dados que possuirá o novo banco de dados. (Esse nome é processado como um identificador com aspas duplas.)

`-S strategy` `--strategy=strategy`: Especifica a estratégia de criação do banco de dados. Consulte [ESTRUTURA DE ESTRATÉGIA DE Criação de Banco de Dados](sql-createdatabase.md#CREATE-DATABASE-STRATEGY) para mais detalhes.

`-T template` `--template=template`: Especifica o banco de dados de modelo a partir do qual será construído este banco de dados. (Esse nome é processado como um identificador com aspas duplas.)

`-V` `--version`: Imprimir a versão do createdb e sair.

`-?` `--help`: Mostrar ajuda sobre os argumentos da linha de comando do comando createdb e sair.

As opções `-D`, `-l`, `-E`, `-O` e `-T` correspondem às opções do comando SQL subjacente [`CREATE DATABASE`](sql-createdatabase.md); consulte-o para obter mais informações sobre elas.

O createdb também aceita os seguintes argumentos de linha de comando para parâmetros de conexão:

`-h host` `--host=host`: Especifica o nome do host da máquina na qual o servidor está sendo executado. Se o valor começar com uma barra, ele é usado como o diretório para o socket de domínio Unix.

`-p port` `--port=port`: Especifica a porta TCP ou a extensão de arquivo de soquete de domínio Unix local em que o servidor está ouvindo conexões.

`-U username` `--username=username`: Nome do usuário para se conectar como.

`-w` `--no-password`: Nunca emita um prompt de senha. Se o servidor exigir autenticação por senha e uma senha não estiver disponível por outros meios, como um arquivo `.pgpass`, a tentativa de conexão falhará. Esta opção pode ser útil em trabalhos em lote e scripts onde nenhum usuário está presente para inserir uma senha.

`-W` `--password`: Força createdb para solicitar uma senha antes de se conectar a um banco de dados.

Essa opção nunca é essencial, pois o createdb solicitará automaticamente uma senha se o servidor exigir autenticação por senha. No entanto, o createdb desperdiçará uma tentativa de conexão descobrindo que o servidor deseja uma senha. Em alguns casos, vale a pena digitar `-W` para evitar a tentativa extra de conexão.

`--maintenance-db=dbname`: Especifica o nome do banco de dados a ser conectado ao ao criar o novo banco de dados. Se não especificado, o banco de dados `postgres` será usado; se este não existir (ou se for o nome do novo banco de dados que está sendo criado), `template1` será usado. Isso pode ser uma [string de conexão](libpq-connect.md#LIBPQ-CONNSTRING "32.1.1. Connection Strings"). Se assim for, os parâmetros da string de conexão substituirão quaisquer opções de linha de comando conflitantes.

## Meio Ambiente

`PGDATABASE`: Se definido, o nome do banco de dados a ser criado, a menos que seja sobrescrito na linha de comando.

`PGHOST` `PGPORT` `PGUSER`: Parâmetros de conexão padrão. `PGUSER` também determina o nome do banco de dados a ser criado, se não for especificado na linha de comando ou por `PGDATABASE`.

`PG_COLOR`: Especifica se a cor deve ser usada nas mensagens de diagnóstico. Os valores possíveis são `always`, `auto` e `never`.

Esse utilitário, como a maioria dos outros utilitários do PostgreSQL, também utiliza as variáveis de ambiente suportadas pelo libpq (consulte a [Seção 32.15](libpq-envars.md)).

## Diagnósticos

Em caso de dificuldade, consulte [CREATE DATABASE](sql-createdatabase.md "CREATE DATABASE") e [psql](app-psql.md "psql") para discussões sobre problemas potenciais e mensagens de erro. O servidor de banco de dados deve estar em execução no host alvo. Além disso, quaisquer configurações de conexão padrão e variáveis de ambiente usadas pela biblioteca de interface libpq serão aplicadas.

## Exemplos

Para criar o banco de dados `demo` usando o servidor de banco de dados padrão:

```
$ createdb demo
```

Para criar o banco de dados `demo` usando o servidor no host `eden`, na porta 5000, usando o banco de dados de modelo `template0`, aqui está o comando de linha de comando e o comando SQL subjacente:

```
$ createdb -p 5000 -h eden -T template0 -e demo
CREATE DATABASE demo TEMPLATE template0;
```

## Veja também

[dropdb](app-dropdb.md "dropdb"), [CREATE DATABASE](sql-createdatabase.md "CREATE DATABASE")