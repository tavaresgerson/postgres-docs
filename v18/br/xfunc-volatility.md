## 36.7. Categorias de volatilidade de função [#](#XFUNC-VOLATILITY)

Cada função tem uma classificação de *volatilidade*, com as possibilidades sendo `VOLATILE`, `STABLE` ou `IMMUTABLE`. `VOLATILE` é a opção padrão se o comando [`CREATE FUNCTION`(sql-createfunction.md "CREATE FUNCTION") não especificar uma categoria. A categoria de volatilidade é uma promessa ao otimizador sobre o comportamento da função:

* Uma função `VOLATILE` pode fazer qualquer coisa, incluindo modificar o banco de dados. Ela pode retornar resultados diferentes em chamadas sucessivas com os mesmos argumentos. O otimizador não faz suposições sobre o comportamento dessas funções. Uma consulta que usa uma função volátil reavaliará a função em cada linha onde seu valor é necessário.
* Uma função `STABLE` não pode modificar o banco de dados e é garantido que ela retorne os mesmos resultados dados os mesmos argumentos para todas as linhas dentro de uma única declaração. Esta categoria permite que o otimizador otimize múltiplas chamadas da função para uma única chamada. Em particular, é seguro usar uma expressão que contenha tal função em uma condição de varredura de índice. (Uma vez que uma varredura de índice avaliará o valor da comparação apenas uma vez, não em cada linha, não é válido usar uma função `VOLATILE` em uma condição de varredura de índice.)
* Uma função `IMMUTABLE` não pode modificar o banco de dados e é garantido que ela retorne os mesmos resultados dados os mesmos argumentos para sempre. Esta categoria permite que o otimizador preavalie a função quando uma consulta a chama com argumentos constantes. Por exemplo, uma consulta como `SELECT ... WHERE x = 2 + 2` pode ser simplificada à vista para `SELECT ... WHERE x = 4`, porque a função subjacente ao operador de adição de inteiros é marcada `IMMUTABLE`.

Para obter os melhores resultados de otimização, você deve rotular suas funções com a categoria de volatilidade mais rigorosa que seja válida para elas.

Qualquer função com efeitos colaterais *deve* ser rotulada `VOLATILE`, para que as chamadas a ela não possam ser otimizadas. Mesmo uma função sem efeitos colaterais precisa ser rotulada `VOLATILE` se seu valor puder mudar em uma única consulta; alguns exemplos são `random()`, `currval()`, `timeofday()`.

Outro exemplo importante é que a família de funções `current_timestamp` se qualifica como `STABLE`, uma vez que seus valores não mudam dentro de uma transação.

Há relativamente pouca diferença entre as categorias `STABLE` e `IMMUTABLE` quando se considera consultas interativas simples que são planejadas e executadas imediatamente: não importa muito se uma função é executada uma vez durante o planejamento ou uma vez durante o início da execução da consulta. Mas há uma grande diferença se o plano for salvo e reutilizado posteriormente. Marcar uma função como `IMMUTABLE` quando ela realmente não é pode permitir que ela seja preenchida prematuramente a uma constante durante o planejamento, resultando em um valor desatualizado sendo reutilizado durante os usos subsequentes do plano. Isso é um perigo ao usar declarações preparadas ou quando se usa linguagens de função que cacheiam planos (como PL/pgSQL).

Para funções escritas em SQL ou em qualquer um dos idiomas processuais padrão, há uma segunda propriedade importante determinada pela categoria de volatilidade, a saber, a visibilidade de quaisquer alterações de dados que tenham sido feitas pelo comando SQL que está chamando a função. Uma função `VOLATILE` verá tais alterações, uma função `STABLE` ou `IMMUTABLE` não verá. Esse comportamento é implementado usando o comportamento de instantâneo do MVCC (ver [Capítulo 13][(mvcc.md "Chapter 13. Concurrency Control")]): as funções `STABLE` e `IMMUTABLE` utilizam um instantâneo estabelecido no início da consulta que está chamando, enquanto as funções `VOLATILE` obtêm um instantâneo fresco no início de cada consulta que executam.

### Nota

As funções escritas em C podem gerenciar instantâneos da maneira que desejam, mas geralmente é uma boa ideia fazer com que as funções em C também funcionem dessa maneira.

Devido a esse comportamento de captura de instantâneo, uma função que contém apenas comandos `SELECT` pode ser marcada com segurança como `STABLE`, mesmo que ela selecione de tabelas que podem estar sendo modificadas por consultas concorrentes. O PostgreSQL executará todos os comandos de uma função `STABLE` usando o instantâneo estabelecido para a consulta que está chamando, e assim verá uma visão fixa do banco de dados ao longo dessa consulta.

O mesmo comportamento de captura de instantâneo é usado para comandos `SELECT` dentro das funções `IMMUTABLE`. Geralmente, não é aconselhável selecionar tabelas de banco de dados dentro de uma função `IMMUTABLE`, pois a imutabilidade será quebrada se o conteúdo da tabela mudar alguma vez. No entanto, o PostgreSQL não exige que você não faça isso.

Um erro comum é rotular uma função `IMMUTABLE` quando seus resultados dependem de um parâmetro de configuração. Por exemplo, uma função que manipula timestamps pode ter resultados que dependem da configuração de [TimeZone](runtime-config-client.md#GUC-TIMEZONE). Por segurança, essas funções devem ser rotuladas `STABLE` em vez disso.

### Nota

O PostgreSQL exige que as funções `STABLE` e `IMMUTABLE` não contenham comandos SQL, exceto `SELECT`, para evitar a modificação de dados. (Este não é um teste completamente à prova de balas, pois tais funções ainda poderiam chamar funções `VOLATILE` que modificam o banco de dados. Se você fizer isso, descobrirá que a função `STABLE` ou `IMMUTABLE` não notará as alterações no banco de dados aplicadas pela função chamada, uma vez que elas são ocultas de seu instantâneo.)