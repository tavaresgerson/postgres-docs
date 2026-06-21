## 18.10. Conexões TCP/IP seguras com criptografia GSSAPI [#](#GSSAPI-ENC)

* [18.10.1. Configuração Básica](gssapi-enc.md#GSSAPI-SETUP)

O PostgreSQL também tem suporte nativo para usar GSSAPI para criptografar comunicações cliente/servidor para maior segurança. O suporte requer que uma implementação GSSAPI (como MIT Kerberos) seja instalada nos sistemas cliente e servidor, e que o suporte no PostgreSQL seja habilitado na hora da construção (consulte [Capítulo 17](installation.md)).

### 18.10.1. Configuração básica [#](#GSSAPI-SETUP)

O servidor PostgreSQL ouvirá conexões criptografadas tanto com GSSAPI quanto com conexões criptografadas normalmente na mesma porta TCP, e negociará com qualquer cliente que se conecte se deve usar GSSAPI para criptografia (e para autenticação). Por padrão, essa decisão cabe ao cliente (o que significa que pode ser reduzida por um atacante); veja [Seção 20.1] sobre como configurar o servidor para exigir o uso de GSSAPI para algumas ou todas as conexões.

Ao usar o GSSAPI para criptografia, é comum usar o GSSAPI também para autenticação, uma vez que o mecanismo subjacente determinará as identidades do cliente e do servidor (de acordo com a implementação do GSSAPI) em qualquer caso. Mas isso não é necessário; outro método de autenticação do PostgreSQL pode ser escolhido para realizar uma verificação adicional.

Além da configuração do comportamento de negociação, a criptografia GSSAPI não requer configuração além da necessária para autenticação GSSAPI. (Para mais informações sobre a configuração disso, consulte [Seção 20.6] ([(gssapi-auth.md "20.6. GSSAPI Authentication")]).)