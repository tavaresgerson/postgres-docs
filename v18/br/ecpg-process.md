## 34.10. Processamento de programas SQL embutidos [#](#ECPG-PROCESS)

Agora que você tem uma ideia de como formar programas de SQL C embutidos, provavelmente quer saber como compilar eles. Antes de compilar, você executa o arquivo através do pré-processador de SQL C embutido, que converte as declarações SQL que você usou em chamadas de função especiais. Após a compilação, você deve vincular com uma biblioteca especial que contém as funções necessárias. Essas funções obtêm informações dos argumentos, executam o comando SQL usando a interface libpq e colocam o resultado nos argumentos especificados para saída.

O programa de pré-processamento é chamado `ecpg` e está incluído em uma instalação normal do PostgreSQL. Os programas de Embedded SQL são tipicamente nomeados com uma extensão `.pgc`. Se você tiver um arquivo de programa chamado `prog1.pgc`, pode pré-processá-lo simplesmente chamando:

```
ecpg prog1.pgc
```

Isso criará um arquivo chamado `prog1.c`. Se seus arquivos de entrada não seguirem o padrão de nomeação sugerido, você pode especificar o arquivo de saída explicitamente usando a opção `-o`.

O arquivo pré-processado pode ser compilado normalmente, por exemplo:

```
cc -c prog1.c
```

Os arquivos de fonte C gerados incluem arquivos de cabeçalho da instalação do PostgreSQL, portanto, se você instalou o PostgreSQL em um local que não é pesquisado por padrão, você deve adicionar uma opção como `-I/usr/local/pgsql/include` à linha de comando de compilação.

Para vincular um programa de SQL incorporado, é necessário incluir a biblioteca `libecpg`, da seguinte forma:

```
cc -o myprog prog1.o prog2.o ... -lecpg
```

Mais uma vez, você pode precisar adicionar uma opção como `-L/usr/local/pgsql/lib` àquela linha de comando.

Você pode usar `pg_config` ou `pkg-config` com o nome do pacote `libecpg` para obter os caminhos para sua instalação.

Se você gerencia o processo de compilação de um projeto maior usando make, pode ser conveniente incluir a seguinte regra implícita em seus arquivos make:

```
ECPG = ecpg

%.c: %.pgc
        $(ECPG) $<
```

A sintaxe completa do comando `ecpg` é detalhada em [ecpg](app-ecpg.md "ecpg").

A biblioteca ecpg é segura em relação a múltiplos fios por padrão. No entanto, você pode precisar usar algumas opções de linha de comando de execução em paralelo para compilar seu código de cliente.