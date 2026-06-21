## 20.15. Autorização/Autenticação OAuth [#](#AUTH-OAUTH)

O OAuth 2.0 é uma estrutura padrão da indústria, definida em [RFC 6749](https://datatracker.ietf.org/doc/html/rfc6749), para permitir que aplicativos de terceiros obtenham acesso limitado a um recurso protegido. O suporte ao cliente OAuth deve ser habilitado quando o PostgreSQL é construído, consulte [Capítulo 17](installation.md) para mais informações.

Esta documentação utiliza a seguinte terminologia ao discutir o ecossistema OAuth:

Proprietário do recurso (ou Usuário final): O usuário ou sistema que possui recursos protegidos e pode conceder acesso a eles. Esta documentação também usa o termo *usuário final* quando o proprietário do recurso é uma pessoa. Quando você usa o psql para se conectar ao banco de dados usando OAuth, você é o proprietário do recurso/usuário final.

Cliente: O sistema que acessa os recursos protegidos usando tokens de acesso. As aplicações que utilizam o libpq, como psql, são os clientes OAuth ao se conectarem a um clúster PostgreSQL.

Servidor de recursos: O sistema que hospeda os recursos protegidos que são acessados pelo cliente. O clúster PostgreSQL que está conectado é o servidor de recursos.

Fornecedor: A organização, o fornecedor do produto ou outra entidade que desenvolve e/ou administra os servidores e clientes de autorização OAuth para um aplicativo específico. Geralmente, diferentes provedores escolhem detalhes de implementação diferentes para seus sistemas OAuth; um cliente de um provedor geralmente não tem garantia de acesso aos servidores de outro.

Esse uso do termo "provedor" não é padrão, mas parece estar em uso coloquial. (Não deve ser confundido com o termo semelhante do OpenID "Fornecedor de Identidade". Embora a implementação do OAuth no PostgreSQL seja destinada a ser interoperável e compatível com o OpenID Connect/OIDC, ele não é ele mesmo um cliente OIDC e não requer seu uso.)

Servidor de Autorização: O sistema que recebe solicitações e emite tokens de acesso ao cliente após o proprietário do recurso autenticado ter dado aprovação. O PostgreSQL não fornece um servidor de autorização; é responsabilidade do provedor OAuth.

Emissor: Um identificador para um servidor de autorização, impresso como um URL `https://`, que fornece um "namespace" confiável para clientes e aplicativos OAuth. O identificador do emissor permite que um único servidor de autorização fale com os clientes de entidades mutuamente desconfiadas, desde que mantenham emissores separados.

### Nota

Para implantações pequenas, pode não haver uma distinção significativa entre o "provedor", o "servidor de autorização" e o "emissor". No entanto, para configurações mais complicadas, pode haver uma relação de um para muitos (ou muitos para muitos): um provedor pode alugar vários identificadores de emissor para inquilinos separados, e, em seguida, fornecer vários servidores de autorização, possivelmente com diferentes conjuntos de recursos suportados, para interagir com seus clientes.

O PostgreSQL suporta tokens de portador, definidos em [RFC 6750](https://datatracker.ietf.org/doc/html/rfc6750), que são um tipo de token de acesso usado com OAuth 2.0, onde o token é uma string opaca. O formato do token de acesso é específico da implementação e é escolhido por cada servidor de autorização.

As seguintes opções de configuração são suportadas para OAuth:

`issuer`: Um URL HTTPS que é o identificador exato do [emissor](auth-oauth.md#AUTH-OAUTH-ISSUER) do servidor de autorização, conforme definido em seu documento de descoberta, ou um URI bem conhecido que aponta diretamente para esse documento de descoberta. Este parâmetro é obrigatório.

Quando um cliente OAuth se conecta ao servidor, uma URL para o documento de descoberta será construída usando o identificador do emissor. Por padrão, essa URL usa as convenções do OpenID Connect Discovery: o caminho `/.well-known/openid-configuration` será anexado ao final do identificador do emissor. Alternativamente, se o `issuer` contiver um segmento de caminho `/.well-known/`, essa URL será fornecida ao cliente como está.

### Aviso

O cliente OAuth no libpq exige que a configuração do emissor do servidor corresponda exatamente ao identificador do emissor fornecido no documento de descoberta, que, por sua vez, deve corresponder à configuração do cliente [oauth_issuer](libpq-connect.md#LIBPQ-CONNECT-OAUTH-ISSUER). Nenhuma variação em termos de caso ou formatação é permitida.

`scope`: Uma lista separada por espaços dos escopos OAuth necessários para que o servidor autorize o cliente e autentique o usuário. Os valores apropriados são determinados pelo servidor de autorização e pelo módulo de validação OAuth utilizado (consulte o [Capítulo 50](oauth-validators.md) para obter mais informações sobre validadores). Este parâmetro é obrigatório.

`validator`: A biblioteca a ser usada para validar tokens de portador. Se fornecida, o nome deve corresponder exatamente a um dos nomes das bibliotecas listadas em [oauth_validator_libraries](runtime-config-connection.md#GUC-OAUTH-VALIDATOR-LIBRARIES). Este parâmetro é opcional, a menos que `oauth_validator_libraries` contenha mais de uma biblioteca, no qual caso é necessário.

`map`: Permite mapear entre os nomes de usuários do provedor de identidade OAuth e os nomes de usuários do banco de dados. Consulte [Seção 20.2](auth-username-maps.md) para obter detalhes. Se um mapa não for especificado, o nome de usuário associado ao token (determinado pelo validador OAuth) deve corresponder exatamente ao nome do papel solicitado. Este parâmetro é opcional.

`delegate_ident_mapping`: Uma opção avançada que não é destinada ao uso comum.

Quando configurado para `1`, o mapeamento padrão do usuário com `pg_ident.conf` é ignorado, e o validador OAuth assume a total responsabilidade pelo mapeamento das identidades dos usuários finais aos papéis do banco de dados. Se o validador autorizar o token, o servidor confia que o usuário está autorizado a se conectar sob o papel solicitado, e a conexão é permitida para prosseguir, independentemente do status de autenticação do usuário.

Este parâmetro é incompatível com `map`.

### Aviso

`delegate_ident_mapping` oferece flexibilidade adicional no projeto do sistema de autenticação, mas também exige uma implementação cuidadosa do validador OAuth, que deve determinar se o token fornecido possui privilégios suficientes do usuário final, além dos [checks padrão](oauth-validators.md) exigidos de todos os validadores. Use com cautela.