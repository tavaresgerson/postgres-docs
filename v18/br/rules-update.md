## 39.4. Regras sobre `INSERT`, `UPDATE` e `DELETE` [#](#RULES-UPDATE)

* [39.4.1. Como funcionam as regras de atualização](rules-update.md#RULES-UPDATE-HOW)
* [39.4.2. Cooperação com vistas](rules-update.md#RULES-UPDATE-VIEWS)

As regras definidas em `INSERT`, `UPDATE` e `DELETE` são significativamente diferentes das regras de visualização descritas nas seções anteriores. Em primeiro lugar, seu comando `CREATE RULE` permite mais:

* Não podem ter nenhuma ação.
* Podem ter múltiplas ações.
* Podem ser `INSTEAD` ou `ALSO` (padrão).
* As pseudorelações `NEW` e `OLD` tornam-se úteis.
* Podem ter qualificações de regra.

Em segundo lugar, eles não modificam a árvore de consulta no local. Em vez disso, eles criam zero ou mais novas árvores de consulta e podem descartar a original.

### Atenção

Em muitos casos, as tarefas que poderiam ser realizadas por regras em `INSERT`/`UPDATE`/`DELETE` são melhor realizadas com gatilhos. Os gatilhos são um pouco mais complicados no que diz respeito à notação, mas sua semântica é muito mais simples de entender. As regras tendem a ter resultados surpreendentes quando a consulta original contém funções voláteis: as funções voláteis podem ser executadas mais vezes do que o esperado no processo de execução das regras.

Além disso, há alguns casos que não são suportados por esses tipos de regras, incluindo, principalmente, as cláusulas `WITH` na consulta original e as sub`SELECT`s de múltiplas atribuições na lista de consultas `SET` do `UPDATE`. Isso ocorre porque copiar esses construtos em uma consulta de regra resultaria em múltiplas avaliações da subconsulta, em contradição com a intenção expressa do autor da consulta.

### 39.4.1. Como funcionam as regras de atualização [#](#RULES-UPDATE-HOW)

Mantenha a sintaxe:

```
CREATE [ OR REPLACE ] RULE name AS ON event
    TO table [ WHERE condition ]
    DO [ ALSO | INSTEAD ] { NOTHING | command | ( command ; command ... ) }
```

Lembre-se disso. No que se segue, *regras de atualização* significa regras definidas em `INSERT`, `UPDATE` ou `DELETE`.

As regras de atualização são aplicadas pelo sistema de regras quando a relação de resultado e o tipo de comando de uma árvore de consulta são iguais ao objeto e ao evento fornecidos no comando `CREATE RULE`. Para as regras de atualização, o sistema de regras cria uma lista de árvores de consulta. Inicialmente, a lista de árvores de consulta está vazia. Pode haver zero (palavra-chave `NOTHING`), uma ou várias ações. Para simplificar, vamos analisar uma regra com uma ação. Essa regra pode ter uma qualificação ou não e pode ser `INSTEAD` ou `ALSO` (o padrão).

O que é uma qualificação de regra? É uma restrição que indica quando as ações da regra devem ser realizadas e quando não devem. Essa qualificação só pode fazer referência às pseudorelações `NEW` e/ou `OLD`, que basicamente representam a relação que foi dada como objeto (mas com um significado especial).

Então, temos três casos que produzem as seguintes árvores de consulta para uma regra de uma ação.

Sem qualificação, com `ALSO` ou `INSTEAD`: a árvore de consulta da ação da regra com a qualificação da árvore de consulta original adicionada

Qualificação dada e `ALSO`: a árvore de consulta da ação da regra com a qualificação da regra e a qualificação da árvore de consulta original adicionada

Qualificação dada e `INSTEAD`: a árvore de consulta da ação da regra com a qualificação da regra e a qualificação da árvore de consulta original; e a árvore de consulta original com a qualificação da regra negada adicionada

Por fim, se a regra for `ALSO`, a árvore de consulta original não modificada é adicionada à lista. Como apenas as regras qualificadas `INSTEAD` já adicionam a árvore de consulta original, acabamos com uma ou duas árvores de consulta de saída para uma regra com uma ação.

Para as regras de `ON INSERT`, a consulta original (se não suprida por `INSTEAD`) é realizada antes de quaisquer ações adicionadas por regras. Isso permite que as ações vejam a(s) linha(s) inserida(s). Mas para as regras de `ON UPDATE` e `ON DELETE`, a consulta original é realizada após as ações adicionadas por regras. Isso garante que as ações possam ver as linhas a serem atualizadas ou a serem excluídas; caso contrário, as ações podem não fazer nada porque não encontram linhas que correspondam às suas qualificações.

As árvores de consulta geradas a partir das ações das regras são lançadas novamente no sistema de reescrita e, talvez, mais regras sejam aplicadas, resultando em árvores de consulta adicionais ou menores. Portanto, as ações de uma regra devem ter um tipo de comando diferente ou uma relação de resultado diferente daquela em que a própria regra está, caso contrário, esse processo recursivo acabará em um loop infinito. (A expansão recursiva de uma regra será detectada e relatada como um erro.)

As consultas de árvores encontradas nas ações do catálogo do sistema `pg_rewrite` são apenas modelos. Como elas podem fazer referência às entradas da tabela de intervalo para `NEW` e `OLD`, algumas substituições têm que ser feitas antes que elas possam ser usadas. Para qualquer referência a `NEW`, a lista de destino da consulta original é pesquisada em busca de uma entrada correspondente. Se encontrada, a expressão daquela entrada substitui a referência. Caso contrário, `NEW` significa o mesmo que `OLD` (para um `UPDATE`) ou é substituído por um valor nulo (para um `INSERT`). Qualquer referência a `OLD` é substituída por uma referência à entrada da tabela de intervalo que é a relação de resultado.

Após o sistema aplicar as regras de atualização, ele aplica as regras de exibição à(s) árvore(s) de consulta produzida(s). As exibições não podem inserir novas ações de atualização, portanto, não há necessidade de aplicar as regras de atualização ao resultado da reescrita da exibição.

#### 39.4.1.1. Uma Primeira Regra Passo a Passo [#](#RULES-UPDATE-HOW-FIRST)

Digamos que queira rastrear alterações na coluna `sl_avail` na relação `shoelace_data`. Então, configuramos uma tabela de registro e uma regra que escreve condicionalmente uma entrada de registro quando um `UPDATE` é realizado em `shoelace_data`.

```
CREATE TABLE shoelace_log (
    sl_name    text,          -- shoelace changed
    sl_avail   integer,       -- new available value
    log_who    text,          -- who did it
    log_when   timestamp      -- when
);

CREATE RULE log_shoelace AS ON UPDATE TO shoelace_data
    WHERE NEW.sl_avail <> OLD.sl_avail
    DO INSERT INTO shoelace_log VALUES (
                                    NEW.sl_name,
                                    NEW.sl_avail,
                                    current_user,
                                    current_timestamp
                                );
```

Agora, alguém faz isso:

```
UPDATE shoelace_data SET sl_avail = 6 WHERE sl_name = 'sl7';
```

e olhamos na tabela de registro:

```
SELECT * FROM shoelace_log;

 sl_name | sl_avail | log_who | log_when
---------+----------+---------+----------------------------------
 sl7     |        6 | Al      | Tue Oct 20 16:14:45 1998 MET DST
(1 row)
```

Isso é o que esperávamos. O que aconteceu em segundo plano é o seguinte. O analisador criou a árvore de consulta:

```
UPDATE shoelace_data SET sl_avail = 6
  FROM shoelace_data shoelace_data
 WHERE shoelace_data.sl_name = 'sl7';
```

Existe uma regra `log_shoelace` que é `ON UPDATE` com a expressão de qualificação da regra:

```
NEW.sl_avail <> OLD.sl_avail
```

e a ação:

```
INSERT INTO shoelace_log VALUES (
       new.sl_name, new.sl_avail,
       current_user, current_timestamp )
  FROM shoelace_data new, shoelace_data old;
```

(Isso parece um pouco estranho, pois normalmente não se pode escrever `INSERT ... VALUES ... FROM`. A cláusula `FROM` aqui é apenas para indicar que há entradas de tabela de intervalo na árvore de consulta para `new` e `old`. Essas são necessárias para que possam ser referenciadas por variáveis na árvore de consulta do comando `INSERT`.

A regra é uma regra qualificada `ALSO`, portanto, o sistema de regras deve retornar duas árvores de consulta: a ação modificada da regra e a árvore de consulta original. No passo 1, a tabela de intervalo da consulta original é incorporada à árvore de consulta da ação da regra. Isso resulta em:

```
INSERT INTO shoelace_log VALUES (
       new.sl_name, new.sl_avail,
       current_user, current_timestamp )
  FROM shoelace_data new, shoelace_data old,
       shoelace_data shoelace_data;
```

No passo 2, a qualificação da regra é adicionada, de modo que o conjunto de resultados é restrito às linhas onde `sl_avail` muda:

```
INSERT INTO shoelace_log VALUES (
       new.sl_name, new.sl_avail,
       current_user, current_timestamp )
  FROM shoelace_data new, shoelace_data old,
       shoelace_data shoelace_data
 WHERE new.sl_avail <> old.sl_avail;
```

(Isso parece ainda mais estranho, já que `INSERT ... VALUES` também não tem uma cláusula `WHERE`, mas o planejador e o executor não terão dificuldade com isso. Eles precisam suportar essa mesma funcionalidade de qualquer forma para `INSERT ... SELECT`.))

No passo 3, a qualificação da árvore de consulta original é adicionada, restringindo ainda mais o conjunto de resultados apenas às linhas que teriam sido afetadas pela consulta original:

```
INSERT INTO shoelace_log VALUES (
       new.sl_name, new.sl_avail,
       current_user, current_timestamp )
  FROM shoelace_data new, shoelace_data old,
       shoelace_data shoelace_data
 WHERE new.sl_avail <> old.sl_avail
   AND shoelace_data.sl_name = 'sl7';
```

O passo 4 substitui as referências a `NEW` pelas entradas da lista de alvos da árvore de consulta original ou pelas referências de variáveis correspondentes da relação de resultado:

```
INSERT INTO shoelace_log VALUES (
       shoelace_data.sl_name, 6,
       current_user, current_timestamp )
  FROM shoelace_data new, shoelace_data old,
       shoelace_data shoelace_data
 WHERE 6 <> old.sl_avail
   AND shoelace_data.sl_name = 'sl7';
```

O passo 5 altera as referências `OLD` para referências de relação de resultado:

```
INSERT INTO shoelace_log VALUES (
       shoelace_data.sl_name, 6,
       current_user, current_timestamp )
  FROM shoelace_data new, shoelace_data old,
       shoelace_data shoelace_data
 WHERE 6 <> shoelace_data.sl_avail
   AND shoelace_data.sl_name = 'sl7';
```

Isso é tudo. Como a regra é `ALSO`, também exibimos a árvore de consulta original. Em suma, a saída do sistema de regras é uma lista de duas árvores de consulta que correspondem a essas declarações:

```
INSERT INTO shoelace_log VALUES (
       shoelace_data.sl_name, 6,
       current_user, current_timestamp )
  FROM shoelace_data
 WHERE 6 <> shoelace_data.sl_avail
   AND shoelace_data.sl_name = 'sl7';

UPDATE shoelace_data SET sl_avail = 6
 WHERE sl_name = 'sl7';
```

Esses são executados nessa ordem, e é exatamente isso que a regra pretendia fazer.

As substituições e as qualificações adicionais garantem que, se a consulta original fosse, por exemplo:

```
UPDATE shoelace_data SET sl_color = 'green'
 WHERE sl_name = 'sl7';
```

não seria registrada nenhuma entrada de registro. Nesse caso, a árvore de consulta original não contém uma entrada na lista de alvos para `sl_avail`, então `NEW.sl_avail` será substituído por `shoelace_data.sl_avail`. Assim, o comando extra gerado pela regra é:

```
INSERT INTO shoelace_log VALUES (
       shoelace_data.sl_name, shoelace_data.sl_avail,
       current_user, current_timestamp )
  FROM shoelace_data
 WHERE shoelace_data.sl_avail <> shoelace_data.sl_avail
   AND shoelace_data.sl_name = 'sl7';
```

e essa qualificação nunca será verdadeira.

Ele também funcionará se a consulta original modificar várias linhas. Portanto, se alguém emitir o comando:

```
UPDATE shoelace_data SET sl_avail = 0
 WHERE sl_color = 'black';
```

quatro linhas, na verdade, são atualizadas (`sl1`, `sl2`, `sl3` e `sl4`). Mas `sl3` já tem `sl_avail = 0`. Neste caso, a qualificação original das árvores de consulta é diferente e isso resulta na árvore de consulta extra:

```
INSERT INTO shoelace_log
SELECT shoelace_data.sl_name, 0,
       current_user, current_timestamp
  FROM shoelace_data
 WHERE 0 <> shoelace_data.sl_avail
   AND shoelace_data.sl_color = 'black';
```

esta sendo gerado pela regra. Essa árvore de consulta certamente inserirá três novas entradas de log. E isso é absolutamente correto.

Aqui podemos ver por que é importante que a árvore de consulta original seja executada por último. Se o `UPDATE` tivesse sido executado primeiro, todas as linhas já teriam sido definidas como zero, então o registro `INSERT` não encontraria nenhuma linha onde `0 <> shoelace_data.sl_avail`.

### 39.4.2. Cooperação com Visões [#](#RULES-UPDATE-VIEWS)

Uma maneira simples de proteger as relações de visualização contra a possibilidade mencionada de que alguém possa tentar executar `INSERT`, `UPDATE` ou `DELETE` nelas é descartar essas árvores de consulta. Assim, poderíamos criar as regras:

```
CREATE RULE shoe_ins_protect AS ON INSERT TO shoe
    DO INSTEAD NOTHING;
CREATE RULE shoe_upd_protect AS ON UPDATE TO shoe
    DO INSTEAD NOTHING;
CREATE RULE shoe_del_protect AS ON DELETE TO shoe
    DO INSTEAD NOTHING;
```

Se alguém tentar realizar alguma dessas operações na relação de visualização `shoe`, o sistema de regras aplicará essas regras. Como as regras não têm ações e são `INSTEAD`, a lista resultante das árvores de consulta será vazia e toda a consulta se tornará sem efeito, porque não há nada que seja necessário otimizar ou executar após o sistema de regras ter terminado com ela.

Uma maneira mais sofisticada de usar o sistema de regras é criar regras que reescrevam a árvore de consulta em uma que realize a operação correta nas tabelas reais. Para fazer isso na visão `shoelace`, criamos as seguintes regras:

```
CREATE RULE shoelace_ins AS ON INSERT TO shoelace
    DO INSTEAD
    INSERT INTO shoelace_data VALUES (
           NEW.sl_name,
           NEW.sl_avail,
           NEW.sl_color,
           NEW.sl_len,
           NEW.sl_unit
    );

CREATE RULE shoelace_upd AS ON UPDATE TO shoelace
    DO INSTEAD
    UPDATE shoelace_data
       SET sl_name = NEW.sl_name,
           sl_avail = NEW.sl_avail,
           sl_color = NEW.sl_color,
           sl_len = NEW.sl_len,
           sl_unit = NEW.sl_unit
     WHERE sl_name = OLD.sl_name;

CREATE RULE shoelace_del AS ON DELETE TO shoelace
    DO INSTEAD
    DELETE FROM shoelace_data
     WHERE sl_name = OLD.sl_name;
```

Se você deseja suportar consultas `RETURNING` na visualização, é necessário que as regras incluam cláusulas `RETURNING` que calculem as linhas da visualização. Isso geralmente é bastante trivial para visualizações em uma única tabela, mas é um pouco tedioso para visualizações de junção, como `shoelace`. Um exemplo para o caso de inserção é:

```
CREATE RULE shoelace_ins AS ON INSERT TO shoelace
    DO INSTEAD
    INSERT INTO shoelace_data VALUES (
           NEW.sl_name,
           NEW.sl_avail,
           NEW.sl_color,
           NEW.sl_len,
           NEW.sl_unit
    )
    RETURNING
           shoelace_data.*,
           (SELECT shoelace_data.sl_len * u.un_fact
            FROM unit u WHERE shoelace_data.sl_unit = u.un_name);
```

Observe que essa regra suporta as consultas `INSERT` e `INSERT RETURNING` na visualização — a cláusula `RETURNING` é simplesmente ignorada para `INSERT`.

Observe que, na cláusula `RETURNING` de uma regra, `OLD` e `NEW` se referem às pseudorelações adicionadas como entradas de tabela de intervalo extra à consulta reescrita, e não às linhas antigas ou novas na relação de resultado. Assim, por exemplo, em uma regra que suporte consultas `UPDATE` neste visual, se a cláusula `RETURNING` contivesse `old.sl_name`, o nome antigo seria sempre retornado, independentemente de a cláusula `RETURNING` na consulta sobre o visual especificar `OLD` ou `NEW`, o que poderia ser confuso. Para evitar essa confusão e suportar o retorno de valores antigos e novos em consultas sobre o visual, a cláusula `RETURNING` na definição da regra deve se referir a entradas da relação de resultado, como `shoelace_data.sl_name`, sem especificar `OLD` ou `NEW`.

Agora, suponha que de vez em quando, um pacote de cordões de sapato chega à loja e junto com ele, uma grande lista de peças. Mas você não quer atualizar manualmente a visão `shoelace` toda vez. Em vez disso, configuramos duas tabelas pequenas: uma onde você pode inserir os itens da lista de peças, e outra com um truque especial. Os comandos de criação para essas são:

```
CREATE TABLE shoelace_arrive (
    arr_name    text,
    arr_quant   integer
);

CREATE TABLE shoelace_ok (
    ok_name     text,
    ok_quant    integer
);

CREATE RULE shoelace_ok_ins AS ON INSERT TO shoelace_ok
    DO INSTEAD
    UPDATE shoelace
       SET sl_avail = sl_avail + NEW.ok_quant
     WHERE sl_name = NEW.ok_name;
```

Agora você pode preencher a tabela `shoelace_arrive` com os dados da lista de peças:

```
SELECT * FROM shoelace_arrive;

 arr_name | arr_quant
----------+-----------
 sl3      |        10
 sl6      |        20
 sl8      |        20
(3 rows)
```

Dê uma olhada rápida nos dados atuais:

```
SELECT * FROM shoelace;

 sl_name  | sl_avail | sl_color | sl_len | sl_unit | sl_len_cm
----------+----------+----------+--------+---------+-----------
 sl1      |        5 | black    |     80 | cm      |        80
 sl2      |        6 | black    |    100 | cm      |       100
 sl7      |        6 | brown    |     60 | cm      |        60
 sl3      |        0 | black    |     35 | inch    |      88.9
 sl4      |        8 | black    |     40 | inch    |     101.6
 sl8      |        1 | brown    |     40 | inch    |     101.6
 sl5      |        4 | brown    |      1 | m       |       100
 sl6      |        0 | brown    |    0.9 | m       |        90
(8 rows)
```

Agora, mova as meias chegadas para:

```
INSERT INTO shoelace_ok SELECT * FROM shoelace_arrive;
```

e verifique os resultados:

```
SELECT * FROM shoelace ORDER BY sl_name;

 sl_name  | sl_avail | sl_color | sl_len | sl_unit | sl_len_cm
----------+----------+----------+--------+---------+-----------
 sl1      |        5 | black    |     80 | cm      |        80
 sl2      |        6 | black    |    100 | cm      |       100
 sl7      |        6 | brown    |     60 | cm      |        60
 sl4      |        8 | black    |     40 | inch    |     101.6
 sl3      |       10 | black    |     35 | inch    |      88.9
 sl8      |       21 | brown    |     40 | inch    |     101.6
 sl5      |        4 | brown    |      1 | m       |       100
 sl6      |       20 | brown    |    0.9 | m       |        90
(8 rows)

SELECT * FROM shoelace_log;

 sl_name | sl_avail | log_who| log_when
---------+----------+--------+----------------------------------
 sl7     |        6 | Al     | Tue Oct 20 19:14:45 1998 MET DST
 sl3     |       10 | Al     | Tue Oct 20 19:25:16 1998 MET DST
 sl6     |       20 | Al     | Tue Oct 20 19:25:16 1998 MET DST
 sl8     |       21 | Al     | Tue Oct 20 19:25:16 1998 MET DST
(4 rows)
```

É um longo caminho de `INSERT ... SELECT` até esses resultados. E a descrição da transformação da árvore de consulta será a última deste capítulo. Primeiro, há a saída do analisador:

```
INSERT INTO shoelace_ok
SELECT shoelace_arrive.arr_name, shoelace_arrive.arr_quant
  FROM shoelace_arrive shoelace_arrive, shoelace_ok shoelace_ok;
```

Agora, a primeira regra `shoelace_ok_ins` é aplicada e se transforma em:

```
UPDATE shoelace
   SET sl_avail = shoelace.sl_avail + shoelace_arrive.arr_quant
  FROM shoelace_arrive shoelace_arrive, shoelace_ok shoelace_ok,
       shoelace_ok old, shoelace_ok new,
       shoelace shoelace
 WHERE shoelace.sl_name = shoelace_arrive.arr_name;
```

e descarta o original `INSERT` em `shoelace_ok`. Esta consulta reescrita é passada novamente para o sistema de regras, e a segunda regra aplicada `shoelace_upd` produz:

```
UPDATE shoelace_data
   SET sl_name = shoelace.sl_name,
       sl_avail = shoelace.sl_avail + shoelace_arrive.arr_quant,
       sl_color = shoelace.sl_color,
       sl_len = shoelace.sl_len,
       sl_unit = shoelace.sl_unit
  FROM shoelace_arrive shoelace_arrive, shoelace_ok shoelace_ok,
       shoelace_ok old, shoelace_ok new,
       shoelace shoelace, shoelace old,
       shoelace new, shoelace_data shoelace_data
 WHERE shoelace.sl_name = shoelace_arrive.arr_name
   AND shoelace_data.sl_name = shoelace.sl_name;
```

Novamente, é uma regra `INSTEAD` e a árvore de consulta anterior está descartada. Note que essa consulta ainda usa a visão `shoelace`. Mas o sistema de regras não está terminado com essa etapa, então ele continua e aplica a regra `_RETURN` sobre ela, e obtemos:

```
UPDATE shoelace_data
   SET sl_name = s.sl_name,
       sl_avail = s.sl_avail + shoelace_arrive.arr_quant,
       sl_color = s.sl_color,
       sl_len = s.sl_len,
       sl_unit = s.sl_unit
  FROM shoelace_arrive shoelace_arrive, shoelace_ok shoelace_ok,
       shoelace_ok old, shoelace_ok new,
       shoelace shoelace, shoelace old,
       shoelace new, shoelace_data shoelace_data,
       shoelace old, shoelace new,
       shoelace_data s, unit u
 WHERE s.sl_name = shoelace_arrive.arr_name
   AND shoelace_data.sl_name = s.sl_name;
```

Por fim, a regra `log_shoelace` é aplicada, produzindo a árvore de consulta extra:

```
INSERT INTO shoelace_log
SELECT s.sl_name,
       s.sl_avail + shoelace_arrive.arr_quant,
       current_user,
       current_timestamp
  FROM shoelace_arrive shoelace_arrive, shoelace_ok shoelace_ok,
       shoelace_ok old, shoelace_ok new,
       shoelace shoelace, shoelace old,
       shoelace new, shoelace_data shoelace_data,
       shoelace old, shoelace new,
       shoelace_data s, unit u,
       shoelace_data old, shoelace_data new
       shoelace_log shoelace_log
 WHERE s.sl_name = shoelace_arrive.arr_name
   AND shoelace_data.sl_name = s.sl_name
   AND (s.sl_avail + shoelace_arrive.arr_quant) <> s.sl_avail;
```

Depois disso, o sistema de regras esgota as regras e retorna as árvores de consulta geradas.

Então, acabamos com dois árvores de consulta finais que são equivalentes às declarações SQL:

```
INSERT INTO shoelace_log
SELECT s.sl_name,
       s.sl_avail + shoelace_arrive.arr_quant,
       current_user,
       current_timestamp
  FROM shoelace_arrive shoelace_arrive, shoelace_data shoelace_data,
       shoelace_data s
 WHERE s.sl_name = shoelace_arrive.arr_name
   AND shoelace_data.sl_name = s.sl_name
   AND s.sl_avail + shoelace_arrive.arr_quant <> s.sl_avail;

UPDATE shoelace_data
   SET sl_avail = shoelace_data.sl_avail + shoelace_arrive.arr_quant
  FROM shoelace_arrive shoelace_arrive,
       shoelace_data shoelace_data,
       shoelace_data s
 WHERE s.sl_name = shoelace_arrive.sl_name
   AND shoelace_data.sl_name = s.sl_name;
```

O resultado é que dados que vêm de uma relação inserida em outra, transformados em atualizações em um terceiro, transformados em atualizações em um quarto e mais o registro desse último update em um quinto, são reduzidos em duas consultas.

Há um pequeno detalhe que é um pouco feio. Ao analisar as duas consultas, verifica-se que a relação `shoelace_data` aparece duas vezes na tabela de intervalo, onde definitivamente poderia ser reduzida a uma. O planejador não a trata e, portanto, o plano de execução para a saída dos sistemas de regras do `INSERT` será

```
Nested Loop
  ->  Merge Join
        ->  Seq Scan
              ->  Sort
                    ->  Seq Scan on s
        ->  Seq Scan
              ->  Sort
                    ->  Seq Scan on shoelace_arrive
  ->  Seq Scan on shoelace_data
```

enquanto a omissão da entrada da tabela de alcance extra resultaria em

```
Merge Join
  ->  Seq Scan
        ->  Sort
              ->  Seq Scan on s
  ->  Seq Scan
        ->  Sort
              ->  Seq Scan on shoelace_arrive
```

que produz exatamente as mesmas entradas na tabela de registro. Assim, o sistema de regras causou um varredura extra na tabela `shoelace_data` que é absolutamente desnecessária. E o mesmo varredura redundante é feito mais uma vez no `UPDATE`. Mas foi um trabalho realmente difícil fazer tudo isso.

Agora, vamos fazer uma demonstração final do sistema de regras do PostgreSQL e seu poder. Digamos que você adicione algumas cordas de sapato com cores extraordinárias ao seu banco de dados:

```
INSERT INTO shoelace VALUES ('sl9', 0, 'pink', 35.0, 'inch', 0.0);
INSERT INTO shoelace VALUES ('sl10', 1000, 'magenta', 40.0, 'inch', 0.0);
```

Gostamos de fazer uma visualização para verificar quais entradas do `shoelace` não correspondem a nenhum sapato na cor. A visualização para isso é:

```
CREATE VIEW shoelace_mismatch AS
    SELECT * FROM shoelace WHERE NOT EXISTS
        (SELECT shoename FROM shoe WHERE slcolor = sl_color);
```

Sua saída é:

```
SELECT * FROM shoelace_mismatch;

 sl_name | sl_avail | sl_color | sl_len | sl_unit | sl_len_cm
---------+----------+----------+--------+---------+-----------
 sl9     |        0 | pink     |     35 | inch    |      88.9
 sl10    |     1000 | magenta  |     40 | inch    |     101.6
```

Agora, queremos configurá-lo para que os cadarços de sapato que não estão em estoque sejam excluídos do banco de dados. Para dificultar um pouco mais para o PostgreSQL, não os excluímos diretamente. Em vez disso, criamos mais uma visão:

```
CREATE VIEW shoelace_can_delete AS
    SELECT * FROM shoelace_mismatch WHERE sl_avail = 0;
```

e faça da seguinte forma:

```
DELETE FROM shoelace WHERE EXISTS
    (SELECT * FROM shoelace_can_delete
             WHERE sl_name = shoelace.sl_name);
```

Os resultados são:

```
SELECT * FROM shoelace;

 sl_name | sl_avail | sl_color | sl_len | sl_unit | sl_len_cm
---------+----------+----------+--------+---------+-----------
 sl1     |        5 | black    |     80 | cm      |        80
 sl2     |        6 | black    |    100 | cm      |       100
 sl7     |        6 | brown    |     60 | cm      |        60
 sl4     |        8 | black    |     40 | inch    |     101.6
 sl3     |       10 | black    |     35 | inch    |      88.9
 sl8     |       21 | brown    |     40 | inch    |     101.6
 sl10    |     1000 | magenta  |     40 | inch    |     101.6
 sl5     |        4 | brown    |      1 | m       |       100
 sl6     |       20 | brown    |    0.9 | m       |        90
(9 rows)
```

Um `DELETE` em uma visão, com uma qualificação de subconsulta que, no total, utiliza 4 vistas aninhadas/juntas, onde uma delas possui uma qualificação de subconsulta que contém uma visão e onde as colunas de visão calculadas são usadas, é reescrito em uma única árvore de consulta que exclui os dados solicitados de uma tabela real.

Provavelmente, há apenas algumas situações no mundo real onde tal construção é necessária. Mas faz você se sentir confortável com o fato de que ela funciona.