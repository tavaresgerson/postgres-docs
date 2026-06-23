## 51.3. A etapa de Parser [#](#PARSER-STAGE)

* [51.3.1. Parser](parser-stage.md#PARSER-STAGE-PARSER)
* [51.3.2. Processo de Transformação](parser-stage.md#PARSER-STAGE-TRANSFORMATION-PROCESS)

A *fase de análise* é composta por duas partes:

* O *parser* definido em `gram.y` e `scan.l` é construído usando as ferramentas Unix bison e flex. * O *processo de transformação* faz modificações e ampliações nas estruturas de dados devolvidas pelo parser.

### 51.3.1. Parser [#](#PARSER-STAGE-PARSER)

O analisador tem que verificar a string de consulta (que chega como texto simples) para sintaxe válida. Se a sintaxe estiver correta, um *árvore de análise* é construída e devolvida; caso contrário, um erro é retornado. O analisador e o analisador lexical são implementados usando as ferramentas Unix conhecidas bison e flex.

O *lexer* é definido no arquivo `scan.l` e é responsável por reconhecer *identificadores*, as *palavras-chave SQL* etc. Para cada palavra-chave ou identificador que é encontrado, um *token* é gerado e entregue ao analisador.

O analisador é definido no arquivo `gram.y` e consiste em um conjunto de *regras gramaticais* e *ações* que são executadas sempre que uma regra é acionada. O código das ações (que é, na verdade, código C) é usado para construir o árvore de análise.

O arquivo `scan.l` é transformado no arquivo de fonte C `scan.c` usando o programa flex e o `gram.y` é transformado para `gram.c` usando bison. Após essas transformações terem sido realizadas, um compilador de C normal pode ser usado para criar o analisador. Nunca faça quaisquer alterações nos arquivos C gerados, pois eles serão sobrescritos na próxima vez que o flex ou o bison forem chamados.

Nota

As transformações e compilações mencionadas são normalmente feitas automaticamente usando os *makefiles* fornecidos com a distribuição de código-fonte do PostgreSQL.

Uma descrição detalhada do bison ou das regras gramaticais fornecidas em `gram.y` estaria além do escopo deste manual. Existem muitos livros e documentos que tratam de flex e bison. Você deve estar familiarizado com o bison antes de começar a estudar a gramática fornecida em `gram.y`, caso contrário, você não entenderá o que acontece lá.

### 51.3.2. Processo de Transformação [#](#PARSER-STAGE-TRANSFORMATION-PROCESS)

A etapa de análise cria uma árvore de análise usando apenas regras fixas sobre a estrutura sintática do SQL. Não faz nenhuma busca nos catálogos do sistema, portanto, não há possibilidade de entender a semântica detalhada das operações solicitadas. Após a conclusão da análise, o *processo de transformação* recebe a árvore devolvida pelo analisador como entrada e realiza a interpretação semântica necessária para entender quais tabelas, funções e operadores são referenciados pela consulta. A estrutura de dados que é construída para representar essas informações é chamada de *árvore de consulta*.

A razão para separar a análise bruta da análise semântica é que as consultas no catálogo do sistema só podem ser feitas dentro de uma transação, e não queremos iniciar uma transação imediatamente após receber uma cadeia de caracteres de consulta. A etapa de análise bruta é suficiente para identificar os comandos de controle de transação (`BEGIN`, `ROLLBACK`, etc.), e esses podem então ser executados corretamente sem qualquer análise adicional. Uma vez que sabemos que estamos lidando com uma consulta real (como `SELECT` ou `UPDATE`), está tudo bem iniciar uma transação se não estivermos nela já. Só então o processo de transformação pode ser invocado.

A árvore de consulta criada pelo processo de transformação é estruturalmente semelhante à árvore de análise bruta na maioria dos casos, mas apresenta muitas diferenças em detalhes. Por exemplo, um nó `FuncCall` na árvore de análise representa algo que parece sintaticamente como uma chamada de função. Isso pode ser transformado em um nó `FuncExpr` ou `Aggref`, dependendo se o nome referenciado se revela ser uma função comum ou uma função agregada. Além disso, informações sobre os tipos de dados reais das colunas e resultados das expressões são adicionadas à árvore de consulta.