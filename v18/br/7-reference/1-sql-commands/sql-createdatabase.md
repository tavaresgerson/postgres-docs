## CRIAR BANCO DE DADOS

CREATE DATABASE — criar um novo banco de dados

## Sinopse

```
CREATE DATABASE name
    [ WITH ] [ OWNER [=] user_name ]
           [ TEMPLATE [=] template ]
           [ ENCODING [=] encoding ]
           [ STRATEGY [=] strategy ]
           [ LOCALE [=] locale ]
           [ LC_COLLATE [=] lc_collate ]
           [ LC_CTYPE [=] lc_ctype ]
           [ BUILTIN_LOCALE [=] builtin_locale ]
           [ ICU_LOCALE [=] icu_locale ]
           [ ICU_RULES [=] icu_rules ]
           [ LOCALE_PROVIDER [=] locale_provider ]
           [ COLLATION_VERSION = collation_version ]
           [ TABLESPACE [=] tablespace_name ]
           [ ALLOW_CONNECTIONS [=] allowconn ]
           [ CONNECTION LIMIT [=] connlimit ]
           [ IS_TEMPLATE [=] istemplate ]
           [ OID [=] oid ]
```

## Descrição

`CREATE DATABASE` cria um novo banco de dados PostgreSQL.

Para criar um banco de dados, você deve ser um superusuário ou ter o privilégio especial `CREATEDB`. Veja [CREATE ROLE](sql-createrole.md "CREATE ROLE").

Por padrão, o novo banco de dados será criado clonando o banco de dados padrão do sistema `template1`. Um modelo diferente pode ser especificado escrevendo `TEMPLATE name`. Em particular, escrevendo `TEMPLATE template0`, você pode criar um banco de dados puro (um onde não existem objetos definidos pelo usuário e onde os objetos do sistema não foram alterados) contendo apenas os objetos padrão predefinidos pela sua versão do PostgreSQL. Isso é útil se você deseja evitar copiar quaisquer objetos locais da instalação que possam ter sido adicionados a `template1`.

## Parâmetros

*`name`* [#](#CREATE-DATABASE-NAME): O nome do banco de dados a ser criado.

*`user_name`* [#](#CREATE-DATABASE-USER-NAME): O nome do usuário que possuirá o novo banco de dados, ou `DEFAULT` para usar o padrão (ou seja, o usuário que executa o comando). Para criar um banco de dados possuído por outro usuário, você deve ser capaz de `SET ROLE` para esse usuário.

*`template`* [#](#CREATE-DATABASE-TEMPLATE): O nome do modelo a partir do qual se deseja criar o novo banco de dados, ou `DEFAULT` para usar o modelo padrão (`template1`).

*`encoding`* [#](#CREATE-DATABASE-ENCODING): Codificação do conjunto de caracteres a ser usada no novo banco de dados. Especifique uma constante de string (por exemplo, `'SQL_ASCII'`), um número de codificação de inteiro ou `DEFAULT` para usar a codificação padrão (ou seja, a codificação do banco de dados de modelo). Os conjuntos de caracteres suportados pelo servidor PostgreSQL são descritos em [Seção 23.3.1](multibyte.md#MULTIBYTE-CHARSET-SUPPORTED "23.3.1. Supported Character Sets"). Veja abaixo para restrições adicionais.

*`strategy`* [#](#CREATE-DATABASE-STRATEGY): Estratégia a ser utilizada na criação do novo banco de dados. Se a estratégia `WAL_LOG` for utilizada, o banco de dados será copiado bloco a bloco e cada bloco será escrito separadamente no log de pré-escrita. Esta é a estratégia mais eficiente em casos em que o banco de dados de modelo é pequeno, e, portanto, é a padrão. A estratégia mais antiga `FILE_COPY` também está disponível. Esta estratégia escreve um pequeno registro no log de pré-escrita para cada espaço de tabela utilizado pelo banco de dados-alvo. Cada registro representa a cópia de um diretório inteiro para um novo local no nível do sistema de arquivos. Embora isso reduza substancialmente o volume do log de pré-escrita, especialmente se o banco de dados de modelo for grande, também obriga o sistema a realizar um ponto de verificação antes e depois da criação do novo banco de dados. Em algumas situações, isso pode ter um impacto negativo perceptível no desempenho geral do sistema. A estratégia `FILE_COPY` é afetada pelo ajuste [file_copy_method](runtime-config-resource.md#GUC-FILE-COPY-METHOD).

*`locale`* [#](#CREATE-DATABASE-LOCALE): Define a ordem de classificação padrão e a classificação de caracteres no novo banco de dados. A classificação afeta a ordem de classificação aplicada a strings, por exemplo, em consultas com `ORDER BY`, bem como a ordem usada em índices em colunas de texto. A classificação de caracteres afeta a categorização de caracteres, como maiúsculas, minúsculas e dígitos. Também define os aspectos associados ao ambiente do sistema operacional, `LC_COLLATE` e `LC_CTYPE`. O padrão é o mesmo da base de dados de modelo. Consulte [Seção 23.2.2.3.1](collation.md#COLLATION-MANAGING-CREATE-LIBC "23.2.2.3.1. libc Collations") e [Seção 23.2.2.3.2](collation.md#COLLATION-MANAGING-CREATE-ICU "23.2.2.3.2. ICU Collations") para detalhes.

Pode ser substituído definindo [*`lc_collate`](sql-createdatabase.md#CREATE-DATABASE-LC-COLLATE), [*`lc_ctype`](sql-createdatabase.md#CREATE-DATABASE-LC-CTYPE), [*`builtin_locale`](sql-createdatabase.md#CREATE-DATABASE-BUILTIN-LOCALE), ou [*`icu_locale`](sql-createdatabase.md#CREATE-DATABASE-ICU-LOCALE) individualmente.

Se [*`locale_provider`](sql-createdatabase.md#CREATE-DATABASE-LOCALE-PROVIDER) é [[PH_LNK_49]], então *`builtin`* ou *`locale`* deve ser especificado e definido como `C`, `C.UTF-8` ou `PG_UNICODE_FAST`.

DICA

Os outros ajustes de localização [lc_messages](runtime-config-client.md#GUC-LC-MESSAGES), [lc_monetary](runtime-config-client.md#GUC-LC-MONETARY), [lc_numeric](runtime-config-client.md#GUC-LC-NUMERIC) e [lc_time](runtime-config-client.md#GUC-LC-TIME) não são fixos por banco de dados e não são definidos por este comando. Se você deseja torná-los padrão para um banco de dados específico, pode usar `ALTER DATABASE ... SET`.

*`lc_collate`* [#](#CREATE-DATABASE-LC-COLLATE): Define `LC_COLLATE` no ambiente do sistema operacional do servidor de banco de dados. O padrão é a configuração de [*`locale`](sql-createdatabase.md#CREATE-DATABASE-LOCALE) se especificada, caso contrário, a mesma configuração que o banco de dados de modelo. Veja abaixo as restrições adicionais.

Se [*`locale_provider`*](sql-createdatabase.md#CREATE-DATABASE-LOCALE-PROVIDER) for `libc`, também define a ordem de ordenação predefinida a ser usada no novo banco de dados, substituindo a configuração [*`locale`*](sql-createdatabase.md#CREATE-DATABASE-LOCALE).

*`lc_ctype`* [#](#CREATE-DATABASE-LC-CTYPE): Define `LC_CTYPE` no ambiente do sistema operacional do servidor de banco de dados. O padrão é a configuração de [*`locale`](sql-createdatabase.md#CREATE-DATABASE-LOCALE) se especificada, caso contrário, a mesma configuração que o banco de dados de modelo. Veja abaixo as restrições adicionais.

Se [*`locale_provider`](sql-createdatabase.md#CREATE-DATABASE-LOCALE-PROVIDER) for `libc`, também define a classificação de caracteres padrão a ser usada no novo banco de dados, substituindo a configuração [*`locale`](sql-createdatabase.md#CREATE-DATABASE-LOCALE).

*`builtin_locale`* [#](#CREATE-DATABASE-BUILTIN-LOCALE): Especifica o localizador do provedor incorporado para a ordem de classificação padrão do banco de dados e classificação de caracteres, substituindo a configuração [*`locale`*](sql-createdatabase.md#CREATE-DATABASE-LOCALE). O [localizador de provedor](sql-createdatabase.md#CREATE-DATABASE-LOCALE-PROVIDER) deve ser `builtin`. A configuração padrão é a do [*`locale`*](sql-createdatabase.md#CREATE-DATABASE-LOCALE) se especificada; caso contrário, a mesma configuração que o banco de dados de modelo.

Os locais disponíveis para o provedor `builtin` são `C`, `C.UTF-8` e `PG_UNICODE_FAST`.

*`icu_locale`* [#](#CREATE-DATABASE-ICU-LOCALE): Especifica o idioma do ICU (ver [Seção 23.2.2.3.2](collation.md#COLLATION-MANAGING-CREATE-ICU "23.2.2.3.2. ICU Collations")) para a ordem de classificação de collation padrão do banco de dados e classificação de caracteres, substituindo a configuração [*`locale`](sql-createdatabase.md#CREATE-DATABASE-LOCALE). O [provedor de localização](sql-createdatabase.md#CREATE-DATABASE-LOCALE-PROVIDER) deve ser ICU. A configuração padrão é a do [*`locale`](sql-createdatabase.md#CREATE-DATABASE-LOCALE) se especificada; caso contrário, a mesma configuração que o banco de dados de modelo.

*`icu_rules`* [#](#CREATE-DATABASE-ICU-RULES): Especifica regras adicionais de ordenação para personalizar o comportamento da ordenação padrão deste banco de dados. Isso é suportado apenas para ICU. Consulte [Seção 23.2.3.4](collation.md#ICU-TAILORING-RULES "23.2.3.4. ICU Tailoring Rules") para detalhes.

*`locale_provider`* [#](#CREATE-DATABASE-LOCALE-PROVIDER): Especifica o provedor a ser usado para a agregação padrão neste banco de dados. Os valores possíveis são `builtin`, `icu` (se o servidor foi construído com suporte ao ICU) ou `libc`. Por padrão, o provedor é o mesmo que o do [*`template`](sql-createdatabase.md#CREATE-DATABASE-TEMPLATE). Veja [Seção 23.1.4](locale.md#LOCALE-PROVIDERS "23.1.4. Locale Providers") para detalhes.

*`collation_version`* [#](#CREATE-DATABASE-COLLATION-VERSION): Especifica a string da versão da correção de texto a ser armazenada com o banco de dados. Normalmente, isso deve ser omitido, o que fará com que a versão seja calculada a partir da versão real da correção de texto do banco de dados, conforme fornecida pelo sistema operacional. Esta opção é destinada a ser usada por `pg_upgrade` para copiar a versão de uma instalação existente.

Veja também [ALTER DATABASE](sql-alterdatabase.md "ALTER DATABASE") para saber como lidar com desalinhamentos na versão da coligação do banco de dados.

*`tablespace_name`* [#](#CREATE-DATABASE-TABLESPACE-NAME): O nome do tablespace que será associado ao novo banco de dados, ou `DEFAULT` para usar o tablespace do banco de dados de modelo. Este tablespace será o tablespace padrão usado para objetos criados neste banco de dados. Consulte [CREATE TABLESPACE](sql-createtablespace.md "CREATE TABLESPACE") para obter mais informações.

*`allowconn`* [#](#CREATE-DATABASE-ALLOWCONN): Se falso, então ninguém pode se conectar a este banco de dados. O padrão é verdadeiro, permitindo conexões (exceto conforme restrito por outros mecanismos, como `GRANT`/`REVOKE CONNECT`).

*`connlimit`* [#](#CREATE-DATABASE-CONNLIMIT): Quantos conexões concorrentes podem ser feitas com este banco de dados. -1 (o padrão) significa sem limite.

*`istemplate`* [#](#CREATE-DATABASE-ISTEMPLATE): Se verdadeiro, então este banco de dados pode ser clonado por qualquer usuário com privilégios `CREATEDB`; se falso (o padrão), então apenas superusuários ou o proprietário do banco de dados podem cloná-lo.

*`oid`* [#](#CREATE-DATABASE-OID): O identificador do objeto a ser utilizado para o novo banco de dados. Se este parâmetro não for especificado, o PostgreSQL escolherá um OID adequado automaticamente. Este parâmetro é destinado principalmente para uso interno pelo pg_upgrade, e apenas o pg_upgrade pode especificar um valor menor que 16384.

Os parâmetros opcionais podem ser escritos em qualquer ordem, não apenas na ordem ilustrada acima.

## Notas

`CREATE DATABASE` não pode ser executado dentro de um bloco de transação.

Erros relacionados à linha “não foi possível inicializar o diretório do banco de dados” provavelmente estão relacionados a permissões insuficientes no diretório de dados, em um disco completo ou outros problemas no sistema de arquivos.

Use `DROP DATABASE`(sql-dropdatabase.md "DROP DATABASE") para remover um banco de dados.

O programa [createdb](app-createdb.md "createdb") é um programa wrapper em torno deste comando, fornecido para conveniência.

Os parâmetros de configuração de nível de banco de dados (definidos por meio de `ALTER DATABASE`](sql-alterdatabase.md "ALTER DATABASE")) e permissões de nível de banco de dados (definidas por meio de `GRANT`](sql-grant.md "GRANT")) não são copiados do banco de dados do modelo.

Embora seja possível copiar um banco de dados que não seja o `template1`, especificando seu nome como o modelo, isso não é (ainda) uma facilidade de propósito geral do tipo `COPY DATABASE`. A principal limitação é que nenhuma outra sessão pode ser conectada ao banco de dados do modelo enquanto ele está sendo copiado. O `CREATE DATABASE` falhará se houver alguma outra conexão existente quando ele for iniciado; caso contrário, novas conexões ao banco de dados do modelo serão bloqueadas até que o `CREATE DATABASE` seja concluído. Consulte [Seção 22.3](manage-ag-templatedbs.md) para obter mais informações.

O conjunto de codificação de caracteres especificado para o novo banco de dados deve ser compatível com as configurações de localização escolhidas (`LC_COLLATE` e `LC_CTYPE`). Se a localização for `C` (ou equivalentemente `POSIX`), então todas as codificações são permitidas, mas para outras configurações de localização, há apenas uma codificação que funcionará corretamente. (No entanto, em Windows, a codificação UTF-8 pode ser usada com qualquer localização). `CREATE DATABASE` permitirá que os superusuários especifiquem a codificação `SQL_ASCII`, independentemente das configurações de localização, mas essa escolha é desaconselhada e pode resultar em comportamento incorreto de funções de cadeia de caracteres se os dados que não são compatíveis com a codificação da localização forem armazenados no banco de dados.

As configurações de codificação e local devem corresponder às do banco de dados do modelo, exceto quando `template0` é usado como modelo. Isso ocorre porque outros bancos de dados podem conter dados que não correspondem à codificação especificada, ou podem conter índices cujos pedidos de classificação são afetados por `LC_COLLATE` e `LC_CTYPE`. A cópia de tais dados resultaria em um banco de dados que seria corrupto de acordo com as novas configurações. `template0`, no entanto, é conhecido por não conter quaisquer dados ou índices que seriam afetados.

Atualmente, não há opção para usar um local de banco de dados com comparações não determinísticas (consulte `CREATE COLLATION` para uma explicação). Se isso for necessário, então as colunas de classificação por coluna precisarão ser usadas.

A opção `CONNECTION LIMIT` é apenas aplicada aproximadamente; se duas novas sessões começarem aproximadamente ao mesmo tempo, quando apenas um "caixote" de conexão permanece para o banco de dados, é possível que ambas falhem. Além disso, o limite não é aplicado contra superusuários ou processos de trabalhador de fundo.

## Exemplos

Para criar um novo banco de dados:

```
CREATE DATABASE lusiadas;
```

Para criar um banco de dados `sales` de propriedade do usuário `salesapp` com um espaço de tabelas padrão de `salesspace`:

```
CREATE DATABASE sales OWNER salesapp TABLESPACE salesspace;
```

Para criar um banco de dados `music` com um local diferente:

```
CREATE DATABASE music
    LOCALE 'sv_SE.utf8'
    TEMPLATE template0;
```

Neste exemplo, a cláusula `TEMPLATE template0` é necessária se o local especificado for diferente do que está em `template1`. (Se não for, então especificar o local explicitamente é redundante.)

Para criar um banco de dados `music2` com um local diferente e um conjunto de codificação de caracteres diferente:

```
CREATE DATABASE music2
    LOCALE 'sv_SE.iso885915'
    ENCODING LATIN9
    TEMPLATE template0;
```

Os ajustes de localização e codificação especificados devem corresponder, ou uma mensagem de erro será relatada.

Observe que os nomes de localização são específicos para o sistema operacional, portanto, os comandos acima podem não funcionar da mesma maneira em todos os lugares.

## Compatibilidade

Não há nenhuma declaração `CREATE DATABASE` no padrão SQL. Os bancos de dados são equivalentes a catálogos, cuja criação é definida pela implementação.

## Veja também

[ALTER DATABASE](sql-alterdatabase.md "ALTER DATABASE"), [DROP DATABASE](sql-dropdatabase.md "DROP DATABASE")