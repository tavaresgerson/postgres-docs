## DICA DE PESQUISA DE TEXTO EM DICOTONIA

DROP TEXT SEARCH DICTIONARY — remova um dicionário de busca de texto

## Sinopse

```
DROP TEXT SEARCH DICTIONARY [ IF EXISTS ] name [ CASCADE | RESTRICT ]
```

## Descrição

`DROP TEXT SEARCH DICTIONARY` descarta um dicionário de pesquisa de texto existente. Para executar este comando, você deve ser o proprietário do dicionário.

## Parâmetros

`IF EXISTS`: Não exija erro se o dicionário de pesquisa de texto não existir. Um aviso é emitido neste caso.

*`name`*: O nome (opcionalmente qualificado por esquema) de um dicionário de pesquisa de texto existente.

`CASCADE`: Descarte automaticamente os objetos que dependem do dicionário de pesquisa de texto e, por sua vez, todos os objetos que dependem desses objetos (consulte [Seção 5.15][(ddl-depend.md "5.15. Dependency Tracking")]).

`RESTRICT`: Rejeitar a eliminação do dicionário de busca de texto se algum objeto depender dele. Isso é o padrão.

## Exemplos

Remova o dicionário de busca de texto `english`:

```
DROP TEXT SEARCH DICTIONARY english;
```

Este comando não terá sucesso se houver alguma configuração de busca de texto existente que utilize o dicionário. Adicione `CASCADE` para descartar tais configurações juntamente com o dicionário.

## Compatibilidade

Não há nenhuma declaração `DROP TEXT SEARCH DICTIONARY` no padrão SQL.

## Veja também

[ALTERAR Dicionário de PESQUISA DE TEXTO](sql-altertsdictionary.md "ALTER TEXT SEARCH DICTIONARY"), [Criação de Dicionário de PESQUISA DE TEXTO](sql-createtsdictionary.md "CREATE TEXT SEARCH DICTIONARY")