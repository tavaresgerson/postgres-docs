## 50.2. Funções de Inicialização [#](#OAUTH-VALIDATOR-INIT)

Os módulos validadores OAuth são carregados dinamicamente a partir das bibliotecas compartilhadas listadas em [oauth_validator_libraries][(runtime-config-connection.md#GUC-OAUTH-VALIDATOR-LIBRARIES)]. Os módulos são carregados sob demanda quando solicitados a partir de um login em andamento. O caminho normal de busca de biblioteca é usado para localizar a biblioteca. Para fornecer os callbacks do validador e indicar que a biblioteca é um módulo validador OAuth, deve ser fornecida uma função chamada `_PG_oauth_validator_module_init`. O valor de retorno da função deve ser um ponteiro para uma estrutura do tipo `OAuthValidatorCallbacks`, que contém um número mágico e ponteiros para as funções de validação de token do módulo. O ponteiro retornado deve ser de vida útil do servidor, que é tipicamente alcançada definindo-o como uma variável `static const` no escopo global.

```
typedef struct OAuthValidatorCallbacks
{
    uint32        magic;            /* must be set to PG_OAUTH_VALIDATOR_MAGIC */

    ValidatorStartupCB startup_cb;
    ValidatorShutdownCB shutdown_cb;
    ValidatorValidateCB validate_cb;
} OAuthValidatorCallbacks;

typedef const OAuthValidatorCallbacks *(*OAuthValidatorModuleInit) (void);
```

Apenas o callback `validate_cb` é necessário, os outros são opcionais.