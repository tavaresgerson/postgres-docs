## Capítulo 66. Armazenamento físico do banco de dados

**Índice**

* [66.1. Estrutura do arquivo de banco de dados](storage-file-layout.md)
* [66.2. TOAST](storage-toast.md)

+ [66.2.1. Armazenamento TOAST fora de linha, em disco](storage-toast.md#STORAGE-TOAST-ONDISK)
+ [66.2.2. Armazenamento TOAST fora de linha, em memória](storage-toast.md#STORAGE-TOAST-INMEMORY)

* [66.3. Mapa de Espaço Livre](storage-fsm.md)
* [66.4. Mapa de Visibilidade](storage-vm.md)
* [66.5. Fork de Inicialização](storage-init.md)
* [66.6. Layout da Página do Banco de Dados](storage-page-layout.md)

+ [66.6.1. Estrutura de linha de tabela](storage-page-layout.md#STORAGE-TUPLE-LAYOUT)

* Tuples apenas de pilha (HOT) [(storage-hot.md)]

Este capítulo fornece uma visão geral do formato de armazenamento físico utilizado pelos bancos de dados PostgreSQL.