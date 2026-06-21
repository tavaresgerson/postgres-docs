## ALTER INDEX

ALTER INDEX — alterar a definição de um índice

## Sinopse

```
ALTER INDEX [ IF EXISTS ] name RENAME TO new_name
ALTER INDEX [ IF EXISTS ] name SET TABLESPACE tablespace_name
ALTER INDEX name ATTACH PARTITION index_name
ALTER INDEX name [ NO ] DEPENDS ON EXTENSION extension_name
ALTER INDEX [ IF EXISTS ] name SET ( storage_parameter [= value] [, ... ] )
ALTER INDEX [ IF EXISTS ] name RESET ( storage_parameter [, ... ] )
ALTER INDEX [ IF EXISTS ] name ALTER [ COLUMN ] column_number
    SET STATISTICS integer
ALTER INDEX ALL IN TABLESPACE name [ OWNED BY role_name [, ... ] ]
    SET TABLESPACE new_tablespace [ NOWAIT ]
```

## Descrição

`ALTER INDEX` altera a definição de um índice existente. Há várias subformas descritas abaixo. Observe que o nível de bloqueio exigido pode diferir para cada subforma. Um bloqueio `ACCESS EXCLUSIVE` é mantido, a menos que seja explicitamente indicado. Quando várias subcomandos são listadas, o bloqueio mantido será o mais rigoroso exigido por qualquer subcomando.

`RENAME`: O formulário `RENAME` altera o nome do índice. Se o índice estiver associado a uma restrição de tabela (seja `UNIQUE`, `PRIMARY KEY` ou `EXCLUDE`), a restrição também é renomeada. Não há efeito nos dados armazenados.

Renomear um índice adquire uma `SHARE UPDATE EXCLUSIVE` lock.

`SET TABLESPACE`: Este formulário altera o espaço de tabelas do índice para o espaço de tabelas especificado e move o(s) arquivo(s) de dados associado(s) ao índice para o novo espaço de tabelas. Para alterar o espaço de tabelas de um índice, você deve possuir o índice e ter o privilégio `CREATE` no novo espaço de tabelas. Todos os índices no banco de dados atual em um espaço de tabelas podem ser movidos usando o formulário `ALL IN TABLESPACE`, que bloqueará todos os índices a serem movidos e, em seguida, moverá cada um deles. Este formulário também suporta `OWNED BY`, que apenas moverá índices de propriedade dos papéis especificados. Se a opção `NOWAIT` for especificada, o comando falhará se não conseguir adquirir todos os bloqueios necessários imediatamente. Note que os catálogos do sistema não serão movidos por este comando, use `ALTER DATABASE` ou invocções explícitas `ALTER INDEX` se desejar. Veja também [`CREATE TABLESPACE`](sql-createtablespace.md "CREATE TABLESPACE").

`ATTACH PARTITION index_name`: Faz com que o índice nomeado (possivelmente qualificado pelo esquema) se torne anexado ao índice alterado. O índice nomeado deve estar em uma partição da tabela que contém o índice sendo alterado e ter uma definição equivalente. Um índice anexado não pode ser excluído por si só e será automaticamente excluído se seu índice pai for excluído.

Se o índice nomeado já estiver anexado ao índice alterado, o comando tentará validar o índice pai se o pai estiver atualmente inválido.

`DEPENDS ON EXTENSION extension_name` `NO DEPENDS ON EXTENSION extension_name`: Este formulário marca o índice como dependente da extensão, ou não mais dependente dessa extensão se `NO` for especificado. Um índice marcado como dependente de uma extensão é automaticamente descartado quando a extensão é descartada.

`SET ( storage_parameter [= value] [, ... ] )`: Este formulário altera um ou mais parâmetros de armazenamento específicos para o método de índice. Consulte `CREATE INDEX` para obter detalhes sobre os parâmetros disponíveis. Note que o conteúdo do índice não será modificado imediatamente por este comando; dependendo do parâmetro, você pode precisar reconstruir o índice com `REINDEX` para obter os efeitos desejados.

`RESET ( storage_parameter [, ... ] )`: Este formulário redefre o(s) parâmetro(es) de armazenamento específico(s) do método de índice para seus valores padrão. Como com `SET`, pode ser necessário um `REINDEX` para atualizar o índice totalmente.

`ALTER [ COLUMN ] column_number SET STATISTICS integer`: Este formulário define o objetivo de coleta de estatísticas por coluna para operações subsequentes do `ANALYZE`(sql-analyze.md "ANALYZE") (operações de índice), embora possa ser usado apenas em colunas de índice que são definidas como uma expressão. Como as expressões não possuem um nome único, as referenciamos usando o número ordinal da coluna de índice. O objetivo pode ser definido no intervalo de 0 a 10000; alternativamente, defina-o em -1 para retornar ao uso do objetivo de estatísticas padrão do sistema ([default_statistics_target][(runtime-config-query.md#GUC-DEFAULT-STATISTICS-TARGET)]). Para mais informações sobre o uso de estatísticas pelo planejador de consultas do PostgreSQL, consulte [Seção 14.2][(planner-stats.md "14.2. Statistics Used by the Planner")].

## Parâmetros

`IF EXISTS`: Não exija erro se o índice não existir. Um aviso é emitido neste caso.

*`column_number`*: O número ordinal refere-se à posição ordinal (da esquerda para a direita) da coluna de índice.

*`name`*: O nome (possivelmente qualificado por esquema) de um índice existente que se deseja alterar.

*`new_name`*: O novo nome do índice.

*`tablespace_name`*: O tablespace para o qual o índice será movido.

*`extension_name`*: O nome da extensão da qual o índice deve depender.

*`storage_parameter`*: O nome de um parâmetro de armazenamento específico para um método de índice.

*`value`*: O novo valor para um parâmetro de armazenamento específico para um método de índice. Isso pode ser um número ou uma palavra, dependendo do parâmetro.

## Notas

Essas operações também são possíveis usando `ALTER TABLE` (sql-altertable.md "ALTER TABLE"). `ALTER INDEX` é, na verdade, apenas um alias para as formas de `ALTER TABLE` que se aplicam a índices.

Anteriormente, havia uma variante de `ALTER INDEX OWNER`, mas isso é ignorado (com um aviso). Um índice não pode ter um proprietário diferente do proprietário da sua tabela. Alterar o proprietário da tabela automaticamente altera o índice também.

Não é permitido alterar qualquer parte do índice do catálogo do sistema.

## Exemplos

Para renomear um índice existente:

```
ALTER INDEX distributors RENAME TO suppliers;
```

Para mover um índice para um espaço de tabelas diferente:

```
ALTER INDEX distributors SET TABLESPACE fasttablespace;
```

Para alterar o fator de preenchimento de um índice (assumindo que o método do índice o suporte):

```
ALTER INDEX distributors SET (fillfactor = 75);
REINDEX INDEX distributors;
```

Defina o objetivo de coleta de estatísticas para um índice de expressão:

```
CREATE INDEX coord_idx ON measured (x, y, (z + t));
ALTER INDEX coord_idx ALTER COLUMN 3 SET STATISTICS 1000;
```

## Compatibilidade

`ALTER INDEX` é uma extensão do PostgreSQL.

## Veja também

[Crie índice](sql-createindex.md "CREATE INDEX"), [Reindexe](sql-reindex.md "REINDEX")