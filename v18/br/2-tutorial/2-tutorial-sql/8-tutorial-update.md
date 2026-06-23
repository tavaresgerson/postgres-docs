### 2.8. Atualizações [#](#TUTORIAL-UPDATE)

Você pode atualizar as linhas existentes usando o comando `UPDATE`. Suponha que você descubra que as leituras de temperatura estão todas erradas em 2 graus após 28 de novembro. Você pode corrigir os dados da seguinte forma:

```
UPDATE weather
    SET temp_hi = temp_hi - 2,  temp_lo = temp_lo - 2
    WHERE date > '1994-11-28';
```

Veja o novo estado dos dados:

```
SELECT * FROM weather;

     city      | temp_lo | temp_hi | prcp |    date
---------------+---------+---------+------+------------
 San Francisco |      46 |      50 | 0.25 | 1994-11-27
 San Francisco |      41 |      55 |    0 | 1994-11-29
 Hayward       |      35 |      52 |      | 1994-11-29
(3 rows)
```
