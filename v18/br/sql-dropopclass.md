## CLASS DO OPERADOR DROP

DROP OPERATOR CLASS — remova uma classe de operador

## Sinopse

```
DROP OPERATOR CLASS [ IF EXISTS ] name USING index_method [ CASCADE | RESTRICT ]
```

## Descrição

`DROP OPERATOR CLASS` elimina uma classe de operador existente. Para executar este comando, você deve ser o proprietário da classe de operador.

`DROP OPERATOR CLASS` não elimina nenhum dos operadores ou funções referenciados pela classe. Se houver algum índice dependente da classe do operador, você precisará especificar `CASCADE` para que a eliminação seja concluída.

## Parâmetros

`IF EXISTS`: Não exija erro se a classe do operador não existir. Neste caso, é emitido um aviso.

*`name`*: O nome (opcionalmente qualificado por esquema) de uma classe de operador existente.

*`index_method`*: O nome do método de acesso ao índice para o qual a classe do operador é destinada.

`CASCADE`: Descarte automaticamente os objetos que dependem da classe do operador (como índices) e, por sua vez, todos os objetos que dependem desses objetos (consulte [Seção 5.15][(ddl-depend.md "5.15. Dependency Tracking")]).

`RESTRICT`: Rejeitar a eliminação da classe de operador se houver objetos que dependem dela. Este é o padrão.

## Notas

`DROP OPERATOR CLASS` não excluirá a família de operadores que contém a classe, mesmo que não haja mais nada na família (particularmente, no caso em que a família foi criada implicitamente por `CREATE OPERATOR CLASS`). Uma família de operadores vazia é inofensiva, mas, por questões de organização, você pode desejar remover a família com `DROP OPERATOR FAMILY`; ou talvez seja melhor usar `DROP OPERATOR FAMILY` em primeiro lugar.

## Exemplos

Remova a classe de operador de árvore B `widget_ops`:

```
DROP OPERATOR CLASS widget_ops USING btree;
```

Este comando não terá sucesso se houver algum índice existente que utilize a classe do operador. Adicione `CASCADE` para descartar tais índices juntamente com a classe do operador.

## Compatibilidade

Não há nenhuma declaração `DROP OPERATOR CLASS` no padrão SQL.

## Veja também

[ALTERAR CLASSE DE OPERADOR](sql-alteropclass.md "ALTER OPERATOR CLASS"), [CADASTRAR CLASSE DE OPERADOR](sql-createopclass.md "CREATE OPERATOR CLASS"), [CANCELAR FAMÍLIA DE OPERADORES](sql-dropopfamily.md "DROP OPERATOR FAMILY")