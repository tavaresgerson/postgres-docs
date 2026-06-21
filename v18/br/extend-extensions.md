## 36.17. Organização de objetos relacionados ao embalamento em uma extensão [#](#EXTEND-EXTENSIONS)

* [36.17.1. Arquivos de extensão](extend-extensions.md#EXTEND-EXTENSIONS-FILES)
* [36.17.2. Realocação de extensão](extend-extensions.md#EXTEND-EXTENSIONS-RELOCATION)
* [36.17.3. Tabelas de configuração de extensão](extend-extensions.md#EXTEND-EXTENSIONS-CONFIG-TABLES)
* [36.17.4. Atualizações de extensão](extend-extensions.md#EXTEND-EXTENSIONS-UPDATES)
* [36.17.5. Instalação de extensões usando scripts de atualização](extend-extensions.md#EXTEND-EXTENSIONS-UPDATE-SCRIPTS)
* [36.17.6. Considerações de segurança para extensões](extend-extensions.md#EXTEND-EXTENSIONS-SECURITY)
* [36.17.7. Exemplo de extensão](extend-extensions.md#EXTEND-EXTENSIONS-EXAMPLE)

Uma extensão útil para o PostgreSQL geralmente inclui vários objetos SQL; por exemplo, um novo tipo de dados exigirá novas funções, novos operadores e, provavelmente, novas classes de operadores de índice. É útil coletar todos esses objetos em um único pacote para simplificar a gestão do banco de dados. O PostgreSQL chama essa extensão de *extensão*. Para definir uma extensão, você precisa de pelo menos um *arquivo de script* que contenha os comandos SQL para criar os objetos da extensão, e um *arquivo de controle* que especifique algumas propriedades básicas da própria extensão. Se a extensão incluir código C, geralmente haverá também um arquivo de biblioteca compartilhada no qual o código C foi construído. Uma vez que você tenha esses arquivos, um comando simples `CREATE EXTENSION`[(sql-createextension.md "CREATE EXTENSION")] carrega os objetos em seu banco de dados.

A principal vantagem de usar uma extensão, em vez de simplesmente executar o script SQL para carregar um monte de objetos "soltos" em seu banco de dados, é que o PostgreSQL então entenderá que os objetos da extensão vão juntos. Você pode descartar todos os objetos com um comando `DROP EXTENSION`(sql-dropextension.md "DROP EXTENSION") (não é necessário manter um script "desinstalar" separado). Ainda mais útil, o pg_dump sabe que não deve drenar os objetos individuais dos membros da extensão — ele simplesmente incluirá um comando `CREATE EXTENSION` em os dumps, em vez disso. Isso simplifica muito a migração para uma nova versão da extensão que pode conter mais ou diferentes objetos do que a versão antiga. No entanto, é importante notar que você deve ter o controle, o script e outros arquivos da extensão disponíveis ao carregar um dump desse tipo em um novo banco de dados.

O PostgreSQL não permitirá que você elimine um objeto individual contido em uma extensão, exceto descartando toda a extensão. Além disso, embora você possa alterar a definição de um objeto membro de uma extensão (por exemplo, via `CREATE OR REPLACE FUNCTION` para uma função), tenha em mente que a definição modificada não será descarregada pelo pg_dump. Essa alteração geralmente é sensível apenas se você fizer simultaneamente a mesma alteração no arquivo de script da extensão. (Mas há disposições especiais para tabelas que contêm dados de configuração; veja [Seção 36.17.3](extend-extensions.md#EXTEND-EXTENSIONS-CONFIG-TABLES). Em situações de produção, geralmente é melhor criar um script de atualização de extensão para realizar alterações em objetos membros da extensão.

O script de extensão pode definir privilégios em objetos que fazem parte da extensão, usando as declarações `GRANT` e `REVOKE`. O conjunto final de privilégios para cada objeto (se algum for definido) será armazenado no catálogo do sistema [[`pg_init_privs`](catalog-pg-init-privs.md)]. Quando o pg_dump é usado, o comando `CREATE EXTENSION` será incluído no dump, seguido pelo conjunto de declarações `GRANT` e `REVOKE` necessárias para definir os privilégios nos objetos para o que estavam na época em que o dump foi feito.

O PostgreSQL atualmente não suporta scripts de extensão que emitem declarações `CREATE POLICY` ou `SECURITY LABEL`. Espera-se que essas sejam definidas após a extensão ter sido criada. Todas as políticas e rótulos de segurança dos objetos de extensão serão incluídos em os backups criados pelo pg_dump.

O mecanismo de extensão também possui disposições para scripts de modificação de pacotes que ajustam as definições dos objetos SQL contidos em uma extensão. Por exemplo, se a versão 1.1 de uma extensão adiciona uma função e altera o corpo de outra função em comparação com a versão 1.0, o autor da extensão pode fornecer um *script de atualização* que faça apenas essas duas alterações. O comando `ALTER EXTENSION UPDATE` pode então ser usado para aplicar essas alterações e rastrear qual versão da extensão está realmente instalada em um banco de dados específico.

Os tipos de objetos SQL que podem ser membros de uma extensão são mostrados na descrição de `ALTER EXTENSION`(sql-alterextension.md "ALTER EXTENSION"). Notavelmente, objetos que são de todo o banco de dados, como bancos de dados, papéis e espaços de tabela, não podem ser membros de uma extensão, uma vez que uma extensão é conhecida apenas em um banco de dados. (Embora um script de extensão não seja proibido de criar tais objetos, se o fizer, eles não serão rastreados como parte da extensão.) Além disso, observe que, embora uma tabela possa ser membro de uma extensão, seus objetos subsidiários, como índices, não são diretamente considerados membros da extensão. Outro ponto importante é que os esquemas podem pertencer a extensões, mas não vice-versa: uma extensão como tal tem um nome não qualificado e não existe “dentro” de nenhum esquema. Os objetos membros da extensão, no entanto, pertencerão a esquemas sempre que apropriado para seus tipos de objeto. Pode ou não ser apropriado para uma extensão possuir os esquemas nos quais seus objetos membros estão.

Se o script de uma extensão criar quaisquer objetos temporários (como tabelas temporárias), esses objetos são tratados como membros da extensão para o restante da sessão atual, mas são automaticamente descartados no final da sessão, como qualquer objeto temporário seria. Esta é uma exceção à regra de que os objetos de membros da extensão não podem ser descartados sem descartar toda a extensão.

### 36.17.1. Arquivos de extensão [#](#EXTEND-EXTENSIONS-FILES)

O comando `CREATE EXTENSION` depende de um arquivo de controle para cada extensão, que deve ser nomeado da mesma forma que a extensão, com um sufixo de `.control`, e deve ser colocado no diretório `SHAREDIR/extension` da instalação. Também deve haver pelo menos um arquivo de script SQL, que segue o padrão de nomeação `extension--version.sql` (por exemplo, `foo--1.0.sql` para a versão `1.0` da extensão `foo`). Por padrão, os(s) arquivo(s) de script também são colocados no diretório `SHAREDIR/extension`, mas o arquivo de controle pode especificar um diretório diferente para o(s) arquivo(s) de script.

Locais adicionais para arquivos de controle de extensão podem ser configurados usando o parâmetro [extension_control_path](runtime-config-client.md#GUC-EXTENSION-CONTROL-PATH).

O formato do arquivo para um arquivo de controle de extensão é o mesmo que para o arquivo `postgresql.conf`, ou seja, uma lista de *`parameter_name`* `=` *`value`* atribuições, uma por linha. Linhas em branco e comentários introduzidos por `#` são permitidos. Certifique-se de citar qualquer valor que não seja uma palavra ou número único.

Um arquivo de controle pode definir os seguintes parâmetros:

`directory` (`string`) [#](#EXTEND-EXTENSIONS-FILES-DIRECTORY): O diretório que contém o(s) arquivo(s) de script SQL da extensão. A menos que um caminho absoluto seja fornecido, o nome é relativo ao diretório onde o arquivo de controle foi encontrado. Por padrão, os arquivos de script são procurados no mesmo diretório onde o arquivo de controle foi encontrado.

`default_version` (`string`) [#](#EXTEND-EXTENSIONS-FILES-DEFAULT-VERSION): A versão padrão da extensão (a que será instalada se nenhuma versão for especificada em `CREATE EXTENSION`). Embora isso possa ser omitido, isso resultará em `CREATE EXTENSION` falhando se nenhuma opção de `VERSION` aparecer, então você geralmente não quer fazer isso.

`comment` (`string`) [#](#EXTEND-EXTENSIONS-FILES-COMMENT): Um comentário (qualquer string) sobre a extensão. O comentário é aplicado ao criar inicialmente uma extensão, mas não durante as atualizações da extensão (já que isso pode substituir comentários adicionados pelo usuário). Alternativamente, o comentário da extensão pode ser definido escrevendo um comando [COMMENT](sql-comment.md "COMMENT") no arquivo de script.

`encoding` (`string`) [#](#EXTEND-EXTENSIONS-FILES-ENCODING): O conjunto de caracteres de codificação usado pelo(s) arquivo(s) de script. Isso deve ser especificado se os arquivos de script contiverem caracteres não ASCII. Caso contrário, os arquivos serão assumidos como tendo a codificação do banco de dados.

`module_pathname` (`string`) [#](#EXTEND-EXTENSIONS-FILES-MODULE-PATHNAME): O valor deste parâmetro será substituído para cada ocorrência de `MODULE_PATHNAME` no(s) arquivo(s) de script. Se não for definido, não haverá substituição. Tipicamente, este é definido como apenas `shared_library_name` e, em seguida, `MODULE_PATHNAME` é usado em comandos de `CREATE FUNCTION` para funções em linguagem C, de modo que os arquivos de script não precisem conectar o nome da biblioteca compartilhada.

`requires` (`string`) [#](#EXTEND-EXTENSIONS-FILES-REQUIRES): Uma lista de nomes das extensões que esta extensão depende, por exemplo `requires = 'foo, bar'`. Essas extensões devem ser instaladas antes que esta possa ser instalada.

`no_relocate` (`string`) [#](#EXTEND-EXTENSIONS-FILES-NO-RELOCATE): Uma lista de nomes de extensões que esta extensão depende e que não devem alterar seus esquemas via `ALTER EXTENSION ... SET SCHEMA`. Isso é necessário se o script desta extensão fizer referência ao nome do esquema de uma extensão necessária (usando a sintaxe `@extschema:name@`) de uma maneira que não possa rastrear renomeamentos.

`superuser` (`boolean`) [#](#EXTEND-EXTENSIONS-FILES-SUPERUSER): Se este parâmetro for `true` (que é o padrão), apenas os usuários superusuários podem criar a extensão ou atualizá-la para uma nova versão (mas veja também `trusted`, abaixo). Se estiver definido como `false`, apenas os privilégios necessários para executar os comandos no script de instalação ou atualização são necessários. Isso normalmente deve ser definido como `true` se algum dos comandos do script exigir privilégios de superusuário. (Tais comandos falhariam de qualquer forma, mas é mais amigável ao usuário dar o erro de antemão.)

`trusted` (`boolean`) [#](#EXTEND-EXTENSIONS-FILES-TRUSTED): Este parâmetro, se definido como `true` (que não é o padrão), permite que alguns usuários não superusuários instalem uma extensão que tenha `superuser` definido como `true`. Especificamente, a instalação será permitida para qualquer pessoa que tenha privilégio `CREATE` no banco de dados atual. Quando o usuário que executa `CREATE EXTENSION` não é um superusuário, mas é autorizado a instalar em virtude deste parâmetro, então o script de instalação ou atualização é executado como o superusuário de bootstrap, não como o usuário que o está solicitando. Este parâmetro é irrelevante se `superuser` for `false`. Geralmente, não deve ser definido como verdadeiro para extensões que poderiam permitir acesso a habilidades que são exclusivas dos superusuários, como acesso ao sistema de arquivos. Além disso, marcar uma extensão como confiável requer um esforço adicional significativo para escrever o(s) script(s) de instalação e atualização da extensão de forma segura; veja [Seção 36.17.6](extend-extensions.md#EXTEND-EXTENSIONS-SECURITY "36.17.6. Security Considerations for Extensions").

`relocatable` (`boolean`) [#](#EXTEND-EXTENSIONS-FILES-RELOCATABLE): Uma extensão é *relocável* se for possível mover seus objetos contidos em um esquema diferente após a criação inicial da extensão. O padrão é `false`, ou seja, a extensão não é relocável. Consulte [Seção 36.17.2](extend-extensions.md#EXTEND-EXTENSIONS-RELOCATION "36.17.2. Extension Relocatability") para obter mais informações.

`schema` (`string`) [#](#EXTEND-EXTENSIONS-FILES-SCHEMA): Este parâmetro só pode ser definido para extensões não relocáveis. Ele obriga a extensão a ser carregada exatamente no esquema nomeado e não em qualquer outro. O parâmetro `schema` é consultado apenas durante a criação inicial de uma extensão, não durante as atualizações da extensão. Consulte [Seção 36.17.2](extend-extensions.md#EXTEND-EXTENSIONS-RELOCATION "36.17.2. Extension Relocatability") para obter mais informações.

Além do arquivo de controle primário `extension.control`, uma extensão pode ter arquivos de controle secundários com nomes no estilo `extension--version.control`. Se fornecidos, esses arquivos devem estar localizados no diretório do arquivo de script. Os arquivos de controle secundários seguem o mesmo formato que o arquivo de controle primário. Quaisquer parâmetros definidos em um arquivo de controle secundário substituem o arquivo de controle primário ao instalar ou atualizar para aquela versão da extensão. No entanto, os parâmetros `directory` e `default_version` não podem ser definidos em um arquivo de controle secundário.

Os arquivos de script SQL de uma extensão podem conter quaisquer comandos SQL, exceto comandos de controle de transação (`BEGIN`, `COMMIT`, etc.) e comandos que não podem ser executados dentro de um bloco de transação (como [[`VACUUM`]). Isso ocorre porque os arquivos de script são executados implicitamente dentro de um bloco de transação.

Os arquivos de script SQL de uma extensão também podem conter linhas que começam com `\echo`, que serão ignoradas (tratadas como comentários) pelo mecanismo de extensão. Esta disposição é comumente usada para lançar um erro se o arquivo de script for fornecido ao psql em vez de ser carregado via `CREATE EXTENSION` (veja o exemplo de script em [Seção 36.17.7](extend-extensions.md#EXTEND-EXTENSIONS-EXAMPLE)). Sem isso, os usuários podem acidentalmente carregar o conteúdo da extensão como objetos "soltos" em vez de como uma extensão, uma situação um pouco tediosa de recuperar.

Se o script de extensão contiver a string `@extowner@`, essa string é substituída pelo nome (citado adequadamente) do usuário que está chamando `CREATE EXTENSION` ou `ALTER EXTENSION`. Tipicamente, essa funcionalidade é usada por extensões marcadas como confiáveis para atribuir a propriedade de objetos selecionados ao usuário que está chamando, em vez do superusuário de inicialização. (No entanto, é preciso ter cuidado ao fazer isso. Por exemplo, atribuir a propriedade de uma função em linguagem C a um usuário que não é um superusuário criaria um caminho de escalada de privilégios para esse usuário.)

Embora os arquivos de script possam conter quaisquer caracteres permitidos pelo codificação especificada, os arquivos de controle devem conter apenas ASCII simples, porque não há como o PostgreSQL saber em qual codificação está um arquivo de controle. Na prática, isso é apenas um problema se você quiser usar caracteres não ASCII no comentário da extensão. A prática recomendada, nesse caso, é não usar o parâmetro `comment` no arquivo de controle, mas sim usar `COMMENT ON EXTENSION` dentro de um arquivo de script para definir o comentário.

### 36.17.2. Extensão relocável [#](#EXTEND-EXTENSIONS-RELOCATION)

Os usuários frequentemente desejam carregar os objetos contidos em uma extensão em um esquema diferente do que o autor da extensão tinha em mente. Existem três níveis de relocatabilidade suportados:

* Uma extensão totalmente relocável pode ser movida para outro esquema a qualquer momento, mesmo depois de ter sido carregada em um banco de dados. Isso é feito com o comando `ALTER EXTENSION SET SCHEMA`, que renomeia automaticamente todos os objetos membros para o novo esquema. Normalmente, isso só é possível se a extensão não contiver suposições internas sobre qual esquema qualquer de seus objetos está. Além disso, os objetos da extensão devem estar todos em um esquema desde o início (ignorando objetos que não pertencem a nenhum esquema, como linguagens procedimentais). Marque uma extensão totalmente relocável definindo `relocatable = true` em seu arquivo de controle.
* Uma extensão pode ser relocável durante a instalação, mas não posteriormente. Isso é tipicamente o caso se o arquivo de script da extensão precisar referenciar explicitamente o esquema alvo, por exemplo, ao definir propriedades `search_path` para funções SQL. Para tal extensão, defina `relocatable = false` em seu arquivo de controle e use `@extschema@` para referenciar o esquema alvo no arquivo de script. Todas as ocorrências desta string serão substituídas pelo nome do esquema alvo real (com aspas duplas, se necessário) antes do script ser executado. O usuário pode definir o esquema alvo usando a opção `SCHEMA` de `CREATE EXTENSION`.
* Se a extensão não suportar relocação, defina `relocatable = false` em seu arquivo de controle e também defina `schema` para o nome do esquema alvo pretendido. Isso impedirá o uso da opção `SCHEMA` de `CREATE EXTENSION`, a menos que especifique o mesmo esquema nomeado no arquivo de controle. Essa escolha é tipicamente necessária se a extensão contiver suposições internas sobre o nome de seu esquema que não podem ser substituídas por usos de `@extschema@`. O mecanismo de substituição `@extschema@` também está disponível neste caso, embora seja de uso limitado, uma vez que o nome do esquema é determinado pelo arquivo de controle.

Em todos os casos, o arquivo de script será executado com [search_path](runtime-config-client.md#GUC-SEARCH-PATH) inicialmente definido para apontar para o esquema de destino; ou seja, `CREATE EXTENSION` faz o equivalente a isso:

```
SET LOCAL search_path TO @extschema@, pg_temp;
```

Isso permite que os objetos criados pelo arquivo de script sejam inseridos no esquema de destino. O arquivo de script pode alterar `search_path`, se desejar, mas isso geralmente não é desejável. `search_path` é restaurado para sua configuração anterior após a conclusão de `CREATE EXTENSION`.

O esquema-alvo é determinado pelo parâmetro `schema` no arquivo de controle, se este for fornecido, caso contrário, pelo parâmetro `SCHEMA` da opção `CREATE EXTENSION`, se este for fornecido, caso contrário, o esquema atual de criação de objetos padrão (o primeiro no `search_path` do solicitante). Quando o parâmetro do arquivo de controle `schema` é usado, o esquema-alvo será criado se ele ainda não existir, mas nos outros dois casos, ele deve já existir.

Se quaisquer extensões pré-requisitárias estiverem listadas em `requires` no arquivo de controle, seus esquemas-alvo são adicionados ao ajuste inicial de `search_path`, seguindo o esquema-alvo da nova extensão. Isso permite que seus objetos sejam visíveis para o arquivo de script da nova extensão.

Por segurança, `pg_temp` é automaticamente anexado ao final de `search_path` em todos os casos.

Embora uma extensão não relocável possa conter objetos espalhados por vários esquemas, geralmente é desejável colocar todos os objetos destinados ao uso externo em um único esquema, que é considerado o esquema-alvo da extensão. Tal arranjo funciona convenientemente com a configuração padrão de `search_path` durante a criação de extensões dependentes.

Se uma extensão fizer referência a objetos pertencentes a outra extensão, é recomendável qualificar esses referências com base no esquema. Para isso, escreva `@extschema:name@` no arquivo de script da extensão, onde *`name`* é o nome da outra extensão (que deve estar listado na lista `requires` desta extensão. Essa string será substituída pelo nome (com duplicidade de aspas, se necessário) do esquema de destino daquela extensão. Embora essa notação evite a necessidade de fazer suposições fixas sobre os nomes dos esquemas no arquivo de script da extensão, seu uso pode incorporar o nome do esquema da outra extensão nos objetos instalados desta extensão. (Tipicamente, isso acontece quando `@extschema:name@` é usado dentro de uma literal de string, como um corpo de função ou um ajuste `search_path`. Em outros casos, a referência ao objeto é reduzida a um OID durante a análise e não requer buscas subsequentes.) Se o nome do esquema da outra extensão estiver incorporado dessa forma, você deve impedir que a outra extensão seja realocada após a sua instalação, adicionando o nome da outra extensão à lista `no_relocate` desta.

### 36.17.3. Tabelas de Configuração de Extensão [#](#EXTEND-EXTENSIONS-CONFIG-TABLES)

Algumas extensões incluem tabelas de configuração, que contêm dados que podem ser adicionados ou alterados pelo usuário após a instalação da extensão. Normalmente, se uma tabela faz parte de uma extensão, nem a definição da tabela nem seu conteúdo serão descarregados pelo pg_dump. Mas esse comportamento é indesejável para uma tabela de configuração; quaisquer alterações de dados feitas pelo usuário precisam ser incluídas em descargas, ou a extensão se comportará de maneira diferente após uma descarga e restauração.

Para resolver esse problema, o arquivo de script de uma extensão pode marcar uma tabela ou uma sequência que ela criou como uma relação de configuração, o que fará com que o pg_dump inclua o conteúdo da tabela ou da sequência (e não sua definição) nos backups. Para fazer isso, chame a função `pg_extension_config_dump(regclass, text)` após criar a tabela ou a sequência, por exemplo:

```
CREATE TABLE my_config (key text, value text);
CREATE SEQUENCE my_config_seq;

SELECT pg_catalog.pg_extension_config_dump('my_config', '');
SELECT pg_catalog.pg_extension_config_dump('my_config_seq', '');
```

Qualquer número de tabelas ou sequências pode ser marcado dessa maneira. Sequências associadas às colunas `serial` ou `bigserial` também podem ser marcadas.

Quando o segundo argumento de `pg_extension_config_dump` for uma string vazia, todo o conteúdo da tabela será descarregada pelo pg_dump. Isso geralmente é correto apenas se a tabela estiver inicialmente vazia, conforme criada pelo script de extensão. Se houver uma mistura de dados iniciais e dados fornecidos pelo usuário na tabela, o segundo argumento de `pg_extension_config_dump` fornece uma condição de `WHERE` que seleciona os dados a serem descarregados. Por exemplo, você pode fazer

```
CREATE TABLE my_config (key text, value text, standard_entry boolean);

SELECT pg_catalog.pg_extension_config_dump('my_config', 'WHERE NOT standard_entry');
```

e, em seguida, certifique-se de que `standard_entry` seja verdadeiro apenas nas linhas criadas pelo script da extensão.

Para sequências, o segundo argumento de `pg_extension_config_dump` não tem efeito.

Situações mais complicadas, como linhas fornecidas inicialmente que podem ser modificadas por usuários, podem ser tratadas criando gatilhos na tabela de configuração para garantir que as linhas modificadas sejam marcadas corretamente.

Você pode alterar a condição do filtro associada a uma tabela de configuração chamando novamente `pg_extension_config_dump`. (Isso geralmente seria útil em um script de atualização de extensão.) A única maneira de marcar uma tabela como não mais uma tabela de configuração é dissociá-la da extensão com `ALTER EXTENSION ... DROP TABLE`.

Observe que as relações de chave estrangeira entre essas tabelas determinarão a ordem em que as tabelas serão descarregadas pelo pg_dump. Especificamente, o pg_dump tentará descarregar a tabela referenciada antes da tabela que a referencia. Como as relações de chave estrangeira são configuradas no momento da criação da extensão (antes dos dados serem carregados nas tabelas), as dependências circulares não são suportadas. Quando existem dependências circulares, os dados ainda serão descarregados, mas o descarregamento não poderá ser restaurado diretamente e será necessária intervenção do usuário.

As sequências associadas às colunas `serial` ou `bigserial` precisam ser marcadas diretamente para descartar seu estado. Marcar sua relação pai não é suficiente para esse propósito.

### 36.17.4. Atualizações de extensão [#](#EXTEND-EXTENSIONS-UPDATES)

Uma vantagem do mecanismo de extensão é que ele oferece maneiras convenientes de gerenciar as atualizações dos comandos SQL que definem os objetos de uma extensão. Isso é feito associando um nome ou número de versão a cada versão lançada do script de instalação da extensão. Além disso, se você deseja que os usuários possam atualizar seus bancos de dados dinamicamente de uma versão para a próxima, você deve fornecer *scripts de atualização* que façam as mudanças necessárias para ir de uma versão para a próxima. Os scripts de atualização têm nomes que seguem o padrão `extension--old_version--target_version.sql` (por exemplo, `foo--1.0--1.1.sql` contém os comandos para modificar a versão `1.0` da extensão `foo` para a versão `1.1`).

Dado que um script de atualização adequado está disponível, o comando `ALTER EXTENSION UPDATE` atualizará uma extensão instalada para a nova versão especificada. O script de atualização é executado no mesmo ambiente que o `CREATE EXTENSION` fornece para os scripts de instalação: em particular, o `search_path` é configurado da mesma maneira, e quaisquer novos objetos criados pelo script são automaticamente adicionados à extensão. Além disso, se o script optar por descartar os objetos membros da extensão, eles são automaticamente dissociados da extensão.

Se uma extensão tiver arquivos de controle secundários, os parâmetros de controle que são usados para um script de atualização são aqueles associados à versão (nova) do alvo do script.

`ALTER EXTENSION` é capaz de executar sequências de arquivos de script de atualização para realizar uma atualização solicitada. Por exemplo, se apenas `foo--1.0--1.1.sql` e `foo--1.1--2.0.sql` estiverem disponíveis, `ALTER EXTENSION` os aplicará em sequência se uma atualização para a versão `2.0` for solicitada quando `1.0` estiver atualmente instalado.

O PostgreSQL não assume nada sobre as propriedades dos nomes das versões: por exemplo, ele não sabe se `1.1` segue `1.0`. Ele apenas combina os nomes das versões disponíveis e segue o caminho que exige a aplicação dos scripts de atualização mais baixos. (Um nome de versão pode ser, na verdade, qualquer string que não contenha `--` ou `-` no início ou no fim.)

Às vezes, é útil fornecer scripts de "rebaixamento", por exemplo `foo--1.1--1.0.sql`, para permitir a reversão das alterações associadas à versão `1.1`. Se você fizer isso, tenha cuidado com a possibilidade de que um script de rebaixamento possa ser aplicado inesperadamente, pois ele gera um caminho mais curto. O caso arriscado é quando há um script de atualização de "caminho rápido" que pula várias versões, bem como um script de rebaixamento para o ponto de partida do caminho rápido. Pode levar menos etapas para aplicar o rebaixamento e depois o caminho rápido do que para avançar uma versão de cada vez. Se o script de rebaixamento eliminar quaisquer objetos irrecuperáveis, isso produzirá resultados indesejáveis.

Para verificar caminhos de atualização inesperados, use este comando:

```
SELECT * FROM pg_extension_update_paths('extension_name');
```

Isso mostra cada par de nomes de versão conhecidos distintos para a extensão especificada, juntamente com a sequência do caminho de atualização que seria tomada para ir da versão de origem para a versão de destino, ou `NULL` se não houver um caminho de atualização disponível. O caminho é mostrado em forma textual com separadores `--`. Você pode usar `regexp_split_to_array(path,'--')` se preferir um formato de matriz.

### 36.17.5. Instalação de extensões usando scripts de atualização [#](#EXTEND-EXTENSIONS-UPDATE-SCRIPTS)

Uma extensão que já existe há algum tempo provavelmente existirá em várias versões, para as quais o autor precisará escrever scripts de atualização. Por exemplo, se você tiver lançado uma extensão `foo` em versões `1.0`, `1.1` e `1.2`, deve haver scripts de atualização `foo--1.0--1.1.sql` e `foo--1.1--1.2.sql`. Antes do PostgreSQL 10, era necessário criar também novos arquivos de script `foo--1.1.sql` e `foo--1.2.sql` que constroem diretamente as versões mais recentes da extensão, caso contrário, as versões mais recentes não poderiam ser instaladas diretamente, apenas instalando `1.0` e depois atualizando. Isso era tedioso e redundante, mas agora é desnecessário, porque o `CREATE EXTENSION` pode seguir cadeias de atualização automaticamente. Por exemplo, se apenas os arquivos de script `foo--1.0.sql`, `foo--1.0--1.1.sql` e `foo--1.1--1.2.sql` estiverem disponíveis, então uma solicitação para instalar a versão `1.2` é atendida ao executar esses três scripts em sequência. O processamento é o mesmo como se primeiro tivesse instalado `1.0` e depois atualizado para `1.2`. (Como com `ALTER EXTENSION UPDATE`, se houver múltiplos caminhos disponíveis, o mais curto é preferido.) Organizar os arquivos de script de uma extensão nesse estilo pode reduzir a quantidade de esforço de manutenção necessário para produzir pequenas atualizações.

Se você usar arquivos de controle secundários (específicos para a versão) com uma extensão mantida nesse estilo, tenha em mente que cada versão precisa de um arquivo de controle, mesmo que não tenha um script de instalação autônomo, pois esse arquivo de controle determinará como a atualização implícita para essa versão será realizada. Por exemplo, se `foo--1.0.control` especifica `requires = 'bar'`, mas os outros arquivos de controle de `foo` não o fazem, a dependência da extensão em `bar` será descartada ao atualizar de `1.0` para outra versão.

### 36.17.6. Considerações de segurança para extensões [#](#EXTEND-EXTENSIONS-SECURITY)

Extensões amplamente distribuídas devem assumir pouco sobre o banco de dados que ocupam. Portanto, é apropriado escrever funções fornecidas por uma extensão em um estilo seguro que não possa ser comprometido por ataques baseados em caminho de pesquisa.

Uma extensão que tenha a propriedade `superuser` definida como verdadeira também deve considerar os riscos de segurança das ações realizadas em seus scripts de instalação e atualização. Não é muito difícil para um usuário malicioso criar objetos de cavalo de Troia que comprometam a execução posterior de um script de extensão mal escrito, permitindo que o usuário adquira privilégios de superusuário.

Se uma extensão estiver marcada com `trusted`, o esquema de instalação pode ser selecionado pelo usuário que a instala, que pode intencionalmente usar um esquema inseguro na esperança de obter privilégios de superusuário. Portanto, uma extensão confiável é extremamente exposta em termos de segurança, e todos os comandos de script devem ser cuidadosamente examinados para garantir que não haja possibilidade de comprometimento.

Conselhos sobre a escrita de funções de forma segura são fornecidos na [Seção 36.17.6.1](extend-extensions.md#EXTEND-EXTENSIONS-SECURITY-FUNCS) abaixo, e conselhos sobre a escrita de scripts de instalação de forma segura são fornecidos na [Seção 36.17.6.2](extend-extensions.md#EXTEND-EXTENSIONS-SECURITY-SCRIPTS).

#### 36.17.6.1. Considerações de segurança para funções de extensão [#](#EXTEND-EXTENSIONS-SECURITY-FUNCS)

As funções de linguagem SQL e PL fornecidas por extensões correm risco de ataques baseados no caminho de busca quando são executadas, uma vez que a análise dessas funções ocorre no momento da execução, e não no momento da criação.

A página de referência `CREATE FUNCTION`(sql-createfunction.md#SQL-CREATEFUNCTION-SECURITY "Writing SECURITY DEFINER Functions Safely") contém conselhos sobre como escrever funções `SECURITY DEFINER` de forma segura. É uma boa prática aplicar essas técnicas para qualquer função fornecida por uma extensão, uma vez que a função pode ser chamada por um usuário com privilégios elevados.

Se você não puder definir o `search_path` para conter apenas esquemas seguros, presuma que cada nome não qualificado poderia resolver-se a um objeto que um usuário malicioso definiu. Esteja atento a construções que dependem implicitamente do `search_path`; por exemplo, `IN` e `CASE expression WHEN` sempre selecionam um operador usando o caminho de busca. Em seu lugar, use `OPERATOR(schema.=) ANY` e `CASE WHEN expression`.

Uma extensão de propósito geral geralmente não deve assumir que ela foi instalada em um esquema seguro, o que significa que até mesmo referências qualificadas por esquema a seus próprios objetos não são totalmente isentas de risco. Por exemplo, se a extensão tiver definido uma função `myschema.myfunc(bigint)`, uma chamada como `myschema.myfunc(42)` poderia ser capturada por uma função hostil `myschema.myfunc(integer)`. Tenha cuidado para que os tipos de dados dos parâmetros da função e do operador correspondam exatamente aos tipos de argumento declarados, usando casts explícitos quando necessário.

#### 36.17.6.2. Considerações de segurança para scripts de extensão [#](#EXTEND-EXTENSIONS-SECURITY-SCRIPTS)

Uma extensão de instalação ou um script de atualização deve ser escrito para proteger contra ataques baseados no caminho de pesquisa que ocorrem quando o script é executado. Se uma referência a um objeto no script puder ser resolvida para algum outro objeto que não o pretendido pelo autor do script, então uma violação pode ocorrer imediatamente ou posteriormente, quando o objeto de extensão mal definido é usado.

Os comandos DDL como `CREATE FUNCTION` e `CREATE OPERATOR CLASS` são geralmente seguros, mas cuidado com qualquer comando que tenha uma expressão de propósito geral como componente. Por exemplo, `CREATE VIEW` precisa ser verificado, assim como uma expressão `DEFAULT` em `CREATE FUNCTION`.

Às vezes, um script de extensão pode precisar executar SQL de propósito geral, por exemplo, para fazer ajustes no catálogo que não são possíveis por meio do DDL. Tenha cuidado em executar tais comandos com um `search_path` seguro; *não* confie no caminho fornecido pelo `CREATE/ALTER EXTENSION` para ser seguro. A melhor prática é definir temporariamente o `search_path` para `pg_catalog, pg_temp` e inserir referências ao esquema de instalação da extensão explicitamente quando necessário. (Essa prática também pode ser útil para criar visualizações.) Exemplos podem ser encontrados nos módulos `contrib` na distribuição do código-fonte do PostgreSQL.

Referências seguras de extensão cruzada geralmente exigem a qualificação do esquema dos nomes dos objetos da outra extensão, usando a sintaxe `@extschema:name@`, além de uma correspondência cuidadosa dos tipos de argumentos para funções e operadores.

### 36.17.7. Exemplo de extensão [#](#EXTEND-EXTENSIONS-EXAMPLE)

Aqui está um exemplo completo de uma extensão apenas com SQL, um tipo composto de dois elementos que pode armazenar qualquer tipo de valor em seus slots, que são nomeados como “k” e “v”. Valores não de texto são automaticamente coercidos para texto para armazenamento.

O arquivo de script `pair--1.0.sql` parece assim:

```
-- complain if script is sourced in psql, rather than via CREATE EXTENSION
\echo Use "CREATE EXTENSION pair" to load this file. \quit

CREATE TYPE pair AS ( k text, v text );

CREATE FUNCTION pair(text, text)
RETURNS pair LANGUAGE SQL AS 'SELECT ROW($1, $2)::@extschema@.pair;';

CREATE OPERATOR ~> (LEFTARG = text, RIGHTARG = text, FUNCTION = pair);

-- "SET search_path" is easy to get right, but qualified names perform better.
CREATE FUNCTION lower(pair)
RETURNS pair LANGUAGE SQL
AS 'SELECT ROW(lower($1.k), lower($1.v))::@extschema@.pair;'
SET search_path = pg_temp;

CREATE FUNCTION pair_concat(pair, pair)
RETURNS pair LANGUAGE SQL
AS 'SELECT ROW($1.k OPERATOR(pg_catalog.||) $2.k,
               $1.v OPERATOR(pg_catalog.||) $2.v)::@extschema@.pair;';
```

O arquivo de controle `pair.control` tem a seguinte aparência:

```
# pair extension
comment = 'A key/value pair data type'
default_version = '1.0'
# cannot be relocatable because of use of @extschema@
relocatable = false
```

Embora você não precise de um makefile para instalar esses dois arquivos no diretório correto, você pode usar um `Makefile` contendo o seguinte:

```
EXTENSION = pair
DATA = pair--1.0.sql

PG_CONFIG = pg_config
PGXS := $(shell $(PG_CONFIG) --pgxs)
include $(PGXS)
```

Este makefile depende do PGXS, que é descrito em [Seção 36.18](extend-pgxs.md). O comando `make install` instalará os arquivos de controle e de script no diretório correto, conforme relatado pelo pg_config.

Depois que os arquivos forem instalados, use o comando `CREATE EXTENSION` para carregar os objetos em qualquer banco de dados específico.