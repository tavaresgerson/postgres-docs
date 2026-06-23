## 39.6. Regras e Status de Comando [#](#RULES-STATUS)

O servidor PostgreSQL retorna uma string de status de comando, como `INSERT 149592 1`, para cada comando que recebe. Isso é simples o suficiente quando não há regras envolvidas, mas o que acontece quando a consulta é reescrita por regras?

As regras afetam o status do comando da seguinte forma:

* Se não houver uma regra `INSTEAD` incondicional para a consulta, então a consulta originalmente fornecida será executada e seu status de comando será retornado como de costume. (Mas observe que, se houvesse alguma regra `INSTEAD` condicional, a negação de suas qualificações teria sido adicionada à consulta original. Isso pode reduzir o número de linhas que ela processa, e, se assim for, o status relatado será afetado.)
* Se houver alguma regra `INSTEAD` incondicional para a consulta, então a consulta original não será executada de forma alguma. Neste caso, o servidor retornará o status de comando para a última consulta que foi inserida por uma regra `INSTEAD` (condicional ou incondicional) e que é do mesmo tipo de comando (`INSERT`, `UPDATE` ou `DELETE`) que a consulta original. Se nenhuma consulta que atenda a esses requisitos for adicionada por qualquer regra, então o status de comando retornado mostrará o tipo de consulta original e zeros para os campos de contagem de linhas e OID.

O programador pode garantir que qualquer regra desejada do `INSTEAD` seja a que define o status do comando no segundo caso, dando-lhe o nome de regra alfabeticamente último entre as regras ativas, para que seja aplicada por último.