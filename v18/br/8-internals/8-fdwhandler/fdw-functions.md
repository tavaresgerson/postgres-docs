## 58.1. Funções de Wrapper de Dados Estrangeiros [#](#FDW-FUNCTIONS)

O autor do FDW precisa implementar uma função de manipulador e, opcionalmente, uma função de validação. Ambas as funções devem ser escritas em uma linguagem compilada, como C, usando a interface da versão 1. Para detalhes sobre as convenções de chamada de linguagem C e carregamento dinâmico, consulte [Seção 36.10](xfunc-c.md).

A função de manipulador simplesmente retorna uma estrutura de ponteiros de função para funções de callback que serão chamadas pelo planejador, executor e vários comandos de manutenção. A maior parte do esforço na escrita de um FDW está na implementação dessas funções de callback. A função de manipulador deve ser registrada no PostgreSQL como não recebendo argumentos e retornando o pseudo-tipo especial `fdw_handler`. As funções de callback são funções C simples e não são visíveis ou acessíveis no nível SQL. As funções de callback são descritas em [Seção 58.2](fdw-callbacks.md).

A função de validação é responsável por validar as opções fornecidas nos comandos `CREATE` e `ALTER` para seu wrapper de dados externos, bem como servidores externos, mapeamentos de usuário e tabelas externas usando o wrapper. A função de validação deve ser registrada para receber dois argumentos, um array de texto contendo as opções a serem validadas e um OID que representa o tipo de objeto com o qual as opções estão associadas. Este último corresponde ao OID do catálogo do sistema no qual o objeto seria armazenado, um dos seguintes:

* `AttributeRelationId`
* `ForeignDataWrapperRelationId`
* `ForeignServerRelationId`
* `ForeignTableRelationId`
* `UserMappingRelationId`

Se nenhuma função de validação for fornecida, as opções não são verificadas no momento da criação do objeto ou no momento da alteração do objeto.