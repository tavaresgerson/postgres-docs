## 36.6. Sobrecarga de função [#](#XFUNC-OVERLOAD)

Mais de uma função pode ser definida com o mesmo nome SQL, desde que os argumentos que eles recebam sejam diferentes. Em outras palavras, os nomes das funções podem ser *sobrecarregados*. Se você os usa ou não, essa capacidade implica precauções de segurança ao chamar funções em bancos de dados onde alguns usuários não confiam em outros usuários; veja [Seção 10.3](typeconv-func.md). Quando uma consulta é executada, o servidor determinará qual função chamar a partir dos tipos de dados e do número dos argumentos fornecidos. O sobrecarregamento também pode ser usado para simular funções com um número variável de argumentos, até um número máximo finito.

Ao criar uma família de funções sobrecarregadas, é importante ter cuidado para não criar ambiguidades. Por exemplo, considerando as funções:

```
CREATE FUNCTION test(int, real) RETURNS ...
CREATE FUNCTION test(smallint, double precision) RETURNS ...
```

Não está imediatamente claro qual função seria chamada com uma entrada trivial como `test(1, 1.5)`. As regras de resolução implementadas atualmente são descritas em [Capítulo 10](typeconv.md), mas não é prudente projetar um sistema que dependa sutilmente desse comportamento.

Uma função que recebe um único argumento de um tipo composto geralmente não deve ter o mesmo nome que qualquer atributo (campo) desse tipo. Lembre-se de que `attribute(table)` é considerado equivalente a `table.attribute`. No caso de haver ambiguidade entre uma função em um tipo composto e um atributo do tipo composto, o atributo será sempre usado. É possível sobrepor essa escolha qualificando o nome da função com o esquema (ou seja, `schema.func(table)`) mas é melhor evitar o problema não escolhendo nomes conflitantes.

Outro possível conflito é entre funções variadicas e não variadicas. Por exemplo, é possível criar tanto `foo(numeric)` quanto `foo(VARIADIC numeric[])`. Neste caso, não está claro qual deles deve ser correspondido a uma chamada que fornece um único argumento numérico, como `foo(10.1)`. A regra é que a função que aparece mais cedo no caminho de busca é usada, ou se as duas funções estão no mesmo esquema, a não variadic é preferida.

Ao sobrecarregar funções em linguagem C, há uma restrição adicional: O nome em C de cada função na família de funções sobrecarregadas deve ser diferente dos nomes em C de todas as outras funções, internas ou carregadas dinamicamente. Se essa regra for violada, o comportamento não será portátil. Você pode obter um erro de linker de tempo de execução ou uma das funções será chamada (geralmente a interna). A forma alternativa da cláusula `AS` para o comando SQL `CREATE FUNCTION` desvincula o nome da função SQL do nome da função no código-fonte em C. Por exemplo:

```
CREATE FUNCTION test(int) RETURNS int
    AS 'filename', 'test_1arg'
    LANGUAGE C;
CREATE FUNCTION test(int, int) RETURNS int
    AS 'filename', 'test_2arg'
    LANGUAGE C;
```

Os nomes das funções C aqui refletem uma das muitas convenções possíveis.