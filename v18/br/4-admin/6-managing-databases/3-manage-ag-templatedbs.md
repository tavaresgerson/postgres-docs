## 22.3. Bancos de dados de modelo [#](#MANAGE-AG-TEMPLATEDBS)

O `CREATE DATABASE` funciona copiando um banco de dados existente. Por padrão, ele copia o banco de dados padrão do sistema chamado `template1`. Assim, esse banco de dados é o “modelo” a partir do qual novos bancos de dados são criados. Se você adicionar objetos ao `template1`, esses objetos serão copiados em bancos de dados de usuários posteriormente criados. Esse comportamento permite modificações locais no conjunto padrão de objetos nos bancos de dados. Por exemplo, se você instalar o PL/Perl de linguagem procedural no `template1`, ele será automaticamente disponível em bancos de dados de usuários sem nenhuma ação adicional quando esses bancos de dados forem criados.

No entanto, o `CREATE DATABASE` não copia as permissões de nível de banco de dados do `GRANT` anexadas ao banco de dados de origem. O novo banco de dados tem permissões padrão de nível de banco de dados.

Existe um segundo banco de dados padrão do sistema chamado `template0`. Este banco de dados contém os mesmos dados que o conteúdo inicial do `template1`, ou seja, apenas os objetos padrão definidos pela sua versão do PostgreSQL. `template0` nunca deve ser alterado após o clúster do banco de dados ter sido inicializado. Ao instruir o `CREATE DATABASE` a copiar `template0` em vez de `template1`, você pode criar um banco de dados de usuário “pura” (um onde não existem objetos definidos pelo usuário e onde os objetos do sistema não foram alterados) que não contenha nenhuma das adições locais do site em `template1`. Isso é particularmente útil ao restaurar um `pg_dump` dump: o script de dump deve ser restaurado em um banco de dados puro para garantir que se recree os conteúdos corretos do banco de dados descartado, sem conflitar com objetos que possam ter sido adicionados ao `template1` posteriormente.

Outra razão comum para copiar `template0` em vez de `template1` é que novas configurações de codificação e local podem ser especificadas ao copiar `template0`, enquanto uma cópia de `template1` deve usar as mesmas configurações que ela. Isso ocorre porque `template1` pode conter dados específicos de codificação ou específicos do local, enquanto `template0` não é conhecido por isso.

Para criar um banco de dados copiando `template0`, use:

```
CREATE DATABASE dbname TEMPLATE template0;
```

do ambiente SQL, ou:

```
createdb -T template0 dbname
```

da casca.

É possível criar bancos de dados de modelo adicionais, e, de fato, é possível copiar qualquer banco de dados em um clúster, especificando seu nome como o modelo para `CREATE DATABASE`. No entanto, é importante entender que isso (ainda) não é uma facilidade de propósito geral do tipo `COPY DATABASE`. A principal limitação é que nenhuma outra sessão pode ser conectada ao banco de dados de origem enquanto ele está sendo copiado. `CREATE DATABASE` falhará se houver alguma outra conexão existente quando ele for iniciado; durante a operação de cópia, novas conexões ao banco de dados de origem são impedidas.

Existem duas bandeiras úteis em `pg_database` para cada banco de dados: as colunas `datistemplate` e `datallowconn`. `datistemplate` pode ser definido para indicar que um banco de dados é destinado como um modelo para `CREATE DATABASE`. Se esta bandeira for definida, o banco de dados pode ser clonado por qualquer usuário com privilégios de `CREATEDB`; se não for definida, apenas os superusuários e o proprietário do banco de dados podem cloná-lo. Se `datallowconn` for falso, então nenhuma nova conexão com esse banco de dados será permitida (mas as sessões existentes não serão terminadas simplesmente ao definir a bandeira como falsa). O banco de dados `template0` é normalmente marcado `datallowconn = false` para evitar sua modificação. Tanto `template0` quanto `template1` devem ser sempre marcados com `datistemplate = true`.

Nota

`template1` e `template0` não têm nenhum status especial além do fato de que o nome `template1` é o nome padrão do banco de dados de origem para `CREATE DATABASE`. Por exemplo, é possível excluir `template1` e recriá-lo a partir de `template0` sem quaisquer efeitos negativos. Este curso de ação pode ser aconselhável se alguém tiver adicionado descuidadamente um monte de lixo em `template1`. (Para excluir `template1`, ele deve ter `pg_database.datistemplate = false`.)

O banco de dados `postgres` também é criado quando um grupo de bancos de dados é inicializado. Este banco de dados é destinado como um banco de dados padrão para que os usuários e aplicativos se conectem. É simplesmente uma cópia do `template1` e pode ser descartado e recriado, se necessário.