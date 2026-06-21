## B.4. Arquivos de configuração de data/hora [#](#DATETIME-CONFIG-FILES)

Como as abreviações de fuso horário não são bem padronizadas, o PostgreSQL fornece uma maneira de personalizar o conjunto de abreviações aceitas na entrada de data e hora. Existem duas fontes para essas abreviações:

1. O parâmetro de tempo de execução [TimeZone][(runtime-config-client.md#GUC-TIMEZONE)] é geralmente definido pelo nome de uma entrada no banco de dados de fuso horário da IANA. Se essa zona tiver abreviações de fuso horário amplamente utilizadas, elas aparecerão nos dados da IANA, e o PostgreSQL reconhecerá preferencialmente essas abreviações com os significados dados nos dados da IANA. Por exemplo, se `timezone` estiver definido como `America/New_York`, então `EST` será entendido como UTC-5 e `EDT` será entendido como UTC-4. (Essas abreviações da IANA também serão usadas na saída de data e hora, se [DateStyle][(runtime-config-client.md#GUC-DATESTYLE)] estiver definido com um estilo que prefira abreviações de fuso horário não numéricas.) 2. Se uma abreviação não for encontrada no fuso horário atual da IANA, ela é procurada na lista especificada pelo parâmetro de tempo de execução [timezone_abbreviations][(runtime-config-client.md#GUC-TIMEZONE-ABBREVIATIONS)]. A lista `timezone_abbreviations` é principalmente útil para permitir que a entrada de data e hora reconheça abreviações para fusos horários que não sejam o fuso horário atual. (Essas abreviações não serão usadas na saída de data e hora.)

Embora o parâmetro `timezone_abbreviations` possa ser alterado por qualquer usuário do banco de dados, os possíveis valores para ele estão sob o controle do administrador do banco de dados — na verdade, são nomes de arquivos de configuração armazenados em `.../share/timezonesets/` do diretório de instalação. Ao adicionar ou alterar arquivos nesse diretório, o administrador pode definir a política local para abreviações de fuso horário.

`timezone_abbreviations` pode ser definido para qualquer nome de arquivo encontrado em `.../share/timezonesets/`, se o nome do arquivo for totalmente alfabético. (A proibição de caracteres não alfabéticos em `timezone_abbreviations` impede a leitura de arquivos fora do diretório pretendido, bem como a leitura de arquivos de backup do editor e outros arquivos estranhos.)

Um arquivo de abreviação de fuso horário pode conter linhas em branco e comentários que começam com `#`. As linhas sem comentários devem ter um desses formatos:

```
zone_abbreviation offset
zone_abbreviation offset D
zone_abbreviation time_zone_name
@INCLUDE file_name
@OVERRIDE
```

Um *`zone_abbreviation`* é apenas uma abreviação que está sendo definida. Um *`offset`* é um número inteiro que fornece o deslocamento equivalente em segundos a partir do UTC, sendo positivo para leste de Greenwich e negativo para oeste. Por exemplo, -18000 seria cinco horas a oeste de Greenwich, ou o horário padrão da costa leste da América do Norte. `D` indica que o nome da zona representa o horário de verão local em vez do horário padrão.

Alternativamente, pode ser dada uma *`time_zone_name`*, referenciando um nome de zona definido no banco de dados de fuso horário IANA. A definição da zona é consultada para verificar se a abreviação está ou esteve em uso nessa zona, e, se estiver, o significado apropriado é usado — ou seja, o significado que estava em uso atualmente no timestamp cujo valor está sendo determinado, ou o significado em uso imediatamente antes disso, se não estiver em uso naquele momento, ou o significado mais antigo, se foi usado apenas após esse momento. Esse comportamento é essencial para lidar com abreviações cujo significado historicamente variou. Também é permitido definir uma abreviação em termos de um nome de zona em que essa abreviação não aparece; então, usar a abreviação é apenas equivalente a escrever o nome da zona.

### DICA

É preferível usar um número inteiro simples *`offset`* ao definir uma abreviação cujo deslocamento em relação ao UTC nunca tenha mudado, pois tais abreviações são muito mais baratas de processar do que aquelas que exigem consulta a uma definição de fuso horário.

A sintaxe `@INCLUDE` permite a inclusão de outro arquivo no diretório `.../share/timezonesets/`. A inclusão pode ser aninhada, até uma profundidade limitada.

A sintaxe `@OVERRIDE` indica que as entradas subsequentes no arquivo podem substituir as entradas anteriores (tipicamente, as entradas obtidas de arquivos incluídos). Sem isso, as definições conflitantes da mesma abreviação de fuso horário são consideradas um erro.

Em uma instalação não modificada, o arquivo `Default` contém todas as abreviações de fuso horário não conflitantes para a maioria do mundo. Arquivos adicionais `Australia` e `India` são fornecidos para essas regiões: esses arquivos incluem primeiro o arquivo `Default` e, em seguida, adicionam ou modificam as abreviações conforme necessário.

Para referência, uma instalação padrão também contém arquivos `Africa.txt`, `America.txt`, etc., contendo informações sobre cada abreviação de fuso horário conhecida que esteja em uso de acordo com o banco de dados de fuso horário da IANA. As definições de nome de zona encontradas nesses arquivos podem ser copiadas e coladas em um arquivo de configuração personalizado conforme necessário. Note que esses arquivos não podem ser referenciados diretamente como configurações `timezone_abbreviations`, devido ao ponto embutido em seus nomes.

### Nota

Se ocorrer um erro ao ler a abreviação do fuso horário definida, nenhum novo valor é aplicado e o conjunto antigo é mantido. Se o erro ocorrer ao iniciar o banco de dados, a inicialização falha.

### Atenção

As abreviações de fuso horário definidas no arquivo de configuração substituem os significados não de fuso horário integrados no PostgreSQL. Por exemplo, o arquivo de configuração `Australia` define `SAT` (para o Horário Padrão do Sul da Austrália). Quando este arquivo está ativo, `SAT` não será reconhecido como uma abreviação para sábado.

### Atenção

Se você modificar arquivos em `.../share/timezonesets/`, é sua responsabilidade fazer backups — um dump de banco de dados normal não incluirá esse diretório.