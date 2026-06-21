## Crie um modelo de busca de texto

Crie um modelo de busca de texto — defina um novo modelo de busca de texto

## Sinopse

```
CREATE TEXT SEARCH TEMPLATE name (
    [ INIT = init_function , ]
    LEXIZE = lexize_function
)
```

## Descrição

`CREATE TEXT SEARCH TEMPLATE` cria um novo modelo de pesquisa de texto. Os modelos de pesquisa de texto definem as funções que implementam os dicionários de pesquisa de texto. Um modelo não é útil por si só, mas deve ser instanciado como um dicionário para ser usado. O dicionário especifica tipicamente os parâmetros que devem ser fornecidos às funções do modelo.

Se um nome de esquema for fornecido, o modelo de busca de texto é criado no esquema especificado. Caso contrário, ele é criado no esquema atual.

Você deve ser um superusuário para usar `CREATE TEXT SEARCH TEMPLATE`. Esta restrição é feita porque uma definição errada do modelo de busca de texto pode confundir ou até mesmo fazer o servidor falhar. A razão para separar os modelos dos dicionários é que um modelo encapsula os aspectos "inseguros" de definir um dicionário. Os parâmetros que podem ser definidos ao definir um dicionário são seguros para usuários não privilegiados, e, portanto, criar um dicionário não precisa ser uma operação privilegiada.

Consulte o [Capítulo 12][(textsearch.md "Chapter 12. Full Text Search")] para obter mais informações.

## Parâmetros

*`name`*: O nome do modelo de busca de texto a ser criado. O nome pode ser qualificado por esquema.

*`init_function`*: O nome da função init para o modelo.

*`lexize_function`*: O nome da função lexize para o modelo.

Os nomes das funções podem ser qualificados por esquema, se necessário. Os tipos de argumento não são fornecidos, uma vez que a lista de argumentos para cada tipo de função é predeterminada. A função lexize é necessária, mas a função init é opcional.

Os argumentos podem aparecer em qualquer ordem, não apenas naquela mostrada acima.

## Compatibilidade

Não há nenhuma declaração `CREATE TEXT SEARCH TEMPLATE` no padrão SQL.

## Veja também

[ALTERAR TEMPLATE DE PESQUISA DE TEXTO](sql-altertstemplate.md "ALTER TEXT SEARCH TEMPLATE"), [DROP TEMPLATE DE PESQUISA DE TEXTO](sql-droptstemplate.md "DROP TEXT SEARCH TEMPLATE")