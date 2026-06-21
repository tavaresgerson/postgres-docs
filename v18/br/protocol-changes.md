## 54.10. Resumo das alterações desde o Protocolo 2.0 [#](#PROTOCOL-CHANGES)

Esta seção fornece uma lista rápida de mudanças, para o benefício dos desenvolvedores que tentam atualizar as bibliotecas de cliente existentes para o protocolo 3.0.

O pacote inicial de inicialização utiliza um formato flexível de lista de strings em vez de um formato fixo. Observe que os valores padrão de sessão para os parâmetros de execução podem agora ser especificados diretamente no pacote inicial. (Na verdade, você poderia fazer isso antes de usar o campo `options`, mas, dada a largura limitada de `options` e a falta de qualquer maneira de citar espaços em branco nos valores, não era uma técnica muito segura.)

Todas as mensagens agora têm um contador de comprimento imediatamente após o byte do tipo de mensagem (exceto pacotes de inicialização, que não têm byte de tipo). Além disso, observe que o PasswordMessage agora tem um byte de tipo.

As mensagens ErrorResponse e NoticeResponse (`E` e `N`) agora contêm vários campos, dos quais o código do cliente pode montar uma mensagem de erro do nível de verbosidade desejado. Observe que os campos individuais geralmente não terminam com uma nova linha, enquanto a única string enviada no protocolo mais antigo sempre fazia.

A mensagem ReadyForQuery (`Z`) inclui um indicador de status de transação.

A distinção entre os tipos de mensagens BinaryRow e DataRow desapareceu; o único tipo de mensagem DataRow serve para retornar dados em todos os formatos. Observe que o layout do DataRow foi alterado para facilitar a análise. Além disso, a representação dos valores binários mudou: ela não está mais diretamente ligada à representação interna do servidor.

Existe um novo subprotocolo de “consulta estendida”, que adiciona os tipos de mensagem de frontend Parse, Bind, Execute, Describe, Close, Flush e Sync, e os tipos de mensagem de backend ParseComplete, BindComplete, PortalSuspended, ParameterDescription, NoData e CloseComplete. Os clientes existentes não precisam se preocupar com este subprotocolo, mas o uso dele pode permitir melhorias no desempenho ou na funcionalidade.

Os dados `COPY` estão agora encapsulados nas mensagens CopyData e CopyDone. Há uma maneira bem definida de recuperar erros durante o `COPY`. A última linha especial “`\.`” não é mais necessária e não é enviada durante o `COPY OUT`. (Ainda é reconhecida como um terminador durante o `COPY IN` em modo de texto, mas não no modo CSV. O comportamento em modo de texto é desatualizado e pode ser eventualmente removido.) O `COPY` binário é suportado. As mensagens CopyInResponse e CopyOutResponse incluem campos que indicam o número de colunas e o formato de cada coluna.

O layout das mensagens FunctionCall e FunctionCallResponse foi alterado. FunctionCall agora pode suportar a passagem de argumentos NULL para funções. Também pode lidar com a passagem de parâmetros e a recuperação de resultados em formato de texto ou binário. Não há mais motivo para considerar FunctionCall uma possível lacuna de segurança, uma vez que não oferece acesso direto às representações de dados do servidor interno.

O backend envia mensagens ParameterStatus (`S`) durante o início da conexão para todos os parâmetros que considera interessantes para a biblioteca do cliente. Posteriormente, uma mensagem ParameterStatus é enviada sempre que o valor ativo muda para qualquer um desses parâmetros.

A mensagem RowDescription ('`T`') carrega novos campos de OID de tabela e número de coluna para cada coluna da linha descrita. Também mostra o código de formato para cada coluna.

A mensagem CursorResponse (`P`) não é mais gerada pelo backend.

A mensagem NotificationResponse (`A`) possui um campo de string adicional, que pode conter uma string de "carga" passada pelo remetente do evento `NOTIFY`.

A mensagem EmptyQueryResponse (`I`) costumava incluir um parâmetro de string vazia; isso foi removido.