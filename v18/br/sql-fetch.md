## FETCH

FETCH — recuperar linhas de uma consulta usando um cursor

## Sinopse

```
FETCH [ direction ] [ FROM | IN ] cursor_name

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

`FETCH` recupera linhas usando um cursor criado anteriormente.

Um cursor tem uma posição associada, que é usada por `FETCH`. A posição do cursor pode ser antes da primeira linha do resultado da consulta, em qualquer linha específica do resultado ou após a última linha do resultado. Quando criado, um cursor é posicionado antes da primeira linha. Após obter algumas linhas, o cursor é posicionado na linha mais recentemente recuperada. Se `FETCH` sair do final das linhas disponíveis, então o cursor é deixado posicionado após a última linha, ou antes da primeira linha se a recuperação for em sentido inverso. `FETCH ALL` ou `FETCH BACKWARD ALL` sempre deixarão o cursor posicionado após a última linha ou antes da primeira linha.

Os formulários `NEXT`, `PRIOR`, `FIRST`, `LAST`, `ABSOLUTE`, `RELATIVE` obtêm uma única linha após mover o cursor de forma apropriada. Se não houver tal linha, é retornado um resultado vazio e o cursor é deixado posicionado antes da primeira linha ou após a última linha, conforme apropriado.

Os formulários que utilizam `FORWARD` e `BACKWARD` recuperam o número indicado de linhas que se movem na direção para a frente ou para trás, deixando o cursor posicionado na última linha devolvida (ou após/antes de todas as linhas, se o *`count`* exceder o número de linhas disponíveis).

`RELATIVE 0`, `FORWARD 0` e `BACKWARD 0` solicitam que a linha atual seja recuperada sem mover o cursor, ou seja, que a linha mais recentemente recuperada seja refeita. Isso será bem-sucedido, a menos que o cursor esteja posicionado antes da primeira linha ou após a última linha; nesse caso, nenhuma linha é devolvida.

### Nota

Esta página descreve o uso de cursor no nível do comando SQL. Se você está tentando usar cursors dentro de uma função PL/pgSQL, as regras são diferentes — veja [Seção 41.7.3][(plpgsql-cursors.md#PLPGSQL-CURSOR-USING "41.7.3. Using Cursors")].

## Parâmetros

*`direction`*: *`direction`* define a direção de busca e o número de linhas a serem buscadas. Pode ser um dos seguintes:

`NEXT` :   Pegue a próxima linha. Este é o padrão se *`direction`* for omitido.

`PRIOR` :   Pegue a linha anterior.

`FIRST` :   Pegue a primeira linha da consulta (mesma que `ABSOLUTE 1`).

`LAST` :   Pegue a última linha da consulta (mesma que `ABSOLUTE -1`).

`ABSOLUTE count` :   Pegue a *`count`'ª linha da consulta, ou a `abs(count)`'ª linha da última se *`count`* for negativo. Posicione antes da primeira linha ou após a última linha se *`count`* estiver fora do intervalo; em particular, `ABSOLUTE 0` posiciona antes da primeira linha.

`RELATIVE count` :   Pegue a *`count`'ª linha subsequente, ou a `abs(count)`'ª linha anterior, se *`count`* for negativo. `RELATIVE 0` refaz a linha atual, se houver.

*`count`* :   Pegue as próximas *`count`* linhas (mesma que `FORWARD count`).

`ALL` :   Pegue todas as linhas restantes (mesma coisa que `FORWARD ALL`).

`FORWARD` :   Pegue a próxima linha (mesma que `NEXT`).

`FORWARD count` :   Pegue as próximas linhas *`count`*. A `FORWARD 0` refaz a linha atual.

`FORWARD ALL` :   Pegue todas as linhas restantes.

`BACKWARD` :   Pegue a linha anterior (mesma que `PRIOR`).

`BACKWARD count` :   Pegue as linhas anteriores *`count`* (pesquisando para trás). `BACKWARD 0` refaz a linha atual.

`BACKWARD ALL` :   Pegue todas as linhas anteriores (pesquisando para trás).

*`count`*: *`count`* é uma constante de inteiro possivelmente assinada, que determina a localização ou o número de linhas a serem recuperadas. Nos casos de `FORWARD` e `BACKWARD`, especificar um *`count`* negativo é equivalente a mudar o sentido de `FORWARD` e `BACKWARD`.

*`cursor_name`*: Nome do cursor aberto.

## Saídas

Após a conclusão bem-sucedida, um comando `FETCH` retorna uma etiqueta de comando na forma de

```
FETCH count
```

O *`count`* é o número de linhas recuperadas (possivelmente zero). Observe que, no psql, o rótulo do comando não será exibido na verdade, pois o psql exibe as linhas recuperadas.

## Notas

O cursor deve ser declarado com a opção `SCROLL` se se pretende usar quaisquer variantes do `FETCH` que não sejam `FETCH NEXT` ou `FETCH FORWARD` com um contagem positiva. Para consultas simples, o PostgreSQL permitirá a recuperação reversa a partir de cursors não declarados com `SCROLL`, mas esse comportamento não deve ser confiado. Se o cursor for declarado com `NO SCROLL`, nenhuma recuperação reversa será permitida.

As consultas `ABSOLUTE` não são mais rápidas do que navegar até a linha desejada com um movimento relativo: a implementação subjacente deve percorrer todas as linhas intermediárias de qualquer maneira. As consultas absolutas negativas são ainda piores: a consulta deve ser lida até o final para encontrar a última linha, e então percorrida para trás a partir daí. No entanto, voltar ao início da consulta (como com `FETCH ABSOLUTE 0`) é rápido.

`DECLARE` é usado para definir um cursor. Use `MOVE` para alterar a posição do cursor sem recuperar dados.

## Exemplos

O exemplo a seguir percorre uma tabela usando um cursor:

```
BEGIN WORK;

-- Set up a cursor:
DECLARE liahona SCROLL CURSOR FOR SELECT * FROM films;

-- Fetch the first 5 rows in the cursor liahona:
FETCH FORWARD 5 FROM liahona;

 code  |          title          | did | date_prod  |   kind   |  len
-------+-------------------------+-----+------------+----------+-------
 BL101 | The Third Man           | 101 | 1949-12-23 | Drama    | 01:44
 BL102 | The African Queen       | 101 | 1951-08-11 | Romantic | 01:43
 JL201 | Une Femme est une Femme | 102 | 1961-03-12 | Romantic | 01:25
 P_301 | Vertigo                 | 103 | 1958-11-14 | Action   | 02:08
 P_302 | Becket                  | 103 | 1964-02-03 | Drama    | 02:28

-- Fetch the previous row:
FETCH PRIOR FROM liahona;

 code  |  title  | did | date_prod  |  kind  |  len
-------+---------+-----+------------+--------+-------
 P_301 | Vertigo | 103 | 1958-11-14 | Action | 02:08

-- Close the cursor and end the transaction:
CLOSE liahona;
COMMIT WORK;
```

## Compatibilidade

O padrão SQL define `FETCH` para uso apenas em SQL embutido. A variante de `FETCH` descrita aqui retorna os dados como se fossem um resultado de `SELECT`, em vez de colocá-los em variáveis hostis. Além deste ponto, `FETCH` é totalmente compatível em relação ao padrão SQL.

Os formulários `FETCH` que envolvem `FORWARD` e `BACKWARD`, bem como os formulários `FETCH count` e `FETCH ALL`, nos quais `FORWARD` é implícito, são extensões do PostgreSQL.

O padrão SQL permite apenas `FROM` antes do nome do cursor; a opção de usar `IN`, ou de deixá-los de fora, é uma extensão.

## Veja também

[FECHAR][(sql-close.md "CLOSE"), [DECLARAÇÃO][(sql-declare.md "DECLARE"), [MOVIMENTO][(sql-move.md "MOVE")