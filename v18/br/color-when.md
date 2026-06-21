## N.º 1. Quando a cor é usada [#](#COLOR-WHEN)

Para usar a saída colorida, defina a variável de ambiente `PG_COLOR` da seguinte forma:

1. Se o valor for `always`, então a cor é usada.  
2. Se o valor for `auto` e a corrente de erro padrão estiver associada a um dispositivo terminal, então a cor é usada.  
3. Caso contrário, a cor não é usada.