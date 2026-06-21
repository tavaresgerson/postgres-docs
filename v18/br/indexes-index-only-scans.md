## 11.9. Análises com base em índices e cobertura de índices [#](#INDEXES-INDEX-ONLY-SCANS)

Todos os índices no PostgreSQL são índices *secundários*, o que significa que cada índice é armazenado separadamente da área principal de dados da tabela (que é chamada de *heap* da tabela na terminologia do PostgreSQL). Isso significa que, em um escândio de índice comum, cada recuperação de linha requer a busca de dados tanto do índice quanto do heap. Além disso, embora as entradas do índice que correspondem a uma condição `WHERE` indexável geralmente estejam próximas umas das outras no índice, as linhas da tabela que elas referenciam podem estar em qualquer lugar do heap. A parte de acesso ao heap de um escândio de índice, portanto, envolve um monte de acesso aleatório ao heap, o que pode ser lento, particularmente em mídia rotativa tradicional. (Como descrito em [Seção 11.5] (indexes-bitmap-scans.md "11.5. Combining Multiple Indexes"), as varreduras de bitmap tentam aliviar esse custo fazendo os acessos ao heap em ordem ordenada, mas isso não vai tão longe.)

Para resolver esse problema de desempenho, o PostgreSQL suporta *escaneamentos apenas com índice*, que podem responder a consultas a partir de um índice sozinho, sem qualquer acesso ao heap. A ideia básica é retornar valores diretamente de cada entrada do índice, em vez de consultar a entrada associada ao heap. Existem duas restrições fundamentais sobre quando esse método pode ser usado:

1. O tipo de índice deve suportar varreduras apenas de índice. As árvores B sempre o fazem. Os índices GiST e SP-GiST suportam varreduras apenas de índice para algumas classes de operadores, mas não para outras. Outros tipos de índice não têm suporte. O requisito subjacente é que o índice deve armazenar fisicamente, ou pelo menos ser capaz de reconstruir, o valor original dos dados para cada entrada do índice. Como exemplo contrário, os índices GIN não podem suportar varreduras apenas de índice porque cada entrada do índice geralmente contém apenas parte do valor original dos dados.
2. A consulta deve referenciar apenas as colunas armazenadas no índice. Por exemplo, dado um índice sobre as colunas `x` e `y` de uma tabela que também tem uma coluna `z`, essas consultas poderiam usar varreduras apenas de índice:

   ```
   SELECT x, y FROM tab WHERE x = 'key';
   SELECT x FROM tab WHERE x = 'key' AND y < 42;
   ```

mas essas consultas não conseguiram:

   ```
   SELECT x, z FROM tab WHERE x = 'key';
   SELECT x FROM tab WHERE x = 'key' AND z < 42;
   ```

(Os índices de expressão e os índices parciais complicam essa regra, conforme discutido abaixo.)

Se esses dois requisitos fundamentais forem atendidos, então todos os valores de dados exigidos pela consulta estarão disponíveis no índice, portanto, uma varredura apenas com índice é fisicamente possível. Mas há um requisito adicional para qualquer varredura de tabela no PostgreSQL: ele deve verificar se cada linha recuperada é “visível” ao snapshot MVCC da consulta, conforme discutido em [Capítulo 13][(mvcc.md "Chapter 13. Concurrency Control")]. As informações de visibilidade não são armazenadas em entradas de índice, apenas em entradas de heap; portanto, à primeira vista, pareceria que cada recuperação de linha exigiria, de qualquer forma, um acesso ao heap. E isso é de fato o caso, se a linha da tabela tiver sido modificada recentemente. No entanto, para dados que raramente são alterados, há uma maneira de contornar esse problema. O PostgreSQL rastreia, para cada página em um heap de uma tabela, se todas as linhas armazenadas nessa página são antigas o suficiente para serem visíveis para todas as transações atuais e futuras. Essas informações são armazenadas em um bit no *mapa de visibilidade* da tabela. Uma varredura apenas com índice, após encontrar uma entrada de índice candidato, verifica o bit do mapa de visibilidade para a página de heap correspondente. Se estiver definido, a linha é conhecida como visível e, portanto, os dados podem ser retornados sem mais trabalho. Se não estiver definido, a entrada de heap deve ser visitada para descobrir se é visível, então não há vantagem de desempenho em relação a uma varredura padrão de índice. Mesmo no caso bem-sucedido, essa abordagem troca acessos ao mapa de visibilidade por acessos ao heap; mas, como o mapa de visibilidade é quatro ordens de magnitude menor que o heap que descreve, é necessário muito menos I/O físico para acessá-lo. Na maioria das situações, o mapa de visibilidade permanece cacheado na memória o tempo todo.

Em suma, embora uma varredura apenas com índice seja possível, dado os dois requisitos fundamentais, será uma vitória apenas se uma fração significativa das páginas do heap da tabela tiver seus bits de mapa visíveis definidos. Mas as tabelas nas quais uma grande fração das linhas é inalterável são comuns o suficiente para tornar esse tipo de varredura muito útil na prática.

Para fazer uso eficaz da função de varredura apenas com índice, você pode optar por criar um *índice coberto*, que é um índice projetado especificamente para incluir as colunas necessárias para um tipo particular de consulta que você executa com frequência. Como as consultas geralmente precisam recuperar mais colunas do que apenas as que elas pesquisam, o PostgreSQL permite que você crie um índice em que algumas colunas são apenas "carga" e não fazem parte da chave de pesquisa. Isso é feito adicionando uma cláusula `INCLUDE` listando as colunas extras. Por exemplo, se você comumente executa consultas como

```
SELECT y FROM tab WHERE x = 'key';
```

a abordagem tradicional para acelerar essas consultas seria criar um índice apenas em `x`. No entanto, um índice definido como

```
CREATE INDEX tab_x_y ON tab(x) INCLUDE (y);
```

poderia lidar com essas consultas como varreduras apenas de índice, porque `y` pode ser obtido do índice sem visitar o heap.

Como a coluna `y` não faz parte da chave de pesquisa do índice, ela não precisa ser de um tipo de dados que o índice possa manipular; ela é apenas armazenada no índice e não é interpretada pela máquina do índice. Além disso, se o índice for um índice único, ou seja

```
CREATE UNIQUE INDEX tab_x_y ON tab(x) INCLUDE (y);
```

A condição de unicidade se aplica apenas à coluna `x`, e não à combinação de `x` e `y`. (Uma cláusula `INCLUDE` também pode ser escrita nas restrições `UNIQUE` e `PRIMARY KEY`, fornecendo sintaxe alternativa para configurar um índice assim.)

É prudente ser conservador ao adicionar colunas de carga não-chave a um índice, especialmente colunas largas. Se um tupla de índice exceder o tamanho máximo permitido para o tipo de índice, a inserção de dados falhará. Em qualquer caso, as colunas não-chave duplicam os dados da tabela do índice e aumentam o tamanho do índice, o que pode retardar as pesquisas. E lembre-se de que não há muito sentido em incluir colunas de carga em um índice, a menos que a tabela mude lentamente o suficiente para que uma varredura apenas com índice provavelmente não precise acessar o heap. Se a tupla do heap deve ser visitada de qualquer maneira, não custa nada obter o valor da coluna de lá. Outra restrição é que as expressões não são atualmente suportadas como colunas incluídas, e que apenas os índices B-tree, GiST e SP-GiST atualmente suportam colunas incluídas.

Antes de o PostgreSQL ter a funcionalidade `INCLUDE`, as pessoas às vezes criavam índices de cobertura escrevendo as colunas de carga como colunas de índice comuns, ou seja, escrevendo

```
CREATE INDEX tab_x_y ON tab(x, y);
```

embora não tenham a intenção de usar `y` como parte de uma cláusula `WHERE`. Isso funciona bem, desde que as colunas extras sejam colunas finais; torná-las colunas iniciais é imprudente pelas razões explicadas na [Seção 11.3](indexes-multicolumn.md "11.3. Multicolumn Indexes"). No entanto, esse método não suporta o caso em que você deseja que o índice imponha a unicidade na(s) coluna(s) chave.

*A quebra de sufixo* sempre remove colunas não-chave dos níveis superiores do B-Tree. Como colunas de carga, elas nunca são usadas para guiar varreduras de índice. O processo de quebra também remove uma ou mais colunas de chave final quando o prefixo restante da(s) coluna(s) de chave acontece ser suficiente para descrever tuplos no nível mais baixo do B-Tree. Na prática, cobrir índices sem uma cláusula `INCLUDE` muitas vezes evita armazenar colunas que são efetivamente de carga nos níveis superiores. No entanto, definir explicitamente as colunas de carga como colunas não-chave *confiável* mantém os tuplos nos níveis superiores pequenos.

Em princípio, varreduras apenas de índice podem ser usadas com índices de expressão. Por exemplo, dado um índice em `f(x)`, onde `x` é uma coluna de tabela, deve ser possível executar

```
SELECT f(x) FROM tab WHERE f(x) < 1;
```

como uma varredura apenas com índice; e isso é muito atraente se `f()` for uma função cara de calcular. No entanto, o planejador do PostgreSQL atualmente não é muito inteligente em relação a esses casos. Ele considera que uma consulta pode ser potencialmente executada por varredura apenas com índice quando todos os *coluna*s necessários pela consulta estão disponíveis no índice. Neste exemplo, `x` não é necessário, exceto no contexto `f(x)`, mas o planejador não percebe isso e conclui que uma varredura apenas com índice não é possível. Se uma varredura apenas com índice parecer suficientemente valiosa, isso pode ser contornado adicionando `x` como uma coluna incluída, por exemplo

```
CREATE INDEX tab_f_x ON tab (f(x)) INCLUDE (x);
```

Uma advertência adicional, se o objetivo for evitar a recálculo de `f(x)`, é que o planejador não necessariamente corresponderá aos usos de `f(x)` que não estão em cláusulas indexáveis `WHERE` ao coluna de índice. Geralmente, ele fará isso corretamente em consultas simples, como as mostradas acima, mas não em consultas que envolvem junções. Essas deficiências podem ser corrigidas em versões futuras do PostgreSQL.

Os índices parciais também têm interações interessantes com varreduras apenas de índice. Considere o índice parcial mostrado em [Exemplo 11.3][(indexes-partial.md#INDEXES-PARTIAL-EX3 "Example 11.3. Setting up a Partial Unique Index")]:

```
CREATE UNIQUE INDEX tests_success_constraint ON tests (subject, target)
    WHERE success;
```

Em princípio, poderíamos fazer uma varredura apenas com índice para satisfazer uma consulta como

```
SELECT target FROM tests WHERE subject = 'some-subject' AND success;
```

Mas há um problema: a cláusula `WHERE` se refere a `success`, que não está disponível como coluna de resultado do índice. No entanto, uma varredura apenas com índice é possível, pois o plano não precisa reverificar essa parte da cláusula `WHERE` no momento da execução: todas as entradas encontradas no índice necessariamente têm `success = true`, então essa necessidade não precisa ser explicitamente verificada no plano. As versões do PostgreSQL 9.6 e posteriores reconhecerão tais casos e permitirão a geração de varreduras apenas com índice, mas as versões mais antigas não farão isso.