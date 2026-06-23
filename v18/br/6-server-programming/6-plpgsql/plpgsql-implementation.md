## 41.11. PL/pgSQL sob o manto [#](#PLPGSQL-IMPLEMENTATION)

* [41.11.1. Substituição de variáveis](plpgsql-implementation.md#PLPGSQL-VAR-SUBST)
* [41.11.2. Caching de plano](plpgsql-implementation.md#PLPGSQL-PLAN-CACHING)

Esta seção discute alguns detalhes de implementação que são frequentemente importantes para os usuários do PL/pgSQL saberem.

### 41.11.1. Substituição de variáveis [#](#PLPGSQL-VAR-SUBST)

As instruções e expressões SQL dentro de uma função PL/pgSQL podem se referir a variáveis e parâmetros da função. Nos bastidores, o PL/pgSQL substitui os parâmetros de consulta por tais referências. Os parâmetros de consulta só serão substituídos nos lugares onde são sintaticamente permitidos. Como um caso extremo, considere este exemplo de estilo de programação ruim:

```
INSERT INTO foo (foo) VALUES (foo(foo));
```

A primeira ocorrência de `foo` deve ser, sintaticamente, o nome de uma tabela, portanto, não será substituída, mesmo que a função tenha uma variável chamada `foo`. A segunda ocorrência deve ser o nome de uma coluna dessa tabela, portanto, também não será substituída. Da mesma forma, a terceira ocorrência deve ser o nome de uma função, portanto, também não será substituída. Apenas a última ocorrência é candidata a ser uma referência a uma variável da função PL/pgSQL.

Outra maneira de entender isso é que a substituição de variáveis só pode inserir valores de dados em um comando SQL; ela não pode alterar dinamicamente quais objetos do banco de dados são referenciados pelo comando. (Se você quiser fazer isso, você deve construir uma string de comando dinamicamente, conforme explicado em [Seção 41.5.4](plpgsql-statements.md#PLPGSQL-STATEMENTS-EXECUTING-DYN)).

Como os nomes das variáveis não são sintaticamente diferentes dos nomes das colunas de tabela, pode haver ambiguidade em declarações que também se referem a tabelas: um nome dado deve se referir a uma coluna de tabela ou a uma variável? Vamos alterar o exemplo anterior para

```
INSERT INTO dest (col) SELECT foo + bar FROM src;
```

Aqui, `dest` e `src` devem ser nomes de tabela, e `col` deve ser uma coluna de `dest`, mas `foo` e `bar` podem razoavelmente ser variáveis da função ou colunas de `src`.

Por padrão, o PL/pgSQL reportará um erro se um nome em uma declaração SQL puder se referir a uma variável ou a uma coluna de tabela. Você pode corrigir esse problema renomeando a variável ou coluna, ou qualificando a referência ambígua, ou dizendo ao PL/pgSQL qual interpretação preferir.

A solução mais simples é renomear a variável ou coluna. Uma regra comum de codificação é usar uma convenção de nomeação diferente para variáveis PL/pgSQL do que você usa para nomes de colunas. Por exemplo, se você consistentemente nomeia as variáveis de função como `v_something`, enquanto nenhum dos nomes de suas colunas começa com `v_`, não haverá conflitos.

Alternativamente, você pode qualificar referências ambíguas para torná-las claras. No exemplo acima, `src.foo` seria uma referência inequívoca à coluna da tabela. Para criar uma referência inequívoca a uma variável, declare-a em um bloco etiquetado e use o rótulo do bloco (consulte [Seção 41.2] (plpgsql-structure.md "41.2. Structure of PL/pgSQL")). Por exemplo,

```
<<block>>
DECLARE
    foo int;
BEGIN
    foo := ...;
    INSERT INTO dest (col) SELECT block.foo + bar FROM src;
```

Aqui `block.foo` significa a variável, mesmo que haja uma coluna `foo` em `src`. Os parâmetros da função, bem como as variáveis especiais, como `FOUND`, podem ser qualificados pelo nome da função, porque são declarados implicitamente em um bloco externo rotulado com o nome da função.

Às vezes, é impraticável corrigir todas as referências ambíguas em um grande corpo de código PL/pgSQL. Nesses casos, você pode especificar que o PL/pgSQL deve resolver referências ambíguas como a variável (que é compatível com o comportamento do PL/pgSQL antes do PostgreSQL 9.0) ou como a coluna da tabela (que é compatível com alguns outros sistemas, como o Oracle).

Para alterar esse comportamento em nível de sistema, defina o parâmetro de configuração `plpgsql.variable_conflict` para um dos valores `error`, `use_variable` ou `use_column` (onde `error` é o padrão da fábrica). Esse parâmetro afeta as compilações subsequentes de declarações em funções PL/pgSQL, mas não as declarações já compiladas na sessão atual. Como alterar esse ajuste pode causar mudanças inesperadas no comportamento das funções PL/pgSQL, ele só pode ser alterado por um usuário administrador.

Você também pode definir o comportamento de forma individual para cada função, inserindo um desses comandos especiais no início do texto da função:

```
#variable_conflict error
#variable_conflict use_variable
#variable_conflict use_column
```

Esses comandos afetam apenas a função em que são escritos e substituem a configuração de `plpgsql.variable_conflict`. Um exemplo é

```
CREATE FUNCTION stamp_user(id int, comment text) RETURNS void AS $$
    #variable_conflict use_variable
    DECLARE
        curtime timestamp := now();
    BEGIN
        UPDATE users SET last_modified = curtime, comment = comment
          WHERE users.id = id;
    END;
$$ LANGUAGE plpgsql;
```

No comando `UPDATE`, `curtime`, `comment` e `id` se referirão à variável e aos parâmetros da função, independentemente de `users` ter colunas com esses nomes. Observe que tivemos que qualificar a referência a `users.id` na cláusula `WHERE` para fazer com que ela se refira à coluna da tabela. Mas não tivemos que qualificar a referência a `comment` como alvo na lista `UPDATE`, porque, sintaticamente, isso deve ser uma coluna de `users`. Podemos escrever a mesma função sem depender da configuração `variable_conflict` desta maneira:

```
CREATE FUNCTION stamp_user(id int, comment text) RETURNS void AS $$
    <<fn>>
    DECLARE
        curtime timestamp := now();
    BEGIN
        UPDATE users SET last_modified = fn.curtime, comment = stamp_user.comment
          WHERE users.id = stamp_user.id;
    END;
$$ LANGUAGE plpgsql;
```

A substituição variável não ocorre em uma string de comando fornecida ao `EXECUTE` ou a uma de suas variantes. Se você precisar inserir um valor variável em tal comando, faça isso como parte da construção do valor da string, ou use `USING`, conforme ilustrado em [Seção 41.5.4](plpgsql-statements.md#PLPGSQL-STATEMENTS-EXECUTING-DYN).

A substituição variável atualmente funciona apenas em `SELECT`, `INSERT`, `UPDATE`, `DELETE`, `MERGE` e comandos que contenham um desses (como `EXPLAIN` e [[`CREATE TABLE ... AS SELECT`]), porque o motor SQL principal permite apenas parâmetros de consulta nesses comandos. Para usar um nome ou valor não constante em outros tipos de declarações (geralmente chamados de declarações de utilidade), você deve construir a declaração de utilidade como uma string e `EXECUTE`-a.

### 41.11.2. Cache do plano [#](#PLPGSQL-PLAN-CACHING)

O interpretador PL/pgSQL analisa o texto fonte da função e produz uma árvore de instruções binárias internas na primeira vez que a função é chamada (dentro de cada sessão). A árvore de instruções traduz completamente a estrutura da declaração PL/pgSQL, mas as expressões SQL individuais e os comandos SQL usados na função não são traduzidos imediatamente.

Como cada expressão e comando SQL é executado primeiro na função, o interpretador PL/pgSQL analisa e analisa o comando para criar uma declaração preparada, usando a função `SPI_prepare` do gerenciador SPI. Visitas subsequentes a essa expressão ou comando reutilizam a declaração preparada. Assim, uma função com caminhos de código condicional que são raramente visitados nunca incorrerá no overhead de analisar aqueles comandos que nunca são executados dentro da sessão atual. Uma desvantagem é que erros em uma expressão ou comando específico não podem ser detectados até que essa parte da função seja alcançada na execução. (Erros de sintaxe trivial serão detectados durante a passagem de análise inicial, mas qualquer coisa mais profunda não será detectada até a execução.)

O PL/pgSQL (ou, mais precisamente, o gerenciador SPI) pode, além disso, tentar em cache o plano de execução associado a qualquer declaração preparada em particular. Se um plano em cache não for usado, então um plano novo é gerado em cada visita à declaração, e os valores atuais dos parâmetros (ou seja, os valores das variáveis PL/pgSQL) podem ser usados para otimizar o plano selecionado. Se a declaração não tiver parâmetros ou for executada muitas vezes, o gerenciador SPI considerará a criação de um plano *genérico* que não dependa de valores de parâmetros específicos, e o cacheá-lo para reutilização. Normalmente, isso acontece apenas se o plano de execução não for muito sensível aos valores das variáveis PL/pgSQL referenciadas nele. Se for, gerar um plano a cada vez é uma vantagem líquida. Consulte [PREPARE](sql-prepare.md) para mais informações sobre o comportamento das declarações preparadas.

Como o PL/pgSQL salva instruções preparadas e, às vezes, planos de execução dessa maneira, os comandos SQL que aparecem diretamente em uma função PL/pgSQL devem se referir às mesmas tabelas e colunas em cada execução; ou seja, você não pode usar um parâmetro como o nome de uma tabela ou coluna em um comando SQL. Para contornar essa restrição, você pode construir comandos dinâmicos usando a declaração `EXECUTE` do PL/pgSQL — no preço de realizar nova análise de análise e construir um novo plano de execução em cada execução.

A natureza mutável das variáveis de registro apresenta outro problema nesse contexto. Quando os campos de uma variável de registro são usados em expressões ou declarações, os tipos de dados dos campos não devem mudar de uma chamada da função para a próxima, uma vez que cada expressão será analisada usando o tipo de dados que está presente quando a expressão é alcançada pela primeira vez. `EXECUTE` pode ser usado para contornar esse problema quando necessário.

Se a mesma função for usada como um gatilho para mais de uma tabela, o PL/pgSQL prepara e armazena instruções de forma independente para cada combinação de tabela e função — ou seja, há um cache para cada combinação de função e tabela, não apenas para cada função. Isso alivia alguns dos problemas com tipos de dados variados; por exemplo, uma função de gatilho poderá funcionar com sucesso com uma coluna chamada `key`, mesmo que ela tenha tipos diferentes em diferentes tabelas.

Da mesma forma, funções com tipos de argumentos polimórficos têm uma cache de declaração separada para cada combinação de tipos de argumentos reais para os quais foram invocadas, para que as diferenças de tipo de dados não causem falhas inesperadas.

O armazenamento de cache de declarações pode, às vezes, ter efeitos surpreendentes na interpretação de valores sensíveis ao tempo. Por exemplo, há uma diferença entre o que essas duas funções fazem:

```
CREATE FUNCTION logfunc1(logtxt text) RETURNS void AS $$
    BEGIN
        INSERT INTO logtable VALUES (logtxt, 'now');
    END;
$$ LANGUAGE plpgsql;
```

e:

```
CREATE FUNCTION logfunc2(logtxt text) RETURNS void AS $$
    DECLARE
        curtime timestamp;
    BEGIN
        curtime := 'now';
        INSERT INTO logtable VALUES (logtxt, curtime);
    END;
$$ LANGUAGE plpgsql;
```

No caso de `logfunc1`, o parser principal do PostgreSQL sabe, ao analisar o `INSERT`, que a string `'now'` deve ser interpretada como `timestamp`, porque a coluna alvo de `logtable` é desse tipo. Assim, `'now'` será convertido em uma constante `timestamp` quando o `INSERT` for analisado, e então usado em todas as invocações de `logfunc1` durante a vida útil da sessão. Desnecessário dizer que isso não é o que o programador queria. Uma ideia melhor é usar a função `now()` ou `current_timestamp`.

No caso de `logfunc2`, o parser principal do PostgreSQL não sabe qual tipo `'now'` deve se tornar e, portanto, retorna um valor de dados do tipo `text`, contendo a string `now`. Durante a subsequente atribuição à variável local `curtime`, o interpretador PL/pgSQL converte essa string para o tipo `timestamp` chamando as funções `textout` e `timestamp_in` para a conversão. Assim, o rótulo de tempo calculado é atualizado em cada execução conforme o programador espera. Embora isso funcione como esperado, não é muito eficiente, então o uso da função `now()` ainda seria uma boa ideia.