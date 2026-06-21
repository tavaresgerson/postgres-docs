## 50.3. Retornos de chamada do Validador OAuth [#](#OAUTH-VALIDATOR-CALLBACKS)

* [50.3.1. Chamada de inicialização](oauth-validator-callbacks.md#OAUTH-VALIDATOR-CALLBACK-STARTUP)
* [50.3.2. Validação de chamada de retorno](oauth-validator-callbacks.md#OAUTH-VALIDATOR-CALLBACK-VALIDATE)
* [50.3.3. Chamada de desligamento](oauth-validator-callbacks.md#OAUTH-VALIDATOR-CALLBACK-SHUTDOWN)

Os módulos de validação OAuth implementam sua funcionalidade definindo um conjunto de callbacks. O servidor os chamará conforme necessário para processar o pedido de autenticação do usuário.

### 50.3.1. Início de chamada Callback [#](#OAUTH-VALIDATOR-CALLBACK-STARTUP)

O callback `startup_cb` é executado diretamente após a carga do módulo. Esse callback pode ser usado para configurar o estado local e realizar a inicialização adicional, se necessário. Se o módulo de validação tiver estado, ele pode usar `state->private_data` para armazená-lo.

```
typedef void (*ValidatorStartupCB) (ValidatorModuleState *state);
```

### 50.3.2. Validar Callback [#](#OAUTH-VALIDATOR-CALLBACK-VALIDATE)

O callback `validate_cb` é executado durante a troca OAuth quando um usuário tenta autenticar usando OAuth. Qualquer estado definido em chamadas anteriores estará disponível em `state->private_data`.

```
typedef bool (*ValidatorValidateCB) (const ValidatorModuleState *state,
                                     const char *token, const char *role,
                                     ValidatorModuleResult *result);
```

*`token`* conterá o token de portador para validação. O PostgreSQL garantiu que o token esteja bem formado sintaticamente, mas nenhuma outra validação foi realizada. *`role`* conterá o papel que o usuário solicitou para fazer login. O callback deve definir os parâmetros de saída na estrutura `result`, que é definida como abaixo:

```
typedef struct ValidatorModuleResult
{
    bool        authorized;
    char       *authn_id;
} ValidatorModuleResult;
```

A conexão só prosseguirá se o módulo definir `result->authorized` para `true`. Para autenticar o usuário, o nome do usuário autenticado (determinado usando o token) deve ser palloc'ado e retornado no campo `result->authn_id`. Alternativamente, `result->authn_id` pode ser definido como NULL se o token for válido, mas a identidade do usuário associada não puder ser determinada.

Um validador pode retornar `false` para sinalizar um erro interno, nesse caso, quaisquer parâmetros de resultado são ignorados e a conexão falha. Caso contrário, o validador deve retornar `true` para indicar que processou o token e tomou uma decisão de autorização.

O comportamento após o retorno de `validate_cb` depende da configuração específica do HBA. Normalmente, o nome de usuário `result->authn_id` deve corresponder exatamente ao papel pelo qual o usuário está fazendo login. (Esse comportamento pode ser modificado com um usermap.) Mas quando autenticando contra uma regra de HBA com `delegate_ident_mapping` ativada, o PostgreSQL não realizará nenhuma verificação no valor de `result->authn_id`; nesse caso, cabe ao validador garantir que o token tenha privilégios suficientes para o usuário fazer login sob o *`role`* indicado.

### 50.3.3. Chamada de Retorno de Fechamento [#](#OAUTH-VALIDATOR-CALLBACK-SHUTDOWN)

O callback `shutdown_cb` é executado quando o processo de backend associado à conexão é encerrado. Se o módulo de validação tiver algum estado alocado, esse callback deve liberá-lo para evitar vazamentos de recursos.

```
typedef void (*ValidatorShutdownCB) (ValidatorModuleState *state);
```
