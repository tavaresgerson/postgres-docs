## PREPARE TRANSAÇÃO

PREPARE TRANSACTION — prepare a transação atual para o compromisso de duas fases

## Sinopse

```
PREPARE TRANSACTION transaction_id
```

## Descrição

`PREPARE TRANSACTION` prepara a transação atual para o commit de duas fases. Após este comando, a transação não está mais associada à sessão atual; em vez disso, seu estado é totalmente armazenado no disco, e há uma alta probabilidade de que ela possa ser comprometida com sucesso, mesmo que um crash do banco de dados ocorra antes do pedido de commit.

Uma vez preparada, uma transação pode ser comprometida ou desfeita posteriormente com `COMMIT PREPARED` (sql-commit-prepared.md "COMMIT PREPARED") ou `ROLLBACK PREPARED` (sql-rollback-prepared.md "ROLLBACK PREPARED"), respectivamente. Esses comandos podem ser emitidos a partir de qualquer sessão, não apenas daquela que executou a transação original.

Do ponto de vista da sessão de emissão, `PREPARE TRANSACTION` não é diferente de um comando `ROLLBACK`: após executá-lo, não há transação ativa em andamento, e os efeitos da transação preparada deixam de ser visíveis. (Os efeitos voltarão a ser visíveis se a transação for comprometida.)

Se o comando `PREPARE TRANSACTION` falhar por qualquer motivo, ele se torna um `ROLLBACK`: a transação atual é cancelada.

## Parâmetros

*`transaction_id`*: Um identificador arbitrário que identifica essa transação posteriormente para `COMMIT PREPARED` ou `ROLLBACK PREPARED`. O identificador deve ser escrito como uma literal de string e deve ter menos de 200 bytes de comprimento. Não deve ser o mesmo identificador usado para qualquer transação atualmente preparada.

## Notas

`PREPARE TRANSACTION` não é destinado para uso em aplicações ou sessões interativas. Seu propósito é permitir que um gerenciador de transação externa realize transações globais atômicas em múltiplos bancos de dados ou outros recursos transacionais. A menos que você esteja escrevendo um gerenciador de transação, provavelmente não deve estar usando `PREPARE TRANSACTION`.

Este comando deve ser usado dentro de um bloco de transação. Use `BEGIN`(sql-begin.md "BEGIN") para iniciá-lo.

Atualmente, não é permitido `PREPARE` uma transação que tenha executado quaisquer operações envolvendo tabelas temporárias ou o espaço temporário da sessão, criado quaisquer cursors `WITH HOLD`, ou executado `LISTEN`, `UNLISTEN` ou `NOTIFY`. Essas funcionalidades estão muito ligadas à sessão atual para serem úteis em uma transação que será preparada.

Se a transação modificou quaisquer parâmetros de execução com `SET` (sem a opção `LOCAL`), esses efeitos persistem após `PREPARE TRANSACTION`, e não serão afetados por qualquer `COMMIT PREPARED` ou `ROLLBACK PREPARED` posterior. Assim, nesse aspecto `PREPARE TRANSACTION` age mais como `COMMIT` do que `ROLLBACK`.

Todas as transações preparadas disponíveis atualmente estão listadas na visualização do sistema `pg_prepared_xacts` (view-pg-prepared-xacts.md "53.17. pg_prepared_xacts").

### Atenção

Não é prudente deixar as transações no estado preparado por muito tempo. Isso interferirá na capacidade do `VACUUM` de recuperar armazenamento, e, em casos extremos, poderá fazer com que o banco de dados seja desligado para evitar o enrolamento do ID de transação (consulte [Seção 24.1.5][(routine-vacuuming.md#VACUUM-FOR-WRAPAROUND "24.1.5. Preventing Transaction ID Wraparound Failures")]). Tenha em mente também que a transação continua a manter quaisquer bloqueios que tenha mantido. O uso pretendido do recurso é que uma transação preparada normalmente será comprometida ou revertida assim que um gerenciador de transação externo tiver verificado que outras bases de dados também estão preparadas para comprometer.

Se você não configurou um gerenciador de transações preparadas para acompanhar as transações preparadas e garantir que elas sejam encerradas prontamente, é melhor manter a funcionalidade de transações preparadas desativada, definindo [max_prepared_transactions][(runtime-config-resource.md#GUC-MAX-PREPARED-TRANSACTIONS)] como zero. Isso evitará a criação acidental de transações preparadas que podem ser esquecidas e, eventualmente, causar problemas.

## Exemplos

Prepare a transação atual para um commit de duas fases, usando `foobar` como o identificador da transação:

```
PREPARE TRANSACTION 'foobar';
```

## Compatibilidade

`PREPARE TRANSACTION` é uma extensão do PostgreSQL. É destinado ao uso por sistemas de gerenciamento de transações externas, alguns dos quais estão cobertos por padrões (como X/Open XA), mas o lado SQL desses sistemas não está padronizado.

## Veja também

[COMMIT PREPARADO](sql-commit-prepared.md "COMMIT PREPARED"), [ROLLBACK PREPARADO](sql-rollback-prepared.md "ROLLBACK PREPARED")