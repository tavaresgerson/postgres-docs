## 11.2. Tipos de índice [#](#INDEXES-TYPES)

* [11.2.1. B-Tree][(indexes-types.md#INDEXES-TYPES-BTREE)
* [11.2.2. Hash][(indexes-types.md#INDEXES-TYPES-HASH)
* [11.2.3. GiST][(indexes-types.md#INDEXES-TYPE-GIST)
* [11.2.4. SP-GiST][(indexes-types.md#INDEXES-TYPE-SPGIST)
* [11.2.5. GIN][(indexes-types.md#INDEXES-TYPES-GIN)
* [11.2.6. BRIN][(indexes-types.md#INDEXES-TYPES-BRIN)

O PostgreSQL oferece vários tipos de índice: B-tree, Hash, GiST, SP-GiST, GIN, BRIN e a extensão [bloom][(bloom.md "F.6. bloom — bloom filter index access method")]. Cada tipo de índice utiliza um algoritmo diferente que é o mais adequado para diferentes tipos de cláusulas indexáveis. Por padrão, o comando [[`CREATE INDEX`][(sql-createindex.md "CREATE INDEX")]] cria índices B-tree, que se encaixam nas situações mais comuns. Os outros tipos de índice são selecionados escrevendo a palavra-chave `USING` seguida do nome do tipo de índice. Por exemplo, para criar um índice Hash:

```
CREATE INDEX name ON table USING HASH (column);
```

### 11.2.1. B-Tree [#](#INDEXES-TYPES-BTREE)

As árvores B podem lidar com consultas de igualdade e intervalo em dados que podem ser ordenados em alguma ordem. Em particular, o planejador de consultas do PostgreSQL considerará o uso de um índice de árvore B sempre que uma coluna indexada esteja envolvida em uma comparação usando um desses operadores:

```
<   <=   =   >=   >
```

Construções equivalentes a combinações desses operadores, como `BETWEEN` e `IN`, também podem ser implementadas com uma pesquisa de índice B-tree. Além disso, uma condição `IS NULL` ou `IS NOT NULL` em uma coluna de índice pode ser usada com um índice B-tree.

O otimizador também pode usar um índice de B-tree para consultas que envolvem os operadores de correspondência de padrões `LIKE` e `~` *se* o padrão for uma constante e estiver ancorado no início da string — por exemplo, `col LIKE 'foo%'` ou `col ~ '^foo'`, mas não `col LIKE '%bar'`. No entanto, se o banco de dados não usa o local C, você precisará criar o índice com uma classe de operador especial para suportar a indexação de consultas de correspondência de padrões; veja [Seção 11.10][(indexes-opclass.md "11.10. Operator Classes and Operator Families")] abaixo. Também é possível usar índices de B-tree para `ILIKE` e `~*`, mas apenas se o padrão começar com caracteres não alfabéticos, ou seja, caracteres que não são afetados pela conversão de maiúsculas e minúsculas.

Os índices de árvore B também podem ser usados para recuperar dados em ordem ordenada. Isso nem sempre é mais rápido do que uma simples varredura e classificação, mas muitas vezes é útil.

### 11.2.2. Hash [#](#INDEXES-TYPES-HASH)

Os índices de hash armazenam um código de hash de 32 bits derivado do valor da coluna indexada. Portanto, tais índices só podem lidar com comparações de igualdade simples. O planejador de consulta considerará o uso de um índice de hash sempre que uma coluna indexada esteja envolvida em uma comparação usando o operador igual:

```
=
```

### 11.2.3. GiST [#](#INDEXES-TYPE-GIST)

Os índices GiST não são um único tipo de índice, mas sim uma infraestrutura dentro da qual muitas estratégias de indexação podem ser implementadas. Consequentemente, os operadores específicos com os quais um índice GiST pode ser usado variam dependendo da estratégia de indexação (a *classe de operador*). Como exemplo, a distribuição padrão do PostgreSQL inclui classes de operadores GiST para vários tipos de dados geométricos bidimensionais, que suportam consultas indexadas usando esses operadores:

```
<<   &<   &>   >>   <<|   &<|   |&>   |>>   @>   <@   ~=   &&
```

(Veja [Seção 9.11] para o significado desses operadores. [(functions-geometry.md "9.11. Geometric Functions and Operators")]) As classes de operadores GiST incluídas na distribuição padrão estão documentadas em [Tabela 65.1] [(gist.md#GIST-BUILTIN-OPCLASSES-TABLE "Table 65.1. Built-in GiST Operator Classes")]. Muitas outras classes de operadores GiST estão disponíveis na coleção `contrib` ou como projetos separados. Para mais informações, consulte [Seção 65.2] [(gist.md "65.2. GiST Indexes")].

Os índices GiST também são capazes de otimizar pesquisas de “vizinho mais próximo”, como

```
SELECT * FROM places ORDER BY location <-> point '(101,456)' LIMIT 10;
```

que encontra os dez locais mais próximos a um ponto de referência dado. A capacidade de fazer isso depende novamente da classe de operador específica que está sendo usada. Em [Tabela 65.1] ((gist.md#GIST-BUILTIN-OPCLASSES-TABLE "Table 65.1. Built-in GiST Operator Classes")), os operadores que podem ser usados dessa maneira estão listados na coluna “Operadores de Ordenação”.

### 11.2.4. SP-GiST [#](#INDEXES-TYPE-SPGIST)

Os índices SP-GiST, assim como os índices GiST, oferecem uma infraestrutura que suporta vários tipos de pesquisas. O SP-GiST permite a implementação de uma ampla gama de diferentes estruturas de dados baseadas em disco não balanceadas, como quadtrees, árvores k-d e árvores radix (tries). Como exemplo, a distribuição padrão do PostgreSQL inclui classes de operadores SP-GiST para pontos bidimensionais, que suportam consultas indexadas usando esses operadores:

```
<<   >>   ~=   <@   <<|   |>>
```

(Veja [Seção 9.11] para o significado desses operadores. [(functions-geometry.md "9.11. Geometric Functions and Operators")]) As classes de operadores SP-GiST incluídas na distribuição padrão estão documentadas em [Tabela 65.2] [(spgist.md#SPGIST-BUILTIN-OPCLASSES-TABLE "Table 65.2. Built-in SP-GiST Operator Classes")]. Para mais informações, consulte [Seção 65.3] [(spgist.md "65.3. SP-GiST Indexes")].

Assim como o GiST, o SP-GiST suporta pesquisas de “vizinho mais próximo”. Para as classes de operadores SP-GiST que suportam ordenação por distância, o operador correspondente está listado na coluna “Operadores de Ordenação” em [Tabela 65.2] [(spgist.md#SPGIST-BUILTIN-OPCLASSES-TABLE "Table 65.2. Built-in SP-GiST Operator Classes")].

### 11.2.5. GIN [#](#INDEXES-TYPES-GIN)

Os índices GIN são "índices invertidos", que são apropriados para valores de dados que contêm múltiplos valores de componentes, como arrays. Um índice invertido contém uma entrada separada para cada valor de componente e pode lidar eficientemente com consultas que testam a presença de valores específicos de componentes.

Assim como GiST e SP-GiST, o GIN pode suportar muitas estratégias de indexação definidas pelo usuário, e os operadores específicos com os quais um índice GIN pode ser usado variam dependendo da estratégia de indexação. Como exemplo, a distribuição padrão do PostgreSQL inclui uma classe de operador GIN para arrays, que suporta consultas indexadas usando esses operadores:

```
<@   @>   =   &&
```

(Veja [Seção 9.19][(functions-array.md "9.19. Array Functions and Operators")] para o significado desses operadores.) As classes de operadores GIN incluídas na distribuição padrão estão documentadas em [Tabela 65.3][(gin.md#GIN-BUILTIN-OPCLASSES-TABLE "Table 65.3. Built-in GIN Operator Classes")]. Muitas outras classes de operadores GIN estão disponíveis na coleção `contrib` ou como projetos separados. Para mais informações, consulte [Seção 65.4][(gin.md "65.4. GIN Indexes")].

### 11.2.6. BRIN [#](#INDEXES-TYPES-BRIN)

Os índices BRIN (abreviação de Block Range INdexes) armazenam resumos sobre os valores armazenados em faixas físicas consecutivas de um bloco de uma tabela. Assim, eles são mais eficazes para colunas cujos valores estão bem correlacionados com a ordem física das linhas da tabela. Assim como GiST, SP-GiST e GIN, o BRIN pode suportar muitas estratégias de indexação diferentes, e os operadores específicos com os quais um índice BRIN pode ser usado variam dependendo da estratégia de indexação. Para tipos de dados que têm uma ordem de classificação linear, os dados indexados correspondem aos valores mínimo e máximo dos valores na coluna para cada faixa de bloco. Isso suporta consultas indexadas usando esses operadores:

```
<   <=   =   >=   >
```

As classes de operadores BRIN incluídas na distribuição padrão estão documentadas em [Tabela 65.4][(brin.md#BRIN-BUILTIN-OPCLASSES-TABLE "Table 65.4. Built-in BRIN Operator Classes")]. Para mais informações, consulte [Seção 65.5][(brin.md "65.5. BRIN Indexes")].