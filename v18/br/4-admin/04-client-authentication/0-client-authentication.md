## Capítulo 20. Autenticação do Cliente

**Índice**

* [20.1. O arquivo `pg_hba.conf`](auth-pg-hba-conf.md)
* [20.2. Mapas de Nome do Usuário](auth-username-maps.md)
* [20.3. Métodos de Autenticação](auth-methods.md)
* [20.4. Autenticação de Confiança](auth-trust.md)
* [20.5. Autenticação por Senha](auth-password.md)
* [20.6. Autenticação GSSAPI](gssapi-auth.md)
* [20.7. Autenticação SSPI](sspi-auth.md)
* [20.8. Autenticação Ident](auth-ident.md)
* [20.9. Autenticação Peer](auth-peer.md)
* [20.10. Autenticação LDAP](auth-ldap.md)
* [20.11. Autenticação RADIUS](auth-radius.md)
* [20.12. Autenticação por Certificado](auth-cert.md)
* [20.13. Autenticação PAM](auth-pam.md)
* [20.14. Autenticação BSD](auth-bsd.md)
* [20.15. Autenticação/Autenticação OAuth](auth-oauth.md)
* [20.16. Problemas de Autenticação](client-authentication-problems.md)

Quando um aplicativo de cliente se conecta ao servidor de banco de dados, ele especifica qual nome de usuário do banco de dados PostgreSQL deseja se conectar como, da mesma forma que se inicia em um computador Unix como um usuário específico. Dentro do ambiente SQL, o nome de usuário do banco de dados ativo determina os privilégios de acesso aos objetos do banco de dados — consulte [Capítulo 21](user-manag.md) para mais informações. Portanto, é essencial restringir quais usuários do banco de dados podem se conectar.

### Nota

Como explicado no [Capítulo 21](user-manag.md), o PostgreSQL, na verdade, realiza a gestão de privilégios em termos de “rolos”. Neste capítulo, usamos consistentemente *usuário do banco de dados* para significar “rol com o privilégio [[`LOGIN`]”.

*Autenticação* é o processo pelo qual o servidor de banco de dados estabelece a identidade do cliente e, por extensão, determina se o aplicativo do cliente (ou o usuário que executa o aplicativo do cliente) está autorizado a se conectar ao nome do usuário do banco de dados que foi solicitado.

O PostgreSQL oferece vários métodos diferentes de autenticação de clientes. O método usado para autenticar uma conexão específica de cliente pode ser selecionado com base no endereço do (cliente) host, banco de dados e usuário.

Os nomes de usuários do banco de dados PostgreSQL são logicamente separados dos nomes de usuários do sistema operacional no qual o servidor é executado. Se todos os usuários de um servidor específico também tiverem contas na máquina do servidor, faz sentido atribuir nomes de usuários do banco de dados que correspondam aos nomes de usuários do sistema operacional. No entanto, um servidor que aceita conexões remotas pode ter muitos usuários do banco de dados que não têm conta no sistema operacional local, e, nesses casos, não há necessidade de haver uma conexão entre os nomes de usuários do banco de dados e os nomes de usuários do sistema operacional.