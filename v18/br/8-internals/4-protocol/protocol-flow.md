## 54.2. Fluxo de Mensagens [#](#PROTOCOL-FLOW)

* [54.2.1. Início de sessão](protocol-flow.md#PROTOCOL-FLOW-START-UP)
* [54.2.2. Consulta simples](protocol-flow.md#PROTOCOL-FLOW-SIMPLE-QUERY)
* [54.2.3. Consulta estendida](protocol-flow.md#PROTOCOL-FLOW-EXT-QUERY)
* [54.2.4. Pipelining](protocol-flow.md#PROTOCOL-FLOW-PIPELINING)
* [54.2.5. Chamada de função](protocol-flow.md#PROTOCOL-FLOW-FUNCTION-CALL)
* [54.2.6. Operações de cópia](protocol-flow.md#PROTOCOL-COPY)
* [54.2.7. Operações assíncronas](protocol-flow.md#PROTOCOL-ASYNC)
* [54.2.8. Cancelamento de solicitações em andamento](protocol-flow.md#PROTOCOL-FLOW-CANCELING-REQUESTS)
* [54.2.9. Termina��o](protocol-flow.md#PROTOCOL-FLOW-TERMINATION)
* [54.2.10. Criptografia de sessão SSL](protocol-flow.md#PROTOCOL-FLOW-SSL)
* [54.2.11. Criptografia de sessão GSSAPI](protocol-flow.md#PROTOCOL-FLOW-GSSAPI)

Esta seção descreve o fluxo de mensagens e a semântica de cada tipo de mensagem. (Os detalhes da representação exata de cada mensagem aparecem em [Seção 54.7] (protocol-message-formats.md "54.7. Message Formats").) Existem vários sub-protocolos diferentes, dependendo do estado da conexão: inicialização, consulta, chamada de função, `COPY` e término. Há também disposições especiais para operações assíncronas (incluindo respostas de notificação e cancelamento de comandos), que podem ocorrer a qualquer momento após a fase de inicialização.

### 54.2.1. Início de negócio [#](#PROTOCOL-FLOW-START-UP)

Para iniciar uma sessão, um frontend abre uma conexão com o servidor e envia uma mensagem de inicialização. Essa mensagem inclui os nomes do usuário e do banco de dados ao qual o usuário deseja se conectar; ela também identifica a versão específica do protocolo a ser usada. (Opcionalmente, a mensagem de inicialização pode incluir configurações adicionais para parâmetros de execução.) O servidor, em seguida, usa essas informações e o conteúdo de seus arquivos de configuração (como `pg_hba.conf`) para determinar se a conexão é provisoriamente aceitável e qual autenticação adicional é necessária (se houver).

O servidor, em seguida, envia uma mensagem apropriada de solicitação de autenticação, à qual o frontend deve responder com uma mensagem apropriada de resposta de autenticação (como uma senha). Para todos os métodos de autenticação, exceto GSSAPI, SSPI e SASL, há no máximo uma solicitação e uma resposta. Em alguns métodos, não é necessária nenhuma resposta do frontend, e, portanto, não ocorre nenhuma solicitação de autenticação. Para GSSAPI, SSPI e SASL, podem ser necessárias várias trocas de pacotes para completar a autenticação.

O ciclo de autenticação termina com o servidor rejeitando a tentativa de conexão (ErrorResponse) ou enviando AuthenticationOk.

As possíveis mensagens do servidor nesta fase são:

Erro de resposta: A tentativa de conexão foi rejeitada. O servidor, então, fecha imediatamente a conexão.

AutenticaçãoOk: A troca de autenticação foi concluída com sucesso.

AutenticaçãoKerberosV5: O frontend agora deve participar de um diálogo de autenticação Kerberos V5 (não descrito aqui, parte da especificação Kerberos) com o servidor. Se isso for bem-sucedido, o servidor responde com um AuthenticationOk, caso contrário, responde com uma ErrorResponse. Isso não é mais suportado.

AutenticaçãoCleartextPassword: O frontend deve agora enviar um PasswordMessage contendo a senha em forma de texto claro. Se essa for a senha correta, o servidor responde com um AuthenticationOk, caso contrário, responde com uma ErrorResponse.

AuthenticationMD5Password: O frontend deve agora enviar um PasswordMessage contendo a senha (com nome de usuário) criptografada via MD5, e depois criptografada novamente usando o sal aleatório de 4 bytes especificado na mensagem AuthenticationMD5Password. Se essa for a senha correta, o servidor responde com um AuthenticationOk, caso contrário, responde com uma ErrorResponse. O PasswordMessage real pode ser calculado em SQL como `concat('md5', md5(concat(md5(concat(password, username)), random-salt)))`. (Tenha em mente que a função `md5()` retorna seu resultado como uma string hexadecimal.)

### Aviso

O suporte para senhas criptografadas com MD5 é desatualizado e será removido em uma versão futura do PostgreSQL. Consulte [Seção 20.5](auth-password.md) para obter detalhes sobre a migração para outro tipo de senha.

Autenticação GSS: O frontend deve agora iniciar uma negociação GSSAPI. O frontend enviará uma mensagem GSSResponse com a primeira parte do fluxo de dados GSSAPI em resposta a isso. Se forem necessárias mais mensagens, o servidor responderá com AuthenticationGSSContinue.

Autenticação SSPI: O frontend deve agora iniciar uma negociação SSPI. O frontend enviará uma GSSResponse com a primeira parte do fluxo de dados SSPI em resposta a isso. Se forem necessárias mais mensagens, o servidor responderá com AuthenticationGSSContinue.

AutenticaçãoGSSContinue: Esta mensagem contém os dados de resposta do passo anterior da negociação GSSAPI ou SSPI (AutenticaçãoGSS, AutenticaçãoSSPI ou uma AutenticaçãoGSSContinue anterior). Se os dados GSSAPI ou SSPI nesta mensagem indicarem que são necessários mais dados para completar a autenticação, o frontend deve enviar esses dados como outra mensagem GSSResponse. Se a autenticação GSSAPI ou SSPI for concluída por esta mensagem, o servidor enviará em seguida AutenticaçãoOk para indicar autenticação bem-sucedida ou ErrorResponse para indicar falha.

AutenticaçãoSASL: O frontend deve agora iniciar uma negociação SASL, usando um dos mecanismos SASL listados na mensagem. O frontend enviará um SASLInitialResponse com o nome do mecanismo selecionado, e a primeira parte do fluxo de dados SASL em resposta a isso. Se forem necessárias mais mensagens, o servidor responderá com AuthenticationSASLContinue. Consulte [Seção 54.3](sasl-authentication.md) para obter detalhes.

AutenticaçãoSASLContinuar: Esta mensagem contém dados de desafio do passo anterior da negociação SASL (AutenticaçãoSASL, ou uma AutenticaçãoSASLContinuar anterior). O frontend deve responder com uma mensagem SASLResponse.

AutenticaçãoSASLFinal: A autenticação SASL foi concluída com dados específicos do mecanismo para o cliente. O servidor enviará em seguida AuthenticationOk para indicar a autenticação bem-sucedida, ou uma ErrorResponse para indicar falha. Esta mensagem é enviada apenas se o mecanismo SASL especificar dados adicionais a serem enviados do servidor para o cliente na conclusão.

NegotiarProtocolVersion: O servidor não suporta a versão menor do protocolo solicitada pelo cliente, mas suporta uma versão anterior do protocolo; esta mensagem indica a versão menor mais alta suportada. Esta mensagem também será enviada se o cliente solicitar opções de protocolo não suportadas (ou seja, começando com `_pq_.`) no pacote de inicialização.

Após esta mensagem, a autenticação continuará usando a versão indicada pelo servidor. Se o cliente não suportar a versão mais antiga, ele deve fechar imediatamente a conexão. Se o servidor não enviar esta mensagem, ele suporta a versão do protocolo solicitada pelo cliente e todas as opções de protocolo.

Se o frontend não suportar o método de autenticação solicitado pelo servidor, ele deve fechar imediatamente a conexão.

Após receber a AuthenticationOk, o frontend deve esperar por mais mensagens do servidor. Nesta fase, um processo de backend está sendo iniciado, e o frontend é apenas um espectador interessado. Ainda é possível que a tentativa de inicialização falhe (ErrorResponse) ou que o servidor recusando o suporte para a versão de protocolo menor solicitada (NegotiateProtocolVersion), mas no caso normal, o backend enviará algumas mensagens de ParameterStatus, BackendKeyData e, finalmente, ReadyForQuery.

Durante essa fase, o backend tentará aplicar quaisquer configurações adicionais de parâmetros de execução que foram fornecidas na mensagem de inicialização. Se bem-sucedida, esses valores se tornam padrões de sessão. Um erro causa ErrorResponse e saída.

As possíveis mensagens do backend nesta fase são:

BackendKeyData: Esta mensagem fornece dados de chave secreta que o frontend deve salvar, se quiser ser capaz de emitir solicitações de cancelamento mais tarde. O frontend não deve responder a esta mensagem, mas deve continuar ouvindo uma mensagem ReadyForQuery.

O servidor PostgreSQL sempre enviará essa mensagem, mas algumas implementações de terceiros do backend do protocolo que não suportam a cancelamento de consulta não são conhecidas por isso.

ParameterStatus: Esta mensagem informa ao frontend sobre a configuração atual (inicial) dos parâmetros do backend, como [client_encoding](runtime-config-client.md#GUC-CLIENT-ENCODING) ou [DateStyle](runtime-config-client.md#GUC-DATESTYLE). O frontend pode ignorar esta mensagem ou registrar as configurações para seu uso futuro; consulte [Seção 54.2.7](protocol-flow.md#PROTOCOL-ASYNC) para mais detalhes. O frontend não deve responder a esta mensagem, mas deve continuar ouvindo uma mensagem ReadyForQuery.

ReadyForQuery: O arranque foi concluído. O frontend pode agora emitir comandos.

Erro de resposta: A inicialização falhou. A conexão foi fechada após a mensagem ser enviada.

Aviso de resposta: Uma mensagem de alerta foi emitida. O frontend deve exibir a mensagem, mas continuar ouvindo para ReadyForQuery ou ErrorResponse.

A mensagem ReadyForQuery é a mesma que o backend emitirá após cada ciclo de comando. Dependendo das necessidades de codificação do frontend, é razoável considerar ReadyForQuery como o início de um ciclo de comando, ou considerar ReadyForQuery como o término da fase de inicialização e cada ciclo de comando subsequente.

### 54.2.2. Consulta simples [#](#PROTOCOL-FLOW-SIMPLE-QUERY)

Um ciclo de consulta simples é iniciado quando o frontend envia uma mensagem de Consulta ao backend. A mensagem inclui um comando SQL (ou comandos) expressos como uma string de texto. O backend, em seguida, envia uma ou mais mensagens de resposta, dependendo do conteúdo da string de comando de consulta, e, finalmente, uma mensagem de resposta ReadyForQuery. ReadyForQuery informa ao frontend que ele pode enviar com segurança um novo comando. (Na verdade, não é necessário que o frontend espere ReadyForQuery antes de emitir outro comando, mas, em seguida, o frontend deve assumir a responsabilidade de descobrir o que acontece se o comando anterior falhar e os comandos já emitidos posteriormente forem bem-sucedidos.)

As possíveis mensagens de resposta do backend são:

CommandComplete: Um comando SQL foi completado normalmente.

CopyInResponse: O backend está pronto para copiar dados do frontend para uma tabela; veja [Seção 54.2.6](protocol-flow.md#PROTOCOL-COPY).

CopyOutResponse: O backend está pronto para copiar dados de uma tabela para o frontend; veja [Seção 54.2.6](protocol-flow.md#PROTOCOL-COPY).

Descrição da linha: Indica que as linhas estão prestes a ser devolvidas em resposta a uma consulta `SELECT`, `FETCH`, etc. O conteúdo desta mensagem descreve o layout da coluna das linhas. Isso será seguido por uma mensagem DataRow para cada linha que será devolvida ao frontend.

DataRow: Um dos conjuntos de linhas retornadas por uma consulta `SELECT`, `FETCH`, etc.

EmptyQueryResponse: Uma string de consulta vazia foi reconhecida.

Erro de resposta: Um erro ocorreu.

ReadyForQuery: O processamento da string de consulta está completo. Uma mensagem separada é enviada para indicar isso, porque a string de consulta pode conter vários comandos SQL. (CommandComplete marca o fim do processamento de um comando SQL, não a string inteira.) ReadyForQuery será sempre enviado, seja o processamento concluído com sucesso ou com um erro.

Aviso de resposta: Uma mensagem de alerta foi emitida em relação à consulta. Os avisos são adicionais a outras respostas, ou seja, o backend continuará processando o comando.

A resposta a uma consulta `SELECT` (ou outras consultas que retornam conjuntos de linhas, como `EXPLAIN` ou `SHOW`) normalmente consiste em RowDescription, zero ou mais mensagens DataRow e, em seguida, CommandComplete. A consulta `COPY` para ou a partir do frontend invoca um protocolo especial conforme descrito em [Seção 54.2.6](protocol-flow.md#PROTOCOL-COPY). Todos os outros tipos de consulta normalmente produzem apenas uma mensagem CommandComplete.

Como uma string de consulta pode conter várias consultas (separadas por pontos e virgulas), pode haver várias sequências de resposta antes que o backend termine de processar a string de consulta. ReadyForQuery é emitido quando toda a string foi processada e o backend está pronto para aceitar uma nova string de consulta.

Se uma string de consulta completamente vazia (sem outros conteúdos além de espaços em branco) for recebida, a resposta é EmptyQueryResponse seguida de ReadyForQuery.

Em caso de erro, é emitida a Response de erro seguida pela ReadyForQuery. Todo o processamento subsequente da string de consulta é abortado pela Response de erro (mesmo que mais consultas permanecessem nela). Observe que isso pode ocorrer em meio à sequência de mensagens geradas por uma consulta individual.

No modo de consulta simples, o formato dos valores recuperados é sempre texto, exceto quando o comando fornecido é um `FETCH` de um cursor declarado com a opção `BINARY`. Nesse caso, os valores recuperados estão no formato binário. Os códigos de formato fornecidos na mensagem RowDescription indicam qual formato está sendo usado.

Um frontend deve estar preparado para aceitar mensagens ErrorResponse e NoticeResponse sempre que espera qualquer outro tipo de mensagem. Veja também [Seção 54.2.7](protocol-flow.md#PROTOCOL-ASYNC) sobre mensagens que o backend pode gerar devido a eventos externos.

A prática recomendada é codificar os frontends em estilo de máquina de estado que aceitará qualquer tipo de mensagem em qualquer momento em que isso faça sentido, em vez de fazer suposições sobre a sequência exata das mensagens.

#### 54.2.2.1. Múltiplas declarações em uma consulta simples [#](#PROTOCOL-FLOW-MULTI-STATEMENT)

Quando uma mensagem de consulta simples contém mais de uma declaração SQL (separadas por pontos e vírgulas), essas declarações são executadas como uma única transação, a menos que comandos explícitos de controle de transação sejam incluídos para forçar um comportamento diferente. Por exemplo, se a mensagem contiver

```
INSERT INTO mytable VALUES(1);
SELECT 1/0;
INSERT INTO mytable VALUES(2);
```

então, o erro de divisão por zero no `SELECT` fará com que o primeiro `INSERT` seja desfeito. Além disso, como a execução da mensagem é abandonada no primeiro erro, o segundo `INSERT` nunca é tentado.

Se, em vez disso, a mensagem contiver

```
BEGIN;
INSERT INTO mytable VALUES(1);
COMMIT;
INSERT INTO mytable VALUES(2);
SELECT 1/0;
```

então o primeiro `INSERT` é comprometido pelo comando explícito `COMMIT`. O segundo `INSERT` e o `SELECT` ainda são tratados como uma única transação, de modo que a falha por divisão por zero reverte o segundo `INSERT`, mas não o primeiro.

Esse comportamento é implementado ao executar as declarações em uma mensagem de consulta de várias declarações em um *bloco de transação implícito*, a menos que haja algum bloco de transação explícito para que elas sejam executadas. A principal diferença entre um bloco de transação implícito e um bloco regular é que um bloco implícito é fechado automaticamente no final da mensagem de consulta, seja por um compromisso implícito se não houver erro, ou um recuo implícito se houver um erro. Isso é semelhante ao compromisso ou recuo implícito que acontece para uma declaração executada por si só (quando não em um bloco de transação).

Se a sessão já estiver em um bloco de transação, como resultado de um `BEGIN` em alguma mensagem anterior, então a mensagem de Consulta simplesmente continua esse bloco de transação, independentemente de a mensagem conter uma declaração ou várias. No entanto, se a mensagem de Consulta contiver um `COMMIT` ou `ROLLBACK` que feche o bloco de transação existente, então quaisquer declarações subsequentes serão executadas em um bloco de transação implícito. Por outro lado, se um `BEGIN` aparecer em uma mensagem de Consulta com várias declarações, então ele inicia um bloco de transação regular que só será terminado por um `COMMIT` ou `ROLLBACK` explícito, independentemente de isso aparecer nesta mensagem de Consulta ou em uma posterior. Se o `BEGIN` seguir algumas declarações que foram executadas como um bloco de transação implícito, essas declarações não serão imediatamente comprometidas; na verdade, elas são retroativamente incluídas no novo bloco de transação regular.

Um `COMMIT` ou `ROLLBACK` que aparece em um bloco de transação implícita é executado normalmente, fechando o bloco implícito; no entanto, um aviso será emitido, pois um `COMMIT` ou `ROLLBACK` sem um `BEGIN` anterior pode representar um erro. Se houver mais declarações, um novo bloco de transação implícita será iniciado para elas.

Os pontos de salvamento não são permitidos em um bloco de transação implícito, pois eles entrariam em conflito com o comportamento de fechar automaticamente o bloco em caso de qualquer erro.

Lembre-se de que, independentemente de quaisquer comandos de controle de transação que possam estar presentes, a execução da mensagem Query para de no primeiro erro. Assim, por exemplo, dado

```
BEGIN;
SELECT 1/0;
ROLLBACK;
```

Em uma única mensagem de consulta, a sessão será deixada dentro de um bloco de transação regular falha, uma vez que o `ROLLBACK` não é alcançado após o erro de divisão por zero. Outro `ROLLBACK` será necessário para restaurar a sessão a um estado utilizável.

Outro comportamento a ser observado é que a análise lexical e sintática inicial é feita em toda a cadeia de consulta antes de qualquer uma delas ser executada. Assim, erros simples (como uma palavra-chave mal escrita) em declarações posteriores podem impedir a execução de qualquer uma das declarações. Isso normalmente é invisível para os usuários, uma vez que as declarações seriam todas revertidas de qualquer maneira quando realizadas como um bloco de transação implícita. No entanto, pode ser visível ao tentar realizar várias transações dentro de uma consulta com múltiplas declarações. Por exemplo, se um erro de digitação transformou nosso exemplo anterior em

```
BEGIN;
INSERT INTO mytable VALUES(1);
COMMIT;
INSERT INTO mytable VALUES(2);
SELCT 1/0;
```

assim, nenhuma das declarações seria executada, resultando na diferença visível de que o primeiro `INSERT` não é comprometido. Erros detectados na análise semântica ou posteriormente, como um nome de tabela ou coluna incorreto, não têm esse efeito.

Por último, observe que todas as declarações na mensagem de Consulta observarão o mesmo valor de `statement_timestamp()`, uma vez que esse timestamp é atualizado apenas após a recepção da mensagem de Consulta. Isso resultará em todas elas observando o mesmo valor de `transaction_timestamp()` também, exceto nos casos em que a string de consulta termina uma transação previamente iniciada e começa uma nova.

### 54.2.3. Consulta estendida [#](#PROTOCOL-FLOW-EXT-QUERY)

O protocolo de consulta estendido desmembra o protocolo de consulta simples descrito acima em múltiplos passos. Os resultados das etapas preparatórias podem ser reutilizados várias vezes para melhorar a eficiência. Além disso, recursos adicionais estão disponíveis, como a possibilidade de fornecer valores de dados como parâmetros separados, em vez de os inserir diretamente em uma cadeia de consulta.

No protocolo estendido, o frontend envia primeiro uma mensagem Parse, que contém uma string de consulta textual, opcionalmente algumas informações sobre os tipos de dados dos placeholders de parâmetros e o nome de um objeto de declaração preparada de destino (uma string vazia seleciona a declaração preparada sem nome). A resposta é ParseComplete ou ErrorResponse. Os tipos de dados dos parâmetros podem ser especificados por OID; se não forem fornecidos, o analisador tenta inferir os tipos de dados da mesma maneira que faria para constantes de string literal não tipadas.

Nota

Um tipo de dado de parâmetro pode ser deixado não especificado ao ser definido como zero ou ao fazer o array de tipos de OID do tipo de parâmetro ser menor que o número de símbolos de parâmetro (`$`*`n`*) usados na string de consulta. Outro caso especial é que o tipo de um parâmetro pode ser especificado como `void` (ou seja, o OID do pseudo-tipo `void`). Isso é para permitir que os símbolos de parâmetro sejam usados para parâmetros de função que são realmente parâmetros OUT. Normalmente, não há contexto em que um parâmetro `void` poderia ser usado, mas se tal símbolo de parâmetro aparecer na lista de parâmetros de uma função, ele é efetivamente ignorado. Por exemplo, uma chamada de função como `foo($1,$2,$3,$4)` poderia corresponder a uma função com dois argumentos IN e dois OUT, se `$3` e `$4` forem especificados como tendo tipo `void`.

Nota

A string de consulta contida em uma mensagem Parse não pode incluir mais de uma declaração SQL; caso contrário, um erro de sintaxe é relatado. Essa restrição não existe no protocolo de consulta simples, mas existe no protocolo estendido, porque permitir que declarações preparadas ou portais contenham vários comandos complicaria indevidamente o protocolo.

Se criado com sucesso, um objeto de declaração preparada nomeada dura até o final da sessão atual, a menos que seja explicitamente destruído. Uma declaração preparada sem nome dura apenas até que a próxima declaração Parse que especifica a declaração sem nome como destino seja emitida. (Observe que uma mensagem de consulta simples também destrói a declaração sem nome.) As declarações preparadas nomeadas também podem ser explicitamente fechadas antes de serem redefinidas por outra mensagem Parse, mas isso não é necessário para a declaração sem nome. As declarações preparadas nomeadas também podem ser criadas e acessadas no nível do comando SQL, usando `PREPARE` e `EXECUTE`.

Uma vez que uma declaração preparada exista, ela pode ser preparada para execução usando uma mensagem de Bind. A mensagem Bind fornece o nome da declaração preparada de origem (string vazia denota a declaração preparada sem nome), o nome do portal de destino (string vazia denota o portal sem nome) e os valores a serem usados para quaisquer marcadores de parâmetro presentes na declaração preparada. O conjunto de parâmetros fornecido deve corresponder àqueles necessários pela declaração preparada. (Se você declarou quaisquer parâmetros `void` na mensagem Parse, passe valores NULL para eles na mensagem Bind.) Bind também especifica o formato a ser usado para quaisquer dados retornados pela consulta; o formato pode ser especificado de forma geral ou por coluna. A resposta é BindComplete ou ErrorResponse.

Nota

A escolha entre saída de texto e binária é determinada pelos códigos de formato fornecidos em Bind, independentemente do comando SQL envolvido. O atributo `BINARY` nas declarações de cursor é irrelevante ao usar o protocolo de consulta estendida.

O planejamento da consulta geralmente ocorre quando a mensagem de vinculação é processada. Se a declaração preparada não tiver parâmetros ou for executada repetidamente, o servidor pode salvar o plano criado e reutilizá-lo durante as mensagens de vinculação subsequentes para a mesma declaração preparada. No entanto, ele fará isso apenas se encontrar que pode ser criado um plano genérico que não seja muito menos eficiente do que um plano que depende dos valores específicos dos parâmetros fornecidos. Isso acontece de forma transparente, no que diz respeito ao protocolo.

Se criado com sucesso, um objeto de portal com nome dura até o final da transação atual, a menos que seja explicitamente destruído. Um portal sem nome é destruído no final da transação ou assim que a próxima declaração Bind que especifica o portal sem nome como destino for emitida. (Observe que uma mensagem simples de Consulta também destrói o portal sem nome.) Portals com nome devem ser explicitamente fechados antes que possam ser redefinidos por outra mensagem Bind, mas isso não é necessário para o portal sem nome. Portals com nome também podem ser criados e acessados no nível do comando SQL, usando `DECLARE CURSOR` e `FETCH`.

Uma vez que um portal exista, ele pode ser executado usando uma mensagem Execute. A mensagem Execute especifica o nome do portal (string vazia denota o portal sem nome) e um número máximo de linhas de resultado (zero significa “pegar todas as linhas”). O número de linhas de resultado é significativo apenas para portais que contêm comandos que retornam conjuntos de linhas; em outros casos, o comando é sempre executado até o final, e o número de linhas é ignorado. As possíveis respostas para Execute são as mesmas que as descritas acima para consultas emitidas via protocolo de consulta simples, exceto que Execute não causa que ReadyForQuery ou RowDescription sejam emitidos.

Se o Execute terminar antes de completar a execução de um portal (por atingir um número de linhas de resultado não nulo), ele enviará uma mensagem PortalSuspended; a aparência dessa mensagem informa ao frontend que outro Execute deve ser emitido contra o mesmo portal para completar a operação. A mensagem CommandComplete, indicando a conclusão do comando SQL da fonte, não é enviada até que a execução do portal seja concluída. Portanto, uma fase de Execute é sempre terminada pela aparência de exatamente uma dessas mensagens: CommandComplete, EmptyQueryResponse (se o portal foi criado a partir de uma string de consulta vazia), ErrorResponse ou PortalSuspended.

Após a conclusão de cada série de mensagens de consulta estendida, o frontend deve emitir uma mensagem de sincronização. Esta mensagem sem parâmetros faz com que o backend feche a transação atual se não estiver dentro de um bloco de transação `BEGIN`/`COMMIT` (“fechar” significa cometer se não houver erro, ou reverter se houver erro). Em seguida, é emitida uma resposta ReadyForQuery. O propósito do Sync é fornecer um ponto de resincronização para recuperação de erros. Quando um erro é detectado durante o processamento de qualquer mensagem de consulta estendida, o backend emite ErrorResponse, depois lê e descarta mensagens até que um Sync seja alcançado, em seguida, emite ReadyForQuery e retorna ao processamento de mensagens normal. (Mas note que não ocorre nenhum desvio se um erro for detectado *durante* o processamento do Sync — isso garante que haja um e apenas um ReadyForQuery enviado para cada Sync.)

Nota

O Sync não faz com que um bloco de transação aberto com `BEGIN` seja fechado. É possível detectar essa situação, pois a mensagem ReadyForQuery inclui informações sobre o status da transação.

Além dessas operações fundamentais e obrigatórias, existem várias operações opcionais que podem ser usadas com o protocolo de consulta estendida.

A mensagem Descrever (variante do portal) especifica o nome de um portal existente (ou uma string vazia para o portal sem nome). A resposta é uma mensagem RowDescription que descreve as linhas que serão devolvidas ao executar o portal; ou uma mensagem NoData se o portal não contiver uma consulta que devolva linhas; ou ErrorResponse se não houver tal portal.

A mensagem Descriver mensagem (variante de declaração) especifica o nome de uma declaração preparada existente (ou uma string vazia para a declaração preparada sem nome). A resposta é uma mensagem ParameterDescription que descreve os parâmetros necessários pela declaração, seguida por uma mensagem RowDescription que descreve as linhas que serão devolvidas quando a declaração for executada (ou uma mensagem NoData se a declaração não devolver linhas). A ErrorResponse é emitida se não houver tal declaração preparada. Note que, uma vez que Bind ainda não foi emitida, os formatos a serem usados para as colunas devolvidas ainda não são conhecidos pelo backend; os campos de código de formato na mensagem RowDescription serão zeros neste caso.

### DICA

Na maioria dos cenários, o frontend deve emitir uma ou outra variante de Descrever antes de emitir Executar, para garantir que ele saiba como interpretar os resultados que receberá.

A mensagem Fechar fecha uma declaração ou portal preparado existente e libera recursos. Não é um erro emitir Fechar contra um nome de declaração ou portal inexistente. A resposta normalmente é CloseComplete, mas pode ser ErrorResponse se alguma dificuldade for encontrada ao liberar recursos. Observe que fechar uma declaração preparada fecha implicitamente quaisquer portais abertos que foram construídos a partir dessa declaração.

A mensagem Flush não gera nenhuma saída específica, mas obriga o backend a entregar quaisquer dados pendentes em seus buffers de saída. Um Flush deve ser enviado após qualquer comando de consulta estendida, exceto Sync, se o frontend desejar examinar os resultados desse comando antes de emitir mais comandos. Sem Flush, as mensagens devolvidas pelo backend serão combinadas no número mínimo possível de pacotes para minimizar o overhead de rede.

Nota

A mensagem simples Query é aproximadamente equivalente à série Parse, Bind, portal Describe, Execute, Close, Sync, usando a declaração preparada sem nome e objetos do portal e sem parâmetros. Uma diferença é que ela aceitará múltiplas declarações SQL no string de consulta, realizando automaticamente a sequência de bind/describe/execute para cada uma delas em sucessão. Outra diferença é que ela não retornará mensagens ParseComplete, BindComplete, CloseComplete ou NoData.

### 54.2.4. Pipelining [#](#PROTOCOL-FLOW-PIPELINING)

O uso do protocolo de consulta estendida permite o *pipeline*, o que significa enviar uma série de consultas sem esperar que as anteriores sejam concluídas. Isso reduz o número de viagens de rede necessárias para completar uma série específica de operações. No entanto, o usuário deve considerar cuidadosamente o comportamento necessário se uma das etapas falhar, uma vez que as consultas subsequentes já estarão em voo para o servidor.

Uma maneira de lidar com isso é fazer com que toda a série de consultas seja uma única transação, ou seja, envolvê-la em `BEGIN`... `COMMIT`. No entanto, isso não ajuda se alguém deseja que alguns dos comandos sejam confirmados independentemente dos outros.

O protocolo de consulta estendido oferece outra maneira de gerenciar essa preocupação, que é omitir o envio de mensagens de sincronização entre etapas que são dependentes. Como, após um erro, o backend ignorará as mensagens de comando até encontrar a sincronização, isso permite que comandos posteriores em um pipeline sejam ignorados automaticamente quando um deles falha, sem que o cliente precise gerenciá-lo explicitamente com `BEGIN` e `COMMIT`. Segsmentos independentemente comitíveis do pipeline podem ser separados por mensagens de sincronização.

Se o cliente não tiver emitido um `BEGIN` explícito, então um bloco de transação implícito é iniciado e cada Sync normalmente causa um `COMMIT` implícito se o(s) passo(s) anterior(es) tiverem sucesso, ou um `ROLLBACK` implícito se falharem. Este bloco de transação implícito só será detectado pelo servidor quando o primeiro comando terminar sem uma sincronização. Existem alguns comandos DDL (como `CREATE DATABASE`) que não podem ser executados dentro de um bloco de transação. Se um desses for executado em um pipeline, falhará a menos que seja o primeiro comando após um Sync. Além disso, após o sucesso, ele forçará um commit imediato para preservar a consistência do banco de dados. Assim, um Sync imediatamente após um desses comandos não tem efeito, exceto para responder com ReadyForQuery.

Ao usar esse método, a conclusão do pipeline deve ser determinada contando as mensagens ReadyForQuery e esperando que esse número atinja o número de sincronizações enviadas. A contagem de respostas de conclusão de comandos é pouco confiável, pois alguns dos comandos podem ser ignorados e, portanto, não produzir uma mensagem de conclusão.

### 54.2.5. Chamada de função [#](#PROTOCOL-FLOW-FUNCTION-CALL)

O subprotocolo Chamada de Função permite que o cliente solicite uma chamada direta de qualquer função que exista no catálogo do sistema `pg_proc` do banco de dados. O cliente deve ter permissão de execução para a função.

Nota

O subprotocolo Chamada de função é uma característica antiga que provavelmente deve ser evitada em novos códigos. Resultados semelhantes podem ser alcançados configurando uma declaração preparada que faça `SELECT function($1, ...)`. O ciclo Chamada de função pode então ser substituído por Bindir/Executar.

Um ciclo de chamada de função é iniciado quando o frontend envia uma mensagem de chamada de função para o backend. O backend, por sua vez, envia uma ou mais mensagens de resposta, dependendo dos resultados da chamada de função, e, finalmente, uma mensagem de resposta ReadyForQuery. ReadyForQuery informa ao frontend que ele pode enviar com segurança uma nova consulta ou chamada de função.

As possíveis mensagens de resposta do backend são:

Erro de resposta: Um erro ocorreu.

FunctionCallResponse: A chamada de função foi concluída e retornou o resultado dado na mensagem. (Observe que o protocolo de chamada de função só pode lidar com um único resultado escalar, não com um tipo de linha ou conjunto de resultados.)

ReadyForQuery: O processamento da chamada de função está concluído. ReadyForQuery será sempre enviado, seja o processamento concluído com sucesso ou com um erro.

Aviso de resposta: Uma mensagem de alerta foi emitida em relação à chamada de função. Os avisos são adicionais a outras respostas, ou seja, o backend continuará processando o comando.

### 54.2.6. Operações de COPIA [#](#PROTOCOL-COPY)

O comando `COPY` permite a transferência de dados em massa de alta velocidade para ou a partir do servidor. As operações de cópia em e cópia para trocam cada vez a conexão para um subprotocolo distinto, que dura até que a operação seja concluída.

O modo de cópia (transferência de dados para o servidor) é iniciado quando o backend executa uma declaração SQL `COPY FROM STDIN`. O backend envia uma mensagem CopyInResponse para o frontend. O frontend deve, em seguida, enviar zero ou mais mensagens CopyData, formando um fluxo de dados de entrada. (Os limites da mensagem não precisam ter nada a ver com os limites das linhas, embora essa seja uma escolha razoável.) O frontend pode finalizar o modo de cópia enviando uma mensagem CopyDone (permitindo a finalização bem-sucedida) ou uma mensagem CopyFail (que fará com que a declaração SQL `COPY` falhe com um erro). O backend, em seguida, retorna ao modo de processamento de comandos que estava antes do início do `COPY`, que será um protocolo de consulta simples ou estendido. Em seguida, ele enviará ou CommandComplete (se bem-sucedido) ou ErrorResponse (se não).

Em caso de erro detectado no backend durante o modo de cópia (incluindo a recepção de uma mensagem de CopyFail), o backend emitirá uma mensagem ErrorResponse. Se o comando `COPY` foi emitido através de uma mensagem de consulta estendida, o backend descartará agora as mensagens do frontend até que uma mensagem de Sync seja recebida, e então emitirá ReadyForQuery e retornará ao processamento normal. Se o comando `COPY` foi emitido em uma mensagem de consulta simples, o restante dessa mensagem será descartado e ReadyForQuery será emitido. Em qualquer caso, quaisquer mensagens subsequentes de CopyData, CopyDone ou CopyFail emitidas pelo frontend serão simplesmente descartadas.

O backend ignorará as mensagens Flush e Sync recebidas durante o modo de cópia. O recebimento de qualquer outro tipo de mensagem não de cópia constitui um erro que abortará o estado de cópia conforme descrito acima. (A exceção para Flush e Sync é para a conveniência das bibliotecas de cliente que sempre enviam Flush ou Sync após uma mensagem Execute, sem verificar se o comando a ser executado é um `COPY FROM STDIN`.)

O modo de cópia (transferência de dados do servidor) é iniciado quando o backend executa uma declaração SQL `COPY TO STDOUT`. O backend envia uma mensagem CopyOutResponse para o frontend, seguida por zero ou mais mensagens CopyData (sempre uma por linha), seguida por CopyDone. O backend, em seguida, retorna ao modo de processamento de comandos em que estava antes de o `COPY` começar, e envia CommandComplete. O frontend não pode abortar a transferência (exceto fechando a conexão ou emitindo uma solicitação Cancel), mas pode descartar mensagens CopyData e CopyDone indesejadas.

Caso um erro seja detectado no backend durante o modo de cópia, o backend emitirá uma mensagem de ErrorResponse e retornará ao processamento normal. O frontend deve tratar a recepção da ErrorResponse como o término do modo de cópia.

É possível que as mensagens NoticeResponse e ParameterStatus sejam intercaladas entre as mensagens CopyData; os frontends devem lidar com esses casos e também estar preparados para outros tipos de mensagens assíncronas (consulte [Seção 54.2.7](protocol-flow.md#PROTOCOL-ASYNC)). Caso contrário, qualquer tipo de mensagem que não seja CopyData ou CopyDone pode ser tratado como o modo de término do modo de saída de cópia.

Existe outro modo relacionado ao Copy chamado copy-both, que permite a transferência de dados em massa de alta velocidade para *e* do servidor. O modo copy-both é iniciado quando um backend em modo walsender executa uma declaração `START_REPLICATION`. O backend envia uma mensagem CopyBothResponse para o frontend. O backend e o frontend podem, então, enviar mensagens CopyData até que um dos lados envie uma mensagem CopyDone. Após o cliente enviar uma mensagem CopyDone, a conexão passa do modo copy-both para o modo copy-out, e o cliente não pode enviar mais mensagens CopyData. Da mesma forma, quando o servidor envia uma mensagem CopyDone, a conexão passa para o modo copy-in, e o servidor não pode enviar mais mensagens CopyData. Após ambos os lados terem enviado uma mensagem CopyDone, o modo de cópia é terminado e o backend retorna ao modo de processamento de comandos. No caso de um erro detectado pelo backend durante o modo copy-both, o backend emitirá uma mensagem ErrorResponse, descartará as mensagens do frontend até que uma mensagem Sync seja recebida, e então emitirá ReadyForQuery e retornará ao processamento normal. O frontend deve tratar a recepção da ErrorResponse como o término da cópia em ambas as direções; não deve ser enviada nenhuma mensagem CopyDone neste caso. Consulte [Seção 54.4](protocol-replication.md) para mais informações sobre o subprotocolo transmitido no modo copy-both.

As mensagens CopyInResponse, CopyOutResponse e CopyBothResponse incluem campos que informam ao frontend o número de colunas por linha e os códigos de formato que estão sendo usados para cada coluna. (A partir da implementação atual, todas as colunas em uma operação dada `COPY` usarão o mesmo formato, mas o desenho da mensagem não assume isso.)

### 54.2.7. Operações Assíncronas [#](#PROTOCOL-ASYNC)

Há vários casos em que o backend envia mensagens que não são especificamente solicitadas pelo fluxo de comandos do frontend. Os frontends devem estar preparados para lidar com essas mensagens a qualquer momento, mesmo quando não estão envolvidos em uma consulta. No mínimo, é necessário verificar esses casos antes de começar a ler uma resposta de consulta.

É possível que mensagens de NoticeResponse sejam geradas devido a atividades externas; por exemplo, se o administrador do banco de dados ordenar o desligamento rápido do banco de dados, o backend enviará uma NoticeResponse indicando esse fato antes de fechar a conexão. Assim, os frontends devem estar sempre preparados para aceitar e exibir mensagens de NoticeResponse, mesmo quando a conexão é nominalmente inativa.

Mensagens de ParameterStatus serão geradas sempre que o valor ativo mudar para qualquer um dos parâmetros que o backend acredita que o frontend deve saber. Mais comumente, isso ocorre em resposta a um comando SQL `SET` executado pelo frontend, e este caso é efetivamente sincrônico — mas também é possível que as mudanças de status dos parâmetros ocorram porque o administrador alterou um arquivo de configuração e, em seguida, enviou o sinal SIGHUP para o servidor. Além disso, se um comando `SET` for revertido, uma mensagem apropriada de ParameterStatus será gerada para relatar o valor efetivo atual.

Atualmente, há um conjunto de parâmetros pré-definidos para os quais o ParameterStatus será gerado. Eles são:



<table border="0" class="simplelist" summary="Simple list">
 <tr>
  <td>
   <code class="varname">
    application_name
   </code>
  </td>
  <td>
   <code class="varname">
    scram_iterations
   </code>
  </td>
 </tr>
 <tr>
  <td>
   <code class="varname">
    client_encoding
   </code>
  </td>
  <td>
   <code class="varname">
    search_path
   </code>
  </td>
 </tr>
 <tr>
  <td>
   <code class="varname">
    DateStyle
   </code>
  </td>
  <td>
   <code class="varname">
    server_encoding
   </code>
  </td>
 </tr>
 <tr>
  <td>
   <code class="varname">
    default_transaction_read_only
   </code>
  </td>
  <td>
   <code class="varname">
    server_version
   </code>
  </td>
 </tr>
 <tr>
  <td>
   <code class="varname">
    in_hot_standby
   </code>
  </td>
  <td>
   <code class="varname">
    session_authorization
   </code>
  </td>
 </tr>
 <tr>
  <td>
   <code class="varname">
    integer_datetimes
   </code>
  </td>
  <td>
   <code class="varname">
    standard_conforming_strings
   </code>
  </td>
 </tr>
 <tr>
  <td>
   <code class="varname">
    IntervalStyle
   </code>
  </td>
  <td>
   <code class="varname">
    TimeZone
   </code>
  </td>
 </tr>
 <tr>
  <td>
   <code class="varname">
    is_superuser
   </code>
  </td>
  <td>
  </td>
 </tr>
</table>







(`default_transaction_read_only` e `in_hot_standby` não foram relatados em versões anteriores a 14; `scram_iterations` não foi relatado em versões anteriores a 16; `search_path` não foi relatado em versões anteriores a 18.) Observe que `server_version`, `server_encoding` e `integer_datetimes` são pseudo-parâmetros que não podem ser alterados após a inicialização. Este conjunto pode mudar no futuro, ou até mesmo se tornar configurável. Assim, um frontend deve simplesmente ignorar o ParameterStatus para os parâmetros que ele não entende ou não se importa.

Se um frontend emitir o comando `LISTEN`, o backend enviará uma mensagem NotificationResponse (não confundir com NoticeResponse!) sempre que um comando `NOTIFY` for executado para o mesmo nome de canal.

Nota

Atualmente, a NotificationResponse só pode ser enviada fora de uma transação, e, portanto, não ocorrerá no meio de uma série de comandos e respostas, embora possa ocorrer logo antes do ReadyForQuery. Não é prudente projetar lógica de frontend que presuma isso. A boa prática é ser capaz de aceitar NotificationResponse em qualquer ponto do protocolo.

### 54.2.8. Cancelamento de solicitações em andamento [#](#PROTOCOL-FLOW-CANCELING-REQUESTS)

Durante o processamento de uma consulta, o frontend pode solicitar a cancelamento da consulta. O pedido de cancelamento não é enviado diretamente na conexão aberta com o backend por razões de eficiência de implementação: não queremos que o backend verifique constantemente novos inputs do frontend durante o processamento da consulta. Os pedidos de cancelamento devem ser relativamente infrequentes, então os fazemos um pouco complicados para evitar uma penalidade no caso normal.

Para emitir um pedido de cancelamento, o frontend abre uma nova conexão com o servidor e envia uma mensagem CancelRequest, em vez da mensagem StartupMessage que normalmente seria enviada através de uma nova conexão. O servidor processará esse pedido e, em seguida, fechará a conexão. Por razões de segurança, não é feita uma resposta direta à mensagem de pedido de cancelamento.

Uma mensagem CancelRequest será ignorada, a menos que contenha os mesmos dados de chave (PID e chave secreta) passados ao frontend durante o início da conexão. Se a solicitação corresponder ao PID e à chave secreta de um backend atualmente em execução, o processamento da consulta atual é abortado. (Na implementação existente, isso é feito enviando um sinal especial ao processo do backend que está processando a consulta.)

O sinal de cancelamento pode ou não ter qualquer efeito — por exemplo, se ele chegar depois que o backend tiver terminado de processar a consulta, então não terá efeito. Se o cancelamento for eficaz, ele resulta no comando atual sendo terminado precocemente com uma mensagem de erro.

O resultado de tudo isso é que, por razões de segurança e eficiência, o frontend não tem nenhuma maneira direta de saber se um pedido de cancelamento foi bem-sucedido. Ele deve continuar a esperar que o backend responda à consulta. Emitir um cancelamento simplesmente melhora as chances de que a consulta atual termine em breve e melhora as chances de que falhe com uma mensagem de erro em vez de ser bem-sucedida.

Como o pedido de cancelamento é enviado através de uma nova conexão com o servidor e não através do link regular de comunicação frontend/backend, é possível que o pedido de cancelamento seja emitido por qualquer processo, não apenas o frontend cuja consulta deve ser cancelada. Isso pode proporcionar flexibilidade adicional ao construir aplicações com múltiplos processos. Também introduz um risco de segurança, pois pessoas não autorizadas podem tentar cancelar consultas. O risco de segurança é abordado ao exigir que uma chave secreta gerada dinamicamente seja fornecida nos pedidos de cancelamento.

### 54.2.9. Termina��o [#](#PROTOCOL-FLOW-TERMINATION)

O procedimento de término normal e gracioso é que o frontend envie uma mensagem de término e feche imediatamente a conexão. Ao receber essa mensagem, o backend fecha a conexão e termina.

Em casos raros (como o desligamento de um banco de dados comandado por um administrador), o backend pode se desconectar sem qualquer solicitação do frontend para fazer isso. Nesses casos, o backend tentará enviar uma mensagem de erro ou aviso, fornecendo o motivo da desconexão antes de fechar a conexão.

Outros cenários de término surgem de vários casos de falha, como o core dump em uma extremidade ou na outra, perda da conexão de comunicação, perda de sincronização de limites de mensagem, etc. Se o frontend ou o backend perceber um fechamento inesperado da conexão, deve limpar e encerrar. O frontend tem a opção de lançar um novo backend, reconectando-se ao servidor se não quiser encerrar a si mesmo. É aconselhável fechar a conexão também se um tipo de mensagem irreconhecível for recebido, uma vez que isso provavelmente indica perda de sincronização de limites de mensagem.

Para uma terminação normal ou anormal, qualquer transação aberta é revertida, não comprometida. No entanto, é importante notar que, se um frontend se desconectar enquanto uma consulta não `SELECT` está sendo processada, o backend provavelmente terminará a consulta antes de notar a desconexão. Se a consulta estiver fora de qualquer bloco de transação (sequência `BEGIN`...`COMMIT`), seus resultados podem ser comprometidos antes de a desconexão ser reconhecida.

### 54.2.10. Encriptação de sessão SSL [#](#PROTOCOL-FLOW-SSL)

Se o PostgreSQL foi construído com suporte SSL, as comunicações frontend/backend podem ser criptografadas usando SSL. Isso fornece segurança de comunicação em ambientes onde os atacantes podem ser capazes de capturar o tráfego da sessão. Para mais informações sobre criptografar sessões do PostgreSQL com SSL, consulte [Seção 18.9](ssl-tcp.md).

Para iniciar uma conexão criptografada SSL, o frontend envia inicialmente uma mensagem SSLRequest em vez de uma StartupMessage. O servidor, em seguida, responde com um único byte contendo `S` ou `N`, indicando que está disposto ou não a realizar SSL, respectivamente. O frontend pode fechar a conexão neste ponto, se estiver insatisfeito com a resposta. Para continuar após `S`, realize um aperto de mão de inicialização SSL (não descrito aqui, parte da especificação SSL) com o servidor. Se isso for bem-sucedido, continue enviando a StartupMessage usual. Neste caso, a StartupMessage e todos os dados subsequentes serão criptografados SSL. Para continuar após `N`, envie a StartupMessage usual e proceda sem criptografia. (Alternativamente, é permitido emitir uma mensagem GSSENCRequest após uma resposta `N` para tentar usar a criptografia GSSAPI em vez de SSL.)

O frontend também deve estar preparado para lidar com uma resposta ErrorMessage do SSLRequest do servidor. O frontend não deve exibir essa mensagem de erro ao usuário ou aplicativo, uma vez que o servidor não foi autenticado ([CVE-2024-10977](https://www.postgresql.org/support/security/CVE-2024-10977/)). Neste caso, a conexão deve ser fechada, mas o frontend pode optar por abrir uma nova conexão e prosseguir sem solicitar SSL.

Quando a criptografia SSL pode ser realizada, espera-se que o servidor envie apenas o único byte `S` e, em seguida, espere o frontend iniciar uma mão de aperto SSL. Se houver bytes adicionais disponíveis para ler neste ponto, provavelmente significa que um homem no meio está tentando realizar um ataque de enchimento de buffer ([CVE-2021-23222](https://www.postgresql.org/support/security/CVE-2021-23222/)). Os frontends devem ser codificados para ler exatamente um byte do socket antes de transferir o socket para sua biblioteca SSL, ou para tratá-lo como uma violação de protocolo se descobrirem que leram bytes adicionais.

Da mesma forma, o servidor espera que o cliente não comece a negociação SSL até receber a resposta de um único byte do servidor à solicitação SSL. Se o cliente começar a negociação SSL imediatamente sem esperar a resposta do servidor ser recebida, pode reduzir a latência da conexão em uma ida e volta. No entanto, isso ocorre às custas de não poder lidar com o caso em que o servidor envia uma resposta negativa à solicitação SSL. Nesse caso, em vez de continuar com GSSAPI ou uma conexão não criptografada ou um erro de protocolo, o servidor simplesmente se desconectará.

Um SSLRequest inicial também pode ser usado em uma conexão que está sendo aberta para enviar uma mensagem CancelRequest.

Uma segunda maneira alternativa de iniciar a criptografia SSL está disponível. O servidor reconhecerá conexões que imediatamente iniciam a negociação SSL sem quaisquer pacotes SSLRequest anteriores. Uma vez que a conexão SSL seja estabelecida, o servidor esperará um pacote de solicitação de inicialização normal e continuará a negociação pelo canal criptografado. Neste caso, quaisquer outras solicitações de criptografia serão recusadas. Este método não é preferido para ferramentas de uso geral, pois não pode negociar a melhor criptografia de conexão disponível ou lidar com conexões não criptografadas. No entanto, é útil para ambientes onde o servidor e o cliente são controlados juntos. Nesse caso, ele evita uma rodada de latência e permite o uso de ferramentas de rede que dependem de conexões SSL padrão. Ao usar conexões SSL neste estilo, o cliente é obrigado a usar a extensão ALPN definida por [RFC 7301](https://tools.ietf.org/html/rfc7301) para proteger contra ataques de confusão de protocolo. O protocolo PostgreSQL é "postgresql", conforme registrado no registro do IANA TLS ALPN Protocol IDs [(https://www.iana.org/assignments/tls-extensiontype-values/tls-extensiontype-values.xhtml#alpn-protocol-ids)].

Embora o próprio protocolo não forneça uma maneira para o servidor forçar a criptografia SSL, o administrador pode configurar o servidor para rejeitar sessões não criptografadas como um subproduto da verificação de autenticação.

### 54.2.11. Encriptação de sessão GSSAPI [#](#PROTOCOL-FLOW-GSSAPI)

Se o PostgreSQL foi construído com suporte GSSAPI, as comunicações frontend/backend podem ser criptografadas usando GSSAPI. Isso fornece segurança de comunicação em ambientes onde os atacantes podem ser capazes de capturar o tráfego da sessão. Para mais informações sobre criptografar sessões do PostgreSQL com GSSAPI, consulte [Seção 18.10](gssapi-enc.md).

Para iniciar uma conexão criptografada GSSAPI, o frontend envia inicialmente uma mensagem GSSENCRequest em vez de uma StartupMessage. O servidor, em seguida, responde com um único byte contendo `G` ou `N`, indicando que está disposto ou não a realizar a criptografia GSSAPI, respectivamente. O frontend pode fechar a conexão neste ponto, se estiver insatisfeito com a resposta. Para continuar após `G`, usando as ligações C GSSAPI conforme discutido em [RFC 2744](https://datatracker.ietf.org/doc/html/rfc2744) ou equivalente, realize uma inicialização GSSAPI chamando `gss_init_sec_context()` em um loop e enviando o resultado para o servidor, começando com uma entrada vazia e depois com cada resultado do servidor, até que ele retorne sem saída. Ao enviar os resultados de `gss_init_sec_context()` para o servidor, adicione o comprimento da mensagem como um inteiro de quatro bytes em ordem de bytes de rede. Para continuar após `N`, envie a StartupMessage usual e proceda sem criptografia. (Alternativamente, é permitido emitir uma mensagem SSLRequest após uma resposta de `N` para tentar usar a criptografia SSL em vez da GSSAPI.)

O frontend também deve estar preparado para lidar com uma resposta ErrorMessage para GSSENCRequest do servidor. O frontend não deve exibir essa mensagem de erro para o usuário ou aplicativo, uma vez que o servidor não foi autenticado ([CVE-2024-10977](https://www.postgresql.org/support/security/CVE-2024-10977/)). Neste caso, a conexão deve ser fechada, mas o frontend pode optar por abrir uma nova conexão e prosseguir sem solicitar criptografia GSSAPI.

Quando a criptografia GSSAPI pode ser realizada, espera-se que o servidor envie apenas o único byte `G` e, em seguida, espere o frontend iniciar um aperto GSSAPI. Se houver bytes adicionais disponíveis para ler neste ponto, provavelmente significa que um homem no meio está tentando realizar um ataque de enchimento de buffer ([CVE-2021-23222](https://www.postgresql.org/support/security/CVE-2021-23222/)). Os frontends devem ser codificados para ler exatamente um byte do socket antes de transferir o socket para sua biblioteca GSSAPI, ou para tratá-lo como uma violação de protocolo se descobrirem que leram bytes adicionais.

Um pedido inicial GSSENCRequest também pode ser usado em uma conexão que está sendo aberta para enviar uma mensagem de CancelRequest.

Uma vez que a criptografia GSSAPI tenha sido estabelecida com sucesso, use `gss_wrap()` para criptografar a Mensagem de Inicialização usual e todos os dados subsequentes, precedendo o comprimento do resultado de `gss_wrap()` como um inteiro de quatro bytes no formato de byte da rede ao carregamento criptografado real. Note que o servidor só aceitará pacotes criptografados do cliente que sejam menores que 16 kB; o `gss_wrap_size_limit()` deve ser usado pelo cliente para determinar o tamanho da mensagem não criptografada que cabe nesse limite e mensagens maiores devem ser divididas em múltiplas chamadas de `gss_wrap()`. Os segmentos típicos são 8 kB de dados não criptografados, resultando em pacotes criptografados ligeiramente maiores que 8 kB, mas bem dentro do máximo de 16 kB. Pode-se esperar que o servidor não envie pacotes criptografados maiores que 16 kB ao cliente.

Embora o próprio protocolo não forneça uma maneira para o servidor forçar a criptografia GSSAPI, o administrador pode configurar o servidor para rejeitar sessões não criptografadas como um subproduto da verificação de autenticação.