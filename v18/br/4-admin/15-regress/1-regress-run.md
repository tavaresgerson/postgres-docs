## 31.1. Realizar os testes [#](#REGRESS-RUN)

* [31.1.1. Executar os testes em uma instalação temporária](regress-run.md#REGRESS-RUN-TEMP-INST)
* [31.1.2. Executar os testes em uma instalação existente](regress-run.md#REGRESS-RUN-EXISTING-INST)
* [31.1.3. Suítes de teste adicionais](regress-run.md#REGRESS-ADDITIONAL)
* [31.1.4. Local e codificação](regress-run.md#REGRESS-RUN-LOCALE)
* [31.1.5. Configurações personalizadas do servidor](regress-run.md#REGRESS-RUN-CUSTOM-SETTINGS)
* [31.1.6. Testes extras](regress-run.md#REGRESS-RUN-EXTRA-TESTS)

Os testes de regressão podem ser executados contra um servidor já instalado e em funcionamento, ou usando uma instalação temporária dentro da árvore de construção. Além disso, há um modo “paralelo” e um modo “sequencial” para executar os testes. O método sequencial executa cada script de teste sozinho, enquanto o método paralelo inicia vários processos de servidor para executar grupos de testes em paralelo. O teste paralelo adiciona a confiança de que a comunicação e o bloqueio entre processos estão funcionando corretamente. Alguns testes podem ser executados sequencialmente mesmo no modo “paralelo”, caso isso seja necessário pelo teste.

### 31.1.1. Executar os testes em uma instalação temporária [#](#REGRESS-RUN-TEMP-INST)

Para executar os testes de regressão paralelos após a construção, mas antes da instalação, digite:

```
make check
```

no diretório de nível superior. (Ou você pode mudar para `src/test/regress` e executar o comando lá.) Os testes que são executados em paralelo são prefixados com “+”, e os testes que são executados sequencialmente são prefixados com “-”. No final, você deve ver algo como:

```
# All 213 tests passed.
```

ou, de outra forma, uma nota sobre quais testes falharam. Veja [Seção 31.2] abaixo antes de assumir que uma “falha” representa um problema sério.

Como este método de teste executa um servidor temporário, ele não funcionará se você tiver feito a compilação como usuário root, uma vez que o servidor não será iniciado como root. O procedimento recomendado é não fazer a compilação como usuário root, ou então realizar o teste após completar a instalação.

Se você configurou o PostgreSQL para instalar em um local onde já existe uma instalação anterior do PostgreSQL, e você realiza `make check` antes de instalar a nova versão, você pode encontrar que os testes falham porque os novos programas tentam usar as bibliotecas compartilhadas já instaladas. (Os sintomas típicos são queixas sobre símbolos indefinidos.) Se você deseja executar os testes antes de sobrescrever a instalação antiga, você precisará construir com `configure --disable-rpath`. No entanto, não é recomendado que você use essa opção para a instalação final.

O teste de regressão paralela começa a executar vários processos sob seu ID de usuário. Atualmente, a concorrência máxima é de vinte scripts de teste paralelos, o que significa quarenta processos: há um processo do servidor e um processo psql para cada script de teste. Portanto, se seu sistema aplicar um limite por usuário no número de processos, certifique-se de que esse limite seja de pelo menos cinquenta ou mais, caso contrário, você pode obter falhas que parecem aleatórias no teste paralelo. Se você não está em condições de aumentar o limite, pode reduzir o grau de paralelismo definindo o parâmetro `MAX_CONNECTIONS`. Por exemplo:

```
make MAX_CONNECTIONS=10 check
```

não executa mais de dez testes simultaneamente.

### 31.1.2. Executar os testes em uma instalação existente [#](#REGRESS-RUN-EXISTING-INST)

Para executar os testes após a instalação (consulte [Capítulo 17](installation.md)), inicialize um diretório de dados e inicie o servidor conforme explicado em [Capítulo 18](runtime.md), em seguida, digite:

```
make installcheck
```

ou para um teste paralelo:

```
make installcheck-parallel
```

Os testes esperam entrar em contato com o servidor no host local e o número de porta padrão, a menos que haja uma orientação diferente das variáveis de ambiente `PGHOST` e `PGPORT`. Os testes serão executados em um banco de dados denominado `regression`; qualquer banco de dados existente com esse nome será descartado.

Os testes também criarão temporariamente alguns objetos em todo o clúster, como papéis, espaços de tabela e assinaturas. Esses objetos terão nomes que começam com `regress_`. Tenha cuidado ao usar o modo `installcheck` em uma instalação que tenha quaisquer objetos globais reais com nomes desse tipo.

### 31.1.3. Suítes de Teste Adicionais [#](#REGRESS-ADDITIONAL)

Os comandos `make check` e `make installcheck` executam apenas os testes de regressão "básicos", que testam a funcionalidade embutida do servidor PostgreSQL. A distribuição de origem contém muitas suítes de teste adicionais, a maioria delas relacionadas a funcionalidades adicionais, como linguagens procedimentais opcionais.

Para executar todas as suítes de teste aplicáveis aos módulos que foram selecionados para serem construídos, incluindo os testes básicos, digite um desses comandos no topo da árvore de construção:

```
make check-world
make installcheck-world
```

Esses comandos executam os testes usando servidores temporários ou um servidor já instalado, respectivamente, assim como explicado anteriormente para `make check` e `make installcheck`. Outras considerações são as mesmas explicadas anteriormente para cada método. Note que `make check-world` constrói uma instância separada (diretório de dados temporário) para cada módulo testado, portanto, requer mais tempo e espaço em disco do que `make installcheck-world`.

Em uma máquina moderna com múltiplos núcleos de CPU e sem limitações rígidas do sistema operacional, é possível fazer as coisas se tornarem substancialmente mais rápidas com paralelismo. A receita que a maioria dos desenvolvedores do PostgreSQL realmente usa para executar todos os testes é algo como

```
make check-world -j8 >/dev/null
```

com um limite `-j` próximo ou um pouco mais do que o número de núcleos disponíveis. Descartar o stdout elimina conversas que não são interessantes quando você só quer verificar o sucesso. (Em caso de falha, as mensagens de stderr geralmente são suficientes para determinar onde procurar mais a fundo.)

Como alternativa, você pode executar conjuntos de testes individuais digitando `make check` ou `make installcheck` no subdiretório apropriado da árvore de construção. Tenha em mente que `make installcheck` assume que você instalou o(s) módulo(s) relevante(s), não apenas o servidor principal.

Os testes adicionais que podem ser solicitados dessa forma incluem:

* Testes de regressão para linguagens processuais opcionais. Esses estão localizados em `src/pl`.
* Testes de regressão para módulos `contrib`, localizados em `contrib`. Nem todos os módulos `contrib` têm testes.
* Testes de regressão para as bibliotecas de interface, localizadas em `src/interfaces/libpq/test` e `src/interfaces/ecpg/test`.
* Testes para métodos de autenticação suportados pelo núcleo, localizados em `src/test/authentication`. (Veja abaixo para testes adicionais relacionados à autenticação.)
* Testes que enfatizam o comportamento de sessões concorrentes, localizados em `src/test/isolation`.
* Testes para recuperação de falhas e replicação física, localizados em `src/test/recovery`.
* Testes para replicação lógica, localizados em `src/test/subscription`.
* Testes de programas de cliente, localizados em `src/bin`.

Ao usar o modo `installcheck`, esses testes criarão e destruirão bancos de dados de teste cujos nomes incluem `regression`, por exemplo, `pl_regression` ou `contrib_regression`. Tenha cuidado ao usar o modo `installcheck` com uma instalação que tenha quaisquer bancos de dados não de teste com nomes assim.

Alguns desses conjuntos de testes auxiliares utilizam a infraestrutura TAP explicada em [Seção 31.4](regress-tap.md). Os testes baseados em TAP são executados apenas quando o PostgreSQL foi configurado com a opção `--enable-tap-tests`. Isso é recomendado para desenvolvimento, mas pode ser omitido se não houver uma instalação adequada do Perl.

Alguns conjuntos de testes não são executados por padrão, porque não são seguros para serem executados em um sistema multiusuário, porque exigem software especial ou porque são intensivos em recursos. Você pode decidir quais conjuntos de testes executar adicionalmente, definindo a variável de ambiente `make` ou `PG_TEST_EXTRA` como uma lista separada por espaços em branco, por exemplo:

```
make check-world PG_TEST_EXTRA='kerberos ldap ssl load_balance libpq_encryption'
```

Os seguintes valores são atualmente suportados:

`kerberos`: Realiza o conjunto de testes sob `src/test/kerberos`. Isso requer uma instalação MIT Kerberos e abre soquetes de escuta TCP/IP.

`ldap`: Realiza o conjunto de testes sob `src/test/ldap`. Isso requer uma instalação do OpenLDAP e abre soquetes de escuta TCP/IP.

`libpq_encryption`: Realiza o teste `src/interfaces/libpq/t/005_negotiate_encryption.pl`. Isso abre os sockets de escuta TCP/IP. Se `PG_TEST_EXTRA` também incluir `kerberos`, testes adicionais que exigem uma instalação MIT Kerberos são ativados.

`load_balance`: Realiza o teste `src/interfaces/libpq/t/004_load_balance_dns.pl`. Isso requer a edição do arquivo do sistema `hosts` e a abertura de soquetes de escuta TCP/IP.

`oauth`: Realiza o conjunto de testes sob `src/test/modules/oauth_validator`. Isso abre soquetes de escuta TCP/IP para um servidor de teste que executa HTTPS.

`regress_dump_restore`: Realiza um conjunto de testes adicionais em `src/bin/pg_upgrade/t/002_pg_upgrade.pl` que cicla o banco de dados de regressão através de `pg_dump`/`pg_restore`. Não é ativado por padrão porque é intensivo em recursos.

`sepgsql`: Realiza o conjunto de testes sob `contrib/sepgsql`. Isso requer um ambiente SELinux configurado de uma maneira específica; consulte [Seção F.40.3](sepgsql.md#SEPGSQL-REGRESSION "F.40.3. Regression Tests").

`ssl`: Realiza o conjunto de testes sob `src/test/ssl`. Isso abre sockets de escuta TCP/IP.

`wal_consistency_checking`: Usa `wal_consistency_checking=all` durante a execução de certos testes sob `src/test/recovery`. Não é ativado por padrão porque é intensivo em recursos.

`xid_wraparound`: Realiza o conjunto de testes sob `src/test/modules/xid_wraparound`. Não é ativado por padrão porque é intensivo em recursos.

Os testes para recursos que não são suportados pela configuração atual de compilação não são executados, mesmo que eles estejam mencionados em `PG_TEST_EXTRA`.

Além disso, existem testes em `src/test/modules` que serão executados por `make check-world`, mas não por `make installcheck-world`. Isso ocorre porque eles instalam extensões não de produção ou têm outros efeitos colaterais que são considerados indesejáveis para uma instalação de produção. Você pode usar `make install` e `make installcheck` em um desses subdiretórios, se desejar, mas não é recomendado fazer isso com um servidor não de teste.

### 31.1.4. Local e codificação [#](#REGRESS-RUN-LOCALE)

Por padrão, os testes que utilizam uma instalação temporária usam o local definido no ambiente atual e o codificação de banco de dados correspondente, conforme determinado por `initdb`. Pode ser útil testar diferentes locais, definindo as variáveis de ambiente apropriadas, por exemplo:

```
make check LANG=C
make check LC_COLLATE=en_US.utf8 LC_CTYPE=fr_CA.utf8
```

Por razões de implementação, definir `LC_ALL` não funciona para esse propósito; todas as outras variáveis de ambiente relacionadas ao local funcionam.

Ao testar contra uma instalação existente, o local é determinado pelo clúster de banco de dados existente e não pode ser definido separadamente para a execução do teste.

Você também pode escolher explicitamente o codificação do banco de dados, definindo a variável `ENCODING`, por exemplo:

```
make check LANG=C ENCODING=EUC_JP
```

Definir o codificação do banco de dados dessa maneira geralmente só faz sentido se o local for C; caso contrário, a codificação é escolhida automaticamente a partir do local, e especificar uma codificação que não corresponda ao local resultará em um erro.

O codificação do banco de dados pode ser definida para testes contra uma instalação temporária ou uma instalação existente, embora, no último caso, ela deve ser compatível com o idioma da instalação.

### 31.1.5. Configurações personalizadas do servidor [#](#REGRESS-RUN-CUSTOM-SETTINGS)

Existem várias maneiras de usar configurações personalizadas do servidor ao executar uma suíte de testes. Isso pode ser útil para habilitar registros adicionais, ajustar limites de recursos ou habilitar verificações adicionais de tempo de execução, como [debug_discard_caches](runtime-config-developer.md#GUC-DEBUG-DISCARD-CACHES). Mas observe que nem todos os testes podem ser esperados para passar de forma limpa com configurações arbitrárias.

Opções adicionais podem ser passadas aos vários comandos `initdb` que são executados internamente durante a configuração do teste usando a variável de ambiente `PG_TEST_INITDB_EXTRA_OPTS`. Por exemplo, para executar um teste com verificações de checksums habilitadas e um tamanho de segmento WAL personalizado e configuração `work_mem`, use:

```
make check PG_TEST_INITDB_EXTRA_OPTS='-k --wal-segsize=4 -c work_mem=50MB'
```

Para a suíte de testes de regressão principal e outros testes impulsionados por `pg_regress`, configurações personalizadas do servidor de execução também podem ser definidas na variável de ambiente `PGOPTIONS` (para configurações que permitem isso), por exemplo:

```
make check PGOPTIONS="-c debug_parallel_query=regress -c work_mem=50MB"
```

(Isso utiliza a funcionalidade fornecida pelo libpq; consulte [opções](libpq-connect.md#LIBPQ-CONNECT-OPTIONS) para detalhes.)

Ao executar em uma instalação temporária, as configurações personalizadas também podem ser definidas fornecendo um pré-escrito `postgresql.conf`:

```
echo 'log_checkpoints = on' > test_postgresql.conf
echo 'work_mem = 50MB' >> test_postgresql.conf
make check EXTRA_REGRESS_OPTS="--temp-config=test_postgresql.conf"
```

### 31.1.6. Testes extras [#](#REGRESS-RUN-EXTRA-TESTS)

A suíte de testes de regressão principal contém alguns arquivos de teste que não são executados por padrão, porque podem ser dependentes da plataforma ou demorar muito tempo para serem executados. Você pode executar esses ou outros arquivos de teste adicionais definindo a variável `EXTRA_TESTS`. Por exemplo, para executar o teste `numeric_big`:

```
make check EXTRA_TESTS=numeric_big
```
