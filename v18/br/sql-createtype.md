## Crie o tipo

Crie tipo — defina um novo tipo de dados

## Sinopse

```
CREATE TYPE name AS
    ( [ attribute_name data_type [ COLLATE collation ] [, ... ] ] )

CREATE TYPE name AS ENUM
    ( [ 'label' [, ... ] ] )

CREATE TYPE name AS RANGE (
    SUBTYPE = subtype
    [ , SUBTYPE_OPCLASS = subtype_operator_class ]
    [ , COLLATION = collation ]
    [ , CANONICAL = canonical_function ]
    [ , SUBTYPE_DIFF = subtype_diff_function ]
    [ , MULTIRANGE_TYPE_NAME = multirange_type_name ]
)

CREATE TYPE name (
    INPUT = input_function,
    OUTPUT = output_function
    [ , RECEIVE = receive_function ]
    [ , SEND = send_function ]
    [ , TYPMOD_IN = type_modifier_input_function ]
    [ , TYPMOD_OUT = type_modifier_output_function ]
    [ , ANALYZE = analyze_function ]
    [ , SUBSCRIPT = subscript_function ]
    [ , INTERNALLENGTH = { internallength | VARIABLE } ]
    [ , PASSEDBYVALUE ]
    [ , ALIGNMENT = alignment ]
    [ , STORAGE = storage ]
    [ , LIKE = like_type ]
    [ , CATEGORY = category ]
    [ , PREFERRED = preferred ]
    [ , DEFAULT = default ]
    [ , ELEMENT = element ]
    [ , DELIMITER = delimiter ]
    [ , COLLATABLE = collatable ]
)

CREATE TYPE name
```

## Descrição

`CREATE TYPE` registra um novo tipo de dados para uso no banco de dados atual. O usuário que define um tipo torna-se seu proprietário.

Se um nome de esquema for fornecido, o tipo é criado no esquema especificado. Caso contrário, é criado no esquema atual. O nome do tipo deve ser distinto do nome de qualquer tipo ou domínio existente no mesmo esquema. (Como as tabelas têm tipos de dados associados, o nome do tipo também deve ser distinto do nome de qualquer tabela existente no mesmo esquema.)

Existem cinco formas de `CREATE TYPE`, conforme mostrado no resumo de sintaxe acima. Elas, respectivamente, criam um *tipo composto*, um *tipo enum*, um *tipo de intervalo*, um *tipo de base* ou um *tipo de concha*. As quatro primeiras dessas são discutidas em ordem abaixo. Um tipo de concha é simplesmente um localizador para um tipo a ser definido mais tarde; ele é criado emitindo `CREATE TYPE` sem parâmetros, exceto pelo nome do tipo. Os tipos de concha são necessários como referências para a frente ao criar tipos de intervalo e tipos de base, conforme discutido nessas seções.

### Tipos compostos

A primeira forma de `CREATE TYPE` cria um tipo composto. O tipo composto é especificado por uma lista de nomes de atributos e tipos de dados. Também é possível especificar a collation de um atributo, se seu tipo de dados for colidível. Um tipo composto é essencialmente o mesmo que o tipo de linha de uma tabela, mas usando `CREATE TYPE` evita a necessidade de criar uma tabela real quando tudo o que se deseja é definir um tipo. Um tipo composto autônomo é útil, por exemplo, como o tipo de argumento ou retorno de uma função.

Para poder criar um tipo composto, você deve ter o privilégio `USAGE` em todos os tipos de atributos.

### Tipos enumerados

A segunda forma de `CREATE TYPE` cria um tipo enumerado (enum), conforme descrito em [Seção 8.7](datatype-enum.md "8.7. Enumerated Types"). Os tipos enumerados levam uma lista de rótulos citados, cada um dos quais deve ter menos de `NAMEDATALEN` bytes de comprimento (64 bytes em uma versão padrão do PostgreSQL). (É possível criar um tipo enumerado com zero rótulos, mas tal tipo não pode ser usado para armazenar valores antes de pelo menos um rótulo ser adicionado usando [`ALTER TYPE`](sql-altertype.md "ALTER TYPE").))

### Tipos de Gama

A terceira forma de `CREATE TYPE` cria um novo tipo de intervalo, conforme descrito na [Seção 8.17][(rangetypes.md "8.17. Range Types")].

O tipo de intervalo *`subtype`* pode ser qualquer tipo com uma classe de operador de árvore b associada (para determinar a ordem dos valores para o tipo de intervalo). Normalmente, a classe de operador de árvore b padrão do subtipo é usada para determinar a ordem; para usar uma classe de operador não padrão, especifique seu nome com *`subtype_opclass`*. Se o subtipo é coletável e você deseja usar uma collation não padrão na ordem do intervalo, especifique a collation desejada com a opção *`collation`*.

A função opcional *`canonical`* deve receber um argumento do tipo de intervalo que está sendo definido e retornar um valor do mesmo tipo. Isso é usado para converter os valores do intervalo em uma forma canônica, quando aplicável. Consulte [Seção 8.17.8][(rangetypes.md#RANGETYPES-DEFINING "8.17.8. Defining New Range Types")] para obter mais informações. Criar uma função *`canonical`* é um pouco complicado, pois ela deve ser definida antes que o tipo de intervalo possa ser declarado. Para fazer isso, você deve primeiro criar um tipo de concha, que é um tipo de marcador que não tem propriedades, exceto um nome e um proprietário. Isso é feito emitindo o comando `CREATE TYPE name`, sem parâmetros adicionais. Em seguida, a função pode ser declarada usando o tipo de concha como argumento e resultado, e, finalmente, o tipo de intervalo pode ser declarado usando o mesmo nome. Isso substitui automaticamente a entrada do tipo de concha por um tipo de intervalo válido.

A função opcional *`subtype_diff`* deve receber dois valores do tipo *`subtype`* como argumento e retornar um valor de `double precision` que representa a diferença entre os dois valores fornecidos. Embora seja opcional, fornecê-la permite uma muito maior eficiência dos índices GiST em colunas do tipo de intervalo. Consulte [Seção 8.17.8][(rangetypes.md#RANGETYPES-DEFINING "8.17.8. Defining New Range Types")] para obter mais informações.

O parâmetro opcional *`multirange_type_name`* especifica o nome do tipo de multiintervalo correspondente. Se não especificado, esse nome é escolhido automaticamente da seguinte forma. Se o nome do tipo de intervalo contiver a subcadeia `range`, então o nome do tipo de multiintervalo é formado pela substituição da subcadeia `range` pela `multirange` no nome do tipo de intervalo. Caso contrário, o nome do tipo de multiintervalo é formado pela adição de um sufixo `_multirange` ao nome do tipo de intervalo.

### Tipos de Base

A quarta forma de `CREATE TYPE` cria um novo tipo de base (tipo escalar). Para criar um novo tipo de base, você deve ser um superusuário. (Essa restrição é feita porque uma definição de tipo errada pode confundir ou até mesmo fazer o servidor falhar.)

Os parâmetros podem aparecer em qualquer ordem, não apenas aquela ilustrada acima, e a maioria é opcional. Você deve registrar duas ou mais funções (usando `CREATE FUNCTION`) antes de definir o tipo. As funções de suporte *`input_function`* e *`output_function`* são necessárias, enquanto as funções *`receive_function`*, *`send_function`*, *`type_modifier_input_function`*, *`type_modifier_output_function`*, *`analyze_function`* e *`subscript_function`* são opcionais. Geralmente, essas funções devem ser codificadas em C ou em outro idioma de baixo nível.

O *`input_function` converte a representação textual externa do tipo para a representação interna usada pelos operadores e funções definidas para o tipo. *`output_function` realiza a transformação inversa. A função de entrada pode ser declarada como aceitando um argumento do tipo `cstring`, ou como aceitando três argumentos dos tipos `cstring`, `oid`, `integer`. O primeiro argumento é o texto de entrada como uma string em C, o segundo argumento é o próprio OID do tipo (exceto para tipos de matriz, que em vez disso recebem o OID do tipo de elemento, e o terceiro é o `typmod` da coluna de destino, se conhecido (-1 será passado se não for o caso). A função de entrada deve retornar um valor do próprio tipo de dados. Normalmente, uma função de entrada deve ser declarada STRICT; se não for, será chamada com um parâmetro primeiro NULL ao ler um valor de entrada NULL. A função ainda deve retornar NULL neste caso, a menos que ele cause um erro. (Este caso é principalmente destinado a suportar funções de entrada de domínio, que podem precisar rejeitar entradas NULL.) A função de saída deve ser declarada como aceitando um argumento do novo tipo de dados. A função de saída deve retornar o tipo `cstring`. As funções de saída não são invocadas para valores NULL.

O opcional *`receive_function`* converte a representação binária externa do tipo para a representação interna. Se esta função não for fornecida, o tipo não pode participar na entrada binária. A representação binária deve ser escolhida para ser barata de converter para a forma interna, sendo ao mesmo tempo razoavelmente portátil. (Por exemplo, os tipos de dados inteiros padrão usam a ordem de bytes da rede como a representação binária externa, enquanto a representação interna é na ordem de bytes nativa da máquina.) A função de recebimento deve realizar verificações adequadas para garantir que o valor seja válido. A função de recebimento pode ser declarada como aceitando um argumento do tipo `internal`, ou como aceitando três argumentos dos tipos `internal`, `oid`, `integer`. O primeiro argumento é um ponteiro para um buffer `StringInfo` que contém a string de bytes recebida; os argumentos opcionais são os mesmos que para a função de entrada de texto. A função de recebimento deve retornar um valor do próprio tipo de dados. Normalmente, uma função de recebimento deve ser declarada STRICT; se não for, ela será chamada com um primeiro parâmetro NULL ao ler um valor de entrada NULL. A função ainda deve retornar NULL neste caso, a menos que ela cause um erro. (Este caso é principalmente destinado a suportar funções de recebimento de domínio, que podem precisar rejeitar entradas NULL.) Da mesma forma, o opcional *`send_function`* converte da representação interna para a representação binária externa. Se esta função não for fornecida, o tipo não pode participar na saída binária. A função de envio deve ser declarada como aceitando um argumento do novo tipo de dados. A função de envio deve retornar o tipo `bytea`. As funções de envio não são invocadas para valores NULL.

Neste ponto, você deve estar se perguntando como as funções de entrada e saída podem ser declaradas para ter resultados ou argumentos do novo tipo, quando elas precisam ser criadas antes que o novo tipo possa ser criado. A resposta é que o tipo deve ser definido primeiro como um *tipo de shell*, que é um tipo de marcador que não tem propriedades, exceto um nome e um proprietário. Isso é feito emitindo o comando `CREATE TYPE name`, sem parâmetros adicionais. Em seguida, as funções de E/S C podem ser definidas, referenciando o tipo de shell. Finalmente, `CREATE TYPE` com uma definição completa substitui a entrada de shell por uma definição de tipo completa e válida, após o que o novo tipo pode ser usado normalmente.

Os opcionais *`type_modifier_input_function`* e *`type_modifier_output_function`* são necessários se o tipo suportar modificadores, ou seja, restrições opcionais anexadas a uma declaração de tipo, como `char(5)` ou `numeric(30,2)`. O PostgreSQL permite que tipos definidos pelo usuário levem uma ou mais constantes simples ou identificadores como modificadores. No entanto, essas informações devem ser capazes de ser embaladas em um único valor inteiro não negativo para armazenamento nos catálogos do sistema. O *`type_modifier_input_function`* recebe os modificadores declarados na forma de um `cstring` array. Ele deve verificar os valores quanto à validade (lançando um erro se estiver errado), e se estiver correto, retornar um único valor inteiro não negativo `integer` que será armazenado como a coluna “typmod”. Os modificadores de tipo serão rejeitados se o tipo não tiver um *`type_modifier_input_function`*. O *`type_modifier_output_function`* converte o valor inteiro interno typmod de volta à forma correta para exibição pelo usuário. Ele deve retornar um valor `cstring` que é a string exata a ser anexada ao nome do tipo; por exemplo, a função do `numeric` pode retornar `(30,2)`. É permitido omitir o *`type_modifier_output_function`*, no caso, o formato de exibição padrão é apenas o valor inteiro typmod armazenado entre parênteses.

O opcional *`analyze_function`* realiza a coleta de estatísticas específicas para tipos de colunas do tipo de dados. Por padrão, `ANALYZE` tentará coletar estatísticas usando os operadores “igual” e “menor que” do tipo, se houver uma classe de operador de árvore b padrão para o tipo. Para tipos não escalares, esse comportamento provavelmente será inadequado, portanto, pode ser sobrescrito especificando uma função de análise personalizada. A função de análise deve ser declarada para receber um único argumento do tipo `internal` e retornar um resultado `boolean`. A API detalhada para funções de análise aparece em `src/include/commands/vacuum.h`.

O opcional *`subscript_function`* permite que o tipo de dados seja subscrito em comandos SQL. Especificar essa função não faz com que o tipo seja considerado um tipo de matriz “verdadeiro”; por exemplo, não será um candidato ao tipo de resultado dos construtos `ARRAY[]`. Mas se a subscrita de um valor do tipo é uma notação natural para extrair dados dele, então um *`subscript_function`* pode ser escrito para definir o que isso significa. A função de subscrito deve ser declarada para receber um único argumento do tipo `internal` e retornar um resultado `internal`, que é um ponteiro para uma estrutura de métodos (funções) que implementam a subscrita. A API detalhada para funções de subscrita aparece em `src/include/nodes/subscripting.h`. Também pode ser útil ler a implementação da matriz em `src/backend/utils/adt/arraysubs.c`, ou o código mais simples em `contrib/hstore/hstore_subs.c`. Informações adicionais aparecem em [Tipos de matriz](sql-createtype.md#SQL-CREATETYPE-ARRAY "Array Types") abaixo.

Embora os detalhes da representação interna do novo tipo sejam conhecidos apenas pelas funções de entrada/saída e outras funções que você cria para trabalhar com o tipo, há várias propriedades da representação interna que devem ser declaradas ao PostgreSQL. A principal delas é *`internallength`*. Os tipos de dados básicos podem ter comprimento fixo, no caso, *`internallength`* é um inteiro positivo, ou podem ter comprimento variável, indicado ao definir *`internallength`* para `VARIABLE`. (Internacionalmente, isso é representado ao definir `typlen` para -1.) A representação interna de todos os tipos de comprimento variável deve começar com um inteiro de 4 bytes que dá o comprimento total desse valor do tipo. (Observe que o campo de comprimento é frequentemente codificado, conforme descrito em [Seção 66.2][(storage-toast.md "66.2. TOAST")]; não é aconselhável acessá-lo diretamente.)

A bandeira opcional `PASSEDBYVALUE` indica que os valores deste tipo de dados são passados por valor, em vez de por referência. Os tipos passados por valor devem ter comprimento fixo, e sua representação interna não pode ser maior que o tamanho do tipo `Datum` (4 bytes em algumas máquinas, 8 bytes em outras).

O parâmetro *`alignment` especifica o alinhamento de armazenamento necessário para o tipo de dados. Os valores permitidos correspondem ao alinhamento em limites de 1, 2, 4 ou 8 bytes. Observe que os tipos de comprimento variável devem ter um alinhamento de pelo menos 4, uma vez que eles necessariamente contêm um `int4` como seu primeiro componente.

O parâmetro *`storage` permite a seleção de estratégias de armazenamento para tipos de dados de comprimento variável. (Apenas `plain` é permitido para tipos de comprimento fixo.) `plain` especifica que os dados do tipo serão sempre armazenados em linha e não comprimidos. `extended` especifica que o sistema tentará primeiro comprimir um valor de dados longo e moverá o valor fora da linha da tabela principal se ainda assim for muito longo. `external` permite que o valor seja movido fora da tabela principal, mas o sistema não tentará comprimí-lo. `main` permite a compressão, mas desencoraja a movimentação do valor fora da tabela principal. (Os itens de dados com essa estratégia de armazenamento ainda podem ser movidos fora da tabela principal se não houver outra maneira de ajustar a linha, mas serão mantidos na tabela principal preferencialmente em relação aos itens de `extended` e `external`.)

Todos os valores *`storage` que não sejam `plain` implicam que as funções do tipo de dados podem lidar com valores que foram *toasteados*, conforme descrito em [Seção 66.2][(storage-toast.md "66.2. TOAST") e [Seção 36.13.1][(xtypes.md#XTYPES-TOAST "36.13.1. TOAST Considerations")]. O valor específico dado simplesmente determina a estratégia de armazenamento TOAST padrão para colunas de um tipo de dados toasteável; os usuários podem escolher outras estratégias para colunas individuais usando `ALTER TABLE SET STORAGE`.

O parâmetro *`like_type` fornece um método alternativo para especificar as propriedades de representação básica de um tipo de dados: copí-las de algum tipo existente. Os valores de *`internallength`*, *`passedbyvalue`*, *`alignment`* e *`storage`* são copiados do tipo nomeado. (É possível, embora geralmente indesejável, sobrescrever alguns desses valores, especificando-os juntamente com a cláusula `LIKE`. Especificar a representação dessa maneira é especialmente útil quando a implementação de nível baixo do novo tipo “pega empurrando” em algum modo em um tipo existente.

Os parâmetros *`category`* e *`preferred`* podem ser usados para ajudar a controlar qual o tipo de cast implícito será aplicado em situações ambíguas. Cada tipo de dado pertence a uma categoria nomeada por um único caractere ASCII, e cada tipo é ou “preferido” ou não dentro de sua categoria. O analisador preferirá o cast para tipos preferidos (mas apenas de outros tipos dentro da mesma categoria) quando essa regra seja útil na resolução de funções ou operadores sobrecarregados. Para mais detalhes, consulte [Capítulo 10][(typeconv.md "Chapter 10. Type Conversion")]. Para tipos que não têm casts implícitos para ou de outros tipos, é suficiente deixar esses ajustes nos padrões. No entanto, para um grupo de tipos relacionados que têm casts implícitos, muitas vezes é útil marcar todos eles como pertencentes a uma categoria e selecionar um ou dois dos tipos “mais gerais” como sendo preferidos dentro da categoria. O parâmetro *`category`* é especialmente útil ao adicionar um tipo definido pelo usuário a uma categoria pré-existente, como os tipos numéricos ou de string. No entanto, também é possível criar novas categorias de tipos totalmente definidas pelo usuário. Selecione qualquer caractere ASCII diferente de uma letra maiúscula para nomear tal categoria.

Um valor padrão pode ser especificado, no caso de um usuário desejar que as colunas do tipo de dados tenham um valor padrão diferente do valor nulo. Especifique o padrão com a palavra-chave `DEFAULT`. (Tal padrão pode ser sobrescrito por uma cláusula explícita `DEFAULT` anexada a uma coluna específica.)

Para indicar que um tipo é um tipo de matriz de comprimento fixo, especifique o tipo dos elementos da matriz usando a palavra-chave `ELEMENT`. Por exemplo, para definir uma matriz de inteiros de 4 bytes (`int4`, especifique `ELEMENT = int4`. Para mais detalhes, consulte [Tipos de matriz](sql-createtype.md#SQL-CREATETYPE-ARRAY "Array Types") abaixo.

Para indicar o delimitador a ser usado entre os valores na representação externa de arrays deste tipo, *`delimiter`* pode ser definido como um caractere específico. O delimitador padrão é a vírgula (`,`). Observe que o delimitador está associado ao tipo do elemento do array, não ao próprio tipo do array.

Se o parâmetro booleano opcional *`collatable`* for verdadeiro, as definições de coluna e as expressões do tipo podem carregar informações de ordenação por meio do uso da cláusula `COLLATE`. Cabe às implementações das funções que operam sobre o tipo fazer uso efetivo das informações de ordenação; isso não acontece automaticamente apenas ao marcar o tipo como colidível.

### Tipos de Array

Sempre que um tipo definido pelo usuário é criado, o PostgreSQL automaticamente cria um tipo de matriz associado, cujo nome consiste no nome do tipo de elemento preenchido com uma sublinhado, e é truncado, se necessário, para mantê-lo com menos de `NAMEDATALEN` bytes de comprimento. (Se o nome gerado em colisão com um nome de tipo existente, o processo é repetido até que um nome não colidir seja encontrado.) Este tipo de matriz criado implicitamente é de comprimento variável e usa as funções de entrada e saída internas `array_in` e `array_out`. Além disso, este tipo é o que o sistema usa para construções como `ARRAY[]` sobre o tipo definido pelo usuário. O tipo de matriz acompanha quaisquer mudanças no tipo de elemento do proprietário ou esquema, e é descartado se o tipo de elemento for.

Você pode razoavelmente perguntar por que existe uma opção `ELEMENT`, se o sistema faz o tipo de matriz correta automaticamente. O caso principal em que é útil usar `ELEMENT` é quando você está criando um tipo de comprimento fixo que, internamente, é uma matriz de um número de coisas idênticas, e você quer permitir que essas coisas sejam acessadas diretamente por subscrito, além das operações que você planeja fornecer para o tipo como um todo. Por exemplo, o tipo `point` é representado como apenas dois números de ponto flutuante, que podem ser acessados usando `point[0]` e `point[1]`. Note que essa facilidade só funciona para tipos de comprimento fixo cuja forma interna é exatamente uma sequência de campos de comprimento fixo idênticos. Por razões históricas (ou seja, isso é claramente errado, mas é tarde demais para mudar), a subscrita de tipos de matriz de comprimento fixo começa de zero, em vez de de um, como para arrays de comprimento variável.

Especificar a opção `SUBSCRIPT` permite que um tipo de dados seja subscrito, mesmo que o sistema não o considere, de outra forma, como um tipo de matriz. O comportamento descrito anteriormente para matrizes de comprimento fixo é, na verdade, implementado pela função de manipulador `SUBSCRIPT` `raw_array_subscript_handler`, que é usada automaticamente se você especificar `ELEMENT` para um tipo de comprimento fixo sem também escrever `SUBSCRIPT`.

Ao especificar uma função personalizada `SUBSCRIPT`, não é necessário especificar `ELEMENT`, a menos que a função de manipulador `SUBSCRIPT` precise consultar `typelem` para descobrir o que deve retornar. Esteja ciente de que especificar `ELEMENT` faz com que o sistema assuma que o novo tipo contém ou está de alguma forma fisicamente dependente do tipo de elemento; portanto, por exemplo, não será permitido alterar as propriedades do tipo de elemento se houver quaisquer colunas do tipo dependente.

## Parâmetros

*`name`*: O nome (opcionalmente qualificado por esquema) de um tipo a ser criado.

*`attribute_name`*: O nome de um atributo (coluna) para o tipo composto.

*`data_type`*: O nome de um tipo de dados existente que se tornará uma coluna do tipo composto.

*`collation`*: O nome de uma correção existente a ser associada a uma coluna de um tipo composto, ou a um tipo de intervalo.

*`label`*: Uma literal de cadeia que representa o rótulo textual associado a um valor de um tipo de enumeração.

*`subtype`*: O nome do tipo de elemento que o tipo de intervalo representará.

*`subtype_operator_class`*: O nome de uma classe de operador de árvore em forma de "b" para o subtipo.

*`canonical_function`*: O nome da função de canonicização para o tipo de intervalo.

*`subtype_diff_function`*: O nome de uma função de diferença para o subtipo.

*`multirange_type_name`*: O nome do tipo correspondente de multi-range.

*`input_function`*: O nome de uma função que converte dados da forma textual externa do tipo para sua forma interna.

*`output_function`*: O nome de uma função que converte dados da forma interna do tipo para sua forma textual externa.

*`receive_function`*: O nome de uma função que converte dados da forma binária externa do tipo para sua forma interna.

*`send_function`*: O nome de uma função que converte dados da forma interna do tipo para sua forma binária externa.

*`type_modifier_input_function`*: O nome de uma função que converte um(s) conjunto(s) de modificador(es) para o tipo em forma interna.

*`type_modifier_output_function`*: O nome de uma função que converte a forma interna do(s) modificador(es) do tipo para a forma textual externa.

*`analyze_function`*: O nome de uma função que realiza análise estatística para o tipo de dados.

*`subscript_function`*: O nome de uma função que define o que significa subscrito um valor do tipo de dados.

*`internallength`*: Uma constante numérica que especifica o comprimento em bytes da representação interna do novo tipo. A suposição padrão é que ela é de comprimento variável.

*`alignment`*: O requisito de alinhamento de armazenamento do tipo de dado. Se especificado, deve ser `char`, `int2`, `int4` ou `double`; o padrão é `int4`.

*`storage`*: A estratégia de armazenamento para o tipo de dados. Se especificado, deve ser `plain`, `external`, `extended` ou `main`; o padrão é `plain`.

*`like_type`*: O nome de um tipo de dados existente que o novo tipo terá a mesma representação. Os valores de *`internallength`*, *`passedbyvalue`*, *`alignment`* e *`storage`* são copiados desse tipo, a menos que sejam especificados explicitamente em outro lugar neste comando *`CREATE TYPE`*.

*`category`*: O código da categoria (um único caractere ASCII) para este tipo. O padrão é `'U'` para "tipo definido pelo usuário". Outros códigos padrão de categoria podem ser encontrados em [Tabela 52.65][(catalog-pg-type.md#CATALOG-TYPCATEGORY-TABLE "Table 52.65. typcategory Codes")]. Você também pode escolher outros caracteres ASCII para criar categorias personalizadas.

*`preferred`*: Verdadeiro se este tipo é um tipo preferido dentro de sua categoria de tipo, caso contrário, falso. O padrão é falso. Tenha muito cuidado ao criar um novo tipo preferido dentro de uma categoria de tipo existente, pois isso pode causar mudanças surpreendentes no comportamento.

*`default`*: O valor padrão para o tipo de dados. Se este for omitido, o padrão é nulo.

*`element`*: O tipo que está sendo criado é um array; isso especifica o tipo dos elementos do array.

*`delimiter`*: O caractere delimitador a ser utilizado entre os valores em arrays feitos deste tipo.

*`collatable`*: Verdadeiro se as operações deste tipo podem usar informações de colagem. O padrão é falso.

## Notas

Como não há restrições sobre o uso de um tipo de dados uma vez que ele tenha sido criado, criar um tipo de base ou um tipo de intervalo equivale a conceder permissão de execução pública nas funções mencionadas na definição do tipo. Geralmente, isso não é um problema para os tipos de funções que são úteis em uma definição de tipo. Mas você pode querer pensar duas vezes antes de projetar um tipo de uma maneira que exija que informações "secretas" sejam usadas ao convertê-lo para ou a partir de um formato externo.

Antes da versão 8.3 do PostgreSQL, o nome de um tipo de matriz gerado era sempre exatamente o nome do tipo de elemento com um caractere de underscore prependido (`_`). (Os nomes dos tipos eram, portanto, limitados em comprimento a um caractere a menos do que outros nomes.) Embora isso ainda seja geralmente o caso, o nome do tipo de matriz pode variar disso no caso de nomes de comprimento máximo ou colisões com nomes de tipos do usuário que começam com underscore. Escrever código que depende dessa convenção é, portanto, desaconselhado. Em vez disso, use `pg_type`.`typarray` para localizar o tipo de matriz associado a um tipo dado.

Pode ser aconselhável evitar o uso de nomes de tipo e de tabela que comecem com um underscore. Embora o servidor mude os nomes de tipo de matriz gerados para evitar colisões com nomes fornecidos pelo usuário, ainda há risco de confusão, especialmente com software antigo do cliente que pode assumir que os nomes de tipo que começam com underscores sempre representam matrizes.

Antes da versão 8.2 do PostgreSQL, a sintaxe de criação do tipo shell `CREATE TYPE name` não existia. A maneira de criar um novo tipo de base era criar primeiro sua função de entrada. Nessa abordagem, o PostgreSQL verá primeiro o nome do novo tipo de dados como o tipo de retorno da função de entrada. O tipo shell é criado implicitamente nessa situação, e então ele pode ser referenciado nas definições das funções de I/O restantes. Essa abordagem ainda funciona, mas é desaconselhada e pode ser desativada em algumas versões futuras. Além disso, para evitar a sobrecarga acidental dos catálogos com tipos shell como resultado de erros simples nas definições das funções, um tipo shell só será criado dessa maneira quando a função de entrada for escrita em C.

Na versão 16 do PostgreSQL e nas versões posteriores, é desejável que as funções de entrada dos tipos básicos retornem erros “suaves” usando o novo mecanismo `errsave()`/`ereturn()`, em vez de lançar exceções `ereport()` como nas versões anteriores. Consulte `src/backend/utils/fmgr/README` para obter mais informações.

## Exemplos

Este exemplo cria um tipo composto e o usa em uma definição de função:

```
CREATE TYPE compfoo AS (f1 int, f2 text);

CREATE FUNCTION getfoo() RETURNS SETOF compfoo AS $$
    SELECT fooid, fooname FROM foo
$$ LANGUAGE SQL;
```

Este exemplo cria um tipo enumerado e o usa em uma definição de tabela:

```
CREATE TYPE bug_status AS ENUM ('new', 'open', 'closed');

CREATE TABLE bug (
    id serial,
    description text,
    status bug_status
);
```

Este exemplo cria um tipo de intervalo:

```
CREATE TYPE float8_range AS RANGE (subtype = float8, subtype_diff = float8mi);
```

Este exemplo cria o tipo de dados base `box` e, em seguida, usa o tipo em uma definição de tabela:

```
CREATE TYPE box;

CREATE FUNCTION my_box_in_function(cstring) RETURNS box AS ... ;
CREATE FUNCTION my_box_out_function(box) RETURNS cstring AS ... ;

CREATE TYPE box (
    INTERNALLENGTH = 16,
    INPUT = my_box_in_function,
    OUTPUT = my_box_out_function
);

CREATE TABLE myboxes (
    id integer,
    description box
);
```

Se a estrutura interna do `box` fosse uma matriz de quatro elementos `float4`, poderíamos, em vez disso, usar:

```
CREATE TYPE box (
    INTERNALLENGTH = 16,
    INPUT = my_box_in_function,
    OUTPUT = my_box_out_function,
    ELEMENT = float4
);
```

que permitiria que os números dos componentes de um valor de caixa fossem acessados por subscrito. Caso contrário, o tipo se comporta da mesma forma que antes.

Este exemplo cria um grande tipo de objeto e o usa em uma definição de tabela:

```
CREATE TYPE bigobj (
    INPUT = lo_filein, OUTPUT = lo_fileout,
    INTERNALLENGTH = VARIABLE
);
CREATE TABLE big_objs (
    id integer,
    obj bigobj
);
```

Mais exemplos, incluindo funções de entrada e saída adequadas, estão em [Seção 36.13][(xtypes.md "36.13. User-Defined Types")].

## Compatibilidade

A primeira forma do comando `CREATE TYPE`, que cria um tipo composto, está em conformidade com o padrão SQL. As outras formas são extensões do PostgreSQL. A declaração `CREATE TYPE` no padrão SQL também define outras formas que não são implementadas no PostgreSQL.

A capacidade de criar um tipo composto com zero atributos é uma exceção específica do PostgreSQL em relação ao padrão (análogo ao mesmo caso em `CREATE TABLE`).

## Veja também

[ALTER TYPE](sql-altertype.md "ALTER TYPE"), [CREATE DOMAIN](sql-createdomain.md "CREATE DOMAIN"), [CREATE FUNCTION](sql-createfunction.md "CREATE FUNCTION"), [DROP TYPE](sql-droptype.md "DROP TYPE")