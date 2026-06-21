## 50.1. Projetar com Segurança um Módulo de Validação [#](#OAUTH-VALIDATOR-DESIGN)

* [50.1.1. Responsabilidades do Validador](oauth-validator-design.md#OAUTH-VALIDATOR-DESIGN-RESPONSIBILITIES)
* [50.1.2. Diretrizes Gerais de Codificação](oauth-validator-design.md#OAUTH-VALIDATOR-DESIGN-GUIDELINES)
* [50.1.3. Autorização de Usuários (Delegação do Usermap)](oauth-validator-design.md#OAUTH-VALIDATOR-DESIGN-USERMAP-DELEGATION)

### Aviso

Leia e entenda a totalidade desta seção antes de implementar um módulo de validação. Um módulo de validação com mau funcionamento é potencialmente pior do que não ter autenticação alguma, tanto por causa do falso senso de segurança que ele oferece, quanto porque pode contribuir para ataques contra outros componentes de um ecossistema OAuth.

### 50.1.1. Responsabilidades do Validador [#](#OAUTH-VALIDATOR-DESIGN-RESPONSIBILITIES)

Embora módulos diferentes possam adotar abordagens muito diferentes para a validação de tokens, as implementações geralmente precisam realizar três ações separadas:

Valide o Token: O validador deve primeiro garantir que o token apresentado é, de fato, um token Bearer válido para uso na autenticação do cliente. A maneira correta de fazer isso depende do provedor, mas geralmente envolve operações criptográficas para provar que o token foi criado por uma parte confiável (validação off-line) ou a apresentação do token àquela parte confiável para que ela possa realizar a validação por você (validação on-line).

A validação online, geralmente implementada por meio da [Inspeção de Token OAuth][(https://datatracker.ietf.org/doc/html/rfc7662)], requer menos etapas de um módulo de validação e permite a revogação centralizada de um token no caso de ele ser roubado ou emitido incorretamente. No entanto, isso exige que o módulo faça pelo menos uma chamada de rede por tentativa de autenticação (todas as quais devem ser concluídas dentro do [timeout_de_autenticação][(runtime-config-connection.md#GUC-AUTHENTICATION-TIMEOUT)] configurado). Além disso, seu provedor pode não fornecer pontos de inspeção para uso por servidores de recursos externos.

A validação offline é muito mais complexa, exigindo, normalmente, que um validador mantenha uma lista de chaves de assinatura confiáveis para um provedor e, em seguida, verifique a assinatura criptográfica do token, juntamente com seu conteúdo. As implementações devem seguir as instruções do provedor à risca, incluindo qualquer verificação do emissor ("de onde vem esse token?"), do público-alvo ("para quem é esse token?"), e do período de validade ("quando esse token pode ser usado?"). Como não há comunicação entre o módulo e o provedor, os tokens não podem ser revogados centralmente usando esse método; as implementações de validadores offline podem desejar estabelecer restrições sobre o comprimento máximo do período de validade de um token.

Se o token não puder ser validado, o módulo deve falhar imediatamente. A autenticação/autorização adicional não faz sentido se o token não foi emitido por uma parte confiável.

Autorize o cliente: Em seguida, o validador deve garantir que o usuário final tenha dado permissão ao cliente para acessar o servidor em seu nome. Isso geralmente envolve verificar os escopos que foram atribuídos ao token, para garantir que cubram o acesso ao banco de dados para os parâmetros atuais do HBA.

O objetivo deste passo é impedir que um cliente OAuth obtenha um token sob pretensões falsas. Se o validador exigir que todos os tokens tenham escopos que cubram o acesso ao banco de dados, o provedor deve então solicitar ao usuário que conceda esse acesso durante o fluxo. Isso lhe dá a oportunidade de rejeitar o pedido se o cliente não deve estar usando suas credenciais para se conectar aos bancos de dados.

Embora seja possível estabelecer autorização do cliente sem escopos explícitos, utilizando conhecimento fora da faixa da arquitetura implementada, isso remove o usuário do processo, o que impede que ele detecte erros de implantação e permite que tais erros sejam explorados silenciosamente. O acesso ao banco de dados deve ser estritamente restrito apenas a clientes confiáveis [[17]](#ftn.id-1.8.17.6.3.3.2.2.3.1) se os usuários não forem solicitados a fornecer escopos adicionais.

Mesmo que a autorização falhe, um módulo pode optar por continuar a extrair informações de autenticação do token para uso em auditoria e depuração.

Autentique o Usuário Final: Finalmente, o validador deve determinar um identificador de usuário para o token, solicitando essa informação ao provedor ou extraindo-a do próprio token, e retornar esse identificador para o servidor (que, em seguida, fará uma decisão final de autorização usando a configuração do HBA). Esse identificador estará disponível na sessão via `system_user`(functions-info.md#FUNCTIONS-INFO-SESSION-TABLE "Table 9.71. Session Information Functions") e registrado nos logs do servidor se [log_connections](runtime-config-logging.md#GUC-LOG-CONNECTIONS) estiver habilitado.

Diferentes provedores podem registrar uma variedade de informações de autenticação diferentes para um usuário final, geralmente referidas como *reivindicações*. Os provedores geralmente documentam quais dessas reivindicações são confiáveis o suficiente para serem usadas em decisões de autorização e quais não são. (Por exemplo, provavelmente não seria sábio usar o nome completo de um usuário final como o identificador de autenticação, uma vez que muitos provedores permitem que os usuários mudem seus nomes de exibição arbitrariamente.) Em última análise, a escolha de qual reivindicação (ou combinação de reivindicações) usar depende das necessidades de implementação e aplicação do provedor.

Observe que o login anônimo/pseudônimo também é possível, habilitando a delegação do usermap; veja [Seção 50.1.3][(oauth-validator-design.md#OAUTH-VALIDATOR-DESIGN-USERMAP-DELEGATION "50.1.3. Authorizing Users (Usermap Delegation)]).

### 50.1.2. Diretrizes Gerais de Codificação [#](#OAUTH-VALIDATOR-DESIGN-GUIDELINES)

Os desenvolvedores devem ter em mente o seguinte ao implementar a validação de tokens:

Confidencialidade dos Tokens: Os módulos não devem escrever tokens ou partes de tokens no log do servidor. Isso é verdade mesmo que o módulo considere o token como inválido; um atacante que confunde um cliente para se comunicar com o fornecedor errado não deve ser capaz de recuperar esse (de outra forma) token válido do disco.

As implementações que enviam tokens pela rede (por exemplo, para realizar validação de tokens online com um provedor) devem autenticar o parceiro e garantir que a segurança de transporte forte esteja sendo usada.

Registros: Os módulos podem usar as mesmas facilidades de registro (error-message-reporting.md "55.2. Reporting Errors Within the Server") que as extensões padrão; no entanto, as regras para emitir entradas de registro ao cliente são sutilmente diferentes durante a fase de autenticação da conexão. De forma geral, os módulos devem registrar problemas de verificação no nível `COMMERROR` e retornar normalmente, em vez de usar `ERROR`/`FATAL` para desfazer a pilha, para evitar vazamento de informações para clientes não autenticados.

Interruptibilidade: Os módulos devem permanecer interrompíveis por sinais para que o servidor possa lidar corretamente com os tempos de autenticação e os sinais de desligamento do pg_ctl. Por exemplo, as chamadas bloqueadas em soquetes geralmente devem ser substituídas por código que lide tanto com eventos de soquete quanto com interrupções sem corridas (ver `WaitLatchOrSocket()`, `WaitEventSetWait()`, entre outros), e os loops de longa duração devem chamar periodicamente `CHECK_FOR_INTERRUPTS()`. A não conformidade com essa orientação pode resultar em sessões de backend que não respondem.

Testes: A amplitude dos testes de um sistema OAuth vai muito além do escopo desta documentação, mas, no mínimo, os testes negativos devem ser considerados obrigatórios. É trivial projetar um módulo que permita a entrada de usuários autorizados; o objetivo principal do sistema é manter usuários não autorizados de fora.

Documentação: As implementações do Validador devem documentar o conteúdo e o formato do ID autenticado que é reportado ao servidor para cada usuário final, uma vez que os DBA podem precisar usar essas informações para construir mapas de pg_ident. (Por exemplo, é um endereço de e-mail? um número de identificação organizacional? um UUID?) Eles também devem documentar se é seguro ou não usar o módulo no modo `delegate_ident_mapping=1`, e quais configurações adicionais são necessárias para isso.

### 50.1.3. Autorizando usuários (Delegação do Usermap) [#](#OAUTH-VALIDATOR-DESIGN-USERMAP-DELEGATION)

O resultado padrão de um módulo de validação é o identificador do usuário, que o servidor então comparará com quaisquer mapeamentos `pg_ident.conf` configurados (auth-username-maps.md "20.2. User Name Maps") e determinará se o usuário final está autorizado a se conectar. No entanto, o OAuth é em si uma estrutura de autorização, e os tokens podem conter informações sobre privilégios do usuário. Por exemplo, um token pode ser associado aos grupos organizacionais a que um usuário pertence, ou listar os papéis que um usuário pode assumir, e duplicar esse conhecimento em mapas de usuário locais para cada servidor pode não ser desejável.

Para contornar completamente a mapeo de nomes de usuário e fazer com que o módulo de validação assuma a responsabilidade adicional de autorizar as conexões dos usuários, o HBA pode ser configurado com [delegate_ident_mapping][(auth-oauth.md#AUTH-OAUTH-DELEGATE-IDENT-MAPPING)]. O módulo pode, então, usar escopos de token ou um método equivalente para decidir se o usuário é autorizado a se conectar sob seu papel desejado. O identificador do usuário ainda será registrado pelo servidor, mas não desempenha nenhum papel na determinação de se a conexão deve ser continuada.

Usando esse esquema, a autenticação em si é opcional. Desde que o módulo informe que a conexão está autorizada, o login continuará mesmo que não haja nenhum identificador de usuário registrado. Isso permite a implementação de acesso anônimo ou pseudônimo ao banco de dados, onde o provedor externo realiza toda a autenticação necessária, mas não fornece nenhuma informação identificadora do usuário ao servidor. (Alguns provedores podem criar um número de identificação anonimizado que pode ser registrado, em vez disso, para auditoria posterior.)

A delegação do Usermap oferece a maior flexibilidade arquitetural, mas transforma o módulo de validação em um único ponto de falha para a autorização de conexão. Use com cautela.

---

Ou seja, "confiável" no sentido de que o cliente OAuth e o servidor PostgreSQL são controlados pela mesma entidade. Notavelmente, o fluxo de autorização de dispositivo suportado pelo libpq geralmente não atende a essa exigência, uma vez que é projetado para uso por clientes públicos/não confiáveis.