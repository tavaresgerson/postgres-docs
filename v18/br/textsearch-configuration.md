## 12.7. Exemplo de configuração [#](#TEXTSEARCH-CONFIGURATION)

Uma configuração de busca de texto especifica todas as opções necessárias para transformar um documento em um `tsvector`: o analisador a ser usado para dividir o texto em tokens e os dicionários a serem usados para transformar cada token em um léxico. Cada chamada de `to_tsvector` ou `to_tsquery` precisa de uma configuração de busca de texto para realizar seu processamento. O parâmetro de configuração [default_text_search_config](runtime-config-client.md#GUC-DEFAULT-TEXT-SEARCH-CONFIG) especifica o nome da configuração padrão, que é a usada pelas funções de busca de texto se um parâmetro de configuração explícito for omitido. Pode ser definido em `postgresql.conf`, ou definido para uma sessão individual usando o comando `SET`.

Várias configurações pré-definidas para pesquisa de texto estão disponíveis, e você pode criar configurações personalizadas facilmente. Para facilitar a gestão de objetos de pesquisa de texto, um conjunto de comandos SQL está disponível, e há vários comandos psql que exibem informações sobre objetos de pesquisa de texto ([Seção 12.10][(textsearch-psql.md "12.10. psql Support")]).

Como exemplo, vamos criar uma configuração `pg`, começando por duplicar a configuração embutida `english`:

```
CREATE TEXT SEARCH CONFIGURATION public.pg ( COPY = pg_catalog.english );
```

Usaremos uma lista de sinônimos específica do PostgreSQL e armazenaremos no `$SHAREDIR/tsearch_data/pg_dict.syn`. O conteúdo do arquivo parece assim:

```
postgres    pg
pgsql       pg
postgresql  pg
```

Definimos o dicionário de sinônimos da seguinte forma:

```
CREATE TEXT SEARCH DICTIONARY pg_dict (
    TEMPLATE = synonym,
    SYNONYMS = pg_dict
);
```

Em seguida, registramos o dicionário Ispell `english_ispell`, que possui seus próprios arquivos de configuração:

```
CREATE TEXT SEARCH DICTIONARY english_ispell (
    TEMPLATE = ispell,
    DictFile = english,
    AffFile = english,
    StopWords = english
);
```

Agora, podemos configurar os mapeamentos para palavras na configuração `pg`:

```
ALTER TEXT SEARCH CONFIGURATION pg
    ALTER MAPPING FOR asciiword, asciihword, hword_asciipart,
                      word, hword, hword_part
    WITH pg_dict, english_ispell, english_stem;
```

Optamos por não indexar ou pesquisar alguns tipos de token que a configuração embutida não trata:

```
ALTER TEXT SEARCH CONFIGURATION pg
    DROP MAPPING FOR email, url, url_path, sfloat, float;
```

Agora podemos testar nossa configuração:

```
SELECT * FROM ts_debug('public.pg', '
PostgreSQL, the highly scalable, SQL compliant, open source object-relational
database management system, is now undergoing beta testing of the next
version of our software.
');
```

O próximo passo é configurar a sessão para usar a nova configuração, que foi criada no esquema `public`:

```
=> \dF
   List of text search configurations
 Schema  | Name | Description
---------+------+-------------
 public  | pg   |

SET default_text_search_config = 'public.pg';
SET

SHOW default_text_search_config;
 default_text_search_config
----------------------------
 public.pg
```
