## 53.25. `pg_settings` [#](#VIEW-PG-SETTINGS)

A vista `pg_settings` fornece acesso aos parâmetros de execução do servidor. É essencialmente uma interface alternativa aos comandos `SHOW` (sql-show.md "SHOW") e `SET` (sql-set.md "SET"). Também fornece acesso a alguns fatos sobre cada parâmetro que não estão diretamente disponíveis em `SHOW` (sql-show.md "SHOW"), como valores mínimo e máximo.

**Tabela 53.25. Colunas `pg_settings`**



<table>
 <colgroup>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th class="catalog_table_entry">
    <p class="column_definition">
     Tipo de coluna
    </p>
    <p>
     Descrição
    </p>
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      name
     </code>
     <code>
      text
     </code>
    </p>
    <p>
     Nome do parâmetro de configuração de tempo de execução
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      setting
     </code>
     <code>
      text
     </code>
    </p>
    <p>
     Valor atual do parâmetro
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      unit
     </code>
     <code>
      text
     </code>
    </p>
    <p>
     Unidade implícita do parâmetro
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      category
     </code>
     <code>
      text
     </code>
    </p>
    <p>
     Grupo lógico do parâmetro
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      short_desc
     </code>
     <code>
      text
     </code>
    </p>
    <p>
     Uma breve descrição do parâmetro
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      extra_desc
     </code>
     <code>
      text
     </code>
    </p>
    <p>
     Descrição adicional e mais detalhada do parâmetro
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      context
     </code>
     <code>
      text
     </code>
    </p>
    <p>
     Contexto necessário para definir o valor do parâmetro (veja abaixo)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      vartype
     </code>
     <code>
      text
     </code>
    </p>
    <p>
     Tipo de parâmetro (
     <code>
      bool
     </code>
     ,
     <code>
      enum
     </code>
     ,
     <code>
      integer
     </code>
     ,
     <code>
      real
     </code>
     , ou
     <code>
      string
     </code>
     )
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      source
     </code>
     <code>
      text
     </code>
    </p>
    <p>
     Fonte do valor atual do parâmetro
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      min_val
     </code>
     <code>
      text
     </code>
    </p>
    <p>
     Valor mínimo permitido do parâmetro (nulo para valores não numéricos)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      max_val
     </code>
     <code>
      text
     </code>
    </p>
    <p>
     Valor máximo permitido do parâmetro (nulo para valores não numéricos)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      enumvals
     </code>
     <code>
      text[]
     </code>
    </p>
    <p>
     Valores permitidos de um parâmetro de enum (nulo para valores não de enum)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      boot_val
     </code>
     <code>
      text
     </code>
    </p>
    <p>
     Valor do parâmetro assumido no início do servidor, se o parâmetro não for definido de outra forma
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      reset_val
     </code>
     <code>
      text
     </code>
    </p>
    <p>
     Valorize
     <a class="link" href="sql-reset.md" title="RESET">
      <code>
       RESET
      </code>
     </a>
     redefinir o parâmetro para em sessão atual
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      sourcefile
     </code>
     <code>
      text
     </code>
    </p>
    <p>
     Arquivo de configuração no qual o valor atual foi definido (nulo para valores definidos a partir de fontes que não são arquivos de configuração, ou quando examinado por um usuário que não é um superusuário nem possui privilégios de
     <code>
      pg_read_all_settings
     </code>
     ); útil ao usar
     <code>
      include
     </code>
     diretrizes em arquivos de configuração
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      sourceline
     </code>
     <code>
      int4
     </code>
    </p>
    <p>
     Número de linha dentro do arquivo de configuração onde o valor atual foi definido (nulo para valores definidos a partir de fontes que não são arquivos de configuração, ou quando examinado por um usuário que não é um superusuário nem tem privilégios de
     <code>
      pg_read_all_settings
     </code>
     ).
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      pending_restart
     </code>
     <code>
      bool
     </code>
    </p>
    <p>
     <code>
      true
     </code>
     se o valor foi alterado no arquivo de configuração, mas precisa de um reinício; ou
     <code>
      false
     </code>
     otherwise.
    </p>
   </td>
  </tr>
 </tbody>
</table>










Existem vários valores possíveis para `context`. Em ordem decrescente de dificuldade para alterar o ajuste, eles são:

`internal`: Esses ajustes não podem ser alterados diretamente; eles refletem valores determinados internamente. Alguns deles podem ser ajustados reconstruindo o servidor com diferentes opções de configuração, ou alterando as opções fornecidas ao initdb.

`postmaster`: Esses ajustes podem ser aplicados apenas quando o servidor é iniciado, portanto, qualquer alteração requer o reinício do servidor. Os valores desses ajustes são normalmente armazenados no arquivo `postgresql.conf`, ou passados na linha de comando ao iniciar o servidor. Claro, os ajustes com qualquer um dos tipos de `context` mais baixos também podem ser definidos no momento do início do servidor.

`sighup`: As alterações nesses ajustes podem ser feitas em `postgresql.conf` sem precisar reiniciar o servidor. Envie um sinal SIGHUP ao postmaster para que ele leia novamente `postgresql.conf` e aplique as alterações. O postmaster também encaminhará o sinal SIGHUP para seus processos filhos, para que todos eles recebam o novo valor.

`superuser-backend`: As alterações nesses ajustes podem ser feitas em `postgresql.conf` sem reiniciar o servidor. Eles também podem ser definidos para uma sessão específica no pacote de solicitação de conexão (por exemplo, através da variável de ambiente `PGOPTIONS` do libpq), mas apenas se o usuário conectado for um superusuário ou tiver sido concedido o privilégio apropriado `SET`. No entanto, esses ajustes nunca são alterados em uma sessão após ela ser iniciada. Se você os alterar em `postgresql.conf`, envie um sinal SIGHUP ao postmaster para fazer com que ele leia novamente [[`postgresql.conf`]. Os novos valores só afetarão as sessões subsequentemente lançadas.

`backend`: As alterações nesses ajustes podem ser feitas em `postgresql.conf` sem reiniciar o servidor. Eles também podem ser definidos para uma sessão específica no pacote de solicitação de conexão (por exemplo, através da variável de ambiente `PGOPTIONS` de libpq); qualquer usuário pode fazer essa alteração para sua sessão. No entanto, esses ajustes nunca são alterados em uma sessão após ela ser iniciada. Se você os alterar em `postgresql.conf`, envie um sinal SIGHUP ao postmaster para fazer com que ele leia novamente `postgresql.conf`. Os novos valores só afetarão as sessões subsequentemente lançadas.

`superuser`: Esses ajustes podem ser definidos a partir de `postgresql.conf`, ou dentro de uma sessão através do comando `SET`; mas apenas superusuários e usuários com o privilégio apropriado `SET` podem alterá-los através de `SET`. Alterações em `postgresql.conf` afetarão as sessões existentes apenas se nenhum valor local de sessão tiver sido estabelecido com `SET`.

`user`: Esses ajustes podem ser definidos a partir de `postgresql.conf`, ou dentro de uma sessão através do comando `SET`. Qualquer usuário pode alterar seu valor local de sessão. Alterações em `postgresql.conf` afetarão apenas as sessões existentes, desde que não tenha sido estabelecido nenhum valor local de sessão com `SET`.

Consulte a [Seção 19.1](config-setting.md) para obter mais informações sobre as várias maneiras de alterar esses parâmetros.

Essa visão não pode ser inserida ou excluída, mas pode ser atualizada. Um `UPDATE` aplicado a uma linha de `pg_settings` é equivalente à execução do comando `SET` nesse parâmetro nomeado. A mudança afeta apenas o valor usado pela sessão atual. Se um `UPDATE` for emitido dentro de uma transação que seja posteriormente abortado, os efeitos do comando `UPDATE` desaparecerão quando a transação for revertida. Uma vez que a transação circunvizinha seja comprometida, os efeitos persistirão até o final da sessão, a menos que seja sobrescrito por outro `UPDATE` ou `SET`.

Essa visualização não exibe as opções personalizadas (runtime-config-custom.md "19.16. Customized Options") a menos que o módulo de extensão que as define tenha sido carregado pelo processo de backend que executa a consulta (por exemplo, por meio de uma menção em [shared_preload_libraries](runtime-config-client.md#GUC-SHARED-PRELOAD-LIBRARIES), uma chamada a uma função C na extensão ou o comando [`LOAD`](sql-load.md)). Por exemplo, uma vez que os módulos de [arquivos de arraste e deslocamento](archive-modules.md) são normalmente carregados apenas pelo processo de arquivador e não por sessões regulares, essa visualização não exibirá nenhuma opção personalizada definida por esses módulos a menos que uma ação especial seja tomada para carregá-los no processo de backend que executa a consulta.