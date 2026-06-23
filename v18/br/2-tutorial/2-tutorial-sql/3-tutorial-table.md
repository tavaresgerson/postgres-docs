### 2.3. Criando uma Nova Tabela [#](#TUTORIAL-TABLE)

Você pode criar uma nova tabela, especificando o nome da tabela, juntamente com todos os nomes de coluna e seus tipos:

```
CREATE TABLE weather (
    city            varchar(80),
    temp_lo         int,           -- low temperature
    temp_hi         int,           -- high temperature
    prcp            real,          -- precipitation
    date            date
);
```

Você pode inserir isso no `psql` com as pausas de linha. `psql` reconhecerá que o comando não é terminado até o ponto e vírgula.

O espaço em branco (ou seja, espaços, tabs e novas linhas) pode ser usado livremente em comandos SQL. Isso significa que você pode digitar o comando alinhado de maneira diferente do que está acima, ou até mesmo tudo em uma única linha. Duas barras ("`--`") introduzem comentários. Tudo o que segue elas é ignorado até o final da linha. O SQL é insensível a palavras-chave e identificadores, exceto quando os identificadores são citados em duplicado para preservar o caso (não feito acima).

`varchar(80)` especifica um tipo de dados que pode armazenar cadeias de caracteres arbitrárias com até 80 caracteres de comprimento. `int` é o tipo de número inteiro normal. `real` é um tipo para armazenar números de ponto flutuante de precisão única. `date` deve ser autoexplicativo. (Sim, a coluna do tipo `date` também é chamada de `date`. Isso pode ser conveniente ou confuso — você escolhe.)

O PostgreSQL suporta os tipos padrão de SQL `int`, `smallint`, `real`, `double precision`, `char(N)`, `varchar(N)`, `date`, `time`, `timestamp` e `interval`, além de outros tipos de utilidade geral e um conjunto rico de tipos geométricos. O PostgreSQL pode ser personalizado com um número arbitrário de tipos de dados definidos pelo usuário. Consequentemente, os nomes dos tipos não são palavras-chave na sintaxe, exceto onde necessário para suportar casos especiais no padrão SQL.

O segundo exemplo armazenará cidades e suas localizações geográficas associadas:

```
CREATE TABLE cities (
    name            varchar(80),
    location        point
);
```

O tipo `point` é um exemplo de um tipo de dados específico do PostgreSQL.

Por fim, deve-se mencionar que, se você não precisar mais de uma tabela ou deseja recriá-la de maneira diferente, pode removê-la usando o seguinte comando:

```
DROP TABLE tablename;
```
