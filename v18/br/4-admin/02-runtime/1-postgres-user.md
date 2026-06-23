## 18.1. A Conta de Usuário do PostgreSQL [#](#POSTGRES-USER)

Como qualquer daemon de servidor que é acessível ao mundo externo, é aconselhável executar o PostgreSQL sob uma conta de usuário separada. Essa conta de usuário deve possuir apenas os dados que são gerenciados pelo servidor e não deve ser compartilhada com outros daemon. (Por exemplo, usar o usuário `nobody` é uma má ideia.) Em particular, é aconselhável que essa conta de usuário não possua os arquivos executáveis do PostgreSQL, para garantir que um processo de servidor comprometido não possa modificar esses executáveis.

As versões pré-embaladas do PostgreSQL geralmente criam uma conta de usuário adequada automaticamente durante a instalação do pacote.

Para adicionar uma conta de usuário Unix ao seu sistema, procure um comando `useradd` ou `adduser`. O nome do usuário postgres é frequentemente usado e é assumido ao longo deste livro, mas você pode usar outro nome se preferir.