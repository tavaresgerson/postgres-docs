## pg_controldata

pg_controldata — exibe informações de controle de um clúster de banco de dados PostgreSQL

## Sinopse

`pg_controldata` [*`option`*] [[ `-D` | `--pgdata` ]*`datadir`*]

## Descrição

`pg_controldata` imprime informações iniciadas durante `initdb`, como a versão do catálogo. Também exibe informações sobre o registro prévio de escrita e o processamento de pontos de verificação. Essas informações são globais para o clúster e não são específicas para nenhum banco de dados.

Este utilitário só pode ser executado pelo usuário que iniciou o clúster, pois requer acesso de leitura ao diretório de dados. Você pode especificar o diretório de dados na linha de comando ou usar a variável de ambiente `PGDATA`. Este utilitário suporta as opções `-V` e `--version`, que imprimem a versão do pg_controldata e saem. Também suporta as opções `-?` e `--help`, que exibem os argumentos suportados.

## Meio Ambiente

`PGDATA`: Local padrão do diretório de dados

`PG_COLOR`: Especifica se a cor deve ser usada em mensagens de diagnóstico. Os valores possíveis são `always`, `auto` e `never`.