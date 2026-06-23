## F.30. pg_prewarm — pré-carregar dados de relação em caches de buffer [#](#PGPREWARM)

* [F.30.1. Funções](pgprewarm.md#PGPREWARM-FUNCS)
* [F.30.2. Parâmetros de Configuração](pgprewarm.md#PGPREWARM-CONFIG-PARAMS)
* [F.30.3. Autor](pgprewarm.md#PGPREWARM-AUTHOR)

O módulo `pg_prewarm` fornece uma maneira conveniente de carregar dados de relação no cache de buffer do sistema operacional ou no cache de buffer do PostgreSQL. O pré-aquecimento pode ser realizado manualmente usando a função `pg_prewarm`, ou pode ser realizado automaticamente incluindo `pg_prewarm` em [shared_preload_libraries](runtime-config-client.md#GUC-SHARED-PRELOAD-LIBRARIES). No último caso, o sistema executará um trabalhador de fundo que registrará periodicamente o conteúdo dos buffers compartilhados em um arquivo chamado `autoprewarm.blocks` e, usando 2 trabalhadores de fundo, recarregará os mesmos blocos após um reinício.

### F.30.1. Funções [#](#PGPREWARM-FUNCS)

```
pg_prewarm(regclass, mode text default 'buffer', fork text default 'main',
           first_block int8 default null,
           last_block int8 default null) RETURNS int8
```

O primeiro argumento é a relação a ser pré-aquecida. O segundo argumento é o método de pré-aquecimento a ser utilizado, conforme discutido mais adiante; o terceiro é a relação para ser pré-aquecida, geralmente `main`. O quarto argumento é o primeiro número de bloco a ser pré-aquecido (`NULL` é aceito como sinônimo de zero). O quinto argumento é o último número de bloco a ser pré-aquecido (`NULL` significa pré-aquecer através do último bloco na relação). O valor de retorno é o número de blocos pré-aquecidos.

Existem três métodos de pré-aquecimento disponíveis. `prefetch` emite solicitações de pré-pesquisa assíncronas ao sistema operacional, se isso for suportado, ou lança um erro caso contrário. `read` lê a faixa de blocos solicitada; ao contrário de `prefetch`, este é síncrono e é suportado em todas as plataformas e compilações, mas pode ser mais lento. `buffer` lê a faixa de blocos solicitada no cache de buffer do banco de dados.

Observe que, com qualquer um desses métodos, tentar pré-aquecer mais blocos do que podem ser armazenados na memória cache — pelo sistema operacional ao usar `prefetch` ou `read`, ou pelo PostgreSQL ao usar `buffer` — provavelmente resultará em blocos com números menores sendo expulsos à medida que blocos com números maiores são lidos. Os dados pré-aquecidos também não desfrutam de proteção especial contra expulsões da memória cache, portanto, é possível que outras atividades do sistema expulsam os blocos pré-aquecidos recém-lidos; por outro lado, o pré-aquecimento também pode expulsar outros dados da memória cache. Por essas razões, o pré-aquecimento é tipicamente mais útil no início, quando os caches estão em grande parte vazios.

```
autoprewarm_start_worker() RETURNS void
```

Inicie o principal trabalhador de pré-aquecimento automático. Isso normalmente acontece automaticamente, mas é útil se o pré-aquecimento automático não foi configurado no momento da inicialização do servidor e você deseja iniciar o trabalhador em um momento posterior.

```
autoprewarm_dump_now() RETURNS int8
```

Atualize imediatamente `autoprewarm.blocks`. Isso pode ser útil se o trabalhador de pré-aquecimento automático não estiver em execução, mas você antecipar que o executará após o próximo reinício. O valor de retorno é o número de registros escritos em `autoprewarm.blocks`.

### F.30.2. Parâmetros de configuração [#](#PGPREWARM-CONFIG-PARAMS)

`pg_prewarm.autoprewarm` (`boolean`): Controla se o servidor deve executar o trabalhador de pré-aquecimento automático. Isso está ativado por padrão. Este parâmetro só pode ser definido no início do servidor.

`pg_prewarm.autoprewarm_interval` (`integer`): Este é o intervalo entre as atualizações para `autoprewarm.blocks`. O padrão é de 300 segundos. Se definido como 0, o arquivo não será descarregado em intervalos regulares, mas apenas quando o servidor for desligado.

Esses parâmetros devem ser definidos em `postgresql.conf`. O uso típico pode ser:

```
# postgresql.conf
shared_preload_libraries = 'pg_prewarm'

pg_prewarm.autoprewarm = true
pg_prewarm.autoprewarm_interval = 300s
```

### F.30.3. Autor [#](#PGPREWARM-AUTHOR)

Robert Haas `<rhaas@postgresql.org>`