## Capítulo 60. Escrevendo um provedor de varredura personalizado

**Índice**

* [60.1. Criar caminhos de varredura personalizados](custom-scan-path.md)

+ [60.1.1. Retornos de chamadas de caminho de varredura personalizado](custom-scan-path.md#CUSTOM-SCAN-PATH-CALLBACKS)

* [60.2. Criar planos de varredura personalizados](custom-scan-plan.md)

+ [60.2.1. Retornos de chamadas do plano de varredura personalizada](custom-scan-plan.md#CUSTOM-SCAN-PLAN-CALLBACKS)

* [60.3. Executar varreduras personalizadas](custom-scan-execution.md)

+ [60.3.1. Chamadas de Retorno de Execução de Varredura Personalizada](custom-scan-execution.md#CUSTOM-SCAN-EXECUTION-CALLBACKS)

O PostgreSQL suporta um conjunto de instalações experimentais que visam permitir que módulos de extensão adicionem novos tipos de varredura ao sistema. Ao contrário de um [wrapper de dados estrangeiro](fdwhandler.md), que é responsável apenas por saber como varrer suas próprias tabelas estrangeiras, um provedor de varredura personalizado pode fornecer um método alternativo de varredura de qualquer relação no sistema. Tipicamente, a motivação para escrever um provedor de varredura personalizado será permitir o uso de alguma otimização não suportada pelo sistema principal, como cache ou alguma forma de aceleração de hardware. Este capítulo descreve como escrever um novo provedor de varredura personalizado.

Implementar um novo tipo de varredura personalizada é um processo em três etapas. Primeiro, durante o planejamento, é necessário gerar caminhos de acesso que representem uma varredura usando a estratégia proposta. Segundo, se um desses caminhos de acesso for selecionado pelo planejador como a estratégia ótima para varredura de uma relação particular, o caminho de acesso deve ser convertido em um plano. Finalmente, deve ser possível executar o plano e gerar os mesmos resultados que teriam sido gerados para qualquer outro caminho de acesso que visasse a mesma relação.