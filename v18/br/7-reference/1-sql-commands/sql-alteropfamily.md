## ALTER FAMÍLIA DE OPERADORES

ALTERAR FAMÍLIA DE OPERADORES — alterar a definição de uma família de operadores

## Sinopse

```
ALTER OPERATOR FAMILY name USING index_method ADD
  {  OPERATOR strategy_number operator_name ( op_type, op_type )
              [ FOR SEARCH | FOR ORDER BY sort_family_name ]
   | FUNCTION support_number [ ( op_type [ , op_type ] ) ]
              function_name [ ( argument_type [, ...] ) ]
  } [, ... ]

ALTER OPERATOR FAMILY name USING index_method DROP
  {  OPERATOR strategy_number ( op_type [ , op_type ] )
   | FUNCTION support_number ( op_type [ , op_type ] )
  } [, ... ]

ALTER OPERATOR FAMILY name USING index_method
    RENAME TO new_name

ALTER OPERATOR FAMILY name USING index_method
    OWNER TO { new_owner | CURRENT_ROLE | CURRENT_USER | SESSION_USER }

ALTER OPERATOR FAMILY name USING index_method
    SET SCHEMA new_schema
```

## Descrição

`ALTER OPERATOR FAMILY` altera a definição de uma família de operadores. Você pode adicionar operadores e funções de suporte à família, removê-los da família ou alterar o nome ou o proprietário da família.

Quando operadores e funções de suporte são adicionados a uma família com `ALTER OPERATOR FAMILY`, eles não fazem parte de nenhuma classe específica de operador dentro da família, mas são apenas "soltos" dentro da família. Isso indica que esses operadores e funções são compatíveis com a semântica da família, mas não são necessários para o funcionamento correto de qualquer índice específico. (Operadores e funções que são necessários para isso devem ser declarados como parte de uma classe de operador, em vez disso; veja [CREATE OPERATOR CLASS](sql-createopclass.md).]) O PostgreSQL permitirá que membros soltos de uma família sejam descartados da família a qualquer momento, mas os membros de uma classe de operador não podem ser descartados sem descartar toda a classe e quaisquer índices que dependem dela. Tipicamente, operadores e funções de único tipo de dado fazem parte de classes de operador porque são necessários para suportar um índice nesse tipo de dado específico, enquanto operadores e funções de vários tipos de dados são feitos membros soltos da família.

Você deve ser um superusuário para usar `ALTER OPERATOR FAMILY`. (Essa restrição é feita porque uma definição errada da família de operadores pode confundir ou até mesmo fazer o servidor falhar.)

`ALTER OPERATOR FAMILY` atualmente não verifica se a definição da família de operadores inclui todos os operadores e funções exigidos pelo método de índice, nem se os operadores e funções formam um conjunto autoconsistente. É responsabilidade do usuário definir uma família de operadores válida.

Consulte [Seção 36.16](xindex.md) para obter mais informações.

## Parâmetros

*`name`*: O nome (opcionalmente qualificado por esquema) de uma família de operadores existente.

*`index_method`*: O nome do método de índice para o qual essa família de operadores é destinada.

*`strategy_number`*: O número da estratégia do método de índice para um operador associado à família de operadores.

*`operator_name`*: O nome (opcionalmente qualificado por esquema) de um operador associado à família de operadores.

*`op_type`*: Em uma cláusula `OPERATOR`, o(s) tipo(s) de dados do operando do operador, ou `NONE` para indicar um operador prefixo. Ao contrário da sintaxe comparável em `CREATE OPERATOR CLASS`, os tipos de dados do operando devem ser sempre especificados.

Em uma cláusula `ADD FUNCTION`, o(s) tipo(s) de dados do operando que a função deve suportar, se diferente do(s) tipo(s) de dados de entrada da função. Para funções de comparação de árvore B e funções de hash, não é necessário especificar *`op_type`* uma vez que o(s) tipo(s) de dados de entrada da função são sempre os corretos a serem usados. Para funções de suporte a classificação de árvore B, funções de imagem igual B-Tree e todas as funções nas classes de operadores GiST, SP-GiST e GIN, é necessário especificar o(s) tipo(s) de dados do operando com o qual a função deve ser usada.

Em uma cláusula `DROP FUNCTION`, o(s) tipo(s) de dados do operando que a função deve suportar deve ser especificado.

*`sort_family_name`*: O nome (opcionalmente qualificado por esquema) de uma família de operadores existente `btree` que descreve a ordem de classificação associada a um operador de classificação.

Se nem `FOR SEARCH` nem `FOR ORDER BY` são especificados, `FOR SEARCH` é o padrão.

*`support_number`*: Número da função de suporte do método de índice para uma função associada à família de operadores.

*`function_name`*: O nome (opcionalmente qualificado por esquema) de uma função que é uma função de suporte de método de índice para a família de operadores. Se não for especificada uma lista de argumentos, o nome deve ser único em seu esquema.

*`argument_type`*: O(s) tipo(s) de dados do parâmetro da função.

*`new_name`*: O novo nome da família do operador.

*`new_owner`*: O novo proprietário da família de operadoras.

*`new_schema`*: O novo esquema para a família de operadores.

As cláusulas `OPERATOR` e `FUNCTION` podem aparecer em qualquer ordem.

## Notas

Observe que a sintaxe `DROP` especifica apenas o "camada" da família do operador, pela estratégia ou número de suporte e pelo(s) tipo(s) de dados de entrada. O nome do operador ou função que ocupa a camada não é mencionado. Além disso, para `DROP FUNCTION`, o tipo(s) a especificar são os(s) tipo(s) de dados de entrada que a função é destinada a suportar; para os índices GiST, SP-GiST e GIN, isso pode não ter nada a ver com os tipos de argumento de entrada reais da função.

Como a máquina de índice não verifica as permissões de acesso nas funções antes de usá-las, incluindo uma função ou operador em uma família de operadores equivale a conceder permissão de execução pública sobre ela. Geralmente, isso não é um problema para os tipos de funções que são úteis em uma família de operadores.

Os operadores não devem ser definidos por funções SQL. É provável que uma função SQL seja embutida na consulta que a chama, o que impedirá o otimizador de reconhecer que a consulta corresponde a um índice.

## Exemplos

O comando a seguir adiciona operadores de dados cruzados e funções de suporte a uma família de operadores que já contém classes de operadores de árvore B para tipos de dados `int4` e `int2`.

```
ALTER OPERATOR FAMILY integer_ops USING btree ADD

  -- int4 vs int2
  OPERATOR 1 < (int4, int2) ,
  OPERATOR 2 <= (int4, int2) ,
  OPERATOR 3 = (int4, int2) ,
  OPERATOR 4 >= (int4, int2) ,
  OPERATOR 5 > (int4, int2) ,
  FUNCTION 1 btint42cmp(int4, int2) ,

  -- int2 vs int4
  OPERATOR 1 < (int2, int4) ,
  OPERATOR 2 <= (int2, int4) ,
  OPERATOR 3 = (int2, int4) ,
  OPERATOR 4 >= (int2, int4) ,
  OPERATOR 5 > (int2, int4) ,
  FUNCTION 1 btint24cmp(int2, int4) ;
```

Para remover essas entradas novamente:

```
ALTER OPERATOR FAMILY integer_ops USING btree DROP

  -- int4 vs int2
  OPERATOR 1 (int4, int2) ,
  OPERATOR 2 (int4, int2) ,
  OPERATOR 3 (int4, int2) ,
  OPERATOR 4 (int4, int2) ,
  OPERATOR 5 (int4, int2) ,
  FUNCTION 1 (int4, int2) ,

  -- int2 vs int4
  OPERATOR 1 (int2, int4) ,
  OPERATOR 2 (int2, int4) ,
  OPERATOR 3 (int2, int4) ,
  OPERATOR 4 (int2, int4) ,
  OPERATOR 5 (int2, int4) ,
  FUNCTION 1 (int2, int4) ;
```

## Compatibilidade

Não há nenhuma declaração `ALTER OPERATOR FAMILY` no padrão SQL.

## Veja também

[Crie família de operadores](sql-createopfamily.md "CREATE OPERATOR FAMILY"), [Remova família de operadores](sql-dropopfamily.md "DROP OPERATOR FAMILY"), [Crie classe de operadores](sql-createopclass.md "CREATE OPERATOR CLASS"), [Altere classe de operadores](sql-alteropclass.md "ALTER OPERATOR CLASS"), [Remova classe de operadores](sql-dropopclass.md "DROP OPERATOR CLASS")