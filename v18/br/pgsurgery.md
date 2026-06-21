## F.34. pg_surgery — realizar cirurgia de baixo nível em dados de relação [#](#PGSURGERY)

* [F.34.1. Funções](pgsurgery.md#PGSURGERY-FUNCS)
* [F.34.2. Autores](pgsurgery.md#PGSURGERY-AUTHORS)

O módulo `pg_surgery` oferece várias funções para realizar cirurgias em uma relação danificada. Essas funções são inseguras por design e, ao usá-las, você pode corromper (ou corromper ainda mais) seu banco de dados. Por exemplo, essas funções podem ser facilmente usadas para tornar uma tabela inconsistente com seus próprios índices, causar violações de restrições `UNIQUE` ou `FOREIGN KEY` ou até mesmo tornar tuplas visíveis que, ao serem lidas, causarão um crash no servidor do banco de dados. Elas devem ser usadas com grande cautela e apenas como último recurso.

### F.34.1. Funções [#](#PGSURGERY-FUNCS)

`heap_force_kill(regclass, tid[]) returns void`: As linhas de ponteiros "usadas" no `heap_force_kill` são marcadas como "morta" sem examinar os tuplos. O uso pretendido desta função é remover, de forma forçada, os tuplos que não são acessíveis de outra forma. Por exemplo:

```
test=> select * from t1 where ctid = '(0, 1)'; ERROR:  could not access status of transaction 4007513275 DETAIL:  Could not open file "pg_xact/0EED": No such file or directory.

test=# select heap_force_kill('t1'::regclass, ARRAY['(0, 1)']::tid[]); heap_force_kill -----------------

(1 row)

test=# select * from t1 where ctid = '(0, 1)'; (0 rows)
```

`heap_force_freeze(regclass, tid[]) returns void`: `heap_force_freeze` marca tuplas como congeladas sem examinar os dados da tupla. O uso pretendido desta função é tornar tuplas acessíveis que são inacessíveis devido a informações de visibilidade corrompidas, ou que impedem que a tabela seja limpa com sucesso devido a informações de visibilidade corrompidas. Por exemplo:

```
test=> vacuum t1; ERROR:  found xmin 507 from before relfrozenxid 515 CONTEXT:  while scanning block 0 of relation "public.t1"

test=# select ctid from t1 where xmin = 507; ctid ------- (0,3) (1 row)

test=# select heap_force_freeze('t1'::regclass, ARRAY['(0, 3)']::tid[]); heap_force_freeze -------------------

(1 row)

test=# select ctid from t1 where xmin = 2; ctid ------- (0,3) (1 row)
```

### F.34.2. Autores [#](#PGSURGERY-AUTHORS)

Ashutosh Sharma `<ashu.coek88@gmail.com>`