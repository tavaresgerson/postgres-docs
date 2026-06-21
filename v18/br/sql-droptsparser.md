## DROP TEXT SEARCH PARSER

DROP TEXT SEARCH PARSER — remova um analisador de busca de texto

## Sinopse

```
DROP TEXT SEARCH PARSER [ IF EXISTS ] name [ CASCADE | RESTRICT ]
```

## Descrição

`DROP TEXT SEARCH PARSER` elimina um analisador de pesquisa de texto existente. Você deve ser um superusuário para usar este comando.

## Parâmetros

`IF EXISTS`: Não exija erro se o analisador de busca de texto não existir. Um aviso é emitido neste caso.

*`name`*: O nome (opcionalmente qualificado por esquema) de um analisador de busca de texto existente.

`CASCADE`: Descarte automaticamente os objetos que dependem do analisador de pesquisa de texto e, por sua vez, todos os objetos que dependem desses objetos (consulte [Seção 5.15][(ddl-depend.md "5.15. Dependency Tracking")]).

`RESTRICT`: Rejeitar a eliminação do analisador de busca de texto se houver objetos que dependem dele. Esse é o padrão.

## Exemplos

Remova o analisador de busca de texto `my_parser`:

```
DROP TEXT SEARCH PARSER my_parser;
```

Este comando não terá sucesso se houver alguma configuração de busca de texto existente que utilize o analisador. Adicione `CASCADE` para descartar tais configurações juntamente com o analisador.

## Compatibilidade

Não há nenhuma declaração `DROP TEXT SEARCH PARSER` no padrão SQL.

## Veja também

[ALTERAR BUSCA DE TEXTO](sql-altertsparser.md "ALTER TEXT SEARCH PARSER"), [CADASTRAR BUSCA DE TEXTO](sql-createtsparser.md "CREATE TEXT SEARCH PARSER")