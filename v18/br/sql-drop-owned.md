## DROP OWNED

DROP OWNED — remova objetos de banco de dados de propriedade de um papel de banco de dados

## Sinopse

```
DROP OWNED BY { name | CURRENT_ROLE | CURRENT_USER | SESSION_USER } [, ...] [ CASCADE | RESTRICT ]
```

## Descrição

`DROP OWNED` elimina todos os objetos dentro do banco de dados atual que são de propriedade de um dos papéis especificados. Quaisquer privilégios concedidos aos papéis fornecidos em objetos no banco de dados atual ou em objetos compartilhados (bancos de dados, espaços de tabela, parâmetros de configuração) também serão revogados.

## Parâmetros

*`name`*: O nome de um papel cujos objetos serão removidos e cujos privilégios serão revogados.

`CASCADE`: Descarte automaticamente os objetos que dependem dos objetos afetados e, por sua vez, todos os objetos que dependem desses objetos (consulte [Seção 5.15](ddl-depend.md)).

`RESTRICT`: Rejeitar a eliminação dos objetos de propriedade de um papel se outros objetos de banco de dados dependerem de um dos objetos afetados. Este é o padrão.

## Notas

`DROP OWNED` é frequentemente usado para preparar a remoção de um ou mais papéis. Como `DROP OWNED` afeta apenas os objetos no banco de dados atual, geralmente é necessário executar este comando em cada banco de dados que contém objetos de propriedade de um papel que será removido.

Usar a opção `CASCADE` pode fazer com que o comando recupere objetos de outros usuários.

O comando `REASSIGN OWNED`(sql-reassign-owned.md "REASSIGN OWNED") é uma alternativa que reatribui a propriedade de todos os objetos do banco de dados detidos por um ou mais papéis. No entanto, o `REASSIGN OWNED` não lida com privilégios para outros objetos.

Os bancos de dados e os espaços de tabela de propriedade do(s) papel(is) não serão removidos.

Veja [Seção 21.4](role-removal.md) para mais discussão.

## Compatibilidade

O comando `DROP OWNED` é uma extensão do PostgreSQL.

## Veja também

[REASSIGN OWNED](sql-reassign-owned.md "REASSIGN OWNED"), [DROP ROLE](sql-droprole.md "DROP ROLE")