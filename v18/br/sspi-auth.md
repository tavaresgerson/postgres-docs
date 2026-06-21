## 20.7. Autenticação SSPI [#](#SSPI-AUTH)

O SSPI é uma tecnologia do Windows para autenticação segura com acesso único. O PostgreSQL usará o SSPI no modo `negotiate`, que usará o Kerberos quando possível e, automaticamente, retornará ao NTLM em outros casos. O SSPI e o GSSAPI interagem como clientes e servidores, por exemplo, um cliente SSPI pode autenticar-se em um servidor GSSAPI. É recomendável usar o SSPI em clientes e servidores do Windows e o GSSAPI em plataformas que não são do Windows.

Ao usar autenticação Kerberos, o SSPI funciona da mesma maneira que o GSSAPI; consulte [Seção 20.6][(gssapi-auth.md "20.6. GSSAPI Authentication")] para obter detalhes.

As seguintes opções de configuração são suportadas para SSPI:

`include_realm`: Se configurado como 0, o nome do domínio do usuário autenticado é removido antes de ser passado pela mapeamento do nome do usuário ([Seção 20.2](auth-username-maps.md "20.2. User Name Maps")). Isso é desencorajado e está disponível principalmente para compatibilidade reversa, pois não é seguro em ambientes de vários domínios, a menos que `krb_realm` também seja usado. Recomenda-se deixar `include_realm` configurado com o valor padrão (1) e fornecer um mapeamento explícito em `pg_ident.conf` para converter nomes de principal em nomes de usuário do PostgreSQL.

`compat_realm`: Se configurado para 1, o nome compatível com SAM do domínio (também conhecido como nome NetBIOS) é usado para a opção `include_realm`. Este é o padrão. Se configurado para 0, o verdadeiro nome do domínio a partir do nome principal de usuário do Kerberos é usado.

Não desative esta opção, a menos que seu servidor esteja executando uma conta de domínio (isso inclui contas de serviço virtual em um sistema membro do domínio) e todos os clientes que se autenticam por meio do SSPI também estejam usando contas de domínio, ou a autenticação falhará.

`upn_username`: Se esta opção for habilitada juntamente com `compat_realm`, o nome do usuário do Kerberos UPN é usado para autenticação. Se estiver desabilitada (o padrão), o nome do usuário compatível com SAM é usado. Por padrão, esses dois nomes são idênticos para novas contas de usuário.

Observe que o libpq usa o nome compatível com SAM se nenhum nome de usuário explícito for especificado. Se você estiver usando o libpq ou um driver baseado nele, você deve deixar essa opção desativada ou especificar explicitamente o nome do usuário na cadeia de conexão.

`map`: Permite mapear entre os nomes de usuário do sistema e do banco de dados. Consulte a [Seção 20.2][(auth-username-maps.md "20.2. User Name Maps")] para obter detalhes. Para uma principal SSPI/Kerberos, como `username@EXAMPLE.COM` (ou, menos comumente, `username/hostbased@EXAMPLE.COM`), o nome de usuário usado para mapear é `username@EXAMPLE.COM` (ou `username/hostbased@EXAMPLE.COM`, respectivamente), a menos que `include_realm` tenha sido definido como 0, caso em que `username` (ou `username/hostbased`) é o que é visto como o nome de usuário do sistema durante a mapeo.

`krb_realm`: Define o domínio para corresponder aos nomes principais do usuário. Se este parâmetro for definido, apenas os usuários desse domínio serão aceitos. Se não for definido, os usuários de qualquer domínio podem se conectar, sujeito a qualquer mapeamento de nome de usuário que seja feito.