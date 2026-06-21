## initdb

initdb — criar um novo clúster de banco de dados PostgreSQL

## Sinopse

`initdb` [*`option`*...] [ `--pgdata` | `-D` ] *`directory`*

## Descrição

`initdb` cria um novo PostgreSQL [*[database cluster](glossary.md#GLOSSARY-DB-CLUSTER "Database cluster")*](glossário.md#GLOSSARY-DB-CLUSTER).

Criar um clúster de banco de dados consiste em criar os [*[diretórios](glossary.md#GLOSSARY-DATA-DIRECTORY "Data directory")*](glossary.md#GLOSSARY-DATA-DIRECTORY) nos quais os dados do clúster serão armazenados, gerar as tabelas de catálogo compartilhadas (tabelas que pertencem a todo o clúster e não a nenhum banco de dados específico) e criar os bancos de dados `postgres`, `template1` e `template0`. O banco de dados `postgres` é um banco de dados padrão destinado ao uso por usuários, utilitários e aplicativos de terceiros. `template1` e `template0` são destinados como bancos de dados de origem que serão copiados por comandos posteriores do `CREATE DATABASE`. `template0` nunca deve ser modificado, mas você pode adicionar objetos ao `template1`, que, por padrão, serão copiados em bancos de dados criados posteriormente. Consulte [Seção 22.3](manage-ag-templatedbs.md "22.3. Template Databases") para obter mais detalhes.

Embora o `initdb` tente criar o diretório de dados especificado, ele pode não ter permissão se o diretório pai do diretório de dados desejado for de propriedade do root. Para inicializar em tal configuração, crie um diretório de dados vazio como root, em seguida, use o `chown` para atribuir a propriedade desse diretório à conta de usuário do banco de dados, em seguida, use o `su` para se tornar o usuário do banco de dados que executará o `initdb`.

`initdb` deve ser executado como o usuário que possuirá o processo do servidor, porque o servidor precisa ter acesso aos arquivos e diretórios que o `initdb` cria. Como o servidor não pode ser executado como root, você não deve executar `initdb` como root também. (De fato, ele se recusará a fazer isso.)

Por razões de segurança, o novo grupo criado por `initdb` será acessível apenas pelo proprietário do grupo por padrão. A opção `--allow-group-access` permite que qualquer usuário no mesmo grupo que o proprietário do grupo leia arquivos no grupo. Isso é útil para realizar backups como um usuário não privilegiado.

`initdb` inicializa o idioma padrão e o conjunto de codificação de caracteres do clúster de banco de dados. Esses valores também podem ser definidos separadamente para cada banco de dados quando ele é criado. `initdb` determina esses ajustes para os bancos de modelo, que servirão como padrão para todos os outros bancos.

Por padrão, o `initdb` utiliza o provedor de localização `libc` (consulte [Seção 23.1.4][(locale.md#LOCALE-PROVIDERS "23.1.4. Locale Providers")]). O provedor de localização `libc` obtém as configurações de localização do ambiente e determina o codificação a partir das configurações de localização.

Para escolher um local diferente para o clúster, use a opção `--locale`. Também existem opções individuais `--lc-*` e `--icu-locale` (veja abaixo) para definir valores para as categorias individuais de local. Observe que configurações inconsistentes para diferentes categorias de local podem gerar resultados sem sentido, portanto, isso deve ser usado com cuidado.

Alternativamente, `initdb` pode usar a biblioteca ICU para fornecer serviços de localização, especificando `--locale-provider=icu`. O servidor deve ser construído com suporte ao ICU. Para escolher o ID específico de localização ICU a ser aplicado, use a opção `--icu-locale`. Note que, por razões de implementação e para suportar código legítimo, `initdb` ainda selecionará e inicializará as configurações de localização da libc quando o provedor de localização ICU for usado.

Quando o `initdb` for executado, ele imprimirá as configurações de localização que ele escolheu. Se você tiver requisitos complexos ou especificou várias opções, é aconselhável verificar se o resultado corresponde ao que foi planejado.

Mais detalhes sobre as configurações de localização podem ser encontrados em [Seção 23.1][(locale.md "23.1. Locale Support")].

Para alterar o codificação padrão, use o `--encoding`. Mais detalhes podem ser encontrados em [Seção 23.3][(multibyte.md "23.3. Character Set Support")].

## Opções

`-A authmethod` `--auth=authmethod` [#](#APP-INITDB-OPTION-AUTH): Esta opção especifica o método de autenticação padrão para usuários locais usados em `pg_hba.conf` (linhas `host` e `local`). Consulte [Seção 20.1](auth-pg-hba-conf.md "20.1. The pg_hba.conf File") para uma visão geral dos valores válidos.

`initdb` preenchirá as entradas de `pg_hba.conf` usando o método de autenticação especificado para conexões de não-replicação, bem como para conexões de replicação.

Não use `trust` a menos que confie em todos os usuários locais do seu sistema. `trust` é o padrão para facilidade de instalação.

`--auth-host=authmethod` [#](#APP-INITDB-OPTION-AUTH-HOST): Esta opção especifica o método de autenticação para usuários locais através de conexões TCP/IP utilizadas em `pg_hba.conf` (linhas `host`).

`--auth-local=authmethod` [#](#APP-INITDB-OPTION-AUTH-LOCAL): Esta opção especifica o método de autenticação para usuários locais através de conexões de soquete de domínio Unix usadas em `pg_hba.conf` (linhas `local`).

`-D directory` `--pgdata=directory` [#](#APP-INITDB-OPTION-PGDATA): Esta opção especifica o diretório onde o cluster de banco de dados deve ser armazenado. Esta é a única informação exigida por `initdb`, mas você pode evitar escrevê-la definindo a variável de ambiente `PGDATA`, o que pode ser conveniente, uma vez que o servidor de banco de dados (`postgres`) pode encontrar o diretório de dados mais tarde pela mesma variável.

`-E encoding` `--encoding=encoding` [#](#APP-INITDB-OPTION-ENCODING): Seleciona o codificação dos bancos de dados de modelo. Isso também será o codificação padrão de qualquer banco de dados que você criar posteriormente, a menos que você o sobrecarregue. Os conjuntos de caracteres suportados pelo servidor PostgreSQL são descritos em [Seção 23.3.1](multibyte.md#MULTIBYTE-CHARSET-SUPPORTED "23.3.1. Supported Character Sets").

Por padrão, o codificação do banco de dados do modelo é derivada do local. Se `--no-locale` (app-initdb.md#APP-INITDB-OPTION-NO-LOCALE) for especificado (ou, de forma equivalente, se o local for `C` ou `POSIX`, então o padrão é `UTF8` para o provedor de UTI e `SQL_ASCII` para o provedor de `libc`.

`-g` `--allow-group-access` [#](#APP-INITDB-ALLOW-GROUP-ACCESS): Permite que os usuários no mesmo grupo que o proprietário do clúster leiam todos os arquivos do clúster criados por `initdb`. Esta opção é ignorada no Windows, pois não suporta permissões de grupo no estilo POSIX.

`--icu-locale=locale` [#](#APP-INITDB-ICU-LOCALE): Especifica o local do ICU quando o provedor de ICU é usado. O suporte ao local é descrito em [Seção 23.1](locale.md "23.1. Locale Support").

`--icu-rules=rules` [#](#APP-INITDB-ICU-RULES): Especifica regras de ordenação adicionais para personalizar o comportamento da ordenação padrão. Isso é suportado apenas para ICU.

`-k` `--data-checksums` [#](#APP-INITDB-DATA-CHECKSUMS): Use verificações de checksums nas páginas de dados para ajudar a detectar corrupção pelo sistema de E/S que, de outra forma, seria silencioso. Isso é ativado por padrão; use [`--no-data-checksums`](app-initdb.md#APP-INITDB-NO-DATA-CHECKSUMS) para desativar as verificações de checksums.

A ativação de verificações de checksum pode resultar em uma pequena penalização de desempenho. Se configurada, as verificações de checksum são calculadas para todos os objetos, em todos os bancos de dados. Todos os falhos de verificação de checksum serão relatados na visão `pg_stat_database`(monitoring-stats.md#MONITORING-PG-STAT-DATABASE-VIEW "27.2.17. pg_stat_database"). Consulte [Seção 28.2](checksums.md "28.2. Data Checksums") para obter detalhes.

`--locale=locale` [#](#APP-INITDB-OPTION-LOCALE): Define o local padrão para o clúster de banco de dados. Se esta opção não for especificada, o local é herdado do ambiente em que o `initdb` é executado. O suporte ao local é descrito em [Seção 23.1](locale.md "23.1. Locale Support").

Se `--locale-provider` for `builtin`, `--locale` ou `--builtin-locale`, deve ser especificado e ajustado para `C`, `C.UTF-8` ou `PG_UNICODE_FAST`.

`--lc-collate=locale` `--lc-ctype=locale` `--lc-messages=locale` `--lc-monetary=locale` `--lc-numeric=locale` `--lc-time=locale` [#](#APP-INITDB-OPTION-LC-COLLATE): Assim como `--locale`, mas apenas define o local na categoria especificada.

`--no-locale` [#](#APP-INITDB-OPTION-NO-LOCALE): Equivalente a `--locale=C`.

`--builtin-locale=locale` [#](#APP-INITDB-BUILTIN-LOCALE): Especifica o nome do local quando o provedor incorporado é usado. O suporte ao local é descrito em [Seção 23.1](locale.md "23.1. Locale Support").

`--locale-provider={builtin|libc|icu}` [#](#APP-INITDB-OPTION-LOCALE-PROVIDER): Esta opção define o provedor de localização para bancos de dados criados no novo clúster. Pode ser sobrescrita no comando `CREATE DATABASE` quando novos bancos de dados são posteriormente criados. O padrão é `libc` (consulte [Seção 23.1.4](locale.md#LOCALE-PROVIDERS "23.1.4. Locale Providers")).

`--no-data-checksums` [#](#APP-INITDB-NO-DATA-CHECKSUMS): Não habilite os checksums de dados.

`--pwfile=filename` [#](#APP-INITDB-OPTION-PWFILE): Faz com que `initdb` leia a senha do superusuário de bootstrap a partir de um arquivo. A primeira linha do arquivo é considerada como a senha.

`-T config` `--text-search-config=config` [#](#APP-INITDB-OPTION-TEXT-SEARCH-CONFIG): Define a configuração padrão de pesquisa de texto. Consulte [configuração_de_pesquisa_de_texto_padrão](runtime-config-client.md#GUC-DEFAULT-TEXT-SEARCH-CONFIG) para obter mais informações.

`-U username` `--username=username` [#](#APP-INITDB-OPTION-USERNAME): Define o nome do usuário do [*[bootstrap superuser](glossary.md#GLOSSARY-BOOTSTRAP-SUPERUSER "Bootstrap superuser")*](glossário.md#GLOSSARY-BOOTSTRAP-SUPERUSER). Este valor padrão é o nome do usuário do sistema operacional que está executando `initdb`.

`-W` `--pwprompt` [#](#APP-INITDB-OPTION-PWPROMPT): Faz com que o `initdb` solicite uma senha para dar o superusuário de inicialização. Se você não planeja usar autenticação por senha, isso não é importante. Caso contrário, você não poderá usar autenticação por senha até que uma senha seja configurada.

`-X directory` `--waldir=directory` [#](#APP-INITDB-OPTION-WALDIR): Esta opção especifica o diretório onde o log de pré-escrita deve ser armazenado.

`--wal-segsize=size` [#](#APP-INITDB-OPTION-WAL-SEGSIZE): Defina o tamanho do *WAL*, em megabytes. Este é o tamanho de cada arquivo individual no log WAL. O tamanho padrão é de 16 megabytes. O valor deve ser um número de potência de 2 entre 1 e 1024 (megabytes). Esta opção só pode ser definida durante a inicialização e não pode ser alterada posteriormente.

Pode ser útil ajustar esse tamanho para controlar a granularidade do envio ou arquivamento do log WAL. Além disso, em bancos de dados com um alto volume de WAL, o número elevado de arquivos WAL por diretório pode se tornar um problema de desempenho e gerenciamento. Aumentar o tamanho do arquivo WAL reduzirá o número de arquivos WAL.

Outras opções, menos usadas, também estão disponíveis:

`-c name=value` `--set name=value` [#](#APP-INITDB-OPTION-SET): Ajuste o parâmetro do servidor *`name`* à força para *`value`* durante `initdb`, e também instale esse ajuste no arquivo gerado `postgresql.conf`, para que ele seja aplicado durante futuras execuções do servidor. Esta opção pode ser dada mais de uma vez para definir vários parâmetros. É principalmente útil quando o ambiente é tal que o servidor não será iniciado de forma alguma usando os parâmetros padrão.

`-d` `--debug` [#](#APP-INITDB-OPTION-DEBUG): Imprimir a saída de depuração do backend de bootstrap e algumas outras mensagens de menor interesse para o público em geral. O backend de bootstrap é o programa que o `initdb` usa para criar as tabelas do catálogo. Esta opção gera uma quantidade enorme de saída extremamente entediante.

`--discard-caches` [#](#APP-INITDB-OPTION-DISCARD-CACHES): Execute o backend de bootstrap com a opção `debug_discard_caches=1`. Isso leva muito tempo e é útil apenas para depuração profunda.

`-L directory` [#](#APP-INITDB-OPTION-L): Especifica onde o `initdb` deve encontrar seus arquivos de entrada para inicializar o clúster do banco de dados. Normalmente, isso não é necessário. Você será informado se você precisa especificar explicitamente sua localização.

`-n` `--no-clean` [#](#APP-INITDB-OPTION-NO-CLEAN): Por padrão, quando o `initdb` determina que um erro impediu que ele criasse completamente o grupo de bancos de dados, ele remove quaisquer arquivos que ele possa ter criado antes de descobrir que não pode completar o trabalho. Esta opção inibe a limpeza e, portanto, é útil para depuração.

`-N` `--no-sync` [#](#APP-INITDB-OPTION-NO-SYNC): Por padrão, `initdb` aguardará que todos os arquivos sejam escritos com segurança no disco. Esta opção faz com que `initdb` retorne sem aguardar, o que é mais rápido, mas significa que um posterior falha do sistema operacional pode deixar o diretório de dados corrompido. Geralmente, esta opção é útil para testes, mas não deve ser usada ao criar uma instalação de produção.

`--no-sync-data-files` [#](#APP-INITDB-OPTION-NO-SYNC-DATA-FILES): Por padrão, `initdb` escreve todos os arquivos do banco de dados em disco de forma segura. Esta opção instrui `initdb` a ignorar a sincronização de todos os arquivos nos diretórios individuais do banco de dados, os próprios diretórios do banco de dados e os diretórios do tablespace, ou seja, tudo no subdiretório `base` e quaisquer outros diretórios do tablespace. Outros arquivos, como os de `pg_wal` e `pg_xact`, ainda serão sincronizados, a menos que a opção `--no-sync` também seja especificada.

Observe que, se o `--no-sync-data-files` for usado em conjunto com o `--sync-method=syncfs`, alguns ou todos os arquivos e diretórios mencionados anteriormente serão sincronizados, pois o `syncfs` processa sistemas de arquivos inteiros.

Esta opção é destinada principalmente para uso interno por ferramentas que garantem separadamente que os arquivos ignorados sejam sincronizados no disco.

`--no-instructions` [#](#APP-INITDB-OPTION-NO-INSTRUCTIONS): Por padrão, `initdb` escreverá instruções sobre como iniciar o clúster no final de sua saída. Esta opção faz com que essas instruções sejam ignoradas. Isso é destinado principalmente para uso de ferramentas que envolvem `initdb` em comportamento específico da plataforma, onde essas instruções provavelmente serão incorretas.

`-s` `--show` [#](#APP-INITDB-OPTION-SHOW): Mostrar configurações internas e sair, sem fazer nada mais. Isso pode ser usado para depurar a instalação do initdb.

`--sync-method=method` [#](#APP-INITDB-OPTION-SYNC-METHOD): Quando configurado para `fsync`, que é o padrão, `initdb` abrirá e sincronizará recursivamente todos os arquivos no diretório de dados. A busca por arquivos seguirá links simbólicos para o diretório WAL e cada espaço de tabela configurado.

Em Linux, `syncfs` pode ser usado para pedir ao sistema operacional que sincronize todos os sistemas de arquivos que contêm o diretório de dados, os arquivos WAL e cada espaço de tabela. Consulte [recovery_init_sync_method][(runtime-config-error-handling.md#GUC-RECOVERY-INIT-SYNC-METHOD)] para obter informações sobre as advertências a serem observadas ao usar `syncfs`.

Esta opção não tem efeito quando o `--no-sync` é utilizado.

`-S` `--sync-only` [#](#APP-INITDB-OPTION-SYNC-ONLY): Escreva todos os arquivos do banco de dados com segurança no disco e saia. Esta opção não realiza nenhuma das operações normais do initdb. Geralmente, esta opção é útil para garantir uma recuperação confiável após a mudança de [fsync](runtime-config-wal.md#GUC-FSYNC) de `off` para `on`.

Outras opções:

`-V` `--version` [#](#APP-INITDB-OPTION-VERSION): Imprimir a versão do initdb e sair.

`-?` `--help` [#](#APP-INITDB-OPTION-HELP): Mostrar ajuda sobre os argumentos da linha de comando do comando initdb e sair.

## Meio Ambiente

`PGDATA` [#](#APP-INITDB-ENVIRONMENT-PGDATA): Especifica o diretório onde o clúster do banco de dados deve ser armazenado; pode ser sobrescrito usando a opção `-D`.

`PG_COLOR` [#](#APP-INITDB-ENVIRONMENT-PG-COLOR): Especifica se a cor deve ser usada em mensagens de diagnóstico. Os valores possíveis são `always`, `auto` e `never`.

`TZ` [#](#APP-INITDB-ENVIRONMENT-TZ): Especifica o fuso horário padrão do clúster de banco de dados criado. O valor deve ser um nome completo de fuso horário (consulte [Seção 8.5.3](datatype-datetime.md#DATATYPE-TIMEZONES "8.5.3. Time Zones")).

## Notas

`initdb` também pode ser invocado através de `pg_ctl initdb`.

## Veja também

[pg_ctl](app-pg-ctl.md "pg_ctl"), [postgres](app-postgres.md "postgres"), [Seção 20.1](auth-pg-hba-conf.md "20.1. The pg_hba.conf File")