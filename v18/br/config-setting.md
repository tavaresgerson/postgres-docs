## 19.1. Configuração de Parâmetros [#](#CONFIG-SETTING)

* [19.1.1. Nomes e Valores dos Parâmetros][(config-setting.md#CONFIG-SETTING-NAMES-VALUES)]
* [19.1.2. Interação do Parâmetro via Arquivo de Configuração][(config-setting.md#CONFIG-SETTING-CONFIGURATION-FILE)]
* [19.1.3. Interação do Parâmetro via SQL][(config-setting.md#CONFIG-SETTING-SQL)]
* [19.1.4. Interação do Parâmetro via Shell][(config-setting.md#CONFIG-SETTING-SHELL)]
* [19.1.5. Gerenciamento do Conteúdo do Arquivo de Configuração][(config-setting.md#CONFIG-INCLUDES)]

### 19.1.1. Nomes e valores dos parâmetros [#](#CONFIG-SETTING-NAMES-VALUES)

Todos os nomes dos parâmetros são sensíveis a maiúsculas e minúsculas. Cada parâmetro recebe um valor de um dos cinco tipos: booleano, string, inteiro, ponto flutuante ou enumerado (enum). O tipo determina a sintaxe para definir o parâmetro:

* *Boolean:* Os valores podem ser escritos como `on`, `off`, `true`, `false`, `yes`, `no`, `1`, `0` (todos sem distinção de maiúsculas e minúsculas) ou qualquer prefixo inequívoco de um desses.
* *String:* Em geral, encerre o valor em aspas duplicadas, se houver aspas dentro do valor. As aspas geralmente podem ser omitidas se o valor for um número simples ou um identificador, no entanto. (Os valores que correspondem a uma palavra-chave SQL requerem citação em alguns contextos.)
* *Numérico (inteiro e ponto flutuante):* Os parâmetros numéricos podem ser especificados nos formatos costumeiros de inteiro e ponto flutuante; os valores fracionários são arredondados para o inteiro mais próximo se o parâmetro for do tipo inteiro. Os parâmetros inteiros também aceitam entrada hexadecimal (começando com `0x`) e entrada octal (começando com `0`), mas esses formatos não podem ter uma fração. Não use separadores de milhares. As aspas não são necessárias, exceto para entrada hexadecimal.
* *Numérico com Unidade:* Alguns parâmetros numéricos têm uma unidade implícita, porque descrevem quantidades de memória ou tempo. A unidade pode ser bytes, kilobytes, blocos (tipicamente oito kilobytes), milissegundos, segundos ou minutos. Um valor numérico não ornamentado para um desses ajustes usará a unidade padrão do ajuste, que pode ser aprendida a partir de `pg_settings`.`unit`. Por conveniência, os ajustes podem ser dados com uma unidade especificada explicitamente, por exemplo `'120 ms'` para um valor de tempo, e eles serão convertidos para o que for a unidade real do parâmetro. Note que o valor deve ser escrito como uma string (com aspas) para usar essa funcionalidade. O nome da unidade é sensível a maiúsculas e minúsculas, e pode haver espaço em branco entre o valor numérico e a unidade.

+ As unidades de memória válidas são `B` (bytes), `kB` (kilobytes), `MB` (megabytes), `GB` (gigabytes) e `TB` (terabytes). O multiplicador para as unidades de memória é 1024, não 1000.
  + As unidades de tempo válidas são `us` (microssegundos), `ms` (milisegundos), `s` (segundos), `min` (minutos), `h` (horas) e `d` (dias).

Se um valor fracionário for especificado com uma unidade, ele será arredondado para um múltiplo da próxima unidade menor, se houver uma. Por exemplo, `30.1 GB` será convertido para `30822 MB` e não para `32319628902 B`. Se o parâmetro for do tipo inteiro, uma arredondamento final para inteiro ocorre após qualquer conversão de unidade.
* *Enumerado:* Os parâmetros de tipo enumerado são escritos da mesma maneira que os parâmetros de string, mas são restritos a ter um dos um conjunto limitado de valores. Os valores permitidos para tal parâmetro podem ser encontrados em `pg_settings`.`enumvals`. Os valores dos parâmetros do tipo enum são sensíveis ao caso.

### 19.1.2. Interação de parâmetros via arquivo de configuração [#](#CONFIG-SETTING-CONFIGURATION-FILE)

A maneira mais fundamental de definir esses parâmetros é editar o arquivo `postgresql.conf`, que normalmente é mantido no diretório de dados. Uma cópia padrão é instalada quando o diretório do clúster do banco de dados é inicializado. Um exemplo do que esse arquivo pode parecer é:

```
# This is a comment
log_connections = all
log_destination = 'syslog'
search_path = '"$user", public'
shared_buffers = 128MB
```

Um parâmetro é especificado por linha. O sinal de igual entre nome e valor é opcional. Espaços em branco são insignificantes (exceto dentro de um valor de parâmetro citado) e linhas em branco são ignoradas. Marcas de hash (`#`) designam o restante da linha como um comentário. Os valores dos parâmetros que não são identificadores ou números simples devem ser citados individualmente. Para incorporar uma citação única em um valor de parâmetro, escreva duas aspas (preferível) ou aspas de barra. Se o arquivo contém várias entradas para o mesmo parâmetro, todas, exceto a última, são ignoradas.

Os parâmetros definidos dessa forma fornecem valores padrão para o clúster. As configurações vistas pelas sessões ativas serão esses valores, a menos que sejam sobrescritos. As seções a seguir descrevem as maneiras pelas quais o administrador ou o usuário pode sobrescrever esses valores padrão.

O arquivo de configuração é lido novamente sempre que o processo do servidor principal recebe um sinal SIGHUP; esse sinal é mais facilmente enviado executando `pg_ctl reload` a partir da linha de comando ou chamando a função SQL `pg_reload_conf()`. O processo do servidor principal também propaga esse sinal para todos os processos de servidor atualmente em execução, de modo que as sessões existentes também adotem os novos valores (isso ocorrerá após elas completarem qualquer comando de cliente atualmente em execução). Alternativamente, você pode enviar o sinal para um único processo de servidor diretamente. Alguns parâmetros só podem ser definidos no início do servidor; quaisquer alterações em suas entradas no arquivo de configuração serão ignoradas até que o servidor seja reiniciado. Configurações de parâmetros inválidas no arquivo de configuração também são ignoradas (mas registradas) durante o processamento do SIGHUP.

Além do `postgresql.conf`, um diretório de dados do PostgreSQL contém um arquivo `postgresql.auto.conf`, que tem o mesmo formato que o `postgresql.conf`, mas é destinado a ser editado automaticamente, não manualmente. Este arquivo contém configurações fornecidas através do comando [`ALTER SYSTEM`(sql-altersystem.md "ALTER SYSTEM")]. Este arquivo é lido sempre que o `postgresql.conf` está presente, e suas configurações entram em vigor da mesma maneira. As configurações em `postgresql.auto.conf` substituem as do `postgresql.conf`.

As ferramentas externas também podem modificar `postgresql.auto.conf`. Não é recomendado fazer isso enquanto o servidor estiver em execução, a menos que [allow_alter_system](runtime-config-compatible.md#GUC-ALLOW-ALTER-SYSTEM) esteja definido como `off`, pois um comando `ALTER SYSTEM` concorrente poderia sobrescrever essas alterações. Essas ferramentas podem simplesmente anexar novos ajustes ao final, ou podem optar por remover configurações duplicadas e/ou comentários (como `ALTER SYSTEM` fará).

A visualização do sistema [[`pg_file_settings`][(view-pg-file-settings.md "53.8. pg_file_settings")]] pode ser útil para testar antecipadamente as alterações nos arquivos de configuração, ou para diagnosticar problemas caso um sinal SIGHUP não tenha produzido os efeitos desejados.

### 19.1.3. Interação de parâmetros via SQL [#](#CONFIG-SETTING-SQL)

O PostgreSQL oferece três comandos SQL para estabelecer configurações padrão. O comando já mencionado `ALTER SYSTEM` fornece um meio de acesso SQL para alterar os padrões globais; ele é funcionalmente equivalente à edição de `postgresql.conf`. Além disso, existem dois comandos que permitem definir padrões em uma base por banco de dados ou por papel:

O comando `ALTER DATABASE` permite que as configurações globais sejam ignoradas em uma base por banco de dados. * O comando `ALTER ROLE` permite que as configurações globais e as configurações por banco de dados sejam ignoradas com valores específicos para o usuário.

Os valores definidos com `ALTER DATABASE` e `ALTER ROLE` são aplicados apenas ao iniciar uma sessão de banco de dados nova. Eles substituem os valores obtidos dos arquivos de configuração ou da linha de comando do servidor e constituem os padrões para o resto da sessão. Observe que alguns ajustes não podem ser alterados após o início do servidor, e, portanto, não podem ser definidos com esses comandos (ou os listados abaixo).

Uma vez que um cliente esteja conectado ao banco de dados, o PostgreSQL fornece dois comandos SQL adicionais (e funções equivalentes) para interagir com as configurações locais de sessão:

O comando `SHOW`(sql-show.md "SHOW") permite a inspeção do valor atual de qualquer parâmetro. A função SQL correspondente é `current_setting(setting_name text)` (consulte [Seção 9.28.1](functions-admin.md#FUNCTIONS-ADMIN-SET "9.28.1. Configuration Settings Functions")).
O comando `SET`(sql-set.md "SET") permite a modificação do valor atual desses parâmetros que podem ser definidos localmente para uma sessão; ele não tem efeito em outras sessões. Muitos parâmetros podem ser definidos dessa forma por qualquer usuário, mas alguns podem ser definidos apenas por superusuários e usuários que receberam o privilégio `SET` nesse parâmetro. A função SQL correspondente é `set_config(setting_name, new_value, is_local)` (consulte [Seção 9.28.1](functions-admin.md#FUNCTIONS-ADMIN-SET "9.28.1. Configuration Settings Functions")).

Além disso, a visualização do sistema [[`pg_settings`][(view-pg-settings.md "53.25. pg_settings")]] pode ser usada para visualizar e alterar os valores locais da sessão:

* Consultar essa visão é semelhante ao uso de `SHOW ALL`, mas fornece mais detalhes. Também é mais flexível, pois é possível especificar condições de filtro ou unir contra outras relações.
* Usar `UPDATE` nessa visão, especificamente atualizando a coluna `setting`, é o equivalente a emitir comandos `SET`. Por exemplo, o equivalente a

  ```
  SET configuration_parameter TO DEFAULT;
  ```

é:

  ```
  UPDATE pg_settings SET setting = reset_val WHERE name = 'configuration_parameter';
  ```

### 19.1.4. Interação de parâmetros via shell [#](#CONFIG-SETTING-SHELL)

Além de definir padrões globais ou anexar sobrescritos no nível do banco de dados ou do papel, você pode passar configurações para o PostgreSQL por meio de recursos do shell. Tanto o servidor quanto a biblioteca de cliente libpq aceitam valores de parâmetros por meio do shell.

* Durante o início do servidor, as configurações dos parâmetros podem ser passadas ao comando `postgres` através do parâmetro de linha de comando `-c name=value`, ou sua variação equivalente `--name=value`. Por exemplo,

  ```
  postgres -c log_connections=all --log-destination='syslog'
  ```

As configurações fornecidas dessa forma substituem as definidas por meio de `postgresql.conf` ou `ALTER SYSTEM`, portanto, não podem ser alteradas globalmente sem reiniciar o servidor.
* Ao iniciar uma sessão de cliente via libpq, as configurações do parâmetro podem ser especificadas usando a variável de ambiente `PGOPTIONS`. As configurações estabelecidas dessa forma constituem os padrões para a vida da sessão, mas não afetam outras sessões. Por razões históricas, o formato de `PGOPTIONS` é semelhante ao usado ao iniciar o comando `postgres`; especificamente, o `-c`, ou o `--` pré-fixado, antes do nome, deve ser especificado. Por exemplo,

  ```
  env PGOPTIONS="-c geqo=off --statement-timeout=5min" psql
  ```

Outros clientes e bibliotecas podem fornecer seus próprios mecanismos, via shell ou de outra forma, que permitam ao usuário alterar as configurações da sessão sem o uso direto de comandos SQL.

### 19.1.5. Gerenciamento do conteúdo do arquivo de configuração [#](#CONFIG-INCLUDES)

O PostgreSQL oferece várias funcionalidades para a quebra de arquivos complexos `postgresql.conf` em subarquivos. Essas funcionalidades são especialmente úteis ao gerenciar vários servidores com configurações relacionadas, mas não idênticas.

Além das configurações de parâmetros individuais, o arquivo `postgresql.conf` pode conter diretivas de *incluir*, que especificam outro arquivo a ser lido e processado como se estivesse inserido no arquivo de configuração neste ponto. Esse recurso permite que um arquivo de configuração seja dividido em partes fisicamente separadas. As diretivas de incluir são simplesmente:

```
include 'filename'
```

Se o nome do arquivo não for um caminho absoluto, ele é considerado relativo ao diretório que contém o arquivo de configuração de referência. As inclusões podem ser aninhadas.

Existe também uma diretiva `include_if_exists`, que funciona da mesma forma que a diretiva `include`, exceto quando o arquivo referenciado não existe ou não pode ser lido. Um `include` regular considerará essa condição como um erro, mas `include_if_exists` apenas registra uma mensagem e continua processando o arquivo de configuração de referência.

O arquivo `postgresql.conf` também pode conter diretivas `include_dir`, que especificam um diretório inteiro de arquivos de configuração a serem incluídos. Essas diretivas parecem

```
include_dir 'directory'
```

Os nomes de diretórios não absolutos são considerados relativos em relação ao diretório que contém o arquivo de configuração de referência. Dentro do diretório especificado, apenas os arquivos que não são diretórios e cujos nomes terminam com o sufixo `.conf` serão incluídos. Os nomes de arquivos que começam com o caractere `.` também são ignorados, para evitar erros, uma vez que esses arquivos são ocultos em algumas plataformas. Múltiplos arquivos dentro de um diretório de inclusão são processados na ordem dos nomes de arquivos (de acordo com as regras do C locale, ou seja, números antes de letras e letras maiúsculas antes de minúsculas).

Pode-se incluir arquivos ou diretórios para separar logicamente porções da configuração do banco de dados, em vez de ter um único grande arquivo `postgresql.conf`. Considere uma empresa que tem dois servidores de banco de dados, cada um com uma quantidade diferente de memória. Há elementos da configuração que ambos compartilharão, como coisas como registro. Mas os parâmetros relacionados à memória no servidor variarão entre os dois. E também pode haver personalizações específicas para o servidor. Uma maneira de gerenciar essa situação é dividir as alterações de configuração personalizadas para o seu site em três arquivos. Você pode adicionar isso ao final do seu arquivo `postgresql.conf` para incluí-los:

```
include 'shared.conf'
include 'memory.conf'
include 'server.conf'
```

Todos os sistemas teriam o mesmo `shared.conf`. Cada servidor com uma quantidade específica de memória poderia compartilhar o mesmo `memory.conf`; você poderia ter um para todos os servidores com 8 GB de RAM, outro para aqueles com 16 GB. E, finalmente, o `server.conf` poderia ter informações de configuração verdadeiramente específicas para o servidor.

Outra possibilidade é criar um diretório de arquivo de configuração e colocar essas informações nele. Por exemplo, um diretório `conf.d` pode ser referenciado no final de `postgresql.conf`:

```
include_dir 'conf.d'
```

Então você pode nomear os arquivos no diretório `conf.d` da seguinte forma:

```
00shared.conf
01memory.conf
02server.conf
```

Essa convenção de nomenclatura estabelece uma ordem clara na qual esses arquivos serão carregados. Isso é importante porque apenas o último ajuste encontrado para um parâmetro específico enquanto o servidor está lendo os arquivos de configuração será usado. Neste exemplo, algo definido em `conf.d/02server.conf` substituiria um valor definido em `conf.d/01memory.conf`.

Você pode, em vez disso, usar essa abordagem para nomear os arquivos de forma descritiva:

```
00shared.conf
01memory-8GB.conf
02server-foo.conf
```

Esse tipo de arranjo dá um nome único para cada variação do arquivo de configuração. Isso pode ajudar a eliminar ambiguidades quando vários servidores têm suas configurações armazenadas em um único lugar, como em um repositório de controle de versão. (Armazenar arquivos de configuração de banco de dados sob controle de versão é outra boa prática a considerar.)