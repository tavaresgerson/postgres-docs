## J.5. Criação de documentação [#](#DOCGUIDE-AUTHORING)

* [J.5.1. Emacs](docguide-authoring.md#DOCGUIDE-AUTHORING-EMACS)

As fontes de documentação são mais convenientemente modificadas com um editor que tenha um modo para edição de XML, e ainda mais se ele tiver alguma consciência sobre os idiomas de esquema XML, para que possa saber sobre a sintaxe do DocBook especificamente.

Observe que, por razões históricas, os arquivos de fonte da documentação são nomeados com a extensão `.sgml`, mesmo que agora sejam arquivos XML. Portanto, você pode precisar ajustar a configuração do seu editor para definir o modo correto.

### J.5.1. Emacs [#](#DOCGUIDE-AUTHORING-EMACS)

O modo nXML, que vem com o Emacs, é o modo mais comum para editar documentos XML com o Emacs. Ele permitirá que você use o Emacs para inserir tags e verificar a consistência do marcado, e suporta DocBook de forma pré-definida. Verifique o manual [nXML][(https://www.gnu.org/software/emacs/manual/html_mono/nxml-mode.html)] para documentação detalhada.

`src/tools/editors/emacs.samples` contém configurações recomendadas para este modo.