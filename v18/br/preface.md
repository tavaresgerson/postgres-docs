# Prefácio

**Índice**

* [1. O que é PostgreSQL?](intro-whatis.md)
* [2. Uma breve história do PostgreSQL](history.md)

+ [2.1. O Projeto Berkeley POSTGRES](history.md#HISTORY-BERKELEY)
+ [2.2. Postgres95](history.md#HISTORY-POSTGRES95)
+ [2.3. PostgreSQL](history.md#HISTORY-POSTGRESQL)

* [3. Convenções](notation.md)
* [4. Informações adicionais](resources.md)
* [5. Diretrizes de relatórios de bugs](bug-reporting.md)

+ [5.1. Identificação de Bugs](bug-reporting.md#BUG-REPORTING-IDENTIFYING-BUGS)
+ [5.2. O que Relatar](bug-reporting.md#BUG-REPORTING-WHAT-TO-REPORT)
+ [5.3. Onde Relatar Bugs](bug-reporting.md#BUG-REPORTING-WHERE-TO-REPORT-BUGS)

Este livro é a documentação oficial do PostgreSQL. Foi escrito pelos desenvolvedores do PostgreSQL e por outros voluntários em paralelo ao desenvolvimento do software PostgreSQL. Ele descreve todas as funcionalidades que a versão atual do PostgreSQL suporta oficialmente.

Para tornar a grande quantidade de informações sobre PostgreSQL gerenciável, este livro foi organizado em várias partes. Cada parte é direcionada a uma classe diferente de usuários, ou a usuários em diferentes estágios de sua experiência com PostgreSQL:

* [Parte I](tutorial.md) é uma introdução informal para novos usuários.
* [Parte II](sql.md) documenta o ambiente de linguagem de consulta SQL, incluindo tipos de dados e funções, bem como ajustes de desempenho em nível de usuário. Todo usuário do PostgreSQL deve ler isso.
* [Parte III](admin.md) descreve a instalação e administração do servidor. Todos que executam um servidor PostgreSQL, seja para uso privado ou para outros, devem ler esta parte.
* [Parte IV](client-interfaces.md) descreve as interfaces de programação para programas clientes do PostgreSQL.
* [Parte V](server-programming.md) contém informações para usuários avançados sobre as capacidades de extensibilidade do servidor. Os tópicos incluem tipos de dados e funções definidos pelo usuário.
* [Parte VI](reference.md) contém informações de referência sobre comandos SQL, programas de cliente e servidor. Esta parte suporta as outras partes com informações estruturadas, classificadas por comando ou programa.
* [Parte VII](internals.md) contém informações variadas que podem ser úteis para desenvolvedores do PostgreSQL.