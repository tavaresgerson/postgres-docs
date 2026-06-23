## EXECUTE IMMEDIATE

EXECUTE IMMEDIATE — prepare e execute dinamicamente uma declaração

## Sinopse

```
EXECUTE IMMEDIATE string
```

## Descrição

`EXECUTE IMMEDIATE` prepara e executa imediatamente uma declaração SQL dinamicamente especificada, sem recuperar linhas de resultado.

## Parâmetros

*`string`* [#](#ECPG-SQL-EXECUTE-IMMEDIATE-STRING): Uma string literal ou uma variável hospedeira que contém a declaração SQL a ser executada.

## Notas

No uso típico, o *`string`* é uma referência de variável hospedeira para uma string que contém uma declaração SQL construída dinamicamente. O caso de uma string literal não é muito útil; você pode escrever a declaração SQL diretamente, sem a digitação extra de `EXECUTE IMMEDIATE`.

Se você usar uma string literal, tenha em mente que quaisquer aspas duplas que você possa querer incluir na declaração SQL devem ser escritas como escapamentos octal (`\042`) e não o usual `\"` idiom C. Isso ocorre porque a string está dentro de uma seção `EXEC SQL`, então o analisador ECPG a analisa de acordo com as regras SQL e não as regras C. Qualquer barra invertida embutida será tratada posteriormente de acordo com as regras C; mas `\"` causa um erro de sintaxe imediato porque é visto como terminando a literal.

## Exemplos

Aqui está um exemplo que executa uma declaração `INSERT` usando `EXECUTE IMMEDIATE` e uma variável hospedeira chamada `command`:

```
sprintf(command, "INSERT INTO test (name, amount, letter) VALUES ('db: ''r1''', 1, 'f')");
EXEC SQL EXECUTE IMMEDIATE :command;
```

## Compatibilidade

`EXECUTE IMMEDIATE` é especificado no padrão SQL.