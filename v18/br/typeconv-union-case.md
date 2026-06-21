## 10.5. `UNION`, `CASE` e Construtos Relacionados [#](#TYPECONV-UNION-CASE)

Os construtos SQL `UNION` devem corresponder a tipos possivelmente distintos para se tornar um único conjunto de resultados. O algoritmo de resolução é aplicado separadamente a cada coluna de saída de uma consulta de união. Os construtos `INTERSECT` e `EXCEPT` resolvem tipos distintos da mesma maneira que o `UNION`. Alguns outros construtos, incluindo os construtos `CASE`, `ARRAY`, `VALUES` e as funções `GREATEST` e `LEAST`, utilizam o mesmo algoritmo para corresponder às suas expressões componentes e selecionar um tipo de dados de resultado.

**Resolução de Tipo para `UNION`, `CASE` e Construtos Relacionados**

1. Se todos os inputs forem do mesmo tipo e não for `unknown`, resolva como esse tipo.
2. Se algum input for de um tipo de domínio, trate-o como sendo do tipo base do domínio para todas as etapas subsequentes. [[12]](#ftn.id-1.5.9.10.9.3.1.1)
3. Se todos os inputs forem do tipo `unknown`, resolva como o tipo `text` (o tipo preferido da categoria de string). Caso contrário, os inputs `unknown` são ignorados para os propósitos das regras restantes.
4. Se os inputs não desconhecidos não forem todos da mesma categoria de tipo, falhe.
5. Selecione o primeiro tipo de input não desconhecido como o tipo candidato, e, em seguida, considere cada outro tipo de input não desconhecido, da esquerda para a direita. [[13]](#ftn.id-1.5.9.10.9.6.1.1) Se o tipo candidato puder ser convertido implicitamente para outro tipo, mas não vice-versa, selecione o outro tipo como o novo tipo candidato. Em seguida, continue considerando os inputs restantes. Se, em qualquer estágio deste processo, um tipo preferido for selecionado, pare de considerar inputs adicionais.
6. Converte todos os inputs no tipo candidato final. Falhe se não houver uma conversão implícita de um tipo de input dado para o tipo candidato.

Alguns exemplos seguem.

**Exemplo 10.10. Resolução de tipo com tipos não especificados em uma união**

```
SELECT text 'a' AS "text" UNION SELECT 'b';

 text
------
 a
 b
(2 rows)
```

Aqui, o literal de tipo desconhecido `'b'` será resolvido para o tipo `text`.

  

**Exemplo 10.11. Resolução de tipo em uma união simples**

```
SELECT 1.2 AS "numeric" UNION SELECT 1;

 numeric
---------
       1
     1.2
(2 rows)
```

O literal `1.2` é do tipo `numeric`, e o valor `integer` `1` pode ser convertido implicitamente para `numeric`, de modo que esse tipo seja usado.

  

**Exemplo 10.12. Resolução de tipo em uma união transposta**

```
SELECT 1 AS "real" UNION SELECT CAST('2.2' AS REAL);

 real
------
    1
  2.2
(2 rows)
```

Aqui, uma vez que o tipo `real` não pode ser implicitamente convertido para `integer`, mas o tipo `integer` pode ser implicitamente convertido para `real`, o tipo de resultado da união é resolvido como `real`.

  

**Exemplo 10.13. Resolução de tipo em uma união aninhada**

```
SELECT NULL UNION SELECT NULL UNION SELECT 1;

ERROR:  UNION types text and integer cannot be matched
```

Esse erro ocorre porque o PostgreSQL trata múltiplos `UNION` como um ninho de operações emparelhadas; ou seja, essa entrada é a mesma que

```
(SELECT NULL UNION SELECT NULL) UNION SELECT 1;
```

O `UNION` interno é resolvido como emitindo o tipo `text`, de acordo com as regras dadas acima. Em seguida, o `UNION` externo tem entradas dos tipos `text` e `integer`, o que leva ao erro observado. O problema pode ser corrigido garantindo que o `UNION` mais à esquerda tenha pelo menos uma entrada do tipo de resultado desejado.

As operações `INTERSECT` e `EXCEPT` são resolvidas de forma semelhante em pares. No entanto, os outros construtos descritos nesta seção consideram todos os seus inputs em uma etapa de resolução.

  

---

De certa forma, semelhante ao tratamento de entradas de domínio para operadores e funções, esse comportamento permite que um tipo de domínio seja preservado por meio de um `UNION` ou construção semelhante, desde que o usuário esteja atento para garantir que todas as entradas sejam implicitamente ou explicitamente do tipo exato. Caso contrário, o tipo de base do domínio será usado.

[[13]](#id-1.5.9.10.9.6.1.1) Por razões históricas, `CASE` trata sua cláusula `ELSE` (se houver) como a entrada “primeira”, com as cláusulas `THEN` (s) consideradas depois disso. Em todos os outros casos, “de esquerda para direita” significa a ordem em que as expressões aparecem no texto da consulta.