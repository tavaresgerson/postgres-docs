## TRUNCAR

TRUNCATE — esvazie uma tabela ou um conjunto de tabelas

## Sinopse

```
TRUNCATE [ TABLE ] [ ONLY ] name [ * ] [, ... ]
    [ RESTART IDENTITY | CONTINUE IDENTITY ] [ CASCADE | RESTRICT ]
```

## Descrição

`TRUNCATE` remove rapidamente todas as linhas de um conjunto de tabelas. Tem o mesmo efeito que um `DELETE` não qualificado em cada tabela, mas, como ele não digitaliza as tabelas, é mais rápido. Além disso, ele reclama o espaço em disco imediatamente, em vez de exigir uma operação subsequente `VACUUM`. Isso é muito útil em tabelas grandes.

## Parâmetros

*`name`*: O nome (opcionalmente qualificado por esquema) de uma tabela a ser truncada. Se `ONLY` for especificado antes do nome da tabela, apenas essa tabela será truncada. Se `ONLY` não for especificado, a tabela e todas as suas tabelas descendentes (se houver) serão truncadas. Opcionalmente, `*` pode ser especificado após o nome da tabela para indicar explicitamente que as tabelas descendentes são incluídas.

`RESTART IDENTITY`: Reinicie automaticamente as sequências de propriedade de colunas da(s) tabela(s) truncada(s).

`CONTINUE IDENTITY`: Não modifique os valores das sequências. Este é o padrão.

`CASCADE`: Trate automaticamente todas as tabelas que tenham referências de chave estrangeira para qualquer uma das tabelas nomeadas, ou para qualquer tabela adicionada ao grupo devido a `CASCADE`.

`RESTRICT`: Recusar a truncação se alguma das tabelas tiver referências de chave estrangeira de tabelas que não estão listadas no comando. Este é o padrão.

## Notas

Você deve ter o privilégio `TRUNCATE` em uma tabela para truncá-la.

`TRUNCATE` adquire um bloqueio `ACCESS EXCLUSIVE` em cada tabela que opera, o que bloqueia todas as outras operações concorrentes na tabela. Quando `RESTART IDENTITY` é especificado, quaisquer sequências que devem ser reiniciadas também são bloqueadas exclusivamente. Se o acesso concorrente a uma tabela for necessário, então o comando `DELETE` deve ser usado em vez disso.

`TRUNCATE` não pode ser usado em uma tabela que tenha referências de chave estrangeira de outras tabelas, a menos que todas essas tabelas também sejam truncadas no mesmo comando. Verificar a validade nesses casos exigiria varreduras de tabela, e o ponto principal não é fazer uma delas. A opção `CASCADE` pode ser usada para incluir automaticamente todas as tabelas dependentes — mas tenha muito cuidado ao usar essa opção, pois você pode perder dados que não tinha a intenção de perder! Note, em particular, que quando a tabela a ser truncada é uma partição, as partições irmãs são deixadas intocadas, mas ocorre uma cascata para todas as tabelas de referência e todas as suas partições, sem distinção.

`TRUNCATE` não disparará quaisquer `ON DELETE` que possam existir para as tabelas. Mas disparará os `ON TRUNCATE` triggers. Se os triggers `ON TRUNCATE` forem definidos para qualquer uma das tabelas, então todos os `BEFORE TRUNCATE` triggers são disparados antes que qualquer truncação ocorra, e todos os `AFTER TRUNCATE` triggers são disparados após a última truncação ser realizada e quaisquer sequências serem redefinidas. Os triggers serão disparados na ordem em que as tabelas devem ser processadas (primeiramente as listadas no comando, e depois quaisquer que tenham sido adicionadas devido ao cascata).

`TRUNCATE` não é seguro para MVCC. Após a truncagem, a tabela parecerá vazia para transações concorrentes, se elas estiverem usando um instantâneo tirado antes da truncagem ter ocorrido. Consulte [Seção 13.6](mvcc-caveats.md) para mais detalhes.

`TRUNCATE` é seguro em relação às transações dos dados nas tabelas: o truncamento será desfeito com segurança se a transação circundante não for confirmada.

Quando `RESTART IDENTITY` é especificado, as operações implícitas de `ALTER SEQUENCE RESTART` também são realizadas de forma transacional; ou seja, serão revertidas se a transação circundante não for confirmada. Esteja ciente de que, se quaisquer operações adicionais de sequência forem realizadas nas sequências reativadas antes de a transação ser revertida, os efeitos dessas operações nas sequências serão revertidos, mas não seus efeitos em `currval()`; ou seja, após a transação `currval()` continuará a refletir o último valor da sequência obtido dentro da transação falha, mesmo que a própria sequência já não seja consistente com isso. Isso é semelhante ao comportamento usual de `currval()` após uma transação falha.

`TRUNCATE` pode ser usado para tabelas estrangeiras se for suportado pelo wrapper de dados estrangeiro, por exemplo, veja [postgres_fdw](postgres-fdw.md).

## Exemplos

Retorne os quadros `bigtable` e `fattable`:

```
TRUNCATE bigtable, fattable;
```

O mesmo, e também redefinir quaisquer geradores de sequência associados:

```
TRUNCATE bigtable, fattable RESTART IDENTITY;
```

Retorne a tabela `othertable` e faça cascata para quaisquer tabelas que façam referência a `othertable` por meio de restrições de chave estrangeira:

```
TRUNCATE othertable CASCADE;
```

## Compatibilidade

O padrão SQL:2008 inclui um comando `TRUNCATE` com a sintaxe `TRUNCATE TABLE tablename`. As cláusulas `CONTINUE IDENTITY`/`RESTART IDENTITY` também aparecem nesse padrão, mas têm significados ligeiramente diferentes, embora relacionados. Algumas das ações de concorrência desse comando são deixadas para definição de implementação pelo padrão, então as notas acima devem ser consideradas e comparadas com outras implementações, se necessário.

## Veja também

[DELETE](sql-delete.md "DELETE")
