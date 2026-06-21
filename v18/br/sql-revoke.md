## REVOGAÇÃO

REVOGAR — remover privilégios de acesso

## Sinopse

```
REVOKE [ GRANT OPTION FOR ]
    { { SELECT | INSERT | UPDATE | DELETE | TRUNCATE | REFERENCES | TRIGGER | MAINTAIN }
    [, ...] | ALL [ PRIVILEGES ] }
    ON { [ TABLE ] table_name [, ...]
         | ALL TABLES IN SCHEMA schema_name [, ...] }
    FROM role_specification [, ...]
    [ GRANTED BY role_specification ]
    [ CASCADE | RESTRICT ]

REVOKE [ GRANT OPTION FOR ]
    { { SELECT | INSERT | UPDATE | REFERENCES } ( column_name [, ...] )
    [, ...] | ALL [ PRIVILEGES ] ( column_name [, ...] ) }
    ON [ TABLE ] table_name [, ...]
    FROM role_specification [, ...]
    [ GRANTED BY role_specification ]
    [ CASCADE | RESTRICT ]

REVOKE [ GRANT OPTION FOR ]
    { { USAGE | SELECT | UPDATE }
    [, ...] | ALL [ PRIVILEGES ] }
    ON { SEQUENCE sequence_name [, ...]
         | ALL SEQUENCES IN SCHEMA schema_name [, ...] }
    FROM role_specification [, ...]
    [ GRANTED BY role_specification ]
    [ CASCADE | RESTRICT ]

REVOKE [ GRANT OPTION FOR ]
    { { CREATE | CONNECT | TEMPORARY | TEMP } [, ...] | ALL [ PRIVILEGES ] }
    ON DATABASE database_name [, ...]
    FROM role_specification [, ...]
    [ GRANTED BY role_specification ]
    [ CASCADE | RESTRICT ]

REVOKE [ GRANT OPTION FOR ]
    { USAGE | ALL [ PRIVILEGES ] }
    ON DOMAIN domain_name [, ...]
    FROM role_specification [, ...]
    [ GRANTED BY role_specification ]
    [ CASCADE | RESTRICT ]

REVOKE [ GRANT OPTION FOR ]
    { USAGE | ALL [ PRIVILEGES ] }
    ON FOREIGN DATA WRAPPER fdw_name [, ...]
    FROM role_specification [, ...]
    [ GRANTED BY role_specification ]
    [ CASCADE | RESTRICT ]

REVOKE [ GRANT OPTION FOR ]
    { USAGE | ALL [ PRIVILEGES ] }
    ON FOREIGN SERVER server_name [, ...]
    FROM role_specification [, ...]
    [ GRANTED BY role_specification ]
    [ CASCADE | RESTRICT ]

REVOKE [ GRANT OPTION FOR ]
    { EXECUTE | ALL [ PRIVILEGES ] }
    ON { { FUNCTION | PROCEDURE | ROUTINE } function_name [ ( [ [ argmode ] [ arg_name ] arg_type [, ...] ] ) ] [, ...]
         | ALL { FUNCTIONS | PROCEDURES | ROUTINES } IN SCHEMA schema_name [, ...] }
    FROM role_specification [, ...]
    [ GRANTED BY role_specification ]
    [ CASCADE | RESTRICT ]

REVOKE [ GRANT OPTION FOR ]
    { USAGE | ALL [ PRIVILEGES ] }
    ON LANGUAGE lang_name [, ...]
    FROM role_specification [, ...]
    [ GRANTED BY role_specification ]
    [ CASCADE | RESTRICT ]

REVOKE [ GRANT OPTION FOR ]
    { { SELECT | UPDATE } [, ...] | ALL [ PRIVILEGES ] }
    ON LARGE OBJECT loid [, ...]
    FROM role_specification [, ...]
    [ GRANTED BY role_specification ]
    [ CASCADE | RESTRICT ]

REVOKE [ GRANT OPTION FOR ]
    { { SET | ALTER SYSTEM } [, ...] | ALL [ PRIVILEGES ] }
    ON PARAMETER configuration_parameter [, ...]
    FROM role_specification [, ...]
    [ GRANTED BY role_specification ]
    [ CASCADE | RESTRICT ]

REVOKE [ GRANT OPTION FOR ]
    { { CREATE | USAGE } [, ...] | ALL [ PRIVILEGES ] }
    ON SCHEMA schema_name [, ...]
    FROM role_specification [, ...]
    [ GRANTED BY role_specification ]
    [ CASCADE | RESTRICT ]

REVOKE [ GRANT OPTION FOR ]
    { CREATE | ALL [ PRIVILEGES ] }
    ON TABLESPACE tablespace_name [, ...]
    FROM role_specification [, ...]
    [ GRANTED BY role_specification ]
    [ CASCADE | RESTRICT ]

REVOKE [ GRANT OPTION FOR ]
    { USAGE | ALL [ PRIVILEGES ] }
    ON TYPE type_name [, ...]
    FROM role_specification [, ...]
    [ GRANTED BY role_specification ]
    [ CASCADE | RESTRICT ]

REVOKE [ { ADMIN | INHERIT | SET } OPTION FOR ]
    role_name [, ...] FROM role_specification [, ...]
    [ GRANTED BY role_specification ]
    [ CASCADE | RESTRICT ]

where role_specification can be:

    [ GROUP ] role_name
  | PUBLIC
  | CURRENT_ROLE
  | CURRENT_USER
  | SESSION_USER
```

## Descrição

O comando `REVOKE` revoga privilégios previamente concedidos a um ou mais papéis. A palavra-chave `PUBLIC` se refere ao grupo implicitamente definido de todos os papéis.

Veja a descrição do comando `GRANT` (sql-grant.md "GRANT") para o significado dos tipos de privilégio.

Observe que qualquer papel específico terá a soma dos privilégios concedidos diretamente a ele, privilégios concedidos a qualquer papel do qual ele atualmente seja membro e privilégios concedidos a `PUBLIC`. Assim, por exemplo, revogar o privilégio `SELECT` de `PUBLIC` não significa necessariamente que todos os papéis tenham perdido o privilégio `SELECT` no objeto: aqueles que o receberam diretamente ou por meio de outro papel ainda o terão. Da mesma forma, revogar `SELECT` de um usuário pode não impedir que esse usuário use `SELECT` se `PUBLIC` ou outro papel de membro ainda tenha direitos `SELECT`.

Se `GRANT OPTION FOR` for especificado, apenas a opção de concessão para o privilégio é revogada, não o privilégio em si. Caso contrário, tanto o privilégio quanto a opção de concessão são revogados.

Se um usuário tiver um privilégio com opção de concessão e o tiver concedido a outros usuários, os privilégios mantidos por esses outros usuários são chamados de privilégios dependentes. Se o privilégio ou a opção de concessão mantida pelo primeiro usuário estiver sendo revogada e houver privilégios dependentes, esses privilégios também serão revogados se `CASCADE` for especificado; se não for, a ação de revogação falhará. Essa revogação recursiva afeta apenas os privilégios que foram concedidos através de uma cadeia de usuários que pode ser rastreada até o usuário que é o objeto deste comando `REVOKE`. Assim, os usuários afetados podem efetivamente manter o privilégio se ele também tiver sido concedido por outros usuários.

Ao revogar privilégios em uma tabela, os privilégios correspondentes da coluna (se houver) são automaticamente revogados em cada coluna da tabela. Por outro lado, se um papel tiver concedido privilégios em uma tabela, a revogação dos mesmos privilégios de colunas individuais não terá efeito.

Ao revogar a filiação a um papel, `GRANT OPTION` é chamado, em vez disso, `ADMIN OPTION`, mas o comportamento é semelhante. Observe que, em versões anteriores ao PostgreSQL 16, os privilégios dependentes não eram rastreados para concessão de filiação a um papel, e, portanto, `CASCADE` não teve efeito para a filiação a um papel. Esse não é mais o caso. Observe também que essa forma do comando não permite a palavra ruidosa `GROUP` em *`role_specification`*.

Assim como o `ADMIN OPTION` pode ser removido de uma concessão de papel existente, também é possível revogar o `INHERIT OPTION` ou o `SET OPTION`. Isso é equivalente a definir o valor da opção correspondente para `FALSE`.

## Notas

Um usuário só pode revogar privilégios que foram concedidos diretamente por esse usuário. Por exemplo, se o usuário A concedeu um privilégio com opção de concessão ao usuário B, e o usuário B, por sua vez, o concedeu ao usuário C, então o usuário A não pode revogar o privilégio diretamente de C. Em vez disso, o usuário A pode revogar a opção de concessão ao usuário B e usar a opção `CASCADE` para que o privilégio, por sua vez, seja revogado do usuário C. Para outro exemplo, se tanto A quanto B concederam o mesmo privilégio ao C, A pode revogar sua própria concessão, mas não a concessão de B, então C ainda terá efetivamente o privilégio.

Quando um não proprietário de um objeto tenta `REVOKE` privilégios no objeto, o comando falhará completamente se o usuário não tiver quaisquer privilégios no objeto. Enquanto algum privilégio estiver disponível, o comando prosseguirá, mas ele revogará apenas os privilégios para os quais o usuário tenha opções de concessão. Os formulários `REVOKE ALL PRIVILEGES` emitirão uma mensagem de aviso se não houver opções de concessão, enquanto os outros formulários emitirão uma mensagem de aviso se as opções de concessão para qualquer um dos privilégios especificamente nomeados no comando não forem mantidas. (Em princípio, essas declarações se aplicam também ao proprietário do objeto, mas como o proprietário é sempre tratado como tendo todas as opções de concessão, os casos nunca podem ocorrer.)

Se um superusuário optar por emitir um comando `GRANT` ou `REVOKE`, o comando é executado como se fosse emitido pelo proprietário do objeto afetado. (Como as funções não têm proprietários, no caso de uma `GRANT` de adesão a funções, o comando é executado como se fosse emitido pelo superusuário de bootstrap.) Como todos os privilégios vêm, em última análise, do proprietário do objeto (possivelmente indiretamente por meio de cadeias de opções de concessão), é possível que um superusuário revogue todos os privilégios, mas isso pode exigir o uso de `CASCADE` conforme mencionado acima.

`REVOKE` também pode ser realizado por um papel que não é o proprietário do objeto afetado, mas que é membro do papel que possui o objeto, ou que é membro de um papel que possui privilégios `WITH GRANT OPTION` sobre o objeto. Neste caso, o comando é realizado como se fosse emitido pelo papel que contém o objeto e que realmente possui os privilégios `WITH GRANT OPTION`. Por exemplo, se a tabela `t1` é propriedade do papel `g1`, do qual o papel `u1` é membro, então `u1` pode revogar privilégios em `t1` que estão registrados como concedidos por `g1`. Isso inclui concessões feitas por `u1` e também por outros membros do papel `g1`.

Se o papel que executa `REVOKE` tiver privilégios indiretamente por meio de mais de um caminho de associação de papel, não é especificado qual papel contendo será usado para executar o comando. Nesses casos, é melhor prática usar `SET ROLE` para se tornar o papel específico que você deseja realizar o `REVOKE`. Não fazer isso pode levar à revogação de privilégios que não são os que você pretendia, ou à não revogação de nada.

Consulte a [Seção 5.8][(ddl-priv.md "5.8. Privileges")] para obter mais informações sobre os tipos específicos de privilégio, bem como sobre como inspecionar os privilégios dos objetos.

## Exemplos

Reveja o privilégio de inserção para o público na tabela `films`:

```
REVOKE INSERT ON films FROM PUBLIC;
```

Reveja todos os privilégios do usuário `manuel` na visualização `kinds`:

```
REVOKE ALL PRIVILEGES ON kinds FROM manuel;
```

Observe que isso realmente significa “retirar todos os privilégios que eu concedi”.

Reveja a filiação no papel `admins` do usuário `joe`:

```
REVOKE admins FROM joe;
```

## Compatibilidade

As notas de compatibilidade do comando `GRANT`(sql-grant.md "GRANT") se aplicam de forma análoga ao `REVOKE`. A palavra-chave `RESTRICT` ou `CASCADE` é necessária de acordo com o padrão, mas o PostgreSQL assume `RESTRICT` por padrão.

## Veja também

[DIVERSIFICAÇÃO DE PRIVILEGIOS](sql-grant.md "GRANT"), [ALTERAR PRIVILEGIOS PREDEFINS](sql-alterdefaultprivileges.md "ALTER DEFAULT PRIVILEGES")