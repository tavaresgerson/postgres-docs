## J.6. Guia de Estilo [#](#DOCGUIDE-STYLE)

* [J.6.1. Páginas de Referência](docguide-style.md#DOCGUIDE-STYLE-REF-PAGES)

### J.6.1. Páginas de referência [#](#DOCGUIDE-STYLE-REF-PAGES)

As páginas de referência devem seguir um layout padrão. Isso permite que os usuários encontrem as informações desejadas mais rapidamente e também incentiva os autores a documentarem todos os aspectos relevantes de um comando. A consistência não é apenas desejada entre as páginas de referência do PostgreSQL, mas também com as páginas de referência fornecidas pelo sistema operacional e outros pacotes. Portanto, as diretrizes a seguir foram desenvolvidas. Elas são, na maior parte, consistentes com diretrizes semelhantes estabelecidas por vários sistemas operacionais.

As páginas de referência que descrevem comandos executáveis devem conter as seguintes seções, nessa ordem. Seções que não se aplicam podem ser omitidas. Seções adicionais de nível superior devem ser usadas apenas em circunstâncias especiais; muitas vezes essa informação pertence à seção “Uso”.

Nome [#](#DOCGUIDE-STYLE-REF-PAGES-NAME): Esta seção é gerada automaticamente. Ela contém o nome do comando e um resumo de meia frase sobre sua funcionalidade.

Sinopse [#](#DOCGUIDE-STYLE-REF-PAGES-SYNOPSIS): Esta seção contém o diagrama de sintaxe do comando. A sinopse normalmente não deve listar cada opção da linha de comando; isso é feito abaixo. Em vez disso, liste os principais componentes da linha de comando, como onde os arquivos de entrada e saída vão.

Descrição [#](#DOCGUIDE-STYLE-REF-PAGES-DESCRIPTION): Vários parágrafos explicando o que o comando faz.

Opções [#](#DOCGUIDE-STYLE-REF-PAGES-OPTIONS): Uma lista que descreve cada opção de linha de comando. Se houver muitas opções, subseções podem ser usadas.

Status de saída [#](#DOCGUIDE-STYLE-REF-PAGES-EXIT-STATUS): Se o programa usa 0 para sucesso e não zero para falha, então você não precisa documentá-lo. Se houver um significado por trás dos diferentes códigos de saída não nulos, liste-os aqui.

Uso [#](#DOCGUIDE-STYLE-REF-PAGES-USAGE): Descreva qualquer sublinguagem ou interface de execução do programa. Se o programa não for interativo, essa seção geralmente pode ser omitida. Caso contrário, essa seção é uma seção geral para descrever recursos de execução. Use subseções, se apropriado.

Ambiente [#](#DOCGUIDE-STYLE-REF-PAGES-ENVIRONMENT): Liste todas as variáveis de ambiente que o programa pode usar. Tente ser completo; até mesmo variáveis aparentemente triviais, como `SHELL`, podem ser de interesse para o usuário.

Arquivos [#](#DOCGUIDE-STYLE-REF-PAGES-FILES): Liste todos os arquivos que o programa pode acessar implicitamente. Ou seja, não liste arquivos de entrada e saída que foram especificados na linha de comando, mas liste arquivos de configuração, etc.

Diagnóstico [#](#DOCGUIDE-STYLE-REF-PAGES-DIAGNOSTICS): Explique qualquer saída incomum que o programa possa criar. Evite listar todas as mensagens de erro possíveis. Isso é muito trabalho e tem pouca utilidade na prática. Mas, se, por exemplo, as mensagens de erro tiverem um formato padrão que o usuário possa analisar, seria o lugar para explicá-lo.

Notas [#](#DOCGUIDE-STYLE-REF-PAGES-NOTES): Qualquer coisa que não se encaixe em outro lugar, mas, em particular, bugs, falhas de implementação, considerações de segurança e problemas de compatibilidade.

Exemplos [#](#DOCGUIDE-STYLE-REF-PAGES-EXAMPLES): Exemplos

História [#](#DOCGUIDE-STYLE-REF-PAGES-HISTORY): Se houver alguns marcos importantes na história do programa, eles podem ser listados aqui. Geralmente, essa seção pode ser omitida.

Autor [#](#DOCGUIDE-STYLE-REF-PAGES-AUTHOR): Autor (usado apenas na seção contrib)

Veja também [#](#DOCGUIDE-STYLE-REF-PAGES-SEE-ALSO): Referências cruzadas, listadas na seguinte ordem: outras páginas de referência de comandos do PostgreSQL, páginas de referência de comandos SQL do PostgreSQL, citação de manuais do PostgreSQL, outras páginas de referência (por exemplo, sistema operacional, outros pacotes), outras documentações. Os itens do mesmo grupo são listados alfabeticamente.

As páginas de referência que descrevem comandos SQL devem conter as seguintes seções: Nome, Sinopse, Descrição, Parâmetros, Saídas, Notas, Exemplos, Compatibilidade, Histórico, Veja também. A seção de Parâmetros é semelhante à seção de Opções, mas há mais liberdade sobre quais cláusulas do comando podem ser listadas. A seção de Saídas é necessária apenas se o comando retornar algo além de uma tag padrão de conclusão de comando. A seção de Compatibilidade deve explicar até que ponto este comando está em conformidade com o (s) padrão (s) SQL, ou com qual outro sistema de banco de dados é compatível. A seção Veja também de comandos SQL deve listar comandos SQL antes de referências cruzadas para programas.