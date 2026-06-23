## Capítulo 18. Configuração e Operação do Servidor

**Índice**

* [18.1. Conta de Usuário do PostgreSQL](postgres-user.md)
* [18.2. Criando um Clúster de Banco de Dados](creating-cluster.md)

+ [18.2.1. Uso de sistemas de arquivos secundários](creating-cluster.md#CREATING-CLUSTER-MOUNT-POINTS)
+ [18.2.2. Sistemas de arquivos](creating-cluster.md#CREATING-CLUSTER-FILESYSTEM)

* [18.3. Iniciar o servidor de banco de dados](server-start.md)

+ [18.3.1. Falhas no início do servidor](server-start.md#SERVER-START-FAILURES)
+ [18.3.2. Problemas com a conexão do cliente](server-start.md#CLIENT-CONNECTION-PROBLEMS)

* [18.4. Gerenciamento de Recursos do Kernel](kernel-resources.md)

+ [18.4.1. Memória compartilhada e semaforos](kernel-resources.md#SYSVIPC)
+ [18.4.2. RemoveIPC do systemd](kernel-resources.md#SYSTEMD-REMOVEIPC)
+ [18.4.3. Limites de recursos](kernel-resources.md#KERNEL-RESOURCES-LIMITS)
+ [18.4.4. Sobrecommit de memória no Linux](kernel-resources.md#LINUX-MEMORY-OVERCOMMIT)
+ [18.4.5. Páginas enormes no Linux](kernel-resources.md#LINUX-HUGE-PAGES)

* [18.5. Desligar o servidor](server-shutdown.md)
* [18.6. Atualizar um cluster PostgreSQL](upgrading.md)

+ [18.6.1. Atualização de dados via pg_dumpall](upgrading.md#UPGRADING-VIA-PGDUMPALL)
+ [18.6.2. Atualização de dados via pg_upgrade](upgrading.md#UPGRADING-VIA-PG-UPGRADE)
+ [18.6.3. Atualização de dados via Replicação](upgrading.md#UPGRADING-VIA-REPLICATION)

* [18.7. Prevenção de falsificação de servidor](preventing-server-spoofing.md)
* [18.8. Opções de criptografia](encryption-options.md)
* [18.9. Conexões seguras TCP/IP com SSL](ssl-tcp.md)

+ [18.9.1. Configuração Básica](ssl-tcp.md#SSL-SETUP)
+ [18.9.2. Configuração do OpenSSL](ssl-tcp.md#SSL-OPENSSL-CONFIG)
+ [18.9.3. Uso de Certificados de Cliente](ssl-tcp.md#SSL-CLIENT-CERTIFICATES)
+ [18.9.4. Uso do Arquivo do Servidor SSL](ssl-tcp.md#SSL-SERVER-FILES)
+ [18.9.5. Criação de Certificados](ssl-tcp.md#SSL-CERTIFICATE-CREATION)

* [18.10. Conexões TCP/IP seguras com criptografia GSSAPI](gssapi-enc.md)

+ [18.10.1. Configuração Básica](gssapi-enc.md#GSSAPI-SETUP)

* [18.11. Conexões seguras TCP/IP com túneis SSH](ssh-tunnels.md)
* [18.12. Registro do Diário de Eventos no Windows](event-log-registration.md)

Este capítulo discute como configurar e executar o servidor de banco de dados e suas interações com o sistema operacional.

As instruções neste capítulo pressupõem que você está trabalhando com PostgreSQL simples sem qualquer infraestrutura adicional, por exemplo, uma cópia que você construiu a partir do código fonte de acordo com as instruções dos capítulos anteriores. Se você está trabalhando com uma versão pré-embalada ou fornecida pelo fornecedor do PostgreSQL, é provável que o pacote tenha feito disposições especiais para a instalação e inicialização do servidor de banco de dados de acordo com as convenções do seu sistema. Consulte a documentação do nível do pacote para obter detalhes.