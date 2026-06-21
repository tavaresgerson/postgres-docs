## 70.1. Mantido de backup do objeto de nível superior [#](#BACKUP-MANIFEST-TOPLEVEL)

O documento JSON de mantimento de backup contém as seguintes chaves.

`PostgreSQL-Backup-Manifest-Version`: O valor associado é um número inteiro. A partir do PostgreSQL `17`, é `2`; em versões mais antigas, é `1`.

`System-Identifier`: O identificador do sistema de banco de dados da instância do PostgreSQL onde o backup foi feito. Este campo está presente apenas quando `PostgreSQL-Backup-Manifest-Version` é `2`.

`Files`: O valor associado é sempre uma lista de objetos, cada um descrevendo um arquivo presente no backup. Não há entradas nesta lista para os arquivos WAL que são necessários para usar o backup, ou para o próprio backup. A estrutura de cada objeto na lista é descrita em [Seção 70.2](backup-manifest-files.md).

`WAL-Ranges`: O valor associado é sempre uma lista de objetos, cada um descrevendo uma faixa de registros WAL que devem ser legíveis de um determinado período temporal a fim de fazer uso do backup. A estrutura desses objetos é descrita mais detalhadamente em [Seção 70.3](backup-manifest-wal-ranges.md).

`Manifest-Checksum`: Esta chave está sempre presente na última linha do arquivo de manifesto de backup. O valor associado é um checksum SHA-256 de todas as linhas anteriores. Usamos um método de checksum fixo aqui para permitir que os clientes realizem uma análise incremental do manifesto. Embora um checksum SHA-256 seja significativamente mais caro do que um checksum CRC-32C, o manifesto normalmente deve ser pequeno o suficiente para que a computação extra não importe muito.