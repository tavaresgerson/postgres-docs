## 64.2. Geradores de Recursos WAL personalizados [#](#CUSTOM-RMGR)

Esta seção explica a interface entre o sistema principal do PostgreSQL e os gestores de recursos WAL personalizados, que permitem que as extensões se integrem diretamente com o [WAL][(wal.md "Chapter 28. Reliability and the Write-Ahead Log")].

Uma extensão, especialmente um [Método de Acesso a Tabela][(tableam.md "Chapter 62. Table Access Method Interface Definition")] ou [Método de Acesso a Índice][(indexam.md "Chapter 63. Index Access Method Interface Definition")], pode precisar usar o WAL para recuperação, replicação e/ou [Decodificação Lógica][(logicaldecoding.md "Chapter 47. Logical Decoding")].

Para criar um novo gerenciador de recursos personalizado WAL, primeiro defina uma estrutura `RmgrData` com implementações para os métodos do gerenciador de recursos. Consulte `src/backend/access/transam/README` e `src/include/access/xlog_internal.h` na fonte do PostgreSQL.

```
/*
 * Method table for resource managers.
 *
 * This struct must be kept in sync with the PG_RMGR definition in
 * rmgr.c.
 *
 * rm_identify must return a name for the record based on xl_info (without
 * reference to the rmid). For example, XLOG_BTREE_VACUUM would be named
 * "VACUUM". rm_desc can then be called to obtain additional detail for the
 * record, if available (e.g. the last block).
 *
 * rm_mask takes as input a page modified by the resource manager and masks
 * out bits that shouldn't be flagged by wal_consistency_checking.
 *
 * RmgrTable[] is indexed by RmgrId values (see rmgrlist.h). If rm_name is
 * NULL, the corresponding RmgrTable entry is considered invalid.
 */
typedef struct RmgrData
{
    const char *rm_name;
    void        (*rm_redo) (XLogReaderState *record);
    void        (*rm_desc) (StringInfo buf, XLogReaderState *record);
    const char *(*rm_identify) (uint8 info);
    void        (*rm_startup) (void);
    void        (*rm_cleanup) (void);
    void        (*rm_mask) (char *pagedata, BlockNumber blkno);
    void        (*rm_decode) (struct LogicalDecodingContext *ctx,
                              struct XLogRecordBuffer *buf);
} RmgrData;
```

O módulo `src/test/modules/test_custom_rmgrs` contém um exemplo funcional, que demonstra o uso de gestores de recursos WAL personalizados.

Em seguida, registre seu novo gerente de recursos.

```
/*
 * Register a new custom WAL resource manager.
 *
 * Resource manager IDs must be globally unique across all extensions. Refer
 * to https://wiki.postgresql.org/wiki/CustomWALResourceManagers to reserve a
 * unique RmgrId for your extension, to avoid conflicts with other extension
 * developers. During development, use RM_EXPERIMENTAL_ID to avoid needlessly
 * reserving a new ID.
 */
extern void RegisterCustomRmgr(RmgrId rmid, const RmgrData *rmgr);
```

`RegisterCustomRmgr` deve ser chamado a partir da função [_PG_init](xfunc-c.md#XFUNC-C-DYNLOAD "36.10.1. Dynamic Loading") do módulo de extensão. Ao desenvolver uma nova extensão, use `RM_EXPERIMENTAL_ID` para *`rmid`*. Quando estiver pronto para liberar a extensão para os usuários, reserve um novo ID de gerenciador de recursos na página [Gerenciador de Recursos WAL Personalizado](https://wiki.postgresql.org/wiki/CustomWALResourceManagers).

Coloque o módulo de extensão que implementa o gerenciador de recursos personalizado em [shared_preload_libraries][(runtime-config-client.md#GUC-SHARED-PRELOAD-LIBRARIES)] para que ele seja carregado cedo durante o início do PostgreSQL.

### Nota

A extensão deve permanecer em `shared_preload_libraries` enquanto houver quaisquer registros personalizados do WAL no sistema. Caso contrário, o PostgreSQL não poderá aplicar ou decodificar os registros personalizados do WAL, o que pode impedir o início do servidor.