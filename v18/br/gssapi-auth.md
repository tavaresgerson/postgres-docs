## 20.6. Autenticação GSSAPI [#](#GSSAPI-AUTH)

O GSSAPI é um protocolo padrão da indústria para autenticação segura definido em [RFC 2743][(https://datatracker.ietf.org/doc/html/rfc2743)]. O PostgreSQL suporta GSSAPI para autenticação, criptografia de comunicações ou ambas. O GSSAPI oferece autenticação automática (login único) para sistemas que o suportam. A autenticação em si é segura. Se a criptografia GSSAPI ou SSL for usada, os dados enviados ao longo da conexão do banco de dados serão criptografados; caso contrário, não serão.

O suporte GSSAPI precisa ser habilitado quando o PostgreSQL é construído; consulte [Capítulo 17][(installation.md "Chapter 17. Installation from Source Code")] para mais informações.

Quando o GSSAPI usa o Kerberos, ele usa um nome padrão de principal de serviço (identidade de autenticação) no formato `servicename/hostname@realm`. O nome da principal usado por uma instalação específica não é codificado no servidor PostgreSQL de nenhuma maneira; em vez disso, é especificado no arquivo *keytab* que o servidor lê para determinar sua identidade. Se vários princípios estão listados no arquivo keytab, o servidor aceitará qualquer um deles. O nome do domínio do servidor é o domínio preferido especificado no(s) arquivo(s) de configuração Kerberos acessível(eis) ao servidor.

Ao se conectar, o cliente deve conhecer o nome principal do servidor ao qual pretende se conectar. A parte *`servicename`* do principal é normalmente `postgres`, mas outro valor pode ser selecionado através do parâmetro de conexão [krbsrvname][(libpq-connect.md#LIBPQ-CONNECT-KRBSRVNAME) de libpq. A parte *`hostname`* é o nome de host totalmente qualificado que a libpq é informada para se conectar. O nome do domínio é o domínio preferido especificado no(s) arquivo(s) de configuração Kerberos acessível(eis) ao cliente.

O cliente também terá um nome principal para sua própria identidade (e deve ter um ticket válido para esse principal). Para usar o GSSAPI para autenticação, o nome do principal do cliente deve ser associado a um nome de usuário de banco de dados PostgreSQL. O arquivo de configuração `pg_ident.conf` pode ser usado para mapear os principais a nomes de usuário; por exemplo, `pgusername@realm` pode ser mapeado para apenas `pgusername`. Alternativamente, você pode usar o principal completo `username@realm` como o nome do papel no PostgreSQL sem qualquer mapeamento.

O PostgreSQL também suporta a mapeo de princípios de cliente para nomes de usuário, simplesmente removendo o domínio do princípio. Esse método é suportado para compatibilidade reversa e é fortemente desencorajado, pois é impossível distinguir diferentes usuários com o mesmo nome de usuário, mas provenientes de diferentes domínios. Para habilitar isso, defina `include_realm` para 0. Para instalações simples de único domínio, fazer isso combinado com a definição do parâmetro `krb_realm` (que verifica se o domínio do princípio corresponde exatamente ao que está no parâmetro `krb_realm`) ainda é seguro; mas essa é uma abordagem menos capaz em comparação com a especificação de um mapeo explícito em `pg_ident.conf`.

A localização do arquivo keytab do servidor é especificada pelo parâmetro de configuração [krb_server_keyfile](runtime-config-connection.md#GUC-KRB-SERVER-KEYFILE). Por razões de segurança, é recomendável usar um arquivo keytab separado apenas para o servidor PostgreSQL, em vez de permitir que o servidor leia o arquivo keytab do sistema. Certifique-se de que o arquivo keytab do seu servidor seja legível (e, de preferência, apenas legível, não gravável) pela conta do servidor PostgreSQL. (Veja também [Seção 18.1](postgres-user.md "18.1. The PostgreSQL User Account").

O arquivo keytab é gerado usando o software Kerberos; consulte a documentação do Kerberos para obter detalhes. O exemplo a seguir mostra como fazer isso usando a ferramenta kadmin do Kerberos do MIT:

```
kadmin% addprinc -randkey postgres/server.my.domain.org
kadmin% ktadd -k krb5.keytab postgres/server.my.domain.org
```

As seguintes opções de autenticação são suportadas para o método de autenticação GSSAPI:

`include_realm`: Se configurado como 0, o nome do domínio do usuário autenticado é removido antes de ser passado pela mapeamento do nome do usuário ([Seção 20.2](auth-username-maps.md "20.2. User Name Maps")). Isso é desencorajado e está disponível principalmente para compatibilidade reversa, pois não é seguro em ambientes de vários domínios, a menos que `krb_realm` também seja usado. Recomenda-se deixar `include_realm` configurado no padrão (1) e fornecer um mapeamento explícito em `pg_ident.conf` para converter nomes de principal em nomes de usuário do PostgreSQL.

`map`: Permite mapear os princípios do cliente para os nomes de usuário do banco de dados. Consulte a [Seção 20.2][(auth-username-maps.md "20.2. User Name Maps")] para obter detalhes. Para um princípio GSSAPI/Kerberos, como `username@EXAMPLE.COM` (ou, menos comumente, `username/hostbased@EXAMPLE.COM`), o nome de usuário usado para mapear é `username@EXAMPLE.COM` (ou `username/hostbased@EXAMPLE.COM`, respectivamente), a menos que `include_realm` tenha sido definido como 0, caso em que `username` (ou `username/hostbased`) é o que é visto como o nome de usuário do sistema durante a mapeo.

`krb_realm`: Define o domínio para corresponder aos nomes principais do usuário. Se este parâmetro for definido, apenas os usuários desse domínio serão aceitos. Se não for definido, os usuários de qualquer domínio podem se conectar, sujeito a qualquer mapeamento de nome de usuário que seja feito.

Além desses ajustes, que podem ser diferentes para diferentes entradas do `pg_hba.conf`, há o parâmetro de configuração [krb_caseins_users](runtime-config-connection.md#GUC-KRB-CASEINS-USERS) para todo o servidor. Se estiver definido como verdadeiro, os princípios dos clientes são correspondidos às entradas do mapa de usuários de forma insensível ao caso. `krb_realm`, se definido, também é correspondido de forma insensível ao caso.