## 41.2. Estrutura do PL/pgSQL [#](#PLPGSQL-STRUCTURE)

As funções escritas em PL/pgSQL são definidas para o servidor executando os comandos [CREATE FUNCTION](sql-createfunction.md). Um comando desse tipo normalmente se parece com, por exemplo:

```
CREATE FUNCTION somefunc(integer, text) RETURNS integer
AS 'function body text'
LANGUAGE plpgsql;
```

O corpo da função é simplesmente uma literal de string, no que diz respeito a `CREATE FUNCTION`. É frequentemente útil usar a citação de dólar (ver [Seção 4.1.2.4](sql-syntax-lexical.md#SQL-SYNTAX-DOLLAR-QUOTING)) para escrever o corpo da função, em vez da sintaxe normal de citação simples. Sem citação de dólar, quaisquer citações simples ou barras invertidas no corpo da função devem ser escapadas duplicando-as. Quase todos os exemplos deste capítulo usam literais com citação de dólar para seus corpos de função.

PL/pgSQL é uma linguagem estruturada em blocos. O texto completo do corpo de uma função deve ser um *bloco*. Um bloco é definido da seguinte forma:

```
[ <<label>> ]
[ DECLARE
    declarations ]
BEGIN
    statements
END [ label ];
```

Cada declaração e cada afirmação dentro de um bloco é finalizada por um ponto e vírgula. Um bloco que aparece dentro de outro bloco deve ter um ponto e vírgula após `END`, como mostrado acima; no entanto, o `END` final que conclui o corpo de uma função não requer um ponto e vírgula.

### DICA

Um erro comum é escrever um ponto e vírgula imediatamente após `BEGIN`. Isso é incorreto e resultará em um erro de sintaxe.

Um *`label`* é necessário apenas se você deseja identificar o bloco para uso em uma declaração `EXIT`, ou para qualificar os nomes das variáveis declaradas no bloco. Se uma etiqueta for dada após `END`, ela deve corresponder à etiqueta no início do bloco.

Todas as palavras-chave são sensíveis a maiúsculas e minúsculas. Os identificadores são implicitamente convertidos para minúsculas, a menos que sejam citados em duplicado, assim como nas ordinais comandos SQL.

Os comentários funcionam da mesma maneira no código PL/pgSQL como no SQL comum. Uma barra dupla (`--`) inicia um comentário que se estende até o final da linha. Um `/*` inicia um comentário de bloco que se estende até a ocorrência correspondente de `*/`. Os comentários de bloco se aninham.

Qualquer declaração na seção de declaração de um bloco pode ser um *subbloco*. Subblocos podem ser usados para agrupamento lógico ou para localizar variáveis em um pequeno grupo de declarações. Variáveis declaradas em um subbloco mascaram quaisquer variáveis com o mesmo nome de blocos externos por toda a duração do subbloco; mas você pode acessar as variáveis externas de qualquer maneira, se qualificar seus nomes com a etiqueta do bloco. Por exemplo:

```
CREATE FUNCTION somefunc() RETURNS integer AS $$
<< outerblock >>
DECLARE
    quantity integer := 30;
BEGIN
    RAISE NOTICE 'Quantity here is %', quantity;  -- Prints 30
    quantity := 50;
    --
    -- Create a subblock
    --
    DECLARE
        quantity integer := 80;
    BEGIN
        RAISE NOTICE 'Quantity here is %', quantity;  -- Prints 80
        RAISE NOTICE 'Outer quantity here is %', outerblock.quantity;  -- Prints 50
    END;

    RAISE NOTICE 'Quantity here is %', quantity;  -- Prints 50

    RETURN quantity;
END;
$$ LANGUAGE plpgsql;
```

### Nota

Na verdade, existe um "bloco externo" oculto que envolve o corpo de qualquer função PL/pgSQL. Esse bloco fornece as declarações dos parâmetros da função (se houver), bem como algumas variáveis especiais, como `FOUND` (consulte [Seção 41.5.5] (plpgsql-statements.md#PLPGSQL-STATEMENTS-DIAGNOSTICS "41.5.5. Obtaining the Result Status")). O bloco externo é marcado com o nome da função, o que significa que os parâmetros e as variáveis especiais podem ser qualificados com o nome da função.

É importante não confundir o uso de `BEGIN`/`END` para agrupar declarações em PL/pgSQL com os comandos SQL com o mesmo nome para controle de transação. O `BEGIN`/`END` do PL/pgSQL são apenas para agrupamento; eles não iniciam ou encerram uma transação. Consulte [Seção 41.8](plpgsql-transactions.md) para obter informações sobre a gestão de transações em PL/pgSQL. Além disso, um bloco contendo uma cláusula `EXCEPTION` forma efetivamente uma subtransação que pode ser revertida sem afetar a transação externa. Para mais informações sobre isso, consulte [Seção 41.6.8](plpgsql-control-structures.md#PLPGSQL-ERROR-TRAPPING).