## 54.7. Formulários de Mensagem [#](#PROTOCOL-MESSAGE-FORMATS)

Esta seção descreve o formato detalhado de cada mensagem. Cada uma é marcada para indicar que pode ser enviada por um frontend (F), um backend (B) ou ambas (F & B). Observe que, embora cada mensagem inclua um contador de bytes no início, a maioria das mensagens é definida de modo que o fim da mensagem possa ser encontrado sem referência ao contador de bytes. Isso ocorre por razões históricas, pois a versão original do protocolo, agora obsoleta, a versão 2, não tinha um campo de comprimento explícito. Isso também auxilia na verificação de validade.

AutenticaçãoOk (B) [#](#PROTOCOL-MESSAGE-FORMATS-AUTHENTICATIONOK): Byte1('R') :   Identifica a mensagem como um pedido de autenticação.

Int32(8) :   Comprimento dos conteúdos da mensagem em bytes, incluindo self.

Int32(0) : Especifica que a autenticação foi bem-sucedida.

AutenticaçãoKerberosV5 (B) [#](#PROTOCOL-MESSAGE-FORMATS-AUTHENTICATIONKERBEROSV5): Byte1('R') :   Identifica a mensagem como um pedido de autenticação.

Int32(8) :   Comprimento dos conteúdos da mensagem em bytes, incluindo self.

Int32(2) : Especifica que a autenticação Kerberos V5 é necessária.

AutenticaçãoCleartextPassword (B) [#](#PROTOCOL-MESSAGE-FORMATS-AUTHENTICATIONCLEARTEXTPASSWORD): Byte1('R') :   Identifica a mensagem como um pedido de autenticação.

Int32(8) :   Comprimento dos conteúdos da mensagem em bytes, incluindo self.

Int32(3) : Especifica que é necessária uma senha em texto claro.

AutenticaçãoMD5Password (B) [#](#PROTOCOL-MESSAGE-FORMATS-AUTHENTICATIONMD5PASSWORD): Byte1('R') :   Identifica a mensagem como um pedido de autenticação.

Int32(12) :   Comprimento dos conteúdos da mensagem em bytes, incluindo self.

Int32(5) : Especifica que é necessária uma senha criptografada por MD5.

Byte4: o sal a ser usado ao criptografar a senha.

Autenticação GSS (B) [#](#PROTOCOL-MESSAGE-FORMATS-AUTHENTICATIONGSS): Byte1('R') :   Identifica a mensagem como um pedido de autenticação.

Int32(8) :   Comprimento dos conteúdos da mensagem em bytes, incluindo self.

Int32(7) : Especifica que a autenticação GSSAPI é necessária.

AutenticaçãoGSSContinue (B) [#](#PROTOCOL-MESSAGE-FORMATS-AUTHENTICATIONGSSCONTINUE): Byte1('R') :   Identifica a mensagem como um pedido de autenticação.

Int32:   Comprimento do conteúdo da mensagem em bytes, incluindo self.

Int32(8) : Especifica que esta mensagem contém dados GSSAPI ou SSPI.

Byte*`n`* :   Dados de autenticação GSSAPI ou SSPI.

AutenticaçãoSSPI (B) [#](#PROTOCOL-MESSAGE-FORMATS-AUTHENTICATIONSSPI): Byte1('R') :   Identifica a mensagem como um pedido de autenticação.

Int32(8) :   Comprimento dos conteúdos da mensagem em bytes, incluindo self.

Int32(9) : Especifica que a autenticação SSPI é necessária.

AutenticaçãoSASL (B) [#](#PROTOCOL-MESSAGE-FORMATS-AUTHENTICATIONSASL): Byte1('R') :   Identifica a mensagem como um pedido de autenticação.

Int32:   Comprimento do conteúdo da mensagem em bytes, incluindo self.

Int32(10) : Especifica que a autenticação SASL é necessária.

O corpo da mensagem é uma lista de mecanismos de autenticação SASL, na ordem de preferência do servidor. Um byte zero é necessário como terminador após o último nome do mecanismo de autenticação. Para cada mecanismo, há o seguinte:

String:   Nome de um mecanismo de autenticação SASL.

AutenticaçãoSASLContinuar (B) [#](#PROTOCOL-MESSAGE-FORMATS-AUTHENTICATIONSASLCONTINUE): Byte1('R') :   Identifica a mensagem como um pedido de autenticação.

Int32:   Comprimento do conteúdo da mensagem em bytes, incluindo self.

Int32(11) : Especifica que esta mensagem contém um desafio SASL.

Byte*`n`* :   Dados SASL, específicos para o mecanismo SASL utilizado.

AutenticaçãoSASLFinal (B) [#](#PROTOCOL-MESSAGE-FORMATS-AUTHENTICATIONSASLFINAL): Byte1('R') :   Identifica a mensagem como um pedido de autenticação.

Int32:   Comprimento do conteúdo da mensagem em bytes, incluindo self.

Int32(12) : Especifica que a autenticação SASL foi concluída.

Byte*`n`* :   Resultado SASL "dados adicionais", específico ao mecanismo SASL que está sendo utilizado.

BackendKeyData (B) [#](#PROTOCOL-MESSAGE-FORMATS-BACKENDKEYDATA): Byte1('K') :   Identifica os dados da chave de cancelamento. O frontend deve salvar esses valores se desejar ser capaz de emitir mensagens CancelRequest mais tarde.

Int32:   Comprimento do conteúdo da mensagem em bytes, incluindo self.

Int32: O ID do processo deste backend.

Byte*`n`* :   A chave secreta deste backend. Este campo se estende até o final da mensagem, indicado pelo campo de comprimento.

O comprimento mínimo e máximo da chave é de 4 e 256 bytes, respectivamente. O servidor PostgreSQL envia chaves apenas até 32 bytes, mas o tamanho máximo maior permite que futuras versões do servidor, bem como geradores de pool de conexões e outros middleware, usem chaves mais longas. Um caso de uso possível é aumentar a chave do servidor com informações adicionais. Portanto, também é incentivado que o middleware não use todos os bytes, caso múltiplos aplicativos de middleware estejam sobrepostos um sobre o outro, cada um dos quais pode envolver a chave com dados adicionais.

Antes da versão 3.2 do protocolo, a chave secreta sempre tinha 4 bytes de comprimento.

Liga (F) [#](#PROTOCOL-MESSAGE-FORMATS-BIND): Byte1('B') :   Identifica a mensagem como um comando de Liga.

Int32:   Comprimento do conteúdo da mensagem em bytes, incluindo self.

String:   O nome do portal de destino (uma string vazia seleciona o portal sem nome).

String:   O nome da declaração preparada da fonte (uma string vazia seleciona a declaração preparada sem nome).

Int16:   O número de códigos de formato de parâmetro que se seguem (denotados *`C`* abaixo). Isso pode ser zero para indicar que não há parâmetros ou que todos os parâmetros usam o formato padrão (texto); ou um, caso em que o código de formato especificado é aplicado a todos os parâmetros; ou pode ser igual ao número real de parâmetros.

Int16[*`C`*] :   Os códigos de formato do parâmetro. Cada um deve ser atualmente zero (texto) ou um (binário).

Int16:   O número de valores de parâmetro que se seguem (possível zero). Isso deve corresponder ao número de parâmetros necessários pela consulta.

Em seguida, o seguinte par de campos aparece para cada parâmetro:

Int32:   O comprimento do valor do parâmetro, em bytes (este contador não inclui o próprio valor). Pode ser zero. Como um caso especial, -1 indica um valor de parâmetro NULL. Não há bytes de valor após o caso NULL.

Byte*`n`* :   O valor do parâmetro, no formato indicado pelo código de formato associado. *`n`* tem o comprimento acima.

Após o último parâmetro, aparecem os seguintes campos:

Int16:   O número de códigos de formato de coluna de resultado que se seguem (denotados *`R`* abaixo). Isso pode ser zero para indicar que não há colunas de resultado ou que todas as colunas de resultado devem usar o formato padrão (texto); ou um, no caso, o código de formato especificado é aplicado a todas as colunas de resultado (se houver); ou pode ser igual ao número real de colunas de resultado da consulta.

Int16[*`R`*] :   Códigos de formato da coluna de resultado. Cada um deve ser atualmente zero (texto) ou um (binário).

BindComplete (B) [#](#PROTOCOL-MESSAGE-FORMATS-BINDCOMPLETE): Byte1('2') :   Identifica a mensagem como um indicador de Bind-complete.

Int32(4) :   Comprimento dos conteúdos da mensagem em bytes, incluindo self.

CancelRequest (F) [#](#PROTOCOL-MESSAGE-FORMATS-CANCELREQUEST): Int32 :   Comprimento dos conteúdos da mensagem em bytes, incluindo self.

Int32(80877102):   O código de solicitação de cancelamento. O valor é escolhido para conter `1234` nos 16 bits mais significativos e `5678` nos 16 bits menos significativos. (Para evitar confusão, este código não deve ser o mesmo que qualquer número de versão do protocolo.)

Int32: O ID do processo do backend alvo.

Byte*`n`* :   A chave secreta para o backend de destino. Este campo se estende até o final da mensagem, indicado pelo campo de comprimento. O comprimento máximo da chave é de 256 bytes.

Antes da versão 3.2 do protocolo, a chave secreta sempre tinha 4 bytes de comprimento.

Fechar (F) [#](#PROTOCOL-MESSAGE-FORMATS-CLOSE): Byte1('C') :   Identifica a mensagem como um comando de Fechamento.

Int32:   Comprimento do conteúdo da mensagem em bytes, incluindo self.

Byte1: '`S`' para fechar uma declaração preparada; ou '`P`' para fechar um portal.

String:   O nome da declaração preparada ou do portal a ser fechado (uma string vazia seleciona a declaração preparada ou o portal sem nome).

Fechamento Completo (B) [#](#PROTOCOL-MESSAGE-FORMATS-CLOSECOMPLETE): Byte1('3') :   Identifica a mensagem como um indicador de Fechamento Completo.

Int32(4) :   Comprimento dos conteúdos da mensagem em bytes, incluindo self.

CommandComplete (B) [#](#PROTOCOL-MESSAGE-FORMATS-COMMANDCOMPLETE): Byte1('C') :   Identifica a mensagem como uma resposta de comando concluída.

Int32:   Comprimento do conteúdo da mensagem em bytes, incluindo self.

String:   O rótulo do comando. Geralmente, é uma palavra única que identifica qual comando SQL foi completado.

Para um comando `INSERT`, a tag é `INSERT oid rows`, onde *`rows`* é o número de linhas inseridas. *`oid`* era o ID do objeto da linha inserida se *`rows`* fosse 1 e a tabela de destino tivesse IDs, mas as colunas de sistema de IDs não são suportadas mais; portanto, *`oid`* é sempre 0.

Para um comando `DELETE`, a tag é `DELETE rows`, onde *`rows`* é o número de linhas excluídas.

Para um comando `UPDATE`, a tag é `UPDATE rows`, onde *`rows`* é o número de linhas atualizadas.

Para um comando `MERGE`, a tag é `MERGE rows`, onde *`rows`* é o número de linhas inseridas, atualizadas ou excluídas.

Para um comando `SELECT` ou `CREATE TABLE AS`, a tag é `SELECT rows`, onde *`rows`* é o número de linhas recuperadas.

Para um comando `MOVE`, a etiqueta é `MOVE rows`, onde *`rows`* é o número de linhas em que a posição do cursor foi alterada.

Para um comando `FETCH`, a tag é `FETCH rows`, onde *`rows`* é o número de linhas que foram recuperadas do cursor.

Para um comando `COPY`, a tag é `COPY rows`, onde *`rows`* é o número de linhas copiadas. (Nota: o contagem de linhas aparece apenas no PostgreSQL 8.2 e versões posteriores.)

CopyData (F & B) [#](#PROTOCOL-MESSAGE-FORMATS-COPYDATA): Byte1('d') :   Identifica a mensagem como dados `COPY`.

Int32:   Comprimento do conteúdo da mensagem em bytes, incluindo self.

Byte*`n`* :   Dados que fazem parte de um fluxo de dados `COPY`. Mensagens enviadas pelo backend sempre correspondem a linhas de dados individuais, mas as mensagens enviadas pelos frontends podem dividir o fluxo de dados arbitrariamente.

CopyDone (F & B) [#](#PROTOCOL-MESSAGE-FORMATS-COPYDONE): Byte1('c') :   Identifica a mensagem como um indicador `COPY`-completo.

Int32(4) :   Comprimento dos conteúdos da mensagem em bytes, incluindo self.

CopyFail (F) [#](#PROTOCOL-MESSAGE-FORMATS-COPYFAIL): Byte1('f') :   Identifica a mensagem como um indicador de `COPY`-falha.

Int32:   Comprimento do conteúdo da mensagem em bytes, incluindo self.

Texto em inglês: String: Uma mensagem de erro a ser relatada como causa do falha.

CopyInResponse (B) [#](#PROTOCOL-MESSAGE-FORMATS-COPYINRESPONSE): Byte1('G') :   Identifica a mensagem como uma Início da cópia em resposta. O frontend deve agora enviar dados de cópia (se não estiver preparado para isso, envie uma mensagem CopyFail).

Int32:   Comprimento do conteúdo da mensagem em bytes, incluindo self.

Int8:   0 indica que o formato geral `COPY` é textual (linhas separadas por novas linhas, colunas separadas por caracteres de separador, etc.). 1 indica que o formato geral de cópia é binário (semelhante ao formato DataRow). Consulte [COPY](sql-copy.md "COPY") para obter mais informações.

Int16:   O número de colunas dos dados a serem copiados (indicado como *`N`* abaixo).

Int16[*`N`*] :   Os códigos de formato a serem utilizados para cada coluna. Cada um deve ser atualmente zero (texto) ou um (binário). Todos devem ser zero se o formato geral da cópia for textual.

CopyOutResponse (B) [#](#PROTOCOL-MESSAGE-FORMATS-COPYOUTRESPONSE): Byte1('H') :   Identifica a mensagem como uma resposta de Início de Saída de Cópia. Esta mensagem será seguida pelos dados de saída de cópia.

Int32:   Comprimento do conteúdo da mensagem em bytes, incluindo self.

Int8:   0 indica que o formato geral `COPY` é textual (linhas separadas por novas linhas, colunas separadas por caracteres de separador, etc.). 1 indica que o formato geral de cópia é binário (semelhante ao formato DataRow). Consulte [COPY](sql-copy.md "COPY") para obter mais informações.

Int16:   O número de colunas dos dados a serem copiados (indicado como *`N`* abaixo).

Int16[*`N`*] :   Os códigos de formato a serem utilizados para cada coluna. Cada um deve ser atualmente zero (texto) ou um (binário). Todos devem ser zero se o formato geral da cópia for textual.

CopyBothResponse (B) [#](#PROTOCOL-MESSAGE-FORMATS-COPYBOTHRESPONSE): Byte1('W') :   Identifica a mensagem como uma resposta de Início de Cópia Ambos. Esta mensagem é usada apenas para Replicação em Streaming.

Int32:   Comprimento do conteúdo da mensagem em bytes, incluindo self.

Int8:   0 indica que o formato geral `COPY` é textual (linhas separadas por novas linhas, colunas separadas por caracteres de separador, etc.). 1 indica que o formato geral de cópia é binário (semelhante ao formato DataRow). Consulte [COPY](sql-copy.md "COPY") para obter mais informações.

Int16:   O número de colunas dos dados a serem copiados (indicado como *`N`* abaixo).

Int16[*`N`*] :   Os códigos de formato a serem utilizados para cada coluna. Cada um deve ser atualmente zero (texto) ou um (binário). Todos devem ser zero se o formato geral da cópia for textual.

DataRow (B) [#](#PROTOCOL-MESSAGE-FORMATS-DATAROW): Byte1('D') :   Identifica a mensagem como uma linha de dados.

Int32:   Comprimento do conteúdo da mensagem em bytes, incluindo self.

Int16:   O número de valores de coluna que se seguem (possível zero).

Em seguida, o seguinte par de campos aparece para cada coluna:

Int32:   O comprimento do valor da coluna, em bytes (este contador não inclui o próprio valor). Pode ser zero. Como um caso especial, -1 indica um valor de coluna NULL. Não há bytes de valor após o caso NULL.

Byte*`n`* :   O valor da coluna, no formato indicado pelo código de formato associado. *`n`* é o comprimento acima.

Descreva (F) [#](#PROTOCOL-MESSAGE-FORMATS-DESCRIBE): Byte1('D') :   Identifica a mensagem como um comando de Descrição.

Int32:   Comprimento do conteúdo da mensagem em bytes, incluindo self.

Byte1: '`S`' para descrever uma declaração preparada; ou '`P`' para descrever um portal.

String:   O nome da declaração preparada ou do portal a ser descrito (uma string vazia seleciona a declaração preparada ou o portal sem nome).

EmptyQueryResponse (B) [#](#PROTOCOL-MESSAGE-FORMATS-EMPTYQUERYRESPONSE): Byte1('I') :   Identifica a mensagem como uma resposta a uma string de consulta vazia. (Isso substitui CommandComplete.)

Int32(4) :   Comprimento dos conteúdos da mensagem em bytes, incluindo self.

ErroResponse (B) [#](#PROTOCOL-MESSAGE-FORMATS-ERRORRESPONSE): Byte1('E') :   Identifica a mensagem como um erro.

Int32:   Comprimento do conteúdo da mensagem em bytes, incluindo self.

O corpo da mensagem consiste em um ou mais campos identificados, seguido por um byte zero como terminador. Os campos podem aparecer em qualquer ordem. Para cada campo, há o seguinte:

Byte1:   Um código que identifica o tipo de campo; se zero, este é o terminador da mensagem e não há uma string a seguir. Os tipos de campo atualmente definidos estão listados em [Seção 54.8](protocol-error-fields.md). Como é possível que mais tipos de campo sejam adicionados no futuro, os frontends devem ignorar silenciosamente campos de tipo não reconhecido.

Campo:   O valor do campo.

Execute (F) [#](#PROTOCOL-MESSAGE-FORMATS-EXECUTE): Byte1('E') :   Identifica a mensagem como um comando Execute.

Int32:   Comprimento do conteúdo da mensagem em bytes, incluindo self.

String:   O nome do portal a ser executado (uma string vazia seleciona o portal sem nome).

Int32: Número máximo de linhas a serem retornadas, se o portal contiver uma consulta que retorna linhas (ignoradas de outra forma). Zero denota “sem limite”.

Flush (F) [#](#PROTOCOL-MESSAGE-FORMATS-FLUSH): Byte1('H') :   Identifica a mensagem como um comando de Flush.

Int32(4) :   Comprimento dos conteúdos da mensagem em bytes, incluindo self.

FunctionCall (F) [#](#PROTOCOL-MESSAGE-FORMATS-FUNCTIONCALL): Byte1('F') :   Identifica a mensagem como uma chamada de função.

Int32:   Comprimento do conteúdo da mensagem em bytes, incluindo self.

Int32: especifica o ID do objeto da função a ser chamada.

Int16:   O número de códigos de formato de argumento que se seguem (denotado *`C`* abaixo). Isso pode ser zero para indicar que não há argumentos ou que todos os argumentos usam o formato padrão (texto); ou um, caso em que o código de formato especificado é aplicado a todos os argumentos; ou pode ser igual ao número real de argumentos.

Int16[*`C`*] :   Os códigos de formato de argumento. Cada um deve ser atualmente zero (texto) ou um (binário).

Int16: especifica o número de argumentos fornecidos à função.

Em seguida, o seguinte par de campos aparece para cada argumento:

Int32:   O comprimento do valor do argumento, em bytes (este contagem não inclui o próprio valor). Pode ser zero. Como um caso especial, -1 indica um valor de argumento NULL. Não há bytes de valor após o caso NULL.

Byte*`n`* :   O valor do argumento, no formato indicado pelo código de formato associado. *`n`* tem o comprimento acima.

Após o último argumento, o seguinte campo aparece:

Int16:   O código de formato para o resultado da função. Deve ser atualmente zero (texto) ou um (binário).

FunctionCallResponse (B) [#](#PROTOCOL-MESSAGE-FORMATS-FUNCTIONCALLRESPONSE): Byte1('V') :   Identifica a mensagem como um resultado de chamada de função.

Int32:   Comprimento do conteúdo da mensagem em bytes, incluindo self.

Int32:   O comprimento do valor do resultado da função, em bytes (este contador não inclui o próprio valor). Pode ser zero. Como um caso especial, -1 indica um resultado de função NULL. Não há bytes de valor após o caso NULL.

Byte*`n`* :   O valor do resultado da função, no formato indicado pelo código de formato associado. *`n`* tem o comprimento acima.

GSSENCRequest (F) [#](#PROTOCOL-MESSAGE-FORMATS-GSSENCREQUEST): Int32(8) :   Comprimento dos conteúdos da mensagem em bytes, incluindo self.

Int32(80877104):   O código de solicitação de criptografia GSSAPI. O valor é escolhido para conter `1234` nos 16 bits mais significativos e `5680` nos 16 bits menos significativos. (Para evitar confusão, este código não deve ser o mesmo que qualquer número de versão do protocolo.)

GSSResponse (F) [#](#PROTOCOL-MESSAGE-FORMATS-GSSRESPONSE): Byte1('p') :   Identifica a mensagem como uma resposta GSSAPI ou SSPI. Note que isso também é usado para mensagens de resposta SASL e senha. O tipo exato da mensagem pode ser deduzido do contexto.

Int32:   Comprimento do conteúdo da mensagem em bytes, incluindo self.

Byte*`n`* :   Dados de mensagem específicos do GSSAPI/SSPI.

Negociar versão do protocolo (B) [#](#PROTOCOL-MESSAGE-FORMATS-NEGOTIATEPROTOCOLVERSION): Byte1('v') :   Identifica a mensagem como uma mensagem de negociação de versão do protocolo.

Int32:   Comprimento do conteúdo da mensagem em bytes, incluindo self.

Int32:   A versão do protocolo menor mais recente suportada pelo servidor para a versão do protocolo principal solicitada pelo cliente.

Int32: Número de opções de protocolo não reconhecidas pelo servidor.

Em seguida, para a opção de protocolo que não é reconhecida pelo servidor, há o seguinte:

String:   Nome da opção.

NoData (B) [#](#PROTOCOL-MESSAGE-FORMATS-NODATA): Byte1('n') :   Identifica a mensagem como um indicador de ausência de dados.

Int32(4) :   Comprimento dos conteúdos da mensagem em bytes, incluindo self.

Aviso (B) [#](#PROTOCOL-MESSAGE-FORMATS-NOTICERESPONSE): Byte1('N') :   Identifica a mensagem como um aviso.

Int32:   Comprimento do conteúdo da mensagem em bytes, incluindo self.

O corpo da mensagem consiste em um ou mais campos identificados, seguido por um byte zero como terminador. Os campos podem aparecer em qualquer ordem. Para cada campo, há o seguinte:

Byte1:   Um código que identifica o tipo de campo; se zero, este é o terminador da mensagem e não há uma string a seguir. Os tipos de campo atualmente definidos estão listados em [Seção 54.8](protocol-error-fields.md). Como pode haver mais tipos de campo no futuro, os frontends devem ignorar silenciosamente campos de tipo não reconhecido.

Campo:   O valor do campo.

NotificaçãoResponse (B) [#](#PROTOCOL-MESSAGE-FORMATS-NOTIFICATIONRESPONSE): Byte1('A') :   Identifica a mensagem como uma resposta de notificação.

Int32:   Comprimento do conteúdo da mensagem em bytes, incluindo self.

Int32: O ID do processo do backend notificador.

String:   O nome do canal em que o notificado foi levantado.

String:   A string “payload” passada pelo processo de notificação.

Descrição do parâmetro (B) [#](#PROTOCOL-MESSAGE-FORMATS-PARAMETERDESCRIPTION): Byte1('t') :   Identifica a mensagem como uma descrição de parâmetro.

Int32:   Comprimento do conteúdo da mensagem em bytes, incluindo self.

Int16:   O número de parâmetros utilizados pela declaração (pode ser zero).

Em seguida, para cada parâmetro, há o seguinte:

Int32: Especifica o ID do objeto do tipo de dados do parâmetro.

ParameterStatus (B) [#](#PROTOCOL-MESSAGE-FORMATS-PARAMETERSTATUS): Byte1('S') :   Identifica a mensagem como um relatório de status de parâmetro de tempo de execução.

Int32:   Comprimento do conteúdo da mensagem em bytes, incluindo self.

String:   O nome do parâmetro de execução que está sendo relatado.

String:   O valor atual do parâmetro.

Parse (F) [#](#PROTOCOL-MESSAGE-FORMATS-PARSE): Byte1('P') :   Identifica a mensagem como um comando Parse.

Int32:   Comprimento do conteúdo da mensagem em bytes, incluindo self.

String:   O nome da declaração preparada do destino (uma string vazia seleciona a declaração preparada sem nome).

String:   A string de consulta a ser analisada.

Int16:   O número de tipos de dados dos parâmetros especificados (pode ser zero). Observe que isso não é uma indicação do número de parâmetros que podem aparecer na string de consulta, apenas o número que o frontend quer especificar tipos para.

Em seguida, para cada parâmetro, há o seguinte:

Int32:   Especifica o ID do objeto do tipo de dados do parâmetro. Colocar um zero aqui é equivalente a deixar o tipo não especificado.

ParseComplete (B) [#](#PROTOCOL-MESSAGE-FORMATS-PARSECOMPLETE): Byte1('1') :   Identifica a mensagem como um indicador de conclusão de análise.

Int32(4) :   Comprimento dos conteúdos da mensagem em bytes, incluindo self.

Mensagem de senha (F) [#](#PROTOCOL-MESSAGE-FORMATS-PASSWORDMESSAGE): Byte1('p') :   Identifica a mensagem como uma resposta de senha. Note que isso também é usado para mensagens de resposta GSSAPI, SSPI e SASL. O tipo exato da mensagem pode ser deduzido do contexto.

Int32:   Comprimento do conteúdo da mensagem em bytes, incluindo self.

Senha: (criptografada, se solicitado).

PortalSuspendido (B) [#](#PROTOCOL-MESSAGE-FORMATS-PORTALSUSPENDED): Byte1('s') :   Identifica a mensagem como um indicador suspenso no portal. Este aviso só aparece se o limite de contagem de linhas de uma mensagem de execução foi atingido.

Int32(4) :   Comprimento dos conteúdos da mensagem em bytes, incluindo self.

Pergunta (F) [#](#PROTOCOL-MESSAGE-FORMATS-QUERY): Byte1('Q') :   Identifica a mensagem como uma simples pergunta.

Int32:   Comprimento do conteúdo da mensagem em bytes, incluindo self.

String:   A própria string de consulta.

ReadyForQuery (B) [#](#PROTOCOL-MESSAGE-FORMATS-READYFORQUERY): Byte1('Z') :   Identifica o tipo de mensagem. O ReadyForQuery é enviado sempre que o backend está pronto para um novo ciclo de consulta.

Int32(5) :   Comprimento dos conteúdos da mensagem em bytes, incluindo self.

Byte1: Indicador atual do status da transação do backend. Os valores possíveis são '`I`' se ocioso (não em um bloco de transação); '`T`' se em um bloco de transação; ou '`E`' se em um bloco de transação falha (as consultas serão rejeitadas até que o bloco seja encerrado).

Descrição da linha (B) [#](#PROTOCOL-MESSAGE-FORMATS-ROWDESCRIPTION): Byte1('T') :   Identifica a mensagem como uma descrição de linha.

Int32:   Comprimento do conteúdo da mensagem em bytes, incluindo self.

Int16: especifica o número de campos em uma linha (pode ser zero).

Em seguida, para cada campo, há o seguinte:

Campo:   O nome do campo.

Int32:   Se o campo puder ser identificado como uma coluna de uma tabela específica, o ID do objeto da tabela; caso contrário, zero.

Int16: Se o campo puder ser identificado como uma coluna de uma tabela específica, o número de atributo da coluna; caso contrário, zero.

Int32: O ID do objeto do tipo de dados do campo.

Int16:   O tipo de dados tamanho (consulte `pg_type.typlen`). Observe que os valores negativos indicam tipos de largura variável.

Int32:   O modificador de tipo (consulte `pg_attribute.atttypmod`). O significado do modificador é específico ao tipo.

Int16:   O código de formato que está sendo usado para o campo. Atualmente será zero (texto) ou um (binário). Em uma Descrição de linha retornada a partir da variante de declaração de Descrever, o código de formato ainda não é conhecido e sempre será zero.

SASLInitialResponse (F) [#](#PROTOCOL-MESSAGE-FORMATS-SASLINITIALRESPONSE): Byte1('p') :   Identifica a mensagem como uma resposta inicial SASL. Observe que isso também é usado para mensagens de resposta GSSAPI, SSPI e senha. O tipo exato da mensagem é deduzido do contexto.

Int32:   Comprimento do conteúdo da mensagem em bytes, incluindo self.

String: Nome do mecanismo de autenticação SASL que o cliente selecionou.

Int32:   Comprimento do mecanismo SASL específico "Resposta Inicial do Cliente" que segue, ou -1 se não houver Resposta Inicial.

Byte*`n`* : Mecanismo de SASL específico "Resposta Inicial".

SASLResponse (F) [#](#PROTOCOL-MESSAGE-FORMATS-SASLRESPONSE): Byte1('p') :   Identifica a mensagem como uma resposta SASL. Note que isso também é usado para mensagens de resposta GSSAPI, SSPI e senha. O tipo exato da mensagem pode ser deduzido do contexto.

Int32:   Comprimento do conteúdo da mensagem em bytes, incluindo self.

Byte*`n`* :   Dados de mensagem específicos do mecanismo SASL.

SSLRequest (F) [#](#PROTOCOL-MESSAGE-FORMATS-SSLREQUEST): Int32(8) :   Comprimento dos conteúdos da mensagem em bytes, incluindo self.

Int32(80877103):   O código da solicitação SSL. O valor é escolhido para conter `1234` nos 16 bits mais significativos e `5679` nos 16 bits menos significativos. (Para evitar confusão, este código não deve ser o mesmo que qualquer número de versão do protocolo.)

StartupMessage (F) [#](#PROTOCOL-MESSAGE-FORMATS-STARTUPMESSAGE): Int32 :   Comprimento dos conteúdos da mensagem em bytes, incluindo self.

Int32(196610) :   O número da versão do protocolo. Os 16 bits mais significativos são o número da versão principal (3 para o protocolo descrito aqui). Os 16 bits menos significativos são o número da versão secundária (2 para o protocolo descrito aqui).

O número da versão do protocolo é seguido por um ou mais pares de nomes de parâmetros e strings de valor. Um byte zero é necessário como um terminador após o último par nome/valor. Os parâmetros podem aparecer em qualquer ordem. `user` é necessário, outros são opcionais. Cada parâmetro é especificado como:

String:   O nome do parâmetro. Os nomes atualmente reconhecidos são:

`user` :   O nome do usuário do banco de dados para se conectar. Requerido; não há um padrão.

`database` :   O banco de dados a ser conectado. O padrão é o nome do usuário.

`options` : Argumentos de linha de comando para o backend. (Isso é desaconselhado em favor da definição de parâmetros individuais de execução.) Espaços dentro desta string são considerados para separar argumentos, a menos que escapados com uma barra invertida (`\`); escreva `\\` para representar uma barra invertida literal.

`replication` :   Usado para conectar no modo de replicação em fluxo, onde um pequeno conjunto de comandos de replicação pode ser emitido em vez de declarações SQL. O valor pode ser `true`, `false` ou `database`, e o padrão é `false`. Veja [Seção 54.4](protocol-replication.md "54.4. Streaming Replication Protocol") para detalhes.

Além do acima, outros parâmetros podem ser listados. Os nomes dos parâmetros que começam com `_pq_.` são reservados para uso como extensões de protocolo, enquanto outros são tratados como parâmetros de tempo de execução a serem definidos no momento do início do backend. Esses ajustes serão aplicados durante o início do backend (após a análise dos argumentos da linha de comando, se houver) e agirão como configurações padrão da sessão.

String:   O valor do parâmetro.

Sincronizar (F) [#](#PROTOCOL-MESSAGE-FORMATS-SYNC): Byte1('S') :   Identifica a mensagem como um comando de sincronização.

Int32(4) :   Comprimento dos conteúdos da mensagem em bytes, incluindo self.

Finalizar (F) [#](#PROTOCOL-MESSAGE-FORMATS-TERMINATE): Byte1('X') :   Identifica a mensagem como uma finalização.

Int32(4) :   Comprimento dos conteúdos da mensagem em bytes, incluindo self.