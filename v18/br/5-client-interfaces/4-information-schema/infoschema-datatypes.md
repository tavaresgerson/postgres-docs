## 35.2. Tipos de dados [#](#INFOSCHEMA-DATATYPES)

As colunas dos pontos de vista do esquema de informações utilizam tipos de dados especiais que são definidos no esquema de informações. Estes são definidos como domínios simples sobre tipos integrados comuns. Você não deve usar esses tipos para trabalhos fora do esquema de informações, mas suas aplicações devem estar preparadas para eles, se elas selecionarem do esquema de informações.

Esses tipos são:

`cardinal_number`: Um número inteiro não negativo.

`character_data`: Uma cadeia de caracteres (sem comprimento máximo específico).

`sql_identifier`: Uma cadeia de caracteres. Este tipo é usado para identificadores SQL, o tipo `character_data` é usado para qualquer outro tipo de dados de texto.

`time_stamp`: Um domínio sobre o tipo `timestamp with time zone`

`yes_or_no`: Uma cadeia de caracteres que contém `YES` ou `NO`. Isso é usado para representar dados booleanos (verdadeiro/falso) no esquema de informações. (O esquema de informações foi inventado antes de o tipo `boolean` ser adicionado ao padrão SQL, então essa convenção é necessária para manter o esquema de informações compatível com versões anteriores.)

Cada coluna no esquema de informações tem um desses cinco tipos.