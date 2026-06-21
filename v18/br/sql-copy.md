## COPIAR

COPY — copiar dados entre um arquivo e uma tabela

## Sinopse

```
COPY table_name [ ( column_name [, ...] ) ]
    FROM { 'filename' | PROGRAM 'command' | STDIN }
    [ [ WITH ] ( option [, ...] ) ]
    [ WHERE condition ]

COPY { table_name [ ( column_name [, ...] ) ] | ( query ) }
    TO { 'filename' | PROGRAM 'command' | STDOUT }
    [ [ WITH ] ( option [, ...] ) ]

where option can be one of:

    FORMAT format_name
    FREEZE [ boolean ]
    DELIMITER 'delimiter_character'
    NULL 'null_string'
    DEFAULT 'default_string'
    HEADER [ boolean | MATCH ]
    QUOTE 'quote_character'
    ESCAPE 'escape_character'
    FORCE_QUOTE { ( column_name [, ...] ) | * }
    FORCE_NOT_NULL { ( column_name [, ...] ) | * }
    FORCE_NULL { ( column_name [, ...] ) | * }
    ON_ERROR error_action
    REJECT_LIMIT maxerror
    ENCODING 'encoding_name'
    LOG_VERBOSITY verbosity
```

## Descrição

`COPY` move dados entre tabelas do PostgreSQL e arquivos padrão do sistema de arquivos. `COPY TO` copia o conteúdo de uma tabela *para* um arquivo, enquanto `COPY FROM` copia dados *de* um arquivo para uma tabela (aplicando os dados ao que já está na tabela). `COPY TO` também pode copiar os resultados de uma consulta `SELECT`.

Se uma lista de colunas for especificada, `COPY TO` copia apenas os dados nas colunas especificadas no arquivo. Para `COPY FROM`, cada campo no arquivo é inserido, em ordem, na coluna especificada. As colunas da tabela que não são especificadas na lista de colunas do `COPY FROM` receberão seus valores padrão.

`COPY` com um nome de arquivo instrui o servidor PostgreSQL a ler diretamente de um arquivo ou a escrever em um arquivo. O arquivo deve ser acessível pelo usuário PostgreSQL (o ID do usuário pelo qual o servidor é executado) e o nome deve ser especificado do ponto de vista do servidor. Quando `PROGRAM` é especificado, o servidor executa o comando fornecido e lê a saída padrão do programa, ou escreve na entrada padrão do programa. O comando deve ser especificado do ponto de vista do servidor e ser executável pelo usuário PostgreSQL. Quando `STDIN` ou `STDOUT` é especificado, os dados são transmitidos através da conexão entre o cliente e o servidor.

Cada backend que executa `COPY` informará seu progresso na visualização `pg_stat_progress_copy`. Consulte [Seção 27.4.3][(progress-reporting.md#COPY-PROGRESS-REPORTING "27.4.3. COPY Progress Reporting")] para obter detalhes.

Por padrão, `COPY` falhará se encontrar um erro durante o processamento. Para casos de uso em que é desejada uma tentativa de melhor esforço para carregar todo o arquivo, a cláusula `ON_ERROR` pode ser usada para especificar outro comportamento.

## Parâmetros

*`table_name`*: O nome (opcionalmente qualificado por esquema) de uma tabela existente.

*`column_name`*: Uma lista opcional de colunas a serem copiadas. Se não for especificado nenhum catálogo de colunas, todas as colunas da tabela, exceto as colunas geradas, serão copiadas.

*`query`*: Um comando [`SELECT`(sql-select.md "SELECT"), [`VALUES`(sql-values.md "VALUES"), [`INSERT`(sql-insert.md "INSERT"), [`UPDATE`(sql-update.md "UPDATE"), [`DELETE`(sql-delete.md "DELETE"), ou [`MERGE`(sql-merge.md "MERGE")]] cujos resultados devem ser copiados. Observe que as chaves de consulta são necessárias ao redor das chaves.

Para as consultas `INSERT`, `UPDATE`, `DELETE` e `MERGE`, uma cláusula `RETURNING` deve ser fornecida, e a relação alvo não deve ter uma regra condicional, nem uma regra `ALSO` ou uma regra `INSTEAD` que se expanda para múltiplas declarações.

*`filename`*: O nome do caminho do arquivo de entrada ou saída. O nome de um arquivo de entrada pode ser um caminho absoluto ou relativo, mas o nome de um arquivo de saída deve ser um caminho absoluto. Os usuários do Windows podem precisar usar uma cadeia `E''` e duplicar quaisquer barras invertidas usadas no nome do caminho.

`PROGRAM`: Um comando a ser executado. Em `COPY FROM`, a entrada é lida a partir da saída padrão do comando, e em `COPY TO`, a saída é escrita na entrada padrão do comando.

Observe que o comando é invocado pelo shell, portanto, se você precisar passar quaisquer argumentos que venham de uma fonte não confiável, você deve ter cuidado para remover ou escapar quaisquer caracteres especiais que possam ter um significado especial para o shell. Por razões de segurança, é melhor usar uma string de comando fixa ou, pelo menos, evitar incluir qualquer entrada do usuário nela.

`STDIN`: Especifica que a entrada vem da aplicação do cliente.

`STDOUT`: Especifica que a saída vai para a aplicação do cliente.

*`boolean`*: Especifica se a opção selecionada deve ser ativada ou desativada. Você pode escrever `TRUE`, `ON` ou `1` para ativar a opção, e `FALSE`, `OFF` ou `0` para desativá-la. O valor *`boolean`* também pode ser omitido, no qual caso `TRUE` é assumido.

`FORMAT`: Seleciona o formato de dados a ser lido ou escrito: `text`, `csv` (Valores separados por vírgula) ou `binary`. O padrão é `text`. Consulte [Formatos de arquivo](sql-copy.md#SQL-COPY-FILE-FORMATS "File Formats") abaixo para obter detalhes.

`FREEZE`: Solicita a cópia dos dados com linhas já congeladas, assim como se fariam após executar o comando `VACUUM FREEZE`. Isso é destinado como uma opção de desempenho para o carregamento inicial dos dados. As linhas serão congeladas apenas se a tabela que está sendo carregada tiver sido criada ou truncada na subtransação atual, não houver cursors abertos e não houver instantâneos mais antigos mantidos por esta transação. Atualmente, não é possível realizar um `COPY FREEZE` em uma tabela particionada ou tabela estrangeira. Esta opção só é permitida em `COPY FROM`.

Observe que todas as outras sessões poderão visualizar os dados imediatamente após o carregamento bem-sucedido. Isso viola as regras normais de visibilidade do MVCC e os usuários devem estar cientes dos problemas potenciais que isso pode causar.

`DELIMITER`: Especifica o caractere que separa as colunas dentro de cada linha (linha) do arquivo. O padrão é um caractere de tabulação em formato de texto, uma vírgula em formato `CSV`. Isso deve ser um único caractere de um byte. Esta opção não é permitida ao usar o formato `binary`.

`NULL`: Especifica a string que representa um valor nulo. O padrão é `\N` (backslash-N) no formato de texto, e uma string vazia não citada em formato `CSV`. Você pode preferir uma string vazia mesmo no formato de texto para casos em que você não quer distinguir nulos de strings vazias. Esta opção não é permitida ao usar o formato `binary`.

### Nota

Ao usar `COPY FROM`, qualquer item de dados que corresponda a essa string será armazenado como um valor nulo, portanto, você deve garantir que você use a mesma string que você usou com `COPY TO`.

`DEFAULT`: Especifica a string que representa um valor padrão. Toda vez que a string for encontrada no arquivo de entrada, o valor padrão da coluna correspondente será usado. Esta opção é permitida apenas em `COPY FROM`, e apenas quando não estiver usando o formato `binary`.

`HEADER`: Especifica que o arquivo contém uma linha de cabeçalho com os nomes de cada coluna do arquivo. Na saída, a primeira linha contém os nomes das colunas da tabela. Na entrada, a primeira linha é descartada quando esta opção é definida para `true` (ou valor booleano equivalente). Se esta opção for definida para `MATCH`, o número e os nomes das colunas na linha de cabeçalho devem corresponder aos nomes reais das colunas da tabela, em ordem; caso contrário, um erro é gerado. Esta opção não é permitida ao usar o formato `binary`. A opção `MATCH` é válida apenas para comandos `COPY FROM`.

`QUOTE`: Especifica o caractere de citação a ser utilizado quando um valor de dados é citado. O padrão é a dupla citação. Isso deve ser um único caractere de um byte. Esta opção é permitida apenas quando se utiliza o formato `CSV`.

`ESCAPE`: Especifica o caractere que deve aparecer antes de um caractere de dados que corresponda ao valor do `QUOTE`. O padrão é o mesmo que o valor do `QUOTE` (para que o caractere de citação seja duplicado se aparecer nos dados). Isso deve ser um único caractere de um byte. Esta opção é permitida apenas ao usar o formato `CSV`.

`FORCE_QUOTE`: Forças que devem ser usadas para todos os valores que não são `NULL` em cada coluna especificada. A saída `NULL` nunca é citada. Se `*` for especificado, os valores que não são `NULL` serão citados em todas as colunas. Esta opção é permitida apenas em `COPY TO`, e apenas quando usando o formato `CSV`.

`FORCE_NOT_NULL`: Não faça correspondência entre os valores das colunas especificadas e a string nula. No caso padrão, onde a string nula é vazia, isso significa que valores vazios serão lidos como strings de comprimento zero, em vez de nulos, mesmo quando não são citados. Se `*` for especificado, a opção será aplicada a todas as colunas. Esta opção é permitida apenas em `COPY FROM`, e apenas quando usando o formato `CSV`.

`FORCE_NULL`: Ajuste os valores das colunas especificadas contra a string nula, mesmo que tenha sido citada, e se uma correspondência for encontrada, defina o valor como `NULL`. No caso padrão, onde a string nula é vazia, isso converte uma string vazia citada em NULL. Se `*` for especificado, a opção será aplicada a todas as colunas. Esta opção é permitida apenas em `COPY FROM`, e apenas quando usando o formato `CSV`.

`ON_ERROR`: Especifica como se comportar ao encontrar um erro ao converter o valor de entrada de uma coluna em seu tipo de dados. Um valor de *`error_action`* de `stop` significa falhar o comando, enquanto `ignore` significa descartar a linha de entrada e continuar com a próxima. O padrão é `stop`.

A opção `ignore` é aplicável apenas para `COPY FROM` quando o `FORMAT` é `text` ou `csv`.

Uma mensagem `NOTICE` contendo o número de linhas ignoradas é emitida no final do `COPY FROM` se pelo menos uma linha foi descartada. Quando a opção `LOG_VERBOSITY` é definida como `verbose`, uma mensagem `NOTICE` contendo a linha do arquivo de entrada e o nome da coluna cuja conversão de entrada falhou é emitida para cada linha descartada. Quando definida como `silent`, nenhuma mensagem é emitida em relação às linhas ignoradas.

`REJECT_LIMIT`: Especifica o número máximo de erros tolerados durante a conversão do valor de entrada de uma coluna para seu tipo de dados, quando `ON_ERROR` está definido como `ignore`. Se a entrada causar mais erros do que o valor especificado, o comando `COPY` falha, mesmo com `ON_ERROR` definido como `ignore`. Esta cláusula deve ser usada com `ON_ERROR`=`ignore` e *`maxerror`* deve ser positivo `bigint`. Se não especificado, `ON_ERROR`=`ignore` permite um número ilimitado de erros, o que significa que `COPY` ignorará todos os dados errôneos.

`ENCODING`: Especifica que o arquivo está codificado no *`encoding_name`*. Se esta opção for omitida, a codificação atual do cliente é usada. Consulte as Notas abaixo para mais detalhes.

`LOG_VERBOSITY`: Especifica a quantidade de mensagens emitidas por um comando `COPY`: `default`, `verbose` ou `silent`. Se `verbose` for especificado, mensagens adicionais são emitidas durante o processamento. `silent` suprime tanto as mensagens verbais quanto as mensagens padrão.

Isso é atualmente utilizado no comando `COPY FROM` quando a opção `ON_ERROR` é definida como `ignore`.

`WHERE`: A cláusula opcional `WHERE` tem a forma geral

``` WHERE condition
    ```

onde *`condition`* é qualquer expressão que avalie um resultado do tipo `boolean`. Qualquer linha que não satisfaça essa condição não será inserida na tabela. Uma linha satisfaz a condição se retornar verdadeiro quando os valores reais da linha são substituídos por quaisquer referências de variáveis.

Atualmente, subconsultas não são permitidas em expressões do `WHERE`, e a avaliação não vê quaisquer alterações feitas pelo próprio `COPY` (isso é importante quando a expressão contém chamadas a funções do `VOLATILE`).

## Saídas

Após a conclusão bem-sucedida, um comando `COPY` retorna uma tag de comando na forma de

```
COPY count
```

O *`count`* é o número de linhas copiadas.

### Nota

O psql imprimirá essa marca de comando apenas se o comando não for `COPY ... TO STDOUT`, ou o equivalente ao meta-comando psql `\copy ... to stdout`. Isso é para evitar confundir a marca de comando com os dados que foram impressos.

## Notas

`COPY TO` pode ser usado com tabelas simples e visualizações materializadas preenchidas. Por exemplo, `COPY table TO` copia as mesmas linhas que `SELECT * FROM ONLY table`. No entanto, ele não suporta diretamente outros tipos de relação, como tabelas particionadas, tabelas filhas de herança ou visualizações. Para copiar todas as linhas desses relacionamentos, use `COPY (SELECT * FROM table) TO`.

`COPY FROM` pode ser usado com tabelas comuns, estrangeiras ou particionadas ou com visualizações que possuem gatilhos `INSTEAD OF INSERT`.

Você deve ter privilégio seletivo na tabela cujos valores são lidos por `COPY TO`, e privilégio de inserção na tabela na qual os valores são inseridos por `COPY FROM`. É suficiente ter privilégios de coluna na(s) coluna(s) listada(s) no comando.

Se a segurança de nível de linha estiver habilitada para a tabela, as políticas relevantes do `SELECT` serão aplicadas às declarações do `COPY table TO`. Atualmente, o `COPY FROM` não é suportado para tabelas com segurança de nível de linha. Use declarações equivalentes do `INSERT` em vez disso.

Os arquivos nomeados em um comando `COPY` são lidos ou escritos diretamente pelo servidor, não pela aplicação cliente. Portanto, eles devem residir no servidor de banco de dados ou ser acessíveis ao servidor do banco de dados, não ao cliente. Eles devem ser acessíveis e legíveis ou modificáveis pelo usuário PostgreSQL (o usuário pelo qual o servidor é executado), não pelo cliente. Da mesma forma, o comando especificado com `PROGRAM` é executado diretamente pelo servidor, não pela aplicação cliente, e deve ser executável pelo usuário PostgreSQL. A nomeação de um arquivo ou comando com `COPY` é permitida apenas para superusuários do banco de dados ou usuários que tenham sido concedidos um dos papéis `pg_read_server_files`, `pg_write_server_files` ou `pg_execute_server_program`, pois permite a leitura ou escrita de qualquer arquivo ou execução de um programa pelo qual o servidor tenha privilégios de acesso.

Não confunda `COPY` com a instrução psql `\copy`. `\copy` invoca `COPY FROM STDIN` ou `COPY TO STDOUT`, e depois recupera/armazena os dados em um arquivo acessível ao cliente psql. Assim, a acessibilidade do arquivo e os direitos de acesso dependem do cliente, e não do servidor, quando `\copy` é usado.

Recomenda-se que o nome do arquivo usado em `COPY` seja sempre especificado como um caminho absoluto. Isso é exigido pelo servidor no caso de `COPY TO`, mas para `COPY FROM` você tem a opção de ler a partir de um arquivo especificado por um caminho relativo. O caminho será interpretado em relação ao diretório de trabalho do processo do servidor (normalmente o diretório de dados do clúster), e não o diretório de trabalho do cliente.

A execução de um comando com `PROGRAM` pode ser restringida pelos mecanismos de controle de acesso do sistema operacional, como o SELinux.

`COPY FROM` irá invocar quaisquer gatilhos e restrições de verificação na tabela de destino. No entanto, não irá invocar regras.

Para as colunas de identidade, o comando `COPY FROM` sempre escreverá os valores da coluna fornecidos nos dados de entrada, como a opção `OVERRIDING SYSTEM VALUE` do `INSERT`.

A entrada e saída do `COPY` são afetadas pelo `DateStyle`. Para garantir a portabilidade para outras instalações do PostgreSQL que possam usar configurações não padrão do `DateStyle`, o `DateStyle` deve ser definido como `ISO` antes de usar o `COPY TO`. Também é uma boa ideia evitar o dumping de dados com o `IntervalStyle` definido como `sql_standard`, porque valores de intervalo negativos podem ser mal interpretados por um servidor que tenha uma configuração diferente para o `IntervalStyle`.

Os dados de entrada são interpretados de acordo com a opção `ENCODING` ou o codificação atual do cliente, e os dados de saída são codificados em `ENCODING` ou a codificação atual do cliente, mesmo que os dados não passem pelo cliente, mas sejam lidos ou escritos diretamente em um arquivo pelo servidor.

O comando `COPY FROM` insere fisicamente as linhas de entrada na tabela à medida que ela progride. Se o comando falhar, essas linhas permanecem em estado de exclusão; essas linhas não serão visíveis, mas ainda ocuparão espaço em disco. Isso pode representar um espaço em disco desperdiçado considerável se a falha ocorrer bem em uma operação de cópia grande. O `VACUUM` deve ser usado para recuperar o espaço desperdiçado.

`FORCE_NULL` e `FORCE_NOT_NULL` podem ser usados simultaneamente na mesma coluna. Isso resulta na conversão de cadeias de texto nulos citados em valores nulos e cadeias de texto nulos não citados em cadeias vazias.

## Formatos de Arquivo

### Formato de texto

Quando o formato `text` é usado, os dados lidos ou escritos são um arquivo de texto com uma linha por linha de tabela. As colunas em uma linha são separadas pelo caractere delimitador. Os próprios valores das colunas são cadeias geradas pela função de saída, ou aceitáveis para a função de entrada, do tipo de dados de cada atributo. A string nula especificada é usada no lugar das colunas que são nulos. `COPY FROM` levantará um erro se qualquer linha do arquivo de entrada contiver mais ou menos colunas do que o esperado.

O fim dos dados pode ser representado por uma linha contendo apenas barra invertida e ponto (`\.`). Um marcador de fim de dados não é necessário ao ler de um arquivo, uma vez que o fim do arquivo serve perfeitamente bem; nesse contexto, essa disposição existe apenas para compatibilidade reversa. No entanto, o psql usa `\.` para finalizar uma operação `COPY FROM STDIN` (ou seja, ler dados em linha `COPY` em um script SQL). Nesse contexto, a regra é necessária para poder finalizar a operação antes do fim do script.

Os caracteres de barra invertida (`\`) podem ser usados nos dados `COPY` para citar caracteres de dados que, de outra forma, poderiam ser tomados como delimitadores de linha ou coluna. Em particular, os seguintes caracteres *devem* ser precedidos por uma barra invertida se aparecerem como parte de um valor de coluna: a própria barra invertida, nova linha, retorno de carro e o caractere de delimitador atual.

A string nula especificada é enviada por `COPY TO` sem adicionar barras invertidas; por outro lado, `COPY FROM` corresponde à entrada contra a string nula antes de remover as barras invertidas. Portanto, uma string nula como `\N` não pode ser confundida com o valor real dos dados `\N` (que seria representado como `\\N`).

As seguintes sequências de barra invertida especiais são reconhecidas por `COPY FROM`:



<table border="1" class="informaltable">
<colgroup>
<col/>
<col/>
</colgroup>
<thead>
<tr>
<th>
    Sequence
   </th>
<th>Representa</th>
</tr>
</thead>
<tbody>
<tr>
<td>
<code class="literal">
     \b
    </code>
</td>
<td>Backspace (ASCII 8)</td>
</tr>
<tr>
<td>
<code class="literal">
     \f
    </code>
</td>
<td>Retorno de formulário (ASCII 12)</td>
</tr>
<tr>
<td>
<code class="literal">
     \n
    </code>
</td>
<td>Newline (ASCII 10)</td>
</tr>
<tr>
<td>
<code class="literal">
     \r
    </code>
</td>
<td>Retorno de carroça (ASCII 13)</td>
</tr>
<tr>
<td>
<code class="literal">
     \t
    </code>
</td>
<td>Tab (ASCII 9)</td>
</tr>
<tr>
<td>
<code class="literal">
     \v
    </code>
</td>
<td>Guia vertical (ASCII 11)</td>
</tr>
<tr>
<td>
<code class="literal">
     \
    </code>
<em class="replaceable">
<code>
      digits
     </code>
</em>
</td>
<td>Backslash seguido por um a três dígitos octal especifica o byte com aquele código numérico</td>
</tr>
<tr>
<td>
<code class="literal">
     \x
    </code>
<em class="replaceable">
<code>
      digits
     </code>
</em>
</td>
<td>Barra de retorno<code class="literal">
     x
    </code>seguido por um ou dois dígitos hexadecimais especifica o byte com aquele código numérico</td>
</tr>
</tbody>
</table>



Atualmente, `COPY TO` nunca emitirá uma sequência de barra invertida de octal ou hexaliteral, mas utiliza as outras sequências listadas acima para esses caracteres de controle.

Qualquer outro caractere com barra invertida que não seja mencionado na tabela acima será considerado como ele mesmo. No entanto, tenha cuidado em adicionar barras invertidas desnecessariamente, pois isso pode produzir acidentalmente uma string que corresponda ao marcador de fim de dados (`\.`) ou à string nula (`\N` por padrão). Essas strings serão reconhecidas antes de qualquer outro processamento de barra invertida ser feito.

É fortemente recomendado que as aplicações que geram dados do `COPY` convertam as novas linhas e os retornos de carro em sequência dos `\n` e `\r`, respectivamente. Atualmente, é possível representar um retorno de carro de dados por uma barra invertida e retorno de carro, e representar uma nova linha de dados por uma barra invertida e nova linha. No entanto, essas representações podem não ser aceitas em versões futuras. Elas também são altamente vulneráveis à corrupção se o arquivo `COPY` for transferido entre diferentes máquinas (por exemplo, de Unix para Windows ou vice-versa).

Todas as sequências de barra invertida são interpretadas após a conversão de codificação. Os bytes especificados com as sequências de barra invertida octal e hexadecimal devem formar caracteres válidos na codificação do banco de dados.

`COPY TO` terminará cada linha com uma nova linha de estilo Unix (“`\n`”). Servidores que funcionam no Microsoft Windows, em vez disso, produzem retorno de carro e nova linha (“`\r\n`”), mas apenas para `COPY` em um arquivo de servidor; para consistência entre plataformas, `COPY TO STDOUT` envia sempre “`\n`”, independentemente da plataforma do servidor. `COPY FROM` pode lidar com linhas que terminam com novas linhas, retornos de carro ou retornos de carro e novas linhas. Para reduzir o risco de erro devido a novas linhas ou retornos de carro que não foram assegurados, `COPY FROM` reclamará se as extremidades de linha no input não forem todas iguais.

### Formato CSV

Essa opção de formato é usada para importar e exportar o formato de arquivo Comma-Separated Value (`CSV`) utilizado por muitos outros programas, como planilhas. Em vez das regras de escape usadas pelo formato de texto padrão do PostgreSQL, ele produz e reconhece o mecanismo de escape comum `CSV`.

Os valores em cada registro são separados pelo caractere `DELIMITER`. Se o valor contiver o caractere delimitador `QUOTE`, a string `NULL`, um retorno de carro ou caractere de nova linha, então todo o valor é prefixado e sufixado pelo caractere `QUOTE`, e qualquer ocorrência dentro do valor de um caractere `QUOTE` ou o caractere `ESCAPE` é precedido pelo caractere de escape. Você também pode usar `FORCE_QUOTE` para forçar aspas ao emitir valores não `NULL` em colunas específicas.

O formato `CSV` não tem uma maneira padrão de distinguir um valor `NULL` de uma string vazia. O `COPY` do PostgreSQL lida com isso usando citação. Um `NULL` é exibido como a string de parâmetro `NULL` e não é citado, enquanto um valor não `NULL` que corresponde à string de parâmetro `NULL` é citado. Por exemplo, com as configurações padrão, um `NULL` é escrito como uma string vazia não citada, enquanto um valor de dados de string com aspas duplas (`""`) é escrito. A leitura de valores segue regras semelhantes. Você pode usar `FORCE_NOT_NULL` para evitar comparações de entrada `NULL` para colunas específicas. Você também pode usar `FORCE_NULL` para converter valores de dados de string com null citado em `NULL`.

Como o backslash não é um caractere especial no formato `CSV`, o marcador de fim de dados usado no modo de texto (`\.`) não é normalmente tratado como especial ao ler dados do `CSV`. Uma exceção é que o psql terminará uma operação `COPY FROM STDIN` (ou seja, a leitura de dados `COPY` em linha em um script SQL) em uma linha que contenha apenas `\.`, seja em modo de texto ou `CSV`.

### Nota

As versões do PostgreSQL anteriores à v18 sempre reconheceram o `\.` não citado como um marcador de fim de dados, mesmo ao ler de um arquivo separado. Para compatibilidade com versões mais antigas, o `COPY TO` irá citar o `\.` quando estiver sozinho em uma linha, embora isso não seja mais necessário.

### Nota

No formato `CSV`, todos os caracteres são significativos. Um valor citado cercado por espaço em branco, ou quaisquer outros caracteres que não sejam `DELIMITER`, incluirão esses caracteres. Isso pode causar erros se você importar dados de um sistema que preench a `CSV` linhas com espaço em branco até uma largura fixa. Se tal situação surgir, você pode precisar pré-processar o arquivo `CSV` para remover o espaço em branco final, antes de importar os dados no PostgreSQL.

### Nota

O formato `CSV` reconhecerá e produzirá arquivos `CSV` com valores citados que contêm retornos de carro e rodízio de linha embutidos. Assim, os arquivos não são estritamente uma linha por linha de tabela, como os arquivos de formato de texto.

### Nota

Muitos programas produzem arquivos estranhos e, por vezes, perversos `CSV`, portanto, o formato do arquivo é mais uma convenção do que um padrão. Assim, você pode encontrar alguns arquivos que não podem ser importados usando esse mecanismo, e o `COPY` pode produzir arquivos que outros programas não podem processar.

### Formato Binário

A opção de formato `binary` faz com que todos os dados sejam armazenados/lidos como formato binário, em vez de como texto. É um pouco mais rápido do que os formatos de texto e `CSV` e, embora um arquivo em formato binário seja menos portátil em diferentes arquiteturas de máquina e versões do PostgreSQL, o formato binário é muito específico para o tipo de dado; por exemplo, não funcionará para saída de dados binários de uma coluna `smallint` e leitura em uma coluna `integer`, embora isso funcione bem no formato de texto.

O formato de arquivo `binary` consiste em um cabeçalho de arquivo, zero ou mais tuplas contendo os dados da linha e um trailer de arquivo. Os cabeçalhos e os dados estão no formato de byte da rede.

### Nota

Os releases do PostgreSQL anteriores à versão 7.4 utilizavam um formato de arquivo binário diferente.

#### Cabeçalho do arquivo

O cabeçalho do arquivo consiste em 15 bytes de campos fixos, seguido de uma área de extensão de cabeçalho de comprimento variável. Os campos fixos são:

Assinatura: sequência de 11 bytes `PGCOPY\n\377\r\n\0` — observe que o byte zero é uma parte necessária da assinatura. (A assinatura é projetada para permitir a identificação fácil de arquivos que foram modificados por uma transferência não limpa de 8 bits. Esta assinatura será alterada por filtros de tradução de fim de linha, bytes zerados, bits altos descartados ou mudanças de paridade.)

Campo de flags: máscara de bits inteiro de 32 bits para denotar aspectos importantes do formato do arquivo. Os bits são numerados de 0 (LSB) a 31 (MSB). Note que este campo é armazenado na ordem de byte da rede (byte mais significativo primeiro), assim como todos os campos inteiros usados no formato do arquivo. Os bits 16–31 são reservados para denotar problemas críticos de formato de arquivo; um leitor deve abortar se encontrar um bit inesperado configurado neste intervalo. Os bits 0–15 são reservados para sinalizar problemas de formato compatível com versões anteriores; um leitor deve simplesmente ignorar quaisquer bits inesperados configurados neste intervalo. Atualmente, apenas um bit de sinalização é definido, e o restante deve ser zero:

Bit 16:   Se 1, os OIDs estão incluídos nos dados; se 0, não. As colunas do sistema Oid não são suportadas no PostgreSQL, mas o formato ainda contém o indicador.

Comprimento da área de extensão do cabeçalho: inteiro de 32 bits, comprimento em bytes do restante do cabeçalho, excluindo o próprio. Atualmente, este é zero, e a primeira tupla segue imediatamente. Alterações futuras no formato podem permitir que dados adicionais estejam presentes no cabeçalho. Um leitor deve ignorar silenciosamente qualquer dado de extensão do cabeçalho que não saiba o que fazer com.

O espaço de extensão do cabeçalho é projetado para conter uma sequência de blocos autoidentificáveis. O campo de bandeiras não é destinado a dizer aos leitores o que está na área de extensão. O design específico do conteúdo da extensão do cabeçalho é deixado para uma versão posterior.

Esse projeto permite tanto adições de cabeçalho compatíveis com versões anteriores (adicionar blocos de extensão de cabeçalho ou definir bits de sinalização de bits de ordem baixa) quanto alterações não compatíveis com versões anteriores (definir bits de sinalização de bits de ordem alta para sinalizar tais alterações e adicionar dados de suporte à área de extensão, se necessário).

#### Tuplas

Cada tupla começa com um contador de 16 bits do número de campos na tupla. (Atualmente, todas as tuplas em uma tabela terão o mesmo contador, mas isso nem sempre será o caso.) Em seguida, repetido para cada campo na tupla, há uma palavra de comprimento de 32 bits seguida por tantos bytes de dados do campo. (O termo de comprimento não inclui a palavra em si e pode ser zero.) Como um caso especial, -1 indica um valor de campo NULL. Não há bytes de valor após o caso NULL.

Não há alinhamento de preenchimento ou qualquer outro dado extra entre os campos.

Atualmente, todos os valores de dados em um arquivo em formato binário são assumidos como em formato binário (código de formato um). Espera-se que uma futura extensão possa adicionar um campo de cabeçalho que permita especificar códigos de formato por coluna.

Para determinar o formato binário apropriado para os dados reais da tupla, você deve consultar a fonte do PostgreSQL, em particular as funções `*send` e `*recv` para o tipo de dados de cada coluna (tipicamente, essas funções são encontradas no diretório `src/backend/utils/adt/` da distribuição da fonte).

Se os OIDs estiverem incluídos no arquivo, o campo OID vem imediatamente após a palavra de contagem de campos. É um campo normal, exceto que não está incluído na contagem de campos. Note que as colunas de sistema oid não são suportadas nas versões atuais do PostgreSQL.

#### Trailer do arquivo

O trailer do arquivo consiste em uma palavra de inteiro de 16 bits contendo -1. Isso é facilmente distinguível da palavra de contagem de campos de uma tupla.

Um leitor deve relatar um erro se uma palavra de contagem de campo não for nem -1 nem o número esperado de colunas. Isso fornece uma verificação adicional para evitar ficar desequilibrado com os dados.

## Exemplos

O exemplo a seguir copia uma tabela para o cliente usando a barra vertical (`|`) como delimitador de campo:

```
COPY country TO STDOUT (DELIMITER '|');
```

Para copiar dados de um arquivo para a tabela `country`:

```
COPY country FROM '/usr1/proj/bray/sql/country_data';
```

Para copiar em um arquivo apenas os países cujos nomes começam com 'A':

```
COPY (SELECT * FROM country WHERE country_name LIKE 'A%') TO '/usr1/proj/bray/sql/a_list_countries.copy';
```

Para copiar em um arquivo compactado, você pode encaminhar a saída através de um programa de compressão externo:

```
COPY country TO PROGRAM 'gzip > /usr1/proj/bray/sql/country_data.gz';
```

Aqui está um exemplo de dados adequados para copiar em uma tabela a partir de `STDIN`:

```
AF      AFGHANISTAN AL      ALBANIA DZ      ALGERIA ZM      ZAMBIA ZW      ZIMBABWE
```

Observe que o espaço em branco em cada linha é, na verdade, um caractere de tabulação.

O que se segue são os mesmos dados, exibidos em formato binário. Os dados são mostrados após filtragem através do utilitário Unix `od -c`. A tabela tem três colunas; a primeira tem tipo `char(2)`, a segunda tem tipo `text` e a terceira tem tipo `integer`. Todas as linhas têm um valor nulo na terceira coluna.

```
0000000   P   G   C   O   P   Y  \n 377  \r  \n  \0  \0  \0  \0  \0  \0 0000020  \0  \0  \0  \0 003  \0  \0  \0 002   A   F  \0  \0  \0 013   A 0000040   F   G   H   A   N   I   S   T   A   N 377 377 377 377  \0 003 0000060  \0  \0  \0 002   A   L  \0  \0  \0 007   A   L   B   A   N   I 0000100   A 377 377 377 377  \0 003  \0  \0  \0 002   D   Z  \0  \0  \0 0000120 007   A   L   G   E   R   I   A 377 377 377 377  \0 003  \0  \0 0000140  \0 002   Z   M  \0  \0  \0 006   Z   A   M   B   I   A 377 377 0000160 377 377  \0 003  \0  \0  \0 002   Z   W  \0  \0  \0  \b   Z   I 0000200   M   B   A   B   W   E 377 377 377 377 377 377
```

## Compatibilidade

Não há nenhuma declaração `COPY` no padrão SQL.

A sintaxe a seguir foi usada antes da versão 9.0 do PostgreSQL e ainda é suportada:

```
COPY table_name [ ( column_name [, ...] ) ] FROM { 'filename' | STDIN } [ [ WITH ] [ BINARY ] [ DELIMITER [ AS ] 'delimiter_character' ] [ NULL [ AS ] 'null_string' ] [ CSV [ HEADER ] [ QUOTE [ AS ] 'quote_character' ] [ ESCAPE [ AS ] 'escape_character' ] [ FORCE NOT NULL column_name [, ...] ] ] ]

COPY { table_name [ ( column_name [, ...] ) ] | ( query ) } TO { 'filename' | STDOUT } [ [ WITH ] [ BINARY ] [ DELIMITER [ AS ] 'delimiter_character' ] [ NULL [ AS ] 'null_string' ] [ CSV [ HEADER ] [ QUOTE [ AS ] 'quote_character' ] [ ESCAPE [ AS ] 'escape_character' ] [ FORCE QUOTE { column_name [, ...] | * } ] ] ]
```

Observe que, nesta sintaxe, `BINARY` e `CSV` são tratados como palavras-chave independentes, não como argumentos de uma opção `FORMAT`.

A sintaxe a seguir foi usada antes da versão 7.3 do PostgreSQL e ainda é suportada:

```
COPY [ BINARY ] table_name FROM { 'filename' | STDIN } [ [USING] DELIMITERS 'delimiter_character' ] [ WITH NULL AS 'null_string' ]

COPY [ BINARY ] table_name TO { 'filename' | STDOUT } [ [USING] DELIMITERS 'delimiter_character' ] [ WITH NULL AS 'null_string' ]
```

## Veja também

[Seção 27.4.3](progress-reporting.md#COPY-PROGRESS-REPORTING "27.4.3. COPY Progress Reporting")