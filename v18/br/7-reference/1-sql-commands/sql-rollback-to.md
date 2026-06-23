## REVERT PARA SAVEPOINT

REVERT PARA SAVEPOINT — reverta para um ponto de salvamento

## Sinopse

```
ROLLBACK [ WORK | TRANSACTION ] TO [ SAVEPOINT ] savepoint_name
```

## Descrição

Reveja todos os comandos que foram executados após o ponto de salvamento ter sido estabelecido e, em seguida, inicie uma nova subtransação no mesmo nível de transação. O ponto de salvamento permanece válido e pode ser revisto novamente, se necessário.

`ROLLBACK TO SAVEPOINT` destrói implicitamente todos os pontos de salvamento que foram estabelecidos após o ponto de salvamento nomeado.

## Parâmetros

*`savepoint_name`*: O ponto de salvamento para o qual se deseja retornar.

## Notas

Use `RELEASE SAVEPOINT`(sql-release-savepoint.md "RELEASE SAVEPOINT") para destruir um ponto de salvamento sem descartar os efeitos dos comandos executados após ele ter sido estabelecido.

Especificar um nome de ponto de salvamento que não foi estabelecido é um erro.

Os cursors têm um comportamento que não é totalmente transacional em relação aos pontos de salvamento. Qualquer cursor que seja aberto dentro de um ponto de salvamento será fechado quando o ponto de salvamento for desfeito. Se um cursor que foi aberto anteriormente for afetado por um comando `FETCH` ou `MOVE` dentro de um ponto de salvamento que é posteriormente desfeito, o cursor permanecerá na posição que o `FETCH` deixou apontando (ou seja, o movimento do cursor causado pelo `FETCH` não é desfeito). A fechamento de um cursor também não é desfeito ao desfazer. No entanto, outros efeitos colaterais causados pela consulta do cursor (como efeitos colaterais de funções voláteis chamadas pela consulta) *são* desfeitos se ocorrerem durante um ponto de salvamento que é posteriormente desfeito. Um cursor cuja execução causa o abort do processo de transação é colocado em um estado de não execução, portanto, embora a transação possa ser restaurada usando `ROLLBACK TO SAVEPOINT`, o cursor não pode mais ser usado.

## Exemplos

Para desfazer os efeitos dos comandos executados após o `my_savepoint` ter sido estabelecido:

```
ROLLBACK TO SAVEPOINT my_savepoint;
```

As posições do cursor não são afetadas pelo rollback do ponto de salvamento:

```
BEGIN;

DECLARE foo CURSOR FOR SELECT 1 UNION SELECT 2;

SAVEPOINT foo;

FETCH 1 FROM foo;
 ?column?
----------
        1

ROLLBACK TO SAVEPOINT foo;

FETCH 1 FROM foo;
 ?column?
----------
        2

COMMIT;
```

## Compatibilidade

O padrão SQL especifica que a palavra-chave `SAVEPOINT` é obrigatória, mas o PostgreSQL e o Oracle permitem que ela seja omitida. O SQL permite apenas `WORK`, não `TRANSACTION`, como uma palavra de ruído após `ROLLBACK`. Além disso, o SQL tem uma cláusula opcional `AND [ NO ] CHAIN` que atualmente não é suportada pelo PostgreSQL. Caso contrário, este comando está em conformidade com o padrão SQL.

## Veja também

[INÍCIO](sql-begin.md "BEGIN"), [COMITAMENTO](sql-commit.md "COMMIT"), [SALVAMENTO DE PONTE](sql-release-savepoint.md "RELEASE SAVEPOINT"), [RETRAÇÃO](sql-rollback.md "ROLLBACK"), [SALVAMENTO DE PONTE](sql-savepoint.md "SAVEPOINT")