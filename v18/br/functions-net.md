## 9.12. Funções e operadores de endereço de rede [#](#FUNCTIONS-NET)

Os tipos de endereço de rede IP, `cidr` e `inet`, suportam os operadores de comparação habituais mostrados na [Tabela 9.1](functions-comparison.md#FUNCTIONS-COMPARISON-OP-TABLE "Table 9.1. Comparison Operators"), bem como os operadores e funções especializados mostrados na [Tabela 9.39](functions-net.md#CIDR-INET-OPERATORS-TABLE "Table 9.39. IP Address Operators") e [Tabela 9.40](functions-net.md#CIDR-INET-FUNCTIONS-TABLE "Table 9.40. IP Address Functions").

Qualquer valor de `cidr` pode ser convertido para `inet` implicitamente; portanto, os operadores e funções mostrados abaixo que operam em `inet` também funcionam em valores de `cidr`. (Onde existem funções separadas para `inet` e `cidr`, isso ocorre porque o comportamento deve ser diferente para os dois casos.) Além disso, é permitido converter um valor de `inet` para `cidr`. Quando isso é feito, quaisquer bits à direita da máscara são zerados silenciosamente para criar um valor válido de `cidr`.

**Tabela 9.39. Operadores de endereço IP**



<table border="1" class="table" summary="IP Address Operators">
<colgroup>
<col/>
</colgroup>
<thead>
<tr>
<th class="func_table_entry">
<p class="func_signature">Operador</p>
<p>Descrição</p>
<p>Exemplo(s)</p>
</th>
</tr>
</thead>
<tbody>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="type">
      inet
     </code>
<code class="literal">
      &lt;&lt;
     </code>
<code class="type">
      inet
     </code>→<code class="returnvalue">
      boolean
     </code>
</p>
<p>A sub-rede é estritamente contida pela sub-rede? Este operador e os quatro seguintes testam a inclusão da sub-rede. Eles consideram apenas as partes de rede dos dois endereços (ignorando quaisquer bits à direita das máscaras de rede) e determinam se uma rede é idêntica à outra ou uma sub-rede dela.</p>
<p>
<code class="literal">
      inet '192.168.1.5' &lt;&lt; inet '192.168.1/24'
     </code>→<code class="returnvalue">
      t
     </code>
</p>
<p>
<code class="literal">
      inet '192.168.0.5' &lt;&lt; inet '192.168.1/24'
     </code>→<code class="returnvalue">
      f
     </code>
</p>
<p>
<code class="literal">
      inet '192.168.1/24' &lt;&lt; inet '192.168.1/24'
     </code>→<code class="returnvalue">
      f
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="type">
      inet
     </code>
<code class="literal">
      &lt;&lt;=
     </code>
<code class="type">
      inet
     </code>→<code class="returnvalue">
      boolean
     </code>
</p>
<p>A sub-rede está contida pela sub-rede ou é igual à sub-rede?</p>
<p>
<code class="literal">
      inet '192.168.1/24' &lt;&lt;= inet '192.168.1/24'
     </code>→<code class="returnvalue">
      t
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="type">
      inet
     </code>
<code class="literal">
      &gt;&gt;
     </code>
<code class="type">
      inet
     </code>→<code class="returnvalue">
      boolean
     </code>
</p>
<p>A sub-rede contém estritamente a sub-rede?</p>
<p>
<code class="literal">
      inet '192.168.1/24' &gt;&gt; inet '192.168.1.5'
     </code>→<code class="returnvalue">
      t
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="type">
      inet
     </code>
<code class="literal">
      &gt;&gt;=
     </code>
<code class="type">
      inet
     </code>→<code class="returnvalue">
      boolean
     </code>
</p>
<p>Sub-rede contém ou é igual a sub-rede?</p>
<p>
<code class="literal">
      inet '192.168.1/24' &gt;&gt;= inet '192.168.1/24'
     </code>→<code class="returnvalue">
      t
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="type">
      inet
     </code>
<code class="literal">
      &amp;&amp;
     </code>
<code class="type">
      inet
     </code>→<code class="returnvalue">
      boolean
     </code>
</p>
<p>Uma das sub-redes contém ou é igual à outra?</p>
<p>
<code class="literal">
      inet '192.168.1/24' &amp;&amp; inet '192.168.1.80/28'
     </code>→<code class="returnvalue">
      t
     </code>
</p>
<p>
<code class="literal">
      inet '192.168.1/24' &amp;&amp; inet '192.168.2.0/28'
     </code>→<code class="returnvalue">
      f
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="literal">
      ~
     </code>
<code class="type">
      inet
     </code>→<code class="returnvalue">
      inet
     </code>
</p>
<p>Calcula a operação de NÃO bit a bit.</p>
<p>
<code class="literal">
      ~ inet '192.168.1.6'
     </code>→<code class="returnvalue">
      63.87.254.249
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="type">
      inet
     </code>
<code class="literal">
      &amp;
     </code>
<code class="type">
      inet
     </code>→<code class="returnvalue">
      inet
     </code>
</p>
<p>Calcula a operação AND bit a bit.</p>
<p>
<code class="literal">
      inet '192.168.1.6' &amp; inet '0.0.0.255'
     </code>→<code class="returnvalue">
      0.0.0.6
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="type">
      inet
     </code>
<code class="literal">
      |
     </code>
<code class="type">
      inet
     </code>→<code class="returnvalue">
      inet
     </code>
</p>
<p>Calcula a OR bit a bit.</p>
<p>
<code class="literal">
      inet '192.168.1.6' | inet '0.0.0.255'
     </code>→<code class="returnvalue">
      192.168.1.255
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="type">
      inet
     </code>
<code class="literal">
      +
     </code>
<code class="type">
      bigint
     </code>→<code class="returnvalue">
      inet
     </code>
</p>
<p>Adiciona um deslocamento a um endereço.</p>
<p>
<code class="literal">
      inet '192.168.1.6' + 25
     </code>→<code class="returnvalue">
      192.168.1.31
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="type">
      bigint
     </code>
<code class="literal">
      +
     </code>
<code class="type">
      inet
     </code>→<code class="returnvalue">
      inet
     </code>
</p>
<p>Adiciona um deslocamento a um endereço.</p>
<p>
<code class="literal">
      200 + inet '::ffff:fff0:1'
     </code>→<code class="returnvalue">
      ::ffff:255.240.0.201
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="type">
      inet
     </code>
<code class="literal">
      -
     </code>
<code class="type">
      bigint
     </code>→<code class="returnvalue">
      inet
     </code>
</p>
<p>Subtrai um deslocamento de um endereço.</p>
<p>
<code class="literal">
      inet '192.168.1.43' - 36
     </code>→<code class="returnvalue">
      192.168.1.7
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="type">
      inet
     </code>
<code class="literal">
      -
     </code>
<code class="type">
      inet
     </code>→<code class="returnvalue">
      bigint
     </code>
</p>
<p>Calcula a diferença entre dois endereços.</p>
<p>
<code class="literal">
      inet '192.168.1.43' - inet '192.168.1.19'
     </code>→<code class="returnvalue">
      24
     </code>
</p>
<p>
<code class="literal">
      inet '::1' - inet '::ffff:1'
     </code>→<code class="returnvalue">
      -4294901760
     </code>
</p>
</td>
</tr>
</tbody>
</table>




  

**Tabela 9.40. Funções de endereço IP**



<table border="1" class="table" summary="IP Address Functions">
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
<p>
     Example(s)
    </p>
</th>
</tr>
</thead>
<tbody>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      abbrev
     </code>
     (
     <code class="type">
      inet
     </code>
     )
        →
     <code class="returnvalue">
      text
     </code>
</p>
<p>
     Creates an abbreviated display format as text. (The result is the same as the
     <code class="type">
      inet
     </code>
     output function produces; it is
     <span class="quote">
      “
      <span class="quote">
       abbreviated
      </span>
      ”
     </span>
     only in comparison to the result of an explicit cast to
     <code class="type">
      text
     </code>
     , which for historical reasons will never suppress the netmask part.)
    </p>
<p>
<code class="literal">
      abbrev(inet '10.1.0.0/32')
     </code>
     →
     <code class="returnvalue">
      10.1.0.0
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      abbrev
     </code>
     (
     <code class="type">
      cidr
     </code>
     )
        →
     <code class="returnvalue">
      text
     </code>
</p>
<p>
     Creates an abbreviated display format as text. (The abbreviation consists of dropping all-zero octets to the right of the netmask; more examples are in
     <a class="xref" href="datatype-net-types.md#DATATYPE-NET-CIDR-TABLE" title="Table 8.22. cidr Type Input Examples">
      Table 8.22
     </a>
     .)
    </p>
<p>
<code class="literal">
      abbrev(cidr '10.1.0.0/16')
     </code>
     →
     <code class="returnvalue">
      10.1/16
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      broadcast
     </code>
     (
     <code class="type">
      inet
     </code>
     )
        →
     <code class="returnvalue">
      inet
     </code>
</p>
<p>
     Computes the broadcast address for the address's network.
    </p>
<p>
<code class="literal">
      broadcast(inet '192.168.1.5/24')
     </code>
     →
     <code class="returnvalue">
      192.168.1.255/24
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      family
     </code>
     (
     <code class="type">
      inet
     </code>
     )
        →
     <code class="returnvalue">
      integer
     </code>
</p>
<p>
     Returns the address's family:
     <code class="literal">
      4
     </code>
     for IPv4,
     <code class="literal">
      6
     </code>
     for IPv6.
    </p>
<p>
<code class="literal">
      family(inet '::1')
     </code>
     →
     <code class="returnvalue">
      6
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      host
     </code>
     (
     <code class="type">
      inet
     </code>
     )
        →
     <code class="returnvalue">
      text
     </code>
</p>
<p>
     Returns the IP address as text, ignoring the netmask.
    </p>
<p>
<code class="literal">
      host(inet '192.168.1.0/24')
     </code>
     →
     <code class="returnvalue">
      192.168.1.0
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      hostmask
     </code>
     (
     <code class="type">
      inet
     </code>
     )
        →
     <code class="returnvalue">
      inet
     </code>
</p>
<p>
     Computes the host mask for the address's network.
    </p>
<p>
<code class="literal">
      hostmask(inet '192.168.23.20/30')
     </code>
     →
     <code class="returnvalue">
      0.0.0.3
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      inet_merge
     </code>
     (
     <code class="type">
      inet
     </code>
     ,
     <code class="type">
      inet
     </code>
     )
        →
     <code class="returnvalue">
      cidr
     </code>
</p>
<p>
     Computes the smallest network that includes both of the given networks.
    </p>
<p>
<code class="literal">
      inet_merge(inet '192.168.1.5/24', inet '192.168.2.5/24')
     </code>
     →
     <code class="returnvalue">
      192.168.0.0/22
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      inet_same_family
     </code>
     (
     <code class="type">
      inet
     </code>
     ,
     <code class="type">
      inet
     </code>
     )
        →
     <code class="returnvalue">
      boolean
     </code>
</p>
<p>
     Tests whether the addresses belong to the same IP family.
    </p>
<p>
<code class="literal">
      inet_same_family(inet '192.168.1.5/24', inet '::1')
     </code>
     →
     <code class="returnvalue">
      f
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      masklen
     </code>
     (
     <code class="type">
      inet
     </code>
     )
        →
     <code class="returnvalue">
      integer
     </code>
</p>
<p>
     Returns the netmask length in bits.
    </p>
<p>
<code class="literal">
      masklen(inet '192.168.1.5/24')
     </code>
     →
     <code class="returnvalue">
      24
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      netmask
     </code>
     (
     <code class="type">
      inet
     </code>
     )
        →
     <code class="returnvalue">
      inet
     </code>
</p>
<p>
     Computes the network mask for the address's network.
    </p>
<p>
<code class="literal">
      netmask(inet '192.168.1.5/24')
     </code>
     →
     <code class="returnvalue">
      255.255.255.0
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      network
     </code>
     (
     <code class="type">
      inet
     </code>
     )
        →
     <code class="returnvalue">
      cidr
     </code>
</p>
<p>
     Returns the network part of the address, zeroing out whatever is to the right of the netmask. (This is equivalent to casting the value to
     <code class="type">
      cidr
     </code>
     .)
    </p>
<p>
<code class="literal">
      network(inet '192.168.1.5/24')
     </code>
     →
     <code class="returnvalue">
      192.168.1.0/24
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      set_masklen
     </code>
     (
     <code class="type">
      inet
     </code>
     ,
     <code class="type">
      integer
     </code>
     )
        →
     <code class="returnvalue">
      inet
     </code>
</p>
<p>
     Sets the netmask length for an
     <code class="type">
      inet
     </code>
     value. The address part does not change.
    </p>
<p>
<code class="literal">
      set_masklen(inet '192.168.1.5/24', 16)
     </code>
     →
     <code class="returnvalue">
      192.168.1.5/16
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      set_masklen
     </code>
     (
     <code class="type">
      cidr
     </code>
     ,
     <code class="type">
      integer
     </code>
     )
        →
     <code class="returnvalue">
      cidr
     </code>
</p>
<p>
     Sets the netmask length for a
     <code class="type">
      cidr
     </code>
     value. Address bits to the right of the new netmask are set to zero.
    </p>
<p>
<code class="literal">
      set_masklen(cidr '192.168.1.0/24', 16)
     </code>
     →
     <code class="returnvalue">
      192.168.0.0/16
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      text
     </code>
     (
     <code class="type">
      inet
     </code>
     )
        →
     <code class="returnvalue">
      text
     </code>
</p>
<p>
     Returns the unabbreviated IP address and netmask length as text. (This has the same result as an explicit cast to
     <code class="type">
      text
     </code>
     .)
    </p>
<p>
<code class="literal">
      text(inet '192.168.1.5')
     </code>
     →
     <code class="returnvalue">
      192.168.1.5/32
     </code>
</p>
</td>
</tr>
</tbody>
</table>




  

### DICA

As funções `abbrev`, `host` e `text` são, principalmente, destinadas a oferecer formatos de exibição alternativos para endereços IP.

Os tipos de endereço MAC `macaddr` e `macaddr8` suportam os operadores de comparação comuns mostrados na [Tabela 9.1] (functions-comparison.md#FUNCTIONS-COMPARISON-OP-TABLE "Table 9.1. Comparison Operators"), bem como as funções especializadas mostradas na [Tabela 9.41] (functions-net.md#MACADDR-FUNCTIONS-TABLE "Table 9.41. MAC Address Functions"). Além disso, eles suportam os operadores lógicos bit a bit `~`, `&` e `|` (NOT, AND e OR), assim como mostrado acima para endereços IP.

**Tabela 9.41. Funções de endereço MAC**



<table border="1" class="table" summary="MAC Address Functions">
<colgroup>
<col/>
</colgroup>
<thead>
<tr>
<th class="func_table_entry">
<p class="func_signature">Função</p>
<p>Descrição</p>
<p>Exemplo(s)</p>
</th>
</tr>
</thead>
<tbody>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      trunc
     </code>(<code class="type">
      macaddr
     </code>)<code class="returnvalue">
      macaddr
     </code>
</p>
<p>Define os últimos 3 bytes do endereço como zero. O prefixo restante pode ser associado a um fabricante específico (usando dados não incluídos na<span class="productname">PostgreSQL</span>
     ).
    </p>
<p>
<code class="literal">
      trunc(macaddr '12:34:56:78:90:ab')
     </code>→<code class="returnvalue">
      12:34:56:00:00:00
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      trunc
     </code>(<code class="type">
      macaddr8
     </code>)<code class="returnvalue">
      macaddr8
     </code>
</p>
<p>Define os últimos 5 bytes do endereço como zero. O prefixo restante pode ser associado a um fabricante específico (usando dados não incluídos na<span class="productname">PostgreSQL</span>
     ).
    </p>
<p>
<code class="literal">
      trunc(macaddr8 '12:34:56:78:90:ab:cd:ef')
     </code>→<code class="returnvalue">
      12:34:56:00:00:00:00:00
     </code>
</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      macaddr8_set7bit
     </code>(<code class="type">
      macaddr8
     </code>)<code class="returnvalue">
      macaddr8
     </code>
</p>
<p>Define o 7º bit do endereço como um, criando o que é conhecido como EUI-64 modificada, para inclusão em um endereço IPv6.</p>
<p>
<code class="literal">
      macaddr8_set7bit(macaddr8 '00:34:56:ab:cd:ef')
     </code>→<code class="returnvalue">
      02:34:56:ff:fe:ab:cd:ef
     </code>
</p>
</td>
</tr>
</tbody>
</table>

