## ecpg

ecpg — pré-processador de SQL C embutido

## Sinopse

`ecpg` [*`option`*...] *`file`*...

## Descrição

`ecpg` é o pré-processador de SQL embutido para programas em C. Ele converte programas em C com declarações SQL embutidas em código C normal, substituindo as chamadas SQL por chamadas especiais de função. Os arquivos de saída podem então ser processados com qualquer ferramenta da cadeia de compiladores C.

`ecpg` converterá cada arquivo de entrada fornecido na linha de comando para o arquivo de saída correspondente em C. Se o nome do arquivo de entrada não tiver nenhuma extensão, `.pgc` é assumido. A extensão do arquivo será substituída por `.c` para construir o nome do arquivo de saída. Mas o nome do arquivo de saída pode ser sobrescrito usando a opção `-o`.

Se o nome do arquivo de entrada for apenas `-`, o programa lê o `ecpg` do padrão de entrada (e escreve na saída padrão, a menos que isso seja sobrescrito com `-o`).

Esta página de referência não descreve a linguagem SQL incorporada. Consulte o [Capítulo 34][(ecpg.md "Chapter 34. ECPG — Embedded SQL in C")] para obter mais informações sobre esse tópico.

## Opções

`ecpg` aceita os seguintes argumentos de linha de comando:

`-c`: Gerar automaticamente certos códigos C a partir de código SQL. Atualmente, isso funciona para `EXEC SQL TYPE`.

`-C mode`: Defina um modo de compatibilidade. *`mode`* pode ser `INFORMIX`, `INFORMIX_SE` ou `ORACLE`.

`-D symbol[=value]`: Defina um símbolo pré-processador, equivalente à diretiva `EXEC SQL DEFINE`. Se não for especificado um *`value`*, o símbolo é definido com o valor `1`.

`-h`: Arquivos de cabeçalho do processo. Quando esta opção é especificada, a extensão do arquivo de saída se torna `.h` e não `.c`, e a extensão padrão do arquivo de entrada é `.pgh` e não `.pgc`. Além disso, a opção `-c` é forçada.

`-i`: Analise também os arquivos de inclusão do sistema.

`-I directory`: Especifique um caminho de inclusão adicional, usado para encontrar arquivos incluídos via `EXEC SQL INCLUDE`. Os valores padrão são `.` (diretório atual), `/usr/local/include`, o diretório de inclusão do PostgreSQL que é definido no momento da compilação (padrão: `/usr/local/pgsql/include`) e `/usr/include`, nessa ordem.

`-o filename`: Especifica que `ecpg` deve escrever toda a sua saída no dado *`filename`*. Escreva `-o -` para enviar toda a saída para a saída padrão.

`-r option`: Seleciona o comportamento em tempo de execução. *`Option`* pode ser um dos seguintes:

`no_indicator` :   Não use indicadores, mas sim valores especiais para representar valores nulos. Historicamente, houve bancos de dados que utilizaram essa abordagem.

`prepare` :   Prepare todas as declarações antes de usá-las. O Libecpg manterá um cache de declarações preparadas e reutilizará uma declaração se ela for executada novamente. Se o cache ficar cheio, o libecpg liberará a declaração menos usada.

`questionmarks` : Permitir o ponto de interrogação como marcador de compatibilidade. Isso costumava ser o padrão há muito tempo.

`-t`: Ative o autocommit de transações. Nesse modo, cada comando SQL é automaticamente comprometido, a menos que esteja dentro de um bloco de transação explícito. No modo padrão, os comandos são comprometidos apenas quando `EXEC SQL COMMIT` é emitido.

`-v`: Imprima informações adicionais, incluindo a versão e o caminho de inclusão.

`--version`: Imprima a versão ecpg e saia.

`-?` `--help`: Mostrar ajuda sobre os argumentos da linha de comando do comando ecpg e sair.

## Notas

Ao compilar os arquivos de código C pré-processados, o compilador precisa ser capaz de encontrar os arquivos de cabeçalho ECPG no diretório de inclusão do PostgreSQL. Portanto, você pode precisar usar a opção `-I` ao invocar o compilador (por exemplo, `-I/usr/local/pgsql/include`).

Os programas que utilizam código C com SQL embutido precisam ser vinculados contra a biblioteca `libecpg`, por exemplo, usando as opções de vinculação `-L/usr/local/pgsql/lib -lecpg`.

O valor de qualquer um desses diretórios que é apropriado para a instalação pode ser encontrado usando [pg_config][(app-pgconfig.md "pg_config")].

## Exemplos

Se você tiver um arquivo de fonte C SQL embutido chamado `prog1.pgc`, você pode criar um programa executável usando a seguinte sequência de comandos:

```
ecpg prog1.pgc
cc -I/usr/local/pgsql/include -c prog1.c
cc -o prog1 prog1.o -L/usr/local/pgsql/lib -lecpg
```
