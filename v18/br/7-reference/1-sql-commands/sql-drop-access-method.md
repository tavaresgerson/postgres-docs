## DROP MÉTODO DE ACESSO

DROP ACCESS METHOD — remova um método de acesso

## Sinopse

```
DROP ACCESS METHOD [ IF EXISTS ] name [ CASCADE | RESTRICT ]
```

## Descrição

`DROP ACCESS METHOD` remove um método de acesso existente. Apenas usuários super podem descartar métodos de acesso.

## Parâmetros

`IF EXISTS`: Não exija erro se o método de acesso não existir. Um aviso é emitido neste caso.

*`name`*: O nome de um método de acesso existente.

`CASCADE`: Descarte automaticamente os objetos que dependem do método de acesso (como as classes de operador, as famílias de operadores e os índices), e, por sua vez, todos os objetos que dependem desses objetos (consulte a [Seção 5.15](ddl-depend.md)).

`RESTRICT`: Rejeitar a eliminação do método de acesso se houver objetos que dependem dele. Esse é o padrão.

## Exemplos

Deixe o método de acesso `heptree`:

```
DROP ACCESS METHOD heptree;
```

## Compatibilidade

`DROP ACCESS METHOD` é uma extensão do PostgreSQL.

## Veja também

[Crie o método de acesso](sql-create-access-method.md "CREATE ACCESS METHOD")