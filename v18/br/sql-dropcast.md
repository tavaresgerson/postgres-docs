## DROP CAST

DROP CAST — remover um elenco

## Sinopse

```
DROP CAST [ IF EXISTS ] (source_type AS target_type) [ CASCADE | RESTRICT ]
```

## Descrição

`DROP CAST` remove um molde previamente definido.

Para poder descartar um cast, você deve possuir o tipo de dados fonte ou alvo. Esses são os mesmos privilégios que são necessários para criar um cast.

## Parâmetros

`IF EXISTS`: Não exija erro se o elenco não existir. Neste caso, é emitido um aviso.

*`source_type`*: O nome do tipo de dados fonte do cast.

*`target_type`*: O nome do tipo de dados de destino do cast.

`CASCADE` `RESTRICT`: Essas palavras-chave não têm efeito, uma vez que não há dependências em casts.

## Exemplos

Para descartar o elenco do tipo `text` para o tipo `int`:

```
DROP CAST (text AS int);
```

## Compatibilidade

O comando `DROP CAST` está de acordo com o padrão SQL.

## Veja também

[Crie uma nova classe](sql-createcast.md "CREATE CAST")