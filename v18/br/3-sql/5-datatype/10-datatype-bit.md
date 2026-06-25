### 8.10. Tipos de String de Bits [#](#DATATYPE-BIT)

As strings de bits são cadeias de 1's e 0's. Elas podem ser usadas para armazenar ou visualizar máscaras de bits. Existem dois tipos de bits SQL: `bit(n)` e `bit varying(n)`, onde *`n`* é um inteiro positivo.

Os dados do tipo `bit` devem corresponder exatamente ao comprimento *`n`*; é um erro tentar armazenar cadeias de bits mais curtas ou mais longas. Os dados do tipo `bit varying` têm comprimento variável, até o comprimento máximo *`n`*; cadeias mais longas serão rejeitadas. Escrever `bit` sem uma especificação de comprimento é equivalente a `bit(1)`, enquanto `bit varying` sem uma especificação de comprimento significa comprimento ilimitado.

Nota

Se um valor de cadeia de bits for explicitamente convertido para `bit(n)`, ele será truncado ou preenchido com zeros à direita para ser exatamente *`n`* bits, sem gerar um erro. Da mesma forma, se um valor de cadeia de bits for explicitamente convertido para `bit varying(n)`, ele será truncado à direita se for mais de *`n`* bits.

Consulte [Seção 4.1.2.5](sql-syntax-lexical.md#SQL-SYNTAX-BIT-STRINGS) para obter informações sobre a sintaxe das constantes de cadeia de bits. Operadores bit-lógicos e funções de manipulação de strings estão disponíveis; consulte [Seção 9.6](functions-bitstring.md).

**Exemplo 8.3. Uso dos tipos de string de bits**

```sql
CREATE TABLE test (a BIT(3), b BIT VARYING(5));
INSERT INTO test VALUES (B'101', B'00');
INSERT INTO test VALUES (B'10', B'101');

ERROR:  bit string length 2 does not match type bit(3)

INSERT INTO test VALUES (B'10'::bit(3), B'101');
SELECT * FROM test;

  a  |  b
-----+-----
 101 | 00
 100 | 101
```

Um valor de cadeia de bits requer 1 byte para cada grupo de 8 bits, além de 5 ou 8 bytes de sobrecarga, dependendo do comprimento da cadeia (mas valores longos podem ser comprimidos ou removidos fora da linha, conforme explicado na [Seção 8.3](datatype-character.md) para cadeias de caracteres).