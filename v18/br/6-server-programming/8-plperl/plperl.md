## Capítulo 43. PL/Perl — Linguagem Procedimental Perl

**Índice**

* [43.1. Funções e Argumentos PL/Perl](plperl-funcs.md)
* [43.2. Valores de Dados em PL/Perl](plperl-data.md)
* [43.3. Funções Integradas](plperl-builtins.md)

+ [43.3.1. Acesso a banco de dados a partir de PL/Perl](plperl-builtins.md#PLPERL-DATABASE)
+ [43.3.2. Funções utilitárias em PL/Perl](plperl-builtins.md#PLPERL-UTILITY-FUNCTIONS)

* [43.4. Valores globais no PL/Perl](plperl-global.md)
* [43.5. PL/Perl confiável e não confiável](plperl-trusted.md)
* [43.6. Gatilhos PL/Perl](plperl-triggers.md)
* [43.7. Gatilhos de eventos PL/Perl](plperl-event-triggers.md)
* [43.8. PL/Perl sob o capô](plperl-under-the-hood.md)

+ [43.8.1. Configuração](plperl-under-the-hood.md#PLPERL-CONFIG)
+ [43.8.2. Limitações e Recursos Ausentes](plperl-under-the-hood.md#PLPERL-MISSING)

PL/Perl é uma linguagem procedural carregável que permite que você escreva funções e procedimentos do PostgreSQL na linguagem de programação [Perl](https://www.perl.org).

A principal vantagem de usar PL/Perl é que isso permite o uso, dentro de funções e procedimentos armazenados, dos muitos operadores e funções de "munging" de strings disponíveis para Perl. A análise de strings complexas pode ser mais fácil usando Perl do que com as funções e estruturas de controle de strings fornecidas em PL/pgSQL.

Para instalar PL/Perl em um banco de dados específico, use `CREATE EXTENSION plperl`.

DICA

Se uma língua for instalada no `template1`, todas as bases de dados posteriormente criadas terão a língua instalada automaticamente.

Nota

Os usuários dos pacotes de fonte devem habilitar especialmente a construção do PL/Perl durante o processo de instalação. (Consulte [Capítulo 17] para mais informações.) Os usuários dos pacotes binários podem encontrar o PL/Perl em um subpacote separado.