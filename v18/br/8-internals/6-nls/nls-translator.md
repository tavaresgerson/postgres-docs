## 56.1. Para o Tradutor [#](#NLS-TRANSLATOR)

* [56.1.1. Requisitos](nls-translator.md#NLS-TRANSLATOR-REQUIREMENTS)
* [56.1.2. Conceitos](nls-translator.md#NLS-TRANSLATOR-CONCEPTS)
* [56.1.3. Criação e Manutenção de Catálogos de Mensagens](nls-translator.md#NLS-TRANSLATOR-MESSAGE-CATALOGS)
* [56.1.4. Edição dos Arquivos PO](nls-translator.md#NLS-TRANSLATOR-EDITING-PO)

Os programas do PostgreSQL (servidor e cliente) podem emitir suas mensagens no idioma que você prefere, desde que as mensagens tenham sido traduzidas. Criar e manter conjuntos de mensagens traduzidas exige a ajuda de pessoas que falam bem o seu próprio idioma e que desejam contribuir para o esforço do PostgreSQL. Você não precisa ser um programador para fazer isso. Esta seção explica como ajudar.

### 56.1.1. Requisitos [#](#NLS-TRANSLATOR-REQUIREMENTS)

Não vamos julgar suas habilidades linguísticas — esta seção trata de ferramentas de software. Teoricamente, você só precisa de um editor de texto. Mas isso é apenas no caso improvável de você não querer testar suas mensagens traduzidas. Ao configurar sua árvore de origem, certifique-se de usar a opção `--enable-nls`. Isso também verificará a biblioteca libintl e o programa `msgfmt`, que todos os usuários finais precisarão de qualquer maneira. Para testar seu trabalho, siga as partes aplicáveis das instruções de instalação.

Se você deseja iniciar um novo esforço de tradução ou deseja realizar uma fusão de catálogo de mensagens (descrito mais tarde), você precisará dos programas `xgettext` e `msgmerge`, respectivamente, em uma implementação compatível com GNU. Mais tarde, tentaremos organizar isso de modo que, se você usar uma distribuição de fonte embalada, você não precisará de `xgettext`. (Se estiver trabalhando com Git, você ainda precisará dele.) O GNU Gettext 0.10.36 ou posterior é atualmente recomendado.

Sua implementação local do gettext deve vir com sua própria documentação. Parte disso provavelmente está duplicada no que segue, mas para detalhes adicionais, você deve procurar lá.

### 56.1.2. Conceitos [#](#NLS-TRANSLATOR-CONCEPTS)

Os pares de mensagens originais (em inglês) e seus (possivelmente) equivalentes traduzidos são mantidos em *catálogos de mensagens*, um para cada programa (embora programas relacionados possam compartilhar um catálogo de mensagens) e para cada idioma-alvo. Existem dois formatos de arquivo para catálogos de mensagens: o primeiro é o arquivo "PO" (para Objeto Portátil), que é um arquivo de texto simples com sintaxe especial que os tradutores editam. O segundo é o arquivo "MO" (para Objeto Máquina), que é um arquivo binário gerado a partir do respectivo arquivo PO e é usado enquanto o programa internacionalizado é executado. Os tradutores não lidam com arquivos MO; na verdade, dificilmente alguém faz isso.

A extensão do arquivo de catálogo de mensagens não é surpresa para `.po` ou `.mo`. O nome base é o nome do programa que acompanha, ou a língua para a qual o arquivo é destinado, dependendo da situação. Isso é um pouco confuso. Exemplos são `psql.po` (arquivo PO para psql) ou `fr.mo` (arquivo MO em francês).

O formato de arquivo dos arquivos PO é ilustrado aqui:

```
# comment

msgid "original string"
msgstr "translated string"

msgid "more original"
msgstr "another translated"
"string can be broken up like this"

...
```

As linhas msgid são extraídas da fonte do programa. (Não precisam ser, mas essa é a maneira mais comum.) As linhas msgstr são inicialmente vazias e são preenchidas com strings úteis pelo tradutor. As strings podem conter caracteres de escape em estilo C e podem ser continuadas em linhas, como ilustrado. (A próxima linha deve começar no início da linha.)

O caractere # introduz um comentário. Se houver espaço em branco imediatamente após o caractere #, então este é um comentário mantido pelo tradutor. Também podem haver comentários automáticos, que têm um caractere não em branco imediatamente após o #. Estes são mantidos pelas várias ferramentas que operam nos arquivos PO e são destinados a auxiliar o tradutor.

```
#. automatic comment
#: filename.c:1023
#, flags, flags
```

Os comentários estilo # são extraídos do arquivo fonte onde a mensagem é usada. Possivelmente, o programador inseriu informações para o tradutor, como sobre o alinhamento esperado. Os comentários #: indicam os locais exatos onde a mensagem é usada na fonte. O tradutor não precisa olhar para a fonte do programa, mas pode se houver dúvida sobre a tradução correta. Os comentários #, contêm bandeiras que descrevem a mensagem de alguma forma. Atualmente, existem duas bandeiras: `fuzzy` é definida se a mensagem possivelmente ficou desatualizada devido a mudanças na fonte do programa. O tradutor pode então verificar isso e possivelmente remover a bandeira borrada. Note que as mensagens borradas não são disponibilizadas para o usuário final. A outra bandeira é `c-format`, que indica que a mensagem é um modelo de formato estilo `printf`. Isso significa que a tradução também deve ser uma string de formato com o mesmo número e tipo de marcadores. Existem ferramentas que podem verificar isso, que se conectam à bandeira c-format.

### 56.1.3. Criar e manter catálogos de mensagens [#](#NLS-TRANSLATOR-MESSAGE-CATALOGS)

OK, então, como criar um catálogo de mensagens “branco”? Primeiro, vá para o diretório que contém o programa cujas mensagens você deseja traduzir. Se houver um arquivo `nls.mk`, então este programa foi preparado para tradução.

Se já houver alguns arquivos `.po`, então alguém já fez algum trabalho de tradução. Os arquivos são nomeados `language.po`, onde *`language`* é o código de idioma de dois caracteres ISO 639-1 (em minúsculas) (https://www.loc.gov/standards/iso639-2/php/English_list.php), por exemplo, `fr.po` para francês. Se realmente houver necessidade de mais de um esforço de tradução por idioma, os arquivos também podem ser nomeados `language_region.po`, onde *`region`* é o código de país de dois caracteres ISO 3166-1 (em maiúsculas) (https://www.iso.org/iso-3166-country-codes.html), por exemplo, `pt_BR.po` para português no Brasil. Se você encontrar a língua que deseja, pode simplesmente começar a trabalhar nesse arquivo.

Se você precisa iniciar um novo esforço de tradução, então execute primeiro o comando:

```
make init-po
```

Isso criará um arquivo `progname.pot`. (`.pot` para diferenciá-lo dos arquivos PO que estão "em produção". O `T` significa "modelo"). Copie este arquivo para `language.po` e edite-o. Para fazer com que seja conhecido que o novo idioma está disponível, edite também o arquivo `po/LINGUAS` e adicione o código de idioma (ou idioma e país) ao lado dos idiomas já listados, como:

```
de fr
```

(Outros idiomas, claro, podem aparecer.)

Como o programa ou a biblioteca subjacente muda, as mensagens podem ser alteradas ou adicionadas pelos programadores. Nesse caso, você não precisa começar do zero. Em vez disso, execute o comando:

```
make update-po
```

que criará um novo arquivo de catálogo de mensagens em branco (o arquivo pot que você começou) e o combinará com os arquivos PO existentes. Se o algoritmo de combinação não tiver certeza sobre uma mensagem em particular, ele marca como "escamativa", conforme explicado acima. O novo arquivo PO é salvo com a extensão `.po.new`.

### 56.1.4. Edição dos arquivos PO [#](#NLS-TRANSLATOR-EDITING-PO)

Os arquivos PO podem ser editados com um editor de texto comum. Existem também vários editores especializados para arquivos PO que podem ajudar no processo com recursos específicos para tradução. Há (sem surpresa) um modo PO para o Emacs, que pode ser bastante útil.

O tradutor deve apenas alterar a área entre as aspas após a diretiva msgstr, adicionar comentários e alterar a bandeira fuzzy.

Os arquivos PO não precisam ser completamente preenchidos. O software voltará automaticamente para a string original se não houver tradução (ou uma tradução vazia) disponível. Não há problema em enviar traduções incompletas para inclusão na árvore de origem; isso dá espaço para outras pessoas tomarem conhecimento do seu trabalho. No entanto, você é incentivado a dar prioridade à remoção de entradas confusas após fazer uma fusão. Lembre-se de que as entradas confusas não serão instaladas; elas servem apenas como referência para o que pode ser a tradução correta.

Aqui estão algumas coisas que você deve ter em mente ao editar as traduções:

* Certifique-se de que, se o original terminar com uma nova linha, a tradução também termine com uma nova linha. Da mesma forma para tabs, etc.
* Se o original for uma string de formato `printf`, a tradução também precisa ser. A tradução também precisa ter os mesmos especificadores de formato na mesma ordem. Às vezes, as regras naturais da língua tornam isso impossível ou pelo menos inconveniente. Nesse caso, você pode modificar os especificadores de formato da seguinte forma:

```
msgstr "Die Datei %2$s hat %1$u Zeichen."
```

Então, o primeiro marcador de posição usará, na verdade, o segundo argumento da lista. O `digits$` precisa seguir o % imediatamente, antes de qualquer outro manipulador de formato. (Essa característica realmente existe na família de funções `printf`. Você pode não ter ouvido falar disso antes, porque há pouco uso para isso fora da internacionalização de mensagens.)
* Se a string original contiver um erro linguístico, informe isso (ou corrija você mesmo na fonte do programa) e traduza normalmente. A string corrigida pode ser mesclada quando as fontes do programa forem atualizadas. Se a string original contiver um erro factual, informe isso (ou corrija você mesmo) e não traduza. Em vez disso, você pode marcar a string com um comentário no arquivo PO.
* Mantenha o estilo e o tom da string original. Especificamente, as mensagens que não são frases (`cannot open file %s`) provavelmente não devem começar com uma letra maiúscula (se sua língua distingue o caso das letras) ou terminar com um ponto (se sua língua usa marcadores de pontuação). Pode ajudar ler [Seção 55.3](error-style-guide.md "55.3. Error Message Style Guide").
* Se você não sabe o que uma mensagem significa, ou se ela é ambígua, pergunte na lista de correio dos desenvolvedores. Há chances de que usuários finais que falam inglês também não a entendam ou a encontrem ambígua, então é melhor melhorar a mensagem.