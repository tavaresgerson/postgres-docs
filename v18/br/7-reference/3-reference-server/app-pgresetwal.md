## pg_resetwal

pg_resetwal — redefinir o log de antecipação de escrita e outras informações de controle de um clúster de banco de dados PostgreSQL

## Sinopse

`pg_resetwal` [ `-f` | `--force` ] [ `-n` | `--dry-run` ] [*`option`*...] [ `-D` | `--pgdata` ]*`datadir`*

## Descrição

`pg_resetwal` limpa o log de pré-escrita (WAL) e, opcionalmente, refaz algumas outras informações de controle armazenadas no arquivo `pg_control`. Essa função é, às vezes, necessária se esses arquivos se tornaram corrompidos. Deve ser usada apenas como último recurso, quando o servidor não iniciar devido a essa corrupção.

Algumas opções, como `--wal-segsize` (veja abaixo), também podem ser usadas para modificar certas configurações globais de um clúster de banco de dados sem a necessidade de executar novamente `initdb`. Isso pode ser feito com segurança em um clúster de banco de dados que funciona corretamente, desde que nenhuma das modalidades perigosas mencionadas abaixo seja usada.

Se `pg_resetwal` for usado em um diretório de dados onde o servidor foi desligado corretamente e o arquivo de controle está em ordem, ele não terá efeito sobre o conteúdo do sistema de banco de dados, exceto que os arquivos WAL que não são mais usados são apagados. Qualquer outro uso é potencialmente perigoso e deve ser feito com grande cuidado. `pg_resetwal` exigirá que a opção `-f` (força) seja especificada antes de trabalhar em um diretório de dados em um estado de desligamento não limpo ou com um arquivo de controle corrompido.

Após executar este comando em um diretório de dados com WAL corrompido ou um arquivo de controle corrompido, deve ser possível iniciar o servidor, mas tenha em mente que o banco de dados pode conter dados inconsistentes devido a transações parcialmente comprometidas. Você deve imediatamente drenar seus dados, executar `initdb` e restaurar. Após a restauração, verifique as inconsistências e faça a reparação conforme necessário.

Se o `pg_resetwal` reclamar que não consegue determinar dados válidos para o `pg_control`, você pode forçá-lo a prosseguir de qualquer maneira, especificando a opção `-f` (forçar). Neste caso, valores plausíveis serão substituídos pelos dados ausentes. Espera-se que a maioria dos campos corresponda, mas pode ser necessária assistência manual para os campos do próximo OID, próximo ID de transação e época, próximo ID de multitransação e deslocamento e localização inicial do WAL. Esses campos podem ser definidos usando as opções discutidas abaixo. Se você não conseguir determinar valores corretos para todos esses campos, o `-f` ainda pode ser usado, mas o banco de dados recuperado deve ser tratado com ainda mais suspeita do que o usual: um descarte e restabelecimento imediatos são imperativos. *Não* execute operações que modifiquem dados no banco de dados antes de fazer o descarte, pois qualquer ação desse tipo provavelmente piorará a corrupção.

Esse utilitário só pode ser executado pelo usuário que instalou o servidor, porque ele requer acesso de leitura/escrita ao diretório de dados.

## Opções

*`datadir`* `-D datadir` `--pgdata=datadir`: Especifica a localização do diretório do banco de dados. Por razões de segurança, você deve especificar o diretório de dados na linha de comando. `pg_resetwal` não utiliza a variável de ambiente `PGDATA`.

`-f` `--force`: Forçar o `pg_resetwal` a prosseguir mesmo em situações em que isso poderia ser perigoso, conforme explicado acima. Especificamente, esta opção é necessária para prosseguir se o servidor não tiver sido desligado corretamente ou se o `pg_resetwal` não puder determinar dados válidos para o `pg_control`.

`-n` `--dry-run`: A opção `-n`/`--dry-run` instrui o `pg_resetwal` a imprimir os valores reconstruídos a partir de `pg_control` e os valores que estão prestes a ser alterados, e então sair sem modificar nada. Esta é principalmente uma ferramenta de depuração, mas pode ser útil como uma verificação de integridade antes de permitir que o `pg_resetwal` prossiga para o real.

`-V` `--version`: Exibir informações da versão, e então sair.

`-?` `--help`: Mostrar ajuda e, em seguida, sair.

As seguintes opções são necessárias apenas quando o `pg_resetwal` não consegue determinar valores apropriados ao ler o `pg_control`. Valores seguros podem ser determinados conforme descrito abaixo. Para valores que aceitam argumentos numéricos, os valores hexadecimais podem ser especificados usando o prefixo `0x`. Note que essas instruções se aplicam apenas com o tamanho padrão do bloco de 8 kB.

`-c xid,xid` `--commit-timestamp-ids=xid,xid`: Configure manualmente os IDs de transação mais antigos e mais novos para os quais o tempo de commit pode ser recuperado.

Um valor seguro para o ID da transação mais antigo para o qual o tempo de commit pode ser recuperado (primeira parte) pode ser determinado procurando pelo nome de arquivo numerologicamente menor no diretório `pg_commit_ts` sob o diretório de dados. Por outro lado, um valor seguro para o ID da transação mais recente para o qual o tempo de commit pode ser recuperado (segunda parte) pode ser determinado procurando pelo nome de arquivo numerologicamente maior no mesmo diretório. Os nomes dos arquivos estão em hexadecimal.

`-e xid_epoch` `--epoch=xid_epoch`: Configure manualmente a época da próxima ID de transação.

O período da ID da transação não é armazenado em nenhum lugar do banco de dados, exceto no campo que é definido por `pg_resetwal`, então qualquer valor funcionará, desde que o próprio banco de dados. Você pode precisar ajustar esse valor para garantir que sistemas de replicação, como Slony-I e Skytools, funcionem corretamente — se assim for, um valor apropriado deve ser obtido do estado do banco de dados replicado em linha.

`-l walfile` `--next-wal-file=walfile`: Configure manualmente a localização inicial do WAL, especificando o nome do próximo arquivo de segmento WAL.

O nome do próximo arquivo de segmento WAL deve ser maior que qualquer nome de arquivo de segmento WAL atualmente existente no diretório `pg_wal` sob o diretório de dados. Esses nomes também estão em hexadecimal e têm três partes. A primeira parte é o “ID de linha de tempo” e geralmente deve ser mantida a mesma. Por exemplo, se `00000001000000320000004A` é a entrada maior em `pg_wal`, use `-l 00000001000000320000004B` ou superior.

Observe que, ao usar tamanhos de segmento WAL não padrão, os números nos nomes dos arquivos WAL são diferentes dos LSNs que são relatados por funções do sistema e visualizações do sistema. Esta opção recebe um nome de arquivo WAL, não um LSN.

### Nota

O próprio `pg_resetwal` analisa os arquivos no `pg_wal` e escolhe uma configuração padrão do `-l` além do último nome de arquivo existente. Portanto, o ajuste manual do `-l` só deve ser necessário se você estiver ciente de arquivos de segmento WAL que não estão atualmente presentes no `pg_wal`, como entradas em um arquivo offline; ou se o conteúdo do `pg_wal` tiver sido perdido completamente.

`-m mxid,mxid` `--multixact-ids=mxid,mxid`: Configure manualmente o próximo e o ID de multitransação mais antigo.

Um valor seguro para o próximo ID de multitransação (primeira parte) pode ser determinado procurando pelo nome de arquivo numerologicamente maior no diretório `pg_multixact/offsets` sob o diretório de dados, adicionando um e, em seguida, multiplicando por 65536 (0x10000). Por outro lado, um valor seguro para o ID de multitransação mais antigo (segunda parte de `-m`) pode ser determinado procurando pelo nome de arquivo numerologicamente menor no mesmo diretório e multiplicando por 65536. Os nomes dos arquivos estão em hexadecimal, então a maneira mais fácil de fazer isso é especificar o valor da opção em hexadecimal e adicionar quatro zeros.

`-o oid` `--next-oid=oid`: Configure manualmente o próximo OID.

Não existe uma maneira comparativamente fácil de determinar o próximo OID que esteja além do maior existente no banco de dados, mas, felizmente, não é crítico acertar a configuração do próximo OID.

`-O mxoff` `--multixact-offset=mxoff`: Configure manualmente o próximo deslocamento de multitransação.

Um valor seguro pode ser determinado procurando pelo nome de arquivo numericamente maior no diretório `pg_multixact/members` sob o diretório de dados, adicionando um e, em seguida, multiplicando por 52352 (0xCC80). Os nomes dos arquivos estão em hexadecimal. Não há uma receita simples, como as outras opções de adição de zeros.

`-u xid` `--oldest-transaction-id=xid`: Configure manualmente o ID da transação mais antiga não congelada.

Um valor seguro pode ser determinado procurando pelo nome de arquivo numerologicamente menor no diretório `pg_xact` sob o diretório de dados e, em seguida, multiplicando por 1048576 (0x100000). Note que os nomes dos arquivos estão em hexadecimal. Geralmente, é mais fácil especificar o valor da opção em hexadecimal também. Por exemplo, se `0007` é a entrada menor em `pg_xact`, `-u 0x700000` funcionará (cinco zeros finais fornecem o multiplicador adequado).

`-x xid` `--next-transaction-id=xid`: Configure manualmente o próximo ID de transação.

Um valor seguro pode ser determinado procurando pelo nome de arquivo numericamente maior no diretório `pg_xact` sob o diretório de dados, adicionando um e, em seguida, multiplicando por 1048576 (0x100000). Note que os nomes dos arquivos estão em hexadecimal. Geralmente, é mais fácil especificar o valor da opção em hexadecimal também. Por exemplo, se `0011` é a entrada maior em `pg_xact`, `-x 0x1200000` funcionará (cinco zeros finais fornecem o multiplicador adequado).

`--char-signedness=option`: Configure manualmente a assinatura de caracteres padrão. Os valores possíveis são `signed` e `unsigned`.

Para um conjunto de bancos de dados que `pg_upgrade` atualizou a partir de uma versão do PostgreSQL anterior a 18, o valor seguro seria a assinatura `char` padrão da plataforma que executou o conjunto antes desse upgrade. Para todos os outros conjuntos, `signed` seria o valor seguro. No entanto, esta opção é exclusivamente para uso com `pg_upgrade` e normalmente não deve ser usada manualmente.

`--wal-segsize=wal_segment_size`: Defina o novo tamanho do segmento WAL, em megabytes. O valor deve ser definido como um expoente de 2 entre 1 e 1024 (megabytes). Consulte a mesma opção de [initdb](app-initdb.md) para obter mais informações.

Essa opção também pode ser usada para alterar o tamanho do segmento WAL de um clúster de banco de dados existente, evitando a necessidade de re-`initdb`.

### Nota

Embora o `pg_resetwal` defina o endereço inicial do WAL além do último arquivo de segmento WAL existente, algumas mudanças no tamanho do segmento podem fazer com que os nomes dos arquivos WAL anteriores sejam reutilizados. Recomenda-se o uso do `-l` juntamente com esta opção para definir manualmente o endereço inicial do WAL, se a sobreposição dos nomes dos arquivos WAL causar problemas com sua estratégia de arquivamento.

## Meio Ambiente

`PG_COLOR`: Especifica se a cor deve ser usada nas mensagens de diagnóstico. Os valores possíveis são `always`, `auto` e `never`.

## Notas

Este comando não deve ser usado quando o servidor estiver em execução. `pg_resetwal` se negar a iniciar se encontrar um arquivo de bloqueio do servidor no diretório de dados. Se o servidor falhar, então um arquivo de bloqueio pode ter sido deixado para trás; nesse caso, você pode remover o arquivo de bloqueio para permitir que `pg_resetwal` seja executado. Mas antes de fazer isso, certifique-se de que não há nenhum processo do servidor ainda vivo.

`pg_resetwal` funciona apenas com servidores da mesma versão principal.

## Veja também

[pg_controldata](app-pgcontroldata.md "pg_controldata")
