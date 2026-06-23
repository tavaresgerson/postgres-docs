## 45.5. Visibilidade das Alterações de Dados [#](#SPI-VISIBILITY)

As seguintes regras regem a visibilidade das alterações de dados em funções que utilizam SPI (ou qualquer outra função C):

* Durante a execução de um comando SQL, quaisquer alterações de dados feitas pelo comando são invisíveis para o próprio comando. Por exemplo, em:

```
INSERT INTO a SELECT * FROM a;
```

As linhas inseridas são invisíveis para a parte `SELECT`.
* As alterações feitas por um comando C são visíveis para todos os comandos que são iniciados após C, independentemente de serem iniciados dentro de C (durante a execução de C) ou após C ter sido concluído.
* Os comandos executados via SPI dentro de uma função chamada por um comando SQL (seja uma função comum ou um gatilho) seguem uma das regras acima, dependendo da bandeira de leitura/escrita passada para o SPI. Os comandos executados em modo de leitura apenas seguem a primeira regra: eles não podem ver as alterações do comando que os solicitou. Os comandos executados em modo de leitura e escrita seguem a segunda regra: eles podem ver todas as alterações feitas até o momento.
* Todos os idiomas processuais padrão definem o modo de leitura e escrita do SPI dependendo do atributo de volatilidade da função. Os comandos das funções `STABLE` e `IMMUTABLE` são feitos em modo de leitura apenas, enquanto os comandos das funções `VOLATILE` são feitos em modo de leitura e escrita. Embora os autores de funções C sejam capazes de violar essa convenção, é improvável que seja uma boa ideia fazer isso.

A próxima seção contém um exemplo que ilustra a aplicação dessas regras.