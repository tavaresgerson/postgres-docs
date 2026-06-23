## 51.4. O Sistema de Regras do PostgreSQL [#](#RULE-SYSTEM)

O PostgreSQL suporta um sistema de regras poderoso para a especificação de *visões* e atualizações de *visões* ambíguas. Originalmente, o sistema de regras do PostgreSQL consistia em duas implementações:

* A primeira funcionava com processamento de nível de *linha* e foi implementada profundamente no *executor*. O sistema de regras era chamado sempre que uma linha individual tivesse sido acessada. Essa implementação foi removida em 1995, quando o último lançamento oficial do projeto Berkeley Postgres foi transformado em Postgres95.
* A segunda implementação do sistema de regras é uma técnica chamada *reescrita de consulta*. O *sistema de reescrita* é um módulo que existe entre a *fase de análise* e o *planificador/opinião*. Essa técnica ainda é implementada.

O reescritor de consultas é discutido em detalhes no [Capítulo 39](rules.md), então não há necessidade de cobrir isso aqui. Apenas vamos ressaltar que tanto a entrada quanto a saída do reescritor são árvores de consulta, ou seja, não há mudança na representação ou no nível de detalhe semântico nas árvores. A reescrita pode ser vista como uma forma de expansão de macro.