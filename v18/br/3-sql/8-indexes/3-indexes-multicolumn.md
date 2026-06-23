## 11.3. Índices de múltiplas colunas [#](#INDEXES-MULTICOLUMN)

Um índice pode ser definido em mais de uma coluna de uma tabela. Por exemplo, se você tem uma tabela com a seguinte forma:

```
CREATE TABLE test2 (
  major int,
  minor int,
  name varchar
);
```

(digamos que você mantenha seu diretório `/dev` em um banco de dados...) e você emite frequentemente consultas como:

```
SELECT name FROM test2 WHERE major = constant AND minor = constant;
```

então, pode ser apropriado definir um índice sobre as colunas `major` e `minor` juntas, por exemplo:

```
CREATE INDEX test2_mm_idx ON test2 (major, minor);
```

Atualmente, apenas os tipos de índices B-tree, GiST, GIN e BRIN suportam índices de coluna com múltiplas chaves. Se pode haver múltiplas colunas de chave, isso é independente de se as colunas `INCLUDE` podem ser adicionadas ao índice. Os índices podem ter até 32 colunas, incluindo as colunas `INCLUDE`. (Esse limite pode ser alterado ao construir o PostgreSQL; veja o arquivo `pg_config_manual.h`).

Um índice B-tree de múltiplas colunas pode ser usado com condições de consulta que envolvem qualquer subconjunto das colunas do índice, mas o índice é mais eficiente quando há restrições nas colunas principais (as mais à esquerda). A regra exata é que as restrições de igualdade nas colunas principais, mais quaisquer restrições de desigualdade na primeira coluna que não tenha uma restrição de igualdade, serão sempre usadas para limitar a parte do índice que é verificada. As restrições nas colunas à direita dessas colunas são verificadas no índice, então elas sempre salvarão visitas à tabela propriamente dita, mas elas não reduzem necessariamente a parte do índice que precisa ser verificada. Se um exame de índice B-tree pode aplicar a otimização de varredura de pular efetivamente, ele aplicará cada restrição de coluna ao navegar pelo índice através de pesquisas repetidas no índice. Isso pode reduzir a parte do índice que precisa ser lida, mesmo que uma ou mais colunas (antes da coluna de índice menos significativa do predicado da consulta) não tenha uma restrição de igualdade convencional. A varredura de pular funciona gerando uma restrição de igualdade dinâmica internamente, que corresponde a cada valor possível em uma coluna de índice (embora apenas dada uma coluna que não tenha uma restrição de igualdade que vem do predicado da consulta, e apenas quando a restrição gerada pode ser usada em conjunto com uma restrição de coluna posterior do predicado da consulta).

Por exemplo, dado um índice em `(x, y)`, e uma condição de consulta em `WHERE y = 7700`, um varredura de índice B-tree pode ser capaz de aplicar a otimização de varredura de salto. Isso geralmente acontece quando o planejador de consulta espera que pesquisas repetidas em `WHERE x = N AND y = 7700` para todos os valores possíveis de `N` (ou para todos os valores em `x` que estão realmente armazenados no índice) seja a abordagem mais rápida possível, dado os índices disponíveis na tabela. Essa abordagem geralmente é tomada apenas quando há tão poucos valores distintos em `x` que o planejador espera que a varredura ignore a maioria do índice (porque a maioria de suas páginas de folha não pode possivelmente conter tuplas relevantes). Se houver muitos valores distintos em `x`, então todo o índice terá que ser varrido, então, na maioria dos casos, o planejador preferirá uma varredura sequencial da tabela em vez de usar o índice.

A otimização do varredura de saltos também pode ser aplicada seletivamente, durante varreduras de árvores B que tenham pelo menos algumas restrições úteis do predicado da consulta. Por exemplo, dado um índice em `(a, b, c)` e uma condição de consulta `WHERE a = 5 AND b >= 42 AND c < 77`, o índice pode ter que ser varrido a partir da primeira entrada com `a` = 5 e `b` = 42 até a última entrada com `a` = 5. As entradas do índice com `c` >= 77 nunca precisarão ser filtradas no nível da tabela, mas pode ser ou não lucrativo ignorá-las dentro do índice. Quando o salto ocorre, a varredura inicia uma nova pesquisa de índice para se reposicionar a partir do final do grupo atual `a` = 5 e `b` = N (ou seja, a partir da posição no índice onde a primeira tupla `a = 5 AND b = N AND c >= 77` aparece), até o início do próximo grupo desse tipo (ou seja, a posição no índice onde a primeira tupla `a = 5 AND b = N + 1` aparece).

Um índice GiST de múltiplas colunas pode ser usado com condições de consulta que envolvem qualquer subconjunto das colunas do índice. As condições em colunas adicionais restringem as entradas devolvidas pelo índice, mas a condição na primeira coluna é a mais importante para determinar quanto do índice precisa ser pesquisado. Um índice GiST será relativamente ineficaz se sua primeira coluna tiver apenas alguns valores distintos, mesmo que haja muitos valores distintos em colunas adicionais.

Um índice GIN de múltiplas colunas pode ser usado com condições de consulta que envolvem qualquer subconjunto das colunas do índice. Ao contrário da árvore B ou GiST, a eficácia da pesquisa do índice é a mesma, independentemente das colunas (ou colunas) do índice que as condições de consulta utilizam.

Um índice BRIN de múltiplas colunas pode ser usado com condições de consulta que envolvem qualquer subconjunto das colunas do índice. Assim como o GIN e ao contrário do B-tree ou GiST, a eficácia da pesquisa do índice é a mesma, independentemente das colunas (ou colunas) do índice que as condições de consulta utilizam. A única razão para ter vários índices BRIN em vez de um índice BRIN de múltiplas colunas em uma única tabela é ter um parâmetro de armazenamento diferente `pages_per_range`.

Claro, cada coluna deve ser usada com operadores apropriados ao tipo de índice; cláusulas que envolvam outros operadores não serão consideradas.

Os índices de múltiplas colunas devem ser usados com parcimônia. Na maioria das situações, um índice em uma única coluna é suficiente e economiza espaço e tempo. É improvável que índices com mais de três colunas sejam úteis, a menos que o uso da tabela seja extremamente estilizado. Veja também [Seção 11.5](indexes-bitmap-scans.md) e [Seção 11.9](indexes-index-only-scans.md) para uma discussão sobre os méritos das diferentes configurações de índice.