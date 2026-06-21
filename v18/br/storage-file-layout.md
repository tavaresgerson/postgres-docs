## 66.1. Estrutura do arquivo de banco de dados [#](#STORAGE-FILE-LAYOUT)

Esta seção descreve o formato de armazenamento ao nível de arquivos e diretórios.

Tradicionalmente, as configurações e os arquivos de dados usados por um clúster de banco de dados são armazenados juntos dentro do diretório de dados do clúster, comumente referido como `PGDATA` (depois do nome da variável de ambiente que pode ser usada para defini-lo). Um local comum para `PGDATA` é `/var/lib/pgsql/data`. Múltiplos clústeres, gerenciados por diferentes instâncias de servidor, podem existir na mesma máquina.

O diretório `PGDATA` contém vários subdiretórios e arquivos de controle, conforme mostrado na [Tabela 66.1](storage-file-layout.md#PGDATA-CONTENTS-TABLE "Table 66.1. Contents of PGDATA"). Além desses itens necessários, os arquivos de configuração do clúster `postgresql.conf`, `pg_hba.conf` e `pg_ident.conf` são tradicionalmente armazenados em `PGDATA`, embora seja possível colocá-los em outro lugar.

**Tabela 66.1. Conteúdo de `PGDATA`**



<table border="1" class="table" summary="Contents of PGDATA">
 <colgroup>
  <col/>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th>
    Item
   </th>
   <th>
    Descrição
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <code class="filename">
     PG_VERSION
    </code>
   </td>
   <td>
    Um arquivo contendo o número da versão principal
    <span class="productname">
     PostgreSQL
    </span>
   </td>
  </tr>
  <tr>
   <td>
    <code class="filename">
     base
    </code>
   </td>
   <td>
    Subdiretório contendo subdiretórios por banco de dados
   </td>
  </tr>
  <tr>
   <td>
    <code class="filename">
     current_logfiles
    </code>
   </td>
   <td>
    Arquivo que registra o(s) arquivo(s) de registro atualmente escrito(s) pelo coletor de registro
   </td>
  </tr>
  <tr>
   <td>
    <code class="filename">
     global
    </code>
   </td>
   <td>
    Subdiretório contendo tabelas de todo o clúster, como
    <code class="structname">
     pg_database
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="filename">
     pg_commit_ts
    </code>
   </td>
   <td>
    Subdiretório contendo dados de marcação de confirmação de transação
   </td>
  </tr>
  <tr>
   <td>
    <code class="filename">
     pg_dynshmem
    </code>
   </td>
   <td>
    Subdiretório contendo arquivos usados pelo subsistema de memória compartilhada dinâmica
   </td>
  </tr>
  <tr>
   <td>
    <code class="filename">
     pg_logical
    </code>
   </td>
   <td>
    Subdiretório contendo dados de status para decodificação lógica
   </td>
  </tr>
  <tr>
   <td>
    <code class="filename">
     pg_multixact
    </code>
   </td>
   <td>
    Subdiretório contendo dados de status de multitransação (usado para bloqueios de linha compartilhada)
   </td>
  </tr>
  <tr>
   <td>
    <code class="filename">
     pg_notify
    </code>
   </td>
   <td>
    Subdiretório contendo dados de status LISTEN/NOTIFY
   </td>
  </tr>
  <tr>
   <td>
    <code class="filename">
     pg_replslot
    </code>
   </td>
   <td>
    Subdiretório contendo dados de slot de replicação
   </td>
  </tr>
  <tr>
   <td>
    <code class="filename">
     pg_serial
    </code>
   </td>
   <td>
    Subdiretório contendo informações sobre transações serializáveis comprometidas
   </td>
  </tr>
  <tr>
   <td>
    <code class="filename">
     pg_snapshots
    </code>
   </td>
   <td>
    Subdiretório contendo instantâneos exportados
   </td>
  </tr>
  <tr>
   <td>
    <code class="filename">
     pg_stat
    </code>
   </td>
   <td>
    Subdiretório contendo arquivos permanentes para o subsistema de estatísticas
   </td>
  </tr>
  <tr>
   <td>
    <code class="filename">
     pg_stat_tmp
    </code>
   </td>
   <td>
    Subdiretório contendo arquivos temporários para o subsistema de estatísticas
   </td>
  </tr>
  <tr>
   <td>
    <code class="filename">
     pg_subtrans
    </code>
   </td>
   <td>
    Subdiretório contendo dados de status de subtransação
   </td>
  </tr>
  <tr>
   <td>
    <code class="filename">
     pg_tblspc
    </code>
   </td>
   <td>
    Subdiretório contendo links simbólicos para espaços de tabela
   </td>
  </tr>
  <tr>
   <td>
    <code class="filename">
     pg_twophase
    </code>
   </td>
   <td>
    Subdiretório contendo arquivos de estado para transações preparadas
   </td>
  </tr>
  <tr>
   <td>
    <code class="filename">
     pg_wal
    </code>
   </td>
   <td>
    Subdiretório contendo arquivos WAL (Write Ahead Log)
   </td>
  </tr>
  <tr>
   <td>
    <code class="filename">
     pg_xact
    </code>
   </td>
   <td>
    Subdiretório contendo dados de status de compromisso de transação
   </td>
  </tr>
  <tr>
   <td>
    <code class="filename">
     postgresql.auto.conf
    </code>
   </td>
   <td>
    Um arquivo usado para armazenar parâmetros de configuração que são definidos por
    <code class="command">
     ALTER SYSTEM
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="filename">
     postmaster.opts
    </code>
   </td>
   <td>
    Um arquivo que registra as opções de linha de comando com as quais o servidor foi iniciado pela última vez
   </td>
  </tr>
  <tr>
   <td>
    <code class="filename">
     postmaster.pid
    </code>
   </td>
   <td>
    Um arquivo de bloqueio que registra o ID atual do processo postmaster (PID), o caminho do diretório de dados do cluster, o timestamp de início do postmaster, o número de porta, o caminho do diretório do socket de domínio Unix (pode estar vazio), o primeiro endereço de escuta válido (endereço IP ou
    <code class="literal">
     *
    </code>
    , ou vazio se não estiver ouvindo em TCP), e ID do segmento de memória compartilhada (este arquivo não está presente após o desligamento do servidor)
   </td>
  </tr>
 </tbody>
</table>









Para cada banco de dados no clúster, há um subdiretório dentro de `PGDATA``/base`, com o nome do OID do banco de dados no `pg_database`. Este subdiretório é o local padrão para os arquivos do banco de dados; em particular, seus catálogos do sistema são armazenados lá.

Observe que as seções a seguir descrevem o comportamento do método de acesso à tabela embutido `heap` [(tableam.md "Chapter 62. Table Access Method Interface Definition")], e os métodos de acesso ao índice embutido (indexam.md "Chapter 63. Index Access Method Interface Definition"). Devido à natureza extensiva do PostgreSQL, outros métodos de acesso podem funcionar de maneira diferente.

Cada tabela e índice é armazenado em um arquivo separado. Para relações comuns, esses arquivos são nomeados com base no número *filenode* da tabela ou índice, que pode ser encontrado em `pg_class`.`relfilenode`. Mas para relações temporárias, o nome do arquivo é da forma `tBBB_FFF`, onde *`BBB`* é o número do processo do backend que criou o arquivo, e *`FFF`* é o número *filenode*. Em ambos os casos, além do arquivo principal (também conhecido como principal), cada tabela e índice tem um *mapa de espaço livre* (ver [Seção 66.3](storage-fsm.md "66.3. Free Space Map")), que armazena informações sobre o espaço livre disponível na relação. O mapa de espaço livre é armazenado em um arquivo com o número *filenode* mais o sufixo `_fsm`. As tabelas também têm um *mapa de visibilidade*, armazenado em um fork com o sufixo `_vm`, para rastrear quais páginas são conhecidas por não ter tuplas mortas. O mapa de visibilidade é descrito mais adiante em [Seção 66.4](storage-vm.md "66.4. Visibility Map") Unlogged tables and indexes have a third fork, known as the initialization fork, which is stored in a fork with the suffix `_init` (see [Section 66.5](storage-init.md "66.5. The Initialization Fork")).

### Atenção

Observe que, embora o filenode de uma tabela muitas vezes corresponda ao seu OID, isso *não* é necessariamente o caso; algumas operações, como `TRUNCATE`, `REINDEX`, `CLUSTER` e algumas formas de `ALTER TABLE`, podem alterar o filenode enquanto preservam o OID. Evite assumir que filenode e OID da tabela são iguais. Além disso, para certos catálogos do sistema, incluindo o próprio `pg_class`, `pg_class`.`relfilenode` contém zero. O número real do filenode desses catálogos é armazenado em uma estrutura de dados de nível inferior e pode ser obtido usando a função `pg_relation_filenode()`.

Quando uma tabela ou índice excede 1 GB, ele é dividido em *segmentos* de tamanho de gigabyte. O nome do arquivo do primeiro segmento é o mesmo do filenode; os segmentos subsequentes são nomeados filenode.1, filenode.2, etc. Esse arranjo evita problemas em plataformas que têm limitações de tamanho de arquivo. (Na verdade, 1 GB é apenas o tamanho padrão do segmento. O tamanho do segmento pode ser ajustado usando a opção de configuração `--with-segsize` ao construir o PostgreSQL.) Em princípio, os mapas de espaço livre e mapas de visibilidade também podem exigir múltiplos segmentos, embora isso seja improvável na prática.

Uma tabela que tem colunas com entradas potencialmente grandes terá uma tabela *TOAST* associada, que é usada para armazenamento fora da linha de valores de campo que são muito grandes para serem mantidos nas próprias linhas da tabela. `pg_class`.`reltoastrelid` faz ligações de uma tabela para sua tabela TOAST, se houver. Consulte [Seção 66.2](storage-toast.md) para mais informações.

Os conteúdos de tabelas e índices são discutidos mais adiante na [Seção 66.6](storage-page-layout.md).

Os tablespaces tornam o cenário mais complicado. Cada tablespace definido pelo usuário tem um link simbólico dentro do diretório `PGDATA``/pg_tblspc`, que aponta para o diretório do tablespace físico (ou seja, o local especificado no comando `CREATE TABLESPACE` do tablespace). Esse link simbólico é nomeado com base no OID do tablespace. Dentro do diretório do tablespace físico, há um subdiretório com um nome que depende da versão do servidor PostgreSQL, como `PG_9.0_201008051`. (O motivo de usar esse subdiretório é para que as versões sucessivas do banco de dados possam usar o mesmo valor de localização `CREATE TABLESPACE` sem conflitos.) Dentro do subdiretório específico para a versão, há um subdiretório para cada banco de dados que tem elementos no tablespace, nomeado com base no OID do banco de dados. Tabelas e índices são armazenados dentro desse diretório, usando o esquema de nomeação de filenode. O tablespace `pg_default` não é acessado através de `pg_tblspc`, mas corresponde a `PGDATA``/base`. Da mesma forma, o tablespace `pg_global` não é acessado através de `pg_tblspc`, mas corresponde a `PGDATA``/global`.

A função `pg_relation_filepath()` mostra o caminho completo (em relação a `PGDATA`) de qualquer relação. É frequentemente útil como substituto para lembrar muitas das regras acima. Mas tenha em mente que essa função apenas fornece o nome do primeiro segmento do principal ramo da relação — você pode precisar adicionar um número de segmento e/ou `_fsm`, `_vm` ou `_init` para encontrar todos os arquivos associados à relação.

Arquivos temporários (para operações como classificação de mais dados do que cabem na memória) são criados dentro de `PGDATA``/base/pgsql_tmp`, ou dentro de um subdiretório `pgsql_tmp` de um diretório de espaço de tabela, se um espaço de tabela diferente de `pg_default` for especificado para eles. O nome de um arquivo temporário tem a forma `pgsql_tmpPPP.NNN`, onde *`PPP`* é o PID do backend proprietário e *`NNN`* distingue diferentes arquivos temporários desse backend.