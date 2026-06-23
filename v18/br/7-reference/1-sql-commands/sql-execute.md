## EXECUTE

EXECUTE — executar uma declaração preparada

## Sinopse

```
EXECUTE name [ ( parameter [, ...] ) ]
```

## Descrição

`EXECUTE` é usado para executar uma declaração previamente preparada. Como as declarações preparadas existem apenas durante a duração de uma sessão, a declaração preparada deve ter sido criada por uma declaração `PREPARE` executada anteriormente na sessão atual.

Se a declaração `PREPARE` que criou a declaração especificar alguns parâmetros, um conjunto compatível de parâmetros deve ser passado para a declaração `EXECUTE`, caso contrário, um erro é exibido. Observe que (ao contrário das funções) as declarações preparadas não são sobrecarregadas com base no tipo ou no número de seus parâmetros; o nome de uma declaração preparada deve ser único dentro de uma sessão do banco de dados.

Para mais informações sobre a criação e o uso de declarações preparadas, consulte [PREPARE](sql-prepare.md).

## Parâmetros

*`name`*: O nome do comunicado preparado a ser executado.

*`parameter`*: O valor real de um parâmetro para a declaração preparada. Isso deve ser uma expressão que produza um valor compatível com o tipo de dados deste parâmetro, conforme determinado quando a declaração preparada foi criada.

## Saídas

O rótulo de comando retornado por `EXECUTE` é o da declaração preparada, e não `EXECUTE`.

## Exemplos

Exemplos são fornecidos em [Exemplos](sql-prepare.md#SQL-PREPARE-EXAMPLES "Examples") na documentação do [PREPARE](sql-prepare.md "PREPARE").

## Compatibilidade

O padrão SQL inclui uma declaração `EXECUTE`, mas ela só deve ser usada em SQL embutido. Esta versão da declaração `EXECUTE` também usa uma sintaxe um pouco diferente.

## Veja também

[DEALLOCATE](sql-deallocate.md "DEALLOCATE"), [PREPARE](sql-prepare.md "PREPARE")