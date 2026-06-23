## psql

psql — Terminal interativo do PostgreSQL

## Sinopse

`psql` [*`option`*...] [*`dbname`* [*`username`*]]

## Descrição

psql é um front-end baseado em terminal para PostgreSQL. Ele permite que você digite interativamente consultas, as emita para o PostgreSQL e veja os resultados das consultas. Alternativamente, a entrada pode ser de um arquivo ou de argumentos da linha de comando. Além disso, o psql oferece vários comandos meta e várias funcionalidades semelhantes a shell para facilitar a escrita de scripts e a automação de uma ampla variedade de tarefas.

## Opções

`-a` `--echo-all` [#](#APP-PSQL-OPTION-ECHO-ALL): Imprima todas as linhas de entrada não vazias no saída padrão conforme elas são lidas. (Isso não se aplica às linhas lidas interativamente.) Isso é equivalente a definir a variável `ECHO` como `all`.

`-A` `--no-align` [#](#APP-PSQL-OPTION-NO-ALIGN): Transfere para o modo de saída não alinhada. (O modo de saída padrão é `aligned`.). Isso é equivalente a `\pset format unaligned`.

`-b` `--echo-errors` [#](#APP-PSQL-OPTION-ECHO-ERRORS): Imprimir comandos SQL de erro para saída padrão de erro. Isso é equivalente a definir a variável `ECHO` para `errors`.

`-c command` `--command=command` [#](#APP-PSQL-OPTION-COMMAND): Especifica que o psql deve executar a string de comando dada, *`command`*. Esta opção pode ser repetida e combinada em qualquer ordem com a opção `-f`. Quando qualquer uma das opções `-c` ou `-f` é especificada, o psql não lê comandos do padrão de entrada; em vez disso, termina após processar todas as opções `-c` e `-f` em sequência.

*`command`* deve ser uma string de comando que seja completamente parsa pelo servidor (ou seja, não contém recursos específicos do psql), ou um único comando de barra invertida. Assim, você não pode misturar SQL e meta-comandos do psql dentro de uma opção `-c`. Para isso, você pode usar opções `-c` repetidas ou canalizar a string para o psql, por exemplo:

```
psql -c '\x' -c 'SELECT * FROM foo;'
```

ou

```
echo '\x \\ SELECT * FROM foo;' | psql
```

(`\\` é o comando meta separador.)

Cada cadeia de comando SQL passada para `-c` é enviada ao servidor como uma única solicitação. Por isso, o servidor a executa como uma única transação, mesmo que a cadeia contenha vários comandos SQL, a menos que haja comandos explícitos de `BEGIN`/`COMMIT` incluídos na cadeia para dividi-la em várias transações. (Consulte [Seção 54.2.2.1] para obter mais detalhes sobre como o servidor lida com cadeias de consultas múltiplas.)

Se não se deseja que vários comandos sejam executados em uma única transação, use comandos `-c` repetidos ou alimente vários comandos no entrada padrão do psql, usando echo como ilustrado acima, ou por meio de um documento de shell, por exemplo:

```
psql <<EOF \x SELECT * FROM foo; EOF
```

`--csv` [#](#APP-PSQL-OPTION-CSV): Transfere para o modo de saída de CSV (Valores separados por vírgula). Isso é equivalente a `\pset format csv`.

`-d dbname` `--dbname=dbname` [#](#APP-PSQL-OPTION-DBNAME): Especifica o nome do banco de dados a ser conectado. Isso é equivalente a especificar *`dbname`* como o primeiro argumento não opcional na linha de comando. O *`dbname`* pode ser uma [string de conexão](libpq-connect.md#LIBPQ-CONNSTRING "32.1.1. Connection Strings"). Se assim for, os parâmetros da string de conexão substituirão quaisquer opções de linha de comando conflitantes.

`-e` `--echo-queries` [#](#APP-PSQL-OPTION-ECHO-QUERIES): Copie todos os comandos SQL enviados ao servidor também para a saída padrão. Isso é equivalente a definir a variável `ECHO` como `queries`.

`-E` `--echo-hidden` [#](#APP-PSQL-OPTION-ECHO-HIDDEN): Repita as consultas reais geradas pelo `\d` e outros comandos de barra invertida. Você pode usar isso para estudar as operações internas do psql. Isso é equivalente a definir a variável `ECHO_HIDDEN` para `on`.

`-f filename` `--file=filename` [#](#APP-PSQL-OPTION-FILE): Leia comandos do arquivo *`filename`*, em vez da entrada padrão. Esta opção pode ser repetida e combinada em qualquer ordem com a opção `-c`. Quando `-c` ou `-f` é especificado, o psql não lê comandos da entrada padrão; em vez disso, termina após processar todas as opções `-c` e `-f` em sequência. Exceto por isso, esta opção é amplamente equivalente ao meta-comando `\i`.

Se *`filename`* for `-` (com hífen), então a entrada padrão é lida até uma indicação de EOF ou comando meta `\q`. Isso pode ser usado para intercalar a entrada interativa com a entrada de arquivos. No entanto, observe que o Readline não é usado neste caso (muito como se `-n` tivesse sido especificado).

Usar essa opção é sutilmente diferente de escrever `psql < filename`. Em geral, ambas farão o que você espera, mas usar `-f` permite algumas funcionalidades interessantes, como mensagens de erro com números de linha. Há também uma pequena chance de que, ao usar essa opção, o overhead de inicialização será reduzido. Por outro lado, a variante que usa a redirecionamento de entrada do shell (teoricamente) garante que produza exatamente a mesma saída que você teria recebido se tivesse digitado tudo à mão.

`-F separator` `--field-separator=separator` [#](#APP-PSQL-OPTION-FIELD-SEPARATOR): Use *`separator`* como separador de campo para saída desalinhada. Isso é equivalente a `\pset fieldsep` ou `\f`.

`-h hostname` `--host=hostname` [#](#APP-PSQL-OPTION-FIELD-HOST): Especifica o nome do host da máquina na qual o servidor está sendo executado. Se o valor começar com uma barra, ele é usado como o diretório para o socket de domínio Unix.

`-H` `--html` [#](#APP-PSQL-OPTION-HTML): Transfere para o modo de saída HTML. Isso é equivalente a `\pset format html` ou ao comando `\H`.

`-l` `--list` [#](#APP-PSQL-OPTION-LIST): Liste todos os bancos de dados disponíveis e, em seguida, saia. Outras opções que não envolvem conexão são ignoradas. Isso é semelhante ao comando meta `\list`.

Quando esta opção é usada, o psql se conectará ao banco de dados `postgres`, a menos que um banco de dados diferente seja nomeado na linha de comando (opção `-d` ou argumento não opção, possivelmente através de uma entrada de serviço, mas não através de uma variável de ambiente).

`-L filename` `--log-file=filename` [#](#APP-PSQL-OPTION-LOG-FILE): Escreva todas as saídas da consulta no arquivo *`filename`*, além do destino normal de saída.

`-n` `--no-readline` [#](#APP-PSQL-OPTION-NO-READLINE): Não use o Readline para edição de linha e não use o histórico de comandos (consulte a seção chamada “Edição de linha de comando”](app-psql.md#APP-PSQL-READLINE "Command-Line Editing") abaixo).

`-o filename` `--output=filename` [#](#APP-PSQL-OPTION-OUTPUT): Coloque todas as saídas da consulta em arquivo *`filename`*. Isso é equivalente ao comando `\o`.

`-p port` `--port=port` [#](#APP-PSQL-OPTION-PORT): Especifica a porta TCP ou a extensão de arquivo de socket de domínio Unix local na qual o servidor está aguardando conexões. Tem como padrão o valor da variável de ambiente `PGPORT` ou, se não definida, a porta especificada no momento da compilação, geralmente 5432.

`-P assignment` `--pset=assignment` [#](#APP-PSQL-OPTION-PSET): Especifica opções de impressão, no estilo de `\pset`. Observe que, aqui, você deve separar nome e valor com um sinal de igual em vez de um espaço. Por exemplo, para definir o formato de saída para LaTeX, você poderia escrever `-P format=latex`.

`-q` `--quiet` [#](#APP-PSQL-OPTION-QUIET): Especifica que o psql deve realizar seu trabalho silenciosamente. Por padrão, ele imprime mensagens de boas-vindas e várias saídas informativas. Se esta opção for usada, nada disso acontece. Isso é útil com a opção `-c`. Isso é equivalente a definir a variável `QUIET` para `on`.

`-R separator` `--record-separator=separator` [#](#APP-PSQL-OPTION-RECORD-SEPARATOR): Use *`separator`* como o separador de registro para saída não alinhada. Isso é equivalente a `\pset recordsep`.

`-s` `--single-step` [#](#APP-PSQL-OPTION-SINGLE-STEP): Execute no modo de uma única etapa. Isso significa que o usuário é solicitado antes de cada comando ser enviado ao servidor, com a opção de cancelar a execução também. Use isso para depurar scripts.

`-S` `--single-line` [#](#APP-PSQL-OPTION-SINGLE-LINE): Funciona no modo de linha única, onde uma nova linha termina um comando SQL, assim como um ponto e vírgula.

### Nota

Este modo é fornecido para aqueles que insistem em usá-lo, mas você não é necessariamente encorajado a usá-lo. Em particular, se você misturar SQL e comandos meta em uma linha, a ordem de execução pode não ser sempre clara para o usuário inexperiente.

`-t` `--tuples-only` [#](#APP-PSQL-OPTION-TUPLES-ONLY): Desative a impressão de rodapés com nomes de colunas e contagem de linhas de resultado, etc. Isso é equivalente a `\t` ou `\pset tuples_only`.

`-T table_options` `--table-attr=table_options` [#](#APP-PSQL-OPTION-TABLE-ATTR): Especifica as opções a serem colocadas dentro da tag HTML `table`. Consulte `\pset tableattr` para detalhes.

`-U username` `--username=username` [#](#APP-PSQL-OPTION-USERNAME): Conecte-se ao banco de dados como o usuário *`username`* em vez do padrão. (É claro que você deve ter permissão para fazer isso.)

`-v assignment` `--set=assignment` `--variable=assignment` [#](#APP-PSQL-OPTION-VARIABLE): Realize uma atribuição de variável, como o comando meta `\set`. Observe que você deve separar o nome e o valor, se houver, com um sinal de igual na linha de comando. Para desativar uma variável, não use o sinal de igual. Para definir uma variável com um valor vazio, use o sinal de igual, mas não o valor. Essas atribuições são feitas durante o processamento da linha de comando, então as variáveis que refletem o estado de conexão serão sobrescritas mais tarde.

`-V` `--version` [#](#APP-PSQL-OPTION-VERSION): Imprimir a versão do psql e sair.

`-w` `--no-password` [#](#APP-PSQL-OPTION-NO-PASSWORD): Nunca emita um prompt de senha. Se o servidor exigir autenticação por senha e não houver senha disponível em outras fontes, como um arquivo `.pgpass`, a tentativa de conexão falhará. Esta opção pode ser útil em trabalhos em lote e scripts onde não há usuário presente para inserir uma senha.

Observe que essa opção permanecerá definida durante toda a sessão, e, portanto, afeta o uso do meta-comando `\connect`, bem como a tentativa inicial de conexão.

`-W` `--password` [#](#APP-PSQL-OPTION-PASSWORD): Forçar o psql a solicitar uma senha antes de se conectar a um banco de dados, mesmo que a senha não seja usada.

Se o servidor exigir autenticação por senha e uma senha não estiver disponível de outras fontes, como um arquivo `.pgpass`, o psql solicitará uma senha em qualquer caso. No entanto, o psql desperdiçará uma tentativa de conexão descobrindo que o servidor deseja uma senha. Em alguns casos, vale a pena digitar [[`-W`] para evitar a tentativa de conexão extra.

Observe que essa opção permanecerá definida durante toda a sessão, e, portanto, afeta o uso do meta-comando `\connect` e a tentativa inicial de conexão.

`-x` `--expanded` [#](#APP-PSQL-OPTION-EXPANDED): Ative o modo de formatação de tabela expandida. Isso é equivalente a `\x` ou `\pset expanded`.

`-X` `--no-psqlrc` [#](#APP-PSQL-OPTION-NO-PSQLRC): Não leia o arquivo de inicialização (nem o arquivo de nível de sistema `psqlrc`, nem o arquivo de usuário `~/.psqlrc`).

`-z` `--field-separator-zero` [#](#APP-PSQL-OPTION-FIELD-SEPARATOR-ZERO): Defina o separador de campo para saída não alinhada em um byte zero. Isso é equivalente a `\pset fieldsep_zero`.

`-0` `--record-separator-zero` [#](#APP-PSQL-OPTION-RECORD-SEPARATOR-ZERO): Defina o separador de registro para saída não alinhada em um byte zero. Isso é útil para a interconexão, por exemplo, com `xargs -0`. Isso é equivalente a `\pset recordsep_zero`.

`-1` `--single-transaction` [#](#APP-PSQL-OPTION-SINGLE-TRANSACTION): Esta opção só pode ser usada em combinação com uma ou mais opções `-c` e/ou `-f`. Ela faz com que o psql emita um comando `BEGIN` antes da primeira opção desse tipo e um comando `COMMIT` após a última, envolvendo assim todos os comandos em uma única transação. Se qualquer um dos comandos falhar e a variável `ON_ERROR_STOP` tiver sido definida, um comando `ROLLBACK` é enviado em vez disso. Isso garante que todos os comandos sejam concluídos com sucesso ou que nenhuma mudança seja aplicada.

Se os próprios comandos contiverem `BEGIN`, `COMMIT` ou `ROLLBACK`, esta opção não terá os efeitos desejados. Além disso, se um comando individual não puder ser executado dentro de um bloco de transação, especificar esta opção fará com que toda a transação falhe.

`-?` `--help[=topic]` [#](#APP-PSQL-OPTION-HELP): Mostrar ajuda sobre psql e sair. O parâmetro opcional *`topic`* (com padrão para `options`) seleciona qual parte do psql é explicada: `commands` descreve os comandos de barra invertida do psql; `options` descreve as opções de linha de comando que podem ser passadas ao psql; e `variables` mostra ajuda sobre as variáveis de configuração do psql.

## Status de saída

psql retorna 0 para o shell se terminou normalmente, 1 se ocorrer um erro fatal próprio (por exemplo, sem memória, arquivo não encontrado), 2 se a conexão com o servidor falhar e a sessão não for interativa, e 3 se ocorrer um erro em um script e a variável `ON_ERROR_STOP` foi definida.

## Uso

### Conectando-se a um banco de dados

psql é uma aplicação regular de cliente PostgreSQL. Para se conectar a um banco de dados, você precisa saber o nome do banco de dados alvo, o nome do host e o número de porta do servidor, e qual nome de usuário do banco de dados você deseja se conectar como. O psql pode ser informado sobre esses parâmetros via opções de linha de comando, especificamente `-d`, `-h`, `-p` e `-U`, respectivamente. Se for encontrado um argumento que não pertence a nenhuma opção, ele será interpretado como o nome do banco de dados (ou o nome de usuário do banco de dados, se o nome do banco de dados já for dado). Nem todas essas opções são necessárias; há opções padrão úteis. Se você omitir o nome do host, o psql se conectará via socket de domínio Unix a um servidor no host local, ou via TCP/IP a `localhost` em Windows. O número de porta padrão é determinado no momento da compilação. Como o servidor de banco de dados usa o mesmo padrão, você não terá que especificar a porta na maioria dos casos. O nome padrão de usuário do banco de dados é o nome do usuário do seu sistema operacional. Uma vez que o nome de usuário do banco de dados é determinado, ele é usado como o nome padrão do banco de dados. Note que você não pode simplesmente se conectar a qualquer banco de dados sob qualquer nome de usuário do banco de dados. Seu administrador de banco de dados deve ter informado sobre seus direitos de acesso.

Quando os valores não estiverem corretos, você pode economizar algumas digitações definindo as variáveis de ambiente `PGDATABASE`, `PGHOST`, `PGPORT` e/ou `PGUSER` para valores apropriados. (Para variáveis de ambiente adicionais, consulte [Seção 32.15](libpq-envars.md). É também conveniente ter um arquivo `~/.pgpass` para evitar a necessidade de digitar senhas regularmente. Consulte [Seção 32.16](libpq-pgpass.md) para obter mais informações.

Uma maneira alternativa de especificar os parâmetros de conexão é em uma string *`conninfo`* ou um URI, que é usado em vez do nome do banco de dados. Esse mecanismo oferece um controle muito amplo sobre a conexão. Por exemplo:

```
$ psql "service=myservice sslmode=require" $ psql postgresql://dbmaster:5433/mydb?sslmode=require
```

Dessa forma, você também pode usar o LDAP para procurar parâmetros de conexão, conforme descrito em [Seção 32.18](libpq-ldap.md). Consulte [Seção 32.1.2](libpq-connect.md#LIBPQ-PARAMKEYWORDS) para obter mais informações sobre todas as opções de conexão disponíveis.

Se a conexão não puder ser feita por qualquer motivo (por exemplo, privilégios insuficientes, o servidor não está em execução no host alvo, etc.), o psql retornará um erro e terminará.

Se tanto a entrada padrão quanto a saída padrão forem um terminal, o psql define o codificação do cliente como “auto”, que detectará a codificação apropriada do cliente a partir das configurações de local (`LC_CTYPE` variável de ambiente em sistemas Unix). Se isso não funcionar conforme o esperado, a codificação do cliente pode ser substituída usando a variável de ambiente `PGCLIENTENCODING`.

### Digitação de comandos SQL

Em operação normal, o psql fornece um prompt com o nome do banco de dados ao qual o psql está conectado atualmente, seguido pela string `=>`. Por exemplo:

```
$ psql testdb psql (18.4) Type "help" for help.

testdb=>
```

Ao receber a solicitação, o usuário pode digitar comandos SQL. Normalmente, as linhas de entrada são enviadas ao servidor quando um ponto-e-vírgula que termina um comando é alcançado. O fim de linha não termina um comando. Assim, os comandos podem ser espalhados por várias linhas para maior clareza. Se o comando foi enviado e executado sem erro, os resultados do comando são exibidos na tela.

Se usuários não confiáveis tiverem acesso a um banco de dados que não adotou um padrão de uso de esquema seguro (ddl-schemas.md#DDL-SCHEMAS-PATTERNS "5.10.6. Usage Patterns"), comece sua sessão removendo esquemas que podem ser escritos publicamente de `search_path`. Pode-se adicionar `options=-csearch_path=` à string de conexão ou emitir `SELECT pg_catalog.set_config('search_path', '', false)` antes de outros comandos SQL. Esta consideração não é específica do psql; ela se aplica a todas as interfaces para executar comandos SQL arbitrários.

Sempre que um comando é executado, o psql também verifica eventos de notificação assíncrona gerados por `LISTEN` e (sql-listen.md "LISTEN") e `NOTIFY` e (sql-notify.md "NOTIFY").

Enquanto os comentários em estilo C são passados ao servidor para processamento e remoção, os comentários padrão do SQL são removidos pelo psql.

### Comandos Meta

Qualquer coisa que você digite no psql que começa com uma barra invertida não citada é um metacomando do psql que é processado pelo próprio psql. Esses comandos tornam o psql mais útil para administração ou script. Meta-comandos são frequentemente chamados de comandos de barra ou barra invertida.

O formato de um comando psql é o traço, seguido imediatamente por um verbo de comando, e depois quaisquer argumentos. Os argumentos são separados do verbo de comando e uns dos outros por qualquer número de caracteres de espaço em branco.

Para incluir espaços em branco em um argumento, você pode citar-o com aspas simples. Para incluir uma única aspa em um argumento, escreva duas aspas simples dentro de texto com aspas simples. Tudo contido em aspas também está sujeito a substituições semelhantes às do C para `\n` (nova linha), `\t` (tab), `\b` (apagar), `\r` (retorno de carro), `\f` (alimentação de formulário), `\`*`digits`* (octal) e `\x`*`digits`* (hexadecimal). Uma barra invertida que precede qualquer outro caractere dentro de texto com aspas simples cita esse caractere simples, seja o que for.

Se um ponto e vírgula não citado (`:`) seguido por um nome de variável psql aparecer dentro de um argumento, ele é substituído pelo valor da variável, conforme descrito em [Interpolação SQL](app-psql.md#APP-PSQL-INTERPOLATION) abaixo. As formas `:'variable_name'` e `:"variable_name"` descritas lá também funcionam. A sintaxe `:{?variable_name}` permite testar se uma variável está definida. Ela é substituída por VERDADEIRO ou FALSO. Esquivar o ponto e vírgula com uma barra invertida o protege da substituição.

Dentro de um argumento, o texto que está encerrado entre aspas (`` ` ``) is taken as a command line that is passed to the shell. The output of the command (with any trailing newline removed) replaces the backquoted text. Within the text enclosed in backquotes, no special quoting or other processing occurs, except that appearances of `:variable_name` where *`variable_name`* is a psql variable name are replaced by the variable's value. Also, appearances of `:'variable_name'` are replaced by the variable's value suitably quoted to become a single shell command argument. (The latter form is almost always preferable, unless you are very sure of what is in the variable.) Because carriage return and line feed characters cannot be safely quoted on all platforms, the `:'variable_name'` forma uma mensagem de erro e não substitui o valor da variável quando tais caracteres aparecem no valor.

Alguns comandos aceitam um identificador SQL (como o nome de uma tabela) como argumento. Esses argumentos seguem as regras de sintaxe do SQL: letras não citadas são forçadas a minúsculas, enquanto as aspas duplas (`"`) protegem as letras da conversão de maiúsculas e permitem a incorporação de espaços em branco no identificador. Dentro de aspas duplas, as aspas duplas emparelhadas reduzem a uma única aspa dupla no nome resultante. Por exemplo, `FOO"BAR"BAZ` é interpretado como `fooBARbaz`, e `"A weird"" name"` se torna `A weird" name`.

A análise de argumentos para o final da linha ou quando outra barra invertida não citada é encontrada. Uma barra invertida não citada é considerada o início de um novo comando meta. A sequência especial `\\` (duas barras invertidas) marca o final dos argumentos e continua a análise de comandos SQL, se houver. Dessa forma, comandos SQL e psql podem ser misturados livremente em uma linha. Mas, em qualquer caso, os argumentos de um comando meta não podem continuar além do final da linha.

Muitos dos comandos meta atuam no *buffer de consulta atual*. Isso é simplesmente um buffer que contém qualquer texto de comando SQL digitado, mas ainda não enviado ao servidor para execução. Isso incluirá as linhas de entrada anteriores, bem como qualquer texto que apareça antes do comando meta na mesma linha.

Muitos dos comandos meta também permitem que `x` seja anexado como uma opção. Isso fará com que os resultados sejam exibidos em modo expandido, como se `\x` ou `\pset expanded` tivesse sido usado.

Os seguintes comandos meta são definidos:

`\a` [#](#APP-PSQL-META-COMMAND-A): Se o formato atual de saída da tabela não estiver alinhado, ele é alterado para alinhado. Se não estiver desalinhado, ele é definido como desalinhado. Este comando é mantido para compatibilidade reversa. Consulte `\pset` para uma solução mais geral.

`\bind` [ *`parameter`* ] ... [#](#APP-PSQL-META-COMMAND-BIND): Define os parâmetros de consulta para a próxima execução da consulta, com os parâmetros especificados passados para quaisquer marcadores de parâmetros (`$1` etc.).

Exemplo:

```
INSERT INTO tbl1 VALUES ($1, $2) \bind 'first value' 'second value' \g
```

Isso também funciona para comandos de execução de consulta além do `\g`, como `\gx` e `\gset`.

Este comando faz com que o protocolo de consulta estendida (consulte [Seção 54.1.2](protocol-overview.md#PROTOCOL-QUERY-CONCEPTS)) seja usado, ao contrário da operação normal do psql, que usa o protocolo de consulta simples. Portanto, este comando pode ser útil para testar o protocolo de consulta estendida do psql. (O protocolo de consulta estendida é usado mesmo que a consulta não tenha parâmetros e este comando especifique zero parâmetros.) Este comando afeta apenas a próxima consulta executada; todas as consultas subsequentes usarão o protocolo de consulta simples por padrão.

`\bind_named` *`statement_name`* [ *`parameter`* ] ... [#](#APP-PSQL-META-COMMAND-BIND-NAMED): `\bind_named` é equivalente a `\bind`, exceto que ele recebe o nome de uma declaração preparada existente como primeiro parâmetro. Uma string vazia denota a declaração preparada sem nome.

Exemplo:

```
INSERT INTO tbls1 VALUES ($1, $2) \parse stmt1 \bind_named stmt1 'first value' 'second value' \g
```

Este comando faz com que o protocolo de consulta estendida (veja [Seção 54.1.2](protocol-overview.md#PROTOCOL-QUERY-CONCEPTS)) seja usado, ao contrário da operação normal do psql, que usa o protocolo de consulta simples. Portanto, este comando pode ser útil para testar o protocolo de consulta estendida do psql.

`\c` ou `\connect [ -reuse-previous=on|off ] [ dbname [ username ] [ host ] [ port ] | conninfo ]` [#](#APP-PSQL-META-COMMAND-C-LC): Estabelece uma nova conexão a um servidor PostgreSQL. Os parâmetros de conexão a serem usados podem ser especificados usando uma sintaxe posicional (um ou mais nomes de banco de dados, usuário, host e porta), ou usando uma *`conninfo`* cadeia de conexão conforme detalhado em [Seção 32.1.1](libpq-connect.md#LIBPQ-CONNSTRING "32.1.1. Connection Strings"). Se não forem fornecidos argumentos, uma nova conexão é feita usando os mesmos parâmetros que antes.

Especificar qualquer um dos seguintes: *`dbname`*, *`username`*, *`host`* ou *`port`* como `-` é equivalente a omitir esse parâmetro.

A nova conexão pode reutilizar os parâmetros de conexão da conexão anterior; não apenas o nome do banco de dados, o usuário, o host e a porta, mas também outros ajustes, como *`sslmode`*. Por padrão, os parâmetros são reutilizados na sintaxe posicional, mas não quando é dada uma string *`conninfo`*. Passar um primeiro argumento de `-reuse-previous=on` ou `-reuse-previous=off` substitui esse padrão. Se os parâmetros forem reutilizados, qualquer parâmetro não especificado explicitamente como um parâmetro posicional ou na string *`conninfo`* será retirado dos parâmetros da conexão existente. Uma exceção é que, se a configuração *`host`* for alterada de seu valor anterior usando a sintaxe posicional, qualquer configuração *`hostaddr`* presente nos parâmetros da conexão existente será descartada. Além disso, qualquer senha usada para a conexão existente será reutilizada apenas se os ajustes de usuário, host e porta não forem alterados. Quando o comando não especifica nem reutiliza um parâmetro particular, o padrão do libpq é usado.

Se a nova conexão for feita com sucesso, a conexão anterior é fechada. Se a tentativa de conexão falhar (nome de usuário errado, acesso negado, etc.), a conexão anterior será mantida se o psql estiver em modo interativo. Mas ao executar um script não interativo, a conexão antiga é fechada e um erro é relatado. Isso pode ou não encerrar o script; se não, todos os comandos de acesso ao banco de dados falharão até que outro comando `\connect` seja executado com sucesso. Essa distinção foi escolhida como uma conveniência para o usuário contra erros de digitação, por um lado, e um mecanismo de segurança de que os scripts não estão acidentalmente agindo na base de dados errada, por outro lado. Note que sempre que um comando `\connect` tenta reutilizar parâmetros, os valores reutilizados são os da última conexão bem-sucedida, não de quaisquer tentativas falhadas feitas posteriormente. No entanto, no caso de uma falha não interativa `\connect`, não é permitido reutilizar parâmetros posteriormente, uma vez que o script provavelmente esperaria que os valores do `\connect` falhado sejam reutilizados.

Exemplos:

```
=> \c mydb myuser host.dom 6432 => \c service=foo => \c "host=localhost port=5432 dbname=mydb connect_timeout=10 sslmode=disable" => \c -reuse-previous=on sslmode=require    -- changes only sslmode => \c postgresql://tom@localhost/mydb?application_name=myapp
```

`\C [ title ]` [#](#APP-PSQL-META-COMMAND-C-UC) :   Define o título de quaisquer tabelas que serão impressas como resultado de uma consulta ou desativa qualquer título. Este comando é equivalente a `\pset title title`. (O nome deste comando deriva de "caption", pois anteriormente era usado apenas para definir a legenda em uma tabela HTML.)

`\cd [ directory ]` [#](#APP-PSQL-META-COMMAND-CD) Altera o diretório de trabalho atual para *`directory`*. Sem argumento, altera o diretório de usuário atual. Para obter detalhes sobre como os diretórios de usuário são encontrados, consulte [Seção 32.16](libpq-pgpass.md "32.16. The Password File").

### DICA

Para imprimir o diretório de trabalho atual, use `\! pwd`.

`\close_prepared` *`prepared_statement_name`* [#](#APP-PSQL-META-COMMAND-CLOSE-PREPARED): Fecha a declaração preparada especificada. Uma string vazia denota a declaração preparada sem nome. Se não existir nenhuma declaração preparada com este nome, a operação é uma operação sem efeito.

Exemplo:

```
SELECT $1 \parse stmt1 \close_prepared stmt1
```

Este comando faz com que o protocolo de consulta estendida seja usado, ao contrário da operação normal do psql, que usa o protocolo de consulta simples. Portanto, este comando pode ser útil para testar o protocolo de consulta estendida a partir do psql.

`\conninfo` [#](#APP-PSQL-META-COMMAND-CONNINFO): Exibe informações sobre a conexão atual do banco de dados, incluindo informações relacionadas ao SSL, se o SSL estiver em uso.

Observe que o campo `Client User` mostra o usuário no momento da conexão, enquanto o campo `Superuser` indica se o usuário atual (no contexto de execução atual) possui privilégios de superusuário. Esses usuários geralmente são os mesmos, mas podem diferir, por exemplo, se o usuário atual foi alterado com o comando `SET ROLE`.

Realiza uma cópia do frontend (cliente). Esta é uma operação que executa um comando SQL `COPY`(sql-copy.md "COPY") , mas em vez de o servidor ler ou escrever o arquivo especificado, psql lê ou escreve o arquivo e encaminha os dados entre o servidor e o sistema de arquivos local. Isso significa que a acessibilidade e os privilégios do arquivo são os do usuário local, não do servidor, e não são necessárias privilégios de superusuário SQL.

Quando `program` é especificado, *`command`* é executado pelo psql e os dados passados de ou para *`command`* são encaminhados entre o servidor e o cliente. Novamente, os privilégios de execução são os do usuário local, não do servidor, e não são necessários privilégios de superusuário do SQL.

Para `\copy ... from stdin`, as linhas de dados são lidas da mesma fonte que emitiu o comando, continuando até que uma linha contendo apenas `\.` seja lida ou o fluxo atinja o fim de arquivo. Esta opção é útil para preencher tabelas em linha dentro de um arquivo de script SQL. Para `\copy ... to stdout`, a saída é enviada para o mesmo local que a saída do comando psql e o status do comando `COPY count` não é impresso (já que pode ser confundido com uma linha de dados). Para ler/escrever a entrada ou saída padrão do psql, independentemente da fonte do comando atual ou da opção `\o`, escreva `from pstdin` ou `to pstdout`.

A sintaxe deste comando é semelhante à do comando `COPY`(sql-copy.md "COPY"). Todas as opções, exceto a fonte/destino dos dados, são especificadas para `COPY`. Por isso, regras de análise especiais se aplicam ao comando `\copy` meta. Ao contrário da maioria dos outros comandos meta, todo o restante da linha é sempre considerado os argumentos de `\copy`, e nem a interpolação de variáveis nem a expansão de aspas são realizadas nos argumentos.

### DICA

Outra maneira de obter o mesmo resultado que `\copy ... to` é usar o comando SQL `COPY ... TO STDOUT` e terminá-lo com `\g filename` ou `\g |program`. Ao contrário de `\copy`, este método permite que o comando abranja várias linhas; também, a interpolação de variáveis e a expansão de aspas podem ser usadas.

### DICA

Essas operações não são tão eficientes quanto o comando `COPY` com uma fonte de dados de arquivo ou programa, ou destino, porque todos os dados devem passar pela conexão cliente/servidor. Para grandes quantidades de dados, o comando SQL pode ser preferível.

`\copyright` [#](#APP-PSQL-META-COMMAND-COPYRIGHT) :   Mostra os direitos autorais e as condições de distribuição do PostgreSQL.

`\crosstabview [ colV [ colH [ colD [ sortcolH ] ] ] ]` [#](#APP-PSQL-META-COMMANDS-CROSSTABVIEW): Executa o buffer de consulta atual (como `\g`) e mostra os resultados em uma grade crosstab. A consulta deve retornar pelo menos três colunas. A coluna de saída identificada por *`colV`* tornar-se um cabeçalho vertical e a coluna de saída identificada por *`colH`* tornar-se um cabeçalho horizontal. *`colD`* identifica a coluna de saída para exibir na grade. *`sortcolH`* identifica uma coluna de classificação opcional para o cabeçalho horizontal.

Cada especificação de coluna pode ser um número de coluna (começando em 1) ou um nome de coluna. As regras usuais de dobramento de caso e citação de SQL se aplicam aos nomes de colunas. Se omitido, *`colV`* é considerado como a coluna 1 e *`colH`* como a coluna 2. *`colH`* deve diferir de *`colV`*. Se *`colD`* não for especificado, então deve haver exatamente três colunas no resultado da consulta, e a coluna que não é *`colV`* nem *`colH`* é considerada como *`colD`*.

O cabeçalho vertical, exibido como a coluna mais à esquerda, contém os valores encontrados na coluna *`colV`*, na mesma ordem dos resultados da consulta, mas com os duplicados removidos.

O cabeçalho horizontal, exibido como a primeira linha, contém os valores encontrados na coluna *`colH`*, com os duplicados removidos. Por padrão, esses valores aparecem na mesma ordem que os resultados da consulta. Mas, se o argumento opcional *`sortcolH`* for fornecido, ele identifica uma coluna cujos valores devem ser números inteiros, e os valores de *`colH`* aparecerão no cabeçalho horizontal, classificados de acordo com os valores correspondentes de *`sortcolH`*.

Dentro da grade de cruzamento, para cada valor distinto `x` de *`colH`* e para cada valor distinto `y` de *`colV`*, a célula localizada na interseção `(x,y)` contém o valor da coluna `colD` na linha do resultado da consulta para a qual o valor de *`colH`* `x` e o valor `colV` `y` é. Se não houver tal linha, a célula está vazia. Se haver várias dessas linhas, um erro é relatado.

`\d[Sx+] [ pattern ]` [#](#APP-PSQL-META-COMMAND-D): Para cada relação (tabela, visão, visão materializada, índice, sequência ou tabela estrangeira) ou tipo composto que corresponda ao *`pattern`*, mostre todas as colunas, seus tipos, o espaço de tabela (se não for o padrão) e quaisquer atributos especiais, como `NOT NULL` ou padrões. Indica-se também os índices associados, restrições, regras e gatilhos. Para tabelas estrangeiras, o servidor estrangeiro associado também é mostrado.

("Correspondendo ao padrão" é definido em [Padrões](app-psql.md#APP-PSQL-PATTERNS "Patterns") abaixo.)

Para alguns tipos de relação, `\d` mostra informações adicionais para cada coluna: valores de coluna para sequências, expressões indexadas para índices e opções de wrapper de dados externos para tabelas externas.

O formulário de comando `\d+` é idêntico, exceto que: são exibidas mais informações: quaisquer comentários associados às colunas da tabela, a presença de OIDs na tabela, a definição da visão, se a relação for uma visão, uma configuração não padrão de [identidade de replica](sql-altertable.md#SQL-ALTERTABLE-REPLICA-IDENTITY) e o nome do [método de acesso](sql-create-access-method.md) se a relação tiver um método de acesso.

Por padrão, apenas os objetos criados pelo usuário são mostrados; forneça um padrão ou o modificador `S` para incluir objetos do sistema.

### Nota

Se `\d` for usado sem um argumento *`pattern`*, é equivalente a `\dtvmsE`, que mostrará uma lista de todas as tabelas, visualizações, visualizações materializadas, sequências e tabelas externas visíveis. Essa é uma medida de conveniência.

Assim como muitos outros comandos, se `x` for anexado ao nome do comando, os resultados são exibidos em modo expandido, mas observe que isso só se aplica quando `\d` é usado sem um argumento de *`pattern`* e o modificador `x` não pode aparecer imediatamente após o `\d` (porque `\dx` é um comando diferente); o modificador `x` pode aparecer apenas após um modificador `S` ou `+`. Por exemplo, `\d+x` é equivalente a `\dtvmsE+x` e mostrará uma lista de todas as relações em modo expandido.

`\da[Sx] [ pattern ]` [#](#APP-PSQL-META-COMMAND-DA-LC): Listas funções agregadas, juntamente com seu tipo de retorno e os tipos de dados nos quais elas operam. Se *`pattern`* for especificado, apenas os agregados cujos nomes correspondem ao padrão são mostrados. Por padrão, apenas objetos criados pelo usuário são mostrados; forneça um padrão ou o modificador `S` para incluir objetos do sistema. Se `x` for anexado ao nome do comando, os resultados são exibidos no modo expandido.

`\dA[x+] [ pattern ]` [#](#APP-PSQL-META-COMMAND-DA-UC): Lista os métodos de acesso. Se *`pattern`* for especificado, apenas os métodos de acesso cujos nomes correspondem ao padrão são mostrados. Se `x` for anexado ao nome do comando, os resultados são exibidos no modo expandido. Se `+` for anexado ao nome do comando, cada método de acesso é listado com sua função de manipulador associada e descrição.

`\dAc[x+] [access-method-pattern [input-type-pattern]]` [#](#APP-PSQL-META-COMMAND-DAC): Listas de classes de operador (consulte [Seção 36.16.1](xindex.md#XINDEX-OPCLASS "36.16.1. Index Methods and Operator Classes")). Se *`access-method-pattern`* for especificado, apenas as classes de operador associadas aos métodos de acesso cujos nomes correspondem a esse padrão são listadas. Se *`input-type-pattern`* for especificado, apenas as classes de operador associadas aos tipos de entrada cujos nomes correspondem a esse padrão são listadas. Se `x` for anexado ao nome do comando, os resultados são exibidos em modo expandido. Se `+` for anexado ao nome do comando, cada classe de operador é listada com sua família de operador associada e proprietário.

`\dAf[x+] [access-method-pattern [input-type-pattern]]` [#](#APP-PSQL-META-COMMAND-DAF): Lista de famílias de operadores (ver [Seção 36.16.5](xindex.md#XINDEX-OPFAMILY "36.16.5. Operator Classes and Operator Families")). Se *`access-method-pattern`* for especificado, apenas as famílias de operadores associadas aos métodos de acesso cujos nomes correspondem a esse padrão são listadas. Se *`input-type-pattern`* for especificado, apenas as famílias de operadores associadas aos tipos de entrada cujos nomes correspondem a esse padrão são listadas. Se `x` for anexado ao nome do comando, os resultados são exibidos em modo expandido. Se `+` for anexado ao nome do comando, cada família de operadores é listada com seu proprietário.

`\dAo[x+] [access-method-pattern [operator-family-pattern]]` [#](#APP-PSQL-META-COMMAND-DAO): Lista de operadores associados a famílias de operadores (consulte [Seção 36.16.2](xindex.md#XINDEX-STRATEGIES "36.16.2. Index Method Strategies")). Se *`access-method-pattern`* for especificado, apenas os membros das famílias de operadores associados a métodos de acesso cujo nome corresponda a esse padrão são listados. Se *`operator-family-pattern`* for especificado, apenas os membros das famílias de operadores cujo nome corresponda a esse padrão são listados. Se `x` for anexada ao nome do comando, os resultados são exibidos em modo expandido. Se `+` for anexada ao nome do comando, cada operador é listado com sua família de operadores de classificação (se for um operador de ordenação), e se sua função subjacente é à prova de vazamento.

`\dAp[x+] [access-method-pattern [operator-family-pattern]]` [#](#APP-PSQL-META-COMMAND-DAP): Funções de suporte para listas associadas a famílias de operadores (consulte [Seção 36.16.3](xindex.md#XINDEX-SUPPORT "36.16.3. Index Method Support Routines")). Se *`access-method-pattern`* for especificado, apenas as funções de famílias de operadores associadas a métodos de acesso cujos nomes correspondem a esse padrão são listadas. Se *`operator-family-pattern`* for especificado, apenas as funções de famílias de operadores cujos nomes correspondem a esse padrão são listadas. Se `x` for anexado ao nome do comando, os resultados são exibidos em modo expandido. Se `+` for anexado ao nome do comando, as funções são exibidas verbosemente, com suas listas de parâmetros reais.

`\db[x+] [ pattern ]` [#](#APP-PSQL-META-COMMAND-DB): Lista espaços de tabela. Se *`pattern`* for especificado, apenas os espaços de tabela cujos nomes correspondem ao padrão são mostrados. Se `x` for anexado ao nome do comando, os resultados são exibidos no modo expandido. Se `+` for anexado ao nome do comando, cada espaço de tabela é listado com suas opções associadas, tamanho no disco, permissões e descrição.

`\dc[Sx+] [ pattern ]` [#](#APP-PSQL-META-COMMAND-DC-LC): Lista de conversões entre codificações de conjuntos de caracteres. Se *`pattern`* for especificado, apenas as conversões cujos nomes correspondem ao padrão são listadas. Por padrão, apenas os objetos criados pelo usuário são mostrados; forneça um padrão ou o modificador `S` para incluir objetos do sistema. Se `x` for anexado ao nome do comando, os resultados são exibidos no modo expandido. Se `+` for anexado ao nome do comando, cada objeto é listado com sua descrição associada.

`\dconfig[x+] [ pattern ]` [#](#APP-PSQL-META-COMMAND-DCONFIG): Lista os parâmetros de configuração do servidor e seus valores. Se *`pattern`* for especificado, apenas os parâmetros cujos nomes correspondem ao padrão são listados. Sem *`pattern`*, apenas os parâmetros que estão definidos com valores não padrão são listados.

(Use `\dconfig *` para ver todos os parâmetros.) Se `x` for anexado ao nome do comando, os resultados são exibidos em modo expandido. Se `+` for anexado ao nome do comando, cada parâmetro é listado com seu tipo de dados, contexto em que o parâmetro pode ser definido e privilégios de acesso (se privilégios de acesso não padrão foram concedidos).

`\dC[x+] [ pattern ]` [#](#APP-PSQL-META-COMMAND-DC-UC): Lista de tipos de conversão. Se *`pattern`* for especificado, apenas as conversões cujos tipos de origem ou destino correspondem ao padrão são listadas. Se `x` for anexado ao nome do comando, os resultados são exibidos no modo expandido. Se `+` for anexado ao nome do comando, informações adicionais sobre cada conversão são mostradas, incluindo se sua função subjacente é à prova de vazamento e a descrição da conversão.

`\dd[Sx] [ pattern ]` [#](#APP-PSQL-META-COMMAND-DD-LC): Mostra as descrições dos objetos do tipo `constraint`, `operator class`, `operator family`, `rule`, e `trigger`. Todos os outros comentários podem ser visualizados pelos respectivos comandos de barra invertida para aqueles tipos de objetos.

`\dd` exibe descrições para objetos que correspondem ao *`pattern`*, ou de objetos visíveis do tipo apropriado, se não for fornecido nenhum argumento. Mas, em qualquer caso, apenas os objetos que têm uma descrição são listados. Por padrão, apenas os objetos criados pelo usuário são mostrados; forneça um ou o modificador `S` para incluir objetos do sistema. Se `x` for anexado ao nome do comando, os resultados são exibidos no modo expandido.

As descrições dos objetos podem ser criadas com o comando SQL [[`COMMENT`](sql-comment.md)].

`\dD[Sx+] [ pattern ]` [#](#APP-PSQL-META-COMMAND-DD-UC): Lista domínios. Se *`pattern`* for especificado, apenas os domínios cujos nomes correspondem ao padrão são mostrados. Por padrão, apenas os objetos criados pelo usuário são mostrados; forneça um padrão ou o modificador `S` para incluir objetos do sistema. Se `x` for anexado ao nome do comando, os resultados são exibidos no modo expandido. Se `+` for anexado ao nome do comando, cada objeto é listado com suas permissões e descrição associadas.

`\ddp[x] [ pattern ]` [#](#APP-PSQL-META-COMMAND-DDP): Lista as configurações de privilégio de acesso padrão. Uma entrada é mostrada para cada papel (e esquema, se aplicável) para o qual as configurações de privilégio padrão foram alteradas a partir dos padrões internos. Se *`pattern`* for especificado, apenas as entradas cujos nomes de papel ou nomes de esquema correspondem ao padrão são listadas. Se `x` for anexado ao nome do comando, os resultados são exibidos no modo expandido.

O comando `ALTER DEFAULT PRIVILEGES` (sql-alterdefaultprivileges.md "ALTER DEFAULT PRIVILEGES") é usado para definir privilégios de acesso padrão. O significado da exibição do privilégio é explicado na [Seção 5.8](ddl-priv.md).

`\dE[Sx+] [ pattern ]` `\di[Sx+] [ pattern ]` `\dm[Sx+] [ pattern ]` `\ds[Sx+] [ pattern ]` `\dt[Sx+] [ pattern ]` `\dv[Sx+] [ pattern ]` [#](#APP-PSQL-META-COMMAND-DE): Neste grupo de comandos, as letras `E`, `i`, `m`, `s`, `t` e `v` representam tabela, índice, visão materializada, sequência, tabela e visão, respectivamente. Você pode especificar qualquer ou todas estas letras, em qualquer ordem, para obter uma lista de objetos desses tipos. Por exemplo, `\dti` lista tabelas e índices. Se `x` é anexado ao nome do comando, os resultados são exibidos em modo expandido. Se `+` é anexado ao nome do comando, cada objeto é listado com seu status de persistência (permanente, temporário ou não registrado), tamanho físico no disco e descrição associada, se houver. Se *`pattern`* é especificado, apenas os objetos cujos nomes correspondem ao padrão são listados. Por padrão, apenas objetos criados pelo usuário são mostrados; forneça um padrão ou o modificador `S` para incluir objetos do sistema.

`\des[x+] [ pattern ]` [#](#APP-PSQL-META-COMMAND-DES): Lista servidores estrangeiros (mnemônico: “servidores externos”). Se *`pattern`* é especificado, apenas os servidores cujo nome corresponde ao padrão são listados. Se `x` é anexado ao nome do comando, os resultados são exibidos no modo expandido. Se `+` é anexado ao nome do comando, uma descrição completa de cada servidor é mostrada, incluindo os privilégios de acesso do servidor, tipo, versão, opções e descrição.

`\det[x+] [ pattern ]` [#](#APP-PSQL-META-COMMAND-DET)   Lista tabelas estrangeiras (mínima: “tabelas externas”). Se *`pattern`* é especificado, apenas as entradas cujo nome da tabela ou nome do esquema correspondem ao padrão são listadas. Se `x` é anexado ao nome do comando, os resultados são exibidos no modo expandido. Se `+` é anexado ao nome do comando, as opções genéricas e a descrição da tabela estrangeira também são exibidas.

`\deu[x+] [ pattern ]` [#](#APP-PSQL-META-COMMAND-DEU): Lista mapeamentos de usuários (nomeclógico: “usuários externos”). Se *`pattern`* é especificado, apenas os mapeamentos cujos nomes de usuário correspondem ao padrão são listados. Se `x` é anexado ao nome do comando, os resultados são exibidos no modo expandido. Se `+` é anexado ao nome do comando, informações adicionais sobre cada mapeamento são mostradas.

### Atenção

`\deu+` também pode exibir o nome do usuário e a senha do usuário remoto, portanto, deve-se ter cuidado para não divulgá-los.

`\dew[x+] [ pattern ]` [#](#APP-PSQL-META-COMMAND-DEW): Lista de wrappers de dados externos (nome: “wrappers externos”). Se *`pattern`* for especificado, apenas os wrappers de dados externos cujos nomes correspondem ao padrão são listados. Se `x` for anexado ao nome do comando, os resultados são exibidos no modo expandido. Se `+` for anexado ao nome do comando, os privilégios de acesso, opções e descrição do wrapper de dados externos também são exibidos.

`\df[anptwSx+] [ pattern [ arg_pattern ... ] ]` [#](#APP-PSQL-META-COMMAND-DF-LC): Lista funções, juntamente com seus tipos de dados de resultado, tipos de dados de argumento e tipos de função, que são classificados como “agg” (agregado), “normal”, “procedimento”, “trigger” ou “janela”. Para exibir apenas funções de um tipo específico, adicione as letras correspondentes `a`, `n`, `p`, `t` ou `w` ao comando. Se *`pattern`* é especificado, apenas as funções cujos nomes correspondem ao padrão são exibidas. Quaisquer argumentos adicionais são padrões de nome de tipo, que são correspondidos aos nomes dos tipos dos primeiros, segundos, e assim por diante, argumentos da função. (As funções que correspondem podem ter mais argumentos do que o que especifica. Para evitar isso, escreva uma barra `-` como o último *`arg_pattern`*.) Por padrão, apenas objetos criados pelo usuário são exibidos; forneça um padrão ou o modificador `S` para incluir objetos do sistema. Se `x` é anexado ao nome do comando, os resultados são exibidos no modo expandido. Se `+` é anexado ao nome do comando, informações adicionais sobre cada função são exibidas, incluindo volatilidade, segurança paralela, proprietário, classificação de segurança, se é impermeável, privilégios de acesso, idioma, nome interno (apenas para funções C e internas), e descrição. O código-fonte de uma função específica pode ser visto usando `\sf`.

`\dF[x+] [ pattern ]` [#](#APP-PSQL-META-COMMAND-DF-UC): Configurações de pesquisa de texto. Se *`pattern`* for especificado, apenas as configurações cujos nomes correspondem ao padrão são mostradas. Se `x` for anexado ao nome do comando, os resultados são exibidos no modo expandido. Se `+` for anexado ao nome do comando, uma descrição completa de cada configuração é mostrada, incluindo o parser de pesquisa de texto subjacente e a lista de dicionário para cada tipo de token do parser.

`\dFd[x+] [ pattern ]` [#](#APP-PSQL-META-COMMAND-DFD): Listas de dicionários de busca de texto. Se *`pattern`* é especificado, apenas os dicionários cujos nomes correspondem ao padrão são mostrados. Se `x` é anexado ao nome do comando, os resultados são exibidos no modo expandido. Se `+` é anexado ao nome do comando, informações adicionais são exibidas sobre cada dicionário selecionado, incluindo o modelo de busca de texto subjacente e os valores das opções.

`\dFp[x+] [ pattern ]` [#](#APP-PSQL-META-COMMAND-DFP): Listas de analisadores de busca de texto. Se *`pattern`* for especificado, apenas os analisadores cujos nomes correspondem ao padrão são mostrados. Se `x` for anexado ao nome do comando, os resultados são exibidos no modo expandido. Se `+` for anexado ao nome do comando, uma descrição completa de cada analisador é mostrada, incluindo as funções subjacentes e a lista de tipos de token reconhecidos.

`\dFt[x+] [ pattern ]` [#](#APP-PSQL-META-COMMAND-DFT): Modelos de busca de texto. Se *`pattern`* for especificado, apenas os modelos cujos nomes correspondem ao padrão são mostrados. Se `x` for anexado ao nome do comando, os resultados são exibidos em modo expandido. Se `+` for anexado ao nome do comando, informações adicionais são exibidas sobre cada modelo, incluindo os nomes das funções subjacentes.

`\dg[Sx+] [ pattern ]` [#](#APP-PSQL-META-COMMAND-DG): Lista os papéis do banco de dados.

(Como os conceitos de “usuários” e “grupos” foram unificados em “ papéis”, este comando é agora equivalente a `\du`. ) Por padrão, apenas os papéis criados pelo usuário são mostrados; forneça o modificador `S` para incluir os papéis do sistema. Se *`pattern`* é especificado, apenas os papéis cujos nomes correspondem ao padrão são listados. Se `x` é anexado ao nome do comando, os resultados são exibidos no modo expandido. Se `+` é anexado ao nome do comando, informações adicionais são exibidas sobre cada papel; atualmente isso adiciona o comentário para cada papel.

`\dl[x+]` [#](#APP-PSQL-META-COMMAND-DL-LC): Este é um alias para `\lo_list`, que mostra uma lista de grandes objetos. Se `x` for anexado ao nome do comando, os resultados são exibidos em modo expandido. Se `+` for anexado ao nome do comando, cada grande objeto é listado com suas permissões associadas, se houver.

`\dL[Sx+] [ pattern ]` [#](#APP-PSQL-META-COMMAND-DL-UC): Lista de idiomas processuais. Se *`pattern`* for especificado, apenas os idiomas cujos nomes correspondem ao padrão são listados. Por padrão, apenas idiomas criados pelo usuário são mostrados; forneça o modificador `S` para incluir objetos do sistema. Se `x` for anexado ao nome do comando, os resultados são exibidos no modo expandido. Se `+` for anexado ao nome do comando, cada idioma é listado com seu manipulador de chamada, validador, privilégios de acesso, e se é um objeto do sistema.

`\dn[Sx+] [ pattern ]` [#](#APP-PSQL-META-COMMAND-DN): Lista esquemas (nomes de namespaces). Se *`pattern`* for especificado, apenas os esquemas cujos nomes correspondem ao padrão são listados. Por padrão, apenas os objetos criados pelo usuário são mostrados; forneça um padrão ou o modificador `S` para incluir objetos do sistema. Se `x` for anexado ao nome do comando, os resultados são exibidos no modo expandido. Se `+` for anexado ao nome do comando, cada objeto é listado com suas permissões e descrição associadas, se houver.

`\do[Sx+] [ pattern [ arg_pattern [ arg_pattern ] ] ]` [#](#APP-PSQL-META-COMMAND-DO-LC): Lista os operadores com seus tipos de operando e resultado. Se *`pattern`* é especificado, apenas os operadores cujos nomes correspondem ao padrão são listados. Se um *`arg_pattern`* é especificado, apenas os operadores prefixos cujos nomes de argumento de direita correspondem a esse padrão são listados. Se dois *`arg_pattern`*s são especificados, apenas os operadores binários cujos nomes de tipo de argumento correspondem a esses padrões são listados. (Alternativamente, escreva `-` para o argumento não utilizado de um operador unário.) Por padrão, apenas objetos criados pelo usuário são mostrados; forneça um padrão ou o modificador `S` para incluir objetos do sistema. Se `x` é anexado ao nome do comando, os resultados são exibidos no modo expandido. Se `+` é anexado ao nome do comando, informações adicionais sobre cada operador são exibidas, incluindo o nome da função subjacente e se é à prova de vazamento.

`\dO[Sx+] [ pattern ]` [#](#APP-PSQL-META-COMMAND-DO-UC): Lista de colatações. Se *`pattern`* for especificado, apenas as colatações cujos nomes correspondem ao padrão são listadas. Por padrão, apenas os objetos criados pelo usuário são mostrados; forneça um padrão ou o modificador `S` para incluir objetos do sistema. Se `x` for anexado ao nome do comando, os resultados são exibidos no modo expandido. Se `+` for anexado ao nome do comando, cada colatação é listada com sua descrição associada, se houver. Observe que apenas as colatações utilizáveis com a codificação do banco de dados atual são mostradas, portanto, os resultados podem variar em diferentes bancos da mesma instalação.

`\dp[Sx] [ pattern ]` [#](#APP-PSQL-META-COMMAND-DP-LC): Lista tabelas, visualizações e sequências com seus privilégios de acesso associados. Se *`pattern`* for especificado, apenas tabelas, visualizações e sequências cujos nomes correspondem ao padrão são listados. Por padrão, apenas objetos criados pelo usuário são mostrados; forneça um padrão ou o modificador `S` para incluir objetos do sistema. Se `x` for anexado ao nome do comando, os resultados são exibidos no modo expandido.

Os comandos `GRANT` e (sql-grant.md "GRANT") são usados para definir privilégios de acesso. O significado da exibição do privilégio é explicado em [Seção 5.8](ddl-priv.md).

`\dP[itnx+] [ pattern ]` [#](#APP-PSQL-META-COMMAND-DP-UC)   Lista relações particionadas. Se *`pattern`* for especificado, apenas as entradas cujo nome corresponda ao padrão são listadas. Os modificadores `t` (tabelas) e `i` (índices) podem ser anexados ao comando, filtrando o tipo de relações a serem listadas. Por padrão, tabelas e índices particionados são listados.

Se o modificador `n` (“aninhado”) for usado, ou um padrão for especificado, então as relações particionadas não-raiz são incluídas, e uma coluna é exibida, mostrando o pai de cada relação particionada.

Se `x` for anexado ao nome do comando, os resultados são exibidos no modo expandido. Se `+` for anexado ao nome do comando, a soma dos tamanhos de cada partição da relação também é exibida, juntamente com a descrição da relação. Se `n` for combinado com `+`, dois tamanhos são mostrados: um incluindo o tamanho total das partições de folha diretamente anexadas e outro mostrando o tamanho total de todas as partições, incluindo subpartições indiretamente anexadas.

`\drds[x] [ role-pattern [ database-pattern ] ]` [#](#APP-PSQL-META-COMMAND-DRDS): Listas definem configurações de configuração. Essas configurações podem ser específicas para o papel, específicas para o banco de dados, ou ambas. *`role-pattern`* e *`database-pattern`* são usados para selecionar roles e bancos de dados específicos para listar, respectivamente. Se omitido, ou se `*` é especificado, todas as configurações são listadas, incluindo aquelas específicas para o papel ou específicas para o banco de dados, respectivamente. Se `x` é anexado ao nome do comando, os resultados são exibidos no modo expandido.

Os comandos `ALTER ROLE`(sql-alterrole.md "ALTER ROLE") e `ALTER DATABASE`(sql-alterdatabase.md "ALTER DATABASE") são usados para definir configurações de configuração por papel e por banco de dados.

`\drg[Sx] [ pattern ]` [#](#APP-PSQL-META-COMMAND-DRG): Lista informações sobre cada membro da associação de papel concedido, incluindo opções atribuídas (`ADMIN`, `INHERIT` e/ou `SET`) e concedente. Veja o comando [`GRANT`](sql-grant.md) para informações sobre associações de papel.

Por padrão, apenas as concessões para papéis criados pelo usuário são exibidas; forneça o modificador `S` para incluir papéis do sistema. Se *`pattern`* for especificado, Apenas as concessões para aqueles papéis cujos nomes correspondem ao padrão são listados. Se `x` for anexado ao nome do comando, os resultados são exibidos no modo expandido.

`\dRp[x+] [ pattern ]` [#](#APP-PSQL-META-COMMAND-DRP): Lista publicações de replicação. Se *`pattern`* for especificado, apenas as publicações cujos nomes correspondem ao padrão são listadas. Se `x` for anexado ao nome do comando, os resultados são exibidos no modo expandido. Se `+` for anexado ao nome do comando, as tabelas e esquemas associados a cada publicação também são exibidos.

`\dRs[x+] [ pattern ]` [#](#APP-PSQL-META-COMMAND-DRS): Lista assinaturas de replicação. Se *`pattern`* é especificado, apenas as assinaturas cujos nomes correspondem ao padrão são listadas. Se `x` é anexado ao nome do comando, os resultados são exibidos no modo expandido. Se `+` é anexado ao nome do comando, propriedades adicionais das assinaturas são mostradas.

`\dT[Sx+] [ pattern ]` [#](#APP-PSQL-META-COMMAND-DT): Lista tipos de dados. Se *`pattern`* for especificado, apenas os tipos cujos nomes correspondem ao padrão são listados. Se `x` for anexado ao nome do comando, os resultados são exibidos no modo expandido. Se `+` for anexado ao nome do comando, cada tipo é listado com seu nome interno e tamanho, seus valores permitidos se for um tipo `enum`, e suas permissões associadas. Por padrão, apenas objetos criados pelo usuário são mostrados; forneça um padrão ou o modificador `S` para incluir objetos do sistema.

`\du[Sx+] [ pattern ]` [#](#APP-PSQL-META-COMMAND-DU): Lista os papéis do banco de dados.

(Como os conceitos de “usuários” e “grupos” foram unificados em “ papéis”, este comando é agora equivalente a `\dg`. Por padrão, apenas os papéis criados pelo usuário são mostrados; forneça o modificador `S` para incluir os papéis do sistema. Se *`pattern`* é especificado, apenas os papéis cujos nomes correspondem ao padrão são listados. Se `x` é anexado ao nome do comando, os resultados são exibidos no modo expandido. Se `+` é anexado ao nome do comando, informações adicionais são exibidas sobre cada papel; atualmente isso adiciona o comentário para cada papel.

`\dx[x+] [ pattern ]` [#](#APP-PSQL-META-COMMAND-DX-LC): Lista de extensões instaladas. Se *`pattern`* for especificado, apenas as extensões cujos nomes correspondem ao padrão são listadas. Se `x` for anexado ao nome do comando, os resultados são exibidos no modo expandido. Se `+` for anexado ao nome do comando, todos os objetos pertencentes a cada extensão correspondente são listados.

`\dX[x] [ pattern ]` [#](#APP-PSQL-META-COMMAND-DX-UC): Lista estatísticas extensas. Se *`pattern`* for especificado, apenas as estatísticas extensas cujos nomes correspondem ao padrão são listadas. Se `x` for anexado ao nome do comando, os resultados são exibidos no modo expandido.

O status de cada tipo de estatísticas estendidas é mostrado em uma coluna com o nome do seu tipo estatístico (por exemplo, Ndistinct). `defined` significa que foi solicitado ao criar as estatísticas, e NULL significa que não foi solicitado. Você pode usar `pg_stats_ext` se quiser saber se [`ANALYZE`](sql-analyze.md) foi executado e as estatísticas estão disponíveis para o planejador.

`\dy[x+] [ pattern ]` [#](#APP-PSQL-META-COMMAND-DY): Lista os gatilhos de evento. Se *`pattern`* for especificado, apenas os gatilhos de evento cujos nomes correspondem ao padrão são listados. Se `x` for anexado ao nome do comando, os resultados são exibidos no modo expandido. Se `+` for anexado ao nome do comando, cada objeto é listado com sua descrição associada.

`\e` ou `\edit` `[ filename ] [ line_number ]` [#](#APP-PSQL-META-COMMAND-EDIT): Se *`filename`* for especificado, o arquivo é editado; após a saída do editor, o conteúdo do arquivo é copiado no buffer de consulta atual. Se não for dado *`filename`*, o buffer de consulta atual é copiado para um arquivo temporário que é então editado da mesma maneira. Ou, se o buffer de consulta atual estiver vazio, a consulta executada mais recentemente é copiada para um arquivo temporário e editada da mesma maneira.

Se você editar um arquivo ou a consulta anterior e sair do editor sem modificar o arquivo, o buffer de consulta é limpo. Caso contrário, os novos conteúdos do buffer de consulta são reinterpretados de acordo com as regras normais do psql, tratando todo o buffer como uma única linha. Quaisquer consultas completas são executadas imediatamente; ou seja, se o buffer de consulta contiver ou terminar com um ponto e vírgula, tudo até esse ponto é executado e removido do buffer de consulta. O que resta no buffer de consulta é redesenhado. Digite ponto e vírgula ou `\g` para enviá-lo, ou `\r` para cancelá-lo, limpando o buffer de consulta.

Tratar o buffer como uma única linha afeta principalmente comandos meta: o(s) conteúdo(s) no buffer após um comando meta será(ão) considerado(s) como argumento(s) para o comando meta, mesmo que ele(s) se estenda(m) por múltiplas linhas.

(Assim, você não pode fazer scripts que utilizem comandos meta dessa maneira. Use `\i` para isso.)

Se um número de linha for especificado, o psql posicionará o cursor na linha especificado do buffer de arquivo ou consulta. Observe que, se um argumento único com todos os dígitos for fornecido, o psql assume que é um número de linha, não um nome de arquivo.

### DICA

Veja [Ambiente](app-psql.md#APP-PSQL-ENVIRONMENT "Environment"), abaixo, para saber como configurar e personalizar seu editor.

`\echo text [ ... ]` [#](#APP-PSQL-META-COMMAND-ECHO): Imprime os argumentos avaliados na saída padrão, separados por espaços e seguidos por uma nova linha. Isso pode ser útil para interpor informações na saída de scripts. Por exemplo:

```
=> \echo `date` Tue Oct 26 21:40:57 CEST 1999
```

Se o primeiro argumento for um `-n` não citado, a última linha não é escrita (nem o primeiro argumento).

### DICA

Se você usa o comando `\o` para redirecionar a saída da sua consulta, talvez queira usar `\qecho` em vez deste comando. Veja também `\warn`.

`\ef [ function_description [ line_number ] ]` [#](#APP-PSQL-META-COMMAND-EF): Este comando recupera e edita a definição da função ou procedimento nomeado, na forma de um comando `CREATE OR REPLACE FUNCTION` ou `CREATE OR REPLACE PROCEDURE` comando. A edição é feita da mesma maneira que para `\edit`. Se você sair do editor sem salvar, a declaração é descartada. Se você salvar e sair do editor, o comando atualizado é executado imediatamente se você adicionou um ponto e vírgula a ele. Caso contrário, ele é reapresentado; Digite ponto e vírgula ou `\g` para enviá-lo, ou `\r` para cancelar.

A função alvo pode ser especificada apenas pelo nome, ou pelo nome e pelos argumentos, por exemplo, `foo(integer, text)`. Os tipos de argumentos devem ser fornecidos se houver mais de uma função com o mesmo nome.

Se nenhuma função for especificada, um modelo em branco `CREATE FUNCTION` será apresentado para edição.

Se um número de linha for especificado, o psql posicionará o cursor na linha especificada do corpo da função. (Observe que o corpo da função geralmente não começa na primeira linha do arquivo.)

Ao contrário da maioria dos outros meta-comandos, todo o resto da linha é sempre considerado o(s) argumento(s) de `\ef`, e nem a interpolação de variáveis nem a expansão de aspas duplas são realizadas nos argumentos.

### DICA

Veja [Ambiente](app-psql.md#APP-PSQL-ENVIRONMENT "Environment"), abaixo, para saber como configurar e personalizar seu editor.

`\encoding [ encoding ]` [#](#APP-PSQL-META-COMMAND-ENCODING): Define o codificador do conjunto de caracteres do cliente. Sem argumento, este comando mostra o codificador atual.

`\errverbose` [#](#APP-PSQL-META-COMMAND-ERRVERBOSE): Repite a mensagem de erro do servidor mais recente na máxima verbosidade, como se `VERBOSITY` estivesse definida como `verbose` e `SHOW_CONTEXT` estivesse definida como `always`.

`\ev [ view_name [ line_number ] ]` [#](#APP-PSQL-META-COMMAND-EV): Este comando recupera e edita a definição da vista nomeada, na forma de um comando `CREATE OR REPLACE VIEW`. A edição é feita da mesma maneira que para `\edit`. Se você sair do editor sem salvar, a declaração é descartada. Se você salvar e sair do editor, o comando atualizado é executado imediatamente se você adicionou um ponto e vírgula a ele. Caso contrário, ele é reapresentado; Digite ponto e vírgula ou `\g` para enviá-lo, ou `\r` para cancelar.

Se nenhuma visão for especificada, um modelo em branco `CREATE VIEW` será apresentado para edição.

Se um número de linha for especificado, o psql posicionará o cursor na linha especificada da definição da vista.

Ao contrário da maioria dos outros meta-comandos, todo o resto da linha é sempre considerado o(s) argumento(s) de `\ev`, e nem a interpolação de variáveis nem a expansão de aspas duplas são realizadas nos argumentos.

`\f [ string ]` [#](#APP-PSQL-META-COMMAND-F): Define o separador de campo para saída de consulta não alinhada. O padrão é a barra vertical (`|`). É equivalente a `\pset fieldsep`.

`\g [ (option=value [...]) ] [ filename ]` `\g [ (option=value [...]) ] [ |command ]` [#](#APP-PSQL-META-COMMAND-G) : Envia o buffer atual da consulta ao servidor para execução.

Se houver parênteses após `\g`, eles cercam uma lista de *`option`*`=`*`value`* cláusulas de opção de formatação, que são interpretadas da mesma maneira que `\pset` *`option`* *`value`* comandos, mas só têm efeito durante a duração desta consulta. Nesta lista, espaços não são permitidos ao redor dos sinais de `=`, mas são necessários entre as cláusulas de opção. Se `=`*`value`* for omitido, o nomeado *`option`* é alterado da mesma maneira que para `\pset` *`option`* sem *`value`* explícito.

Se um argumento *`filename`* ou `|`*`command`* for fornecido, a saída da consulta é escrita no arquivo nomeado ou redirecionada para o comando shell fornecido, em vez de ser exibida como de costume. O arquivo ou comando é escrito apenas se a consulta retornar com sucesso zero ou mais tuplas, não se a consulta falhar ou for um comando SQL que não retorna dados.

Se o buffer de consulta atual estiver vazio, a consulta enviada mais recentemente é reexecutada. Exceto por esse comportamento, `\g` sem quaisquer argumentos é essencialmente equivalente a um ponto e vírgula. Com argumentos, `\g` fornece uma alternativa "de uma só vez" ao comando `\o` e, adicionalmente, permite ajustes de formatação de saída normalmente definidos por `\pset` em uma só vez.

Quando o último argumento começa com `|`, todo o restante da linha é considerado o *`command`* a ser executado, e nem a interpolação de variáveis nem a expansão de aspas são realizadas nele. O restante da linha é simplesmente passado literalmente para a concha.

`\gdesc` [#](#APP-PSQL-META-COMMAND-GDESC) :   Mostra a descrição (ou seja, os nomes das colunas e os tipos de dados) do resultado do buffer de consulta atual. A consulta não é executada na verdade; no entanto, se ela contiver algum tipo de erro de sintaxe, esse erro será relatado normalmente.

Se o buffer de consulta atual estiver vazio, a consulta mais recentemente enviada é descrita em vez disso.

`\getenv psql_var env_var` [#](#APP-PSQL-META-COMMAND-GETENV): Obtém o valor da variável de ambiente *`env_var`* e a atribui à variável psql *`psql_var`*. Se *`env_var`* não estiver definido no ambiente do processo psql, *`psql_var`* não será alterado. Exemplo:

```
=> \getenv home HOME => \echo :home /home/postgres
```

`\gexec` [#](#APP-PSQL-META-COMMAND-GEXEC): Envia o buffer de consulta atual ao servidor, e, em seguida, trata cada coluna de cada linha do resultado da consulta (se houver) como uma declaração SQL a ser executada. Por exemplo, para criar um índice em cada coluna de `my_table`:

```
=> SELECT format('create index on my_table(%I)', attname) -> FROM pg_attribute -> WHERE attrelid = 'my_table'::regclass AND attnum > 0 -> ORDER BY attnum -> \gexec CREATE INDEX CREATE INDEX CREATE INDEX CREATE INDEX
```

As consultas geradas são executadas na ordem em que as linhas são devolvidas e de esquerda para direita dentro de cada linha, se houver mais de uma coluna. Os campos NULL são ignorados. As consultas geradas são enviadas literalmente ao servidor para processamento, portanto, não podem ser comandos meta do psql nem conter referências de variáveis do psql. Se qualquer consulta individual falhar, a execução das consultas restantes continua a menos que `ON_ERROR_STOP` seja definida. A execução de cada consulta está sujeita ao processamento de `ECHO`. (Definir `ECHO` para `all` ou `queries` é frequentemente aconselhável ao usar `\gexec`). O registro de consultas, modo de etapa única, cronometragem e outras características de execução de consultas aplicam-se a cada consulta gerada também.

Se o buffer de consulta atual estiver vazio, a consulta enviada mais recentemente é executada novamente.

`\gset [ prefix ]` [#](#APP-PSQL-META-COMMAND-GSET): Envia o buffer atual da consulta ao servidor e armazena a saída da consulta em variáveis do psql (consulte [Variáveis](app-psql.md#APP-PSQL-VARIABLES "Variables") abaixo). A consulta a ser executada deve retornar exatamente uma linha. Cada coluna da linha é armazenada em uma variável separada, com o mesmo nome da coluna. Por exemplo:

```
=> SELECT 'hello' AS var1, 10 AS var2 -> \gset => \echo :var1 :var2 hello 10
```

Se você especificar um *`prefix`*, essa string é prependida aos nomes dos colunas da consulta para criar os nomes de variáveis a serem usados:

```
=> SELECT 'hello' AS var1, 10 AS var2 -> \gset result_ => \echo :result_var1 :result_var2 hello 10
```

Se o resultado de uma coluna for NULL, a variável correspondente é desativada, em vez de ser definida.

Se a consulta falhar ou não retornar uma única linha, nenhuma variável é alterada.

Se o buffer de consulta atual estiver vazio, a consulta enviada mais recentemente é executada novamente.

`\gx [ (option=value [...]) ] [ filename ]` `\gx [ (option=value [...]) ] [ |command ]` [#](#APP-PSQL-META-COMMAND-GX): `\gx` é equivalente a `\g`, exceto que ele força o modo de saída expandida para esta consulta, pois se `expanded=on` fosse incluído na lista de opções de `\pset`. Veja também `\x`.

`\h` ou `\help` `[ command ]` [#](#APP-PSQL-META-COMMAND-HELP): Fornece ajuda de sintaxe no comando SQL especificado. Se *`command`* não for especificado, o psql listará todos os comandos para os quais a ajuda de sintaxe está disponível. Se *`command`* for um asterisco (`*`), então a ajuda de sintaxe em todos os comandos SQL é exibida.

Ao contrário da maioria dos outros meta-comandos, todo o resto da linha é sempre considerado o(s) argumento(s) de `\help`, e nem a interpolação de variáveis nem a expansão de aspas duplas são realizadas nos argumentos.

### Nota

Para simplificar a digitação, comandos que consistem em várias palavras não precisam ser citados. Assim, é permitido digitar **`\help alter table`**.

`\H` ou `\html` [#](#APP-PSQL-META-COMMAND-HTML): Ativa o formato de saída de consulta HTML. Se o formato HTML já estiver ativado, ele é revertido para o formato de texto alinhado padrão. Este comando é para compatibilidade e conveniência, mas consulte `\pset` sobre a definição de outras opções de saída.

`\i` ou `\include` *`filename`* [#](#APP-PSQL-META-COMMAND-INCLUDE): Leia a entrada do arquivo *`filename`* e execute-a como se tivesse sido digitada no teclado.

Se *`filename`* for `-` (com hífen), então a entrada padrão é lida até uma indicação de EOF ou `\q` meta-comando. Isso pode ser usado para intercalar a entrada interativa com a entrada de arquivos. Observe que o comportamento do Readline será usado apenas se estiver ativo no nível mais externo.

### Nota

Se você deseja ver as linhas no ecrã conforme são lidas, deve definir a variável `ECHO` para `all`.

`\if` *`expression`* `\elif` *`expression`* `\else` `\endif` [#](#PSQL-METACOMMAND-IF): Este grupo de comandos implementa blocos condicionais nestables. Um bloco condicional deve começar com um `\if` e terminar com um `\endif`. Entre eles, pode haver qualquer número de cláusulas `\elif`, que podem ser seguidas opcionalmente por uma única cláusula `\else`. Perguntas comuns e outros tipos de comandos de barra invertida podem (e geralmente fazem) aparecer entre os comandos que formam um bloco condicional.

Os comandos `\if` e `\elif` leem seus(s) argumento(s) e os avaliam como uma expressão booleana. Se a expressão gerar `true`, o processamento continua normalmente; caso contrário, as linhas são ignoradas até que seja alcançado um `\elif`, `\else`, ou `\endif`. Uma vez que um teste `\if` ou `\elif` tenha sido bem-sucedido, os argumentos dos comandos posteriores `\elif` no mesmo bloco não são avaliados, mas são tratados como falsos. As linhas que seguem um `\else` são processadas apenas se nenhum `\if` ou `\elif` anterior tenha sido bem-sucedido.

O argumento *`expression`* de um comando `\if` ou `\elif` está sujeito a interpolação variável e expansão de aspas, assim como qualquer outro argumento de comando de barra invertida. Depois disso, ele é avaliado como o valor de uma variável de opção de ativação/desativação. Portanto, um valor válido é qualquer correspondência clara, independentemente do caso, para um dos seguintes: `true`, `false`, `1`, `0`, `on`, `off`, `yes`, `no`. Por exemplo, `t`, `T` e `tR` todos serão considerados `true`.

Expressões que não retornam verdadeiro ou falso corretamente gerarão um aviso e serão tratadas como falsas.

As linhas que são ignoradas são analisadas normalmente para identificar consultas e comandos de barra invertida, mas as consultas não são enviadas ao servidor, e os comandos de barra invertida, exceto os condicionais (`\if`, `\elif`, `\else`, `\endif`) são ignorados. Os comandos condicionados são verificados apenas para o emenda válida. As referências de variáveis nas linhas ignoradas não são expandidas, e a expansão de aspas também não é realizada.

Todos os comandos de barra invertida de um bloco condicional dado devem aparecer no mesmo arquivo de origem. Se o EOF for alcançado no arquivo de entrada principal ou em um arquivo `\include` antes que todos os blocos locais `\if` tenham sido fechados, o psql levantará um erro.

Aqui está um exemplo:

```
-- check for the existence of two separate records in the database and store -- the results in separate psql variables SELECT EXISTS(SELECT 1 FROM customer WHERE customer_id = 123) as is_customer, EXISTS(SELECT 1 FROM employee WHERE employee_id = 456) as is_employee \gset \if :is_customer SELECT * FROM customer WHERE customer_id = 123; \elif :is_employee \echo 'is not a customer but is an employee' SELECT * FROM employee WHERE employee_id = 456; \else \if yes \echo 'not a customer or employee' \else \echo 'this will never print' \endif \endif
```

`\ir` ou `\include_relative` *`filename`* [#](#APP-PSQL-META-COMMAND-INCLUDE-RELATIVE): O comando `\ir` é semelhante ao `\i`, mas resolve nomes de arquivos relativos de maneira diferente. Ao ser executado em modo interativo, os dois comandos se comportam de maneira idêntica. No entanto, quando invocado a partir de um script, `\ir` interpreta nomes de arquivos relativos à diretório em que o script está localizado, em vez do diretório de trabalho atual.

`\l[x+]` ou `\list[x+] [ pattern ]` [#](#APP-PSQL-META-COMMAND-LIST): Liste os bancos de dados no servidor e mostre seus nomes, proprietários, códigos de codificação de caracteres e privilégios de acesso. Se *`pattern`* for especificado, apenas os bancos de dados cujos nomes correspondem ao padrão são listados. Se `x` for anexado ao nome do comando, os resultados são exibidos em modo expandido. Se `+` for anexado ao nome do comando, os tamanhos dos bancos de dados, espaços de tabelas padrão e descrições também são exibidos.

(As informações de tamanho estão disponíveis apenas para bancos de dados que o usuário atual pode conectar.)

`\lo_export loid filename` [#](#APP-PSQL-META-COMMAND-LO-EXPORT) :   Leia o grande objeto com OID *`loid`* do banco de dados e escreva-o em *`filename`*. Observe que isso é sutilmente diferente da função do servidor `lo_export`, que atua com as permissões do usuário que o servidor de banco de dados executa e no sistema de arquivos do servidor.

### DICA

Use `\lo_list` para descobrir o OID do objeto grande.

`\lo_import filename [ comment ]` [#](#APP-PSQL-META-COMMAND-LO-IMPORT): Armazena o arquivo em um objeto grande do PostgreSQL. Opcionalmente, associa o comentário fornecido ao objeto. Exemplo:

```
foo=> \lo_import '/home/peter/pictures/photo.xcf' 'a picture of me' lo_import 152801
```

A resposta indica que o grande objeto recebeu o ID de objeto 152801, que pode ser usado para acessar o objeto recém-criado no futuro. Por questões de legibilidade, é recomendado sempre associar um comentário legível para cada objeto. Tanto os OIDs quanto os comentários podem ser visualizados com o comando `\lo_list`.

Observe que este comando é sutilmente diferente do lado do servidor `lo_import` porque ele atua como o usuário local no sistema de arquivos local, em vez do usuário e sistema de arquivos do servidor.

`\lo_list[x+]` [#](#APP-PSQL-META-COMMAND-LO-LIST): Mostra uma lista de todos os objetos grandes do PostgreSQL atualmente armazenados no banco de dados, juntamente com quaisquer comentários fornecidos para eles. Se `x` é anexado ao nome do comando, os resultados são exibidos no modo expandido. Se `+` é anexado ao nome do comando, cada objeto grande é listado com suas permissões associadas, se houver.

`\lo_unlink loid` [#](#APP-PSQL-META-COMMAND-LO-UNLINK): Exclui o grande objeto com OID *`loid`* do banco de dados.

### DICA

Use `\lo_list` para descobrir o OID do objeto grande.

`\o` ou `\out [ filename ]` `\o` ou `\out [ |command ]` [#](#APP-PSQL-META-COMMAND-OUT): Organiza para salvar os resultados futuros da consulta no arquivo *`filename`* ou pipe os resultados futuros para o comando de shell *`command`*. Se não for especificado nenhum argumento, a saída da consulta é redefinida para a saída padrão.

Se o argumento começar com `|`, então todo o restante da linha é considerado o *`command`* a ser executado, e nem a interpolação de variáveis nem a expansão de aspas são realizadas nele. O resto da linha é simplesmente passado literalmente para a concha.

“Resultados da consulta” inclui todas as tabelas, respostas de comando e avisos obtidos do servidor de banco de dados, bem como a saída de vários comandos de barra invertida que consultam o banco de dados (como `\d`); mas não mensagens de erro.

### DICA

Para intercalar a saída de texto entre os resultados da consulta, use `\qecho`.

`\p` ou `\print` [#](#APP-PSQL-META-COMMAND-PRINT): Imprima o buffer de consulta atual na saída padrão. Se o buffer de consulta atual estiver vazio, a consulta executada mais recentemente é impressa em vez disso.

`\parse statement_name` [#](#APP-PSQL-META-COMMAND-PARSE): Cria uma declaração preparada a partir do buffer de consulta atual, com base no nome de um objeto de declaração preparada de destino. Uma string vazia denota a declaração preparada sem nome.

Exemplo:

```
SELECT $1 \parse stmt1
```

Este comando faz com que o protocolo de consulta estendida seja usado, ao contrário da operação normal do psql, que usa o protocolo de consulta simples. Uma mensagem [Parse (F)] (protocol-message-formats.md#PROTOCOL-MESSAGE-FORMATS-PARSE) será emitida por este comando, então pode ser útil para testar o protocolo de consulta estendida a partir do psql. Este comando afeta apenas a próxima consulta executada; todas as consultas subsequentes usarão o protocolo de consulta simples por padrão.

`\password [ username ]` [#](#APP-PSQL-META-COMMAND-PASSWORD) :   Altera a senha do usuário especificado (por padrão, o usuário atual). Este comando solicita a nova senha, a encripta e a envia ao servidor como um comando `ALTER ROLE`. Isso garante que a nova senha não apareça em texto claro no histórico de comandos, no log do servidor ou em outros lugares.

`\prompt [ text ] name` [#](#APP-PSQL-META-COMMAND-PROMPT) :   Solicita ao usuário que forneça texto, que será atribuído à variável *`name`*.  Uma string de solicitação opcional, *`text`*, pode ser especificada. (Para solicitações de texto em várias palavras, envolva o texto em aspas simples.)

Por padrão, `\prompt` usa o terminal para entrada e saída. No entanto, se o interruptor de linha de comando `-f` foi usado, `\prompt` usa entrada padrão e saída padrão.

`\pset [ option [ value ] ]` [#](#APP-PSQL-META-COMMAND-PSET): Este comando define opções que afetam o resultado das tabelas de resultados da consulta. *`option`* indica qual opção deve ser definida. A semântica de *`value`* varia dependendo da opção selecionada. Para algumas opções, omitir *`value`* faz com que a opção seja alternada ou desdefinida, conforme descrito na opção específica. Se não for mencionado tal comportamento, então omitir *`value`* resulta apenas na exibição do ajuste atual.

`\pset` sem quaisquer argumentos exibe o status atual de todas as opções de impressão.

As opções de impressão ajustáveis são:

`border` [#](#APP-PSQL-META-COMMAND-PSET-BORDER) :   O *`value`* deve ser um número. Em geral, quanto maior o número, mais bordas e linhas as tabelas terão, mas os detalhes dependem do formato específico. No formato HTML, isso se traduzirá diretamente no atributo `border=...`. Na maioria dos outros formatos, apenas os valores 0 (sem borda), 1 (linhas de divisão internas) e 2 (quadro da tabela) fazem sentido, e os valores acima de 2 serão tratados da mesma forma que `border = 2`. Os formatos `latex` e `latex-longtable` permitirão adicionalmente um valor de 3 para adicionar linhas de divisão entre as linhas de dados.

`columns` [#](#APP-PSQL-META-COMMAND-PSET-COLUMNS) :   Define a largura alvo para o formato `wrapped`, e também o limite de largura para determinar se a saída é larga o suficiente para exigir o pager ou a mudança para a exibição vertical no modo automático expandido. Zero (o padrão) faz com que a largura alvo seja controlada pela variável de ambiente `COLUMNS`, ou pela largura do ecrã detectada se `COLUMNS` não estiver definida. Além disso, se `columns` for zero, então o formato `wrapped` afeta apenas a saída do ecrã. Se `columns` for diferente de zero, então a saída de ficheiros e pipes é envolta nessa largura também.

`csv_fieldsep` [#](#APP-PSQL-META-COMMAND-PSET-CSV-FIELDSEP) :   Especifica o separador de campo a ser utilizado no formato de saída CSV. Se o caractere do separador aparecer no valor de um campo, esse campo é exibido entre aspas duplas, seguindo as regras padrão do CSV. O padrão é uma vírgula.

`expanded` (ou `x`) [#](#APP-PSQL-META-COMMAND-PSET-EXPANDED) :   Se *`value`* for especificado, deve ser `on` ou `off`, o que ativa ou desativa o modo expandido, ou `auto`. Se *`value`* for omitido, o comando troca entre as configurações de ativação e desativação. Quando o modo expandido é ativado, os resultados da consulta são exibidos em duas colunas, com o nome da coluna à esquerda e os dados à direita. Esse modo é útil se os dados não caberem na tela no modo "horizontal" normal. No ajuste automático, o modo expandido é usado sempre que a saída da consulta tiver mais de uma coluna e for mais larga que a tela; caso contrário, o modo regular é usado. O ajuste automático é eficaz apenas nos formatos alinhados e empacotados. Em outros formatos, ele sempre se comporta como se o modo expandido estivesse desligado.

`fieldsep` [#](#APP-PSQL-META-COMMAND-PSET-FIELDSEP) :   Especifica o separador de campo a ser usado no formato de saída não alinhada. Dessa forma, é possível criar, por exemplo, uma saída com separação por tabulação, que outros programas podem preferir. Para definir um tab como separador de campo, digite `\pset fieldsep '\t'`. O separador de campo padrão é `'|'` (uma barra vertical).

`fieldsep_zero` [#](#APP-PSQL-META-COMMAND-PSET-FIELDSEP-ZERO) :   Define o separador de campo a ser usado no formato de saída não alinhada com um byte zero.

`footer` [#](#APP-PSQL-META-COMMAND-PSET-FOOTER) :   Se *`value`* for especificado deve ser `on` ou `off` que habilitará ou desabilitará a exibição do rodapé da tabela (a contagem de `(n rows)`). Se *`value`* for omitido, o comando alternará a exibição do rodapé ligando ou desligando.

`format` [#](#APP-PSQL-META-COMMAND-PSET-FORMAT) :   Define o formato de saída como um dos `aligned`, `asciidoc`, `csv`, `html`, `latex`, `latex-longtable`, `troff-ms`, `unaligned`, ou `wrapped`. São permitidas abreviações exclusivas.

O formato `aligned` é o formato padrão, texto legível por humanos e bem formatado; este é o padrão.

O formato `unaligned` escreve todas as colunas de uma linha em uma única linha, separadas pelo separador de campo atualmente ativo. Isso é útil para criar saída que pode ser lida por outros programas, por exemplo, formatação com separação por tabulação ou separação por vírgula. No entanto, o caractere do separador de campo não é tratado especialmente se ele aparecer no valor de uma coluna; portanto, o formato CSV pode ser mais adequado para tais propósitos.

O formato `csv` escreve os valores das colunas separados por vírgulas, aplicando as regras de citação descritas em [RFC 4180](https://datatracker.ietf.org/doc/html/rfc4180). Essa saída é compatível com o formato CSV do comando `COPY` do servidor. Uma linha de cabeçalho com os nomes das colunas é gerada, a menos que o parâmetro `tuples_only` `on`. Títulos e rodapés não são impressos. Cada linha é terminada pelo caractere de fim de linha dependente do sistema, que é tipicamente uma única nova linha (`\n`) para sistemas semelhantes ao Unix ou uma sequência de retorno de carro e nova linha (`\r\n`) para o Microsoft Windows. Caracteres de separador de campo, outros que a vírgula, podem ser selecionados com `\pset csv_fieldsep`.

O formato `wrapped` é como o formato `aligned`, mas envolve valores de dados amplos em linhas para fazer com que a saída se ajuste à largura da coluna-alvo. A largura-alvo é determinada conforme descrito na opção `columns`. Observe que o psql não tentará envolver títulos de cabeçalhos de coluna; portanto, o formato `wrapped` se comporta da mesma forma que o formato `aligned` se o comprimento total necessário para os cabeçalhos de coluna exceder a largura-alvo.

Os formatos `asciidoc`, `html`, `latex`, `latex-longtable` e `troff-ms` colocam tabelas que são destinadas a serem incluídas em documentos que utilizam o respectivo linguagem de marcação. Eles não são documentos completos! Isso pode não ser necessário em HTML, mas em LaTeX você deve ter um pacote de documento completo. O formato `latex` usa o ambiente `tabular` do LaTeX. O formato `latex-longtable` requirir os pacotes LaTeX `longtable` e `booktabs`.

`linestyle` [#](#APP-PSQL-META-COMMAND-PSET-LINESTYLE) :   Define o estilo de desenho da linha de contorno como um dos `ascii`, `old-ascii`, ou `unicode`. São permitidas abreviações únicas. (Isso significaria que uma única letra é suficiente.) O ajuste padrão é `ascii`. Esta opção afeta apenas os formatos de saída `aligned` e `wrapped`.

O estilo `ascii` utiliza caracteres ASCII simples. As novas linhas de dados são mostradas usando o símbolo `+` na margem direita. Quando o formato `wrapped` enquadra dados de uma linha para a próxima sem um caractere de nova linha, um ponto (`.`) é mostrado na margem direita da primeira linha e novamente na margem esquerda da linha seguinte.

O estilo `old-ascii` usa caracteres ASCII simples, usando o estilo de formatação usado no PostgreSQL 8.4 e versões anteriores. As novas linhas de dados são mostradas usando um símbolo `:` em vez do separador da coluna à esquerda. Quando os dados são enrolados de uma linha para a próxima sem um caractere de nova linha, um símbolo `;` é usado em vez do separador da coluna à esquerda.

O estilo `unicode` utiliza caracteres de desenho de caixa Unicode. As novas linhas de dados são mostradas usando um símbolo de retorno de carro no margem direita. Quando os dados são enrolados de uma linha para a próxima sem um caractere de nova linha, um símbolo de elipse é mostrado na margem direita da primeira linha e, novamente, na margem esquerda da linha seguinte.

Quando o ajuste `border` for maior que zero, a opção `linestyle` também determina os caracteres com os quais as linhas de borda são desenhadas. Os caracteres ASCII simples funcionam em todos os lugares, mas os caracteres Unicode ficam mais bonitos em monitores que os reconhecem.

`null` [#](#APP-PSQL-META-COMMAND-PSET-NULL) :   Define a string que será impressa no lugar de um valor nulo. O padrão é imprimir nada, o que pode ser facilmente confundido com uma string vazia. Por exemplo, pode-se preferir `\pset null '(null)'`.

`numericlocale` [#](#APP-PSQL-META-COMMAND-PSET-NUMERICLOCALE) :   Se *`value`* for especificado deve ser `on` ou `off` que habilitará ou desabilitará a exibição de um caractere específico do local para separar grupos de dígitos à esquerda do marcador decimal. Se *`value`* for omitido, o comando alternará entre saída numérica regular e específica do local.

`pager` [#](#APP-PSQL-META-COMMAND-PSET-PAGER) :   Controles utilizam um programa de pager para saída de consulta e psql ajudando. Quando a opção `pager` é `off`, o programa de pager não é utilizado. Quando a opção `pager` é `on`, o pager é utilizado quando apropriado, ou seja, quando a saída é para um terminal e não cabe na tela. A opção `pager` também pode ser definida como `always`, o que faz com que o pager seja utilizado para todas as saídas de terminal independentemente de se encaixar na tela. `\pset pager` sem um *`value`* ativa e desativa o uso do pager.

Se a variável de ambiente `PSQL_PAGER` ou `PAGER` estiver definida, a saída a ser paginada é redirecionada para o programa especificado. Caso contrário, é usado um programa padrão dependente da plataforma (como `more`).

Ao usar o comando `\watch` para executar uma consulta repetidamente, a variável de ambiente `PSQL_WATCH_PAGER` é usada para encontrar o programa de pager em vez disso, em sistemas Unix. Isso é configurado separadamente porque pode confundir pagers tradicionais, mas pode ser usado para enviar saída para ferramentas que entendem o formato de saída do psql (como `pspg --stream`).

`pager_min_lines` [#](#APP-PSQL-META-COMMAND-PSET-PAGER-MIN-LINES) :   Se `pager_min_lines` estiver definido com um número maior que a altura da página, o programa de paginador não será chamado, a menos que haja pelo menos essa quantidade de linhas de saída a serem exibidas. O ajuste padrão é 0.

`recordsep` [#](#APP-PSQL-META-COMMAND-PSET-RECORDSEP) :   Especifica o separador de registro (linha) a ser usado no formato de saída não alinhado. O padrão é um caractere de nova linha.

`recordsep_zero` [#](#APP-PSQL-META-COMMAND-PSET-RECORDSEP-ZERO) :   Define o separador de registro a ser usado no formato de saída não alinhada com um byte zero.

`tableattr` (ou `T`) [#](#APP-PSQL-META-COMMAND-PSET-TABLEATTR) :   Em formato HTML, especifica atributos a serem colocados dentro da tag `table`. Isso, por exemplo, pode ser `cellpadding` ou `bgcolor`. Note que você provavelmente não quer especificar `border` aqui, pois isso já está sendo atendido por `\pset border`. Se não for fornecido *`value`*, os atributos da tabela são desativados.

Em formato `latex-longtable`, este controla a largura proporcional de cada coluna que contém um tipo de dados alinhado à esquerda. É especificado como uma lista de valores separados por espaços em branco, por exemplo, `'0.2 0.2 0.6'`. Colunas de saída não especificadas usam o último valor especificado.

`title` (ou `C`) [#](#APP-PSQL-META-COMMAND-PSET-TITLE) :   Define o título da tabela para quaisquer tabelas impressas posteriormente. Isso pode ser usado para fornecer etiquetas descritivas para sua saída. Se não for fornecido o *`value`*, o título não será definido.

`tuples_only` (ou `t`) [#](#APP-PSQL-META-COMMAND-PSET-TUPLES-ONLY) :   Se *`value`* for especificado deve ser `on` ou `off` que habilitará ou desabilitará o modo apenas de tuplas. Se *`value`* for omitido, o comando alternará entre saída regular e apenas de tuplas. A saída regular inclui informações extras, como cabeçalhos de coluna, títulos e vários rodapés. No modo apenas de tuplas, apenas os dados reais da tabela são mostrados.

`unicode_border_linestyle` [#](#APP-PSQL-META-COMMAND-PSET-UNICODE-BORDER-LINESTYLE) :   Define o estilo de desenho da borda para o estilo de linha do `unicode` , que pode ser um dos estilos de linha do `single` ou `double`.

`unicode_column_linestyle` [#](#APP-PSQL-META-COMMAND-PSET-UNICODE-COLUMN-LINESTYLE) :   Define o estilo de desenho da coluna para o estilo de linha do `unicode` , que pode ser um dos estilos de linha do `single` ou `double`.

`unicode_header_linestyle` [#](#APP-PSQL-META-COMMAND-PSET-UNICODE-HEADER-LINESTYLE) :   Define o estilo de desenho do cabeçalho para o estilo de linha `unicode` para um dos estilos de linha `single` ou `double`.

`xheader_width` [#](#APP-PSQL-META-COMMAND-PSET-XHEADER-WIDTH) : Define a largura máxima do cabeçalho para saída expandida como um dos valores de: `full`, `column`, `page` ou um *`integer value`*.

`full`: o cabeçalho expandido não é truncado, e será tão largo quanto a linha de saída mais larga.

`column`: truncar a linha do cabeçalho ao tamanho da primeira coluna.

`page`: truncar a linha do cabeçalho até o comprimento do terminal.

*`integer value`*: especifique a largura máxima exata da linha do cabeçalho.

Ilustrações de como esses diferentes formatos se parecem podem ser vistas em [Exemplos](app-psql.md#APP-PSQL-EXAMPLES "Examples"), abaixo.

### DICA

Existem vários comandos atalhos para `\pset`. Veja `\a`, `\C`, `\f`, `\H`, `\t`, `\T`, e `\x`.

`\q` ou `\quit` [#](#APP-PSQL-META-COMMAND-QUIT): Finaliza o programa psql. Em um arquivo de script, apenas a execução desse script é finalizada.

`\qecho text [ ... ]` [#](#APP-PSQL-META-COMMAND-QECHO): Este comando é idêntico a `\echo`, exceto que a saída será escrita no canal de saída da consulta, conforme definido por `\o`.

`\r` ou `\reset` [#](#APP-PSQL-META-COMMAND-RESET): Redefine (limpa) o buffer de consulta.

`\restrict restrict_key` [#](#APP-PSQL-META-COMMAND-RESTRICT): Entre no modo "restritivo" com a chave fornecida. Nesse modo, o único meta-comando permitido é `\unrestrict`, para sair do modo restrito. A chave pode conter apenas caracteres alfanuméricos.

Este comando é destinado principalmente para uso em dumps de texto simples gerados por pg_dump, pg_dumpall e pg_restore, mas pode ser útil em outros lugares.

`\s [ filename ]` [#](#APP-PSQL-META-COMMAND-S): Imprimir o histórico de linha de comando do psql para *`filename`*. Se *`filename`* for omitido, o histórico é escrito na saída padrão (usando o pager, se apropriado). Este comando não está disponível se o psql foi construído sem suporte a Readline.

`\set [ name [ value [ ... ] ] ]` [#](#APP-PSQL-META-COMMAND-SET): Define a variável psql *`name`* para *`value`*, ou, se forem fornecidos mais de um valor, para a concatenação de todos eles. Se apenas um argumento for fornecido, a variável é definida para um valor de cadeia vazia. Para desdefinir uma variável, use o comando `\unset`.

`\set` sem quaisquer argumentos exibe os nomes e valores de todas as variáveis psql atualmente definidas.

Os nomes de variáveis válidos podem conter letras, dígitos e sublinhados. Consulte [Variáveis](app-psql.md#APP-PSQL-VARIABLES) abaixo para obter detalhes. Os nomes de variáveis são sensíveis ao caso.

Algumas variáveis são especiais, pois controlam o comportamento do psql ou são automaticamente definidas para refletir o estado da conexão. Essas variáveis são documentadas em [Variáveis](app-psql.md#APP-PSQL-VARIABLES), abaixo.

### Nota

Este comando não está relacionado ao comando SQL `SET` (sql-set.md "SET").

`\setenv name [ value ]` [#](#APP-PSQL-META-COMMAND-SETENV): Define a variável de ambiente *`name`* para *`value`*, ou se o *`value`* não for fornecido, desativa a variável de ambiente. Exemplo:

```
testdb=> \setenv PAGER less testdb=> \setenv LESS -imx4F
```

`\sf[+] function_description` [#](#APP-PSQL-META-COMMAND-SF): Este comando recupera e exibe a definição da função ou procedimento nomeado, na forma de um comando `CREATE OR REPLACE FUNCTION` ou `CREATE OR REPLACE PROCEDURE`, A definição é impressa no canal de saída atual da consulta, definido por `\o`.

A função alvo pode ser especificada apenas pelo nome, ou pelo nome e pelos argumentos, por exemplo, `foo(integer, text)`. Os tipos de argumentos devem ser fornecidos se houver mais de uma função com o mesmo nome.

Se `+` for anexado ao nome do comando, as linhas de saída serão numeradas, com a primeira linha do corpo da função sendo a linha 1.

Ao contrário da maioria dos outros meta-comandos, todo o resto da linha é sempre considerado o(s) argumento(s) de `\sf`, e nem a interpolação de variáveis nem a expansão de aspas duplas são realizadas nos argumentos.

`\sv[+] view_name` [#](#APP-PSQL-META-COMMAND-SV): Este comando recupera e exibe a definição da visão nomeada, na forma de um comando `CREATE OR REPLACE VIEW`. A definição é impressa no canal de saída da consulta atual, definido por `\o`.

Se `+` for anexado ao nome do comando, as linhas de saída serão numeradas a partir do número 1.

Ao contrário da maioria dos outros meta-comandos, todo o resto da linha é sempre considerado o(s) argumento(s) de `\sv`, e nem a interpolação de variáveis nem a expansão de aspas duplas são realizadas nos argumentos.

`\startpipeline` `\sendpipeline` `\syncpipeline` `\endpipeline` `\flushrequest` `\flush` `\getresults [ number_results ]` [#](#APP-PSQL-META-COMMAND-PIPELINE): Este grupo de comandos implementa a linha de comandos de instruções SQL. Uma linha de comandos deve começar com um `\startpipeline` e terminar com um `\endpipeline`. Entre eles, pode haver qualquer número de comandos `\syncpipeline`, que envia uma mensagem de sincronização (protocol-flow.md#PROTOCOL-FLOW-EXT-QUERY "54.2.3. Extended Query") sem encerrar a linha de comandos em andamento e limpar o buffer de envio. No modo de linha de comandos, as instruções são enviadas ao servidor sem esperar pelos resultados das instruções anteriores. Veja [Seção 32.5](libpq-pipeline-mode.md "32.5. Pipeline Mode") para mais detalhes.

Todas as consultas executadas enquanto um pipeline está em andamento utilizam o protocolo de consulta estendido. As consultas são anexadas ao pipeline ao final de um ponto e vírgula. Os meta-comandos `\bind`, `\bind_named`, `\close_prepared` ou `\parse` podem ser utilizados em um pipeline em andamento. Enquanto o pipeline está em andamento, `\sendpipeline` anexará o buffer atual da consulta ao pipeline. Outros meta-comandos como `\g`, `\gx` ou `\gdesc` não são permitidos no modo pipeline.

`\flushrequest` adiciona um comando de limpeza à pipeline, permitindo ler resultados com `\getresults` sem emitir um sincronismo ou encerrar a pipeline. `\getresults` empurrará automaticamente dados não enviados para o servidor. `\flush` pode ser usado para empurrar manualmente dados não enviados.

`\getresults` aceita um parâmetro opcional *`number_results`*. Se fornecido, apenas os primeiros resultados pendentes de *`number_results`* serão lidos. Se não for fornecido ou `0`, todos os resultados pendentes são lidos.

Quando o modo de pipeline está ativo, uma variável de prompt dedicada está disponível para relatar o status do pipeline. Consulte `%P` para mais detalhes

`COPY` não é suportado enquanto no modo de pipeline.

Exemplo:

```
\startpipeline SELECT * FROM pg_class; SELECT 1 \bind \sendpipeline \flushrequest \getresults \endpipeline
```

`\t` [#](#APP-PSQL-META-COMMAND-T-LC): Ativa ou desativa a exibição de cabeçalhos de colunas de saída e contagem de linhas de rodapé. Esse comando é equivalente a `\pset tuples_only` e é fornecido por conveniência.

`\T table_options` [#](#APP-PSQL-META-COMMAND-T-UC): Especifica atributos a serem colocados dentro da `table` tag no formato de saída HTML. Este comando é equivalente a `\pset tableattr table_options`.

`\timing [ on | off ]` [#](#APP-PSQL-META-COMMAND-TIMING): Com um parâmetro, ativa ou desativa a exibição de quanto tempo cada declaração SQL leva. Sem um parâmetro, alternar a exibição entre ligado e desligado. A exibição é em milissegundos; intervalos mais longos do que 1 segundo também são mostrados no formato minutos:segundos, com campos de horas e dias adicionados, se necessário.

`\unrestrict restrict_key` [#](#APP-PSQL-META-COMMAND-UNRESTRICT): Sair do modo "restritivo" (ou seja, onde todos os outros comandos meta são bloqueados), desde que a chave especificada corresponda àquela fornecida para `\restrict` quando o modo restrito foi inserido.

Este comando é destinado principalmente para uso em dumps de texto simples gerados por pg_dump, pg_dumpall e pg_restore, mas pode ser útil em outros lugares.

`\unset name` [#](#APP-PSQL-META-COMMAND-UNSET): Desfaz (deleta) a variável psql *`name`*.

A maioria das variáveis que controlam o comportamento do psql não pode ser desativada; em vez disso, um comando `\unset` é interpretado como o estabelecimento de seus valores padrão. Veja [Variáveis](app-psql.md#APP-PSQL-VARIABLES) abaixo.

`\w` ou `\write` *`filename`* `\w` ou `\write` `|`*`command`* [#](#APP-PSQL-META-COMMAND-WRITE): Escreve o buffer de consulta atual no arquivo *`filename`* ou o pipeia para o comando de shell *`command`*. Se o buffer de consulta atual estiver vazio, a consulta executada mais recentemente é escrita em vez disso.

Se o argumento começar com `|`, então todo o restante da linha é considerado o *`command`* a ser executado, e nem a interpolação de variáveis nem a expansão de aspas são realizadas nele. O resto da linha é simplesmente passado literalmente para a concha.

`\warn text [ ... ]` [#](#APP-PSQL-META-COMMAND-WARN): Este comando é idêntico a `\echo`, exceto que a saída será escrita no canal de erro padrão do psql, em vez da saída padrão.

Execute repetidamente o buffer de consulta atual (como o `\g` faz) até ser interrompido, ou a consulta falhar, ou o limite de contagem de execução (se dado) for atingido, ou a consulta não retorne mais o número mínimo de linhas. Aguarde o número especificado de segundos (padrão 2) entre as execuções. O intervalo de espera padrão pode ser alterado com a variável [`WATCH_INTERVAL`](app-psql.md#APP-PSQL-VARIABLES-WATCH-INTERVAL). Para compatibilidade reversa, *`seconds`* pode ser especificado com ou sem um prefixo de `interval=`. Cada resultado da consulta é exibido com um cabeçalho que inclui a string `\pset title` (se houver), o tempo a partir do início da consulta e o intervalo de atraso.

Se o buffer de consulta atual estiver vazio, a consulta enviada mais recentemente é executada novamente.

`\x [ on | off | auto ]` [#](#APP-PSQL-META-COMMAND-X): Define ou ativa o modo de formatação de tabela expandida. Como tal, é equivalente a `\pset expanded`.

`\z[Sx] [ pattern ]` [#](#APP-PSQL-META-COMMAND-Z)   Lista tabelas, visualizações e sequências com seus privilégios de acesso associados. Se um *`pattern`* for especificado, apenas tabelas, visualizações e sequências cujos nomes correspondem ao padrão são listados. Por padrão, apenas objetos criados pelo usuário são mostrados; forneça um padrão ou o modificador `S` para incluir objetos do sistema. Se `x` for anexado ao nome do comando, os resultados são exibidos no modo expandido.

Este é um alias para `\dp` (“exibir privilégios”).

`\! [ command ]` [#](#APP-PSQL-META-COMMAND-EXCLAMATION-MARK): Sem argumento, escapa para uma sub-shell; psql retoma quando a sub-shell sai. Com um argumento, executa o comando de shell *`command`*.

Ao contrário da maioria dos outros meta-comandos, o restante inteiro da linha é sempre considerado o(s) argumento(s) de `\!`, e nem a interpolação de variáveis nem a expansão de aspas são realizadas nos argumentos. O restante da linha é simplesmente passado literalmente para o shell.

`\? [ topic ]` [#](#APP-PSQL-META-COMMAND-QUESTION-MARK)  Mostra informações de ajuda. O parâmetro opcional *`topic`* (com valor padrão `commands`) seleciona qual parte do psql é explicada: `commands` descreve os comandos de barra invertida do psql; `options` descreve as opções de linha de comando que podem ser passadas ao psql; e `variables` mostra ajuda sobre as variáveis de configuração do psql.

`\;` [#](#APP-PSQL-META-COMMAND-SEMICOLON): O backslash-ponto-e-vírgula não é um comando meta da mesma maneira que os comandos anteriores; em vez disso, ele simplesmente faz com que um ponto-e-vírgula seja adicionado ao buffer de consulta sem qualquer processamento adicional.

Normalmente, o psql envia um comando SQL para o servidor assim que atinge o ponto-e-vírgula que marca o fim do comando, mesmo que mais entrada permaneça na linha atual. Portanto, por exemplo, ao digitar

```
select 1; select 2; select 3;
```

resultará no envio individual dos três comandos SQL ao servidor, com os resultados de cada um sendo exibidos antes de continuar para o próximo comando. No entanto, um ponto e vírgula inserido como `\;` não acionará o processamento do comando, de modo que o comando anterior e o seguinte sejam efetivamente combinados e enviados ao servidor em uma única solicitação. Portanto, por exemplo

```
select 1\; select 2\; select 3;
```

leva ao envio dos três comandos SQL para o servidor em uma única solicitação, quando o ponto-e-vírgula não recuado é alcançado. O servidor executa tal solicitação como uma única transação, a menos que haja explicitamente comandos `BEGIN`/`COMMIT` incluídos na string para dividi-la em múltiplas transações. (Consulte [Seção 54.2.2.1](protocol-flow.md#PROTOCOL-FLOW-MULTI-STATEMENT) para mais detalhes sobre como o servidor lida com strings de várias consultas.)

#### Padrões

Os vários comandos `\d` aceitam um parâmetro *`pattern`* para especificar o(s) nome(s) do(s) objeto(s) a ser(em) exibido(s). No caso mais simples, um padrão é apenas o nome exato do objeto. Os caracteres dentro de um padrão são normalmente dobrados para minúsculas, assim como nos nomes do SQL; por exemplo, `\dt FOO` exibirá a tabela denominada `foo`. Como nos nomes do SQL, colocar aspas duplas em torno de um padrão para não dobrar para minúsculas. Se você precisar incluir um caractere de aspas reais em um padrão, escreva-o como um par de aspas dentro de uma sequência de aspas; novamente, isso está de acordo com as regras para identificadores com aspas do SQL. Por exemplo, `\dt "FOO""BAR"` exibirá a tabela denominada `FOO"BAR` (não `foo"bar`). Ao contrário das regras normais para nomes do SQL, você pode colocar aspas duplas apenas em parte de um padrão, por exemplo, `\dt FOO"FOO"BAR` exibirá a tabela denominada `fooFOObar`.

Sempre que o parâmetro *`pattern`* é omitido completamente, os comandos `\d` exibem todos os objetos que são visíveis no caminho de pesquisa do esquema atual — isso é equivalente ao uso de `*` como padrão. (Um objeto é dito *visível* se seu esquema contendo estiver no caminho de pesquisa e nenhum objeto do mesmo tipo e nome aparece anteriormente no caminho de pesquisa. Isso é equivalente à declaração de que o objeto pode ser referenciado pelo nome sem qualificação explícita do esquema.) Para ver todos os objetos no banco de dados, independentemente da visibilidade, use `*.*` como padrão.

Dentro de um padrão, `*` corresponde a qualquer sequência de caracteres (incluindo nenhum caractere) e `?` corresponde a qualquer único caractere.

(Essa notação é comparável aos padrões de nomes de arquivos de shell Unix.) Por exemplo, `\dt int*` exibe tabelas cujos nomes começam com `int`. Mas dentro de aspas duplas, `*` e `?` perdem esses significados especiais e são apenas correspondidos literalmente.

Um padrão de relação que contém um ponto (`.`) é interpretado como um padrão de nome de esquema. Por exemplo, `\dt foo*.*bar*` exibe todas as tabelas cujo nome de tabela inclui `bar` que estão em esquemas cujo nome de esquema começa com `foo`. Quando não aparece nenhum ponto, então o padrão concorda apenas com objetos que são visíveis no caminho de busca atual do esquema. Novamente, um ponto dentro de aspas perde seu significado especial e é compatível literalmente. Um padrão de relação que contém dois pontos (`.`) é interpretado como um nome de banco de dados seguido por um padrão de nome de esquema seguido por um padrão de nome de objeto. A porção do nome do banco de dados não será tratada como um padrão e deve corresponder ao nome do banco de dados conectado atualmente, caso contrário será gerado um erro.

Um padrão de esquema que contém um ponto (`.`) é interpretado como um nome de banco de dados seguido de um padrão de nome de esquema. Por exemplo, `\dn mydb.*foo*` exibe todos os esquemas cujo nome de esquema inclui `foo`. A parte do nome do banco de dados não será tratada como um padrão e deve corresponder ao nome do banco de dados conectado atualmente, caso contrário, um erro será exibido.

Os usuários avançados podem usar notações de expressão regular, como classes de caracteres, por exemplo, `[0-9]` para corresponder a qualquer dígito. Todos os caracteres especiais de expressão regular funcionam conforme especificado em [Seção 9.7.3](functions-matching.md#FUNCTIONS-POSIX-REGEXP "9.7.3. POSIX Regular Expressions"), exceto para `.` que é tomado como um separador conforme mencionado acima, `*` que é traduzido para a notação de expressão regular `.*`, `?` que é traduzido para `.`, e `$` que é correspondido literalmente. Você pode emular esses caracteres de padrão conforme necessário, escrevendo `?` para `.`, `(R+|)` para `R*`, ou `(R|)` para `R?`. `$` não é necessário como um caractere de expressão regular, uma vez que o padrão deve corresponder ao nome inteiro, ao contrário da interpretação usual de expressões regulares (em outras palavras, `$` é automaticamente anexado ao seu padrão). Escreva `*` no começo e/ou fim se você não deseja que o padrão seja ancorado. Note que, dentro de aspas, todos os caracteres especiais de expressão regular perdem seus significados especiais e são correspondidos literalmente. Além disso, os caracteres especiais de expressão regular são correspondidos literalmente em padrões de nomes de operadores (ou seja, o argumento de `\do`).

### Recursos Avançados

#### Variáveis

psql oferece substituição de variáveis com características semelhantes às das caixas de comandos comuns do Unix. As variáveis são simplesmente pares nome/valor, onde o valor pode ser qualquer string de qualquer comprimento. O nome deve consistir em letras (incluindo letras não latinas), dígitos e sublinhados.

Para definir uma variável, use o meta-comando psql `\set`. Por exemplo,

```
testdb=> \set foo bar
```

define a variável `foo` para o valor `bar`. Para recuperar o conteúdo da variável, antecipe o nome com um colon, por exemplo:

```
testdb=> \echo :foo bar
```

Isso funciona tanto em comandos SQL regulares quanto em meta-comandos; há mais detalhes em [Interpolação SQL](app-psql.md#APP-PSQL-INTERPOLATION), abaixo.

Se você chamar `\set` sem um segundo argumento, a variável é definida com um valor de cadeia vazia. Para desdefinir (ou seja, excluir) uma variável, use o comando `\unset`. Para mostrar os valores de todas as variáveis, chame `\set` sem qualquer argumento.

### Nota

Os argumentos de `\set` estão sujeitos às mesmas regras de substituição que com outros comandos. Assim, você pode construir referências interessantes, como `\set :foo 'something'`, e obter "links suaves" ou "variáveis variáveis" de fama de Perl ou PHP, respectivamente. Infelizmente (ou por sorte?), não há como fazer algo útil com esses construtos. Por outro lado, `\set bar :foo` é uma maneira perfeitamente válida de copiar uma variável.

Várias dessas variáveis são tratadas especialmente pelo psql. Elas representam certos ajustes de opção que podem ser alterados no momento da execução, alterando o valor da variável, ou, em alguns casos, representam o estado modificável do psql. Por convenção, todos os nomes de variáveis tratadas especialmente consistem em todas as letras maiúsculas do ASCII (e, possivelmente, dígitos e sublinhados). Para garantir a compatibilidade máxima no futuro, evite usar tais nomes de variáveis para seus próprios propósitos.

As variáveis que controlam o comportamento do psql geralmente não podem ser desativadas ou definidas com valores inválidos. Um comando `\unset` é permitido, mas é interpretado como a definição da variável com seu valor padrão. Um comando `\set` sem um segundo argumento é interpretado como a definição da variável com `on`, para as variáveis de controle que aceitam esse valor, e é rejeitado para outras. Além disso, as variáveis de controle que aceitam os valores `on` e `off` também aceitarão outras grafias comuns de valores booleanos, como `true` e `false`.

As variáveis especialmente tratadas são:

`AUTOCOMMIT` [#](#APP-PSQL-VARIABLES-AUTOCOMMIT): Quando `on` (padrão), cada comando SQL é automaticamente commitado após a conclusão bem-sucedida. Para adiar o commit nesse modo, você deve inserir um comando SQL de `BEGIN` ou `START TRANSACTION`. Quando `off` ou não definido, os comandos SQL não são comprometidos até que você emita explicitamente `COMMIT` ou `END`. O modo off autocommit funciona emitindo um `BEGIN` implícito para você, logo antes de qualquer comando que não esteja em um bloco de transação e não seja ele mesmo um `BEGIN` ou outro comando de controle de transação, nem um comando que não possa ser executado dentro de um bloco de transação (como `VACUUM`).

### Nota

No modo de autocommit-off, você deve explicitamente abandonar qualquer transação falha, inserindo `ABORT` ou `ROLLBACK`. Além disso, lembre-se de que, se você sair da sessão sem cometer, seu trabalho será perdido.

### Nota

O modo autocommit-on é o comportamento tradicional do PostgreSQL, mas o autocommit-off está mais próximo da especificação SQL. Se você prefere o autocommit-off, pode querer configurá-lo no arquivo de nível de sistema `psqlrc` ou no seu arquivo `~/.psqlrc`.

`COMP_KEYWORD_CASE` [#](#APP-PSQL-VARIABLES-COMP-KEYWORD-CASE)   Determina qual caso de letra usar ao completar uma palavra-chave SQL. Se definido como `lower` ou `upper`, a palavra completada será em letras minúsculas ou maiúsculas, respectivamente. Se definido como `preserve-lower` ou `preserve-upper` (o padrão), a palavra completada será no caso da palavra já inserida, mas palavras que estão sendo completadas sem nada inserido serão em letras minúsculas ou maiúsculas, respectivamente.

`DBNAME` [#](#APP-PSQL-VARIABLES-DBNAME): O nome do banco de dados ao qual você está conectado atualmente. Este é definido sempre que você se conecta a um banco de dados (incluindo o inicialização do programa), mas pode ser alterado ou desfeito.

`ECHO` [#](#APP-PSQL-VARIABLES-ECHO): Se configurado para `all`, todas as linhas de entrada não vazias são impressas no saída padrão conforme elas são lidas. (Isso não se aplica às linhas lidas interativamente.) Para selecionar esse comportamento no início do programa, use a chave `-a`. Se configurado para `queries`, psql imprime cada consulta na saída padrão conforme ela é enviada ao servidor. A chave para selecionar esse comportamento é `-e`. Se configurado para `errors`, então apenas as consultas falhadas são exibidas na saída de erro padrão. A chave para esse comportamento é `-b`. Se configurado para `none` (o padrão), então nenhuma consulta é exibida.

`ECHO_HIDDEN` [#](#APP-PSQL-VARIABLES-ECHO-HIDDEN): Quando essa variável é definida como `on` e um comando de barra invertida consulta o banco de dados, a consulta é exibida primeiro. Essa funcionalidade ajuda você a estudar os internals do PostgreSQL e fornecer funcionalidade semelhante em seus próprios programas. (Para selecionar esse comportamento no início do programa, use a opção `-E`.]) Se você definir esta variável para o valor `noexec`, as consultas são apresentadas, mas não são realmente enviadas ao servidor e executadas. O valor padrão é `off`.

`ENCODING` [#](#APP-PSQL-VARIABLES-ENCODING): O atual conjunto de codificação de caracteres do cliente. Isso é definido toda vez que você se conecta a um banco de dados (incluindo o início do programa), e quando você altera a codificação com `\encoding`, mas pode ser alterado ou desativado.

`ERROR` [#](#APP-PSQL-VARIABLES-ERROR): `true` se a última consulta SQL falhou, `false` se sucediu. Veja também `SQLSTATE`.

`FETCH_COUNT` [#](#APP-PSQL-VARIABLES-FETCH-COUNT) : Se essa variável for definida com um valor inteiro maior que zero, os resultados das consultas de `SELECT` são obtidos e exibidos em grupos com tantas linhas quanto o número definido, em vez do comportamento padrão de coletar todo o conjunto de resultados antes da exibição. Portanto, apenas uma quantidade limitada de memória é usada, independentemente do tamanho do conjunto de resultados. Configurações de 100 a 1000 são comumente usadas ao habilitar essa funcionalidade. Lembre-se de que, ao usar essa funcionalidade, uma consulta pode falhar após ter exibido algumas linhas.

### DICA

Embora você possa usar qualquer formato de saída com este recurso, o formato padrão `aligned` tende a parecer ruim porque cada grupo de linhas `FETCH_COUNT` será formatado separadamente, levando a diferentes larguras de coluna nos grupos de linhas. Os outros formatos de saída funcionam melhor.

`HIDE_TABLEAM` [#](#APP-PSQL-VARIABLES-HIDE-TABLEAM): Se essa variável estiver definida como `true`, os detalhes do método de acesso de uma tabela não serão exibidos. Isso é principalmente útil para testes de regressão.

`HIDE_TOAST_COMPRESSION` [#](#APP-PSQL-VARIABLES-HIDE-TOAST-COMPRESSION): Se essa variável estiver definida como `true`, os detalhes do método de compressão da coluna não serão exibidos. Isso é principalmente útil para testes de regressão.

`HISTCONTROL` [#](#APP-PSQL-VARIABLES-HISTCONTROL) : Se esta variável estiver definida como `ignorespace`, linhas que começam com um espaço não são inseridas na lista de histórico. Se definida como um valor de `ignoredups`, linhas que correspondem à linha de histórico anterior não são inseridas. Um valor de `ignoreboth` combina as duas opções. Se definida como `none` (padrão), todas as linhas lidas no modo interativo são salvas na lista de histórico.

### Nota

Essa característica foi plágio descarado do Bash.

`HISTFILE` [#](#APP-PSQL-VARIABLES-HISTFILE): O nome do arquivo que será usado para armazenar a lista de histórico. Se não definido, o nome do arquivo é retirado da variável de ambiente `PSQL_HISTORY` . Se essa não for definida, o padrão é `~/.psql_history`, ou `%APPDATA%\postgresql\psql_history` no Windows. Por exemplo, colocando:

```
\set HISTFILE ~/.psql_history-:DBNAME
```

Em `~/.psqlrc`, isso fará com que o psql mantenha um histórico separado para cada banco de dados.

### Nota

Essa característica foi plágio descarado do Bash.

`HISTSIZE` [#](#APP-PSQL-VARIABLES-HISTSIZE): O número máximo de comandos para armazenar no histórico de comandos (padrão 500). Se definido como um valor negativo, não há limite aplicado.

### Nota

Essa característica foi plágio descarado do Bash.

`HOST` [#](#APP-PSQL-VARIABLES-HOST): O servidor de banco de dados ao qual você está conectado atualmente. Isso é definido sempre que você se conecta a um banco de dados (incluindo o inicialização do programa), mas pode ser alterado ou desativado.

`IGNOREEOF` [#](#APP-PSQL-VARIABLES-IGNOREEOF): Se definido como 1 ou menos, enviar um caractere EOF (geralmente **Ctrl**+**D**) para uma sessão interativa do psql terminará o aplicativo. Se definido como um valor numérico maior, esse número consecutivo de caracteres EOF deve ser digitado para terminar uma sessão interativa. Se a variável for definida como um valor não numérico, ela será interpretada como 10. O padrão é 0.

### Nota

Essa característica foi plágio descarado do Bash.

`LASTOID` [#](#APP-PSQL-VARIABLES-LASTOID): O valor do último OID afetado, conforme retornado por um `INSERT` ou `\lo_import` comando. Esta variável só é garantida como válida até após o resultado do próximo comando SQL ter sido exibido. Servidores PostgreSQL a partir da versão 12 não apoiam mais colunas de sistema OID, portanto, LASTOID sempre será 0 após `INSERT` ao direcionar esses servidores.

`LAST_ERROR_MESSAGE` `LAST_ERROR_SQLSTATE` [#](#APP-PSQL-VARIABLES-LAST-ERROR-MESSAGE): A mensagem de erro principal e o código SQLSTATE associado para a consulta mais recente que falhou na sessão atual do psql, ou uma string vazia e `00000` se não houver ocorrido erro na sessão atual.

`ON_ERROR_ROLLBACK` [#](#APP-PSQL-VARIABLES-ON-ERROR-ROLLBACK): Quando definido como `on`, se uma declaração em um bloco de transação gerar um erro, o erro é ignorado e a transação continua. Quando definido como `interactive`, tais erros são ignorados apenas em sessões interativas, e não ao ler arquivos de script. Quando definido como `off` (o padrão), uma declaração em um bloco de transação que gera um erro interrompe toda a transação. O modo de rollback de erro funciona emitindo um `SAVEPOINT` implícito para você, logo antes de cada comando que está em um bloco de transação, e depois revertendo para o ponto de salvamento se o comando falhar.

`ON_ERROR_STOP` [#](#APP-PSQL-VARIABLES-ON-ERROR-STOP): Por padrão, o processamento do comando continua após um erro. Quando esta variável é definida como `on`, o processamento será interrompido imediatamente. No modo interativo, psql retornará ao prompt de comando; caso contrário, o psql encerrará, retornando código de erro 3 para distinguir este caso de condições de erro fatal, que são relatadas usando código de erro 1. Em qualquer caso, qualquer script atualmente em execução (o script de nível superior, se houver, e qualquer outro script que possa ter sido invocado) será encerrado imediatamente. Se a string de comando de nível superior contivesse múltiplos comandos SQL, o processamento será interrompido com o comando atual.

`PIPELINE_COMMAND_COUNT` [#](#APP-PSQL-VARIABLES-PIPELINE-COMMAND-COUNT): O número de comandos em fila em um pipeline em andamento.

`PIPELINE_RESULT_COUNT` [#](#APP-PSQL-VARIABLES-PIPELINE-RESULT-COUNT): O número de comandos de um pipeline em andamento que foram seguidos por uma `\flushrequest` ou uma `\syncpipeline`, forçando o servidor a enviar os resultados. Esses resultados podem ser recuperados com `\getresults`.

`PIPELINE_SYNC_COUNT` [#](#APP-PSQL-VARIABLES-PIPELINE-SYNC-COUNT): O número de mensagens de sincronização em fila em um pipeline em andamento.

`PORT` [#](#APP-PSQL-VARIABLES-PORT): A porta do servidor de banco de dados a qual você está conectado atualmente. Isso é definido toda vez que você se conecta a um banco de dados (incluindo o início do programa), mas pode ser alterado ou desativado.

`PROMPT1` `PROMPT2` `PROMPT3` [#](#APP-PSQL-VARIABLES-PROMPT): Estes especificam como os prompts que o psql emite devem ser. Veja [Prompting](app-psql.md#APP-PSQL-PROMPTING "Prompting") abaixo.

`QUIET` [#](#APP-PSQL-VARIABLES-QUIET): Definir essa variável para `on` é equivalente à opção de linha de comando `-q`. Provavelmente, não é muito útil no modo interativo.

`ROW_COUNT` [#](#APP-PSQL-VARIABLES-ROW-COUNT): O número de linhas devolvidas ou afetadas pela última consulta SQL, ou 0 se a consulta falhou ou não relatou um número de linhas.

`SERVER_VERSION_NAME` `SERVER_VERSION_NUM` [#](#APP-PSQL-VARIABLES-SERVER-VERSION-NAME): O número da versão do servidor como uma string, por exemplo, `9.6.2`, `10.1` ou `11beta1`, e em forma numérica, por exemplo, `90602` ou `100001`. Estes são definidos sempre que você se conecta a um banco de dados (incluindo o início do programa), mas podem ser alterados ou desativados.

`SERVICE` [#](#APP-PSQL-VARIABLES-SERVICE): O nome do serviço, se aplicável.

`SHELL_ERROR` [#](#APP-PSQL-VARIABLES-SHELL-ERROR): `true` se o último comando de shell `false` se tiver sido bem-sucedido. Isso se aplica a comandos de shell invocados através dos meta-comandos `\!`, `\g`, `\o`, `\w`, e `\copy`, bem como a backquote (`` ` ``) expansion. Note that for `\o`, this variable is updated when the output pipe is closed by the next `\o` command. See also `SHELL_EXIT_CODE`.

O status de saída retornado pelo último comando de shell. 0–127 representa códigos de saída de programas, 128–255 indicam a terminação por um sinal, e -1 indica falha ao iniciar um programa ou ao coletar seu status de saída. Isso se aplica a comandos de shell invocados através dos meta-comandos `\!`, `\g`, `\o`, `\w`, e `\copy`, bem como as aspas duplas (`` ` `) expansion. Note that for `\o`, this variable is updated when the output pipe is closed by the next `\o` command. See also `SHELL_ERROR`.

`SHOW_ALL_RESULTS` [#](#APP-PSQL-VARIABLES-SHOW-ALL-RESULTS): Quando essa variável é definida como `off`, apenas o último resultado de uma consulta combinada (`\;`) é mostrado em vez de todos eles. O comportamento padrão é `on`. O comportamento off é para compatibilidade com versões mais antigas do psql.

`SHOW_CONTEXT` [#](#APP-PSQL-VARIABLES-SHOW-CONTEXT): Essa variável pode ser definida com os valores `never`, `errors` ou `always` para controlar se os campos `CONTEXT` são exibidos em mensagens do servidor. O padrão é `errors` (o que significa que o contexto será exibido em mensagens de erro, mas não em mensagens de aviso ou de alerta). Esse ajuste não tem efeito quando `VERBOSITY` é definido como `terse` ou `sqlstate`.

(Veja também `\errverbose`, para uso quando você deseja uma versão detalhada do erro que acabou de receber.)

`SINGLELINE` [#](#APP-PSQL-VARIABLES-SINGLELINE): Definir essa variável para `on` é equivalente à opção de linha de comando `-S`.

`SINGLESTEP` [#](#APP-PSQL-VARIABLES-SINGLESTEP): Definir essa variável para `on` é equivalente à opção de linha de comando `-s`.

`SQLSTATE` [#](#APP-PSQL-VARIABLES-SQLSTATE): O código de erro (consulte [Apêndice A](errcodes-appendix.md "Appendix A. PostgreSQL Error Codes")) associado ao fracasso da última consulta SQL, ou `00000` se ela tiver sido bem-sucedida.

`USER` [#](#APP-PSQL-VARIABLES-USER): O usuário do banco de dados ao qual você está conectado atualmente. Isso é definido toda vez que você se conecta a um banco de dados (incluindo o início do programa), mas pode ser alterado ou desativado.

`VERBOSITY` [#](#APP-PSQL-VARIABLES-VERBOSITY): Essa variável pode ser definida com os valores `default`, `verbose`, `terse`, ou `sqlstate` para controlar a verbosidade dos relatórios de erro.

(Veja também `\errverbose`, para uso quando você deseja uma versão detalhada do erro que acabou de receber.)

`VERSION` `VERSION_NAME` `VERSION_NUM` [#](#APP-PSQL-VARIABLES-VERSION): Essas variáveis são definidas no início do programa para refletir a versão do psql, respectivamente como uma string verbose, uma string curta (por exemplo, `9.6.2`, `10.1`, ou `11beta1`), e um número (por exemplo, `90602` ou `100001`). Elas podem ser alteradas ou desdefinidas.

`WATCH_INTERVAL` [#](#APP-PSQL-VARIABLES-WATCH-INTERVAL): Esta variável define o intervalo padrão, em segundos, que o `\watch` espera entre a execução da consulta. O padrão é de 2 segundos. Especificar um intervalo no comando substitui esta variável.

#### Interpolação SQL

Uma característica importante das variáveis do psql é que você pode substituí-las (interpolar) em declarações SQL regulares, bem como nos argumentos de comandos meta. Além disso, o psql oferece facilidades para garantir que os valores das variáveis usados como literais e identificadores SQL sejam corretamente citados. A sintaxe para interpolar um valor sem qualquer citação é preenchendo o nome da variável com um colon (`:`). Por exemplo,

```
testdb=> \set foo 'my_table' testdb=> SELECT * FROM :foo;
```

você deve consultar a tabela `my_table`. Note que isso pode ser inseguro: o valor da variável é copiado literalmente, portanto, pode conter aspas desequilibradas ou até mesmo comandos de barra invertida. Você deve garantir que faça sentido onde você o coloca.

Quando um valor deve ser usado como uma literal SQL ou identificador, é mais seguro organizá-lo para que seja citado. Para citar o valor de uma variável como uma literal SQL, escreva um colon seguido do nome da variável em aspas simples. Para citar o valor como um identificador SQL, escreva um colon seguido do nome da variável em aspas duplas. Esses construtos lidam corretamente com as citações e outros caracteres especiais incorporados no valor da variável. O exemplo anterior seria mais seguro escrito dessa maneira:

```
testdb=> \set foo 'my_table' testdb=> SELECT * FROM :"foo";
```

A interpolação variável não será realizada dentro de literais SQL e identificadores citados. Portanto, uma construção como `':foo'` não funciona para produzir um literal citado a partir do valor de uma variável (e seria inseguro se funcionasse, pois não trataria corretamente as citações embutidas no valor).

Um exemplo de uso desse mecanismo é copiar o conteúdo de um arquivo para uma coluna de tabela. Primeiro, carregue o arquivo em uma variável e, em seguida, intercale o valor da variável como uma string citada:

```
testdb=> \set content `cat my_file.txt` testdb=> INSERT INTO my_table VALUES (:'content');
```

(Observe que isso ainda não funcionará se `my_file.txt` contiver bytes NUL. O psql não suporta bytes NUL embutidos em valores variáveis.)

Como os pontos e vírgulas podem aparecer legalmente em comandos SQL, uma tentativa aparente de interpolação (ou seja, `:name`, `:'name'` ou `:"name"`) não é substituída, a menos que a variável nomeada esteja atualmente definida. Em qualquer caso, você pode escapar um ponto e vírgula com uma barra invertida para protegê-lo da substituição.

A sintaxe especial `:{?name}` retorna TRUE ou FALSE, dependendo se a variável existe ou não, e, portanto, é sempre substituída, a menos que o colon seja escapado com barra invertida.

A sintaxe de colon para variáveis é o SQL padrão para linguagens de consulta embutidas, como o ECPG. As sintaxes de colon para fatias de matriz e tipos de conversão são extensões do PostgreSQL, que, às vezes, podem entrar em conflito com o uso padrão. A sintaxe de colon-quoting para escapar o valor de uma variável como um literal ou identificador SQL é uma extensão do psql.

#### Promptando

Os prompts que o psql emite podem ser personalizados conforme sua preferência. As três variáveis `PROMPT1`, `PROMPT2` e `PROMPT3` contêm strings e sequências de escape especiais que descrevem a aparência do prompt. O Prompt 1 é o prompt normal que é emitido quando o psql solicita um novo comando. O Prompt 2 é emitido quando se espera mais entrada durante a entrada do comando, por exemplo, porque o comando não foi terminado com um ponto e vírgula ou uma citação não foi fechada. O Prompt 3 é emitido quando você está executando um comando SQL `COPY FROM STDIN` e precisa digitar um valor de linha no terminal.

O valor da variável de prompt selecionada é impresso literalmente, exceto quando um sinal de porcentagem (`%`) é encontrado. Dependendo do próximo caractere, outros textos são substituídos. As substituições definidas são:

`%M` [#](#APP-PSQL-PROMPTING-M-UC) :   O nome completo do servidor de banco de dados (com nome de domínio), ou `[local]` se a conexão for feita por meio de um socket de domínio Unix, ou `[local:/dir/name]`, se o socket de domínio Unix não estiver na localização pré-compilada por padrão.

`%m` [#](#APP-PSQL-PROMPTING-M-LC): O nome do host do servidor de banco de dados, truncado no primeiro ponto, ou `[local]` se a conexão for feita por meio de um socket de domínio Unix.

`%>` [#](#APP-PSQL-PROMPTING-GT): O número de porta na qual o servidor de banco de dados está ouvindo.

`%n` [#](#APP-PSQL-PROMPTING-N): Nome do usuário da sessão do banco de dados. (A expansão deste valor pode mudar durante uma sessão do banco de dados como resultado do comando `SET SESSION AUTHORIZATION`.)

`%s` [#](#APP-PSQL-PROMPTING-S): O nome do serviço.

`%/` [#](#APP-PSQL-PROMPTING-SLASH): O nome do banco de dados atual.

`%~` [#](#APP-PSQL-PROMPTING-TILDE): Como `%/`, mas a saída é `~` (tilde) se o banco de dados for o seu banco de dados padrão.

`%#` [#](#APP-PSQL-PROMPTING-NUMBERSIGN): Se o usuário da sessão for um superusuário do banco de dados, então um `#`, caso contrário, um `>`.

(A expansão deste valor pode mudar durante uma sessão do banco de dados como resultado do comando `SET SESSION AUTHORIZATION`.)

`%p` [#](#APP-PSQL-PROMPTING-P): O ID do processo do backend atualmente conectado.

`%P` [#](#APP-PSQL-PROMPTING-P-UC): Status do pipeline: `off` quando não está em pipeline, `on` quando está em pipeline em andamento ou `abort` quando está em pipeline abortado.

`%R` [#](#APP-PSQL-PROMPTING-R): Na prompt 1 normalmente `=`, mas `@` se a sessão estiver em um ramo inativo de um bloco condicional, ou `^` se no modo de linha única, ou `!` se a sessão estiver desconectada do banco de dados (o que pode acontecer se `\connect` falhar). Na prompt 2 `%R` é substituído por um caractere que depende de por que o psql espera mais entrada: `-` se o comando simplesmente não foi terminado ainda, mas `*` se houver um comentário inacabado `/* ... */` com comentário, uma única citação se houver uma string com comentário inacabada, uma dupla citação se houver um identificador com citação inacabada, um sinal de dólar se houver uma string com citação de dólar inacabada, ou `(` se houver um parêntese esquerdo não correspondente. Na prompt 3 `%R` não produz nada.

`%x` [#](#APP-PSQL-PROMPTING-X): Status da transação: uma string vazia quando não está em um bloco de transação, ou `*` quando está em um bloco de transação, ou `!` quando está em um bloco de transação falha, ou `?` quando o estado da transação é indeterminado (por exemplo, porque não há conexão).

`%l` [#](#APP-PSQL-PROMPTING-L): O número da linha dentro da declaração atual, a partir de `1`.

`%`*`digits`* [#](#APP-PSQL-PROMPTING-DIGITS): O caractere com o código octal indicado é substituído.

`%:`*`name`*`:` [#](#APP-PSQL-PROMPTING-NAME): O valor da variável psql *`name`*. Veja [Variáveis](app-psql.md#APP-PSQL-VARIABLES "Variables"), acima, para detalhes.

`` %` ``*` comando `*` `` ` comando *`, semelhante à substituição de “back-tick”

`%[` ... `%]` [#](#APP-PSQL-PROMPTING-SQUARE-BRACKETS): Os prompts podem conter caracteres de controle terminais que, por exemplo, alteram a cor, o fundo ou o estilo do texto do prompt ou alteram o título da janela do terminal. Para que as funcionalidades de edição de linha do Readline funcionem corretamente, esses caracteres de controle não imprimíveis devem ser designados como invisíveis ao os envolver com `%[` e `%]`. Pode haver múltiplos pares desses caracteres dentro do prompt. Por exemplo:

```
testdb=> \set PROMPT1 '%[%033[1;33;40m%]%n@%/%R%[%033[0m%]%# '
```

resulta em um prompt em amarelo sobre preto (`1;`) em `33;40` em terminais VT100 compatíveis e com capacidade de cores.

`%w` [#](#APP-PSQL-PROMPTING-W): Espaçamento com a mesma largura que a saída mais recente de `PROMPT1`. Isso pode ser usado como um `PROMPT2` de configuração, de modo que as declarações de várias linhas estejam alinhadas com a primeira linha, mas não há um prompt secundário visível.

Para inserir um sinal de porcentagem em seu prompt, escreva `%%`. Os prompts padrão são `'%/%R%x%# '` para os prompts 1 e 2, e `'>> '` para o prompt 3.

### Nota

Esse recurso foi plágio descarado de tcsh.

#### Edição em Linha de Comando

psql usa a biblioteca Readline ou libedit, se disponível, para edição e recuperação de linhas convenientes. O histórico de comandos é salvo automaticamente quando o psql sai e é carregado novamente quando o psql é iniciado. Digite seta para cima ou control-P para recuperar as linhas anteriores.

Você também pode usar a autocompletar para preencher palavras-chave parcialmente digitadas e nomes de objetos SQL em muitos (de forma nenhuma todos) contextos. Por exemplo, no início de um comando, digitar `ins` e pressionar TAB preencherá `insert into`. Em seguida, digitar alguns caracteres de um nome de tabela ou esquema e pressionar `TAB` preencherá o nome inacabado, ou oferecerá um menu de possíveis complementos quando houver mais de um. (Dependendo da biblioteca usada, você pode precisar pressionar `TAB` mais de uma vez para obter um menu.)

A conclusão de tabulação para nomes de objetos SQL requer o envio de consultas ao servidor para encontrar possíveis correspondências. Em alguns contextos, isso pode interferir em outras operações. Por exemplo, após `BEGIN`, será tarde demais para emitir `SET TRANSACTION ISOLATION LEVEL` se uma consulta de conclusão de tabulação for emitida entre elas. Se você não deseja conclusão de tabulação, pode desativá-la permanentemente colocando isso em um arquivo chamado `.inputrc` em seu diretório doméstico:

```
$if psql set disable-completion on $endif
```

(Isso não é uma funcionalidade do psql, mas do Readline. Leia a documentação para obter mais detalhes.)

A opção de linha de comando `-n` (`--no-readline`) também pode ser útil para desabilitar o uso de Readline para uma única execução do psql. Isso impede o preenchimento de tabulação, o uso ou registro do histórico de linha de comando e a edição de comandos de várias linhas. É particularmente útil quando você precisa copiar e colar texto que contém caracteres `TAB`.

## Meio Ambiente

`COLUMNS` [#](#APP-PSQL-ENVIRONMENT-COLUMNS) :   Se `\pset columns` for zero, controla a largura para o formato `wrapped` e a largura para determinar se a saída larga requer o pager ou deve ser alterada para o formato vertical no modo de auto expansão.

`PGDATABASE` `PGHOST` `PGPORT` `PGUSER` [#](#APP-PSQL-ENVIRONMENT-PGDATABASE): Parâmetros de conexão padrão (consulte [Seção 32.15](libpq-envars.md "32.15. Environment Variables")).

`PG_COLOR` [#](#APP-PSQL-ENVIRONMENT-PG-COLOR) : Especifica se a cor deve ser usada nas mensagens de diagnóstico. Os valores possíveis são `always`, `auto` e `never`.

`PSQL_EDITOR` `EDITOR` `VISUAL` [#](#APP-PSQL-ENVIRONMENT-PSQL-EDITOR): Editor utilizado pelos comandos `\e`, `\ef`, e `\ev`. Essas variáveis são examinadas na ordem listada; a primeira que é definida é usada. Se nenhuma delas for definida, o padrão é usar `vi` em sistemas Unix ou `notepad.exe` em sistemas Windows.

`PSQL_EDITOR_LINENUMBER_ARG` [#](#APP-PSQL-ENVIRONMENT-PSQL-EDITOR-LINENUMBER-ARG): Quando `\e`, `\ef`, ou `\ev` é usado com um argumento de número de linha, esta variável especifica o argumento de linha de comando usado para passar o número de linha inicial ao editor do usuário. Para editores como Emacs ou vi, este é um sinal de mais. Inclua um espaço final no valor da variável se precisar haver espaço entre o nome da opção e o número de linha. Exemplos:

```
PSQL_EDITOR_LINENUMBER_ARG='+' PSQL_EDITOR_LINENUMBER_ARG='--line '
```

O padrão é `+` em sistemas Unix (correspondente ao editor padrão `vi`, e útil para muitos outros editores comuns); mas não há padrão em sistemas Windows.

`PSQL_HISTORY` [#](#APP-PSQL-ENVIRONMENT-PSQL-HISTORY): Local alternativo para o arquivo de histórico de comandos. A expansão de tilde (`~`) é realizada.

`PSQL_PAGER` `PAGER` [#](#APP-PSQL-ENVIRONMENT-PAGER): Se os resultados de uma consulta não caberem na tela, eles são redirecionados através deste comando. Valores típicos são `more` ou `less`. O uso do pager pode ser desativado definindo `PSQL_PAGER` ou `PAGER` como uma string vazia, ou ajustando as opções relacionadas ao pager do comando `\pset`. Essas variáveis são examinadas na ordem listada; a primeira que é definida é usada. Se nenhuma delas for definida, o padrão é usar `more` na maioria das plataformas, mas `less` no Cygwin.

`PSQL_WATCH_PAGER` [#](#APP-PSQL-ENVIRONMENT-PSQL-WATCH-PAGER): Quando uma consulta é executada repetidamente com o comando `\watch`, um pager não é usado por padrão. Esse comportamento pode ser alterado definindo `PSQL_WATCH_PAGER` para um comando de pager, em sistemas Unix. O pager `pspg` (não faz parte do PostgreSQL, mas está disponível em muitas distribuições de software de código aberto) pode exibir a saída de `\watch` se iniciado com a opção `--stream`.

`PSQLRC` [#](#APP-PSQL-ENVIRONMENT-PSQLRC): Local alternativo do arquivo do usuário `.psqlrc`. A expansão de til (~) (`~`) é realizada.

`SHELL` [#](#APP-PSQL-ENVIRONMENT-SHELL): Comando executado pelo comando `\!`.

`TMPDIR` [#](#APP-PSQL-ENVIRONMENT-TMPDIR): Diretório para armazenar arquivos temporários. O padrão é `/tmp`.

Esse utilitário, como a maioria dos outros utilitários do PostgreSQL, também utiliza as variáveis de ambiente suportadas pelo libpq (consulte [Seção 32.15](libpq-envars.md)).

## Arquivos

`psqlrc` e `~/.psqlrc` [#](#APP-PSQL-FILES-PSQLRC): A menos que seja passada uma opção `-X`, psql tenta ler e executar comandos do arquivo de inicialização de nível de sistema (`psqlrc`) e, em seguida, o arquivo de inicialização pessoal do usuário (`~/.psqlrc`), após conectar-se ao banco de dados, mas antes de aceitar comandos normais. Esses arquivos podem ser usados para configurar o cliente e/ou o servidor conforme o gosto, tipicamente com os comandos `\set` e `SET`.

O arquivo de inicialização para todo o sistema é denominado `psqlrc`. Por padrão, ele é procurado no diretório de "configuração do sistema" da instalação, que é identificado de forma mais confiável ao executar `pg_config --sysconfdir`. Tipicamente, esse diretório será `../etc/` em relação ao diretório que contém os executaveis do PostgreSQL. O diretório a ser procurado pode ser definido explicitamente através da variável de ambiente `PGSYSCONFDIR`.

O arquivo de inicialização pessoal do usuário é denominado `.psqlrc` e é procurado no diretório de origem do usuário que está solicitando. No Windows, o arquivo de inicialização pessoal é denominado, em vez disso, `%APPDATA%\postgresql\psqlrc.conf`. Em qualquer caso, este caminho padrão do arquivo pode ser substituído definindo a variável de ambiente `PSQLRC`.

Tanto o arquivo de inicialização do sistema quanto o arquivo de inicialização pessoal do usuário podem ser específicos para a versão do psql adicionando um travessão e o identificador da versão principal ou secundária do PostgreSQL ao nome do arquivo, por exemplo, `~/.psqlrc-18` ou `~/.psqlrc-18.4`. O arquivo com a versão mais específica será lido preferencialmente em detrimento de um arquivo não específico para a versão. Esses sufixos de versão são adicionados após a determinação do caminho do arquivo como explicado acima.

O histórico de linha de comando é armazenado no arquivo `~/.psql_history`, ou `%APPDATA%\postgresql\psql_history` no Windows.

A localização do arquivo de histórico pode ser definida explicitamente através da variável `HISTFILE` psql ou da variável de ambiente `PSQL_HISTORY`.

## Notas

* O psql funciona melhor com servidores da mesma versão ou uma versão anterior. Os comandos de barra invertida são particularmente propensos a falhar se o servidor for uma versão mais recente do que o próprio psql. No entanto, os comandos de barra invertida da família `\d` devem funcionar com servidores das versões que remontam ao 9.2, embora não necessariamente com servidores mais recentes do que o próprio psql. A funcionalidade geral de executar comandos SQL e exibir resultados de consulta também deve funcionar com servidores de uma versão principal mais recente, mas isso não pode ser garantido em todos os casos.

Se você deseja usar o psql para se conectar a vários servidores de diferentes versões principais, é recomendável que você use a versão mais recente do psql. Alternativamente, você pode manter uma cópia do psql de cada versão principal e certifique-se de usar a versão que corresponde ao respectivo servidor. Mas, na prática, essa complicação adicional não deve ser necessária.
* Antes do PostgreSQL 9.6, a opção `-c` implicava em `-X` (`--no-psqlrc`)); esse não é mais o caso.
* Antes do PostgreSQL 8.4, o psql permitia que o primeiro argumento de um comando de barra invertida de uma única letra começasse diretamente após o comando, sem espaços em branco intermediários. Agora, alguns espaços em branco são necessários.

## Notas para usuários do Windows

O psql é construído como uma "aplicação de console". Como as janelas do console do Windows usam um codificação diferente do resto do sistema, você deve ter cuidado especial ao usar caracteres de 8 bits no psql. Se o psql detectar uma página de código de console problemática, ele o avisará na inicialização. Para alterar a página de código de console, são necessárias duas coisas:

* Defina a página de código digitando **`cmd.exe /c chcp 1252`**. (1252 é uma página de código apropriada para alemão; substitua com seu valor.) Se você estiver usando o Cygwin, pode colocar este comando em `/etc/profile`.
* Defina a fonte da consola em `Lucida Console`, porque a fonte raster não funciona com a página de código ANSI.

## Exemplos

O primeiro exemplo mostra como espalhar um comando em várias linhas de entrada. Observe o prompt em mudança:

```
testdb=> CREATE TABLE my_table ( testdb(>  first integer not null default 0, testdb(>  second text) testdb-> ; CREATE TABLE
```

Agora, olhe novamente para a definição da tabela:

```
testdb=> \d my_table Table "public.my_table" Column |  Type   | Collation | Nullable | Default --------+---------+-----------+----------+--------- first  | integer |           | not null | 0 second | text    |           |          |
```

Agora, vamos mudar o pedido para algo mais interessante:

```
testdb=> \set PROMPT1 '%n@%m %~%R%# ' peter@localhost testdb=>
```

Vamos supor que você preencheu a tabela com dados e quer dar uma olhada nela:

```
peter@localhost testdb=> SELECT * FROM my_table; first | second -------+-------- 1 | one 2 | two 3 | three 4 | four (4 rows)
```

Você pode exibir tabelas de diferentes maneiras usando o comando `\pset`:

```
peter@localhost testdb=> \pset border 2 Border style is 2. peter@localhost testdb=> SELECT * FROM my_table; +-------+--------+
| first | second |
+-------+--------+
|     1 | one    |
|     2 | two    |
|     3 | three  |
|     4 | four   |
+-------+--------+ (4 rows)

peter@localhost testdb=> \pset border 0 Border style is 0. peter@localhost testdb=> SELECT * FROM my_table; first second ----- ------ 1 one 2 two 3 three 4 four (4 rows)

peter@localhost testdb=> \pset border 1 Border style is 1. peter@localhost testdb=> \pset format csv Output format is csv. peter@localhost testdb=> \pset tuples_only Tuples only is on. peter@localhost testdb=> SELECT second, first FROM my_table; one,1 two,2 three,3 four,4 peter@localhost testdb=> \pset format unaligned Output format is unaligned. peter@localhost testdb=> \pset fieldsep '\t' Field separator is "    ". peter@localhost testdb=> SELECT second, first FROM my_table; one     1 two     2 three   3 four    4
```

Alternativamente, use os comandos curtos:

```
peter@localhost testdb=> \a \t \x Output format is aligned. Tuples only is off. Expanded display is on. peter@localhost testdb=> SELECT * FROM my_table; -[ RECORD 1 ]- first  | 1 second | one -[ RECORD 2 ]- first  | 2 second | two -[ RECORD 3 ]- first  | 3 second | three -[ RECORD 4 ]- first  | 4 second | four
```

Além disso, essas opções de formato de saída podem ser definidas para apenas uma consulta usando `\g`:

```
peter@localhost testdb=> SELECT * FROM my_table peter@localhost testdb-> \g (format=aligned tuples_only=off expanded=on) -[ RECORD 1 ]- first  | 1 second | one -[ RECORD 2 ]- first  | 2 second | two -[ RECORD 3 ]- first  | 3 second | three -[ RECORD 4 ]- first  | 4 second | four
```

Aqui está um exemplo de uso do comando `\df` para encontrar apenas funções com nomes que correspondem a `int*pl` e cujo segundo argumento é do tipo `bigint`:

```
testdb=> \df int*pl * bigint List of functions Schema   |  Name   | Result data type | Argument data types | Type ------------+---------+------------------+---------------------+------ pg_catalog | int28pl | bigint           | smallint, bigint    | func pg_catalog | int48pl | bigint           | integer, bigint     | func pg_catalog | int8pl  | bigint           | bigint, bigint      | func (3 rows)
```

Aqui, a opção `+` é usada para exibir informações adicionais sobre uma dessas funções, e `x` é usada para exibir os resultados em modo expandido:

```
testdb=> \df+x int*pl integer bigint List of functions -[ RECORD 1 ]-------+----------------------------- Schema              | pg_catalog Name                | int48pl Result data type    | bigint Argument data types | integer, bigint Type                | func Volatility          | immutable Parallel            | safe Owner               | postgres Security            | invoker Leakproof?          | no Access privileges   | Language            | internal Internal name       | int48pl Description         | implementation of + operator
```

Quando apropriado, os resultados da consulta podem ser exibidos em uma representação cruzada com o comando `\crosstabview`:

```
testdb=> SELECT first, second, first > 2 AS gt2 FROM my_table; first | second | gt2 -------+--------+----- 1 | one    | f 2 | two    | f 3 | three  | t 4 | four   | t (4 rows)

testdb=> \crosstabview first second first | one | two | three | four -------+-----+-----+-------+------ 1 | f   |     |       | 2 |     | f   |       | 3 |     |     | t     | 4 |     |     |       | t (4 rows)
```

Este segundo exemplo mostra uma tabela de multiplicação com linhas ordenadas em ordem numérica inversa e colunas com uma ordem numérica independente e ascendente.

```
testdb=> SELECT t1.first as "A", t2.first+100 AS "B", t1.first*(t2.first+100) as "AxB", testdb-> row_number() over(order by t2.first) AS ord testdb-> FROM my_table t1 CROSS JOIN my_table t2 ORDER BY 1 DESC testdb-> \crosstabview "A" "B" "AxB" ord A | 101 | 102 | 103 | 104 ---+-----+-----+-----+----- 4 | 404 | 408 | 412 | 416 3 | 303 | 306 | 309 | 312 2 | 202 | 204 | 206 | 208 1 | 101 | 102 | 103 | 104 (4 rows)
```
