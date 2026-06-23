## 2. Uma Breve História do PostgreSQL [#](#HISTORY)

* [2.1. O Projeto Berkeley POSTGRES](history.md#HISTORY-BERKELEY)
* [2.2. Postgres95](history.md#HISTORY-POSTGRES95)
* [2.3. PostgreSQL](history.md#HISTORY-POSTGRESQL)

O sistema de gerenciamento de banco de dados orientado a objetos, agora conhecido como PostgreSQL, é derivado do pacote POSTGRES escrito na Universidade da Califórnia em Berkeley. Com décadas de desenvolvimento por trás, o PostgreSQL é agora o banco de dados de código aberto mais avançado disponível em qualquer lugar.

Outra abordagem sobre a história apresentada aqui pode ser encontrada no artigo do Dr. Joe Hellerstein “Olhando para trás no Postgres” [[hell18]](biblio.md#HELL18).

### 2.1. O Projeto Berkeley POSTGRES [#](#HISTORY-BERKELEY)

O projeto POSTGRES, liderado pelo Professor Michael Stonebraker, foi patrocinado pela Agência de Projetos de Pesquisa Avançada de Defesa (DARPA), pelo Escritório de Pesquisa do Exército (ARO), pela Fundação Nacional de Ciência (NSF) e pela ESL, Inc. A implementação do POSTGRES começou em 1986. Os conceitos iniciais para o sistema foram apresentados em [[ston86]] e a definição do modelo de dados inicial apareceu em [[rowe87]] (biblio.md#ROWE87). O projeto do sistema de regras naquela época foi descrito em [[ston87a]] (biblio.md#STON87A). A justificativa e a arquitetura do gerenciador de armazenamento foram detalhadas em [[ston87b]] (biblio.md#STON87B).

O POSTGRES passou por várias versões importantes desde então. O primeiro sistema de "demoware" entrou em operação em 1987 e foi apresentado na Conferência ACM-SIGMOD de 1988. A versão 1, descrita em [[ston90a]](biblio.md#STON90A), foi lançada para alguns usuários externos em junho de 1989. Em resposta a uma crítica ao primeiro sistema de regras ([[ston89]](biblio.md#STON89)), o sistema de regras foi redesenhado ([[ston90b]](biblio.md#STON90B)) e a versão 2 foi lançada em junho de 1990 com o novo sistema de regras. A versão 3 apareceu em 1991 e adicionou suporte para vários gestores de armazenamento, um executor de consulta aprimorado e um sistema de regras reescrito. Na maior parte, as versões subsequentes até o Postgres95 (veja abaixo) focaram em portabilidade e confiabilidade.

O POSTGRES foi utilizado para implementar muitas aplicações de pesquisa e produção diferentes. Essas incluem: um sistema de análise de dados financeiros, um pacote de monitoramento de desempenho de motores a jato, um banco de dados de rastreamento de asteroides, um banco de dados de informações médicas e vários sistemas de informação geográfica. O POSTGRES também foi utilizado como uma ferramenta educacional em várias universidades. Finalmente, as Illustra Information Technologies (posteriormente incorporadas à [Informix](https://www.ibm.com/analytics/informix), que agora pertence à [IBM](https://www.ibm.com/)) adotaram o código e o comercializaram. No final de 1992, o POSTGRES tornou-se o gerente de dados principal para o projeto de computação científica Sequoia 2000 descrito em [[ston92]][(biblio.md#STON92)].

O tamanho da comunidade de usuários externos quase dobrou durante 1993. Tornou-se cada vez mais óbvio que a manutenção do código protótipo e o suporte estavam consumindo grandes quantidades de tempo que deveriam ter sido dedicados à pesquisa de banco de dados. Em um esforço para reduzir essa carga de suporte, o projeto Berkeley POSTGRES terminou oficialmente com a Versão 4.2.

### 2.2. Postgres95 [#](#HISTORY-POSTGRES95)

Em 1994, Andrew Yu e Jolly Chen adicionaram um interpretador de linguagem SQL ao POSTGRES. Posteriormente, sob um novo nome, o Postgres95 foi lançado na web para encontrar seu próprio caminho no mundo como um descendente de código aberto do original POSTGRES Berkeley.

O código do Postgres95 era completamente em ANSI C e reduzido em tamanho em 25%. Muitas mudanças internas melhoraram o desempenho e a manutenibilidade. O lançamento do Postgres95 1.0.x rodou cerca de 30–50% mais rápido no Wisconsin Benchmark em comparação com o POSTGRES, versão 4.2. Além das correções de bugs, as principais melhorias foram:

* O idioma de consulta PostQUEL foi substituído pelo SQL (implementado no servidor). (A biblioteca de interface [libpq](libpq.md "Chapter 32. libpq — C Library") recebeu o nome de PostQUEL.) Subconsultas não eram suportadas até o PostgreSQL (ver abaixo), mas podiam ser imitadas no Postgres95 com funções SQL definidas pelo usuário. As funções agregadas foram reimplementadas. O suporte à cláusula de consulta `GROUP BY` também foi adicionado.
* Um novo programa (psql) foi fornecido para consultas interativas de SQL, que utilizava o GNU Readline. Isso substituiu em grande parte o antigo programa de monitor.
* Uma nova biblioteca de interface de usuário, `libpgtcl`, suportou clientes baseados em Tcl. Um shell de amostra, `pgtclsh`, forneceu novos comandos Tcl para interfacear programas Tcl com o servidor Postgres95.
* A interface de objeto grande foi revisada. Os objetos inversos eram o único mecanismo para armazenar objetos grandes. (O sistema de arquivos inversão foi removido.)
* O sistema de regras de nível de instância foi removido. As regras ainda estavam disponíveis como regras de reescrita.
* Um breve tutorial introduzindo recursos regulares de SQL, bem como os do Postgres95, foi distribuído com o código-fonte.
* O GNU make (em vez do make BSD) foi usado para a construção. Além disso, o Postgres95 pôde ser compilado com um GCC não corrigido (o alinhamento de dados de duplos foi corrigido).

### 2.3. PostgreSQL [#](#HISTORY-POSTGRESQL)

Em 1996, ficou claro que o nome “Postgres95” não resistiria ao teste do tempo. Escolhemos um novo nome, PostgreSQL, para refletir a relação entre o POSTGRES original e as versões mais recentes com capacidade SQL. Ao mesmo tempo, definimos a numeração da versão para começar em 6.0, colocando os números de volta na sequência originalmente iniciada pelo projeto Berkeley POSTGRES.

Postgres ainda é considerado um nome oficial de projeto, tanto por tradição quanto porque as pessoas acham mais fácil pronunciar Postgres do que PostgreSQL.

A ênfase durante o desenvolvimento do Postgres95 foi identificar e entender os problemas existentes no código do servidor. Com o PostgreSQL, a ênfase mudou para aumentar recursos e capacidades, embora o trabalho continue em todas as áreas.

Detalhes sobre o que aconteceu em cada lançamento do PostgreSQL desde então podem ser encontrados em <https://www.postgresql.org/docs/release/>.