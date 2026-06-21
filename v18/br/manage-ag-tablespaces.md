## 22.6. Tablespaces [#](#MANAGE-AG-TABLESPACES)

Os tablespaces no PostgreSQL permitem que os administradores de banco de dados definam locais no sistema de arquivos onde os arquivos que representam os objetos do banco de dados podem ser armazenados. Uma vez criado, um tablespace pode ser referido pelo nome ao criar objetos do banco de dados.

Ao usar tablespaces, um administrador pode controlar o layout do disco de uma instalação do PostgreSQL. Isso é útil de pelo menos duas maneiras. Primeiro, se a partição ou o volume em que o clúster foi inicializado ficar sem espaço e não puder ser estendido, um tablespace pode ser criado em uma partição diferente e usado até que o sistema possa ser reconfigurado.

Em segundo lugar, os tablespaces permitem que um administrador use o conhecimento do padrão de uso dos objetos do banco de dados para otimizar o desempenho. Por exemplo, um índice que é muito utilizado pode ser colocado em um disco muito rápido e altamente disponível, como um dispositivo de estado sólido caro. Ao mesmo tempo, uma tabela que armazena dados arquivados que são raramente utilizados ou não críticos para o desempenho pode ser armazenada em um sistema de disco menos caro e mais lento.

### Aviso

Embora localizada fora do diretório principal de dados do PostgreSQL, os espaços de tabela são uma parte integrante do clúster do banco de dados e *não podem* ser tratados como uma coleção autônoma de arquivos de dados. Eles dependem dos metadados contidos no diretório principal de dados e, portanto, não podem ser anexados a um clúster de banco de dados diferente ou fazer backup individualmente. Da mesma forma, se você perder um espaço de tabela (deleção de arquivo, falha no disco, etc.), o clúster do banco de dados pode se tornar ilegível ou incapaz de iniciar. Colocar um espaço de tabela em um sistema de arquivos temporário, como um disco RAM, arrisca a confiabilidade de todo o clúster.

Para definir um tablespace, use o comando [CREATE TABLESPACE](sql-createtablespace.md "CREATE TABLESPACE"), por exemplo:

```
CREATE TABLESPACE fastspace LOCATION '/ssd1/postgresql/data';
```

O local deve ser um diretório existente e vazio que seja de propriedade do usuário do sistema operacional PostgreSQL. Todos os objetos posteriormente criados dentro do espaço de tabelas serão armazenados em arquivos abaixo deste diretório. O local não deve estar em armazenamento removível ou transitório, pois o clúster pode não funcionar corretamente se o espaço de tabelas estiver ausente ou perdido.

### Nota

Geralmente, não há muito sentido em criar mais de um espaço de tabela por sistema de arquivos lógico, uma vez que você não pode controlar a localização dos arquivos individuais dentro de um sistema de arquivos lógico. No entanto, o PostgreSQL não impõe nenhuma limitação desse tipo e, de fato, não está diretamente consciente dos limites do sistema de arquivos em seu sistema. Ele apenas armazena arquivos nos diretórios que você lhe diz para usar.

A criação do próprio tablespace deve ser feita como um superusuário do banco de dados, mas, depois disso, você pode permitir que usuários comuns do banco de dados o usem. Para fazer isso, conceda a eles o privilégio `CREATE` sobre ele.

Tabelas, índices e bancos de dados inteiros podem ser atribuídos a tabelas específicas. Para fazer isso, um usuário com o privilégio `CREATE` em um determinado espaço de tabelas deve passar o nome do espaço de tabelas como um parâmetro no comando relevante. Por exemplo, o seguinte cria uma tabela no espaço de tabelas `space1`:

```
CREATE TABLE foo(i int) TABLESPACE space1;
```

Alternativamente, use o parâmetro [default_tablespace][(runtime-config-client.md#GUC-DEFAULT-TABLESPACE)]:

```
SET default_tablespace = space1;
CREATE TABLE foo(i int);
```

Quando `default_tablespace` é definido como qualquer coisa, exceto uma string vazia, ele fornece uma cláusula implícita para `TABLESPACE` para comandos `CREATE TABLE` e `CREATE INDEX` que não possuem uma cláusula explícita.

Existe também um parâmetro [temp_tablespaces][(runtime-config-client.md#GUC-TEMP-TABLESPACES)], que determina a colocação de tabelas e índices temporários, bem como arquivos temporários que são usados para fins como o ordenamento de grandes conjuntos de dados. Isso pode ser uma lista de nomes de tablespace, e não apenas um, para que a carga associada aos objetos temporários possa ser espalhada por vários tablespace. Um membro aleatório da lista é escolhido a cada vez que um objeto temporário deve ser criado.

O tablespace associado a um banco de dados é usado para armazenar os catálogos do sistema desse banco de dados. Além disso, é o tablespace padrão usado para tabelas, índices e arquivos temporários criados dentro do banco de dados, se não houver cláusula `TABLESPACE` e nenhuma outra seleção seja especificada por `default_tablespace` ou `temp_tablespaces` (conforme apropriado). Se um banco de dados for criado sem especificar um tablespace para ele, ele usa o mesmo tablespace que o banco de dados de modelo do qual é copiado.

Dois tablespaces são criados automaticamente quando o clúster do banco de dados é inicializado. O tablespace `pg_global` é usado apenas para catálogos de sistema compartilhados. O tablespace `pg_default` é o tablespace padrão dos bancos de dados `template1` e `template0` (e, portanto, será o tablespace padrão também para outros bancos de dados, a menos que seja sobrescrito por uma cláusula `TABLESPACE` em `CREATE DATABASE`).

Uma vez criado, um espaço de tabela pode ser usado a partir de qualquer banco de dados, desde que o usuário solicitante tenha privilégios suficientes. Isso significa que um espaço de tabela não pode ser excluído até que todos os objetos em todos os bancos de dados que utilizam o espaço de tabela tenham sido removidos.

Para remover um espaço de tabela vazio, use o comando [DROP TABLESPACE](sql-droptablespace.md "DROP TABLESPACE").

Para determinar o conjunto de espaços de tabela existentes, examine o catálogo do sistema `pg_tablespace`(catalog-pg-tablespace.md "52.56. pg_tablespace"), por exemplo.

```
SELECT spcname, spcowner::regrole, pg_tablespace_location(oid) FROM pg_tablespace;
```

É possível descobrir quais bancos de dados utilizam quais tablespaces; veja [Tabela 9.76][(functions-info.md#FUNCTIONS-INFO-CATALOG-TABLE "Table 9.76. System Catalog Information Functions")]. O meta-comando `\db` do programa [psql][(app-psql.md "psql")] também é útil para listar os tablespaces existentes.

O diretório `$PGDATA/pg_tblspc` contém links simbólicos que apontam para cada um dos espaços de tabela não pré-definidos no clúster. Embora não seja recomendado, é possível ajustar o layout do espaço de tabela manualmente, redefinindo esses links. Em nenhuma circunstância realize essa operação enquanto o servidor estiver em execução.