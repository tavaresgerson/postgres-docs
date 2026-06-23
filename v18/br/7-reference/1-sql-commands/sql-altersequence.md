## ALTER SEQUENCE

ALTER SEQUENCE — alterar a definição de um gerador de sequência

## Sinopse

```
ALTER SEQUENCE [ IF EXISTS ] name
    [ AS data_type ]
    [ INCREMENT [ BY ] increment ]
    [ MINVALUE minvalue | NO MINVALUE ] [ MAXVALUE maxvalue | NO MAXVALUE ]
    [ [ NO ] CYCLE ]
    [ START [ WITH ] start ]
    [ RESTART [ [ WITH ] restart ] ]
    [ CACHE cache ]
    [ OWNED BY { table_name.column_name | NONE } ]
ALTER SEQUENCE [ IF EXISTS ] name SET { LOGGED | UNLOGGED }
ALTER SEQUENCE [ IF EXISTS ] name OWNER TO { new_owner | CURRENT_ROLE | CURRENT_USER | SESSION_USER }
ALTER SEQUENCE [ IF EXISTS ] name RENAME TO new_name
ALTER SEQUENCE [ IF EXISTS ] name SET SCHEMA new_schema
```

## Descrição

`ALTER SEQUENCE` altera os parâmetros de um gerador de sequência existente. Quaisquer parâmetros que não sejam especificamente definidos no comando `ALTER SEQUENCE` mantêm suas configurações anteriores.

Você deve possuir a sequência para usar `ALTER SEQUENCE`. Para alterar o esquema de uma sequência, você também deve ter privilégio `CREATE` no novo esquema. Para alterar o proprietário, você deve ser capaz de `SET ROLE` para o novo papel de proprietário, e esse papel deve ter privilégio `CREATE` no esquema da sequência. (Essas restrições garantem que alterar o proprietário não faz nada que você não pudesse fazer ao descartar e recriar a sequência. No entanto, um superusuário pode alterar a propriedade de qualquer sequência de qualquer maneira.)

## Parâmetros

*`name`*: O nome (opcionalmente qualificado por esquema) de uma sequência que será alterada.

`IF EXISTS`: Não emita um erro se a sequência não existir. Um aviso é emitido neste caso.

*`data_type`*: A cláusula opcional `AS data_type` altera o tipo de dados da sequência. Os tipos válidos são `smallint`, `integer` e `bigint`.

Alterar o tipo de dados automaticamente altera os valores mínimo e máximo da sequência se e somente se os valores mínimo e máximo anteriores fossem o valor mínimo ou máximo do tipo de dados antigo (em outras palavras, se a sequência tivesse sido criada usando `NO MINVALUE` ou `NO MAXVALUE`, implicitamente ou explicitamente). Caso contrário, os valores mínimo e máximo são preservados, a menos que novos valores sejam fornecidos como parte do mesmo comando. Se os valores mínimo e máximo não se encaixarem no novo tipo de dados, um erro será gerado.

*`increment`*: A cláusula `INCREMENT BY increment` é opcional. Um valor positivo fará uma sequência ascendente, um valor negativo uma sequência descendente. Se não especificado, o valor antigo do incremento será mantido.

*`minvalue`* `NO MINVALUE`: A cláusula opcional `MINVALUE minvalue` determina o valor mínimo que uma sequência pode gerar. Se `NO MINVALUE` for especificado, os valores padrão de 1 e o valor mínimo do tipo de dados para sequências ascendentes e descendentes, respectivamente, serão usados. Se nenhuma opção for especificada, o valor mínimo atual será mantido.

*`maxvalue`* `NO MAXVALUE`: A cláusula opcional `MAXVALUE maxvalue` determina o valor máximo para a sequência. Se `NO MAXVALUE` for especificado, os valores padrão do valor máximo do tipo de dados e -1 para sequências ascendentes e descendentes, respectivamente, serão usados. Se nenhuma opção for especificada, o valor máximo atual será mantido.

`CYCLE`: A palavra-chave opcional `CYCLE` pode ser usada para permitir que a sequência se repita quando o *`maxvalue`* ou *`minvalue`* for alcançado por uma sequência ascendente ou descendente, respectivamente. Se o limite for atingido, o próximo número gerado será o *`minvalue`* ou *`maxvalue`*, respectivamente.

`NO CYCLE`: Se a palavra-chave opcional `NO CYCLE` for especificada, quaisquer chamadas para `nextval` após a sequência atingir seu valor máximo retornarão um erro. Se nem `CYCLE` nem `NO CYCLE` forem especificados, o comportamento do ciclo antigo será mantido.

*`start`*: A cláusula opcional `START WITH start` altera o valor inicial registrado da sequência. Isso não afeta o valor *atual* da sequência; simplesmente define o valor que os comandos futuros do `ALTER SEQUENCE RESTART` usarão.

*`restart`*: A cláusula opcional `RESTART [ WITH restart ]` altera o valor atual da sequência. Isso é semelhante a chamar a função `setval` com `is_called` = `false`: o valor especificado será retornado pelo *próximo* chamado de `nextval`. Escrever `RESTART` sem *`restart`* é equivalente a fornecer o valor inicial que foi registrado por `CREATE SEQUENCE` ou definido pela última `ALTER SEQUENCE START WITH`.

Em contraste com uma chamada `setval`, uma operação `RESTART` em uma sequência é transacional e bloqueia transações concorrentes de obter números da mesma sequência. Se esse não for o modo de operação desejado, deve-se usar `setval`.

*`cache`*: A cláusula `CACHE cache` permite que os números de sequência sejam pré-alocados e armazenados na memória para acesso mais rápido. O valor mínimo é 1 (apenas um valor pode ser gerado de cada vez, ou seja, sem cache). Se não especificado, o valor antigo do cache será mantido.

`SET { LOGGED | UNLOGGED }`: Este formulário altera a sequência de não registrada para registrada ou vice-versa (consulte [CREATE SEQUENCE](sql-createsequence.md "CREATE SEQUENCE")). Não pode ser aplicado a uma sequência temporária.

`OWNED BY` *`table_name`*.*`column_name`* `OWNED BY NONE`: A opção `OWNED BY` faz com que a sequência seja associada a uma coluna específica da tabela, de modo que, se essa coluna (ou toda a tabela) for excluída, a sequência também será automaticamente excluída. Se especificada, essa associação substitui qualquer associação especificada anteriormente para a sequência. A tabela especificada deve ter o mesmo proprietário e estar no mesmo esquema que a sequência. Especificar `OWNED BY NONE` remove qualquer associação existente, tornando a sequência “autônoma”.

*`new_owner`*: O nome do usuário do novo proprietário da sequência.

*`new_name`*: O novo nome para a sequência.

*`new_schema`*: O novo esquema para a sequência.

## Notas

`ALTER SEQUENCE` não afetará imediatamente os resultados do `nextval` nos backends, exceto o atual, que possuem valores de sequência pré-alocados (cacheados). Eles consumirão todos os valores cacheados antes de notar os parâmetros de geração de sequência alterados. O backend atual será afetado imediatamente.

`ALTER SEQUENCE` não afeta o status `currval` para a sequência. (Antes do PostgreSQL 8.3, às vezes isso acontecia.)

`ALTER SEQUENCE` bloqueia chamadas concorrentes para `nextval`, `currval`, `lastval` e `setval`.

Por razões históricas, `ALTER TABLE` também pode ser usado com sequências; mas as únicas variantes de `ALTER TABLE` que são permitidas com sequências são equivalentes às formas mostradas acima.

## Exemplos

Reinicie uma sequência chamada `serial`, na posição 105:

```
ALTER SEQUENCE serial RESTART WITH 105;
```

## Compatibilidade

`ALTER SEQUENCE` está em conformidade com o padrão SQL, exceto pelas cláusulas `AS`, `START WITH`, `OWNED BY`, `OWNER TO`, `RENAME TO` e `SET SCHEMA`, que são extensões do PostgreSQL.

## Veja também

[Crie Sequência](sql-createsequence.md "CREATE SEQUENCE"), [Retire Sequência](sql-dropsequence.md "DROP SEQUENCE")