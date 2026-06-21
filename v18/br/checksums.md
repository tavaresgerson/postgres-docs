## 28.2. Verificação de checksums de dados [#](#CHECKSUMS)

* [28.2.1. Habilitação de checksums off-line](checksums.md#CHECKSUMS-OFFLINE-ENABLE-DISABLE)

Por padrão, as páginas de dados são protegidas por verificações de checksum, mas isso pode ser desativado opcionalmente para um clúster. Quando ativado, cada página de dados inclui um checksum que é atualizado quando a página é escrita e verificado cada vez que a página é lida. Apenas as páginas de dados são protegidas por verificações de checksum; as estruturas de dados internas e os arquivos temporários não são.

Os checksums podem ser desativados quando o clúster é inicializado usando [initdb][(app-initdb.md#APP-INITDB-DATA-CHECKSUMS)]. Eles também podem ser ativados ou desativados posteriormente como uma operação off-line. Os checksums de dados são ativados ou desativados no nível completo do clúster e não podem ser especificados individualmente para bancos de dados ou tabelas.

O estado atual dos checksums no clúster pode ser verificado ao visualizar o valor da variável de configuração somente de leitura [data_checksums](runtime-config-preset.md#GUC-DATA-CHECKSUMS) executando o comando `SHOW data_checksums`.

Ao tentar recuperar de corrupções de página, pode ser necessário contornar a proteção de verificação de checksum. Para fazer isso, defina temporariamente o parâmetro de configuração [ignore_checksum_failure][(runtime-config-developer.md#GUC-IGNORE-CHECKSUM-FAILURE)].

### 28.2.1. Habilitação de checksums off-line [#](#CHECKSUMS-OFFLINE-ENABLE-DISABLE)

O aplicativo [pg_checksums][(app-pgchecksums.md "pg_checksums")] pode ser usado para habilitar ou desabilitar verificações de checksum de dados, bem como para verificar verificações de checksum, em um clúster offline.