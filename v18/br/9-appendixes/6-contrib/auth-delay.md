## F.2. auth_delay — pausar após falha na autenticação [#](#AUTH-DELAY)

* [F.2.1. Parâmetros de Configuração](auth-delay.md#AUTH-DELAY-CONFIGURATION-PARAMETERS)
* [F.2.2. Autor](auth-delay.md#AUTH-DELAY-AUTHOR)

`auth_delay` faz com que o servidor faça uma pausa breve antes de relatar a falha de autenticação, para tornar mais difícil os ataques brutais às senhas do banco de dados. Note que ele não faz nada para prevenir ataques de negação de serviço e pode até exacerbar esses ataques, uma vez que os processos que estão esperando antes de relatar a falha de autenticação ainda consumirão faixas de conexão.

Para funcionar, este módulo deve ser carregado via [shared_preload_libraries](runtime-config-client.md#GUC-SHARED-PRELOAD-LIBRARIES) em `postgresql.conf`.

### F.2.1. Parâmetros de Configuração [#](#AUTH-DELAY-CONFIGURATION-PARAMETERS)

`auth_delay.milliseconds` (`integer`): O número de milissegundos para esperar antes de relatar uma falha de autenticação. O padrão é 0.

Esses parâmetros devem ser definidos em `postgresql.conf`. O uso típico pode ser:

```
# postgresql.conf
shared_preload_libraries = 'auth_delay'

auth_delay.milliseconds = '500'
```

### F.2.2. Autor [#](#AUTH-DELAY-AUTHOR)

KaiGai Kohei `<kaigai@ak.jp.nec.com>`