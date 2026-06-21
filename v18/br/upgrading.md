## 18.6. Atualização de um cluster PostgreSQL [#](#UPGRADING)

* [18.6.1. Atualização de dados via pg_dumpall](upgrading.md#UPGRADING-VIA-PGDUMPALL)
* [18.6.2. Atualização de dados via pg_upgrade](upgrading.md#UPGRADING-VIA-PG-UPGRADE)
* [18.6.3. Atualização de dados via Replicação](upgrading.md#UPGRADING-VIA-REPLICATION)

Esta seção discute como atualizar os dados do seu banco de dados de uma versão do PostgreSQL para uma versão mais recente.

Os números de versão atuais do PostgreSQL consistem em um número de versão principal e um número de versão secundária. Por exemplo, no número de versão 10.1, o 10 é o número de versão principal e o 1 é o número de versão secundária, o que significa que essa seria a primeira versão secundária da versão principal 10. Para versões anteriores à versão 10.0 do PostgreSQL, os números de versão consistem em três números, por exemplo, 9.5.3. Nesses casos, a versão principal consiste nos dois primeiros grupos de dígitos do número de versão, por exemplo, 9.5, e a versão secundária é o terceiro número, por exemplo, 3, o que significa que essa seria a terceira versão secundária da versão principal 9.5.

As versões menores nunca alteram o formato de armazenamento interno e são sempre compatíveis com versões menores anteriores e posteriores do mesmo número de versão principal. Por exemplo, a versão 10.1 é compatível com a versão 10.0 e a versão 10.6. Da mesma forma, por exemplo, 9.5.3 é compatível com 9.5.0, 9.5.1 e 9.5.6. Para atualizar entre versões compatíveis, você simplesmente substitui os executáveis enquanto o servidor está fora de operação e reinicia o servidor. O diretório de dados permanece inalterado — as atualizações menores são tão simples assim.

Para as versões *importantes* do PostgreSQL, o formato de armazenamento de dados interno está sujeito a alterações, o que complica as atualizações. O método tradicional para mover dados para uma nova versão importante é fazer o dump e restaurar o banco de dados, embora isso possa ser lento. Um método mais rápido é [pg_upgrade](pgupgrade.md). Métodos de replicação também estão disponíveis, conforme discutido abaixo. (Se você está usando uma versão pré-embalada do PostgreSQL, ela pode fornecer scripts para auxiliar nas atualizações de versão importante. Consulte a documentação do nível do pacote para detalhes.)

Novas versões principais também geralmente introduzem algumas incompatibilidades visíveis para o usuário, portanto, podem ser necessárias mudanças na programação de aplicativos. Todas as alterações visíveis para o usuário estão listadas nas notas de lançamento ([Apêndice E](release.md)); preste atenção especial à seção rotulada "Migração". Embora você possa fazer a atualização de uma versão principal para outra sem fazer a atualização para versões intermediárias, você deve ler as notas de lançamento principais de todas as versões intermediárias.

Os usuários cautelosos desejam testar suas aplicações de cliente na nova versão antes de fazer a migração completa; portanto, é frequentemente uma boa ideia configurar instalações concorrentes das versões antigas e novas. Ao testar uma atualização importante do PostgreSQL, considere as seguintes categorias de possíveis mudanças:

Administração: As capacidades disponíveis para os administradores para monitorar e controlar o servidor muitas vezes mudam e melhoram em cada versão importante.

SQL: Normalmente, isso inclui novas capacidades de comandos SQL e não mudanças de comportamento, a menos que especificamente mencionadas nas notas de lançamento.

API da biblioteca: Normalmente, bibliotecas como a libpq só adicionam novas funcionalidades, a menos que isso seja mencionado nas notas de lançamento.

Catálogos do sistema: as alterações nos catálogos do sistema geralmente afetam apenas as ferramentas de gerenciamento de banco de dados.

API de linguagem C do servidor: Isso envolve mudanças na API da função de backend, que é escrita na linguagem de programação C. Tais mudanças afetam o código que faz referência a funções de backend profundamente no servidor.

### 18.6.1. Atualização de dados via pg_dumpall [#](#UPGRADING-VIA-PGDUMPALL)

Um método de atualização é descartar dados de uma versão principal do PostgreSQL e restaurá-los em outra — para fazer isso, você deve usar uma ferramenta de backup *lógica*, como pg_dumpall; métodos de backup em nível de sistema de arquivos não funcionarão. (Existem verificações em vigor que impedem que você use um diretório de dados com uma versão incompatível do PostgreSQL, então não pode causar grande dano tentar iniciar a versão errada do servidor em um diretório de dados.)

Recomenda-se que você use os programas pg_dump e pg_dumpall da versão *mais recente* do PostgreSQL, para aproveitar as melhorias que podem ter sido feitas nesses programas. As versões atuais dos programas de dump podem ler dados de qualquer versão do servidor, desde a 9.2.

Essas instruções assumem que sua instalação existente está na pasta `/usr/local/pgsql`, e que a área de dados está em `/usr/local/pgsql/data`. Substitua seus caminhos conforme necessário.

1. Se estiver fazendo um backup, certifique-se de que seu banco de dados não esteja sendo atualizado. Isso não afeta a integridade do backup, mas, claro, os dados alterados não seriam incluídos. Se necessário, edite as permissões no arquivo `/usr/local/pgsql/data/pg_hba.conf` (ou equivalente) para não permitir acesso de todos, exceto você. Consulte [Capítulo 20](client-authentication.md) para obter informações adicionais sobre controle de acesso.

Para fazer backup da sua instalação do banco de dados, digite:

```
pg_dumpall > outputfile
```

Para fazer o backup, você pode usar o comando pg_dumpall da versão que você está executando atualmente; consulte [Seção 25.1.2](backup-dump.md#BACKUP-DUMP-ALL) para mais detalhes. No entanto, para obter os melhores resultados, tente usar o comando pg_dumpall do PostgreSQL 18.4, pois essa versão contém correções de bugs e melhorias em relação às versões anteriores. Embora esse conselho possa parecer peculiar, já que você ainda não instalou a nova versão, é aconselhável segui-lo se você planeja instalar a nova versão em paralelo com a versão antiga. Nesse caso, você pode completar a instalação normalmente e transferir os dados mais tarde. Isso também diminuirá o tempo de inatividade.

```
pg_ctl stop
```

Em sistemas que têm PostgreSQL iniciado no momento do boot, provavelmente há um arquivo de inicialização que fará a mesma coisa. Por exemplo, em um sistema Red Hat Linux, pode-se descobrir que isso funciona:

```
/etc/rc.d/init.d/postgresql stop
```

Veja [Capítulo 18](runtime.md) para obter detalhes sobre como iniciar e parar o servidor.
3. Se estiver restaurando a partir de um backup, renomeie ou exclua o diretório de instalação antigo, se não for específico para a versão. É uma boa ideia renomear o diretório, em vez de excluí-lo, caso você tenha problemas e precise revertê-lo. Tenha em mente que o diretório pode consumir um espaço de disco significativo. Para renomear o diretório, use um comando como este:

```
mv /usr/local/pgsql /usr/local/pgsql.old
```

(Certifique-se de mover o diretório como uma única unidade para que as caminhos relativos permaneçam inalterados.)
4. Instale a nova versão do PostgreSQL conforme descrito em [Capítulo 17](installation.md).
5. Crie um novo grupo de bancos de dados, se necessário. Lembre-se de que você deve executar esses comandos enquanto estiver logado na conta de usuário de banco de dados especial (que você já tem se estiver atualizando).

6. Restaure seus ``` /usr/local/pgsql/bin/initdb -D /usr/local/pgsql/data
```
anteriores e quaisquer modificações dos `pg_hba.conf`.
7. Inicie o servidor de banco de dados, novamente usando a conta de usuário especial do banco de dados:

8. Por fim, restaure seus dados do backup com:

```
   /usr/local/pgsql/bin/psql -d postgres -f outputfile
```

usando o *novo* psql.

O menor tempo de inatividade pode ser alcançado instalando o novo servidor em um diretório diferente e executando tanto o servidor antigo quanto o novo em paralelo, em diferentes portas. Em seguida, você pode usar algo como:

```
pg_dumpall -p 5432 | psql -d postgres -p 5433
```

para transferir seus dados.

### 18.6.2. Atualização de dados via pg_upgrade [#](#UPGRADING-VIA-PG-UPGRADE)

O módulo [pg_upgrade](pgupgrade.md) permite que uma instalação seja migrada in-place de uma versão principal do PostgreSQL para outra. As atualizações podem ser realizadas em minutos, particularmente com o modo `--link`. Requer etapas semelhantes às do pg_dumpall acima, por exemplo, iniciar/parar o servidor, executar initdb. A [documentação](pgupgrade.md) do pg_upgrade descreve as etapas necessárias.

### 18.6.3. Atualização de dados por replicação [#](#UPGRADING-VIA-REPLICATION)

É também possível usar métodos de replicação lógica para criar um servidor de espera com a versão atualizada do PostgreSQL. Isso é possível porque a replicação lógica suporta a replicação entre diferentes versões principais do PostgreSQL. O standby pode estar no mesmo computador ou em um computador diferente. Uma vez que tenha sincronizado-se com o servidor principal (que executa a versão mais antiga do PostgreSQL), você pode alternar os principais e fazer do standby o principal e desligar a instância do banco de dados mais antiga. Tal alternância resulta em apenas alguns segundos de tempo de inatividade para uma atualização.

Esse método de atualização pode ser realizado usando as facilidades de replicação lógica embutidas, bem como usando sistemas de replicação lógica externos, como pglogical, Slony, Londiste e Bucardo.