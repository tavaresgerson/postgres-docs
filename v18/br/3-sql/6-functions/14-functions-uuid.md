### 9.14. Funções UUID [#](#FUNCTIONS-UUID)

[Tabela 9.45](functions-uuid.md#FUNC_UUID_GEN_TABLE) mostra as funções do PostgreSQL que podem ser usadas para gerar UUIDs.

**Tabela 9.45. Funções de Geração de UUID**

<table>
 <colgroup>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th class="func_table_entry">
    <p class="func_signature">
     Função
    </p>
    <p>
     Descrição
    </p>
    <p>
     Exemplo(s)
    </p>
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      gen_random_uuid
     </code>
     ( )
     <code>
      uuid
     </code>
    </p>
    <p class="func_signature">
     <code>
      uuidv4
     </code>
     ( )
     <code>
      uuid
     </code>
    </p>
    <p>
     Gera uma versão 4 (aleatória) de UUID
    </p>
    <p>
     <code>
      gen_random_uuid()
     </code>
     →
     <code>
      5b30857f-0bfa-48b5-ac0b-5c64e28078d1
     </code>
    </p>
    <p>
     <code>
      uuidv4()
     </code>
     →
     <code>
      b42410ee-132f-42ee-9e4f-09a6485c95b8
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      uuidv7
     </code>
     ( [
     <span class="optional">
      <em class="parameter">
       <code>
        shift
       </code>
      </em>
      <code>
       interval
      </code>
     </span>
     ] ) →
     <code>
      uuid
     </code>
    </p>
    <p>
     Gera uma UUID da versão 7 (ordenada cronologicamente). O timestamp é calculado usando o timestamp UNIX com precisão de milissegundo + timestamp sub-milissegundo + aleatório. O parâmetro opcional
     <em class="parameter">
      <code>
       shift
      </code>
     </em>
     mudará o horário de registro calculado pelo dado
     <code>
      interval
     </code>
     .
    </p>
    <p>
     <code>
      uuidv7()
     </code>
     →
     <code>
      019535d9-3df7-79fb-b466-fa907fa17f9e
     </code>
    </p>
   </td>
  </tr>
 </tbody>
</table>

Nota

O módulo [uuid-ossp](uuid-ossp.md) fornece funções adicionais que implementam outros algoritmos padrão para gerar UUIDs.

[Tabela 9.46](functions-uuid.md#FUNC_UUID_EXTRACT_TABLE) mostra as funções do PostgreSQL que podem ser usadas para extrair informações de UUIDs.

**Tabela 9.46. Funções de extração de UUID**

<table>
 <colgroup>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th class="func_table_entry">
    <p class="func_signature">
     Função
    </p>
    <p>
     Descrição
    </p>
    <p>
     Exemplo(s)
    </p>
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      uuid_extract_timestamp
     </code>
     (
     <code>
      uuid
     </code>
     ) →
     <code>
      timestamp with time zone
     </code>
    </p>
    <p>
     Extrai um
     <code>
      timestamp with time zone
     </code>
     de uma UUID da versão 1 ou 7. Para outras versões, essa função retorna null. Observe que o timestamp extraído não é necessariamente exatamente igual ao momento em que a UUID foi gerada; isso depende da implementação que gerou a UUID.
    </p>
    <p>
     <code>
      uuid_extract_timestamp('019535d9-3df7-79fb-b466-​fa907fa17f9e'::uuid)
     </code>
     →
     <code>
      2025-02-23 21:46:24.503-05
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      uuid_extract_version
     </code>
     (
     <code>
      uuid
     </code>
     ) →
     <code>
      smallint
     </code>
    </p>
    <p>
     Extrai a versão a partir de uma UUID de uma das variantes descritas por
     <a class="ulink" href="https://datatracker.ietf.org/doc/html/rfc9562" target="_top">
      RFC 9562
     </a>
     Para outras variantes, essa função retorna null. Por exemplo, para uma UUID gerada por
     <code>
      gen_random_uuid()
     </code>
     , essa função retornará 4.
    </p>
    <p>
     <code>
      uuid_extract_version('41db1265-8bc1-4ab3-992f-​885799a4af1d'::uuid)
     </code>
     →
     <code>
      4
     </code>
    </p>
    <p>
     <code>
      uuid_extract_version('019535d9-3df7-79fb-b466-​fa907fa17f9e'::uuid)
     </code>
     →
     <code>
      7
     </code>
    </p>
   </td>
  </tr>
 </tbody>
</table>

O PostgreSQL também fornece os operadores de comparação habituais mostrados na [Tabela 9.1](functions-comparison.md#FUNCTIONS-COMPARISON-OP-TABLE) para UUIDs.

Consulte a [Seção 8.12](datatype-uuid.md) para obter detalhes sobre o tipo de dado `uuid` no PostgreSQL.