## ALTER TYPE

ALTER TYPE — alterar a definição de um tipo

## Sinopse

```
ALTER TYPE name OWNER TO { new_owner | CURRENT_ROLE | CURRENT_USER | SESSION_USER }
ALTER TYPE name RENAME TO new_name
ALTER TYPE name SET SCHEMA new_schema
ALTER TYPE name RENAME ATTRIBUTE attribute_name TO new_attribute_name [ CASCADE | RESTRICT ]
ALTER TYPE name action [, ... ]
ALTER TYPE name ADD VALUE [ IF NOT EXISTS ] new_enum_value [ { BEFORE | AFTER } neighbor_enum_value ]
ALTER TYPE name RENAME VALUE existing_enum_value TO new_enum_value
ALTER TYPE name SET ( property = value [, ... ] )

where action is one of:

    ADD ATTRIBUTE attribute_name data_type [ COLLATE collation ] [ CASCADE | RESTRICT ]
    DROP ATTRIBUTE [ IF EXISTS ] attribute_name [ CASCADE | RESTRICT ]
    ALTER ATTRIBUTE attribute_name [ SET DATA ] TYPE data_type [ COLLATE collation ] [ CASCADE | RESTRICT ]
```

## Descrição

`ALTER TYPE` altera a definição de um tipo existente. Existem vários subformularios:

`OWNER`: Este formulário altera o proprietário do tipo.

`RENAME`: Este formulário altera o nome do tipo.

`SET SCHEMA`: Este formulário move o tipo para outro esquema.

`RENAME ATTRIBUTE`: Este formulário só pode ser usado com tipos compostos. Ele altera o nome de um atributo individual do tipo.

`ADD ATTRIBUTE`: Este formulário adiciona um novo atributo a um tipo composto, usando a mesma sintaxe que [`CREATE TYPE`](sql-createtype.md "CREATE TYPE").

`DROP ATTRIBUTE [ IF EXISTS ]`: Este formulário exclui um atributo de um tipo composto. Se `IF EXISTS` for especificado e o atributo não existir, não será lançada nenhuma exceção. Nesse caso, é emitido um aviso em vez disso.

`ALTER ATTRIBUTE ... SET DATA TYPE`: Este formulário altera o tipo de um atributo de um tipo composto.

`ADD VALUE [ IF NOT EXISTS ] [ BEFORE | AFTER ]`: Este formulário adiciona um novo valor a um tipo de enum. O lugar do novo valor na ordem do enum pode ser especificado como sendo `BEFORE` ou `AFTER`, um dos valores existentes. Caso contrário, o novo item é adicionado no final da lista de valores.

Se `IF NOT EXISTS` for especificado, não é um erro se o tipo já contiver o novo valor: um aviso é emitido, mas nenhuma outra ação é tomada. Caso contrário, ocorrerá um erro se o novo valor já estiver presente.

`RENAME VALUE`: Este formulário renomeia um valor de um tipo de enum. O lugar do valor na ordem do enum não é afetado. Um erro ocorrerá se o valor especificado não estiver presente ou se o novo nome já estiver presente.

`SET ( property = value [, ... ] )`: Este formulário é aplicável apenas aos tipos básicos. Permite o ajuste de um subconjunto das propriedades do tipo básico que podem ser definidas em `CREATE TYPE`. Especificamente, essas propriedades podem ser alteradas:

* `RECEIVE` pode ser definido como o nome de uma função de entrada binária, ou `NONE` para remover a função de entrada binária do tipo. O uso desta opção requer privilégio de administrador. * `SEND` pode ser definido como o nome de uma função de saída binária, ou `NONE` para remover a função de saída binária do tipo. O uso desta opção requer privilégio de administrador. * `TYPMOD_IN` pode ser definido como o nome de uma função de entrada de modificador de tipo, ou `NONE` para remover a função de entrada de modificador de tipo do tipo. O uso desta opção requer privilégio de administrador. * `TYPMOD_OUT` pode ser definido como o nome de uma função de saída de modificador de tipo, ou `NONE` para remover a função de saída de modificador de tipo do tipo. O uso desta opção requer privilégio de administrador. * `ANALYZE` pode ser definido como o nome de uma função de coleta de estatísticas específica do tipo, ou `NONE` para remover a função de coleta de estatísticas do tipo. O uso desta opção requer privilégio de administrador. * `SUBSCRIPT` pode ser definido como o nome de uma função de subscrito específica do tipo, ou `NONE` para remover a função de subscrito do tipo. O uso desta opção requer privilégio de administrador. * `STORAGE` pode ser definido como `plain`, `extended`, `external` ou `main` (consulte [Seção 66.2](storage-toast.md "66.2. TOAST") para mais informações sobre o que isso significa). No entanto, alterar de `plain` para outra configuração requer privilégio de administrador (porque exige que as funções C do tipo sejam todas preparadas para TOAST), e alterar para `plain` a partir de outra configuração não é permitido de forma alguma (já que o tipo pode ter valores TOASTados presentes no banco de dados). Note que alterar esta opção não altera, por si só, nenhum dado armazenado, ela apenas define a estratégia padrão de TOAST a ser usada para colunas de tabela criadas no futuro. Veja [ALTER TABLE](sql-altertable.md "ALTER TABLE") para alterar a estratégia de TOAST para colunas de tabela existentes.

Veja [CREATE TYPE](sql-createtype.md "CREATE TYPE") para mais detalhes sobre essas propriedades do tipo. Observe que, quando apropriado, uma mudança nesses atributos de um tipo base será propagada automaticamente para domínios com base nesse tipo.

As ações `ADD ATTRIBUTE`, `DROP ATTRIBUTE` e `ALTER ATTRIBUTE` podem ser combinadas em uma lista de várias alterações para serem aplicadas em paralelo. Por exemplo, é possível adicionar vários atributos e/ou alterar o tipo de vários atributos em um único comando.

Você deve possuir o tipo para usar `ALTER TYPE`. Para alterar o esquema de um tipo, você também deve ter `CREATE` privilégio no novo esquema. Para alterar o proprietário, você deve ser capaz de `SET ROLE` para o novo papel de proprietário, e esse papel deve ter `CREATE` privilégio no esquema do tipo. (Essas restrições garantem que alterar o proprietário não faz nada que você não poderia fazer ao descartar e recriar o tipo. No entanto, um superusuário pode alterar a propriedade de qualquer tipo de qualquer maneira.) Para adicionar um atributo ou alterar um tipo de atributo, você também deve ter `USAGE` privilégio no tipo de dados do atributo.

## Parâmetros

*`name`*: O nome (possivelmente qualificado por esquema) de um tipo existente que se deseja alterar.

*`new_name`*: O novo nome para o tipo.

*`new_owner`*: O nome do usuário do novo proprietário do tipo.

*`new_schema`*: O novo esquema para o tipo.

*`attribute_name`*: O nome do atributo a ser adicionado, alterado ou excluído.

*`new_attribute_name`*: O novo nome do atributo que será renomeado.

*`data_type`*: O tipo de dados do atributo a ser adicionado ou o novo tipo do atributo a ser alterado.

*`new_enum_value`*: O novo valor a ser adicionado à lista de valores de um tipo de enum, ou o novo nome a ser dado a um valor existente. Como todos os literais de enum, ele precisa ser citado.

*`neighbor_enum_value`*: O valor existente do enum que o novo valor deve ser adicionado imediatamente antes ou depois na ordem de classificação do tipo de enum. Como todos os literais de enum, ele precisa ser citado.

*`existing_enum_value`*: O valor existente do enum que deve ser renomeado. Como todos os literais de enum, ele precisa ser citado.

*`property`*: O nome de uma propriedade de tipo de base a ser modificada; consulte o acima para valores possíveis.

`CASCADE`: Propague automaticamente a operação para tabelas digitadas do tipo que está sendo alterado e seus descendentes.

`RESTRICT`: Recuse a operação se o tipo que está sendo alterado for o tipo de uma tabela tipada. Isso é o padrão.

## Notas

Se `ALTER TYPE ... ADD VALUE` (o formulário que adiciona um novo valor a um tipo de enum) for executado dentro de um bloco de transação, o novo valor não pode ser usado até que a transação tenha sido comprometida.

As comparações que envolvem um valor adicional do enum serão, às vezes, mais lentas do que as comparações que envolvem apenas os membros originais do tipo enum. Isso geralmente ocorre apenas se `BEFORE` ou `AFTER` é usado para definir a posição de classificação do novo valor em outro lugar que não no final da lista. No entanto, às vezes, isso acontece mesmo que o novo valor seja adicionado no final (isso ocorre se o contador de OID "voltou" desde a criação original do tipo enum). O atraso geralmente é insignificante; mas se for importante, o desempenho ótimo pode ser recuperado descartando e recriando o tipo enum, ou descartando e restaurando o banco de dados.

## Exemplos

Para renomear um tipo de dados:

```
ALTER TYPE electronic_mail RENAME TO email;
```

Para alterar o proprietário do tipo `email` para `joe`:

```
ALTER TYPE email OWNER TO joe;
```

Para alterar o esquema do tipo `email` para `customers`:

```
ALTER TYPE email SET SCHEMA customers;
```

Para adicionar um novo atributo a um tipo composto:

```
ALTER TYPE compfoo ADD ATTRIBUTE f3 int;
```

Para adicionar um novo valor a um tipo de enum em uma posição de classificação específica:

```
ALTER TYPE colors ADD VALUE 'orange' AFTER 'red';
```

Para renomear um valor de enum:

```
ALTER TYPE colors RENAME VALUE 'purple' TO 'mauve';
```

Para criar funções de E/S binárias para um tipo de base existente:

```
CREATE FUNCTION mytypesend(mytype) RETURNS bytea ...;
CREATE FUNCTION mytyperecv(internal, oid, integer) RETURNS mytype ...;
ALTER TYPE mytype SET (
    SEND = mytypesend,
    RECEIVE = mytyperecv
);
```

## Compatibilidade

As variantes para adicionar e descartar atributos fazem parte do padrão SQL; as outras variantes são extensões do PostgreSQL.

## Veja também

[Crie o tipo](sql-createtype.md "CREATE TYPE"), [Remova o tipo](sql-droptype.md "DROP TYPE")