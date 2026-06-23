## 13.7. Bloqueio e índices [#](#LOCKING-INDEXES)

Embora o PostgreSQL ofereça acesso não bloqueante de leitura/escrita aos dados da tabela, o acesso não bloqueante de leitura/escrita não é oferecido atualmente para todos os métodos de acesso a índices implementados no PostgreSQL. Os vários tipos de índice são tratados da seguinte forma:

Índices de árvore B, GiST e SP-GiST: As bloqueadoras de página exclusivas de nível de página/partilha de curto prazo são usadas para acesso de leitura/escrita. As bloqueadoras são liberadas imediatamente após cada linha do índice ser obtida ou inserida. Esses tipos de índice oferecem a maior concorrência sem condições de bloqueio.

Indekses de hash: As permissões de nível de cache exclusiva/exclusiva de hash são usadas para acesso de leitura/escrita. As permissões são liberadas após o processamento de todo o cache. As permissões de nível de cache oferecem melhor concorrência do que as de nível de índice, mas é possível ocorrer um impasse, uma vez que as permissões são mantidas por mais tempo do que uma operação de índice.

Índices GIN: As bloqueadoras de página exclusivas e de nível de página são usadas para acesso de leitura/escrita. As bloqueadoras são liberadas imediatamente após cada linha do índice ser obtida ou inserida. Mas observe que a inserção de um valor indexado por GIN geralmente produz várias inserções de chave de índice por linha, então o GIN pode realizar um trabalho substancial para a inserção de um único valor.

Atualmente, os índices de árvore B oferecem o melhor desempenho para aplicações concorrentes; uma vez que também possuem mais recursos do que índices de hash, eles são o tipo de índice recomendado para aplicações concorrentes que precisam indexar dados escalares. Ao lidar com dados não escalares, as árvores B não são úteis, e os índices GiST, SP-GiST ou GIN devem ser usados em vez disso.