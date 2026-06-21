## F.9. citext — um tipo de cadeia de caracteres não sensível a maiúsculas e minúsculas [#](#CITEXT)

* [F.9.1. Razão][(citext.md#CITEXT-RATIONALE)]  
* [F.9.2. Como usá-lo][(citext.md#CITEXT-HOW-TO-USE-IT)]  
* [F.9.3. Comportamento de comparação de strings][(citext.md#CITEXT-STRING-COMPARISON-BEHAVIOR)]  
* [F.9.4. Limitações][(citext.md#CITEXT-LIMITATIONS)]  
* [F.9.5. Autor][(citext.md#CITEXT-AUTHOR)]

O módulo `citext` fornece um tipo de cadeia de caracteres insensível a maiúsculas e minúsculas, `citext`. Essencialmente, ele chama internamente `lower` ao comparar valores. Caso contrário, ele se comporta quase exatamente como `text`.

### DICA

Considere usar *colunações não determinísticas* (consulte [Seção 23.2.2.4][(collation.md#COLLATION-NONDETERMINISTIC "23.2.2.4. Nondeterministic Collations")]) em vez deste módulo. Elas podem ser usadas para comparações não sensíveis ao caso, comparações não sensíveis ao acento e outras combinações, e elas tratam mais casos especiais do Unicode corretamente.

Este módulo é considerado "confiável", ou seja, pode ser instalado por usuários não superusuários que possuem privilégio `CREATE` no banco de dados atual.

### F.9.1. **Razão [#](#CITEXT-RATIONALE)

A abordagem padrão para fazer correspondências não sensíveis ao caso em maiúsculas e minúsculas no PostgreSQL tem sido usar a função `lower` ao comparar valores, por exemplo:

```
SELECT * FROM tab WHERE lower(col) = LOWER(?);
```

Isso funciona razoavelmente bem, mas tem vários inconvenientes:

* Isso torna suas declarações SQL verbosas, e você sempre tem que se lembrar de usar `lower` tanto no valor da coluna quanto na consulta.
* Não usará um índice, a menos que você crie um índice funcional usando `lower`.
* Se você declarar uma coluna como `UNIQUE` ou `PRIMARY KEY`, o índice implicitamente gerado é sensível ao caso. Portanto, é inútil para pesquisas que não são sensíveis ao caso, e não aplicará a unicidade de forma sensível ao caso.

O tipo de dados `citext` permite que você elimine chamadas para `lower` em consultas SQL e permite que uma chave primária seja sensível a maiúsculas e minúsculas. `citext` é sensível ao idioma, assim como `text`, o que significa que a correspondência de caracteres maiúsculos e minúsculos depende das regras do conjunto de definições `LC_CTYPE` do banco de dados. Novamente, esse comportamento é idêntico ao uso de `lower` em consultas. Mas, como isso é feito de forma transparente pelo tipo de dados, você não precisa se lembrar de fazer algo especial em suas consultas.

### F.9.2. Como usá-lo [#](#CITEXT-HOW-TO-USE-IT)

Aqui está um exemplo simples de uso:

```
CREATE TABLE users (
    nick CITEXT PRIMARY KEY,
    pass TEXT   NOT NULL
);

INSERT INTO users VALUES ( 'larry',  sha256(random()::text::bytea) );
INSERT INTO users VALUES ( 'Tom',    sha256(random()::text::bytea) );
INSERT INTO users VALUES ( 'Damian', sha256(random()::text::bytea) );
INSERT INTO users VALUES ( 'NEAL',   sha256(random()::text::bytea) );
INSERT INTO users VALUES ( 'Bjørn',  sha256(random()::text::bytea) );

SELECT * FROM users WHERE nick = 'Larry';
```

A declaração `SELECT` retornará um tuplo, mesmo que a coluna `nick` tenha sido definida como `larry` e a consulta fosse para `Larry`.

### F.9.3. Comportamento de comparação de strings [#](#CITEXT-STRING-COMPARISON-BEHAVIOR)

`citext` realiza comparações convertendo cada string para maiúsculas (como se `lower` estivesse sendo chamado) e, em seguida, comparando os resultados normalmente. Assim, por exemplo, duas strings são consideradas iguais se `lower` produziria resultados idênticos para elas.

Para emular uma ordenação não sensível ao caso o mais possível, existem versões específicas do `citext` de vários operadores e funções de processamento de strings. Portanto, por exemplo, os operadores de expressão regular `~` e `~*` apresentam o mesmo comportamento quando aplicados ao `citext`: ambos correspondem de forma não sensível ao caso. O mesmo vale para os operadores `!~` e `!~*`, bem como para os operadores `LIKE` `~~` e `~~*`, e `!~~` e `!~~*`. Se você deseja corresponder de forma sensível ao caso, pode converter os argumentos do operador para `text`.

Da mesma forma, todas as funções a seguir realizam correspondência de forma sensível ao caso, se seus argumentos forem `citext`:

* `regexp_match()`
* `regexp_matches()`
* `regexp_replace()`
* `regexp_split_to_array()`
* `regexp_split_to_table()`
* `replace()`
* `split_part()`
* `strpos()`
* `translate()`

Para as funções de regexp, se você deseja fazer uma correspondência sensível ao caso, pode especificar a bandeira “c” para forçar uma correspondência sensível ao caso. Caso contrário, você deve converter para `text` antes de usar uma dessas funções se desejar comportamento sensível ao caso.

### F.9.4. Limitações [#](#CITEXT-LIMITATIONS)

* O comportamento de dobramento de caso de `citext` depende da configuração de `LC_CTYPE` do seu banco de dados. Portanto, como os valores são comparados é determinado quando o banco de dados é criado. Não é verdadeiramente insensível ao caso nos termos definidos pelo padrão Unicode. Efetivamente, o que isso significa é que, desde que você esteja satisfeito com sua ordenação, você deve estar satisfeito com as comparações de `citext`. Mas se você tiver dados em diferentes idiomas armazenados em seu banco de dados, os usuários de um idioma podem achar que os resultados das suas consultas não são os esperados se a ordenação for para outro idioma.
* A partir do PostgreSQL 9.1, você pode anexar uma especificação de `COLLATE` a colunas de `citext` ou valores de dados. Atualmente, os operadores `citext` respeitarão uma especificação de `COLLATE` não padrão ao comparar strings dobradas por caso, mas o dobramento inicial para maiúsculas é sempre feito de acordo com a configuração de `LC_CTYPE` do banco de dados (ou seja, como se `COLLATE "default"` fosse dado). Isso pode ser alterado em uma versão futura para que ambas as etapas sigam a especificação de `COLLATE`.
* `citext` não é tão eficiente quanto `text` porque as funções de operadores e as funções de comparação de B-tree devem fazer cópias dos dados e convertê-los para maiúsculas para comparações. Além disso, apenas `text` pode suportar a deduplicação de B-Tree. No entanto, `citext` é um pouco mais eficiente do que usar `lower` para obter correspondência insensível ao caso.
* `citext` não ajuda muito se você precisa de dados para comparar sensível ao caso em alguns contextos e insensível ao caso em outros contextos. A resposta padrão é usar o tipo `text` e usar manualmente a função `lower` quando você precisa comparar insensível ao caso; isso funciona bem se a comparação insensível ao caso for necessária apenas raramente. Se você precisa do comportamento insensível ao caso na maioria das vezes e sensível ao caso raramente, considere armazenar os dados como `citext` e projetar explicitamente a coluna para `text` quando você deseja uma comparação sensível ao caso. Em qualquer situação, você precisará de dois índices se quiser que os dois tipos de pesquisas sejam rápidos.
* O esquema contendo os operadores de `citext` deve estar no `search_path` atual (tipicamente `public`); se não estiver, os operadores normais sensíveis ao caso de `text` serão invocados em vez disso.
* A abordagem de dobramento de strings para comparação não lida corretamente com alguns casos especiais do Unicode, por exemplo, quando uma letra maiúscula tem dois equivalentes de letras minúsculas. O Unicode distingue entre *mapeamento de caso* e *dobramento de caso* por essa razão. Use colunas não determinísticas em vez de `citext` para lidar corretamente com isso.

### F.9.5. Autor [#](#CITEXT-AUTHOR)

David E. Wheeler `<david@kineticode.com>`

Inspirado no módulo original `citext` de Donald Fraser.