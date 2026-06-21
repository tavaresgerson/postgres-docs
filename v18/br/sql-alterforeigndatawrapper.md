## ALTER FOREIGN DATA WRAPPER

ALTERAR O WRAPPER DE DADOS ESTRANGEIRO — alterar a definição de um wrapper de dados estrangeiro

## Sinopse

```
ALTER FOREIGN DATA WRAPPER name
    [ HANDLER handler_function | NO HANDLER ]
    [ VALIDATOR validator_function | NO VALIDATOR ]
    [ OPTIONS ( [ ADD | SET | DROP ] option ['value'] [, ... ]) ]
ALTER FOREIGN DATA WRAPPER name OWNER TO { new_owner | CURRENT_ROLE | CURRENT_USER | SESSION_USER }
ALTER FOREIGN DATA WRAPPER name RENAME TO new_name
```

## Descrição

`ALTER FOREIGN DATA WRAPPER` altera a definição de um wrapper de dados estrangeiros. A primeira forma do comando altera as funções de suporte ou as opções genéricas do wrapper de dados estrangeiros (pelo menos uma cláusula é necessária). A segunda forma altera o proprietário do wrapper de dados estrangeiros.

Apenas superusuários podem alterar os wrappers de dados externos. Além disso, apenas superusuários podem possuir wrappers de dados externos.

## Parâmetros

*`name`*: O nome de um wrapper de dados estrangeiro existente.

`HANDLER handler_function`: Especifica uma nova função de manipulador para o wrapper de dados estrangeiros.

`NO HANDLER`: Isso é usado para especificar que o wrapper de dados estrangeiros não deve mais ter uma função de manipulador.

Observe que as tabelas estrangeiras que utilizam um wrapper de dados estrangeiro sem um manipulador não podem ser acessadas.

`VALIDATOR validator_function`: Especifica uma nova função de validação para o wrapper de dados estrangeiros.

Observe que é possível que opções pré-existentes do wrapper de dados externos, ou de servidores dependentes, mapeamentos de usuários ou tabelas externas, sejam inválidas de acordo com o novo validador. O PostgreSQL não verifica isso. Cabe ao usuário garantir que essas opções estejam corretas antes de usar o wrapper de dados externos modificado. No entanto, quaisquer opções especificadas neste comando `ALTER FOREIGN DATA WRAPPER` serão verificadas usando o novo validador.

`NO VALIDATOR`: Isso é usado para especificar que o wrapper de dados estrangeiros não deve mais ter uma função de validação.

`OPTIONS ( [ ADD | SET | DROP ] option ['value'] [, ... ] )`: Opções de alteração para o wrapper de dados estrangeiros. `ADD`, `SET` e `DROP` especificam a ação a ser realizada. `ADD` é assumido se nenhuma operação for especificada explicitamente. Os nomes das opções devem ser exclusivos; os nomes e valores também são validados usando a função de validação do wrapper de dados estrangeiros, se houver.

*`new_owner`*: O nome do usuário do novo proprietário do wrapper de dados estrangeiros.

*`new_name`*: O novo nome para o wrapper de dados estrangeiros.

## Exemplos

Altere o wrapper de dados estrangeiros `dbi`, adicione a opção `foo`, remova `bar`:

```
ALTER FOREIGN DATA WRAPPER dbi OPTIONS (ADD foo '1', DROP bar);
```

Altere o wrapper de dados estrangeiros `dbi` para `bob.myvalidator`:

```
ALTER FOREIGN DATA WRAPPER dbi VALIDATOR bob.myvalidator;
```

## Compatibilidade

`ALTER FOREIGN DATA WRAPPER` está em conformidade com a ISO/IEC 9075-9 (SQL/MED), exceto que as cláusulas `HANDLER`, `VALIDATOR`, `OWNER TO` e `RENAME` são extensões.

## Veja também

[Crie um Wrapper de Dados Estrangeiro](sql-createforeigndatawrapper.md "CREATE FOREIGN DATA WRAPPER"), [Retire o Wrapper de Dados Estrangeiro](sql-dropforeigndatawrapper.md "DROP FOREIGN DATA WRAPPER")