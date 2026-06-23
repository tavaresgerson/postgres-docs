## 30.4. Extensibilidade [#](#JIT-EXTENSIBILITY)

* [30.4.1. Suporte para Extensões Inlineadas](jit-extensibility.md#JIT-EXTENSIBILITY-BITCODE)
* [30.4.2. Fornecedores JIT Desconectables](jit-extensibility.md#JIT-PLUGGABLE)

### 30.4.1. Suporte para Extensões Inlineadas [#](#JIT-EXTENSIBILITY-BITCODE)

A implementação JIT do PostgreSQL pode incluir os corpos das funções dos tipos `C` e `internal`, bem como operadores baseados nessas funções. Para fazer isso para funções em extensões, as definições dessas funções precisam ser disponibilizadas. Ao usar [PGXS](extend-pgxs.md) para construir uma extensão contra um servidor que foi compilado com suporte JIT do LLVM, os arquivos relevantes serão construídos e instalados automaticamente.

Os arquivos relevantes devem ser instalados em `$pkglibdir/bitcode/$extension/` e um resumo deles em `$pkglibdir/bitcode/$extension.index.bc`, onde `$pkglibdir` é o diretório retornado por `pg_config --pkglibdir` e `$extension` é o nome base da biblioteca compartilhada da extensão.

### Nota

Para funções embutidas no próprio PostgreSQL, o bitcode é instalado em `$pkglibdir/bitcode/postgres`.

### 30.4.2. Fornecedores JIT encaixáveis [#](#JIT-PLUGGABLE)

O PostgreSQL fornece uma implementação JIT baseada no LLVM. A interface para o provedor JIT é intercambiável e o provedor pode ser alterado sem recompilação (embora, atualmente, o processo de construção forneça apenas dados de suporte de encaixe para o LLVM). O provedor ativo é escolhido através da configuração [jit_provider](runtime-config-client.md#GUC-JIT-PROVIDER).

#### 30.4.2.1. Interface do Fornecedor JIT [#](#JIT-PLUGGABLE-PROVIDER-INTERFACE)

Um provedor JIT é carregado ao carregar dinamicamente a biblioteca compartilhada nomeada. O caminho normal de busca de biblioteca é usado para localizar a biblioteca. Para fornecer os callbacks do provedor JIT necessários e indicar que a biblioteca é realmente um provedor JIT, ele precisa fornecer uma função C chamada `_PG_jit_provider_init`. Essa função é passada uma estrutura que precisa ser preenchida com os ponteiros da função de callback para ações individuais:

```
struct JitProviderCallbacks
{
    JitProviderResetAfterErrorCB reset_after_error;
    JitProviderReleaseContextCB release_context;
    JitProviderCompileExprCB compile_expr;
};

extern void _PG_jit_provider_init(JitProviderCallbacks *cb);
```
