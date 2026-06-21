## Capítulo 33. Objetos Grandes

**Índice**

* [33.1. Introdução](lo-intro.md)
* [33.2. Recursos de implementação](lo-implementation.md)
* [33.3. Interfaces do cliente](lo-interfaces.md)

+ [33.3.1. Criando um Objeto Grande][(lo-interfaces.md#LO-CREATE)]
+ [33.3.2. Importando um Objeto Grande][(lo-interfaces.md#LO-IMPORT)]
+ [33.3.3. Exportando um Objeto Grande][(lo-interfaces.md#LO-EXPORT)]
+ [33.3.4. Abrindo um Objeto Grande Existente][(lo-interfaces.md#LO-OPEN)]
+ [33.3.5. Escrevendo Dados em um Objeto Grande][(lo-interfaces.md#LO-WRITE)]
+ [33.3.6. Lendo Dados de um Objeto Grande][(lo-interfaces.md#LO-READ)]
+ [33.3.7. Buscando em um Objeto Grande][(lo-interfaces.md#LO-SEEK)]
+ [33.3.8. Obtendo a Posição de Busca de um Objeto Grande][(lo-interfaces.md#LO-TELL)]
+ [33.3.9. Cortando um Objeto Grande][(lo-interfaces.md#LO-TRUNCATE)]
+ [33.3.10. Fechando um Descritor de Objeto Grande][(lo-interfaces.md#LO-CLOSE)]
+ [33.3.11. Removendo um Objeto Grande][(lo-interfaces.md#LO-UNLINK)]

* [33.4. Funções no lado do servidor](lo-funcs.md)
* [33.5. Programa exemplo](lo-examplesect.md)

O PostgreSQL possui uma *facilidade de objeto grande*, que oferece acesso em estilo de fluxo aos dados do usuário que são armazenados em uma estrutura especial de objeto grande. O acesso em fluxo é útil ao trabalhar com valores de dados que são grandes demais para serem manipulados convenientemente como um todo.

Este capítulo descreve a implementação e as interfaces de linguagem de programação e consulta para dados de objetos grandes do PostgreSQL. Usamos a biblioteca C libpq para os exemplos neste capítulo, mas a maioria das interfaces de programação nativas do PostgreSQL suporta funcionalidades equivalentes. Outras interfaces podem usar a interface de objeto grande internamente para fornecer suporte genérico para valores grandes. Isso não é descrito aqui.