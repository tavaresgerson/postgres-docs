## E.1. Versão 18.4 [#](#RELEASE-18-4)

* [E.1.1. Migração para a Versão 18.4](release-18-4.md#RELEASE-18-4-MIGRATION)
* [E.1.2. Alterações](release-18-4.md#RELEASE-18-4-CHANGES)

**Data de lançamento:** 2026-05-14

Esta versão contém uma variedade de correções da versão 18.3. Para informações sobre as novas funcionalidades da versão principal 18, consulte [Seção E.5](release-18.md).

### E.1.1. Migração para a Versão 18.4 [#](#RELEASE-18-4-MIGRATION)

Não é necessário fazer um descarte/restauração para aqueles que estão rodando a versão 18.X.

No entanto, se você está atualizando a partir de uma versão anterior à 18.2, consulte [Seção E.3](release-18-2.md).

### E.1.2. Alterações [#](#RELEASE-18-4-CHANGES)

* Evite a recursão ilimitada durante o processamento de pacotes de inicialização (Michael Paquier) [§](https://postgr.es/c/f7a191f53)

Um cliente malicioso poderia fazer o backend conectado falhar ao alternar entre solicitações de criptografia SSL e GSS rejeitadas indefinidamente.

O Projeto PostgreSQL agradece à Calif.io (em colaboração com Claude e Anthropic Research) por relatar esse problema. (CVE-2026-6479)
* Correção de possíveis transbordamentos de inteiros em cálculos de alocação de memória (Tom Lane, Nathan Bossart, Heikki Linnakangas) [§](https://postgr.es/c/e1c30458a) [§](https://postgr.es/c/01e568b8c) [§](https://postgr.es/c/f3cee4dc4) [§](https://postgr.es/c/dd8af778d) [§](https://postgr.es/c/55328e3a9) [§](https://postgr.es/c/67dd6243d) [§](https://postgr.es/c/8d1489d50) [§](https://postgr.es/c/c7fb9f765) [§](https://postgr.es/c/3fbec9e50)

Vários lugares não estavam atentos à possibilidade de excesso de inteiros em cálculos sobre quanto memória alocar. O excesso levaria a alocar um buffer muito pequeno, que o chamador então escreveria além do final. Isso causaria pelo menos falhas no servidor e, provavelmente, poderia ser explorado para execução de código arbitrário. Em muitos, mas não em todos os casos, o perigo existe apenas em compilações de 32 bits.

O Projeto PostgreSQL agradece ao Xint Code, Bruce Dang, Sven Klemm e Pavel Kohout por relatar esses problemas. (CVE-2026-6473)
* Citar adequadamente os nomes das assinaturas no pg_createsubscriber (Nathan Bossart) [§](https://postgr.es/c/c2e44c370)

O nome da assinatura fornecido foi inserido em comandos SQL sem aspas, de modo que uma injeção SQL pudesse ser realizada no caso (possivelmente improvável) de o nome da assinatura vir de uma fonte não confiável.

O Projeto PostgreSQL agradece a Yu Kunpeng por relatar esse problema. (CVE-2026-6476)
* Citar corretamente os nomes dos objetos em verificações de origem de replicação lógica (Pavel Kohout) [§](https://postgr.es/c/cb35d7306)

O esquema e os nomes das relações interpolados no `ALTER SUBSCRIPTION ... REFRESH PUBLICATION` foram inseridos nos comandos SQL sem serem citados, permitindo a execução de SQL arbitrário no provedor.

O Projeto PostgreSQL agradece a Pavel Kohout por relatar esse problema. (CVE-2026-6638)
* Rejeitar opções de comprimento excessivo em `ts_headline()` (Michael Paquier) [§](https://postgr.es/c/62ad26266)

As strings `StartSel`, `StopSel` e `FragmentDelimiter` não devem exceder 32 Kb de comprimento, mas isso não foi verificado. Um valor com comprimento excessivo geralmente causaria o crash do servidor.

O Projeto PostgreSQL agradece ao Xint Code por relatar esse problema. (CVE-2026-6473)
* Detectar entrada defeituosa ao restaurar estatísticas de atributo MCV (Michael Paquier) [§](https://postgr.es/c/661095c40)

As funções de restauração de estatísticas eram insuficientemente cuidadosas ao validar estatísticas de valor mais comum, e aceitavam valores que poderiam causar falhas no planejador mais tarde.

O Projeto PostgreSQL agradece a Jeroen Gui por relatar esse problema. (CVE-2026-6575)
* Proteja contra nomes de fuso horário maliciosos em `timeofday()` e `pg_strftime()` (Tom Lane) [§](https://postgr.es/c/ba27389c2) [§](https://postgr.es/c/c6e7a9ef3)

Uma configuração de fuso horário elaborada poderia passar sequências `%` para `snprintf()`, causando potencialmente falhas ou divulgação da memória do servidor. Outra via para resultados semelhantes era sobrecarregar o buffer de saída de tamanho limitado usado por `pg_strftime()`.

O Projeto PostgreSQL agradece ao Xint Code por relatar esse problema. (CVE-2026-6474) * Ao criar um tipo de intervalo múltiplo, certifique-se de que o usuário tenha o privilégio `CREATE` no esquema especificado para o tipo de intervalo múltiplo (Jelte Fennema-Nio) [§](https://postgr.es/c/a44780f41)

O tipo multirange pode ser colocado em um esquema diferente do seu tipo de intervalo principal, mas negligenciamos aplicar a verificação de privilégio necessária ao fazer isso.

O Projeto PostgreSQL agradece a Jelte Fennema-Nio por relatar esse problema. (CVE-2026-6472)
* Use comparações de string seguras em termos de tempo no código de autenticação (Michael Paquier) [§](https://postgr.es/c/d93ef4131)

Use `timingsafe_bcmp()` em vez de `memcpy()` ou `strcmp()` ao verificar senhas, hashes, etc. Não se sabe se a dependência de dados dessas funções é de fato explorável em algum desses lugares, mas por questões de segurança, substitua-as.

O Projeto PostgreSQL agradece a Joe Conway por relatar esse problema. (CVE-2026-6478)
* Marque `PQfn()` como inseguro e evite usá-lo dentro do libpq (Nathan Bossart) [§](https://postgr.es/c/be0136440)

Para um tipo de resultado não integral, `PQfn()` não recebe o tamanho do buffer de saída, portanto, não pode verificar se os dados retornados pelo servidor caberão. Portanto, um servidor malicioso poderia sobrescrever a memória do cliente. Isso não pode ser corrigido sem uma mudança na API, então marque a função como obsoleta. Internamente na libpq, use uma versão variante que possa aplicar a verificação que falta.

O Projeto PostgreSQL agradece a Yu Kunpeng e Martin Heistermann por relatar esse problema. (CVE-2026-6477)
* Evite a travessia de caminho em pg_basebackup e pg_rewind (Michael Paquier) [§](https://postgr.es/c/6a67c540a)

Essas aplicações não conseguiram validar os caminhos dos arquivos de saída lidos de seus arquivos de entrada, de modo que uma fonte maliciosa pudesse sobrescrever qualquer arquivo que essas aplicações pudessem escrever. Constrinja onde os dados podem ser escritos, rejeitando caminhos que são absolutos ou que contêm referências a diretórios parentais.

O Projeto PostgreSQL agradece à equipe XlabAI do Tencent Xuanwu Lab e a Valery Gubanov por relatar este problema. (CVE-2026-6475)
* Proteja-se contra o excesso de campo dentro dos tipos `contrib/intarray` de `query_int` e `contrib/ltree` (Tom Lane) [§](https://postgr.es/c/c5790ec4f) [§](https://postgr.es/c/05e73b5c3)

A análise dessas estruturas de consulta não verificou o excesso de campos de 16 bits, o que permitiu a construção de uma árvore de consulta inválida. Isso pode fazer o servidor falhar ao executar a consulta.

O Projeto PostgreSQL agradece ao Xint Code por relatar esse problema. (CVE-2026-6473)
* Proteja contra valores excessivamente longos do tipo `contrib/ltree` de `lquery` (Michael Paquier) [§](https://postgr.es/c/7f019f341)

Os valores com mais de 64K itens causaram transbordamentos internos, resultando potencialmente em falhas de pilha ou respostas erradas.

O Projeto PostgreSQL agradece ao Vergissmeinnicht, A1ex e ao Jihe Wang por relatar esse problema. (CVE-2026-6473)
* Evite injeção SQL e exaustão de buffer em `contrib/spi` (Nathan Bossart) [§](https://postgr.es/c/1ebda7da9)

`check_foreign_key()` não foi suficientemente cuidadoso ao citar valores-chave e também usou buffers de comprimento fixo para a construção de consultas. Embora este módulo seja apenas um código de exemplo, ainda assim não deve conter erros tão perigosos.

O Projeto PostgreSQL agradece a Nikolay Samokhvalov por relatar esse problema. (CVE-2026-6637)
* Verifique se há colatões não determinísticos antes de assumir que uma condição de igualdade em um tipo cotabilizável implica unicidade (Richard Guo) [§](https://postgr.es/c/e8fd5e579) [§](https://postgr.es/c/1132af22c) [§](https://postgr.es/c/5c214b58b) [§](https://postgr.es/c/b62f514ac) [§](https://postgr.es/c/bed3ffbf9)

Muitos otimizações de planejadores assumem, por exemplo, que, no máximo, uma linha de tabela pode satisfazer `WHERE x = 'abc'` se houver um índice único em `x`. No entanto, essa conclusão não é segura em geral se o índice e a cláusula `WHERE` tiverem colunas diferentes anexadas. É seguro quando ambas as colunas são determinísticas, porque essa propriedade essencialmente exige que a igualdade de duas strings signifique igualdade bit a bit. Mas as colunas não determinísticas não agem dessa maneira, portanto, otimizar com a suposição de correspondências únicas pode dar respostas erradas às consultas se a cláusula `WHERE` ou o índice tiver uma colocação não determinística.
* Corrigir a remoção incompleta de referências de relação em structs `RestrictInfo` durante a remoção de junção (Tom Lane) [§](https://postgr.es/c/16fb94605)

Essa omissão tem sido mostrada como resultando em falhas do planejador, como erros inesperados de "JOIN TOTAL só é suportado com condições de junção que podem ser mescladas ou que podem ser junções de hash". Isso também pode ter causado a falha em considerar planos válidos em outros casos.
* Melhorar a correspondência do planejador de colunas de chave de partição às saídas de sub-consulta (Richard Guo) [§](https://postgr.es/c/8e8b2bef7)

Remova as variáveis PlaceHolderVars sem ação antes de compará-las com chaves de partição. Essa mudança permite que o controle de poda de partição tenha sucesso em alguns casos em que anteriormente não conseguia reconhecer que uma partição não precisa ser analisada.
* Remoção de auto-conjunção para lidar com cláusulas de junção que são colunas booleanas vazias, por exemplo, `ON t1.boolcol` (Andrei Lepikhov, Tender Wang, Alexander Korotkov) [§](https://postgr.es/c/e8b9d6497)

Anteriormente, um caso semelhante gerava um erro de "nenhuma relação para a entrada de relid *`N`*".
* Consertar `UPDATE/DELETE ... WHERE CURRENT OF` para funcionar em tabelas com colunas geradas virtualmente (Satyanarayana Narlapuram, Dean Rasheed) [§](https://postgr.es/c/f3d03fbd5)
* Consertar a expansão das colunas geradas virtualmente em `EXCLUDED` em referências de coluna em `INSERT ... ON CONFLICT` (Satyanarayana Narlapuram, Dean Rasheed) [§](https://postgr.es/c/cf38dedf6)
* Consertar o tratamento incorreto das colunas geradas `NEW` em ações de regra e qualificações de regra (Richard Guo, Dean Rasheed) [§](https://postgr.es/c/e528bfe97)

Anteriormente, tais referências de coluna produziam NULL nos casos de `INSERT`, ou eram equivalentes ao valor de `OLD` nos casos de `UPDATE`.
* Corrija erros falsos de “índice em colunas geradas virtualmente não são suportados” (Robert Haas) [§](https://postgr.es/c/cceb9c18a)

A criação de um índice de expressão pode, às vezes, reportar incorretamente esse erro.
* Corrija erros falsos de "colunas geradas não são suportadas em condições de COPY FROM WHERE" (Tom Lane) [§](https://postgr.es/c/11c2c0cc8)

O uso de uma coluna de sistema em uma condição de `COPY FROM WHERE` poderia, às vezes, relatar incorretamente esse erro.
* Relatar corretamente uma falha de serialização quando o `MERGE` encontra um tuplo atualizado simultaneamente no modo de leitura repetitiva ou serializável (Tender Wang) [§](https://postgr.es/c/13fab378e)

Anteriormente, esses casos se comportavam da mesma forma que em níveis de isolamento mais baixos.
* Consertar `CREATE TABLE ... LIKE ... INCLUDING STATISTICS` para casos em que a tabela de origem perdeu colunas (Julien Tachoires) [§](https://postgr.es/c/149c875fc)

Nesses casos, objetos de estatísticas estendidos poderiam ser copiados incorretamente, ou o comando poderia dar um erro incorreto. * Permita que `ALTER INDEX ... ATTACH PARTITION` marque o índice pai como válido, se apropriado (Sami Imseih) [§](https://postgr.es/c/5713ac248)

Existem casos especiais em que um índice particionado pode permanecer marcado como inválido, mesmo quando todos os seus índices de folha são válidos. Essa mudança fornece um mecanismo pelo qual um usuário pode corrigir essa situação sem recorrer a atualizações manuais do catálogo.
* Corrija `ALTER TABLE ... SET NOT NULL` para invocar funções de gancho de acesso a objetos apenas após completar a mudança do catálogo (Artur Zakirov) [§](https://postgr.es/c/6958077ce)
* Corrija `ALTER FOREIGN DATA WRAPPER` para não descartar a dependência do objeto de revestimento em sua função de manipulador (Jeff Davis) [§](https://postgr.es/c/c11f87b1a)
* Corrija a perda de deferrabilidade dos gatilhos de chave estrangeira (Yasuo Honda) [§](https://postgr.es/c/5db5e3396)

Anteriormente, uma chave estrangeira definida como `DEFERRABLE INITIALLY DEFERRED` se comportaria como `NOT DEFERRABLE` após ser definida para o status `NOT ENFORCED` e, em seguida, de volta para `ENFORCED`.

Se você tiver uma chave estrangeira com esse problema, ela pode ser reparada (após instalar essa atualização) ao definir novamente para `NOT ENFORCED` e, em seguida, de volta para `ENFORCED`. * Repare `WITHOUT OVERLAPS` para permitir domínios (Jian He) [§](https://postgr.es/c/49f3cb453)

`UNIQUE/PRIMARY KEY ... WITHOUT OVERLAPS` exige que a coluna sem sobreposição seja um intervalo ou um multiintervalo, mas deve permitir um domínio sobre esse tipo também. * Não permitir que um tipo composto seja membro de si mesmo por meio de um multiintervalo (Heikki Linnakangas) [§](https://postgr.es/c/ff8f27d6e)

Já proibimos tais casos quando o tipo intermediário é um domínio, um array, um tipo composto ou uma faixa; mas as multifaixas foram negligenciadas.
* Fixar as comparações de dados-imagem para ser insensíveis às variações de extensão de sinal (David Rowley) [§](https://postgr.es/c/49315de0c)

Isso corrige algumas situações que anteriormente levavam a erros de "não foi possível encontrar a entrada da tabela de memoização" ou resultados de consulta errados.
* Corrija a lógica incorreta para `IN`/`NOT IN` com operador de igualdade não estrito (Chengpeng Yan) [§](https://postgr.es/c/035c520db)

O código anterior poderia falhar ou fornecer respostas erradas. Todos os tipos de dados embutidos têm operadores de igualdade estritos, de modo que esse problema só poderia surgir com um tipo de dados de extensão.
* Trate os símbolos numéricos específicos de localização excessivamente longos em `to_char()` (Tom Lane) [§](https://postgr.es/c/580e7be88)

Se um local especificar um símbolo de moeda, separador de milhares ou símbolo decimal ou de sinal com mais de 8 bytes, foi possível uma sobreposição de buffer. Não existem tais locais no mundo real, e é impraticável para um invasor não privilegiado instalar uma definição de local maliciosa sob um servidor Postgres; mas, por segurança, verifique os símbolos de comprimento excessivo e corte se necessário.
* Evite sobreposições de buffer ao analisar um arquivo de afix para um dicionário `Ispell` (Tom Lane) [§](https://postgr.es/c/00c6e0819) [§](https://postgr.es/c/c2bfeb3bb)

Um arquivo de aditivo corrupto ou malicioso pode fazer o servidor falhar. Isso não é considerado um problema de segurança, porque os arquivos de configuração de pesquisa de texto são considerados confiáveis, mas ainda assim parece ser uma correção que vale a pena fazer.
* Proteja contra o excesso de inteiros nos cálculos das posições de início e fim de quadro para agregados de janela (Richard Guo) [§](https://postgr.es/c/bfc7dff26)

Períodos de deslocamento muito grandes especificados pelo usuário (próximos a INT64_MAX) poderiam resultar em erros ou resultados de consulta incorretos.
* Considere `array_agg_array_combine()` para combinar os mapas de bits nulos dos arrays corretamente (Dmytro Astapov) [§](https://postgr.es/c/14bf2c39e)

Esse erro resultou em saída às vezes incorreta dos cálculos `array_agg(anyarray)` paralelos.
* Refaça `sync_file_range()` se ele retornar o código de erro `EINTR` (DaeMyung Kang) [§](https://postgr.es/c/6cb307251)
* Considere corrigir o comportamento incorreto de `pg_stat_reset_single_table_counters()` em um catálogo compartilhado (Chao Li) [§](https://postgr.es/c/b081c5b07)

Tais casos tiveram como efeito colateral o reajuste do `stat_reset_timestamp` do banco de dados atual, o que não era intencional.
* Atualize as estatísticas de atividade quando um trabalhador de aplicação paralela estiver parado (Zhijie Hou) [§](https://postgr.es/c/44c8dc280)

Anteriormente, as estatísticas de uma transação recentemente concluída podem não ser relatadas por longos intervalos, especialmente se a carga de trabalho for leve.
* Corrija a falha “sem entrada de relação para relid 0” ao estimar as longitudes do array em operações de conjunto (Tender Wang) [§](https://postgr.es/c/13e20d1c9)
* Corrija a leitura excessiva do buffer quando o `pglz_decompress()` recebe entrada corrupta (Andrew Dunstan) [§](https://postgr.es/c/c3e436b1c)

Foi possível ler alguns bytes além do final do input, o que, em casos muito maliciosos, pode causar um crash.
* Correção do processamento de tokens numéricos que atravessam os limites do buffer de entrada pelo parser incremental de JSON (Andrew Dunstan) [§](https://postgr.es/c/3e4955630)

Foi possível aceitar um número incorretamente formatado, o que levou a falhas mais tarde.
* Evite a visibilidade de mapas de relação de inchaço durante o restabelecimento de um backup incremental (Robert Haas) [§](https://postgr.es/c/9540c0e5d)

O Restore poderia adicionar muitos blocos de zeros a um mapa de visibilidade, devido ao cálculo incorreto do comprimento esperado do arquivo. Isso não resulta em corrupção de dados, mas pode desperdiçar uma quantidade substancial de espaço em disco.
* Use a collation C, não a collation padrão do banco de dados, nas consultas de cache de catálogo em colunas de texto (Jeff Davis) [§](https://postgr.es/c/03c4f243e)

Isso evita falhas em casos extremos, como o início da replicação física, onde não há um banco de dados identificado, de modo que não é possível determinar uma agregação padrão.
* Evite que os processos de trabalho de sincronização de slots bloqueados bloqueiem a promoção de um servidor de espera (Nisha Moond, Ajin Cherian) [§](https://postgr.es/c/58c1188a3) [§](https://postgr.es/c/acf49bfed) [§](https://postgr.es/c/94efd308b)

Um processo de trabalho que estava em vão esperando uma resposta do primário atrasaria a promoção por um período indevido de tempo.
* Corrija a saída excessiva de logs de processos de trabalho idle sync (Zhijie Hou) [§](https://postgr.es/c/540fe8fb5)
* Garanta que as estruturas de dados tuplestore sejam consistentes internamente mesmo após um erro (Tom Lane) [§](https://postgr.es/c/adb7873bb)

O código anteriormente não se preocupava com isso, o que é bom na maioria das vezes, mas é problemático para o `WITH HOLD` que suporta o cursor. Nas versões v15 e anteriores, isso leva a falhas facilmente reproduzíveis; as versões posteriores não são conhecidas por serem vulneráveis, mas parece melhor preservar a consistência em tudo.
* Faça com que a coluna `pid` da visão do sistema `pg_aios` mostre NULL e não 0 quando uma entrada não tem processo proprietário (ChangAo Chen) [§](https://postgr.es/c/882bdcf9f)
* Considere a reportagem prematura do atraso NULL no `pg_stat_replication` (Shinya Kato) [§](https://postgr.es/c/98e96e579)

As colunas de atraso frequentemente são lidas como NULL mesmo quando a atividade de replicação estava acontecendo.
* Correção da alocação insuficiente de memória compartilhada usada para varreduras de índice btree paralelo (Siddharth Kothari) [§](https://postgr.es/c/1e71970d2)

Em casos extremos, isso pode resultar em um travamento do servidor.
* Evite falha rara de esvaziamento ao trabalhar com índices GiST não registrados por WAL (Tomas Vondra) [§](https://postgr.es/c/5b3f63a1b)

Um índice GiST não registrado, contudo, às vezes pode produzir erros como “xlog flush request *`n/nnnn`* não é atendido” devido à seleção incorreta de um “LSN falso” para representar um ponto de inserção.
* Correção de subestimação do tamanho necessário dos mapas de páginas DSA para segmentos de tamanho ímpar (Paul Bunn) [§](https://postgr.es/c/a0f38604d)

Esse cálculo incorreto levou a acessos fora dos limites e, consequentemente, a falhas no servidor.
* Correção da indexação dos arrays multixact mais antigos na memória compartilhada (Yura Sokolov) [§](https://postgr.es/c/0a50ef094) [§](https://postgr.es/c/fa3b328e6)

Esse erro pode fazer com que os bloqueios de linha de uma transação preparada, mas ainda não comprometida, pareçam invisíveis para outras sessões, ou que outros problemas de visibilidade afetem os resultados dessa transação. Com um valor muito pequeno para max_connections, também foram possíveis erros de memória.
* Consertar o problema de excedente de matriz quando muitas opções de extensão `EXPLAIN` são instaladas (Joel Jacobson) [§](https://postgr.es/c/730c98d03)
* Consertar o possível travamento do servidor ao processar estatísticas extensas em expressões de tipos de dados de extensão (Michael Paquier) [§](https://postgr.es/c/83671c0da)

Os desvios de ponteiros nulos eram possíveis se a função typanalyze do tipo de dados não computasse estatísticas úteis. Nenhuma função de typanalyze no núcleo comporta essa maneira, mas extensões poderiam. * Exibir corretamente os aliases de junção Vars que são usados em `GROUP BY` (Tom Lane) [§](https://postgr.es/c/c2c1962a6)

Em visualizações que contêm consultas como `SELECT ... t1 LEFT JOIN t2 USING (x) GROUP BY x`, a cláusula `GROUP BY` pode ser exibida incorretamente por desestruturação, levando a falhas de descarte/restauração. As falhas ocorreram apenas se `t1.x` e `t2.x` não fossem do mesmo tipo de dados e `t1.x` fosse o lado que exigia uma coerção implícita.
* Consertar vazamentos de memória menores no processamento de strings baseado em ICU (Jeff Davis) [§](https://postgr.es/c/4abf63c62)
* Se o processo de inicialização falhar, desligue adequadamente outros processos filhos antes de sair do postmaster (Ayush Tiwari) [§](https://postgr.es/c/affdb2dd5)

O manejo dessa situação se baseava em uma suposição há muito obsoleta de que não existem outras crianças de postmaster enquanto o processo de inicialização está em execução, de modo que a saída imediata do postmaster seja aceitável. As crianças órfãs eventualmente perceberiam a morte e a saída do postmaster por conta própria, mas um procedimento de desligamento mais limpo é desejável. * Corrigir a condição de corrida entre o replay de pontos de verificação do WAL e as criações de IDs multixact (Heikki Linnakangas) [§](https://postgr.es/c/0852643e1)

Um servidor de espera que siga o WAL de um primário de uma versão menor pode entrar em um ciclo de falha e reinício, reclamando que "não conseguiu acessar o status da transação".
* Evite a espera indefinida na interrupção de um processo walsender (Anthonin Bonnefoy) [§](https://postgr.es/c/3eb2fecdb) [§](https://postgr.es/c/980498138)

Ao encerrar um clúster que está publicando dados de replicação lógica, o walsender aguarda que todos os WAL pendentes sejam escritos. Mas ele não solicitou corretamente que isso acontecesse, de modo que, em alguns casos, isso poderia se tornar uma espera indefinida.
* Garanta que as alterações nos mapas de espaço livre das tabelas sejam persistidas durante a recuperação (Alexey Makhmutov) [§](https://postgr.es/c/ac3b97db3)

Anteriormente, quando o replay WAL atualizava o mapa de espaço livre ao refazer operações que deveriam alterá-lo, o buffer da página do mapa não era marcado como sujo se as verificações de checksums estivessem ativadas, de modo que as alterações talvez nunca fossem escritas. Em um servidor de espera, com o tempo, isso resultaria em um mapa muito divergente dos conteúdos reais da tabela. Embora o mapa seja usado apenas como um indicativo, essa condição poderia causar uma degradação significativa do desempenho por um período de tempo após o servidor de espera ser promovido para ser ativo, até que a maioria do mapa tenha sido reparada por atualizações.
* Corrija falhas em algumas funções ecpg quando chamadas sem nenhuma conexão estabelecida (Shruthi Gowda) [§](https://postgr.es/c/e2688ea5e)
* Fortaleça a lógica de análise de arquivos tar contra arquivos que não pode manipular (Tom Lane) [§](https://postgr.es/c/698eae7db)

O código de leitura de arquivo tar usado em pg_basebackup e pg_verifybackup não conseguiu verificar se o arquivo de entrada é realmente um arquivo tar, quanto mais se encaixa no subconjunto de arquivos tar válidos que podemos manipular. Esse não é um problema para o cenário normal em que o arquivo de entrada foi gerado pelo código do PostgreSQL, mas pode ser um problema se o arquivo de entrada foi gerado por algum outro programa tar.
* Corrigir vários bugs na descompressão de backup e no código de análise de tar (Andrew Dunstan, Tom Lane, Chao Li) [§](https://postgr.es/c/5095f3f4a) [§](https://postgr.es/c/a01a592b1) [§](https://postgr.es/c/78dc9a808)

O código de leitura de arquivos de descompactação e de arquivos de xarope usado em pg_basebackup e pg_verifybackup maltratou os dados de preenchimento dos arquivos tar, poderia corromper os dados comprimidos LZ4 em casos extremos, não verificou algumas condições de erro incomuns, não saiu após erros de compressão/descompressão (levando a relatórios de erro em cascata) e vazou memória.
* Em pg_dump, preserve a propriedade `NO INHERIT` das restrições de `NOT NULL` (Jian He) [§](https://postgr.es/c/c3c8b63d7)

Alguns casos não imprimiam a cláusula `NO INHERIT`.
* Em pg_dumpall, não ignore os papéis `GRANT`s com OIDs de concedente pendente (Tom Lane) [§](https://postgr.es/c/b09158cc7)

Em vez disso, trate esses casos emitindo `GRANT` sem qualquer cláusula `GRANTED BY`, como fizemos antes da v16. Isso evita perder a concessão em casos previsíveis, uma vez que os servidores pré-v16 não impediram a perda do papel do concedente. Continue emitindo um aviso sobre o concedente ausente, mas apenas se o servidor de origem for da v16 ou posterior.
* Em pg_upgrade, tenha cuidado para usar a versão correta do protocolo ao se conectar a servidores de origem mais antigos (Jacob Champion) [§](https://postgr.es/c/1b2773179)

Isso pode ser problemático ao tentar fazer uma atualização a partir de um servidor anterior a 2018. * Em `contrib/basic_archive`, permita que o diretório de arquivo esteja ausente no início (Nathan Bossart) [§](https://postgr.es/c/bde9ad315)

Anteriormente, a configuração de `basic_archive.archive_directory` era rejeitada se não apontasse para um diretório existente. Isso é indesejável porque o arquivamento ficará preso indefinidamente, mesmo se o diretório aparecer mais tarde.
* Considere `contrib/ltree` para lidar com mudanças no comprimento de bytes de uma string ao dobrar letras maiúsculas e minúsculas (Jeff Davis) [§](https://postgr.es/c/b3c2a3d38) [§](https://postgr.es/c/53a57cae1)

Anteriormente, os padrões `lquery` que especificam correspondência sensível ao caso podem não corresponder às etiquetas que deveriam corresponder.
* Corrija a saída mal estruturada da opção `contrib/pg_overexplain` de `RANGE_TABLE` (Satyanarayana Narlapuram) [§](https://postgr.es/c/6723d462d)

Alguns campos estavam mal posicionados nos formatos JSON, YAML e XML, resultando em saída estruturalmente inválida.
* Em `contrib/pg_stat_statements`, não vazue memória se ocorrer um erro ao analisar o arquivo `pgss_query_texts.stat` (Heikki Linnakangas) [§](https://postgr.es/c/25b02320e)
* Em `contrib/postgres_fdw`, evite o travamento devido à limpeza prematura de uma conexão falha (Etsuro Fujita) [§](https://postgr.es/c/c318777da)

Se uma conexão remota falhar e abortar a limpeza, não podemos usá-la mais. Mas adiamos o fechamento do objeto de conexão até o final da transação, porque ainda pode haver referências a ele dentro de estruturas de dados, como cursors abertos.
* Atualize os arquivos de dados de fuso horário para a versão tzdata 2026b (Tom Lane) [§](https://postgr.es/c/8a431b6d6)

A Colúmbia Britânica (America/Vancouver) estará no UTC-07 (efetivamente, DST permanente) durante todo o ano, começando em novembro de 2026. Este lançamento assume que sua abreviação de TZ será `MST` a partir desse momento. Parece provável que isso mude, mas não está claro qual nova abreviação será usada. Além disso, uma correção histórica para a Moldávia: eles seguiram os tempos de transição da DST da UE desde 2022.