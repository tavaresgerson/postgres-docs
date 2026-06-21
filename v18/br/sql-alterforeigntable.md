## ALTER FOREIGN TABLE

ALTER TABLE FOREIGN — alterar a definição de uma tabela estrangeira

## Sinopse

```
ALTER FOREIGN TABLE [ IF EXISTS ] [ ONLY ] name [ * ]
    action [, ... ]
ALTER FOREIGN TABLE [ IF EXISTS ] [ ONLY ] name [ * ]
    RENAME [ COLUMN ] column_name TO new_column_name
ALTER FOREIGN TABLE [ IF EXISTS ] name
    RENAME TO new_name
ALTER FOREIGN TABLE [ IF EXISTS ] name
    SET SCHEMA new_schema

where action is one of:

    ADD [ COLUMN ] [ IF NOT EXISTS ] column_name data_type [ COLLATE collation ] [ column_constraint [ ... ] ]
    DROP [ COLUMN ] [ IF EXISTS ] column_name [ RESTRICT | CASCADE ]
    ALTER [ COLUMN ] column_name [ SET DATA ] TYPE data_type [ COLLATE collation ]
    ALTER [ COLUMN ] column_name SET DEFAULT expression
    ALTER [ COLUMN ] column_name DROP DEFAULT
    ALTER [ COLUMN ] column_name { SET | DROP } NOT NULL
    ALTER [ COLUMN ] column_name SET STATISTICS integer
    ALTER [ COLUMN ] column_name SET ( attribute_option = value [, ... ] )
    ALTER [ COLUMN ] column_name RESET ( attribute_option [, ... ] )
    ALTER [ COLUMN ] column_name SET STORAGE { PLAIN | EXTERNAL | EXTENDED | MAIN | DEFAULT }
    ALTER [ COLUMN ] column_name OPTIONS ( [ ADD | SET | DROP ] option ['value'] [, ... ])
    ADD table_constraint [ NOT VALID ]
    VALIDATE CONSTRAINT constraint_name
    DROP CONSTRAINT [ IF EXISTS ]  constraint_name [ RESTRICT | CASCADE ]
    DISABLE TRIGGER [ trigger_name | ALL | USER ]
    ENABLE TRIGGER [ trigger_name | ALL | USER ]
    ENABLE REPLICA TRIGGER trigger_name
    ENABLE ALWAYS TRIGGER trigger_name
    SET WITHOUT OIDS
    INHERIT parent_table
    NO INHERIT parent_table
    OWNER TO { new_owner | CURRENT_ROLE | CURRENT_USER | SESSION_USER }
    OPTIONS ( [ ADD | SET | DROP ] option ['value'] [, ... ])
```

## Descrição

`ALTER FOREIGN TABLE` altera a definição de uma tabela estrangeira existente. Existem vários subformularios:

`ADD [ COLUMN ] [ IF NOT EXISTS ]`: Este formulário adiciona uma nova coluna à tabela estrangeira, usando a mesma sintaxe que [`CREATE FOREIGN TABLE`](sql-createforeigntable.md "CREATE FOREIGN TABLE"). Se `IF NOT EXISTS` for especificado e uma coluna já existir com esse nome, não será lançada nenhuma exceção. Ao contrário do caso quando se adiciona uma coluna a uma tabela regular, nada acontece com o armazenamento subjacente: essa ação simplesmente declara que alguma nova coluna agora é acessível através da tabela estrangeira.

`DROP [ COLUMN ] [ IF EXISTS ]`: Este formulário exclui uma coluna de uma tabela externa. Você precisará dizer `CASCADE` se algo fora da tabela depender da coluna; por exemplo, visualizações. Se `IF EXISTS` for especificado e a coluna não existir, nenhum erro é lançado. Nesse caso, um aviso é emitido em vez disso.

`SET DATA TYPE`: Este formulário altera o tipo de uma coluna de uma tabela estrangeira. Novamente, isso não afeta qualquer armazenamento subjacente: essa ação simplesmente altera o tipo que o PostgreSQL acredita que a coluna tenha.

`SET`/`DROP DEFAULT`: Esses formulários definem ou removem o valor padrão para uma coluna. Os valores padrão só se aplicam em comandos subsequentes `INSERT` ou `UPDATE`; eles não fazem com que as linhas já na tabela sejam alteradas.

`SET`/`DROP NOT NULL`: Marque uma coluna como permitindo ou não permitindo valores nulos.

`SET STATISTICS`: Este formulário define o objetivo de coleta de estatísticas por coluna para operações subsequentes do `ANALYZE` (sql-analyze.md "ANALYZE"). Consulte o formulário semelhante do `ALTER TABLE` (sql-altertable.md "ALTER TABLE") para mais detalhes.

`SET ( attribute_option = value [, ... ] )` `RESET ( attribute_option [, ... ] )`: Este formulário define ou redefiniu opções por atributo. Consulte o formulário semelhante de [`ALTER TABLE`](sql-altertable.md "ALTER TABLE") para mais detalhes.

`SET STORAGE`: Este formulário define o modo de armazenamento para uma coluna. Consulte o formulário semelhante de `ALTER TABLE`(sql-altertable.md "ALTER TABLE") para mais detalhes. Observe que o modo de armazenamento não tem efeito a menos que o wrapper de dados externos da tabela escolha prestar atenção nele.

`ADD table_constraint [ NOT VALID ]`: Este formulário adiciona uma nova restrição a uma tabela estrangeira, usando a mesma sintaxe que [`CREATE FOREIGN TABLE`](sql-createforeigntable.md "CREATE FOREIGN TABLE"). Atualmente, apenas as restrições `CHECK` e `NOT NULL` são suportadas.

Ao contrário do caso em que se adiciona uma restrição a uma tabela regular, nada é feito para verificar se a restrição está correta; em vez disso, essa ação simplesmente declara que alguma nova condição deve ser assumida para todas as linhas da tabela estrangeira. (Veja a discussão em `CREATE FOREIGN TABLE` (sql-createforeigntable.md "CREATE FOREIGN TABLE"). Se a restrição estiver marcada `NOT VALID` (permitida apenas para o caso `CHECK`, então não é assumida que ela seja válida, mas apenas registrada para uso possível no futuro.

`VALIDATE CONSTRAINT`: Este formulário marca como válida uma restrição que anteriormente estava marcada como `NOT VALID`. Não é tomada nenhuma ação para verificar a restrição, mas as consultas futuras irão assumir que ela se mantém.

`DROP CONSTRAINT [ IF EXISTS ]`: Este formulário elimina a restrição especificada em uma tabela estrangeira. Se `IF EXISTS` for especificado e a restrição não existir, não será lançada nenhuma exceção. Nesse caso, é emitido um aviso em vez disso.

`DISABLE`/`ENABLE [ REPLICA | ALWAYS ] TRIGGER`: Esses formulários configuram o disparo do(s) gatilho(s) pertencente(s) à tabela estrangeira. Consulte o formulário semelhante de `ALTER TABLE`(sql-altertable.md "ALTER TABLE") para mais detalhes.

`SET WITHOUT OIDS`: Sintaxe de compatibilidade reversa para remover a coluna do sistema `oid`. Como as colunas do sistema `oid` não podem ser adicionadas mais, isso nunca tem efeito.

`INHERIT parent_table`: Este formulário adiciona a tabela estrangeira alvo como uma nova criança da tabela pai especificada. Consulte o formulário semelhante de `ALTER TABLE`(sql-altertable.md "ALTER TABLE") para mais detalhes.

`NO INHERIT parent_table`: Este formulário remove a tabela estrangeira alvo da lista de filhos da tabela pai especificada.

`OWNER`: Este formulário muda o proprietário da tabela estrangeira para o usuário especificado.

`OPTIONS ( [ ADD | SET | DROP ] option ['value'] [, ... ] )`: Opções de alteração para a tabela estrangeira ou uma de suas colunas. `ADD`, `SET` e `DROP` especificam a ação a ser realizada. `ADD` é assumido se nenhuma operação for especificada explicitamente. Nomes de opções duplicados não são permitidos (embora seja OK para uma opção de tabela e uma opção de coluna terem o mesmo nome). Os nomes e valores das opções também são validados usando a biblioteca de wrapper de dados externos.

`RENAME`: As formas dos `RENAME` alteram o nome de uma tabela estrangeira ou o nome de uma coluna individual em uma tabela estrangeira.

`SET SCHEMA`: Este formulário move a tabela estrangeira para outro esquema.

Todas as ações, exceto `RENAME` e `SET SCHEMA`, podem ser combinadas em uma lista de várias alterações para serem aplicadas em paralelo. Por exemplo, é possível adicionar várias colunas e/ou alterar o tipo de várias colunas em um único comando.

Se o comando for escrito como `ALTER FOREIGN TABLE IF EXISTS ...` e a tabela estrangeira não existir, não será lançada nenhuma exceção. Neste caso, é emitido um aviso.

Você deve possuir a tabela para usar `ALTER FOREIGN TABLE`. Para alterar o esquema de uma tabela estrangeira, você também deve ter `CREATE` privilégio no novo esquema. Para alterar o proprietário, você deve ser capaz de `SET ROLE` para o novo papel de proprietário, e esse papel deve ter `CREATE` privilégio no esquema da tabela. (Essas restrições garantem que alterar o proprietário não faz nada que você não poderia fazer ao descartar e recriar a tabela. No entanto, um superusuário pode alterar a propriedade de qualquer tabela de qualquer maneira.) Para adicionar uma coluna ou alterar o tipo de coluna, você também deve ter `USAGE` privilégio no tipo de dados.

## Parâmetros

*`name`*: O nome (possivelmente qualificado por esquema) de uma tabela estrangeira existente para alterar. Se `ONLY` é especificado antes do nome da tabela, apenas essa tabela é alterada. Se `ONLY` não é especificado, a tabela e todas as suas tabelas descendentes (se houver) são alteradas. Opcionalmente, `*` pode ser especificado após o nome da tabela para indicar explicitamente que as tabelas descendentes são incluídas.

*`column_name`*: Nome de uma coluna nova ou existente.

*`new_column_name`*: Novo nome para uma coluna existente.

*`new_name`*: Novo nome para a tabela.

*`data_type`*: Tipo de dados da nova coluna, ou novo tipo de dados para uma coluna existente.

*`table_constraint`*: Nova restrição de tabela para a tabela estrangeira.

*`constraint_name`*: Nome de uma restrição existente a ser descartada.

`CASCADE`: Descarte automaticamente os objetos que dependem da coluna ou restrição descartada (por exemplo, visualizações que fazem referência à coluna), e, por sua vez, todos os objetos que dependem desses objetos (consulte [Seção 5.15][(ddl-depend.md "5.15. Dependency Tracking")]).

`RESTRICT`: Rejeitar a eliminação da coluna ou restrição se houver quaisquer objetos dependentes. Esse é o comportamento padrão.

*`trigger_name`*: Nome de um único gatilho para desabilitar ou habilitar.

`ALL`: Desabilitar ou habilitar todos os gatilhos pertencentes à tabela estrangeira. (Isso requer privilégio de superusuário, se algum dos gatilhos for um gatilho gerado internamente. O sistema principal não adiciona tais gatilhos às tabelas estrangeiras, mas o código adicional pode fazer isso.)

`USER`: Desabilitar ou habilitar todos os gatilhos pertencentes à tabela externa, exceto os gatilhos gerados internamente.

*`parent_table`*: Uma tabela principal para associar ou desassociar com esta tabela estrangeira.

*`new_owner`*: O nome do usuário do novo proprietário da tabela.

*`new_schema`*: O nome do esquema para o qual a tabela será movida.

## Notas

A palavra-chave `COLUMN` é ruído e pode ser omitida.

A consistência com o servidor estrangeiro não é verificada quando uma coluna é adicionada ou removida com `ADD COLUMN` ou `DROP COLUMN`, uma restrição `NOT NULL` ou `CHECK` é adicionada, ou o tipo de coluna é alterado com `SET DATA TYPE`. É responsabilidade do usuário garantir que a definição da tabela corresponda ao lado remoto.

Consulte `CREATE FOREIGN TABLE`(sql-createforeigntable.md "CREATE FOREIGN TABLE") para uma descrição adicional dos parâmetros válidos.

## Exemplos

Para marcar uma coluna como não nula:

```
ALTER FOREIGN TABLE distributors ALTER COLUMN street SET NOT NULL;
```

Para alterar as opções de uma tabela estrangeira:

```
ALTER FOREIGN TABLE myschema.distributors OPTIONS (ADD opt1 'value', SET opt2 'value2', DROP opt3);
```

## Compatibilidade

Os formulários `ADD`, `DROP` e `SET DATA TYPE` estão em conformidade com o padrão SQL. Os outros formulários são extensões do padrão SQL do PostgreSQL. Além disso, a capacidade de especificar mais de uma manipulação em um único comando `ALTER FOREIGN TABLE` é uma extensão.

`ALTER FOREIGN TABLE DROP COLUMN` pode ser usado para descartar a única coluna de uma tabela estrangeira, deixando uma tabela de coluna zero. Esta é uma extensão do SQL, que não permite tabelas estrangeiras de coluna zero.

## Veja também

[Crie uma tabela estrangeira](sql-createforeigntable.md "CREATE FOREIGN TABLE"), [Remova a tabela estrangeira](sql-dropforeigntable.md "DROP FOREIGN TABLE")