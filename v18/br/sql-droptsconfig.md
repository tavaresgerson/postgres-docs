## DROP TEXT SEARCH CONFIGURATION

DROP TEXT SEARCH CONFIGURATION — remova uma configuração de busca de texto

## Sinopse

```
DROP TEXT SEARCH CONFIGURATION [ IF EXISTS ] name [ CASCADE | RESTRICT ]
```

## Descrição

`DROP TEXT SEARCH CONFIGURATION` elimina uma configuração de pesquisa de texto existente. Para executar este comando, você deve ser o proprietário da configuração.

## Parâmetros

`IF EXISTS`: Não exija erro se a configuração de pesquisa de texto não existir. Um aviso é emitido neste caso.

*`name`*: O nome (opcionalmente qualificado por esquema) de uma configuração de busca de texto existente.

`CASCADE`: Descarte automaticamente os objetos que dependem da configuração de pesquisa de texto e, por sua vez, todos os objetos que dependem desses objetos (consulte [Seção 5.15][(ddl-depend.md "5.15. Dependency Tracking")]).

`RESTRICT`: Rejeitar a eliminação da configuração de busca de texto se algum objeto depender dela. Isso é o padrão.

## Exemplos

Remova a configuração de busca de texto `my_english`:

```
DROP TEXT SEARCH CONFIGURATION my_english;
```

Este comando não terá sucesso se houver algum índice existente que faça referência à configuração em chamadas `to_tsvector`. Adicione `CASCADE` para descartar tais índices juntamente com a configuração de pesquisa de texto.

## Compatibilidade

Não há nenhuma declaração `DROP TEXT SEARCH CONFIGURATION` no padrão SQL.

## Veja também

[ALTERAR CONFIGURAÇÃO DE PESQUISA DE TEXTO](sql-altertsconfig.md "ALTER TEXT SEARCH CONFIGURATION"), [CADASTRAR CONFIGURAÇÃO DE PESQUISA DE TEXTO](sql-createtsconfig.md "CREATE TEXT SEARCH CONFIGURATION")