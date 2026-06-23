## ALTER SERVER

ALTERAR SERVIDOR — alterar a definição de um servidor estrangeiro

## Sinopse

```
ALTER SERVER name [ VERSION 'new_version' ]
    [ OPTIONS ( [ ADD | SET | DROP ] option ['value'] [, ... ] ) ]
ALTER SERVER name OWNER TO { new_owner | CURRENT_ROLE | CURRENT_USER | SESSION_USER }
ALTER SERVER name RENAME TO new_name
```

## Descrição

`ALTER SERVER` altera a definição de um servidor estrangeiro. O primeiro formulário altera a string da versão do servidor ou as opções genéricas do servidor (pelo menos uma cláusula é necessária). O segundo formulário altera o proprietário do servidor.

Para alterar o servidor, você deve ser o proprietário do servidor. Além disso, para alterar o proprietário, você deve ser capaz de `SET ROLE` para o novo papel de proprietário e deve ter `USAGE` privilégio no wrapper de dados externos do servidor. (Observe que os superusuários satisfazem automaticamente todos esses critérios.)

## Parâmetros

*`name`*: O nome de um servidor existente.

*`new_version`*: Nova versão do servidor.

`OPTIONS ( [ ADD | SET | DROP ] option ['value'] [, ... ] )`: Opções de alteração para o servidor. `ADD`, `SET` e `DROP` especificam a ação a ser realizada. `ADD` é assumido se nenhuma operação for especificada explicitamente. Os nomes das opções devem ser exclusivos; os nomes e valores também são validados usando a biblioteca de wrapper de dados externos do servidor.

*`new_owner`*: O nome do usuário do novo proprietário do servidor estrangeiro.

*`new_name`*: O novo nome do servidor externo.

## Exemplos

Alterar servidor `foo`, adicionar opções de conexão:

```
ALTER SERVER foo OPTIONS (host 'foo', dbname 'foodb');
```

Alterar o servidor `foo`, alterar a versão, alterar a opção `host`:

```
ALTER SERVER foo VERSION '8.4' OPTIONS (SET host 'baz');
```

## Compatibilidade

O `ALTER SERVER` está de acordo com a ISO/IEC 9075-9 (SQL/MED). Os formulários `OWNER TO` e `RENAME` são extensões do PostgreSQL.

## Veja também

[Crie servidor](sql-createserver.md "CREATE SERVER"), [Retire servidor](sql-dropserver.md "DROP SERVER")