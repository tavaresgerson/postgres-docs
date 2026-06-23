## dblink_connect_u

dblink_connect_u — abre uma conexão persistente a um banco de dados remoto, de forma insegura

## Sinopse

```
dblink_connect_u(text connstr) returns text
dblink_connect_u(text connname, text connstr) returns text
```

## Descrição

`dblink_connect_u()` é idêntico a `dblink_connect()`, exceto que permitirá que usuários não superusuários se conectem usando qualquer método de autenticação.

Se o servidor remoto selecionar um método de autenticação que não envolva uma senha, então a imposição de identidade e a subsequente escalada de privilégios podem ocorrer, porque a sessão parecerá ter origem no usuário pelo qual o servidor PostgreSQL local é executado. Além disso, mesmo que o servidor remoto exija uma senha, é possível que a senha seja fornecida pelo ambiente do servidor, como um arquivo `~/.pgpass` pertencente ao usuário do servidor. Isso não só abre o risco de imposição de identidade, mas também a possibilidade de expor uma senha a um servidor remoto não confiável. Portanto, o `dblink_connect_u()` é instalado inicialmente com todos os privilégios revogados de `PUBLIC`, tornando-o inutilizável, exceto por superusuários. Em algumas situações, pode ser apropriado conceder permissão ao `EXECUTE` para o `dblink_connect_u()` a usuários específicos que são considerados confiáveis, mas isso deve ser feito com cuidado. Também é recomendado que qualquer arquivo `~/.pgpass` pertencente ao usuário do servidor *não* contenha registros que especifiquem um nome de host wildcard.

Para mais detalhes, consulte `dblink_connect()`.