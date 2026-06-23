## dropuser

dropuser — remover uma conta de usuário do PostgreSQL

## Sinopse

`dropuser` [*`connection-option`*...] [*`option`*...] [*`username`*]

## Descrição

dropuser remove um usuário existente do PostgreSQL. Superusuários podem usar este comando para remover qualquer papel; caso contrário, apenas os papéis que não são de superusuário podem ser removidos, e apenas por um usuário que possui o privilégio `CREATEROLE` e que foi concedido `ADMIN OPTION` no papel alvo.

dropuser é um wrapper em torno do comando SQL `DROP ROLE` (sql-droprole.md "DROP ROLE"). Não há diferença efetiva entre a eliminação de usuários por meio deste utilitário e por meio de outros métodos para acessar o servidor.

## Opções

dropuser aceita os seguintes argumentos de linha de comando:

*`username`*: Especifica o nome do usuário do PostgreSQL a ser removido. Você será solicitado a digitar um nome se nenhum nome for especificado na linha de comando e a opção `-i`/`--interactive` for usada.

`-e` `--echo`: Repita os comandos que o dropuser gera e envia para o servidor.

`-i` `--interactive`: Solicitar confirmação antes de realmente remover o usuário e solicitar o nome do usuário se nenhum nome for especificado na linha de comando.

`-V` `--version`: Imprimir a versão do dropuser e sair.

`--if-exists`: Não exija erro se o usuário não existir. Um aviso é emitido neste caso.

`-?` `--help`: Mostrar ajuda sobre os argumentos da linha de comando do comando dropuser e sair.

O dropuser também aceita os seguintes argumentos de linha de comando para parâmetros de conexão:

`-h host` `--host=host`: Especifica o nome do host da máquina em que o servidor está sendo executado. Se o valor começar com uma barra, ele é usado como o diretório para o socket de domínio Unix.

`-p port` `--port=port`: Especifica a porta TCP ou a extensão de arquivo de soquete de domínio Unix local em que o servidor está ouvindo conexões.

`-U username` `--username=username`: Nome do usuário para se conectar como (não o nome do usuário para ser descartado).

`-w` `--no-password`: Nunca emita um prompt de senha. Se o servidor exigir autenticação por senha e uma senha não estiver disponível por outros meios, como um arquivo `.pgpass`, a tentativa de conexão falhará. Esta opção pode ser útil em trabalhos em lote e scripts onde nenhum usuário está presente para inserir uma senha.

`-W` `--password`: Forçar o usuário a solicitar uma senha antes de se conectar a um banco de dados.

Essa opção nunca é essencial, pois o dropuser solicitará automaticamente uma senha se o servidor exigir autenticação por senha. No entanto, o dropuser desperdiçará uma tentativa de conexão descobrindo que o servidor deseja uma senha. Em alguns casos, vale a pena digitar `-W` para evitar a tentativa extra de conexão.

## Meio Ambiente

`PGHOST` `PGPORT` `PGUSER`: Parâmetros de conexão padrão

`PG_COLOR`: Especifica se a cor deve ser usada em mensagens de diagnóstico. Os valores possíveis são `always`, `auto` e `never`.

Esse utilitário, como a maioria dos outros utilitários do PostgreSQL, também utiliza as variáveis de ambiente suportadas pelo libpq (consulte a [Seção 32.15](libpq-envars.md)).

## Diagnósticos

Em caso de dificuldade, consulte [DROP ROLE](sql-droprole.md "DROP ROLE") e [psql](app-psql.md "psql") para discussões sobre problemas potenciais e mensagens de erro. O servidor de banco de dados deve estar em execução no host alvo. Além disso, quaisquer configurações de conexão padrão e variáveis de ambiente usadas pela biblioteca de interface libpq serão aplicadas.

## Exemplos

Para remover o usuário `joe` do servidor de banco de dados padrão:

```
$ dropuser joe
```

Para remover o usuário `joe` usando o servidor no host `eden`, porta 5000, com verificação e uma visão do comando subjacente:

```
$ dropuser -p 5000 -h eden -i -e joe
Role "joe" will be permanently removed.
Are you sure? (y/n) y
DROP ROLE joe;
```

## Veja também

[criarusuário](app-createuser.md "createuser"), [DROP ROLE](sql-droprole.md "DROP ROLE")