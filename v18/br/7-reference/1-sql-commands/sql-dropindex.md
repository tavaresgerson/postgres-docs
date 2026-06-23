## DROP INDEX

DROP INDEX — remover um índice

## Sinopse

```
DROP INDEX [ CONCURRENTLY ] [ IF EXISTS ] name [, ...] [ CASCADE | RESTRICT ]
```

## Descrição

`DROP INDEX` elimina um índice existente do sistema de banco de dados. Para executar este comando, você deve ser o proprietário do índice.

## Parâmetros

`CONCURRENTLY`: Descarte o índice sem bloquear seleções concorrentes, inserções, atualizações e apagamentos na tabela do índice. Um `DROP INDEX` normal adquire um bloqueio `ACCESS EXCLUSIVE` na tabela, bloqueando outros acessos até que o descarte do índice possa ser concluído. Com esta opção, o comando, em vez disso, espera até que as transações conflitantes tenham sido concluídas.

Há várias advertências que devem ser consideradas ao usar essa opção. Apenas um nome de índice pode ser especificado, e a opção `CASCADE` não é suportada. (Assim, um índice que suporte uma restrição `UNIQUE` ou `PRIMARY KEY` não pode ser excluído dessa maneira.) Além disso, comandos regulares de `DROP INDEX` podem ser realizados dentro de um bloco de transação, mas `DROP INDEX CONCURRENTLY` não pode. Por último, índices em tabelas particionadas não podem ser excluídos usando essa opção.

Para tabelas temporárias, `DROP INDEX` é sempre não concorrente, pois nenhuma outra sessão pode acessá-las, e a eliminação de índice não concorrente é mais barata.

`IF EXISTS`: Não exija erro se o índice não existir. Um aviso é emitido neste caso.

*`name`*: O nome (opcionalmente qualificado por esquema) de um índice a ser removido.

`CASCADE`: Descarte automaticamente os objetos que dependem do índice e, por sua vez, todos os objetos que dependem desses objetos (consulte [Seção 5.15](ddl-depend.md)).

`RESTRICT`: Rejeitar a eliminação do índice se houver algum objeto dependente dele. Esse é o padrão.

## Exemplos

Este comando removerá o índice `title_idx`:

```
DROP INDEX title_idx;
```

## Compatibilidade

`DROP INDEX` é uma extensão de linguagem do PostgreSQL. Não há disposições para índices no padrão SQL.

## Veja também

[Crie índice](sql-createindex.md "CREATE INDEX")