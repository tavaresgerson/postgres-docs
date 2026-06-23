## 39.2. Visões e o Sistema de Regras [#](#RULES-VIEWS)

* [39.2.1. Como as regras do `SELECT` funcionam](rules-views.md#RULES-SELECT)
* [39.2.2. Visualizar regras em declarações não do `SELECT`](rules-views.md#RULES-VIEWS-NON-SELECT)
* [39.2.3. O poder das visualizações no PostgreSQL](rules-views.md#RULES-VIEWS-POWER)
* [39.2.4. Atualizando uma visualização](rules-views.md#RULES-VIEWS-UPDATE)

As vistas no PostgreSQL são implementadas usando o sistema de regras. Uma vista é basicamente uma tabela vazia (sem armazenamento real) com uma regra `ON SELECT DO INSTEAD`. Convencionalmente, essa regra é chamada de `_RETURN`. Portanto, uma vista como

```
CREATE VIEW myview AS SELECT * FROM mytab;
```

é praticamente a mesma coisa que

```
CREATE TABLE myview (same column list as mytab);
CREATE RULE "_RETURN" AS ON SELECT TO myview DO INSTEAD
    SELECT * FROM mytab;
```

embora você não possa realmente escrever isso, porque as tabelas não podem ter regras `ON SELECT`.

Uma visão também pode ter outros tipos de regras `DO INSTEAD`, permitindo que os comandos `INSERT`, `UPDATE` ou `DELETE` sejam executados na visão, apesar da falta de armazenamento subjacente. Isso é discutido mais adiante, na [Seção 39.2.4](rules-views.md#RULES-VIEWS-UPDATE).

### 39.2.1. Como funcionam as regras do `SELECT` [#](#RULES-SELECT)

As regras `ON SELECT` são aplicadas a todas as consultas como o último passo, mesmo que o comando dado seja um `INSERT`, `UPDATE` ou `DELETE`. E elas têm uma semântica diferente das regras dos outros tipos de comandos, pois modificam a árvore de consulta no local em vez de criar uma nova. Portanto, as regras `SELECT` são descritas primeiro.

Atualmente, só pode haver uma ação em uma regra de `ON SELECT`, e ela deve ser uma ação `SELECT` incondicional que é `INSTEAD`. Essa restrição foi necessária para tornar as regras seguras o suficiente para serem abertas para usuários comuns, e ela restringe as regras de `ON SELECT` a agir como visualizações.

Os exemplos deste capítulo são duas vistas de junção que realizam alguns cálculos e algumas outras vistas que as utilizam, por sua vez. Uma das duas primeiras vistas é personalizada posteriormente, adicionando regras para as operações `INSERT`, `UPDATE` e `DELETE`, para que o resultado final seja uma vista que se comporte como uma verdadeira tabela com alguma funcionalidade mágica. Este não é um exemplo tão simples para começar e isso torna as coisas mais difíceis de entender. Mas é melhor ter um exemplo que cubra todos os pontos discutidos passo a passo, em vez de ter muitos diferentes que podem se misturar na mente.

As tabelas reais que precisamos nas duas primeiras descrições do sistema de regras são estas:

```
CREATE TABLE shoe_data (
    shoename   text,          -- primary key
    sh_avail   integer,       -- available number of pairs
    slcolor    text,          -- preferred shoelace color
    slminlen   real,          -- minimum shoelace length
    slmaxlen   real,          -- maximum shoelace length
    slunit     text           -- length unit
);

CREATE TABLE shoelace_data (
    sl_name    text,          -- primary key
    sl_avail   integer,       -- available number of pairs
    sl_color   text,          -- shoelace color
    sl_len     real,          -- shoelace length
    sl_unit    text           -- length unit
);

CREATE TABLE unit (
    un_name    text,          -- primary key
    un_fact    real           -- factor to transform to cm
);
```

Como você pode ver, eles representam dados de lojas de calçados.

As vistas são criadas como:

```
CREATE VIEW shoe AS
    SELECT sh.shoename,
           sh.sh_avail,
           sh.slcolor,
           sh.slminlen,
           sh.slminlen * un.un_fact AS slminlen_cm,
           sh.slmaxlen,
           sh.slmaxlen * un.un_fact AS slmaxlen_cm,
           sh.slunit
      FROM shoe_data sh, unit un
     WHERE sh.slunit = un.un_name;

CREATE VIEW shoelace AS
    SELECT s.sl_name,
           s.sl_avail,
           s.sl_color,
           s.sl_len,
           s.sl_unit,
           s.sl_len * u.un_fact AS sl_len_cm
      FROM shoelace_data s, unit u
     WHERE s.sl_unit = u.un_name;

CREATE VIEW shoe_ready AS
    SELECT rsh.shoename,
           rsh.sh_avail,
           rsl.sl_name,
           rsl.sl_avail,
           least(rsh.sh_avail, rsl.sl_avail) AS total_avail
      FROM shoe rsh, shoelace rsl
     WHERE rsl.sl_color = rsh.slcolor
       AND rsl.sl_len_cm >= rsh.slminlen_cm
       AND rsl.sl_len_cm <= rsh.slmaxlen_cm;
```

O comando `CREATE VIEW` para a visualização `shoelace` (que é a mais simples que temos) criará uma relação `shoelace` e uma entrada em `pg_rewrite` que indica que há uma regra de reescrita que deve ser aplicada sempre que a relação `shoelace` seja referenciada em uma tabela de intervalo de consulta. A regra não tem qualificação de regra (discutida mais tarde, com as regras não `SELECT`, uma vez que as regras `SELECT` atualmente não podem tê-las) e é `INSTEAD`. Note que as qualificações de regra não são as mesmas que as qualificações de consulta. A ação da nossa regra tem uma qualificação de consulta. A ação da regra é uma árvore de consulta que é uma cópia da declaração `SELECT` no comando de criação da visualização.

### Nota

As duas entradas de tabela de intervalo adicional para `NEW` e `OLD` que você pode ver na entrada `pg_rewrite` não são de interesse para as regras de `SELECT`.

Agora, vamos preencher `unit`, `shoe_data` e `shoelace_data` e executar uma consulta simples em uma visão:

```
INSERT INTO unit VALUES ('cm', 1.0);
INSERT INTO unit VALUES ('m', 100.0);
INSERT INTO unit VALUES ('inch', 2.54);

INSERT INTO shoe_data VALUES ('sh1', 2, 'black', 70.0, 90.0, 'cm');
INSERT INTO shoe_data VALUES ('sh2', 0, 'black', 30.0, 40.0, 'inch');
INSERT INTO shoe_data VALUES ('sh3', 4, 'brown', 50.0, 65.0, 'cm');
INSERT INTO shoe_data VALUES ('sh4', 3, 'brown', 40.0, 50.0, 'inch');

INSERT INTO shoelace_data VALUES ('sl1', 5, 'black', 80.0, 'cm');
INSERT INTO shoelace_data VALUES ('sl2', 6, 'black', 100.0, 'cm');
INSERT INTO shoelace_data VALUES ('sl3', 0, 'black', 35.0 , 'inch');
INSERT INTO shoelace_data VALUES ('sl4', 8, 'black', 40.0 , 'inch');
INSERT INTO shoelace_data VALUES ('sl5', 4, 'brown', 1.0 , 'm');
INSERT INTO shoelace_data VALUES ('sl6', 0, 'brown', 0.9 , 'm');
INSERT INTO shoelace_data VALUES ('sl7', 7, 'brown', 60 , 'cm');
INSERT INTO shoelace_data VALUES ('sl8', 1, 'brown', 40 , 'inch');

SELECT * FROM shoelace;

 sl_name   | sl_avail | sl_color | sl_len | sl_unit | sl_len_cm
-----------+----------+----------+--------+---------+-----------
 sl1       |        5 | black    |     80 | cm      |        80
 sl2       |        6 | black    |    100 | cm      |       100
 sl7       |        7 | brown    |     60 | cm      |        60
 sl3       |        0 | black    |     35 | inch    |      88.9
 sl4       |        8 | black    |     40 | inch    |     101.6
 sl8       |        1 | brown    |     40 | inch    |     101.6
 sl5       |        4 | brown    |      1 | m       |       100
 sl6       |        0 | brown    |    0.9 | m       |        90
(8 rows)
```

Este é o `SELECT` mais simples que você pode fazer em nossas visualizações, então aproveitamos para explicar os conceitos básicos das regras de visualização. O `SELECT * FROM shoelace` foi interpretado pelo analisador e produziu a árvore de consulta:

```
SELECT shoelace.sl_name, shoelace.sl_avail,
       shoelace.sl_color, shoelace.sl_len,
       shoelace.sl_unit, shoelace.sl_len_cm
  FROM shoelace shoelace;
```

e isso é dado ao sistema de regras. O sistema de regras percorre a tabela de intervalo e verifica se há regras para qualquer relação. Ao processar a entrada da tabela de intervalo para `shoelace` (a única até agora), ele encontra a regra `_RETURN` com a árvore de consulta:

```
SELECT s.sl_name, s.sl_avail,
       s.sl_color, s.sl_len, s.sl_unit,
       s.sl_len * u.un_fact AS sl_len_cm
  FROM shoelace old, shoelace new,
       shoelace_data s, unit u
 WHERE s.sl_unit = u.un_name;
```

Para expandir a visão, o reescritor simplesmente cria uma entrada de tabela de intervalo de subconsulta que contém a árvore de consulta de ação da regra e substitui essa entrada de tabela de intervalo pela original que fazia referência à visão. A árvore de consulta reescrita resultante é quase a mesma como se tivesse digitado:

```
SELECT shoelace.sl_name, shoelace.sl_avail,
       shoelace.sl_color, shoelace.sl_len,
       shoelace.sl_unit, shoelace.sl_len_cm
  FROM (SELECT s.sl_name,
               s.sl_avail,
               s.sl_color,
               s.sl_len,
               s.sl_unit,
               s.sl_len * u.un_fact AS sl_len_cm
          FROM shoelace_data s, unit u
         WHERE s.sl_unit = u.un_name) shoelace;
```

Há, no entanto, uma diferença: a tabela de intervalo da subconsulta tem duas entradas extras `shoelace old` e `shoelace new`. Essas entradas não participam diretamente da consulta, uma vez que não são referenciadas pela árvore de junção ou pela lista de alvos da subconsulta. O reescritor as usa para armazenar as informações de verificação de privilégios de acesso que estavam originalmente presentes na entrada da tabela de intervalo que referenciava a visão. Dessa forma, o executor ainda verificará se o usuário tem os privilégios adequados para acessar a visão, mesmo que não haja uso direto da visão na consulta reescrita.

Essa foi a primeira regra aplicada. O sistema de regras continuará verificando as entradas restantes da tabela de intervalo na consulta principal (nesse exemplo, não há mais), e verificará recursivamente as entradas da tabela de intervalo na subconsulta adicionada para ver se alguma delas faz referência a visualizações. (Mas não expandirá `old` ou `new` — caso contrário, teríamos uma recursão infinita!) Neste exemplo, não há regras de reescrita para `shoelace_data` ou `unit`, portanto, a reescrita está completa e o resultado acima é o dado ao planejador.

Agora, queremos escrever uma consulta que descubra para quais sapatos que atualmente estão na loja temos as fivelas correspondentes (cor e comprimento) e onde o número total de pares exatamente correspondentes é maior ou igual a dois.

```
SELECT * FROM shoe_ready WHERE total_avail >= 2;

 shoename | sh_avail | sl_name | sl_avail | total_avail
----------+----------+---------+----------+-------------
 sh1      |        2 | sl1     |        5 |           2
 sh3      |        4 | sl7     |        7 |           4
(2 rows)
```

A saída do analisador desta vez é a árvore de consulta:

```
SELECT shoe_ready.shoename, shoe_ready.sh_avail,
       shoe_ready.sl_name, shoe_ready.sl_avail,
       shoe_ready.total_avail
  FROM shoe_ready shoe_ready
 WHERE shoe_ready.total_avail >= 2;
```

A primeira regra aplicada será a da vista `shoe_ready` e isso resulta na árvore de consulta:

```
SELECT shoe_ready.shoename, shoe_ready.sh_avail,
       shoe_ready.sl_name, shoe_ready.sl_avail,
       shoe_ready.total_avail
  FROM (SELECT rsh.shoename,
               rsh.sh_avail,
               rsl.sl_name,
               rsl.sl_avail,
               least(rsh.sh_avail, rsl.sl_avail) AS total_avail
          FROM shoe rsh, shoelace rsl
         WHERE rsl.sl_color = rsh.slcolor
           AND rsl.sl_len_cm >= rsh.slminlen_cm
           AND rsl.sl_len_cm <= rsh.slmaxlen_cm) shoe_ready
 WHERE shoe_ready.total_avail >= 2;
```

Da mesma forma, as regras para `shoe` e `shoelace` são substituídas na tabela de intervalo da subconsulta, resultando em uma árvore de consulta final de três níveis:

```
SELECT shoe_ready.shoename, shoe_ready.sh_avail,
       shoe_ready.sl_name, shoe_ready.sl_avail,
       shoe_ready.total_avail
  FROM (SELECT rsh.shoename,
               rsh.sh_avail,
               rsl.sl_name,
               rsl.sl_avail,
               least(rsh.sh_avail, rsl.sl_avail) AS total_avail
          FROM (SELECT sh.shoename,
                       sh.sh_avail,
                       sh.slcolor,
                       sh.slminlen,
                       sh.slminlen * un.un_fact AS slminlen_cm,
                       sh.slmaxlen,
                       sh.slmaxlen * un.un_fact AS slmaxlen_cm,
                       sh.slunit
                  FROM shoe_data sh, unit un
                 WHERE sh.slunit = un.un_name) rsh,
               (SELECT s.sl_name,
                       s.sl_avail,
                       s.sl_color,
                       s.sl_len,
                       s.sl_unit,
                       s.sl_len * u.un_fact AS sl_len_cm
                  FROM shoelace_data s, unit u
                 WHERE s.sl_unit = u.un_name) rsl
         WHERE rsl.sl_color = rsh.slcolor
           AND rsl.sl_len_cm >= rsh.slminlen_cm
           AND rsl.sl_len_cm <= rsh.slmaxlen_cm) shoe_ready
 WHERE shoe_ready.total_avail > 2;
```

Isso pode parecer ineficiente, mas o planejador reduzirá essa consulta em uma árvore de consulta de nível único, "levantado" as subconsultas, e então planejará as junções como se as tivéssemos escrito manualmente. Portanto, a redução da árvore de consulta é uma otimização com a qual o sistema de reescrita não precisa se preocupar.

### 39.2.2. Verifique as regras em declarações não `SELECT` [#](#RULES-VIEWS-NON-SELECT)

Dois detalhes da árvore de consulta não são mencionados na descrição das regras de visualização acima. Esses são o tipo de comando e a relação de resultado. De fato, o tipo de comando não é necessário para as regras de visualização, mas a relação de resultado pode afetar a maneira como o reescritor de consulta funciona, porque é necessário ter cuidado especial se a relação de resultado for uma visualização.

Há apenas algumas diferenças entre uma árvore de consulta para um `SELECT` e uma para qualquer outro comando. Obviamente, eles têm um tipo de comando diferente e, para um comando diferente de um `SELECT`, a relação de resultado aponta para a entrada da tabela de intervalo onde o resultado deve ir. Tudo o resto é absolutamente o mesmo. Portanto, tendo duas tabelas `t1` e `t2` com as colunas `a` e `b`, as árvores de consulta para as duas declarações:

```
SELECT t2.b FROM t1, t2 WHERE t1.a = t2.a;

UPDATE t1 SET b = t2.b FROM t2 WHERE t1.a = t2.a;
```

são quase idênticas. Em particular:

* As tabelas de intervalo contêm entradas para as tabelas `t1` e `t2`.
* As listas de alvos contêm uma variável que aponta para a coluna `b` da entrada da tabela de intervalo para a tabela `t2`.
* As expressões de qualificação comparam as colunas `a` de ambas as entradas da tabela de intervalo para igualdade.
* As árvores de junção mostram uma junção simples entre `t1` e `t2`.

A consequência é que ambos os árvores de consulta resultam em planos de execução semelhantes: ambos são junções sobre as duas tabelas. Para o `UPDATE`, as colunas ausentes do `t1` são adicionadas à lista de destino pelo planejador e a árvore final de consulta será lida como:

```
UPDATE t1 SET a = t1.a, b = t2.b FROM t2 WHERE t1.a = t2.a;
```

e, assim, o executor que executa a junção produzirá exatamente o mesmo conjunto de resultados que:

```
SELECT t1.a, t2.b FROM t1, t2 WHERE t1.a = t2.a;
```

Mas há um pequeno problema no `UPDATE`: a parte do plano do executor que faz a junção não se importa com para que os resultados da junção sejam usados. Ela simplesmente produz um conjunto de resultados de linhas. O fato de um ser um comando `SELECT` e o outro um `UPDATE` é tratado mais acima no executor, onde sabe que isso é um `UPDATE`, e sabe que esse resultado deve ser inserido na tabela `t1`. Mas qual das linhas que estão lá deve ser substituída pela nova linha?

Para resolver esse problema, outra entrada é adicionada à lista de alvos nas declarações de `UPDATE` (e também em `DELETE`): o ID atual do tuplo (CTID). Esta é uma coluna do sistema que contém o número e a posição do bloco do arquivo para a linha. Conhecendo a tabela, o CTID pode ser usado para recuperar a linha original de `t1` a ser atualizada. Após adicionar o CTID à lista de alvos, a consulta na verdade parece assim:

```
SELECT t1.a, t2.b, t1.ctid FROM t1, t2 WHERE t1.a = t2.a;
```

Agora, outro detalhe do PostgreSQL entra em cena. As linhas antigas da tabela não são sobrescritas, e é por isso que `ROLLBACK` é rápido. Em um `UPDATE`, a nova linha de resultado é inserida na tabela (após a remoção do CTID) e, no cabeçalho da linha antiga, que o CTID apontou, as entradas `cmax` e `xmax` são definidas como o contador de comando atual e o ID de transação atual. Assim, a linha antiga é oculta, e, após a transação ser confirmada, o aspirador de pó pode eventualmente remover a linha morta.

Sabendo disso, podemos simplesmente aplicar as regras de visualização da mesma maneira a qualquer comando. Não há diferença.

### 39.2.3. O poder das vistas no PostgreSQL [#](#RULES-VIEWS-POWER)

O acima demonstra como o sistema de regras incorpora definições de visão na árvore de consulta original. No segundo exemplo, um simples `SELECT` de uma visão criou uma árvore de consulta final que é uma junção de 4 tabelas (`unit` foi usado duas vezes com nomes diferentes).

A vantagem de implementar vistas com o sistema de regras é que o planejador tem todas as informações sobre quais tabelas precisam ser pesquisadas, além das relações entre essas tabelas, as qualificações restritivas das vistas e as qualificações da consulta original em uma única árvore de consulta. E essa ainda é a situação quando a consulta original já é uma junção sobre vistas. O planejador tem que decidir qual é o melhor caminho para executar a consulta, e quanto mais informações o planejador tiver, melhor essa decisão pode ser. E o sistema de regras, conforme implementado no PostgreSQL, garante que todas essas informações estejam disponíveis sobre a consulta até esse ponto.

### 39.2.4. Atualizando uma visualização [#](#RULES-VIEWS-UPDATE)

O que acontece se uma visão for nomeada como a relação de destino para um `INSERT`, `UPDATE`, `DELETE` ou `MERGE`? Fazer as substituições descritas acima daria uma árvore de consulta na qual a relação de resultado aponta para uma entrada de tabela de intervalo de subconsulta, o que não funcionará. Há várias maneiras pelas quais o PostgreSQL pode suportar a aparência de atualização de uma visão, no entanto. Em ordem de complexidade de experiência do usuário, elas são: substituir automaticamente na tabela subjacente para a visão, executar um gatilho definido pelo usuário ou reescrever a consulta por uma regra definida pelo usuário. Essas opções são discutidas abaixo.

Se a subconsulta selecionar uma única relação de base e for simples o suficiente, o reescritor pode substituir automaticamente a subconsulta pela relação de base subjacente, de modo que o `INSERT`, `UPDATE`, `DELETE` ou `MERGE` seja aplicado à relação de base da maneira apropriada. As visualizações que são “simples o suficiente” para isso são chamadas de *automaticamente atualizáveis*. Para informações detalhadas sobre os tipos de visualização que podem ser atualizados automaticamente, consulte [CREATE VIEW](sql-createview.md "CREATE VIEW").

Alternativamente, a operação pode ser gerenciada por um gatilho fornecido pelo usuário `INSTEAD OF` na visualização (consulte [CREATE TRIGGER](sql-createtrigger.md)). A reescrita funciona de maneira um pouco diferente neste caso. Para `INSERT`, o reescritor não faz nada com a visualização, deixando-a como a relação de resultado para a consulta. Para `UPDATE`, `DELETE` e `MERGE`, ainda é necessário expandir a consulta da visualização para produzir as linhas “antigas” que o comando tentará atualizar, excluir ou combinar. Portanto, a visualização é expandida normalmente, mas outra entrada de tabela não expandida é adicionada à consulta para representar a visualização em sua capacidade como a relação de resultado.

O problema que agora surge é como identificar as linhas que devem ser atualizadas na visualização. Lembre-se de que, quando a relação de resultado é uma tabela, uma entrada especial de CTID é adicionada à lista de destino para identificar as localizações físicas das linhas que devem ser atualizadas. Isso não funciona se a relação de resultado for uma visualização, porque uma visualização não tem nenhum CTID, uma vez que suas linhas não têm locais físicos reais. Em vez disso, para uma operação de `UPDATE`, `DELETE` ou `MERGE`, uma entrada especial de `wholerow` é adicionada à lista de destino, que se expande para incluir todas as colunas da visualização. O executor usa esse valor para fornecer o "antigo" registro ao gatilho `INSTEAD OF`. Cabe ao gatilho determinar o que deve ser atualizado com base nos valores das linhas antigas e novas.

Outra possibilidade é o usuário definir regras `INSTEAD` que especifiquem ações de substituição para os comandos `INSERT`, `UPDATE` e `DELETE` em uma visão. Essas regras reescreverão o comando, tipicamente em um comando que atualiza uma ou mais tabelas, em vez de visões. Esse é o tema do [Seção 39.4](rules-update.md). Observe que isso não funcionará com `MERGE`, que atualmente não suporta regras na relação de destino, exceto as regras `SELECT`.

Observe que as regras são avaliadas primeiro, reescrevendo a consulta original antes de ser planejada e executada. Portanto, se uma visão tiver gatilhos `INSTEAD OF` bem como regras em `INSERT`, `UPDATE` ou `DELETE`, então as regras serão avaliadas primeiro, e dependendo do resultado, os gatilhos podem não ser usados em absoluto.

A reescrita automática de uma consulta `INSERT`, `UPDATE`, `DELETE` ou `MERGE` em uma visão simples é sempre tentada como última opção. Portanto, se uma visão tiver regras ou gatilhos, eles substituirão o comportamento padrão de visões automaticamente atualizáveis.

Se não houver regras `INSTEAD` ou gatilhos `INSTEAD OF` para a visualização, e o reescritor não possa reescrever automaticamente a consulta como uma atualização na relação base subjacente, um erro será lançado porque o executor não pode atualizar uma visualização como tal.