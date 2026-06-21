## SPI_prepare

SPI_prepare — preparar uma declaração, sem executá-la ainda

## Sinopse

```
SPIPlanPtr SPI_prepare(const char * command, int nargs, Oid * argtypes)
```

## Descrição

`SPI_prepare` cria e retorna uma declaração preparada para o comando especificado, mas não executa o comando. A declaração preparada pode ser executada repetidamente posteriormente usando `SPI_execute_plan`.

Quando o mesmo ou um comando semelhante deve ser executado repetidamente, geralmente é vantajoso realizar a análise de parse apenas uma vez e, além disso, pode ser vantajoso reutilizar um plano de execução para o comando. `SPI_prepare` converte uma string de comando em uma declaração preparada que encapsula os resultados da análise de parse. A declaração preparada também fornece um local para cachear um plano de execução, se for encontrado que gerar um plano personalizado para cada execução não é útil.

Um comando preparado pode ser generalizado escrevendo parâmetros (`$1`, `$2`, etc.) no lugar do que seria constantes em um comando normal. Os valores reais dos parâmetros são então especificados quando `SPI_execute_plan` é chamado. Isso permite que o comando preparado seja usado em uma faixa mais ampla de situações do que seria possível sem parâmetros.

A declaração devolvida por `SPI_prepare` pode ser usada apenas na invocação atual da função C, uma vez que `SPI_finish` libera a memória alocada para tal declaração. Mas a declaração pode ser salva por mais tempo usando as funções `SPI_keepplan` ou `SPI_saveplan`.

## Argumentos

`const char * command`: string de comando

`int nargs`: número de parâmetros de entrada (`$1`, `$2`, etc.)

`Oid * argtypes`: ponteiro para um array contendo os OIDs dos tipos de dados dos parâmetros

## Valor de retorno

`SPI_prepare` retorna um ponteiro não nulo para um `SPIPlan`, que é uma estrutura opaca que representa uma declaração preparada. Em caso de erro, `NULL` será retornado e `SPI_result` será definido para um dos mesmos códigos de erro usados por `SPI_execute`, exceto que é definido para `SPI_ERROR_ARGUMENT` se *`command`* é `NULL`, ou se *`nargs`* é menor que 0, ou se *`nargs`* é maior que 0 e *`argtypes`* é `NULL`.

## Notas

Se não forem definidos parâmetros, um plano genérico será criado na primeira utilização de `SPI_execute_plan`, e utilizado para todas as execuções subsequentes também. Se houver parâmetros, os primeiros usos de `SPI_execute_plan` gerarão planos personalizados que são específicos aos valores do parâmetro fornecidos. Após o uso suficiente da mesma declaração preparada, `SPI_execute_plan` construirá um plano genérico, e se isso não for muito mais caro do que os planos personalizados, começará a usar o plano genérico em vez de planejar novamente a cada vez. Se esse comportamento padrão não for adequado, você pode alterá-lo passando a bandeira `CURSOR_OPT_GENERIC_PLAN` ou `CURSOR_OPT_CUSTOM_PLAN` para `SPI_prepare_cursor`, para forçar o uso de planos genéricos ou personalizados, respectivamente.

Embora o principal objetivo de uma declaração preparada seja evitar a análise e o planejamento repetidos da declaração, o PostgreSQL forçará a reanálise e o replanejamento da declaração antes de usá-la sempre que os objetos do banco de dados utilizados na declaração tenham sofrido alterações definicionais (DDL) desde o uso anterior da declaração preparada. Além disso, se o valor de [search_path](runtime-config-client.md#GUC-SEARCH-PATH) mudar de uma utilização para a próxima, a declaração será reanalisada usando o novo `search_path`. (Esse comportamento é novo a partir do PostgreSQL 9.3.) Consulte [PREPARE](sql-prepare.md) para obter mais informações sobre o comportamento das declarações preparadas.

Essa função deve ser chamada apenas a partir de uma função C conectada.

`SPIPlanPtr` é declarado como um ponteiro para um tipo de estrutura opaca em `spi.h`. Não é prudente tentar acessar diretamente seu conteúdo, pois isso torna seu código muito mais propenso a quebrar em futuras revisões do PostgreSQL.

O nome `SPIPlanPtr` é um tanto histórico, uma vez que a estrutura de dados não contém mais necessariamente um plano de execução.