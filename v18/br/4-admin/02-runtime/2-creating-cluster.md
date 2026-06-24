## 18.2. Criando um Clúster de Banco de Dados [#](#CREATING-CLUSTER)

* [18.2.1. Uso de sistemas de arquivos secundários](creating-cluster.md#CREATING-CLUSTER-MOUNT-POINTS)
* [18.2.2. Sistemas de arquivos](creating-cluster.md#CREATING-CLUSTER-FILESYSTEM)

Antes de poder fazer qualquer coisa, você deve inicializar uma área de armazenamento de banco de dados no disco. Chamamos isso de *clúster de banco de dados*. (O padrão SQL usa o termo clúster de catálogo.) Um clúster de banco de dados é uma coleção de bancos de dados que é gerenciada por uma única instância de um servidor de banco de dados em execução. Após a inicialização, um clúster de banco de dados conterá um banco de dados chamado `postgres`, que é destinado como um banco de dados padrão para uso por utilitários, usuários e aplicativos de terceiros. O próprio servidor de banco de dados não requer que o banco de dados `postgres` exista, mas muitos programas externos assumem que ele existe. Existem mais dois bancos de dados criados dentro de cada clúster durante a inicialização, nomeados `template1` e `template0`. Como os nomes sugerem, esses serão usados como modelos para bancos de dados posteriormente criados; eles não devem ser usados para trabalho real. (Consulte [Capítulo 22](managing-databases.md) para informações sobre a criação de novos bancos de dados dentro de um clúster.)

Em termos de sistema de arquivos, um grupo de bancos de dados é um único diretório sob o qual todos os dados serão armazenados. Chamamos isso de *diretório de dados* ou *área de dados*. É completamente sua escolha onde você deseja armazenar seus dados. Não há um padrão, embora locais como `/usr/local/pgsql/data` ou `/var/lib/pgsql/data` sejam populares. O diretório de dados deve ser inicializado antes de ser usado, usando o programa [initdb](app-initdb.md "initdb") que é instalado com o PostgreSQL.

Se você estiver usando uma versão pré-embalada do PostgreSQL, ela pode ter uma convenção específica sobre onde colocar o diretório de dados, e também pode fornecer um script para criar o diretório de dados. Nesse caso, você deve usar esse script em preferência para executar o `initdb` diretamente. Consulte a documentação do nível do pacote para obter detalhes.

Para inicializar um clúster de banco de dados manualmente, execute `initdb` e especifique a localização desejada do sistema de arquivos do clúster de banco de dados com a opção `-D`, por exemplo:

```
$ initdb -D /usr/local/pgsql/data
```

Observe que você deve executar este comando enquanto estiver logado na conta do usuário PostgreSQL, que é descrita na seção anterior.

DICA

Como alternativa à opção `-D`, você pode definir a variável de ambiente `PGDATA`.

Como alternativa, você pode executar `initdb` através do programa [pg_ctl](app-pg-ctl.md "pg_ctl") da seguinte forma:

```
$ pg_ctl -D /usr/local/pgsql/data initdb
```

Isso pode ser mais intuitivo se você estiver usando `pg_ctl` para iniciar e parar o servidor (consulte [Seção 18.3](server-start.md)), de modo que `pg_ctl` seja o único comando que você use para gerenciar a instância do servidor de banco de dados.

`initdb` tentará criar o diretório que você especificar se ele já não existir. Claro, isso falhará se `initdb` não tiver permissões para gravar no diretório pai. Geralmente é recomendável que o usuário do PostgreSQL não possua apenas o diretório de dados, mas também seu diretório pai, para que isso não seja um problema. Se o diretório pai desejado também não existir, você precisará criá-lo primeiro, usando privilégios de root se o diretório bisavô não for legível. Então, o processo pode parecer assim:

```
root# mkdir /usr/local/pgsql
root# chown postgres /usr/local/pgsql
root# su postgres
postgres$ initdb -D /usr/local/pgsql/data
```

`initdb` se negará a executar se o diretório de dados existir e já contiver arquivos; isso é para evitar sobrescrever acidentalmente uma instalação existente.

Como o diretório de dados contém todos os dados armazenados no banco de dados, é essencial que ele seja protegido contra acesso não autorizado. `initdb` revoga, portanto, as permissões de acesso de todos, exceto do usuário PostgreSQL e, opcionalmente, do grupo. O acesso do grupo, quando habilitado, é somente de leitura. Isso permite que um usuário não privilegiado no mesmo grupo do proprietário do clúster faça um backup dos dados do clúster ou realize outras operações que exigem apenas acesso de leitura.

Observe que habilitar ou desabilitar o acesso de grupo em um clúster existente requer que o clúster seja desligado e o modo apropriado seja definido em todos os diretórios e arquivos antes de reiniciar o PostgreSQL. Caso contrário, pode haver uma mistura de modos no diretório de dados. Para clústeres que permitem acesso apenas pelo proprietário, os modos apropriados são `0700` para diretórios e `0600` para arquivos. Para clústeres que também permitem leituras pelo grupo, os modos apropriados são `0750` para diretórios e `0640` para arquivos.

No entanto, embora o conteúdo do diretório seja seguro, a configuração padrão de autenticação do cliente permite que qualquer usuário local se conecte ao banco de dados e até se torne o superusuário do banco de dados. Se você não confia em outros usuários locais, recomendamos que você use uma das opções `initdb`, `-W`, `--pwprompt` ou `--pwfile` do `initdb` para atribuir uma senha ao superusuário do banco de dados. Além disso, especifique `-A scram-sha-256` para que o modo padrão de autenticação `trust` não seja usado; ou modifique o arquivo gerado `pg_hba.conf` após executar `initdb`, mas *antes* de iniciar o servidor pela primeira vez. (Outras abordagens razoáveis incluem o uso da autenticação `peer` ou permissões do sistema de arquivos para restringir as conexões. Consulte [Capítulo 20](client-authentication.md) para obter mais informações.)

`initdb` também inicializa o local padrão para o clúster de bancos de dados. Normalmente, ele apenas toma as configurações de local do ambiente e as aplica ao banco de dados inicializado. É possível especificar um local diferente para o banco de dados; mais informações sobre isso podem ser encontradas em [Seção 23.1](locale.md). A ordem de classificação padrão usada dentro do clúster de bancos de dados específico é definida por `initdb`, e, embora você possa criar novos bancos de dados usando diferentes ordens de classificação, a ordem usada nos bancos de dados de modelo que o initdb cria não pode ser alterada sem descartá-los e recriá-los. Há também um impacto de desempenho para o uso de locais diferentes de `C` ou `POSIX`. Portanto, é importante fazer essa escolha corretamente na primeira vez.

`initdb` também define o conjunto de codificação de caracteres padrão para o clúster de banco de dados. Normalmente, isso deve ser escolhido para corresponder ao ajuste do local. Para detalhes, consulte [Seção 23.3](multibyte.md).

Os locais não `C` e não `POSIX` dependem da biblioteca de ordenação do sistema operacional para a ordenação do conjunto de caracteres. Isso controla a ordenação das chaves armazenadas em índices. Por esse motivo, um clúster não pode alternar para uma versão incompatível da biblioteca de ordenação, seja por restauração de instantâneo, replicação binária em fluxo, um sistema operacional diferente ou uma atualização do sistema operacional.

### 18.2.1. Uso de sistemas de arquivos secundários [#](#CREATING-CLUSTER-MOUNT-POINTS)

Muitas instalações criam seus clusters de banco de dados em sistemas de arquivos (volumes) que não são o volume "raiz" da máquina. Se você optar por fazer isso, não é aconselhável tentar usar o diretório mais alto do volume secundário (ponto de montagem) como o diretório de dados. A melhor prática é criar um diretório dentro do diretório de ponto de montagem que seja de propriedade do usuário PostgreSQL e, em seguida, criar o diretório de dados dentro dele. Isso evita problemas de permissões, particularmente para operações como o pg_upgrade, e também garante falhas limpas se o volume secundário for desconectado.

### 18.2.2. Sistemas de Arquivos [#](#CREATING-CLUSTER-FILESYSTEM)

Geralmente, qualquer sistema de arquivos com semântica POSIX pode ser usado para o PostgreSQL. Os usuários preferem diferentes sistemas de arquivos por várias razões, incluindo suporte do fornecedor, desempenho e familiaridade. A experiência sugere que, se todas as outras coisas forem iguais, não se deve esperar grandes mudanças de desempenho ou comportamento apenas ao mudar de sistemas de arquivos ou fazer pequenas alterações na configuração do sistema de arquivos.

#### 18.2.2.1. NFS [#](#CREATING-CLUSTER-NFS)

É possível usar um sistema de arquivos NFS para armazenar o diretório de dados do PostgreSQL. O PostgreSQL não faz nada de especial para sistemas de arquivos NFS, o que significa que ele assume que o NFS se comporta exatamente como unidades conectadas localmente. O PostgreSQL não usa nenhuma funcionalidade que é conhecida por ter comportamento não padrão no NFS, como bloqueio de arquivos.

A única exigência para usar o NFS com o PostgreSQL é que o sistema de arquivos seja montado usando a opção `hard`. Com a opção `hard`, os processos podem "ficar" indefinidamente se houver problemas de rede, então essa configuração exigirá uma configuração cuidadosa. A opção `soft` interromperá as chamadas do sistema em caso de problemas de rede, mas o PostgreSQL não repetirá as chamadas do sistema interrompidas dessa maneira, então qualquer interrupção resultará em um erro de I/O sendo relatado.

Não é necessário usar a opção de montagem `sync`. O comportamento da opção `async` é suficiente, pois o PostgreSQL emite chamadas `fsync` em momentos apropriados para esvaziar os caches de escrita. (Isso é análogo ao funcionamento em um sistema de arquivos local.) No entanto, é fortemente recomendado usar a opção de exportação `sync` no *servidor* NFS em sistemas onde ela existe (principalmente Linux). Caso contrário, não é garantido que uma `fsync` ou equivalente no cliente NFS realmente alcance o armazenamento permanente no servidor, o que poderia causar corrupção semelhante à execução com o parâmetro [fsync](runtime-config-wal.md#GUC-FSYNC) desativado. Os padrões dessas opções de montagem e exportação diferem entre fornecedores e versões, portanto, é recomendável verificar e, se possível, especificá-los explicitamente, em qualquer caso, para evitar qualquer ambiguidade.

Em alguns casos, um produto de armazenamento externo pode ser acessado através de NFS ou de um protocolo de nível inferior, como iSCSI. Neste último caso, o armazenamento aparece como um dispositivo de bloco e qualquer sistema de arquivos disponível pode ser criado nele. Essa abordagem pode aliviar o DBA de ter que lidar com algumas das características peculiares do NFS, mas, claro, a complexidade de gerenciar armazenamento remoto ocorre em outros níveis.