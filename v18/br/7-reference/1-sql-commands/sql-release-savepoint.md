## LIBERAR SAVEPOINT

RELANCE SAVEPOINT — liberar um ponto de salvamento previamente definido

## Sinopse

```
RELEASE [ SAVEPOINT ] savepoint_name
```

## Descrição

`RELEASE SAVEPOINT` libera o ponto de salvamento nomeado e todos os pontos de salvamento ativos que foram criados após o ponto de salvamento nomeado, e libera seus recursos. Todas as alterações feitas desde a criação do ponto de salvamento que não foram já revertidas são unidas à transação ou ao ponto de salvamento que estava ativo quando o ponto de salvamento nomeado foi criado. As alterações feitas após `RELEASE SAVEPOINT` também farão parte desta transação ou ponto de salvamento ativo.

## Parâmetros

*`savepoint_name`*: O nome do ponto de salvamento a ser liberado.

## Notas

Especificar um nome de ponto de salvamento que não foi definido anteriormente é um erro.

Não é possível liberar um ponto de salvamento quando a transação está em estado abortado; para fazer isso, use [REVERT TO SAVEPOINT](sql-rollback-to.md "ROLLBACK TO SAVEPOINT").

Se vários pontos de salvamento tiverem o mesmo nome, apenas o mais recentemente definido e não lançado é liberado. Os comandos repetidos liberam progressivamente os pontos de salvamento mais antigos.

## Exemplos

Para estabelecer e, posteriormente, liberar um ponto de salvamento:

```
BEGIN;
    INSERT INTO table1 VALUES (3);
    SAVEPOINT my_savepoint;
    INSERT INTO table1 VALUES (4);
    RELEASE SAVEPOINT my_savepoint;
COMMIT;
```

A transação acima inserirá tanto o 3 quanto o 4.

Um exemplo mais complexo com múltiplas subtransações aninhadas:

```
BEGIN;
    INSERT INTO table1 VALUES (1);
    SAVEPOINT sp1;
    INSERT INTO table1 VALUES (2);
    SAVEPOINT sp2;
    INSERT INTO table1 VALUES (3);
    RELEASE SAVEPOINT sp2;
    INSERT INTO table1 VALUES (4))); -- generates an error
```

Neste exemplo, o aplicativo solicita a liberação do ponto de salvamento `sp2`, que inseriu 3. Isso altera o contexto da transação de inserção para `sp1`. Quando a declaração que tenta inserir o valor 4 gera um erro, a inserção de 2 e 4 são perdidas porque estão no mesmo ponto de salvamento, agora desfeito, e o valor 3 está no mesmo contexto de transação. O aplicativo agora só pode escolher um desses dois comandos, uma vez que todos os outros comandos serão ignorados:

```
ROLLBACK;
ROLLBACK TO SAVEPOINT sp1;
```

Escolher `ROLLBACK` fará com que tudo seja abortado, incluindo o valor 1, enquanto `ROLLBACK TO SAVEPOINT sp1` manterá o valor 1 e permitirá que a transação continue.

## Compatibilidade

Este comando está de acordo com o padrão SQL. O padrão especifica que a palavra-chave `SAVEPOINT` é obrigatória, mas o PostgreSQL permite que ela seja omitida.

## Veja também

[INÍCIO](sql-begin.md "BEGIN"), [COMITAMENTO](sql-commit.md "COMMIT"), [RETRAÇÃO](sql-rollback.md "ROLLBACK"), [RETRAÇÃO PARA SAVEPOINT](sql-rollback-to.md "ROLLBACK TO SAVEPOINT"), [SAVEPOINT](sql-savepoint.md "SAVEPOINT")