## 30.1. O que é a compilação JIT? [#](#JIT-REASON)

* [30.1.1. Operações Aceleradas JIT](jit-reason.md#JIT-ACCELERATED-OPERATIONS)
* [30.1.2. Inlining](jit-reason.md#JIT-INLINING)
* [30.1.3. Otimização](jit-reason.md#JIT-OPTIMIZATION)

A compilação Just-in-Time (JIT) é o processo de transformar alguma forma de avaliação de programas interpretados em um programa nativo, e fazer isso em tempo de execução. Por exemplo, em vez de usar código de propósito geral que pode avaliar expressões SQL arbitrárias para avaliar um predicado SQL específico como `WHERE a.col = 3`, é possível gerar uma função que é específica para essa expressão e que pode ser executada nativamente pela CPU, resultando em um aumento de velocidade.

O PostgreSQL tem suporte integrado para realizar a compilação JIT usando [LLVM](https://llvm.org/) quando o PostgreSQL é construído com [`--with-llvm`](install-make.md#CONFIGURE-WITH-LLVM).

Veja `src/backend/jit/README` para mais detalhes.

### 30.1.1. Operações Aceleradas JIT [#](#JIT-ACCELERATED-OPERATIONS)

Atualmente, a implementação JIT do PostgreSQL oferece suporte para acelerar a avaliação de expressões e a deformação de tuplas. Várias outras operações podem ser aceleradas no futuro.

A avaliação de expressão é usada para avaliar cláusulas `WHERE`, listas de alvos, agregados e projeções. Pode ser acelerada ao gerar código específico para cada caso.

A deformação de tupla é o processo de transformar uma tupla em disco (ver [Seção 66.6.1](storage-page-layout.md#STORAGE-TUPLE-LAYOUT)) em sua representação de memória. Pode ser acelerada ao criar uma função específica para o layout da tabela e o número de colunas a serem extraídas.

### 30.1.2. Inlinhamento [#](#JIT-INLINING)

O PostgreSQL é muito extensivo e permite que novos tipos de dados, funções, operadores e outros objetos de banco de dados sejam definidos; veja [Capítulo 36](extend.md). De fato, os objetos embutidos são implementados usando mecanismos quase idênticos. Essa extensibilidade implica em algum custo adicional, por exemplo, devido a chamadas de função (veja [Seção 36.3](xfunc.md)). Para reduzir esse custo adicional, a compilação JIT pode incluir os corpos das pequenas funções nas expressões que as utilizam. Isso permite que uma porcentagem significativa do custo adicional seja otimizada.

### 30.1.3. Otimização [#](#JIT-OPTIMIZATION)

O LLVM tem suporte para otimização de código gerado. Algumas das otimizações são suficientemente baratas para serem realizadas sempre que o JIT é usado, enquanto outras são benéficas apenas para consultas de maior duração. Consulte <https://llvm.org/docs/Passes.html#transform-passes> para mais detalhes sobre otimizações.