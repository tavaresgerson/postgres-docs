## 36.13. Tipos Definidos pelo Usuário [#](#XTYPES)

* [36.13.1. CONSIDERACAO DE TOAST][(xtypes.md#XTYPES-TOAST)

Como descrito na [Seção 36.2][(extend-type-system.md "36.2. The PostgreSQL Type System")], o PostgreSQL pode ser estendido para suportar novos tipos de dados. Esta seção descreve como definir novos tipos básicos, que são tipos de dados definidos abaixo do nível da linguagem SQL. Criar um novo tipo básico requer a implementação de funções para operar no tipo em um idioma de baixo nível, geralmente C.

Os exemplos desta seção podem ser encontrados em `complex.sql` e `complex.c` no diretório `src/tutorial` da distribuição de origem. Consulte o arquivo `README` nesse diretório para obter instruções sobre como executar os exemplos.

Um tipo definido pelo usuário deve sempre ter funções de entrada e saída. Essas funções determinam como o tipo aparece em strings (para entrada pelo usuário e saída para o usuário) e como o tipo é organizado na memória. A função de entrada recebe uma string de caracteres terminada por nulo como seu argumento e retorna a representação interna (na memória) do tipo. A função de saída recebe a representação interna do tipo como argumento e retorna uma string de caracteres terminada por nulo. Se quisermos fazer algo mais com o tipo do que apenas armazená-lo, devemos fornecer funções adicionais para implementar quaisquer operações que queiramos ter para o tipo.

Suponha que queira definir um tipo `complex` que represente números complexos. Uma maneira natural de representar um número complexo na memória seria a seguinte estrutura em C:

```
typedef struct Complex {
    double      x;
    double      y;
} Complex;
```

Precisaremos fazer isso um tipo de passagem por referência, pois é muito grande para caber em um único valor `Datum`.

Como representação externa da cadeia de caracteres do tipo, escolhemos uma cadeia de caracteres na forma `(x,y)`.

As funções de entrada e saída geralmente não são difíceis de escrever, especialmente a função de saída. Mas ao definir a representação de string externa do tipo, lembre-se de que você deve, eventualmente, escrever um analisador completo e robusto para essa representação como sua função de entrada. Por exemplo:

```
PG_FUNCTION_INFO_V1(complex_in);

Datum
complex_in(PG_FUNCTION_ARGS)
{
    char       *str = PG_GETARG_CSTRING(0);
    double      x,
                y;
    Complex    *result;

    if (sscanf(str, " ( %lf , %lf )", &x, &y) != 2)
        ereport(ERROR,
                (errcode(ERRCODE_INVALID_TEXT_REPRESENTATION),
                 errmsg("invalid input syntax for type %s: \"%s\"",
                        "complex", str)));

    result = (Complex *) palloc(sizeof(Complex));
    result->x = x;
    result->y = y;
    PG_RETURN_POINTER(result);
}
```

A função de saída pode ser simplesmente:

```
PG_FUNCTION_INFO_V1(complex_out);

Datum
complex_out(PG_FUNCTION_ARGS)
{
    Complex    *complex = (Complex *) PG_GETARG_POINTER(0);
    char       *result;

    result = psprintf("(%g,%g)", complex->x, complex->y);
    PG_RETURN_CSTRING(result);
}
```

Você deve ter cuidado para fazer as funções de entrada e saída serem inversas uma da outra. Se não fizer isso, você terá problemas graves quando precisar descartar seus dados em um arquivo e depois lê-los novamente. Esse é um problema particularmente comum quando números em ponto flutuante estão envolvidos.

Opcionalmente, um tipo definido pelo usuário pode fornecer rotinas de entrada e saída binárias. A entrada e saída binária é normalmente mais rápida, mas menos portátil do que a entrada e saída textual. Assim como na entrada e saída textual, cabe a você definir exatamente qual é a representação binária externa. A maioria dos tipos de dados embutidos tenta fornecer uma representação binária independente da máquina. Para `complex`, faremos uso dos conversores de entrada e saída binária para o tipo `float8`:

```
PG_FUNCTION_INFO_V1(complex_recv);

Datum
complex_recv(PG_FUNCTION_ARGS)
{
    StringInfo  buf = (StringInfo) PG_GETARG_POINTER(0);
    Complex    *result;

    result = (Complex *) palloc(sizeof(Complex));
    result->x = pq_getmsgfloat8(buf);
    result->y = pq_getmsgfloat8(buf);
    PG_RETURN_POINTER(result);
}

PG_FUNCTION_INFO_V1(complex_send);

Datum
complex_send(PG_FUNCTION_ARGS)
{
    Complex    *complex = (Complex *) PG_GETARG_POINTER(0);
    StringInfoData buf;

    pq_begintypsend(&buf);
    pq_sendfloat8(&buf, complex->x);
    pq_sendfloat8(&buf, complex->y);
    PG_RETURN_BYTEA_P(pq_endtypsend(&buf));
}
```

Depois de escrevermos as funções de entrada/saída e compilarmos-nas em uma biblioteca compartilhada, podemos definir o tipo `complex` no SQL. Primeiro, declaramos-o como um tipo de shell:

```
CREATE TYPE complex;
```

Isso serve como um marcador que nos permite fazer referência ao tipo ao definir suas funções de E/S. Agora podemos definir as funções de E/S:

```
CREATE FUNCTION complex_in(cstring)
    RETURNS complex
    AS 'filename'
    LANGUAGE C IMMUTABLE STRICT;

CREATE FUNCTION complex_out(complex)
    RETURNS cstring
    AS 'filename'
    LANGUAGE C IMMUTABLE STRICT;

CREATE FUNCTION complex_recv(internal)
   RETURNS complex
   AS 'filename'
   LANGUAGE C IMMUTABLE STRICT;

CREATE FUNCTION complex_send(complex)
   RETURNS bytea
   AS 'filename'
   LANGUAGE C IMMUTABLE STRICT;
```

Por fim, podemos fornecer a definição completa do tipo de dados:

```
CREATE TYPE complex (
   internallength = 16,
   input = complex_in,
   output = complex_out,
   receive = complex_recv,
   send = complex_send,
   alignment = double
);
```

Quando você define um novo tipo de base, o PostgreSQL fornece automaticamente suporte para arrays desse tipo. O tipo de array geralmente tem o mesmo nome que o tipo de base, com o caractere sublinhado (`_`) prependido.

Uma vez que o tipo de dados exista, podemos declarar funções adicionais para fornecer operações úteis sobre o tipo de dados. Os operadores podem então ser definidos em cima das funções, e, se necessário, classes de operador podem ser criadas para suportar a indexação do tipo de dados. Essas camadas adicionais são discutidas nas seções seguintes.

Se a representação interna do tipo de dados for de comprimento variável, a representação interna deve seguir o layout padrão para dados de comprimento variável: os primeiros quatro bytes devem ser um campo `char[4]`, que nunca é acessado diretamente (comumente denominado `vl_len_`). Você deve usar a macro `SET_VARSIZE()` para armazenar o tamanho total do dado (incluindo o próprio campo de comprimento) neste campo e `VARSIZE()` para recuperá-lo. (Essas macros existem porque o campo de comprimento pode ser codificado dependendo da plataforma.)

Para mais detalhes, consulte a descrição do comando [CREATE TYPE](sql-createtype.md "CREATE TYPE").

### 36.13.1. Considerações sobre TOAST [#](#XTYPES-TOAST)

Se os valores do seu tipo de dados variam em tamanho (na forma interna), geralmente é desejável tornar o tipo de dados TOAST-ável (consulte [Seção 66.2] [(storage-toast.md "66.2. TOAST")]). Você deve fazer isso mesmo que os valores sempre sejam muito pequenos para serem comprimidos ou armazenados externamente, porque o TOAST pode economizar espaço em dados pequenos também, reduzindo o overhead do cabeçalho.

Para suportar o armazenamento TOAST, as funções C que operam sobre o tipo de dados devem sempre ter cuidado ao desempacotar quaisquer valores tostados que lhes sejam entregues usando `PG_DETOAST_DATUM`. (Esse detalhe é normalmente oculto ao definir macros específicas para o tipo `GETARG_DATATYPE_P`. Em seguida, ao executar o comando `CREATE TYPE`, especifique o comprimento interno como `variable` e selecione uma opção de armazenamento apropriada, diferente de `plain`.

Se o alinhamento de dados não for importante (seja apenas para uma função específica ou porque o tipo de dados especifica alinhamento de byte de qualquer maneira), é possível evitar alguns dos custos adicionais do `PG_DETOAST_DATUM`. É possível usar o `PG_DETOAST_DATUM_PACKED` (comumente oculto definindo um `GETARG_DATATYPE_PP` macro) e usar as macros `VARSIZE_ANY_EXHDR` e `VARDATA_ANY` para acessar um dado potencialmente embalado. Novamente, os dados retornados por essas macros não são alinhados, mesmo que a definição do tipo de dados especifique um alinhamento. Se o alinhamento for importante, você deve seguir a interface regular do `PG_DETOAST_DATUM`.

### Nota

O código mais antigo frequentemente declara `vl_len_` como um campo `int32` em vez de `char[4]`. Isso está bem, desde que a definição da estrutura tenha outros campos que tenham pelo menos alinhamento `int32`. Mas é perigoso usar uma definição de estrutura desse tipo ao trabalhar com um dado potencialmente desalinhado; o compilador pode assumir que o dado está realmente alinhado, levando a depurações de núcleo em arquiteturas que são rigorosas em relação ao alinhamento.

Outra característica que é habilitada pelo suporte do TOAST é a possibilidade de ter uma representação de dados em memória *expandia* que é mais conveniente de trabalhar do que o formato que é armazenado em disco. O formato de armazenamento regular ou "plano" de varlena é, em última análise, apenas um blob de bytes; ele não pode, por exemplo, conter ponteiros, pois pode ser copiado para outras localizações na memória. Para tipos de dados complexos, o formato plano pode ser bastante caro de trabalhar, então o PostgreSQL fornece uma maneira de "expandir" o formato plano em uma representação que é mais adequada para computação, e depois passar esse formato em memória entre funções do tipo de dados.

Para usar o armazenamento expandido, um tipo de dados deve definir um formato expandido que siga as regras dadas em `src/include/utils/expandeddatum.h`, e fornecer funções para "expandir" um valor de varlena plano para o formato expandido e "aplanar" o formato expandido de volta à representação regular de varlena. Em seguida, garanta que todas as funções C para o tipo de dados possam aceitar qualquer uma das representações, possivelmente convertendo uma para a outra imediatamente após a recepção. Isso não requer a correção de todas as funções existentes para o tipo de dados de uma só vez, porque a macro padrão `PG_DETOAST_DATUM` é definida para converter entradas expandidas para o formato plano regular. Portanto, as funções existentes que trabalham com o formato de varlena plano continuarão a funcionar, embora de forma ligeiramente ineficiente, com entradas expandidas; elas não precisam ser convertidas a menos que o desempenho melhor seja importante.

As funções C que sabem trabalhar com uma representação expandida geralmente se enquadram em duas categorias: aquelas que só podem lidar com formatos expandidos e aquelas que podem lidar com entradas de varlena planas ou expandidas. As primeiras são mais fáceis de escrever, mas podem ser menos eficientes no geral, porque converter uma entrada plana para uma forma expandida para uso por uma única função pode custar mais do que o que é economizado ao operar no formato expandido. Quando apenas o formato expandido precisa ser tratado, a conversão de entradas planas para uma forma expandida pode ser oculta dentro de uma macro de obtenção de argumentos, de modo que a função não pareça mais complexa do que uma que trabalha com entrada de varlena tradicional. Para lidar com ambos os tipos de entrada, escreva uma função de obtenção de argumentos que irá decodificar entradas de varlena externas, de cabeçalho curto e comprimidas, mas não expandidas. Tal função pode ser definida como retornando um ponteiro para uma união do formato de varlena plano e do formato expandido. Os solicitantes podem usar a macro `VARATT_IS_EXPANDED_HEADER()` para determinar qual formato eles receberam.

A infraestrutura TOAST não só permite distinguir valores varlena regulares de valores expandidos, mas também distingue ponteiros de "leitura-escrita" e "somente leitura" para valores expandidos. As funções C que precisam apenas examinar um valor expandido, ou que apenas o alterarão de maneiras seguras e não semânticamente visíveis, não precisam se preocupar com o tipo de ponteiro que recebem. As funções C que produzem uma versão modificada de um valor de entrada podem modificar um valor de entrada expandido in-place se recebem um ponteiro de leitura-escrita, mas não devem modificar a entrada se recebem um ponteiro de apenas leitura; nesse caso, elas devem copiar o valor primeiro, produzindo um novo valor para modificar. Uma função C que construiu um novo valor expandido deve sempre retornar um ponteiro de leitura-escrita para ele. Além disso, uma função C que está modificando um valor expandido de leitura-escrita in-place deve cuidar para deixar o valor em um estado sadio se falhar em meio caminho.

Para exemplos de trabalho com valores expandidos, consulte a infraestrutura de matriz padrão, particularmente `src/backend/utils/adt/array_expanded.c`.