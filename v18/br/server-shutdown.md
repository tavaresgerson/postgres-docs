## 18.5. Desligar o servidor [#](#SERVER-SHUTDOWN)

Existem várias maneiras de desligar o servidor de banco de dados. Sob o capô, todos eles se reduzem a enviar um sinal para o processo do supervisor `postgres`.

Se você está usando uma versão pré-embalada do PostgreSQL e usou suas disposições para iniciar o servidor, então você também deve usar suas disposições para parar o servidor. Consulte a documentação do nível do pacote para obter detalhes.

Ao gerenciar o servidor diretamente, você pode controlar o tipo de desligamento enviando diferentes sinais ao processo `postgres`:

SIGTERM: Este é o modo *Smart Shutdown*. Após receber o SIGTERM, o servidor não permite novas conexões, mas permite que as sessões existentes terminem seu trabalho normalmente. Ele é desligado apenas após todas as sessões terem terminado. Se o servidor estiver em recuperação quando uma parada inteligente for solicitada, a recuperação e a replicação em streaming serão interrompidas apenas após todas as sessões regulares terem terminado.

SIGINT: Este é o modo *Fast Shutdown*. O servidor não permite novas conexões e envia SIGTERM a todos os processos do servidor existentes, o que fará com que abordem suas transações atuais e saiam imediatamente. Em seguida, ele espera que todos os processos do servidor saiam e, finalmente, o servidor é desligado.

SIGQUIT: Este é o modo de *Fechamento Imediato*. O servidor enviará SIGQUIT para todos os processos filhos e aguardará que eles sejam encerrados. Se algum não for encerrado dentro de 5 segundos, ele será enviado SIGKILL. O processo do servidor supervisor sai assim que todos os processos filhos tiverem sido encerrados, sem realizar o processamento normal de fechamento do banco de dados. Isso levará à recuperação (retransmitindo o log WAL) na próxima inicialização. Isso é recomendado apenas em situações de emergência.

O programa [pg_ctl](app-pg-ctl.md "pg_ctl") oferece uma interface conveniente para enviar esses sinais para desligar o servidor. Alternativamente, você pode enviar o sinal diretamente usando `kill` em sistemas que não são do Windows. O PID do processo `postgres` pode ser encontrado usando o programa `ps`, ou a partir do arquivo `postmaster.pid` no diretório de dados. Por exemplo, para fazer uma parada rápida:

```
$ kill -INT `head -1 /usr/local/pgsql/data/postmaster.pid`
```

### Importante

É melhor não usar SIGKILL para desligar o servidor. Isso impedirá o servidor de liberar memória compartilhada e semaforos. Além disso, o SIGKILL mata o processo `postgres` sem permitir que ele retransmita o sinal para seus subprocessos, portanto, pode ser necessário matar os subprocessos individuais manualmente também.

Para encerrar uma sessão individual enquanto permite que outras sessões continuem, use `pg_terminate_backend()` (consulte [Tabela 9.96][(functions-admin.md#FUNCTIONS-ADMIN-SIGNAL-TABLE "Table 9.96. Server Signaling Functions")]) ou envie um sinal SIGTERM ao processo filho associado à sessão.