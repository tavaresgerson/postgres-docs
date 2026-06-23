## 31.5. Exame de Cobertura de Testes [#](#REGRESS-COVERAGE)

* [31.5.1. Cobertura com Autoconf e Make](regress-coverage.md#REGRESS-COVERAGE-CONFIGURE)
* [31.5.2. Cobertura com Meson](regress-coverage.md#REGRESS-COVERAGE-MESON)

O código-fonte do PostgreSQL pode ser compilado com instrumentação de testes de cobertura, de modo que seja possível examinar quais partes do código são cobertas pelos testes de regressão ou qualquer outra suíte de teste que seja executada com o código. Isso é atualmente suportado ao compilar com o GCC e requer os pacotes `gcov` e `lcov`.

### 31.5.1. Cobertura com Autoconf e Make [#](#REGRESS-COVERAGE-CONFIGURE)

Um fluxo de trabalho típico é o seguinte:

```
./configure --enable-coverage ... OTHER OPTIONS ...
make
make check # or other test suite
make coverage-html
```

Em seguida, aponte seu navegador HTML para `coverage/index.html`.

Se você não tem `lcov` ou prefere saída de texto em vez de um relatório HTML, você pode executar

```
make coverage
```

em vez de `make coverage-html`, que produzirá arquivos de saída `.gcov` para cada arquivo de origem relevante para o teste. (`make coverage` e `make coverage-html` irão sobrepor os arquivos uns dos outros, então misturá-los pode ser confuso.)

Você pode executar vários testes diferentes antes de fazer o relatório de cobertura; as contagens de execução se acumularão. Se você quiser redefinir as contagens de execução entre as execuções de teste, execute:

```
make coverage-clean
```

Você pode executar o comando `make coverage-html` ou `make coverage` em um subdiretório, se desejar um relatório de cobertura apenas para uma parte da árvore de código.

Use `make distclean` para limpar quando estiver pronto.

### 31.5.2. Cobertura com Meson [#](#REGRESS-COVERAGE-MESON)

Um fluxo de trabalho típico é o seguinte:

```
meson setup -Db_coverage=true ... OTHER OPTIONS ... builddir/
meson compile -C builddir/
meson test -C builddir/
cd builddir/
ninja coverage-html
```

Em seguida, aponte seu navegador HTML para `./meson-logs/coveragereport/index.html`.

Você pode executar vários testes diferentes antes de fazer o relatório de cobertura; as contagens de execução se acumularão.