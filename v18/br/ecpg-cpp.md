## 34.13. Aplicações em C++ [#](#ECPG-CPP)

* [34.13.1. Alcance das variáveis de host](ecpg-cpp.md#ECPG-CPP-SCOPE)
* [34.13.2. Desenvolvimento de aplicativos em C++ com módulo C externo](ecpg-cpp.md#ECPG-CPP-AND-C)

O ECPG tem um suporte limitado para aplicações em C++. Esta seção descreve algumas ressalvas.

O pré-processador `ecpg` recebe um arquivo de entrada escrito em C (ou algo parecido com C) e comandos SQL embutidos, converte os comandos SQL embutidos em trechos de linguagem C e, finalmente, gera um arquivo `.c`. As declarações de arquivo de cabeçalho das funções da biblioteca usadas pelos trechos de linguagem C que o `ecpg` gera são envolvidas em blocos `extern "C" { ... }` quando usadas sob C++, portanto, elas devem funcionar perfeitamente em C++.

No geral, no entanto, o pré-processador `ecpg` só entende C; ele não lida com a sintaxe especial e as palavras reservadas da linguagem C++. Portanto, algum código SQL embutido escrito em código de aplicativo C++ que utiliza recursos complicados específicos do C++ pode não ser pré-processado corretamente ou pode não funcionar conforme o esperado.

Uma maneira segura de usar o código SQL embutido em uma aplicação C++ é ocultar as chamadas ECPG em um módulo C, que o código da aplicação C++ chama para acessar o banco de dados, e vinculá-las ao resto do código C++. Veja [Seção 34.13.2][(ecpg-cpp.md#ECPG-CPP-AND-C "34.13.2. C++ Application Development with External C Module")] sobre isso.

### 34.13.1. Âmbito das variáveis de hospedeiro [#](#ECPG-CPP-SCOPE)

O pré-processador `ecpg` entende o escopo das variáveis em C. No idioma C, isso é bastante simples, pois o escopo das variáveis é baseado em seus blocos de código. No entanto, no C++, as variáveis de membro de classe são referenciadas em um bloco de código diferente da posição declarada, então o pré-processador `ecpg` não entenderá o escopo das variáveis de membro de classe.

Por exemplo, no caso a seguir, o pré-processador `ecpg` não consegue encontrar nenhuma declaração para a variável `dbname` no método `test`, então ocorrerá um erro.

```
class TestCpp
{
    EXEC SQL BEGIN DECLARE SECTION;
    char dbname[1024];
    EXEC SQL END DECLARE SECTION;

  public:
    TestCpp();
    void test();
    ~TestCpp();
};

TestCpp::TestCpp()
{
    EXEC SQL CONNECT TO testdb1;
    EXEC SQL SELECT pg_catalog.set_config('search_path', '', false); EXEC SQL COMMIT;
}

void Test::test()
{
    EXEC SQL SELECT current_database() INTO :dbname;
    printf("current_database = %s\n", dbname);
}

TestCpp::~TestCpp()
{
    EXEC SQL DISCONNECT ALL;
}
```

Esse código resultará em um erro como este:

```
ecpg test_cpp.pgc
test_cpp.pgc:28: ERROR: variable "dbname" is not declared
```

Para evitar esse problema de escopo, o método `test` poderia ser modificado para usar uma variável local como armazenamento intermediário. Mas essa abordagem é apenas uma solução precária, porque simplifica o código e reduz o desempenho.

```
void TestCpp::test()
{
    EXEC SQL BEGIN DECLARE SECTION;
    char tmp[1024];
    EXEC SQL END DECLARE SECTION;

    EXEC SQL SELECT current_database() INTO :tmp;
    strlcpy(dbname, tmp, sizeof(tmp));

    printf("current_database = %s\n", dbname);
}
```

### 34.13.2. Desenvolvimento de Aplicativos em C++ com Módulo C Externo [#](#ECPG-CPP-AND-C)

Se você entender essas limitações técnicas do pré-processador `ecpg` em C++, pode chegar à conclusão de que vincular objetos C e objetos C++ na fase de vinculação para permitir que aplicativos C++ usem recursos do ECPG pode ser melhor do que escrever alguns comandos SQL embutidos diretamente no código em C++. Esta seção descreve uma maneira de separar alguns comandos SQL embutidos do código do aplicativo em C++ com um exemplo simples. Neste exemplo, o aplicativo é implementado em C++, enquanto C e ECPG são usados para se conectar ao servidor PostgreSQL.

Três tipos de arquivos devem ser criados: um arquivo C (`*.pgc`), um arquivo de cabeçalho e um arquivo em C++;

`test_mod.pgc` [#](#ECPG-CPP-AND-C-TEST-MOD-PGC): Um módulo de subrotina para executar comandos SQL embutidos em C. Ele será convertido em `test_mod.c` pelo pré-processador.

``` #include "test_mod.h" #include <stdio.h>

void db_connect() { EXEC SQL CONNECT TO testdb1; EXEC SQL SELECT pg_catalog.set_config('search_path', '', false); EXEC SQL COMMIT; }

void db_test() { EXEC SQL BEGIN DECLARE SECTION; char dbname[1024]; EXEC SQL END DECLARE SECTION;

EXEC SQL SELECT current_database() INTO :dbname; printf("current_database = %s\n", dbname); }

void db_disconnect() { EXEC SQL DISCONNECT ALL; }
    ```

`test_mod.h` [#](#ECPG-CPP-AND-C-TEST-MOD-H): Um arquivo de cabeçalho com as declarações das funções no módulo C (`test_mod.pgc`). Ele é incluído por `test_cpp.cpp`. Este arquivo deve ter um bloco `extern "C"` ao redor das declarações, porque ele será vinculado a partir do módulo C++.

``` #ifdef __cplusplus extern "C" { #endif

void db_connect(); void db_test(); void db_disconnect();

#ifdef __cplusplus } #endif
    ```

`test_cpp.cpp` [#](#ECPG-CPP-AND-C-TEST-CPP-CPP)
:   O código principal do aplicativo, incluindo a rotina `main`, e, neste exemplo, uma classe em C++.

    ```
    #include "test_mod.h"

    class TestCpp { public: TestCpp(); void test(); ~TestCpp(); };

    TestCpp::TestCpp() { db_connect(); }

    void TestCpp::test() { db_test(); }

    TestCpp::~TestCpp() { db_disconnect(); }

    int main(void) { TestCpp *t = new TestCpp();

        t->test(); return 0; }
    ```

Para construir o aplicativo, proceda da seguinte forma. Converte `test_mod.pgc` em `test_mod.c` executando `ecpg`, e gere `test_mod.o` compilando `test_mod.c` com o compilador C:

```
ecpg -o test_mod.c test_mod.pgc cc -c test_mod.c -o test_mod.o
```

Em seguida, gere `test_cpp.o` compilando
`test_cpp.cpp` com o compilador C++.

```
c++ -c test_cpp.cpp -o test_cpp.o
```

Por fim, ligue esses arquivos de objeto, `test_cpp.o` e `test_mod.o`, em um executável, usando o driver do compilador de C++.

```
c++ test_cpp.o test_mod.o -lecpg -o test_cpp
```
