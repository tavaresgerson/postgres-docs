## 34.8. Gerenciamento de Erros [#](#ECPG-ERRORS)

* [34.8.1. Retornos de chamada][(ecpg-errors.md#ECPG-WHENEVER)]
* [34.8.2. sqlca][(ecpg-errors.md#ECPG-SQLCA)]
* [34.8.3. `SQLSTATE` vs. `SQLCODE`[(ecpg-errors.md#ECPG-SQLSTATE-SQLCODE)]

Esta seção descreve como você pode lidar com condições excepcionais e avisos em um programa de SQL incorporado. Existem duas facilidades não exclusivas para isso.

* Os callbacks podem ser configurados para lidar com condições de alerta e erro usando o comando `WHENEVER`. * Informações detalhadas sobre o erro ou alerta podem ser obtidas a partir da variável `sqlca`.

### 34.8.1. Configuração de callbacks [#](#ECPG-WHENEVER)

Um método simples para detectar erros e avisos é definir uma ação específica que será executada sempre que uma condição particular ocorrer. Em geral:

```
EXEC SQL WHENEVER condition action;
```

*`condition`* pode ser um dos seguintes:

`SQLERROR` [#](#ECPG-WHENEVER-SQLERROR): A ação especificada é chamada sempre que ocorre um erro durante a execução de uma declaração SQL.

`SQLWARNING` [#](#ECPG-WHENEVER-SQLWARNING): A ação especificada é chamada sempre que ocorre um aviso durante a execução de uma declaração SQL.

`NOT FOUND` [#](#ECPG-WHENEVER-NOT-FOUND): A ação especificada é chamada sempre que uma declaração SQL recupera ou afeta zero linhas. (Essa condição não é um erro, mas você pode estar interessado em tratá-la especialmente.)

*`action`* pode ser um dos seguintes:

`CONTINUE` [#](#ECPG-WHENEVER-CONTINUE): Isso significa que a condição é ignorada. Esse é o padrão.

`GOTO label` `GO TO label` [#](#ECPG-WHENEVER-GOTO): Saltar para o rótulo especificado (usando uma declaração C `goto`).

`SQLPRINT` [#](#ECPG-WHENEVER-SQLPRINT): Imprimir uma mensagem para o erro padrão. Isso é útil para programas simples ou durante a prototipagem. Os detalhes da mensagem não podem ser configurados.

`STOP` [#](#ECPG-WHENEVER-STOP): Chame `exit(1)`, que terminará o programa.

`DO BREAK` [#](#ECPG-WHENEVER-DO-BREAK): Execute a declaração C `break`. Isso deve ser usado apenas em loops ou declarações `switch`.

`DO CONTINUE` [#](#ECPG-WHENEVER-DO-CONTINUE): Execute a declaração C `continue`. Isso deve ser usado apenas em declarações de loops. Se executado, fará com que o fluxo de controle retorne ao topo do loop.

`CALL name (args)` `DO name (args)` [#](#ECPG-WHENEVER-CALL): Chame as funções C especificadas com os argumentos especificados. (Este uso é diferente do significado de `CALL` e `DO` na gramática normal do PostgreSQL.)

O padrão SQL apenas prevê as ações `CONTINUE` e `GOTO` (e `GO TO`).

Aqui está um exemplo que você pode querer usar em um programa simples. Ele imprime uma mensagem simples quando ocorre um aviso e interrompe o programa quando ocorre um erro:

```
EXEC SQL WHENEVER SQLWARNING SQLPRINT;
EXEC SQL WHENEVER SQLERROR STOP;
```

A declaração `EXEC SQL WHENEVER` é uma directiva do pré-processador SQL, não uma declaração em C. As ações de erro ou aviso que ela define se aplicam a todas as declarações SQL incorporadas que aparecem abaixo do ponto onde o manipulador é definido, a menos que uma ação diferente tenha sido definida para a mesma condição entre o primeiro `EXEC SQL WHENEVER` e a declaração SQL que causa a condição, independentemente do fluxo de controle no programa em C. Portanto, nenhum dos dois trechos de programa em C a seguir terá o efeito desejado:

```
/*
 * WRONG
 */
int main(int argc, char *argv[])
{
    ...
    if (verbose) {
        EXEC SQL WHENEVER SQLWARNING SQLPRINT;
    }
    ...
    EXEC SQL SELECT ...;
    ...
}
```

```
/*
 * WRONG
 */
int main(int argc, char *argv[])
{
    ...
    set_error_handler();
    ...
    EXEC SQL SELECT ...;
    ...
}

static void set_error_handler(void)
{
    EXEC SQL WHENEVER SQLERROR STOP;
}
```

### 34.8.2. sqlca [#](#ECPG-SQLCA)

Para uma manipulação de erros mais poderosa, a interface de SQL incorporada fornece uma variável global com o nome `sqlca` (área de comunicação SQL) que tem a seguinte estrutura:

```
struct
{
    char sqlcaid[8];
    long sqlabc;
    long sqlcode;
    struct
    {
        int sqlerrml;
        char sqlerrmc[SQLERRMC_LEN];
    } sqlerrm;
    char sqlerrp[8];
    long sqlerrd[6];
    char sqlwarn[8];
    char sqlstate[5];
} sqlca;
```

(Em um programa multithreading, cada thread recebe automaticamente sua própria cópia de `sqlca`. Isso funciona de maneira semelhante ao manuseio da variável global padrão C `errno`.)

`sqlca` abrange tanto os avisos quanto os erros. Se vários avisos ou erros ocorrerem durante a execução de uma declaração, então `sqlca` conterá apenas informações sobre o último.

Se não houver ocorrido nenhum erro na última declaração SQL, `sqlca.sqlcode` será 0 e `sqlca.sqlstate` será `"00000"`. Se houver um aviso ou erro, então `sqlca.sqlcode` será negativo e `sqlca.sqlstate` será diferente de `"00000"`. Um `sqlca.sqlcode` positivo indica uma condição inofensiva, como que a última consulta retornou zero linhas. `sqlcode` e `sqlstate` são dois esquemas de código de erro diferentes; os detalhes aparecem abaixo.

Se a última instrução SQL tiver sido bem-sucedida, então `sqlca.sqlerrd[1]` contém o OID da linha processada, se aplicável, e `sqlca.sqlerrd[2]` contém o número de linhas processadas ou retornadas, se aplicável ao comando.

Em caso de um erro ou aviso, `sqlca.sqlerrm.sqlerrmc` conterá uma string que descreve o erro. O campo `sqlca.sqlerrm.sqlerrml` contém o comprimento da mensagem de erro que é armazenada em `sqlca.sqlerrm.sqlerrmc` (o resultado de `strlen()`, que não é realmente interessante para um programador C). Note que algumas mensagens são muito longas para caber no array de tamanho fixo `sqlerrmc`; elas serão truncadas.

Em caso de um aviso, `sqlca.sqlwarn[2]` é definido como `W`. (Em todos os outros casos, é definido como algo diferente de `W`.). Se `sqlca.sqlwarn[1]` está definido como `W`, então um valor foi truncado quando foi armazenado em uma variável hospedeira. `sqlca.sqlwarn[0]` é definido como `W` se algum dos outros elementos estiver definido para indicar um aviso.

Os campos `sqlcaid`, `sqlabc`, `sqlerrp` e os elementos restantes de `sqlerrd` e `sqlwarn` atualmente não contêm informações úteis.

A estrutura `sqlca` não está definida no padrão SQL, mas é implementada em vários outros sistemas de banco de dados SQL. As definições são semelhantes no núcleo, mas se você deseja escrever aplicativos portáteis, então deve investigar as diferentes implementações cuidadosamente.

Aqui está um exemplo que combina o uso de `WHENEVER` e `sqlca`, imprimindo o conteúdo de `sqlca` quando ocorre um erro. Isso é talvez útil para depuração ou prototipagem de aplicativos, antes de instalar um manipulador de erro mais “friendly” para o usuário.

```
EXEC SQL WHENEVER SQLERROR CALL print_sqlca();

void
print_sqlca()
{
    fprintf(stderr, "==== sqlca ====\n");
    fprintf(stderr, "sqlcode: %ld\n", sqlca.sqlcode);
    fprintf(stderr, "sqlerrm.sqlerrml: %d\n", sqlca.sqlerrm.sqlerrml);
    fprintf(stderr, "sqlerrm.sqlerrmc: %s\n", sqlca.sqlerrm.sqlerrmc);
    fprintf(stderr, "sqlerrd: %ld %ld %ld %ld %ld %ld\n", sqlca.sqlerrd[0],sqlca.sqlerrd[1],sqlca.sqlerrd[2],
                                                          sqlca.sqlerrd[3],sqlca.sqlerrd[4],sqlca.sqlerrd[5]);
    fprintf(stderr, "sqlwarn: %d %d %d %d %d %d %d %d\n", sqlca.sqlwarn[0], sqlca.sqlwarn[1], sqlca.sqlwarn[2],
                                                          sqlca.sqlwarn[3], sqlca.sqlwarn[4], sqlca.sqlwarn[5],
                                                          sqlca.sqlwarn[6], sqlca.sqlwarn[7]);
    fprintf(stderr, "sqlstate: %5s\n", sqlca.sqlstate);
    fprintf(stderr, "===============\n");
}
```

O resultado pode parecer da seguinte forma (aqui, um erro devido a um nome de tabela mal escrito):

```
==== sqlca ====
sqlcode: -400
sqlerrm.sqlerrml: 49
sqlerrm.sqlerrmc: relation "pg_databasep" does not exist on line 38
sqlerrd: 0 0 0 0 0 0
sqlwarn: 0 0 0 0 0 0 0 0
sqlstate: 42P01
===============
```

### 34.8.3. `SQLSTATE` vs. `SQLCODE` [#](#ECPG-SQLSTATE-SQLCODE)

Os campos `sqlca.sqlstate` e `sqlca.sqlcode` são dois esquemas diferentes que fornecem códigos de erro. Ambos são derivados do padrão SQL, mas `SQLCODE` foi marcado como desatualizado na edição SQL-92 do padrão e foi descartado em edições posteriores. Portanto, novas aplicações são fortemente incentivadas a usar `SQLSTATE`.

`SQLSTATE` é uma matriz de cinco caracteres. Os cinco caracteres contêm dígitos ou letras maiúsculas que representam códigos de várias condições de erro e aviso. `SQLSTATE` tem um esquema hierárquico: os dois primeiros caracteres indicam a classe geral da condição, os três últimos caracteres indicam uma subclasse da condição geral. Um estado bem-sucedido é indicado pelo código `00000`. Os códigos `SQLSTATE` são, na maior parte, definidos no padrão SQL. O servidor PostgreSQL suporta nativamente os códigos de erro `SQLSTATE`, portanto, pode-se alcançar um alto grau de consistência usando este esquema de código de erro em todas as aplicações. Para mais informações, consulte [Apêndice A][(errcodes-appendix.md "Appendix A. PostgreSQL Error Codes")].

`SQLCODE`, o esquema de código de erro obsoleto, é um número simples. Um valor de 0 indica sucesso, um valor positivo indica sucesso com informações adicionais, um valor negativo indica um erro. O padrão SQL define apenas o valor positivo +100, que indica que o último comando retornou ou afetou zero linhas, e não há valores negativos específicos. Portanto, este esquema só pode alcançar uma baixa portabilidade e não tem uma atribuição de código hierárquico. Historicamente, o processador de SQL incorporado para o PostgreSQL atribuiu alguns valores específicos `SQLCODE` para seu uso, que estão listados abaixo com seu valor numérico e seu nome simbólico. Lembre-se de que esses valores não são portáveis para outras implementações de SQL. Para simplificar a portar de aplicativos para o esquema `SQLSTATE`, o `SQLSTATE` correspondente também está listado. No entanto, não há mapeamento um para um ou um para muitos entre os dois esquemas (de fato, é muitos para muitos), então você deve consultar a lista global `SQLSTATE` em [Apêndice A](errcodes-appendix.md "Appendix A. PostgreSQL Error Codes") em cada caso.

Estes são os valores atribuídos `SQLCODE`:

0 (`ECPG_NO_ERROR`) [#](#ECPG-SQLSTATE-SQLCODE-ECPG-NO-ERROR): Indica que não há erro. (SQLSTATE 00000)

100 (`ECPG_NOT_FOUND`) [#](#ECPG-SQLSTATE-SQLCODE-ECPG-NOT-FOUND): Esta é uma condição inofensiva que indica que o último comando recuperado ou processado não retornou ou processou zero linhas, ou que você está no final do cursor. (SQLSTATE 02000)

Ao processar um cursor em um loop, você pode usar esse código como uma maneira de detectar quando abortar o loop, assim:

``` while (1) { EXEC SQL FETCH ... ; if (sqlca.sqlcode == ECPG_NOT_FOUND) break; }
    ```

Mas o `WHENEVER NOT FOUND DO BREAK` faz isso efetivamente internamente, então geralmente não há vantagem em escrever isso explicitamente.

-12 (`ECPG_OUT_OF_MEMORY`) [#](#ECPG-SQLSTATE-SQLCODE-ECPG-OUT-OF-MEMORY): Indica que sua memória virtual está esgotada. O valor numérico é definido como `-ENOMEM`. (SQLSTATE YE001)

-200 (`ECPG_UNSUPPORTED`) [#](#ECPG-SQLSTATE-SQLCODE-ECPG-UNSUPPORTED): Indica que o pré-processador gerou algo que a biblioteca não conhece. Talvez você esteja executando versões incompatíveis do pré-processador e da biblioteca. (SQLSTATE YE002)

-201 (`ECPG_TOO_MANY_ARGUMENTS`) [#](#ECPG-SQLSTATE-SQLCODE-ECPG-TOO-MANY-ARGUMENTS): Isso significa que o comando especificou mais variáveis de host do que o esperado. (SQLSTATE 07001 ou 07002)

-202 (`ECPG_TOO_FEW_ARGUMENTS`) [#](#ECPG-SQLSTATE-SQLCODE-ECPG-TOO-FEW-ARGUMENTS): Isso significa que o comando especificou menos variáveis de host do que o esperado. (SQLSTATE 07001 ou 07002)

-203 (`ECPG_TOO_MANY_MATCHES`) [#](#ECPG-SQLSTATE-SQLCODE-ECPG-TOO-MANY-MATCHES): Isso significa que uma consulta retornou várias linhas, mas a declaração foi preparada apenas para armazenar uma linha de resultado (por exemplo, porque as variáveis especificadas não são matrizes). (SQLSTATE 21000)

-204 (`ECPG_INT_FORMAT`) [#](#ECPG-SQLSTATE-SQLCODE-ECPG-INT-FORMAT): A variável host é do tipo `int` e o dado no banco de dados é de um tipo diferente e contém um valor que não pode ser interpretado como um `int`. A biblioteca usa `strtol()` para essa conversão. (SQLSTATE 42804)

-205 (`ECPG_UINT_FORMAT`) [#](#ECPG-SQLSTATE-SQLCODE-ECPG-UINT-FORMAT): A variável host é do tipo `unsigned int` e o dado no banco de dados é de um tipo diferente e contém um valor que não pode ser interpretado como um `unsigned int`. A biblioteca usa `strtoul()` para essa conversão. (SQLSTATE 42804)

-206 (`ECPG_FLOAT_FORMAT`) [#](#ECPG-SQLSTATE-SQLCODE-ECPG-FLOAT-FORMAT): A variável host é do tipo `float` e o dado no banco de dados é de outro tipo e contém um valor que não pode ser interpretado como um `float`. A biblioteca usa `strtod()` para essa conversão. (SQLSTATE 42804)

-207 (`ECPG_NUMERIC_FORMAT`) [#](#ECPG-SQLSTATE-SQLCODE-ECPG-NUMERIC-FORMAT): A variável host é do tipo `numeric` e o dado no banco de dados é de outro tipo e contém um valor que não pode ser interpretado como um valor `numeric`. (SQLSTATE 42804)

-208 (`ECPG_INTERVAL_FORMAT`) [#](#ECPG-SQLSTATE-SQLCODE-ECPG-INTERVAL-FORMAT): A variável host é do tipo `interval` e o dado no banco de dados é de outro tipo e contém um valor que não pode ser interpretado como um valor de `interval`. (SQLSTATE 42804)

-209 (`ECPG_DATE_FORMAT`) [#](#ECPG-SQLSTATE-SQLCODE-ECPG-DATE-FORMAT): A variável host é do tipo `date` e o dado no banco de dados é de outro tipo e contém um valor que não pode ser interpretado como um valor `date`. (SQLSTATE 42804)

-210 (`ECPG_TIMESTAMP_FORMAT`) [#](#ECPG-SQLSTATE-SQLCODE-ECPG-TIMESTAMP-FORMAT): A variável host é do tipo `timestamp` e o dado no banco de dados é de outro tipo e contém um valor que não pode ser interpretado como um valor `timestamp`. (SQLSTATE 42804)

-211 (`ECPG_CONVERT_BOOL`) [#](#ECPG-SQLSTATE-SQLCODE-ECPG-CONVERT-BOOL): Isso significa que a variável host é do tipo `bool` e o dado no banco de dados não é nem `'t'` nem `'f'`. (SQLSTATE 42804)

-212 (`ECPG_EMPTY`) [#](#ECPG-SQLSTATE-SQLCODE-ECPG-EMPTY): A declaração enviada ao servidor PostgreSQL estava vazia. (Isso normalmente não pode acontecer em um programa de SQL integrado, então pode indicar um erro interno.) (SQLSTATE YE002)

-213 (`ECPG_MISSING_INDICATOR`) [#](#ECPG-SQLSTATE-SQLCODE-ECPG-MISSING-INDICATOR): Foi retornado um valor nulo e não foi fornecida uma variável de indicador nulo. (SQLSTATE 22002)

-214 (`ECPG_NO_ARRAY`) [#](#ECPG-SQLSTATE-SQLCODE-ECPG-NO-ARRAY): Uma variável comum foi usada em um lugar que exige um array. (SQLSTATE 42804)

-215 (`ECPG_DATA_NOT_ARRAY`) [#](#ECPG-SQLSTATE-SQLCODE-ECPG-DATA-NOT-ARRAY): O banco de dados retornou uma variável comum em um lugar que exige o valor de um array. (SQLSTATE 42804)

-216 (`ECPG_ARRAY_INSERT`) [#](#ECPG-SQLSTATE-SQLCODE-ECPG-ARRAY-INSERT): O valor não pôde ser inserido no array. (SQLSTATE 42804)

-220 (`ECPG_NO_CONN`) [#](#ECPG-SQLSTATE-SQLCODE-ECPG-NO-CONN): O programa tentou acessar uma conexão que não existe. (SQLSTATE 08003)

-221 (`ECPG_NOT_CONN`) [#](#ECPG-SQLSTATE-SQLCODE-ECPG-NOT-CONN): O programa tentou acessar uma conexão que existe, mas não está aberta. (Este é um erro interno.) (SQLSTATE YE002)

-230 (`ECPG_INVALID_STMT`) [#](#ECPG-SQLSTATE-SQLCODE-ECPG-INVALID-STMT): A declaração que você está tentando usar não foi preparada. (SQLSTATE 26000)

-239 (`ECPG_INFORMIX_DUPLICATE_KEY`) [#](#ECPG-SQLSTATE-SQLCODE-ECPG-INFORMIX-DUPLICATE-KEY): Erro de chave duplicada, violação da restrição única (modo de compatibilidade Informix). (SQLSTATE 23505)

-240 (`ECPG_UNKNOWN_DESCRIPTOR`) [#](#ECPG-SQLSTATE-SQLCODE-ECPG-UNKNOWN-DESCRIPTOR): O descritor especificado não foi encontrado. A declaração que você está tentando usar não foi preparada. (SQLSTATE 33000)

-241 (`ECPG_INVALID_DESCRIPTOR_INDEX`) [#](#ECPG-SQLSTATE-SQLCODE-ECPG-INVALID-DESCRIPTOR-INDEX): O índice de descriptografia especificado estava fora do intervalo. (SQLSTATE 07009)

-242 (`ECPG_UNKNOWN_DESCRIPTOR_ITEM`) [#](#ECPG-SQLSTATE-SQLCODE-ECPG-UNKNOWN-DESCRIPTOR-ITEM): Um item de descritor inválido foi solicitado. (Este é um erro interno.) (SQLSTATE YE002)

-243 (`ECPG_VAR_NOT_NUMERIC`) [#](#ECPG-SQLSTATE-SQLCODE-ECPG-VAR-NOT-NUMERIC): Durante a execução de uma declaração dinâmica, o banco de dados retornou um valor numérico e a variável hospedeira não era numérica. (SQLSTATE 07006)

-244 (`ECPG_VAR_NOT_CHAR`) [#](#ECPG-SQLSTATE-SQLCODE-ECPG-VAR-NOT-CHAR): Durante a execução de uma declaração dinâmica, o banco de dados retornou um valor não numérico e a variável do host era numérica. (SQLSTATE 07006)

-284 (`ECPG_INFORMIX_SUBSELECT_NOT_ONE`) [#](#ECPG-SQLSTATE-SQLCODE-ECPG-INFORMIX-SUBSELECT-NOT-ONE): O resultado da subconsulta não é uma única linha (modo de compatibilidade Informix). (SQLSTATE 21000)

-400 (`ECPG_PGSQL`) [#](#ECPG-SQLSTATE-SQLCODE-ECPG-PGSQL): Algum erro causado pelo servidor PostgreSQL. A mensagem contém a mensagem de erro do servidor PostgreSQL.

-401 (`ECPG_TRANS`) [#](#ECPG-SQLSTATE-SQLCODE-ECPG-TRANS): O servidor PostgreSQL sinalizou que não podemos iniciar, confirmar ou reverter a transação. (SQLSTATE 08007)

-402 (`ECPG_CONNECT`) [#](#ECPG-SQLSTATE-SQLCODE-ECPG-CONNECT): A tentativa de conexão com o banco de dados não foi bem-sucedida. (SQLSTATE 08001)

-403 (`ECPG_DUPLICATE_KEY`) [#](#ECPG-SQLSTATE-SQLCODE-ECPG-DUPLICATE-KEY): Erro de chave duplicada, violação da restrição única. (SQLSTATE 23505)

-404 (`ECPG_SUBSELECT_NOT_ONE`) [#](#ECPG-SQLSTATE-SQLCODE-ECPG-SUBSELECT-NOT-ONE): O resultado da subconsulta não é uma única linha. (SQLSTATE 21000)

-602 (`ECPG_WARNING_UNKNOWN_PORTAL`) [#](#ECPG-SQLSTATE-SQLCODE-ECPG-WARNING-UNKNOWN-PORTAL): Um nome de cursor inválido foi especificado. (SQLSTATE 34000)

-603 (`ECPG_WARNING_IN_TRANSACTION`) [#](#ECPG-SQLSTATE-SQLCODE-ECPG-WARNING-IN-TRANSACTION): Transação em andamento. (SQLSTATE 25001)

-604 (`ECPG_WARNING_NO_TRANSACTION`) [#](#ECPG-SQLSTATE-SQLCODE-ECPG-WARNING-NO-TRANSACTION): Não há transação ativa (em andamento). (SQLSTATE 25P01)

-605 (`ECPG_WARNING_PORTAL_EXISTS`) [#](#ECPG-SQLSTATE-SQLCODE-ECPG-WARNING-PORTAL-EXISTS): Foi especificado um nome de cursor existente. (SQLSTATE 42P03)