## TYPE

TYPE — definir um novo tipo de dados

## Sinopse

```
TYPE type_name IS ctype
```

## Descrição

O comando `TYPE` define um novo tipo C. É equivalente a colocar um `typedef` em uma seção de declaração.

Este comando é reconhecido apenas quando `ecpg` é executado com a opção `-c`.

## Parâmetros

*`type_name`* [#](#ECPG-SQL-TYPE-TYPE-NAME): O nome para o novo tipo. Deve ser um nome válido de tipo C.

*`ctype`* [#](#ECPG-SQL-TYPE-CTYPE): Uma especificação do tipo C.

## Exemplos

```
EXEC SQL TYPE customer IS
    struct
    {
        varchar name[50];
        int     phone;
    };

EXEC SQL TYPE cust_ind IS
    struct ind
    {
        short   name_ind;
        short   phone_ind;
    };

EXEC SQL TYPE c IS char reference;
EXEC SQL TYPE ind IS union { int integer; short smallint; };
EXEC SQL TYPE intarray IS int[AMOUNT];
EXEC SQL TYPE str IS varchar[BUFFERSIZ];
EXEC SQL TYPE string IS char[11];
```

Aqui está um exemplo de programa que utiliza `EXEC SQL TYPE`:

```
EXEC SQL WHENEVER SQLERROR SQLPRINT;

EXEC SQL TYPE tt IS
    struct
    {
        varchar v[256];
        int     i;
    };

EXEC SQL TYPE tt_ind IS
    struct ind {
        short   v_ind;
        short   i_ind;
    };

int
main(void)
{
EXEC SQL BEGIN DECLARE SECTION;
    tt t;
    tt_ind t_ind;
EXEC SQL END DECLARE SECTION;

    EXEC SQL CONNECT TO testdb AS con1;
    EXEC SQL SELECT pg_catalog.set_config('search_path', '', false); EXEC SQL COMMIT;

    EXEC SQL SELECT current_database(), 256 INTO :t:t_ind LIMIT 1;

    printf("t.v = %s\n", t.v.arr);
    printf("t.i = %d\n", t.i);

    printf("t_ind.v_ind = %d\n", t_ind.v_ind);
    printf("t_ind.i_ind = %d\n", t_ind.i_ind);

    EXEC SQL DISCONNECT con1;

    return 0;
}
```

A saída deste programa é a seguinte:

```
t.v = testdb
t.i = 256
t_ind.v_ind = 0
t_ind.i_ind = 0
```

## Compatibilidade

O comando `TYPE` é uma extensão do PostgreSQL.