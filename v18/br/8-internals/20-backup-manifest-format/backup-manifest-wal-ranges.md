## 70.3. Objeto de intervalo de mantimento WAL [#](#BACKUP-MANIFEST-WAL-RANGES)

O objeto que descreve uma faixa WAL sempre tem três chaves:

`Timeline`: O cronograma para este intervalo de registros WAL, como um número inteiro.

`Start-LSN`: O LSN pelo qual o replay deve começar no cronograma indicado para fazer uso deste backup. O LSN é armazenado no formato normalmente usado pelo PostgreSQL; ou seja, é uma string composta por duas strings de caracteres hexadecimais, cada uma com um comprimento entre 1 e 8, separadas por uma barra.

`End-LSN`: A LSN (Last Known Good State) mais antiga em que o replay no cronograma indicado pode terminar ao fazer uso deste backup. Isso é armazenado no mesmo formato que `Start-LSN`.

Normalmente, haverá apenas uma única faixa WAL. No entanto, se um backup for feito de um standby que muda de linha de tempo durante o backup devido a uma promoção de linha de tempo de topo, é possível que existam várias faixas WAL, cada uma com um tempo de linha de tempo diferente. Nunca haverá várias faixas WAL presentes para o mesmo tempo de linha de tempo.