## Capítulo 63. Definição da Interface do Método de Acesso ao Índice

**Índice**

* [63.1. Estrutura Básica da API para Índices](index-api.md)
* [63.2. Funções de Método de Acesso ao Índice](index-functions.md)
* [63.3. Detecção de Índices](index-scanning.md)
* [63.4. Considerações sobre o Bloqueio do Índice](index-locking.md)
* [63.5. Verificação de Unicidade do Índice](index-unique-checks.md)
* [63.6. Funções de Estimativa do Custo do Índice](index-cost-estimation.md)

Este capítulo define a interface entre o sistema principal do PostgreSQL e os métodos de acesso ao índice, que gerenciam os tipos de índice individuais. O sistema principal não sabe nada sobre índices além do que é especificado aqui, portanto é possível desenvolver tipos de índice totalmente novos escrevendo código adicional.

Todos os índices no PostgreSQL são o que são tecnicamente conhecidos como *índices secundários*; ou seja, o índice é fisicamente separado do arquivo da tabela que ele descreve. Cada índice é armazenado como sua própria *relação* física e, portanto, é descrito por uma entrada no catálogo `pg_class`. O conteúdo de um índice está inteiramente sob o controle do seu método de acesso ao índice. Na prática, todos os métodos de acesso ao índice dividem os índices em páginas de tamanho padrão para que possam usar o gerenciador de armazenamento regular e o gerenciador de buffer para acessar o conteúdo do índice. (Todos os métodos de acesso ao índice existentes usam, além disso, o layout padrão de página descrito na [Seção 66.6] (storage-page-layout.md "66.6. Database Page Layout"), e a maioria usa o mesmo formato para os cabeçalhos de tupla do índice; mas essas decisões não são impostas em um método de acesso.)

Um índice é, efetivamente, uma mapeo de alguns valores de chave de dados para *identificador de tupla*, ou TIDs, das versões de linha (tuplas) na tabela pai do índice. Um TID consiste em um número de bloco e um número de item dentro desse bloco (ver [Seção 66.6](storage-page-layout.md)). Esta é informação suficiente para obter uma versão específica de linha da tabela. Os índices não são diretamente conscientes de que, sob MVCC, pode haver múltiplas versões existentes da mesma linha lógica; para um índice, cada tupla é um objeto independente que precisa de sua própria entrada de índice. Assim, uma atualização de uma linha sempre cria novas entradas de índice para a linha, mesmo que os valores das chaves não tenham mudado. ([Tuples HOT](storage-hot.md)) são uma exceção a esta declaração; mas os índices também não lidam com esses.) As entradas de índice para tuplas mortas são recuperadas (por vácuo) quando as próprias tuplas mortas são recuperadas.