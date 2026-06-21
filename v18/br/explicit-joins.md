## 14.3. Controlar o Planejador com Cláusulas Exíguas `JOIN` [#](#EXPLICIT-JOINS)

É possível controlar o planejador de consulta até certo ponto usando a sintaxe explícita `JOIN`. Para entender por que isso é importante, primeiro precisamos de um pouco de contexto.

Em uma consulta de junção simples, como:

```
SELECT * FROM a, b, c WHERE a.id = b.id AND b.ref = c.id;
```

O planejador pode adicionar as tabelas fornecidas em qualquer ordem. Por exemplo, ele pode gerar um plano de consulta que junta A a B, usando a condição `WHERE`, e depois junta C a essa tabela conjunta, usando a outra condição [[`WHERE`]. Ou pode juntar B a C e depois juntar A a esse resultado. Ou pode juntar A a C e depois juntá-los com B — mas isso seria ineficiente, uma vez que o produto cartesiano completo de A e C teria que ser formado, não havendo nenhuma condição aplicável na cláusula `WHERE` para permitir a otimização da junção. (Todas as junções no executor PostgreSQL acontecem entre duas tabelas de entrada, portanto, é necessário construir o resultado de uma ou outra dessas maneiras.) O ponto importante é que essas diferentes possibilidades de junção dão resultados semanticamente equivalentes, mas podem ter custos de execução extremamente diferentes. Portanto, o planejador explorará todas elas para tentar encontrar o plano de consulta mais eficiente.

Quando uma consulta envolve apenas duas ou três tabelas, não há muitas ordens de junção para se preocupar. Mas o número de possíveis ordens de junção cresce exponencialmente à medida que o número de tabelas aumenta. Além de dez ou mais tabelas de entrada, não é mais prático fazer uma busca exhaustiva de todas as possibilidades, e mesmo para seis ou sete tabelas, o planejamento pode levar um tempo irritantemente longo. Quando há muitas tabelas de entrada, o planejador do PostgreSQL passará de uma busca exhaustiva para uma busca *genética* probabilística através de um número limitado de possibilidades. (O limite de alternância é definido pelo parâmetro [geqo_threshold][(runtime-config-query.md#GUC-GEQO-THRESHOLD)] do parâmetro de tempo de execução.) A busca genética leva menos tempo, mas não necessariamente encontrará o melhor plano possível.

Quando a consulta envolve junções externas, o planejador tem menos liberdade do que para junções simples (internas). Por exemplo, considere:

```
SELECT * FROM a LEFT JOIN (b JOIN c ON (b.ref = c.id)) ON (a.id = b.id);
```

Embora as restrições desta consulta sejam superficialmente semelhantes ao exemplo anterior, a semântica é diferente porque uma linha deve ser emitida para cada linha de A que não tenha uma linha correspondente na junção de B e C. Portanto, o planejador não tem escolha no ordenamento da junção aqui: ele deve unir B a C e, em seguida, unir A a esse resultado. Consequentemente, esta consulta leva menos tempo para ser planejada do que a consulta anterior. Em outros casos, o planejador pode determinar que mais de um ordenamento de junção é seguro. Por exemplo, dado:

```
SELECT * FROM a LEFT JOIN b ON (a.bid = b.id) LEFT JOIN c ON (a.cid = c.id);
```

É válido juntar A a B ou C primeiro. Atualmente, apenas `FULL JOIN` restringe completamente a ordem de junção. A maioria dos casos práticos que envolvem `LEFT JOIN` ou `RIGHT JOIN` pode ser reorganizada em certa medida.

A sintaxe de junção explícita interna (`INNER JOIN`, `CROSS JOIN`, ou sem marcação `JOIN`) é semanticamente a mesma que listar as relações de entrada em `FROM`, portanto, não restringe a ordem de junção.

Embora a maioria dos tipos de `JOIN` não restrinja completamente a ordem de junção, é possível instruir o planejador de consultas do PostgreSQL a tratar todas as cláusulas `JOIN` como restritivas à ordem de junção, de qualquer forma. Por exemplo, essas três consultas são logicamente equivalentes:

```
SELECT * FROM a, b, c WHERE a.id = b.id AND b.ref = c.id;
SELECT * FROM a CROSS JOIN b CROSS JOIN c WHERE a.id = b.id AND b.ref = c.id;
SELECT * FROM a JOIN (b JOIN c ON (b.ref = c.id)) ON (a.id = b.id);
```

Mas se dissermos ao planejador que deve seguir a ordem do `JOIN`, o segundo e o terceiro levam menos tempo para ser planejado do que o primeiro. Esse efeito não vale a pena se preocupar apenas com três tabelas, mas pode ser uma salvação com muitas tabelas.

Para forçar o planejador a seguir a ordem de junção estabelecida pelos `JOIN`s explícitos, defina o parâmetro de limite de colapso de junção [join_collapse_limit][(runtime-config-query.md#GUC-JOIN-COLLAPSE-LIMIT)] para 1. (Outras possíveis valores são discutidos abaixo.)

Você não precisa restringir completamente a ordem de junção para reduzir o tempo de pesquisa, pois é OK usar operadores `JOIN` dentro de itens de uma lista simples `FROM`. Por exemplo, considere:

```
SELECT * FROM a CROSS JOIN b, c, d, e WHERE ...;
```

Com `join_collapse_limit` = 1, isso obriga o planejador a unir A a B antes de unir-los a outras tabelas, mas não restringe suas escolhas de outra forma. Neste exemplo, o número de possíveis ordens de junção é reduzido por um fator de 5.

O controle da busca do planejador dessa maneira é uma técnica útil tanto para reduzir o tempo de planejamento quanto para direcionar o planejador para um bom plano de consulta. Se o planejador escolher uma ordem de junção ruim por padrão, você pode forçá-lo a escolher uma ordem melhor via sintaxe `JOIN` — assumindo que você saiba de uma ordem melhor, ou seja, recomenda-se a experimentação.

Um problema intimamente relacionado que afeta o tempo de planejamento é o colapso de subconsultas em sua consulta principal. Por exemplo, considere:

```
SELECT *
FROM x, y,
    (SELECT * FROM a, b, c WHERE something) AS ss
WHERE somethingelse;
```

Essa situação pode surgir pelo uso de uma visão que contém uma junção; a regra `SELECT` da visão será inserida no lugar da referência da visão, resultando em uma consulta muito semelhante à acima. Normalmente, o planejador tentará reduzir a subconsulta ao nível do pai, resultando em:

```
SELECT * FROM x, y, a, b, c WHERE something AND somethingelse;
```

Isso geralmente resulta em um plano melhor do que planejar a subconsulta separadamente. (Por exemplo, as condições externas do `WHERE` podem ser tais que a união de X com A elimina primeiro muitas linhas de A, evitando assim a necessidade de formar a saída lógica completa da subconsulta.) Mas, ao mesmo tempo, aumentamos o tempo de planejamento; aqui, temos um problema de junção de cinco vias que substitui dois problemas de junção de três vias separados. Devido ao crescimento exponencial do número de possibilidades, isso faz uma grande diferença. O planejador tenta evitar ficar preso em enormes problemas de busca de junção, não reduzindo uma subconsulta se mais de `from_collapse_limit` itens do `FROM` resultar na consulta pai. Você pode fazer um trade-off entre o tempo de planejamento e a qualidade do plano ajustando este parâmetro de tempo de execução para cima ou para baixo.

[de_limite_de_colapso](runtime-config-query.md#GUC-FROM-COLLAPSE-LIMIT) e [join_collapse_limit](runtime-config-query.md#GUC-JOIN-COLLAPSE-LIMIT) têm nomes semelhantes porque fazem quase a mesma coisa: um controla quando o planejador "desdobra" subconsultas, e o outro controla quando ele desdobrará as junções explícitas. Normalmente, você pode definir `join_collapse_limit` igual a `from_collapse_limit` (para que as junções e subconsultas explícitas atuem de forma semelhante) ou definir `join_collapse_limit` para 1 (se você quiser controlar a ordem de junção com junções explícitas). Mas você pode defini-los de maneira diferente se estiver tentando ajustar o equilíbrio entre o tempo de planejamento e o tempo de execução.