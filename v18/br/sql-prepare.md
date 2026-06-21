## PREPARE

PREPARE — prepare uma declaração para execução

## Sinopse

```
PREPARE name [ ( data_type [, ...] ) ] AS statement
```

## Descrição

`PREPARE` cria uma declaração preparada. Uma declaração preparada é um objeto do lado do servidor que pode ser usado para otimizar o desempenho. Quando a declaração `PREPARE` é executada, a declaração especificada é analisada, analisada e reescrita. Quando um comando `EXECUTE` é emitido subsequentemente, a declaração preparada é planejada e executada. Essa divisão do trabalho evita o trabalho repetitivo de análise de análise, permitindo que o plano de execução dependa dos valores específicos dos parâmetros fornecidos.

As declarações preparadas podem receber parâmetros: valores que são substituídos na declaração quando ela é executada. Ao criar a declaração preparada, consulte os parâmetros por posição, usando `$1`, `$2`, etc. Uma lista correspondente dos tipos de dados dos parâmetros pode ser especificada opcionalmente. Quando o tipo de dados de um parâmetro não é especificado ou é declarado como `unknown`, o tipo é inferido do contexto em que o parâmetro é referenciado pela primeira vez (se possível). Ao executar a declaração, especifique os valores reais desses parâmetros na declaração `EXECUTE`. Consulte [EXECUTAR](sql-execute.md "EXECUTE") para obter mais informações sobre isso.

As declarações preparadas só duram durante a sessão atual da base de dados. Quando a sessão termina, a declaração preparada é esquecida, portanto, ela deve ser recriada antes de ser usada novamente. Isso também significa que uma única declaração preparada não pode ser usada por vários clientes simultâneos da base de dados; no entanto, cada cliente pode criar sua própria declaração preparada para usar. As declarações preparadas podem ser limpas manualmente usando o comando `DEALLOCATE`(sql-deallocate.md "DEALLOCATE").

As declarações preparadas têm uma vantagem de desempenho potencialmente maior quando uma única sessão está sendo usada para executar um grande número de declarações semelhantes. A diferença de desempenho será particularmente significativa se as declarações forem complexas de planejar ou reescrever, por exemplo, se a consulta envolver uma junção de muitas tabelas ou exigir a aplicação de várias regras. Se a declaração for relativamente simples de planejar e reescrever, mas relativamente cara de executar, a vantagem de desempenho das declarações preparadas será menos notável.

## Parâmetros

*`name`*: Um nome arbitrário dado a esta declaração preparada em particular. Deve ser único dentro de uma única sessão e, subsequentemente, é usado para executar ou realocar uma declaração preparada anteriormente.

*`data_type`*: O tipo de dados de um parâmetro para a declaração preparada. Se o tipo de dados de um parâmetro específico não for especificado ou for especificado como `unknown`, ele será inferido do contexto em que o parâmetro é referido pela primeira vez. Para referenciar os parâmetros na própria declaração preparada, use `$1`, `$2`, etc.

*`statement`*: Qualquer declaração `SELECT`, `INSERT`, `UPDATE`, `DELETE`, `MERGE` ou `VALUES`.

## Notas

Uma declaração preparada pode ser executada com um *plano genérico* ou um *plano personalizado*. Um plano genérico é o mesmo em todas as execuções, enquanto um plano personalizado é gerado para uma execução específica usando os valores dos parâmetros fornecidos naquela chamada. O uso de um plano genérico evita o overhead de planejamento, mas, em algumas situações, um plano personalizado será muito mais eficiente para execução, porque o planejador pode utilizar o conhecimento dos valores dos parâmetros. (Claro, se a declaração preparada não tiver parâmetros, então isso não é relevante e um plano genérico é sempre usado.)

Por padrão (ou seja, quando [plan_cache_mode][(runtime-config-query.md#GUC-PLAN-CACHE-MODE)] está definido como `auto`), o servidor escolherá automaticamente se deve usar um plano genérico ou um plano personalizado para uma declaração preparada que tenha parâmetros. A regra atual para isso é que as cinco primeiras execuções são feitas com planos personalizados e o custo estimado médio desses planos é calculado. Em seguida, um plano genérico é criado e seu custo estimado é comparado ao custo médio do plano personalizado. As execuções subsequentes usam o plano genérico se seu custo não for tão alto quanto o custo médio do plano personalizado para que a replanejamento repetido pareça preferível.

Essa heurística pode ser ignorada, forçando o servidor a usar planos genéricos ou personalizados, definindo `plan_cache_mode` para `force_generic_plan` ou `force_custom_plan`, respectivamente. Essa configuração é principalmente útil se a estimativa de custo do plano genérico estiver mal definida por algum motivo, permitindo que ele seja escolhido, mesmo que seu custo real seja muito maior do que o de um plano personalizado.

Para examinar o plano de consulta que o PostgreSQL está usando para uma declaração preparada, use `EXPLAIN`(sql-explain.md "EXPLAIN"), por exemplo.

```
EXPLAIN EXECUTE name(parameter_values);
```

Se um plano genérico estiver em uso, ele conterá símbolos de parâmetros `$n`, enquanto um plano personalizado terá os valores de parâmetros fornecidos substituídos nele.

Para mais informações sobre o planejamento de consultas e as estatísticas coletadas pelo PostgreSQL para esse propósito, consulte a documentação do [ANALYZE][(sql-analyze.md "ANALYZE")].

Embora o principal objetivo de uma declaração preparada seja evitar a análise e o planejamento repetidos da declaração, o PostgreSQL forçará a reanálise e o replanejamento da declaração antes de usá-la sempre que os objetos do banco de dados utilizados na declaração tenham sofrido mudanças definicionais (DDL) ou suas estatísticas do planejador tenham sido atualizadas desde o uso anterior da declaração preparada. Além disso, se o valor de [search_path][(runtime-config-client.md#GUC-SEARCH-PATH)] mudar de uma utilização para a próxima, a declaração será reanalisada usando o novo `search_path`. (Esse comportamento é novo a partir do PostgreSQL 9.3.) Essas regras utilizam uma declaração preparada semanticamente quase equivalente a submeter novamente o mesmo texto da consulta, mas com um benefício de desempenho se nenhuma definição de objeto for alterada, especialmente se o melhor plano permanecer o mesmo em todas as utilizações. Um exemplo de um caso em que a equivalência semântica não é perfeita é que, se a declaração se referir a uma tabela por um nome não qualificado, e então uma nova tabela do mesmo nome seja criada em um esquema que aparece anteriormente no `search_path`, não ocorrerá reanálise automática, uma vez que nenhum objeto utilizado na declaração foi alterado. No entanto, se alguma outra mudança forçar uma reanálise, a nova tabela será referenciada em utilizações subsequentes.

Você pode ver todas as declarações preparadas disponíveis na sessão, fazendo uma consulta à visão do sistema `pg_prepared_statements`(view-pg-prepared-statements.md "53.16. pg_prepared_statements").

## Exemplos

Crie uma declaração preparada para uma declaração `INSERT` e, em seguida, execute-a:

```
PREPARE fooplan (int, text, bool, numeric) AS
    INSERT INTO foo VALUES($1, $2, $3, $4);
EXECUTE fooplan(1, 'Hunter Valley', 't', 200.00);
```

Crie uma declaração preparada para uma declaração `SELECT` e, em seguida, execute-a:

```
PREPARE usrrptplan (int) AS
    SELECT * FROM users u, logs l WHERE u.usrid=$1 AND u.usrid=l.usrid
    AND l.date = $2;
EXECUTE usrrptplan(1, current_date);
```

Neste exemplo, o tipo de dados do segundo parâmetro não é especificado, então ele é inferido pelo contexto em que `$2` é usado.

## Compatibilidade

O padrão SQL inclui uma declaração `PREPARE`, mas ela só deve ser usada em SQL embutido. Esta versão da declaração `PREPARE` também usa uma sintaxe um pouco diferente.

## Veja também

[DEALLOCATE](sql-deallocate.md "DEALLOCATE"), [EXECUTAR](sql-execute.md "EXECUTE")