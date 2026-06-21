## PREPARE

PREPARE — prepare uma declaração para execução

## Sinopse

```
PREPARE prepared_name FROM string
```

## Descrição

`PREPARE` prepara uma declaração dinamicamente especificada como uma string para execução. Isso é diferente da declaração SQL direta [PREPARE](sql-prepare.md "PREPARE"), que também pode ser usada em programas embutidos. O comando [EXECUTE](sql-execute.md "EXECUTE") é usado para executar qualquer tipo de declaração preparada.

## Parâmetros

*`prepared_name`* [#](#ECPG-SQL-PREPARE-PREPARED-NAME): Um identificador para a consulta preparada.

*`string`* [#](#ECPG-SQL-PREPARE-STRING): Uma string literal ou uma variável hospedeira que contém uma declaração SQL preparável, uma das opções SELECT, INSERT, UPDATE ou DELETE. Use pontos de interrogação (`?`) para valores de parâmetros que devem ser fornecidos na execução.

## Notas

No uso típico, o *`string`* é uma referência de variável hospedeira para uma string que contém uma declaração SQL construída dinamicamente. O caso de uma string literal não é muito útil; você pode escrever diretamente uma declaração SQL `PREPARE`.

Se você usar uma string literal, tenha em mente que quaisquer aspas duplas que você possa querer incluir na declaração SQL devem ser escritas como escapamentos octal (`\042`) e não o usual `\"` idiom C. Isso ocorre porque a string está dentro de uma seção `EXEC SQL`, então o analisador ECPG a analisa de acordo com as regras SQL e não as regras C. Qualquer barra invertida embutida será tratada posteriormente de acordo com as regras C; mas `\"` causa um erro de sintaxe imediato porque é visto como terminando a literal.

## Exemplos

```
char *stmt = "SELECT * FROM test1 WHERE a = ? AND b = ?";

EXEC SQL ALLOCATE DESCRIPTOR outdesc;
EXEC SQL PREPARE foo FROM :stmt;

EXEC SQL EXECUTE foo USING SQL DESCRIPTOR indesc INTO SQL DESCRIPTOR outdesc;
```

## Compatibilidade

`PREPARE` é especificado no padrão SQL.

## Veja também

[EXECUTE](sql-execute.md "EXECUTE")
