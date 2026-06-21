## F.26. pgcrypto — funções criptográficas [#](#PGCRYPTO)

* [F.26.1. Funções de Hashamento Geral](pgcrypto.md#PGCRYPTO-GENERAL-HASHING-FUNCS)
* [F.26.2. Funções de Hash de Senhas](pgcrypto.md#PGCRYPTO-PASSWORD-HASHING-FUNCS)
* [F.26.3. Funções de Criptografia PGP](pgcrypto.md#PGCRYPTO-PGP-ENC-FUNCS)
* [F.26.4. Funções de Criptografia Raw](pgcrypto.md#PGCRYPTO-RAW-ENC-FUNCS)
* [F.26.5. Funções de Dados Aleatórios](pgcrypto.md#PGCRYPTO-RANDOM-DATA-FUNCS)
* [F.26.6. Funções de Suporte OpenSSL](pgcrypto.md#PGCRYPTO-OPENSSL-SUPPORT-FUNCS)
* [F.26.7. Parâmetros de Configuração](pgcrypto.md#PGCRYPTO-CONFIGURATION-PARAMETERS)
* [F.26.8. Notas](pgcrypto.md#PGCRYPTO-NOTES)
* [F.26.9. Autor](pgcrypto.md#PGCRYPTO-AUTHOR)

O módulo `pgcrypto` fornece funções criptográficas para o PostgreSQL.

Este módulo é considerado "confiável", ou seja, pode ser instalado por usuários não superusuários que possuem privilégio `CREATE` no banco de dados atual.

`pgcrypto` exige o OpenSSL e não será instalado se o suporte ao OpenSSL não foi selecionado quando o PostgreSQL foi construído.

### F.26.1. Funções de Hashamento Geral [#](#PGCRYPTO-GENERAL-HASHING-FUNCS)

#### F.26.1.1. `digest()` [#](#PGCRYPTO-GENERAL-HASHING-FUNCS-DIGEST)

```
digest(data text, type text) returns bytea
digest(data bytea, type text) returns bytea
```

Calcula um hash binário do dado *`data`*. *`type`* é o algoritmo a ser utilizado. Os algoritmos padrão são `md5`, `sha1`, `sha224`, `sha256`, `sha384` e `sha512`. Além disso, qualquer algoritmo de digest que o OpenSSL suporte é automaticamente escolhido.

Se você deseja o resumo como uma string hexadecimal, use `encode()` no resultado. Por exemplo:

```
CREATE OR REPLACE FUNCTION sha1(bytea) returns text AS $$
    SELECT encode(digest($1, 'sha1'), 'hex')
$$ LANGUAGE SQL STRICT IMMUTABLE;
```

#### F.26.1.2. `hmac()` [#](#PGCRYPTO-GENERAL-HASHING-FUNCS-HMAC)

```
hmac(data text, key text, type text) returns bytea
hmac(data bytea, key bytea, type text) returns bytea
```

Calcula o MAC hashado para *`data`* com a chave *`key`*. *`type`* é o mesmo que em `digest()`.

Isso é semelhante ao `digest()`, mas o hash só pode ser recalculado conhecendo a chave. Isso previne o cenário de alguém alterar os dados e também alterar o hash para corresponder.

Se a chave for maior que o tamanho do bloco de hash, ela será primeiramente hash e o resultado será usado como chave.

### F.26.2. Funções de hashing de senhas [#](#PGCRYPTO-PASSWORD-HASHING-FUNCS)

As funções `crypt()` e `gen_salt()` são especificamente projetadas para a geração de hashs de senhas. `crypt()` faz a geração do hash e `gen_salt()` prepara os parâmetros do algoritmo para isso.

Os algoritmos em `crypt()` diferem dos algoritmos de hashing MD5 ou SHA-1 usuais nos seguintes aspectos:

1. Eles são lentos. Como a quantidade de dados é tão pequena, essa é a única maneira de tornar as senhas difíceis de forçar.
2. Eles usam um valor aleatório, chamado *salto*, para que usuários com a mesma senha tenham senhas criptografadas diferentes. Isso também é uma defesa adicional contra a reversão do algoritmo.
3. Eles incluem o tipo de algoritmo no resultado, para que senhas criptografadas com diferentes algoritmos possam coexistir.
4. Alguns deles são adaptativos — isso significa que, quando os computadores ficam mais rápidos, você pode ajustar o algoritmo para ser mais lento, sem introduzir incompatibilidade com senhas existentes.

[Tabela F.18](pgcrypto.md#PGCRYPTO-CRYPT-ALGORITHMS "Table F.18. Supported Algorithms for crypt()]) lista os algoritmos suportados pela função `crypt()`.

**Tabela F.18. Algoritmos suportados para `crypt()`**



<table border="1" class="table" summary="Supported Algorithms for crypt()">
<colgroup>
<col class="col1"/>
<col class="col2"/>
<col class="col3"/>
<col class="col4"/>
<col class="col5"/>
<col class="col6"/>
</colgroup>
<thead>
<tr>
<th>
    Algorithm
   </th>
<th>
    Max Password Length
   </th>
<th>
    Adaptive?
   </th>
<th>
    Salt Bits
   </th>
<th>
    Output Length
   </th>
<th>Descrição</th>
</tr>
</thead>
<tbody>
<tr>
<td>
<code class="literal">
     bf
    </code>
</td>
<td>
    72
   </td>
<td>
    yes
   </td>
<td>
    128
   </td>
<td>
    60
   </td>
<td>Baseado em Blowfish, variante 2a</td>
</tr>
<tr>
<td>
<code class="literal">
     md5
    </code>
</td>
<td>
    unlimited
   </td>
<td>
    no
   </td>
<td>
    48
   </td>
<td>
    34
   </td>
<td>criptografia baseada em MD5</td>
</tr>
<tr>
<td>
<code class="literal">
     xdes
    </code>
</td>
<td>
    8
   </td>
<td>
    yes
   </td>
<td>
    24
   </td>
<td>
    20
   </td>
<td>DES estendido</td>
</tr>
<tr>
<td>
<code class="literal">
     des
    </code>
</td>
<td>
    8
   </td>
<td>
    no
   </td>
<td>
    12
   </td>
<td>
    13
   </td>
<td>cripto original UNIX</td>
</tr>
<tr>
<td>
<code class="literal">
     sha256crypt
    </code>
</td>
<td>
    unlimited
   </td>
<td>
    yes
   </td>
<td>
    up to 32
   </td>
<td>
    80
   </td>
<td>Adaptado de uma implementação de referência disponível publicamente<a class="ulink" href="https://www.akkadia.org/drepper/SHA-crypt.txt" target="_top">Unix crypt usando SHA-256 e SHA-512</a>
</td>
</tr>
<tr>
<td>
<code class="literal">
     sha512crypt
    </code>
</td>
<td>
    unlimited
   </td>
<td>
    yes
   </td>
<td>
    up to 32
   </td>
<td>
    123
   </td>
<td>Adaptado de uma implementação de referência disponível publicamente<a class="ulink" href="https://www.akkadia.org/drepper/SHA-crypt.txt" target="_top">Unix crypt usando SHA-256 e SHA-512</a>
</td>
</tr>
</tbody>
</table>




  

#### F.26.2.1. `crypt()` [#](#PGCRYPTO-PASSWORD-HASHING-FUNCS-CRYPT)

```
crypt(password text, salt text) returns text
```

Calcula um hash em estilo crypt(3) de *`password`*. Ao armazenar uma nova senha, você precisa usar `gen_salt()` para gerar um novo valor *`salt`*. Para verificar uma senha, passe o valor do hash armazenado como *`salt`*, e teste se o resultado corresponde ao valor armazenado.

Exemplo de definição de uma nova senha:

```
UPDATE ... SET pswhash = crypt('new password', gen_salt('md5'));
```

Exemplo de autenticação:

```
SELECT (pswhash = crypt('entered password', pswhash)) AS pswmatch FROM ... ;
```

Isso retorna `true` se a senha inserida estiver correta.

#### F.26.2.2. `gen_salt()` [#](#PGCRYPTO-PASSWORD-HASHING-FUNCS-GEN-SALT)

```
gen_salt(type text [, iter_count integer ]) returns text
```

Gera uma nova cadeia de sal aleatória para uso em `crypt()`. A cadeia de sal também informa ao `crypt()` qual algoritmo usar.

O parâmetro *`type` especifica o algoritmo de hashing. Os tipos aceitos são: `des`, `xdes`, `md5`, `bf`, `sha256crypt` e `sha512crypt`. Os dois últimos, `sha256crypt` e `sha512crypt`, são hashes de senha modernos baseados no `SHA-2`.

O parâmetro *`iter_count`* permite que o usuário especifique o número de iterações, para algoritmos que tenham uma. Quanto maior o número, mais tempo leva para gerar o hash da senha e, portanto, mais tempo para quebrá-la. Embora, com um número muito alto, o tempo para calcular um hash possa ser vários anos — o que é um tanto impraticável. Se o parâmetro *`iter_count`* for omitido, o número de iterações padrão é usado. Os valores permitidos para *`iter_count`* dependem do algoritmo e são mostrados em [Tabela F.19](pgcrypto.md#PGCRYPTO-ICFC-TABLE "Table F.19. Iteration Counts for crypt()").

**Tabela F.19. Contagem de iterações para `crypt()`**



<table border="1" class="table" summary="Iteration Counts for crypt()">
<colgroup>
<col/>
<col/>
<col/>
<col/>
</colgroup>
<thead>
<tr>
<th>
    Algorithm
   </th>
<th>
    Default
   </th>
<th>
    Min
   </th>
<th>
    Max
   </th>
</tr>
</thead>
<tbody>
<tr>
<td>
<code class="literal">
     xdes
    </code>
</td>
<td>
    725
   </td>
<td>
    1
   </td>
<td>
    16777215
   </td>
</tr>
<tr>
<td>
<code class="literal">
     bf
    </code>
</td>
<td>
    6
   </td>
<td>
    4
   </td>
<td>
    31
   </td>
</tr>
<tr>
<td>
<code class="literal">
     sha256crypt, sha512crypt
    </code>
</td>
<td>
    5000
   </td>
<td>
    1000
   </td>
<td>
    999999999
   </td>
</tr>
</tbody>
</table>




  

Para `xdes`, há uma limitação adicional de que o número de iterações deve ser um número ímpar.

Para escolher um número apropriado de iterações, considere que o DES original foi projetado para ter a velocidade de 4 hashes por segundo no hardware daquela época. Mais lento que 4 hashes por segundo provavelmente tornaria a usabilidade menos agradável. Mais rápido que 100 hashes por segundo provavelmente é muito rápido.

[Tabela F.20](pgcrypto.md#PGCRYPTO-HASH-SPEED-TABLE "Table F.20. Hash Algorithm Speeds") fornece uma visão geral da relativa lentidão dos diferentes algoritmos de hashing. A tabela mostra quanto tempo levaria para tentar todas as combinações de caracteres em uma senha de 8 caracteres, assumindo que a senha contenha apenas letras minúsculas, ou letras maiúsculas e minúsculas e números. Nas entradas do `crypt-bf`, o número após uma barra é o parâmetro *`iter_count`* do `gen_salt`.

O padrão *`iter_count` para `sha256crypt` e `sha512crypt` de `5000` é considerado muito baixo para o hardware moderno, mas pode ser ajustado para gerar hashes de senha mais fortes. Caso contrário, ambos os hashes, `sha256crypt` e `sha512crypt` são considerados seguros.

**Tabela F.20. Velocidades dos algoritmos de hash**



<table border="1" class="table" summary="Hash Algorithm Speeds">
<colgroup>
<col/>
<col/>
<col/>
<col/>
<col/>
</colgroup>
<thead>
<tr>
<th>
    Algorithm
   </th>
<th>
    Hashes/sec
   </th>
<th>
    For
    <code class="literal">
     [a-z]
    </code>
</th>
<th>
    For
    <code class="literal">
     [A-Za-z0-9]
    </code>
</th>
<th>
    Duration relative to
    <code class="literal">
     md5 hash
    </code>
</th>
</tr>
</thead>
<tbody>
<tr>
<td>
<code class="literal">
     crypt-bf/8
    </code>
</td>
<td>
    1792
   </td>
<td>
    4 years
   </td>
<td>
    3927 years
   </td>
<td>
    100k
   </td>
</tr>
<tr>
<td>
<code class="literal">
     crypt-bf/7
    </code>
</td>
<td>
    3648
   </td>
<td>
    2 years
   </td>
<td>
    1929 years
   </td>
<td>
    50k
   </td>
</tr>
<tr>
<td>
<code class="literal">
     crypt-bf/6
    </code>
</td>
<td>
    7168
   </td>
<td>
    1 year
   </td>
<td>
    982 years
   </td>
<td>
    25k
   </td>
</tr>
<tr>
<td>
<code class="literal">
     crypt-bf/5
    </code>
</td>
<td>
    13504
   </td>
<td>
    188 days
   </td>
<td>
    521 years
   </td>
<td>
    12.5k
   </td>
</tr>
<tr>
<td>
<code class="literal">
     crypt-md5
    </code>
</td>
<td>
    171584
   </td>
<td>
    15 days
   </td>
<td>
    41 years
   </td>
<td>
    1k
   </td>
</tr>
<tr>
<td>
<code class="literal">
     crypt-des
    </code>
</td>
<td>
    23221568
   </td>
<td>
    157.5 minutes
   </td>
<td>
    108 days
   </td>
<td>
    7
   </td>
</tr>
<tr>
<td>
<code class="literal">
     sha1
    </code>
</td>
<td>
    37774272
   </td>
<td>
    90 minutes
   </td>
<td>
    68 days
   </td>
<td>
    4
   </td>
</tr>
<tr>
<td>
<code class="literal">
     md5
    </code>
    (hash)
   </td>
<td>
    150085504
   </td>
<td>
    22.5 minutes
   </td>
<td>
    17 days
   </td>
<td>
    1
   </td>
</tr>
</tbody>
</table>




  

Notas:

* Os números dos algoritmos utilizados são `crypt-des` e `crypt-md5`. Os números são extraídos da saída do John the Ripper v1.6.38 `-test`. * Os números `md5 hash` são do mdcrack 1.2. * Os números `sha1` são do lcrack-20031130-beta. * Os números `crypt-bf` são obtidos por meio de um programa simples que percorre 1000 senhas de 8 caracteres. Dessa forma, a velocidade com diferentes números de iterações pode ser mostrada. Para referência: `john -test` mostra 13506 loops/seg para `crypt-bf/5`. (A pequena diferença nos resultados está de acordo com o fato de que a implementação do `crypt-bf` no `pgcrypto` é a mesma usada no John the Ripper.)

Observe que "tentar todas as combinações" não é um exercício realista. Geralmente, a quebra de senha é feita com a ajuda de dicionários, que contêm tanto palavras regulares quanto várias mutações delas. Portanto, até mesmo senhas um tanto semelhantes a palavras podem ser quebradas muito mais rápido do que os números acima sugerem, enquanto uma senha de 6 caracteres que não é semelhante a uma palavra pode escapar da quebra. Ou

### F.26.3. Funções de Encriptação PGP [#](#PGCRYPTO-PGP-ENC-FUNCS)

As funções aqui implementam a parte de criptografia do padrão OpenPGP ([RFC 4880][(https://datatracker.ietf.org/doc/html/rfc4880)]). São suportadas a criptografia de chave simétrica e a criptografia de chave pública.

Uma mensagem PGP criptografada é composta por 2 partes, ou *pacotes*:

* Pacotes contendo uma chave de sessão — criptografada por chave simétrica ou chave pública. * Pacotes contendo dados criptografados com a chave de sessão.

Ao criptografar com uma chave simétrica (ou seja, uma senha):

1. A senha fornecida é criptografada usando um algoritmo String2Key (S2K). Isso é bastante semelhante aos algoritmos `crypt()` — propositalmente lentos e com sal aleatório — mas produz uma chave binária de comprimento total.
2. Se uma chave de sessão separada for solicitada, uma nova chave aleatória será gerada. Caso contrário, a chave S2K será usada diretamente como chave de sessão.
3. Se a chave S2K for usada diretamente, apenas as configurações S2K serão colocadas no pacote da chave de sessão. Caso contrário, a chave de sessão será criptografada com a chave S2K e colocada no pacote da chave de sessão.

Ao criptografar com uma chave pública:

1. Uma nova chave aleatória de sessão é gerada.  
2. Ela é criptografada usando a chave pública e colocada no pacote de chave de sessão.

Em qualquer caso, os dados a serem criptografados são processados da seguinte forma:

1. Manipulação opcional de dados: compressão, conversão para UTF-8 e/ou conversão de finais de linha. 2. Os dados são prefixados com um bloco de bytes aleatórios. Isso é equivalente ao uso de um IV aleatório. 3. Um hash SHA-1 do prefixo e dos dados aleatórios é anexado. 4. Tudo isso é criptografado com a chave de sessão e colocado no pacote de dados.

#### F.26.3.1. `pgp_sym_encrypt()` [#](#PGCRYPTO-PGP-ENC-FUNCS-PGP-SYM-ENCRYPT)

```
pgp_sym_encrypt(data text, psw text [, options text ]) returns bytea
pgp_sym_encrypt_bytea(data bytea, psw text [, options text ]) returns bytea
```

Encripte *`data`* com uma chave PGP simétrica *`psw`*. O parâmetro *`options`* pode conter configurações de opção, conforme descrito abaixo.

#### F.26.3.2. `pgp_sym_decrypt()` [#](#PGCRYPTO-PGP-ENC-FUNCS-PGP-SYM-DECRYPT)

```
pgp_sym_decrypt(msg bytea, psw text [, options text ]) returns text
pgp_sym_decrypt_bytea(msg bytea, psw text [, options text ]) returns bytea
```

Descifre uma mensagem PGP criptografada com chave simétrica.

A descriptografia dos dados `bytea` com `pgp_sym_decrypt` não é permitida. Isso é para evitar a saída de dados de caracteres inválidos. A descriptografia de dados originalmente textuais com `pgp_sym_decrypt_bytea` está bem.

O parâmetro *`options`* pode conter configurações de opção, conforme descrito abaixo.

#### F.26.3.3. `pgp_pub_encrypt()` [#](#PGCRYPTO-PGP-ENC-FUNCS-PGP-PUB-ENCRYPT)

```
pgp_pub_encrypt(data text, key bytea [, options text ]) returns bytea
pgp_pub_encrypt_bytea(data bytea, key bytea [, options text ]) returns bytea
```

Encripte *`data`* com uma chave PGP pública *`key`*. Dar uma chave secreta a esta função produzirá um erro.

O parâmetro *`options`* pode conter configurações de opção, conforme descrito abaixo.

#### F.26.3.4. `pgp_pub_decrypt()` [#](#PGCRYPTO-PGP-ENC-FUNCS-PGP-PUB-DECRYPT)

```
pgp_pub_decrypt(msg bytea, key bytea [, psw text [, options text ]]) returns text
pgp_pub_decrypt_bytea(msg bytea, key bytea [, psw text [, options text ]]) returns bytea
```

Descubra uma mensagem criptografada com chave pública. *`key`* deve ser a chave secreta correspondente à chave pública que foi usada para criptografar. Se a chave secreta estiver protegida por senha, você deve fornecer a senha em *`psw`*. Se não houver senha, mas você deseja especificar opções, você precisa fornecer uma senha vazia.

A descriptografia dos dados `bytea` com `pgp_pub_decrypt` não é permitida. Isso é para evitar a saída de dados com caracteres inválidos. A descriptografia de dados originalmente textuais com `pgp_pub_decrypt_bytea` está bem.

O parâmetro *`options`* pode conter configurações de opção, conforme descrito abaixo.

#### F.26.3.5. `pgp_key_id()` [#](#PGCRYPTO-PGP-ENC-FUNCS-PGP-KEY-ID)

```
pgp_key_id(bytea) returns text
```

`pgp_key_id` extrai o ID chave de uma chave pública ou secreta do PGP. Ou fornece o ID da chave que foi usado para criptografar os dados, se for fornecida uma mensagem criptografada.

Ele pode retornar 2 IDs de chave especiais:

* `SYMKEY`

A mensagem é criptografada com uma chave simétrica. * `ANYKEY`

A mensagem é criptografada com chave pública, mas o ID da chave foi removido. Isso significa que você precisará testar todas as suas chaves secretas nela para ver qual delas a decifra. O próprio `pgcrypto` não produz mensagens desse tipo.

Observe que diferentes chaves podem ter o mesmo ID. Isso é raro, mas um evento normal. O aplicativo cliente deve então tentar descriptografar com cada uma delas, para ver qual se encaixa — como lidar com `ANYKEY`.

#### F.26.3.6. `armor()`, `dearmor()` [#](#PGCRYPTO-PGP-ENC-FUNCS-ARMOR)

```
armor(data bytea [ , keys text[], values text[] ]) returns text
dearmor(data text) returns bytea
```

Essas funções envolvem/desenvolvem dados binários no formato PGP ASCII-armor, que é basicamente Base64 com CRC e formatação adicional.

Se os arrays *`keys`* e *`values`* forem especificados, um *cabeçalho de armadura* é adicionado ao formato protegido para cada par chave/valor. Ambos os arrays devem ser unidimensionais e devem ter o mesmo comprimento. As chaves e os valores não podem conter quaisquer caracteres não ASCII.

#### F.26.3.7. `pgp_armor_headers` [#](#PGCRYPTO-PGP-ENC-FUNCS-PGP-ARMOR-HEADERS)

```
pgp_armor_headers(data text, key out text, value out text) returns setof record
```

`pgp_armor_headers()` extrai os cabeçalhos de armadura de *`data`*. O valor de retorno é um conjunto de linhas com duas colunas, chave e valor. Se as chaves ou valores contiverem caracteres não ASCII, eles são tratados como UTF-8.

#### F.26.3.8. Opções para funções PGP [#](#PGCRYPTO-PGP-ENC-FUNCS-OPTS)

As opções são nomeadas para serem semelhantes à GnuPG. O valor de uma opção deve ser dado após um sinal de igual; separe as opções entre si com vírgulas. Por exemplo:

```
pgp_sym_encrypt(data, psw, 'compress-algo=1, cipher-algo=aes256')
```

Todas as opções, exceto `convert-crlf`, aplicam-se apenas a funções de criptografia. As funções de descriptografia obtêm os parâmetros dos dados PGP.

As opções mais interessantes são provavelmente `compress-algo` e `unicode-mode`. O resto deve ter configurações padrão razoáveis.

##### F.26.3.8.1. cifra-algo [#](#PGCRYPTO-PGP-ENC-FUNCS-OPTS-CIPHER-ALGO)

Qual algoritmo de cifra utilizar.

Valores: bf, aes128, aes192, aes256, 3des, cast5 Padrão: aes128 Aplica-se a: pgp_sym_encrypt, pgp_pub_encrypt

##### F.26.3.8.2. comprimir-algo [#](#PGCRYPTO-PGP-ENC-FUNCS-OPTS-COMPRESS-ALGO)

Qual algoritmo de compressão usar. Disponível apenas se o PostgreSQL foi construído com zlib.

Valores: 0 — sem compressão 1 — compressão ZIP 2 — compressão ZLIB (= ZIP mais metadados e CRCs de bloco) Padrão: 0 Aplica-se a: pgp_sym_encrypt, pgp_pub_encrypt

##### F.26.3.8.3. nível de compressão [#](#PGCRYPTO-PGP-ENC-FUNCS-OPTS-COMPRESS-LEVEL)

Quanto comprimir. Níveis mais altos comprimem menos, mas são mais lentos. 0 desativa a compressão.

Valores: 0, 1-9 Padrão: 6 Aplica-se a: pgp_sym_encrypt, pgp_pub_encrypt

##### F.26.3.8.4. convert-crlf [#](#PGCRYPTO-PGP-ENC-FUNCS-OPTS-CONVERT-CRLF)

Se deve converter `\n` em `\r\n` ao criptografar e `\r\n` em `\n` ao descriptografar. O RFC 4880 especifica que os dados de texto devem ser armazenados usando `\r\n` de rodapés. Use isso para obter um comportamento totalmente compatível com o RFC.

Valores: 0, 1 Padrão: 0 Aplica-se a: pgp_sym_encrypt, pgp_pub_encrypt, pgp_sym_decrypt, pgp_pub_decrypt

##### F.26.3.8.5. desabilitar-mdc [#](#PGCRYPTO-PGP-ENC-FUNCS-OPTS-DISABLE-MDC)

Não proteja dados com SHA-1. A única boa razão para usar essa opção é para alcançar compatibilidade com produtos antigos do PGP, que antecedem a adição de pacotes protegidos com SHA-1 ao RFC 4880. O software recente do gnupg.org e pgp.com suporta isso bem.

Valores: 0, 1 Padrão: 0 Aplica-se a: pgp_sym_encrypt, pgp_pub_encrypt

##### F.26.3.8.6. sess-key [#](#PGCRYPTO-PGP-ENC-FUNCS-OPTS-SESS-KEY)

Use uma chave de sessão separada. A criptografia de chave pública sempre usa uma chave de sessão separada; esta opção é para criptografia de chave simétrica, que, por padrão, usa a chave S2K diretamente.

Valores: 0, 1 Padrão: 0 Aplica-se a: pgp_sym_encrypt

##### F.26.3.8.7. s2k-mode [#](#PGCRYPTO-PGP-ENC-FUNCS-OPTS-S2K-MODE)

Qual algoritmo S2K utilizar.

Valores: 0 — Sem sal. Perigoso! 1 — Com sal, mas com contagem fixa de iterações. 3 — Contagem variável de iterações. Padrão: 3 Aplica-se a: pgp_sym_encrypt

##### F.26.3.8.8. s2k-count [#](#PGCRYPTO-PGP-ENC-FUNCS-OPTS-S2K-COUNT)

O número de iterações do algoritmo S2K a ser utilizado. Deve ser um valor entre 1024 e 65011712, inclusive.

Padrão: Um valor aleatório entre 65536 e 253952. Aplica-se a: pgp_sym_encrypt, apenas com s2k-mode=3

##### F.26.3.8.9. s2k-digest-algo [#](#PGCRYPTO-PGP-ENC-FUNCS-OPTS-S2K-DIGEST-ALGO)

Qual algoritmo de digestão deve ser usado no cálculo S2K.

Valores: md5, sha1 Padrão: sha1 Aplica-se a: pgp_sym_encrypt

##### F.26.3.8.10. s2k-cipher-algo [#](#PGCRYPTO-PGP-ENC-FUNCS-OPTS-S2K-CIPHER-ALGO)

Qual cifrador usar para criptografar a chave de sessão separada.

Valores: bf, aes, aes128, aes192, aes256 Padrão: use cipher-algo Aplica-se a: pgp_sym_encrypt

##### F.26.3.8.11. modo-unicode [#](#PGCRYPTO-PGP-ENC-FUNCS-OPTS-UNICODE-MODE)

Se você deseja converter dados textuais do codificação interna do banco de dados para UTF-8 e vice-versa. Se o seu banco de dados já estiver em UTF-8, nenhuma conversão será feita, mas a mensagem será marcada como UTF-8. Sem essa opção, não será.

Valores: 0, 1 Padrão: 0 Aplica-se a: pgp_sym_encrypt, pgp_pub_encrypt

#### F.26.3.9. Gerando Chaves PGP com GnuPG [#](#PGCRYPTO-PGP-ENC-FUNCS-GNUPG)

Para gerar uma nova chave:

```
gpg --gen-key
```

O tipo de chave preferido é “DSA e Elgamal”.

Para criptografia RSA, você deve criar uma chave de assinatura apenas DSA ou RSA como mestre e, em seguida, adicionar uma subchave de criptografia RSA com `gpg --edit-key`.

Para listar as chaves:

```
gpg --list-secret-keys
```

Para exportar uma chave pública no formato ASCII-armor:

```
gpg -a --export KEYID > public.key
```

Para exportar uma chave secreta no formato ASCII-armor:

```
gpg -a --export-secret-keys KEYID > secret.key
```

Você precisa usar `dearmor()` nessas chaves antes de entregá-las às funções PGP. Ou, se você pode lidar com dados binários, pode descartar `-a` do comando.

Para mais detalhes, consulte `man gpg`, [O Manual de Privacidade do GNU][(https://www.gnupg.org/gph/en/manual.html)] e outras documentações em <https://www.gnupg.org/>.

#### F.26.3.10. Limitações do Código PGP [#](#PGCRYPTO-PGP-ENC-FUNCS-LIMITATIONS)

* Sem suporte para assinatura. Isso também significa que não é verificado se a subchave de criptografia pertence à chave mestre.
* Sem suporte para chave de criptografia como chave mestre. Como essa prática é geralmente desencorajada, isso não deve ser um problema.
* Sem suporte para várias sub Chaves. Isso pode parecer um problema, pois é uma prática comum. Por outro lado, você não deve usar suas chaves GPG/PGP regulares com `pgcrypto`, mas crie novas, pois o cenário de uso é bastante diferente.

### F.26.4. Funções de criptografia bruta [#](#PGCRYPTO-RAW-ENC-FUNCS)

Essas funções apenas aplicam um cifrador aos dados; elas não possuem nenhuma característica avançada da criptografia PGP. Portanto, elas têm alguns problemas importantes:

1. Eles usam a chave do usuário diretamente como chave de cifra.  
2. Eles não fornecem nenhum controle de integridade para verificar se os dados criptografados foram modificados.  
3. Eles esperam que os usuários gerenciem todos os parâmetros de criptografia, até mesmo o IV.  
4. Eles não lidam com texto.

Portanto, com a introdução da criptografia PGP, o uso de funções de criptografia bruta é desencorajado.

```
encrypt(data bytea, key bytea, type text) returns bytea
decrypt(data bytea, key bytea, type text) returns bytea

encrypt_iv(data bytea, key bytea, iv bytea, type text) returns bytea
decrypt_iv(data bytea, key bytea, iv bytea, type text) returns bytea
```

Criptografar/descriptar dados usando o método de cifra especificado por *`type`*. A sintaxe da string *`type`* é:

```
algorithm [ - mode ] [ /pad: padding ]
```

onde *`algorithm`* é um dos:

* `bf` — Blowfish
* `aes` — AES (Rijndael-128, -192 ou -256)

e *`mode`* é uma das:

* `cbc` — o próximo bloco depende do bloco anterior (padrão)
* `cfb` — o próximo bloco depende do bloco anterior criptografado
* `ecb` — cada bloco é criptografado separadamente (apenas para testes)

e *`padding`* é uma das:

* `pkcs` — os dados podem ter qualquer comprimento (padrão)  
* `none` — os dados devem ser múltiplos do tamanho do bloco de cifra

Então, por exemplo, estes são equivalentes:

```
encrypt(data, 'fooz', 'bf')
encrypt(data, 'fooz', 'bf-cbc/pad:pkcs')
```

Em `encrypt_iv` e `decrypt_iv`, o parâmetro *`iv`* é o valor inicial para o modo CBC e CFB; ele é ignorado para ECB. É recortado ou preenchido com zeros se não for exatamente o tamanho do bloco. Ele tem como padrão todos os zeros nas funções sem este parâmetro.

### F.26.5. Funções de dados aleatórios [#](#PGCRYPTO-RANDOM-DATA-FUNCS)

```
gen_random_bytes(count integer) returns bytea
```

Retorna *`count`* bytes aleatórios criptograficamente fortes. No máximo, 1024 bytes podem ser extraídos de cada vez. Isso é para evitar esgotar o pool de geradores de aleatoriedade.

```
gen_random_uuid() returns uuid
```

Retorna uma UUID da versão 4 (aleatória). (Desatualizada, essa função chama internamente a função [função central][(functions-uuid.md "9.14. UUID Functions")] do mesmo nome.)

### F.26.6. Funções de Suporte OpenSSL [#](#PGCRYPTO-OPENSSL-SUPPORT-FUNCS)

```
fips_mode() returns boolean
```

Retorna `true` se o OpenSSL estiver em execução com o modo FIPS habilitado, caso contrário, `false`.

### F.26.7. Parâmetros de configuração [#](#PGCRYPTO-CONFIGURATION-PARAMETERS)

Há um parâmetro de configuração que controla o comportamento do `pgcrypto`.

`pgcrypto.builtin_crypto_enabled` (`enum`) [#](#PGCRYPTO-CONFIGURATION-PARAMETERS-BUILTIN_CRYPTO_ENABLED): `pgcrypto.builtin_crypto_enabled` determina se as funções criptográficas integradas `gen_salt()`, e `crypt()` estão disponíveis para uso. Definir isso para `off` desativa essas funções. `on` (o padrão) habilita essas funções para funcionar normalmente. `fips` desativa essas funções se o OpenSSL for detectado para operar no modo FIPS.

No uso comum, este parâmetro é definido em `postgresql.conf`, embora os superusuários possam alterá-lo em tempo real dentro de suas próprias sessões.

### F.26.8. Notas [#](#PGCRYPTO-NOTES)

#### F.26.8.1. Configuração [#](#PGCRYPTO-NOTES-CONFIG)

`pgcrypto` se configura de acordo com as descobertas do principal script `configure` do PostgreSQL. As opções que afetam isso são `--with-zlib` e `--with-ssl=openssl`.

Quando compilado com zlib, as funções de criptografia PGP conseguem comprimir os dados antes de criptografá-los.

`pgcrypto` requer OpenSSL. Caso contrário, ele não será construído ou instalado.

Quando compilado contra OpenSSL 3.0.0 e versões posteriores, o provedor legítimo deve ser ativado no arquivo de configuração `openssl.cnf` para utilizar cifras mais antigas, como DES ou Blowfish.

#### F.26.8.2. Tratamento de NULO [#](#PGCRYPTO-NOTES-NULL-HANDLING)

Como é padrão no SQL, todas as funções retornam NULL, se algum dos argumentos for NULL. Isso pode criar riscos de segurança em uso descuidado.

#### F.26.8.3. Limitações de segurança [#](#PGCRYPTO-NOTES-SEC-LIMITS)

Todas as funções do `pgcrypto` são executadas dentro do servidor de banco de dados. Isso significa que todos os dados e senhas se movem entre o `pgcrypto` e as aplicações do cliente em texto claro. Assim, você deve:

1. Conecte localmente ou use conexões SSL.  
2. Confie tanto no administrador do sistema quanto no do banco de dados.

Se não puder, então é melhor fazer criptografia dentro da aplicação do cliente.

A implementação não resiste a ataques de canal lateral (https://en.wikipedia.org/wiki/Side-channel_attack). Por exemplo, o tempo necessário para que uma função de descriptografia `pgcrypto` seja concluída varia entre os textos cifrados de um tamanho dado.

### F.26.9. Autor [#](#PGCRYPTO-AUTHOR)

Marko Kreen `<markokr@gmail.com>`

`pgcrypto` utiliza código das seguintes fontes:



<table border="1" class="informaltable">
<colgroup>
<col/>
<col/>
<col/>
</colgroup>
<thead>
<tr>
<th>
    Algorithm
   </th>
<th>
    Author
   </th>
<th>
    Source origin
   </th>
</tr>
</thead>
<tbody>
<tr>
<td>
    DES crypt
   </td>
<td>
    David Burren and others
   </td>
<td>
    FreeBSD libcrypt
   </td>
</tr>
<tr>
<td>
    MD5 crypt
   </td>
<td>
    Poul-Henning Kamp
   </td>
<td>
    FreeBSD libcrypt
   </td>
</tr>
<tr>
<td>
    Blowfish crypt
   </td>
<td>
    Solar Designer
   </td>
<td>
    www.openwall.com
   </td>
</tr>
</tbody>
</table>

