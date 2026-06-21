## 2.4. Populando uma Tabela com Linhas [#](#TUTORIAL-POPULATE)

A declaração `INSERT` é usada para preencher uma tabela com linhas:

```
INSERT INTO weather VALUES ('San Francisco', 46, 50, 0.25, '1994-11-27');
```

Observe que todos os tipos de dados utilizam formatos de entrada bastante óbvios. As constantes que não são valores numéricos simples geralmente devem ser cercadas por aspas simples (`'`), como no exemplo. O tipo `date` é, na verdade, bastante flexível em relação ao que ele aceita, mas para este tutorial, vamos nos ater ao formato inequívoco mostrado aqui.

O tipo `point` requer um par de coordenadas como entrada, conforme mostrado aqui:

```
INSERT INTO cities VALUES ('San Francisco', '(-194.0, 53.0)');
```

A sintaxe usada até agora exige que você se lembre da ordem das colunas. Uma sintaxe alternativa permite que você liste as colunas explicitamente:

```
INSERT INTO weather (city, temp_lo, temp_hi, prcp, date)
    VALUES ('San Francisco', 43, 57, 0.0, '1994-11-29');
```

Você pode listar as colunas em uma ordem diferente, se desejar, ou até mesmo omitir algumas colunas, por exemplo, se a precipitação for desconhecida:

```
INSERT INTO weather (date, city, temp_hi, temp_lo)
    VALUES ('1994-11-29', 'Hayward', 54, 37);
```

Muitos desenvolvedores consideram que listar explicitamente as colunas é um estilo melhor do que confiar na ordem implicitamente.

Por favor, insira todos os comandos mostrados acima para que você tenha alguns dados com os quais trabalhar nas seções a seguir.

Você também poderia ter usado `COPY` para carregar grandes quantidades de dados a partir de arquivos de texto plano. Isso geralmente é mais rápido, pois o comando `COPY` é otimizado para essa aplicação, permitindo menos flexibilidade do que `INSERT`. Um exemplo seria:

```
COPY weather FROM '/home/user/weather.txt';
```

onde o nome do arquivo para o arquivo de origem deve estar disponível na máquina que executa o processo de backend, não no cliente, uma vez que o processo de backend lê o arquivo diretamente. Os dados inseridos acima na tabela de clima também podem ser inseridos a partir de um arquivo que contenha (os valores são separados por um caractere de tabulação):

```
San Francisco    46    50    0.25    1994-11-27
San Francisco    43    57    0.0    1994-11-29
Hayward    37    54    \N    1994-11-29
```

Você pode ler mais sobre o comando `COPY` em [COPY](sql-copy.md "COPY").