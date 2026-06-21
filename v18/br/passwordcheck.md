## F.24. passwordcheck — verificar a força da senha [#](#PASSWORDCHECK)

* [F.24.1. Parâmetros de Configuração](passwordcheck.md#PASSWORDCHECK-CONFIGURATION-PARAMETERS)

O módulo `passwordcheck` verifica as senhas dos usuários sempre que elas são definidas com [CREATE ROLE](sql-createrole.md "CREATE ROLE") ou [ALTER ROLE](sql-alterrole.md "ALTER ROLE"). Se uma senha for considerada muito fraca, ela será rejeitada e o comando terminará com um erro.

Para habilitar este módulo, adicione `'$libdir/passwordcheck'` a [shared_preload_libraries](runtime-config-client.md#GUC-SHARED-PRELOAD-LIBRARIES) em `postgresql.conf`, em seguida, reinicie o servidor.

Você pode adaptar este módulo às suas necessidades, alterando o código-fonte. Por exemplo, você pode usar [CrackLib](https://github.com/cracklib/cracklib) para verificar senhas — isso só requer a descomentar duas linhas no `Makefile` e a reconstrução do módulo. (Não podemos incluir CrackLib por razões de licença). Sem CrackLib, o módulo impõe algumas regras simples para a força da senha, que você pode modificar ou estender conforme desejar.

### Atenção

Para evitar que senhas não criptografadas sejam enviadas pela rede, escritas no log do servidor ou roubadas de outra forma por um administrador de banco de dados, o PostgreSQL permite que o usuário forneça senhas pré-criptografadas. Muitos programas cliente utilizam essa funcionalidade e criptografam a senha antes de enviá-la ao servidor.

Isso limita a utilidade do módulo `passwordcheck`, porque, nesse caso, ele só pode tentar adivinhar a senha. Por essa razão, `passwordcheck` não é recomendado se seus requisitos de segurança forem altos. É mais seguro usar um método de autenticação externo, como GSSAPI (consulte [Capítulo 20](client-authentication.md)), do que confiar em senhas dentro do banco de dados.

Como alternativa, você poderia modificar `passwordcheck` para rejeitar senhas pré-encriptadas, mas forçar os usuários a definir suas senhas em texto claro traz seus próprios riscos de segurança.

### F.24.1. Parâmetros de configuração [#](#PASSWORDCHECK-CONFIGURATION-PARAMETERS)

`passwordcheck.min_password_length` (`integer`): O comprimento mínimo aceitável da senha em bytes. O padrão é 8. Somente os usuários super podem alterar essa configuração.

### Nota

Este parâmetro não tem efeito se o usuário fornecer uma senha pré-encriptada.

No uso comum, este parâmetro é definido em `postgresql.conf`, mas os usuários super podem alterá-lo em tempo real dentro de suas próprias sessões. O uso típico pode ser:

```
# postgresql.conf
passwordcheck.min_password_length = 12
```
