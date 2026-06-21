## 68.3. Formato de arquivo BKI [#](#BKI-FORMAT)

Esta seção descreve como o backend PostgreSQL interpreta os arquivos BKI. Essa descrição será mais fácil de entender se o arquivo `postgres.bki` estiver disponível como exemplo.

A entrada BKI consiste em uma sequência de comandos. Os comandos são compostos por um número de tokens, dependendo da sintaxe do comando. Os tokens são geralmente separados por espaços em branco, mas não precisam ser se não houver ambiguidade. Não há um separador de comando especial; o próximo token que não possa sintaticamente pertencer ao comando anterior começa um novo. (Normalmente, você colocaria um novo comando em uma nova linha, para clareza.) Os tokens podem ser palavras-chave específicas, caracteres especiais (parenteses, vírgulas, etc.), identificadores, números ou strings com aspas simples. Tudo é sensível ao caso.

As linhas que começam com `#` são ignoradas.