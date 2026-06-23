## 29.6. Replicação de Coluna Gerada [#](#LOGICAL-REPLICATION-GENCOLS)

Normalmente, uma tabela no assinante será definida da mesma forma que a tabela do editor, então se a tabela do editor tiver um `GENERATED column` (ddl-generated-columns.md "5.4. Generated Columns"), a tabela do assinante terá uma coluna gerada correspondente. Neste caso, é sempre o valor da coluna gerada da tabela do assinante que é usado.

Por exemplo, observe abaixo que o valor da coluna gerada na tabela de assinantes vem do cálculo da coluna de assinantes.

```
/* pub # */ CREATE TABLE tab_gen_to_gen (a int, b int GENERATED ALWAYS AS (a + 1) STORED);
/* pub # */ INSERT INTO tab_gen_to_gen VALUES (1),(2),(3);
/* pub # */ CREATE PUBLICATION pub1 FOR TABLE tab_gen_to_gen;
/* pub # */ SELECT * FROM tab_gen_to_gen;
 a | b
---+---
 1 | 2
 2 | 3
 3 | 4
(3 rows)

/* sub # */ CREATE TABLE tab_gen_to_gen (a int, b int GENERATED ALWAYS AS (a * 100) STORED);
/* sub # */ CREATE SUBSCRIPTION sub1 CONNECTION 'dbname=test_pub' PUBLICATION pub1;
/* sub # */ SELECT * from tab_gen_to_gen;
 a | b
---+----
 1 | 100
 2 | 200
 3 | 300
(3 rows)
```

De fato, antes da versão 18.0, a replicação lógica não publica as colunas `GENERATED` de forma alguma.

Mas, replicar uma coluna gerada para uma coluna comum pode, às vezes, ser desejável.

### DICA

Essa funcionalidade pode ser útil ao replicar dados para um banco de dados que não é do PostgreSQL via plugin de saída, especialmente se o banco de dados de destino não suportar colunas geradas.

As colunas geradas não são publicadas por padrão, mas os usuários podem optar por publicar colunas geradas armazenadas assim como as colunas regulares.

Existem duas maneiras de fazer isso:

* Defina o parâmetro `PUBLICATION` [`publish_generated_columns`](sql-createpublication.md#SQL-CREATEPUBLICATION-PARAMS-WITH-PUBLISH-GENERATED-COLUMNS) para `stored`. Isso instrui a replicação lógica do PostgreSQL a publicar colunas geradas armazenadas atuais e futuras das tabelas da publicação.
* Especifique uma tabela [lista de colunas](logical-replication-col-lists.md "29.5. Column Lists") para nomear explicitamente quais colunas geradas armazenadas serão publicadas.

Nota

Ao determinar quais colunas da tabela serão publicadas, uma lista de colunas tem precedência, substituindo o efeito do parâmetro `publish_generated_columns`.

O quadro a seguir resume o comportamento quando há colunas geradas envolvidas na replicação lógica. Os resultados são mostrados quando a publicação de colunas geradas não está habilitada e quando está habilitada.

**Tabela 29.2. Resumo dos resultados da replicação**



<table border="1" class="table" summary="Replication Result Summary">
 <colgroup>
  <col/>
  <col/>
  <col/>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th>
    Publish generated columns?
   </th>
   <th>
    Publisher table column
   </th>
   <th>
    Subscriber table column
   </th>
   <th>
    Resultado
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    No
   </td>
   <td>
    GENERATED
   </td>
   <td>
    GENERATED
   </td>
   <td>
    A coluna da tabela de publicador não é replicada. Use o valor da coluna da tabela de assinante gerada.
   </td>
  </tr>
  <tr>
   <td>
    No
   </td>
   <td>
    GENERATED
   </td>
   <td>
    regular
   </td>
   <td>
    A coluna da tabela de publicador não é replicada. Use o valor padrão da coluna regular da tabela de assinante.
   </td>
  </tr>
  <tr>
   <td>
    No
   </td>
   <td>
    GENERATED
   </td>
   <td>
    --missing--
   </td>
   <td>
    A coluna da tabela do editor não é replicada. Nada acontece.
   </td>
  </tr>
  <tr>
   <td>
    Yes
   </td>
   <td>
    GENERATED
   </td>
   <td>
    GENERATED
   </td>
   <td>
    ERRO. Não é suportado.
   </td>
  </tr>
  <tr>
   <td>
    Yes
   </td>
   <td>
    GENERATED
   </td>
   <td>
    regular
   </td>
   <td>
    O valor da coluna da tabela de publicações é replicado para a coluna da tabela de assinantes.
   </td>
  </tr>
  <tr>
   <td>
    Yes
   </td>
   <td>
    GENERATED
   </td>
   <td>
    --missing--
   </td>
   <td>
    ERRO. A coluna é relatada como ausente da tabela do assinante.
   </td>
  </tr>
 </tbody>
</table>










### Aviso

Atualmente, não há suporte para assinaturas que compreendem várias publicações onde a mesma tabela foi publicada com diferentes listas de colunas. Veja [Seção 29.5](logical-replication-col-lists.md).

Essa mesma situação pode ocorrer se uma publicação está publicando colunas geradas, enquanto outra publicação na mesma assinatura não está publicando colunas geradas para a mesma tabela.

Nota

Se o assinante tiver uma versão anterior a 18, a sincronização inicial da tabela não copiará as colunas geradas, mesmo que elas estejam definidas no publicador.