## DESCRIÇÃO DO SETE

DESCRIÇÃO DO SET — informações do conjunto em uma área de descritor SQL

## Sinopse

```
SET DESCRIPTOR descriptor_name descriptor_header_item = value [, ... ]
SET DESCRIPTOR descriptor_name VALUE number descriptor_item = value [, ...]
```

## Descrição

`SET DESCRIPTOR` popula uma área de descritor SQL com valores. A área de descritor é então, normalmente, usada para vincular parâmetros em uma execução de consulta preparada.

Este comando tem duas formas: A primeira forma se aplica ao descritor "cabeçalho", que é independente de um dado específico. A segunda forma atribui valores a dados específicos, identificados por número.

## Parâmetros

*`descriptor_name`* [#](#ECPG-SQL-SET-DESCRIPTOR-DESCRIPTOR-NAME): Um nome de descritor.

*`descriptor_header_item`* [#](#ECPG-SQL-SET-DESCRIPTOR-DESCRIPTOR-HEADER-ITEM): Um identificador que indica qual item de informação de cabeçalho deve ser definido. Apenas `COUNT`, para definir o número de itens de descritor, é atualmente suportado.

*`number`* [#](#ECPG-SQL-SET-DESCRIPTOR-NUMBER): O número do item do descritor a ser definido. A contagem começa em 1.

*`descriptor_item`* [#](#ECPG-SQL-SET-DESCRIPTOR-DESCRIPTOR-ITEM): Um token que identifica qual item de informação deve ser definido no descritor. Consulte [Seção 34.7.1](ecpg-descriptors.md#ECPG-NAMED-DESCRIPTORS "34.7.1. Named SQL Descriptor Areas") para uma lista de itens suportados.

*`value`* [#](#ECPG-SQL-SET-DESCRIPTOR-VALUE): Um valor para armazenar no item do descritor. Isso pode ser uma constante SQL ou uma variável do host.

## Exemplos

```
EXEC SQL SET DESCRIPTOR indesc COUNT = 1;
EXEC SQL SET DESCRIPTOR indesc VALUE 1 DATA = 2;
EXEC SQL SET DESCRIPTOR indesc VALUE 1 DATA = :val1;
EXEC SQL SET DESCRIPTOR indesc VALUE 2 INDICATOR = :val1, DATA = 'some string';
EXEC SQL SET DESCRIPTOR indesc VALUE 2 INDICATOR = :val2null, DATA = :val2;
```

## Compatibilidade

`SET DESCRIPTOR` é especificado no padrão SQL.

## Veja também

(ecpg-sql-allocate-descriptor.md "ALLOCATE DESCRIPTOR"), (ecpg-sql-get-descriptor.md "GET DESCRIPTOR")