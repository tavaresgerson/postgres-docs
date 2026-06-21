## F.49. uuid-ossp — um gerador de UUID [#](#UUID-OSSP)

* [F.49.1. Funções `uuid-ossp`](uuid-ossp.md#UUID-OSSP-FUNCTIONS-SECT)
* [F.49.2. Edifício `uuid-ossp`](uuid-ossp.md#UUID-OSSP-BUILDING)
* [F.49.3. Autor](uuid-ossp.md#UUID-OSSP-AUTHOR)

O módulo `uuid-ossp` fornece funções para gerar identificadores universais e únicos (UUIDs) usando um dos vários algoritmos padrão. Também há funções para produzir certas constantes de UUID especiais. Este módulo é necessário apenas para requisitos especiais além do que está disponível no PostgreSQL básico. Veja [Seção 9.14](functions-uuid.md) para formas embutidas de gerar UUIDs.

Este módulo é considerado "confiável", ou seja, pode ser instalado por usuários não superusuários que possuem privilégio `CREATE` no banco de dados atual.

### F.49.1. `uuid-ossp` Funções [#](#UUID-OSSP-FUNCTIONS-SECT)

[Tabela F.35](uuid-ossp.md#UUID-OSSP-FUNCTIONS "Table F.35. Functions for UUID Generation") mostra as funções disponíveis para gerar UUIDs. As normas relevantes ITU-T Rec. X.667, ISO/IEC 9834-8:2005 e [RFC 4122](https://datatracker.ietf.org/doc/html/rfc4122) especificam quatro algoritmos para gerar UUIDs, identificados pelos números de versão 1, 3, 4 e 5. (Não há um algoritmo de versão 2.) Cada um desses algoritmos pode ser adequado para um conjunto diferente de aplicações.

**Tabela F.35. Funções para Geração de UUID**



<table border="1" class="table" summary="Functions for UUID Generation">
 <colgroup>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th class="func_table_entry">
    <p class="func_signature">
     Function
    </p>
    <p>
     Description
    </p>
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      uuid_generate_v1
     </code>
     () →
     <code class="returnvalue">
      uuid
     </code>
    </p>
    <p>
     Generates a version 1 UUID.  This involves the MAC address of the computer and a time stamp.  Note that UUIDs of this kind reveal the identity of the computer that created the identifier and the time at which it did so, which might make it unsuitable for certain security-sensitive applications.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      uuid_generate_v1mc
     </code>
     () →
     <code class="returnvalue">
      uuid
     </code>
    </p>
    <p>
     Generates a version 1 UUID, but uses a random multicast MAC address instead of the real MAC address of the computer.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      uuid_generate_v3
     </code>
     (
     <em class="parameter">
      <code>
       namespace
      </code>
     </em>
     <code class="type">
      uuid
     </code>
     ,
     <em class="parameter">
      <code>
       name
      </code>
     </em>
     <code class="type">
      text
     </code>
     ) →
     <code class="returnvalue">
      uuid
     </code>
    </p>
    <p>
     Generates a version 3 UUID in the given namespace using the specified input name.  The namespace should be one of the special constants produced by the
     <code class="function">
      uuid_ns_*()
     </code>
     functions shown in
     <a class="xref" href="uuid-ossp.md#UUID-OSSP-CONSTANTS" title="Table F.36. Functions Returning UUID Constants">
      Table F.36
     </a>
     .  (It could be any UUID in theory.)  The name is an identifier in the selected namespace.
    </p>
    <p>
     For example:
    </p>
    <pre class="programlisting">
SELECT uuid_generate_v3(uuid_ns_url(), 'http://www.postgresql.org');
</pre>
    <p>
     The name parameter will be MD5-hashed, so the cleartext cannot be derived from the generated UUID. The generation of UUIDs by this method has no random or environment-dependent element and is therefore reproducible.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      uuid_generate_v4
     </code>
     () →
     <code class="returnvalue">
      uuid
     </code>
    </p>
    <p>
     Generates a version 4 UUID, which is derived entirely from random numbers.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      uuid_generate_v5
     </code>
     (
     <em class="parameter">
      <code>
       namespace
      </code>
     </em>
     <code class="type">
      uuid
     </code>
     ,
     <em class="parameter">
      <code>
       name
      </code>
     </em>
     <code class="type">
      text
     </code>
     ) →
     <code class="returnvalue">
      uuid
     </code>
    </p>
    <p>
     Generates a version 5 UUID, which works like a version 3 UUID except that SHA-1 is used as a hashing method.  Version 5 should be preferred over version 3 because SHA-1 is thought to be more secure than MD5.
    </p>
   </td>
  </tr>
 </tbody>
</table>










**Tabela F.36. Funções que retornam constantes UUID**



<table border="1" class="table" summary="Functions Returning UUID Constants">
 <colgroup>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th class="func_table_entry">
    <p class="func_signature">
     Function
    </p>
    <p>
     Description
    </p>
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      uuid_nil
     </code>
     () →
     <code class="returnvalue">
      uuid
     </code>
    </p>
    <p>
     Returns a
     <span class="quote">
      “
      <span class="quote">
       nil
      </span>
      ”
     </span>
     UUID constant, which does not occur as a real UUID.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      uuid_ns_dns
     </code>
     () →
     <code class="returnvalue">
      uuid
     </code>
    </p>
    <p>
     Returns a constant designating the DNS namespace for UUIDs.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      uuid_ns_url
     </code>
     () →
     <code class="returnvalue">
      uuid
     </code>
    </p>
    <p>
     Returns a constant designating the URL namespace for UUIDs.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      uuid_ns_oid
     </code>
     () →
     <code class="returnvalue">
      uuid
     </code>
    </p>
    <p>
     Returns a constant designating the ISO object identifier (OID) namespace for UUIDs.  (This pertains to ASN.1 OIDs, which are unrelated to the OIDs used in
     <span class="productname">
      PostgreSQL
     </span>
     .)
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      uuid_ns_x500
     </code>
     () →
     <code class="returnvalue">
      uuid
     </code>
    </p>
    <p>
     Returns a constant designating the X.500 distinguished name (DN) namespace for UUIDs.
    </p>
   </td>
  </tr>
 </tbody>
</table>







### F.49.2. Edifício `uuid-ossp` [#](#UUID-OSSP-BUILDING)

Historicamente, este módulo dependia da biblioteca OSSP UUID, que é responsável pelo nome do módulo. Embora a biblioteca OSSP ainda possa ser encontrada em <http://www.ossp.org/pkg/lib/uuid/>, ela não é bem mantida e está se tornando cada vez mais difícil de portar para plataformas mais recentes. `uuid-ossp` pode agora ser construído sem a biblioteca OSSP em algumas plataformas. Em FreeBSD e em algumas outras plataformas derivadas do BSD, funções adequadas de criação de UUID estão incluídas na biblioteca central `libc`. Em Linux, macOS e em algumas outras plataformas, funções adequadas estão fornecidas na biblioteca `libuuid`, que originalmente veio do projeto `e2fsprogs` (embora em Linux moderno, ela seja considerada parte de `util-linux-ng`). Ao invocar `configure`, especifique `--with-uuid=bsd` para usar as funções BSD, ou `--with-uuid=e2fs` para usar `e2fsprogs` `libuuid`, ou `--with-uuid=ossp` para usar a biblioteca UUID OSSP. Mais de uma dessas bibliotecas podem estar disponíveis em uma máquina específica, então `configure` não escolhe automaticamente uma.

### F.49.3. Autor [#](#UUID-OSSP-AUTHOR)

Peter Eisentraut `<peter_e@gmx.net>`