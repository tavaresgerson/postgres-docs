## E.3. Versão 18.2 [#](#RELEASE-18-2)

* [E.3.1. Migração para a Versão 18.2](release-18-2.md#RELEASE-18-2-MIGRATION)
* [E.3.2. Alterações](release-18-2.md#RELEASE-18-2-CHANGES)

**Data de lançamento:** 2026-02-12

Esta versão contém uma variedade de correções da versão 18.1. Para informações sobre as novas funcionalidades da versão principal 18, consulte [Seção E.5](release-18.md).

### E.3.1. Migração para a Versão 18.2 [#](#RELEASE-18-2-MIGRATION)

Não é necessário fazer um descarte/restauração para aqueles que estão rodando a versão 18.X.

No entanto, se você tiver algum índice nas colunas `ltree`, pode ser necessário reindexá-las após a atualização. Veja a sexta entrada do changelog abaixo.

### E.3.2. Alterações [#](#RELEASE-18-2-CHANGES)

* Proteja contra dimensões inesperadas de `oidvector`/`int2vector` (Tom Lane) [§](https://postgr.es/c/3b6588cd9)

Espera-se que esses tipos de dados sejam matrizes unidimensionais que não contenham nulos, mas existem caminhos de conversão que permitem violar essas expectativas. Adicione verificações em algumas funções que dependiam dessas expectativas sem as verificar, e que poderiam se comportar mal como consequência.

O Projeto PostgreSQL agradece a Altan Birler por relatar esse problema. (CVE-2026-2003)
* Harden os estimadores de seletividade contra serem anexados a operadores que aceitam tipos de dados inesperados (Tom Lane) [§](https://postgr.es/c/66ddac698) [§](https://postgr.es/c/b69af3dda)

`contrib/intarray` continha uma função de estimativa de seletividade que poderia ser abusada para execução de código arbitrário, porque não verificava se sua entrada era do tipo de dados esperado. Extensões de terceiros devem verificar perigos semelhantes e adicionar defesas usando a técnica que a intarray agora usa. Como essas correções de extensão levam tempo, agora exigimos privilégio de superusuário para anexar um não embutido estimulador de seletividade a um operador.

O Projeto PostgreSQL agradece a Daniel Firer, como parte da zeroday.cloud, por relatar esse problema. (CVE-2026-2004)
* Correção de estouro de buffer nas funções de descriptografia PGP de `contrib/pgcrypto` (Michael Paquier) [§](https://postgr.es/c/209f387b8)

A descriptografia de uma mensagem elaborada com uma chave de sessão com comprimento excessivo causou uma sobreposição de buffer, com consequências tão ruins quanto a execução de código arbitrário.

O Projeto PostgreSQL agradece ao Team Xint Code, como parte da zeroday.cloud, por relatar esse problema. (CVE-2026-2005)
* Correção da validação inadequada de comprimentos de caracteres multibyte (Thomas Munro, Noah Misch) [§](https://postgr.es/c/df0852fe0) [§](https://postgr.es/c/efef05ba9) [§](https://postgr.es/c/7b5fc85be) [§](https://postgr.es/c/b0f5d25bc) [§](https://postgr.es/c/b42709194) [§](https://postgr.es/c/4543b02af)

Falhas variadas permitiram que um atacante emita SQL elaborado para sobrecarregar buffers de string, com consequências tão ruins quanto a execução de código arbitrário. Após essas correções, os aplicativos podem observar erros de "sequência de byte inválida para codificação" quando as funções de string processam texto inválido que foi armazenado no banco de dados.

O Projeto PostgreSQL agradece a Paul Gerste e Moritz Sanft, como parte da zeroday.cloud, por relatar este problema. (CVE-2026-2006) * Harden `contrib/pg_trgm` contra mudanças no comportamento de maiúsculas e minúsculas das strings (Heikki Linnakangas) [§](https://postgr.es/c/e0965fb1a) [§](https://postgr.es/c/18548681d)

Corrija possíveis excedentes de buffer decorrentes do fato de que, em alguns locais, a minificação de uma string pode produzir mais caracteres (não bytes) do que os originais. Esse comportamento é novo na versão 18, assim como o bug.

O Projeto PostgreSQL agradece a Heikki Linnakangas por relatar esse problema. (CVE-2026-2007)
* Consertar a correspondência inconsistente que não é sensível ao caso em `contrib/ltree` (Jeff Davis) [§](https://postgr.es/c/806555e30) [§](https://postgr.es/c/8993bf099)

As rotinas relacionadas ao índice em `ltree` utilizavam uma implementação diferente de dobramento de caracteres do que os operadores principais. Seu comportamento era equivalente apenas se o provedor de codificação padrão fosse libc e a codificação fosse de um único byte.

Para corrigir, altere o código para usar a codificação de maiúsculas e minúsculas com a collation padrão do banco de dados. Essa alteração exigirá a reindexação dos índices nas colunas `ltree` (independentemente do método de acesso ao índice), a menos que o banco de dados use libc como provedor de codificação e sua codificação seja de único byte. Sem isso, as pesquisas desses índices não conseguirão localizar entradas relevantes.
* Ao usar `ALTER TABLE ... ADD CONSTRAINT` para adicionar uma restrição não nula com um nome explícito, se a coluna já estiver marcada como NOT NULL, exija que o nome fornecido corresponda ao nome da restrição existente (Álvaro Herrera, Srinath Reddy Sadipiralla) [§](https://postgr.es/c/492a69e14)
* Não permita referências a CTE em subseleções para determinar níveis semânticos de funções agregadas (Tom Lane) [§](https://postgr.es/c/12bc32917)

Essa mudança anula uma mudança feita há duas versões menores, ao invés de lançar um erro se um subseleto fizer referência a um CTE que esteja abaixo do nível semântico que as regras padrão do SQL atribuiriam ao agregado com base em referências de coluna contidas e agregados. A tentativa de correção acabou por causar problemas por conta própria, e não está claro o que fazer em vez disso. Como os subseletos dentro dos agregados são totalmente proibidos pelo padrão SQL, tratar esses casos como erros parece ser suficiente.
* Fixar a captura da tabela de transição de gatilho para `MERGE` em consultas de CTE (Dean Rasheed) [§](https://postgr.es/c/c6ce4dcf9)

Quando executa uma consulta CTE que modifica dados, contendo tanto um `MERGE` quanto outra operação DML em uma tabela com gatilhos de nível de declaração `AFTER`, as tabelas de transição passadas aos gatilhos não incluirão as linhas afetadas pelo `MERGE`, apenas aquelas afetadas pela(s) outra(s) operação(ões).
* Corrija a poda incorreta de marcas de linha pertencentes a entradas de rangetable não relacionadas, como subconsultas (Dean Rasheed) [§](https://postgr.es/c/f335457e8)

Isso levou a resultados incorretos se uma atualização de linha proposta precisasse ser modificada pela revalidação do EvalPlanQual, como poderia acontecer se houvesse uma atualização concorrente nessa linha.
* Correção de falha quando todos os filhos de uma tabela de destino particionada de uma atualização ou exclusão foram eliminados (Amit Langote) [§](https://postgr.es/c/9f4b7bfc5)

Nesses casos, o executor poderia relatar erros de "não conseguiu encontrar a coluna ctid lixo", mesmo que não seja necessário fazer nada.
* Correção de erro de avaliação de expressão para um subseleto dentro de um índice de matriz (Andres Freund) [§](https://postgr.es/c/bdc5dedfc)
* Correção da busca de substring de texto para colchações não determinísticas (Laurenz Albe) [§](https://postgr.es/c/18b349315)

Ao usar uma ordenação não determinística, não conseguimos detectar uma correspondência que ocorre bem no final da string pesquisada. * Evite possíveis falhas do planejador quando uma consulta contém chamadas duplicadas de função de janela (Meng Zhang, David Rowley) [§](https://postgr.es/c/ccde5be68)

A confusão sobre a deduplicação dessas chamadas poderia resultar em erros como "WindowFunc com winref 2 atribuído a WindowAgg com winref 1".
* Consertar erro do planejador com funções que retornam um conjunto e agrupamento de conjuntos (Richard Guo) [§](https://postgr.es/c/382ce9cb7)

Ao construir um nó do plano ProjectSet, o planejador não conseguiu detectar que subexpressões envolvendo expressões de agrupamento já haviam sido calculadas pelo plano de entrada. Isso levou a planos ineficientes ou a erros, como "variável não encontrada na lista de alvos do subplano". * Evite otimização incorreta quando a cláusula de agrupamento de uma subconsulta contém uma função volátil ou que retorna um conjunto (Richard Guo) [§](https://postgr.es/c/7650eabb6)

O planejador estava disposto a reduzir as restrições de consulta externa que fazem referência a uma coluna desse agrupamento, o que levou a um comportamento incorreto devido à avaliação múltipla de uma função volátil, ou erros causados pela introdução de uma função que retorna um conjunto nas cláusulas `WHERE`/`HAVING` da subconsulta.
* Verifique os PlaceHolderVar quando estiver procurando estatísticas sobre uma expressão (Richard Guo) [§](https://postgr.es/c/7e9f852a7)

Essa mudança permite que o planejador encontre estatísticas relevantes sobre expressões extraídas de subconsultas ou usadas em `GROUP BY`, evitando voltar a uma estimativa padrão. (Provavelmente, devemos ajustar quaisquer estatísticas encontradas para levar em conta uma probabilidade aumentada de o valor ser NULL, mas nunca fizemos a coisa equivalente para Vars comuns também.) Embora essa restrição seja antiga, as mudanças na versão 18 do PostgreSQL tornaram os PlaceHolderVars mais comuns do que antes, então faça a mudança para evitar regreções no plano em casos afetados. * Não olhe para nós PlaceHolderVar sem ação ao combinar expressões com índices (Richard Guo) [§](https://postgr.es/c/b4cf74420)

Como a versão 18 do PostgreSQL usa PlaceHolderVars em mais casos do que antes, algumas consultas que anteriormente podiam usar um índice não conseguiram fazê-lo. Adicione lógica para evitar essa regressão.
* Conserte a conversão do `OR` do planejador em condições de índice ScalarArrayOp (Tender Wang, Tom Lane) [§](https://postgr.es/c/bf5b13a8a)

O código não tratou corretamente os nós RelabelType e poderia gerar expressões inválidas ou não realizar uma conversão válida.
* Permitir indexação em índices de hash parciais mesmo quando o predicado do índice implica a verdade da cláusula WHERE (Tom Lane) [§](https://postgr.es/c/a212877dc)

Normalmente, descartamos uma cláusula WHERE que é implícita pelo predicado, pois não faz sentido testá-la; ela deve ser válida para todas as entradas do índice. No entanto, isso pode impedir a criação de um plano de scan de índice se o índice for aquele que requer uma cláusula WHERE na chave do índice principal, como os índices de hash. Não descarte cláusulas implícitas ao considerar um índice desse tipo.
* Não emita WAL para índices BRIN não registrados (Kirill Reshke) [§](https://postgr.es/c/d77a5f981)

Um caminho de código raramente utilizado emitiu incorretamente um registro WAL relacionado a um índice BRIN, mesmo que o índice estivesse marcado como não registrado. A recuperação de falhas, então, falharia ao refazer esse registro, reclamando que o arquivo já existe. * Use a função correta de ordenação em construções paralelas de índices GIN (Tomas Vondra) [§](https://postgr.es/c/eee71a66c)

O código paralelo usou o operador de ordenação padrão (que é determinado pelo tipo de dados da coluna btree opclass), enquanto deveria usar a função de ordenação especificada pelo GIN opclass, se houver. Isso levou a um erro se o tipo de dados não tiver uma opclass btree, ou a um índice inválido se a opclass especificar uma função de ordenação que não esteja de acordo com a opclass btree.
* Evite o corte de CLOG que ainda é necessário para mensagens não lidas `NOTIFY` (Joel Jacobson, Heikki Linnakangas) [§][(https://postgr.es/c/321ec5462) [§][(https://postgr.es/c/7b069a187) [§][(https://postgr.es/c/82fa6b78d)

Essa correção impede os erros de "não foi possível acessar o status da transação" quando um backend é lento em absorver mensagens `NOTIFY`. * Escalar erros que ocorrem durante o processamento de mensagens `NOTIFY` para FATAL, ou seja, fechar a conexão (Heikki Linnakangas) [§](https://postgr.es/c/aab4a84bb)

Anteriormente, se um backend recebesse um erro ao absorver uma mensagem `NOTIFY`, ele avançaria além dessa mensagem, relataria o erro ao cliente e continuaria. Esse comportamento, no entanto, estava repleto de problemas. Uma grande preocupação é que o cliente não tenha uma boa maneira de saber que uma notificação foi perdida e, certamente, nenhuma maneira de saber o que estava nela. Dependendo da lógica do aplicativo, perder uma notificação poderia fazer com que o aplicativo ficasse preso esperando, por exemplo. Além disso, quaisquer mensagens restantes não seriam processadas até que alguém enviasse um novo `NOTIFY`.

Além disso, se a conexão estiver inativa no momento da recepção de um sinal `NOTIFY`, qualquer ERRO será escalado para FATAL de qualquer forma, devido a preocupações não relacionadas. Portanto, escolhemos fazer isso em todos os casos, por consistência e para fornecer um sinal claro ao aplicativo de que ele pode ter perdido algumas notificações.
* Considere agrupar expressões ao computar um hash de ID de consulta (Jian He) [§](https://postgr.es/c/9c3caad02)

Anteriormente, duas consultas que eram iguais, exceto nas expressões de `GROUP BY`, seriam unidas por `contrib/pg_stat_statements` e outros usuários dos IDs de consulta.
* Consertar o contagem errada de atualizações em `EXPLAIN ANALYZE MERGE` com uma atualização concorrente (Dean Rasheed) [§](https://postgr.es/c/5749d95d4)

Essa situação levou a um contagem incorreta de tuplas "saltadas" na saída do `EXPLAIN`, ou a uma falha na asserção em uma construção habilitada para asserção. * Corrigir o bug na cadeia de atualização seguinte ao bloquear uma tupla (Jasper Smit) [§](https://postgr.es/c/3e3a80f62)

Esse caminho de código negligenciou a verificação do xmin do primeiro novo tuplo na cadeia de atualização, tornando possível bloquear um tuplo não relacionado se o atualizador original abortar e o espaço for imediatamente recuperado por `VACUUM` e então reutilizado. Isso poderia causar atrasos inesperados na transação ou deadlocks. Erros associados à identificação do tuplo errado também foram observados.
* Consertar o tratamento incorreto de backups incrementais de tabelas grandes (Robert Haas, Oleg Tkachenko) [§](https://postgr.es/c/c80b0c9d6)

Se uma tabela que excede 1 GB (ou, de forma geral, o tamanho do segmento da instalação) for truncada por `VACUUM` entre o backup de base e o backup incremental, o pg_combinebackup pode falhar com um erro sobre “comprimento do bloco de truncação em excesso do tamanho do segmento”. Isso impediu a restauração do backup incremental.
* Corrija o potencial falha do processo de backend na saída do processo devido ao tentar liberar um bloqueio em um segmento de memória compartilhada que já não está mapeado (Rahila Syed) [§](https://postgr.es/c/1943ceb38)
* Corrija a condição de corrida no código de E/S assíncrona (Andres Freund) [§](https://postgr.es/c/7f1b3a4ce)

Era possível que o código de resultado de uma operação de E/S assíncrona fosse sobrescrito antes de ser obtido.
* Evite o corte incorreto do log multixact após um crash (Heikki Linnakangas) [§](https://postgr.es/c/09532a78b)
* Conserte o resultado possivelmente mal codificado de `pg_stat_get_backend_activity()` (Chao Li) [§](https://postgr.es/c/06907e864)

O buffer de memória compartilhada que contém a string de atividade de uma sessão pode terminar com um caractere multibyte incompleto. Os leitores devem cortar qualquer caractere incompleto desse tipo, mas essa função não conseguiu fazer isso.
* Proteja contra o registro recursivo do contexto de memória (Fujii Masao) [§](https://postgr.es/c/b863d8d87)

Um fluxo constante de sinais solicitando registro de contexto de memória pode causar a execução recursiva do código de registro, o que, em teoria, pode levar a um excesso de pilha.
* Correção do uso de contexto de memória ao reinicializar um contexto de execução paralela (Jakub Wartak, Jeevan Chalke) [§](https://postgr.es/c/57df5ab80)

Esse erro pode resultar em um travamento devido a uma estrutura de dados subsidiária ter uma vida útil mais curta do que o contexto paralelo. O problema não é conhecido por ser acessível apenas com o PostgreSQL principal, mas temos relatos de problemas em extensões.
* Defina o próximo deslocamento do multixid ao criar um novo multixid, para remover o loop de espera que era necessário em casos de esquina (Andrey Borodin) [§](https://postgr.es/c/e46041fd9) [§](https://postgr.es/c/02ba5e3be)

A lógica anterior pode ficar presa esperando uma atualização que nunca ocorreria.
* Evite reescrever CTEs que modificam dados mais de uma vez (Bernice Southey, Dean Rasheed) [§](https://postgr.es/c/b880d9a02)

Anteriormente, ao atualizar uma visão auto-atualizável ou uma relação com regras, se a consulta original tivesse quaisquer CTEs que modificassem dados, o reescritor reescreveria essas CTEs várias vezes devido à recursão. Isso era ineficiente e poderia produzir erros falsos se um CTE incluísse uma atualização de uma coluna sempre gerada.
* Permitir a tentativa de inicialização de uma entrada de registro do DSM (Nathan Bossart) [§](https://postgr.es/c/b83bcc0df)

Se falharmos durante a inicialização de uma entrada de memória compartilhada dinâmica, permita que a próxima tentativa use essa entrada para tentar a inicialização novamente. Anteriormente, a entrada era deixada em um estado permanentemente falhado.
* Evite a falha das visualizações de status NUMA quando uma página foi trocada (Tomas Vondra) [§](https://postgr.es/c/9796c4f56)
* Evite os erros de "operação não permitida" ao consultar o status da página NUMA com versões mais antigas do libnuma (Tomas Vondra) [§](https://postgr.es/c/482e98ac4)
* Falhe a recuperação se o WAL não existir de volta ao ponto de refazer indicado pelo registro do checkpoint (Nitin Jadhav) [§](https://postgr.es/c/68ebdf2b0)

Adicione uma verificação explícita para isso antes de iniciar a recuperação, para que não haja danos e uma mensagem de erro útil seja fornecida. Anteriormente, a recuperação poderia falhar ou corromper o banco de dados nessa situação. * Evite anotar na árvore da consulta de origem durante `ALTER PUBLICATION` (Sunil S) [§](https://postgr.es/c/bea57a6b4)

Esse erro teve o efeito visível de que um gatilho de evento para a consulta veria apenas a primeira opção `publish`, mesmo que várias tivessem sido especificadas. Se tal consulta fosse configurada como uma declaração preparada, as reexecuções também se comportariam mal. * As opções de conexão passadas em `CREATE SUBSCRIPTION ... CONNECTION` ao walsender do editor (Fujii Masao) [§](https://postgr.es/c/797fc5d1b)

Antes desta correção, a opção de conexão `options` (se houver) era ignorada, impedindo, por exemplo, a definição de valores personalizados de parâmetros do servidor na sessão do walsender. Era o que se pretendia, e funcionava antes de a refatoração na versão 15 do PostgreSQL a quebrar, então restaure o comportamento anterior.
* Evite a invalidação de slots de replicação recém-criados ou recém-sincronizados (Zhijie Hou) [§](https://postgr.es/c/919c9fa13) [§](https://postgr.es/c/1c60f7236) [§](https://postgr.es/c/d3ceb2084)

Uma condição de corrida com um ponto de verificação concorrente poderia permitir que o WAL seja removido, o que é necessário pelo intervalo de replicação, fazendo com que o intervalo seja imediatamente marcado como inválido.
* Consertar a condição de corrida na computação do xmin necessário para um intervalo de replicação (Zhijie Hou) [§](https://postgr.es/c/fd7c86cfa)

Isso pode levar ao erro “não é possível construir um snapshot inicial de slot, pois o xid mais antigo seguro segue o xmin do snapshot”.
* Durante a sincronização inicial de uma assinatura de replicação lógica, confirme a adição de uma entrada `pg_replication_origin` antes de começar a copiar dados (Zhijie Hou) [§](https://postgr.es/c/b07c32619)

Anteriormente, se a etapa de cópia falhasse, a nova entrada `pg_replication_origin` seria perdida devido ao rollback da transação. Isso levou a um estado inconsistente na memória compartilhada. * Não avance o progresso da replicação lógica após o fracasso de um aplicativo de trabalhador paralelo (Zhijie Hou) [§](https://postgr.es/c/2f7ffe124)

O comportamento anterior permitia que as transações fossem perdidas por um assinante.
* Consertar os processos de trabalho de replicação lógica slotsync para lidar corretamente com sinais LOCK_TIMEOUT (Zhijie Hou) [§](https://postgr.es/c/6c61c69d5)

Anteriormente, os sinais de timeout eram ignorados efetivamente.
* Consertar possível falha com "dados inesperados além do EOF" durante o reinício de um servidor de replicação em streaming (Anthonin Bonnefoy) [§](https://postgr.es/c/9ed411e08)
* Consertar o relatório de erro para desalinhamentos de tipo de caminho SQL/JSON (Jian He) [§](https://postgr.es/c/15ba0702c)

O código poderia produzir um erro de "busca de cache falhou para o tipo 0" em vez da reclamação pretendida sobre a expressão de caminho não ser do tipo certo.
* Correção do rastreamento errôneo da posição da coluna ao analisar os limites de alcance da partição (myzhen) [§](https://postgr.es/c/c35e5dd9a)

Isso pode, por exemplo, levar ao nome da coluna errada ser citado em mensagens de erro sobre a conversão de valores vinculados à partição para o tipo de dados da coluna.
* Corre diversos erros menores nas mensagens de erro (Man Zeng, Tianchen Zhang) [§](https://postgr.es/c/acfa422c3) [§](https://postgr.es/c/2ca4464b6) [§](https://postgr.es/c/ab61f0087) [§](https://postgr.es/c/69ee81932) [§](https://postgr.es/c/cff2ef984)

Por exemplo, um relatório de erro sobre número de linha de tempo incompatível em um manifesto de backup mostrou o número de linha de tempo inicial onde deveria mostrar o número de linha de tempo final.
* Corrigir a falha em realizar a função de inline quando se faz a compilação JIT com a versão 17 do LLVM ou posterior (Anthonin Bonnefoy) [§](https://postgr.es/c/f1c6b153c)
* Ajustar nosso código JIT para trabalhar com o LLVM 21 (Holger Hoffstätte) [§](https://postgr.es/c/912cfa314)

A codificação anterior não conseguiu compilar em máquinas aarch64.
* Corrija o código específico para aarch64 para construir com arquivos de cabeçalho de sistema antigos (RHEL7-era) (Tom Lane) [§](https://postgr.es/c/db4eba152) [§](https://postgr.es/c/6a5170755)
* Corrija a sonda de configuração incorreta para `io_uring_queue_init_mem()` (Masahiko Sawada) [§](https://postgr.es/c/640772c6d)

Esse erro resultou em falha na otimização das alocações de buffers de I/O assíncronos em compilações baseadas em autotools, embora o código funcionasse ao compilar com o meson. O principal impacto da omissão foi a saída do processo de backend mais lenta do que o necessário.
* Adicione o novo parâmetro do servidor [file_extend_method](runtime-config-resource.md#GUC-FILE-EXTEND-METHOD) para controlar o uso de `posix_fallocate()` (Thomas Munro) [§](https://postgr.es/c/33e3de6d7)

A versão 16 e posterior do PostgreSQL usará `posix_fallocate()`, se a plataforma o fornecer, para estender os arquivos de relação. No entanto, foi relatado que isso interage mal com alguns sistemas de arquivos: a compressão BTRFS é desativada pelo uso de `posix_fallocate()`, e o XFS pode produzir erros `ENOSPC` espúrios em versões mais antigas do kernel do Linux. Para fornecer uma solução, introduza este novo parâmetro do servidor. Definir `file_extend_method` para `write_zeros` fará com que o servidor retorne ao método antigo de extensão de arquivos, escrevendo blocos de zeros.
* Honre a bandeira `open()` do `O_CLOEXEC` no Windows (Bryan Green, Thomas Munro) [§](https://postgr.es/c/bebb281b0) [§](https://postgr.es/c/a7d06e74d) [§](https://postgr.es/c/4da5c33a3)

Faça com que essa bandeira funcione como na plataforma POSIX, para que não haja vazamento de identificadores de arquivo em processos filhos, como `COPY TO/FROM PROGRAM`. Embora essa vazamento não tenha causado muitos problemas, parece indesejável.
* Conserte a falha na análise de opções longas na linha de comando do servidor em executáveis Solaris construídos com meson (Tom Lane) [§](https://postgr.es/c/5eac1d68f)
* Suporte para mudanças de título de processo no GNU/Hurd (Michael Banck) [§](https://postgr.es/c/bcfca332f)
* Conserte o preenchimento de tabela do psql para valores das opções `VACUUM` (Yugo Nagata) [§](https://postgr.es/c/4e1376900)
* Nos prompts de comando do psql, não mostre um valor para `%P` (status de pipeline) quando não há conexão com o servidor (Chao Li) [§](https://postgr.es/c/d42735b1e)

Isso faz com que `%P` agira como outras sequências de escape de prompt cujos valores dependem da conexão ativa.
* A lógica do pg_dump para coletar valores de sequência (Nathan Bossart) [§](https://postgr.es/c/39d555576) [§](https://postgr.es/c/56e1f5010)

O pg_dump falhou se uma sequência foi descartada simultaneamente com o dump, mesmo que a sequência não estivesse entre os objetos do banco de dados a serem descartados. Além disso, se o usuário que está fazendo a chamada não tem privilégios para ler o valor de uma sequência, o pg_dump emitiu valores incorretos em vez de falhar como esperado.
* Corrija a citação potencialmente incorreta dos valores de `oauth_validator_libraries` pelo pg_dump (ChangAo Chen) [§](https://postgr.es/c/61c78e1f4)

O pg_dump aplicou a regra de citação errada se precisasse drenar um valor dessa configuração.
* Evite o erro de afirmação do pg_dump no modo de upgrade binário (Vignesh C) [§](https://postgr.es/c/573e679a2)

A falha na manipulação de objetos relacionados à assinatura no código de classificação de objetos desencadeou uma asserção, embora não houvesse efeitos graves na produção.
* Correção de erro incorreto no pgbench com múltiplos comandos `\syncpipeline` no modo de pipeline (Yugo Nagata) [§](https://postgr.es/c/00e64e35c)

Se forem encontrados vários comandos `\syncpipeline` após um erro de consulta, o pgbench informará que "não conseguiu sair do modo de pipeline", ou terá uma falha de afirmação em uma compilação habilitada para afirmação.
* Faça com que o pg_resetwal imprima o valor atualizado ao alterar OldestXID (Heikki Linnakangas) [§](https://postgr.es/c/19594271c)

Já fez isso para todas as outras variáveis que pode alterar.
* Faça com que pg_resetwal permita definir o próximo xid multixact como 0 ou o próximo deslocamento multixact como UINT32_MAX (Maxim Orlov) [§](https://postgr.es/c/8747b969f)

Esses são valores válidos, então rejeitá-los foi incorreto. No pior dos casos, se um pg_upgrade for tentado exatamente no ponto de envolvimento multixact, a atualização falharia.
* Em `contrib/amcheck`, use o snapshot correto para verificações de pais de índice btree (Mihail Nikalayeu) [§](https://postgr.es/c/df93f94dd) [§](https://postgr.es/c/3c83a2a0a)

A codificação anterior causava erros falsos ao examinar índices criados com `CREATE INDEX CONCURRENTLY`.
* Conserte `contrib/amcheck` para lidar corretamente com páginas de índice btree "meia-morta" (Heikki Linnakangas) [§](https://postgr.es/c/19e786727)

`amcheck` esperava que uma página desse tipo tivesse um downlink pai, mas não tem, o que leva a um relatório de erro falso sobre "desajuste entre a chave pai e a chave alta da criança".
* Considere `contrib/amcheck` para lidar corretamente com as divisões incompletas das páginas de raiz do btree (Heikki Linnakangas) [§](https://postgr.es/c/50c63ebb0)

`amcheck` poderia relatar um erro falso sobre “bloco não é verdadeiro raiz”.
* Consertar a alocação excessiva de memória em `contrib/pg_buffercache` (David Geier) [§](https://postgr.es/c/580b5c2f3)

O código alocou o dobro da memória que precisava para o status de página NUMA.
* Correção de overflow de inteiros em borda de caso no estimador de seletividade de `contrib/intarray` para `@@` (Chao Li) [§](https://postgr.es/c/07c1c6ec5)

Isso pode causar estimativas de seletividade precárias em casos que envolvem o valor inteiro máximo. * Correção de problema de codificação multiletra (multibyte) em `contrib/ltree` (Jeff Davis) [§](https://postgr.es/c/f79e239e0)

A codificação anterior poderia passar um caractere multibyte incompleto para `lower()`, provavelmente resultando em comportamento incorreto.
* Evite o travamento em `contrib/pg_stat_statements` quando uma lista de `IN` contém tanto constantes quanto expressões não constantes (Sami Imseih) [§](https://postgr.es/c/3304e97b1)
* Atualize os arquivos de dados de fuso horário para a versão 2025c do tzdata (Tom Lane) [§](https://postgr.es/c/6574bee64)

A única alteração é nos dados históricos para datas pré-1976 em Baja California.