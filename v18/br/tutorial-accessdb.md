## 1.4. Acessando um banco de dados [#](#TUTORIAL-ACCESSDB)

Depois de criar um banco de dados, você pode acessá-lo da seguinte forma:

* Executar o programa de terminal interativo PostgreSQL, chamado *psql*, que permite inserir, editar e executar comandos SQL de forma interativa.
* Usar uma ferramenta gráfica existente, como pgAdmin ou uma suite de escritório com suporte a ODBC ou JDBC, para criar e manipular um banco de dados. Essas possibilidades não são abordadas neste tutorial.
* Escrever uma aplicação personalizada, usando uma das várias vinculações de linguagem disponíveis. Essas possibilidades são discutidas mais adiante em [Parte IV][(client-interfaces.md "Part IV. Client Interfaces")].

Você provavelmente quer iniciar o `psql` para experimentar os exemplos neste tutorial. Ele pode ser ativado para o banco de dados `mydb` digitando o comando:

```
$ psql mydb
```

Se você não fornecer o nome do banco de dados, ele será predefinido com o nome da sua conta de usuário. Você já descobriu esse esquema na seção anterior usando `createdb`.

Em `psql`, você será recebido com a seguinte mensagem:

```
psql (18.4)
Type "help" for help.

mydb=>
```

A última linha também pode ser:

```
mydb=#
```

Isso significaria que você é um superusuário do banco de dados, o que provavelmente é o caso se você instalou a instância do PostgreSQL por si mesmo. Ser um superusuário significa que você não está sujeito a controles de acesso. Para os propósitos deste tutorial, isso não é importante.

Se você encontrar problemas ao iniciar `psql`, volte para a seção anterior. Os diagnósticos de `createdb` e `psql` são semelhantes, e se o primeiro funcionasse, o segundo também deveria funcionar.

A última linha impressa por `psql` é o prompt, e indica que `psql` está ouvindo você e que você pode digitar consultas SQL em um espaço de trabalho mantido por `psql`. Experimente esses comandos:

```
mydb=> SELECT version();
                                         version
-------------------------------------------------------------------​-----------------------
 PostgreSQL 18.4 on x86_64-pc-linux-gnu, compiled by gcc (Debian 4.9.2-10) 4.9.2, 64-bit
(1 row)

mydb=> SELECT current_date;
    date
------------
 2016-01-07
(1 row)

mydb=> SELECT 2 + 2;
 ?column?
----------
        4
(1 row)
```

O programa `psql` possui vários comandos internos que não são comandos SQL. Eles começam com o caractere barra invertida, “[[`\`]”. Por exemplo, você pode obter ajuda sobre a sintaxe de vários comandos SQL do PostgreSQL digitando:

```
mydb=> \h
```

Para sair do `psql`, digite:

```
mydb=> \q
```

e `psql` encerrará e retornará ao seu shell de comando. (Para mais comandos internos, digite `\?` no prompt `psql`. As capacidades completas de `psql` estão documentadas em [psql](app-psql.md "psql"). Neste tutorial, não usaremos esses recursos explicitamente, mas você pode usá-los por si mesmo quando for útil.