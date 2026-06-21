## 40.1. Instalação de Linguagens Procedimentais [#](#XPLANG-INSTALL)

Uma linguagem procedural deve ser “instalada” em cada banco de dados onde ela deve ser usada. Mas as linguagens procedimentais instaladas no banco de dados `template1` estão automaticamente disponíveis em todos os bancos de dados posteriormente criados, uma vez que suas entradas em `template1` serão copiadas por `CREATE DATABASE`. Assim, o administrador do banco de dados pode decidir quais linguagens estão disponíveis em quais bancos de dados e pode tornar algumas linguagens disponíveis por padrão, se desejar.

Para as linguagens fornecidas com a distribuição padrão, é necessário apenas executar `CREATE EXTENSION` *`language_name`* para instalar a linguagem no banco de dados atual. O procedimento manual descrito abaixo é recomendado apenas para instalar linguagens que não foram embaladas como extensões.

**Instalação de Linguagem Procedimental Manual**

Uma linguagem procedural é instalada em um banco de dados em cinco etapas, que deve ser realizada por um superusuário do banco de dados. Na maioria dos casos, os comandos SQL necessários devem ser embalados como o script de instalação de uma “extensão”, para que `CREATE EXTENSION` possa ser usado para executá-los.

1. O objeto compartilhado para o manipulador de linguagem deve ser compilado e instalado em um diretório de biblioteca apropriado. Isso funciona da mesma maneira que a construção e instalação de módulos com funções C definidas pelo usuário padrão; veja [Seção 36.10.5][(xfunc-c.md#DFUNC "36.10.5. Compiling and Linking Dynamically-Loaded Functions")]. Muitas vezes, o manipulador de linguagem dependerá de uma biblioteca externa que forneça o motor real da linguagem de programação; se assim for, ela também deve ser instalada.
2. O manipulador deve ser declarado com o comando

   ```
   CREATE FUNCTION handler_function_name()
       RETURNS language_handler
       AS 'path-to-shared-object'
       LANGUAGE C;
   ```

O tipo especial de retorno de `language_handler` informa ao sistema de banco de dados que esta função não retorna um dos tipos de dados definidos pelo SQL e não é diretamente utilizável em declarações SQL.
3. Opcionalmente, o manipulador de linguagem pode fornecer um manipulador "inline" que executa blocos de código anônimo (comandos `DO` (sql-do.md "DO")) escritos nesta linguagem. Se um manipulador inline for fornecido pelo idioma, declare-o com um comando como

4. Opcionalmente, o manipulador de linguagem pode fornecer uma função "validador" que verifica a definição de uma função quanto à correção sem executá-la na verdade. A função validador é chamada por `CREATE FUNCTION` se ela existir. Se uma função validador é fornecida pelo idioma, declare-a com um comando como

5. Por fim, o PL deve ser declarado com o comando

   ```
   CREATE [TRUSTED] LANGUAGE language_name
       HANDLER handler_function_name
       [INLINE inline_function_name]
       [VALIDATOR validator_function_name] ;
   ```

A palavra-chave opcional `TRUSTED` especifica que a linguagem não concede acesso a dados que o usuário não teria de outra forma. As linguagens confiáveis são projetadas para usuários comuns de banco de dados (aqueles sem privilégios de superusuário) e permitem que eles criem funções e procedimentos com segurança. Como as funções PL são executadas dentro do servidor de banco de dados, a bandeira `TRUSTED` deve ser dada apenas para linguagens que não permitem acesso aos recursos internos do servidor de banco de dados ou ao sistema de arquivos. As linguagens PL/pgSQL, PL/Tcl e PL/Perl são consideradas confiáveis; as linguagens PL/TclU, PL/PerlU e PL/PythonU são projetadas para fornecer funcionalidade ilimitada e *não* devem ser marcadas como confiáveis.

[Exemplo 40.1][(xplang-install.md#XPLANG-INSTALL-EXAMPLE "Example 40.1. Manual Installation of PL/Perl")] mostra como o procedimento de instalação manual funcionaria com o idioma PL/Perl.

**Exemplo 40.1. Instalação manual do PL/Perl**

O comando a seguir indica ao servidor de banco de dados onde encontrar o objeto compartilhado para a função de manipulador de chamadas do PL/Perl:

```
CREATE FUNCTION plperl_call_handler() RETURNS language_handler AS
    '$libdir/plperl' LANGUAGE C;
```

O PL/Perl tem uma função de manipulador inline e uma função de validação, então declaramos essas também:

```
CREATE FUNCTION plperl_inline_handler(internal) RETURNS void AS
    '$libdir/plperl' LANGUAGE C STRICT;

CREATE FUNCTION plperl_validator(oid) RETURNS void AS
    '$libdir/plperl' LANGUAGE C STRICT;
```

O comando:

```
CREATE TRUSTED LANGUAGE plperl
    HANDLER plperl_call_handler
    INLINE plperl_inline_handler
    VALIDATOR plperl_validator;
```

então define que as funções previamente declaradas devem ser invocadas para funções e procedimentos onde o atributo de idioma é `plperl`.

  

Em uma instalação padrão do PostgreSQL, o manipulador para o idioma PL/pgSQL é construído e instalado no diretório "biblioteca"; além disso, o próprio idioma PL/pgSQL é instalado em todos os bancos de dados. Se o suporte Tcl estiver configurado, os manipuladores para PL/Tcl e PL/TclU são construídos e instalados no diretório da biblioteca, mas o próprio idioma não é instalado em nenhum banco de dados por padrão. Da mesma forma, os manipuladores para PL/Perl e PL/PerlU são construídos e instalados se o suporte Perl estiver configurado, e o manipulador PL/PythonU é instalado se o suporte Python estiver configurado, mas esses idiomas não são instalados por padrão.