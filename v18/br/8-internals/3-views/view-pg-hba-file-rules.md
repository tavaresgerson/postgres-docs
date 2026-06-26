## 53.10. `pg_hba_file_rules` [#](#VIEW-PG-HBA-FILE-RULES)

A vista `pg_hba_file_rules` fornece um resumo dos conteúdos do arquivo de configuração de autenticação do cliente, `pg_hba.conf`(auth-pg-hba-conf.md "20.1. The pg_hba.conf File"). Uma linha aparece nesta vista para cada linha não vazia e não comentada no arquivo, com anotações indicando se a regra poderia ser aplicada com sucesso.

Essa visão pode ser útil para verificar se as alterações planejadas no arquivo de configuração de autenticação funcionarão ou para diagnosticar uma falha anterior. Note que essa visão relata os *conteúdos* atuais do arquivo, não sobre o que foi carregado pela última vez pelo servidor.

Por padrão, a visualização `pg_hba_file_rules` pode ser lida apenas por superusuários.

**Tabela 53.10. Colunas `pg_hba_file_rules`**



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
      rule_number
     </code>
     <code>
      int4
     </code>
    </p>
    <p>
     Número desta regra, se válida, caso contrário
     <code>
      NULL
     </code>
     . Isso indica a ordem em que cada regra é considerada até que uma correspondência seja encontrada durante a autenticação.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      file_name
     </code>
     <code>
      text
     </code>
    </p>
    <p>
     Nome do arquivo que contém esta regra
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      line_number
     </code>
     <code>
      int4
     </code>
    </p>
    <p>
     Número da linha desta regra em
     <code>
      file_name
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      type
     </code>
     <code>
      text
     </code>
    </p>
    <p>
     Tipo de conexão
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      database
     </code>
     <code>
      text[]
     </code>
    </p>
    <p>
     Lista de nome(s) do banco de dados a que esta regra se aplica
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      user_name
     </code>
     <code>
      text[]
     </code>
    </p>
    <p>
     Lista de nome(s) do usuário e grupo(s) a que esta regra se aplica
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      address
     </code>
     <code>
      text
     </code>
    </p>
    <p>
     Nome do host ou endereço IP, ou um dos
     <code>
      all
     </code>
     ,
     <code>
      samehost
     </code>
     , ou
     <code>
      samenet
     </code>
     , ou nulo para conexões locais
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      netmask
     </code>
     <code>
      text
     </code>
    </p>
    <p>
     Máscara de endereço IP, ou nulo, se não for aplicável
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      auth_method
     </code>
     <code>
      text
     </code>
    </p>
    <p>
     Método de autenticação
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      options
     </code>
     <code>
      text[]
     </code>
    </p>
    <p>
     Opções especificadas para o método de autenticação, se houver
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      error
     </code>
     <code>
      text
     </code>
    </p>
    <p>
     Se não for nulo, uma mensagem de erro indicando por que essa linha não pode ser processada
    </p>
   </td>
  </tr>
 </tbody>
</table>










Normalmente, uma linha que reflete uma entrada incorreta terá valores apenas nos campos `line_number` e `error`.

Veja [Capítulo 20](client-authentication.md "Chapter 20. Client Authentication") para mais informações sobre a configuração de autenticação do cliente.