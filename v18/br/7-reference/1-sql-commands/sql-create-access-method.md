## Crie o método de acesso

Crie o método de acesso — defina um novo método de acesso

## Sinopse

```
CREATE ACCESS METHOD name
    TYPE access_method_type
    HANDLER handler_function
```

## Descrição

`CREATE ACCESS METHOD` cria um novo método de acesso.

O nome do método de acesso deve ser único dentro do banco de dados.

Apenas os superusuários podem definir novos métodos de acesso.

## Parâmetros

*`name`*: O nome do método de acesso a ser criado.

*`access_method_type`*: Esta cláusula especifica o tipo de método de acesso a ser definido. Apenas `TABLE` e `INDEX` são suportados atualmente.

*`handler_function`*: *`handler_function`* é o nome (possivelmente qualificado por esquema) de uma função previamente registrada que representa o método de acesso. A função de manipulador deve ser declarada para receber um único argumento do tipo `internal`, e seu tipo de retorno depende do tipo do método de acesso; para métodos de acesso `TABLE`, deve ser `table_am_handler`, e para métodos de acesso `INDEX`, deve ser `index_am_handler`. A API do nível C que a função de manipulador deve implementar varia dependendo do tipo do método de acesso. A API do método de acesso de tabela é descrita em [Capítulo 62](tableam.md "Chapter 62. Table Access Method Interface Definition") e a API do método de acesso de índice é descrita em [Capítulo 63](indexam.md "Chapter 63. Index Access Method Interface Definition").

## Exemplos

Crie um método de acesso ao índice `heptree` com a função de manipulador `heptree_handler`:

```
CREATE ACCESS METHOD heptree TYPE INDEX HANDLER heptree_handler;
```

## Compatibilidade

`CREATE ACCESS METHOD` é uma extensão do PostgreSQL.

## Veja também

[MÉTODO DE PERMISSÃO DE ACESSO](sql-drop-access-method.md "DROP ACCESS METHOD"), [CLASSE DE OPERADOR CRIADO](sql-createopclass.md "CREATE OPERATOR CLASS"), [FAMÍLIA DE OPERADORES CRIADA](sql-createopfamily.md "CREATE OPERATOR FAMILY")