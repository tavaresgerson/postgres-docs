## CRIAR MAPeamento de USUÁRIOS

Crie mapeamento de usuário — defina um novo mapeamento de um usuário para um servidor externo

## Sinopse

```
CREATE USER MAPPING [ IF NOT EXISTS ] FOR { user_name | USER | CURRENT_ROLE | CURRENT_USER | PUBLIC }
    SERVER server_name
    [ OPTIONS ( option 'value' [ , ... ] ) ]
```

## Descrição

`CREATE USER MAPPING` define um mapeamento de um usuário para um servidor externo. Um mapeamento de usuário geralmente encapsula informações de conexão que um wrapper de dados externo usa juntamente com as informações encapsuladas por um servidor externo para acessar um recurso de dados externo.

O proprietário de um servidor estrangeiro pode criar mapeamentos de usuário para esse servidor para qualquer usuário. Além disso, um usuário pode criar um mapeamento de usuário para seu próprio nome de usuário se o privilégio `USAGE` no servidor tiver sido concedido ao usuário.

## Parâmetros

`IF NOT EXISTS`: Não exija um erro se uma mapeo do usuário dado ao servidor estrangeiro dado já existir. Um aviso é emitido neste caso. Note que não há garantia de que a mapeo de usuário existente seja algo como a que teria sido criada.

*`user_name`*: O nome de um usuário existente que está mapeado para um servidor externo. `CURRENT_ROLE`, `CURRENT_USER` e `USER` correspondem ao nome do usuário atual. Quando `PUBLIC` é especificado, uma chamada de mapeamento público é criada e é usada quando nenhum mapeamento específico do usuário é aplicável.

*`server_name`*: O nome de um servidor existente para o qual a mapeo de usuários deve ser criado.

`OPTIONS ( option 'value' [, ... ] )`: Esta cláusula especifica as opções de mapeamento de usuário. As opções definem, normalmente, o nome e a senha do usuário real do mapeamento. Os nomes das opções devem ser exclusivos. Os nomes e valores das opções permitidos são específicos para o wrapper de dados externos do servidor.

## Exemplos

Crie um mapeamento de usuário para o usuário `bob`, servidor `foo`:

```
CREATE USER MAPPING FOR bob SERVER foo OPTIONS (user 'bob', password 'secret');
```

## Compatibilidade

`CREATE USER MAPPING` está em conformidade com a ISO/IEC 9075-9 (SQL/MED).

## Veja também

[ALTERAR MAPeamento de USUÁRIOS](sql-alterusermapping.md "ALTER USER MAPPING"), [DROP MAPeamento de USUÁRIOS](sql-dropusermapping.md "DROP USER MAPPING"), [C R E A C E R E D I A T A WRAPPER](sql-createforeigndatawrapper.md "CREATE FOREIGN DATA WRAPPER"), [C R E A C E R E D I A T A SERVIDOR](sql-createserver.md "CREATE SERVER")