## 10.4. Armazenamento de Valores [#](#TYPECONV-QUERY)

Os valores a serem inseridos em uma tabela são convertidos para o tipo de dados da coluna de destino de acordo com os seguintes passos.

**Conversão do tipo de armazenamento de valor**

1. Verifique se há uma correspondência exata com o alvo.
2. Caso contrário, tente converter a expressão para o tipo alvo. Isso é possível se uma *decomposição de atribuição* entre os dois tipos estiver registrada no catálogo `pg_cast` (consulte [CREATE CAST](sql-createcast.md "CREATE CAST")). Alternativamente, se a expressão for uma literal de tipo desconhecido, o conteúdo da string literal será fornecido à rotina de conversão de entrada para o tipo alvo.
3. Verifique se há uma decomposição de tamanho para o tipo alvo. Uma decomposição de tamanho é uma decomposição desse tipo para si mesmo. Se uma for encontrada no catálogo `pg_cast`, aplique-a à expressão antes de armazená-la na coluna de destino. A função de implementação para tal decomposição sempre recebe um parâmetro extra do tipo `integer`, que recebe o valor do `atttypmod` da coluna de destino (tipicamente seu comprimento declarado, embora a interpretação de `atttypmod` varie para diferentes tipos de dados), e pode receber um terceiro parâmetro `boolean` que diz se a decomposição é explícita ou implícita. A função de decomposição é responsável por aplicar qualquer semântica dependente do tamanho, como verificação de tamanho ou truncação.

**Exemplo 10.9. `character` Conversão do Tipo de Armazenamento**

Para uma coluna-alvo declarada como `character(20)`, a seguinte declaração mostra que o valor armazenado está corretamente dimensionado:

```
CREATE TABLE vv (v character(20));
INSERT INTO vv SELECT 'abc' || 'def';
SELECT v, octet_length(v) FROM vv;

          v           | octet_length
----------------------+--------------
 abcdef               |           20
(1 row)
```

O que realmente aconteceu aqui é que os dois literais desconhecidos são resolvidos como `text` por padrão, permitindo que o operador `||` seja resolvido como concatenação de `text`. Em seguida, o resultado do operador `text` é convertido em `bpchar` (“caractere preenchido com espaços em branco”, o nome interno do tipo de dados `character`) para corresponder ao tipo da coluna alvo. (Como a conversão de `text` para `bpchar` é binária, essa conversão não insere nenhuma chamada real de função.) Finalmente, a função de dimensionamento `bpchar(bpchar, integer, boolean)` é encontrada no catálogo do sistema e aplicada ao resultado do operador e ao comprimento da coluna armazenada. Essa função específica do tipo realiza a verificação do comprimento necessária e a adição de espaços de preenchimento.