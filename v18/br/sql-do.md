## DO

DO — execute um bloco de código anônimo

## Sinopse

```
DO [ LANGUAGE lang_name ] code
```

## Descrição

`DO` executa um bloco de código anônimo, ou, em outras palavras, uma função anônima transitória em uma linguagem procedural.

O bloco de código é tratado como se fosse o corpo de uma função sem parâmetros, retornando `void`. Ele é analisado e executado uma única vez.

A cláusula opcional `LANGUAGE` pode ser escrita antes ou depois do bloco de código.

## Parâmetros

*`code`*: O código de linguagem procedural a ser executado. Isso deve ser especificado como uma literal de string, assim como em `CREATE FUNCTION`. É recomendado o uso de uma literal com dólar citado.

*`lang_name`*: O nome da linguagem procedural na qual o código foi escrito. Se omitido, o padrão é `plpgsql`.

## Notas

O idioma processual a ser utilizado já deve ter sido instalado no banco de dados atual por meio de `CREATE EXTENSION`. `plpgsql` é instalado por padrão, mas outros idiomas não são.

O usuário deve ter o privilégio `USAGE` para o idioma de procedimentos, ou deve ser um superusuário se o idioma não for confiável. Esse é o mesmo requisito de privilégio para criar uma função no idioma.

Se `DO` for executado em um bloco de transação, então o código do procedimento não pode executar instruções de controle de transação. As instruções de controle de transação só são permitidas se `DO` for executado em sua própria transação.

## Exemplos

Concede todos os privilégios em todas as visualizações no esquema `public` ao papel `webuser`:

```
DO $$DECLARE r record;
BEGIN
    FOR r IN SELECT table_schema, table_name FROM information_schema.tables
             WHERE table_type = 'VIEW' AND table_schema = 'public'
    LOOP
        EXECUTE 'GRANT ALL ON ' || quote_ident(r.table_schema) || '.' || quote_ident(r.table_name) || ' TO webuser';
    END LOOP;
END$$;
```

## Compatibilidade

Não há nenhuma declaração `DO` no padrão SQL.

## Veja também

[Crie Linguagem](sql-createlanguage.md "CREATE LANGUAGE")