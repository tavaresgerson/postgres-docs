## 8.9. Tipos de Endereços de Rede [#](#DATATYPE-NET-TYPES)

* [8.9.1. `inet`](datatype-net-types.md#DATATYPE-INET)
* [8.9.2. `cidr`](datatype-net-types.md#DATATYPE-CIDR)
* [8.9.3. `inet` vs. `cidr`](datatype-net-types.md#DATATYPE-INET-VS-CIDR)
* [8.9.4. `macaddr`](datatype-net-types.md#DATATYPE-MACADDR)
* [8.9.5. `macaddr8`](datatype-net-types.md#DATATYPE-MACADDR8)

O PostgreSQL oferece tipos de dados para armazenar endereços IPv4, IPv6 e MAC, conforme mostrado na [Tabela 8.21] ([(datatype-net-types.md#DATATYPE-NET-TYPES-TABLE "Table 8.21. Network Address Types")]). É melhor usar esses tipos em vez de tipos de texto simples para armazenar endereços de rede, porque esses tipos oferecem verificação de erro de entrada e operadores e funções especializados (veja [Seção 9.12] ([(functions-net.md "9.12. Network Address Functions and Operators")]).

**Tabela 8.21. Tipos de Endereços de Rede**



<table border="1" class="table" summary="Network Address Types">
<colgroup>
<col class="col1"/>
<col class="col2"/>
<col class="col3"/>
</colgroup>
<thead>
<tr>
<th>
    Name
   </th>
<th>Tamanho de armazenamento</th>
<th>Descrição</th>
</tr>
</thead>
<tbody>
<tr>
<td>
<code class="type">
     cidr
    </code>
</td>
<td>7 ou 19 bytes</td>
<td>Redes IPv4 e IPv6</td>
</tr>
<tr>
<td>
<code class="type">
     inet
    </code>
</td>
<td>7 ou 19 bytes</td>
<td>Hospedeiros e redes IPv4 e IPv6</td>
</tr>
<tr>
<td>
<code class="type">
     macaddr
    </code>
</td>
<td>6 bytes</td>
<td>Endereços MAC</td>
</tr>
<tr>
<td>
<code class="type">
     macaddr8
    </code>
</td>
<td>8 bytes</td>
<td>Endereços MAC (formato EUI-64)</td>
</tr>
</tbody>
</table>




  

Ao classificar os tipos de dados `inet` ou `cidr`, as endereços IPv4 serão sempre classificados antes das endereços IPv6, incluindo endereços IPv4 encapsulados ou mapeados para endereços IPv6, como ::10.2.3.4 ou ::ffff:10.4.3.2.

### 8.9.1. `inet` [#](#DATATYPE-INET)

O tipo `inet` contém um endereço de host IPv4 ou IPv6, e opcionalmente sua sub-rede, tudo em um único campo. A sub-rede é representada pelo número de bits de endereço de rede presentes no endereço de host (a “máscara de rede”). Se a máscara de rede for 32 e o endereço for IPv4, então o valor não indica uma sub-rede, apenas um único host. No IPv6, o comprimento do endereço é de 128 bits, então 128 bits especificam um endereço de host único. Note que, se você deseja aceitar apenas redes, você deve usar o tipo `cidr` em vez de `inet`.

O formato de entrada para este tipo é *`address/y`* onde *`address`* é uma endereço IPv4 ou IPv6 e *`y`* é o número de bits na máscara de rede. Se a parte *`/y`* for omitida, a máscara de rede é considerada 32 para IPv4 ou 128 para IPv6, portanto, o valor representa apenas um único host. Na tela, a parte *`/y`* é suprimida se a máscara de rede especificar um único host.

### 8.9.2. `cidr` [#](#DATATYPE-CIDR)

O tipo `cidr` contém uma especificação de rede IPv4 ou IPv6. Os formatos de entrada e saída seguem as convenções da Classless Internet Domain Routing. O formato para especificar redes é *`address/y`*, onde *`address`* é o endereço mais baixo da rede representado como uma endereço IPv4 ou IPv6, e *`y`* é o número de bits na máscara de rede. Se *`y`* for omitido, ele será calculado usando suposições do sistema de numeração de redes mais antigas, exceto que será grande o suficiente para incluir todos os octetos escritos na entrada. É um erro especificar um endereço de rede que tem bits definidos à direita da máscara de rede especificada.

[Tabela 8.22](datatype-net-types.md#DATATYPE-NET-CIDR-TABLE "Table 8.22. cidr Type Input Examples") mostra alguns exemplos.

**Tabela 8.22. Exemplos de entrada de tipo `cidr`**



<table border="1" class="table" summary="cidr Type Input Examples">
<colgroup>
<col/>
<col/>
<col/>
</colgroup>
<thead>
<tr>
<th>
<code class="type">
     cidr
    </code>
    Input
   </th>
<th>
<code class="type">
     cidr
    </code>
    Output
   </th>
<th>
<code class="literal">
<code class="function">
      abbrev(
      <code class="type">
       cidr
      </code>
      )
     </code>
</code>
</th>
</tr>
</thead>
<tbody>
<tr>
<td>
    192.168.100.128/25
   </td>
<td>
    192.168.100.128/25
   </td>
<td>
    192.168.100.128/25
   </td>
</tr>
<tr>
<td>
    192.168/24
   </td>
<td>
    192.168.0.0/24
   </td>
<td>
    192.168.0/24
   </td>
</tr>
<tr>
<td>
    192.168/25
   </td>
<td>
    192.168.0.0/25
   </td>
<td>
    192.168.0.0/25
   </td>
</tr>
<tr>
<td>
    192.168.1
   </td>
<td>
    192.168.1.0/24
   </td>
<td>
    192.168.1/24
   </td>
</tr>
<tr>
<td>
    192.168
   </td>
<td>
    192.168.0.0/24
   </td>
<td>
    192.168.0/24
   </td>
</tr>
<tr>
<td>
    128.1
   </td>
<td>
    128.1.0.0/16
   </td>
<td>
    128.1/16
   </td>
</tr>
<tr>
<td>
    128
   </td>
<td>
    128.0.0.0/16
   </td>
<td>
    128.0/16
   </td>
</tr>
<tr>
<td>
    128.1.2
   </td>
<td>
    128.1.2.0/24
   </td>
<td>
    128.1.2/24
   </td>
</tr>
<tr>
<td>
    10.1.2
   </td>
<td>
    10.1.2.0/24
   </td>
<td>
    10.1.2/24
   </td>
</tr>
<tr>
<td>
    10.1
   </td>
<td>
    10.1.0.0/16
   </td>
<td>
    10.1/16
   </td>
</tr>
<tr>
<td>
    10
   </td>
<td>
    10.0.0.0/8
   </td>
<td>
    10/8
   </td>
</tr>
<tr>
<td>
    10.1.2.3/32
   </td>
<td>
    10.1.2.3/32
   </td>
<td>
    10.1.2.3/32
   </td>
</tr>
<tr>
<td>
    2001:4f8:3:ba::/64
   </td>
<td>
    2001:4f8:3:ba::/64
   </td>
<td>
    2001:4f8:3:ba/64
   </td>
</tr>
<tr>
<td>
    2001:4f8:3:ba:​2e0:81ff:fe22:d1f1/128
   </td>
<td>
    2001:4f8:3:ba:​2e0:81ff:fe22:d1f1/128
   </td>
<td>
    2001:4f8:3:ba:​2e0:81ff:fe22:d1f1/128
   </td>
</tr>
<tr>
<td>
    ::ffff:1.2.3.0/120
   </td>
<td>
    ::ffff:1.2.3.0/120
   </td>
<td>
    ::ffff:1.2.3/120
   </td>
</tr>
<tr>
<td>
    ::ffff:1.2.3.0/128
   </td>
<td>
    ::ffff:1.2.3.0/128
   </td>
<td>
    ::ffff:1.2.3.0/128
   </td>
</tr>
</tbody>
</table>



### 8.9.3. `inet` vs. `cidr` [#](#DATATYPE-INET-VS-CIDR)

A diferença essencial entre os tipos de dados `inet` e `cidr` é que o `inet` aceita valores com bits não nulos à direita da máscara de rede, enquanto o `cidr` não. Por exemplo, o `192.168.0.1/24` é válido para `inet`, mas não para `cidr`.

### DICA

Se você não gosta do formato de saída para os valores de `inet` ou `cidr`, tente as funções `host`, `text` e `abbrev`.

### 8.9.4. `macaddr` [#](#DATATYPE-MACADDR)

O tipo `macaddr` armazena endereços MAC, conhecidos, por exemplo, dos endereços de hardware dos cartões Ethernet (embora os endereços MAC sejam usados para outros propósitos também). A entrada é aceita nos seguintes formatos:



<table border="0" class="simplelist" summary="Simple list">
<tr>
<td>
<code class="literal">
    '08:00:2b:01:02:03'
   </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
    '08-00-2b-01-02-03'
   </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
    '08002b:010203'
   </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
    '08002b-010203'
   </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
    '0800.2b01.0203'
   </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
    '0800-2b01-0203'
   </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
    '08002b010203'
   </code>
</td>
</tr>
</table>



Esses exemplos especificam todos o mesmo endereço. Maiúsculas e minúsculas são aceitas para os dígitos `a` até `f`. A saída é sempre na primeira das formas mostradas.

O Padrão IEEE 802-2001 especifica a segunda forma mostrada (com hífens) como a forma canônica para endereços MAC, e especifica a primeira forma (com colchetes) como usada com notação de bits invertidos, MSB-first, de modo que 08-00-2b-01-02-03 = 10:00:D4:80:40:C0. Essa convenção é amplamente ignorada atualmente, e é relevante apenas para protocolos de rede obsoletos (como Token Ring). O PostgreSQL não faz nenhuma disposição para inversão de bits; todos os formatos aceitos usam a ordem canônica LSB.

Os cinco formatos de entrada restantes não fazem parte de nenhum padrão.

### 8.9.5. `macaddr8` [#](#DATATYPE-MACADDR8)

O tipo `macaddr8` armazena endereços MAC no formato EUI-64, conhecido, por exemplo, dos endereços de hardware de cartões Ethernet (embora os endereços MAC sejam usados para outros propósitos também). Este tipo pode aceitar endereços MAC de comprimento de 6 e 8 bytes e os armazena no formato de comprimento de 8 bytes. Os endereços MAC fornecidos no formato de 6 bytes serão armazenados no formato de comprimento de 8 bytes com os 4º e 5º bytes definidos como FF e FE, respectivamente. Observe que o IPv6 usa um formato EUI-64 modificado, onde o 7º bit deve ser definido como um após a conversão do EUI-48. A função `macaddr8_set7bit` é fornecida para fazer essa mudança. De maneira geral, qualquer entrada que seja composta por pares de algarismos hex (em limites de byte), opcionalmente separados consistentemente por um dos `':'`, `'-'` ou `'.'`, é aceita. O número de algarismos hex deve ser de 16 (8 bytes) ou 12 (6 bytes). Espaços em branco no início e no fim são ignorados. Os seguintes são exemplos de formatos de entrada que são aceitos:



<table border="0" class="simplelist" summary="Simple list">
<tr>
<td>
<code class="literal">
    '08:00:2b:01:02:03:04:05'
   </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
    '08-00-2b-01-02-03-04-05'
   </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
    '08002b:0102030405'
   </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
    '08002b-0102030405'
   </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
    '0800.2b01.0203.0405'
   </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
    '0800-2b01-0203-0405'
   </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
    '08002b01:02030405'
   </code>
</td>
</tr>
<tr>
<td>
<code class="literal">
    '08002b0102030405'
   </code>
</td>
</tr>
</table>



Esses exemplos especificam todos o mesmo endereço. Maiúsculas e minúsculas são aceitas para os dígitos `a` até `f`. A saída é sempre na primeira das formas mostradas.

Os seis últimos formatos de entrada mostrados acima não fazem parte de nenhum padrão.

Para converter um endereço MAC tradicional de 48 bits no formato EUI-48 para o formato modificado EUI-64, a ser incluído como a parte do host de um endereço IPv6, use `macaddr8_set7bit` como mostrado:

```
SELECT macaddr8_set7bit('08:00:2b:01:02:03');

    macaddr8_set7bit
-------------------------
 0a:00:2b:ff:fe:01:02:03
(1 row)
```
