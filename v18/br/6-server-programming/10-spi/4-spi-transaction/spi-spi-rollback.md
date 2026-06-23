## SPI_rollback

SPI_rollback, SPI_rollback_and_chain — abortar a transação atual

## Sinopse

```
void SPI_rollback(void)
```

```
void SPI_rollback_and_chain(void)
```

## Descrição

`SPI_rollback` desfaz a transação atual. É aproximadamente equivalente a executar o comando SQL `ROLLBACK`. Após a transação ser desfeita, uma nova transação é iniciada automaticamente usando as características de transação padrão, para que o solicitante possa continuar usando as facilidades do SPI.

`SPI_rollback_and_chain` é o mesmo, mas a nova transação é iniciada com as mesmas características da transação que acabou de ser concluída, como com o comando SQL `ROLLBACK AND CHAIN`.

Essas funções só podem ser executadas se a conexão SPI tiver sido definida como nonatomic na chamada para `SPI_connect_ext`.