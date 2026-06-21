## Capítulo 40. Linguagens Procedimentais

**Índice**

* [40.1. Instalação de Linguagens Procedimentais](xplang-install.md)

O PostgreSQL permite que funções definidas pelo usuário sejam escritas em outros idiomas além do SQL e do C. Esses outros idiomas são genericamente chamados de *linguagens procedimentais* (PLs). Para uma função escrita em uma linguagem procedural, o servidor de banco de dados não tem conhecimento embutido sobre como interpretar o texto fonte da função. Em vez disso, a tarefa é passada para um manipulador especial que conhece os detalhes da linguagem. O manipulador pode realizar todo o trabalho de análise, análise sintática, execução, etc. ele mesmo, ou pode servir como "cola" entre o PostgreSQL e uma implementação existente de uma linguagem de programação. O próprio manipulador é uma função em linguagem C compilada em um objeto compartilhado e carregada sob demanda, assim como qualquer outra função em C.

Atualmente, há quatro linguagens processuais disponíveis na distribuição padrão do PostgreSQL: PL/pgSQL ([Capítulo 41](plpgsql.md)), PL/Tcl ([Capítulo 42](pltcl.md)), PL/Perl ([Capítulo 43](plperl.md)) e PL/Python ([Capítulo 44](plpython.md)). Há linguagens processuais adicionais disponíveis que não estão incluídas na distribuição básica. [Apêndice H](external-projects.md) contém informações sobre como encontrá-las. Além disso, outros idiomas podem ser definidos por usuários; os fundamentos do desenvolvimento de uma nova linguagem processual são abordados em [Capítulo 57](plhandler.md).