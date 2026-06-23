## ALTERAR MAPeamento de USUÁRIO

ALTERAR MAPeamento de USUÁRIO — alterar a definição de um mapeamento de usuário

## Sinopse

```
ALTER USER MAPPING FOR { user_name | USER | CURRENT_ROLE | CURRENT_USER | SESSION_USER | PUBLIC }
    SERVER server_name
    OPTIONS ( [ ADD | SET | DROP ] option ['value'] [, ... ] )
```

## Descrição

`ALTER USER MAPPING` altera a definição de mapeamento de usuário.

O proprietário de um servidor estrangeiro pode alterar mapeamentos de usuário para esse servidor para qualquer usuário. Além disso, um usuário pode alterar um mapeamento de usuário para seu próprio nome de usuário se o privilégio `USAGE` no servidor tiver sido concedido ao usuário.

## Parâmetros

*`user_name`*: Nome do usuário do mapeamento. `CURRENT_ROLE`, `CURRENT_USER` e `USER` correspondem ao nome do usuário atual. `PUBLIC` é usado para corresponder a todos os nomes de usuário presentes e futuros no sistema.

*`server_name`*: Nome do servidor de mapeamento de usuários.

`OPTIONS ( [ ADD | SET | DROP ] option ['value'] [, ... ] )`: Opções de alteração para o mapeamento do usuário. As novas opções substituem quaisquer opções especificadas anteriormente. `ADD`, `SET` e `DROP` especificam a ação a ser realizada. `ADD` é assumido se nenhuma operação for especificada explicitamente. Os nomes das opções devem ser exclusivos; as opções também são validadas pelo wrapper de dados externos do servidor.

## Exemplos

Altere a senha para mapeamento de usuário `bob`, servidor `foo`:

```
ALTER USER MAPPING FOR bob SERVER foo OPTIONS (SET password 'public');
```

## Compatibilidade

`ALTER USER MAPPING` está em conformidade com a ISO/IEC 9075-9 (SQL/MED). Há um problema de sintaxe sutil: o padrão omite a palavra-chave `FOR`. Como tanto `CREATE USER MAPPING` quanto `DROP USER MAPPING` usam `FOR` em posições análogas, e o IBM DB2 (sendo a outra implementação principal do SQL/MED) também a exige para `ALTER USER MAPPING`, o PostgreSQL diverge do padrão aqui, no interesse da consistência e da interoperabilidade.

## Veja também

[Criação de mapeamento de usuário](sql-createusermapping.md "CREATE USER MAPPING"), [Remoção de mapeamento de usuário](sql-dropusermapping.md "DROP USER MAPPING")