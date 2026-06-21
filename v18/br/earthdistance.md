## F.14. distância_terra — calcular distâncias em círculo máximo [#](#EARTHDISTANCE)

* [F.14.1. Distâncias à Terra com base em cubos](earthdistance.md#EARTHDISTANCE-CUBE-BASED)
* [F.14.2. Distâncias à Terra com base em pontos](earthdistance.md#EARTHDISTANCE-POINT-BASED)

O módulo `earthdistance` oferece duas abordagens diferentes para calcular as distâncias em círculo máximo na superfície da Terra. A primeira descrita depende do módulo `cube`. A segunda é baseada no tipo de dados embutido `point`, utilizando longitude e latitude para as coordenadas.

Neste módulo, assume-se que a Terra é perfeitamente esférica. (Se isso for muito impreciso para você, talvez queira consultar o projeto [PostGIS][(https://postgis.net/)].

O módulo `cube` deve ser instalado antes que o `earthdistance` possa ser instalado (embora você possa usar a opção `CASCADE` do `CREATE EXTENSION` para instalar ambos em um comando).

### Atenção

É fortemente recomendado que `earthdistance` e `cube` sejam instalados no mesmo esquema, e que esse esquema seja aquele para o qual o privilégio de CREATE não tenha sido concedido e não será concedido a nenhum usuário não confiável. Caso contrário, há riscos de segurança no momento da instalação se o esquema de `earthdistance` contiver objetos definidos por um usuário hostil. Além disso, ao usar as funções de `earthdistance` após a instalação, todo o caminho de busca deve conter apenas esquemas confiáveis.

### F.14.1. Distâncias à Terra baseadas em cubos [#](#EARTHDISTANCE-CUBE-BASED)

Os dados são armazenados em cubos que são pontos (ambos os cantos são iguais) usando 3 coordenadas que representam a distância x, y e z do centro da Terra. Um [*[domain](glossary.md#GLOSSARY-DOMAIN "Domain")*](glossary.md#GLOSSARY-DOMAIN) `earth` sobre o tipo `cube` é fornecido, que inclui verificações de restrições de que o valor atende a essas restrições e está razoavelmente próximo à superfície real da Terra.

O raio da Terra é obtido a partir da função `earth()`. É dado em metros. Mas, ao alterar essa função, você pode alterar o módulo para usar algumas outras unidades ou para usar um valor diferente do raio que você achar mais apropriado.

Este pacote também tem aplicações em bancos de dados astronômicos. Os astrônomos provavelmente desejam alterar `earth()` para retornar um raio de `180/pi()`, para que as distâncias estejam em graus.

São fornecidas funções para suportar a entrada de latitude e longitude (em graus), para suportar a saída de latitude e longitude, para calcular a distância em círculo máximo entre dois pontos e para especificar facilmente uma caixa de delimitação utilizável para pesquisas de índice.

As funções fornecidas são mostradas na [Tabela F.4][(earthdistance.md#EARTHDISTANCE-CUBE-FUNCTIONS "Table F.4. Cube-Based Earthdistance Functions")].

**Tabela F.4. Funções de distância terrestre baseadas em cubo**



<table border="1" class="table" summary="Cube-Based Earthdistance Functions">
<colgroup>
<col/>
</colgroup>
<thead>
<tr>
<th class="func_table_entry">
<p class="func_signature">Função</p>
<p>Descrição</p>
</th>
</tr>
</thead>
<tbody>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      earth
     </code>()<code class="returnvalue">
      float8
     </code>
</p>
<p>Retorna o raio assumido da Terra.</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      sec_to_gc
     </code>(<code class="type">
      float8
     </code>)<code class="returnvalue">
      float8
     </code>
</p>
<p>Converte a distância normal em linha reta (secante) entre dois pontos na superfície da Terra para a distância em círculo grande entre eles.</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      gc_to_sec
     </code>(<code class="type">
      float8
     </code>)<code class="returnvalue">
      float8
     </code>
</p>
<p>Converte a distância em círculo máximo entre dois pontos na superfície da Terra para a distância normal em linha reta (secante) entre eles.</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      ll_to_earth
     </code>(<code class="type">
      float8
     </code>,<code class="type">
      float8
     </code>)<code class="returnvalue">
      earth
     </code>
</p>
<p>Retorna a localização de um ponto na superfície da Terra, dado sua latitude (argumento 1) e longitude (argumento 2) em graus.</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      latitude
     </code>(<code class="type">
      earth
     </code>)<code class="returnvalue">
      float8
     </code>
</p>
<p>Retorna a latitude em graus de um ponto na superfície da Terra.</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      longitude
     </code>(<code class="type">
      earth
     </code>)<code class="returnvalue">
      float8
     </code>
</p>
<p>Retorna a longitude em graus de um ponto na superfície da Terra.</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      earth_distance
     </code>(<code class="type">
      earth
     </code>,<code class="type">
      earth
     </code>)<code class="returnvalue">
      float8
     </code>
</p>
<p>Retorna a distância em círculo máximo entre dois pontos na superfície da Terra.</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      earth_box
     </code>(<code class="type">
      earth
     </code>,<code class="type">
      float8
     </code>)<code class="returnvalue">
      cube
     </code>
</p>
<p>Retorna uma caixa adequada para uma pesquisa indexada usando o<code class="type">
      cube
     </code>
<code class="literal">
      @&gt;
     </code>operador para pontos dentro de uma distância dada em círculo máximo de uma localização. Alguns pontos nesta caixa estão mais distantes do que a distância especificado em círculo máximo da localização, então uma segunda verificação usando<code class="function">
      earth_distance
     </code>deveriam ser incluídas na consulta.</p>
</td>
</tr>
</tbody>
</table>



### F.14.2. Distâncias terrestres baseadas em pontos [#](#EARTHDISTANCE-POINT-BASED)

A segunda parte do módulo depende da representação de locais na Terra como valores do tipo `point`, na qual o primeiro componente é considerado para representar a longitude em graus, e o segundo componente é considerado para representar a latitude em graus. Os pontos são considerados como (longitude, latitude) e não vice-versa, porque a longitude está mais próxima da ideia intuitiva do eixo x e a latitude do eixo y.

Um único operador é fornecido, mostrado em [Tabela F.5][(earthdistance.md#EARTHDISTANCE-POINT-OPERATORS "Table F.5. Point-Based Earthdistance Operators")].

**Tabela F.5. Operadores de distância terrestre baseados em pontos**



<table border="1" class="table" summary="Point-Based Earthdistance Operators">
<colgroup>
<col/>
</colgroup>
<thead>
<tr>
<th class="func_table_entry">
<p class="func_signature">Operador</p>
<p>Descrição</p>
</th>
</tr>
</thead>
<tbody>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="type">
      point
     </code>
<code class="literal">
      &lt;@&gt;
     </code>
<code class="type">
      point
     </code>→<code class="returnvalue">
      float8
     </code>
</p>
<p>Calcula a distância em milhas estatutárias entre dois pontos na superfície da Terra.</p>
</td>
</tr>
</tbody>
</table>




  

Observe que, ao contrário da parte do módulo baseada no `cube`, as unidades estão conectadas diretamente aqui: alterar a função do `earth()` não afetará os resultados desse operador.

Uma desvantagem da representação de longitude/latitude é que você precisa ter cuidado com as condições de borda perto dos polos e perto de +/- 180 graus de longitude. A representação baseada no `cube` evita essas discontinuidades.