## 18.8. Opções de criptografia [#](#ENCRYPTION-OPTIONS)

O PostgreSQL oferece criptografia em vários níveis e oferece flexibilidade para proteger os dados contra divulgação devido ao roubo do servidor do banco de dados, administradores sem escrúpulos e redes inseguras. A criptografia também pode ser necessária para proteger dados sensíveis, como registros médicos ou transações financeiras.

Encriptação da senha: As senhas dos usuários do banco de dados são armazenadas como hashes (determinados pelo ajuste [password_encryption][(runtime-config-connection.md#GUC-PASSWORD-ENCRYPTION)]), portanto, o administrador não pode determinar a senha real atribuída ao usuário. Se a encriptação SCRAM ou MD5 for usada para autenticação de cliente, a senha não encriptada nunca está presente temporariamente no servidor, porque o cliente a encripta antes de ser enviada pela rede. O SCRAM é preferido, porque é um padrão da Internet e é mais seguro do que o protocolo de autenticação MD5 específico do PostgreSQL.

### Aviso

O suporte para senhas criptografadas com MD5 é desatualizado e será removido em uma versão futura do PostgreSQL. Consulte [Seção 20.5][(auth-password.md "20.5. Password Authentication")] para obter detalhes sobre a migração para outro tipo de senha.

Encriptação para colunas específicas: O módulo [pgcrypto][(pgcrypto.md "F.26. pgcrypto — cryptographic functions")] permite que certos campos sejam armazenados encriptados. Isso é útil se apenas alguns dos dados forem sensíveis. O cliente fornece a chave de descriptografia e os dados são descriptografados no servidor e, em seguida, enviados ao cliente.

Os dados descifrados e a chave de descriptografia estão presentes no servidor por um breve período enquanto estão sendo descifrados e comunicados entre o cliente e o servidor. Isso apresenta um breve momento em que os dados e as chaves podem ser interceptados por alguém com acesso completo ao servidor de banco de dados, como o administrador do sistema.

Encriptação de Partição de Dados: A encriptação de armazenamento pode ser realizada no nível do sistema de arquivos ou no nível do bloco. As opções de encriptação de sistema de arquivos Linux incluem eCryptfs e EncFS, enquanto o FreeBSD usa PEFS. As opções de encriptação de nível de bloco ou disco completo incluem dm-crypt + LUKS no Linux e os módulos GEOM geli e gbde no FreeBSD. Muitas outras sistemas operacionais suportam essa funcionalidade, incluindo o Windows.

Esse mecanismo impede que dados não criptografados sejam lidos dos discos se os discos ou o computador inteiro forem roubados. Isso não protege contra ataques enquanto o sistema de arquivos estiver montado, porque, quando montado, o sistema operacional fornece uma visão não criptografada dos dados. No entanto, para montar o sistema de arquivos, você precisa de uma maneira de que a chave de criptografia seja passada para o sistema operacional, e, às vezes, a chave é armazenada em algum lugar no host que monta o disco.

Encriptar dados em uma rede: as conexões SSL encriptam todos os dados enviados em uma rede: a senha, as consultas e os dados retornados. O arquivo `pg_hba.conf` permite que os administradores especifiquem quais hosts podem usar conexões não encriptadas (`host`) e quais exigem conexões criptografadas SSL (`hostssl`). Além disso, os clientes podem especificar que se conectam aos servidores apenas via SSL.

As conexões criptografadas GSSAPI criptografam todos os dados enviados pela rede, incluindo consultas e dados retornados. (Nenhuma senha é enviada pela rede.) O arquivo `pg_hba.conf` permite que os administradores especifiquem quais hosts podem usar conexões não criptografadas (`host`) e quais exigem conexões criptografadas GSSAPI (`hostgssenc`). Além disso, os clientes podem especificar que se conectam a servidores apenas em conexões criptografadas GSSAPI (`gssencmode=require`).

Stunnel ou SSH também pode ser usado para criptografar as transmissões.

Autenticação de Host SSL: É possível que tanto o cliente quanto o servidor forneçam certificados SSL um ao outro. Isso requer alguma configuração extra em cada lado, mas isso oferece uma verificação de identidade mais forte do que o mero uso de senhas. Isso impede que um computador finja ser o servidor por um período de tempo suficiente para ler a senha enviada pelo cliente. Também ajuda a prevenir ataques de "homem no meio do caminho", onde um computador entre o cliente e o servidor finge ser o servidor e lê e passa todos os dados entre o cliente e o servidor.

Criptografia no lado do cliente: Se o administrador do sistema da máquina do servidor não pode ser confiável, é necessário que o cliente criptografar os dados; dessa forma, os dados não criptografados nunca aparecem no servidor do banco de dados. Os dados são criptografados no cliente antes de serem enviados ao servidor, e os resultados do banco de dados devem ser descriptografados no cliente antes de serem usados.