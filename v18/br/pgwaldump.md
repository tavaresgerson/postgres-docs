## pg_waldump

pg_waldump — exibe uma representação legível para humanos do log de pré-escrita de um clúster de banco de dados PostgreSQL

## Sinopse

`pg_waldump` [`option`...] [`startseg` [`endseg`]]

## Descrição

`pg_waldump` exibe o log de pré-escrita (WAL) e é principalmente útil para fins de depuração ou educacionais.

Esse utilitário só pode ser executado pelo usuário que instalou o servidor, porque ele requer acesso apenas de leitura ao diretório de dados.

## Opções

As opções de linha de comando a seguir controlam a localização e o formato do resultado:

*`startseg`*: Comece a leitura no arquivo especificado do segmento WAL. Isso determina implicitamente o caminho em que os arquivos serão pesquisados e o cronograma a ser usado.

*`endseg`*: Parar após a leitura do arquivo especificado do segmento WAL.

`-b` `--bkp-details`: Forneça informações detalhadas sobre os blocos de backup.

`-B block` `--block=block`: Exiba apenas os registros que modificam o bloco fornecido. A relação também deve ser fornecida com `--relation` ou `-R`.

`-e end` `--end=end`: Parar de ler na localização especificada do WAL, em vez de ler até o final do fluxo de registro.

`-f` `--follow`: Após atingir o fim do WAL válido, continue a fazer uma pesquisa por segundo para que um novo WAL apareça.

`-F fork` `--fork=fork`: Exiba apenas os registros que modificam blocos no ramo dado. Os valores válidos são `main` para o ramo principal, `fsm` para o mapa de espaço livre, `vm` para o mapa de visibilidade e `init` para o ramo init.

`-n limit` `--limit=limit`: Exibir o número especificado de registros e, em seguida, parar.

`-p path` `--path=path`: Especifica um diretório para procurar arquivos de segmento WAL ou um diretório com um subdiretório `pg_wal` que contenha tais arquivos. O padrão é procurar no diretório atual, no subdiretório `pg_wal` do diretório atual e no subdiretório `pg_wal` de `PGDATA`.

`-q` `--quiet`: Não imprima nenhum resultado, exceto erros. Esta opção pode ser útil quando você deseja saber se um intervalo de registros WAL pode ser analisado com sucesso, mas não se importa com o conteúdo do registro.

`-r rmgr` `--rmgr=rmgr`: Exiba apenas os registros gerados pelo gerenciador de recursos especificado. Você pode especificar a opção várias vezes para selecionar vários geradores de recursos. Se `list` for passado como nome, imprima uma lista de nomes válidos de geradores de recursos e saia.

As extensões podem definir gestores de recursos personalizados, mas o pg_waldump não carrega o módulo de extensão e, portanto, não reconhece gestores de recursos personalizados pelo nome. Em vez disso, você pode especificar os gestores de recursos personalizados como `custom###` onde *`###`* é o ID do gerente de recursos de três dígitos. Os nomes dessa forma serão sempre considerados válidos.

`-R tblspc/db/rel` `--relation=tblspc/db/rel`: Exiba apenas os registros que modificam blocos na relação especificada. A relação é especificada com OID de tablespace, OID de banco de dados e relfilenode separados por barras, por exemplo `1234/12345/12345`. Este é o mesmo formato usado para relações na saída do programa.

`-s start` `--start=start`: Local da WAL em que se deve começar a leitura. O padrão é começar a leitura do primeiro registro válido da WAL encontrado no primeiro arquivo encontrado.

`-t timeline` `--timeline=timeline`: Cronograma a partir do qual os registros WAL devem ser lidos. O valor padrão é o especificado em *`startseg`*, se este for especificado; caso contrário, o valor padrão é 1. O valor pode ser especificado em decimal ou hexadecimal, por exemplo, `17` ou `0x11`.

`-V` `--version`: Imprima a versão do pg_waldump e saia.

`-w` `--fullpage`: Exiba apenas os registros que incluem imagens de página inteira.

`-x xid` `--xid=xid`: Exiba apenas os registros marcados com o ID de transação fornecido.

`-z` `--stats[=record]`: Exibir estatísticas resumidas (número e tamanho dos registros e imagens de página inteira) em vez de registros individuais. Opcionalmente, gerar estatísticas por registro em vez de por rmg.

Se o pg_waldump for encerrado por sinal SIGINT (**Controle** + **C**), o resumo das estatísticas calculadas é exibido até o ponto de término. Essa operação não é suportada no Windows.

`--save-fullpage=save_path`: Salve as imagens completas da página encontradas nos registros do WAL no diretório *`save_path`*. As imagens salvas estão sujeitas aos mesmos critérios de filtragem e limitação que os registros exibidos.

As imagens da página inteira são salvas com o seguinte formato de nome de arquivo: `TIMELINE-LSN.RELTABLESPACE.DATOID.RELNODE.BLKNO_FORK` Os nomes dos arquivos são compostos pelas seguintes partes:



<table border="1" class="informaltable">
 <colgroup>
  <col/>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th>
    Component
   </th>
   <th>
    Descrição
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    TIMELINE
   </td>
   <td>
    A linha cronológica do arquivo de segmento WAL, onde o registro está localizado, formatada como um número hexadecimal de 8 caracteres
    <code class="literal">
     %08X
    </code>
   </td>
  </tr>
  <tr>
   <td>
    LSN
   </td>
   <td>
    O
    <acronym class="acronym">
     LSN
    </acronym>
    do registro com esta imagem, formatado como dois números hexadecimais de 8 caracteres
    <code class="literal">
     %08X-%08X
    </code>
   </td>
  </tr>
  <tr>
   <td>
    RELTABLESPACE
   </td>
   <td>
    índice de identificação de espaço de tabela do bloco
   </td>
  </tr>
  <tr>
   <td>
    DATOID
   </td>
   <td>
    OID do banco de dados do bloco
   </td>
  </tr>
  <tr>
   <td>
    RELNODE
   </td>
   <td>
    nó de arquivo do bloco
   </td>
  </tr>
  <tr>
   <td>
    BLKNO
   </td>
   <td>
    número de bloco do bloco
   </td>
  </tr>
  <tr>
   <td>
    FORK
   </td>
   <td>
    O nome do garfo de onde a imagem da página inteira veio, como
    <code class="literal">
     main
    </code>
    ,
    <code class="literal">
     fsm
    </code>
    ,
    <code class="literal">
     vm
    </code>
    , ou
    <code class="literal">
     init
    </code>
    .
   </td>
  </tr>
 </tbody>
</table>







`-?` `--help`: Mostrar ajuda sobre os argumentos da linha de comando do comando pg_waldump e sair.

## Meio Ambiente

`PGDATA`: Diretório de dados; veja também a opção `-p`.

`PG_COLOR`: Especifica se a cor deve ser usada nas mensagens de diagnóstico. Os valores possíveis são `always`, `auto` e `never`.

## Notas

Pode dar resultados errados quando o servidor está em execução.

Apenas o cronograma especificado é exibido (ou o padrão, se nenhum for especificado). Os registros em outros cronogramas são ignorados.

O pg_waldump não pode ler arquivos WAL com o sufixo `.partial`. Se esses arquivos precisam ser lidos, o sufixo `.partial` precisa ser removido do nome do arquivo.

## Veja também

[Seção 28.6](wal-internals.md "28.6. WAL Internals")