## CRIAR Dicionário de PESQUISA DE TEXTO

CREATE TEXT SEARCH DICTIONARY — defina um novo dicionário de pesquisa de texto

## Sinopse

```
CREATE TEXT SEARCH DICTIONARY name (
    TEMPLATE = template
    [, option = value [, ... ]]
)
```

## Descrição

`CREATE TEXT SEARCH DICTIONARY` cria um novo dicionário de busca de texto. Um dicionário de busca de texto especifica uma maneira de reconhecer palavras interessantes ou não interessantes para a busca. Um dicionário depende de um modelo de busca de texto, que especifica as funções que realmente realizam o trabalho. Tipicamente, o dicionário fornece algumas opções que controlam o comportamento detalhado das funções do modelo.

Se um nome de esquema for fornecido, o dicionário de pesquisa de texto é criado no esquema especificado. Caso contrário, ele é criado no esquema atual.

O usuário que define um dicionário de busca de texto se torna seu proprietário.

Consulte o [Capítulo 12](textsearch.md) para obter mais informações.

## Parâmetros

*`name`*: O nome do dicionário de busca de texto a ser criado. O nome pode ser qualificado por esquema.

*`template`*: O nome do modelo de busca de texto que definirá o comportamento básico deste dicionário.

*`option`*: O nome de uma opção específica do modelo a ser definida para este dicionário.

*`value`*: O valor a ser usado para uma opção específica do modelo. Se o valor não for um identificador ou número simples, ele deve ser citado (mas você pode sempre citá-lo, se desejar).

As opções podem aparecer em qualquer ordem.

## Exemplos

O comando a seguir cria um dicionário baseado em Snowball com uma lista não padrão de palavras paradas.

```
CREATE TEXT SEARCH DICTIONARY my_russian (
    template = snowball,
    language = russian,
    stopwords = myrussian
);
```

## Compatibilidade

Não há nenhuma declaração `CREATE TEXT SEARCH DICTIONARY` no padrão SQL.

## Veja também

[ALTERAR Dicionário de PESQUISA DE TEXTO](sql-altertsdictionary.md "ALTER TEXT SEARCH DICTIONARY"), [DROP Dicionário de PESQUISA DE TEXTO](sql-droptsdictionary.md "DROP TEXT SEARCH DICTIONARY")