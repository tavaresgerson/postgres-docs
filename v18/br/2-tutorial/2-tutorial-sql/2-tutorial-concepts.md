## 2.2. Conceitos [#](#TUTORIAL-CONCEPTS)

O PostgreSQL é um *sistema de gerenciamento de banco de dados relacional* (RDBMS). Isso significa que é um sistema para gerenciar dados armazenados em *relações*. Relação é essencialmente um termo matemático para *tabela*. A noção de armazenar dados em tabelas é tão comum hoje que pode parecer inerentemente óbvio, mas há várias outras maneiras de organizar bancos de dados. Arquivos e diretórios em sistemas operacionais semelhantes ao Unix formam um exemplo de um banco de dados hierárquico. Um desenvolvimento mais moderno é o banco de dados orientado a objetos.

Cada tabela é uma coleção nomeada de *linhas*. Cada linha de uma tabela dada tem o mesmo conjunto de *colunas* nomeadas, e cada coluna é de um tipo de dados específico. Embora as colunas tenham uma ordem fixa em cada linha, é importante lembrar que o SQL não garante a ordem das linhas dentro da tabela de qualquer maneira (embora elas possam ser explicitamente ordenadas para exibição).

As tabelas são agrupadas em bancos de dados, e uma coleção de bancos de dados gerenciada por uma única instância do servidor PostgreSQL constitui um *clúster* de banco de dados.