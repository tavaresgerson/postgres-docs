## 53.8. `pg_file_settings` [#](#VIEW-PG-FILE-SETTINGS)

A vista `pg_file_settings` fornece um resumo dos conteúdos do(s) arquivo(s) de configuração do servidor. Uma linha aparece nesta vista para cada entrada “nome = valor” que aparece nos arquivos, com anotações indicando se o valor pode ser aplicado com sucesso. Pode aparecer(em) mais uma linha(s) para problemas não vinculados a uma entrada “nome = valor”, como erros de sintaxe nos arquivos.

Essa visão é útil para verificar se as mudanças planejadas nos arquivos de configuração funcionarão ou para diagnosticar uma falha anterior. Note que essa visão relata os *conteúdos* atuais dos arquivos, não sobre o que foi aplicado pela última vez pelo servidor. (A visão `pg_settings`(view-pg-settings.md "53.25. pg_settings") geralmente é suficiente para determinar isso.)

Por padrão, a visualização `pg_file_settings` pode ser lida apenas por superusuários.

**Tabela 53.8. Colunas `pg_file_settings`**



<table border="1" class="table" summary="pg_file_settings Columns">
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
     <code class="structfield">
      sourcefile
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     Nome completo do caminho do arquivo de configuração
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      sourceline
     </code>
     <code class="type">
      int4
     </code>
    </p>
    <p>
     Número da linha dentro do arquivo de configuração onde a entrada aparece
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      seqno
     </code>
     <code class="type">
      int4
     </code>
    </p>
    <p>
     Ordem em que as entradas são processadas (1..
     <em class="replaceable">
      <code>
       n
      </code>
     </em>
     )
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      name
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     Nome do parâmetro de configuração
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      setting
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     Valor a ser atribuído ao parâmetro
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      applied
     </code>
     <code class="type">
      bool
     </code>
    </p>
    <p>
     Verdadeiro se o valor puder ser aplicado com sucesso
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      error
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     Se não for nulo, uma mensagem de erro indicando por que essa entrada não pode ser aplicada
    </p>
   </td>
  </tr>
 </tbody>
</table>









Se o arquivo de configuração contiver erros de sintaxe ou nomes de parâmetros inválidos, o servidor não tentará aplicar quaisquer configurações nele, e, portanto, todos os campos `applied` serão lidos como falsos. Nesse caso, haverá uma ou mais linhas com campos `error` não nulos, indicando o(s) problema(s). Caso contrário, as configurações individuais serão aplicadas, se possível. Se uma configuração individual não puder ser aplicada (por exemplo, um valor inválido ou a configuração não pode ser alterada após o início do servidor), ela terá uma mensagem apropriada no campo `error`. Outra maneira em que uma entrada pode ter `applied` = false é que ela seja sobrescrita por uma entrada posterior para o mesmo nome de parâmetro; esse caso não é considerado um erro, então nada aparece no campo `error`.

Consulte a [Seção 19.1](config-setting.md) para obter mais informações sobre as várias maneiras de alterar os parâmetros de execução.