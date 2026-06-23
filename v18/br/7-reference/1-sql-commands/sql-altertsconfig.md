## ALTERAR CONFIGURAÇÃO DE PESQUISA DE TEXTO

ALTERAR CONFIGURAÇÃO DE PESQUISA DE TEXTO — alterar a definição de uma configuração de pesquisa de texto

## Sinopse

```
ALTER TEXT SEARCH CONFIGURATION name
    ADD MAPPING FOR token_type [, ... ] WITH dictionary_name [, ... ]
ALTER TEXT SEARCH CONFIGURATION name
    ALTER MAPPING FOR token_type [, ... ] WITH dictionary_name [, ... ]
ALTER TEXT SEARCH CONFIGURATION name
    ALTER MAPPING REPLACE old_dictionary WITH new_dictionary
ALTER TEXT SEARCH CONFIGURATION name
    ALTER MAPPING FOR token_type [, ... ] REPLACE old_dictionary WITH new_dictionary
ALTER TEXT SEARCH CONFIGURATION name
    DROP MAPPING [ IF EXISTS ] FOR token_type [, ... ]
ALTER TEXT SEARCH CONFIGURATION name RENAME TO new_name
ALTER TEXT SEARCH CONFIGURATION name OWNER TO { new_owner | CURRENT_ROLE | CURRENT_USER | SESSION_USER }
ALTER TEXT SEARCH CONFIGURATION name SET SCHEMA new_schema
```

## Descrição

`ALTER TEXT SEARCH CONFIGURATION` altera a definição de uma configuração de pesquisa de texto. Você pode modificar suas correspondências de tipos de token para dicionários ou alterar o nome ou o proprietário da configuração.

Você deve ser o proprietário da configuração para usar `ALTER TEXT SEARCH CONFIGURATION`.

## Parâmetros

*`name`*: O nome (opcionalmente qualificado por esquema) de uma configuração de busca de texto existente.

*`token_type`*: O nome de um tipo de token emitido pelo analisador da configuração.

*`dictionary_name`*: O nome de um dicionário de pesquisa de texto a ser consultado para o(s) tipo(s) de token especificado(s). Se houver vários dicionários listados, eles são consultados na ordem especificada.

*`old_dictionary`*: O nome de um dicionário de busca de texto a ser substituído no mapeamento.

*`new_dictionary`*: O nome de um dicionário de busca de texto que será substituído por *`old_dictionary`*.

*`new_name`*: O novo nome da configuração de pesquisa de texto.

*`new_owner`*: O novo proprietário da configuração de busca de texto.

*`new_schema`*: O novo esquema para a configuração de busca de texto.

O formulário `ADD MAPPING FOR` instala uma lista de dicionários a serem consultados para o(s) tipo(s) de token especificado(s); é um erro se já houver uma mapeamento para qualquer um dos tipos de token. O formulário `ALTER MAPPING FOR` faz o mesmo, mas primeiro removendo qualquer mapeamento existente para esses tipos de token. Os formulários `ALTER MAPPING REPLACE` substituem *`new_dictionary`* por *`old_dictionary`* em qualquer lugar que este último apareça. Isso é feito apenas para os tipos de token especificados quando aparece `FOR`, ou para todas as mapeamentos da configuração quando isso não acontece. O formulário `DROP MAPPING` remove todos os dicionários para o(s) tipo(s) de token especificado(s), fazendo com que os tokens desses tipos sejam ignorados pela configuração de pesquisa de texto. É um erro se não houver mapeamento para os tipos de token, a menos que apareça `IF EXISTS`.

## Exemplos

O exemplo a seguir substitui o dicionário `english` pelo dicionário `swedish` em qualquer lugar onde o `english` é usado dentro de `my_config`.

```
ALTER TEXT SEARCH CONFIGURATION my_config
  ALTER MAPPING REPLACE english WITH swedish;
```

## Compatibilidade

Não há declaração `ALTER TEXT SEARCH CONFIGURATION` no padrão SQL.

## Veja também

[Crie configuração de busca de texto](sql-createtsconfig.md "CREATE TEXT SEARCH CONFIGURATION"), [Remova configuração de busca de texto](sql-droptsconfig.md "DROP TEXT SEARCH CONFIGURATION")