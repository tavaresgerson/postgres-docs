## 31.3. Arquivos de Comparação de Variantes [#](#REGRESS-VARIANT)

Como alguns dos testes produzem resultados inerentemente dependentes do ambiente, fornecemos maneiras de especificar arquivos de resultado "esperado" alternativos. Cada teste de regressão pode ter vários arquivos de comparação que mostram resultados possíveis em diferentes plataformas. Existem dois mecanismos independentes para determinar qual arquivo de comparação é usado para cada teste.

O primeiro mecanismo permite que arquivos de comparação sejam selecionados para plataformas específicas. Há um arquivo de mapeamento, `src/test/regress/resultmap`, que define qual arquivo de comparação deve ser usado para cada plataforma. Para eliminar falsos "fracasso" de teste para uma plataforma específica, você primeiro escolhe ou cria um arquivo de resultado de variante e, em seguida, adiciona uma linha ao arquivo `resultmap`.

Cada linha do arquivo de mapeamento tem a forma

```
testname:output:platformpattern=comparisonfilename
```

O nome do teste é apenas o nome do módulo de teste de regressão específico. O valor de saída indica qual arquivo de saída deve ser verificado. Para os testes de regressão padrão, este é sempre `out`. O valor corresponde à extensão do arquivo de saída. O padrão da plataforma é um padrão no estilo da ferramenta Unix `expr` (ou seja, uma expressão regular com um âncora `^` implícita no início). Ele é correspondido ao nome da plataforma conforme impresso por `config.guess`. O nome do arquivo de comparação é o nome base do arquivo de comparação de substituição de resultados.

Por exemplo: alguns sistemas não possuem uma função `strtof` funcional, para a qual nossa solução temporária causa erros de arredondamento no teste de regressão `float4`. Portanto, fornecemos um arquivo de comparação de variantes, `float4-misrounded-input.out`, que inclui os resultados esperados nesses sistemas. Para silenciar a falsa mensagem de “falha” em plataformas Cygwin, `resultmap` inclui:

```
float4:out:.*-.*-cygwin.*=float4-misrounded-input.out
```

que será ativado em qualquer máquina onde a saída de `config.guess` corresponda a `.*-.*-cygwin.*`. Outras linhas em `resultmap` selecionam o arquivo de comparação de variantes para outras plataformas onde for apropriado.

O segundo mecanismo de seleção para arquivos de comparação de variantes é muito mais automático: ele simplesmente usa a "melhor correspondência" entre vários arquivos de comparação fornecidos. O script do motorista de teste de regressão considera tanto o arquivo de comparação padrão para um teste, `testname.out`, quanto arquivos de variante nomeados `testname_digit.out` (onde o *`digit`* é qualquer dígito único `0`-`9`). Se qualquer um desses arquivos for uma correspondência exata, o teste é considerado aprovado; caso contrário, o que gera a menor diferença é usado para criar o relatório de falha. (Se `resultmap` incluir uma entrada para o teste específico, então o nome base *`testname`* é o nome substituto dado em `resultmap`.).

Por exemplo, para o teste `char`, o arquivo de comparação `char.out` contém resultados esperados nos locais `C` e `POSIX`, enquanto o arquivo `char_1.out` contém resultados ordenados conforme aparecem em muitos outros locais.

O mecanismo de correspondência ideal foi concebido para lidar com resultados dependentes do local, mas ele pode ser usado em qualquer situação em que os resultados do teste não possam ser facilmente previstos apenas pelo nome da plataforma. Uma limitação desse mecanismo é que o motorista do teste não pode dizer qual variante é realmente "correta" para o ambiente atual; ele simplesmente escolherá a variante que parece funcionar melhor. Portanto, é mais seguro usar esse mecanismo apenas para resultados de variantes que você está disposto a considerar igualmente válidos em todos os contextos.