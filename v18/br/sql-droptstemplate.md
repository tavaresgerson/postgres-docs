## DROP TEXT SEARCH TEMPLATE

DROP TEXT SEARCH TEMPLATE — remova um modelo de busca de texto

## Sinopse

```
DROP TEXT SEARCH TEMPLATE [ IF EXISTS ] name [ CASCADE | RESTRICT ]
```

## Descrição

`DROP TEXT SEARCH TEMPLATE` elimina um modelo de busca de texto existente. Você deve ser um superusuário para usar este comando.

## Parâmetros

`IF EXISTS`: Não exija erro se o modelo de busca de texto não existir. Neste caso, é emitido um aviso.

*`name`*: O nome (opcionalmente qualificado por esquema) de um modelo de busca de texto existente.

`CASCADE`: Descarte automaticamente os objetos que dependem do modelo de pesquisa de texto e, por sua vez, todos os objetos que dependem desses objetos (consulte [Seção 5.15](ddl-depend.md)).

`RESTRICT`: Rejeitar a eliminação do modelo de busca de texto se houver objetos que dependem dele. Isso é o padrão.

## Exemplos

Remova o modelo de busca de texto `thesaurus`:

```
DROP TEXT SEARCH TEMPLATE thesaurus;
```

Este comando não terá sucesso se houver algum dicionário de pesquisa de texto existente que utilize o modelo. Adicione `CASCADE` para descartar tais dicionários juntamente com o modelo.

## Compatibilidade

Não há nenhuma declaração `DROP TEXT SEARCH TEMPLATE` no padrão SQL.

## Veja também

[ALTERAR TEMPLATE DE PESQUISA DE TEXTO](sql-altertstemplate.md "ALTER TEXT SEARCH TEMPLATE"), [CADASTRAR TEMPLATE DE PESQUISA DE TEXTO](sql-createtstemplate.md "CREATE TEXT SEARCH TEMPLATE")