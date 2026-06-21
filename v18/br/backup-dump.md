## 25.1. Dump de SQL [#](#BACKUP-DUMP)

* [25.1.1. Restauração do Dump](backup-dump.md#BACKUP-DUMP-RESTORE)
* [25.1.2. Uso de pg_dumpall](backup-dump.md#BACKUP-DUMP-ALL)
* [25.1.3. Tratamento de bancos de dados grandes](backup-dump.md#BACKUP-DUMP-LARGE)

A ideia por trás desse método de descarte é gerar um arquivo com comandos SQL que, quando devolvidos ao servidor, irão recriar o banco de dados no mesmo estado em que estava na época do descarte. O PostgreSQL fornece o programa de utilidade [pg_dump][(app-pgdump.md "pg_dump")] para esse propósito. O uso básico desse comando é:

```
pg_dump dbname > dumpfile
```

Como você pode ver, o pg_dump escreve seu resultado na saída padrão. Veremos abaixo como isso pode ser útil. Embora o comando acima crie um arquivo de texto, o pg_dump pode criar arquivos em outros formatos que permitem paralelismo e controle mais detalhado da restauração de objetos.

pg_dump é uma aplicação cliente regular do PostgreSQL (embora uma particularmente inteligente). Isso significa que você pode realizar esse procedimento de backup a partir de qualquer host remoto que tenha acesso ao banco de dados. Mas lembre-se de que o pg_dump não opera com permissões especiais. Em particular, ele deve ter acesso de leitura a todas as tabelas que você deseja fazer backup, então, para fazer backup de todo o banco de dados, quase sempre você deve executá-lo como um superusuário do banco de dados. (Se você não tem privilégios suficientes para fazer backup de todo o banco de dados, ainda pode fazer backup de partes do banco de dados para as quais você tem acesso usando opções como `-n schema` ou `-t table`).

Para especificar qual servidor de banco de dados o pg_dump deve contatar, use as opções de linha de comando `-h host` e `-p port`. O host padrão é o host local ou o que a sua variável de ambiente `PGHOST` especifica. Da mesma forma, a porta padrão é indicada pela variável de ambiente `PGPORT` ou, caso contrário, pelo padrão incorporado. (Convenientemente, o servidor normalmente terá o mesmo padrão incorporado.)

Como qualquer outra aplicação cliente do PostgreSQL, o pg_dump, por padrão, se conecta com o nome do usuário do banco de dados que é igual ao nome do usuário do sistema operacional atual. Para ignorar isso, especifique a opção `-U` ou defina a variável de ambiente `PGUSER`. Lembre-se de que as conexões do pg_dump estão sujeitas aos mecanismos normais de autenticação do cliente (que são descritos em [Capítulo 20][(client-authentication.md "Chapter 20. Client Authentication")]).

Uma vantagem importante do pg_dump em relação aos outros métodos de backup descritos mais adiante é que a saída do pg_dump geralmente pode ser recarregada em versões mais recentes do PostgreSQL, enquanto os backups de nível de arquivo e o arquivamento contínuo são ambos extremamente específicos para a versão do servidor. O pg_dump também é o único método que funcionará ao transferir um banco de dados para uma arquitetura de máquina diferente, como de um servidor de 32 bits para um de 64 bits.

Os descargas criados pelo pg_dump são consistentes internamente, o que significa que o descarte representa um instantâneo do banco de dados no momento em que o pg_dump começou a ser executado. O pg_dump não bloqueia outras operações no banco de dados enquanto está em funcionamento. (As exceções são aquelas operações que precisam operar com um bloqueio exclusivo, como a maioria das formas de `ALTER TABLE`.)

### 25.1.1. Restauração do Dump [#](#BACKUP-DUMP-RESTORE)

Os arquivos de texto criados pelo pg_dump são destinados a serem lidos pelo programa psql usando suas configurações padrão. A forma geral do comando para restaurar um dump de texto é

```
psql -X dbname < dumpfile
```

onde *`dumpfile`* é o arquivo gerado pelo comando pg_dump. O banco de dados *`dbname`* não será criado por este comando, então você deve criá-lo manualmente a partir de `template0` antes de executar o psql (por exemplo, com `createdb -T template0 dbname`). Para garantir que o psql execute com suas configurações padrão, use a opção `-X` (`--no-psqlrc`). O psql suporta opções semelhantes às do pg_dump para especificar o servidor de banco de dados a ser conectado e o nome de usuário a ser usado. Consulte a página de referência [psql][(app-psql.md "psql")] para obter mais informações.

Os arquivos de dump não de texto devem ser restaurados usando o utilitário [pg_restore][(app-pgrestore.md "pg_restore")].

Antes de restaurar um dump SQL, todos os usuários que possuem objetos ou que receberam permissões em objetos no banco de dados descartado devem já existir. Se não existirem, o restauro não conseguirá recriar os objetos com a propriedade e/ou permissões originais. (Às vezes, isso é o que você quer, mas geralmente não é.)

Por padrão, o script psql continuará a ser executado após ocorrências de erros SQL. Você pode querer executar o psql com a variável `ON_ERROR_STOP` definida para alterar esse comportamento e fazer com que o psql saia com um status de saída de 3 se um erro SQL ocorrer:

```
psql -X --set ON_ERROR_STOP=on dbname < dumpfile
```

De qualquer forma, você terá apenas um banco de dados parcialmente restaurado. Alternativamente, você pode especificar que todo o dump deve ser restaurado como uma única transação, para que o restabelecimento seja totalmente concluído ou totalmente revertido. Esse modo pode ser especificado passando as opções de linha de comando `-1` ou `--single-transaction` para o psql. Ao usar esse modo, esteja ciente de que até mesmo um erro menor pode reverter um restabelecimento que já foi executado por muitas horas. No entanto, isso ainda pode ser preferível a limpar manualmente um banco de dados complexo após um dump parcialmente restaurado.

A capacidade do pg_dump e do psql de gravar ou ler de tubos permite que você descarregue um banco de dados diretamente de um servidor para outro, por exemplo:

```
pg_dump -h host1 dbname | psql -X -h host2 dbname
```

### Importante

Os dados de dump produzidos pelo pg_dump são relativos a `template0`. Isso significa que quaisquer idiomas, procedimentos, etc., adicionados via `template1` também serão dumpados pelo pg_dump. Como resultado, ao restaurar, se você estiver usando um `template1` personalizado, você deve criar o banco de dados vazio a partir de `template0`, como no exemplo acima.

Após restaurar um backup, é prudente executar `ANALYZE`(sql-analyze.md "ANALYZE") em cada banco de dados para que o otimizador de consulta tenha estatísticas úteis; consulte [Seção 24.1.3][(routine-vacuuming.md#VACUUM-FOR-STATISTICS "24.1.3. Updating Planner Statistics")] e [Seção 24.1.6][(routine-vacuuming.md#AUTOVACUUM "24.1.6. The Autovacuum Daemon")] para mais informações. Para mais conselhos sobre como carregar grandes quantidades de dados no PostgreSQL de forma eficiente, consulte [Seção 14.4][(populate.md "14.4. Populating a Database")].

### 25.1.2. Usando pg_dumpall [#](#BACKUP-DUMP-ALL)

O pg_dump exclui apenas um único banco de dados de cada vez e não exibe informações sobre papéis ou espaços de tabela (porque essas são globais para o clúster e não por banco de dados). Para suportar o descarte conveniente de todo o conteúdo de um clúster de bancos, o programa [pg_dumpall][(app-pg-dumpall.md "pg_dumpall")] é fornecido. O pg_dumpall faz backup de cada banco de dados em um clúster dado e também preserva dados globais para o clúster, como definições de papéis e espaços de tabela. O uso básico deste comando é:

```
pg_dumpall > dumpfile
```

O dump resultante pode ser restaurado com o psql:

```
psql -X -f dumpfile postgres
```

(Na verdade, você pode especificar qualquer nome de banco de dados existente para começar, mas se você estiver carregando em um cluster vazio, então `postgres` geralmente deve ser usado). É sempre necessário ter acesso ao superusuário do banco de dados ao restaurar um dump pg_dumpall, pois isso é necessário para restaurar as informações de role e tablespace. Se você usar tablespaces, certifique-se de que os caminhos do tablespace no dump sejam apropriados para a nova instalação.

O pg_dumpall funciona emitindo comandos para recriar papéis, espaços de tabela e bancos vazios, e, em seguida, invocando o pg_dump para cada banco de dados. Isso significa que, embora cada banco de dados seja consistente internamente, os instantâneos de diferentes bancos de dados não são sincronizados.

Os dados de todo o clúster podem ser descarregados individualmente usando a opção pg_dumpall `--globals-only`. Isso é necessário para fazer um backup completo do clúster se o comando pg_dump for executado em bancos de dados individuais.

### 25.1.3. Gerenciamento de grandes bancos de dados [#](#BACKUP-DUMP-LARGE)

Alguns sistemas operacionais têm limites de tamanho máximo de arquivo que causam problemas ao criar arquivos de saída do pg_dump grandes. Felizmente, o pg_dump pode escrever na saída padrão, então você pode usar ferramentas padrão do Unix para contornar esse problema potencial. Existem vários métodos possíveis:

**Use arquivos compactados.** Você pode usar seu programa de compactação favorito, por exemplo, gzip:

```
pg_dump dbname | gzip > filename.gz
```

Recarregue com:

```
gunzip -c filename.gz | psql dbname
```

ou:

```
cat filename.gz | gunzip | psql dbname
```

**Use `split`.** O comando `split` permite que você divida a saída em arquivos menores que são aceitáveis em tamanho para o sistema de arquivos subjacente. Por exemplo, para fazer porções de 2 gigabytes:

```
pg_dump dbname | split -b 2G - filename
```

Recarregue com:

```
cat filename* | psql dbname
```

Se estiver usando o GNU split, é possível usá-lo junto com o gzip:

```
pg_dump dbname | split -b 2G --filter='gzip > $FILE.gz'
```

Pode ser restaurada usando `zcat`.

**Use o formato de dump personalizado do pg_dump.** Se o PostgreSQL foi construído em um sistema com a biblioteca de compressão zlib instalada, o formato de dump personalizado comprimirá os dados conforme os escreve no arquivo de saída. Isso produzirá tamanhos de arquivo de dump semelhantes ao uso do `gzip`, mas tem a vantagem adicional de que as tabelas podem ser restauradas seletivamente. O comando a seguir faz um dump de um banco de dados usando o formato de dump personalizado:

```
pg_dump -Fc dbname > filename
```

Um dump em formato personalizado não é um script para psql, mas, em vez disso, deve ser restaurado com pg_restore, por exemplo:

```
pg_restore -d dbname filename
```

Consulte as páginas de referência [pg_dump][(app-pgdump.md "pg_dump")] e [pg_restore][(app-pgrestore.md "pg_restore")] para obter detalhes.

Para bancos de dados muito grandes, você pode precisar combinar `split` com uma das outras duas abordagens.

**Use a função de dump paralelo do pg_dump.** Para acelerar o dump de um banco de dados grande, você pode usar o modo paralelo do pg_dump. Isso fará o dump de várias tabelas ao mesmo tempo. Você pode controlar o grau de paralelismo com o parâmetro `-j`. Os dumps paralelos são suportados apenas para o formato de arquivo "directory".

```
pg_dump -j num -F d -f out.dir dbname
```

Você pode usar `pg_restore -j` para restaurar um dump em paralelo. Isso funcionará para qualquer arquivo do modo de arquivo "custom" ou "directory", independentemente de ter sido criado com `pg_dump -j` ou