## Capítulo 21. Papéis de banco de dados

**Índice**

* [21.1. Papéis de banco de dados](database-roles.md)
* [21.2. Atributos de papel](role-attributes.md)
* [21.3. Membros do papel](role-membership.md)
* [21.4. Remoção de papéis](role-removal.md)
* [21.5. Papéis predefinidos](predefined-roles.md)
* [21.6. Segurança de função](perm-functions.md)

O PostgreSQL gerencia as permissões de acesso ao banco de dados usando o conceito de *roles*. Um role pode ser considerado como um usuário do banco de dados ou um grupo de usuários do banco de dados, dependendo de como o role é configurado. Os roles podem possuir objetos do banco de dados (por exemplo, tabelas e funções) e podem atribuir privilégios a esses objetos a outros roles para controlar quem tem acesso a quais objetos. Além disso, é possível conceder *membriado* em um role a outro role, permitindo assim que o role membro use privilégios atribuídos a outro role.

O conceito de papéis subsume os conceitos de “usuários” e “grupos”. Nas versões do PostgreSQL anteriores à versão 8.1, os usuários e os grupos eram tipos distintos de entidades, mas agora existem apenas papéis. Qualquer papel pode atuar como um usuário, um grupo ou ambos.

Este capítulo descreve como criar e gerenciar papéis. Mais informações sobre os efeitos dos privilégios de papel em vários objetos do banco de dados podem ser encontradas em [Seção 5.8](ddl-priv.md).