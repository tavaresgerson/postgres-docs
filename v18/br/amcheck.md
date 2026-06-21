## F.1. amcheck — ferramentas para verificar a consistência de tabelas e índices [#](#AMCHECK)

* [F.1.1. Funções](amcheck.md#AMCHECK-FUNCTIONS)
* [F.1.2. Verificação opcional *`heapallindexed`*](amcheck.md#AMCHECK-OPTIONAL-HEAPALLINDEXED-VERIFICATION)
* [F.1.3. Uso eficaz do `amcheck`](amcheck.md#AMCHECK-USING-AMCHECK-EFFECTIVELY)
* [F.1.4. Reparo de corrupção](amcheck.md#AMCHECK-REPAIRING-CORRUPTION)

O módulo `amcheck` fornece funções que permitem verificar a consistência lógica da estrutura das relações.

As funções de verificação de B-Tree verificam vários *invariantes* na estrutura da representação de relações específicas. A correção dos métodos de acesso por trás de varreduras de índice e outras operações importantes depende desses invariantes sempre se mantiverem. Por exemplo, certas funções verificam, entre outras coisas, que todas as páginas de B-Tree têm itens em ordem "lógica" (por exemplo, para índices de B-Tree em `text`, os tuplos de índice devem estar em ordem lexicográfica coligada). Se esse invariante específico de alguma forma não se mantiver, podemos esperar que as pesquisas binárias na página afetada guiem incorretamente as varreduras de índice, resultando em respostas erradas às consultas SQL. Se a estrutura parecer válida, nenhum erro é exibido. Enquanto essas funções de verificação são executadas, o [search_path][(runtime-config-client.md#GUC-SEARCH-PATH)] é temporariamente alterado para `pg_catalog, pg_temp`.

A verificação é realizada utilizando os mesmos procedimentos utilizados pelos próprios varreduras de índice, que podem ser códigos de classe de operador definidos pelo usuário. Por exemplo, a verificação do índice B-Tree depende de comparações feitas com uma ou mais rotinas de função de suporte 1 do B-Tree. Consulte [Seção 36.16.3][(xindex.md#XINDEX-SUPPORT "36.16.3. Index Method Support Routines")] para obter detalhes sobre as funções de suporte de classe de operador.

Ao contrário das funções de verificação de árvore B que relatam a corrupção ao levantar erros, a função de verificação de pilha `verify_heapam` verifica uma tabela e tenta retornar um conjunto de linhas, uma linha por corrupção detectada. Apesar disso, se as instalações nas quais a `verify_heapam` depende forem corrompidas, a função pode não ser capaz de continuar e, em vez disso, levantar um erro.

A permissão para executar as funções do `amcheck` pode ser concedida a usuários não superusuários, mas, antes de conceder tais permissões, deve-se considerar cuidadosamente as preocupações com a segurança e a privacidade dos dados. Embora os relatórios de corrupção gerados por essas funções não se concentrem tanto nos conteúdos dos dados corrompidos quanto na estrutura desses dados e na natureza das corrupções encontradas, um atacante que obtém permissão para executar essas funções, especialmente se o atacante também puder induzir corrupção, pode ser capaz de inferir algo sobre os próprios dados a partir dessas mensagens.

### F.1.1. Funções [#](#AMCHECK-FUNCTIONS)

`bt_index_check(index regclass, heapallindexed boolean, checkunique boolean) returns void`: `bt_index_check` testa que seu alvo, um índice B-Tree, respeita uma variedade de invariantes. Exemplo de uso:

``` test=# SELECT bt_index_check(index => c.oid, heapallindexed => i.indisunique), c.relname, c.relpages FROM pg_index i JOIN pg_opclass op ON i.indclass[0] = op.oid JOIN pg_am am ON op.opcmethod = am.oid JOIN pg_class c ON i.indexrelid = c.oid JOIN pg_namespace n ON c.relnamespace = n.oid WHERE am.amname = 'btree' AND n.nspname = 'pg_catalog' -- Don't check temp tables, which may be from another session: AND c.relpersistence != 't' -- Function may throw an error when this is omitted: AND c.relkind = 'i' AND i.indisready AND i.indisvalid ORDER BY c.relpages DESC LIMIT 10; bt_index_check |             relname             | relpages ----------------+---------------------------------+---------- | pg_depend_reference_index       |       43 | pg_depend_depender_index        |       40 | pg_proc_proname_args_nsp_index  |       31 | pg_description_o_c_o_index      |       21 | pg_attribute_relid_attnam_index |       14 | pg_proc_oid_index               |       10 | pg_attribute_relid_attnum_index |        9 | pg_amproc_fam_proc_index        |        5 | pg_amop_opr_fam_index           |        5 | pg_amop_fam_strat_index         |        5 (10 rows)
    ```

Este exemplo mostra uma sessão que realiza a verificação dos 10 maiores índices do catálogo no banco de dados “test”. A verificação da presença de tuplas de heap como tuplas de índice é solicitada para o subconjunto que são índices exclusivos. Como não há erro, todos os índices testados parecem ser consistentes logicamente. Naturalmente, essa consulta poderia ser facilmente alterada para chamar `bt_index_check` para cada índice no banco de dados onde a verificação é suportada.

`bt_index_check` adquire um `AccessShareLock` no índice alvo e na relação de pilha a que pertence. Este modo de bloqueio é o mesmo modo de bloqueio adquirido em relações por declarações simples de `SELECT`. `bt_index_check` não verifica invariantes que abrangem relações de filho/pai, mas verificará a presença de todos os tuplos de pilha como tuplos de índice dentro do índice quando *`heapallindexed`* é `true`. Quando *`checkunique`* é `true` `bt_index_check` verificará que não há mais de um entre as entradas duplicadas em índice único que seja visível. Quando uma rotina, teste leve para corrupção é necessário em um ambiente de produção em tempo real, usando `bt_index_check` muitas vezes oferece a melhor combinação entre a profundidade da verificação e a limitação do impacto no desempenho e na disponibilidade da aplicação.

`bt_index_parent_check(index regclass, heapallindexed boolean, rootdescend boolean, checkunique boolean) returns void`: `bt_index_parent_check` testes que seu alvo, um índice B-Tree, respeita uma variedade de invariantes. Opcionalmente, quando o argumento *`heapallindexed`* é `true`, a função verifica a presença de todos os tuplos de heap que devem ser encontrados dentro do índice. Quando *`checkunique`* é `true`, `bt_index_parent_check` verificará que não mais de um entre as entradas duplicadas em um índice único é visível. Quando o argumento opcional *`rootdescend`* é `true`, a verificação refaz os tuplos no nível de folha, realizando uma nova busca a partir da página raiz para cada tupla. Os verificações que podem ser realizadas por `bt_index_parent_check` são um subconjunto das verificações que podem ser realizadas por `bt_index_check`. `bt_index_parent_check` pode ser considerado uma variante mais completa de `bt_index_check`: ao contrário de `bt_index_check`, `bt_index_parent_check` também verifica invariantes que abrangem relações pai/filho, incluindo a verificação de que não há links de baixo faltando na estrutura do índice. `bt_index_parent_check` segue a convenção geral de levantar um erro se encontrar uma inconsistência lógica ou outro problema.

É necessário um `ShareLock` no índice alvo pelo `bt_index_parent_check` (um `ShareLock` também é adquirido na relação de pilha). Esses bloqueios impedem a modificação de dados concorrente dos comandos `INSERT`, `UPDATE` e `DELETE`. Os bloqueios também impedem que a relação subjacente seja processada concorrentemente pelo `VACUUM`, bem como todos os outros comandos utilitários. Note que a função mantém os bloqueios apenas enquanto está em execução, não para toda a transação.

A verificação adicional do `bt_index_parent_check` é mais provável de detectar vários casos patológicos. Esses casos podem envolver uma classe de operador B-Tree implementada incorretamente usada pelo índice que está sendo verificado, ou, hipoteticamente, bugs não descobertos no código do método de acesso ao índice B-Tree subjacente. Note que o `bt_index_parent_check` não pode ser usado quando o modo de espera quente está habilitado (ou seja, em réplicas físicas somente de leitura), ao contrário do `bt_index_check`.

`gin_index_check(index regclass) returns void`: `gin_index_check` testa que o índice GIN alvo tenha relações consistentes de tuplas pai-filho (nenhuma tupla pai requer ajuste de tupla) e que o gráfico de página respeite os invariantes de árvore balanceada (páginas internas referenciam apenas a página de folha ou apenas páginas internas).

### DICA

`bt_index_check` e `bt_index_parent_check` emitem mensagens de log sobre o processo de verificação em níveis de gravidade `DEBUG1` e `DEBUG2`. Essas mensagens fornecem informações detalhadas sobre o processo de verificação que podem ser de interesse para os desenvolvedores do PostgreSQL. Usuários avançados também podem achar essa informação útil, pois fornece contexto adicional caso a verificação realmente detecte uma inconsistência.

```
SET client_min_messages = DEBUG1;
```

Em uma sessão interativa do psql, antes de executar uma consulta de verificação, serão exibidas mensagens sobre o progresso da verificação com um nível gerenciável de detalhes.

`verify_heapam(relation regclass, on_error_stop boolean, check_toast boolean, skip text, startblock bigint, endblock bigint, blkno OUT bigint, offnum OUT integer, attnum OUT integer, msg OUT text) returns setof record`: Verifica uma tabela, sequência ou visão materializada quanto à corrupção estrutural, onde as páginas na relação contêm dados formatados de forma inválida, e quanto à corrupção lógica, onde as páginas são estruturalmente válidas, mas inconsistentes com o resto do clúster do banco de dados.

Os seguintes argumentos opcionais são reconhecidos:

`on_error_stop` :   Se verdadeiro, a verificação de corrupção para para no final do primeiro bloco em que quaisquer corrupções forem encontradas.

Padrão por padrão é falso.

`check_toast` :   Se verdadeiro, os valores torrados são verificados contra a tabela TOAST da relação alvo.

Esta opção é conhecida por ser lenta. Além disso, se a tabela de torradas ou seu índice estiver corrompido, verificá-lo em relação aos valores de torradas poderia, teoricamente, fazer o servidor falhar, embora, na maioria dos casos, isso apenas produza um erro.

Padrão por padrão é falso.

`skip` :   Se não for `none`, a verificação de corrupção pula blocos que estão marcados como totalmente visíveis ou totalmente congelados, conforme especificado. As opções válidas são `all-visible`, `all-frozen` e `none`.

Padrão para `none`.

`startblock` :   Se especificado, o controle de corrupção começa no bloco especificado, ignorando todos os blocos anteriores. É um erro especificar um *`startblock`* fora da faixa de blocos na tabela de destino.

Por padrão, a verificação começa no primeiro bloco.

`endblock` :   Se especificado, o controle de corrupção termina no bloco especificado, ignorando todos os blocos restantes. É um erro especificar um *`endblock`* fora da faixa de blocos na tabela de destino.

Por padrão, todos os blocos são verificados.

Para cada corrupção detectada, `verify_heapam` retorna uma linha com as seguintes colunas:

`blkno` :   O número do bloco que contém a página corrupta.

`offnum` :   O Número de Deslocamento do par ordenado corrupto.

`attnum` :   O número do atributo da coluna corrupta na tupla, se a corrupção for específica de uma coluna e não da tupla como um todo.

`msg` :   Uma mensagem descrevendo o problema detectado.

### F.1.2. Verificação opcional *`heapallindexed`* [#](#AMCHECK-OPTIONAL-HEAPALLINDEXED-VERIFICATION)

Quando o argumento *`heapallindexed`* para as funções de verificação de B-Tree é `true`, uma fase adicional de verificação é realizada contra a tabela associada à relação do índice alvo. Isso consiste em uma operação de “falsa” `CREATE INDEX CONCURRENTLY`, que verifica a presença de todos os hipotéticos novos tuplos de índice contra uma estrutura resumida temporária em memória (esta é construída quando necessário durante a primeira fase básica de verificação). A estrutura resumida “digitaliza” cada tupla encontrada dentro do índice alvo. O princípio de alto nível por trás da verificação de *`heapallindexed`* é que um novo índice que é equivalente ao índice existente e alvo deve ter apenas entradas que podem ser encontradas na estrutura existente.

A fase adicional *`heapallindexed`* adiciona um custo significativo: a verificação geralmente leva vários tempos. No entanto, não há alteração nas bloqueadoras de nível de relação adquiridas quando a verificação *`heapallindexed`* é realizada.

A estrutura resumida é limitada em tamanho por `maintenance_work_mem`. Para garantir que não haja mais de uma probabilidade de 2% de falha na detecção de uma inconsistência para cada tupla de pilha que deve ser representada no índice, são necessários aproximadamente 2 bytes de memória por tupla. À medida que menos memória é disponibilizada por tupla, a probabilidade de não detectar uma inconsistência aumenta lentamente. Essa abordagem limita significativamente o custo de verificação, ao mesmo tempo em que reduz apenas ligeiramente a probabilidade de detectar um problema, especialmente para instalações onde a verificação é tratada como uma tarefa de manutenção de rotina. Qualquer tupla ausente ou malformada tem uma nova oportunidade de ser detectada em cada nova tentativa de verificação.

### F.1.3. Usando `amcheck` de forma eficaz [#](#AMCHECK-USING-AMCHECK-EFFECTIVELY)

`amcheck` pode ser eficaz na detecção de vários tipos de modos de falha que os (app-initdb.md#APP-INITDB-DATA-CHECKSUMS) de verificação de dados não conseguem detectar. Esses incluem:

* Inconsistências estruturais causadas por implementações incorretas da classe do operador.

Isso inclui problemas causados pelas regras de comparação das colatações do sistema operacional que mudam. As comparações de datas de um tipo de colável como `text` devem ser imutáveis (assim como todas as comparações usadas para varreduras de índice B-Tree devem ser imutáveis), o que implica que as regras de colatação do sistema operacional nunca devem mudar. Embora sejam raras, as atualizações das regras de colatação do sistema operacional podem causar esses problemas. Mais comumente, uma inconsistência na ordem de colatação entre um servidor principal e um servidor de reserva é implicada, possivelmente porque a versão *principal* do sistema operacional em uso é inconsistente. Tais inconsistências geralmente surgem apenas em servidores de reserva, e, portanto, geralmente só podem ser detectadas em servidores de reserva.

Se um problema como esse surgir, ele pode não afetar cada índice individual que é ordenado usando uma codificação afetada, simplesmente porque os valores *indexados* podem ter a mesma ordem absoluta, independentemente da inconsistência comportamental. Veja [Seção 23.1][(locale.md "23.1. Locale Support")] e [Seção 23.2][(collation.md "23.2. Collation Support")] para mais detalhes sobre como o PostgreSQL usa locais e codificações do sistema operacional.
* Incoerências estruturais entre índices e as relações de pilha que são indexadas (quando a verificação *`heapallindexed`* é realizada).

Não há verificação cruzada de índices em relação à sua relação de pilha durante o funcionamento normal. Os sintomas de corrupção de pilha podem ser sutis. * Corrupção causada por bugs hipotéticos não descobertos no código do método de acesso subjacente do PostgreSQL, código de classificação ou código de gerenciamento de transações.

A verificação automática da integridade estrutural dos índices desempenha um papel no teste geral de novos ou propostos recursos do PostgreSQL que possam, de forma plausível, permitir a introdução de uma inconsistência lógica. A verificação da estrutura da tabela e das informações associadas à visibilidade e ao status de transação desempenha um papel semelhante. Uma estratégia de teste óbvia é chamar as funções `amcheck` continuamente ao executar os testes de regressão padrão. Consulte [Seção 31.1][(regress-run.md "31.1. Running the Tests")] para obter detalhes sobre a execução dos testes.
* Falhas no sistema de arquivos ou no subsistema de armazenamento quando as verificações de checksum de dados estão desativadas.

Observe que `amcheck` examina uma página conforme representada em algum buffer de memória compartilhada no momento da verificação, se houver apenas um achado de buffer compartilhado ao acessar o bloco. Consequentemente, `amcheck` não necessariamente examina os dados lidos do sistema de arquivos no momento da verificação. Observe que, quando as verificações de checksum estão habilitadas, `amcheck` pode gerar um erro devido a uma falha de checksum quando um bloco corrupto é lido em um buffer. * Corrupção causada por RAM defeituosa ou pelo subsistema de memória mais amplo.

O PostgreSQL não protege contra erros de memória corrigíveis e se assume que você operará com RAM que utiliza Códigos de Correção de Erros (ECC) padrão da indústria ou uma proteção melhor. No entanto, a memória ECC geralmente é imune apenas a erros de um bit e não deve ser assumida que ela ofereça proteção *absoluta* contra falhas que resultem em corrupção de memória.

Quando a verificação de *`heapallindexed`* é realizada, geralmente há uma chance muito maior de detectar erros de único bit, uma vez que a igualdade binária estrita é testada e os atributos indexados dentro do heap são testados.

A corrupção estrutural pode ocorrer devido a um hardware de armazenamento defeituoso ou a arquivos de relação serem sobrescritos ou modificados por software não relacionado. Esse tipo de corrupção também pode ser detectado com [checksums de página de dados][(checksums.md "28.2. Data Checksums")].

Páginas de relação que estão corretamente formatadas, consistentes internamente e corretas em relação às suas próprias verificações internas podem ainda conter corrupção lógica. Como tal, esse tipo de corrupção não pode ser detectado com verificações. Exemplos incluem valores torrados na tabela principal que não possuem uma entrada correspondente na tabela de torra, e tuplas na tabela principal com um ID de Transação que é mais antigo que o ID de Transação mais antigo válido no banco de dados ou no clúster.

Foram observadas várias causas de corrupção lógica nos sistemas de produção, incluindo erros no software do servidor PostgreSQL, ferramentas de backup e restauração defeituosas e mal conceituadas, e erros do usuário.

As relações corruptas são as mais preocupantes em ambientes de produção ao vivo, exatamente os mesmos ambientes onde as atividades de alto risco são menos bem-vindas. Por essa razão, o `verify_heapam` foi projetado para diagnosticar corrupção sem risco indevido. Ele não pode proteger contra todas as causas de falhas no backend, pois até mesmo a execução da consulta de chamada pode ser insegura em um sistema mal corrupto. O acesso às (catalogs-overview.md "52.1. Overview") das tabelas do catálogo é realizado e pode ser problemático se os próprios catálogos estiverem corrompidos.

Em geral, `amcheck` só pode comprovar a presença de corrupção; não pode comprovar sua ausência.

### F.1.4. Reparo de corrupção [#](#AMCHECK-REPAIRING-CORRUPTION)

Nenhum erro relacionado à corrupção levantado por `amcheck` nunca deve ser um falso positivo. `amcheck` levanta erros no caso de condições que, por definição, nunca devem ocorrer, e, portanto, uma análise cuidadosa dos erros de `amcheck` é frequentemente necessária.

Não há um método geral para reparar problemas que o `amcheck` detecta. Deve-se buscar uma explicação para a causa raiz de uma violação invariável. O (pageinspect.md "F.23. pageinspect — low-level inspection of database pages") pode desempenhar um papel útil no diagnóstico de corrupção que o `amcheck` detecta. O `REINDEX` pode não ser eficaz para reparar a corrupção.