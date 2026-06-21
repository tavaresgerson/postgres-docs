## F.3. auto_explain — registro dos planos de execução de consultas lentas [#](#AUTO-EXPLAIN)

* [F.3.1. Parâmetros de Configuração](auto-explain.md#AUTO-EXPLAIN-CONFIGURATION-PARAMETERS)
* [F.3.2. Exemplo](auto-explain.md#AUTO-EXPLAIN-EXAMPLE)
* [F.3.3. Autor](auto-explain.md#AUTO-EXPLAIN-AUTHOR)

O módulo `auto_explain` fornece uma maneira de registrar automaticamente os planos de execução de instruções lentas, sem precisar executar manualmente [EXPLAIN][(sql-explain.md "EXPLAIN")]. Isso é especialmente útil para localizar consultas não otimizadas em aplicações grandes.

O módulo não oferece funções acessíveis por SQL. Para usá-lo, basta carregá-lo no servidor. Você pode carregá-lo em uma sessão individual:

```
LOAD 'auto_explain';
```

(Você deve ser um superusuário para fazer isso.) O uso mais típico é pré-carregá-lo em algumas ou todas as sessões, incluindo `auto_explain` em [session_preload_libraries](runtime-config-client.md#GUC-SESSION-PRELOAD-LIBRARIES) ou [shared_preload_libraries](runtime-config-client.md#GUC-SHARED-PRELOAD-LIBRARIES) em `postgresql.conf`. Em seguida, você pode rastrear consultas inesperadamente lentas, independentemente de quando elas ocorrem. Claro, há um custo adicional para isso.

### F.3.1. Parâmetros de Configuração [#](#AUTO-EXPLAIN-CONFIGURATION-PARAMETERS)

Existem vários parâmetros de configuração que controlam o comportamento do `auto_explain`. Observe que o comportamento padrão é não fazer nada, portanto, você deve definir pelo menos `auto_explain.log_min_duration` se quiser obter algum resultado.

`auto_explain.log_min_duration` (`integer`) [#](#AUTO-EXPLAIN-CONFIGURATION-PARAMETERS-LOG-MIN-DURATION): `auto_explain.log_min_duration` é o tempo mínimo de execução da declaração, em milissegundos, que fará com que o plano da declaração seja registrado. Definindo isso para `0`, todos os planos são registrados. `-1` (o padrão) desativa o registro dos planos. Por exemplo, se você definir isso para `250ms`, todas as declarações que demoram 250 ms ou mais serão registradas. Somente os usuários superusuários podem alterar essa configuração.

`auto_explain.log_parameter_max_length` (`integer`) [#](#AUTO-EXPLAIN-CONFIGURATION-PARAMETERS-LOG-PARAMETER-MAX-LENGTH): `auto_explain.log_parameter_max_length` controla o registro dos valores dos parâmetros de consulta. Um valor de `-1` (o padrão) registra os valores dos parâmetros na íntegra. `0` desativa o registro dos valores dos parâmetros. Um valor maior que zero truncata cada valor do parâmetro para quantos bytes. Somente os usuários superusuários podem alterar esta configuração.

`auto_explain.log_analyze` (`boolean`) [#](#AUTO-EXPLAIN-CONFIGURATION-PARAMETERS-LOG-ANALYZE): `auto_explain.log_analyze` faz com que a saída `EXPLAIN ANALYZE` seja impressa, em vez de apenas a saída `EXPLAIN`, quando um plano de execução é registrado. Este parâmetro está desativado por padrão. Somente os usuários superusuários podem alterar esta configuração.

### Nota

Quando este parâmetro está ativado, o temporizador por plano de nó ocorre para todas as declarações executadas, independentemente de elas rodarem o tempo suficiente para serem realmente registradas. Isso pode ter um impacto extremamente negativo no desempenho. Desativar `auto_explain.log_timing` melhora o custo de desempenho, no preço de obter menos informações.

`auto_explain.log_buffers` (`boolean`) [#](#AUTO-EXPLAIN-CONFIGURATION-PARAMETERS-LOG-BUFFERS): `auto_explain.log_buffers` controla se as estatísticas de uso de buffer são impressas quando um plano de execução é registrado; é equivalente à opção `BUFFERS` de `EXPLAIN`. Este parâmetro não tem efeito a menos que `auto_explain.log_analyze` esteja habilitado. Este parâmetro está desligado por padrão. Somente os usuários superusuários podem alterar esta configuração.

`auto_explain.log_wal` (`boolean`) [#](#AUTO-EXPLAIN-CONFIGURATION-PARAMETERS-LOG-WAL): `auto_explain.log_wal` controla se as estatísticas de uso do WAL são impressas quando um plano de execução é registrado; é equivalente à opção `WAL` de `EXPLAIN`. Este parâmetro não tem efeito a menos que `auto_explain.log_analyze` esteja habilitado. Este parâmetro está desativado por padrão. Somente os usuários superusuários podem alterar esta configuração.

`auto_explain.log_timing` (`boolean`) [#](#AUTO-EXPLAIN-CONFIGURATION-PARAMETERS-LOG-TIMING): `auto_explain.log_timing` controla se as informações de temporização por nó são impressas quando um plano de execução é registrado; é equivalente à opção `TIMING` de `EXPLAIN`. O custo adicional de ler repetidamente o relógio do sistema pode desacelerar significativamente as consultas em alguns sistemas, portanto, pode ser útil definir este parâmetro para desligado quando apenas as contagens reais de linhas, e não os tempos exatos, são necessárias. Este parâmetro não tem efeito a menos que `auto_explain.log_analyze` esteja habilitado. Este parâmetro está ativado por padrão. Somente os usuários superusuários podem alterar esta configuração.

`auto_explain.log_triggers` (`boolean`) [#](#AUTO-EXPLAIN-CONFIGURATION-PARAMETERS-LOG-TRIGGERS): As estatísticas de execução de gatilho são incluídas quando um plano de execução é registrado. Este parâmetro não tem efeito a menos que `auto_explain.log_analyze` esteja habilitado. Este parâmetro está desativado por padrão. Somente os usuários superusuários podem alterar esta configuração.

`auto_explain.log_verbose` (`boolean`) [#](#AUTO-EXPLAIN-CONFIGURATION-PARAMETERS-LOG-VERBOSE): `auto_explain.log_verbose` controla se detalhes verbais são impressos quando um plano de execução é registrado; é equivalente à opção `VERBOSE` de `EXPLAIN`. Este parâmetro está desativado por padrão. Somente superusuários podem alterar esta configuração.

`auto_explain.log_settings` (`boolean`) [#](#AUTO-EXPLAIN-CONFIGURATION-PARAMETERS-LOG-SETTINGS): `auto_explain.log_settings` controla se as informações sobre as opções de configuração modificadas são impressas quando um plano de execução é registrado. Apenas as opções que afetam o planejamento de consulta com valor diferente do valor padrão embutido são incluídas na saída. Este parâmetro está desativado por padrão. Somente os usuários superusuários podem alterar esta configuração.

`auto_explain.log_format` (`enum`) [#](#AUTO-EXPLAIN-CONFIGURATION-PARAMETERS-LOG-FORMAT): `auto_explain.log_format` seleciona o formato de saída `EXPLAIN` a ser utilizado. Os valores permitidos são `text`, `xml`, `json` e `yaml`. O padrão é texto. Somente usuários superusuários podem alterar esta configuração.

`auto_explain.log_level` (`enum`) [#](#AUTO-EXPLAIN-CONFIGURATION-PARAMETERS-LOG-LEVEL): `auto_explain.log_level` seleciona o nível de log no qual o auto_explain registrará o plano da consulta. Os valores válidos são `DEBUG5`, `DEBUG4`, `DEBUG3`, `DEBUG2`, `DEBUG1`, `INFO`, `NOTICE`, `WARNING` e `LOG`. O padrão é `LOG`. Somente os usuários superusuários podem alterar essa configuração.

`auto_explain.log_nested_statements` (`boolean`) [#](#AUTO-EXPLAIN-CONFIGURATION-PARAMETERS-LOG-NESTED-STATEMENTS): `auto_explain.log_nested_statements` faz com que as declarações aninhadas (declarações executadas dentro de uma função) sejam consideradas para registro. Quando está desativado, apenas os planos de consulta de nível superior são registrados. Este parâmetro está desativado por padrão. Somente os superusuários podem alterar esta configuração.

`auto_explain.sample_rate` (`real`) [#](#AUTO-EXPLAIN-CONFIGURATION-PARAMETERS-SAMPLE-RATE): `auto_explain.sample_rate` faz com que auto_explain explique apenas uma fração das declarações em cada sessão. O padrão é 1, o que significa explicar todas as consultas. Em caso de declarações aninhadas, todas serão explicadas ou nenhuma. Somente superusuários podem alterar essa configuração.

No uso comum, esses parâmetros são definidos em `postgresql.conf`, embora os usuários avançados possam alterá-los em tempo real dentro de suas próprias sessões. O uso típico pode ser:

```
# postgresql.conf
session_preload_libraries = 'auto_explain'

auto_explain.log_min_duration = '3s'
```

### F.3.2. Exemplo [#](#AUTO-EXPLAIN-EXAMPLE)

```
postgres=# LOAD 'auto_explain';
postgres=# SET auto_explain.log_min_duration = 0;
postgres=# SET auto_explain.log_analyze = true;
postgres=# SELECT count(*)
           FROM pg_class, pg_index
           WHERE oid = indrelid AND indisunique;
```

Isso pode produzir saída de log, como:

```
LOG:  duration: 3.651 ms  plan:
  Query Text: SELECT count(*)
              FROM pg_class, pg_index
              WHERE oid = indrelid AND indisunique;
  Aggregate  (cost=16.79..16.80 rows=1 width=0) (actual time=3.626..3.627 rows=1.00 loops=1)
    ->  Hash Join  (cost=4.17..16.55 rows=92 width=0) (actual time=3.349..3.594 rows=92.00 loops=1)
          Hash Cond: (pg_class.oid = pg_index.indrelid)
          ->  Seq Scan on pg_class  (cost=0.00..9.55 rows=255 width=4) (actual time=0.016..0.140 rows=255.00 loops=1)
          ->  Hash  (cost=3.02..3.02 rows=92 width=4) (actual time=3.238..3.238 rows=92.00 loops=1)
                Buckets: 1024  Batches: 1  Memory Usage: 4kB
                ->  Seq Scan on pg_index  (cost=0.00..3.02 rows=92 width=4) (actual time=0.008..3.187 rows=92.00 loops=1)
                      Filter: indisunique
```

### F.3.3. Autor [#](#AUTO-EXPLAIN-AUTHOR)

Takahiro Itagaki `<itagaki.takahiro@oss.ntt.co.jp>`