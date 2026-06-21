## Crie agregado

CREATE AGGREGATE — definir uma nova função agregada

## Sinopse

```
CREATE [ OR REPLACE ] AGGREGATE name ( [ argmode ] [ argname ] arg_data_type [ , ... ] ) (
    SFUNC = sfunc,
    STYPE = state_data_type
    [ , SSPACE = state_data_size ]
    [ , FINALFUNC = ffunc ]
    [ , FINALFUNC_EXTRA ]
    [ , FINALFUNC_MODIFY = { READ_ONLY | SHAREABLE | READ_WRITE } ]
    [ , COMBINEFUNC = combinefunc ]
    [ , SERIALFUNC = serialfunc ]
    [ , DESERIALFUNC = deserialfunc ]
    [ , INITCOND = initial_condition ]
    [ , MSFUNC = msfunc ]
    [ , MINVFUNC = minvfunc ]
    [ , MSTYPE = mstate_data_type ]
    [ , MSSPACE = mstate_data_size ]
    [ , MFINALFUNC = mffunc ]
    [ , MFINALFUNC_EXTRA ]
    [ , MFINALFUNC_MODIFY = { READ_ONLY | SHAREABLE | READ_WRITE } ]
    [ , MINITCOND = minitial_condition ]
    [ , SORTOP = sort_operator ]
    [ , PARALLEL = { SAFE | RESTRICTED | UNSAFE } ]
)

CREATE [ OR REPLACE ] AGGREGATE name ( [ [ argmode ] [ argname ] arg_data_type [ , ... ] ]
                        ORDER BY [ argmode ] [ argname ] arg_data_type [ , ... ] ) (
    SFUNC = sfunc,
    STYPE = state_data_type
    [ , SSPACE = state_data_size ]
    [ , FINALFUNC = ffunc ]
    [ , FINALFUNC_EXTRA ]
    [ , FINALFUNC_MODIFY = { READ_ONLY | SHAREABLE | READ_WRITE } ]
    [ , INITCOND = initial_condition ]
    [ , PARALLEL = { SAFE | RESTRICTED | UNSAFE } ]
    [ , HYPOTHETICAL ]
)

or the old syntax

CREATE [ OR REPLACE ] AGGREGATE name (
    BASETYPE = base_type,
    SFUNC = sfunc,
    STYPE = state_data_type
    [ , SSPACE = state_data_size ]
    [ , FINALFUNC = ffunc ]
    [ , FINALFUNC_EXTRA ]
    [ , FINALFUNC_MODIFY = { READ_ONLY | SHAREABLE | READ_WRITE } ]
    [ , COMBINEFUNC = combinefunc ]
    [ , SERIALFUNC = serialfunc ]
    [ , DESERIALFUNC = deserialfunc ]
    [ , INITCOND = initial_condition ]
    [ , MSFUNC = msfunc ]
    [ , MINVFUNC = minvfunc ]
    [ , MSTYPE = mstate_data_type ]
    [ , MSSPACE = mstate_data_size ]
    [ , MFINALFUNC = mffunc ]
    [ , MFINALFUNC_EXTRA ]
    [ , MFINALFUNC_MODIFY = { READ_ONLY | SHAREABLE | READ_WRITE } ]
    [ , MINITCOND = minitial_condition ]
    [ , SORTOP = sort_operator ]
)
```

## Descrição

`CREATE AGGREGATE` define uma nova função agregada. `CREATE OR REPLACE AGGREGATE` irá definir uma nova função agregada ou substituir uma definição existente. Algumas funções agregadas básicas e comumente usadas estão incluídas na distribuição; elas são documentadas em [Seção 9.21][(functions-aggregate.md "9.21. Aggregate Functions")]. Se se definir novos tipos ou precisar de uma função agregada que não esteja já fornecida, então `CREATE AGGREGATE` pode ser usado para fornecer as características desejadas.

Ao substituir uma definição existente, os tipos de argumentos, o tipo de resultado e o número de argumentos diretos não podem ser alterados. Além disso, a nova definição deve ser do mesmo tipo (agregado agregado ordinário, agregado de conjunto ordenado ou agregado de conjunto hipotético) que a antiga.

Se um nome de esquema for fornecido (por exemplo, `CREATE AGGREGATE myschema.myagg ...`) então a função agregada é criada no esquema especificado. Caso contrário, ela é criada no esquema atual.

Uma função agregada é identificada pelo seu nome e pelo(s) tipo(s) de dados de entrada. Duas funções agregadas no mesmo esquema podem ter o mesmo nome se operarem em tipos de entrada diferentes. O nome e o(s) tipo(s) de dados de entrada de uma função agregada também devem ser distintos do nome e do(s) tipo(s) de dados de entrada de todas as funções comuns no mesmo esquema. Esse comportamento é idêntico ao sobrecarga de nomes de funções comuns (consulte [CREATE FUNCTION][(sql-createfunction.md "CREATE FUNCTION")]).

Uma função agregada simples é composta por uma ou duas funções comuns: uma função de transição de estado *`sfunc`* e uma função de cálculo final opcional *`ffunc`*. Elas são usadas da seguinte forma:

```
sfunc( internal-state, next-data-values ) ---> next-internal-state
ffunc( internal-state ) ---> aggregate-value
```

O PostgreSQL cria uma variável temporária do tipo de dados *`stype`* para armazenar o estado interno atual do agregado. Em cada linha de entrada, os(s) valor(es) do argumento do agregado são calculados e a função de transição de estado é invocada com o valor do estado atual e o(s) novo(s) valor(es) do argumento para calcular um novo valor de estado interno. Após todos os registros terem sido processados, a função final é invocada uma vez para calcular o valor de retorno do agregado. Se não houver função final, o valor do estado final é retornado como está.

Uma função agregada pode fornecer uma condição inicial, ou seja, um valor inicial para o valor do estado interno. Isso é especificado e armazenado no banco de dados como um valor do tipo `text`, mas deve ser uma representação externa válida de uma constante do tipo de dados do valor do estado. Se não for fornecida, o valor do estado começa como nulo.

Se a função de transição de estado for declarada como "strict", ela não pode ser chamada com entradas nulos. Com uma função desse tipo, a execução agregada se comporta da seguinte forma. As linhas com quaisquer valores de entrada nulos são ignoradas (a função não é chamada e o valor do estado anterior é retido). Se o valor inicial do estado for nulo, então, na primeira linha com todos os valores de entrada não nulos, o valor do primeiro argumento substitui o valor do estado, e a função de transição é invocada em cada linha subsequente com todos os valores de entrada não nulos. Isso é útil para implementar agregados como `max`. Note que esse comportamento só está disponível quando *`state_data_type`* é o mesmo que o primeiro *`arg_data_type`*. Quando esses tipos são diferentes, você deve fornecer uma condição inicial não nula ou usar uma função de transição não strict.

Se a função de transição de estado não for estrita, ela será chamada incondicionalmente em cada linha de entrada e deve lidar com entradas nulos e valores de estado nulos por si mesma. Isso permite que o autor do agregado tenha controle total sobre o tratamento de valores nulos pelo agregado.

Se a função final for declarada como "strict", ela não será chamada quando o valor do estado final for nulo; em vez disso, um resultado nulo será retornado automaticamente. (Claro que isso é apenas o comportamento normal das funções strictas.) Em qualquer caso, a função final tem a opção de retornar um valor nulo. Por exemplo, a função final para `avg` retorna nulo quando vê que havia zero linhas de entrada.

Às vezes, é útil declarar que a função final não só recebe o valor do estado, mas também parâmetros adicionais correspondentes aos valores de entrada do agregado. A principal razão para fazer isso é se a função final for polimórfica e o tipo de dados do valor do estado não seria adequado para determinar o tipo do resultado. Esses parâmetros adicionais são sempre passados como NULL (e, portanto, a função final não deve ser estrita quando a opção `FINALFUNC_EXTRA` é usada), mas, não obstante, são parâmetros válidos. A função final poderia, por exemplo, utilizar `get_fn_expr_argtype` para identificar o tipo de argumento real na chamada atual.

Um agregado pode, opcionalmente, suportar o modo *agregado móvel*, conforme descrito em [Seção 36.12.1][(xaggr.md#XAGGR-MOVING-AGGREGATES "36.12.1. Moving-Aggregate Mode")]. Isso requer a especificação dos parâmetros `MSFUNC`, `MINVFUNC` e `MSTYPE`, e opcionalmente dos parâmetros `MSSPACE`, `MFINALFUNC`, `MFINALFUNC_EXTRA`, `MFINALFUNC_MODIFY` e `MINITCOND`. Exceto para `MINVFUNC`, esses parâmetros funcionam como os parâmetros correspondentes de agregado simples sem `M`; eles definem uma implementação separada do agregado que inclui uma função de transição inversa.

A sintaxe com `ORDER BY` na lista de parâmetros cria um tipo especial de agregado chamado *agregado de conjunto ordenado*; ou se `HYPOTHETICAL` for especificado, então um *agregado de conjunto hipotético* é criado. Esses agregados operam sobre grupos de valores ordenados de maneiras dependentes da ordem, de modo que a especificação de uma ordem de classificação de entrada é uma parte essencial de uma chamada. Além disso, eles podem ter argumentos *diretos*, que são argumentos que são avaliados apenas uma vez por agregação em vez de uma vez por linha de entrada. Agregados de conjunto hipotético são uma subclasse de agregados de conjunto ordenado nos quais alguns dos argumentos diretos são obrigatórios para corresponder, em número e tipos de dados, às colunas dos argumentos agregados. Isso permite que os valores desses argumentos diretos sejam adicionados à coleção de linhas de entrada de agregação como uma linha "hipotética" adicional.

Um agregado pode, opcionalmente, suportar *agregamento parcial*, conforme descrito em [Seção 36.12.4][(xaggr.md#XAGGR-PARTIAL-AGGREGATES "36.12.4. Partial Aggregation")]. Isso requer a especificação do parâmetro `COMBINEFUNC`. Se o *`state_data_type`* for `internal`, geralmente também é apropriado fornecer os parâmetros `SERIALFUNC` e `DESERIALFUNC` para que a agregação paralela seja possível. Observe que o agregado também deve ser marcado `PARALLEL SAFE` para habilitar a agregação paralela.

Os agregados que se comportam como `MIN` ou `MAX` podem, às vezes, ser otimizados ao examinar um índice em vez de digitalizar cada linha de entrada. Se esse agregado puder ser otimizado dessa forma, indique-o especificando um *operador de ordenação*. O requisito básico é que o agregado deve produzir o primeiro elemento na ordem de ordenação induzida pelo operador; em outras palavras:

```
SELECT agg(col) FROM tab;
```

deve ser equivalente a:

```
SELECT col FROM tab ORDER BY col USING sortop LIMIT 1;
```

Outras suposições são que o agregado ignora entradas nulos e que ele entrega um resultado nulo se e somente se não houvesse entradas não nulos. Normalmente, o operador `<` de um tipo de dados é o operador de classificação adequado para `MIN`, e `>` é o operador de classificação adequado para `MAX`. Note que a otimização nunca terá efeito real a menos que o operador especificado seja o membro da estratégia “menor que” ou “maior que” de uma classe de operador de índice de árvore B.

Para poder criar uma função agregada, você deve ter privilégio `USAGE` nos tipos de argumento, o(s) tipo(s) de estado e o tipo de retorno, bem como privilégio `EXECUTE` nas funções de suporte.

## Parâmetros

*`name`*: O nome (opcionalmente qualificado por esquema) da função agregada a ser criada.

*`argmode`*: O modo de um argumento: `IN` ou `VARIADIC`. (As funções agregadas não suportam argumentos `OUT`. Se omitido, o padrão é `IN`. Apenas o último argumento pode ser marcado `VARIADIC`.

*`argname`*: O nome de um argumento. Este é atualmente útil apenas para fins de documentação. Se omitido, o argumento não tem nome.

*`arg_data_type`*: Um tipo de dados de entrada sobre o qual essa função agregada opera. Para criar uma função agregada de argumento zero, escreva `*` no lugar da lista de especificações de argumento. (Um exemplo de tal agregação é `count(*)`.)

*`base_type`*: Na antiga sintaxe para `CREATE AGGREGATE`, o tipo de dados de entrada é especificado por um parâmetro `basetype` em vez de ser escrito ao lado do nome do agregado. Note que essa sintaxe permite apenas um parâmetro de entrada. Para definir uma função agregada de argumento zero com essa sintaxe, especifique o `basetype` como `"ANY"` (não `*`). Agregados de conjuntos ordenados não podem ser definidos com a sintaxe antiga.

*`sfunc`*: O nome da função de transição de estado a ser chamada para cada linha de entrada. Para uma função agregada *`N`*-argument normal, o *`sfunc`* deve receber *`N`*+1 argumentos, sendo o primeiro do tipo *`state_data_type`* e os demais correspondendo ao(s) tipo(s) de dados de entrada declarados do agregado. A função deve retornar um valor do tipo *`state_data_type`*. Esta função recebe o valor do estado atual e o(s) valor(es) de dados de entrada atual(is), e retorna o próximo valor de estado.

Para agregados de conjunto ordenado (incluindo conjuntos hipotéticos), a função de transição de estado recebe apenas o valor do estado atual e os argumentos agregados, não os argumentos diretos. Caso contrário, é o mesmo.

*`state_data_type`*: O tipo de dados para o valor do estado do agregado.

*`state_data_size`*: O tamanho médio aproximado (em bytes) do valor do estado do agregado. Se este parâmetro for omitido ou for zero, uma estimativa padrão é usada com base no *`state_data_type`*. O planejador usa esse valor para estimar a memória necessária para uma consulta de agregado agrupado.

*`ffunc`*: O nome da função final chamada para calcular o resultado do agregado após todas as linhas de entrada terem sido percorridas. Para um agregado normal, essa função deve receber um único argumento do tipo *`state_data_type`*. O tipo de dados de retorno do agregado é definido como o tipo de retorno dessa função. Se *`ffunc`* não for especificado, então o valor do estado final é usado como resultado do agregado, e o tipo de retorno é *`state_data_type`*.

Para agregados de conjunto ordenado (incluindo conjuntos hipotéticos), a função final recebe não apenas o valor do estado final, mas também os valores de todos os argumentos diretos.

Se `FINALFUNC_EXTRA` for especificado, além do valor do estado final e de quaisquer argumentos diretos, a função final recebe valores NULL adicionais correspondentes aos argumentos regulares (agregados) do agregado. Isso é principalmente útil para permitir a resolução correta do tipo do resultado do agregado quando um agregado polimórfico está sendo definido.

`FINALFUNC_MODIFY` = { `READ_ONLY` | `SHAREABLE` | `READ_WRITE` : Esta opção especifica se a função final é uma função pura que não modifica seus argumentos. `READ_ONLY` indica que não o faz; os outros dois valores indicam que ela pode alterar o valor do estado de transição. Consulte [Notas](sql-createaggregate.md#SQL-CREATEAGGREGATE-NOTES "Notes") abaixo para mais detalhes. O padrão é `READ_ONLY`, exceto para agregados de conjuntos ordenados, para os quais o padrão é `READ_WRITE`.

*`combinefunc`*: A função *`combinefunc`* pode ser especificada opcionalmente para permitir que a função agregada suporte agregação parcial. Se fornecida, a *`combinefunc`* deve combinar dois valores de *`state_data_type`*, cada um contendo o resultado da agregação sobre algum subconjunto dos valores de entrada, para produzir um novo *`state_data_type`* que representa o resultado da agregação sobre ambos os conjuntos de entradas. Esta função pode ser considerada como uma *`sfunc`*, onde, em vez de agir sobre uma linha de entrada individual e adicioná-la ao estado agregado em execução, adiciona outro estado agregado ao estado em execução.

O *`combinefunc`* deve ser declarado para receber dois argumentos do *`state_data_type`* e retornar um valor do *`state_data_type`*. Opcionalmente, essa função pode ser “estricta”. Nesse caso, a função não será chamada quando qualquer um dos estados de entrada for nulo; o outro estado será considerado o resultado correto.

Para funções agregadas cujo *`state_data_type`* é `internal`, o *`combinefunc`* não deve ser estrito. Neste caso, o *`combinefunc`* deve garantir que os estados nulos sejam tratados corretamente e que o estado sendo retornado seja armazenado corretamente no contexto da memória agregada.

*`serialfunc`*: Uma função agregada cuja *`state_data_type`* é `internal` pode participar em agregação paralela apenas se tiver uma função *`serialfunc`*, que deve serializar o estado agregado em um valor de `bytea` para transmissão a outro processo. Esta função deve receber um único argumento do tipo `internal` e retornar tipo `bytea`. Também é necessária uma *`deserialfunc`* correspondente.

*`deserialfunc`*: Deserialize um estado agregado serializado anteriormente de volta para *`state_data_type`. Esta função deve receber dois argumentos do tipo `bytea` e `internal`, e produzir um resultado do tipo `internal`. (Nota: o segundo argumento, `internal`, é não utilizado, mas é necessário por razões de segurança do tipo.)

*`initial_condition`*: O valor inicial do estado. Isso deve ser uma constante de string na forma aceita para o tipo de dados *`state_data_type`*. Se não especificado, o valor do estado começa como nulo.

*`msfunc`*: O nome da função de transição de estado para frente que deve ser chamada para cada linha de entrada no modo de agregação em movimento. Isso é exatamente como a função de transição regular, exceto que seu primeiro argumento e resultado são do tipo *`mstate_data_type`*, que pode ser diferente de *`state_data_type`*.

*`minvfunc`*: O nome da função de transição inversa a ser usada no modo de movimento de agregados. Esta função tem os mesmos tipos de argumentos e resultados que *`msfunc`*, mas é usada para remover um valor do estado agregado atual, em vez de adicioná-lo. A função de transição inversa deve ter o mesmo atributo de estrícção que a função de transição de estado para a frente.

*`mstate_data_type`*: O tipo de dados para o valor do estado do agregado, quando se usa o modo de agregado móvel.

*`mstate_data_size`*: O tamanho médio aproximado (em bytes) do valor do estado do agregado, quando se usa o modo de agregado móvel. Isso funciona da mesma forma que *`state_data_size`*.

*`mffunc`*: O nome da função final chamada para calcular o resultado do agregado após todas as linhas de entrada terem sido percorridas, quando o modo de agregação móvel é usado. Isso funciona da mesma forma que *`ffunc`*, exceto que o tipo do primeiro argumento é *`mstate_data_type`* e argumentos fictícios adicionais são especificados escrevendo `MFINALFUNC_EXTRA`. O tipo do resultado do agregado determinado por *`mffunc`* ou *`mstate_data_type`* deve corresponder ao determinado pela implementação regular do agregado.

`MFINALFUNC_MODIFY` = { `READ_ONLY` | `SHAREABLE` | `READ_WRITE` }: Esta opção é semelhante a `FINALFUNC_MODIFY`, mas descreve o comportamento da função final agregada em movimento.

*`minitial_condition`*: O ajuste inicial para o valor do estado, quando se usa o modo de agregação móvel. Isso funciona da mesma forma que *`initial_condition`*.

*`sort_operator`*: O operador de ordenação associado a um agregado semelhante a `MIN` ou `MAX`. Este é apenas um nome de operador (possivelmente qualificado pelo esquema). Assume-se que o operador tenha os mesmos tipos de dados de entrada que o agregado (que deve ser um agregado normal de um argumento).

`PARALLEL =` { `SAFE` | `RESTRICTED` | `UNSAFE` : Os significados de `PARALLEL SAFE`, `PARALLEL RESTRICTED` e `PARALLEL UNSAFE` são os mesmos que em [`CREATE FUNCTION`](sql-createfunction.md "CREATE FUNCTION"). Um agregado não será considerado para paralelização se estiver marcado `PARALLEL UNSAFE` (que é o padrão!) ou `PARALLEL RESTRICTED`. Note que as marcações de segurança paralela das funções de suporte do agregado não são consultadas pelo planejador, apenas a marcação do próprio agregado.

`HYPOTHETICAL`: Apenas para agregados de conjuntos ordenados, esta bandeira especifica que os argumentos do agregado devem ser processados de acordo com os requisitos para agregados de conjuntos hipotéticos: ou seja, os últimos argumentos diretos devem corresponder aos tipos de dados dos argumentos agregados (`WITHIN GROUP`). A bandeira `HYPOTHETICAL` não tem efeito no comportamento em tempo de execução, apenas na resolução em tempo de análise dos tipos de dados e colatitudes dos argumentos do agregado.

Os parâmetros de `CREATE AGGREGATE` podem ser escritos em qualquer ordem, não apenas na ordem ilustrada acima.

## Notas

Nos parâmetros que especificam os nomes das funções de suporte, você pode escrever um nome de esquema, se necessário, por exemplo, `SFUNC = public.sum`. No entanto, não escreva tipos de argumento lá — os tipos de argumento das funções de suporte são determinados a partir de outros parâmetros.

Normalmente, espera-se que as funções do PostgreSQL sejam funções verdadeiras que não modifiquem seus valores de entrada. No entanto, uma função de transição agregada, *quando usada no contexto de um agregado*, é permitida para enganar e modificar seu argumento de estado de transição no local. Isso pode proporcionar benefícios substanciais de desempenho em comparação com a criação de uma cópia fresca do estado de transição a cada vez.

Da mesma forma, embora normalmente se espere que uma função final agregada não modifique seus valores de entrada, às vezes é impraticável evitar modificar o argumento do estado de transição. Esse comportamento deve ser declarado usando o parâmetro `FINALFUNC_MODIFY`. O valor `READ_WRITE` indica que a função final modifica o estado de transição de maneiras não especificadas. Esse valor impede o uso do agregado como uma função de janela e também impede a fusão de estados de transição para chamadas agregadas que compartilham os mesmos valores de entrada e funções de transição. O valor `SHAREABLE` indica que a função de transição não pode ser aplicada após a função final, mas múltiplas chamadas de função final podem ser realizadas no valor do estado de transição final. Esse valor impede o uso do agregado como uma função de janela, mas permite a fusão de estados de transição. (Ou seja, a otimização de interesse aqui não é aplicar a mesma função final repetidamente, mas aplicar diferentes funções finais ao mesmo valor do estado de transição final. Isso é permitido desde que nenhuma das funções finais seja marcada `READ_WRITE`.).

Se um agregado suportar o modo de agregado móvel, ele melhorará a eficiência do cálculo quando o agregado é usado como uma função de janela para uma janela com início de quadro móvel (ou seja, um modo de início de quadro diferente de `UNBOUNDED PRECEDING`). Conceitualmente, a função de transição para frente adiciona valores de entrada ao estado do agregado quando eles entram no quadro da janela da parte inferior, e a função de transição inversa os remove novamente quando eles saem do quadro na parte superior. Portanto, quando os valores são removidos, eles são sempre removidos na mesma ordem em que foram adicionados. Sempre que a função de transição inversa é invocada, ela receberá, assim, o valor(es) do argumento adicionado(s) mais antigo(s). A função de transição inversa pode assumir que pelo menos uma linha permanecerá no estado atual após remover a linha mais antiga. (Quando isso não seria o caso, o mecanismo da função de janela simplesmente inicia uma nova agregação, em vez de usar a função de transição inversa.)

A função de transição para a frente para o modo de agregação móvel não é permitida para retornar NULL como o novo valor do estado. Se a função de transição inversa retornar NULL, isso é considerado uma indicação de que a função inversa não pode reverter o cálculo do estado para este entrada em particular, e, portanto, o cálculo do agregado será feito novamente do zero para a posição atual de início do quadro. Esta convenção permite que o modo de agregação móvel seja usado em situações em que existem alguns casos infrequentes que são impraticáveis para reverter fora do valor do estado em execução.

Se não for fornecida uma implementação de agregação em movimento, o agregado ainda pode ser usado com quadros em movimento, mas o PostgreSQL recomporá toda a agregação sempre que o início do quadro se mover. Observe que, independentemente de o agregado suportar o modo de agregação em movimento, o PostgreSQL pode lidar com o fim de um quadro em movimento sem recalcular; isso é feito continuando a adicionar novos valores ao estado do agregado. É por isso que o uso de um agregado como uma função de janela requer que a função final seja somente de leitura: ela não deve danificar o valor do estado do agregado, para que a agregação possa ser continuada mesmo após um valor de resultado de agregação ter sido obtido para um conjunto de limites de quadro.

A sintaxe para agregados de conjuntos ordenados permite que `VARIADIC` seja especificado tanto para o último parâmetro direto quanto para o último parâmetro agregado (`WITHIN GROUP`). No entanto, a implementação atual restringe o uso de `VARIADIC` de duas maneiras. Primeiro, os agregados de conjuntos ordenados só podem usar `VARIADIC "any"`, não outros tipos de matriz variável. Segundo, se o último parâmetro direto for `VARIADIC "any"`, então pode haver apenas um parâmetro agregado e ele também deve ser `VARIADIC "any"`. (Na representação usada nos catálogos do sistema, esses dois parâmetros são reunidos em um único item `VARIADIC "any"`, uma vez que `pg_proc` não pode representar funções com mais de um parâmetro `VARIADIC`. Se o agregado for um agregado hipotético, os argumentos diretos que correspondem ao parâmetro `VARIADIC "any"` são os hipotéticos; quaisquer parâmetros anteriores representam argumentos diretos adicionais que não são obrigados a corresponder aos argumentos agregados.

Atualmente, os agregados de conjunto ordenado não precisam suportar o modo de agregado móvel, uma vez que não podem ser usados como funções de janela.

A agregação parcial (incluindo a agregação paralela) atualmente não é suportada para agregados de conjuntos ordenados. Além disso, ela nunca será usada para chamadas de agregação que incluem cláusulas `DISTINCT` ou `ORDER BY`, uma vez que essas semânticas não podem ser suportadas durante a agregação parcial.

## Exemplos

Veja [Seção 36.12](xaggr.md "36.12. User-Defined Aggregates").

## Compatibilidade

`CREATE AGGREGATE` é uma extensão de linguagem do PostgreSQL. O padrão SQL não prevê funções agregadas definidas pelo usuário.

## Veja também

[ALTERA AGREGADO](sql-alteraggregate.md "ALTER AGGREGATE"), [DROP AGREGADO](sql-dropaggregate.md "DROP AGGREGATE")