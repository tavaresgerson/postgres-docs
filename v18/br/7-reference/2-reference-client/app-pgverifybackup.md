## pg_verifybackup

pg_verifybackup — verificar a integridade de um backup de base de um clúster PostgreSQL

## Sinopse

`pg_verifybackup` [*`option`*...]

## Descrição

O pg_verifybackup é usado para verificar a integridade de um backup de um clúster de banco de dados feito usando `pg_basebackup` contra um `backup_manifest` gerado pelo servidor no momento do backup. O backup pode ser armazenado no formato "simples" ou "tar"; isso inclui backups no formato tar comprimidos com qualquer algoritmo suportado pelo pg_basebackup. No entanto, atualmente, a verificação do `WAL` é suportada apenas para backups no formato simples. Portanto, se o backup for armazenado no formato tar, a opção `-n, --no-parse-wal` deve ser usada.

É importante notar que a validação que é realizada pelo pg_verifybackup não inclui e não pode incluir todas as verificações que serão realizadas por um servidor em execução ao tentar fazer uso do backup. Mesmo que você use essa ferramenta, ainda deve realizar restaurações de teste e verificar se os bancos de dados resultantes funcionam conforme o esperado e se parecem conter os dados corretos. No entanto, o pg_verifybackup pode detectar muitos problemas que ocorrem comumente devido a problemas de armazenamento ou erro do usuário.

A verificação de backup prossegue em quatro etapas. Primeiro, o `pg_verifybackup` lê o arquivo `backup_manifest`. Se esse arquivo não existir, não puder ser lido, estiver mal formado, não corresponder ao identificador do sistema com o `pg_control` do diretório de backup ou não passar pela verificação contra seu próprio checksum interno, o `pg_verifybackup` terminará com um erro fatal.

Em segundo lugar, o `pg_verifybackup` tentará verificar se os arquivos de dados atualmente armazenados no disco são exatamente os mesmos que os arquivos de dados que o servidor pretendia enviar, com algumas exceções que são descritas abaixo. Arquivos extras e ausentes serão detectados, com algumas exceções. Esta etapa ignorará a presença ou ausência de, ou qualquer modificação em, `postgresql.auto.conf`, `standby.signal` e `recovery.signal`, porque espera-se que esses arquivos tenham sido criados ou modificados como parte do processo de realização do backup. Além disso, não se queixará de um arquivo `backup_manifest` no diretório de destino ou de qualquer coisa dentro de `pg_wal`, embora esses arquivos não sejam listados no manifesto do backup. Apenas os arquivos são verificados; a presença ou ausência de diretórios não é verificada, exceto indiretamente: se um diretório estiver ausente, quaisquer arquivos que ele deveria ter contido serão necessariamente ausentes.

Em seguida, `pg_verifybackup` verificará todos os arquivos, comparará os checksums com os valores do manifesto e emitirá erros para quaisquer arquivos para os quais o checksum calculado não corresponder ao checksum armazenado no manifesto. Esse passo não é realizado para quaisquer arquivos que tenham produzido erros na etapa anterior, uma vez que já se sabe que eles têm problemas. Os arquivos que foram ignorados na etapa anterior também são ignorados nesta etapa.

Finalmente, o `pg_verifybackup` usará o manifesto para verificar se os registros do log de pré-escrita que serão necessários para recuperar o backup estão presentes e se podem ser lidos e analisados. O `backup_manifest` contém informações sobre quais registros do log de pré-escrita serão necessários, e o `pg_verifybackup` usará essas informações para invocar o `pg_waldump` para analisar esses registros do log de pré-escrita. A bandeira `--quiet` será usada, de modo que o `pg_waldump` apenas relatará erros, sem produzir qualquer outra saída. Embora esse nível de verificação seja suficiente para detectar problemas óbvios, como um arquivo ausente ou um cujo checksum interno não corresponda, eles não são extensos o suficiente para detectar todos os problemas possíveis que podem ocorrer ao tentar recuperar. Por exemplo, um bug no servidor que produz registros do log de pré-escrita que têm os checksums corretos, mas especificam ações sem sentido, não pode ser detectado por esse método.

Observe que, se houver arquivos WAL adicionais que não são necessários para recuperar o backup, eles não serão verificados por essa ferramenta, embora uma invocação separada de `pg_waldump` possa ser usada para esse propósito. Além disso, observe que as verificações de integridade do arquivo WAL são específicas da versão: você deve usar a versão de `pg_verifybackup`, e, portanto, de `pg_waldump`, que se refere ao backup que está sendo verificado. Em contraste, as verificações de integridade do arquivo de dados devem funcionar com qualquer versão do servidor que gere um arquivo `backup_manifest`.

## Opções

pg_verifybackup aceita os seguintes argumentos de linha de comando:

`-e` `--exit-on-error`: Saia imediatamente assim que um problema com o backup for detectado. Se esta opção não for especificada, `pg_verifybackup` continuará a verificar o backup mesmo após o problema ter sido detectado, e reportará todos os problemas detectados como erros.

`-F format` `--format=format`: Especifica o formato do backup. *`format`* pode ser um dos seguintes:

`p` `plain` :   O backup consiste em arquivos simples com o mesmo layout do diretório de dados do servidor de origem e dos espaços de tabela.

`t` `tar` :   O backup consiste em arquivos tar, que podem ser comprimidos. Um backup válido inclui o diretório de dados principal em um arquivo denominado `base.tar`, os arquivos WAL em `pg_wal.tar`, e arquivos tar separados para cada espaço de tabela, nomeados de acordo com o OID do espaço de tabela. Se o backup for comprimido, a extensão de compressão relevante é adicionada ao final de cada nome de arquivo.

`-i path` `--ignore=path`: Ignore o arquivo ou diretório especificado, que deve ser expresso como um nome de caminho relativo, ao comparar a lista de arquivos de dados realmente presentes no backup com os listados no arquivo `backup_manifest`. Se um diretório for especificado, esta opção afeta toda a subárvore enraizada naquela localização. Queixas sobre arquivos extras, arquivos ausentes, diferenças de tamanho de arquivo ou desalinhamentos de verificação de checksum serão suprimidos se o nome do caminho relativo corresponder ao nome do caminho especificado. Esta opção pode ser especificada várias vezes.

`-m path` `--manifest-path=path`: Use o arquivo de manifesto no caminho especificado, em vez de um localizado na raiz do diretório de backup.

`-n` `--no-parse-wal`: Não tente analisar os dados de log de pré-escrita que serão necessários para recuperar a partir deste backup.

`-P` `--progress`: Habilitar o relatório de progresso. Ao ativar isso, será entregue um relatório de progresso enquanto verifica os checksums.

Esta opção não pode ser usada em conjunto com a opção `--quiet`.

`-q` `--quiet`: Não imprima nada quando um backup for verificado com sucesso.

`-s` `--skip-checksums`: Não verifique os checksums do arquivo de dados. A presença ou ausência de arquivos e os tamanhos desses arquivos ainda serão verificados. Isso é muito mais rápido, porque os próprios arquivos não precisam ser lidos.

`-w path` `--wal-directory=path`: Tente analisar os arquivos WAL armazenados no diretório especificado, em vez de em `pg_wal`. Isso pode ser útil se o backup estiver armazenado em um local separado do arquivo WAL.

Outras opções também estão disponíveis:

`-V` `--version`: Imprimir a versão do pg_verifybackup e sair.

`-?` `--help`: Mostrar ajuda sobre os argumentos da linha de comando do comando pg_verifybackup e sair.

## Exemplos

Para criar uma cópia de segurança básica do servidor em `mydbserver` e verificar a integridade da cópia de segurança:

```
$ pg_basebackup -h mydbserver -D /usr/local/pgsql/data
$ pg_verifybackup /usr/local/pgsql/data
```

Para criar um backup básico do servidor em `mydbserver`, mova o manifesto para algum lugar fora do diretório de backup e verifique o backup:

```
$ pg_basebackup -h mydbserver -D /usr/local/pgsql/backup1234
$ mv /usr/local/pgsql/backup1234/backup_manifest /my/secure/location/backup_manifest.1234
$ pg_verifybackup -m /my/secure/location/backup_manifest.1234 /usr/local/pgsql/backup1234
```

Para verificar um backup, ignorando um arquivo que foi adicionado manualmente ao diretório de backup, e também ignorando a verificação de checksum:

```
$ pg_basebackup -h mydbserver -D /usr/local/pgsql/data
$ edit /usr/local/pgsql/data/note.to.self
$ pg_verifybackup --ignore=note.to.self --skip-checksums /usr/local/pgsql/data
```

## Veja também

[pg_basebackup](app-pgbasebackup.md "pg_basebackup")
