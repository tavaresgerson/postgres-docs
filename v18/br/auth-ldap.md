## 20.10. Autenticação LDAP [#](#AUTH-LDAP)

Este método de autenticação opera de forma semelhante ao `password`, exceto que ele usa LDAP como o método de verificação de senha. O LDAP é usado apenas para validar os pares de nome/senha do usuário. Portanto, o usuário deve já existir no banco de dados antes que o LDAP possa ser usado para autenticação.

A autenticação LDAP pode operar em dois modos. No primeiro modo, que chamaremos de modo de vinculação simples, o servidor se vincula ao nome distinto construído como *`prefix`* *`username`* *`suffix`*. Tipicamente, o parâmetro *`prefix`* é usado para especificar `cn=`, ou *`DOMAIN`*[[`\`] em um ambiente de Active Directory. *`suffix`* é usado para especificar a parte restante do DN em um ambiente não de Active Directory.

No segundo modo, que chamaremos de modo de busca+vinculação, o servidor primeiro se vincula ao diretório LDAP com um nome de usuário e senha fixos, especificados com *`ldapbinddn`* e *`ldapbindpasswd`*, e realiza uma busca pelo usuário que está tentando fazer login no banco de dados. Se não houver usuário e senha configurados, será realizada uma vinculação anônima ao diretório. A busca será realizada sobre a subárvore em *`ldapbasedn`*, e tentará realizar uma correspondência exata do atributo especificado em *`ldapsearchattribute`*. Uma vez que o usuário tenha sido encontrado nesta busca, o servidor se vincula novamente ao diretório como este usuário, usando a senha especificada pelo cliente, para verificar se o login é correto. Este modo é o mesmo que o usado pelos esquemas de autenticação LDAP em outros softwares, como o Apache `mod_authnz_ldap` e `pam_ldap`. Este método permite uma flexibilidade significativamente maior sobre onde os objetos do usuário estão localizados no diretório, mas causará duas solicitações adicionais ao servidor LDAP.

As seguintes opções de configuração são usadas em ambos os modos:

`ldapserver`: Nomes ou endereços IP dos servidores LDAP a serem conectados. Pode-se especificar vários servidores, separados por espaços.

`ldapport`: Número de porta no servidor LDAP para se conectar. Se não for especificado nenhum número de porta, o ajuste padrão da porta da biblioteca LDAP será utilizado.

`ldapscheme`: Defina para `ldaps` para usar LDAPS. Esta é uma maneira não padrão de usar LDAP sobre SSL, suportada por algumas implementações de servidor LDAP. Consulte também a opção `ldaptls` para uma alternativa.

`ldaptls`: Defina para 1 para fazer com que a conexão entre o PostgreSQL e o servidor LDAP use criptografia TLS. Isso utiliza a operação `StartTLS` conforme [RFC 4513](https://datatracker.ietf.org/doc/html/rfc4513). Veja também a opção `ldapscheme` para uma alternativa.

Observe que o uso de `ldapscheme` ou `ldaptls` apenas criptografa o tráfego entre o servidor PostgreSQL e o servidor LDAP. A conexão entre o servidor PostgreSQL e o cliente PostgreSQL ainda será não criptografada, a menos que SSL também seja usado.

As seguintes opções são usadas apenas no modo de vinculação simples:

`ldapprefix`: String para prependido ao nome do usuário ao formar o DN para vincular como, ao realizar autenticação de vinculação simples.

`ldapsuffix`: String para adicionar ao nome do usuário ao formar o DN para se ligar como, ao realizar autenticação de ligação simples.

As seguintes opções são usadas apenas no modo search+bind:

`ldapbasedn`: DN raiz para iniciar a pesquisa do usuário, ao realizar a autenticação de busca+ligação.

`ldapbinddn`: DN do usuário a ser vinculado ao diretório para realizar a pesquisa ao realizar autenticação de pesquisa+vinculação.

`ldapbindpasswd`: Senha para o usuário se vincular ao diretório para realizar a pesquisa ao realizar a autenticação de pesquisa+vinculação.

`ldapsearchattribute`: Atributo para corresponder ao nome do usuário na busca quando realizar autenticação de busca+vinculação. Se nenhum atributo for especificado, o atributo `uid` será usado.

`ldapsearchfilter`: O filtro de busca a ser usado ao realizar autenticação de busca+ligação. As ocorrências de `$username` serão substituídas pelo nome do usuário. Isso permite filtros de busca mais flexíveis do que `ldapsearchattribute`.

A opção a seguir pode ser usada como uma forma alternativa de escrever algumas das opções LDAP acima de forma mais compacta e padrão:

`ldapurl`: Um URL LDAP [RFC 4516][(https://datatracker.ietf.org/doc/html/rfc4516)]. O formato é

``` ldap[s]://host[:port]/basedn[?[attribute][?[scope][?[filter]]]]
    ```

*`scope`* deve ser um dos `base`, `one`, `sub`, normalmente o último. (O padrão é `base`, que normalmente não é útil nesta aplicação.) *`attribute`* pode nominar um único atributo, nesse caso, é usado como um valor para `ldapsearchattribute`. Se *`attribute`* estiver vazio, então *`filter`* pode ser usado como um valor para `ldapsearchfilter`.

O esquema de URL `ldaps` escolhe o método LDAPS para fazer conexões LDAP sobre SSL, equivalente ao uso de `ldapscheme=ldaps`. Para usar conexões LDAP criptografadas usando a operação `StartTLS`, use o esquema de URL normal `ldap` e especifique a opção `ldaptls`, além de `ldapurl`.

Para vincos não anônimos, `ldapbinddn` e `ldapbindpasswd` devem ser especificados como opções separadas.

Atualmente, os URLs LDAP são suportados apenas com o OpenLDAP, não no Windows.

É um erro misturar opções de configuração para bind simples com opções para search+bind. Para usar `ldapurl` no modo bind simples, o URL não deve conter elementos `basedn` ou de consulta.

Ao usar o modo de busca+bind, a busca pode ser realizada usando um único atributo especificado com `ldapsearchattribute`, ou usando um filtro de busca personalizado especificado com `ldapsearchfilter`. Especificar `ldapsearchattribute=foo` é equivalente a especificar `ldapsearchfilter="(foo=$username)"`. Se nenhuma opção for especificada, o padrão é `ldapsearchattribute=uid`.

Se o PostgreSQL foi compilado com o OpenLDAP como a biblioteca de clientes LDAP, o ajuste `ldapserver` pode ser omitido. Nesse caso, uma lista de nomes de host e portas é consultada através dos registros DNS SRV [RFC 2782][(https://datatracker.ietf.org/doc/html/rfc2782)]. O nome `_ldap._tcp.DOMAIN` é procurado, onde `DOMAIN` é extraído de `ldapbasedn`.

Aqui está um exemplo para uma configuração LDAP simples:

```
host ... ldap ldapserver=ldap.example.net ldapprefix="cn=" ldapsuffix=", dc=example, dc=net"
```

Quando é solicitada uma conexão com o servidor de banco de dados como usuário do banco de dados `someuser`, o PostgreSQL tentará se vincular ao servidor LDAP usando o DN `cn=someuser, dc=example, dc=net` e a senha fornecida pelo cliente. Se essa conexão for bem-sucedida, o acesso ao banco de dados é concedido.

Aqui está uma configuração de vinculação simples diferente, que utiliza o esquema LDAPS e um número de porta personalizado, escrito como um URL:

```
host ... ldap ldapurl="ldaps://ldap.example.net:49151" ldapprefix="cn=" ldapsuffix=", dc=example, dc=net"
```

Isso é um pouco mais compacto do que especificar `ldapserver`, `ldapscheme` e `ldapport` separadamente.

Aqui está um exemplo para uma configuração de busca+vinculação:

```
host ... ldap ldapserver=ldap.example.net ldapbasedn="dc=example, dc=net" ldapsearchattribute=uid
```

Quando é solicitada uma conexão com o servidor de banco de dados como usuário de banco de dados `someuser`, o PostgreSQL tentará vincular-se anonimamente (já que `ldapbinddn` não foi especificado) ao servidor LDAP, realizar uma busca por `(uid=someuser)` sob o DN de base especificado. Se uma entrada for encontrada, então tentará vincular-se usando as informações encontradas e a senha fornecida pelo cliente. Se essa segunda vinculação tiver sucesso, o acesso ao banco de dados é concedido.

Aqui está a mesma configuração de busca + bind escrita como um URL:

```
host ... ldap ldapurl="ldap://ldap.example.net/dc=example,dc=net?uid?sub"
```

Alguns outros softwares que suportam autenticação contra LDAP usam o mesmo formato de URL, então será mais fácil compartilhar a configuração.

Aqui está um exemplo para uma configuração de busca e vinculação que utiliza `ldapsearchfilter` em vez de `ldapsearchattribute` para permitir a autenticação por ID de usuário ou endereço de e-mail:

```
host ... ldap ldapserver=ldap.example.net ldapbasedn="dc=example, dc=net" ldapsearchfilter="(|(uid=$username)(mail=$username))"
```

Aqui está um exemplo para uma configuração de busca e vinculação que utiliza a descoberta DNS SRV para encontrar o nome(s) do(s) host(es) e a(s) porta(s) para o serviço LDAP para o nome de domínio `example.net`:

```
host ... ldap ldapbasedn="dc=example,dc=net"
```

### DICA

Como o LDAP frequentemente usa vírgulas e espaços para separar as diferentes partes de um DN, é frequentemente necessário usar valores de parâmetros com aspas duplas ao configurar opções LDAP, conforme mostrado nos exemplos.