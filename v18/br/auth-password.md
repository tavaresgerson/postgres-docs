## 20.5. Autenticação por senha [#](#AUTH-PASSWORD)

Existem vários métodos de autenticação baseados em senha. Esses métodos funcionam de maneira semelhante, mas diferem na forma como as senhas dos usuários são armazenadas no servidor e na forma como a senha fornecida por um cliente é enviada através da conexão.

`scram-sha-256`: O método `scram-sha-256` realiza a autenticação SCRAM-SHA-256, conforme descrito em [RFC 7677](https://datatracker.ietf.org/doc/html/rfc7677). É um esquema de desafio-resposta que impede o rastreamento de senhas em conexões não confiáveis e suporta o armazenamento de senhas no servidor em uma forma criptografada que é considerada segura.

Este é o método mais seguro dos atualmente fornecidos, mas não é suportado por bibliotecas de cliente mais antigas.

`md5`: O método `md5` utiliza um mecanismo de desafio e resposta menos seguro personalizado. Ele previne o rastreamento de senhas e evita armazenar senhas no servidor em texto plano, mas não oferece proteção se um invasor conseguir roubar o hash da senha do servidor. Além disso, o algoritmo de hash MD5 já não é considerado seguro contra ataques determinados.

Para facilitar a transição do método `md5` para o método SCRAM mais recente, se `md5` for especificado como método em `pg_hba.conf`, mas a senha do usuário no servidor estiver criptografada para SCRAM (veja abaixo), então a autenticação baseada em SCRAM será escolhida automaticamente.

### Aviso

O suporte para senhas criptografadas com MD5 é desatualizado e será removido em uma versão futura do PostgreSQL. Consulte o texto abaixo para obter detalhes sobre a migração para outro tipo de senha.

`password`: O método `password` envia a senha em texto claro e, portanto, é vulnerável a ataques de "sniffing" de senhas. Deve ser evitado sempre que possível. Se a conexão estiver protegida por criptografia SSL, então `password` pode ser usado com segurança, embora. (Embora a autenticação com certificado SSL possa ser uma escolha melhor se alguém depende do uso do SSL).

As senhas do banco de dados PostgreSQL são separadas das senhas do usuário do sistema operacional. A senha de cada usuário do banco de dados é armazenada no catálogo do sistema `pg_authid`. As senhas podem ser gerenciadas com os comandos SQL [CREATE ROLE](sql-createrole.md "CREATE ROLE") e [ALTER ROLE](sql-alterrole.md "ALTER ROLE"), por exemplo, **`CREATE ROLE foo WITH LOGIN PASSWORD 'secret'`**, ou o comando psql `\password`. Se nenhuma senha tiver sido configurada para um usuário, a senha armazenada é nula e a autenticação de senha sempre falhará para esse usuário.

A disponibilidade dos diferentes métodos de autenticação baseados em senha depende de como a senha de um usuário no servidor é criptografada (ou, mais precisamente, hashada). Isso é controlado pelo parâmetro de configuração [password_encryption][(runtime-config-connection.md#GUC-PASSWORD-ENCRYPTION)] no momento em que a senha é definida. Se uma senha foi criptografada usando a configuração `scram-sha-256`, então ela pode ser usada para os métodos de autenticação `scram-sha-256` e `password` (mas a transmissão da senha será em texto plano no último caso). A especificação do método de autenticação `md5` mudará automaticamente para usar o método `scram-sha-256` neste caso, como explicado acima, então também funcionará. Se uma senha foi criptografada usando a configuração `md5`, então ela pode ser usada apenas para as especificações de métodos de autenticação `md5` e `password` (novamente, com a senha transmitida em texto plano no último caso). (As versões anteriores do PostgreSQL suportavam o armazenamento das hashas de senha no servidor em texto plano. Isso não é mais possível.) Para verificar as hashas de senha armazenadas atualmente, consulte o catálogo do sistema `pg_authid`.

Para atualizar uma instalação existente de `md5` para `scram-sha-256`, após garantir que todas as bibliotecas de cliente em uso sejam novas o suficiente para suportar SCRAM, configure `password_encryption = 'scram-sha-256'` em `postgresql.conf`, faça com que todos os usuários definam novas senhas e mude as especificações do método de autenticação em `pg_hba.conf` para `scram-sha-256`.