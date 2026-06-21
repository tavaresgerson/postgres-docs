## 54.3. Autenticação SASL [#](#SASL-AUTHENTICATION)

* [54.3.1. Autenticação SCRAM-SHA-256](sasl-authentication.md#SASL-SCRAM-SHA-256)
* [54.3.2. Autenticação OAUTHBEARER](sasl-authentication.md#SASL-OAUTHBEARER)

*SASL* é uma estrutura para autenticação em protocolos orientados a conexão. No momento, o PostgreSQL implementa três mecanismos de autenticação SASL: SCRAM-SHA-256, SCRAM-SHA-256-PLUS e OAUTHBEARER. Mais podem ser adicionados no futuro. Os passos abaixo ilustram como a autenticação SASL é realizada em geral, enquanto as próximas subseções fornecem mais detalhes sobre mecanismos específicos.

Fluxo de Mensagem de Autenticação SASL

1. Para iniciar uma troca de autenticação SASL, o servidor envia uma mensagem de AutenticaçãoSASL. Ela inclui uma lista de mecanismos de autenticação SASL que o servidor pode aceitar, na ordem preferida do servidor.
2. O cliente seleciona um dos mecanismos suportados da lista e envia uma mensagem SASLInitialResponse ao servidor. A mensagem inclui o nome do mecanismo selecionado e uma Resposta Inicial do Cliente opcional, se o mecanismo selecionado o usar.
3. Um ou mais desafios do servidor e mensagens de resposta do cliente seguirão. Cada desafio do servidor é enviado em uma mensagem de AutenticaçãoSASLContinue, seguida por uma resposta do cliente em uma mensagem SASLResponse. Os detalhes das mensagens são específicos do mecanismo.
4. Finalmente, quando a troca de autenticação é concluída com sucesso, o servidor envia uma mensagem opcional de AutenticaçãoSASLFinal, seguida imediatamente por uma mensagem AuthenticationOk. A AutenticaçãoSASLFinal contém dados adicionais do servidor para o cliente, cujo conteúdo é específico do mecanismo de autenticação selecionado. Se o mecanismo de autenticação não usar dados adicionais enviados na conclusão, a mensagem de AutenticaçãoSASLFinal não é enviada.

Em caso de erro, o servidor pode abortar a autenticação em qualquer estágio e enviar uma ErrorMessage.

### 54.3.1. Autenticação SCRAM-SHA-256 [#](#SASL-SCRAM-SHA-256)

`SCRAM-SHA-256`, e sua variante com vinculação de canal `SCRAM-SHA-256-PLUS`, são mecanismos de autenticação baseados em senha. Eles são descritos em detalhes em [RFC 7677][(https://datatracker.ietf.org/doc/html/rfc7677)] e [RFC 5802][(https://datatracker.ietf.org/doc/html/rfc5802)].

Quando o SCRAM-SHA-256 é usado no PostgreSQL, o servidor ignorará o nome do usuário que o cliente envia no `client-first-message`. O nome do usuário que já foi enviado na mensagem de inicialização é usado em vez disso. O PostgreSQL suporta múltiplos codificações de caracteres, enquanto o SCRAM dita que o UTF-8 deve ser usado para o nome do usuário, então pode ser impossível representar o nome do usuário do PostgreSQL em UTF-8.

A especificação SCRAM determina que a senha também é em UTF-8 e é processada com o algoritmo *SASLprep*. No entanto, o PostgreSQL não exige que a UTF-8 seja usada para a senha. Quando a senha de um usuário é definida, ela é processada com SASLprep como se estivesse em UTF-8, independentemente da codificação real usada. No entanto, se não for uma sequência de bytes UTF-8 legal ou se contiver sequências de bytes UTF-8 que são proibidas pelo algoritmo SASLprep, a senha bruta será usada sem processamento SASLprep, em vez de lançar um erro. Isso permite que a senha seja normalizada quando está em UTF-8, mas ainda permite que uma senha não em UTF-8 seja usada e não exige que o sistema saiba em qual codificação a senha está.

O *binding de canal* é suportado em edições do PostgreSQL com suporte SSL. O nome do mecanismo SASL para SCRAM com binding de canal é `SCRAM-SHA-256-PLUS`. O tipo de binding de canal usado pelo PostgreSQL é `tls-server-end-point`.

No SCRAM sem vinculação de canal, o servidor escolhe um número aleatório que é transmitido ao cliente para ser misturado com a senha fornecida pelo usuário no hash da senha transmitida. Embora isso impeça o hash da senha de ser retransmitido com sucesso em uma sessão posterior, não impede que um servidor falso entre o servidor real e o cliente passe pelo valor aleatório do servidor e autentique com sucesso.

O SCRAM com vinculação de canal previne ataques de homem no meio ao misturar a assinatura do certificado do servidor no hash da senha transmitida. Embora um servidor falso possa retransmitir o certificado do servidor real, ele não tem acesso à chave privada correspondente a esse certificado e, portanto, não pode provar que é o proprietário, causando falha na conexão SSL.

**Exemplo**

1. O servidor envia uma mensagem de AutenticaçãoSASL. Ela inclui uma lista de mecanismos de autenticação SASL que o servidor pode aceitar. Isso será `SCRAM-SHA-256-PLUS` e `SCRAM-SHA-256` se o servidor for construído com suporte SSL, ou apenas o último.
2. O cliente responde enviando uma mensagem SASLInitialResponse, que indica o mecanismo escolhido, `SCRAM-SHA-256` ou `SCRAM-SHA-256-PLUS`. (O cliente é livre para escolher qualquer mecanismo, mas para melhor segurança, deve escolher a variante de vinculação de canal se puder suportá-la.) No campo de resposta do Cliente Inicial, a mensagem contém o SCRAM `client-first-message`. O `client-first-message` também contém o tipo de vinculação de canal escolhido pelo cliente.
3. O servidor envia uma mensagem de AutenticaçãoSASLContinue, com um SCRAM `server-first-message` como conteúdo.
4. O cliente envia uma mensagem SASLResponse, com SCRAM `client-final-message` como conteúdo.
5. O servidor envia uma mensagem de AutenticaçãoSASLFinal, com o SCRAM `server-final-message`, seguida imediatamente por uma mensagem de AutenticaçãoOk.

### 54.3.2. Autenticação OAUTHBEARER [#](#SASL-OAUTHBEARER)

`OAUTHBEARER` é um mecanismo baseado em tokens para autenticação federada. Ele é descrito em detalhes em [RFC 7628][(https://datatracker.ietf.org/doc/html/rfc7628)].

Uma troca típica difere dependendo se o cliente já tem um token portador armazenado em cache para o usuário atual. Se não tiver, a troca ocorrerá em duas conexões: a primeira conexão de "descoberta" para obter metadados OAuth do servidor e a segunda conexão para enviar o token após o cliente tê-lo obtido. (O libpq atualmente não implementa um método de cache como parte de seu fluxo integrado, então ele usa a troca de duas conexões.)

Esse mecanismo é iniciado pelo cliente, assim como o SCRAM. A resposta inicial do cliente consiste no cabeçalho padrão "GS2" usado pelo SCRAM, seguido de uma lista de pares `key=value`. A única chave atualmente suportada pelo servidor é `auth`, que contém o token de portador. `OAUTHBEARER` especifica adicionalmente três componentes opcionais da resposta inicial do cliente (os `authzid` do cabeçalho GS2 e as chaves `host` e `port`) que são atualmente ignorados pelo servidor.

`OAUTHBEARER` não suporta a vinculação de canal, e não há mecanismo de "OAUTHBEARER-PLUS". Esse mecanismo não utiliza dados do servidor durante uma autenticação bem-sucedida, portanto, a mensagem AuthenticationSASLFinal não é usada na troca.

**Exemplo**

1. Durante a primeira troca, o servidor envia uma mensagem de Autenticação SASL com o mecanismo `OAUTHBEARER` anunciado.
2. O cliente responde enviando uma mensagem SASLInitialResponse que indica o mecanismo `OAUTHBEARER`. Supondo que o cliente não tenha um token de portador válido para o usuário atual, o campo `auth` está vazio, indicando uma conexão de descoberta.
3. O servidor envia uma mensagem de Autenticação SASLContinue contendo um erro `status` ao lado de um URI bem conhecido e escopos que o cliente deve usar para conduzir um fluxo OAuth.
4. O cliente envia uma mensagem SASLResponse contendo o conjunto vazio (um único byte `0x01`) para finalizar sua metade da troca de descoberta.
5. O servidor envia uma ErrorMessage para falhar a primeira troca.

Neste ponto, o cliente realiza um dos muitos fluxos possíveis de OAuth para obter um token de portador, usando qualquer metadados que tenha sido configurado além daqueles fornecidos pelo servidor. (Esta descrição é deixada deliberadamente vaga; `OAUTHBEARER` não especifica ou não exige nenhum método particular para obter um token.)

Uma vez que tenha um token, o cliente se reconecta ao servidor para a troca final:
6. O servidor, novamente, envia uma mensagem de Autenticação SASL com o mecanismo `OAUTHBEARER` anunciado.
7. O cliente responde enviando uma mensagem SASLInitialResponse, mas, desta vez, o campo `auth` na mensagem contém o token de portador que foi obtido durante o fluxo do cliente.
8. O servidor valida o token de acordo com as instruções do provedor do token. Se o cliente estiver autorizado a se conectar, ele envia uma mensagem AuthenticationOk para finalizar a troca SASL.