## ALTERAR TEMPLATE DE PESQUISA DE TEXTO

ALTERAR TEMPLATE DE PESQUISA DE TEXTO — alterar a definição de um modelo de pesquisa de texto

## Sinopse

```
ALTER TEXT SEARCH TEMPLATE name RENAME TO new_name
ALTER TEXT SEARCH TEMPLATE name SET SCHEMA new_schema
```

## Descrição

`ALTER TEXT SEARCH TEMPLATE` altera a definição de um modelo de busca de texto. Atualmente, a única funcionalidade compatível é a de alterar o nome do modelo.

Você deve ser um superusuário para usar `ALTER TEXT SEARCH TEMPLATE`.

## Parâmetros

*`name`*: O nome (opcionalmente qualificado por esquema) de um modelo de busca de texto existente.

*`new_name`*: O novo nome do modelo de busca de texto.

*`new_schema`*: O novo esquema para o modelo de busca de texto.

## Compatibilidade

Não há nenhuma declaração `ALTER TEXT SEARCH TEMPLATE` no padrão SQL.

## Veja também

[Crie um modelo de busca de texto](sql-createtstemplate.md "CREATE TEXT SEARCH TEMPLATE"), [Remova o modelo de busca de texto](sql-droptstemplate.md "DROP TEXT SEARCH TEMPLATE")