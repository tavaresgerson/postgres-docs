## ESCUTA

ESCUTA — ouça uma notificação

## Sinopse

```
LISTEN channel
```

## Descrição

`LISTEN` registra a sessão atual como um ouvinte no canal de notificação denominado *`channel`*. Se a sessão atual já estiver registrada como ouvinte para este canal de notificação, nada é feito.

Sempre que o comando `NOTIFY channel` é invocado, seja por esta sessão ou por outra conectada à mesma base de dados, todas as sessões que estão atualmente ouvindo nesse canal de notificação são notificadas, e cada uma, por sua vez, notificará sua aplicação de cliente conectada.

Uma sessão pode ser desregistrada para um determinado canal de notificação com o comando `UNLISTEN`. Os registros de escuta de uma sessão são automaticamente apagados quando a sessão termina.

O método que uma aplicação cliente deve usar para detectar eventos de notificação depende da interface de programação de aplicativos do PostgreSQL que ela utiliza. Com a biblioteca libpq, a aplicação emite `LISTEN` como um comando SQL comum, e então deve chamar periodicamente a função `PQnotifies` para descobrir se algum evento de notificação foi recebido. Outras interfaces, como libpgtcl, fornecem métodos de nível superior para lidar com eventos de notificação; de fato, com libpgtcl, o programador da aplicação nem mesmo deve emitir `LISTEN` ou `UNLISTEN` diretamente. Consulte a documentação da interface que você está usando para obter mais detalhes.

## Parâmetros

*`channel`*: Nome de um canal de notificação (qualquer identificador).

## Notas

`LISTEN` entra em vigor no momento do commit da transação. Se `LISTEN` ou `UNLISTEN` for executado dentro de uma transação que posteriormente seja revertida, o conjunto de canais de notificação que estão sendo ouvidos não será alterado.

Uma transação que foi executada com `LISTEN` não pode ser preparada para um compromisso de duas fases.

Há uma condição de corrida ao configurar a primeira sessão de escuta: se as transações com commit simultâneo estão enviando eventos de notificação, exatamente quais desses serão recebidos pela nova sessão de escuta? A resposta é que a sessão receberá todos os eventos que forem comprometidos após um instante durante a etapa de commit da transação. Mas isso é um pouco mais tarde do que qualquer estado do banco de dados que a transação poderia ter observado em consultas. Isso leva à seguinte regra para o uso do `LISTEN`: primeiro execute (e commit!) esse comando, em seguida, em uma nova transação, inspecione o estado do banco de dados conforme necessário pela lógica da aplicação, e então confie nas notificações para descobrir sobre as mudanças subsequentes no estado do banco de dados. As primeiras notificações recebidas podem se referir a atualizações já observadas na inspeção inicial do banco de dados, mas isso geralmente é inofensivo.

[NOTIFICAR](sql-notify.md "NOTIFY") contém uma discussão mais extensa sobre o uso de `LISTEN` e `NOTIFY`.

## Exemplos

Configure e execute uma sequência de escuta/notificação a partir do psql:

```
LISTEN virtual;
NOTIFY virtual;
Asynchronous notification "virtual" received from server process with PID 8448.
```

## Compatibilidade

Não há nenhuma declaração `LISTEN` no padrão SQL.

## Veja também

[NOTIFICAR][(sql-notify.md "NOTIFY"), [DESCONECTAR][(sql-unlisten.md "UNLISTEN"), [max_notify_queue_pages][(runtime-config-resource.md#GUC-MAX-NOTIFY-QUEUE-PAGES)