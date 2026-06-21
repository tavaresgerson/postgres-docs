## pg_isready

pg_isready — Verifique o status de conexão de um servidor PostgreSQL

## Sinopse

`pg_isready` [*`connection-option`*...] [*`option`*...]

## Descrição

pg_isready é uma ferramenta para verificar o estado de conexão de um servidor de banco de dados PostgreSQL. O status de saída especifica o resultado da verificação de conexão.

## Opções

`-d dbname` `--dbname=dbname`: Especifica o nome do banco de dados a ser conectado. O *`dbname`* pode ser uma [string de conexão][(libpq-connect.md#LIBPQ-CONNSTRING "32.1.1. Connection Strings")]. Se assim for, os parâmetros da string de conexão substituirão quaisquer opções de linha de comando conflitantes.

`-h hostname`: Especifica o nome do host da máquina em que o servidor está sendo executado. Se o valor começar com uma barra, ele é usado como o diretório para o socket de domínio Unix. `--host=hostname`: Especifica o nome do host da máquina em que o servidor está sendo executado. Se o valor começar com uma barra, ele é usado como o diretório para o socket de domínio Unix.

`-p port` `--port=port`: Especifica a porta TCP ou a extensão de arquivo de soquete de domínio Unix local em que o servidor está aguardando conexões. Tem como padrão o valor da variável de ambiente `PGPORT` ou, se não for definida, a porta especificada no momento da compilação, geralmente 5432.

`-q` `--quiet`: Não exiba a mensagem de status. Isso é útil ao escrever scripts.

`-t seconds` `--timeout=seconds`: O número máximo de segundos para esperar ao tentar a conexão antes de retornar que o servidor não está respondendo. Definindo 0 desativa. O padrão é 3 segundos.

`-U username` `--username=username`: Conecte-se ao banco de dados como o usuário *`username`* em vez do padrão.

`-V` `--version`: Imprimir a versão do pg_isready e sair.

`-?` `--help`: Mostrar ajuda sobre os argumentos da linha de comando do comando pg_isready e sair.

## Status de saída

pg_isready retorna `0` para o shell se o servidor estiver aceitando conexões normalmente, `1` se o servidor estiver rejeitando conexões (por exemplo, durante o início), `2` se não houve resposta à tentativa de conexão, e `3` se não foi feita nenhuma tentativa (por exemplo, devido a parâmetros inválidos).

## Meio Ambiente

`pg_isready`, como a maioria das outras utilidades do PostgreSQL, também utiliza as variáveis de ambiente suportadas pelo libpq (consulte a Seção 32.15 (libpq-envars.md "32.15. Environment Variables")).

A variável de ambiente `PG_COLOR` especifica se a cor deve ser usada nas mensagens de diagnóstico. Os valores possíveis são `always`, `auto` e `never`.

## Notas

Não é necessário fornecer os valores corretos para nome de usuário, senha ou nome do banco de dados para obter o status do servidor; no entanto, se valores incorretos forem fornecidos, o servidor registrará uma tentativa de conexão falhada.

## Exemplos

Uso padrão:

```
$ pg_isready
/tmp:5432 - accepting connections
$ echo $?
0
```

Executando com parâmetros de conexão em um clúster PostgreSQL na inicialização:

```
$ pg_isready -h localhost -p 5433
localhost:5433 - rejecting connections
$ echo $?
1
```

Executando com parâmetros de conexão em um clúster PostgreSQL não responsivo:

```
$ pg_isready -h someremotehost
someremotehost:5432 - no response
$ echo $?
2
```
