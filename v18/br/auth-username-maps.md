## 20.2. Mapas de Nome de Usuário [#](#AUTH-USERNAME-MAPS)

Ao usar um sistema de autenticação externo, como Ident ou GSSAPI, o nome do usuário do sistema operacional que iniciou a conexão pode não ser o mesmo que o usuário (papel) do banco de dados que será usado. Neste caso, um mapa de nomes de usuário pode ser aplicado para mapear o nome do usuário do sistema operacional para um usuário do banco de dados. Para usar o mapeamento de nomes de usuário, especifique `map`=*`map-name`* no campo de opções em `pg_hba.conf`. Esta opção é suportada para todos os métodos de autenticação que recebem nomes de usuário externos. Como diferentes mapeamentos podem ser necessários para diferentes conexões, o nome do mapa a ser usado é especificado no parâmetro *`map-name`* em `pg_hba.conf` para indicar qual mapa usar para cada conexão individual.

Os mapas de nome de usuário são definidos no arquivo de mapa ident, que, por padrão, é denominado `pg_ident.conf` e é armazenado no diretório de dados do clúster. (É possível colocar o arquivo de mapa em outro lugar, no entanto; veja o parâmetro de configuração [ident_file][(runtime-config-file-locations.md#GUC-IDENT-FILE)]. O arquivo de mapa ident contém linhas das formas gerais:

```
map-name system-username database-username
include file
include_if_exists file
include_dir directory
```

Comentários, espaços em branco e continuações de linha são tratados da mesma maneira que em `pg_hba.conf`. O *`map-name`* é um nome arbitrário que será usado para se referir a este mapeamento em `pg_hba.conf`. Os outros dois campos especificam o nome de usuário do sistema operacional e o nome de usuário do banco de dados correspondente. O mesmo *`map-name`* pode ser usado repetidamente para especificar múltiplos mapeamentos de usuário dentro de um único mapa.

Quanto ao `pg_hba.conf`, as linhas neste arquivo podem ser diretrizes de inclusão, seguindo as mesmas regras.

O arquivo `pg_ident.conf` é lido ao iniciar o sistema e quando o processo do servidor principal recebe um sinal SIGHUP. Se você editar o arquivo em um sistema ativo, você precisará sinalizar o postmaster (usando `pg_ctl reload`, chamando a função SQL `pg_reload_conf()`, ou usando `kill -HUP`) para fazer com que ele leia o arquivo novamente.

A visualização do sistema `pg_ident_file_mappings`(view-pg-ident-file-mappings.md "53.11. pg_ident_file_mappings") pode ser útil para testar prévia as alterações no arquivo `pg_ident.conf`, ou para diagnosticar problemas se o carregamento do arquivo não tiver tido os efeitos desejados. As linhas da visualização com campos `error` que não são nulos indicam problemas nas linhas correspondentes do arquivo.

Não há restrição sobre quantos usuários de banco de dados um usuário de um sistema operacional específico pode corresponder, nem vice-versa. Assim, as entradas em um mapa devem ser entendidas como significando “este usuário do sistema operacional é autorizado a se conectar como este usuário do banco de dados”, em vez de implicando que são equivalentes. A conexão será permitida se houver alguma entrada no mapa que pare o nome do usuário obtido do sistema de autenticação externo com o nome do usuário do banco de dados que o usuário solicitou para se conectar. O valor `all` pode ser usado como *`database-username`* para especificar que, se o *`system-username`* corresponder, então este usuário é autorizado a fazer login como qualquer um dos usuários existentes do banco de dados. Citando `all` faz com que a palavra-chave perca seu significado especial.

Se o *`database-username`* começar com um caractere `+`, o usuário do sistema operacional pode fazer login como qualquer usuário pertencente a esse papel, da mesma forma que os nomes de usuário que começam com `+` são tratados em `pg_hba.conf`. Assim, uma marcação `+` significa “correspondência com qualquer um dos papéis que são membros diretamente ou indiretamente desse papel”, enquanto um nome sem uma marcação `+` corresponde apenas a esse papel específico. Citar um nome de usuário que começa com um `+` faz com que o `+` perca seu significado especial.

Se o campo *`system-username`* começar com uma barra (`/`,) o restante do campo é tratado como uma expressão regular. (Consulte [Seção 9.7.3.1][(functions-matching.md#POSIX-SYNTAX-DETAILS "9.7.3.1. Regular Expression Details")] para detalhes da sintaxe de expressão regular do PostgreSQL. A expressão regular pode incluir uma única captura ou uma subexpressão entre parênteses. A parte do nome do usuário do sistema que correspondeu à captura pode então ser referenciada no campo *`database-username`* como `\1` (barra-um). Isso permite a mapeo de múltiplos nomes de usuário em uma única linha, o que é particularmente útil para substituições de sintaxe simples. Por exemplo, essas entradas

```
mymap   /^(.*)@mydomain\.com$      \1
mymap   /^(.*)@otherdomain\.com$   guest
```

removerá a parte do domínio para usuários com nomes de usuário do sistema que terminam com `@mydomain.com`, e permitirá que qualquer usuário cujo nome do sistema termine com `@otherdomain.com` faça login como `guest`. Citando um *`database-username`* que contém `\1` *não* fará com que `\1` perca seu significado especial.

Se o campo *`database-username`* começar com uma barra (`/`), o restante do campo é tratado como uma expressão regular. Quando o campo *`database-username`* é uma expressão regular, não é possível usar `\1` dentro dela para se referir a uma captura do campo *`system-username`*.

### DICA

Tenha em mente que, por padrão, uma expressão regular pode corresponder apenas a parte de uma string. Geralmente é prudente usar `^` e `$`, como mostrado no exemplo acima, para forçar a correspondência a ser ao nome completo do usuário do sistema.

Um arquivo `pg_ident.conf` que pode ser usado em conjunto com o arquivo `pg_hba.conf` em [Exemplo 20.1](auth-pg-hba-conf.md#EXAMPLE-PG-HBA.CONF "Example 20.1. Example pg_hba.conf Entries") é mostrado em [Exemplo 20.2](auth-username-maps.md#EXAMPLE-PG-IDENT.CONF "Example 20.2. An Example pg_ident.conf File"). Neste exemplo, qualquer pessoa autenticada em uma máquina na rede 192.168 que não tenha o nome de usuário do sistema operacional `bryanh`, `ann` ou `robert` não teria acesso. O usuário Unix `robert` só teria permissão para acessar quando tentar se conectar como usuário PostgreSQL `bob`, não como `robert` ou qualquer outra pessoa. `ann` só teria permissão para se conectar como `ann`. O usuário `bryanh` teria permissão para se conectar como `bryanh` ou como `guest1`.

**Exemplo 20.2. Um exemplo de arquivo `pg_ident.conf`**

```
# MAPNAME       SYSTEM-USERNAME         PG-USERNAME

omicron         bryanh                  bryanh
omicron         ann                     ann
# bob has user name robert on these machines
omicron         robert                  bob
# bryanh can also connect as guest1
omicron         bryanh                  guest1
```
