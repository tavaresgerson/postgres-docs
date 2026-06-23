### 2.9. Deletações [#](#TUTORIAL-DELETE)

As linhas podem ser removidas de uma tabela usando o comando `DELETE`. Suponha que você não esteja mais interessado no clima de Hayward. Então, você pode fazer o seguinte para excluir essas linhas da tabela:

```
DELETE FROM weather WHERE city = 'Hayward';
```

Todos os registros meteorológicos pertencentes a Hayward são removidos.

```
SELECT * FROM weather;
```

```
     city      | temp_lo | temp_hi | prcp |    date
---------------+---------+---------+------+------------
 San Francisco |      46 |      50 | 0.25 | 1994-11-27
 San Francisco |      41 |      55 |    0 | 1994-11-29
(2 rows)
```

Deve-se ficar atento a declarações do tipo

```
DELETE FROM tablename;
```

Sem uma qualificação, `DELETE` removerá *todas* as linhas da tabela fornecida, deixando-a vazia. O sistema não solicitará confirmação antes de fazer isso!