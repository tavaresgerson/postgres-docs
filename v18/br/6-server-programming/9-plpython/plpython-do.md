## 44.4. Blocos de código anônimo [#](#PLPYTHON-DO)

O PL/Python também suporta blocos de código anônimos chamados com a declaração [DO](sql-do.md):

```
DO $$
    # PL/Python code
$$ LANGUAGE plpython3u;
```

Um bloco de código anônimo não recebe argumentos e qualquer valor que ele possa retornar é descartado. Caso contrário, ele se comporta exatamente como uma função.