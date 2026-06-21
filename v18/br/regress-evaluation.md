## 31.2. Avaliação de Teste [#](#REGRESS-EVALUATION)

* [31.2.1. Diferenças de Mensagem de Erro][(regress-evaluation.md#REGRESS-EVALUATION-MESSAGE-DIFFERENCES)]
* [31.2.2. Diferenças de Local][(regress-evaluation.md#REGRESS-EVALUATION-LOCALE-DIFFERENCES)]
* [31.2.3. Diferenças de Data e Hora][(regress-evaluation.md#REGRESS-EVALUATION-DATE-TIME-DIFFERENCES)]
* [31.2.4. Diferenças de Ponto Flutuante][(regress-evaluation.md#REGRESS-EVALUATION-FLOAT-DIFFERENCES)]
* [31.2.5. Diferenças de Ordem de Linha][(regress-evaluation.md#REGRESS-EVALUATION-ORDERING-DIFFERENCES)]
* [31.2.6. Insuficiente Profundidade de Pilha][(regress-evaluation.md#REGRESS-EVALUATION-STACK-DEPTH)]
* [31.2.7. O Teste “aleatório”][(regress-evaluation.md#REGRESS-EVALUATION-RANDOM-TEST)]
* [31.2.8. Parâmetros de Configuração][(regress-evaluation.md#REGRESS-EVALUATION-CONFIG-PARAMS)]

Algumas instalações de PostgreSQL adequadamente instaladas e totalmente funcionais podem "falhar" alguns desses testes de regressão devido a artefatos específicos da plataforma, como a representação variável de ponto flutuante e a formulação das mensagens. Os testes são atualmente avaliados usando uma comparação simples `diff` contra as saídas geradas em um sistema de referência, portanto, os resultados são sensíveis a pequenas diferenças no sistema. Quando um teste é relatado como "falha", sempre examine as diferenças entre os resultados esperados e os resultados reais; você pode descobrir que as diferenças não são significativas. No entanto, ainda nos esforçamos para manter arquivos de referência precisos em todas as plataformas suportadas, portanto, pode-se esperar que todos os testes passem.

As saídas reais dos testes de regressão estão em arquivos no diretório `src/test/regress/results`. O script de teste usa `diff` para comparar cada arquivo de saída contra as saídas de referência armazenadas no diretório `src/test/regress/expected`. Quaisquer diferenças são salvas para sua inspeção em `src/test/regress/regression.diffs`. (Ao executar uma suíte de teste que não seja os testes principais, esses arquivos, claro, aparecem no subdiretório relevante, não em `src/test/regress`.)

Se você não gosta das opções `diff` que são usadas por padrão, defina a variável de ambiente `PG_REGRESS_DIFF_OPTS`, por exemplo, `PG_REGRESS_DIFF_OPTS='-c'`. (Ou você pode executar `diff` você mesmo, se preferir.)

Se, por algum motivo, uma plataforma específica gerar um "erro" para um teste específico, mas a inspeção do resultado o convença de que o resultado é válido, você pode adicionar um novo arquivo de comparação para silenciar o relatório de falha em futuras execuções do teste. Consulte [Seção 31.3][(regress-variant.md "31.3. Variant Comparison Files")] para obter detalhes.

### 31.2.1. Diferenças nos Mensagens de Erro [#](#REGRESS-EVALUATION-MESSAGE-DIFFERENCES)

Alguns dos testes de regressão envolvem valores de entrada inválidos intencionais. As mensagens de erro podem vir do código PostgreSQL ou das rotinas do sistema da plataforma hospedeira. No último caso, as mensagens podem variar entre as plataformas, mas devem refletir informações semelhantes. Essas diferenças nas mensagens resultarão em um teste de regressão "falha" que pode ser validado por inspeção.

### 31.2.2. Diferenças de localização [#](#REGRESS-EVALUATION-LOCALE-DIFFERENCES)

Se você executar os testes em um servidor que foi inicializado com um idioma de ordem de colagem diferente de C, então pode haver diferenças devido à ordem de classificação e falhas subsequentes. A suite de testes de regressão é configurada para lidar com esse problema, fornecendo arquivos de resultado alternativos que, juntos, são conhecidos por lidar com um grande número de idiomas.

Para executar os testes em um local diferente ao usar o método de instalação temporária, passe as variáveis de ambiente relacionadas ao local apropriado na linha de comando do comando `make`, por exemplo:

```
make check LANG=de_DE.utf8
```

(O motorista de teste de regressão desativa `LC_ALL`, portanto, não funciona para escolher o local usando essa variável. Para não usar nenhum local, desative todas as variáveis de ambiente relacionadas ao local (ou defina-as como `C`) ou use a seguinte invocação especial:

```
make check NO_LOCALE=1
```

Ao executar os testes contra uma instalação existente, a configuração do local é determinada pela instalação existente. Para alterá-la, inicialize o clúster de banco de dados com um local diferente, passando as opções apropriadas para `initdb`.

De forma geral, é aconselhável tentar executar os testes de regressão no ambiente de configuração do local que é desejado para uso em produção, pois isso exercitará as partes do código relacionadas ao local e ao codificação que serão realmente utilizadas em produção. Dependendo do ambiente do sistema operacional, você pode obter falhas, mas, então, pelo menos saberá quais comportamentos específicos do local devem ser esperados ao executar aplicativos reais.

### 31.2.3. Diferenças de data e hora [#](#REGRESS-EVALUATION-DATE-TIME-DIFFERENCES)

A maioria dos resultados de data e hora depende do ambiente do fuso horário. Os arquivos de referência são gerados para o fuso horário `America/Los_Angeles`, e haverá falhas evidentes se os testes não forem executados com essa configuração de fuso horário. O driver de teste de regressão define a variável de ambiente `PGTZ` para `America/Los_Angeles`, o que normalmente garante resultados adequados.

### 31.2.4. Diferenças de Ponto Flutuante [#](#REGRESS-EVALUATION-FLOAT-DIFFERENCES)

Alguns dos testes envolvem a computação de números de ponto flutuante de 64 bits (`double precision`) a partir de colunas da tabela. Diferenças nos resultados que envolvem funções matemáticas das colunas de `double precision` foram observadas. Os testes de `float8` e `geometry` são particularmente propensos a pequenas diferenças entre plataformas, ou até mesmo com diferentes configurações de otimização do compilador. A comparação com o olho humano é necessária para determinar o significado real dessas diferenças, que geralmente são 10 lugares à direita do ponto decimal.

Alguns sistemas exibem zero negativo como `-0`, enquanto outros apenas mostram `0`.

Alguns sistemas sinalizam erros de `pow()` e `exp()` de maneira diferente do mecanismo esperado pelo código atual do PostgreSQL.

### 31.2.5. Diferenças na Ordem das Linhas [#](#REGRESS-EVALUATION-ORDERING-DIFFERENCES)

Você pode observar diferenças na ordem em que as mesmas linhas são exibidas em um arquivo diferente do esperado. Na maioria dos casos, isso não é, estritamente falando, um bug. A maioria dos scripts de teste de regressão não é tão pedindo quanto a utilização de um `ORDER BY` para cada `SELECT`, e, portanto, suas ordenações de linhas de resultado não são bem definidas de acordo com a especificação SQL. Na prática, uma vez que estamos analisando as mesmas consultas sendo executadas nos mesmos dados pelo mesmo software, geralmente obtemos a mesma ordem de resultado em todas as plataformas, então a falta de `ORDER BY` não é um problema. No entanto, algumas consultas apresentam diferenças de ordenação entre plataformas. Quando testadas contra um servidor já instalado, as diferenças de ordenação também podem ser causadas por configurações de não-C locale ou configurações de parâmetros não padrão, como valores personalizados de `work_mem` ou os parâmetros de custo do planejador.

Portanto, se você observar uma diferença na ordem, não há motivo para se preocupar, a menos que a consulta tenha um `ORDER BY` que seu resultado esteja violando. No entanto, por favor, informe isso mesmo assim, para que possamos adicionar um `ORDER BY` àquela consulta específica e eliminar o falso “fracasso” em futuras versões.

Você pode se perguntar por que não solicitamos todas as consultas de teste de regressão explicitamente para se livrar desse problema de uma vez por todas. O motivo é que isso tornaria os testes de regressão menos úteis, não mais, pois eles tenderiam a exercitar tipos de plano de consulta que produzem resultados ordenados à exclusão daqueles que não o fazem.

### 31.2.6. Profundidade de pilha insuficiente [#](#REGRESS-EVALUATION-STACK-DEPTH)

Se o resultado do teste `errors` resultar em um crash do servidor no comando `select infinite_recurse()`, isso significa que o limite da plataforma em relação ao tamanho da pilha de processos é menor do que o que o parâmetro [max_stack_depth](runtime-config-resource.md#GUC-MAX-STACK-DEPTH) indica. Isso pode ser corrigido executando o servidor sob um limite de tamanho de pilha mais alto (recomendado 4 MB com o valor padrão de `max_stack_depth`). Se você não conseguir fazer isso, uma alternativa é reduzir o valor de `max_stack_depth`.

Em plataformas que suportam `getrlimit()`, o servidor deve escolher automaticamente um valor seguro de `max_stack_depth`; portanto, a menos que você tenha sobrescrito manualmente essa configuração, uma falha desse tipo é um bug que deve ser relatado.

### 31.2.7. O Teste “aleatório” [#](#REGRESS-EVALUATION-RANDOM-TEST)

O script de teste `random` é destinado a produzir resultados aleatórios. Em casos muito raros, isso faz com que o teste de regressão falhe. Digitação:

```
diff results/random.out expected/random.out
```

deveria produzir apenas uma ou algumas linhas de diferenças. Você não precisa se preocupar, a menos que o teste aleatório falhe repetidamente.

### 31.2.8. Parâmetros de configuração [#](#REGRESS-EVALUATION-CONFIG-PARAMS)

Ao executar os testes em uma instalação existente, algumas configurações de parâmetros não padrão podem fazer com que os testes falhem. Por exemplo, alterar parâmetros como `enable_seqscan` ou `enable_indexscan` pode causar alterações no plano que afetarão os resultados dos testes que utilizam `EXPLAIN`.