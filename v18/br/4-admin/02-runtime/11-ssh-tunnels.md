## 18.11. Conexões seguras TCP/IP com Túneis SSH [#](#SSH-TUNNELS)

É possível usar SSH para criptografar a conexão de rede entre clientes e um servidor PostgreSQL. Se feito corretamente, isso oferece uma conexão de rede adequadamente segura, mesmo para clientes que não possuem suporte a SSL.

Primeiro, certifique-se de que um servidor SSH esteja funcionando corretamente na mesma máquina que o servidor PostgreSQL e que você possa fazer login usando `ssh` como algum usuário; então, você pode estabelecer um túnel seguro para o servidor remoto. Um túnel seguro escuta em uma porta local e encaminha todo o tráfego para uma porta na máquina remota. O tráfego enviado para a porta remota pode chegar em seu endereço `localhost`, ou em um endereço de vinculação diferente, se desejado; ele não parece ser proveniente da sua máquina local. Este comando cria um túnel seguro da máquina cliente para a máquina remota `foo.com`:

```
ssh -L 63333:localhost:5432 joe@foo.com
```

O primeiro número no argumento `-L`, 63333, é o número de porta local do túnel; pode ser qualquer porta não utilizada. (A IANA reserva portas de 49152 a 65535 para uso privado.) O nome ou endereço IP após este é o endereço de vinculação remoto ao qual você está se conectando, ou seja, `localhost`, que é o padrão. O segundo número, 5432, é o extremo remoto do túnel, por exemplo, o número de porta que seu servidor de banco de dados está usando. Para se conectar ao servidor de banco de dados usando este túnel, você se conecta à porta 63333 na máquina local:

```
psql -h localhost -p 63333 postgres
```

Para o servidor de banco de dados, ele parecerá como se você fosse o usuário `joe` no host `foo.com` conectando-se ao endereço de vinculação `localhost`, e ele usará qualquer procedimento de autenticação configurado para conexões desse usuário ao endereço de vinculação. Note que o servidor não pensará que a conexão esteja criptografada SSL, pois, na verdade, não está criptografada entre o servidor SSH e o servidor PostgreSQL. Isso não deve representar nenhum risco adicional de segurança, pois eles estão na mesma máquina.

Para que a configuração do túnel seja bem-sucedida, você deve ser autorizado a se conectar via `ssh` como `joe@foo.com`, assim como se tivesse tentado usar `ssh` para criar uma sessão de terminal.

Você também poderia ter configurado o encaminhamento de porta como

```
ssh -L 63333:foo.com:5432 joe@foo.com
```

mas, então, o servidor de banco de dados verá a conexão chegando em seu endereço de ligação `foo.com`, que não é aberto pelo ajuste padrão `listen_addresses = 'localhost'`. Isso geralmente não é o que você quer.

Se você precisa "pular" para o servidor de banco de dados através de algum host de login, uma configuração possível pode parecer assim:

```
ssh -L 63333:db.foo.com:5432 joe@shell.foo.com
```

Observe que, dessa forma, a conexão de `shell.foo.com` para `db.foo.com` não será criptografada pelo túnel SSH. O SSH oferece várias possibilidades de configuração quando a rede é restrita de várias maneiras. Consulte a documentação do SSH para obter detalhes.

DICA

Existem várias outras aplicações que podem fornecer túneis seguros usando um procedimento semelhante ao que foi descrito.