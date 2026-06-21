## SPI_commit

SPI_commit, SPI_commit_and_chain — commitar a transação atual

## Sinopse

```
void SPI_commit(void)
```

```
void SPI_commit_and_chain(void)
```

## Descrição

`SPI_commit` executa a transação atual. É aproximadamente equivalente a executar o comando SQL `COMMIT`. Após a transação ser executada, uma nova transação é automaticamente iniciada usando as características de transação padrão, para que o solicitante possa continuar usando as facilidades do SPI. Se houver uma falha durante o commit, a transação atual é, em vez disso, revertida e uma nova transação é iniciada, após o que o erro é lançado da maneira usual.

`SPI_commit_and_chain` é o mesmo, mas a nova transação é iniciada com as mesmas características da transação que acabou de ser concluída, como com o comando SQL `COMMIT AND CHAIN`.

Essas funções só podem ser executadas se a conexão SPI tiver sido definida como nonatomic na chamada para `SPI_connect_ext`.