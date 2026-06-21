## Capítulo 54. Protocolo Frontend/Backend

**Índice**

* [54.1. Visão geral](protocol-overview.md)

+ [54.1.1. Visão geral de mensagens](protocol-overview.md#PROTOCOL-MESSAGE-CONCEPTS)
+ [54.1.2. Visão geral de consultas extensas](protocol-overview.md#PROTOCOL-QUERY-CONCEPTS)
+ [54.1.3. Formatos e códigos de formato](protocol-overview.md#PROTOCOL-FORMAT-CODES)
+ [54.1.4. Versões de protocolo](protocol-overview.md#PROTOCOL-VERSIONS)

* [54.2. Fluxo de Mensagem](protocol-flow.md)

+ [54.2.1. Início de sessão](protocol-flow.md#PROTOCOL-FLOW-START-UP)
+ [54.2.2. Consulta simples](protocol-flow.md#PROTOCOL-FLOW-SIMPLE-QUERY)
+ [54.2.3. Consulta estendida](protocol-flow.md#PROTOCOL-FLOW-EXT-QUERY)
+ [54.2.4. Pipelining](protocol-flow.md#PROTOCOL-FLOW-PIPELINING)
+ [54.2.5. Chamada de função](protocol-flow.md#PROTOCOL-FLOW-FUNCTION-CALL)
+ [54.2.6. Operações de cópia](protocol-flow.md#PROTOCOL-COPY)
+ [54.2.7. Operações assíncronas](protocol-flow.md#PROTOCOL-ASYNC)
+ [54.2.8. Cancelamento de solicitações em andamento](protocol-flow.md#PROTOCOL-FLOW-CANCELING-REQUESTS)
+ [54.2.9. Termina��o](protocol-flow.md#PROTOCOL-FLOW-TERMINATION)
+ [54.2.10. Criptografia de sessão SSL](protocol-flow.md#PROTOCOL-FLOW-SSL)
+ [54.2.11. Criptografia de sessão GSSAPI](protocol-flow.md#PROTOCOL-FLOW-GSSAPI)

* [54.3. Autenticação SASL](sasl-authentication.md)

+ [54.3.1. Autenticação SCRAM-SHA-256](sasl-authentication.md#SASL-SCRAM-SHA-256)
+ [54.3.2. Autenticação OAUTHBEARER](sasl-authentication.md#SASL-OAUTHBEARER)

* [54.4. Protocolo de Replicação de Streaming](protocol-replication.md)
* [54.5. Protocolo de Replicação de Streaming Lógico](protocol-logical-replication.md)

+ [54.5.1. Parâmetros de Replicação de Streaming Lógico](protocol-logical-replication.md#PROTOCOL-LOGICAL-REPLICATION-PARAMS)
+ [54.5.2. Mensagens de Protocolo de Replicação Lógico](protocol-logical-replication.md#PROTOCOL-LOGICAL-MESSAGES)
+ [54.5.3. Fluxo de Mensagens de Protocolo de Replicação Lógico](protocol-logical-replication.md#PROTOCOL-LOGICAL-MESSAGES-FLOW)

* [54.6. Tipos de dados de mensagem](protocol-message-types.md)
* [54.7. Formatos de mensagem](protocol-message-formats.md)
* [54.8. Campos de mensagens de erro e aviso](protocol-error-fields.md)
* [54.9. Formatos de mensagens de replicação lógica](protocol-logicalrep-message-formats.md)
* [54.10. Resumo das alterações desde o Protocolo 2.0](protocol-changes.md)

O PostgreSQL utiliza um protocolo baseado em mensagens para comunicação entre frontends e backends (clientes e servidores). O protocolo é suportado por TCP/IP e também por sockets de domínio Unix. O número de porta 5432 foi registrado na IANA como o número de porta TCP convencional para servidores que suportam este protocolo, mas, na prática, qualquer número de porta não privilegiada pode ser usado.

Este documento descreve a versão 3.2 do protocolo, introduzida na versão 18 do PostgreSQL. O servidor e a biblioteca de cliente libpq são compatíveis com a versão 3.0 do protocolo, implementada no PostgreSQL 7.4 e versões posteriores.

Para atender a vários clientes de forma eficiente, o servidor lança um novo processo de "back-end" para cada cliente. Na implementação atual, um novo processo filho é criado imediatamente após a detecção de uma conexão recebida. Isso é transparente para o protocolo, no entanto. Para fins do protocolo, os termos "back-end" e "servidor" são intercambiáveis; da mesma forma, "front-end" e "cliente" são intercambiáveis.