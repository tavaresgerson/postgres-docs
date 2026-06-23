## 20.3. Métodos de autenticação [#](#AUTH-METHODS)

PostgreSQL oferece vários métodos para autenticação de usuários:

* [Autenticação por confiança](auth-trust.md "20.4. Trust Authentication"), que simplesmente confia que os usuários são quem dizem ser.
* [Autenticação por senha](auth-password.md "20.5. Password Authentication"), que exige que os usuários enviem uma senha.
* [Autenticação GSSAPI](gssapi-auth.md "20.6. GSSAPI Authentication"), que depende de uma biblioteca de segurança compatível com GSSAPI. Tipicamente, isso é usado para acessar um servidor de autenticação, como um servidor Kerberos ou Microsoft Active Directory.
* [Autenticação SSPI](sspi-auth.md "20.7. SSPI Authentication"), que usa um protocolo específico do Windows semelhante ao GSSAPI.
* [Autenticação Ident](auth-ident.md "20.8. Ident Authentication"), que depende de um serviço de "Protocolo de Identificação" ([RFC 1413](https://datatracker.ietf.org/doc/html/rfc1413)) na máquina do cliente. (Em conexões locais de socket Unix, isso é tratado como autenticação de igual para igual.)
* [Autenticação Peer](auth-peer.md "20.9. Peer Authentication"), que depende das facilidades do sistema operacional para identificar o processo do outro lado de uma conexão local. Isso não é suportado para conexões remotas.
* [Autenticação LDAP](auth-ldap.md "20.10. LDAP Authentication"), que depende de um servidor de autenticação LDAP.
* [Autenticação RADIUS](auth-radius.md "20.11. RADIUS Authentication"), que depende de um servidor de autenticação RADIUS.
* [Autenticação por certificado](auth-cert.md "20.12. Certificate Authentication"), que exige uma conexão SSL e autentica os usuários verificando o certificado SSL que eles enviam.
* [Autenticação PAM](auth-pam.md "20.13. PAM Authentication"), que depende de uma biblioteca de módulos de autenticação plugável (PAM - Pluggable Authentication Modules).
* [Autenticação BSD](auth-bsd.md "20.14. BSD Authentication"), que depende da estrutura de autenticação BSD (atualmente disponível apenas no OpenBSD).
* [Autenticação OAuth/autorização](auth-oauth.md "20.15. OAuth Authorization/Authentication"), que depende de um provedor de identidade OAuth 2.0 externo.

A autenticação de pares é geralmente recomendada para conexões locais, embora a autenticação de confiança possa ser suficiente em algumas circunstâncias. A autenticação por senha é a opção mais fácil para conexões remotas. Todas as outras opções exigem algum tipo de infraestrutura de segurança externa (geralmente um servidor de autenticação ou uma autoridade de certificação para emitir certificados SSL) ou são específicas para a plataforma.

As seções a seguir descrevem cada um desses métodos de autenticação com mais detalhes.