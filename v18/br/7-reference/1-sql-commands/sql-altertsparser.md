## ALTER TEXT SEARCH PARSER

ALTERAR O PESQUISA DE TEXTO PARSER — alterar a definição de um parser de pesquisa de texto

## Sinopse

```
ALTER TEXT SEARCH PARSER name RENAME TO new_name
ALTER TEXT SEARCH PARSER name SET SCHEMA new_schema
```

## Descrição

`ALTER TEXT SEARCH PARSER` altera a definição de um analisador de pesquisa de texto. Atualmente, a única funcionalidade compatível é a de alterar o nome do analisador.

Você deve ser um superusuário para usar `ALTER TEXT SEARCH PARSER`.

## Parâmetros

*`name`*: O nome (opcionalmente qualificado por esquema) de um analisador de busca de texto existente.

*`new_name`*: O novo nome do analisador de busca de texto.

*`new_schema`*: O novo esquema para o analisador de busca de texto.

## Compatibilidade

Não há nenhuma declaração `ALTER TEXT SEARCH PARSER` no padrão SQL.

## Veja também

[CRIAR PARSETOR DE PESQUISA DE TEXTO](sql-createtsparser.md "CREATE TEXT SEARCH PARSER"), [DROP PARSETOR DE PESQUISA DE TEXTO](sql-droptsparser.md "DROP TEXT SEARCH PARSER")