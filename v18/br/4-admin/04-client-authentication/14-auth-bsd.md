## 20.14. Autenticação BSD [#](#AUTH-BSD)

Este método de autenticação funciona de forma semelhante ao `password`, exceto que ele usa a Autenticação BSD para verificar a senha. A Autenticação BSD é usada apenas para validar pares de nome/senha do usuário. Portanto, o papel do usuário deve já existir no banco de dados antes que a Autenticação BSD possa ser usada para autenticação. O framework de Autenticação BSD está atualmente disponível apenas no OpenBSD.

A autenticação BSD no PostgreSQL utiliza o tipo de login `auth-postgresql` e autentica com a classe de login `postgresql` se essa for definida em `login.conf`. Por padrão, essa classe de login não existe, e o PostgreSQL usará a classe de login padrão.

### Nota

Para usar a Autenticação BSD, a conta de usuário do PostgreSQL (ou seja, o usuário do sistema operacional que executa o servidor) deve primeiro ser adicionada ao grupo `auth`. O grupo `auth` existe por padrão em sistemas OpenBSD.