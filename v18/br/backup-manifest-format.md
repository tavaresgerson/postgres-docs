## Capítulo 70. Formato de manifesto de backup

**Índice**

* [70.1. Objeto de nível superior do manifesto de backup](backup-manifest-toplevel.md)
* [70.2. Objeto de arquivo de manifesto de backup](backup-manifest-files.md)
* [70.3. Objeto de intervalo WAL do manifesto de backup](backup-manifest-wal-ranges.md)

O manifesto de backup gerado por [pg_basebackup][(app-pgbasebackup.md "pg_basebackup")] é destinado principalmente a permitir que o backup seja verificado usando [pg_verifybackup][(app-pgverifybackup.md "pg_verifybackup")]. No entanto, também é possível que outras ferramentas leiam o arquivo do manifesto de backup e usem as informações contidas nele para seus próprios propósitos. Para esse fim, este capítulo descreve o formato do arquivo do manifesto de backup.

Um manifesto de backup é um documento JSON codificado como UTF-8. (Embora, em geral, os documentos JSON sejam obrigados a serem Unicode, o PostgreSQL permite que os tipos de dados `json` e `jsonb` sejam usados com qualquer codificação de servidor compatível. Não há uma exceção semelhante para manifestos de backup.) O documento JSON é sempre um objeto; as chaves presentes neste objeto são descritas na próxima seção.