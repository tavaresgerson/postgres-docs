## DROP PUBLICATION

DROP PUBLICATION — remover uma publicação

## Sinopse

```
DROP PUBLICATION [ IF EXISTS ] name [, ...] [ CASCADE | RESTRICT ]
```

## Descrição

`DROP PUBLICATION` remove uma publicação existente do banco de dados.

Uma publicação só pode ser excluída pelo seu proprietário ou por um superusuário.

## Parâmetros

`IF EXISTS`: Não exija erro se a publicação não existir. Um aviso é emitido neste caso.

*`name`*: O nome de uma publicação existente.

`CASCADE` `RESTRICT`: Essas palavras-chave não têm efeito, uma vez que não há dependências em publicações.

## Exemplos

Deixe uma publicação:

```
DROP PUBLICATION mypublication;
```

## Compatibilidade

`DROP PUBLICATION` é uma extensão do PostgreSQL.

## Veja também

[CADASTRAR PUBLICAÇÃO](sql-createpublication.md "CREATE PUBLICATION"), [ALTERAR PUBLICAÇÃO](sql-alterpublication.md "ALTER PUBLICATION")