## 36.3. Funções Definidas pelo Usuário [#](#XFUNC)

PostgreSQL oferece quatro tipos de funções:

* funções de linguagem de consulta (funções escritas em SQL) ([Seção 36.5][(xfunc-sql.md "36.5. Query Language (SQL)] Funções)
* funções de linguagem procedural (funções escritas, por exemplo, em PL/pgSQL ou PL/Tcl) ([Seção 36.8][(xfunc-pl.md "36.8. Procedural Language Functions")])
* funções internas ([Seção 36.9][(xfunc-internal.md "36.9. Internal Functions")])
* funções em linguagem C ([Seção 36.10][(xfunc-c.md "36.10. C-Language Functions")])

Todo tipo de função pode receber tipos básicos, tipos compostos ou combinações desses como argumentos (parâmetros). Além disso, todo tipo de função pode retornar um tipo básico ou um tipo composto. As funções também podem ser definidas para retornar conjuntos de valores básicos ou compostos.

Muitos tipos de funções podem receber ou retornar certos pseudotípicos (como tipos polimórficos), mas as facilidades disponíveis variam. Consulte a descrição de cada tipo de função para obter mais detalhes.

É mais fácil definir funções SQL, então vamos começar discutindo essas funções. A maioria dos conceitos apresentados para funções SQL serão aplicados aos outros tipos de funções.

Ao longo deste capítulo, pode ser útil consultar a página de referência do comando `CREATE FUNCTION` (sql-createfunction.md "CREATE FUNCTION") para entender melhor os exemplos. Alguns exemplos deste capítulo podem ser encontrados em `funcs.sql` e `funcs.c` no diretório `src/tutorial` na distribuição de código-fonte do PostgreSQL.