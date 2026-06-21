## 10.1. Visão geral [#](#TYPECONV-OVERVIEW)

O SQL é uma linguagem fortemente tipada. Isso significa que cada item de dados tem um tipo de dados associado que determina seu comportamento e uso permitido. O PostgreSQL tem um sistema de tipos extensibile que é mais geral e flexível do que outras implementações de SQL. Portanto, a maioria do comportamento de conversão de tipos no PostgreSQL é regida por regras gerais, em vez de heurísticas ad hoc. Isso permite o uso de expressões de tipos mistos, mesmo com tipos definidos pelo usuário.

O scanner/parser do PostgreSQL divide os elementos lexicais em cinco categorias fundamentais: inteiros, números não inteiros, strings, identificadores e palavras-chave. As constantes dos tipos não numéricos são classificadas como strings primeiro. A definição da linguagem SQL permite especificar nomes de tipos com strings, e esse mecanismo pode ser usado no PostgreSQL para iniciar o parser pelo caminho correto. Por exemplo, a consulta:

```
SELECT text 'Origin' AS "label", point '(0,0)' AS "value";

 label  | value
--------+-------
 Origin | (0,0)
(1 row)
```

tem duas constantes literais, do tipo `text` e `point`. Se um tipo não for especificado para uma constante de cadeia, então o tipo de marcador `unknown` é atribuído inicialmente, para ser resolvido em etapas posteriores, conforme descrito abaixo.

Existem quatro construções fundamentais do SQL que exigem regras distintas de conversão de tipos no analisador do PostgreSQL:

Chamadas de função: Muitas das funções do sistema de tipos do PostgreSQL são construídas em torno de um conjunto rico de funções. As funções podem ter um ou mais argumentos. Como o PostgreSQL permite a sobrecarga de funções, o nome da função por si só não identifica de forma única a função a ser chamada; o analisador deve selecionar a função correta com base nos tipos de dados dos argumentos fornecidos.

Operadores: O PostgreSQL permite expressões com operadores prefixados (de um argumento) e também operadores infixados (de dois argumentos). Assim como as funções, os operadores podem ser sobrecarregados, portanto, o mesmo problema de seleção do operador correto existe.

Armazenamento de valor: As declarações SQL `INSERT` e `UPDATE` colocam os resultados das expressões em uma tabela. As expressões na declaração devem ser correspondidas e, possivelmente, convertidas para os tipos das colunas de destino.

`UNION`, `CASE` e construções relacionadas: Como todos os resultados de consulta de uma declaração unificada `SELECT` devem aparecer em um único conjunto de colunas, os tipos dos resultados de cada cláusula `SELECT` devem ser correspondidos e convertidos para um conjunto uniforme. Da mesma forma, as expressões de resultado de uma construção `CASE` devem ser convertidas para um tipo comum para que a expressão `CASE` como um todo tenha um tipo de saída conhecido. Algumas outras construções, como `ARRAY[]` e as funções `GREATEST` e `LEAST`, também requerem a determinação de um tipo comum para várias subexpressões.

Os catálogos do sistema armazenam informações sobre quais conversões ou *casts* existem entre quais tipos de dados e como realizar essas conversões. Conversões adicionais podem ser adicionadas pelo usuário com o comando [CREATE CAST](sql-createcast.md "CREATE CAST"). (Isso geralmente é feito em conjunto com a definição de novos tipos de dados. O conjunto de conversões entre os tipos embutidos foi cuidadosamente elaborado e não deve ser alterado.)

Uma heurística adicional fornecida pelo analisador permite uma determinação aprimorada do comportamento de conversão adequado entre grupos de tipos que têm conversões implícitas. Os tipos de dados são divididos em várias categorias básicas de *tipo*, incluindo `boolean`, `numeric`, `string`, `bitstring`, `datetime`, `timespan`, `geometric`, `network` e definidos pelo usuário. (Para uma lista, consulte a [Tabela 52.65][(catalog-pg-type.md#CATALOG-TYPCATEGORY-TABLE "Table 52.65. typcategory Codes")]; mas note que também é possível criar categorias de tipos personalizadas.) Dentro de cada categoria, pode haver um ou mais *tipos preferidos*, que são preferidos quando há uma escolha de tipos possíveis. Com a seleção cuidadosa de tipos preferidos e conversões implícitas disponíveis, é possível garantir que expressões ambíguas (aqueles com múltiplas soluções de análise candidatas) possam ser resolvidas de uma maneira útil.

Todas as regras de conversão de tipo são projetadas com vários princípios em mente:

* As conversões implícitas nunca devem ter resultados surpreendentes ou imprevisíveis.
* Não deve haver sobrecarga adicional no analisador ou executor se uma consulta não precisar de conversão de tipo implícita. Isso significa que, se uma consulta estiver bem formada e os tipos já corresponderem, a consulta deve ser executada sem gastar tempo extra no analisador e sem introduzir chamadas de conversão implícita desnecessárias na consulta.
* Além disso, se uma consulta geralmente requer uma conversão implícita para uma função e, em seguida, o usuário define uma nova função com os tipos de argumento corretos, o analisador deve usar essa nova função e não mais realizar conversão implícita para usar a função antiga.