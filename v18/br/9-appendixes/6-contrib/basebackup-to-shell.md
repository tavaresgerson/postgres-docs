## F.4. basebackup_to_shell — exemplo de módulo "shell" pg_basebackup [#](#BASEBACKUP-TO-SHELL)

* [F.4.1. Parâmetros de Configuração](basebackup-to-shell.md#BASEBACKUP-TO-SHELL-CONFIGURATION-PARAMETERS)
* [F.4.2. Autor](basebackup-to-shell.md#BASEBACKUP-TO-SHELL-AUTHOR)

`basebackup_to_shell` adiciona um alvo de basebackup personalizado chamado `shell`. Isso permite executar `pg_basebackup --target=shell` ou, dependendo da configuração deste módulo, `pg_basebackup --target=shell:DETAIL_STRING`, e fazer com que um comando do servidor escolhido pelo administrador do servidor seja executado para cada arquivo tar gerado pelo processo de backup. O comando receberá o conteúdo do arquivo através da entrada padrão.

Este módulo é destinado principalmente como um exemplo de como criar novos alvos de backup através de um módulo de extensão, mas, em alguns cenários, pode ser útil por si só. Para funcionar, este módulo deve ser carregado através de [shared_preload_libraries](runtime-config-client.md#GUC-SHARED-PRELOAD-LIBRARIES) ou [local_preload_libraries](runtime-config-client.md#GUC-LOCAL-PRELOAD-LIBRARIES).

### F.4.1. Parâmetros de Configuração [#](#BASEBACKUP-TO-SHELL-CONFIGURATION-PARAMETERS)

`basebackup_to_shell.command` (`string`): O comando que o servidor deve executar para cada arquivo gerado pelo processo de backup. Se `%f` ocorrer na string de comando, ele será substituído pelo nome do arquivo (por exemplo, `base.tar`). Se `%d` ocorrer na string de comando, ele será substituído pelo detalhe do alvo fornecido pelo usuário. Um detalhe do alvo é necessário se `%d` for usado na string de comando, e é proibido caso contrário. Por razões de segurança, ele pode conter apenas caracteres alfanuméricos. Se `%%` ocorrer na string de comando, ele será substituído por um único `%`. Se `%` ocorrer na string de comando seguido por qualquer outro caractere ou no final da string, ocorre um erro.

`basebackup_to_shell.required_role` (`string`): O papel necessário para fazer uso do alvo de backup `shell`. Se este não for definido, qualquer usuário de replicação pode fazer uso do alvo de backup `shell`.

### F.4.2. Autor [#](#BASEBACKUP-TO-SHELL-AUTHOR)

Robert Haas `<rhaas@postgresql.org>`