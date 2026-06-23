## Dicionário de Pesquisa de Texto ALTER

ALTERAR Dicionário de PESQUISA DE TEXTO — alterar a definição de um dicionário de pesquisa de texto

## Sinopse

```
ALTER TEXT SEARCH DICTIONARY name (
    option [ = value ] [, ... ]
)
ALTER TEXT SEARCH DICTIONARY name RENAME TO new_name
ALTER TEXT SEARCH DICTIONARY name OWNER TO { new_owner | CURRENT_ROLE | CURRENT_USER | SESSION_USER }
ALTER TEXT SEARCH DICTIONARY name SET SCHEMA new_schema
```

## Descrição

`ALTER TEXT SEARCH DICTIONARY` altera a definição de um dicionário de pesquisa de texto. Você pode alterar as opções específicas do modelo do dicionário ou alterar o nome ou o proprietário do dicionário.

Você deve ser o proprietário do dicionário para usar `ALTER TEXT SEARCH DICTIONARY`.

## Parâmetros

*`name`*: O nome (opcionalmente qualificado por esquema) de um dicionário de pesquisa de texto existente.

*`option`*: O nome de uma opção específica do modelo a ser definida para este dicionário.

*`value`*: O novo valor a ser usado para uma opção específica do modelo. Se o sinal de igual e o valor forem omitidos, então qualquer configuração anterior para a opção será removida do dicionário, permitindo que o padrão seja usado.

*`new_name`*: O novo nome do dicionário de busca de texto.

*`new_owner`*: O novo proprietário do dicionário de busca de texto.

*`new_schema`*: O novo esquema para o dicionário de busca de texto.

As opções específicas do modelo podem aparecer em qualquer ordem.

## Exemplos

O comando a seguir altera a lista de palavras irrelevantes para um dicionário baseado em Snowball. Outros parâmetros permanecem inalterados.

```
ALTER TEXT SEARCH DICTIONARY my_dict ( StopWords = newrussian );
```

O comando a seguir muda a opção de idioma para `dutch` e remove a opção de palavra-stop completamente.

```
ALTER TEXT SEARCH DICTIONARY my_dict ( language = dutch, StopWords );
```

O comando a seguir “atualiza” a definição do dicionário sem, na verdade, alterar nada.

```
ALTER TEXT SEARCH DICTIONARY my_dict ( dummy );
```

(A razão pela qual isso funciona é que o código de remoção de opção não se queixa se não houver tal opção.) Esse truque é útil ao alterar arquivos de configuração para o dicionário: o `ALTER` fará com que as sessões de banco de dados existentes re-leiam os arquivos de configuração, o que, caso contrário, nunca faria se os tivesse lido anteriormente.

## Compatibilidade

Não há nenhuma declaração `ALTER TEXT SEARCH DICTIONARY` no padrão SQL.

## Veja também

[Crie um dicionário de busca de texto](sql-createtsdictionary.md "CREATE TEXT SEARCH DICTIONARY"), [Remova o dicionário de busca de texto](sql-droptsdictionary.md "DROP TEXT SEARCH DICTIONARY")