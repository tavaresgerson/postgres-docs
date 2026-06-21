## ABERTO

OPEN — abrir um cursor dinâmico

## Sinopse

```
OPEN cursor_name
OPEN cursor_name USING value [, ... ]
OPEN cursor_name USING SQL DESCRIPTOR descriptor_name
```

## Descrição

`OPEN` abre um cursor e, opcionalmente, vincula os valores reais aos placeholders na declaração do cursor. O cursor deve ter sido previamente declarado com o comando `DECLARE`. A execução de `OPEN` faz com que a consulta comece a ser executada no servidor.

## Parâmetros

*`cursor_name`* [#](#ECPG-SQL-OPEN-CURSOR-NAME): O nome do cursor a ser aberto. Isso pode ser um identificador SQL ou uma variável de hospedagem.

*`value`* [#](#ECPG-SQL-OPEN-VALUE): Um valor que deve ser vinculado a um localizador no cursor. Isso pode ser uma constante SQL, uma variável de host ou uma variável de host com indicador.

*`descriptor_name`* [#](#ECPG-SQL-OPEN-DESCRIPTOR-NAME): O nome de um descritor que contém os valores a serem vinculados aos marcadores no cursor. Isso pode ser um identificador SQL ou uma variável de host.

## Exemplos

```
EXEC SQL OPEN a;
EXEC SQL OPEN d USING 1, 'test';
EXEC SQL OPEN c1 USING SQL DESCRIPTOR mydesc;
EXEC SQL OPEN :curname1;
```

## Compatibilidade

`OPEN` é especificado no padrão SQL.

## Veja também

[DECLARAR](ecpg-sql-declare.md "DECLARE"), [FECHAR](sql-close.md "CLOSE")