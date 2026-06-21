## DROP TRANSFORM

DROP TRANSFORM — remover uma transformação

## Sinopse

```
DROP TRANSFORM [ IF EXISTS ] FOR type_name LANGUAGE lang_name [ CASCADE | RESTRICT ]
```

## Descrição

`DROP TRANSFORM` remove uma transformação previamente definida.

Para poder descartar uma transformação, você deve possuir o tipo e a linguagem. Esses são os mesmos privilégios que são necessários para criar uma transformação.

## Parâmetros

`IF EXISTS`: Não exija erro se a transformação não existir. Um aviso é emitido neste caso.

*`type_name`*: O nome do tipo de dados do transformador.

*`lang_name`*: O nome da língua do transformado.

`CASCADE`: Descarte automaticamente os objetos que dependem da transformação e, por sua vez, todos os objetos que dependem desses objetos (consulte [Seção 5.15][(ddl-depend.md "5.15. Dependency Tracking")]).

`RESTRICT`: Recusar a eliminação do transformador se qualquer objeto depender dele. Esse é o padrão.

## Exemplos

Para descartar a transformação para o tipo `hstore` e idioma `plpython3u`:

```
DROP TRANSFORM FOR hstore LANGUAGE plpython3u;
```

## Compatibilidade

Essa forma de `DROP TRANSFORM` é uma extensão do PostgreSQL. Consulte [CREATE TRANSFORM](sql-createtransform.md "CREATE TRANSFORM") para obter detalhes.

## Veja também

[Crie Transformação](sql-createtransform.md "CREATE TRANSFORM")