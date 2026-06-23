## 34.12. Objetos grandes [#](#ECPG-LO)

Os grandes objetos não são diretamente suportados pelo ECPG, mas a aplicação do ECPG pode manipular grandes objetos através das funções de objeto grande da libpq, obtendo o objeto necessário `PGconn` chamando a função `ECPGget_PGconn()`. (No entanto, o uso da função `ECPGget_PGconn()` e o toque em objetos `PGconn` diretamente deve ser feito com muito cuidado e, idealmente, não misturado com outras chamadas de acesso ao banco de dados do ECPG.)

Para mais detalhes sobre o `ECPGget_PGconn()`, consulte [Seção 34.11](ecpg-library.md). Para informações sobre a interface de função de objeto grande, consulte [Capítulo 33](largeobjects.md).

Funções de objeto grande devem ser chamadas em um bloco de transação, portanto, quando o autocommit está desativado, os comandos `BEGIN` devem ser emitidos explicitamente.

[Exemplo 34.2](ecpg-lo.md#ECPG-LO-EXAMPLE) mostra um programa exemplo que ilustra como criar, escrever e ler um objeto grande em uma aplicação ECPG.

**Exemplo 34.2. Acesso ao Programa ECPG a Objetos Grandes**

```
#include <stdio.h>
#include <stdlib.h>
#include <libpq-fe.h>
#include <libpq/libpq-fs.h>

EXEC SQL WHENEVER SQLERROR STOP;

int
main(void)
{
    PGconn     *conn;
    Oid         loid;
    int         fd;
    char        buf[256];
    int         buflen = 256;
    char        buf2[256];
    int         rc;

    memset(buf, 1, buflen);

    EXEC SQL CONNECT TO testdb AS con1;
    EXEC SQL SELECT pg_catalog.set_config('search_path', '', false); EXEC SQL COMMIT;

    conn = ECPGget_PGconn("con1");
    printf("conn = %p\n", conn);

    /* create */
    loid = lo_create(conn, 0);
    if (loid &lt; 0)
        printf("lo_create() failed: %s", PQerrorMessage(conn));

    printf("loid = %d\n", loid);

    /* write test */
    fd = lo_open(conn, loid, INV_READ|INV_WRITE);
    if (fd &lt; 0)
        printf("lo_open() failed: %s", PQerrorMessage(conn));

    printf("fd = %d\n", fd);

    rc = lo_write(conn, fd, buf, buflen);
    if (rc &lt; 0)
        printf("lo_write() failed\n");

    rc = lo_close(conn, fd);
    if (rc &lt; 0)
        printf("lo_close() failed: %s", PQerrorMessage(conn));

    /* read test */
    fd = lo_open(conn, loid, INV_READ);
    if (fd &lt; 0)
        printf("lo_open() failed: %s", PQerrorMessage(conn));

    printf("fd = %d\n", fd);

    rc = lo_read(conn, fd, buf2, buflen);
    if (rc &lt; 0)
        printf("lo_read() failed\n");

    rc = lo_close(conn, fd);
    if (rc &lt; 0)
        printf("lo_close() failed: %s", PQerrorMessage(conn));

    /* check */
    rc = memcmp(buf, buf2, buflen);
    printf("memcmp() = %d\n", rc);

    /* cleanup */
    rc = lo_unlink(conn, loid);
    if (rc &lt; 0)
        printf("lo_unlink() failed: %s", PQerrorMessage(conn));

    EXEC SQL COMMIT;
    EXEC SQL DISCONNECT ALL;
    return 0;
}
```
