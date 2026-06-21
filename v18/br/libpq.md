## Capítulo 32. libpq — Biblioteca C

**Índice**

* [32.1. Funções de Controle de Conexão de Banco de Dados](libpq-connect.md)

+ [32.1.1. Conexões de conexão][(libpq-connect.md#LIBPQ-CONNSTRING)]
+ [32.1.2. Palavras-chave de parâmetros][(libpq-connect.md#LIBPQ-PARAMKEYWORDS)]

* [32.2. Funções de Status de Conexão](libpq-status.md)
* [32.3. Funções de Execução de Comandos](libpq-exec.md)

+ [32.3.1. Funções Principais][(libpq-exec.md#LIBPQ-EXEC-MAIN)]
+ [32.3.2. Recuperação de Informações do Resultado da Consulta][(libpq-exec.md#LIBPQ-EXEC-SELECT-INFO)]
+ [32.3.3. Recuperação de Outras Informações do Resultado][(libpq-exec.md#LIBPQ-EXEC-NONSELECT)]
+ [32.3.4. Echappement de Strings para Inclusão em Comandos SQL][(libpq-exec.md#LIBPQ-EXEC-ESCAPE-STRING)]

* [32.4. Processamento de comandos assíncrono](libpq-async.md)
* [32.5. Modo Pipeline](libpq-pipeline-mode.md)

+ [32.5.1. Uso do Modo Pipeline][(libpq-pipeline-mode.md#LIBPQ-PIPELINE-USING)]
+ [32.5.2. Funções Associadas ao Modo Pipeline][(libpq-pipeline-mode.md#LIBPQ-PIPELINE-FUNCTIONS)]
+ [32.5.3. Quando Usar o Modo Pipeline][(libpq-pipeline-mode.md#LIBPQ-PIPELINE-TIPS)]

* [32.6. Recuperação de resultados de consulta em partes](libpq-single-row-mode.md)
* [32.7. Cancelamento de consultas em andamento](libpq-cancel.md)

+ [32.7.1. Funções para Enviar Solicitações de Cancelamento](libpq-cancel.md#LIBPQ-CANCEL-FUNCTIONS)
+ [32.7.2. Funções Obsoletas para Enviar Solicitações de Cancelamento](libpq-cancel.md#LIBPQ-CANCEL-DEPRECATED)

* [32.8. Interface de Caminho Rápido][(libpq-fastpath.md)]
* [32.9. Notificação Assíncrona][(libpq-notify.md)]
* [32.10. Funções Associadas ao Comando `COPY`][(libpq-copy.md)]

+ [32.10.1. Funções para enviar dados do `COPY`](libpq-copy.md#LIBPQ-COPY-SEND)
+ [32.10.2. Funções para receber dados do `COPY`](libpq-copy.md#LIBPQ-COPY-RECEIVE)
+ [32.10.3. Funções obsoletas para `COPY`](libpq-copy.md#LIBPQ-COPY-DEPRECATED)

* [32.11. Funções de Controle](libpq-control.md)
* [32.12. Funções Diversas](libpq-misc.md)
* [32.13. Processamento de Notificações](libpq-notice-processing.md)
* [32.14. Sistema de Eventos](libpq-events.md)

+ [32.14.1. Tipos de Evento](libpq-events.md#LIBPQ-EVENTS-TYPES)
+ [32.14.2. Procedimento de Callback de Evento](libpq-events.md#LIBPQ-EVENTS-PROC)
+ [32.14.3. Funções de Suporte de Evento](libpq-events.md#LIBPQ-EVENTS-FUNCS)
+ [32.14.4. Exemplo de Evento](libpq-events.md#LIBPQ-EVENTS-EXAMPLE)

* [32.15. Variáveis de Ambiente](libpq-envars.md)
* [32.16. O arquivo de senha](libpq-pgpass.md)
* [32.17. O arquivo do serviço de conexão](libpq-pgservice.md)
* [32.18. Busca LDAP dos parâmetros de conexão](libpq-ldap.md)
* [32.19. Suporte SSL](libpq-ssl.md)

+ [32.19.1. Verificação do Cliente dos Certificados do Servidor][(libpq-ssl.md#LIBQ-SSL-CERTIFICATES)]
+ [32.19.2. Certificados do Cliente][(libpq-ssl.md#LIBPQ-SSL-CLIENTCERT)]
+ [32.19.3. Proteção Fornecida em Diferentes Modos][(libpq-ssl.md#LIBPQ-SSL-PROTECTION)]
+ [32.19.4. Uso do Arquivo de Cliente SSL][(libpq-ssl.md#LIBPQ-SSL-FILEUSAGE)]
+ [32.19.5. Inicialização da Biblioteca SSL][(libpq-ssl.md#LIBPQ-SSL-INITIALIZE)]

* [32.20. Suporte OAuth](libpq-oauth.md)

+ [32.20.1. Ganchos de Authdata](libpq-oauth.md#LIBPQ-OAUTH-AUTHDATA-HOOKS)
+ [32.20.2. Configurações de depuração e desenvolvedor](libpq-oauth.md#LIBPQ-OAUTH-DEBUGGING)

* [32.21. Comportamento em programas em emaranhados][(libpq-threading.md)]
* [32.22. Construção de programas libpq][(libpq-build.md)]
* [32.23. Programas de exemplo][(libpq-example.md)]

libpq é a interface do programador de aplicativos em C para PostgreSQL. libpq é um conjunto de funções de biblioteca que permitem que programas cliente passem consultas ao servidor de banco de dados PostgreSQL e recebam os resultados dessas consultas.

libpq também é o mecanismo subjacente para várias outras interfaces de aplicativos do PostgreSQL, incluindo aquelas escritas para C++, Perl, Python, Tcl e ECPG. Portanto, alguns aspectos do comportamento do libpq serão importantes para você se você usar um desses pacotes. Em particular, [Seção 32.15][(libpq-envars.md "32.15. Environment Variables")], [Seção 32.16][(libpq-pgpass.md "32.16. The Password File")] e [Seção 32.19][(libpq-ssl.md "32.19. SSL Support")] descrevem comportamentos que são visíveis para o usuário de qualquer aplicativo que use libpq.

Alguns programas curtos estão incluídos no final deste capítulo ([Seção 32.23][(libpq-example.md "32.23. Example Programs")]) para mostrar como escrever programas que utilizam o libpq. Há também vários exemplos completos de aplicações do libpq no diretório `src/test/examples` na distribuição do código-fonte.

Os programas de clientes que utilizam o libpq devem incluir o arquivo de cabeçalho `libpq-fe.h` e devem ser vinculados com a biblioteca libpq.