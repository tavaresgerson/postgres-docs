## 42.9. Subtransações explícitas no PL/Tcl [#](#PLTCL-SUBTRANSACTIONS)

Recuperar erros causados pelo acesso ao banco de dados, conforme descrito em [Seção 42.8](pltcl-error-handling.md), pode levar a uma situação indesejável em que algumas operações têm sucesso antes de uma delas falhar, e, após a recuperação desse erro, os dados permanecem em um estado inconsistente. O PL/Tcl oferece uma solução para esse problema na forma de subtransações explícitas.

Considere uma função que implemente uma transferência entre duas contas:

```
CREATE FUNCTION transfer_funds() RETURNS void AS $$
    if [catch {
        spi_exec "UPDATE accounts SET balance = balance - 100 WHERE account_name = 'joe'"
        spi_exec "UPDATE accounts SET balance = balance + 100 WHERE account_name = 'mary'"
    } errormsg] {
        set result [format "error transferring funds: %s" $errormsg]
    } else {
        set result "funds transferred successfully"
    }
    spi_exec "INSERT INTO operations (result) VALUES ('[quote $result]')"
$$ LANGUAGE pltcl;
```

Se a segunda declaração `UPDATE` resultar em uma exceção ser levantada, esta função registrará a falha, mas o resultado do primeiro `UPDATE` será, no entanto, comprometido. Em outras palavras, os fundos serão retirados da conta de Joe, mas não serão transferidos para a conta de Mary. Isso acontece porque cada `spi_exec` é uma subtransação separada e apenas uma dessas subtransações foi revertida.

Para lidar com esses casos, você pode envolver várias operações de banco de dados em uma subtransação explícita, que será bem-sucedida ou revogada como um todo. O PL/Tcl fornece um comando `subtransaction` para gerenciar isso. Podemos reescrever nossa função como:

```
CREATE FUNCTION transfer_funds2() RETURNS void AS $$
    if [catch {
        subtransaction {
            spi_exec "UPDATE accounts SET balance = balance - 100 WHERE account_name = 'joe'"
            spi_exec "UPDATE accounts SET balance = balance + 100 WHERE account_name = 'mary'"
        }
    } errormsg] {
        set result [format "error transferring funds: %s" $errormsg]
    } else {
        set result "funds transferred successfully"
    }
    spi_exec "INSERT INTO operations (result) VALUES ('[quote $result]')"
$$ LANGUAGE pltcl;
```

Observe que o uso de `catch` ainda é necessário para esse propósito. Caso contrário, o erro se propagaria ao nível superior da função, impedindo a inserção desejada na tabela `operations`. O comando `subtransaction` não arrisca erros, apenas assegura que todas as operações de banco de dados executadas dentro de seu escopo sejam revertidas juntas quando um erro é relatado.

Um recuo de uma subtransação explícita ocorre em qualquer erro relatado pelo código Tcl contido, e não apenas erros originários do acesso ao banco de dados. Assim, uma exceção regular de Tcl levantada dentro de um comando `subtransaction` também fará com que a subtransação seja recuada. No entanto, saídas não relacionadas a erros do código Tcl contido (por exemplo, devido a `return`) não causarão um recuo.