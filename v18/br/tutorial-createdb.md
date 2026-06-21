## 1.3. Criando um banco de dados [#](#TUTORIAL-CREATEDB)

O primeiro teste para verificar se você pode acessar o servidor de banco de dados é tentar criar um banco de dados. Um servidor PostgreSQL em execução pode gerenciar muitos bancos de dados. Normalmente, um banco de dados separado é usado para cada projeto ou para cada usuário.

Possivelmente, o administrador do seu site já criou um banco de dados para o seu uso. Nesse caso, você pode omitir este passo e pular para a próxima seção.

Para criar um novo banco de dados a partir da linha de comando, neste exemplo chamado `mydb`, você usa o seguinte comando:

```
$ createdb mydb
```

Se não houver nenhuma resposta, então este passo foi bem-sucedido e você pode ignorar o restante desta seção.

Se você ver uma mensagem semelhante a:

```
createdb: command not found
```

então o PostgreSQL não foi instalado corretamente. Ou ele não foi instalado, ou o caminho de busca do seu shell não foi configurado para incluí-lo. Tente chamar o comando com um caminho absoluto em vez disso:

```
$ /usr/local/pgsql/bin/createdb mydb
```

O caminho no seu site pode ser diferente. Entre em contato com o administrador do site ou verifique as instruções de instalação para corrigir a situação.

Outra resposta poderia ser esta:

```
createdb: error: connection to server on socket "/tmp/.s.PGSQL.5432" failed: No such file or directory
        Is the server running locally and accepting connections on that socket?
```

Isso significa que o servidor não foi iniciado ou não está ouvindo onde o `createdb` espera contatá-lo. Novamente, verifique as instruções de instalação ou consulte o administrador.

Outra resposta poderia ser esta:

```
createdb: error: connection to server on socket "/tmp/.s.PGSQL.5432" failed: FATAL:  role "joe" does not exist
```

onde seu próprio nome de login é mencionado. Isso acontecerá se o administrador não criou uma conta de usuário do PostgreSQL para você. (As contas de usuário do PostgreSQL são distintas das contas de usuário do sistema operacional.) Se você é o administrador, consulte [Capítulo 21](user-manag.md) para obter ajuda na criação de contas. Você precisará se tornar o usuário do sistema operacional sob o qual o PostgreSQL foi instalado (geralmente `postgres`) para criar a primeira conta de usuário. Também pode ser que você tenha recebido um nome de usuário do PostgreSQL que é diferente do nome de usuário do seu sistema operacional; nesse caso, você precisa usar a chave `-U` ou definir a variável de ambiente `PGUSER` para especificar o nome do usuário do PostgreSQL.

Se você tiver uma conta de usuário, mas não tiver os privilégios necessários para criar um banco de dados, você verá o seguinte:

```
createdb: error: database creation failed: ERROR:  permission denied to create database
```

Nem todos os usuários têm autorização para criar novos bancos de dados. Se o PostgreSQL se recusar a criar bancos de dados para você, o administrador do site precisa conceder a você permissão para criar bancos de dados. Consulte o administrador do site se isso ocorrer. Se você instalou o PostgreSQL por si mesmo, então você deve fazer login para os propósitos deste tutorial sob a conta de usuário que você iniciou o servidor. [[1]](#ftn.id-1.4.3.4.10.4)

Você também pode criar bancos de dados com outros nomes. O PostgreSQL permite que você crie qualquer número de bancos de dados em um determinado site. Os nomes dos bancos de dados devem ter um primeiro caractere alfabético e são limitados a 63 bytes de comprimento. Uma escolha conveniente é criar um banco de dados com o mesmo nome do seu nome atual. Muitas ferramentas assumem que o nome do banco de dados é o padrão, então isso pode economizar algumas digitações. Para criar esse banco de dados, basta digitar:

```
$ createdb
```

Se você não quiser mais usar seu banco de dados, pode removê-lo. Por exemplo, se você é o proprietário (criador) do banco de dados `mydb`, pode destruí-lo usando o seguinte comando:

```
$ dropdb mydb
```

(Para este comando, o nome do banco de dados não é o nome da conta do usuário. Você sempre precisa especiá-lo.) Essa ação remove fisicamente todos os arquivos associados ao banco de dados e não pode ser desfeito, então isso deve ser feito apenas com muita reflexão.

Mais informações sobre `createdb` e `dropdb` podem ser encontradas em [createdb](app-createdb.md "createdb") e [dropdb](app-dropdb.md "dropdb"), respectivamente.

---

Como explicação para o porquê disso funcionar: os nomes de usuário do PostgreSQL são separados dos perfis de usuário do sistema operacional. Quando você se conecta a um banco de dados, pode escolher qual nome de usuário do PostgreSQL se conectar; se não fizer isso, ele será o mesmo nome do seu perfil de conta do sistema operacional. Como acontece, sempre haverá uma conta de usuário do PostgreSQL que tenha o mesmo nome do usuário do sistema operacional que iniciou o servidor, e também acontece que esse usuário sempre tem permissão para criar bancos de dados. Em vez de fazer login como esse usuário, você também pode especificar a opção `-U` em todos os lugares para selecionar um nome de usuário do PostgreSQL para se conectar.