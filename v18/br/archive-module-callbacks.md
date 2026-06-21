## 49.2. Chamadas de Retorno de Arquivo do Módulo [#](#ARCHIVE-MODULE-CALLBACKS)

* [49.2.1. Chamada de inicialização][(archive-module-callbacks.md#ARCHIVE-MODULE-STARTUP)]
* [49.2.2. Verificação de chamada][(archive-module-callbacks.md#ARCHIVE-MODULE-CHECK)]
* [49.2.3. Arquivo de chamada][(archive-module-callbacks.md#ARCHIVE-MODULE-ARCHIVE)]
* [49.2.4. Desativação de chamada][(archive-module-callbacks.md#ARCHIVE-MODULE-SHUTDOWN)]

Os callbacks do arquivo definem o comportamento real de arquivamento do módulo. O servidor os chamará conforme necessário para processar cada arquivo WAL individual.

### 49.2.1. Início de chamada Callback [#](#ARCHIVE-MODULE-STARTUP)

O callback `startup_cb` é chamado logo após o módulo ser carregado. Esse callback pode ser usado para realizar qualquer inicialização adicional necessária. Se o módulo de arquivo tiver algum estado, ele pode usar `state->private_data` para armazená-lo.

```
typedef void (*ArchiveStartupCB) (ArchiveModuleState *state);
```

### 49.2.2. Verificar o Callback [#](#ARCHIVE-MODULE-CHECK)

O callback `check_configured_cb` é chamado para determinar se o módulo está totalmente configurado e pronto para aceitar arquivos WAL (por exemplo, seus parâmetros de configuração estão definidos com valores válidos). Se não for definido nenhum `check_configured_cb`, o servidor sempre assume que o módulo está configurado.

```
typedef bool (*ArchiveCheckConfiguredCB) (ArchiveModuleState *state);
```

Se `true` for retornado, o servidor procederá com o arquivamento do arquivo, chamando o callback `archive_file_cb`. Se `false` for retornado, o arquivamento não prosseguirá, e o arquivador emitirá a seguinte mensagem no log do servidor:

```
WARNING:  archive_mode enabled, yet archiving is not configured
```

No último caso, o servidor chamará periodicamente essa função, e o arquivamento prosseguirá apenas quando ela retornar `true`.

### Nota

Ao retornar `false`, pode ser útil anexar algumas informações adicionais à mensagem de aviso genérica. Para fazer isso, forneça uma mensagem ao macro `arch_module_check_errdetail` antes de retornar `false`. Assim como `errdetail()`, este macro aceita uma string de formato seguida por uma lista opcional de argumentos. A string resultante será emitida como a linha `DETAIL` da mensagem de aviso.

### 49.2.3. Retorno de chamada de arquivo [#](#ARCHIVE-MODULE-ARCHIVE)

O callback `archive_file_cb` é chamado para arquivar um único arquivo WAL.

```
typedef bool (*ArchiveFileCB) (ArchiveModuleState *state, const char *file, const char *path);
```

Se `true` for retornado, o servidor prossegue como se o arquivo tivesse sido arquivado com sucesso, o que pode incluir reciclagem ou remoção do arquivo WAL original. Se `false` for retornado ou um erro for lançado, o servidor manterá o arquivo WAL original e tentará arquivar novamente mais tarde. *`file`* conterá apenas o nome do arquivo do arquivo WAL a ser arquivado, enquanto *`path`* contém o caminho completo do arquivo WAL (incluindo o nome do arquivo).

### Nota

O callback `archive_file_cb` é chamado em um contexto de memória de curta duração que será redefinido entre as chamadas. Se você precisar de armazenamento de maior duração, crie um contexto de memória no callback `startup_cb` do módulo.

### 49.2.4. Chamada de retorno de desligamento [#](#ARCHIVE-MODULE-SHUTDOWN)

O callback `shutdown_cb` é chamado quando o processo de arquivamento sai (por exemplo, após um erro) ou quando o valor de [archive_library](runtime-config-wal.md#GUC-ARCHIVE-LIBRARY) muda. Se não for definido nenhum `shutdown_cb`, não será realizada nenhuma ação especial nessas situações. Se o módulo de arquivamento tiver algum estado, esse callback deve liberá-lo para evitar vazamentos.

```
typedef void (*ArchiveShutdownCB) (ArchiveModuleState *state);
```
