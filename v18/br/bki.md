## Capítulo 68. Declarações do Catálogo do Sistema e Conteúdo Inicial

**Índice**

* [68.1. Regras de Declaração do Catálogo do Sistema](system-catalog-declarations.md)
* [68.2. Dados Iniciais do Catálogo do Sistema](system-catalog-initial-data.md)

+ [68.2.1. Formato do arquivo de dados][(system-catalog-initial-data.md#SYSTEM-CATALOG-INITIAL-DATA-FORMAT)]
+ [68.2.2. Atribuição de OID][(system-catalog-initial-data.md#SYSTEM-CATALOG-OID-ASSIGNMENT)]
+ [68.2.3. Pesquisa de referência de OID][(system-catalog-initial-data.md#SYSTEM-CATALOG-OID-REFERENCES)]
+ [68.2.4. Criação automática de tipos de matriz][(system-catalog-initial-data.md#SYSTEM-CATALOG-AUTO-ARRAY-TYPES)]
+ [68.2.5. Receitas para edição de arquivos de dados][(system-catalog-initial-data.md#SYSTEM-CATALOG-RECIPES)]

* [68.3. Formato do arquivo BKI][(bki-format.md)
* [68.4. Comandos BKI][(bki-commands.md)
* [68.5. Estrutura do arquivo BKI Bootstrap][(bki-structure.md)
* [68.6. Exemplo BKI][(bki-example.md)

O PostgreSQL utiliza muitos catálogos diferentes do sistema para acompanhar a existência e as propriedades dos objetos do banco de dados, como tabelas e funções. Fisicamente, não há diferença entre um catálogo do sistema e uma tabela comum do usuário, mas o código C do backend conhece a estrutura e as propriedades de cada catálogo e pode manipulá-lo diretamente em um nível baixo. Assim, por exemplo, é desaconselhável tentar alterar a estrutura de um catálogo em tempo real; isso quebraria as suposições construídas no código C sobre como as linhas do catálogo são dispostas. Mas a estrutura dos catálogos pode mudar entre as versões principais.

As estruturas dos catálogos são declaradas em arquivos de cabeçalho C especialmente formatados no diretório `src/include/catalog/` da árvore de origem. Para cada catálogo, há um arquivo de cabeçalho com o nome do catálogo (por exemplo, `pg_class.h` para `pg_class`), que define o conjunto de colunas que o catálogo possui, bem como algumas outras propriedades básicas, como seu OID.

Muitos dos catálogos têm dados iniciais que devem ser carregados neles durante a fase de "bootstrap" do initdb, para levar o sistema a um ponto em que seja capaz de executar comandos SQL. (Por exemplo, `pg_class.h` deve conter uma entrada para si mesmo, bem como uma para cada outro catálogo e índice do sistema.) Esses dados iniciais são mantidos em forma editável em arquivos de dados que também são armazenados no diretório `src/include/catalog/`. Por exemplo, `pg_proc.dat` descreve todas as linhas iniciais que devem ser inseridas no catálogo `pg_proc`.

Para criar os arquivos do catálogo e carregar esses dados iniciais neles, um backend que funciona no modo bootstrap lê um arquivo BKI (Interface de Backend) que contém comandos e dados iniciais. O arquivo `postgres.bki` usado nesse modo é preparado a partir dos arquivos de cabeçalho e de dados mencionados anteriormente, ao construir uma distribuição do PostgreSQL, por meio de um script Perl chamado `genbki.pl`. Embora seja específico para uma versão particular do PostgreSQL, `postgres.bki` é independente da plataforma e é instalado no subdiretório `share` da árvore de instalação.

`genbki.pl` também produz um arquivo de cabeçalho derivado para cada catálogo, por exemplo, `pg_class_d.h` para o catálogo `pg_class`. Este arquivo contém definições de macro geradas automaticamente e pode conter outras macros, declarações de enum, etc., que podem ser úteis para o código C do cliente que lê um catálogo específico.

A maioria dos desenvolvedores do PostgreSQL não precisa se preocupar diretamente com o arquivo BKI, mas quase qualquer adição de recurso não trivial no backend exigirá a modificação dos arquivos de cabeçalho do catálogo e/ou dos arquivos de dados iniciais. O restante deste capítulo fornece algumas informações sobre isso, e, para a completude, descreve o formato do arquivo BKI.