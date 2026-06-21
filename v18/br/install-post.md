## 17.5. Configuração pós-instalação [#](#INSTALL-POST)

* [17.5.1. Bibliotecas Compartilhadas](install-post.md#INSTALL-POST-SHLIBS)
* [17.5.2. Variáveis Ambientais](install-post.md#INSTALL-POST-ENV-VARS)

### 17.5.1. Bibliotecas Compartilhadas [#](#INSTALL-POST-SHLIBS)

Em alguns sistemas com bibliotecas compartilhadas, você precisa informar ao sistema como encontrar as bibliotecas compartilhadas recém-instaladas. Os sistemas em que isso *não* é necessário incluem FreeBSD, Linux, NetBSD, OpenBSD e Solaris.

O método para definir o caminho de busca da biblioteca compartilhada varia entre as plataformas, mas o método mais amplamente utilizado é definir a variável de ambiente `LD_LIBRARY_PATH` da seguinte forma: Em shells Bourne (`sh`, `ksh`, `bash`, `zsh`):

```
LD_LIBRARY_PATH=/usr/local/pgsql/lib
export LD_LIBRARY_PATH
```

ou em `csh` ou `tcsh`:

```
setenv LD_LIBRARY_PATH /usr/local/pgsql/lib
```

Substitua `/usr/local/pgsql/lib` por qualquer valor que você tenha definido para `--libdir` em [Passo 1](install-make.md#CONFIGURE "Configuration"). Coloque esses comandos em um arquivo de inicialização de shell, como `/etc/profile` ou `~/.bash_profile`. Algumas informações úteis sobre as advertências associadas a esse método podem ser encontradas em <http://xahlee.info/UnixResource_dir/_/ldpath.html>.

Em alguns sistemas, pode ser preferível definir a variável de ambiente `LD_RUN_PATH` *antes* da construção.

Em Cygwin, coloque o diretório da biblioteca no `PATH` ou mova os arquivos do `.dll` para o diretório `bin`.

Se tiver dúvidas, consulte as páginas do manual do seu sistema (talvez `ld.so` ou `rld`). Se receber uma mensagem como:

```
psql: error in loading shared libraries
libpq.so.2.1: cannot open shared object file: No such file or directory
```

Então, esse passo era necessário. Simplesmente cuide disso, então.

Se você está no Linux e tem acesso como root, pode executar:

```
/sbin/ldconfig /usr/local/pgsql/lib
```

(ou um diretório equivalente) após a instalação para permitir que o linkador de tempo de execução encontre as bibliotecas compartilhadas mais rapidamente. Consulte a página do manual de `ldconfig` para obter mais informações. Em FreeBSD, NetBSD e OpenBSD, o comando é:

```
/sbin/ldconfig -m /usr/local/pgsql/lib
```

Outros sistemas não são conhecidos por terem um comando equivalente.

### 17.5.2. Variáveis de ambiente [#](#INSTALL-POST-ENV-VARS)

Se você instalou no `/usr/local/pgsql` ou em algum outro local que não é pesquisado por programas por padrão, você deve adicionar `/usr/local/pgsql/bin` (ou o que você definiu para `--bindir` em [Passo 1](install-make.md#CONFIGURE "Configuration")) em seu `PATH`. Sob estrita obediência, isso não é necessário, mas isso tornará o uso do PostgreSQL muito mais conveniente.

Para fazer isso, adicione o seguinte ao seu arquivo de inicialização do shell, como `~/.bash_profile` (ou `/etc/profile`, se você quiser que ele afete todos os usuários):

```
PATH=/usr/local/pgsql/bin:$PATH
export PATH
```

Se você estiver usando `csh` ou `tcsh`, então use este comando:

```
set path = ( /usr/local/pgsql/bin $path )
```

Para permitir que seu sistema encontre a documentação do homem, você precisa adicionar linhas como as seguintes a um arquivo de inicialização de shell, a menos que você tenha instalado em um local que seja pesquisado por padrão:

```
MANPATH=/usr/local/pgsql/share/man:$MANPATH
export MANPATH
```

As variáveis de ambiente `PGHOST` e `PGPORT` especificam aos aplicativos de cliente o host e o porto do servidor de banco de dados, substituindo os valores padrão compilados. Se você vai executar aplicativos de cliente remotamente, é conveniente que cada usuário que planeja usar o banco de dados defina `PGHOST`. No entanto, isso não é necessário; as configurações podem ser comunicadas via opções de linha de comando para a maioria dos programas de cliente.