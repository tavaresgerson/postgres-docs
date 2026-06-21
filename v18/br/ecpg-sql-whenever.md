## QUANDO

QUANDO — especifique a ação a ser tomada quando uma declaração SQL causa a ocorrência de uma condição específica de classe

## Sinopse

```
WHENEVER { NOT FOUND | SQLERROR | SQLWARNING } action
```

## Descrição

Defina um comportamento que é chamado nos casos especiais (linhas não encontradas, avisos ou erros SQL) no resultado da execução do SQL.

## Parâmetros

Veja [Seção 34.8.1][(ecpg-errors.md#ECPG-WHENEVER "34.8.1. Setting Callbacks")] para uma descrição dos parâmetros.

## Exemplos

```
EXEC SQL WHENEVER NOT FOUND CONTINUE;
EXEC SQL WHENEVER NOT FOUND DO BREAK;
EXEC SQL WHENEVER NOT FOUND DO CONTINUE;
EXEC SQL WHENEVER SQLWARNING SQLPRINT;
EXEC SQL WHENEVER SQLWARNING DO warn();
EXEC SQL WHENEVER SQLERROR sqlprint;
EXEC SQL WHENEVER SQLERROR CALL print2();
EXEC SQL WHENEVER SQLERROR DO handle_error("select");
EXEC SQL WHENEVER SQLERROR DO sqlnotice(NULL, NONO);
EXEC SQL WHENEVER SQLERROR DO sqlprint();
EXEC SQL WHENEVER SQLERROR GOTO error_label;
EXEC SQL WHENEVER SQLERROR STOP;
```

Uma aplicação típica é o uso de `WHENEVER NOT FOUND BREAK` para lidar com o loopeamento de conjuntos de resultados:

```
int
main(void)
{
    EXEC SQL CONNECT TO testdb AS con1;
    EXEC SQL SELECT pg_catalog.set_config('search_path', '', false); EXEC SQL COMMIT;
    EXEC SQL ALLOCATE DESCRIPTOR d;
    EXEC SQL DECLARE cur CURSOR FOR SELECT current_database(), 'hoge', 256;
    EXEC SQL OPEN cur;

    /* when end of result set reached, break out of while loop */
    EXEC SQL WHENEVER NOT FOUND DO BREAK;

    while (1)
    {
        EXEC SQL FETCH NEXT FROM cur INTO SQL DESCRIPTOR d;
        ...
    }

    EXEC SQL CLOSE cur;
    EXEC SQL COMMIT;

    EXEC SQL DEALLOCATE DESCRIPTOR d;
    EXEC SQL DISCONNECT ALL;

    return 0;
}
```

## Compatibilidade

`WHENEVER` é especificado no padrão SQL, mas a maioria das ações são extensões do PostgreSQL.