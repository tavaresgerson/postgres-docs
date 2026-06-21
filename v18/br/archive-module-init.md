## 49.1. Funções de Inicialização [#](#ARCHIVE-MODULE-INIT)

Uma biblioteca de arquivos é carregada ao carregar dinamicamente uma biblioteca compartilhada com o nome da biblioteca [archive_library][(runtime-config-wal.md#GUC-ARCHIVE-LIBRARY)] como o nome da base da biblioteca. O caminho normal de busca da biblioteca é usado para localizar a biblioteca. Para fornecer os callbacks do módulo de arquivo necessários e indicar que a biblioteca é realmente um módulo de arquivo, ela precisa fornecer uma função chamada `_PG_archive_module_init`. O resultado da função deve ser um ponteiro para uma estrutura do tipo `ArchiveModuleCallbacks`, que contém tudo o que o código do núcleo precisa saber para fazer uso do módulo de arquivo. O valor de retorno precisa ser de vida útil do servidor, que é tipicamente alcançada definindo-o como uma variável `static const` no escopo global.

```
typedef struct ArchiveModuleCallbacks
{
    ArchiveStartupCB startup_cb;
    ArchiveCheckConfiguredCB check_configured_cb;
    ArchiveFileCB archive_file_cb;
    ArchiveShutdownCB shutdown_cb;
} ArchiveModuleCallbacks;
typedef const ArchiveModuleCallbacks *(*ArchiveModuleInit) (void);
```

Apenas o callback `archive_file_cb` é necessário. Os outros são opcionais.