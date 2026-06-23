## GRANTE

GRANT — definir privilégios de acesso

## Sinopse

```
GRANT { { SELECT | INSERT | UPDATE | DELETE | TRUNCATE | REFERENCES | TRIGGER | MAINTAIN }
    [, ...] | ALL [ PRIVILEGES ] }
    ON { [ TABLE ] table_name [, ...]
         | ALL TABLES IN SCHEMA schema_name [, ...] }
    TO role_specification [, ...] [ WITH GRANT OPTION ]
    [ GRANTED BY role_specification ]

GRANT { { SELECT | INSERT | UPDATE | REFERENCES } ( column_name [, ...] )
    [, ...] | ALL [ PRIVILEGES ] ( column_name [, ...] ) }
    ON [ TABLE ] table_name [, ...]
    TO role_specification [, ...] [ WITH GRANT OPTION ]
    [ GRANTED BY role_specification ]

GRANT { { USAGE | SELECT | UPDATE }
    [, ...] | ALL [ PRIVILEGES ] }
    ON { SEQUENCE sequence_name [, ...]
         | ALL SEQUENCES IN SCHEMA schema_name [, ...] }
    TO role_specification [, ...] [ WITH GRANT OPTION ]
    [ GRANTED BY role_specification ]

GRANT { { CREATE | CONNECT | TEMPORARY | TEMP } [, ...] | ALL [ PRIVILEGES ] }
    ON DATABASE database_name [, ...]
    TO role_specification [, ...] [ WITH GRANT OPTION ]
    [ GRANTED BY role_specification ]

GRANT { USAGE | ALL [ PRIVILEGES ] }
    ON DOMAIN domain_name [, ...]
    TO role_specification [, ...] [ WITH GRANT OPTION ]
    [ GRANTED BY role_specification ]

GRANT { USAGE | ALL [ PRIVILEGES ] }
    ON FOREIGN DATA WRAPPER fdw_name [, ...]
    TO role_specification [, ...] [ WITH GRANT OPTION ]
    [ GRANTED BY role_specification ]

GRANT { USAGE | ALL [ PRIVILEGES ] }
    ON FOREIGN SERVER server_name [, ...]
    TO role_specification [, ...] [ WITH GRANT OPTION ]
    [ GRANTED BY role_specification ]

GRANT { EXECUTE | ALL [ PRIVILEGES ] }
    ON { { FUNCTION | PROCEDURE | ROUTINE } routine_name [ ( [ [ argmode ] [ arg_name ] arg_type [, ...] ] ) ] [, ...]
         | ALL { FUNCTIONS | PROCEDURES | ROUTINES } IN SCHEMA schema_name [, ...] }
    TO role_specification [, ...] [ WITH GRANT OPTION ]
    [ GRANTED BY role_specification ]

GRANT { USAGE | ALL [ PRIVILEGES ] }
    ON LANGUAGE lang_name [, ...]
    TO role_specification [, ...] [ WITH GRANT OPTION ]
    [ GRANTED BY role_specification ]

GRANT { { SELECT | UPDATE } [, ...] | ALL [ PRIVILEGES ] }
    ON LARGE OBJECT loid [, ...]
    TO role_specification [, ...] [ WITH GRANT OPTION ]
    [ GRANTED BY role_specification ]

GRANT { { SET | ALTER SYSTEM } [, ... ] | ALL [ PRIVILEGES ] }
    ON PARAMETER configuration_parameter [, ...]
    TO role_specification [, ...] [ WITH GRANT OPTION ]
    [ GRANTED BY role_specification ]

GRANT { { CREATE | USAGE } [, ...] | ALL [ PRIVILEGES ] }
    ON SCHEMA schema_name [, ...]
    TO role_specification [, ...] [ WITH GRANT OPTION ]
    [ GRANTED BY role_specification ]

GRANT { CREATE | ALL [ PRIVILEGES ] }
    ON TABLESPACE tablespace_name [, ...]
    TO role_specification [, ...] [ WITH GRANT OPTION ]
    [ GRANTED BY role_specification ]

GRANT { USAGE | ALL [ PRIVILEGES ] }
    ON TYPE type_name [, ...]
    TO role_specification [, ...] [ WITH GRANT OPTION ]
    [ GRANTED BY role_specification ]

GRANT role_name [, ...] TO role_specification [, ...]
    [ WITH { ADMIN | INHERIT | SET } { OPTION | TRUE | FALSE } ]
    [ GRANTED BY role_specification ]

where role_specification can be:

    [ GROUP ] role_name
  | PUBLIC
  | CURRENT_ROLE
  | CURRENT_USER
  | SESSION_USER
```

## Descrição

O comando `GRANT` tem duas variantes básicas: uma que concede privilégios em um objeto de banco de dados (tabela, coluna, visão, tabela estrangeira, sequência, banco de dados, invólucro de dados estrangeiro, servidor estrangeiro, função, procedimento, linguagem procedural, grande objeto, parâmetro de configuração, esquema, tablespace ou tipo), e uma que concede a filiação em um papel. Essas variantes são semelhantes em muitos aspectos, mas são diferentes o suficiente para serem descritas separadamente.

### CONCEDA em Objetos de Banco de Dados

Esta variante do comando `GRANT` concede privilégios específicos a um objeto de banco de dados a um ou mais papéis. Esses privilégios são adicionados aos já concedidos, se houver.

A palavra-chave `PUBLIC` indica que os privilégios devem ser concedidos a todos os papéis, incluindo aqueles que podem ser criados posteriormente. `PUBLIC` pode ser considerado um grupo implicitamente definido que sempre inclui todos os papéis. Qualquer papel específico terá a soma de privilégios concedidos diretamente a ele, privilégios concedidos a qualquer papel do qual ele atualmente é membro e privilégios concedidos a `PUBLIC`.

Se `WITH GRANT OPTION` for especificado, o destinatário do privilégio pode, por sua vez, concedê-lo a outros. Sem uma opção de concessão, o destinatário não pode fazer isso. Opções de concessão não podem ser concedidas a `PUBLIC`.

Se `GRANTED BY` for especificado, o concedente especificado deve ser o usuário atual. Esta cláusula está presente atualmente apenas nesta forma para compatibilidade com SQL.

Não é necessário conceder privilégios ao proprietário de um objeto (geralmente o usuário que o criou), pois o proprietário possui todos os privilégios por padrão. (O proprietário, no entanto, pode optar por revogar alguns de seus próprios privilégios por segurança.)

O direito de descartar um objeto ou alterar sua definição de qualquer maneira não é tratado como um privilégio concedível; é inerente ao proprietário e não pode ser concedido ou revogado. (No entanto, um efeito semelhante pode ser obtido concedendo ou revogando a associação ao papel que possui o objeto; veja abaixo.) O proprietário implicitamente tem todas as opções de concessão para o objeto também.

Os possíveis privilégios são:

`SELECT` `INSERT` `UPDATE` `DELETE` `TRUNCATE` `REFERENCES` `TRIGGER` `CREATE` `CONNECT` `TEMPORARY` `EXECUTE` `USAGE` `SET` `ALTER SYSTEM` `MAINTAIN`: Tipos específicos de privilégios, conforme definido na [Seção 5.8](ddl-priv.md "5.8. Privileges").

`TEMP`: Esboço alternativo para `TEMPORARY`.

`ALL PRIVILEGES`: Conceda todos os privilégios disponíveis para o tipo do objeto. A palavra-chave `PRIVILEGES` é opcional no PostgreSQL, embora seja exigida pelo SQL rigoroso.

A sintaxe `FUNCTION` funciona para funções simples, funções agregadas e funções de janela, mas não para procedimentos; use `PROCEDURE` para esses casos. Alternativamente, use `ROUTINE` para se referir a uma função, função agregada, função de janela ou procedimento, independentemente do seu tipo preciso.

Há também uma opção para conceder privilégios em todos os objetos do mesmo tipo dentro de um ou mais esquemas. Essa funcionalidade atualmente é suportada apenas para tabelas, sequências, funções e procedimentos. `ALL TABLES` também afeta vistas e tabelas externas, assim como o comando específico de objeto `GRANT`. `ALL FUNCTIONS` também afeta funções agregadas e de janela, mas não procedimentos, novamente assim como o comando específico de objeto `GRANT`. Use `ALL ROUTINES` para incluir procedimentos.

### CONCESÃO em Funções

Esta variante do comando `GRANT` concede a filiação a um ou mais outros papéis, e a modificação das opções de filiação `SET`, `INHERIT` e `ADMIN`; consulte [Seção 21.3](role-membership.md "21.3. Role Membership") para detalhes. A filiação a um papel é significativa porque, potencialmente, permite o acesso aos privilégios concedidos a um papel a cada um de seus membros, e potencialmente também a capacidade de fazer alterações no próprio papel. No entanto, as permissões reais conferidas dependem das opções associadas à concessão. Para modificar essas opções de uma filiação existente, basta especificar a filiação com valores de opção atualizados.

Cada uma das opções descritas abaixo pode ser definida como `TRUE` ou `FALSE`. A palavra-chave `OPTION` é aceita como sinônimo de `TRUE`, de modo que `WITH ADMIN OPTION` é sinônimo de `WITH ADMIN TRUE`. Ao alterar uma associação existente, a omissão de uma opção resulta na retenção do valor atual.

A opção `ADMIN` permite que o membro, por sua vez, conceda a filiação no papel a outros e também revogue a filiação no papel. Sem a opção de administrador, os usuários comuns não podem fazer isso. Um papel não é considerado para ter `WITH ADMIN OPTION` em si. Superusuários do banco de dados podem conceder ou revogar a filiação em qualquer papel para qualquer pessoa. Esta opção tem como padrão `FALSE`.

A opção `INHERIT` controla o status de herança da nova adesão; consulte [Seção 21.3](role-membership.md) para detalhes sobre herança. Se estiver definida como `TRUE`, isso faz com que o novo membro herde do papel concedido. Se definida como `FALSE`, o novo membro não herda. Se não especificado ao criar uma nova adesão de papel, isso é padrão para o atributo de herança do novo membro.

A opção `SET`, se configurada como `TRUE`, permite que o membro mude para o papel concedido usando o comando (sql-set-role.md "SET ROLE"). Se um papel for um membro indireto de outro papel, ele pode usar `SET ROLE` para mudar para esse papel apenas se houver uma cadeia de concessões, cada uma das quais tem `SET TRUE`. Esta opção tem como padrão `TRUE`.

Para criar um objeto pertencente a outro papel ou conceder a propriedade de um objeto existente a outro papel, você deve ter a capacidade de `SET ROLE` para esse papel; caso contrário, comandos como `ALTER ... OWNER TO` ou `CREATE DATABASE ... OWNER` falharão. No entanto, um usuário que herda os privilégios de um papel, mas não tem a capacidade de `SET ROLE` para esse papel, pode ser capaz de obter acesso total ao papel manipulando objetos existentes pertencentes a esse papel (por exemplo, eles poderiam redefinir uma função existente para agir como um cavalo de Troia). Portanto, se os privilégios de um papel devem ser herdados, mas não devem ser acessíveis via `SET ROLE`, ele não deve possuir nenhum objeto SQL.

Se `GRANTED BY` for especificado, a concessão é registrada como tendo sido feita pelo papel especificado. Um usuário só pode atribuir uma concessão a outro papel se possuir os privilégios desse papel. O papel registrado como concedente deve ter `ADMIN OPTION` no papel alvo, a menos que seja o superusuário de bootstrap. Quando uma concessão é registrada como tendo um concedente diferente do superusuário de bootstrap, depende do concedente continuar possuindo `ADMIN OPTION` no papel; portanto, se `ADMIN OPTION` for revogada, as concessões dependentes também devem ser revogadas.

Ao contrário do que ocorre com os privilégios, a adesão a um papel não pode ser concedida a `PUBLIC`. Observe também que essa forma do comando não permite a palavra de ruído `GROUP` em *`role_specification`*.

## Notas

O comando `REVOKE`(sql-revoke.md "REVOKE") é usado para revogar privilégios de acesso.

Desde o PostgreSQL 8.1, os conceitos de usuários e grupos foram unificados em um único tipo de entidade chamada papel. Portanto, não é mais necessário usar a palavra-chave `GROUP` para identificar se um beneficiário é um usuário ou um grupo. `GROUP` ainda é permitido no comando, mas é uma palavra de ruído.

Um usuário pode realizar `SELECT`, `INSERT`, etc., em uma coluna se ele tiver esse privilégio para a coluna específica ou para toda a tabela. Conceder o privilégio no nível da tabela e, em seguida, revogá-lo para uma coluna não fará o que se poderia desejar: a concessão no nível da tabela não é afetada por uma operação no nível da coluna.

Quando um não proprietário de um objeto tenta `GRANT` privilégios no objeto, o comando falhará completamente se o usuário não tiver quaisquer privilégios no objeto. Enquanto algum privilégio estiver disponível, o comando prosseguirá, mas concederá apenas os privilégios para os quais o usuário tenha opções de concessão. Os formulários `GRANT ALL PRIVILEGES` emitirão uma mensagem de aviso se não houver opções de concessão, enquanto os outros formulários emitirão uma mensagem de aviso se as opções de concessão para qualquer um dos privilégios especificamente nomeados no comando não forem mantidas. (Em princípio, essas declarações se aplicam também ao proprietário do objeto, mas como o proprietário é sempre tratado como tendo todas as opções de concessão, os casos nunca podem ocorrer.)

Deve-se notar que os superusuários de banco de dados podem acessar todos os objetos, independentemente das configurações de privilégio do objeto. Isso é comparável aos direitos do `root` em um sistema Unix. Assim como no caso do `root`, não é prudente operar como um superusuário, exceto quando absolutamente necessário.

Se um superusuário optar por emitir um comando `GRANT` ou `REVOKE`, o comando é executado como se tivesse sido emitido pelo proprietário do objeto afetado. Em particular, os privilégios concedidos por meio de tal comando parecerão ter sido concedidos pelo proprietário do objeto. (Para a associação de papéis, a associação parece ter sido concedida pelo superusuário de bootstrap.)

`GRANT` e `REVOKE` também podem ser concedidos por um papel que não é o proprietário do objeto afetado, mas que é membro do papel que possui o objeto, ou que é membro de um papel que possui privilégios `WITH GRANT OPTION` sobre o objeto. Neste caso, os privilégios serão registrados como tendo sido concedidos pelo papel que realmente possui o objeto ou que possui os privilégios `WITH GRANT OPTION`. Por exemplo, se a tabela `t1` é de propriedade do papel `g1`, do qual o papel `u1` é membro, então `u1` pode conceder privilégios em `t1` para `u2`, mas esses privilégios aparecerão como tendo sido concedidos diretamente por `g1`. Qualquer outro membro do papel `g1` poderia revô-los mais tarde.

Se o papel que executa `GRANT` possuir os privilégios necessários indiretamente por meio de mais de um caminho de associação de papel, não é especificado qual papel contendo será registrado como tendo feito a concessão. Nesses casos, é uma prática recomendada usar `SET ROLE` para se tornar o papel específico que você deseja realizar o `GRANT`.

A concessão de permissão em uma tabela não estende automaticamente as permissões para quaisquer sequências utilizadas pela tabela, incluindo sequências vinculadas às colunas `SERIAL`. As permissões em sequências devem ser definidas separadamente.

Consulte a [Seção 5.8](ddl-priv.md) para obter mais informações sobre os tipos específicos de privilégio, bem como sobre como inspecionar os privilégios dos objetos.

## Exemplos

Concede privilégios de inserção a todos os usuários na tabela `films`:

```
GRANT INSERT ON films TO PUBLIC;
```

Concede todos os privilégios disponíveis ao usuário `manuel` para visualizar `kinds`:

```
GRANT ALL PRIVILEGES ON kinds TO manuel;
```

Observe que, embora o acima conceda de fato todos os privilégios se executado por um superusuário ou pelo proprietário de `kinds`, quando executado por outra pessoa, ele apenas concederá os permissões para as quais a outra pessoa tenha opções de concessão.

Concede a filiação no papel `admins` ao usuário `joe`:

```
GRANT admins TO joe;
```

## Compatibilidade

De acordo com o padrão SQL, a palavra-chave `PRIVILEGES` no `ALL PRIVILEGES` é necessária. O padrão SQL não suporta a definição de privilégios em mais de um objeto por comando.

O PostgreSQL permite que o proprietário de um objeto revogue seus próprios privilégios comuns: por exemplo, um proprietário de uma tabela pode tornar a tabela somente de leitura para si mesmo, revogando seus próprios privilégios `INSERT`, `UPDATE`, `DELETE` e `TRUNCATE`. Isso não é possível de acordo com o padrão SQL. O motivo é que o PostgreSQL trata os privilégios do proprietário como se eles tivessem sido concedidos pelo proprietário para si mesmo; portanto, eles também podem revogá-los. No padrão SQL, os privilégios do proprietário são concedidos por uma entidade assumida “_SYSTEM”. Não sendo “_SYSTEM”, o proprietário não pode revogar esses direitos.

De acordo com o padrão SQL, as opções de concessão podem ser concedidas a `PUBLIC`; o PostgreSQL só suporta a concessão de opções de concessão a papéis.

O padrão SQL permite que a opção `GRANTED BY` especifique apenas `CURRENT_USER` ou `CURRENT_ROLE`. As outras variantes são extensões do PostgreSQL.

O padrão SQL prevê um privilégio `USAGE` em outros tipos de objetos: conjuntos de caracteres, codificações, traduções.

No padrão SQL, as sequências têm apenas o privilégio `USAGE`, que controla o uso da expressão `NEXT VALUE FOR`, que é equivalente à função `nextval` no PostgreSQL. Os privilégios de sequência `SELECT` e `UPDATE` são extensões do PostgreSQL. A aplicação do privilégio de sequência `USAGE` à função `currval` também é uma extensão do PostgreSQL (assim como a própria função).

Os privilégios em bancos de dados, espaços de tabelas, esquemas, idiomas e parâmetros de configuração são extensões do PostgreSQL.

## Veja também

[REVOGA](sql-revoke.md "REVOKE"), [ALTERA PRIVILEGIOS O PREDEFECTO](sql-alterdefaultprivileges.md "ALTER DEFAULT PRIVILEGES")