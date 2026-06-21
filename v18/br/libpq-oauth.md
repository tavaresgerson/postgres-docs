## 32.20. Suporte a OAuth [#](#LIBPQ-OAUTH)

* [32.20.1. Ganchos Authdata](libpq-oauth.md#LIBPQ-OAUTH-AUTHDATA-HOOKS)
* [32.20.2. Configurações de depuração e de desenvolvedor](libpq-oauth.md#LIBPQ-OAUTH-DEBUGGING)

O libpq implementa suporte para o fluxo de autorização de dispositivo OAuth v2, documentado em [RFC 8628][(https://datatracker.ietf.org/doc/html/rfc8628)], como um módulo opcional. Consulte a [documentação de instalação][(install-make.md#CONFIGURE-OPTION-WITH-LIBCURL)] para obter informações sobre como habilitar o suporte à Autorização de Dispositivo como um fluxo integrado.

Quando o suporte é habilitado e o módulo opcional instalado, o libpq usará o fluxo embutido por padrão se o servidor [solicitar um token de porta][(auth-oauth.md "20.15. OAuth Authorization/Authentication")] durante a autenticação. Esse fluxo pode ser utilizado mesmo que o sistema que executa o aplicativo cliente não tenha um navegador web utilizável, por exemplo, ao executar um cliente via SSH.

O fluxo integrado, por padrão, imprimirá uma URL para visitar e um código de usuário para inserir:

```
$ psql 'dbname=postgres oauth_issuer=https://example.com oauth_client_id=...'
Visit https://example.com/device and enter the code: ABCD-EFGH
```

(Este prompt pode ser [personalizado][(libpq-oauth.md#LIBPQ-OAUTH-AUTHDATA-PROMPT-OAUTH-DEVICE)].). O usuário então fará login em seu provedor OAuth, que perguntará se deseja permitir que o libpq e o servidor realizem ações em seu nome. É sempre uma boa ideia revisar cuidadosamente o URL e as permissões exibidas, para garantir que elas correspondam às expectativas, antes de continuar. As permissões não devem ser concedidas a terceiros não confiáveis.

Os aplicativos do cliente podem implementar seus próprios fluxos para personalizar a interação e a integração com aplicativos. Consulte [Seção 32.20.1] para obter mais informações sobre como adicionar um fluxo personalizado ao libpq.

Para que um fluxo de cliente OAuth possa ser utilizado, a string de conexão deve, no mínimo, conter [oauth_issuer](libpq-connect.md#LIBPQ-CONNECT-OAUTH-ISSUER) e [oauth_client_id](libpq-connect.md#LIBPQ-CONNECT-OAUTH-CLIENT-ID). (Essas configurações são determinadas pelo provedor de OAuth da sua organização.) O fluxo integrado também exige que o servidor de autorização OAuth publique um endpoint de autorização de dispositivo.

### Nota

O fluxo de autorização de dispositivo integrado atualmente não é suportado no Windows. Fluxo de cliente personalizado ainda pode ser implementado.

### 32.20.1. Ganchos Authdata [#](#LIBPQ-OAUTH-AUTHDATA-HOOKS)

O comportamento do fluxo OAuth pode ser modificado ou substituído por um cliente usando a seguinte API de gancho:

`PQsetAuthDataHook` [#](#LIBPQ-PQSETAUTHDATAHOOK): Define o `PGauthDataHook`, substituindo o tratamento do libpq de um ou mais aspectos do fluxo do cliente OAuth.

``` void PQsetAuthDataHook(PQauthDataHook_type hook);
    ```

Se *`hook`* for `NULL`, o manipulador padrão será reinstalado. Caso contrário, o aplicativo passa um ponteiro para uma função de callback com a assinatura:

    ```
    int hook_fn(PGauthData type, PGconn *conn, void *data);
    ```

que o libpq chamará quando uma ação for necessária do aplicativo. *`type`* descreve a solicitação que está sendo feita, *`conn`* é o controle de conexão que está sendo autenticado e *`data`* aponta para metadados específicos da solicitação. O conteúdo deste ponteiro é determinado por *`type`*; veja [Seção 32.20.1.1][(libpq-oauth.md#LIBPQ-OAUTH-AUTHDATA-HOOKS-TYPES "32.20.1.1. Hook Types") para a lista de suporte.

Os hooks podem ser encadeados para permitir comportamento cooperativo e/ou de fallback. Em geral, uma implementação de hook deve examinar o *`type`* recebido (e, potencialmente, os metadados do pedido e/ou as configurações para o *`conn`* específico em uso) para decidir se deve ou não manipular um determinado pedaço de authdata. Se não, deve delegar para o hook anterior na cadeia (recuperável via `PQgetAuthDataHook`).

O sucesso é indicado pelo retorno de um inteiro maior que zero. O retorno de um inteiro negativo sinaliza uma condição de erro e abandona a tentativa de conexão. (Um valor zero é reservado para a implementação padrão.)

`PQgetAuthDataHook` [#](#LIBPQ-PQGETAUTHDATAHOOK): Retorna o valor atual de `PGauthDataHook`.

``` PQauthDataHook_type PQgetAuthDataHook(void);
    ```

No momento da inicialização (antes da primeira chamada de
`PQsetAuthDataHook`, esta função retornará
`PQdefaultAuthDataHook`.

#### 32.20.1.1. Tipos de ganchos [#](#LIBPQ-OAUTH-AUTHDATA-HOOKS-TYPES)

Os seguintes tipos `PGauthData` e suas estruturas correspondentes *`data`* são definidos:

`PQAUTHDATA_PROMPT_OAUTH_DEVICE` [#](#LIBPQ-OAUTH-AUTHDATA-PROMPT-OAUTH-DEVICE)
:   Substitui o prompt de usuário padrão durante o fluxo de cliente de autorização de dispositivo integrado. *`data`* aponta para uma instância de `PGpromptOAuthDevice`:

    ```
    typedef struct _PGpromptOAuthDevice { const char *verification_uri;   /* verification URI to visit */ const char *user_code;          /* user code to enter */ const char *verification_uri_complete;  /* optional combination of URI and
                                                 * code, or NULL */ int         expires_in;         /* seconds until user code expires */ } PGpromptOAuthDevice;
    ```

O fluxo de autorização de dispositivo OAuth que pode ser incluído em libpq requer que o usuário final visite um URL com um navegador, em seguida, insira um código que permita ao libpq se conectar ao servidor em seu nome. O prompt padrão simplesmente imprime os (install-make.md#CONFIGURE-OPTION-WITH-LIBCURL) e `verification_uri` e `user_code` em erro padrão. As implementações de substituição podem exibir essas informações usando qualquer método preferido, por exemplo, com uma GUI.

Este callback é acionado apenas durante o fluxo de autorização do dispositivo integrado. Se o aplicativo instalar um fluxo [OAuth personalizado](libpq-oauth.md#LIBPQ-OAUTH-AUTHDATA-OAUTH-BEARER-TOKEN), ou se o libpq não foi construído com suporte para o fluxo integrado, este tipo de authdata não será usado.

Se um `verification_uri_complete` que não é nulo for fornecido, ele pode ser usado opcionalmente para verificação não textual (por exemplo, exibindo um código QR). O URL e o código do usuário ainda devem ser exibidos ao usuário final neste caso, porque o código será confirmado manualmente pelo provedor, e o URL permite que os usuários continuem mesmo se não puderem usar o método não textual. Para mais informações, consulte a seção 3.3.1 em [RFC 8628][(https://datatracker.ietf.org/doc/html/rfc8628#section-3.3.1)].

`PQAUTHDATA_OAUTH_BEARER_TOKEN` [#](#LIBPQ-OAUTH-AUTHDATA-OAUTH-BEARER-TOKEN)
:   Adiciona uma implementação personalizada de um fluxo, substituindo o fluxo pré-instalado se
    ele estiver [instalado](install-make.md#CONFIGURE-OPTION-WITH-LIBCURL).
    O gancho deve retornar diretamente um token Bearer para a combinação atual de usuário/emissor/escopo, se disponível sem bloquear, ou
    de outra forma, configurar um callback assíncrono para recuperá-lo.

*`data`* aponta para uma instância de `PGoauthBearerRequest`, que deve ser preenchida pela implementação:

    ```
    typedef struct PGoauthBearerRequest { /* Hook inputs (constant across all calls) */ const char *openid_configuration; /* OIDC discovery URL */ const char *scope;                /* required scope(s), or NULL */

        /* Hook outputs */

        /*
         * Callback implementing a custom asynchronous OAuth flow. The signature is
         * platform-dependent: PQ_SOCKTYPE is SOCKET on Windows, and int everywhere
         * else. */ PostgresPollingStatusType (*async) (PGconn *conn, struct PGoauthBearerRequest *request, PQ_SOCKTYPE *altsock);

        /* Callback to clean up custom allocations. */ void        (*cleanup) (PGconn *conn, struct PGoauthBearerRequest *request);

        char       *token;   /* acquired Bearer token */ void       *user;    /* hook-defined allocated data */ } PGoauthBearerRequest;
    ```

Dois dados são fornecidos ao gancho pela libpq:
*`openid_configuration`* contém o URL de um documento de descoberta OAuth que descreve os fluxos suportados pelo servidor de autorização, e *`scope`* contém uma lista (possivelmente vazia) de escopos OAuth separados por espaços que são necessários para acessar o servidor. Uma ou ambas podem ser
`NULL` para indicar que a informação não foi descoberta. (Neste caso, as implementações podem ser capazes de estabelecer os requisitos usando algum outro conhecimento pré-configurado, ou podem optar por falhar.)

A saída final do gancho é *`token`*, que
deve apontar para um token de portador válido para uso na conexão. (Este
token deve ser emitido pelo
[oauth_issuer][(libpq-connect.md#LIBPQ-CONNECT-OAUTH-ISSUER)] e conter os escopos solicitados, ou a conexão será
rejeitada pelo módulo validador do servidor.) A string de token alocada deve
permanecer válida até que a libpq termine a conexão; o gancho
deve definir um *`cleanup`* callback que será
chamado quando a libpq não o requerer mais.

Se uma implementação não puder produzir imediatamente um
*`token`* durante a chamada inicial ao gancho,
deverá definir o *`async`* callback para lidar com
comunicação não bloqueante com o servidor de autorização.
[[16]](#ftn.id-1.7.3.27.8.3.2.3.2.2.5.3)
Isso será chamado para iniciar o fluxo imediatamente após o retorno do
gancho. Quando o callback não puder fazer mais progresso sem bloquear,
deverá retornar `PGRES_POLLING_READING` ou
`PGRES_POLLING_WRITING` após definir
`*altsock` para o descritor de arquivo que será marcado
pronto para leitura/escrita quando o progresso puder ser feito novamente. (Esse descritor
então é fornecido ao loop de pesquisa de nível superior via
`PQsocket()`.). Retorne `PGRES_POLLING_OK`
depois de definir *`token`* quando o fluxo estiver
completo, ou `PGRES_POLLING_FAILED` para indicar falha.

As implementações podem desejar armazenar dados adicionais para contabilidade em todas as chamadas aos callbacks *`async`* e *`cleanup`*. O ponteiro *`user`* é fornecido para esse propósito; a libpq não tocará em seu conteúdo e o aplicativo pode usá-lo conforme sua conveniência. (Lembre-se de liberar quaisquer alocações durante a limpeza de tokens.)

### 32.20.2. Depuração e Configurações de Desenvolvedor [#](#LIBPQ-OAUTH-DEBUGGING)

Um "modo de depuração perigoso" pode ser habilitado definindo a variável de ambiente `PGOAUTHDEBUG=UNSAFE`. Essa funcionalidade é fornecida apenas para facilitar o desenvolvimento e teste local. Ela faz várias coisas que você não vai querer que um sistema de produção faça:

* permite o uso de HTTP não criptografado durante a troca do provedor OAuth
* permite que a lista de CA de confiança do sistema seja completamente substituída usando a
`PGOAUTHCAFILE` variável de ambiente
* imprime o tráfego HTTP (contendo vários segredos críticos) no erro padrão durante o fluxo OAuth
* permite o uso de intervalos de tentativa de zero segundo, o que pode fazer com que o
cliente fique em um loop e consuma CPU sem sentido

### Aviso

Não compartilhe o tráfego de saída do fluxo OAuth com terceiros. Ele contém segredos que podem ser usados para atacar seus clientes e servidores.

---

Realizar operações de bloqueio durante o callback do gancho (#id-1.7.3.27.8.3.2.3.2.2.5.3) interferirá com APIs de conexão não bloqueáveis, como `PQAUTHDATA_OAUTH_BEARER_TOKEN`, e impedirá que conexões concorrentes avancem. Aplicativos que utilizam apenas os primitivos de conexão sincronos, como `PQconnectdb`, podem recuperar um token de forma sincrona durante o gancho em vez de implementar o *`async`*, mas eles serão necessariamente limitados a uma conexão por vez.