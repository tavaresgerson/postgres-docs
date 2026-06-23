## Capítulo 69. Como o planejador usa estatísticas

**Índice**

* [69.1. Exemplos de Estimação de Linha](row-estimation-examples.md)
* [69.2. Exemplos de Estatísticas Multivariadas](multivariate-statistics-examples.md)

+ [69.2.1. Dependências Funcionais](multivariate-statistics-examples.md#FUNCTIONAL-DEPENDENCIES)
+ [69.2.2. Contagem Múltipla N-Distanta](multivariate-statistics-examples.md#MULTIVARIATE-NDISTINCT-COUNTS)
+ [69.2.3. Listas de MCV](multivariate-statistics-examples.md#MCV-LISTS)

* [69.3. Planejamento Estatísticas e Segurança](planner-stats-security.md)

Este capítulo se baseia no material abordado em [Seção 14.1] e [Seção 14.2] para mostrar alguns detalhes adicionais sobre como o planejador usa as estatísticas do sistema para estimar o número de linhas que cada parte de uma consulta pode retornar. Esta é uma parte significativa do processo de planejamento, fornecendo grande parte da matéria-prima para o cálculo de custos.

O objetivo deste capítulo não é documentar o código em detalhes, mas sim apresentar uma visão geral de como ele funciona. Isso talvez facilite a curva de aprendizado para alguém que, posteriormente, queira ler o código.