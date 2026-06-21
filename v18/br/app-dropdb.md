## dropdb

dropdb — remover um banco de dados PostgreSQL

## Sinopse

`dropdb` [*`connection-option`*...] [*`option`*...] *`dbname`*

## Descrição

dropdb destrói um banco de dados PostgreSQL existente. O usuário que executa este comando deve ser um superusuário do banco de dados ou o proprietário do banco de dados.

dropdb é um wrapper em torno do comando SQL `DROP DATABASE`(sql-dropdatabase.md "DROP DATABASE"). Não há diferença efetiva entre a eliminação de bancos de dados por meio deste utilitário e por meio de outros métodos para acessar o servidor.

## Opções

dropdb aceita os seguintes argumentos de linha de comando:

*`dbname`*: Especifica o nome do banco de dados que será removido.

`-e` `--echo`: Repita os comandos que o dropdb gera e envia para o servidor.

`-f`: Tente encerrar todas as conexões existentes com o banco de dados de destino antes de descartá-lo. Consulte [DROP DATABASE](sql-dropdatabase.md "DROP DATABASE") para obter mais informações sobre essa opção.

`-i` `--interactive`: Emite um prompt de verificação antes de realizar qualquer ação destrutiva.

`-V` `--version`: Imprimir a versão do dropdb e sair.

`--if-exists`: Não exija erro se o banco de dados não existir. Um aviso é emitido neste caso.

`-?` `--help`: Mostrar ajuda sobre os argumentos da linha de comando do comando dropdb e sair.

O dropdb também aceita os seguintes argumentos de linha de comando para parâmetros de conexão:

`-h host` `--host=host`: Especifica o nome do host da máquina em que o servidor está sendo executado. Se o valor começar com uma barra, ele é usado como o diretório para o socket de domínio Unix.

`-p port` `--port=port`: Especifica a porta TCP ou a extensão de arquivo de soquete de domínio Unix local em que o servidor está ouvindo conexões.

`-U username` `--username=username`: Nome do usuário para se conectar como.

`-w` `--no-password`: Nunca emita um prompt de senha. Se o servidor exigir autenticação por senha e uma senha não estiver disponível por outros meios, como um arquivo `.pgpass`, a tentativa de conexão falhará. Esta opção pode ser útil em trabalhos em lote e scripts onde nenhum usuário está presente para inserir uma senha.

`-W` `--password`: Forçar o dropdb a solicitar uma senha antes de se conectar a um banco de dados.

Essa opção nunca é essencial, pois o dropdb solicitará automaticamente uma senha se o servidor exigir autenticação por senha. No entanto, o dropdb desperdiçará uma tentativa de conexão descobrindo que o servidor deseja uma senha. Em alguns casos, vale a pena digitar `-W` para evitar a tentativa extra de conexão.

`--maintenance-db=dbname`: Especifica o nome do banco de dados a ser conectado para descartar o banco de dados de destino. Se não especificado, o banco de dados `postgres` será usado; se este não existir (ou o banco de dados está sendo descartado), `template1` será usado. Isso pode ser uma [string de conexão](libpq-connect.md#LIBPQ-CONNSTRING "32.1.1. Connection Strings"). Se assim for, os parâmetros da string de conexão substituirão quaisquer opções de linha de comando conflitantes.

## Meio Ambiente

`PGHOST` `PGPORT` `PGUSER`: Parâmetros de conexão padrão

`PG_COLOR`: Especifica se a cor deve ser usada nas mensagens de diagnóstico. Os valores possíveis são `always`, `auto` e `never`.

Esse utilitário, como a maioria dos outros utilitários do PostgreSQL, também utiliza as variáveis de ambiente suportadas pelo libpq (consulte a [Seção 32.15](libpq-envars.md)).

## Diagnósticos

Em caso de dificuldade, consulte [DROP DATABASE](sql-dropdatabase.md) e [psql](app-psql.md) para discussões sobre problemas potenciais e mensagens de erro. O servidor de banco de dados deve estar em execução no host alvo. Além disso, quaisquer configurações de conexão padrão e variáveis de ambiente usadas pela biblioteca de interface libpq serão aplicadas.

## Exemplos

Para destruir o banco de dados `demo` no servidor de banco de dados padrão:

```
$ dropdb demo
```

Para destruir o banco de dados `demo` usando o servidor no host `eden`, porta 5000, com verificação e uma olhada no comando subjacente:

```
$ dropdb -p 5000 -h eden -i -e demo
Database "demo" will be permanently deleted.
Are you sure? (y/n) y
DROP DATABASE demo;
```

## Veja também

[createdb](app-createdb.md "createdb"), [DROP DATABASE](sql-dropdatabase.md "DROP DATABASE")