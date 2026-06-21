## DESTAQUE A SUBSCRIPÃO

DROP SUBSCRIPTION — remover uma assinatura

## Sinopse

```
DROP SUBSCRIPTION [ IF EXISTS ] name [ CASCADE | RESTRICT ]
```

## Descrição

`DROP SUBSCRIPTION` remove uma assinatura do cluster de banco de dados.

Para executar este comando, o usuário deve ser o proprietário da assinatura.

`DROP SUBSCRIPTION` não pode ser executado dentro de um bloco de transação se a assinatura estiver associada a um intervalo de replicação. (Você pode usar `ALTER SUBSCRIPTION` (sql-altersubscription.md "ALTER SUBSCRIPTION") para desativar o intervalo.)

## Parâmetros

`IF EXISTS`: Não exija erro se a assinatura não existir. Um aviso é emitido neste caso.

*`name`*: O nome de uma assinatura que deve ser excluído.

`CASCADE` `RESTRICT`: Essas palavras-chave não têm nenhum efeito, uma vez que não há dependências em assinaturas.

## Notas

Ao cancelar uma assinatura associada a um slot de replicação no host remoto (o estado normal), o `DROP SUBSCRIPTION` se conectará ao host remoto e tentará cancelar o slot de replicação (e quaisquer slots de sincronização de tabela restantes) como parte de sua operação. Isso é necessário para que os recursos alocados para a assinatura no host remoto sejam liberados. Se isso falhar, seja porque o host remoto não é acessível ou porque o slot de replicação remoto não pode ser cancelado ou não existe ou nunca existiu, o comando `DROP SUBSCRIPTION` falhará. Para prosseguir nessa situação, primeiro desabilite a assinatura executando [`ALTER SUBSCRIPTION ... DISABLE`](sql-altersubscription.md#SQL-ALTERSUBSCRIPTION-PARAMS-DISABLE), e depois desvincule-a do slot de replicação executando [`ALTER SUBSCRIPTION ... SET (slot_name = NONE)`](sql-altersubscription.md#SQL-ALTERSUBSCRIPTION-PARAMS-SET). Após isso, o `DROP SUBSCRIPTION` não tentará mais realizar nenhuma ação em um host remoto. Observe que, se o slot de replicação remoto ainda existir, ele (e quaisquer slots de sincronização de tabela relacionados) deve ser cancelado manualmente; caso contrário, eles continuarão a reservar o WAL e podem acabar enchendo o disco. Veja também [Seção 29.2.1](logical-replication-subscription.md#LOGICAL-REPLICATION-SUBSCRIPTION-SLOT "29.2.1. Replication Slot Management").

Se uma assinatura estiver associada a um intervalo de replicação, então `DROP SUBSCRIPTION` não pode ser executado dentro de um bloco de transação.

## Exemplos

Cancelar uma assinatura:

```
DROP SUBSCRIPTION mysub;
```

## Compatibilidade

`DROP SUBSCRIPTION` é uma extensão do PostgreSQL.

## Veja também

[Crie uma assinatura](sql-createsubscription.md "CREATE SUBSCRIPTION"), [Alterar assinatura](sql-altersubscription.md "ALTER SUBSCRIPTION")