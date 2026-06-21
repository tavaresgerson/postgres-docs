## 19.13. Versão e compatibilidade com a plataforma [#](#RUNTIME-CONFIG-COMPATIBLE)

* [19.13.1. Versões anteriores do PostgreSQL](runtime-config-compatible.md#RUNTIME-CONFIG-COMPATIBLE-VERSION)
* [19.13.2. Compatibilidade da plataforma e do cliente](runtime-config-compatible.md#RUNTIME-CONFIG-COMPATIBLE-CLIENTS)

### 19.13.1. Versões anteriores do PostgreSQL [#](#RUNTIME-CONFIG-COMPATIBLE-VERSION)

`array_nulls` (`boolean`) [#](#GUC-ARRAY-NULLS): Isso controla se o analisador de entrada de matriz reconhece `NULL` não citado como especificando um elemento de matriz nulo. Por padrão, isso é `on`, permitindo que os valores da matriz contenham valores nulos. No entanto, as versões do PostgreSQL anteriores à versão 8.2 não suportam valores nulos em matrizes, e, portanto, tratariam `NULL` como especificando um elemento de matriz normal com o valor de string “NULL”. Para compatibilidade reversa com aplicativos que exigem o comportamento antigo, essa variável pode ser configurada como `off`.

Observe que é possível criar valores de matriz que contenham valores nulos, mesmo quando essa variável é `off`.

`backslash_quote` (`enum`) [#](#GUC-BACKSLASH-QUOTE): Isso controla se uma aspas pode ser representada por `\'` em uma literal de string. A maneira preferida, conforme padrão SQL, de representar uma aspas é duplicá-la (`''`) mas o PostgreSQL historicamente também aceitou `\'`. No entanto, o uso de `\'` cria riscos de segurança porque, em alguns conjuntos de caracteres do cliente, há caracteres multibyte em que o último byte é numericamente equivalente ao ASCII `\`. Se o código do lado do cliente faz escapamento incorretamente, então é possível um ataque de injetão SQL. Esse risco pode ser prevenido fazendo com que o servidor rejeite consultas nas quais uma aspas parece ser escapada por uma barra invertida. Os valores permitidos de `backslash_quote` são `on` (permitir `\'` sempre), `off` (rejeitar sempre) e `safe_encoding` (permitir apenas se o codificação do cliente não permite ASCII `\` dentro de um caractere multibyte). `safe_encoding` é o ajuste padrão.

Observe que, em uma literal de string conforme padrão, `\` significa simplesmente `\`. Esse parâmetro afeta apenas o tratamento de literais não conforme padrão, incluindo a sintaxe de string de escape (`E'...'`).

`escape_string_warning` (`boolean`) [#](#GUC-ESCAPE-STRING-WARNING): Quando ativado, é emitido um aviso se uma barra invertida (`\`) aparecer em uma literal de string comum (sintaxe `'...'`), e `standard_conforming_strings` estiver desativado. O padrão é `on`.

Os aplicativos que desejam usar barras invertidas como escape devem ser modificados para usar a sintaxe de string de escape (`E'...'`), porque o comportamento padrão das strings comuns agora é tratar a barra invertida como um caractere comum, de acordo com o padrão SQL. Essa variável pode ser habilitada para ajudar a localizar o código que precisa ser alterado.

`lo_compat_privileges` (`boolean`) [#](#GUC-LO-COMPAT-PRIVILEGES): Em versões do PostgreSQL anteriores à 9.0, os objetos grandes não tinham privilégios de acesso e, portanto, sempre podiam ser lidos e escritos por todos os usuários. Definir essa variável para `on` desativa as novas verificações de privilégios, para compatibilidade com versões anteriores. O padrão é `off`. Somente superusuários e usuários com o privilégio apropriado `SET` podem alterar essa configuração.

Definir essa variável não desativa todas as verificações de segurança relacionadas a objetos grandes — apenas aquelas para as quais o comportamento padrão foi alterado no PostgreSQL 9.0.

`quote_all_identifiers` (`boolean`) [#](#GUC-QUOTE-ALL-IDENTIFIERS): Quando o banco de dados gerar SQL, force todos os identificadores a serem citados, mesmo que não sejam (atualmente) palavras-chave. Isso afetará a saída de `EXPLAIN` bem como os resultados de funções como `pg_get_viewdef`. Veja também a opção `--quote-all-identifiers` de [pg_dump](app-pgdump.md "pg_dump") e [pg_dumpall](app-pg-dumpall.md "pg_dumpall").

`standard_conforming_strings` (`boolean`) [#](#GUC-STANDARD-CONFORMING-STRINGS): Isso controla se as literais de string comuns (`'...'`) tratam as barras invertidas literalmente, conforme especificado no padrão SQL. A partir do PostgreSQL 9.1, o padrão é `on` (as versões anteriores tinham como padrão `off`). As aplicações podem verificar esse parâmetro para determinar como as literais de string serão processadas. A presença desse parâmetro também pode ser interpretada como uma indicação de que a sintaxe de string de escape ([Seção 4.1.2.2](sql-syntax-lexical.md#SQL-SYNTAX-STRINGS-ESCAPE "4.1.2.2. String Constants with C-Style Escapes")) é suportada. A sintaxe de string de escape ([Seção 4.1.2.2](sql-syntax-lexical.md#SQL-SYNTAX-STRINGS-ESCAPE "4.1.2.2. String Constants with C-Style Escapes")) deve ser usada se uma aplicação desejar que as barras invertidas sejam tratadas como caracteres de escape.

`synchronize_seqscans` (`boolean`) [#](#GUC-SYNCHRONIZE-SEQSCANS): Isso permite que varreduras sequenciais de grandes tabelas sejam sincronizadas entre si, de modo que varreduras concorrentes leem o mesmo bloco aproximadamente no mesmo momento e, portanto, compartilham a carga de trabalho de I/O. Quando isso é habilitado, uma varredura pode começar no meio da tabela e, em seguida, "dar a volta" ao final para cobrir todas as linhas, de modo a sincronizar com a atividade das varreduras já em progresso. Isso pode resultar em mudanças imprevisíveis na ordem das linhas devolvidas por consultas que não têm a cláusula `ORDER BY`. Definir este parâmetro para `off` garante o comportamento pré-8.3, no qual uma varredura sequencial sempre começa pelo início da tabela. O padrão é `on`.

### 19.13.2. Compatibilidade da Plataforma e do Cliente [#](#RUNTIME-CONFIG-COMPATIBLE-CLIENTS)

`transform_null_equals` (`boolean`) [#](#GUC-TRANSFORM-NULL-EQUALS): Quando ativado, as expressões na forma de `expr = NULL` (ou `NULL = expr`) são tratadas como `expr IS NULL`, ou seja, elas retornam verdadeiro se *`expr`* avaliar ao valor nulo, e falso de outra forma. O comportamento correto conforme a especificação SQL de `expr = NULL` é sempre retornar nulo (desconhecido). Portanto, este parâmetro tem como padrão `off`.

No entanto, os formulários filtrados no Microsoft Access geram consultas que parecem usar `expr = NULL` para testar valores nulos, portanto, se você usar essa interface para acessar o banco de dados, talvez queira ativar essa opção. Como as expressões do formulário `expr = NULL` sempre retornam o valor nulo (usando a interpretação padrão do SQL), elas não são muito úteis e não aparecem com frequência em aplicações normais, então essa opção não causa muito dano na prática. Mas novos usuários são frequentemente confusos sobre a semântica das expressões que envolvem valores nulos, então essa opção está desativada por padrão.

Observe que essa opção afeta apenas o formato exato `= NULL`, não outros operadores de comparação ou outras expressões que são computacionalmente equivalentes a alguma expressão que envolva o operador de igualdade (como `IN`). Assim, essa opção não é uma correção geral para programação ruim.

Consulte a seção [9.2][(functions-comparison.md "9.2. Comparison Functions and Operators")] para informações relacionadas.

`allow_alter_system` (`boolean`) [#](#GUC-ALLOW-ALTER-SYSTEM): Quando `allow_alter_system` está definido como `off`, um erro é retornado se o comando `ALTER SYSTEM` for executado. Este parâmetro só pode ser definido no arquivo `postgresql.conf` ou na linha de comando do servidor. O valor padrão é `on`.

Observe que essa configuração não deve ser considerada uma característica de segurança. Ela apenas desabilita o comando `ALTER SYSTEM`. Não impede que um superusuário mude a configuração usando outros comandos SQL. Um superusuário tem muitas maneiras de executar comandos de shell no nível do sistema operacional e, portanto, pode modificar `postgresql.auto.conf` independentemente do valor dessa configuração.

Desativar essa configuração é destinado a ambientes onde a configuração do PostgreSQL é gerenciada por alguma ferramenta externa. Nesses ambientes, um superusuário bem-intencionado pode *por engano* usar `ALTER SYSTEM` para alterar a configuração em vez de usar a ferramenta externa. Isso pode resultar em comportamento não intencional, como a ferramenta externa sobrescrevendo a mudança em algum momento posterior, quando ela atualiza a configuração. Definir esse parâmetro para `off` pode ajudar a evitar tais erros.

Este parâmetro controla apenas o uso de `ALTER SYSTEM`. As configurações armazenadas em `postgresql.auto.conf` entram em vigor mesmo que `allow_alter_system` esteja definido como `off`.