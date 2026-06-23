## VAR

VAR — definir uma variável

## Sinopse

```
VAR varname IS ctype
```

## Descrição

O comando `VAR` atribui um novo tipo de dados C a uma variável de host. A variável de host deve ser previamente declarada em uma seção declare.

## Parâmetros

*`varname`* [#](#ECPG-SQL-VAR-VARNAME): Um nome de variável C.

*`ctype`* [#](#ECPG-SQL-VAR-CTYPE): Uma especificação do tipo C.

## Exemplos

```
Exec sql begin declare section;
short a;
exec sql end declare section;
EXEC SQL VAR a IS int;
```

## Compatibilidade

O comando `VAR` é uma extensão do PostgreSQL.