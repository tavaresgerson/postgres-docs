## Capítulo 49. Módulos de Arquivo

**Índice**

* [49.1. Funções de Inicialização](archive-module-init.md)
* [49.2. Retornos de Chamada do Módulo de Arquivo](archive-module-callbacks.md)

+ [49.2.1. Chamada de inicialização](archive-module-callbacks.md#ARCHIVE-MODULE-STARTUP)
+ [49.2.2. Verificação de chamada](archive-module-callbacks.md#ARCHIVE-MODULE-CHECK)
+ [49.2.3. Arquivo de chamada](archive-module-callbacks.md#ARCHIVE-MODULE-ARCHIVE)
+ [49.2.4. Desativação de chamada](archive-module-callbacks.md#ARCHIVE-MODULE-SHUTDOWN)

O PostgreSQL oferece uma infraestrutura para criar módulos personalizados para arquivamento contínuo (consulte [Seção 25.3](continuous-archiving.md)). Embora o arquivamento via comando de shell (ou seja, [comando_de_arquivamento](runtime-config-wal.md#GUC-ARCHIVE-COMMAND)) seja muito mais simples, um módulo de arquivo personalizado geralmente será consideravelmente mais robusto e eficiente.

Quando uma [archive_library](runtime-config-wal.md#GUC-ARCHIVE-LIBRARY) personalizada é configurada, o PostgreSQL enviará os arquivos WAL completos para o módulo, e o servidor evitará reciclar ou remover esses arquivos WAL até que o módulo indique que os arquivos foram arquivados com sucesso. Em última análise, cabe ao módulo decidir o que fazer com cada arquivo WAL, mas muitas recomendações estão listadas em [Seção 25.3.1](continuous-archiving.md#BACKUP-ARCHIVING-WAL).

Os módulos de arquivamento devem, pelo menos, consistir em uma função de inicialização (ver [Seção 49.1](archive-module-init.md)) e os callbacks necessários (ver [Seção 49.2](archive-module-callbacks.md)). No entanto, os módulos de arquivamento também são permitidos para fazer muito mais (por exemplo, declarar GUCs e registrar trabalhadores de fundo).

O módulo `contrib/basic_archive` contém um exemplo funcional, que demonstra algumas técnicas úteis.