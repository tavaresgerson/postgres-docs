## 70.2. Objeto do arquivo de manifestação de backup [#](#BACKUP-MANIFEST-FILES)

O objeto que descreve um único arquivo contém uma chave `Path` ou uma chave `Encoded-Path`. Normalmente, a chave `Path` estará presente. O valor associado da string é o caminho do arquivo em relação à raiz do diretório de backup. Arquivos localizados em um espaço de tabela definido pelo usuário terão caminhos cujos dois primeiros componentes são `pg_tblspc` e o OID do espaço de tabela. Se o caminho não for uma string que é legal em UTF-8, ou se o usuário solicitar que caminhos codificados sejam usados para todos os arquivos, então a chave `Encoded-Path` estará presente em vez disso. Isso armazena os mesmos dados, mas é codificado como uma string de dígitos hexadecimais. Cada par de dígitos hexadecimais na string representa um único octeto.

As duas chaves a seguir estão sempre presentes:

`Size`: O tamanho esperado deste arquivo, como um número inteiro.

`Last-Modified`: O horário da última modificação do arquivo conforme relatado pelo servidor no momento do backup. Ao contrário dos outros campos armazenados no backup, este campo não é utilizado pelo [pg_verifybackup][(app-pgverifybackup.md "pg_verifybackup")]. É incluído apenas para fins informativos.

Se o backup foi feito com verificação de checksums de arquivo habilitada, as seguintes chaves estarão presentes:

`Checksum-Algorithm`: O algoritmo de verificação de checksum usado para calcular um checksum para este arquivo. Atualmente, isso será o mesmo para todos os arquivos no manifesto de backup, mas isso pode mudar em versões futuras. Atualmente, os algoritmos de verificação de checksum suportados são `CRC32C`, `SHA224`, `SHA256`, `SHA384` e `SHA512`.

`Checksum`: O checksum calculado para este arquivo, armazenado como uma série de caracteres hexadecimais, dois para cada byte do checksum.