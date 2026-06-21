## 10.3. Funções [#](#TYPECONV-FUNC)

A função específica que é referenciada por uma chamada de função é determinada usando o procedimento a seguir.

**Resolução do Tipo de Função**

1. Selecione as funções a serem consideradas do catálogo do sistema `pg_proc`. Se um nome de função não qualificada pelo esquema foi usado, as funções consideradas são aquelas com o nome correspondente e o número de argumentos que são visíveis no caminho de pesquisa atual (ver [Seção 5.10.3](ddl-schemas.md#DDL-SCHEMAS-PATH)). Se um nome de função qualificada foi fornecido, apenas as funções no esquema especificado são consideradas.

1. Se o caminho de busca encontrar múltiplas funções com tipos de argumentos idênticos, apenas a que aparece mais cedo no caminho é considerada. Funções com tipos de argumentos diferentes são consideradas em pé de igualdade, independentemente da posição no caminho de busca.
2. Se uma função for declarada com um parâmetro de matriz `VARIADIC`, e a chamada não use a palavra-chave `VARIADIC`, então a função é tratada como se o parâmetro de matriz fosse substituído por uma ou mais ocorrências de seu tipo de elemento, conforme necessário para corresponder à chamada. Após essa expansão, a função pode ter tipos de argumento efetivos idênticos a uma função não variável. Nesse caso, a função que aparece mais cedo no caminho de busca é usada, ou, se as duas funções estiverem no mesmo esquema, a não variável é preferida.

Isso cria um perigo de segurança ao chamar, via nome qualificado [[10]](#ftn.FUNC-QUALIFIED-SECURITY), uma função variável encontrada em um esquema que permite que usuários não confiáveis criem objetos. Um usuário malicioso pode assumir o controle e executar funções SQL arbitrárias como se você as tivesse executado. Substitua uma chamada que contém a palavra-chave `VARIADIC`, que contorna esse perigo. Chamadas que preenchem os parâmetros `VARIADIC "any"` muitas vezes não têm uma formulação equivalente que contenha a palavra-chave `VARIADIC`. Para emitir essas chamadas com segurança, o esquema da função deve permitir que apenas usuários confiáveis criem objetos.
3. Funções que têm valores padrão para os parâmetros são consideradas compatíveis com qualquer chamada que omite zero ou mais das posições de parâmetro que podem ter valores padrão. Se mais de uma dessas funções corresponder a uma chamada, a que aparece mais cedo no caminho de busca é usada. Se houver duas ou mais dessas funções no mesmo esquema com tipos de parâmetro idênticos nas posições não padrão (o que é possível se eles tiverem diferentes conjuntos de parâmetros padrão), o sistema não será capaz de determinar qual prefere, e, portanto, ocorrerá um erro de "chamada de função ambígua" se não for encontrada uma correspondência melhor para a chamada.

Isso cria um risco de disponibilidade ao chamar, via nome qualificado [[10]](typeconv-func.md#ftn.FUNC-QUALIFIED-SECURITY), qualquer função encontrada em um esquema que permita que usuários não confiáveis criem objetos. Um usuário malicioso pode criar uma função com o nome de uma função existente, replicando os parâmetros daquela função e anexando novos parâmetros com valores padrão. Isso preter os novos chamados à função original. Para evitar esse risco, coloque as funções em esquemas que permitam apenas que usuários confiáveis criem objetos.
2. Verifique se uma função aceita exatamente os tipos de argumentos de entrada. Se existir (pode haver apenas uma correspondência exata no conjunto de funções consideradas), use-a. A falta de uma correspondência exata cria um risco de segurança ao chamar, via nome qualificado [[10]](typeconv-func.md#ftn.FUNC-QUALIFIED-SECURITY), uma função encontrada em um esquema que permita que usuários não confiáveis criem objetos. Nessas situações, force os argumentos para obter uma correspondência exata. (Os casos que envolvem `unknown` nunca encontrarão uma correspondência nesta etapa.)
3. Se não for encontrada uma correspondência exata, verifique se o chamado de função parece ser um pedido de conversão de tipo especial. Isso acontece se o chamado de função tiver apenas um argumento e o nome da função for o mesmo que o nome (interno) de algum tipo de dados. Além disso, o argumento da função deve ser uma literal de tipo desconhecido ou um tipo que seja coercível binário para o tipo de dados nomeado, ou um tipo que poderia ser convertido para o tipo de dados nomeado aplicando as funções de E/S (ou seja, a conversão é para ou a partir de um dos tipos de string padrão). Quando essas condições são atendidas, o chamado de função é tratado como uma forma de especificação de `CAST`. [[11]](#ftn.id-1.5.9.8.4.4.1.2)
4. Procure a melhor correspondência.

1. Descarte as funções candidatas para as quais os tipos de entrada não correspondem e não podem ser convertidos (usando uma conversão implícita) para corresponder. Os literais `unknown` são assumidos como convertidos para qualquer coisa para esse propósito. Se apenas uma candidata permanecer, use-a; caso contrário, continue para o próximo passo.
2. Se qualquer argumento de entrada estiver de um tipo de domínio, trate-o como sendo do tipo base do domínio para todos os passos subsequentes. Isso garante que os domínios atuem como seus tipos base para fins de resolução de funções ambíguas.
3. Analise todas as candidatas e mantenha aquelas com os mais exatos correspondências nos tipos de entrada. Mantenha todas as candidatas se nenhuma delas tiver correspondências exatas. Se apenas uma candidata permanecer, use-a; caso contrário, continue para o próximo passo.
4. Analise todas as candidatas e mantenha aquelas que aceitam tipos preferidos (da categoria de tipo do tipo de dados de entrada) nas posições mais onde a conversão de tipo será necessária. Mantenha todas as candidatas se nenhuma delas aceitar tipos preferidos. Se apenas uma candidata permanecer, use-a; caso contrário, continue para o próximo passo.
5. Se quaisquer argumentos de entrada forem `unknown`, verifique as categorias de tipo aceitas nessas posições de argumento pelos candidatos restantes. Em cada posição, selecione a categoria `string` se qualquer candidato aceitar essa categoria. (Esse viés em direção à string é apropriado, pois um literal de tipo desconhecido parece uma string.) Caso contrário, se todos os candidatos restantes aceitarem a mesma categoria de tipo, selecione essa categoria; caso contrário, falhe porque a escolha correta não pode ser deduzida sem mais pistas. Agora, descarte as candidatas que não aceitam a categoria de tipo selecionada. Além disso, se qualquer candidato aceitar um tipo preferido nessa categoria, descarte as candidatas que aceitam tipos não preferidos para esse argumento. Mantenha todas as candidatas se nenhuma sobreviver a essas testes. Se apenas uma candidata permanecer, use-a; caso contrário, continue para o próximo passo.
6. Se houver tanto `unknown` quanto argumentos de tipo conhecido, e todos os argumentos de tipo conhecido tiverem o mesmo tipo, assuma que os argumentos `unknown` também são desse tipo, e verifique quais candidatos podem aceitar esse tipo nas posições de argumento `unknown`. Se exatamente uma candidata passar esse teste, use-a. Caso contrário, falhe.

Observe que as regras de "melhor correspondência" são idênticas para a resolução de operadores e tipos de funções. Alguns exemplos seguem.

**Exemplo 10.6. Resolução do tipo de argumento da função de arredondamento**

Existe apenas uma função `round` que recebe dois argumentos; ela recebe um primeiro argumento do tipo `numeric` e um segundo argumento do tipo `integer`. Portanto, a seguinte consulta converte automaticamente o primeiro argumento do tipo `integer` para `numeric`:

```
SELECT round(4, 4);

 round
--------
 4.0000
(1 row)
```

Essa consulta é, na verdade, transformada pelo analisador em:

```
SELECT round(CAST (4 AS numeric), 4);
```

Como as constantes numéricas com pontos decimais são inicialmente atribuídas ao tipo `numeric`, a consulta a seguir não exigirá conversão de tipo e, portanto, pode ser ligeiramente mais eficiente:

```
SELECT round(4.0, 4);
```



**Exemplo 10.7. Resolução de função variadic**

```
CREATE FUNCTION public.variadic_example(VARIADIC numeric[]) RETURNS int
  LANGUAGE sql AS 'SELECT 1';
CREATE FUNCTION
```

Essa função aceita, mas não exige, a palavra-chave VARIADIC. Ela tolera argumentos tanto inteiros quanto numéricos:

```
SELECT public.variadic_example(0),
       public.variadic_example(0.0),
       public.variadic_example(VARIADIC array[0.0]);
 variadic_example | variadic_example | variadic_example
------------------+------------------+------------------
                1 |                1 |                1
(1 row)
```

No entanto, as primeiras e segundas chamadas preferirão funções mais específicas, se disponíveis:

```
CREATE FUNCTION public.variadic_example(numeric) RETURNS int
  LANGUAGE sql AS 'SELECT 2';
CREATE FUNCTION

CREATE FUNCTION public.variadic_example(int) RETURNS int
  LANGUAGE sql AS 'SELECT 3';
CREATE FUNCTION

SELECT public.variadic_example(0),
       public.variadic_example(0.0),
       public.variadic_example(VARIADIC array[0.0]);
 variadic_example | variadic_example | variadic_example
------------------+------------------+------------------
                3 |                2 |                1
(1 row)
```

Dado a configuração padrão e apenas a primeira função existente, as primeiras e segundas chamadas são inseguras. Qualquer usuário poderia interceptá-las ao criar a segunda ou terceira função. Ao corresponder exatamente ao tipo de argumento e usar a palavra-chave `VARIADIC`, a terceira chamada é segura.



**Exemplo 10.8. Resolução do tipo de função de substring**

Existem várias funções `substr`, uma das quais aceita os tipos `text` e `integer`. Se chamada com uma constante de cadeia de caracteres de tipo não especificado, o sistema escolhe a função candidata que aceita um argumento da categoria preferida `string` (ou seja, de tipo `text`).

```
SELECT substr('1234', 3);

 substr
--------
     34
(1 row)
```

Se a string for declarada como do tipo `varchar`, como pode ser o caso se ela vem de uma tabela, então o analisador tentará convertê-la para se tornar `text`:

```
SELECT substr(varchar '1234', 3);

 substr
--------
     34
(1 row)
```

Isso é transformado pelo analisador para se tornar efetivamente:

```
SELECT substr(CAST (varchar '1234' AS text), 3);
```

### Nota

O analisador aprende do catálogo `pg_cast` que `text` e `varchar` são binariamente compatíveis, o que significa que um deles pode ser passado para uma função que aceita o outro sem realizar nenhuma conversão física. Portanto, não há realmente chamada de conversão de tipo neste caso.

E, se a função for chamada com um argumento do tipo `integer`, o analisador tentará convertê-lo em `text`:

```
SELECT substr(1234, 3);
ERROR:  function substr(integer, integer) does not exist
HINT:  No function matches the given name and argument types. You might need
to add explicit type casts.
```

Isso não funciona porque `integer` não tem uma cast implícita para `text`. No entanto, uma cast explícita funcionará:

```
SELECT substr(CAST (1234 AS text), 3);

 substr
--------
     34
(1 row)
```



---

[[10]](#FUNC-QUALIFIED-SECURITY) O perigo não surge com um nome não qualificado por esquema, porque um caminho de pesquisa que contém esquemas que permitem que usuários não confiáveis criem objetos não é um padrão de uso seguro de esquema (ddl-schemas.md#DDL-SCHEMAS-PATTERNS "5.10.6. Usage Patterns").

[[11]](#id-1.5.9.8.4.4.1.2) A razão para essa etapa é para suportar especificações de cast estilo função nos casos em que não há uma função de cast real. Se houver uma função de cast, ela é convencionalmente nomeada de acordo com seu tipo de saída, e, portanto, não há necessidade de ter um caso especial. Consulte [CREATE CAST](sql-createcast.md "CREATE CAST") para comentários adicionais.