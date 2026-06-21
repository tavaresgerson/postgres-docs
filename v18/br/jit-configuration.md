## 30.3. Configuração [#](#JIT-CONFIGURATION)

A variável de configuração [jit](runtime-config-query.md#GUC-JIT) determina se a compilação JIT é habilitada ou desabilitada. Se habilitada, as variáveis de configuração [jit_above_cost][(runtime-config-query.md#GUC-JIT-ABOVE-COST), [jit_inline_above_cost][(runtime-config-query.md#GUC-JIT-INLINE-ABOVE-COST) e [jit_optimize_above_cost][(runtime-config-query.md#GUC-JIT-OPTIMIZE-ABOVE-COST) determinam se a compilação JIT é realizada para uma consulta e quanto esforço é gasto para isso.

[jit_provider](runtime-config-client.md#GUC-JIT-PROVIDER) determina qual implementação JIT é usada. Raramente é necessário alterá-la. Veja [Seção 30.4.2](jit-extensibility.md#JIT-PLUGGABLE).

Para fins de desenvolvimento e depuração, existem alguns parâmetros de configuração adicionais, conforme descrito em [Seção 19.17](runtime-config-developer.md).