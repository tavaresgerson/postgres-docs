## F.12. dict_int — dicionário de busca de texto completo para inteiros [#](#DICT-INT)

* [F.12.1. Configuração](dict-int.md#DICT-INT-CONFIG)
* [F.12.2. Uso](dict-int.md#DICT-INT-USAGE)

`dict_int` é um exemplo de um modelo de dicionário de complemento para pesquisa de texto completo. A motivação para este dicionário de exemplo é controlar a indexação de inteiros (assinados e não assinados), permitindo que tais números sejam indexados enquanto se previne o crescimento excessivo no número de palavras únicas, o que afeta muito o desempenho da pesquisa.

Este módulo é considerado "confiável", ou seja, pode ser instalado por usuários não superusuários que possuem privilégio `CREATE` no banco de dados atual.

### F.12.1. Configuração [#](#DICT-INT-CONFIG)

O dicionário aceita três opções:

* O parâmetro `maxlen` especifica o número máximo de dígitos permitidos em uma palavra inteira. O valor padrão é 6.
* O parâmetro `rejectlong` especifica se uma palavra inteira de comprimento excessivo deve ser truncada ou ignorada. Se `rejectlong` for `false` (o padrão), o dicionário retorna os primeiros `maxlen` dígitos da palavra inteira. Se `rejectlong` for `true`, o dicionário trata uma palavra inteira de comprimento excessivo como uma palavra parada, de modo que ela não será indexada. Note que isso também significa que tal número não pode ser pesquisado.
* O parâmetro `absval` especifica se os sinais iniciais “`+`” ou “`-`” devem ser removidos das palavras inteiras. O valor padrão é `false`. Quando `true`, o sinal é removido antes que `maxlen` seja aplicado.

### F.12.2. Uso [#](#DICT-INT-USAGE)

A instalação da extensão `dict_int` cria um modelo de busca de texto `intdict_template` e um dicionário `intdict` com base nele, com os parâmetros padrão. Você pode alterar os parâmetros, por exemplo

```
mydb# ALTER TEXT SEARCH DICTIONARY intdict (MAXLEN = 4, REJECTLONG = true);
ALTER TEXT SEARCH DICTIONARY
```

ou crie novos dicionários com base no modelo.

Para testar o dicionário, você pode tentar

```
mydb# select ts_lexize('intdict', '12345678');
 ts_lexize
-----------
 {123456}
```

mas o uso no mundo real envolverá incluí-lo em uma configuração de pesquisa de texto, conforme descrito em [Capítulo 12](textsearch.md). Isso pode parecer assim:

```
ALTER TEXT SEARCH CONFIGURATION english
    ALTER MAPPING FOR int, uint WITH intdict;
```
