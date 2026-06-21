## H.1. Interfaces do Cliente [#](#EXTERNAL-INTERFACES)

Existem apenas duas interfaces de cliente incluídas na distribuição básica do PostgreSQL:

* [libpq][(libpq.md "Chapter 32. libpq — C Library")] é incluído porque é a principal interface em linguagem C, e porque muitas outras interfaces de cliente são construídas sobre ela.
* [ECPG][(ecpg.md "Chapter 34. ECPG — Embedded SQL in C")] é incluído porque depende da gramática SQL do lado do servidor, e, portanto, é sensível a mudanças no PostgreSQL em si.

Todas as outras interfaces de idioma são projetos externos e são distribuídos separadamente. Uma lista de interfaces de idioma (https://wiki.postgresql.org/wiki/List_of_drivers) é mantida no wiki do PostgreSQL. Note que alguns desses pacotes não são lançados sob a mesma licença que o PostgreSQL. Para mais informações sobre cada interface de idioma, incluindo os termos de licenciamento, consulte seu site e documentação.

<https://wiki.postgresql.org/wiki/List_of_drivers>
