## Crie Sequência

CREATE SEQUENCE — definir um novo gerador de sequência

## Sinopse

```
CREATE [ { TEMPORARY | TEMP } | UNLOGGED ] SEQUENCE [ IF NOT EXISTS ] name
    [ AS data_type ]
    [ INCREMENT [ BY ] increment ]
    [ MINVALUE minvalue | NO MINVALUE ] [ MAXVALUE maxvalue | NO MAXVALUE ]
    [ [ NO ] CYCLE ]
    [ START [ WITH ] start ]
    [ CACHE cache ]
    [ OWNED BY { table_name.column_name | NONE } ]
```

## Descrição

`CREATE SEQUENCE` cria um novo gerador de número de sequência. Isso envolve a criação e inicialização de uma nova tabela especial de uma única linha com o nome *`name`*. O gerador será de propriedade do usuário que emite o comando.

Se um nome de esquema for fornecido, a sequência será criada no esquema especificado. Caso contrário, será criada no esquema atual. Sequências temporárias existem em um esquema especial, portanto, não é possível fornecer um nome de esquema ao criar uma sequência temporária. O nome da sequência deve ser distinto do nome de qualquer outra relação (tabela, sequência, índice, visão, visão materializada ou tabela externa) no mesmo esquema.

Após a criação de uma sequência, você usa as funções `nextval`, `currval` e `setval` para operar na sequência. Essas funções estão documentadas em [Seção 9.17][(functions-sequence.md "9.17. Sequence Manipulation Functions")].

Embora você não possa atualizar uma sequência diretamente, você pode usar uma consulta como:

```
SELECT * FROM name;
```

para examinar os parâmetros e o estado atual de uma sequência. Em particular, o campo `last_value` da sequência mostra o último valor atribuído por qualquer sessão. (É claro que esse valor pode estar obsoleto no momento em que é impresso, se outras sessões estiverem realizando chamadas `nextval` ativamente.)

## Parâmetros

`TEMPORARY` ou `TEMP`: Se especificado, o objeto de sequência é criado apenas para esta sessão e é automaticamente descartado na saída da sessão. As sequências permanentes existentes com o mesmo nome não são visíveis (na sessão) enquanto a sequência temporária existir, a menos que sejam referenciadas com nomes qualificados pelo esquema.

`UNLOGGED`: Se especificado, a sequência é criada como uma sequência não registrada. As alterações em sequências não registradas não são escritas no log de pré-escrita. Elas não são seguras em caso de falha: uma sequência não registrada é automaticamente redefinida para seu estado inicial após uma falha ou desligamento não limpo. Sequências não registradas também não são replicadas para servidores de espera.

Ao contrário das tabelas não registradas, as sequências não registradas não oferecem uma vantagem significativa de desempenho. Esta opção é destinada principalmente a sequências associadas a tabelas não registradas por meio de colunas de identidade ou colunas serializadas. Nesses casos, geralmente não faz sentido ter a sequência registrada no WAL e replicada, mas não sua tabela associada.

`IF NOT EXISTS`: Não exija um erro se uma relação com o mesmo nome já existir. Neste caso, é emitido um aviso. Observe que não há garantia de que a relação existente seja algo semelhante à sequência que teria sido criada — ela pode não ser sequencia.

*`name`*: O nome (opcionalmente qualificado por esquema) da sequência a ser criada.

*`data_type`*: A cláusula opcional `AS data_type` especifica o tipo de dados da sequência. Os tipos válidos são `smallint`, `integer` e `bigint`. `bigint` é o padrão. O tipo de dados determina os valores mínimo e máximo padrão da sequência.

*`increment`*: A cláusula opcional `INCREMENT BY increment` especifica qual valor é adicionado ao valor atual da sequência para criar um novo valor. Um valor positivo criará uma sequência ascendente, um valor negativo uma sequência descendente. O valor padrão é 1.

*`minvalue`* `NO MINVALUE`: A cláusula opcional `MINVALUE minvalue` determina o valor mínimo que uma sequência pode gerar. Se esta cláusula não for fornecida ou se `NO MINVALUE` for especificado, então os padrões serão usados. O padrão para uma sequência ascendente é 1. O padrão para uma sequência descendente é o valor mínimo do tipo de dados.

*`maxvalue` `NO MAXVALUE`: A cláusula opcional `MAXVALUE maxvalue` determina o valor máximo para a sequência. Se esta cláusula não for fornecida ou se `NO MAXVALUE` for especificado, os valores padrão serão utilizados. O padrão para uma sequência ascendente é o valor máximo do tipo de dados. O padrão para uma sequência descendente é -1.

`CYCLE` `NO CYCLE`: A opção `CYCLE` permite que a sequência se repita quando o *`maxvalue`* ou *`minvalue`* é alcançado por uma sequência ascendente ou descendente, respectivamente. Se o limite for atingido, o próximo número gerado será o *`minvalue`* ou *`maxvalue`*, respectivamente.

Se `NO CYCLE` for especificado, quaisquer chamadas para `nextval` após a sequência ter atingido seu valor máximo retornarão um erro. Se nem `CYCLE` nem `NO CYCLE` forem especificados, `NO CYCLE` é o padrão.

*`start`*: A cláusula opcional `START WITH start` permite que a sequência comece em qualquer lugar. O valor inicial padrão é *`minvalue`* para sequências ascendentes e *`maxvalue`* para as descendentes.

*`cache`*: A cláusula opcional `CACHE cache` especifica quantos números de sequência devem ser pré-alocados e armazenados na memória para acesso mais rápido. O valor mínimo é 1 (apenas um valor pode ser gerado de cada vez, ou seja, sem cache), e este também é o padrão.

`OWNED BY` *`table_name`*.*`column_name`* `OWNED BY NONE`: A opção `OWNED BY` faz com que a sequência seja associada a uma coluna específica da tabela, de modo que, se essa coluna (ou toda a tabela) for excluída, a sequência também será automaticamente excluída. A tabela especificada deve ter o mesmo proprietário e estar no mesmo esquema que a sequência. `OWNED BY NONE`, o padrão, especifica que não há essa associação.

## Notas

Use `DROP SEQUENCE` para remover uma sequência.

As sequências são baseadas em aritmética `bigint`, portanto, a faixa não pode exceder a faixa de um inteiro de oito bytes (-9223372036854775808 a 9223372036854775807).

Como as chamadas `nextval` e `setval` nunca são revertidas, os objetos de sequência não podem ser usados se for necessária uma atribuição "sem lacunas" de números de sequência. É possível construir uma atribuição sem lacunas usando bloqueio exclusivo de uma tabela que contenha um contador; mas essa solução é muito mais cara do que os objetos de sequência, especialmente se muitas transações precisam de números de sequência simultaneamente.

Resultados inesperados podem ser obtidos se um *`cache`* com um valor maior que um for utilizado para um objeto de sequência que será utilizado simultaneamente por múltiplas sessões. Cada sessão alocará e cacheá-lo-á valores sucessivos de sequência durante um acesso ao objeto de sequência e aumentará o `last_value` do objeto de sequência de acordo. Em seguida, as próximas utilizações de *`cache`*-1 do `nextval` dentro dessa sessão simplesmente retornarão os valores pré-alocados sem tocar no objeto de sequência. Assim, quaisquer números alocados, mas não utilizados dentro de uma sessão, serão perdidos quando essa sessão terminar, resultando em "buracos" na sequência.

Além disso, embora múltiplas sessões garantam a alocação de valores de sequência distintos, os valores podem ser gerados fora de sequência quando todas as sessões são consideradas. Por exemplo, com um *`cache`* de 10, a sessão A pode reservar valores de 1 a 10 e retornar `nextval`=1, então a sessão B pode reservar valores de 11 a 20 e retornar `nextval`=11 antes que a sessão A tenha gerado `nextval`=2. Assim, com um *`cache`* de um, é seguro assumir que os valores de `nextval` são gerados sequencialmente; com um *`cache`* maior que um, você deve apenas assumir que os valores de `nextval` são todos distintos, não que eles são gerados puramente sequencialmente. Além disso, `last_value` refletirá o último valor reservado por qualquer sessão, independentemente de ter sido retornado ou não por `nextval`.

Outra consideração é que uma `setval` executada em tal sequência não será notada por outras sessões até que elas tenham esgotado quaisquer valores pré-alocados que tenham sido cacheados.

## Exemplos

Crie uma sequência ascendente chamada `serial`, começando em 101:

```
CREATE SEQUENCE serial START 101;
```

Selecione o próximo número desta sequência:

```
SELECT nextval('serial');

 nextval
---------
     101
```

Selecione o próximo número desta sequência:

```
SELECT nextval('serial');

 nextval
---------
     102
```

Use essa sequência em um comando `INSERT`.

```
INSERT INTO distributors VALUES (nextval('serial'), 'nothing');
```

Atualize o valor da sequência após um `COPY FROM`:

```
BEGIN;
COPY distributors FROM 'input_file';
SELECT setval('serial', max(id)) FROM distributors;
END;
```

## Compatibilidade

`CREATE SEQUENCE` está em conformidade com o padrão SQL, com as seguintes exceções:

* A obtenção do próximo valor é feita usando a função `nextval()` em vez da expressão `NEXT VALUE FOR` padrão.
* A cláusula `OWNED BY` é uma extensão do PostgreSQL.

## Veja também

[ALTER SEQUÊNCIA](sql-altersequence.md "ALTER SEQUENCE"), [DROP SEQUÊNCIA](sql-dropsequence.md "DROP SEQUENCE")