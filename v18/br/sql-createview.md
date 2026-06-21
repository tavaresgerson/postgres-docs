## CRIAR VISTA

CREATE VIEW — definir uma nova visualização

## Sinopse

```
CREATE [ OR REPLACE ] [ TEMP | TEMPORARY ] [ RECURSIVE ] VIEW name [ ( column_name [, ...] ) ]
    [ WITH ( view_option_name [= view_option_value] [, ... ] ) ]
    AS query
    [ WITH [ CASCADED | LOCAL ] CHECK OPTION ]
```

## Descrição

`CREATE VIEW` define uma visão de uma consulta. A visão não é materializada fisicamente. Em vez disso, a consulta é executada toda vez que a visão é referenciada em uma consulta.

`CREATE OR REPLACE VIEW` é semelhante, mas se uma visão com o mesmo nome já existir, ela é substituída. A nova consulta deve gerar as mesmas colunas que foram geradas pela consulta da visão existente (ou seja, os mesmos nomes de coluna na mesma ordem e com os mesmos tipos de dados), mas pode adicionar colunas adicionais no final da lista. Os cálculos que dão origem às colunas de saída podem ser completamente diferentes.

Se um nome de esquema for fornecido (por exemplo, `CREATE VIEW myschema.myview ...`) então a visualização é criada no esquema especificado. Caso contrário, ela é criada no esquema atual. Visualizações temporárias existem em um esquema especial, portanto, não é possível fornecer um nome de esquema ao criar uma visualização temporária. O nome da visualização deve ser distinto do nome de qualquer outra relação (tabela, sequência, índice, visualização, visualização materializada ou tabela estrangeira) no mesmo esquema.

## Parâmetros

`TEMPORARY` ou `TEMP`: Se especificado, a visualização é criada como uma visualização temporária. As visualizações temporárias são automaticamente descartadas no final da sessão atual. As relações permanentes existentes com o mesmo nome não são visíveis para a sessão atual enquanto a visualização temporária existir, a menos que sejam referenciadas com nomes qualificados pelo esquema.

Se alguma das tabelas referenciadas pela visão for temporária, a visão é criada como uma visão temporária (se `TEMPORARY` for especificado ou não).

`RECURSIVE`: Cria uma visão recursiva. A sintaxe

``` CREATE RECURSIVE VIEW [ schema . ] view_name (column_names) AS SELECT ...;
    ```

é equivalente a

    ```
    CREATE VIEW [ schema . ] view_name AS WITH RECURSIVE view_name (column_names) AS (SELECT ...) SELECT column_names FROM view_name;
    ```

Uma lista de nome de coluna de visualização deve ser especificada para uma visualização recursiva.

*`name`*: O nome (opcionalmente qualificado por esquema) de uma visão a ser criada.

*`column_name`*: Uma lista opcional de nomes a serem usados para as colunas da visualização. Se não for fornecida, os nomes das colunas são deduzidos da consulta.

`WITH ( view_option_name [= view_option_value] [, ... ] )`: Esta cláusula especifica parâmetros opcionais para uma visualização; os seguintes parâmetros são suportados:

`check_option` (`enum`) : Este parâmetro pode ser `local` ou `cascaded`, e é equivalente a especificar `WITH [ CASCADED | LOCAL ] CHECK OPTION` (veja abaixo).

`security_barrier` (`boolean`) :   Isso deve ser usado se a visão estiver destinada a fornecer segurança em nível de linha. Consulte [Seção 39.5](rules-privileges.md "39.5. Rules and Privileges") para obter detalhes completos.

`security_invoker` (`boolean`) :  Esta opção faz com que as relações de base subjacentes sejam verificadas em relação aos privilégios do usuário da visualização, em vez do proprietário da visualização. Consulte as notas abaixo para obter detalhes completos.

Todas as opções acima podem ser alteradas em visualizações existentes usando `ALTER VIEW`(sql-alterview.md "ALTER VIEW").

*`query`*: Um comando [`SELECT`](sql-select.md "SELECT") ou [`VALUES`](sql-values.md "VALUES") que fornecerá as colunas e linhas da visualização.

`WITH [ CASCADED | LOCAL ] CHECK OPTION`: Esta opção controla o comportamento das visualizações automaticamente atualizáveis. Quando esta opção é especificada, os comandos `INSERT`, `UPDATE` e `MERGE` na visualização serão verificados para garantir que as novas linhas satisfaçam a condição que define a visualização (ou seja, as novas linhas são verificadas para garantir que sejam visíveis através da visualização). Se não forem, a atualização será rejeitada. Se o `CHECK OPTION` não for especificado, os comandos `INSERT`, `UPDATE` e `MERGE` na visualização podem criar linhas que não são visíveis através da visualização. As seguintes opções de verificação são suportadas:

`LOCAL` :   As novas linhas são verificadas apenas contra as condições definidas diretamente na própria visualização. Quaisquer condições definidas em visualizações base subjacentes não são verificadas (a menos que também especifiquem o `CHECK OPTION`).

`CASCADED` :   Novas linhas são verificadas em relação às condições da visualização e de todas as visualizações de base subjacentes. Se o `CHECK OPTION` for especificado e nem o `LOCAL` nem o `CASCADED` forem especificados, então o `CASCADED` é assumido.

O `CHECK OPTION` não pode ser usado com as visualizações do `RECURSIVE`.

Observe que o `CHECK OPTION` é suportado apenas em visualizações que são automaticamente atualizáveis e não possuem gatilhos `INSTEAD OF` ou regras `INSTEAD`. Se uma visualização automaticamente atualizável for definida sobre uma visualização base que tenha gatilhos `INSTEAD OF`, então o `LOCAL CHECK OPTION` pode ser usado para verificar as condições na visualização automaticamente atualizável, mas as condições na visualização base com gatilhos `INSTEAD OF` não serão verificadas (uma opção de verificação em cascata não se castiga para uma visualização atualizável por gatilho, e quaisquer opções de verificação definidas diretamente em uma visualização atualizável por gatilho serão ignoradas). Se a visualização ou qualquer uma de suas relações base tiver uma regra `INSTEAD` que faça com que o comando `INSERT` ou `UPDATE` seja reescrito, então todas as opções de verificação serão ignoradas na consulta reescrita, incluindo quaisquer verificações de visualizações automaticamente atualizáveis definidas sobre a relação com a regra `INSTEAD`. O `MERGE` não é suportado se a visualização ou qualquer uma de suas relações base tiverem regras.

## Notas

Use a declaração `DROP VIEW`(sql-dropview.md "DROP VIEW") para descartar visualizações.

Tenha cuidado para que os nomes e os tipos das colunas da visualização sejam atribuídos da maneira que você deseja. Por exemplo:

```
CREATE VIEW vista AS SELECT 'Hello World';
```

é uma má prática, pois o nome da coluna por padrão é `?column?`; além disso, o tipo de dados da coluna por padrão é `text`, o que pode não ser o que você queria. Um estilo melhor para uma literal de string em um resultado de uma visualização é algo como:

```
CREATE VIEW vista AS SELECT text 'Hello World' AS hello;
```

Por padrão, o acesso às relações subjacentes referenciadas na visualização é determinado pelas permissões do proprietário da visualização. Em alguns casos, isso pode ser usado para fornecer acesso seguro, mas restrito, às tabelas subjacentes. No entanto, nem todas as visualizações são seguras contra manipulações; consulte [Seção 39.5][(rules-privileges.md "39.5. Rules and Privileges")] para obter detalhes.

Se a vista tiver a propriedade `security_invoker` definida como `true`, o acesso às relações de base subjacentes é determinado pelas permissões do usuário que executa a consulta, e não pelo proprietário da vista. Assim, o usuário de uma vista de invocação de segurança deve ter as permissões relevantes na vista e nas suas relações de base subjacentes.

Se qualquer uma das relações de base subjacentes for uma visualização de invocação de segurança, ela será tratada como se tivesse sido acessada diretamente a partir da consulta original. Assim, uma visualização de invocação de segurança sempre verificará suas relações de base subjacentes usando as permissões do usuário atual, mesmo que seja acessada a partir de uma visualização sem a propriedade `security_invoker`.

Se alguma das relações de base subjacentes tiver a segurança de nível de linha habilitada, então, por padrão, as políticas de segurança de nível de linha do proprietário da visão são aplicadas, e o acesso a quaisquer relações adicionais referenciadas por essas políticas é determinado pelas permissões do proprietário da visão. No entanto, se a visão tiver `security_invoker` definida como `true`, então as políticas e permissões do usuário que está invocando são usadas em vez disso, como se as relações de base tivessem sido referenciadas diretamente a partir da consulta usando a visão.

As funções chamadas na visualização são tratadas da mesma forma como se fossem chamadas diretamente a partir da consulta usando a visualização. Portanto, o usuário de uma visualização deve ter permissões para chamar todas as funções usadas pela visualização. As funções na visualização são executadas com os privilégios do usuário que está executando a consulta ou do proprietário da função, dependendo se as funções são definidas como `SECURITY INVOKER` ou `SECURITY DEFINER`. Assim, por exemplo, chamar `CURRENT_USER` diretamente em uma visualização sempre retornará o usuário que está invocando, não o proprietário da visualização. Isso não é afetado pela configuração `security_invoker` da visualização, e, portanto, uma visualização com `security_invoker` definida como `false` não é *equivalente* a uma função `SECURITY DEFINER` e esses conceitos não devem ser confundidos.

O usuário que cria ou substitui uma visão deve ter privilégios `USAGE` em quaisquer esquemas referenciados na consulta da visão, a fim de consultar os objetos referenciados nesses esquemas. No entanto, observe que essa consulta ocorre apenas quando a visão é criada ou substituída. Portanto, o usuário da visão requer apenas o privilégio `USAGE` no esquema que contém a visão, e não nos esquemas referenciados na consulta da visão, mesmo para uma visão de invocador de segurança.

Quando o `CREATE OR REPLACE VIEW` é usado em uma visão existente, apenas a regra de definição SELECT da visão, além de quaisquer parâmetros `WITH ( ... )` e seu `CHECK OPTION` são alterados. Outras propriedades da visão, incluindo propriedade, permissões e regras que não são SELECT, permanecem inalteradas. Você deve possuir a visão para substituí-la (isso inclui ser membro do papel de propriedade).

### Visualizações Atualizáveis

As consultas simples são automaticamente atualizáveis: o sistema permitirá que as declarações `INSERT`, `UPDATE`, `DELETE` e `MERGE` sejam usadas na consulta da mesma maneira que em uma tabela comum. Uma consulta é automaticamente atualizável se satisfazer todas as seguintes condições:

* A visão deve ter exatamente uma entrada em sua lista `FROM`, que deve ser uma tabela ou outra visão atualizável.
* A definição da visão não deve conter cláusulas `WITH`, `DISTINCT`, `GROUP BY`, `HAVING`, `LIMIT` ou `OFFSET` no nível superior.
* A definição da visão não deve conter operações de conjunto (`UNION`, `INTERSECT` ou `EXCEPT`) no nível superior.
* A lista de seleção da visão não deve conter quaisquer agregados, funções de janela ou funções que retornam conjuntos.

Uma visão automaticamente atualizável pode conter uma mistura de colunas atualizáveis e não atualizáveis. Uma coluna é atualizável se for uma simples referência a uma coluna atualizável da relação base subjacente; caso contrário, a coluna é somente de leitura, e um erro será exibido se uma declaração `INSERT`, `UPDATE` ou `MERGE` tentar atribuir um valor a ela.

Se a visualização for automaticamente atualizável, o sistema converterá qualquer declaração `INSERT`, `UPDATE`, `DELETE` ou `MERGE` na visualização na declaração correspondente na relação de base subjacente. As declarações `INSERT` que possuem uma cláusula `ON CONFLICT UPDATE` são totalmente suportadas.

Se uma visão automaticamente atualizável contiver uma condição `WHERE`, a condição restringe quais linhas da relação base estão disponíveis para serem modificadas pelas instruções `UPDATE`, `DELETE` e `MERGE` na visão. No entanto, uma `UPDATE` ou `MERGE` é permitida para alterar uma linha de modo que ela não satisfaça mais a condição `WHERE`, e assim não seja mais visível através da visão. Da mesma forma, um comando `INSERT` ou `MERGE` pode potencialmente inserir linhas da relação base que não satisfaçam a condição `WHERE` e, portanto, não sejam visíveis através da visão (`ON CONFLICT UPDATE` pode afetar de maneira semelhante uma linha existente que não seja visível através da visão). A `CHECK OPTION` pode ser usada para impedir que as instruções `INSERT`, `UPDATE` e `MERGE` criem tais linhas que não sejam visíveis através da visão.

Se uma visão automaticamente atualizável for marcada com a propriedade `security_barrier`, todas as condições `WHERE` da visão (e quaisquer condições que utilizem operadores que estejam marcados como `LEAKPROOF`) serão sempre avaliadas antes de quaisquer condições que um usuário da visão tenha adicionado. Consulte [Seção 39.5][(rules-privileges.md "39.5. Rules and Privileges")] para obter detalhes completos. Observe que, devido a isso, as linhas que não são devolvidas (porque não passam das condições `WHERE` do usuário) ainda podem acabar sendo bloqueadas. `EXPLAIN` pode ser usado para ver quais condições são aplicadas no nível da relação (e, portanto, não bloqueiam linhas) e quais não são.

Uma visão mais complexa que não satisfaça todas essas condições é leitura somente por padrão: o sistema não permitirá um `INSERT`, `UPDATE`, `DELETE` ou `MERGE` na visão. Você pode obter o efeito de uma visão atualizável criando gatilhos `INSTEAD OF` na visão, que devem converter tentativas de inserção, etc., na visão em ações apropriadas em outras tabelas. Para mais informações, consulte [CREATE TRIGGER](sql-createtrigger.md "CREATE TRIGGER"). Outra possibilidade é criar regras (consulte [CREATE RULE](sql-createrule.md "CREATE RULE")) , mas, na prática, os gatilhos são mais fáceis de entender e usar corretamente. Além disso, note que o `MERGE` não é suportado em relações com regras.

Observe que o usuário que realiza a inserção, atualização ou exclusão na visualização deve ter os privilégios correspondentes de inserção, atualização ou exclusão na visualização. Além disso, por padrão, o proprietário da visualização deve ter os privilégios relevantes nas relações de base subjacentes, enquanto o usuário que realiza a atualização não precisa de quaisquer permissões nas relações de base subjacentes (consulte [Seção 39.5] [(rules-privileges.md "39.5. Rules and Privileges")]). No entanto, se a visualização tiver `security_invoker` definida como `true`, o usuário que realiza a atualização, e não o proprietário da visualização, deve ter os privilégios relevantes nas relações de base subjacentes.

## Exemplos

Crie uma visualização que inclua todos os filmes de comédia:

```
CREATE VIEW comedies AS SELECT * FROM films WHERE kind = 'Comedy';
```

Isso criará uma visualização que contém as colunas que estão na tabela `film` no momento da criação da visualização. Embora `*` tenha sido usado para criar a visualização, as colunas adicionadas posteriormente à tabela não farão parte da visualização.

Crie uma visão com `LOCAL CHECK OPTION`:

```
CREATE VIEW universal_comedies AS SELECT * FROM comedies WHERE classification = 'U' WITH LOCAL CHECK OPTION;
```

Isso criará uma visualização com base na visualização `comedies`, mostrando apenas filmes com `kind = 'Comedy'` e `classification = 'U'`. Qualquer tentativa de `INSERT` ou `UPDATE` uma linha na visualização será rejeitada se a nova linha não tiver `classification = 'U'`, mas o filme `kind` não será verificado.

Crie uma visão com `CASCADED CHECK OPTION`:

```
CREATE VIEW pg_comedies AS SELECT * FROM comedies WHERE classification = 'PG' WITH CASCADED CHECK OPTION;
```

Isso criará uma visão que verifica tanto os `kind` quanto os `classification` das novas linhas.

Crie uma visão com uma mistura de colunas atualizáveis e não atualizáveis:

```
CREATE VIEW comedies AS SELECT f.*, country_code_to_name(f.country_code) AS country, (SELECT avg(r.rating) FROM user_ratings r WHERE r.film_id = f.id) AS avg_rating FROM films f WHERE f.kind = 'Comedy';
```

Essa visão apoiará `INSERT`, `UPDATE` e `DELETE`. Todas as colunas da tabela `films` serão atualizáveis, enquanto as colunas calculadas `country` e `avg_rating` serão somente de leitura.

Crie uma visualização recursiva composta pelos números de 1 a 100:

```
CREATE RECURSIVE VIEW public.nums_1_100 (n) AS VALUES (1) UNION ALL SELECT n+1 FROM nums_1_100 WHERE n < 100;
```

Observe que, embora o nome da visão recursiva seja qualificado por esquema neste `CREATE`, sua auto-referência interna não é qualificado por esquema. Isso ocorre porque o nome do CTE criado implicitamente não pode ser qualificado por esquema.

## Compatibilidade

`CREATE OR REPLACE VIEW` é uma extensão de linguagem do PostgreSQL. O mesmo vale para o conceito de visão temporária. A cláusula `WITH ( ... )` também é uma extensão, assim como as visões de barreira de segurança e as visões de invocador de segurança.

## Veja também

[ALTERAR VISTA](sql-alterview.md "ALTER VIEW"), [DROP VIEW](sql-dropview.md "DROP VIEW"), [CREATE MATERIALIZED VIEW](sql-creatematerializedview.md "CREATE MATERIALIZED VIEW")