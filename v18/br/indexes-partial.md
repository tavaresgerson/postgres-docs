## 11.8. Índices Parciais [#](#INDEXES-PARTIAL)

Um *índice parcial* é um índice construído sobre um subconjunto de uma tabela; o subconjunto é definido por uma expressão condicional (chamada de *predicado* do índice parcial). O índice contém entradas apenas para as linhas da tabela que satisfazem o predicado. Os índices parciais são uma característica especializada, mas há várias situações em que eles são úteis.

Uma das principais razões para usar um índice parcial é evitar indexar valores comuns. Como uma consulta que busca um valor comum (um que representa mais de alguns por cento de todas as linhas da tabela) não usará o índice de qualquer maneira, não há sentido em manter essas linhas no índice. Isso reduz o tamanho do índice, o que acelerará as consultas que usam o índice. Também acelerará muitas operações de atualização de tabela, porque o índice não precisa ser atualizado em todos os casos. [Exemplo 11.1] [(indexes-partial.md#INDEXES-PARTIAL-EX1 "Example 11.1. Setting up a Partial Index to Exclude Common Values")] mostra uma possível aplicação dessa ideia.

**Exemplo 11.1. Configurando um Índice Parcial para Excluir Valores Comuns**

Suponha que você esteja armazenando logs de acesso do servidor web em um banco de dados. A maioria dos acessos provém do intervalo de endereços IP da sua organização, mas alguns vêm de outros lugares (digamos, funcionários com conexões dial-up). Se suas pesquisas por IP são principalmente para acessos externos, provavelmente não precisa indexar o intervalo de IP que corresponde à sub-rede da sua organização.

Suponha uma tabela como esta:

```
CREATE TABLE access_log (
    url varchar,
    client_ip inet,
    ...
);
```

Para criar um índice parcial que se adeque ao nosso exemplo, use um comando como este:

```
CREATE INDEX access_log_client_ip_ix ON access_log (client_ip)
WHERE NOT (client_ip > inet '192.168.100.0' AND
           client_ip < inet '192.168.100.255');
```

Uma consulta típica que pode usar esse índice seria:

```
SELECT *
FROM access_log
WHERE url = '/index.html' AND client_ip = inet '212.78.10.32';
```

Aqui, o endereço IP da consulta é coberto pelo índice parcial. A consulta a seguir não pode usar o índice parcial, pois utiliza um endereço IP que está excluído do índice:

```
SELECT *
FROM access_log
WHERE url = '/index.html' AND client_ip = inet '192.168.100.23';
```

Observe que esse tipo de índice parcial exige que os valores comuns sejam predeterminados, portanto, esses índices parciais são os melhores para distribuições de dados que não mudam. Esses índices podem ser recriados ocasionalmente para ajustar-se a novas distribuições de dados, mas isso adiciona esforço de manutenção.

  

Outro uso possível para um índice parcial é excluir valores do índice que o volume de trabalho típico de consulta não está interessado; isso é mostrado em [Exemplo 11.2][(indexes-partial.md#INDEXES-PARTIAL-EX2 "Example 11.2. Setting up a Partial Index to Exclude Uninteresting Values")]. Isso resulta nas mesmas vantagens listadas acima, mas impede que os valores “não interessantes” sejam acessados por meio desse índice, mesmo que uma varredura de índice possa ser lucrativa nesse caso. Obviamente, configurar índices parciais para esse tipo de cenário exigirá muito cuidado e experimentação.

**Exemplo 11.2. Configurando um índice parcial para excluir valores sem interesse**

Se você tem uma tabela que contém tanto pedidos faturados quanto não faturados, onde os pedidos não faturados ocupam uma pequena fração do total da tabela e, no entanto, são as linhas mais acessadas, você pode melhorar o desempenho criando um índice apenas nas linhas não faturadas. O comando para criar o índice seria o seguinte:

```
CREATE INDEX orders_unbilled_index ON orders (order_nr)
    WHERE billed is not true;
```

Uma consulta possível para usar esse índice seria:

```
SELECT * FROM orders WHERE billed is not true AND order_nr < 10000;
```

No entanto, o índice também pode ser usado em consultas que não envolvem `order_nr` de forma alguma, por exemplo:

```
SELECT * FROM orders WHERE billed is not true AND amount > 5000.00;
```

Isso não é tão eficiente quanto um índice parcial na coluna `amount`, pois o sistema tem que percorrer todo o índice. No entanto, se houver relativamente poucas ordens não faturadas, usar esse índice parcial apenas para encontrar as ordens não faturadas pode ser uma vantagem.

Observe que esta consulta não pode usar este índice:

```
SELECT * FROM orders WHERE order_nr = 3501;
```

O pedido 3501 pode estar entre os pedidos faturados ou não faturados.

  

[Exemplo 11.2][(indexes-partial.md#INDEXES-PARTIAL-EX2 "Example 11.2. Setting up a Partial Index to Exclude Uninteresting Values")] também ilustra que a coluna indexada e a coluna usada no predicado não precisam corresponder. O PostgreSQL suporta índices parciais com predicados arbitrários, desde que apenas as colunas da tabela que está sendo indexada estejam envolvidas. No entanto, tenha em mente que o predicado deve corresponder às condições usadas nas consultas que devem se beneficiar do índice. Para ser preciso, um índice parcial pode ser usado em uma consulta apenas se o sistema puder reconhecer que a condição `WHERE` da consulta implica matematicamente o predicado do índice. O PostgreSQL não tem um provador de teoremas sofisticado que possa reconhecer expressões matematicamente equivalentes que são escritas em diferentes formas. (Não só é extremamente difícil criar um provador de teoremas tão geral, como provavelmente seria muito lento para ter qualquer uso real.) O sistema pode reconhecer simples implicações de desigualdade, por exemplo, “x < 1” implica “x < 2”; caso contrário, a condição do predicado deve corresponder exatamente a parte da condição `WHERE` da consulta ou o índice não será reconhecido como utilizável. A correspondência ocorre no momento do planejamento da consulta, não no momento da execução. Como resultado, as cláusulas de consulta parametrizadas não funcionam com um índice parcial. Por exemplo, uma consulta preparada com um parâmetro pode especificar “x < ?” que nunca implicará “x < 2” para todos os valores possíveis do parâmetro.

Um terceiro uso possível para índices parciais não exige que o índice seja usado em consultas. A ideia aqui é criar um índice único sobre um subconjunto de uma tabela, como no [Exemplo 11.3][(indexes-partial.md#INDEXES-PARTIAL-EX3 "Example 11.3. Setting up a Partial Unique Index")]. Isso garante a unicidade entre as linhas que satisfazem o predicado do índice, sem restringir aquelas que não o fazem.

**Exemplo 11.3. Configuração de um índice único parcial**

Suponha que tenhamos uma tabela que descreve os resultados dos testes. Queremos garantir que haja apenas uma entrada "sucesso" para uma combinação específica de assunto e alvo, mas pode haver qualquer número de entradas "não bem-sucedidas". Aqui está uma maneira de fazer isso:

```
CREATE TABLE tests (
    subject text,
    target text,
    success boolean,
    ...
);

CREATE UNIQUE INDEX tests_success_constraint ON tests (subject, target)
    WHERE success;
```

Essa é uma abordagem particularmente eficiente quando há poucos testes bem-sucedidos e muitos não bem-sucedidos. Também é possível permitir apenas um nulo em uma coluna, criando um índice parcial único com uma restrição `IS NULL`.

  

Por fim, um índice parcial também pode ser usado para substituir as escolhas do plano de consulta do sistema. Além disso, os conjuntos de dados com distribuições peculiares podem fazer com que o sistema use um índice quando realmente não deveria. Nesse caso, o índice pode ser configurado para que não esteja disponível para a consulta que causa problemas. Normalmente, o PostgreSQL faz escolhas razoáveis sobre o uso de índices (por exemplo, evita-os ao recuperar valores comuns, então o exemplo anterior realmente só salva o tamanho do índice, não é necessário evitar o uso de índice), e escolhas de plano grosseiramente incorretas são motivo de um relatório de bug.

Tenha em mente que configurar um índice parcial indica que você sabe pelo menos tanto quanto o planejador de consulta, em particular, sabe quando um índice pode ser lucrativo. Formar esse conhecimento requer experiência e entendimento de como os índices no PostgreSQL funcionam. Na maioria dos casos, a vantagem de um índice parcial em relação a um índice regular será mínima. Há casos em que eles são bastante contraproducentes, como no [Exemplo 11.4] [(indexes-partial.md#INDEXES-PARTIAL-EX4 "Example 11.4. Do Not Use Partial Indexes as a Substitute for Partitioning")].

**Exemplo 11.4. Não use índices parciais como substituto para particionamento**

Você pode ser tentado a criar um grande conjunto de índices parciais que não se sobrepõem, por exemplo

```
CREATE INDEX mytable_cat_1 ON mytable (data) WHERE category = 1;
CREATE INDEX mytable_cat_2 ON mytable (data) WHERE category = 2;
CREATE INDEX mytable_cat_3 ON mytable (data) WHERE category = 3;
...
CREATE INDEX mytable_cat_N ON mytable (data) WHERE category = N;
```

Essa é uma má ideia! Provavelmente, você terá mais sucesso com um único índice não parcial, declarado como

```
CREATE INDEX mytable_cat_data ON mytable (category, data);
```

(Coloque a coluna de categoria primeiro, pelas razões descritas em [Seção 11.3] (indexes-multicolumn.md "11.3. Multicolumn Indexes").). Embora uma pesquisa neste índice maior possa ter que descer por um par de níveis de árvore a mais do que uma pesquisa em um índice menor, isso quase certamente será mais barato do que o esforço do planejador necessário para selecionar o parcial índice apropriado. O cerne do problema é que o sistema não entende a relação entre os índices parciais e trabalhará arduamente para testar cada um deles para ver se é aplicável à consulta atual.

Se a sua tabela for grande o suficiente para que um único índice realmente seja uma má ideia, você deve considerar o uso de particionamento (consulte [Seção 5.12][(ddl-partitioning.md "5.12. Table Partitioning")]). Com esse mecanismo, o sistema entende que as tabelas e os índices não se sobrepõem, permitindo um desempenho ainda melhor.

  

Mais informações sobre índices parciais podem ser encontradas em [[ston89b]](biblio.md#STON89B), [[olson93]](biblio.md#OLSON93 "Partial indexing in POSTGRES: research project") e [[seshadri95]](biblio.md#SESHADRI95).