## Crie conversão

CREATE CONVERSION — definir uma nova conversão de codificação

## Sinopse

```
CREATE [ DEFAULT ] CONVERSION name
    FOR source_encoding TO dest_encoding FROM function_name
```

## Descrição

`CREATE CONVERSION` define uma nova conversão entre dois conjuntos de codificação de caracteres.

As conversões marcadas com `DEFAULT` podem ser usadas para conversão automática de codificação entre cliente e servidor. Para suportar esse uso, duas conversões, de codificação A para B *e* de codificação B para A, devem ser definidas.

Para criar uma conversão, você deve ter privilégio `EXECUTE` na função e privilégio `CREATE` no esquema de destino.

## Parâmetros

`DEFAULT`: A cláusula `DEFAULT` indica que essa conversão é a opção padrão para este conjunto de codificação de origem para destino. Deve haver apenas uma codificação padrão em um esquema para o par de codificação.

*`name`*: O nome da conversão. O nome da conversão pode ser qualificado pelo esquema. Se não for, a conversão é definida no esquema atual. O nome da conversão deve ser único dentro de um esquema.

*`source_encoding`*: Nome do codificador de fonte.

*`dest_encoding`*: O nome do codificador de destino.

*`function_name`*: A função usada para realizar a conversão. O nome da função pode ser qualificada pelo esquema. Se não for, a função será procurada no caminho.

A função deve ter a seguinte assinatura:

``` conv_proc( integer,  -- source encoding ID integer,  -- destination encoding ID cstring,  -- source string (null terminated C string) internal, -- destination (fill with a null terminated C string) integer,  -- source string length boolean   -- if true, don't throw an error if conversion fails ) RETURNS integer;
    ```

O valor de retorno é o número de bytes de origem que foram convertidos com sucesso. Se o último argumento for falso, a função deve lançar um erro em caso de entrada inválida, e o valor de retorno é sempre igual ao comprimento da string de origem.

## Notas

Nem o codificação de origem nem a codificação de destino podem ser `SQL_ASCII`, pois o comportamento do servidor em casos que envolvem a codificação do `SQL_ASCII` é pré-configurado.

Use `DROP CONVERSION` para remover conversões definidas pelo usuário.

Os privilégios necessários para criar uma conversão podem ser alterados em uma versão futura.

## Exemplos

Para criar uma conversão de codificação `UTF8` para `LATIN1` usando `myfunc`:

```
CREATE CONVERSION myconv FOR 'UTF8' TO 'LATIN1' FROM myfunc;
```

## Compatibilidade

`CREATE CONVERSION` é uma extensão do PostgreSQL. Não há uma declaração `CREATE CONVERSION` no padrão SQL, mas uma declaração `CREATE TRANSLATION` que é muito semelhante em propósito e sintaxe.

## Veja também

[ALTERAR CONVERSÃO](sql-alterconversion.md "ALTER CONVERSION"), [CADASTRAR FUNÇÃO](sql-createfunction.md "CREATE FUNCTION"), [CANCELAR CONVERSÃO](sql-dropconversion.md "DROP CONVERSION")