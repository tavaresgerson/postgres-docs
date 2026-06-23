## DROP USER MAPPING

DROP USER MAPPING — remova um mapeamento de usuário para um servidor externo

## Sinopse

```
DROP USER MAPPING [ IF EXISTS ] FOR { user_name | USER | CURRENT_ROLE | CURRENT_USER | PUBLIC } SERVER server_name
```

## Descrição

`DROP USER MAPPING` remove um mapeamento de usuário existente do servidor estrangeiro.

O proprietário de um servidor estrangeiro pode excluir mapeamentos de usuário para esse servidor para qualquer usuário. Além disso, um usuário pode excluir um mapeamento de usuário para o seu próprio nome de usuário se o privilégio `USAGE` no servidor tiver sido concedido ao usuário.

## Parâmetros

`IF EXISTS`: Não exija erro se o mapeamento do usuário não existir. Um aviso é emitido neste caso.

*`user_name`*: Nome do usuário do mapeamento. `CURRENT_ROLE`, `CURRENT_USER` e `USER` correspondem ao nome do usuário atual. `PUBLIC` é usado para corresponder a todos os nomes de usuário presentes e futuros no sistema.

*`server_name`*: Nome do servidor de mapeamento de usuários.

## Exemplos

Deixe um mapeamento de usuário `bob`, servidor `foo` se existir:

```
DROP USER MAPPING IF EXISTS FOR bob SERVER foo;
```

## Compatibilidade

`DROP USER MAPPING` está em conformidade com a ISO/IEC 9075-9 (SQL/MED). A cláusula `IF EXISTS` é uma extensão do PostgreSQL.

## Veja também

[Criação de mapeamento de usuário](sql-createusermapping.md "CREATE USER MAPPING"), [Alteração de mapeamento de usuário](sql-alterusermapping.md "ALTER USER MAPPING")