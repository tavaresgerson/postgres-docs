## CHECKPOINT

CHECKPOINT — força um ponto de registro de escrita antecipada

## Sinopse

```
CHECKPOINT
```

## Descrição

Um ponto de verificação é um ponto na sequência de registro prévio em que todos os arquivos de dados foram atualizados para refletir as informações no log. Todos os arquivos de dados serão descarregados no disco. Consulte [Seção 28.5](wal-configuration.md) para obter mais detalhes sobre o que acontece durante um ponto de verificação.

O comando `CHECKPOINT` obriga um ponto de verificação imediato quando o comando é emitido, sem esperar por um ponto de verificação regular agendado pelo sistema (controlado pelos ajustes em [Seção 19.5.2](runtime-config-wal.md#RUNTIME-CONFIG-WAL-CHECKPOINTS)). `CHECKPOINT` não é destinado para uso durante operação normal.

Se executado durante a recuperação, o comando `CHECKPOINT` fará com que um ponto de reinício seja forçado (consulte [Seção 28.5](wal-configuration.md)) em vez de escrever um novo ponto de verificação.

Apenas superusuários ou usuários com os privilégios da função [pg_checkpoint](predefined-roles.md#PREDEFINED-ROLE-PG-CHECKPOINT) podem chamar `CHECKPOINT`.

## Compatibilidade

O comando `CHECKPOINT` é uma extensão de linguagem do PostgreSQL.