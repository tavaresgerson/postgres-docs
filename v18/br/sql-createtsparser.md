## CRIAR UM PARSER DE PESQUISA DE TEXTO

CREATE TEXT SEARCH PARSER — definir um novo analisador de busca de texto

## Sinopse

```
CREATE TEXT SEARCH PARSER name (
    START = start_function ,
    GETTOKEN = gettoken_function ,
    END = end_function ,
    LEXTYPES = lextypes_function
    [, HEADLINE = headline_function ]
)
```

## Descrição

`CREATE TEXT SEARCH PARSER` cria um novo analisador de pesquisa de texto. Um analisador de pesquisa de texto define um método para dividir uma string de texto em tokens e atribuir tipos (categorias) aos tokens. Um analisador não é particularmente útil por si só, mas deve ser vinculado a uma configuração de pesquisa de texto juntamente com alguns dicionários de pesquisa de texto que serão usados para a pesquisa.

Se um nome de esquema for fornecido, o analisador de busca de texto é criado no esquema especificado. Caso contrário, ele é criado no esquema atual.

Você deve ser um superusuário para usar `CREATE TEXT SEARCH PARSER`. (Essa restrição é feita porque uma definição errada do parser de busca de texto pode confundir ou até mesmo fazer o servidor falhar.)

Consulte o [Capítulo 12][(textsearch.md "Chapter 12. Full Text Search")] para obter mais informações.

## Parâmetros

*`name`*: O nome do analisador de busca de texto a ser criado. O nome pode ser qualificado por esquema.

*`start_function`*: O nome da função de início para o analisador.

*`gettoken_function`*: O nome da função get-next-token para o analisador.

*`end_function`*: O nome da função final para o analisador.

*`lextypes_function`*: O nome da função de lextypes para o analisador (uma função que retorna informações sobre o conjunto de tipos de tokens que produz).

*`headline_function`*: O nome da função de cabeçalho para o analisador (uma função que resume um conjunto de tokens).

Os nomes das funções podem ser qualificados pelo esquema, se necessário. Os tipos de argumento não são fornecidos, uma vez que a lista de argumentos para cada tipo de função é predeterminada. Todos, exceto a função de título, são obrigatórios.

Os argumentos podem aparecer em qualquer ordem, não apenas naquela mostrada acima.

## Compatibilidade

Não há nenhuma declaração `CREATE TEXT SEARCH PARSER` no padrão SQL.

## Veja também

[ALTERAR BUSCA DE TEXTO](sql-altertsparser.md "ALTER TEXT SEARCH PARSER"), [DROP BUSCA DE TEXTO](sql-droptsparser.md "DROP TEXT SEARCH PARSER")