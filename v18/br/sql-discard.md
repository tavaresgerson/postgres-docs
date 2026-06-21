## DESCARTE

DISCARD — descarte do estado da sessão

## Sinopse

```
DISCARD { ALL | PLANS | SEQUENCES | TEMPORARY | TEMP }
```

## Descrição

`DISCARD` libera recursos internos associados a uma sessão de banco de dados. Esse comando é útil para redefinir parcialmente ou totalmente o estado da sessão. Existem vários subcomandos para liberar diferentes tipos de recursos; a variante `DISCARD ALL` engloba todos os outros, e também redefere estado adicional.

## Parâmetros

`PLANS`: Libera todos os planos de consulta cacheados, forçando a re-planejamento a ocorrer na próxima vez que a declaração preparada associada for usada.

`SEQUENCES`: Descarte todos os estados relacionados a sequência cacheados, incluindo as informações `currval()`/`lastval()` e quaisquer valores de sequência pré-alocados que ainda não tenham sido retornados por `nextval()`. (Consulte [CREATE SEQUENCE](sql-createsequence.md "CREATE SEQUENCE") para uma descrição dos valores de sequência pré-alocados.)

`TEMPORARY` ou `TEMP`: Exclui todas as tabelas temporárias criadas na sessão atual.

`ALL`: Libera todos os recursos temporários associados à sessão atual e refaz a sessão ao seu estado inicial. Atualmente, isso tem o mesmo efeito que executar a seguinte sequência de instruções:

``` CLOSE ALL; SET SESSION AUTHORIZATION DEFAULT; RESET ALL; DEALLOCATE ALL; UNLISTEN *; SELECT pg_advisory_unlock_all(); DISCARD PLANS; DISCARD TEMP; DISCARD SEQUENCES;
    ```

## Notas

`DISCARD ALL` não pode ser executado dentro de um bloco de transação.

## Compatibilidade

`DISCARD` é uma extensão do PostgreSQL.