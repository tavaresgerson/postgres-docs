## 10.6. Colunas de saída [#](#TYPECONV-SELECT) `SELECT`

As regras dadas nas seções anteriores resultarão na atribuição de tipos de dados não `unknown` a todas as expressões em uma consulta SQL, exceto para literais de tipo não especificado que aparecem como colunas de saída simples de um comando `SELECT`. Por exemplo, em

```
SELECT 'Hello World';
```

não há nada para identificar que tipo a literal de string deve ser tratada. Nessa situação, o PostgreSQL voltará a resolver o tipo da literal como `text`.

Quando o `SELECT` é um dos braços de um `UNION` (ou `INTERSECT` ou `EXCEPT`) construído, ou quando aparece dentro de `INSERT ... SELECT`, esta regra não é aplicada, uma vez que as regras dadas nas seções anteriores têm precedência. O tipo de um literal de tipo não especificado pode ser obtido do outro braço do `UNION` no primeiro caso, ou da coluna de destino no segundo caso.

As listas de `RETURNING` são tratadas da mesma forma que as listas de saída de `SELECT` para esse propósito.

Nota

Antes do PostgreSQL 10, essa regra não existia, e os literais de tipo não especificado em uma lista de saída `SELECT` eram deixados como tipo `unknown`. Isso teve várias consequências ruins, então foi alterado.