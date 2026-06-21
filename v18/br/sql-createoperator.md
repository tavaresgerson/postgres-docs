## Crie Operador

CREATE OPERATOR — definir um novo operador

## Sinopse

```
CREATE OPERATOR name (
    {FUNCTION|PROCEDURE} = function_name
    [, LEFTARG = left_type ] [, RIGHTARG = right_type ]
    [, COMMUTATOR = com_op ] [, NEGATOR = neg_op ]
    [, RESTRICT = res_proc ] [, JOIN = join_proc ]
    [, HASHES ] [, MERGES ]
)
```

## Descrição

`CREATE OPERATOR` define um novo operador, *`name`*. O usuário que define um operador torna-se seu proprietário. Se um nome de esquema for fornecido, o operador é criado no esquema especificado. Caso contrário, ele é criado no esquema atual.

O nome do operador é uma sequência de até `NAMEDATALEN`-1 (63 por padrão) caracteres da lista a seguir:

+ - * / < > = ~ ! @ # % ^ & | ` ?

Há algumas restrições na escolha do nome:

* `--` e `/*` não podem aparecer em nenhum lugar em um nome de operador, pois serão interpretados como o início de um comentário.
* Um nome de operador de vários caracteres não pode terminar em `+` ou `-`, a menos que o nome também contenha pelo menos um desses caracteres:

~ ! @ # % ^ & | ' ?

Por exemplo, `@-` é um nome de operador permitido, mas `*-` não é. Essa restrição permite que o PostgreSQL analise comandos compatíveis com SQL sem exigir espaços entre os tokens.
* O símbolo `=>` é reservado pela gramática SQL, portanto, não pode ser usado como um nome de operador.

O operador `!=` é mapeado para `<>` na entrada, portanto, esses dois nomes são sempre equivalentes.

Para operadores binários, tanto `LEFTARG` quanto `RIGHTARG` devem ser definidos. Apenas para operadores prefixados, deve ser definido o *`RIGHTARG`*. A função *`function_name`* deve ter sido definida anteriormente usando `CREATE FUNCTION` e deve ser definida para aceitar o número correto de argumentos (um ou dois) dos tipos indicados.

Na sintaxe do `CREATE OPERATOR`, as palavras-chave `FUNCTION` e `PROCEDURE` são equivalentes, mas a função referenciada deve, em qualquer caso, ser uma função, não um procedimento. O uso da palavra-chave `PROCEDURE` aqui é histórico e desaconselhado.

As outras cláusulas especificam atributos de otimização opcional do operador. Seu significado é detalhado em [Seção 36.15][(xoper-optimization.md "36.15. Operator Optimization Information")].

Para poder criar um operador, você deve ter o privilégio `USAGE` nos tipos de argumento e no tipo de retorno, além do privilégio `EXECUTE` na função subjacente. Se um operador de commutator ou negador for especificado, você deve possuir esses operadores.

## Parâmetros

*`name`*: O nome do operador a ser definido. Veja acima para caracteres permitidos. O nome pode ser qualificado por esquema, por exemplo `CREATE OPERATOR myschema.+ (...)`. Se não for assim, então o operador é criado no esquema atual. Dois operadores no mesmo esquema podem ter o mesmo nome se operarem em diferentes tipos de dados. Isso é chamado de *sobrecarga*.

*`function_name`*: A função usada para implementar este operador.

*`left_type`*: O tipo de dados do operador do operando esquerdo, se houver. Esta opção seria omitida para um operador prefixo.

*`right_type`*: O tipo de dados do operador do operando da direita.

*`com_op`*: O commutator desse operador.

*`neg_op`*: O negador deste operador.

*`res_proc`*: A função de estimativa de seletividade de restrição para este operador.

*`join_proc`*: A função de estimativa de seletividade de junção para este operador.

`HASHES`: Indica que este operador pode suportar uma junção hash.

`MERGES`: Indica que este operador pode suportar uma junção de fusão.

Para dar um nome de operador qualificado por esquema em *`com_op`* ou outros argumentos opcionais, use a sintaxe `OPERATOR()`, por exemplo:

```
COMMUTATOR = OPERATOR(myschema.===) ,
```

## Notas

Consulte a [Seção 36.14][(xoper.md "36.14. User-Defined Operators")] e a [Seção 36.15][(xoper-optimization.md "36.15. Operator Optimization Information")] para obter mais informações.

Quando você está definindo um operador auto-comutativo, você simplesmente o faz. Quando você está definindo um par de operadores compostos, as coisas ficam um pouco mais complicadas: como o primeiro a ser definido pode se referir ao outro, que você ainda não definiu? Existem três soluções para esse problema:

* Uma maneira é omitir a cláusula `COMMUTATOR` no primeiro operador que você define e, em seguida, fornecer uma na definição do segundo operador. Como o PostgreSQL sabe que os operadores compostos vêm em pares, quando ele vê a segunda definição, ele automaticamente volta e preenche a cláusula `COMMUTATOR` que falta na primeira definição.
* Outra maneira, mais direta, é simplesmente incluir cláusulas `COMMUTATOR` em ambas as definições. Quando o PostgreSQL processa a primeira definição e percebe que `COMMUTATOR` se refere a um operador inexistente, o sistema faz uma entrada fictícia para esse operador no catálogo do sistema. Essa entrada fictícia terá dados válidos apenas para o nome do operador, os tipos de operandos esquerdo e direito, e o proprietário, pois é tudo o que o PostgreSQL pode deduzir neste ponto. A entrada do catálogo do primeiro operador será vinculada a essa entrada fictícia. Mais tarde, quando você definir o segundo operador, o sistema atualiza a entrada fictícia com as informações adicionais da segunda definição. Se você tentar usar o operador fictício antes de ele ter sido preenchido, você apenas receberá uma mensagem de erro.
* Alternativamente, ambos os operadores podem ser definidos sem cláusulas `COMMUTATOR` e, em seguida, `ALTER OPERATOR` pode ser usado para definir seus links de commutator. É suficiente `ALTER` qualquer um dos pares.

Em todos os três casos, você deve possuir ambos os operadores para marcá-los como commutadores.

Os pares de operadores negadores podem ser definidos usando os mesmos métodos que para pares de commutadores.

Não é possível especificar a precedência lexical de um operador em `CREATE OPERATOR`, porque o comportamento de precedência do analisador é pré-configurado. Consulte a Seção 4.1.6 [(sql-syntax-lexical.md#SQL-PRECEDENCE "4.1.6. Operator Precedence")] para obter detalhes sobre a precedência.

As opções obsoletas `SORT1`, `SORT2`, `LTCMP` e `GTCMP` eram anteriormente usadas para especificar os nomes dos operadores de ordenação associados a um operador de junção. Isso não é mais necessário, uma vez que as informações sobre os operadores associados são encontradas ao analisar as famílias de operadores de árvore B. Se uma dessas opções for fornecida, ela é ignorada, exceto pelo fato de implicitamente definir `MERGES` como verdadeiro.

Use `DROP OPERATOR` para excluir operadores definidos pelo usuário de um banco de dados. Use `ALTER OPERATOR` para modificar operadores em um banco de dados.

## Exemplos

O comando a seguir define um novo operador, igualdade de área, para o tipo de dados `box`:

```
CREATE OPERATOR === (
    LEFTARG = box,
    RIGHTARG = box,
    FUNCTION = area_equal_function,
    COMMUTATOR = ===,
    NEGATOR = !==,
    RESTRICT = area_restriction_function,
    JOIN = area_join_function,
    HASHES, MERGES
);
```

## Compatibilidade

`CREATE OPERATOR` é uma extensão do PostgreSQL. Não há disposições para operadores definidos pelo usuário no padrão SQL.

## Veja também

[ALTER OPERADOR](sql-alteroperator.md "ALTER OPERATOR"), [CADAQUE OPERADOR CLASS](sql-createopclass.md "CREATE OPERATOR CLASS"), [DROP OPERADOR](sql-dropoperator.md "DROP OPERATOR")