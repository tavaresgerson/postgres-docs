## 31.4. Testes TAP [#](#REGRESS-TAP)

* [31.4.1. Variáveis de ambiente](regress-tap.md#REGRESS-TAP-VARS)

Vários testes, particularmente os testes do programa cliente sob `src/bin`, utilizam as ferramentas Perl TAP e são executados usando o programa de teste Perl `prove`. Você pode passar opções de linha de comando para `prove` definindo a variável `make`, por exemplo:

```
make -C src/bin check PROVE_FLAGS='--timer'
```

Veja a página do manual de `prove` para mais informações.

A variável `make` `PROVE_TESTS` pode ser usada para definir uma lista de caminhos separados por espaços em branco relativa ao `Makefile` que invoca `prove` para executar o subconjunto especificado de testes em vez do conjunto padrão `t/*.pl`. Por exemplo:

```
make check PROVE_TESTS='t/001_test1.pl t/003_test3.pl'
```

Os testes do TAP exigem o módulo Perl `IPC::Run`. Esse módulo está disponível no [CPAN](https://metacpan.org/dist/IPC-Run) ou em um pacote do sistema operacional. Eles também exigem que o PostgreSQL seja configurado com a opção `--enable-tap-tests`.

De forma genérica, os testes do TAP testarão os executáveis em uma árvore de instalação pré-instalada se você disser `make installcheck`, ou construirá uma nova árvore de instalação local a partir das fontes atuais se você disser `make check`. Em qualquer caso, eles inicializarão uma instância local (diretório de dados) e executarão temporariamente um servidor nela. Alguns desses testes executam mais de um servidor. Assim, esses testes podem ser bastante intensivos em recursos.

É importante perceber que os testes do TAP começarão a testar servidores, mesmo quando você digitar `make installcheck`; isso é diferente da infraestrutura de testes tradicional que não utiliza o TAP, que espera usar um servidor de teste já em execução nesse caso. Alguns subdiretórios do PostgreSQL contêm testes de estilo tradicional e de estilo TAP, o que significa que `make installcheck` produzirá uma mistura de resultados de servidores temporários e do servidor de teste já em execução.

### 31.4.1. Variáveis de ambiente [#](#REGRESS-TAP-VARS)

Os diretórios de dados são nomeados de acordo com o nome do arquivo de teste e serão retidos se um teste falhar. Se a variável de ambiente `PG_TEST_NOCLEAN` estiver definida, os diretórios de dados serão retidos independentemente do status do teste. Por exemplo, reter o diretório de dados independentemente dos resultados do teste ao executar os testes pg_dump:

```
PG_TEST_NOCLEAN=1 make -C src/bin/pg_dump check
```

Essa variável de ambiente também impede que os diretórios temporários do teste sejam removidos.

Muitas operações nas suítes de teste usam um limite de tempo de 180 segundos, o que, em hosts lentos, pode levar a tempos de espera induzidos por carga. Definir a variável de ambiente `PG_TEST_TIMEOUT_DEFAULT` para um número maior mudará o padrão para evitar isso.