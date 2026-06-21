## 3.2. Visões [#](#TUTORIAL-VIEWS)

Reveja as consultas na [Seção 2.6](tutorial-join.md). Suponha que a listagem combinada de registros climáticos e localização da cidade seja de particular interesse para sua aplicação, mas você não queira digitar a consulta toda vez que precisar dela. Você pode criar uma *visualização* sobre a consulta, o que dá um nome à consulta que você pode referir como uma tabela comum:

```
CREATE VIEW myview AS
    SELECT name, temp_lo, temp_hi, prcp, date, location
        FROM weather, cities
        WHERE city = name;

SELECT * FROM myview;
```

Fazer uso liberal de vistas é um aspecto fundamental do bom projeto de banco de dados SQL. As vistas permitem encapsular os detalhes da estrutura de suas tabelas, que podem mudar à medida que sua aplicação evolui, por trás de interfaces consistentes.

As vistas podem ser usadas em praticamente qualquer lugar onde uma mesa real pode ser usada. É comum construir vistas com base em outras vistas.