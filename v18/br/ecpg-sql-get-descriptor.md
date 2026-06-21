## GET DESCRIPTOR

GET DESCRIPTOR — obter informações de uma área de descriptografia SQL

## Sinopse

```
GET DESCRIPTOR descriptor_name :cvariable = descriptor_header_item [, ... ]
GET DESCRIPTOR descriptor_name VALUE column_number :cvariable = descriptor_item [, ... ]
```

## Descrição

`GET DESCRIPTOR` recupera informações sobre um conjunto de resultados de consulta de uma área de descritor SQL e as armazena em variáveis do host. Uma área de descritor é tipicamente preenchida usando `FETCH` ou `SELECT` antes de usar este comando para transferir as informações para variáveis em linguagem do host.

Este comando tem duas formas: A primeira forma recupera itens do descritor “cabeçalho”, que se aplica ao conjunto de resultados na íntegra. Um exemplo é o número de linhas. A segunda forma, que requer o número da coluna como parâmetro adicional, recupera informações sobre uma coluna específica. Exemplos são o nome da coluna e o valor real da coluna.

## Parâmetros

*`descriptor_name`* [#](#ECPG-SQL-GET-DESCRIPTOR-DESCRIPTOR-NAME): Um nome de descritor.

*`descriptor_header_item`* [#](#ECPG-SQL-GET-DESCRIPTOR-DESCRIPTOR-HEADER-ITEM): Um token que identifica qual item de informação de cabeçalho deve ser recuperado. Apenas `COUNT`, para obter o número de colunas no conjunto de resultados, é atualmente suportado.

*`column_number`* [#](#ECPG-SQL-GET-DESCRIPTOR-COLUMN-NUMBER): O número da coluna sobre a qual as informações devem ser recuperadas. A contagem começa em 1.

*`descriptor_item`* [#](#ECPG-SQL-GET-DESCRIPTOR-DESCRIPTOR-ITEM): Um token que identifica qual item de informação sobre uma coluna deve ser recuperado. Consulte [Seção 34.7.1](ecpg-descriptors.md#ECPG-NAMED-DESCRIPTORS "34.7.1. Named SQL Descriptor Areas") para uma lista de itens suportados.

*`cvariable`* [#](#ECPG-SQL-GET-DESCRIPTOR-CVARIABLE): Uma variável hospedeira que receberá os dados recuperados da área de descritor.

## Exemplos

Um exemplo para recuperar o número de colunas em um conjunto de resultados:

```
EXEC SQL GET DESCRIPTOR d :d_count = COUNT;
```

Um exemplo para recuperar o comprimento de dados na primeira coluna:

```
EXEC SQL GET DESCRIPTOR d VALUE 1 :d_returned_octet_length = RETURNED_OCTET_LENGTH;
```

Um exemplo para recuperar o corpo dos dados da segunda coluna como uma string:

```
EXEC SQL GET DESCRIPTOR d VALUE 2 :d_data = DATA;
```

Aqui está um exemplo de um procedimento completo para executar `SELECT current_database();` e mostrar o número de colunas, o comprimento dos dados das colunas e os dados das colunas:

```
int
main(void)
{
EXEC SQL BEGIN DECLARE SECTION;
    int  d_count;
    char d_data[1024];
    int  d_returned_octet_length;
EXEC SQL END DECLARE SECTION;

    EXEC SQL CONNECT TO testdb AS con1 USER testuser;
    EXEC SQL SELECT pg_catalog.set_config('search_path', '', false); EXEC SQL COMMIT;
    EXEC SQL ALLOCATE DESCRIPTOR d;

    /* Declare, open a cursor, and assign a descriptor to the cursor  */
    EXEC SQL DECLARE cur CURSOR FOR SELECT current_database();
    EXEC SQL OPEN cur;
    EXEC SQL FETCH NEXT FROM cur INTO SQL DESCRIPTOR d;

    /* Get a number of total columns */
    EXEC SQL GET DESCRIPTOR d :d_count = COUNT;
    printf("d_count                 = %d\n", d_count);

    /* Get length of a returned column */
    EXEC SQL GET DESCRIPTOR d VALUE 1 :d_returned_octet_length = RETURNED_OCTET_LENGTH;
    printf("d_returned_octet_length = %d\n", d_returned_octet_length);

    /* Fetch the returned column as a string */
    EXEC SQL GET DESCRIPTOR d VALUE 1 :d_data = DATA;
    printf("d_data                  = %s\n", d_data);

    /* Closing */
    EXEC SQL CLOSE cur;
    EXEC SQL COMMIT;

    EXEC SQL DEALLOCATE DESCRIPTOR d;
    EXEC SQL DISCONNECT ALL;

    return 0;
}
```

Quando o exemplo for executado, o resultado ficará assim:

```
d_count                 = 1
d_returned_octet_length = 6
d_data                  = testdb
```

## Compatibilidade

`GET DESCRIPTOR` é especificado no padrão SQL.

## Veja também

(ecpg-sql-allocate-descriptor.md "ALLOCATE DESCRIPTOR"), (ecpg-sql-set-descriptor.md "SET DESCRIPTOR")