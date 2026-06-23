## DROP CONVERSION

DROP CONVERSION — remova uma conversão

## Sinopse

```
DROP CONVERSION [ IF EXISTS ] name [ CASCADE | RESTRICT ]
```

## Descrição

`DROP CONVERSION` remove uma conversão previamente definida. Para poder descartar uma conversão, você deve possuir a conversão.

## Parâmetros

`IF EXISTS`: Não exija erro se a conversão não existir. Neste caso, é emitido um aviso.

*`name`*: O nome da conversão. O nome da conversão pode ser qualificado por esquema.

`CASCADE` `RESTRICT`: Essas palavras-chave não têm efeito, uma vez que não há dependências em conversões.

## Exemplos

Para descartar a conversão chamada `myname`:

```
DROP CONVERSION myname;
```

## Compatibilidade

Não há uma declaração `DROP CONVERSION` no padrão SQL, mas uma declaração `DROP TRANSLATION` que acompanha a declaração `CREATE TRANSLATION`, que é semelhante à declaração `CREATE CONVERSION` no PostgreSQL.

## Veja também

[ALTERAR CONVERSÃO](sql-alterconversion.md "ALTER CONVERSION"), [CADASTRAR CONVERSÃO](sql-createconversion.md "CREATE CONVERSION")