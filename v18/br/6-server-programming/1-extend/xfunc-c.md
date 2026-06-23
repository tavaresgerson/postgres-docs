## 36.10. Funções em linguagem C [#](#XFUNC-C)

* [36.10.1. Carregamento Dinâmico][(xfunc-c.md#XFUNC-C-DYNLOAD)
* [36.10.2. Tipos Básicos em Funções em Linguagem C][(xfunc-c.md#XFUNC-C-BASETYPE)
* [36.10.3. Convenções de Chamada da Versão 1][(xfunc-c.md#XFUNC-C-V1-CALL-CONV)
* [36.10.4. Escrevendo Código][(xfunc-c.md#XFUNC-C-CODE)
* [36.10.5. Compilando e Ligando Funções Carregadas Dinamicamente][(xfunc-c.md#DFUNC)
* [36.10.6. Orientações sobre a Estabilidade da API e ABI do Servidor][(xfunc-c.md#XFUNC-API-ABI-STABILITY-GUIDANCE)
* [36.10.7. Argumentos de Tipo Composto][(xfunc-c.md#XFUNC-C-COMPOSITE-TYPE-ARGS)
* [36.10.8. Retornando Linhas (Tipos Compostos)][(xfunc-c.md#XFUNC-C-RETURNING-ROWS)
* [36.10.9. Retornando Conjuntos][(xfunc-c.md#XFUNC-C-RETURN-SET)
* [36.10.10. Argumentos Polimórficos e Tipos de Retorno][(xfunc-c.md#XFUNC-C-POLYMORPHIC)
* [36.10.11. Memória Compartilhada][(xfunc-c.md#XFUNC-SHARED-ADDIN)
* [36.10.12. LWLocks][(xfunc-c.md#XFUNC-ADDIN-LWLOCKS)
* [36.10.13. Eventos de Aguarda Personalizados][(xfunc-c.md#XFUNC-ADDIN-WAIT-EVENTS)
* [36.10.14. Pontos de Injeção][(xfunc-c.md#XFUNC-ADDIN-INJECTION-POINTS)
* [36.10.15. Estatísticas Cumulativas Personalizadas][(xfunc-c.md#XFUNC-ADDIN-CUSTOM-CUMULATIVE-STATISTICS)
* [36.10.16. Usando C++ para Extensibilidade][(xfunc-c.md#EXTEND-CPP)

As funções definidas pelo usuário podem ser escritas em C (ou em uma linguagem que possa ser feita compatível com C, como C++) Essas funções são compiladas em objetos dinamicamente carregáveis (também chamados de bibliotecas compartilhadas) e são carregadas pelo servidor conforme necessário. O recurso de carregamento dinâmico é o que distingue as funções de "linguagem C" das funções "internas" — as convenções de codificação são essencialmente as mesmas para ambas. (Portanto, a biblioteca padrão de funções internas é uma rica fonte de exemplos de codificação para funções C definidas pelo usuário.)

Atualmente, apenas uma convenção de chamada é usada para funções C (“versão 1”). O suporte para essa convenção de chamada é indicado ao escrever uma chamada de macro `PG_FUNCTION_INFO_V1()` para a função, conforme ilustrado abaixo.

### 36.10.1. Carregamento Dinâmico [#](#XFUNC-C-DYNLOAD)

A primeira vez que uma função definida pelo usuário em um arquivo de objeto carregável específico é chamada em uma sessão, o carregador dinâmico carrega esse arquivo de objeto na memória para que a função possa ser chamada. O `CREATE FUNCTION` para uma função C definida pelo usuário deve, portanto, especificar duas informações para a função: o nome do arquivo de objeto carregável e o nome C (símbolo de ligação) da função específica a ser chamada nesse arquivo de objeto. Se o nome C não for especificado explicitamente, presume-se que seja o mesmo que o nome da função SQL.

O seguinte algoritmo é usado para localizar o arquivo de objeto compartilhado com base no nome fornecido no comando `CREATE FUNCTION`:

1. Se o nome for um caminho absoluto, o arquivo fornecido é carregado.
2. Se o nome começar com a string `$libdir`, essa parte é substituída pelo nome do diretório da biblioteca do PostgreSQL, que é determinado no momento da construção.
3. Se o nome não contiver uma parte de diretório, o arquivo é procurado no caminho especificado pela variável de configuração [dynamic_library_path](runtime-config-client.md#GUC-DYNAMIC-LIBRARY-PATH).
4. Caso contrário (o arquivo não foi encontrado no caminho ou contém uma parte de diretório não absoluta), o carregador dinâmico tentará usar o nome fornecido, o que provavelmente falhará. (Não é confiável depender do diretório de trabalho atual.)

Se essa sequência não funcionar, o nome da extensão do arquivo da biblioteca compartilhada específico da plataforma (frequentemente `.so`) é anexado ao nome fornecido e essa sequência é testado novamente. Se isso também falhar, a carga falhará.

Recomenda-se localizar bibliotecas compartilhadas ou em relação a `$libdir` ou através do caminho de bibliotecas dinâmicas. Isso simplifica as atualizações de versão se a nova instalação estiver em um local diferente. O diretório real para o qual `$libdir` se refere pode ser encontrado com o comando `pg_config --pkglibdir`.

O ID do usuário pelo qual o servidor PostgreSQL é executado deve ser capaz de percorrer o caminho até o arquivo que você pretende carregar. Tornar o arquivo ou um diretório de nível superior não legível e/ou não executável pelo usuário postgres é um erro comum.

De qualquer forma, o nome do arquivo que é dado no comando `CREATE FUNCTION` é registrado literalmente nos catálogos do sistema, então, se o arquivo precisar ser carregado novamente, o mesmo procedimento é aplicado.

### Nota

O PostgreSQL não compilará uma função C automaticamente. O arquivo objeto deve ser compilado antes de ser referenciado em um comando `CREATE FUNCTION`. Consulte [Seção 36.10.5](xfunc-c.md#DFUNC) para obter informações adicionais.

Para garantir que um arquivo de objeto carregado dinamicamente não seja carregado em um servidor incompatível, o PostgreSQL verifica se o arquivo contém um "bloco mágico" com o conteúdo apropriado. Isso permite que o servidor detecte incompatibilidades óbvias, como código compilado para uma versão principal diferente do PostgreSQL. Para incluir um bloco mágico, escreva isso em um (e apenas um) dos arquivos de fonte do módulo, após ter incluído o cabeçalho `fmgr.h`:

```
PG_MODULE_MAGIC;
```

ou

```
PG_MODULE_MAGIC_EXT(parameters);
```

A variante `PG_MODULE_MAGIC_EXT` permite a especificação de informações adicionais sobre o módulo; atualmente, um nome e/ou uma string de versão podem ser adicionados. (Mais campos podem ser permitidos no futuro.) Escreva algo assim:

```
PG_MODULE_MAGIC_EXT(
    .name = "my_module_name",
    .version = "1.2.3"
);
```

Posteriormente, o nome e a versão podem ser examinados através da função `pg_get_loaded_modules()`. O significado da string de versão não é restrito pelo PostgreSQL, mas o uso de regras de versão semântica é recomendado.

Após ser usado pela primeira vez, um arquivo de objeto carregado dinamicamente é mantido na memória. Futuras chamadas na mesma sessão para a(s) função(ões) nesse arquivo só implicará no pequeno custo de uma pesquisa na tabela de símbolos. Se você precisar forçar um recarregamento de um arquivo de objeto, por exemplo, após recompilar, comece uma sessão nova.

Opcionalmente, um arquivo carregado dinamicamente pode conter uma função de inicialização. Se o arquivo incluir uma função chamada `_PG_init`, essa função será chamada imediatamente após o carregamento do arquivo. A função não recebe parâmetros e deve retornar void. Atualmente, não há como descarregar um arquivo carregado dinamicamente.

### 36.10.2. Tipos básicos em funções da linguagem C [#](#XFUNC-C-BASETYPE)

Para saber como escrever funções em linguagem C, você precisa saber como o PostgreSQL representa internamente os tipos de dados básicos e como eles podem ser passados para e a partir das funções. Internamente, o PostgreSQL considera um tipo básico como um "bloco de memória". As funções definidas pelo usuário que você define sobre um tipo, por sua vez, definem a maneira pela qual o PostgreSQL pode operá-lo. Isso significa que o PostgreSQL só armazenará e recuperará os dados do disco e usará suas funções definidas pelo usuário para inserir, processar e fornecer os dados.

Os tipos de base podem ter um dos três formatos internos:

* passagem por valor, de comprimento fixo
* passagem por referência, de comprimento fixo
* passagem por referência, de comprimento variável

Os tipos por valor só podem ter 1, 2 ou 4 bytes de comprimento (também 8 bytes, se `sizeof(Datum)` estiver em 8 na sua máquina). Você deve ter cuidado para definir seus tipos de forma que eles tenham o mesmo tamanho (em bytes) em todas as arquiteturas. Por exemplo, o tipo `long` é perigoso porque é de 4 bytes em algumas máquinas e de 8 bytes em outras, enquanto o tipo `int` é de 4 bytes na maioria das máquinas Unix. Uma implementação razoável do tipo `int4` em máquinas Unix pode ser:

```
/* 4-byte integer, passed by value */
typedef int int4;
```

(O código C real de PostgreSQL chama esse tipo `int32`, porque é uma convenção em C que `intXX` significa *`XX`* *bits*. Portanto, também note que o tipo C `int8` tem tamanho de 1 byte. O tipo SQL `int8` é chamado `int64` em C. Veja também [Tabela 36.2](xfunc-c.md#XFUNC-C-TYPE-TABLE "Table 36.2. Equivalent C Types for Built-in SQL Types").)

Por outro lado, tipos de comprimento fixo de qualquer tamanho podem ser passados por referência. Por exemplo, aqui está uma implementação de amostra de um tipo PostgreSQL:

```
/* 16-byte structure, passed by reference */
typedef struct
{
    double  x, y;
} Point;
```

Apenas ponteiros para esses tipos podem ser usados ao passá-los para dentro e para fora de funções do PostgreSQL. Para retornar um valor desse tipo, aloque a quantidade certa de memória com `palloc`, preencha a memória alocada e retorne um ponteiro para ela. (Além disso, se você apenas deseja retornar o mesmo valor como um dos seus argumentos de entrada que é do mesmo tipo de dados, você pode pular o `palloc` extra e apenas retornar o ponteiro para o valor de entrada.)

Por fim, todos os tipos de comprimento variável também devem ser passados por referência. Todos os tipos de comprimento variável devem começar com um campo de comprimento opaco de exatamente 4 bytes, que será definido por `SET_VARSIZE`; nunca definir esse campo diretamente! Todos os dados que devem ser armazenados dentro desse tipo devem ser localizados na memória imediatamente após esse campo de comprimento. O campo de comprimento contém o comprimento total da estrutura, ou seja, inclui o tamanho do próprio campo de comprimento.

Outro ponto importante é evitar deixar quaisquer bits não inicializados dentro dos valores dos tipos de dados; por exemplo, tenha cuidado para zerar quaisquer bytes de alinhamento que possam estar presentes nas estruturas. Sem isso, as constantes logicamente equivalentes do seu tipo de dados podem ser vistas como desiguais pelo planejador, levando a planos ineficientes (embora não incorretos).

### Aviso

*Nunca* modifique o conteúdo de um valor de entrada por referência. Se você fizer isso, provavelmente corromperá os dados no disco, uma vez que o ponteiro que você recebe pode apontar diretamente para um buffer de disco. A única exceção a essa regra é explicada em [Seção 36.12](xaggr.md).

Como exemplo, podemos definir o tipo `text` da seguinte forma:

```
typedef struct {
    int32 length;
    char data[FLEXIBLE_ARRAY_MEMBER];
} text;
```

A notação `[FLEXIBLE_ARRAY_MEMBER]` significa que o comprimento real da parte de dados não é especificado por esta declaração.

Ao manipular tipos de comprimento variável, devemos ter cuidado para alocar a quantidade correta de memória e definir o campo de comprimento corretamente. Por exemplo, se quiséssemos armazenar 40 bytes em uma estrutura `text`, poderíamos usar um trecho de código como este:

```
#include "postgres.h"
...
char buffer[40]; /* our source data */
...
text *destination = (text *) palloc(VARHDRSZ + 40);
SET_VARSIZE(destination, VARHDRSZ + 40);
memcpy(destination->data, buffer, 40);
...
```

`VARHDRSZ` é o mesmo que `sizeof(int32)`, mas é considerado bom estilo usar a macro `VARHDRSZ` para se referir ao tamanho do overhead para um tipo de comprimento variável. Além disso, o campo de comprimento *deve* ser definido usando a macro `SET_VARSIZE`, não por simples atribuição.

[Tabela 36.2](xfunc-c.md#XFUNC-C-TYPE-TABLE) mostra os tipos C correspondentes a muitos dos tipos de dados SQL integrados do PostgreSQL. A coluna “Definido em” fornece o arquivo de cabeçalho que precisa ser incluído para obter a definição do tipo. (A definição real pode estar em um arquivo diferente que é incluído pelo arquivo listado. É recomendável que os usuários sigam a interface definida.) Note que você deve sempre incluir `postgres.h` primeiro em qualquer arquivo de fonte de código do servidor, porque ele declara várias coisas que você precisará de qualquer maneira, e porque incluir outros cabeçalhos primeiro pode causar problemas de portabilidade.

**Tabela 36.2. Tipos C equivalentes para tipos SQL integrados**



<table border="1" class="table" summary="Equivalent C Types for Built-in SQL Types">
 <colgroup>
  <col class="col1"/>
  <col class="col2"/>
  <col class="col3"/>
 </colgroup>
 <thead>
  <tr>
   <th>
    SQL Type
   </th>
   <th>
    C Type
   </th>
   <th>
    Defined In
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <code class="type">
     boolean
    </code>
   </td>
   <td>
    <code class="type">
     bool
    </code>
   </td>
   <td>
    <code class="filename">
     postgres.h
    </code>
    (maybe compiler built-in)
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     box
    </code>
   </td>
   <td>
    <code class="type">
     BOX*
    </code>
   </td>
   <td>
    <code class="filename">
     utils/geo_decls.h
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     bytea
    </code>
   </td>
   <td>
    <code class="type">
     bytea*
    </code>
   </td>
   <td>
    <code class="filename">
     postgres.h
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     "char"
    </code>
   </td>
   <td>
    <code class="type">
     char
    </code>
   </td>
   <td>
    (compiler built-in)
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     character
    </code>
   </td>
   <td>
    <code class="type">
     BpChar*
    </code>
   </td>
   <td>
    <code class="filename">
     postgres.h
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     cid
    </code>
   </td>
   <td>
    <code class="type">
     CommandId
    </code>
   </td>
   <td>
    <code class="filename">
     postgres.h
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     date
    </code>
   </td>
   <td>
    <code class="type">
     DateADT
    </code>
   </td>
   <td>
    <code class="filename">
     utils/date.h
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     float4
    </code>
    (
    <code class="type">
     real
    </code>
    )
   </td>
   <td>
    <code class="type">
     float4
    </code>
   </td>
   <td>
    <code class="filename">
     postgres.h
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     float8
    </code>
    (
    <code class="type">
     double precision
    </code>
    )
   </td>
   <td>
    <code class="type">
     float8
    </code>
   </td>
   <td>
    <code class="filename">
     postgres.h
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     int2
    </code>
    (
    <code class="type">
     smallint
    </code>
    )
   </td>
   <td>
    <code class="type">
     int16
    </code>
   </td>
   <td>
    <code class="filename">
     postgres.h
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     int4
    </code>
    (
    <code class="type">
     integer
    </code>
    )
   </td>
   <td>
    <code class="type">
     int32
    </code>
   </td>
   <td>
    <code class="filename">
     postgres.h
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     int8
    </code>
    (
    <code class="type">
     bigint
    </code>
    )
   </td>
   <td>
    <code class="type">
     int64
    </code>
   </td>
   <td>
    <code class="filename">
     postgres.h
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     interval
    </code>
   </td>
   <td>
    <code class="type">
     Interval*
    </code>
   </td>
   <td>
    <code class="filename">
     datatype/timestamp.h
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     lseg
    </code>
   </td>
   <td>
    <code class="type">
     LSEG*
    </code>
   </td>
   <td>
    <code class="filename">
     utils/geo_decls.h
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     name
    </code>
   </td>
   <td>
    <code class="type">
     Name
    </code>
   </td>
   <td>
    <code class="filename">
     postgres.h
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     numeric
    </code>
   </td>
   <td>
    <code class="type">
     Numeric
    </code>
   </td>
   <td>
    <code class="filename">
     utils/numeric.h
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     oid
    </code>
   </td>
   <td>
    <code class="type">
     Oid
    </code>
   </td>
   <td>
    <code class="filename">
     postgres.h
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     oidvector
    </code>
   </td>
   <td>
    <code class="type">
     oidvector*
    </code>
   </td>
   <td>
    <code class="filename">
     postgres.h
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     path
    </code>
   </td>
   <td>
    <code class="type">
     PATH*
    </code>
   </td>
   <td>
    <code class="filename">
     utils/geo_decls.h
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     point
    </code>
   </td>
   <td>
    <code class="type">
     POINT*
    </code>
   </td>
   <td>
    <code class="filename">
     utils/geo_decls.h
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     regproc
    </code>
   </td>
   <td>
    <code class="type">
     RegProcedure
    </code>
   </td>
   <td>
    <code class="filename">
     postgres.h
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     text
    </code>
   </td>
   <td>
    <code class="type">
     text*
    </code>
   </td>
   <td>
    <code class="filename">
     postgres.h
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     tid
    </code>
   </td>
   <td>
    <code class="type">
     ItemPointer
    </code>
   </td>
   <td>
    <code class="filename">
     storage/itemptr.h
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     time
    </code>
   </td>
   <td>
    <code class="type">
     TimeADT
    </code>
   </td>
   <td>
    <code class="filename">
     utils/date.h
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     time with time zone
    </code>
   </td>
   <td>
    <code class="type">
     TimeTzADT
    </code>
   </td>
   <td>
    <code class="filename">
     utils/date.h
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     timestamp
    </code>
   </td>
   <td>
    <code class="type">
     Timestamp
    </code>
   </td>
   <td>
    <code class="filename">
     datatype/timestamp.h
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     timestamp with time zone
    </code>
   </td>
   <td>
    <code class="type">
     TimestampTz
    </code>
   </td>
   <td>
    <code class="filename">
     datatype/timestamp.h
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     varchar
    </code>
   </td>
   <td>
    <code class="type">
     VarChar*
    </code>
   </td>
   <td>
    <code class="filename">
     postgres.h
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     xid
    </code>
   </td>
   <td>
    <code class="type">
     TransactionId
    </code>
   </td>
   <td>
    <code class="filename">
     postgres.h
    </code>
   </td>
  </tr>
 </tbody>
</table>










Agora que já analisamos todas as possíveis estruturas para os tipos de base, podemos mostrar alguns exemplos de funções reais.

### 36.10.3. Convenções de Chamada da Versão 1 [#](#XFUNC-C-V1-CALL-CONV)

A convenção de chamada da versão 1 depende de macros para suprimir a maioria da complexidade da passagem de argumentos e resultados. A declaração C de uma função da versão 1 é sempre:

```
Datum funcname(PG_FUNCTION_ARGS)
```

Além disso, o chamado macro:

```
PG_FUNCTION_INFO_V1(funcname);
```

deve aparecer no mesmo arquivo de origem. (Convencionalmente, é escrito logo antes da própria função.) Este chamado de macro não é necessário para funções de linguagem `internal`, uma vez que o PostgreSQL assume que todas as funções internas usam a convenção de versão 1. No entanto, é necessário para funções carregadas dinamicamente.

Em uma função de versão 1, cada argumento real é obtido usando uma macro `PG_GETARG_xxx()` que corresponde ao tipo de dados do argumento. (Em funções não estritas, é necessário uma verificação anterior sobre a nulidade do argumento usando `PG_ARGISNULL()`; veja abaixo.) O resultado é retornado usando uma macro `PG_RETURN_xxx()` para o tipo de retorno. `PG_GETARG_xxx()` leva como argumento o número do argumento da função a ser obtido, onde a contagem começa em 0. `PG_RETURN_xxx()` leva como argumento o valor real a ser retornado.

Para chamar outra função da versão 1, você pode usar `DirectFunctionCalln(func, arg1, ..., argn)`. Isso é particularmente útil quando você deseja chamar funções definidas na biblioteca interna padrão, usando uma interface semelhante à sua assinatura SQL.

Essas funções de conveniência e outras semelhantes podem ser encontradas em `fmgr.h`. A família `DirectFunctionCalln` espera um nome de função em C como seu primeiro argumento. Há também `OidFunctionCalln` que pedem o OID da função alvo, e algumas outras variantes. Todas essas esperam que os argumentos da função sejam fornecidos como `Datum`, e, da mesma forma, elas retornam `Datum`. Note que nem os argumentos nem o resultado podem ser NULL ao usar essas funções de conveniência.

Por exemplo, para chamar a função `starts_with(text, text)` a partir do C, você pode procurar no catálogo e descobrir que sua implementação em C é a função `Datum text_starts_with(PG_FUNCTION_ARGS)`. Normalmente, você usaria `DirectFunctionCall2(text_starts_with, ...)` para chamar tal função. No entanto, `starts_with(text, text)` requer informações de ordenação, portanto, falhará com “não foi possível determinar qual ordenação usar para comparação de strings” se chamada dessa maneira. Em vez disso, você deve usar `DirectFunctionCall2Coll(text_starts_with, ...)` e fornecer a ordenação desejada, que normalmente é apenas passada a partir de `PG_GET_COLLATION()`, como mostrado no exemplo abaixo.

`fmgr.h` também fornece macros que facilitam as conversões entre os tipos C e `Datum`. Por exemplo, para transformar `Datum` em `text*`, você pode usar `DatumGetTextPP(X)`. Embora alguns tipos tenham macros com nomes como `TypeGetDatum(X)` para a conversão reversa, `text*` não tem; é suficiente usar a macro genérica `PointerGetDatum(X)` para isso. Se sua extensão definir tipos adicionais, geralmente é conveniente definir macros semelhantes para seus tipos também.

Aqui estão alguns exemplos usando a convenção de chamada da versão 1:

```
#include "postgres.h"
#include <string.h>
#include "fmgr.h"
#include "utils/geo_decls.h"
#include "varatt.h"

PG_MODULE_MAGIC;

/* by value */

PG_FUNCTION_INFO_V1(add_one);

Datum
add_one(PG_FUNCTION_ARGS)
{
    int32   arg = PG_GETARG_INT32(0);

    PG_RETURN_INT32(arg + 1);
}

/* by reference, fixed length */

PG_FUNCTION_INFO_V1(add_one_float8);

Datum
add_one_float8(PG_FUNCTION_ARGS)
{
    /* The macros for FLOAT8 hide its pass-by-reference nature. */
    float8   arg = PG_GETARG_FLOAT8(0);

    PG_RETURN_FLOAT8(arg + 1.0);
}

PG_FUNCTION_INFO_V1(makepoint);

Datum
makepoint(PG_FUNCTION_ARGS)
{
    /* Here, the pass-by-reference nature of Point is not hidden. */
    Point     *pointx = PG_GETARG_POINT_P(0);
    Point     *pointy = PG_GETARG_POINT_P(1);
    Point     *new_point = (Point *) palloc(sizeof(Point));

    new_point->x = pointx->x;
    new_point->y = pointy->y;

    PG_RETURN_POINT_P(new_point);
}

/* by reference, variable length */

PG_FUNCTION_INFO_V1(copytext);

Datum
copytext(PG_FUNCTION_ARGS)
{
    text     *t = PG_GETARG_TEXT_PP(0);

    /*
     * VARSIZE_ANY_EXHDR is the size of the struct in bytes, minus the
     * VARHDRSZ or VARHDRSZ_SHORT of its header.  Construct the copy with a
     * full-length header.
     */
    text     *new_t = (text *) palloc(VARSIZE_ANY_EXHDR(t) + VARHDRSZ);
    SET_VARSIZE(new_t, VARSIZE_ANY_EXHDR(t) + VARHDRSZ);

    /*
     * VARDATA is a pointer to the data region of the new struct.  The source
     * could be a short datum, so retrieve its data through VARDATA_ANY.
     */
    memcpy(VARDATA(new_t),          /* destination */
           VARDATA_ANY(t),          /* source */
           VARSIZE_ANY_EXHDR(t));   /* how many bytes */
    PG_RETURN_TEXT_P(new_t);
}

PG_FUNCTION_INFO_V1(concat_text);

Datum
concat_text(PG_FUNCTION_ARGS)
{
    text  *arg1 = PG_GETARG_TEXT_PP(0);
    text  *arg2 = PG_GETARG_TEXT_PP(1);
    int32 arg1_size = VARSIZE_ANY_EXHDR(arg1);
    int32 arg2_size = VARSIZE_ANY_EXHDR(arg2);
    int32 new_text_size = arg1_size + arg2_size + VARHDRSZ;
    text *new_text = (text *) palloc(new_text_size);

    SET_VARSIZE(new_text, new_text_size);
    memcpy(VARDATA(new_text), VARDATA_ANY(arg1), arg1_size);
    memcpy(VARDATA(new_text) + arg1_size, VARDATA_ANY(arg2), arg2_size);
    PG_RETURN_TEXT_P(new_text);
}

/* A wrapper around starts_with(text, text) */

PG_FUNCTION_INFO_V1(t_starts_with);

Datum
t_starts_with(PG_FUNCTION_ARGS)
{
    text       *t1 = PG_GETARG_TEXT_PP(0);
    text       *t2 = PG_GETARG_TEXT_PP(1);
    Oid         collid = PG_GET_COLLATION();
    bool        result;

    result = DatumGetBool(DirectFunctionCall2Coll(text_starts_with,
                                                  collid,
                                                  PointerGetDatum(t1),
                                                  PointerGetDatum(t2)));
    PG_RETURN_BOOL(result);
}
```

Supondo que o código acima tenha sido preparado no arquivo `funcs.c` e compilado em um objeto compartilhado, poderíamos definir as funções para o PostgreSQL com comandos como este:

```
CREATE FUNCTION add_one(integer) RETURNS integer
     AS 'DIRECTORY/funcs', 'add_one'
     LANGUAGE C STRICT;

-- note overloading of SQL function name "add_one"
CREATE FUNCTION add_one(double precision) RETURNS double precision
     AS 'DIRECTORY/funcs', 'add_one_float8'
     LANGUAGE C STRICT;

CREATE FUNCTION makepoint(point, point) RETURNS point
     AS 'DIRECTORY/funcs', 'makepoint'
     LANGUAGE C STRICT;

CREATE FUNCTION copytext(text) RETURNS text
     AS 'DIRECTORY/funcs', 'copytext'
     LANGUAGE C STRICT;

CREATE FUNCTION concat_text(text, text) RETURNS text
     AS 'DIRECTORY/funcs', 'concat_text'
     LANGUAGE C STRICT;

CREATE FUNCTION t_starts_with(text, text) RETURNS boolean
     AS 'DIRECTORY/funcs', 't_starts_with'
     LANGUAGE C STRICT;
```

Aqui, *`DIRECTORY`* representa o diretório do arquivo da biblioteca compartilhada (por exemplo, o diretório do tutorial PostgreSQL, que contém o código dos exemplos usados nesta seção). (Um estilo melhor seria usar apenas `'funcs'` na cláusula `AS`, após ter adicionado *`DIRECTORY`* ao caminho de busca. Em qualquer caso, podemos omitir a extensão específica do sistema para uma biblioteca compartilhada, comumente `.so`.))

Observe que especificamos as funções como "strict", o que significa que o sistema deve assumir automaticamente um resultado nu se qualquer valor de entrada for nulo. Ao fazer isso, evitamos ter que verificar entradas nulos no código da função. Sem isso, teríamos que verificar valores nulos explicitamente, usando `PG_ARGISNULL()`.

O macro `PG_ARGISNULL(n)` permite que uma função teste se cada entrada é nula. (É claro que fazer isso é necessário apenas em funções não declaradas como "estricas". Como com os macros `PG_GETARG_xxx()`, os argumentos de entrada são contados a partir de zero. Note que se deve abster de executar `PG_GETARG_xxx()` até verificar que o argumento não é nulo. Para retornar um resultado nulo, execute `PG_RETURN_NULL()`; isso funciona tanto em funções estritas quanto em funções não estritas.

À primeira vista, as convenções de codificação da versão 1 podem parecer apenas obscuridade inútil, em comparação com o uso de convenções de chamada simples `C`. No entanto, elas nos permitem lidar com argumentos/valores de retorno `NULL`áveis e valores "toasteados" (comprimidos ou fora de linha).

Outras opções fornecidas pela interface da versão 1 são duas variantes das macros `PG_GETARG_xxx()`. A primeira delas, `PG_GETARG_xxx_COPY()`, garante o retorno de uma cópia do argumento especificado que é segura para escrita. (As macros normais às vezes retornam um ponteiro para um valor que é fisicamente armazenado em uma tabela, que não deve ser escrito. Usar as macros `PG_GETARG_xxx_COPY()` garante um resultado legível.) A segunda variante consiste nas macros `PG_GETARG_xxx_SLICE()`, que levam três argumentos. O primeiro é o número do argumento da função (como acima). O segundo e terceiro são o deslocamento e o comprimento do segmento a ser retornado. Os deslocamentos são contados a partir de zero, e um comprimento negativo solicita que o restante do valor seja retornado. Essas macros fornecem acesso mais eficiente a partes de grandes valores no caso em que eles têm tipo de armazenamento “externo”. (O tipo de armazenamento de uma coluna pode ser especificado usando `ALTER TABLE tablename ALTER COLUMN colname SET STORAGE storagetype`. *`storagetype`* é uma das `plain`, `external`, `extended`, ou `main`.)

Por fim, as convenções de chamada de função da versão 1 permitem retornar resultados de conjunto ([Seção 36.10.9](xfunc-c.md#XFUNC-C-RETURN-SET)) e implementar funções de gatilho ([Capítulo 37](triggers.md)) e manipuladores de chamadas de linguagem procedural ([Capítulo 57](plhandler.md)). Para mais detalhes, consulte `src/backend/utils/fmgr/README` na distribuição de fonte.

### 36.10.4. Escrever Código [#](#XFUNC-C-CODE)

Antes de nos aprofundarmos em tópicos mais avançados, devemos discutir algumas regras de codificação para funções em linguagem C do PostgreSQL. Embora seja possível carregar funções escritas em linguagens que não são C no PostgreSQL, isso geralmente é difícil (quando é possível) porque outras linguagens, como C++, FORTRAN ou Pascal, muitas vezes não seguem a mesma convenção de chamada que o C. Isso significa que outras linguagens não passam argumentos e valores de retorno entre funções da mesma maneira. Por essa razão, vamos assumir que suas funções em linguagem C são realmente escritas em C.

As regras básicas para escrever e construir funções C são as seguintes:

* Use `pg_config --includedir-server` para descobrir onde os arquivos de cabeçalho do servidor PostgreSQL estão instalados no seu sistema (ou no sistema no qual seus usuários irão executar).
* Compilar e vincular seu código de forma que ele possa ser carregado dinamicamente no PostgreSQL sempre requer flags especiais. Veja [Seção 36.10.5](xfunc-c.md#DFUNC) para uma explicação detalhada de como fazer isso para seu sistema operacional específico.
* Lembre-se de definir um "bloco mágico" para sua biblioteca compartilhada, conforme descrito em [Seção 36.10.1](xfunc-c.md#XFUNC-C-DYNLOAD).
* Ao alocar memória, use as funções PostgreSQL `palloc` e `pfree` em vez das funções correspondentes da biblioteca C `malloc` e `free`. A memória alocada por `palloc` será liberada automaticamente no final de cada transação, prevenindo vazamentos de memória.
* Sempre inicialize os bytes de suas estruturas usando `memset` (ou aloque-os com `palloc0` em primeiro lugar). Mesmo que você atribua a cada campo de sua estrutura, pode haver alinhamento de preenchimento (buracos na estrutura) que contenham valores de lixo. Sem isso, é difícil suportar índices de hash ou junções de hash, pois você deve selecionar apenas os bits significativos de sua estrutura de dados para calcular um hash. O planejador também às vezes depende da comparação de constantes via igualdade binária, então você pode obter resultados indesejados de planejamento se valores logicamente equivalentes não forem iguais binariamente.
* A maioria dos tipos internos do PostgreSQL são declarados em `postgres.h`, enquanto as interfaces do gerenciador de funções (`PG_FUNCTION_ARGS`, etc.) estão em `fmgr.h`, então você precisará incluir pelo menos esses dois arquivos. Por razões de portabilidade, é melhor incluir `postgres.h` *primeiro*, antes de qualquer outro arquivo de cabeçalho do sistema ou do usuário. Incluir `postgres.h` também incluirá `elog.h` e `palloc.h` para você.
* Os nomes de símbolos definidos dentro de arquivos de objeto não devem conflitar entre si ou com símbolos definidos no executável do servidor PostgreSQL. Você terá que renomear suas funções ou variáveis se receber mensagens de erro a esse efeito.

### 36.10.5. Compilação e vinculação de funções carregadas dinamicamente [#](#DFUNC)

Antes de você poder usar as funções de extensão do PostgreSQL escritas em C, elas devem ser compiladas e vinculadas de uma maneira especial para produzir um arquivo que pode ser carregado dinamicamente pelo servidor. Para ser preciso, uma *biblioteca compartilhada* precisa ser criada.

Para obter informações além do que está contido nesta seção, você deve ler a documentação do seu sistema operacional, em particular as páginas do manual do compilador C, `cc`, e do editor de links, `ld`. Além disso, o código-fonte do PostgreSQL contém vários exemplos de funcionamento no diretório `contrib`. Se você depender desses exemplos, seus módulos ficarão dependentes da disponibilidade do código-fonte do PostgreSQL, no entanto.

Criar bibliotecas compartilhadas é, em geral, análogo a vincular executaveis: primeiro, os arquivos de origem são compilados em arquivos de objeto, então os arquivos de objeto são vinculados juntos. Os arquivos de objeto precisam ser criados como código *independente da posição* (PIC), o que conceitualmente significa que eles podem ser colocados em um local arbitrário na memória quando são carregados pelo executável. (Arquivos de objeto destinados a executaveis geralmente não são compilados dessa maneira.) O comando para vincular uma biblioteca compartilhada contém faixas especiais para distingui-la do vincular um executável (pelo menos teoricamente — em alguns sistemas a prática é muito mais desagradável).

Nos exemplos a seguir, assumimos que seu código-fonte está em um arquivo `foo.c` e criaremos uma biblioteca compartilhada `foo.so`. O arquivo de objeto intermediário será chamado `foo.o`, a menos que haja outra indicação. Uma biblioteca compartilhada pode conter mais de um arquivo de objeto, mas aqui usamos apenas um.

FreeBSD: A bandeira do compilador para criar PIC é `-fPIC`. Para criar bibliotecas compartilhadas, a bandeira do compilador é `-shared`.

```
cc -fPIC -c foo.c cc -shared -o foo.so foo.o
```

Isso é aplicável a partir da versão 13.0 do FreeBSD, versões mais antigas utilizavam o compilador `gcc`.

Linux: A bandeira do compilador para criar PIC é `-fPIC`. A bandeira do compilador para criar uma biblioteca compartilhada é `-shared`. Um exemplo completo parece assim:

```
cc -fPIC -c foo.c cc -shared -o foo.so foo.o
```

macOS: Aqui está um exemplo. Assume que as ferramentas de desenvolvimento estão instaladas.

```
cc -c foo.c cc -bundle -flat_namespace -undefined suppress -o foo.so foo.o
```

NetBSD: A opção do compilador para criar PIC é `-fPIC`. Para sistemas ELF, o compilador com a opção `-shared` é usado para vincular bibliotecas compartilhadas. Nos sistemas mais antigos, não ELF, é usado `ld -Bshareable`.

```
gcc -fPIC -c foo.c gcc -shared -o foo.so foo.o
```

OpenBSD: A opção do compilador para criar PIC é `-fPIC`. `ld -Bshareable` é usada para vincular bibliotecas compartilhadas.

```
gcc -fPIC -c foo.c ld -Bshareable -o foo.so foo.o
```

Solaris: A bandeira do compilador para criar PIC é `-KPIC` com o compilador Sun e `-fPIC` com GCC. Para vincular bibliotecas compartilhadas, a opção do compilador é `-G` com qualquer compilador ou, alternativamente, `-shared` com GCC.

```
cc -KPIC -c foo.c cc -G -o foo.so foo.o
```

ou

```
gcc -fPIC -c foo.c gcc -G -o foo.so foo.o
```

### DICA

Se isso é muito complicado para você, você deve considerar o uso de [GNU Libtool](https://www.gnu.org/software/libtool/), que esconde as diferenças de plataforma por trás de uma interface uniforme.

O arquivo de biblioteca compartilhada resultante pode então ser carregado no PostgreSQL. Ao especificar o nome do arquivo da biblioteca compartilhada para o comando `CREATE FUNCTION`, é necessário fornecer o nome do arquivo de objeto intermediário, não o arquivo de objeto intermediário. Observe que a extensão padrão de biblioteca compartilhada do sistema (geralmente `.so` ou `.sl`) pode ser omitida do comando `CREATE FUNCTION`, e normalmente deve ser omitida para melhor portabilidade.

Reveja [Seção 36.10.1](xfunc-c.md#XFUNC-C-DYNLOAD) sobre onde o servidor espera encontrar os arquivos da biblioteca compartilhada.

### 36.10.6. Orientações sobre estabilidade da API e ABI do servidor [#](#XFUNC-API-ABI-STABILITY-GUIDANCE)

Esta seção contém orientações para autores de extensões e outros plugins do servidor sobre a estabilidade da API e ABI no servidor PostgreSQL.

#### 36.10.6.1. Geral [#](#XFUNC-GUIDANCE-GENERAL)

O servidor PostgreSQL contém várias APIs bem demarcadas para plugins do servidor, como o gerenciador de funções (fmgr, descrito neste capítulo), SPI ([Capítulo 45](spi.md)) e vários ganchos especificamente projetados para extensões. Essas interfaces são cuidadosamente gerenciadas para estabilidade e compatibilidade a longo prazo. No entanto, o conjunto completo de funções e variáveis globais no servidor efetivamente constitui a API públicamente utilizável, e a maioria delas não foi projetada com extensibilidade e estabilidade a longo prazo em mente.

Portanto, embora aproveitar essas interfaces seja válido, quanto mais se afasta do caminho bem trilhado, mais provável é que, em algum momento, se possa encontrar problemas de compatibilidade com API ou ABI. Os autores de extensões são incentivados a fornecer feedback sobre seus requisitos, para que, com o tempo, à medida que novos padrões de uso surgem, certas interfaces possam ser consideradas mais estabilizadas ou novas interfaces, melhor projetadas, podem ser adicionadas.

#### 36.10.6.2. Compatibilidade com API [#](#XFUNC-GUIDANCE-API-COMPATIBILITY)

A API, ou interface de programação de aplicativos, é a interface usada na hora da compilação.

##### 36.10.6.2.1. Principais versões [#](#XFUNC-GUIDANCE-API-MAJOR-VERSIONS)

Não há *nenhuma* promessa de compatibilidade com a API entre as versões principais do PostgreSQL. Portanto, o código de extensão pode exigir alterações no código-fonte para funcionar com várias versões principais. Essas alterações geralmente podem ser gerenciadas com condições pré-processadoras, como `#if PG_VERSION_NUM >= 160000`. Extensões sofisticadas que utilizam interfaces além das bem demarcadas geralmente exigem algumas dessas alterações para cada versão principal do servidor.

##### 36.10.6.2.2. Versões menores [#](#XFUNC-GUIDANCE-API-MNINOR-VERSIONS)

O PostgreSQL faz um esforço para evitar quebras de API no servidor em versões menores. Em geral, o código de extensão que compila e funciona com uma versão menor também deve compilar e funcionar com qualquer outra versão menor da mesma versão principal, passada ou futura.

Quando uma mudança *for* necessária, ela será cuidadosamente gerenciada, levando em consideração os requisitos das extensões. Essas mudanças serão comunicadas nas notas de lançamento ([Apêndice E](release.md "Appendix E. Release Notes")).

#### 36.10.6.3. Compatibilidade com o ABI [#](#XFUNC-GUIDANCE-ABI-COMPATIBILITY)

A ABI, ou interface binária de aplicação, é a interface utilizada no momento da execução.

##### 36.10.6.3.1. Principais versões [#](#XFUNC-GUIDANCE-ABI-MAJOR-VERSIONS)

Servidores de diferentes versões principais têm ABIs intencionalmente incompatíveis. Portanto, as extensões que utilizam APIs de servidor devem ser recompiladas para cada versão principal. A inclusão de `PG_MODULE_MAGIC` (consulte [Seção 36.10.1] (xfunc-c.md#XFUNC-C-DYNLOAD "36.10.1. Dynamic Loading")) garante que o código compilado para uma versão principal será rejeitado por outras versões principais.

##### 36.10.6.3.2. Versões menores [#](#XFUNC-GUIDANCE-ABI-MNINOR-VERSIONS)

O PostgreSQL faz um esforço para evitar quebras no ABI em versões menores. Em geral, uma extensão compilada contra qualquer versão menor deve funcionar com qualquer outra versão menor da mesma versão principal, passada ou futura.

Quando uma mudança *é* necessária, o PostgreSQL escolherá a mudança menos invasiva possível, por exemplo, encolhendo um novo campo em espaço de preenchimento ou anexando-o ao final de uma estrutura. Esse tipo de mudança não deve afetar extensões, a menos que use padrões de código muito incomuns.

Em casos raros, no entanto, mesmo essas mudanças não invasivas podem ser impraticáveis ou impossíveis. Nesse caso, a mudança será cuidadosamente gerenciada, levando em consideração os requisitos das extensões. Essas mudanças também serão documentadas nas notas de lançamento ([Apêndice E](release.md)).

Observe, no entanto, que muitas partes do servidor não são projetadas ou mantidas como APIs (e que, na maioria dos casos, a fronteira real também não é bem definida). Se necessidades urgentes surgirem, as alterações nessas partes serão feitas naturalmente com menos consideração para o código de extensão do que as alterações em interfaces bem definidas e amplamente utilizadas.

Além disso, na ausência de detecção automática dessas mudanças, isso não é uma garantia, mas historicamente, tais mudanças de quebra foram extremamente raras.

### 36.10.7. Argumentos de tipo composto [#](#XFUNC-C-COMPOSITE-TYPE-ARGS)

Os tipos compostos não têm um layout fixo como as estruturas C. As instâncias de um tipo composto podem conter campos nulos. Além disso, os tipos compostos que fazem parte de uma hierarquia de herança podem ter campos diferentes de outros membros da mesma hierarquia de herança. Portanto, o PostgreSQL fornece uma interface de função para acessar campos de tipos compostos a partir de C.

Suponha que queira escrever uma função para responder à consulta:

```
SELECT name, c_overpaid(emp, 1500) AS overpaid FROM emp WHERE name = 'Bill' OR name = 'Sam';
```

Usando as convenções de chamada da versão 1, podemos definir `c_overpaid` como:

```
#include "postgres.h"
#include "executor/executor.h"  /* for GetAttributeByName() */

PG_MODULE_MAGIC;

PG_FUNCTION_INFO_V1(c_overpaid);

Datum c_overpaid(PG_FUNCTION_ARGS) { HeapTupleHeader  t = PG_GETARG_HEAPTUPLEHEADER(0); int32            limit = PG_GETARG_INT32(1); bool isnull; Datum salary;

    salary = GetAttributeByName(t, "salary", &isnull); if (isnull) PG_RETURN_BOOL(false); /* Alternatively, we might prefer to do PG_RETURN_NULL() for null salary. */

    PG_RETURN_BOOL(DatumGetInt32(salary) > limit); }
```

`GetAttributeByName` é a função do sistema PostgreSQL que retorna atributos da linha especificada. Ela tem três argumentos: o argumento do tipo `HeapTupleHeader` passado na função, o nome do atributo desejado e um parâmetro de retorno que indica se o atributo é nulo. `GetAttributeByName` retorna um valor `Datum` que você pode converter para o tipo de dados apropriado usando a função apropriada `DatumGetXXX()`. Observe que o valor de retorno não tem significado se a marca de nulo estiver definida; sempre verifique a marca de nulo antes de tentar fazer algo com o resultado.

Existe também `GetAttributeByNum`, que seleciona o atributo alvo pelo número da coluna em vez do nome.

O comando a seguir declara a função `c_overpaid` em SQL:

```
CREATE FUNCTION c_overpaid(emp, integer) RETURNS boolean AS 'DIRECTORY/funcs', 'c_overpaid' LANGUAGE C STRICT;
```

Observe que usamos `STRICT` para não ter que verificar se os argumentos de entrada eram NULL.

### 36.10.8. Retorno de linhas (tipos compostos) [#](#XFUNC-C-RETURNING-ROWS)

Para retornar uma linha ou um valor de tipo composto de uma função em linguagem C, você pode usar uma API especial que oferece macros e funções para ocultar a maioria da complexidade na construção de tipos de dados compostos. Para usar essa API, o arquivo de origem deve incluir:

```
#include "funcapi.h"
```

Existem duas maneiras de construir um valor de dados composto (doravante denominado “tuplo”): você pode construí-lo a partir de uma matriz de valores de Datum, ou a partir de uma matriz de strings C que podem ser passadas às funções de conversão de entrada dos tipos de dados das colunas do tuplo. Em qualquer caso, você precisa primeiro obter ou construir um descritor `TupleDesc` para a estrutura do tuplo. Ao trabalhar com Datums, você passa o `TupleDesc` para `BlessTupleDesc`, e então chama o `heap_form_tuple` para cada linha. Ao trabalhar com strings C, você passa o `TupleDesc` para `TupleDescGetAttInMetadata`, e então chama `BuildTupleFromCStrings` para cada linha. No caso de uma função que retorne um conjunto de tuplos, as etapas de configuração podem ser feitas todas uma vez durante a primeira chamada da função.

Várias funções auxiliares estão disponíveis para configurar o necessário `TupleDesc`. A maneira recomendada para fazer isso na maioria das funções que retornam valores compostos é chamar:

```
TypeFuncClass get_call_result_type(FunctionCallInfo fcinfo, Oid *resultTypeId, TupleDesc *resultTupleDesc)
```

passando a mesma estrutura `fcinfo` passada para a função chamada própria. (Isso, claro, exige que você use as convenções de chamada da versão 1.) `resultTypeId` pode ser especificado como `NULL` ou como o endereço de uma variável local para receber o tipo OID do resultado da função. `resultTupleDesc` deve ser o endereço de uma variável local `TupleDesc`. Verifique se o resultado é `TYPEFUNC_COMPOSITE`; se sim, `resultTupleDesc` foi preenchido com o necessário `TupleDesc`. (Se não for, você pode relatar um erro na linha do tipo “registro de retorno da função chamado em contexto que não pode aceitar registro de tipo”).

### DICA

`get_call_result_type` pode resolver o tipo real de um resultado de função polimórfica; portanto, é útil em funções que retornam resultados escalares polimórficos, não apenas em funções que retornam compostos. A saída `resultTypeId` é principalmente útil para funções que retornam escalares polimórficos.

### Nota

`get_call_result_type` tem um irmão `get_expr_result_type`, que pode ser usado para resolver o tipo de saída esperado para uma chamada de função representada por uma árvore de expressão. Isso pode ser usado quando se tenta determinar o tipo de resultado de fora da própria função. Também existe `get_func_result_type`, que pode ser usado quando apenas o OID da função está disponível. No entanto, essas funções não podem lidar com funções declaradas para retornar `record`, e `get_func_result_type` não pode resolver tipos polimórficos, portanto, você deve preferencialmente usar `get_call_result_type`.

Funções mais antigas, agora desatualizadas, para obtenção de `TupleDesc` são:

```
TupleDesc RelationNameGetTupleDesc(const char *relname)
```

para obter um `TupleDesc` para o tipo de linha de uma relação nomeada, e:

```
TupleDesc TypeGetTupleDesc(Oid typeoid, List *colaliases)
```

para obter um `TupleDesc` com base em um OID de tipo. Isso pode ser usado para obter um `TupleDesc` para um tipo de base ou composto. No entanto, não funcionará para uma função que retorne `record`, e não pode resolver tipos polimórficos.

Depois de ter um `TupleDesc`, ligue:

```
TupleDesc BlessTupleDesc(TupleDesc tupdesc)
```

se você planeja trabalhar com Datums, ou:

```
AttInMetadata *TupleDescGetAttInMetadata(TupleDesc tupdesc)
```

se você planeja trabalhar com strings C. Se você está escrevendo uma função que retorna um conjunto, pode salvar os resultados dessas funções na estrutura `FuncCallContext` — use o campo `tuple_desc` ou `attinmeta`, respectivamente.

Ao trabalhar com Dimensões, use:

```
HeapTuple heap_form_tuple(TupleDesc tupdesc, Datum *values, bool *isnull)
```

para construir um `HeapTuple` com base em dados do usuário em formato Datum.

Ao trabalhar com strings C, use:

```
HeapTuple BuildTupleFromCStrings(AttInMetadata *attinmeta, char **values)
```

para construir um `HeapTuple` com base em dados do usuário em forma de string C. *`values`* é um array de strings C, um para cada atributo da linha de retorno. Cada string C deve estar na forma esperada pela função de entrada do tipo de dados do atributo. Para retornar um valor nulo para um dos atributos, o ponteiro correspondente no array *`values`* deve ser definido como `NULL`. Esta função precisará ser chamada novamente para cada linha que você retornar.

Depois de construir uma tupla para retornar de sua função, ela deve ser convertida em um `Datum`. Use:

```
HeapTupleGetDatum(HeapTuple tuple)
```

para converter um `HeapTuple` em um Datum válido. Este `Datum` pode ser retornado diretamente se você pretende retornar apenas uma única linha, ou ele pode ser usado como o valor de retorno atual em uma função que retorna um conjunto.

Um exemplo aparece na seção seguinte.

### 36.10.9. Conjuntos de retorno [#](#XFUNC-C-RETURN-SET)

As funções em linguagem C têm duas opções para retornar conjuntos (várias linhas). Em um método, chamado modo *ValuePerCall*, uma função que retorna um conjunto é chamada repetidamente (passando os mesmos argumentos cada vez) e retorna uma nova linha em cada chamada, até que não tenha mais linhas para retornar e sinaliza isso ao retornar NULL. A função que retorna um conjunto (SRF) deve, portanto, salvar estado suficiente entre as chamadas para lembrar o que estava fazendo e retornar o próximo item correto em cada chamada. No outro método, chamado modo *Materialize*, uma SRF preenche e retorna um objeto de tuplestore contendo todo o seu resultado; então, apenas uma chamada ocorre para todo o resultado, e não é necessário estado entre as chamadas.

Ao usar o modo ValuePerCall, é importante lembrar que a consulta não é garantida para ser executada até o final; ou seja, devido a opções como `LIMIT`, o executor pode parar de fazer chamadas à função que retorna o conjunto antes de todas as linhas terem sido obtidas. Isso significa que não é seguro realizar atividades de limpeza na última chamada, porque isso pode nunca acontecer. Recomenda-se usar o modo Materialize para funções que precisam acessar recursos externos, como descritores de arquivo.

O restante desta seção documenta um conjunto de macros auxiliares que são comumente usadas (embora não sejam obrigatórias para serem usadas) para SRFs que utilizam o modo ValuePerCall. Detalhes adicionais sobre o modo Materialize podem ser encontrados em `src/backend/utils/fmgr/README`. Além disso, os módulos `contrib` na distribuição de código-fonte do PostgreSQL contêm muitos exemplos de SRFs que utilizam tanto o modo ValuePerCall quanto o Materialize.

Para usar as macros de suporte ValuePerCall descritas aqui, inclua `funcapi.h`. Essas macros funcionam com uma estrutura `FuncCallContext` que contém o estado que precisa ser salvo em todas as chamadas. Dentro do SRF de chamada, `fcinfo->flinfo->fn_extra` é usado para manter um ponteiro para `FuncCallContext` em todas as chamadas. As macros preenchem automaticamente esse campo na primeira utilização e esperam encontrar o mesmo ponteiro lá nos usos subsequentes.

```
typedef struct FuncCallContext { /*
     * Number of times we've been called before *
     * call_cntr is initialized to 0 for you by SRF_FIRSTCALL_INIT(), and
     * incremented for you every time SRF_RETURN_NEXT() is called. */ uint64 call_cntr;

    /*
     * OPTIONAL maximum number of calls *
     * max_calls is here for convenience only and setting it is optional.
     * If not set, you must provide alternative means to know when the
     * function is done. */ uint64 max_calls;

    /*
     * OPTIONAL pointer to miscellaneous user-provided context information *
     * user_fctx is for use as a pointer to your own data to retain
     * arbitrary context information between calls of your function. */ void *user_fctx;

    /*
     * OPTIONAL pointer to struct containing attribute type input metadata *
     * attinmeta is for use when returning tuples (i.e., composite data types)
     * and is not used when returning base data types. It is only needed
     * if you intend to use BuildTupleFromCStrings() to create the return
     * tuple. */ AttInMetadata *attinmeta;

    /*
     * memory context used for structures that must live for multiple calls *
     * multi_call_memory_ctx is set by SRF_FIRSTCALL_INIT() for you, and used
     * by SRF_RETURN_DONE() for cleanup. It is the most appropriate memory
     * context for any memory that is to be reused across multiple calls
     * of the SRF. */ MemoryContext multi_call_memory_ctx;

    /*
     * OPTIONAL pointer to struct containing tuple description *
     * tuple_desc is for use when returning tuples (i.e., composite data types)
     * and is only needed if you are going to build the tuples with
     * heap_form_tuple() rather than with BuildTupleFromCStrings().  Note that
     * the TupleDesc pointer stored here should usually have been run through
     * BlessTupleDesc() first. */ TupleDesc tuple_desc;

} FuncCallContext;
```

As macros a serem utilizadas por um SRF usando essa infraestrutura são:

```
SRF_IS_FIRSTCALL()
```

Use isso para determinar se sua função está sendo chamada pela primeira ou uma segunda vez. Na primeira chamada (apenas), chame:

```
SRF_FIRSTCALL_INIT()
```

para inicializar o `FuncCallContext`. Em cada chamada de função, incluindo a primeira, chame:

```
SRF_PERCALL_SETUP()
```

para configurar para uso do `FuncCallContext`.

Se sua função tiver dados para ser retornados na chamada atual, use:

```
SRF_RETURN_NEXT(funcctx, result)
```

para devolvê-lo ao chamador. (`result` deve ser do tipo `Datum`, um único valor ou uma tupla preparada conforme descrito acima.) Finalmente, quando sua função terminar de devolver dados, use:

```
SRF_RETURN_DONE(funcctx)
```

limpar e acabar com o SRF.

O contexto de memória que é atual quando o SRF é chamado é um contexto transitório que será apagado entre as chamadas. Isso significa que você não precisa chamar `pfree` em tudo o que você alocou usando `palloc`; ele desaparecerá de qualquer maneira. No entanto, se você quiser alocar quaisquer estruturas de dados para serem mantidas entre as chamadas, você precisa colocá-las em outro lugar. O contexto de memória referenciado por `multi_call_memory_ctx` é um local adequado para qualquer dado que precise sobreviver até o SRF terminar de ser executado. Na maioria dos casos, isso significa que você deve alternar para `multi_call_memory_ctx` enquanto faz a configuração da primeira chamada. Use `funcctx->user_fctx` para manter um ponteiro para quaisquer estruturas de dados de chamada cruzada.

(Os dados que você aloca em `multi_call_memory_ctx` desaparecerão automaticamente quando a consulta terminar, então não é necessário liberar manualmente esses dados.)

### Aviso

Embora os argumentos reais da função permaneçam inalterados entre as chamadas, se você destoar os valores dos argumentos (o que normalmente é feito de forma transparente pelo macro `PG_GETARG_xxx` em contexto transitório, então as cópias destoadas serão liberadas em cada ciclo. Assim, se você manter referências a tais valores em `user_fctx`, você deve ou copiá-los para o `multi_call_memory_ctx` após o destoação, ou garantir que você destoar os valores apenas nesse contexto.

Um exemplo completo de pseudo-código parece o seguinte:

```
Datum my_set_returning_function(PG_FUNCTION_ARGS) { FuncCallContext  *funcctx; Datum             result; further declarations as needed

    if (SRF_IS_FIRSTCALL()) { MemoryContext oldcontext;

        funcctx = SRF_FIRSTCALL_INIT(); oldcontext = MemoryContextSwitchTo(funcctx->multi_call_memory_ctx); /* One-time setup code appears here: */ user code if returning composite build TupleDesc, and perhaps AttInMetadata endif returning composite user code MemoryContextSwitchTo(oldcontext); }

    /* Each-time setup code appears here: */ user code funcctx = SRF_PERCALL_SETUP(); user code

    /* this is just one way we might test whether we are done: */ if (funcctx->call_cntr < funcctx->max_calls) { /* Here we want to return another item: */ user code obtain result Datum SRF_RETURN_NEXT(funcctx, result); } else { /* Here we are done returning items, so just report that fact. */ /* (Resist the temptation to put cleanup code here.) */ SRF_RETURN_DONE(funcctx); } }
```

Um exemplo completo de um SRF simples que retorna um tipo composto parece assim:

```
PG_FUNCTION_INFO_V1(retcomposite);

Datum retcomposite(PG_FUNCTION_ARGS) { FuncCallContext     *funcctx; int                  call_cntr; int                  max_calls; TupleDesc            tupdesc; AttInMetadata       *attinmeta;

    /* stuff done only on the first call of the function */ if (SRF_IS_FIRSTCALL()) { MemoryContext   oldcontext;

        /* create a function context for cross-call persistence */ funcctx = SRF_FIRSTCALL_INIT();

        /* switch to memory context appropriate for multiple function calls */ oldcontext = MemoryContextSwitchTo(funcctx->multi_call_memory_ctx);

        /* total number of tuples to be returned */ funcctx->max_calls = PG_GETARG_INT32(0);

        /* Build a tuple descriptor for our result type */ if (get_call_result_type(fcinfo, NULL, &tupdesc) != TYPEFUNC_COMPOSITE) ereport(ERROR, (errcode(ERRCODE_FEATURE_NOT_SUPPORTED), errmsg("function returning record called in context " "that cannot accept type record")));

        /*
         * generate attribute metadata needed later to produce tuples from raw
         * C strings */ attinmeta = TupleDescGetAttInMetadata(tupdesc); funcctx->attinmeta = attinmeta;

        MemoryContextSwitchTo(oldcontext); }

    /* stuff done on every call of the function */ funcctx = SRF_PERCALL_SETUP();

    call_cntr = funcctx->call_cntr; max_calls = funcctx->max_calls; attinmeta = funcctx->attinmeta;

    if (call_cntr < max_calls)    /* do when there is more left to send */ { char       **values; HeapTuple    tuple; Datum        result;

        /*
         * Prepare a values array for building the returned tuple.
         * This should be an array of C strings which will
         * be processed later by the type input functions. */ values = (char **) palloc(3 * sizeof(char *)); values[0] = (char *) palloc(16 * sizeof(char)); values[1] = (char *) palloc(16 * sizeof(char)); values[2] = (char *) palloc(16 * sizeof(char));

        snprintf(values[0], 16, "%d", 1 * PG_GETARG_INT32(1)); snprintf(values[1], 16, "%d", 2 * PG_GETARG_INT32(1)); snprintf(values[2], 16, "%d", 3 * PG_GETARG_INT32(1));

        /* build a tuple */ tuple = BuildTupleFromCStrings(attinmeta, values);

        /* make the tuple into a datum */ result = HeapTupleGetDatum(tuple);

        /* clean up (this is not really necessary) */ pfree(values[0]); pfree(values[1]); pfree(values[2]); pfree(values);

        SRF_RETURN_NEXT(funcctx, result); } else    /* do when there is no more left */ { SRF_RETURN_DONE(funcctx); } }
```

Uma maneira de declarar essa função no SQL é:

```
CREATE TYPE __retcomposite AS (f1 integer, f2 integer, f3 integer);

CREATE OR REPLACE FUNCTION retcomposite(integer, integer) RETURNS SETOF __retcomposite AS 'filename', 'retcomposite' LANGUAGE C IMMUTABLE STRICT;
```

Outra maneira é usar parâmetros OUT:

```
CREATE OR REPLACE FUNCTION retcomposite(IN integer, IN integer, OUT f1 integer, OUT f2 integer, OUT f3 integer) RETURNS SETOF record AS 'filename', 'retcomposite' LANGUAGE C IMMUTABLE STRICT;
```

Observe que, nesse método, o tipo de saída da função é formalmente um tipo anônimo `record`.

### 36.10.10. Argumentos polimórficos e tipos de retorno [#](#XFUNC-C-POLYMORPHIC)

As funções em linguagem C podem ser declaradas para aceitar e retornar os tipos polimórficos descritos em [Seção 36.2.5](extend-type-system.md#EXTEND-TYPES-POLYMORPHIC). Quando os argumentos ou os tipos de retorno de uma função são definidos como tipos polimórficos, o autor da função não pode saber adiantadamente com que tipo de dados será chamada ou precisa retornar. Existem duas rotinas fornecidas em `fmgr.h` para permitir que uma função C de versão 1 descubra os tipos de dados reais de seus argumentos e o tipo que espera retornar. As rotinas são chamadas de `get_fn_expr_rettype(FmgrInfo *flinfo)` e `get_fn_expr_argtype(FmgrInfo *flinfo, int argnum)`. Retornam o tipo de resultado ou argumento OID, ou `InvalidOid` se a informação não estiver disponível. A estrutura `flinfo` é normalmente acessada como `fcinfo->flinfo`. O parâmetro `argnum` é baseado em zero. `get_call_result_type` também pode ser usado como uma alternativa a `get_fn_expr_rettype`. Há também `get_fn_expr_variadic`, que pode ser usado para determinar se argumentos variáveis foram mesclados em um array. Isso é principalmente útil para funções `VARIADIC "any"`, já que tal mesclagem sempre ocorrerá para funções variáveis que utilizam tipos de array comuns.

Por exemplo, suponha que queira escrever uma função que aceite um único elemento de qualquer tipo e retorne uma matriz unidimensional desse tipo:

```
PG_FUNCTION_INFO_V1(make_array); Datum make_array(PG_FUNCTION_ARGS) { ArrayType  *result; Oid         element_type = get_fn_expr_argtype(fcinfo->flinfo, 0); Datum       element; bool        isnull; int16       typlen; bool        typbyval; char        typalign; int         ndims; int         dims[MAXDIM]; int         lbs[MAXDIM];

    if (!OidIsValid(element_type)) elog(ERROR, "could not determine data type of input");

    /* get the provided element, being careful in case it's NULL */ isnull = PG_ARGISNULL(0); if (isnull) element = (Datum) 0; else element = PG_GETARG_DATUM(0);

    /* we have one dimension */ ndims = 1; /* and one element */ dims[0] = 1; /* and lower bound is 1 */ lbs[0] = 1;

    /* get required info about the element type */ get_typlenbyvalalign(element_type, &typlen, &typbyval, &typalign);

    /* now build the array */ result = construct_md_array(&element, &isnull, ndims, dims, lbs, element_type, typlen, typbyval, typalign);

    PG_RETURN_ARRAYTYPE_P(result); }
```

O comando a seguir declara a função `make_array` em SQL:

```
CREATE FUNCTION make_array(anyelement) RETURNS anyarray AS 'DIRECTORY/funcs', 'make_array' LANGUAGE C IMMUTABLE;
```

Existe uma variante de polimorfismo que só está disponível para funções em linguagem C: elas podem ser declaradas para receber parâmetros do tipo `"any"`. (Observe que esse nome de tipo deve ser colocado entre aspas duplas, pois também é uma palavra reservada do SQL.) Isso funciona como `anyelement`, exceto que não restringe que diferentes `"any"` argumentos sejam do mesmo tipo, nem ajudam a determinar o tipo do resultado da função. Uma função em linguagem C também pode declarar seu parâmetro final como `VARIADIC "any"`. Isso corresponderá a um ou mais argumentos reais de qualquer tipo (não necessariamente do mesmo tipo). Esses argumentos *não* serão reunidos em um array, como acontece com funções variáveis normais; eles serão simplesmente passados para a função separadamente. O `PG_NARGS()` macro e os métodos descritos acima devem ser usados para determinar o número de argumentos reais e seus tipos ao usar essa funcionalidade. Além disso, os usuários dessa função podem desejar usar a palavra-chave `VARIADIC` em sua chamada de função, com a expectativa de que a função trate os elementos da matriz como argumentos separados. A própria função deve implementar esse comportamento se desejado, após usar `get_fn_expr_variadic` para detectar que o argumento real foi marcado com `VARIADIC`.

### 36.10.11. Memória compartilhada [#](#XFUNC-SHARED-ADDIN)

#### 36.10.11.1. Solicitação de Memória Compartilhada na Inicialização [#](#XFUNC-SHARED-ADDIN-AT-STARTUP)

Os complementos podem reservar memória compartilhada no início do servidor. Para isso, a biblioteca compartilhada do complemento deve ser pré-carregada, especificando-a em [shared_preload_libraries](runtime-config-client.md#GUC-SHARED-PRELOAD-LIBRARIES). A biblioteca compartilhada também deve registrar um `shmem_request_hook` em sua `_PG_init` função. Este `shmem_request_hook` pode reservar memória compartilhada chamando:

```
void RequestAddinShmemSpace(Size size)
```

Cada backend deve obter um ponteiro para a memória compartilhada reservada chamando:

```
void *ShmemInitStruct(const char *name, Size size, bool *foundPtr)
```

Se essa função definir `foundPtr` para `false`, o chamador deve proceder à inicialização dos conteúdos da memória compartilhada reservada. Se `foundPtr` for definido para `true`, a memória compartilhada já foi inicializada por outro backend, e o chamador não precisa inicializar mais.

Para evitar condições de corrida, cada backend deve usar o LWLock ao inicializar sua alocação de memória compartilhada, como mostrado aqui:

```
static mystruct *ptr = NULL; bool        found;

LWLockAcquire(AddinShmemInitLock, LW_EXCLUSIVE); ptr = ShmemInitStruct("my struct name", size, &found); if (!found) { ... initialize contents of shared memory ... ptr->locks = GetNamedLWLockTranche("my tranche name"); } LWLockRelease(AddinShmemInitLock);
```

`shmem_startup_hook` fornece um local conveniente para o código de inicialização, mas não é estritamente necessário que todo esse código seja colocado neste gancho. Em Windows (e em qualquer outro lugar onde `EXEC_BACKEND` é definido), cada backend executa o `shmem_startup_hook` registrado logo após se conectar à memória compartilhada, portanto, os complementos ainda devem adquirir `AddinShmemInitLock` dentro deste gancho, como mostrado no exemplo acima. Em outras plataformas, apenas o processo postmaster executa o `shmem_startup_hook`, e cada backend herda automaticamente os ponteiros para a memória compartilhada.

Um exemplo de um `shmem_request_hook` e `shmem_startup_hook` pode ser encontrado em `contrib/pg_stat_statements/pg_stat_statements.c` em a árvore de código-fonte do PostgreSQL.

#### 36.10.11.2. Solicitação de Memória Compartilhada Após o Inicialização [#](#XFUNC-SHARED-ADDIN-AFTER-STARTUP)

Existe outro método mais flexível de reserva de memória compartilhada que pode ser feito após a inicialização do servidor e fora de um `shmem_request_hook`. Para isso, cada backend que utilizará a memória compartilhada deve obter um ponteiro para ela, chamando:

```
void *GetNamedDSMSegment(const char *name, size_t size, void (*init_callback) (void *ptr), bool *found)
```

Se um segmento de memória compartilhada dinâmica com o nome fornecido ainda não existir, esta função o alocará e o iniciará com a função de callback fornecida `init_callback`. Se o segmento já tiver sido alocado e iniciado por outro backend, esta função simplesmente anexa o segmento de memória compartilhada dinâmica existente ao backend atual.

Ao contrário da memória compartilhada reservada no início do servidor, não é necessário adquirir `AddinShmemInitLock` ou tomar outras ações para evitar condições de corrida ao reservar memória compartilhada com `GetNamedDSMSegment`. Esta função garante que apenas um backend aloque e inicie o segmento e que todos os outros backends recebam um ponteiro para o segmento totalmente alocado e inicializado.

Um exemplo completo de uso de `GetNamedDSMSegment` pode ser encontrado em `src/test/modules/test_dsm_registry/test_dsm_registry.c` na árvore de código-fonte do PostgreSQL.

### 36.10.12. LWLocks [#](#XFUNC-ADDIN-LWLOCKS)

#### 36.10.12.1. Solicitação de LWLocks na inicialização [#](#XFUNC-ADDIN-LWLOCKS-AT-STARTUP)

Os complementos podem reservar LWLocks no início da inicialização do servidor. Assim como a memória compartilhada reservada no início da inicialização do servidor, a biblioteca compartilhada do complemento deve ser pré-carregada, especificando-a em [shared_preload_libraries](runtime-config-client.md#GUC-SHARED-PRELOAD-LIBRARIES), e a biblioteca compartilhada deve registrar um `shmem_request_hook` em sua `_PG_init` função. Este `shmem_request_hook` pode reservar LWLocks chamando:

```
void RequestNamedLWLockTranche(const char *tranche_name, int num_lwlocks)
```

Isso garante que uma matriz de `num_lwlocks` LWLocks esteja disponível sob o nome `tranche_name`. Um ponteiro para essa matriz pode ser obtido chamando:

```
LWLockPadded *GetNamedLWLockTranche(const char *tranche_name)
```

#### 36.10.12.2. Solicitação de LWLocks após o início do sistema [#](#XFUNC-ADDIN-LWLOCKS-AFTER-STARTUP)

Existe outro método mais flexível de obtenção de LWLocks que pode ser feito após a inicialização do servidor e fora de um `shmem_request_hook`. Para isso, aloque primeiro um `tranche_id` chamando:

```
int LWLockNewTrancheId(void)
```

Em seguida, inicialize cada LWLock, passando o novo `tranche_id` como um argumento:

```
void LWLockInitialize(LWLock *lock, int tranche_id)
```

Semelhante à memória compartilhada, cada backend deve garantir que apenas um processo aloque um novo `tranche_id` e inicie cada novo LWLock. Uma maneira de fazer isso é chamar essas funções apenas em seu código de inicialização da memória compartilhada com o `AddinShmemInitLock` mantido exclusivamente. Se estiver usando o `GetNamedDSMSegment`, chamar essas funções na função de callback `init_callback` é suficiente para evitar condições de corrida.

Por fim, cada backend que utilize o `tranche_id` deve associá-lo a um `tranche_name` chamando:

```
void LWLockRegisterTranche(int tranche_id, const char *tranche_name)
```

Um exemplo completo de uso de `LWLockNewTrancheId`, `LWLockInitialize` e `LWLockRegisterTranche` pode ser encontrado em `contrib/pg_prewarm/autoprewarm.c` na árvore de código-fonte do PostgreSQL.

### 36.10.13. Eventos de espera personalizados [#](#XFUNC-ADDIN-WAIT-EVENTS)

Os complementos podem definir eventos de espera personalizados sob o tipo de evento de espera `Extension` chamando:

```
uint32 WaitEventExtensionNew(const char *wait_event_name)
```

O evento de espera está associado a uma string personalizada voltada para o usuário. Um exemplo pode ser encontrado em `src/test/modules/worker_spi` no repositório de código-fonte do PostgreSQL.

Eventos de espera personalizados podem ser visualizados em `pg_stat_activity`(monitoring-stats.md#MONITORING-PG-STAT-ACTIVITY-VIEW "27.2.3. pg_stat_activity"):

```
=# SELECT wait_event_type, wait_event FROM pg_stat_activity WHERE backend_type ~ 'worker_spi'; wait_event_type |  wait_event -----------------+--------------- Extension       | WorkerSpiMain (1 row)
```

### 36.10.14. Pontos de Injeção [#](#XFUNC-ADDIN-INJECTION-POINTS)

Um ponto de injeção com um `name` dado é declarado usando a macro:

```
INJECTION_POINT(name, arg);
```

Existem alguns pontos de injeção já declarados em pontos estratégicos dentro do código do servidor. Após adicionar um novo ponto de injeção, o código precisa ser compilado para que esse ponto de injeção esteja disponível no binário. Os complementos escritos em linguagem C podem declarar pontos de injeção em seu próprio código usando a mesma macro. Os nomes dos pontos de injeção devem usar caracteres minúsculos, com termos separados por traços. `arg` é um valor de argumento opcional dado ao callback em tempo de execução.

Executar um ponto de injeção pode exigir a alocação de uma pequena quantidade de memória, o que pode falhar. Se você precisa ter um ponto de injeção em uma seção crítica onde alocações dinâmicas não são permitidas, você pode usar uma abordagem de dois passos com as seguintes macros:

```
INJECTION_POINT_LOAD(name); INJECTION_POINT_CACHED(name, arg);
```

Antes de entrar na seção crítica, chame `INJECTION_POINT_LOAD`. Ele verifica o estado da memória compartilhada e carrega o callback na memória privada do backend, se estiver ativo. Dentro da seção crítica, use `INJECTION_POINT_CACHED` para executar o callback.

Os complementos podem anexar callbacks a um ponto de injeção já declarado chamando:

```
extern void InjectionPointAttach(const char *name, const char *library, const char *function, const void *private_data, int private_data_size);
```

`name` é o nome do ponto de injeção, que, quando alcançado durante a execução, executará o `function` carregado a partir de `library`. `private_data` é uma área privada de dados com tamanho `private_data_size` fornecido como argumento ao callback quando executado.

Aqui está um exemplo de callback para `InjectionPointCallback`:

```
static void custom_injection_callback(const char *name, const void *private_data, void *arg) { uint32 wait_event_info = WaitEventInjectionPointNew(name);

    pgstat_report_wait_start(wait_event_info); elog(NOTICE, "%s: executed custom callback", name); pgstat_report_wait_end(); }
```

Este callback imprime uma mensagem no log de erro do servidor com a gravidade `NOTICE`, mas os callbacks podem implementar uma lógica mais complexa.

Uma maneira alternativa de definir a ação a ser tomada quando um ponto de injeção é atingido é adicionar o código de teste ao lado do código fonte normal. Isso pode ser útil se a ação, por exemplo, depende de variáveis locais que não são acessíveis aos módulos carregados. O `IS_INJECTION_POINT_ATTACHED` macro pode então ser usado para verificar se um ponto de injeção está anexado, por exemplo:

```
#ifdef USE_INJECTION_POINTS
if (IS_INJECTION_POINT_ATTACHED("before-foobar")) { /* change a local variable if injection point is attached */ local_var = 123;

    /* also execute the callback */ INJECTION_POINT_CACHED("before-foobar", NULL); }
#endif
```

Observe que o callback anexado ao ponto de injeção não será executado pelo macro `IS_INJECTION_POINT_ATTACHED`. Se você deseja executar o callback, também deve chamar `INJECTION_POINT_CACHED`, como no exemplo acima.

Opcionalmente, é possível deslocar um ponto de injeção chamando:

```
extern bool InjectionPointDetach(const char *name);
```

Em caso de sucesso, `true` é retornado, caso contrário, [[`false`].

Um callback vinculado a um ponto de injeção está disponível em todos os backends, incluindo os backends iniciados após a chamada de `InjectionPointAttach`. Ele permanece vinculado enquanto o servidor estiver em execução ou até que o ponto de injeção seja desvinculado usando `InjectionPointDetach`.

Um exemplo pode ser encontrado em `src/test/modules/injection_points` na árvore de origem do PostgreSQL.

Para habilitar os pontos de injeção, é necessário o `--enable-injection-points` com `configure` ou `-Dinjection_points=true` com o Meson.

### 36.10.15. Estatísticas cumulativas personalizadas [#](#XFUNC-ADDIN-CUSTOM-CUMULATIVE-STATISTICS)

É possível que complementos escritos em linguagem C utilizem tipos personalizados de estatísticas acumuladas registrados no [Sistema de Estatísticas Acumuladas](monitoring-stats.md#MONITORING-STATS-SETUP).

Primeiro, defina um `PgStat_KindInfo` que inclua todas as informações relacionadas ao tipo personalizado registrado. Por exemplo:

```
static const PgStat_KindInfo custom_stats = { .name = "custom_stats", .fixed_amount = false, .shared_size = sizeof(PgStatShared_Custom), .shared_data_off = offsetof(PgStatShared_Custom, stats), .shared_data_len = sizeof(((PgStatShared_Custom *) 0)->stats), .pending_size = sizeof(PgStat_StatCustomEntry), }
```

Em seguida, cada backend que precise usar esse tipo personalizado precisa registrá-lo com `pgstat_register_kind` e um ID único usado para armazenar as entradas relacionadas a esse tipo de estatísticas:

```
extern PgStat_Kind pgstat_register_kind(PgStat_Kind kind, const PgStat_KindInfo *kind_info);
```

Ao desenvolver uma nova extensão, use `PGSTAT_KIND_EXPERIMENTAL` para *`kind`*. Quando estiver pronto para liberar a extensão para os usuários, reserve um ID amigável na página [Estatísticas cumulativas personalizadas](https://wiki.postgresql.org/wiki/CustomCumulativeStats).

Os detalhes da API para `PgStat_KindInfo` podem ser encontrados em `src/include/utils/pgstat_internal.h`.

O tipo de estatísticas registrado está associado a um nome e a um ID único compartilhado em todo o servidor na memória compartilhada. Cada backend que utiliza um tipo personalizado de estatísticas mantém um cache local que armazena as informações de cada `PgStat_KindInfo` personalizado.

Coloque o módulo de extensão que implementa as estatísticas cumulativas personalizadas no [shared_preload_libraries](runtime-config-client.md#GUC-SHARED-PRELOAD-LIBRARIES) para que ele seja carregado cedo durante o início do PostgreSQL.

Um exemplo que descreve como registrar e usar estatísticas personalizadas pode ser encontrado em `src/test/modules/injection_points`.

### 36.10.16. Uso do C++ para Extensibilidade [#](#EXTEND-CPP)

Embora o backend do PostgreSQL seja escrito em C, é possível escrever extensões em C++, desde que essas diretrizes sejam seguidas:

* Todas as funções acessadas pelo backend devem apresentar uma interface C para o backend; essas funções em C podem então chamar funções em C++. Por exemplo, a vinculação `extern C` é necessária para funções acessadas pelo backend. Isso também é necessário para quaisquer funções que sejam passadas como ponteiros entre o backend e o código em C++.
* Lembre-se de liberar a memória usando o método apropriado de alocação. Por exemplo, a maioria da memória do backend é alocada usando `palloc()`, então use `pfree()` para liberá-la. Usar C++ `delete` nesses casos falhará.
* Impedir que exceções se propague para o código em C (use um bloco de captura geral no nível superior de todas as funções `extern C`). Isso é necessário mesmo que o código em C++ não arraste explicitamente quaisquer exceções, porque eventos como falta de memória ainda podem lançar exceções. Qualquer exceção deve ser capturada e erros apropriados devem ser passados de volta para a interface em C. Se possível, compile o C++ com `-fno-exceptions` para eliminar exceções completamente; nesses casos, você deve verificar por falhas no seu código em C++, por exemplo, verificar o NULL retornado por `new()`.
* Se estiver chamando funções do backend a partir do código em C++, certifique-se de que a pilha de chamadas do C++ contenha apenas estruturas de dados simples e antigas (POD). Isso é necessário porque os erros do backend geram um `longjmp()` distante que não desenrola adequadamente uma pilha de chamadas em C++ com objetos não-POD.

Em resumo, é melhor colocar o código em C++ atrás de uma parede de funções que interagem com o backend, e evitar exceções, vazamento de memória e vazamento de pilha de chamadas.