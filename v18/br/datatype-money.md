## 8.2. Tipos Monetários [#](#DATATYPE-MONEY)

O tipo `money` armazena um valor monetário com precisão fracionária fixa; veja [Tabela 8.3][(datatype-money.md#DATATYPE-MONEY-TABLE "Table 8.3. Monetary Types")]. A precisão fracionária é determinada pelo ajuste [lc_monetary][(runtime-config-client.md#GUC-LC-MONETARY)] do banco de dados. A faixa mostrada na tabela assume que há duas dígitos fracionários. A entrada é aceita em uma variedade de formatos, incluindo literais inteiros e de ponto flutuante, bem como formatação típica de moeda, como `'$1,000.00'`. A saída geralmente é na forma do último, mas depende do local.

**Tabela 8.3. Tipos Monetários**



<table border="1" class="table" summary="Monetary Types">
<colgroup>
<col class="col1"/>
<col class="col2"/>
<col class="col3"/>
<col class="col4"/>
</colgroup>
<thead>
<tr>
<th>
    Name
   </th>
<th>
    Storage Size
   </th>
<th>
    Description
   </th>
<th>
    Range
   </th>
</tr>
</thead>
<tbody>
<tr>
<td>
<code class="type">
     money
    </code>
</td>
<td>
    8 bytes
   </td>
<td>
    currency amount
   </td>
<td>
    -92233720368547758.08 to +92233720368547758.07
   </td>
</tr>
</tbody>
</table>




  

Como a saída deste tipo de dados é sensível ao local, pode não funcionar carregar os dados `money` em um banco de dados que tenha um conjunto diferente de `lc_monetary`. Para evitar problemas, antes de restaurar um dump em um novo banco de dados, certifique-se de que `lc_monetary` tenha o mesmo valor ou um valor equivalente ao do banco de dados que foi exportado.

Os valores dos tipos de dados `numeric`, `int` e `bigint` podem ser convertidos para `money`. A conversão dos tipos de dados `real` e `double precision` pode ser feita por conversão para `numeric` primeiro, por exemplo:

```
SELECT '12.34'::float8::numeric::money;
```

No entanto, isso não é recomendado. Números em ponto flutuante não devem ser usados para manipular dinheiro devido ao potencial de erros de arredondamento.

Um valor de `money` pode ser convertido para `numeric` sem perda de precisão. A conversão para outros tipos pode potencialmente perder precisão, e também deve ser feita em duas etapas:

```
SELECT '52093.89'::money::numeric::float8;
```

A divisão de um valor `money` por um valor inteiro é realizada com o truncamento da parte fracionária em direção a zero. Para obter um resultado arredondado, divida por um valor de ponto flutuante ou faça a conversão do valor `money` para `numeric` antes de dividir e, posteriormente, de volta para `money`. (Esta última opção é preferível para evitar o risco de perda de precisão.) Quando um valor `money` é dividido por outro valor `money`, o resultado é `double precision` (ou seja, um número puro, não dinheiro); as unidades de moeda se cancelam mutuamente na divisão.