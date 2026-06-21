## 3.3. Chaves Estrangeiras [#](#TUTORIAL-FK)

Recorde as tabelas `weather` e `cities` de [Capítulo 2](tutorial-sql.md "Chapter 2. The SQL Language"). Considere o seguinte problema: você quer garantir que ninguém possa inserir linhas na tabela `weather` que não tenham uma entrada correspondente na tabela `cities`. Isso é chamado de manutenção da *integridade referencial* dos seus dados. Em sistemas de banco de dados simplificados, isso seria implementado (se for) primeiro, olhando para a tabela `cities` para verificar se existe um registro correspondente, e então inserindo ou rejeitando os novos registros `weather`. Essa abordagem tem vários problemas e é muito inconveniente, então o PostgreSQL pode fazer isso por você.

A nova declaração das tabelas ficaria assim:

```
CREATE TABLE cities (
        name     varchar(80) primary key,
        location point
);

CREATE TABLE weather (
        city      varchar(80) references cities(name),
        temp_lo   int,
        temp_hi   int,
        prcp      real,
        date      date
);
```

Agora, tente inserir um registro inválido:

```
INSERT INTO weather VALUES ('Berkeley', 45, 53, 0.0, '1994-11-28');
```

```
ERROR:  insert or update on table "weather" violates foreign key constraint "weather_city_fkey"
DETAIL:  Key (city)=(Berkeley) is not present in table "cities".
```

O comportamento das chaves estrangeiras pode ser ajustado conforme a sua aplicação. Não iremos além deste exemplo simples neste tutorial, mas apenas nos referiremos a [Capítulo 5][(ddl.md "Chapter 5. Data Definition")] para obter mais informações. Fazer o uso correto das chaves estrangeiras definitivamente melhorará a qualidade de suas aplicações de banco de dados, portanto, é fortemente recomendado que você aprenda sobre elas.