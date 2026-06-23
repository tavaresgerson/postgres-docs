## 39.1. A Árvore de Consulta [#](#QUERYTREE)

Para entender como o sistema de regras funciona, é necessário saber quando ele é invocado e quais são seus insumos e resultados.

O sistema de regras está localizado entre o analisador e o planejador. Ele recebe a saída do analisador, uma árvore de consulta e as regras de reescrita definidas pelo usuário, que também são árvores de consulta com algumas informações adicionais, e cria zero ou mais árvores de consulta como resultado. Portanto, sua entrada e saída são sempre coisas que o próprio analisador poderia ter produzido e, portanto, qualquer coisa que ele vê é basicamente representável como uma declaração SQL.

Agora, o que é uma árvore de consulta? É uma representação interna de uma declaração SQL na qual as partes individuais de que é composta são armazenadas separadamente. Essas árvores de consulta podem ser exibidas no log do servidor se você definir os parâmetros de configuração `debug_print_parse`, `debug_print_rewritten` ou `debug_print_plan`. As ações das regras também são armazenadas como árvores de consulta, no catálogo do sistema `pg_rewrite`. Elas não são formatadas como a saída do log, mas contêm exatamente as mesmas informações.

Ler uma árvore de consulta bruta requer alguma experiência. Mas, como as representações SQL das árvores de consulta são suficientes para entender o sistema de regras, este capítulo não ensinará como lê-las.

Ao ler as representações SQL das árvores de consulta neste capítulo, é necessário ser capaz de identificar as partes em que a declaração é dividida quando está na estrutura da árvore de consulta. As partes de uma árvore de consulta são

o tipo de comando: Este é um valor simples que indica qual comando (`SELECT`, `INSERT`, `UPDATE`, `DELETE`) produziu a árvore de consulta.

a tabela de intervalo: A tabela de intervalo é uma lista de relações que são utilizadas na consulta. Em uma declaração `SELECT`, essas são as relações fornecidas após a palavra-chave `FROM`.

Cada entrada da tabela de intervalo identifica uma tabela ou visão e indica pelo qual nome ela é chamada nas outras partes da consulta. Na árvore de consulta, as entradas da tabela de intervalo são referenciadas por número, em vez de por nome, então aqui não importa se há nomes duplicados, como aconteceria em uma declaração SQL. Isso pode acontecer após as tabelas de intervalo das regras terem sido unidas. Os exemplos deste capítulo não terão essa situação.

a relação de resultado: Este é um índice na tabela de intervalo que identifica a relação onde os resultados da consulta são enviados.

As consultas do `SELECT` não têm uma relação de resultado. (O caso especial do `SELECT INTO` é, na maioria das vezes, idêntico ao `CREATE TABLE`, seguido por `INSERT ... SELECT`, e não é discutido separadamente aqui.)

Para os comandos `INSERT`, `UPDATE` e `DELETE`, a relação de resultado é a tabela (ou a visualização!) onde as alterações devem entrar em vigor.

a lista de alvos: A lista de alvos é uma lista de expressões que definem o resultado da consulta. No caso de um `SELECT`, essas expressões são as que constroem a saída final da consulta. Elas correspondem às expressões entre as palavras-chave `SELECT` e `FROM`. (`*` é apenas uma abreviação para todos os nomes das colunas de uma relação. É expandido pelo analisador em colunas individuais, então o sistema de regras nunca o vê.)

Os comandos `DELETE` não precisam de uma lista de destino normal, porque eles não produzem nenhum resultado. Em vez disso, o planejador adiciona uma entrada especial de CTID à lista de destino vazia, para permitir que o executor encontre a linha a ser excluída. (O CTID é adicionado quando a relação de resultado é uma tabela ordinária. Se for uma visão, uma variável de linha inteira é adicionada, em vez disso, pelo sistema de regras, conforme descrito em [Seção 39.2.4](rules-views.md#RULES-VIEWS-UPDATE).))

Para comandos de `INSERT`, a lista de alvos descreve as novas linhas que devem ser inseridas na relação de resultado. Ela consiste nas expressões na cláusula `VALUES` ou nas que vêm da cláusula `SELECT` em `INSERT ... SELECT`. O primeiro passo do processo de reescrita adiciona entradas da lista de alvos para quaisquer colunas que não tenham sido atribuídas pelo comando original, mas que tenham valores padrão. As colunas restantes (sem valor dado ou padrão) serão preenchidas pelo planejador com uma expressão constante nulo.

Para os comandos `UPDATE`, a lista de alvos descreve as novas linhas que devem substituir as antigas. No sistema de regras, ela contém apenas as expressões da parte `SET column = expression` do comando. O planejador tratará das colunas ausentes, inserindo expressões que copiam os valores da linha antiga para a nova. Assim como para `DELETE`, uma CTID ou variável de linha inteira é adicionada para que o executor possa identificar a linha antiga a ser atualizada.

Cada entrada na lista de destino contém uma expressão que pode ser um valor constante, uma variável que aponta para uma coluna de uma das relações na tabela de intervalo, um parâmetro ou uma árvore de expressão composta por chamadas de função, constantes, variáveis, operadores, etc.

a qualificação: A qualificação da consulta é uma expressão muito semelhante àquelas contidas nas entradas da lista de destino. O valor de resultado desta expressão é um Booleano que indica se a operação (`INSERT`, `UPDATE`, `DELETE` ou `SELECT`) para a linha do resultado final deve ser executada ou não. Isso corresponde à cláusula `WHERE` de uma declaração SQL.

a árvore de junção: A árvore de junção da consulta mostra a estrutura da cláusula `FROM`. Para uma consulta simples como `SELECT ... FROM a, b, c`, a árvore de junção é apenas uma lista dos itens `FROM`, porque podemos unir os itens em qualquer ordem. Mas quando são usadas expressões `JOIN`, particularmente junções externas, temos que unir na ordem mostrada pelas junções. Nesse caso, a árvore de junção mostra a estrutura das expressões `JOIN`. As restrições associadas a cláusulas `JOIN` específicas (de expressões `ON` ou `USING`) são armazenadas como expressões de qualificação anexadas a esses nós da árvore de junção. Acontece que é conveniente armazenar a expressão `WHERE` de nível superior como uma qualificação anexada ao item de nível superior da árvore de junção. Portanto, na verdade, a árvore de junção representa tanto as cláusulas `FROM` e `WHERE` de uma `SELECT`.

os outros: As outras partes da árvore de consulta, como a cláusula `ORDER BY`, não interessam aqui. O sistema de regras substitui algumas entradas lá, enquanto aplica regras, mas isso não tem muito a ver com os fundamentos do sistema de regras.