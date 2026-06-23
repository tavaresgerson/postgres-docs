## SAVEPOINT

SAVEPOINT — definir um novo ponto de salvamento dentro da transação atual

## Sinopse

```
SAVEPOINT savepoint_name
```

## Descrição

`SAVEPOINT` estabelece um novo ponto de salvamento dentro da transação atual.

Um ponto de salvamento é uma marca especial dentro de uma transação que permite que todos os comandos executados após sua criação sejam revertidos, restaurando o estado da transação ao que era no momento do ponto de salvamento.

## Parâmetros

*`savepoint_name`*: O nome que se deve dar ao novo ponto de salvamento. Se houver pontos de salvamento com o mesmo nome, eles serão inacessíveis até que novos pontos de salvamento com o mesmo nome sejam liberados.

## Notas

Use `ROLLBACK TO` para fazer um rollback a um ponto de salvamento. Use `RELEASE SAVEPOINT` para destruir um ponto de salvamento, mantendo os efeitos dos comandos executados após sua criação.

Os pontos de salvamento só podem ser estabelecidos dentro de um bloco de transação. Pode haver vários pontos de salvamento definidos dentro de uma transação.

## Exemplos

Para estabelecer um ponto de salvamento e, posteriormente, desfazer os efeitos de todos os comandos executados após o seu estabelecimento:

```
BEGIN;
    INSERT INTO table1 VALUES (1);
    SAVEPOINT my_savepoint;
    INSERT INTO table1 VALUES (2);
    ROLLBACK TO SAVEPOINT my_savepoint;
    INSERT INTO table1 VALUES (3);
COMMIT;
```

A transação acima inserirá os valores 1 e 3, mas não o número 2.

Para estabelecer e, posteriormente, destruir um ponto de salvamento:

```
BEGIN;
    INSERT INTO table1 VALUES (3);
    SAVEPOINT my_savepoint;
    INSERT INTO table1 VALUES (4);
    RELEASE SAVEPOINT my_savepoint;
COMMIT;
```

A transação acima inserirá tanto o 3 quanto o 4.

Para usar um nome de ponto de salvamento único:

```
BEGIN;
    INSERT INTO table1 VALUES (1);
    SAVEPOINT my_savepoint;
    INSERT INTO table1 VALUES (2);
    SAVEPOINT my_savepoint;
    INSERT INTO table1 VALUES (3);

    -- rollback to the second savepoint
    ROLLBACK TO SAVEPOINT my_savepoint;
    SELECT * FROM table1;               -- shows rows 1 and 2

    -- release the second savepoint
    RELEASE SAVEPOINT my_savepoint;

    -- rollback to the first savepoint
    ROLLBACK TO SAVEPOINT my_savepoint;
    SELECT * FROM table1;               -- shows only row 1
COMMIT;
```

A transação acima mostra que a linha 3 é revertida primeiro, seguida pela linha 2.

## Compatibilidade

O SQL exige que um ponto de salvamento seja destruído automaticamente quando outro ponto de salvamento com o mesmo nome é estabelecido. No PostgreSQL, o ponto de salvamento antigo é mantido, embora apenas o mais recente seja usado ao reverter ou liberar. (Liberar o ponto de salvamento mais recente com `RELEASE SAVEPOINT` fará com que o antigo novamente se torne acessível ao `ROLLBACK TO SAVEPOINT` e ao `RELEASE SAVEPOINT`.)) Caso contrário, o `SAVEPOINT` é totalmente conforme com o SQL.

## Veja também

[INÍCIO](sql-begin.md "BEGIN"), [COMITAMENTO](sql-commit.md "COMMIT"), [SALVAMENTO DE PONTE DE REAÇÃO](sql-release-savepoint.md "RELEASE SAVEPOINT"), [RETRAÇÃO](sql-rollback.md "ROLLBACK"), [RETRAÇÃO PARA PONTE DE REAÇÃO](sql-rollback-to.md "ROLLBACK TO SAVEPOINT")