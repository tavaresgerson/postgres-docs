## 51.1. O Caminho de uma Consulta [#](#QUERY-PATH)

Aqui, damos uma breve visão geral das etapas que uma consulta deve passar para obter um resultado.

1. Uma conexão de um programa de aplicação ao servidor PostgreSQL deve ser estabelecida. O programa de aplicação transmite uma consulta ao servidor e espera receber os resultados enviados de volta pelo servidor.
2. A *fase de análise* verifica a consulta transmitida pelo programa de aplicação para a sintaxe correta e cria uma *árvore de consulta*.
3. O *sistema de reescrita* pega a árvore de consulta criada pela fase de análise e procura por quaisquer *regras* (armazenadas nos *catálogos do sistema*) para aplicar à árvore de consulta. Realiza as transformações dadas nos *corpos das regras*.

Uma aplicação do sistema de reescrita é na realização de *visões*. Sempre que uma consulta contra uma visão (ou seja, uma *tabela virtual*) é feita, o sistema de reescrita reescreve a consulta do usuário para uma consulta que acessa as *tabelas de base* dadas na *definição da visão* em vez disso.
4. O *planificador/opinião* pega a árvore de consulta (reescrita) e cria um *plano de consulta* que será a entrada para o *executor*.

Isso é feito, primeiro, criando todos os *caminhos* possíveis que levam ao mesmo resultado. Por exemplo, se houver um índice em uma relação a ser examinada, há dois caminhos para a varredura. Uma possibilidade é uma varredura sequencial simples e a outra possibilidade é usar o índice. Em seguida, o custo para a execução de cada caminho é estimado e o caminho mais barato é escolhido. O caminho mais barato é expandido em um plano completo que o executor pode usar.
5. O executor percorre recursivamente a *árvore de plano* e recupera as linhas da maneira representada pelo plano. O executor faz uso do *sistema de armazenamento* ao examinar as relações, realiza *sorts* e *joins*, avalia *qualificações* e, finalmente, devolve as linhas derivadas.

Nas seções a seguir, vamos cobrir cada um dos itens listados acima com mais detalhes para dar uma melhor compreensão dos controles internos e estruturas de dados do PostgreSQL.