## SPI_start_transaction

SPI_start_transaction — função obsoleta

## Sinopse

```
void SPI_start_transaction(void)
```

## Descrição

`SPI_start_transaction` não faz nada e existe apenas para compatibilidade de código com versões anteriores do PostgreSQL. Ele costumava ser necessário após a chamada de `SPI_commit` ou `SPI_rollback`, mas agora essas funções iniciam uma nova transação automaticamente.