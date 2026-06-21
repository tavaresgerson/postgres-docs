## F.26. pgcrypto — cryptographic functions [#](#PGCRYPTO)

* [F.26.1. General Hashing Functions](pgcrypto.md#PGCRYPTO-GENERAL-HASHING-FUNCS)
* [F.26.2. Password Hashing Functions](pgcrypto.md#PGCRYPTO-PASSWORD-HASHING-FUNCS)
* [F.26.3. PGP Encryption Functions](pgcrypto.md#PGCRYPTO-PGP-ENC-FUNCS)
* [F.26.4. Raw Encryption Functions](pgcrypto.md#PGCRYPTO-RAW-ENC-FUNCS)
* [F.26.5. Random-Data Functions](pgcrypto.md#PGCRYPTO-RANDOM-DATA-FUNCS)
* [F.26.6. OpenSSL Support Functions](pgcrypto.md#PGCRYPTO-OPENSSL-SUPPORT-FUNCS)
* [F.26.7. Configuration Parameters](pgcrypto.md#PGCRYPTO-CONFIGURATION-PARAMETERS)
* [F.26.8. Notes](pgcrypto.md#PGCRYPTO-NOTES)
* [F.26.9. Author](pgcrypto.md#PGCRYPTO-AUTHOR)

The `pgcrypto` module provides cryptographic functions for PostgreSQL.

This module is considered “trusted”, that is, it can be installed by non-superusers who have `CREATE` privilege on the current database.

`pgcrypto` requires OpenSSL and won't be installed if OpenSSL support was not selected when PostgreSQL was built.

### F.26.1. General Hashing Functions [#](#PGCRYPTO-GENERAL-HASHING-FUNCS)

#### F.26.1.1. `digest()` [#](#PGCRYPTO-GENERAL-HASHING-FUNCS-DIGEST)

```
digest(data text, type text) returns bytea
digest(data bytea, type text) returns bytea
```

Computes a binary hash of the given *`data`*. *`type`* is the algorithm to use. Standard algorithms are `md5`, `sha1`, `sha224`, `sha256`, `sha384` and `sha512`. Moreover, any digest algorithm OpenSSL supports is automatically picked up.

If you want the digest as a hexadecimal string, use `encode()` on the result. For example:

```
CREATE OR REPLACE FUNCTION sha1(bytea) returns text AS $$
    SELECT encode(digest($1, 'sha1'), 'hex')
$$ LANGUAGE SQL STRICT IMMUTABLE;
```

#### F.26.1.2. `hmac()` [#](#PGCRYPTO-GENERAL-HASHING-FUNCS-HMAC)

```
hmac(data text, key text, type text) returns bytea
hmac(data bytea, key bytea, type text) returns bytea
```

Calculates hashed MAC for *`data`* with key *`key`*. *`type`* is the same as in `digest()`.

This is similar to `digest()` but the hash can only be recalculated knowing the key. This prevents the scenario of someone altering data and also changing the hash to match.

If the key is larger than the hash block size it will first be hashed and the result will be used as key.

### F.26.2. Password Hashing Functions [#](#PGCRYPTO-PASSWORD-HASHING-FUNCS)

The functions `crypt()` and `gen_salt()` are specifically designed for hashing passwords. `crypt()` does the hashing and `gen_salt()` prepares algorithm parameters for it.

The algorithms in `crypt()` differ from the usual MD5 or SHA-1 hashing algorithms in the following respects:

1. They are slow. As the amount of data is so small, this is the only way to make brute-forcing passwords hard.
2. They use a random value, called the *salt*, so that users having the same password will have different encrypted passwords. This is also an additional defense against reversing the algorithm.
3. They include the algorithm type in the result, so passwords hashed with different algorithms can co-exist.
4. Some of them are adaptive — that means when computers get faster, you can tune the algorithm to be slower, without introducing incompatibility with existing passwords.

[Table F.18](pgcrypto.md#PGCRYPTO-CRYPT-ALGORITHMS "Table F.18. Supported Algorithms for crypt()") lists the algorithms supported by the `crypt()` function.

**Table F.18. Supported Algorithms for `crypt()`**



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
   <th>
    Description
   </th>
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
   <td>
    Blowfish-based, variant 2a
   </td>
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
   <td>
    MD5-based crypt
   </td>
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
   <td>
    Extended DES
   </td>
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
   <td>
    Original UNIX crypt
   </td>
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
   <td>
    Adapted from publicly available reference implementation
    <a class="ulink" href="https://www.akkadia.org/drepper/SHA-crypt.txt" target="_top">
     Unix crypt using SHA-256 and SHA-512
    </a>
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
   <td>
    Adapted from publicly available reference implementation
    <a class="ulink" href="https://www.akkadia.org/drepper/SHA-crypt.txt" target="_top">
     Unix crypt using SHA-256 and SHA-512
    </a>
   </td>
  </tr>
 </tbody>
</table>




  

#### F.26.2.1. `crypt()` [#](#PGCRYPTO-PASSWORD-HASHING-FUNCS-CRYPT)

```
crypt(password text, salt text) returns text
```

Calculates a crypt(3)-style hash of *`password`*. When storing a new password, you need to use `gen_salt()` to generate a new *`salt`* value. To check a password, pass the stored hash value as *`salt`*, and test whether the result matches the stored value.

Example of setting a new password:

```
UPDATE ... SET pswhash = crypt('new password', gen_salt('md5'));
```

Example of authentication:

```
SELECT (pswhash = crypt('entered password', pswhash)) AS pswmatch FROM ... ;
```

This returns `true` if the entered password is correct.

#### F.26.2.2. `gen_salt()` [#](#PGCRYPTO-PASSWORD-HASHING-FUNCS-GEN-SALT)

```
gen_salt(type text [, iter_count integer ]) returns text
```

Generates a new random salt string for use in `crypt()`. The salt string also tells `crypt()` which algorithm to use.

The *`type`* parameter specifies the hashing algorithm. The accepted types are: `des`, `xdes`, `md5`, `bf`, `sha256crypt` and `sha512crypt`. The last two, `sha256crypt` and `sha512crypt` are modern `SHA-2` based password hashes.

The *`iter_count`* parameter lets the user specify the iteration count, for algorithms that have one. The higher the count, the more time it takes to hash the password and therefore the more time to break it. Although with too high a count the time to calculate a hash may be several years — which is somewhat impractical. If the *`iter_count`* parameter is omitted, the default iteration count is used. Allowed values for *`iter_count`* depend on the algorithm and are shown in [Table F.19](pgcrypto.md#PGCRYPTO-ICFC-TABLE "Table F.19. Iteration Counts for crypt()").

**Table F.19. Iteration Counts for `crypt()`**



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




  

For `xdes` there is an additional limitation that the iteration count must be an odd number.

To pick an appropriate iteration count, consider that the original DES crypt was designed to have the speed of 4 hashes per second on the hardware of that time. Slower than 4 hashes per second would probably dampen usability. Faster than 100 hashes per second is probably too fast.

[Table F.20](pgcrypto.md#PGCRYPTO-HASH-SPEED-TABLE "Table F.20. Hash Algorithm Speeds") gives an overview of the relative slowness of different hashing algorithms. The table shows how much time it would take to try all combinations of characters in an 8-character password, assuming that the password contains either only lower case letters, or upper- and lower-case letters and numbers. In the `crypt-bf` entries, the number after a slash is the *`iter_count`* parameter of `gen_salt`.

The default *`iter_count`* for `sha256crypt` and `sha512crypt` of `5000` is considered too low for modern hardware, but can be adjusted to generate stronger password hashes. Otherwise both hashes, `sha256crypt` and `sha512crypt` are considered safe.

**Table F.20. Hash Algorithm Speeds**



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




  

Notes:

* The machine used is an Intel Mobile Core i3.
* `crypt-des` and `crypt-md5` algorithm numbers are taken from John the Ripper v1.6.38 `-test` output.
* `md5 hash` numbers are from mdcrack 1.2.
* `sha1` numbers are from lcrack-20031130-beta.
* `crypt-bf` numbers are taken using a simple program that loops over 1000 8-character passwords. That way the speed with different numbers of iterations can be shown. For reference: `john -test` shows 13506 loops/sec for `crypt-bf/5`. (The very small difference in results is in accordance with the fact that the `crypt-bf` implementation in `pgcrypto` is the same one used in John the Ripper.)

Note that “try all combinations” is not a realistic exercise. Usually password cracking is done with the help of dictionaries, which contain both regular words and various mutations of them. So, even somewhat word-like passwords could be cracked much faster than the above numbers suggest, while a 6-character non-word-like password may escape cracking. Or not.

### F.26.3. PGP Encryption Functions [#](#PGCRYPTO-PGP-ENC-FUNCS)

The functions here implement the encryption part of the OpenPGP ([RFC 4880](https://datatracker.ietf.org/doc/html/rfc4880)) standard. Supported are both symmetric-key and public-key encryption.

An encrypted PGP message consists of 2 parts, or *packets*:

* Packet containing a session key — either symmetric-key or public-key encrypted.
* Packet containing data encrypted with the session key.

When encrypting with a symmetric key (i.e., a password):

1. The given password is hashed using a String2Key (S2K) algorithm. This is rather similar to `crypt()` algorithms — purposefully slow and with random salt — but it produces a full-length binary key.
2. If a separate session key is requested, a new random key will be generated. Otherwise the S2K key will be used directly as the session key.
3. If the S2K key is to be used directly, then only S2K settings will be put into the session key packet. Otherwise the session key will be encrypted with the S2K key and put into the session key packet.

When encrypting with a public key:

1. A new random session key is generated.
2. It is encrypted using the public key and put into the session key packet.

In either case the data to be encrypted is processed as follows:

1. Optional data-manipulation: compression, conversion to UTF-8, and/or conversion of line-endings.
2. The data is prefixed with a block of random bytes. This is equivalent to using a random IV.
3. A SHA-1 hash of the random prefix and data is appended.
4. All this is encrypted with the session key and placed in the data packet.

#### F.26.3.1. `pgp_sym_encrypt()` [#](#PGCRYPTO-PGP-ENC-FUNCS-PGP-SYM-ENCRYPT)

```
pgp_sym_encrypt(data text, psw text [, options text ]) returns bytea
pgp_sym_encrypt_bytea(data bytea, psw text [, options text ]) returns bytea
```

Encrypt *`data`* with a symmetric PGP key *`psw`*. The *`options`* parameter can contain option settings, as described below.

#### F.26.3.2. `pgp_sym_decrypt()` [#](#PGCRYPTO-PGP-ENC-FUNCS-PGP-SYM-DECRYPT)

```
pgp_sym_decrypt(msg bytea, psw text [, options text ]) returns text
pgp_sym_decrypt_bytea(msg bytea, psw text [, options text ]) returns bytea
```

Decrypt a symmetric-key-encrypted PGP message.

Decrypting `bytea` data with `pgp_sym_decrypt` is disallowed. This is to avoid outputting invalid character data. Decrypting originally textual data with `pgp_sym_decrypt_bytea` is fine.

The *`options`* parameter can contain option settings, as described below.

#### F.26.3.3. `pgp_pub_encrypt()` [#](#PGCRYPTO-PGP-ENC-FUNCS-PGP-PUB-ENCRYPT)

```
pgp_pub_encrypt(data text, key bytea [, options text ]) returns bytea
pgp_pub_encrypt_bytea(data bytea, key bytea [, options text ]) returns bytea
```

Encrypt *`data`* with a public PGP key *`key`*. Giving this function a secret key will produce an error.

The *`options`* parameter can contain option settings, as described below.

#### F.26.3.4. `pgp_pub_decrypt()` [#](#PGCRYPTO-PGP-ENC-FUNCS-PGP-PUB-DECRYPT)

```
pgp_pub_decrypt(msg bytea, key bytea [, psw text [, options text ]]) returns text
pgp_pub_decrypt_bytea(msg bytea, key bytea [, psw text [, options text ]]) returns bytea
```

Decrypt a public-key-encrypted message. *`key`* must be the secret key corresponding to the public key that was used to encrypt. If the secret key is password-protected, you must give the password in *`psw`*. If there is no password, but you want to specify options, you need to give an empty password.

Decrypting `bytea` data with `pgp_pub_decrypt` is disallowed. This is to avoid outputting invalid character data. Decrypting originally textual data with `pgp_pub_decrypt_bytea` is fine.

The *`options`* parameter can contain option settings, as described below.

#### F.26.3.5. `pgp_key_id()` [#](#PGCRYPTO-PGP-ENC-FUNCS-PGP-KEY-ID)

```
pgp_key_id(bytea) returns text
```

`pgp_key_id` extracts the key ID of a PGP public or secret key. Or it gives the key ID that was used for encrypting the data, if given an encrypted message.

It can return 2 special key IDs:

* `SYMKEY`

  The message is encrypted with a symmetric key.
* `ANYKEY`

  The message is public-key encrypted, but the key ID has been removed. That means you will need to try all your secret keys on it to see which one decrypts it. `pgcrypto` itself does not produce such messages.

Note that different keys may have the same ID. This is rare but a normal event. The client application should then try to decrypt with each one, to see which fits — like handling `ANYKEY`.

#### F.26.3.6. `armor()`, `dearmor()` [#](#PGCRYPTO-PGP-ENC-FUNCS-ARMOR)

```
armor(data bytea [ , keys text[], values text[] ]) returns text
dearmor(data text) returns bytea
```

These functions wrap/unwrap binary data into PGP ASCII-armor format, which is basically Base64 with CRC and additional formatting.

If the *`keys`* and *`values`* arrays are specified, an *armor header* is added to the armored format for each key/value pair. Both arrays must be single-dimensional, and they must be of the same length. The keys and values cannot contain any non-ASCII characters.

#### F.26.3.7. `pgp_armor_headers` [#](#PGCRYPTO-PGP-ENC-FUNCS-PGP-ARMOR-HEADERS)

```
pgp_armor_headers(data text, key out text, value out text) returns setof record
```

`pgp_armor_headers()` extracts the armor headers from *`data`*. The return value is a set of rows with two columns, key and value. If the keys or values contain any non-ASCII characters, they are treated as UTF-8.

#### F.26.3.8. Options for PGP Functions [#](#PGCRYPTO-PGP-ENC-FUNCS-OPTS)

Options are named to be similar to GnuPG. An option's value should be given after an equal sign; separate options from each other with commas. For example:

```
pgp_sym_encrypt(data, psw, 'compress-algo=1, cipher-algo=aes256')
```

All of the options except `convert-crlf` apply only to encrypt functions. Decrypt functions get the parameters from the PGP data.

The most interesting options are probably `compress-algo` and `unicode-mode`. The rest should have reasonable defaults.

##### F.26.3.8.1. cipher-algo [#](#PGCRYPTO-PGP-ENC-FUNCS-OPTS-CIPHER-ALGO)

Which cipher algorithm to use.

Values: bf, aes128, aes192, aes256, 3des, cast5 Default: aes128 Applies to: pgp_sym_encrypt, pgp_pub_encrypt

##### F.26.3.8.2. compress-algo [#](#PGCRYPTO-PGP-ENC-FUNCS-OPTS-COMPRESS-ALGO)

Which compression algorithm to use. Only available if PostgreSQL was built with zlib.

Values: 0 - no compression 1 - ZIP compression 2 - ZLIB compression (= ZIP plus meta-data and block CRCs) Default: 0 Applies to: pgp_sym_encrypt, pgp_pub_encrypt

##### F.26.3.8.3. compress-level [#](#PGCRYPTO-PGP-ENC-FUNCS-OPTS-COMPRESS-LEVEL)

How much to compress. Higher levels compress smaller but are slower. 0 disables compression.

Values: 0, 1-9 Default: 6 Applies to: pgp_sym_encrypt, pgp_pub_encrypt

##### F.26.3.8.4. convert-crlf [#](#PGCRYPTO-PGP-ENC-FUNCS-OPTS-CONVERT-CRLF)

Whether to convert `\n` into `\r\n` when encrypting and `\r\n` to `\n` when decrypting. RFC 4880 specifies that text data should be stored using `\r\n` line-feeds. Use this to get fully RFC-compliant behavior.

Values: 0, 1 Default: 0 Applies to: pgp_sym_encrypt, pgp_pub_encrypt, pgp_sym_decrypt, pgp_pub_decrypt

##### F.26.3.8.5. disable-mdc [#](#PGCRYPTO-PGP-ENC-FUNCS-OPTS-DISABLE-MDC)

Do not protect data with SHA-1. The only good reason to use this option is to achieve compatibility with ancient PGP products, predating the addition of SHA-1 protected packets to RFC 4880. Recent gnupg.org and pgp.com software supports it fine.

Values: 0, 1 Default: 0 Applies to: pgp_sym_encrypt, pgp_pub_encrypt

##### F.26.3.8.6. sess-key [#](#PGCRYPTO-PGP-ENC-FUNCS-OPTS-SESS-KEY)

Use separate session key. Public-key encryption always uses a separate session key; this option is for symmetric-key encryption, which by default uses the S2K key directly.

Values: 0, 1 Default: 0 Applies to: pgp_sym_encrypt

##### F.26.3.8.7. s2k-mode [#](#PGCRYPTO-PGP-ENC-FUNCS-OPTS-S2K-MODE)

Which S2K algorithm to use.

Values: 0 - Without salt.  Dangerous! 1 - With salt but with fixed iteration count. 3 - Variable iteration count. Default: 3 Applies to: pgp_sym_encrypt

##### F.26.3.8.8. s2k-count [#](#PGCRYPTO-PGP-ENC-FUNCS-OPTS-S2K-COUNT)

The number of iterations of the S2K algorithm to use. It must be a value between 1024 and 65011712, inclusive.

Default: A random value between 65536 and 253952 Applies to: pgp_sym_encrypt, only with s2k-mode=3

##### F.26.3.8.9. s2k-digest-algo [#](#PGCRYPTO-PGP-ENC-FUNCS-OPTS-S2K-DIGEST-ALGO)

Which digest algorithm to use in S2K calculation.

Values: md5, sha1 Default: sha1 Applies to: pgp_sym_encrypt

##### F.26.3.8.10. s2k-cipher-algo [#](#PGCRYPTO-PGP-ENC-FUNCS-OPTS-S2K-CIPHER-ALGO)

Which cipher to use for encrypting separate session key.

Values: bf, aes, aes128, aes192, aes256 Default: use cipher-algo Applies to: pgp_sym_encrypt

##### F.26.3.8.11. unicode-mode [#](#PGCRYPTO-PGP-ENC-FUNCS-OPTS-UNICODE-MODE)

Whether to convert textual data from database internal encoding to UTF-8 and back. If your database already is UTF-8, no conversion will be done, but the message will be tagged as UTF-8. Without this option it will not be.

Values: 0, 1 Default: 0 Applies to: pgp_sym_encrypt, pgp_pub_encrypt

#### F.26.3.9. Generating PGP Keys with GnuPG [#](#PGCRYPTO-PGP-ENC-FUNCS-GNUPG)

To generate a new key:

```
gpg --gen-key
```

The preferred key type is “DSA and Elgamal”.

For RSA encryption you must create either DSA or RSA sign-only key as master and then add an RSA encryption subkey with `gpg --edit-key`.

To list keys:

```
gpg --list-secret-keys
```

To export a public key in ASCII-armor format:

```
gpg -a --export KEYID > public.key
```

To export a secret key in ASCII-armor format:

```
gpg -a --export-secret-keys KEYID > secret.key
```

You need to use `dearmor()` on these keys before giving them to the PGP functions. Or if you can handle binary data, you can drop `-a` from the command.

For more details see `man gpg`, [The GNU Privacy Handbook](https://www.gnupg.org/gph/en/manual.html) and other documentation on
<https://www.gnupg.org/>.

#### F.26.3.10. Limitations of PGP Code [#](#PGCRYPTO-PGP-ENC-FUNCS-LIMITATIONS)

* No support for signing. That also means that it is not checked whether the encryption subkey belongs to the master key.
* No support for encryption key as master key. As such practice is generally discouraged, this should not be a problem.
* No support for several subkeys. This may seem like a problem, as this is common practice. On the other hand, you should not use your regular GPG/PGP keys with `pgcrypto`, but create new ones, as the usage scenario is rather different.

### F.26.4. Raw Encryption Functions [#](#PGCRYPTO-RAW-ENC-FUNCS)

These functions only run a cipher over data; they don't have any advanced features of PGP encryption. Therefore they have some major problems:

1. They use user key directly as cipher key.
2. They don't provide any integrity checking, to see if the encrypted data was modified.
3. They expect that users manage all encryption parameters themselves, even IV.
4. They don't handle text.

So, with the introduction of PGP encryption, usage of raw encryption functions is discouraged.

```
encrypt(data bytea, key bytea, type text) returns bytea
decrypt(data bytea, key bytea, type text) returns bytea

encrypt_iv(data bytea, key bytea, iv bytea, type text) returns bytea
decrypt_iv(data bytea, key bytea, iv bytea, type text) returns bytea
```

Encrypt/decrypt data using the cipher method specified by *`type`*. The syntax of the *`type`* string is:

```
algorithm [ - mode ] [ /pad: padding ]
```

where *`algorithm`* is one of:

* `bf` — Blowfish
* `aes` — AES (Rijndael-128, -192 or -256)

and *`mode`* is one of:

* `cbc` — next block depends on previous (default)
* `cfb` — next block depends on previous encrypted block
* `ecb` — each block is encrypted separately (for testing only)

and *`padding`* is one of:

* `pkcs` — data may be any length (default)
* `none` — data must be multiple of cipher block size

So, for example, these are equivalent:

```
encrypt(data, 'fooz', 'bf')
encrypt(data, 'fooz', 'bf-cbc/pad:pkcs')
```

In `encrypt_iv` and `decrypt_iv`, the *`iv`* parameter is the initial value for the CBC and CFB mode; it is ignored for ECB. It is clipped or padded with zeroes if not exactly block size. It defaults to all zeroes in the functions without this parameter.

### F.26.5. Random-Data Functions [#](#PGCRYPTO-RANDOM-DATA-FUNCS)

```
gen_random_bytes(count integer) returns bytea
```

Returns *`count`* cryptographically strong random bytes. At most 1024 bytes can be extracted at a time. This is to avoid draining the randomness generator pool.

```
gen_random_uuid() returns uuid
```

Returns a version 4 (random) UUID. (Obsolete, this function internally calls the [core function](functions-uuid.md "9.14. UUID Functions") of the same name.)

### F.26.6. OpenSSL Support Functions [#](#PGCRYPTO-OPENSSL-SUPPORT-FUNCS)

```
fips_mode() returns boolean
```

Returns `true` if OpenSSL is running with FIPS mode enabled, otherwise `false`.

### F.26.7. Configuration Parameters [#](#PGCRYPTO-CONFIGURATION-PARAMETERS)

There is one configuration parameter that controls the behavior of `pgcrypto`.

`pgcrypto.builtin_crypto_enabled` (`enum`) [#](#PGCRYPTO-CONFIGURATION-PARAMETERS-BUILTIN_CRYPTO_ENABLED): `pgcrypto.builtin_crypto_enabled` determines if the built in crypto functions `gen_salt()`, and `crypt()` are available for use. Setting this to `off` disables these functions. `on` (the default) enables these functions to work normally. `fips` disables these functions if OpenSSL is detected to operate in FIPS mode.

In ordinary usage, this parameter is set in `postgresql.conf`, although superusers can alter it on-the-fly within their own sessions.

### F.26.8. Notes [#](#PGCRYPTO-NOTES)

#### F.26.8.1. Configuration [#](#PGCRYPTO-NOTES-CONFIG)

`pgcrypto` configures itself according to the findings of the main PostgreSQL `configure` script. The options that affect it are `--with-zlib` and `--with-ssl=openssl`.

When compiled with zlib, PGP encryption functions are able to compress data before encrypting.

`pgcrypto` requires OpenSSL. Otherwise, it will not be built or installed.

When compiled against OpenSSL 3.0.0 and later versions, the legacy provider must be activated in the `openssl.cnf` configuration file in order to use older ciphers like DES or Blowfish.

#### F.26.8.2. NULL Handling [#](#PGCRYPTO-NOTES-NULL-HANDLING)

As is standard in SQL, all functions return NULL, if any of the arguments are NULL. This may create security risks on careless usage.

#### F.26.8.3. Security Limitations [#](#PGCRYPTO-NOTES-SEC-LIMITS)

All `pgcrypto` functions run inside the database server. That means that all the data and passwords move between `pgcrypto` and client applications in clear text. Thus you must:

1. Connect locally or use SSL connections.
2. Trust both system and database administrator.

If you cannot, then better do crypto inside client application.

The implementation does not resist [side-channel attacks](https://en.wikipedia.org/wiki/Side-channel_attack). For example, the time required for a `pgcrypto` decryption function to complete varies among ciphertexts of a given size.

### F.26.9. Author [#](#PGCRYPTO-AUTHOR)

Marko Kreen `<markokr@gmail.com>`

`pgcrypto` uses code from the following sources:



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

