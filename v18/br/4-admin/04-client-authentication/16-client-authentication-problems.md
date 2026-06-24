## 20.16. Problemas de autenticação [#](#CLIENT-AUTHENTICATION-PROBLEMS)

Os problemas de autenticação e os problemas relacionados geralmente se manifestam através de mensagens de erro como as seguintes:

```
FATAL:  no pg_hba.conf entry for host "123.123.123.123", user "andym", database "testdb"
```

Isso é o que você provavelmente vai obter se conseguir entrar em contato com o servidor, mas ele não quer falar com você. Como a mensagem sugere, o servidor recusou o pedido de conexão porque não encontrou nenhuma entrada correspondente em seu arquivo de configuração `pg_hba.conf`.

```
FATAL:  password authentication failed for user "andym"
```

Mensagens como essa indicam que você entrou em contato com o servidor, e ele está disposto a conversar com você, mas não antes de você passar pelo método de autorização especificado no arquivo `pg_hba.conf`. Verifique a senha que você está fornecendo, ou verifique seu software Kerberos ou ident se a reclamação mencionar um desses tipos de autenticação.

```
FATAL:  user "andym" does not exist
```

O nome do usuário do banco de dados indicado não foi encontrado.

```
FATAL:  database "testdb" does not exist
```

O banco de dados ao qual você está tentando se conectar não existe. Observe que, se você não especificar um nome de banco de dados, ele será predefinido com o nome do usuário do banco de dados.

DICA

O log do servidor pode conter mais informações sobre uma falha de autenticação do que as relatadas ao cliente. Se você está confuso sobre o motivo de uma falha, verifique o log do servidor.