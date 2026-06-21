## Crie regra

Crie regra — defina uma nova regra de reescrita

## Sinopse

```
CREATE [ OR REPLACE ] RULE name AS ON event
    TO table_name [ WHERE condition ]
    DO [ ALSO | INSTEAD ] { NOTHING | command | ( command ; command ... ) }

where event can be one of:

    SELECT | INSERT | UPDATE | DELETE
```

## Descrição

`CREATE RULE` define uma nova regra aplicável a uma tabela ou visão especificada. `CREATE OR REPLACE RULE` criará uma nova regra ou substituirá uma regra existente com o mesmo nome para a mesma tabela.

O sistema de regras do PostgreSQL permite definir uma ação alternativa a ser realizada em inserções, atualizações ou exclusões em tabelas de banco de dados. Grosso modo, uma regra faz com que comandos adicionais sejam executados quando um comando dado em uma tabela dada é executado. Alternativamente, uma regra `INSTEAD` pode substituir um comando dado por outro ou fazer com que um comando não seja executado. As regras também são usadas para implementar vistas SQL. É importante perceber que uma regra é realmente um mecanismo de transformação de comando ou macro de comando. A transformação acontece antes do início da execução do comando. Se você realmente deseja uma operação que acione de forma independente para cada linha física, provavelmente deseja usar um gatilho, não uma regra. Mais informações sobre o sistema de regras estão em [Capítulo 39][(rules.md "Chapter 39. The Rule System")].

Atualmente, as regras do `ON SELECT` só podem ser anexadas a visualizações. Uma regra desse tipo deve ser denominada `"_RETURN"`, deve ser uma regra condicional do `INSTEAD` e deve ter uma ação que consista em um único comando do `SELECT`. Esse comando define o conteúdo visível da visualização. (A própria visualização é basicamente uma tabela fictícia sem armazenamento.) É melhor considerar essa regra como um detalhe de implementação. Embora uma visualização possa ser redefinida via `CREATE OR REPLACE RULE "_RETURN" AS ...`, é melhor estilo usar `CREATE OR REPLACE VIEW`.

Você pode criar a ilusão de uma visão atualizável definindo as regras `ON INSERT`, `ON UPDATE` e `ON DELETE` (ou qualquer subconjunto dessas que seja suficiente para seus propósitos) para substituir as ações de atualização na visão com atualizações apropriadas em outras tabelas. Se você deseja suportar `INSERT RETURNING` e assim por diante, então certifique-se de colocar uma cláusula `RETURNING` adequada em cada uma dessas regras.

Há uma ressalva se você tentar usar regras condicionais para atualizações de visualização complexas: *deve* haver uma regra `INSTEAD` incondicional para cada ação que você deseja permitir na visualização. Se a regra for condicional ou não for `INSTEAD`, o sistema ainda rejeitará as tentativas de realizar a ação de atualização, porque pensa que, em alguns casos, pode acabar tentando realizar a ação na tabela fictícia da visualização. Se você deseja lidar com todos os casos úteis em regras condicionais, adicione uma regra `DO INSTEAD NOTHING` incondicional para garantir que o sistema entenda que nunca será chamado para atualizar a tabela fictícia. Em seguida, faça as regras condicionais não `INSTEAD`; nos casos em que elas são aplicadas, elas adicionam à ação padrão `INSTEAD NOTHING`. (Este método atualmente não funciona para suportar consultas `RETURNING`, no entanto.)

### Nota

Uma visão que é simples o suficiente para ser automaticamente atualizável (consulte [CREATE VIEW](sql-createview.md "CREATE VIEW")) não requer uma regra criada pelo usuário para ser atualizável. Embora você possa criar uma regra explícita de qualquer maneira, a transformação de atualização automática geralmente supera uma regra explícita.

Outra alternativa que vale a pena considerar é usar gatilhos `INSTEAD OF` (consulte CREATE TRIGGER (sql-createtrigger.md "CREATE TRIGGER")) em vez de regras.

## Parâmetros

*`name`*: O nome de uma regra a ser criada. Isso deve ser distinto do nome de qualquer outra regra para a mesma tabela. Múltiplas regras na mesma tabela e no mesmo tipo de evento são aplicadas em ordem alfabética de nome.

*`event`*: O evento é um dos `SELECT`, `INSERT`, `UPDATE` ou `DELETE`. Observe que um `INSERT` que contenha uma cláusula `ON CONFLICT` não pode ser usado em tabelas que possuem regras de `INSERT` ou `UPDATE`. Considere usar uma visão atualizável em vez disso.

*`table_name`*: O nome (opcionalmente qualificado por esquema) da tabela ou visão à qual a regra se aplica.

*`condition`*: Qualquer expressão condicional SQL (retornando `boolean`). A expressão condicional não pode se referir a nenhuma tabela exceto `NEW` e `OLD`, e não pode conter funções agregadas.

`INSTEAD`: `INSTEAD` indica que os comandos devem ser executados em vez do comando original.

`ALSO`: `ALSO` indica que os comandos devem ser executados *a mais* do que o comando original.

Se nem `ALSO` nem `INSTEAD` forem especificados, `ALSO` é o padrão.

*`command`*: O comando ou comandos que compõem a ação da regra. Os comandos válidos são `SELECT`, `INSERT`, `UPDATE`, `DELETE` ou `NOTIFY`.

Dentro de *`condition`* e *`command`*, os nomes especiais das tabelas `NEW` e `OLD` podem ser usados para referenciar valores na tabela referenciada. `NEW` é válido em `ON INSERT` e `ON UPDATE` para referenciar a nova linha sendo inserida ou atualizada. `OLD` é válido em `ON UPDATE` e `ON DELETE` para referenciar a linha existente sendo atualizada ou excluída.

## Notas

Você deve ser o proprietário de uma tabela para criar ou alterar regras para ela.

Em uma regra para `INSERT`, `UPDATE` ou `DELETE` em uma visualização, você pode adicionar uma cláusula `RETURNING` que emite as colunas da visualização. Esta cláusula será usada para calcular as saídas se a regra for acionada por um comando `INSERT RETURNING`, `UPDATE RETURNING` ou `DELETE RETURNING`, respectivamente. Quando a regra é acionada por um comando sem `RETURNING`, a cláusula `RETURNING` da regra será ignorada. A implementação atual permite que apenas regras `INSTEAD` incondicionais contenham `RETURNING`; além disso, pode haver no máximo uma cláusula `RETURNING` entre todas as regras para o mesmo evento. (Isso garante que exista apenas uma cláusula candidata `RETURNING` a ser usada para calcular os resultados.) Consultas `RETURNING` na visualização serão rejeitadas se não houver nenhuma cláusula `RETURNING` em qualquer regra disponível.

É muito importante ter cuidado para evitar regras circulares. Por exemplo, embora cada uma das seguintes duas definições de regra sejam aceitas pelo PostgreSQL, o comando `SELECT` faria com que o PostgreSQL relatasse um erro devido à expansão recursiva de uma regra:

```
CREATE RULE "_RETURN" AS
    ON SELECT TO t1
    DO INSTEAD
        SELECT * FROM t2;

CREATE RULE "_RETURN" AS
    ON SELECT TO t2
    DO INSTEAD
        SELECT * FROM t1;

SELECT * FROM t1;
```

Atualmente, se uma ação de regra contiver um comando `NOTIFY`, o comando `NOTIFY` será executado incondicionalmente, ou seja, o `NOTIFY` será emitido mesmo que não haja nenhuma linha para a qual a regra deva ser aplicada. Por exemplo, em:

```
CREATE RULE notify_me AS ON UPDATE TO mytable DO ALSO NOTIFY mytable;

UPDATE mytable SET name = 'foo' WHERE id = 42;
```

um evento `NOTIFY` será enviado durante o `UPDATE`, independentemente de haver ou não linhas que correspondam à condição `id = 42`. Esta é uma restrição de implementação que pode ser corrigida em versões futuras.

## Compatibilidade

`CREATE RULE` é uma extensão de linguagem do PostgreSQL, assim como todo o sistema de reescrita de consultas.

## Veja também

[ALTERAR REGRA](sql-alterrule.md "ALTER RULE"), [DROP REGRA](sql-droprule.md "DROP RULE")