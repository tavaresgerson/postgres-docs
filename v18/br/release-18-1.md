## E.4. Versão 18.1 [#](#RELEASE-18-1)

* [E.4.1. Migração para a Versão 18.1](release-18-1.md#RELEASE-18-1-MIGRATION)
* [E.4.2. Alterações](release-18-1.md#RELEASE-18-1-CHANGES)

**Data de lançamento:** 2025-11-13

Esta versão contém uma variedade de correções do 18.0. Para informações sobre as novas funcionalidades na versão principal 18, consulte [Seção E.5](release-18.md).

### E.4.1. Migração para a Versão 18.1 [#](#RELEASE-18-1-MIGRATION)

Não é necessário fazer um descarte/restauração para aqueles que estão rodando a versão 18.X.

### E.4.2. Alterações [#](#RELEASE-18-1-CHANGES)

* Verifique os privilégios de `CREATE` no esquema em `CREATE STATISTICS` (Jelte Fennema-Nio) [§](https://postgr.es/c/00eb646ea)

Essa omissão permitiu que os proprietários de tabelas criassem estatísticas em qualquer esquema, o que poderia levar a conflitos inesperados de nomeação.

O Projeto PostgreSQL agradece a Jelte Fennema-Nio por relatar esse problema. (CVE-2025-12817)
* Evite o excesso de inteiros nos cálculos de tamanho de alocação dentro do libpq (Jacob Champion) [§](https://postgr.es/c/7eb8fcad8)

Vários lugares no libpq não foram suficientemente cuidadosos ao calcular o tamanho necessário de uma alocação de memória. Entradas suficientemente grandes poderiam causar overflow de inteiros, resultando em um buffer de tamanho insuficiente, o que, em seguida, levaria a escrever além do final do buffer.

O Projeto PostgreSQL agradece a Aleksey Solovev da Positive Technologies por relatar esse problema. (CVE-2025-12818)
* Evite erros de "tipo de nó não reconhecido" quando uma função SQL/JSON, como `JSON_VALUE` tem uma cláusula `DEFAULT` contendo uma expressão `COLLATE` (Jian He) [§](https://postgr.es/c/dc9125111) [§](https://postgr.es/c/1baae827e)
* Evite a otimização incorreta de cláusulas `HAVING` sem variáveis com conjuntos de agrupamento (Richard Guo) [§](https://postgr.es/c/40c242830) [§](https://postgr.es/c/ee49f2cf4)
* Não use paralelismo em junções semi-join de direita de hash (Richard Guo) [§](https://postgr.es/c/ef6168baf)

O caso não funciona de forma confiável devido a uma condição de corrida na atualização da tabela de hash compartilhada do join. * Evite a possível divisão por zero ao criar planos de anexação ordenada (Richard Guo) [§](https://postgr.es/c/500f64636)

Esse erro pode resultar na seleção incorreta do caminho mais barato ou em uma falha na asserção em builds de depuração.
* Falha no planejador com tipos de índice que podem realizar acesso ordenado, mas não varreduras apenas de índice (Maxime Schoemans) [§](https://postgr.es/c/74197bdc8)

Essa omissão resultou em erros como “não foram retornados dados para varredura apenas de índice”. O caso não ocorre com qualquer tipo de índice de núcleo, mas algumas extensões encontraram o problema.
* Remova a afirmação defeituosa na limpeza do índice btree (Peter Geoghegan) [§](https://postgr.es/c/61de81a49)
* Evite possíveis falhas de “tamanho inválido de solicitação de alocação de memória” ou “falha de memória fora de memória” durante a construção paralela do índice GIN (Tomas Vondra) [§](https://postgr.es/c/a26b753a0)
* Garanta que a auto-resumo do BRIN forneça um instantâneo para expressões de índice que precisam dele (Álvaro Herrera) [§](https://postgr.es/c/419ffde23) [§](https://postgr.es/c/8733f0b54)

Anteriormente, a auto-resumo falharia para tais índices e, em seguida, deixaria tuplas de índice de marcador, causando o inchaço do índice ao longo do tempo.
* Corrija o perigo de overflow de inteiro em varreduras de índice BRIN quando a tabela contém quase 232 páginas (Sunil S) [§](https://postgr.es/c/715983a81)

Essa falha pode resultar em um loop infinito ou em uma varredura de páginas de tabela desnecessárias.
* Consertar a extensão incorreta de zero dos valores armazenados no código de formação de tupla gerado pelo JIT (David Rowley) [§](https://postgr.es/c/ceb51d09b)

Quando não se utiliza JIT, o código equivalente não faz extensão de sinalização, o que leva a uma representação diferente do Datum dos tipos de dados de inteiro pequeno. Essa inconsistência foi mascarada na maioria dos casos, mas é conhecida por causar erros de "não foi possível encontrar a entrada da tabela de memoização" ao usar os nós do plano Memoize, e pode haver outros sintomas.
* Consertar o raro travamento ao processar consultas `GROUPING SETS` hasheadas (David Rowley) [§](https://postgr.es/c/0b6a02f03)
* Reparar a lógica de escolha de tamanho da tabela de hash em junções de hash (Tomas Vondra) [§](https://postgr.es/c/aa151022e)

As junções hash às vezes utilizavam mais memória do que o esperado ou não a dividiam de maneira eficiente.
* Melhore a lógica de busca de relação nas funções de manipulação estatística (Nathan Bossart) [§](https://postgr.es/c/c8af5019b) [§](https://postgr.es/c/15d7dded0)

Corrija `pg_restore_relation_stats()`, `pg_clear_relation_stats()`, `pg_restore_attribute_stats()` e `pg_clear_attribute_stats()` para verificar privilégios antes de adquirir bloqueio na relação de destino, em vez de depois.
* Corrija a lógica incorreta para cachear informações de relação de resultado para gatilhos (David Rowley, Amit Langote) [§](https://postgr.es/c/a2387c32f)

Em casos em que os conjuntos de colunas das partições não são fisicamente idênticos aos conjuntos de colunas das tabelas particionadas que os originam, essa omissão pode levar a falhas.
* Corrija falhas durante o recheck do EvalPlanQual em tabelas particionadas (David Rowley, Amit Langote) [§](https://postgr.es/c/1296dcf18)
* Corrija o tratamento do EvalPlanQual de junções externas ou personalizadas que não têm um plano de junção local alternativo preparado para EPQ (Masahiko Sawada, Etsuro Fujita) [§](https://postgr.es/c/b14144325)

Nesses casos, o método de acesso estrangeiro ou personalizado deve ser invocado normalmente, mas isso não aconteceu, levando tipicamente a um crash.
* Evite duplicar restrições de partição de hash durante `DETACH CONCURRENTLY` (Haiyang Li) [§](https://postgr.es/c/08c037dff)

`ALTER TABLE DETACH PARTITION CONCURRENTLY` foi escrito para adicionar uma cópia da restrição de particionamento à partição agora desconectada. Isso foi equivocado, parcialmente porque o `DETACH` não não-concorrente não faz isso, mas principalmente porque, no caso de particionamento por hash, a expressão da restrição contém referências ao OID da tabela pai. Isso causa problemas durante o dump/restore, ou se a tabela pai for eliminada após `DETACH`. Em v19 e versões posteriores, não criaremos mais nenhuma dessas restrições copiadas. Em ramos lançados, para minimizar o risco de consequências imprevisíveis, apenas pule a adição de uma restrição copiada se for para particionamento por hash.
* Não permita colunas geradas em chaves de partição (Jian He, Ashutosh Bapat) [§](https://postgr.es/c/ba99c9491)

Isso já não era permitido, mas o controle perdeu alguns casos, como quando a referência da coluna é implícita em uma referência de uma linha inteira.
* Não permita colunas geradas em cláusulas `COPY ... FROM ... WHERE` (Peter Eisentraut, Jian He) [§](https://postgr.es/c/0f9e0068b)

Anteriormente, o comportamento incorreto ou uma mensagem de erro obscura resultava ao tentar fazer referência a uma coluna desse tipo, pois as colunas geradas ainda não foram calculadas no ponto em que o filtro `WHERE` é feito.
* Evite definir uma coluna como identidade se ela tiver uma restrição não nula, mas a restrição estiver marcada como inválida (Jian He) [§](https://postgr.es/c/d9ffc2729)

As colunas de identidade devem ser não nulos, mas a verificação falhou em considerar esse caso específico.
* Evite o uso potencial de free após uso em vácuo em paralelo (Kevin Oommen Anish) [§](https://postgr.es/c/76613b539)

Esse erro parece não ter consequências em compilações padrão, mas, teoricamente, é um perigo.
* Considere a verificação de visibilidade para objetos de estatísticas em `pg_temp` (Noah Misch) [§](https://postgr.es/c/d024160ff)

Um objeto de estatísticas localizado em um esquema temporário não pode ser nomeado sem qualificação de esquema, mas `pg_statistics_obj_is_visible()` esqueceu essa nota e poderia retornar “true” independentemente. Por sua vez, funções como `pg_describe_object()` poderiam falhar em qualificar o nome do objeto conforme esperado.
* Consertar vazamento de memória menor durante a repetição do WAL da criação do banco de dados (Nathan Bossart) [§](https://postgr.es/c/33e7b4a7c)
* Consertar o relatório incorreto do atraso de replicação em `pg_stat_replication` (Fujii Masao) [§](https://postgr.es/c/9670032cc)

Se o LSN (Last Seen Timestamp) de qualquer servidor de espera parasse de avançar, as colunas `write_lag` e `flush_lag` eventualmente parariam de ser atualizadas.
* Evite mensagens de log duplicadas sobre configurações inválidas de `primary_slot_name` (Fujii Masao) [§](https://postgr.es/c/6ff7ba9fe)
* Evite falhas quando as referências `synchronized_standby_slots` de (https://postgr.es/c/b45a8d7d8) apontam para slots de replicação inexistentes
* Remova o arquivo de estado de slot inacabado após falhar em escrever o estado de um slot de replicação no disco (Michael Paquier) [§](https://postgr.es/c/9a6ea00ac)

Anteriormente, um erro como falta de espaço em disco resultava em deixar um arquivo temporário `state.tmp` para trás. Isso é problemático porque isso bloquearia todas as tentativas subsequentes de gravar o estado, exigindo intervenção manual para limpar.
* Consertar o mau manuseio de sinais de timeout de bloqueio em trabalhadores de aplicação paralela para replicação lógica (Hayato Kuroda) [§](https://postgr.es/c/37fc5de43)

O mesmo número de sinal estava sendo usado tanto para o desligamento do trabalhador quanto para o tempo limite de bloqueio, o que gerava confusão.
* Evite o desligamento indesejado do receptor WAL ao mudar de fonte WAL de streaming para arquivo (Xuneng Zhou) [§](https://postgr.es/c/a14201073)

Durante uma alteração no cronograma, o receptor WAL de um servidor de espera deve permanecer vivo, aguardando um novo ponto de início de transmissão WAL. Em vez disso, ele foi repetidamente desligado e imediatamente reiniciado, o que poderia confundir o código de monitoramento de status.
* Corrija o problema de uso após a liberação na cache de sincronização de relação mantida pelo plugin de decodificação lógica pgoutput (Vignesh C, Masahiko Sawada) [§](https://postgr.es/c/32b95fc71)

Um erro durante a decodificação lógica pode resultar em falhas em tentativas subsequentes de decodificação lógica na mesma sessão. O caso só é acessível quando o pgoutput é invocado através de funções SQL.
* Evite a invalidação desnecessária de slots de replicação lógica (Bertrand Drouvot) [§](https://postgr.es/c/bf3dba508)
* Reestabeleça o caso especial para a collation `C` na configuração do local (Jeff Davis) [§](https://postgr.es/c/3ebea75f9)

Isso corrige uma regressão no acesso a catálogos compartilhados no início do início do backend, antes de uma base de dados ter sido selecionada. Não se sabe se é um problema para qualquer código principal do PostgreSQL, mas algumas extensões foram quebradas.
* Corrija a impressão incorreta de mensagens sobre falhas na verificação de se o usuário tem privilégio de administrador do Windows (Bryan Green) [§](https://postgr.es/c/b48ae226e)

Esse código teria falhado ou, pelo menos, imprimido lixo. No entanto, não foram relatados casos como esse, indicando que a falha dessas chamadas de sistema é extremamente rara.
* Evitar falha ao tentar testar o PostgreSQL com certas opções do libsanitizer (Emmanuel Sibi, Jacob Champion) [§](https://postgr.es/c/6d8acb777)
* Corrigir os avisos falsos de verificação de contexto de memória em compilações de depuração no Windows de 64 bits (David Rowley) [§](https://postgr.es/c/af3a79e08)
* Lidar corretamente com `GROUP BY DISTINCT` em declarações de atribuição do PL/pgSQL (Tom Lane) [§](https://postgr.es/c/78a284b0b)

O analisador não conseguiu registrar a opção `DISTINCT` neste contexto, de modo que o comando agiria como se fosse uma simples `GROUP BY`.
* Evitar vazamento de memória ao lidar com um erro SQL dentro do PL/Python (Tom Lane) [§](https://postgr.es/c/447a794f6)

Isso corrige uma falha de vazamento de memória de duração de sessão introduzida em nossas versões menores anteriores.
* Correção do tratamento de erros relacionados a sockets do libpq no Windows dentro de sua lógica GSSAPI (Ning Wu, Tom Lane) [§](https://postgr.es/c/d83879a32)

O código para criptografar/descriptografar dados transmitidos usando GSSAPI não reconhecia corretamente as condições de erro no soquete de conexão, uma vez que o Windows reporta essas condições de forma diferente das outras plataformas. Isso levou ao fracasso na realização de conexões no Windows.
* Correção do descarte de restrições não herdadas não nulos em colunas de tabelas herdadas (Dilip Kumar) [§](https://postgr.es/c/0fe07fa11)

O pg_dump não conseguiu preservar tais restrições ao fazer o dumping de um servidor pré-v18. * Corrigir a ordenação das restrições de chave estrangeira pelo pg_dump (Álvaro Herrera) [§](https://postgr.es/c/162e70ea0)

Assegure a ordenação consistente desses objetos do banco de dados, como já foi feito para outros tipos de objetos.
* Repare erros variados na lógica de compressão de dados em pg_dump e pg_restore (Daniel Gustafsson, Tom Lane) [§](https://postgr.es/c/8980c724b) [§](https://postgr.es/c/6a4009747) [§](https://postgr.es/c/aa1fcd087)

O controle de erro estava ausente ou incorreto em vários lugares, e também havia problemas de portabilidade que se manifestariam em hardware big-endian. Esses problemas tinham sido ignorados porque esse código é usado apenas para ler arquivos TOC comprimidos dentro de dumps em formato de diretório. O pg_dump nunca produz tal dump; o caso pode ser alcançado apenas comprimindo manualmente o arquivo TOC após o fato, o que é uma coisa suportada, mas muito incomum. * Consertar o pgbench para sair limpo se uma operação `COPY` for iniciada (Anthonin Bonnefoy) [§](https://postgr.es/c/c00637b5f)

pgbench não pretende suportar esse caso, mas anteriormente ele entrou em um loop infinito.
* Correção do relatório de múltiplos erros do pgbench (Yugo Nagata) [§](https://postgr.es/c/29aabbc43)

Em casos em que duas chamadas consecutivas do `PQgetResult` falhem, o pgbench pode apresentar a mensagem de erro errada.
* Em pgbench, corrija a assertiva defeituosa sobre erros no modo de pipeline (Yugo Nagata) [§](https://postgr.es/c/c736808e0)
* Corrija a fuga de memória por arquivo em pg_combinebackup (Tom Lane) [§](https://postgr.es/c/e2072b47b)
* Garanta que as funções do `contrib/pg_buffercache` possam ser canceladas (Satyanarayana Narlapuram, Yuhang Qiu) [§](https://postgr.es/c/71aa2e114) [§](https://postgr.es/c/0beb7e933)

Alguns caminhos de código eram capazes de funcionar por um longo período sem verificar interrupções.
* Consertar as verificações de privilégios de `contrib/pg_prewarm` para índices (Ayush Vatsa, Nathan Bossart) [§](https://postgr.es/c/3ccf8e9ac) [§](https://postgr.es/c/c29d32d27)

`pg_prewarm()` exige privilégio `SELECT` nas relações para que sejam pré-aquecidas. No entanto, uma vez que os índices não têm privilégios SQL próprios, isso resultou em não-superusuários não conseguindo pré-aquecer índices. Em vez disso, verifique o privilégio `SELECT` na tabela do índice.
* Em `contrib/pg_stat_statements`, evite o travamento quando duas ou mais constantes são marcadas como tendo a mesma localização no texto da declaração SQL (Sami Imseih, Dmitry Dolgov) [§](https://postgr.es/c/b1635c166)
* Faça `contrib/pgstattuple` mais robusto em relação a páginas de índice vazias ou inválidas (Nitin Motiani) [§](https://postgr.es/c/fc295beb7)

Conte todas as páginas com todos os zeros como espaço livre e ignore as páginas que são inválidas de acordo com uma verificação do tamanho do espaço especial da página. O código para índices btree já contava todas as páginas com todos os zeros como livres, mas o código de hash e gist gerava erros, o que foi encontrado como muito menos amigável ao usuário. Da mesma forma, faça com que os três casos concordem em ignorar páginas corrompidas em vez de lançar erros.
* Fortaleça nossas macros de barreira de leitura e escrita para satisfazer o Clang (Thomas Munro) [§](https://postgr.es/c/f8ccab0e9)

Supusemos que `__atomic_thread_fence()` é uma barreira suficiente para impedir que o compilador C reordene os acessos de memória ao seu redor, mas parece que isso não é verdade para o Clang, permitindo que ele gere código incorreto para pelo menos as máquinas RISC-V, MIPS e LoongArch. Adicione barreiras explícitas ao compilador para corrigir isso.
* Considere corrigir a infraestrutura de construção do PGXS para suportar a construção de arquivos NLS `po` para extensões (Ryo Matsumura) [§](https://postgr.es/c/6aa04a60c)