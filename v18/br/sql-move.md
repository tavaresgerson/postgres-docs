## MOVE

MOVE — posicione um cursor

## Sinopse

```
MOVE [ direction ] [ FROM | IN ] cursor_name

where direction can be one of:

    NEXT
    PRIOR
    FIRST
    LAST
    ABSOLUTE count
    RELATIVE count
    count
    ALL
    FORWARD
    FORWARD count
    FORWARD ALL
    BACKWARD
    BACKWARD count
    BACKWARD ALL
```

## Descrição

`MOVE` reposiciona um cursor sem recuperar nenhum dado. `MOVE` funciona exatamente como o comando `FETCH`, exceto que ele apenas posiciona o cursor e não retorna linhas.

Os parâmetros para o comando `MOVE` são idênticos aos do comando `FETCH`; consulte [FETCH](sql-fetch.md "FETCH") para detalhes sobre sintaxe e uso.

## Saídas

Após a conclusão bem-sucedida, um comando `MOVE` retorna uma etiqueta de comando na forma de

```
MOVE count
```

O *`count` é o número de linhas que um comando `FETCH` com os mesmos parâmetros teria retornado (possivelmente zero).

## Exemplos

```
BEGIN WORK;
DECLARE liahona CURSOR FOR SELECT * FROM films;

-- Skip the first 5 rows:
MOVE FORWARD 5 IN liahona;
MOVE 5

-- Fetch the 6th row from the cursor liahona:
FETCH 1 FROM liahona;
 code  | title  | did | date_prod  |  kind  |  len
-------+--------+-----+------------+--------+-------
 P_303 | 48 Hrs | 103 | 1982-10-22 | Action | 01:37
(1 row)

-- Close the cursor liahona and end the transaction:
CLOSE liahona;
COMMIT WORK;
```

## Compatibilidade

Não há nenhuma declaração `MOVE` no padrão SQL.

## Veja também

[FECHAR][(sql-close.md "CLOSE"), [DECLARAÇÃO][(sql-declare.md "DECLARE"), [PESQUISA][(sql-fetch.md "FETCH")