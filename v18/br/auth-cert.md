## 20.12. Autenticação de certificado [#](#AUTH-CERT)

Este método de autenticação utiliza certificados de cliente SSL para realizar a autenticação. Portanto, ele só está disponível para conexões SSL; consulte [Seção 18.9.2][(ssl-tcp.md#SSL-OPENSSL-CONFIG "18.9.2. OpenSSL Configuration")] para instruções de configuração SSL. Ao usar este método de autenticação, o servidor exigirá que o cliente forneça um certificado válido e confiável. Não será enviada nenhuma solicitação de senha ao cliente. O atributo `cn` (Nome Comum) do certificado será comparado ao nome do usuário do banco de dados solicitado, e se corresponderem, o login será permitido. O mapeamento do nome do usuário pode ser usado para permitir que `cn` seja diferente do nome do usuário do banco de dados.

As seguintes opções de configuração são suportadas para autenticação com certificado SSL:

`map`: Permite mapear entre os nomes de usuários do sistema e do banco de dados. Consulte a [Seção 20.2][(auth-username-maps.md "20.2. User Name Maps")] para obter detalhes.

É redundante usar a opção `clientcert` com autenticação `cert`, porque a autenticação `cert` é efetivamente a autenticação `trust` com `clientcert=verify-full`.