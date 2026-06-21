## CHAMADA

CHAMADA — invoque um procedimento

## Sinopse

```
CALL name ( [ argument ] [, ...] )
```

## Descrição

`CALL` executa um procedimento.

Se o procedimento tiver algum parâmetro de saída, então uma linha de resultado será retornada, contendo os valores desses parâmetros.

## Parâmetros

*`name`*: O nome (opcionalmente qualificado por esquema) do procedimento.

*`argument`*: Uma expressão de argumento para a chamada do procedimento.

Os argumentos podem incluir nomes de parâmetros, usando a sintaxe `name => value`. Isso funciona da mesma forma que em chamadas de função comuns; consulte [Seção 4.3][(sql-syntax-calling-funcs.md "4.3. Calling Functions")] para detalhes.

Os argumentos devem ser fornecidos para todos os parâmetros do procedimento que não possuem valores padrão, incluindo os parâmetros `OUT`. No entanto, os argumentos que correspondem aos parâmetros `OUT` não são avaliados, portanto, é comum apenas escrever `NULL` para eles. (Escrever algo diferente para um parâmetro `OUT` pode causar problemas de compatibilidade com futuras versões do PostgreSQL.)

## Notas

O usuário deve ter o privilégio `EXECUTE` no procedimento para que seja permitido invocá-lo.

Para chamar uma função (não um procedimento), use `SELECT` em vez disso.

Se `CALL` for executado em um bloco de transação, então o procedimento chamado não pode executar instruções de controle de transação. As instruções de controle de transação só são permitidas se `CALL` for executado em sua própria transação.

O PL/pgSQL lida com os parâmetros de saída nos comandos `CALL` de maneira diferente; veja [Seção 41.6.3][(plpgsql-control-structures.md#PLPGSQL-STATEMENTS-CALLING-PROCEDURE "41.6.3. Calling a Procedure")].

## Exemplos

```
CALL do_db_maintenance();
```

## Compatibilidade

`CALL` está de acordo com o padrão SQL, exceto pelo tratamento dos parâmetros de saída. O padrão diz que os usuários devem escrever variáveis para receber os valores dos parâmetros de saída.

## Veja também

[Crie procedimento](sql-createprocedure.md "CREATE PROCEDURE")