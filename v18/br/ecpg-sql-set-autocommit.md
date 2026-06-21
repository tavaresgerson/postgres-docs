## SET AUTOCOMMIT

SET AUTOCOMMIT — define o comportamento de autocommit da sessão atual

## Sinopse

```
SET AUTOCOMMIT { = | TO } { ON | OFF }
```

## Descrição

`SET AUTOCOMMIT` define o comportamento de autocommit da sessão atual do banco de dados. Por padrão, os programas de SQL embutido não estão no modo de autocommit, portanto, `COMMIT` precisa ser emitido explicitamente quando desejado. Este comando pode alterar a sessão para o modo de autocommit, onde cada declaração individual é comprometida implicitamente.

## Compatibilidade

`SET AUTOCOMMIT` é uma extensão do PostgreSQL ECPG.