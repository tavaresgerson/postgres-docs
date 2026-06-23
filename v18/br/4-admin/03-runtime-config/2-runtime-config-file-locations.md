## 19.2. Localização dos arquivos [#](#RUNTIME-CONFIG-FILE-LOCATIONS)

Além do arquivo `postgresql.conf` já mencionado, o PostgreSQL usa outros dois arquivos de configuração editados manualmente, que controlam a autenticação do cliente (seu uso é discutido em [Capítulo 20](client-authentication.md)). Por padrão, todos os três arquivos de configuração são armazenados no diretório de dados do clúster do banco de dados. Os parâmetros descritos nesta seção permitem que os arquivos de configuração sejam colocados em outros lugares. (Fazer isso pode facilitar a administração. Em particular, é frequentemente mais fácil garantir que os arquivos de configuração sejam devidamente protegidos quando eles são mantidos separados.)

`data_directory` (`string`) [#](#GUC-DATA-DIRECTORY): Especifica o diretório a ser usado para armazenamento de dados. Este parâmetro só pode ser definido no início do servidor.

`config_file` (`string`) [#](#GUC-CONFIG-FILE): Especifica o arquivo de configuração principal do servidor (comumente chamado `postgresql.conf`). Este parâmetro só pode ser definido na linha de comando do comando `postgres`.

`hba_file` (`string`) [#](#GUC-HBA-FILE): Especifica o arquivo de configuração para autenticação baseada em host (comumente chamada `pg_hba.conf`). Este parâmetro só pode ser definido no início do servidor.

`ident_file` (`string`) [#](#GUC-IDENT-FILE): Especifica o arquivo de configuração para mapeamento de nome de usuário (comumente chamado `pg_ident.conf`). Este parâmetro só pode ser definido no início do servidor. Veja também [Seção 20.2](auth-username-maps.md "20.2. User Name Maps").

`external_pid_file` (`string`) [#](#GUC-EXTERNAL-PID-FILE): Especifica o nome de um arquivo de ID de processo adicional (PID) que o servidor deve criar para uso por programas de administração do servidor. Este parâmetro só pode ser definido na inicialização do servidor.

Em uma instalação padrão, nenhum dos parâmetros acima é definido explicitamente. Em vez disso, o diretório de dados é especificado pela opção de linha de comando `-D` ou pela variável de ambiente `PGDATA`, e os arquivos de configuração são encontrados dentro do diretório de dados.

Se você deseja manter os arquivos de configuração em outro local que não o diretório de dados, a opção de linha de comando `postgres` ou a variável de ambiente `-D` deve apontar para o diretório que contém os arquivos de configuração, e o parâmetro `data_directory` deve ser definido em `postgresql.conf` (ou na linha de comando) para mostrar onde o diretório de dados está realmente localizado. Observe que `data_directory` substitui `-D` e `PGDATA` para a localização do diretório de dados, mas não para a localização dos arquivos de configuração.

Se desejar, pode especificar os nomes e locais dos arquivos de configuração individualmente usando os parâmetros `config_file`, `hba_file` e/ou `ident_file`. `config_file` só pode ser especificado na linha de comando do comando `postgres`, mas os outros podem ser definidos no arquivo de configuração principal. Se todos os três parâmetros, além de `data_directory`, forem explicitamente definidos, então não é necessário especificar `-D` ou `PGDATA`.

Ao definir qualquer um desses parâmetros, um caminho relativo será interpretado em relação ao diretório em que o `postgres` é iniciado.