## 66.3. Mapa de Espaço Livre [#](#STORAGE-FSM)

Cada relação de pilha e índice, exceto índices de hash, tem um Mapa de Espaço Livre (FSM) para acompanhar o espaço disponível na relação. Ele é armazenado ao lado dos dados principais da relação em uma relação separada, com o nome do número do filenode da relação, mais um sufixo `_fsm`. Por exemplo, se o filenode de uma relação é 12345, o FSM é armazenado em um arquivo chamado `12345_fsm`, no mesmo diretório que o arquivo da relação principal.

O mapa de espaço livre é organizado como uma árvore de páginas do FSM. As páginas de FSM do nível inferior armazenam o espaço livre disponível em cada página de pilha (ou índice), usando um byte para representar cada página desse tipo. Os níveis superiores agregam informações dos níveis inferiores.

Dentro de cada página do FSM, há um triângulo binário, armazenado em um array com um byte por nó. Cada nó folha representa uma página de heap, ou uma página de FSM de nível inferior. Em cada nó não folha, o valor mais alto de seus filhos é armazenado. O valor máximo nos nós folha é, portanto, armazenado na raiz.

Veja `src/backend/storage/freespace/README` para mais detalhes sobre como o FSM é estruturado e como ele é atualizado e pesquisado. O módulo [pg_freespacemap][(pgfreespacemap.md "F.27. pg_freespacemap — examine the free space map")] pode ser usado para examinar as informações armazenadas em mapas de espaço livre.