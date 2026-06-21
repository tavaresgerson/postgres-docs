## 65.6. Índices de hash [#](#HASH-INDEX)

* [65.6.1. Visão geral](hash-index.md#HASH-INTRO)
* [65.6.2. Implementação](hash-index.md#HASH-IMPLEMENTATION)

### 65.6.1. Visão geral [#](#HASH-INTRO)

O PostgreSQL inclui uma implementação de índices de hash persistentes no disco, que são totalmente recuperáveis em caso de falha. Qualquer tipo de dados pode ser indexado por um índice de hash, incluindo tipos de dados que não têm uma ordem linear bem definida. Os índices de hash armazenam apenas o valor de hash dos dados que estão sendo indexados, portanto, não há restrições sobre o tamanho da coluna de dados que está sendo indexada.

Os índices hash só suportam índices de uma única coluna e não permitem verificação de unicidade.

Os índices de hash só suportam o operador `=`, portanto, as cláusulas WHERE que especificam operações de intervalo não poderão aproveitar os índices de hash.

Cada tupla do índice de hash armazena apenas o valor de hash de 4 bytes, não o valor real da coluna. Como resultado, os índices de hash podem ser muito menores que as árvores B ao indexar itens de dados mais longos, como UUIDs, URLs, etc. A ausência do valor da coluna também torna todas as pesquisas de índice de hash perdas. Os índices de hash podem participar de pesquisas de índice de bitmap e pesquisas reversas.

Os índices de hash são os mais otimizados para cargas de trabalho pesadas de SELECT e UPDATE que utilizam varreduras de igualdade em tabelas maiores. Em um índice de B-tree, as pesquisas devem descer pela árvore até que a página de folha seja encontrada. Em tabelas com milhões de linhas, essa descida pode aumentar o tempo de acesso aos dados. O equivalente a uma página de folha em um índice de hash é referido como uma página de bucket. Em contraste, um índice de hash permite o acesso direto às páginas de bucket, reduzindo potencialmente o tempo de acesso ao índice em tabelas maiores. Essa redução no "I/O lógico" torna-se ainda mais pronunciada em índices/dados maiores que shared_buffers/RAM.

Os índices de hash foram projetados para lidar com distribuições desiguais de valores de hash. O acesso direto às páginas do bucket funciona bem se os valores de hash estiverem distribuídos de forma uniforme. Quando as inserções significam que a página do bucket fica cheia, páginas adicionais de overflow são encadeadas àquela página específica do bucket, expandindo localmente o armazenamento para tuplas de índice que correspondem a esse valor de hash. Ao digitalizar um bucket de hash durante consultas, precisamos percorrer todas as páginas de overflow. Assim, um índice de hash desequilibrado pode ser, na verdade, pior do que uma árvore B em termos de número de acessos de bloco necessários, para alguns dados.

Como resultado dos casos de excesso, podemos dizer que os índices de hash são mais adequados para dados únicos, quase únicos ou dados com um número baixo de linhas por cache de hash. Uma maneira possível de evitar problemas é excluir valores altamente não únicos do índice usando uma condição de índice parcial, mas isso pode não ser adequado em muitos casos.

Assim como as árvores B, os índices de hash realizam a simples exclusão de tuplas de índice. Essa é uma operação de manutenção diferida que exclui as tuplas de índice que são conhecidas como seguras para serem excluídas (aquelas cujos bits LP_DEAD do identificador do item já estão definidos). Se uma inserção não encontrar espaço disponível em uma página, tentamos evitar a criação de uma nova página de excesso tentando remover tuplas de índice mortas. A remoção não pode ocorrer se a página estiver marcada naquele momento. A exclusão dos ponteiros de índice morto também ocorre durante o VACUUM.

Se puder, o VACUUM também tentará engolir os tuplos do índice em o número de páginas de overflow possível, minimizando a cadeia de overflow. Se uma página de overflow ficar vazia, as páginas de overflow podem ser recicladas para serem reutilizadas em outros buckets, embora nunca as devolvamos ao sistema operacional. Atualmente, não há disposição para encolher um índice de hash, exceto reconstruí-lo com REINDEX. Não há disposição para reduzir o número de buckets, também.

Os índices de hash podem expandir o número de páginas de bucket à medida que o número de linhas indexadas cresce. A correspondência entre a chave de hash e o número de bucket é escolhida para que o índice possa ser expandido incrementalmente. Quando um novo bucket deve ser adicionado ao índice, exatamente um bucket existente precisará ser "dividido", com alguns de seus tuplos sendo transferidos para o novo bucket de acordo com a correspondência atualizada entre a chave e o número de bucket.

A expansão ocorre no plano de fundo, o que pode aumentar o tempo de execução para inserções de usuários. Assim, os índices de hash podem não ser adequados para tabelas com um número de linhas que aumenta rapidamente.

### 65.6.2. Implementação [#](#HASH-IMPLEMENTATION)

Existem quatro tipos de páginas em um índice de hash: a página meta (página zero), que contém informações de controle alocadas estaticamente; páginas de cache primário; páginas de overflow; e páginas de mapa de bits, que acompanham as páginas de overflow que foram liberadas e estão disponíveis para reutilização. Para fins de endereçamento, as páginas de mapa de bits são consideradas um subconjunto das páginas de overflow.

Tanto a digitalização do índice quanto a inserção de tuplas exigem localizar o bucket onde uma determinada tupla deve ser localizada. Para isso, precisamos do número de buckets, highmask e lowmask da metapágina; no entanto, por razões de desempenho, não é desejável precisar bloquear e prender a metapágina para cada operação desse tipo. Em vez disso, mantemos uma cópia cacheada da metapágina na entrada relcache de cada backend. Isso produzirá a correção mapeamento de buckets, desde que o bucket alvo não tenha sido dividido desde a última atualização do cache.

As páginas de balde primário e as páginas de overflow são alocadas de forma independente, pois qualquer índice dado pode precisar de mais ou menos páginas de overflow em relação ao seu número de baldes. O código de hash utiliza um conjunto interessante de regras de endereçamento para suportar um número variável de páginas de overflow, sem precisar mover as páginas de balde primário depois que elas são criadas.

Cada linha da tabela indexada é representada por um único tupla de índice no índice hash. As tuplas de índice hash são armazenadas em páginas de balde e, se existirem, em páginas de overflow. Aceleração das pesquisas é feita mantendo as entradas do índice em qualquer página de índice ordenadas pelo código hash, permitindo assim a utilização de pesquisa binária dentro de uma página de índice. No entanto, é importante notar que não há *nenhuma* suposição sobre a ordem relativa dos códigos hash em diferentes páginas de índice de um balde.

Os algoritmos de divisão de balde para expandir o índice de hash são complexos demais para serem mencionados aqui, embora sejam descritos com mais detalhes em `src/backend/access/hash/README`. O algoritmo de divisão é seguro em caso de falha e pode ser reiniciado se não for concluído com sucesso.