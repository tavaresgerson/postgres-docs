## CRIAR CONFIGURAÇÃO DE PESQUISA DE TEXTO

Crie configuração de pesquisa de texto — defina uma nova configuração de pesquisa de texto

## Sinopse

```
CREATE TEXT SEARCH CONFIGURATION name (
    PARSER = parser_name |
    COPY = source_config
)
```

## Descrição

`CREATE TEXT SEARCH CONFIGURATION` cria uma nova configuração de pesquisa de texto. Uma configuração de pesquisa de texto especifica um analisador de pesquisa de texto que pode dividir uma string em tokens, além de dicionários que podem ser usados para determinar quais tokens são de interesse para a pesquisa.

Se apenas o analisador for especificado, a nova configuração de pesquisa de texto inicialmente não terá mapeamentos de tipos de token para dicionários, e, portanto, ignorará todas as palavras. Os comandos subsequentes `ALTER TEXT SEARCH CONFIGURATION` devem ser usados para criar mapeamentos e tornar a configuração útil. Alternativamente, uma configuração de pesquisa de texto existente pode ser copiada.

Se um nome de esquema for fornecido, a configuração de pesquisa de texto é criada no esquema especificado. Caso contrário, ela é criada no esquema atual.

O usuário que define uma configuração de busca de texto torna-se seu proprietário.

Consulte o [Capítulo 12](textsearch.md) para obter mais informações.

## Parâmetros

*`name`*: O nome da configuração de busca de texto a ser criada. O nome pode ser qualificado por esquema.

*`parser_name`*: O nome do analisador de busca de texto a ser usado para esta configuração.

*`source_config`*: O nome de uma configuração de busca de texto existente para copiar.

## Notas

As opções `PARSER` e `COPY` são mutuamente exclusivas, porque, quando uma configuração existente é copiada, sua seleção de analisador também é copiada.

## Compatibilidade

Não há nenhuma declaração `CREATE TEXT SEARCH CONFIGURATION` no padrão SQL.

## Veja também

[ALTERAR CONFIGURAÇÃO DE PESQUISA DE TEXTO](sql-altertsconfig.md "ALTER TEXT SEARCH CONFIGURATION"), [DROP CONFIGURAÇÃO DE PESQUISA DE TEXTO](sql-droptsconfig.md "DROP TEXT SEARCH CONFIGURATION")