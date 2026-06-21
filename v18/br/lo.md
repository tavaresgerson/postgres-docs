## F.21. lo — gerenciar objetos grandes [#](#LO)

* [F.21.1. Razão][(lo.md#LO-RATIONALE)
* [F.21.2. Como usá-lo][(lo.md#LO-HOW-TO-USE)
* [F.21.3. Limitações][(lo.md#LO-LIMITATIONS)
* [F.21.4. Autor][(lo.md#LO-AUTHOR)

O módulo `lo` oferece suporte para gerenciar Objetos Grandes (também chamados de LOs ou BLOBs). Isso inclui um tipo de dados `lo` e um gatilho `lo_manage`.

Este módulo é considerado "confiável", ou seja, pode ser instalado por usuários não superusuários que possuem privilégio `CREATE` no banco de dados atual.

### F.21.1. **Razão [#](#LO-RATIONALE)

Um dos problemas com o driver JDBC (e isso afeta também o driver ODBC) é que a especificação assume que as referências a BLOBs (Objetos grandes binários) são armazenadas dentro de uma tabela, e se essa entrada for alterada, o BLOB associado é excluído do banco de dados.

Como o PostgreSQL está configurado, isso não ocorre. Objetos grandes são tratados como objetos em si mesmos; uma entrada de tabela pode fazer referência a um objeto grande pelo OID, mas pode haver várias entradas de tabela fazendo referência ao mesmo OID do objeto grande, então o sistema não exclui o objeto grande apenas porque você muda ou remove uma dessas entradas.

Agora, isso é bom para aplicações específicas do PostgreSQL, mas códigos padrão que utilizam JDBC ou ODBC não irão deletar os objetos, resultando em objetos órfãos — objetos que não são referenciados por nada e simplesmente ocupam espaço em disco.

O módulo `lo` permite corrigir isso ao anexar um gatilho a tabelas que contêm colunas de referência LO. O gatilho essencialmente faz um `lo_unlink` sempre que você exclui ou modifica um valor que faz referência a um objeto grande. Ao usar este gatilho, você está assumindo que há apenas uma referência de banco de dados para qualquer objeto grande que é feito referência em uma coluna controlada por gatilho!

O módulo também fornece um tipo de dados `lo`, que é realmente apenas um [*[domain](glossary.md#GLOSSARY-DOMAIN "Domain")*](glossário.md#GLOSSARY-DOMAIN) sobre o tipo `oid`. Isso é útil para diferenciar as colunas do banco de dados que contêm grandes referências de objetos das que são OIDs de outras coisas. Você não precisa usar o tipo `lo` para usar o gatilho, mas pode ser conveniente usá-lo para acompanhar quais colunas em seu banco de dados representam grandes objetos que você está gerenciando com o gatilho. Também há rumores de que o driver ODBC fica confuso se você não usar `lo` para colunas BLOB.

### F.21.2. Como usá-lo [#](#LO-HOW-TO-USE)

Aqui está um exemplo simples de uso:

```
CREATE TABLE image (title text, raster lo);

CREATE TRIGGER t_raster BEFORE UPDATE OR DELETE ON image
    FOR EACH ROW EXECUTE FUNCTION lo_manage(raster);
```

Para cada coluna que conterá referências únicas para grandes objetos, crie um gatilho `BEFORE UPDATE OR DELETE` e dê o nome da coluna como o único argumento do gatilho. Você também pode restringir o gatilho para executar apenas em atualizações na coluna usando `BEFORE UPDATE OF` *`column_name`*. Se você precisar de várias colunas `lo` na mesma tabela, crie um gatilho separado para cada uma delas, lembrando de dar um nome diferente a cada gatilho na mesma tabela.

### F.21.3. Limitações [#](#LO-LIMITATIONS)

* A eliminação de uma tabela ainda deixará órfãos quaisquer objetos que ela contenha, pois o gatilho não será executado. Você pode evitar isso ao preceder o `DROP TABLE` com `DELETE FROM table`.

`TRUNCATE` tem o mesmo perigo.

Se você já tem, ou suspeita que tem, objetos grandes órfãos, consulte o módulo [vacuumlo](vacuumlo.md) para ajudá-lo a limpá-los. É uma boa ideia executar o vacuumlo ocasionalmente como um backup para o gatilho `lo_manage`. * Alguns frontends podem criar suas próprias tabelas e não criar os gatilhos associados. Além disso, os usuários podem não se lembrar (ou não saber) de criar os gatilhos.

### F.21.4. Autor [#](#LO-AUTHOR)

Peter Mount `<peter@retep.org.uk>`