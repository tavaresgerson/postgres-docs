## CRIAR CLASSE DE OPERADOR

Crie uma classe de operador — defina uma nova classe de operador

## Sinopse

```
CREATE OPERATOR CLASS name [ DEFAULT ] FOR TYPE data_type
  USING index_method [ FAMILY family_name ] AS
  {  OPERATOR strategy_number operator_name [ ( op_type, op_type ) ] [ FOR SEARCH | FOR ORDER BY sort_family_name ]
   | FUNCTION support_number [ ( op_type [ , op_type ] ) ] function_name ( argument_type [, ...] )
   | STORAGE storage_type
  } [, ... ]
```

## Descrição

`CREATE OPERATOR CLASS` cria uma nova classe de operador. Uma classe de operador define como um determinado tipo de dados pode ser usado com um índice. A classe de operador especifica que certos operadores preencherão papéis ou "estratégias" particulares para este tipo de dados e este método de índice. A classe de operador também especifica as funções de suporte a serem usadas pelo método de índice quando a classe de operador é selecionada para uma coluna de índice. Todos os operadores e funções usados por uma classe de operador devem ser definidos antes que a classe de operador possa ser criada.

Se um nome de esquema for fornecido, a classe do operador é criada no esquema especificado. Caso contrário, ela é criada no esquema atual. Duas classes de operador no mesmo esquema podem ter o mesmo nome apenas se forem para métodos de índice diferentes.

O usuário que define uma classe de operador se torna seu proprietário. Atualmente, o usuário que está criando deve ser um superusuário. (Essa restrição é feita porque uma definição errada de classe de operador pode confundir ou até mesmo fazer o servidor falhar.)

`CREATE OPERATOR CLASS` atualmente não verifica se a definição da classe de operadores inclui todos os operadores e funções exigidos pelo método de índice, nem se os operadores e funções formam um conjunto autoconsistente. É responsabilidade do usuário definir uma classe de operadores válida.

As classes de operador relacionadas podem ser agrupadas em *famílias de operadores*. Para adicionar uma nova classe de operador a uma família existente, especifique a opção `FAMILY` em `CREATE OPERATOR CLASS`. Sem essa opção, a nova classe é colocada em uma família com o mesmo nome da nova classe (criando essa família se ela ainda não existir).

Consulte [Seção 36.16][(xindex.md "36.16. Interfacing Extensions to Indexes")] para obter mais informações.

## Parâmetros

*`name`*: O nome da classe de operador a ser criada. O nome pode ser qualificado pelo esquema.

`DEFAULT`: Se presente, a classe de operador se tornará a classe de operador padrão para seu tipo de dados. No máximo, uma classe de operador pode ser a padrão para um tipo de dados específico e método de índice.

*`data_type`*: O tipo de dados da coluna para a qual essa classe de operador é destinada.

*`index_method`*: O nome do método de índice para o qual essa classe de operador é destinada.

*`family_name`*: O nome da família de operadores existente para adicionar esta classe de operador. Se não especificado, uma família com o mesmo nome que a classe de operador é usada (criando-a, se ainda não existir).

*`strategy_number`*: O número da estratégia do método de índice para um operador associado à classe de operador.

*`operator_name`*: O nome (opcionalmente qualificado por esquema) de um operador associado à classe de operador.

*`op_type`*: Em uma cláusula `OPERATOR`, o(s) tipo(s) de dados do operando do operador, ou `NONE` para indicar um operador prefixo. Os tipos de dados do operando podem ser omitidos no caso normal, quando são iguais ao tipo de dados da classe do operador.

Em uma cláusula `FUNCTION`, o(s) tipo(s) de dados do operando que a função deve suportar, se diferente do(s) tipo(s) de dados de entrada da função (para funções de comparação de árvore B e funções de hash) ou do tipo de dados da classe (para funções de suporte a classificação de árvore B, funções de imagem igual de árvore B e todas as funções nas classes de operadores GiST, SP-GiST, GIN e BRIN). Esses padrões são corretos, e *`op_type`* não precisa ser especificado em cláusulas `FUNCTION`, exceto no caso de uma função de suporte a classificação de árvore B que deve suportar comparações entre tipos de dados.

*`sort_family_name`*: O nome (opcionalmente qualificado por esquema) de uma família de operadores existente `btree` que descreve a ordem de classificação associada a um operador de classificação.

Se nem `FOR SEARCH` nem `FOR ORDER BY` são especificados, `FOR SEARCH` é o padrão.

*`support_number`*: Número da função de suporte do método de índice para uma função associada à classe de operador.

*`function_name`*: O nome (opcionalmente qualificado por esquema) de uma função que é uma função de suporte de método de índice para a classe de operadores.

*`argument_type`*: O(s) tipo(s) de dados do parâmetro da função.

*`storage_type`*: O tipo de dados que é realmente armazenado no índice. Normalmente, este é o mesmo que o tipo de dados da coluna, mas alguns métodos de índice (atualmente GiST, GIN, SP-GiST e BRIN) permitem que seja diferente. A cláusula `STORAGE` deve ser omitida, a menos que o método de índice permita que um tipo diferente seja usado. Se a coluna *`data_type`* for especificada como `anyarray`, o *`storage_type`* pode ser declarado como `anyelement` para indicar que as entradas do índice são membros do tipo de elemento pertencente ao tipo de matriz real para o qual cada índice específico é criado.

As cláusulas `OPERATOR`, `FUNCTION` e `STORAGE` podem aparecer em qualquer ordem.

## Notas

Como a máquina de índice não verifica as permissões de acesso às funções antes de usá-las, incluindo uma função ou operador em uma classe de operador é equivalente a conceder permissão de execução pública sobre ela. Geralmente, isso não é um problema para os tipos de funções que são úteis em uma classe de operador.

Os operadores não devem ser definidos por funções SQL. É provável que uma função SQL seja embutida na consulta que a chama, o que impedirá o otimizador de reconhecer que a consulta corresponde a um índice.

## Exemplos

O comando a seguir define uma classe de operador de índice GiST para o tipo de dados `_int4` (matriz de `int4`). Consulte o módulo [intarray](intarray.md "F.19. intarray — manipulate arrays of integers") para o exemplo completo.

```
CREATE OPERATOR CLASS gist__int_ops
    DEFAULT FOR TYPE _int4 USING gist AS
        OPERATOR        3       &&,
        OPERATOR        6       = (anyarray, anyarray),
        OPERATOR        7       @>,
        OPERATOR        8       <@,
        OPERATOR        20      @@ (_int4, query_int),
        FUNCTION        1       g_int_consistent (internal, _int4, smallint, oid, internal),
        FUNCTION        2       g_int_union (internal, internal),
        FUNCTION        3       g_int_compress (internal),
        FUNCTION        4       g_int_decompress (internal),
        FUNCTION        5       g_int_penalty (internal, internal, internal),
        FUNCTION        6       g_int_picksplit (internal, internal),
        FUNCTION        7       g_int_same (_int4, _int4, internal);
```

## Compatibilidade

`CREATE OPERATOR CLASS` é uma extensão do PostgreSQL. Não há uma declaração `CREATE OPERATOR CLASS` no padrão SQL.

## Veja também

[ALTERAR CLASSE DE OPERADOR](sql-alteropclass.md "ALTER OPERATOR CLASS"), [DROP CLASS DE OPERADOR](sql-dropopclass.md "DROP OPERATOR CLASS"), [CADASTRAR FAMÍLIA DE OPERADORES](sql-createopfamily.md "CREATE OPERATOR FAMILY"), [ALTERAR FAMÍLIA DE OPERADORES](sql-alteropfamily.md "ALTER OPERATOR FAMILY")