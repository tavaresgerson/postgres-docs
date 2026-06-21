## 11.1. Introdução [#](#INDEXES-INTRO)

Suponha que tenhamos uma tabela semelhante a esta:

```
CREATE TABLE test1 (
    id integer,
    content varchar
);
```

e o aplicativo emite muitas consultas do tipo:

```
SELECT content FROM test1 WHERE id = constant;
```

Sem preparação prévia, o sistema teria que analisar toda a tabela `test1`, linha por linha, para encontrar todas as entradas correspondentes. Se houver muitas linhas em `test1` e apenas algumas linhas (talvez zero ou uma) que seriam devolvidas por tal consulta, isso é claramente um método ineficiente. Mas se o sistema foi instruído a manter um índice na coluna `id`, ele pode usar um método mais eficiente para localizar as linhas correspondentes. Por exemplo, ele pode ter que percorrer apenas alguns níveis de profundidade em uma árvore de busca.

Uma abordagem semelhante é usada na maioria dos livros de não ficção: termos e conceitos que são frequentemente pesquisados pelos leitores são coletados em um índice alfabético no final do livro. O leitor interessado pode digitalizar o índice relativamente rapidamente e alternar para a(s) página(s) apropriada(s), em vez de ter que ler todo o livro para encontrar o material de interesse. Assim como é a tarefa do autor antecipar os itens que os leitores provavelmente irão pesquisar, é a tarefa do programador da base de dados prever quais índices serão úteis.

O comando a seguir pode ser usado para criar um índice na coluna `id`, conforme discutido:

```
CREATE INDEX test1_id_index ON test1 (id);
```

O nome `test1_id_index` pode ser escolhido livremente, mas você deve escolher algo que permita lembrar mais tarde para qual índice se tratava.

Para remover um índice, use o comando `DROP INDEX`. Os índices podem ser adicionados e removidos de tabelas a qualquer momento.

Uma vez que um índice seja criado, nenhuma intervenção adicional é necessária: o sistema atualizará o índice quando a tabela for modificada, e usará o índice em consultas quando achar que isso seria mais eficiente do que um varredura sequencial da tabela. Mas você pode ter que executar o comando `ANALYZE` regularmente para atualizar as estatísticas para permitir que o planejador de consultas tome decisões informadas. Consulte [Capítulo 14][(performance-tips.md "Chapter 14. Performance Tips")] para obter informações sobre como descobrir se um índice é usado e quando e por que o planejador pode optar por *não* usar um índice.

Os índices também podem beneficiar os comandos `UPDATE` e `DELETE` com condições de pesquisa. Além disso, os índices podem ser usados em pesquisas de junção. Assim, um índice definido em uma coluna que faz parte de uma condição de junção também pode acelerar significativamente as consultas com junções.

Em geral, os índices do PostgreSQL podem ser usados para otimizar consultas que contenham uma ou mais cláusulas `WHERE` ou `JOIN` do tipo

```
indexed-column indexable-operator comparison-value
```

Aqui, o *`indexed-column`* é a coluna ou expressão em que o índice foi definido. O *`indexable-operator`* é um operador que é membro da *classe de operadores* do índice para a coluna indexada. (Mais detalhes sobre isso aparecem abaixo.) E o *`comparison-value`* pode ser qualquer expressão que não seja volátil e não refira a tabela do índice.

Em alguns casos, o planejador de consultas pode extrair uma cláusula indexável dessa forma de outra construção SQL. Um exemplo simples é que, se a cláusula original fosse

```
comparison-value operator indexed-column
```

então, ele pode ser convertido em uma forma indexável se o original *`operator`* tiver um operador commutativo que seja membro da classe de operadores do índice.

Criar um índice em uma tabela grande pode levar muito tempo. Por padrão, o PostgreSQL permite que as leituras (declarações `SELECT`) ocorram na tabela em paralelo com a criação do índice, mas as escritas (`INSERT`, `UPDATE`, `DELETE`) são bloqueadas até que a construção do índice esteja concluída. Em ambientes de produção, isso é frequentemente inaceitável. É possível permitir que as escritas ocorram em paralelo com a criação do índice, mas há várias ressalvas a serem consideradas — para mais informações, consulte [Construção de Índices Concorrentemente][(sql-createindex.md#SQL-CREATEINDEX-CONCURRENTLY "Building Indexes Concurrently")].

Após a criação de um índice, o sistema precisa mantê-lo sincronizado com a tabela. Isso adiciona sobrecarga às operações de manipulação de dados. Os índices também podem impedir a criação de tuplas [somente heap][(storage-hot.md "66.7. Heap-Only Tuples (HOT)]"). Portanto, os índices que raramente ou nunca são usados em consultas devem ser removidos.