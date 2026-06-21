## 39.7. Regras versus gatilhos [#](#RULES-TRIGGERS)

Muitas coisas que podem ser feitas usando gatilhos também podem ser implementadas usando o sistema de regras do PostgreSQL. Uma das coisas que não podem ser implementadas por regras são alguns tipos de restrições, especialmente as chaves estrangeiras. É possível colocar uma regra qualificada que reescreve um comando para `NOTHING` se o valor de uma coluna não aparecer em outra tabela. Mas, então, os dados são silenciosamente descartados e isso não é uma boa ideia. Se verificações de valores válidos são necessárias e, no caso de um valor inválido, deve ser gerada uma mensagem de erro, isso deve ser feito por um gatilho.

Neste capítulo, focamos no uso de regras para atualizar visualizações. Todos os exemplos de regras de atualização neste capítulo também podem ser implementados usando gatilhos `INSTEAD OF` nas visualizações. Escrever tais gatilhos é muitas vezes mais fácil do que escrever regras, especialmente se for necessária lógica complexa para realizar a atualização.

Para as coisas que podem ser implementadas por ambos, o que é melhor depende do uso do banco de dados. Um gatilho é disparado uma vez para cada linha afetada. Uma regra modifica a consulta ou gera uma consulta adicional. Portanto, se muitas linhas são afetadas em uma declaração, uma regra que emite um comando extra é provavelmente mais rápida do que um gatilho que é chamado para cada linha individual e deve redefinir o que fazer várias vezes. No entanto, a abordagem do gatilho é conceitualmente muito mais simples do que a abordagem da regra, e é mais fácil para iniciantes entender.

Aqui, mostramos um exemplo de como a escolha de regras versus gatilhos se manifesta em uma situação. Existem duas tabelas:

```
CREATE TABLE computer (
    hostname        text,    -- indexed
    manufacturer    text     -- indexed
);

CREATE TABLE software (
    software        text,    -- indexed
    hostname        text     -- indexed
);
```

Ambas as tabelas têm muitos milhares de linhas e os índices em `hostname` são exclusivos. A regra ou gatilho deve implementar uma restrição que exclua as linhas em `software` que fazem referência a um computador excluído. O gatilho usaria este comando:

```
DELETE FROM software WHERE hostname = $1;
```

Como o gatilho é chamado para cada linha individual excluída do `computer`, ele pode preparar e salvar o plano para este comando e passar o valor do `hostname` no parâmetro. A regra seria escrita da seguinte forma:

```
CREATE RULE computer_del AS ON DELETE TO computer
    DO DELETE FROM software WHERE hostname = OLD.hostname;
```

Agora, vamos analisar diferentes tipos de apagamentos. No caso de:

```
DELETE FROM computer WHERE hostname = 'mypc.local.net';
```

a tabela `computer` é verificada por índice (rápida), e o comando emitido pelo gatilho também usaria uma verificação por índice (também rápida). O comando adicional da regra seria:

```
DELETE FROM software WHERE computer.hostname = 'mypc.local.net'
                       AND software.hostname = computer.hostname;
```

Como há índices adequados configurados, o planejador criará um plano de

```
Nestloop
  ->  Index Scan using comp_hostidx on computer
  ->  Index Scan using soft_hostidx on software
```

Portanto, não haveria muita diferença de velocidade entre o gatilho e a implementação da regra.

Com a próxima exclusão, queremos eliminar todos os 2000 computadores onde o `hostname` começa com `old`. Existem dois comandos possíveis para fazer isso. Um deles é:

```
DELETE FROM computer WHERE hostname >= 'old'
                       AND hostname <  'ole'
```

O comando adicionado pela regra será:

```
DELETE FROM software WHERE computer.hostname >= 'old' AND computer.hostname < 'ole'
                       AND software.hostname = computer.hostname;
```

com o plano

```
Hash Join
  ->  Seq Scan on software
  ->  Hash
    ->  Index Scan using comp_hostidx on computer
```

O outro comando possível é:

```
DELETE FROM computer WHERE hostname ~ '^old';
```

que resulta no seguinte plano de execução para o comando adicionado pela regra:

```
Nestloop
  ->  Index Scan using comp_hostidx on computer
  ->  Index Scan using soft_hostidx on software
```

Isso mostra que o planejador não percebe que a qualificação para `hostname` em `computer` também pode ser usada para uma varredura de índice em `software`, quando há várias expressões de qualificação combinadas com `AND`, o que é o que ele faz na versão de expressão regular do comando. O gatilho será acionado uma vez para cada um dos 2000 computadores antigos que precisam ser excluídos, o que resultará em uma varredura de índice em `computer` e 2000 varreduras de índice em `software`. A implementação da regra será feita com dois comandos que usam índices. E depende do tamanho total da tabela `software` se a regra ainda será mais rápida na situação de varredura sequencial. 2000 execuções de comando do gatilho sobre o gerenciador SPI levam algum tempo, mesmo que todos os blocos de índice logo estejam na cache.

O último comando que analisamos é:

```
DELETE FROM computer WHERE manufacturer = 'bim';
```

Novamente, isso pode resultar na exclusão de muitas linhas do `computer`. Assim, o gatilho executará novamente muitos comandos através do executor. O comando gerado pela regra será:

```
DELETE FROM software WHERE computer.manufacturer = 'bim'
                       AND software.hostname = computer.hostname;
```

O plano para esse comando será novamente o loop aninhado sobre dois varreduras de índice, usando apenas um índice diferente em `computer`:

```
Nestloop
  ->  Index Scan using comp_manufidx on computer
  ->  Index Scan using soft_hostidx on software
```

Em qualquer um desses casos, os comandos adicionais do sistema de regras serão mais ou menos independentes do número de linhas afetadas em um comando.

O resumo é que as regras só serão significativamente mais lentas que os gatilhos se suas ações resultarem em junções grandes e mal qualificadas, uma situação em que o planejador falha.