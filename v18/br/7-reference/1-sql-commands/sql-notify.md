## NOTIFICAR

NOTIFICAR — gerar uma notificação

## Sinopse

```
NOTIFY channel [ , payload ]
```

## Descrição

O comando `NOTIFY` envia um evento de notificação junto com uma string de "carga" opcional para cada aplicativo de cliente que tenha executado previamente `LISTEN channel` para o nome do canal especificado no banco de dados atual. As notificações são visíveis para todos os usuários.

`NOTIFY` fornece um mecanismo simples de comunicação entre processos para uma coleção de processos que acessam o mesmo banco de dados PostgreSQL. Uma string de carga pode ser enviada juntamente com a notificação, e mecanismos de nível superior para passar dados estruturados podem ser construídos usando tabelas no banco de dados para passar dados adicionais do notificador para o(s) ouvinte(s).

As informações transmitidas ao cliente para um evento de notificação incluem o nome do canal de notificação, o PID do processo do servidor da sessão notificadora e a string de carga, que é uma string vazia se não tiver sido especificada.

Cabe ao projetista do banco de dados definir os nomes dos canais que serão usados em um banco de dados específico e o que cada um deles significa. Comumente, o nome do canal é o mesmo que o nome de alguma tabela no banco de dados, e o evento de notificação essencialmente significa: “Eu alterei esta tabela, dê uma olhada nela para ver o que há de novo”. Mas nenhuma associação desse tipo é imposta pelos comandos `NOTIFY` e `LISTEN`. Por exemplo, um projetista de banco de dados poderia usar vários nomes de canais diferentes para sinalizar diferentes tipos de alterações em uma única tabela. Alternativamente, a string de carga pode ser usada para diferenciar vários casos.

Quando o `NOTIFY` é usado para sinalizar a ocorrência de alterações em uma tabela específica, uma técnica de programação útil é colocar o `NOTIFY` em um gatilho de declaração que seja acionado por atualizações de tabela. Dessa forma, a notificação acontece automaticamente quando a tabela é alterada, e o programador da aplicação não pode esquecer acidentalmente de fazer isso.

`NOTIFY` interage com transações SQL de algumas maneiras importantes. Primeiramente, se um `NOTIFY` for executado dentro de uma transação, os eventos de notificação não serão entregues até que a transação seja comprometida. Isso é apropriado, pois, se a transação for abortada, todos os comandos dentro dela não terão efeito, incluindo `NOTIFY`. Mas pode ser desconcertante se alguém espera que os eventos de notificação sejam entregues imediatamente. Em segundo lugar, se uma sessão de escuta recebe um sinal de notificação enquanto está dentro de uma transação, o evento de notificação não será entregue ao seu cliente conectado até logo após a transação ser concluída (ou comprometida ou abortada). Novamente, o raciocínio é que, se uma notificação fosse entregue dentro de uma transação que foi posteriormente abortada, alguém gostaria de que a notificação fosse desfeita de alguma forma — mas o servidor não pode “retirar” uma notificação uma vez que a tenha enviado ao cliente. Portanto, os eventos de notificação são entregues apenas entre transações. O resultado disso é que as aplicações que usam `NOTIFY` para sinalização em tempo real devem tentar manter suas transações curtas.

Se o mesmo nome de canal for sinalizado várias vezes com strings de carga idênticas dentro da mesma transação, apenas uma instância do evento de notificação será entregue aos ouvintes. Por outro lado, as notificações com strings de carga distintas serão sempre entregues como notificações distintas. Da mesma forma, as notificações de diferentes transações nunca serão dobradas em uma única notificação. Exceto pelo descarte de instâncias subsequentes de notificações duplicadas, `NOTIFY` garante que as notificações da mesma transação sejam entregues na ordem em que foram enviadas. Também é garantido que as mensagens de diferentes transações sejam entregues na ordem em que as transações foram comprometidas.

É comum que um cliente que executa `NOTIFY` esteja ouvindo o mesmo canal de notificação. Nesse caso, ele receberá um evento de notificação, assim como todas as outras sessões de escuta. Dependendo da lógica do aplicativo, isso pode resultar em trabalho inútil, por exemplo, ler uma tabela de banco de dados para encontrar as mesmas atualizações que aquela sessão acabou de escrever. É possível evitar esse trabalho extra ao notar se o PID do processo do servidor da sessão notificadora (fornecido na mensagem do evento de notificação) é o mesmo que o PID da própria sessão (disponível em libpq). Quando eles são os mesmos, o evento de notificação é o próprio trabalho que retorna, e pode ser ignorado.

## Parâmetros

*`channel`*: Nome do canal de notificação a ser sinalizado (qualquer identificador).

*`payload`*: A string “carga” a ser comunicada juntamente com a notificação. Deve ser especificada como uma literal de string simples. Na configuração padrão, deve ser mais curta que 8000 bytes. (Se dados binários ou grandes quantidades de informações precisam ser comunicadas, é melhor colocá-los em uma tabela de banco de dados e enviar a chave do registro.)

## Notas

Existe uma fila que contém notificações que foram enviadas, mas ainda não processadas por todas as sessões de escuta. Se essa fila ficar cheia, as transações que chamam `NOTIFY` falharão no commit. A fila é bastante grande (8 GB em uma instalação padrão) e deve ser dimensionada de forma suficiente para quase todos os casos de uso. No entanto, não é possível realizar uma limpeza se uma sessão executar `LISTEN` e, em seguida, entrar em uma transação por um período muito longo. Uma vez que a fila esteja meio cheia, você verá avisos no arquivo de log apontando para a sessão que está impedindo a limpeza. Neste caso, você deve garantir que essa sessão termine sua transação atual para que a limpeza possa prosseguir.

A função `pg_notification_queue_usage` retorna a fração da fila que está atualmente ocupada por notificações pendentes. Consulte [Seção 9.27](functions-info.md) para obter mais informações.

Uma transação que executou `NOTIFY` não pode ser preparada para um compromisso de duas fases.

### pg_notify

Para enviar uma notificação, você também pode usar a função `pg_notify(text, text)`. A função recebe o nome do canal como o primeiro argumento e o payload como o segundo. A função é muito mais fácil de usar do que o comando `NOTIFY` se você precisar trabalhar com nomes de canal e payloads não constantes.

## Exemplos

Configure e execute uma sequência de escuta/notificação a partir do psql:

```
LISTEN virtual;
NOTIFY virtual;
Asynchronous notification "virtual" received from server process with PID 8448.
NOTIFY virtual, 'This is the payload';
Asynchronous notification "virtual" with payload "This is the payload" received from server process with PID 8448.

LISTEN foo;
SELECT pg_notify('fo' || 'o', 'pay' || 'load');
Asynchronous notification "foo" with payload "payload" received from server process with PID 14728.
```

## Compatibilidade

Não há nenhuma declaração `NOTIFY` no padrão SQL.

## Veja também

[ESCOLHER](sql-listen.md "LISTEN"), [DESESCOLHER](sql-unlisten.md "UNLISTEN"), [max_notify_queue_pages](runtime-config-resource.md#GUC-MAX-NOTIFY-QUEUE-PAGES)