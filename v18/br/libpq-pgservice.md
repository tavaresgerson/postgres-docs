## 32.17. O arquivo de serviço de conexão [#](#LIBPQ-PGSERVICE)

O arquivo de serviço de conexão permite que os parâmetros de conexão do libpq sejam associados a um único nome de serviço. Esse nome de serviço pode então ser especificado usando a palavra-chave `service` em uma string de conexão do libpq, e as configurações associadas serão usadas. Isso permite que os parâmetros de conexão sejam modificados sem exigir uma recompilação do aplicativo que usa o libpq. O nome do serviço também pode ser especificado usando a variável de ambiente `PGSERVICE`.

Os nomes dos serviços podem ser definidos em um arquivo de serviço por usuário ou em um arquivo para todo o sistema. Se o mesmo nome de serviço existir tanto no arquivo do usuário quanto no arquivo do sistema, o arquivo do usuário terá precedência. Por padrão, o arquivo de serviço por usuário é denominado `~/.pg_service.conf`. No Microsoft Windows, é denominado `%APPDATA%\postgresql\.pg_service.conf` (onde `%APPDATA%` se refere ao subdiretório de Dados da Aplicação no perfil do usuário). Um nome de arquivo diferente pode ser especificado definindo a variável de ambiente `PGSERVICEFILE`. O arquivo para todo o sistema é denominado `pg_service.conf`. Por padrão, ele é procurado no diretório `etc` da instalação do PostgreSQL (use `pg_config --sysconfdir` para identificar esse diretório com precisão). Outro diretório, mas não um nome de arquivo diferente, pode ser especificado definindo a variável de ambiente `PGSYSCONFDIR`.

Qualquer um dos arquivos de serviço usa um formato de arquivo "INI", onde o nome da seção é o nome do serviço e os parâmetros são os parâmetros de conexão; consulte [Seção 32.1.2] para uma lista. Por exemplo:

```
# comment
[mydb]
host=somehost
port=5433
user=admin
```

Um exemplo de arquivo é fornecido na instalação do PostgreSQL em `share/pg_service.conf.sample`.

Os parâmetros de conexão obtidos de um arquivo de serviço são combinados com os parâmetros obtidos de outras fontes. Um ajuste do arquivo de serviço substitui a variável de ambiente correspondente e, por sua vez, pode ser substituído por um valor fornecido diretamente na cadeia de conexão. Por exemplo, usando o arquivo de serviço acima, uma cadeia de conexão `service=mydb port=5434` usará o host `somehost`, a porta `5434`, o usuário `admin` e outros parâmetros definidos por variáveis de ambiente ou padrões internos.