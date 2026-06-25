### 8.13. Tipo XML [#](#DATATYPE-XML)

* [8.13.1. Criação de Valores XML](datatype-xml.md#DATATYPE-XML-CREATING)
* [8.13.2. Manipulação de codificação](datatype-xml.md#DATATYPE-XML-ENCODING-HANDLING)
* [8.13.3. Acesso a Valores XML](datatype-xml.md#DATATYPE-XML-ACCESSING-XML-VALUES)

O tipo de dados `xml` pode ser usado para armazenar dados XML. Sua vantagem em relação ao armazenamento de dados XML em um campo `text` é que ele verifica os valores de entrada quanto à forma bem formada, e há funções de suporte para realizar operações tipo-seguras sobre ele; veja [Seção 9.15](functions-xml.md). O uso deste tipo de dados requer que a instalação tenha sido construída com `configure --with-libxml`.

O tipo `xml` pode armazenar documentos bem formados, conforme definido pelo padrão XML, bem como fragmentos de “conteúdo”, que são definidos por referência ao mais permissivo [“nó de documento”](https://www.w3.org/TR/2010/REC-xpath-datamodel-20101214/#DocumentNode) do modelo de dados XQuery e XPath. Aproximadamente, isso significa que os fragmentos de conteúdo podem ter mais de um elemento de nível superior ou nó de caractere. A expressão `xmlvalue IS DOCUMENT` pode ser usada para avaliar se um valor específico de `xml` é um documento completo ou apenas um fragmento de conteúdo.

Limites e notas de compatibilidade para o tipo de dados `xml` podem ser encontrados em [Seção D.3](xml-limits-conformance.md).

#### 8.13.1. Criando valores XML [#](#DATATYPE-XML-CREATING)

Para produzir um valor do tipo `xml` a partir de dados de caracteres, use a função `xmlparse`:

```sql
XMLPARSE ( { DOCUMENT | CONTENT } value)
```

Exemplos:

```sql
XMLPARSE (DOCUMENT '<?xml version="1.0"?><book><title>Manual</title><chapter>...</chapter></book>')
XMLPARSE (CONTENT 'abc<foo>bar</foo><bar>foo</bar>')
```

Embora essa seja a única maneira de converter cadeias de caracteres em valores XML de acordo com o padrão SQL, as sintaxes específicas do PostgreSQL são:

```sql
xml '<foo>bar</foo>'
'<foo>bar</foo>'::xml
```

também pode ser usado.

O tipo `xml` não valida os valores de entrada contra uma declaração de tipo de documento (DTD), mesmo quando o valor de entrada especifica uma DTD. Além disso, atualmente não há suporte integrado para validação contra outros idiomas de esquema XML, como o XML Schema.

A operação inversa, que produz um valor de cadeia de caracteres a partir de `xml`, utiliza a função `xmlserialize`:

```sql
XMLSERIALIZE ( { DOCUMENT | CONTENT } value AS type [ [ NO ] INDENT ] )
```

*`type`* pode ser `character`, `character varying` ou `text` (ou um alias para um desses). Novamente, de acordo com o padrão SQL, essa é a única maneira de converter entre os tipos `xml` e os tipos de caracteres, mas o PostgreSQL também permite que você simplesmente realize a conversão do valor.

A opção `INDENT` faz com que o resultado seja formatado, enquanto `NO INDENT` (que é o padrão) apenas emite a string de entrada original. A conversão para um tipo de caractere também produz a string original.

Quando um valor de cadeia de caracteres é convertido para ou a partir do tipo `xml`, sem passar por `XMLPARSE` ou `XMLSERIALIZE`, respectivamente, a escolha entre `DOCUMENT` e `CONTENT` é determinada pelo parâmetro de configuração da sessão “opção XML”, que pode ser definido usando o comando padrão:

```sql
SET XML OPTION { DOCUMENT | CONTENT };
```

ou a sintaxe mais semelhante à do PostgreSQL

```sql
SET xmloption TO { DOCUMENT | CONTENT };
```

O padrão é `CONTENT`, portanto, todas as formas de dados XML são permitidas.

#### 8.13.2. Gerenciamento de codificação [#](#DATATYPE-XML-ENCODING-HANDLING)

É necessário ter cuidado ao lidar com múltiplos codificações de caracteres no cliente, no servidor e nos dados XML passados por eles. Ao usar o modo de texto para passar consultas ao servidor e resultados de consulta ao cliente (que é o modo normal), o PostgreSQL converte todos os dados de caracteres passados entre o cliente e o servidor e vice-versa para a codificação de caracteres do respectivo fim; veja [Seção 23.3](multibyte.md). Isso inclui representações de texto de valores XML, como nos exemplos acima. Isso normalmente significaria que as declarações de codificação contidas nos dados XML podem se tornar inválidas à medida que os dados de caracteres são convertidos em outras codificações enquanto viajam entre o cliente e o servidor, porque a declaração de codificação embutida não é alterada. Para lidar com esse comportamento, as declarações de codificação contidas em strings de caracteres apresentadas para entrada no tipo `xml` são *ignoradas*, e o conteúdo é assumido estar na codificação atual do servidor. Consequentemente, para o processamento correto, as strings de caracteres dos dados XML devem ser enviadas pelo cliente na codificação atual do cliente. É responsabilidade do cliente converter os documentos para a codificação atual do cliente antes de enviá-los ao servidor, ou ajustar a codificação do cliente de forma apropriada. Na saída, os valores do tipo `xml` não terão uma declaração de codificação, e os clientes devem assumir que todos os dados estão na codificação atual do cliente.

Ao usar o modo binário para passar parâmetros de consulta ao servidor e retornar os resultados da consulta ao cliente, nenhuma conversão de codificação é realizada, portanto, a situação é diferente. Neste caso, uma declaração de codificação nos dados XML será observada, e se estiver ausente, os dados serão assumidos como UTF-8 (conforme exigido pelo padrão XML; observe que o PostgreSQL não suporta UTF-16). Na saída, os dados terão uma declaração de codificação que especifica a codificação do cliente, a menos que a codificação do cliente seja UTF-8, na qual caso ela será omitida.

Desnecessário dizer que o processamento de dados XML com PostgreSQL será menos propenso a erros e mais eficiente se o codificação de dados XML, codificação do cliente e codificação do servidor forem os mesmos. Como os dados XML são processados internamente em UTF-8, as operações serão mais eficientes se a codificação do servidor também for UTF-8.

Atenção

Algumas funções relacionadas ao XML podem não funcionar de forma alguma em dados não ASCII quando o codificação do servidor não é UTF-8. Sabe-se que isso é um problema, em particular, para `xmltable()` e `xpath()`.

#### 8.13.3. Acesso a valores XML [#](#DATATYPE-XML-ACCESSING-XML-VALUES)

O tipo de dados `xml` é incomum porque não oferece operadores de comparação. Isso ocorre porque não há um algoritmo de comparação bem definido e universalmente útil para dados XML. Uma consequência disso é que você não pode recuperar linhas comparando uma coluna `xml` com um valor de pesquisa. Os valores XML devem, portanto, ser acompanhados tipicamente por um campo de chave separado, como um ID. Uma solução alternativa para comparar valores XML é convertê-los primeiro em cadeias de caracteres, mas observe que a comparação de cadeias de caracteres tem pouco a ver com um método de comparação XML útil.

Como não há operadores de comparação para o tipo de dados `xml`, não é possível criar um índice diretamente em uma coluna desse tipo. Se busca rápida em dados XML é desejada, possíveis soluções incluem a conversão da expressão em um tipo de cadeia de caracteres e indexação dessa forma, ou indexação de uma expressão XPath. Claro, a consulta real teria que ser ajustada para pesquisar pela expressão indexada.

A funcionalidade de busca de texto no PostgreSQL também pode ser usada para acelerar pesquisas de documentos completos de dados XML. No entanto, o suporte necessário para pré-processamento ainda não está disponível na distribuição do PostgreSQL.