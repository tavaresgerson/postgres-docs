## F.41. spi — Recursos/exemplos de interface de programação do servidor [#](#CONTRIB-SPI)

* [F.41.1. refint — Funções para implementar integridade referencial](contrib-spi.md#CONTRIB-SPI-REFINT)
* [F.41.2. autoinc — Funções para autoincremento de campos](contrib-spi.md#CONTRIB-SPI-AUTOINC)
* [F.41.3. insert_username — Funções para rastrear quem modificou uma tabela](contrib-spi.md#CONTRIB-SPI-INSERT-USERNAME)
* [F.41.4. moddatetime — Funções para rastrear a última hora de modificação](contrib-spi.md#CONTRIB-SPI-MODDATETIME)

O módulo spi oferece vários exemplos práticos de uso da [Interface de Programação do Servidor](spi.md) (SPI) e gatilhos. Embora essas funções sejam úteis por si mesmas, elas são ainda mais úteis como exemplos para modificar para seus próprios propósitos. As funções são suficientemente gerais para serem usadas com qualquer tabela, mas você precisa especificar os nomes da tabela e do campo (como descrito abaixo) ao criar um gatilho.

Cada um dos grupos de funções descritos abaixo é fornecido como uma extensão separadamente instalável.

### F.41.1. refint — Funções para implementar a integridade referencial [#](#CONTRIB-SPI-REFINT)

`check_primary_key()` e `check_foreign_key()` são usados para verificar restrições de chave estrangeira. (Essa funcionalidade já foi substituída há muito tempo pelo mecanismo de chave estrangeira integrado, claro, mas o módulo ainda é útil como exemplo.)

`check_primary_key()` verifica a tabela de referência. Para usar, crie um gatilho `AFTER INSERT OR UPDATE` usando essa função em uma tabela que faz referência a outra tabela. Especifique como argumentos do gatilho: o(s) nome(s) da(s) coluna(s) da tabela de referência que formam a chave estrangeira, o nome da tabela referenciada e os nomes das colunas na tabela referenciada que formam a chave primária/única. Para lidar com múltiplas chaves estrangeiras, crie um gatilho para cada referência.

`check_foreign_key()` verifica a tabela referenciada. Para usar, crie um gatilho `AFTER DELETE OR UPDATE` usando essa função em uma tabela referenciada por(s) outra(s) tabela(s). Especifique como argumentos do gatilho: o número de tabelas de referência para as quais a função deve realizar a verificação, a ação se uma chave de referência for encontrada (`cascade` — para excluir a linha de referência, `restrict` — para abortar a transação se chaves de referência existirem, `setnull` — para definir os campos da chave de referência para nulos), os nomes das colunas da tabela desencadeada que formam a chave primária/única, e em seguida, o nome da tabela de referência e os nomes das colunas (repetidos para tantas tabelas de referência quanto foram especificadas pelo primeiro argumento). Note que as colunas da chave primária/única devem ser marcadas como NOT NULL e devem ter um índice único.

Observe que, se esses gatilhos forem executados a partir de outro gatilho `BEFORE`, eles podem falhar inesperadamente. Por exemplo, se um usuário inserir a linha row1 e, em seguida, o gatilho `BEFORE` inserir a linha row2 e chamar um gatilho com o `check_foreign_key()`, a função `check_foreign_key()` não verá a linha row1 e falhará.

Há exemplos em `refint.example`.

### F.41.2. autoinc — Funções para autoincremento de campos [#](#CONTRIB-SPI-AUTOINC)

`autoinc()` é um gatilho que armazena o próximo valor de uma sequência em um campo inteiro. Isso tem alguma sobreposição com o recurso embutido de "coluna serial", mas não é o mesmo. O gatilho substituirá o valor do campo apenas se esse valor for inicialmente zero ou nulo (após a ação do comando SQL que inseriu ou atualizou a linha). Além disso, se o próximo valor da sequência for zero, `nextval()` será chamado uma segunda vez para obter um valor não nulo.

Para usar, crie um gatilho `BEFORE INSERT` (ou opcionalmente `BEFORE INSERT OR UPDATE`) usando esta função. Especifique dois argumentos de gatilho: o nome da coluna inteira a ser modificada e o nome do objeto de sequência que fornecerá os valores. (Na verdade, você pode especificar qualquer número de pares desses nomes, se desejar atualizar mais de uma coluna autoincrementada.)

Há um exemplo em `autoinc.example`.

### F.41.3. insert_username — Funções para rastrear quem alterou uma tabela [#](#CONTRIB-SPI-INSERT-USERNAME)

`insert_username()` é um gatilho que armazena o nome do usuário atual em um campo de texto. Isso pode ser útil para rastrear quem modificou a última linha em uma tabela.

Para usar, crie um `BEFORE INSERT` e/ou `UPDATE` usando essa função. Especifique um único argumento de gatilho: o nome da coluna de texto a ser modificada.

Há um exemplo em `insert_username.example`.

### F.41.4. moddatetime — Funções para Rastrear o Último Tempo de Modificação [#](#CONTRIB-SPI-MODDATETIME)

`moddatetime()` é um gatilho que armazena a hora atual em um campo `timestamp`. Isso pode ser útil para rastrear o último tempo de modificação de uma linha específica dentro de uma tabela.

Para usar, crie um gatilho `BEFORE UPDATE` usando essa função. Especifique um único argumento de gatilho: o nome da coluna a ser modificada. A coluna deve ser do tipo `timestamp` ou `timestamp with time zone`.

Há um exemplo em `moddatetime.example`.