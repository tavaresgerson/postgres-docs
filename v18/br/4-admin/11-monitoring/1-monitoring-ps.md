## 27.1. Ferramentas Unix padrão [#](#MONITORING-PS)

Na maioria das plataformas Unix, o PostgreSQL modifica seu título de comando conforme relatado por `ps`, de modo que os processos individuais do servidor possam ser facilmente identificados. Um exemplo de exibição é

```
$ ps auxww | grep ^postgres
postgres  15551  0.0  0.1  57536  7132 pts/0    S    18:02   0:00 postgres -i
postgres  15554  0.0  0.0  57536  1184 ?        Ss   18:02   0:00 postgres: background writer
postgres  15555  0.0  0.0  57536   916 ?        Ss   18:02   0:00 postgres: checkpointer
postgres  15556  0.0  0.0  57536   916 ?        Ss   18:02   0:00 postgres: walwriter
postgres  15557  0.0  0.0  58504  2244 ?        Ss   18:02   0:00 postgres: autovacuum launcher
postgres  15582  0.0  0.0  58772  3080 ?        Ss   18:04   0:00 postgres: joe runbug 127.0.0.1 idle
postgres  15606  0.0  0.0  58772  3052 ?        Ss   18:07   0:00 postgres: tgl regression [local] SELECT waiting
postgres  15610  0.0  0.0  58772  3056 ?        Ss   18:07   0:00 postgres: tgl regression [local] idle in transaction
```

(A invocação apropriada de `ps` varia entre diferentes plataformas, assim como os detalhes do que é mostrado. Este exemplo é de um sistema recente de Linux.) O primeiro processo listado aqui é o processo do servidor primário. Os argumentos do comando mostrados para ele são os mesmos usados quando ele foi lançado. Os próximos quatro processos são processos de trabalhador de fundo automaticamente lançados pelo processo primário. (O processo "autovacuum launcher" não estará presente se você configurou o sistema para não executar o autovacuum.) Cada um dos processos restantes é um processo servidor que lida com uma conexão de cliente. Cada um desses processos define sua exibição na linha de comando na forma

```
postgres: user database host activity
```

Os itens usuário, banco de dados e (cliente) host permanecem os mesmos durante a vida da conexão do cliente, mas o indicador de atividade muda. A atividade pode ser `idle` (ou seja, esperando um comando do cliente), `idle in transaction` (esperando por um cliente dentro de um bloco `BEGIN`, ou um nome de tipo de comando, como `SELECT`. Além disso, `waiting` é anexado se o processo do servidor estiver atualmente esperando por um bloqueio mantido por outra sessão. No exemplo acima, podemos inferir que o processo 15606 está esperando que o processo 15610 complete sua transação e, assim, libere algum bloqueio. (O processo 15610 deve ser o bloqueante, porque não há outra sessão ativa. Em casos mais complicados, seria necessário examinar a visão do sistema [`pg_locks`](view-pg-locks.md) para determinar quem está bloqueando quem.)

Se [cluster_name](runtime-config-logging.md#GUC-CLUSTER-NAME) tiver sido configurado, o nome do cluster também será exibido na saída `ps`:

```
$ psql -c 'SHOW cluster_name'
 cluster_name
--------------
 server1
(1 row)

$ ps aux|grep server1
postgres   27093  0.0  0.0  30096  2752 ?        Ss   11:34   0:00 postgres: server1: background writer
...
```

Se você desativou [update_process_title](runtime-config-logging.md#GUC-UPDATE-PROCESS-TITLE), o indicador de atividade não é atualizado; o título do processo é definido apenas uma vez quando um novo processo é iniciado. Em algumas plataformas, isso economiza uma quantidade mensurável de sobrecarga por comando; em outras, é insignificante.

### DICA

O Solaris exige um manuseio especial. Você deve usar `/usr/ucb/ps`, em vez de `/bin/ps`. Além disso, você deve usar duas `w` flags, não apenas uma. Além disso, sua invocação original do comando `postgres` deve ter um display de status `ps` mais curto do que o fornecido por cada processo do servidor. Se você não fizer todas as três coisas, a saída `ps` para cada processo do servidor será a linha de comando original `postgres`.