## CARREGAR

LOAD — carregar um arquivo de biblioteca compartilhada

## Sinopse

```
LOAD 'filename'
```

## Descrição

Este comando carrega um arquivo de biblioteca compartilhada no espaço de endereçamento do servidor PostgreSQL. Se o arquivo já tiver sido carregado, o comando não faz nada. Arquivos de biblioteca compartilhados que contêm funções C são carregados automaticamente sempre que uma de suas funções é chamada. Portanto, um `LOAD` explícito geralmente é necessário apenas para carregar uma biblioteca que modifica o comportamento do servidor por meio de "ganchos", em vez de fornecer um conjunto de funções.

O nome do arquivo da biblioteca é tipicamente fornecido como apenas um nome de arquivo simples, que é procurado no caminho de busca da biblioteca do servidor (definido por [dynamic_library_path][(runtime-config-client.md#GUC-DYNAMIC-LIBRARY-PATH)]). Alternativamente, pode ser fornecido como um nome de caminho completo. Em qualquer caso, a extensão padrão de arquivo de biblioteca compartilhada da plataforma pode ser omitida. Consulte [Seção 36.10.1][(xfunc-c.md#XFUNC-C-DYNLOAD "36.10.1. Dynamic Loading")] para obter mais informações sobre este tópico.

Os não superusuários só podem aplicar `LOAD` em arquivos de biblioteca localizados em `$libdir/plugins/` — o *`filename`* especificado deve começar exatamente com essa string. (É responsabilidade do administrador do banco de dados garantir que apenas bibliotecas "seguras" sejam instaladas lá.)

## Compatibilidade

`LOAD` é uma extensão do PostgreSQL.

## Veja também

[Crie função](sql-createfunction.md "CREATE FUNCTION")