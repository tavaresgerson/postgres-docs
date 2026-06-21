## pg_recvlogical

pg_recvlogical — controle de fluxos de decodificação lógica do PostgreSQL

## Sinopse

`pg_recvlogical` [*`option`*...]

## Descrição

`pg_recvlogical` controla os slots de replicação de decodificação lógica e transmite dados a partir desses slots de replicação.

Ele cria uma conexão em modo de replicação, portanto, está sujeito às mesmas restrições que [pg_receivewal][(app-pgreceivewal.md "pg_receivewal")], além das restrições para replicação lógica (consulte [Capítulo 47][(logicaldecoding.md "Chapter 47. Logical Decoding")]).

`pg_recvlogical` não tem equivalente às funções peek e get dos modos de decodificação lógica da interface SQL. Envia confirmações de replay para dados que são recebidos de forma preguiçosa e em uma saída limpa. Para examinar dados pendentes em um slot sem consumi-los, use `pg_logical_slot_peek_changes`(functions-admin.md#FUNCTIONS-REPLICATION "9.28.6. Replication Management Functions").

Na ausência de erros fatais, o pg_recvlogical será executado até ser encerrado pelo sinal SIGINT (**Controle** + **C**) ou SIGTERM.

Quando o pg_recvlogical recebe um sinal SIGHUP, ele fecha o arquivo de saída atual e abre um novo usando o nome de arquivo especificado pela opção `--file`. Isso nos permite rotar o arquivo de saída, primeiro renomeando o arquivo atual e, em seguida, enviando um sinal SIGHUP para o pg_recvlogical.

## Opções

Pelo menos uma das seguintes opções deve ser especificada para selecionar uma ação:

`--create-slot`: Crie um novo slot de replicação lógica com o nome especificado por `--slot`, usando o plugin de saída especificado por `--plugin`, para o banco de dados especificado por `--dbname`.

O `--slot` e o `--dbname` são necessários para essa ação.

As opções `--enable-two-phase` e `--enable-failover` podem ser especificadas com `--create-slot`.

`--drop-slot`: Descarte o slot de replicação com o nome especificado por `--slot`, e então saia.

O `--slot` é necessário para essa ação.

`--start`: Começar a transmitir alterações a partir do slot de replicação lógica especificado por `--slot`, continuando até ser interrompido por um sinal. Se o fluxo de alterações do lado do servidor terminar com o desligamento ou desconexão do servidor, tente novamente em um loop, a menos que `--no-loop` seja especificado.

Os `--slot` e `--dbname`, `--file` são necessários para essa ação.

O formato do fluxo é determinado pelo plugin de saída especificado quando o slot foi criado.

A conexão deve ser com o mesmo banco de dados utilizado para criar o slot.

`--create-slot` e `--start` podem ser especificados juntos. `--drop-slot` não pode ser combinado com outra ação.

As opções de linha de comando a seguir controlam a localização e o formato do resultado e o comportamento de replicação:

`-E lsn` `--endpos=lsn`: No modo `--start`, pare automaticamente a replicação e saia com o status de saída normal 0 quando o recebimento atingir o LSN especificado. Se especificado quando não estiver no modo `--start`, um erro é exibido.

Se houver um registro com LSN exatamente igual a *`lsn`*, o registro será emitido.

A opção `--endpos` não é consciente dos limites das transações e pode truncar a saída em meio a uma transação. Qualquer transação parcialmente emitida não será consumida e será reinterpretada novamente quando a posição for lida novamente. Mensagens individuais nunca são truncadas.

`--enable-failover`: Habilita o slot para ser sincronizado com os standbys. Esta opção só pode ser especificada com `--create-slot`.

`-f filename` `--file=filename`: Escreva os dados de transação recebidos e decodificados neste arquivo. Use `-` para stdout.

Este parâmetro é necessário para `--start`.

`-F interval_seconds` `--fsync-interval=interval_seconds`: Especifica quantas vezes o pg_recvlogical deve emitir chamadas `fsync()` para garantir que o arquivo de saída seja descarregado com segurança no disco.

O servidor ocasionalmente solicitará ao cliente que realize um esvaziamento e informe a posição de esvaziamento ao servidor. Esse ajuste é adicional, para realizar esvaziamentos com mais frequência.

Especificar um intervalo de `0` desabilita a emissão de chamadas de `fsync()` completamente, ainda relatando o progresso ao servidor. Nesse caso, os dados poderiam ser perdidos em caso de falha.

`-I lsn` `--startpos=lsn`: No modo `--start`, inicie a replicação a partir do LSN especificado. Para obter detalhes sobre o efeito disso, consulte a documentação em [Capítulo 47](logicaldecoding.md "Chapter 47. Logical Decoding") e [Seção 54.4](protocol-replication.md "54.4. Streaming Replication Protocol"). Ignorado em outros modos.

`--if-not-exists`: Não erre quando o `--create-slot` é especificado e um slot com o nome especificado já existe.

`-n` `--no-loop`: Quando a conexão com o servidor for perdida, não tente novamente em um loop, apenas saia.

`-o name[=value]` `--option=name[=value]`: Passe a opção *`name`* para o plugin de saída com, se especificado, o valor da opção *`value`*. As opções existentes e seus efeitos dependem do plugin de saída utilizado.

`-P plugin` `--plugin=plugin`: Ao criar um slot, use o plugin de saída de decodificação lógica especificado. Veja [Capítulo 47](logicaldecoding.md "Chapter 47. Logical Decoding"). Esta opção não tem efeito se o slot já existir.

`-s interval_seconds` `--status-interval=interval_seconds`: Esta opção tem o mesmo efeito que a opção do mesmo nome em [pg_receivewal](app-pgreceivewal.md "pg_receivewal"). Veja a descrição lá.

`-S slot_name` `--slot=slot_name`: No modo `--start`, use o slot de replicação lógica existente com o nome *`slot_name`*. No modo `--create-slot`, crie o slot com este nome. No modo `--drop-slot`, exclua o slot com este nome.

Este parâmetro é necessário para qualquer uma das ações.

`-t` `--enable-two-phase` `--two-phase` (desatualizado): Habilita a decodificação de transações preparadas. Esta opção só pode ser especificada com `--create-slot`.

`-v` `--verbose`: Habilita o modo verbose.

As opções de linha de comando a seguir controlam os parâmetros de conexão do banco de dados.

`-d dbname` `--dbname=dbname`: O banco de dados a ser conectado. Veja a descrição das ações para entender o que isso significa em detalhes. O *`dbname`* pode ser uma [string de conexão][(libpq-connect.md#LIBPQ-CONNSTRING "32.1.1. Connection Strings")]. Se assim for, os parâmetros da string de conexão substituirão quaisquer opções de linha de comando conflitantes.

Este parâmetro é necessário para `--create-slot` e `--start`.

`-h hostname-or-ip` `--host=hostname-or-ip`: Especifica o nome do host da máquina na qual o servidor está sendo executado. Se o valor começar com uma barra, ele é usado como o diretório para o socket de domínio Unix. O padrão é tomado da variável de ambiente `PGHOST`, se definida, caso contrário, uma conexão de socket de domínio Unix é tentada.

`-p port` `--port=port`: Especifica a porta TCP ou a extensão de arquivo de soquete de domínio Unix local em que o servidor está ouvindo conexões. Tem como padrão a variável de ambiente `PGPORT`, se definida, ou um padrão incorporado.

`-U user` `--username=user`: Nome do usuário para se conectar como. Por padrão, é o nome do usuário do sistema operacional atual.

`-w` `--no-password`: Nunca emita um prompt de senha. Se o servidor exigir autenticação por senha e uma senha não estiver disponível por outros meios, como um arquivo `.pgpass`, a tentativa de conexão falhará. Esta opção pode ser útil em trabalhos em lote e scripts onde nenhum usuário está presente para inserir uma senha.

`-W` `--password`: Força o pg_recvlogical a solicitar uma senha antes de se conectar a um banco de dados.

Essa opção nunca é essencial, pois o pg_recvlogical solicitará automaticamente uma senha se o servidor exigir autenticação por senha. No entanto, o pg_recvlogical desperdiçará uma tentativa de conexão descobrindo que o servidor deseja uma senha. Em alguns casos, vale a pena digitar `-W` para evitar a tentativa extra de conexão.

As seguintes opções adicionais estão disponíveis:

`-V` `--version`: Imprima a versão do pg_recvlogical e saia.

`-?` `--help`: Mostrar ajuda sobre os argumentos da linha de comando do comando pg_recvlogical e sair.

## Status de saída

pg_recvlogical sairá com status 0 quando encerrado pelo sinal SIGINT ou SIGTERM. (Essa é a maneira normal de encerrá-lo. Portanto, não é um erro.) Para erros fatais ou outros sinais, o status de saída será diferente de zero.

## Meio Ambiente

Esse utilitário, como a maioria dos outros utilitários do PostgreSQL, utiliza as variáveis de ambiente suportadas pelo libpq (consulte a Seção 32.15 [(libpq-envars.md "32.15. Environment Variables")]).

A variável de ambiente `PG_COLOR` especifica se a cor deve ser usada nas mensagens de diagnóstico. Os valores possíveis são `always`, `auto` e `never`.

## Notas

pg_recvlogical preservará as permissões de grupo nos arquivos WAL recebidos se as permissões de grupo estiverem habilitadas no clúster de origem.

## Exemplos

Veja [Seção 47.1][(logicaldecoding-example.md "47.1. Logical Decoding Examples")] para um exemplo.

## Veja também

[pg_receivewal](app-pgreceivewal.md "pg_receivewal")
