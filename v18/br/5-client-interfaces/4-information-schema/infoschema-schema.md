## 35.1. O Esquema [#](#INFOSCHEMA-SCHEMA)

O próprio esquema de informações é um esquema chamado `information_schema`. Esse esquema existe automaticamente em todos os bancos de dados. O proprietário desse esquema é o usuário inicial do banco de dados no clúster, e esse usuário naturalmente tem todos os privilégios nesse esquema, incluindo a capacidade de descartá-lo (mas a economia de espaço alcançada por isso é mínima).

Por padrão, o esquema de informações não está no caminho de pesquisa do esquema, então você precisa acessar todos os objetos nele por meio de nomes qualificados. Como os nomes de alguns dos objetos no esquema de informações são nomes genéricos que podem ocorrer em aplicativos de usuários, você deve ter cuidado se quiser colocar o esquema de informações no caminho.