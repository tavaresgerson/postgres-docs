## 32.8. Interface de Caminho Rápido [#](#LIBPQ-FASTPATH)

O PostgreSQL oferece uma interface de caminho rápido para enviar chamadas simples de função ao servidor.

### Aviso

Essa interface não é segura e não deve ser usada. Quando *`result_is_int`* está definido como `0`, `PQfn` pode escrever dados além do final de *`result_buf`*, independentemente de o buffer ter espaço suficiente para o número de bytes solicitado. Além disso, é obsoleta, pois é possível alcançar um desempenho semelhante e maior funcionalidade configurando uma declaração preparada para definir a chamada de função. Em seguida, executar a declaração com transmissão binária de parâmetros e resultados substitui uma chamada de função de caminho rápido.

A função `PQfn` solicita a execução de uma função do servidor através da interface de caminho rápido:

```
PGresult *PQfn(PGconn *conn,
               int fnid,
               int *result_buf,
               int *result_len,
               int result_is_int,
               const PQArgBlock *args,
               int nargs);

typedef struct
{
    int len;
    int isint;
    union
    {
        int *ptr;
        int integer;
    } u;
} PQArgBlock;
```

O argumento *`fnid`* é o OID da função a ser executada. *`args`* e *`nargs`* definem os parâmetros a serem passados para a função; eles devem corresponder à lista declarada de argumentos da função. Quando o campo *`isint` de uma estrutura de parâmetro é verdadeiro, o valor *`u.integer` é enviado ao servidor como um inteiro do comprimento indicado (este deve ser 2 ou 4 bytes); ocorre a troca adequada de bytes. Quando *`isint` é falso, o número indicado de bytes em *`*u.ptr` são enviados sem processamento; os dados devem estar no formato esperado pelo servidor para transmissão binária do tipo de argumento do argumento da função. (A declaração de *`u.ptr`* como sendo do tipo `int *` é histórica; seria melhor considerá-la `void *`.)*`result_buf`* aponta para o buffer em que colocar o valor de retorno da função. O chamador deve ter alocado espaço suficiente para armazenar o valor de retorno. (Não há verificação!) O comprimento real do resultado em bytes será retornado no inteiro apontado por *`result_len`*. Se um resultado de inteiro de 2 ou 4 bytes é esperado, defina *`result_is_int`* para 1, caso contrário, defina-o para 0. Definir *`result_is_int`* para 1 faz com que o libpq troque os valores de byte, se necessário, para que sejam entregues como um valor adequado *`int` para a máquina do cliente; note que um inteiro de 4 bytes é entregue em *`*result_buf`* para qualquer tamanho de resultado permitido. Quando *`result_is_int` é 0, a string de bytes de formato binário enviada pelo servidor é devolvida sem modificação. (Neste caso, é melhor considerar *`result_buf`* como sendo do tipo `void *`.)

`PQfn` sempre retorna um ponteiro válido `PGresult`, com status `PGRES_COMMAND_OK` para sucesso ou `PGRES_FATAL_ERROR` se algum problema foi encontrado. O status do resultado deve ser verificado antes de o resultado ser usado. O chamador é responsável por liberar o `PGresult` com [`PQclear`](libpq-exec.md#LIBPQ-PQCLEAR) quando ele não for mais necessário.

Para passar um argumento NULL para a função, defina o campo *`len`* daquela estrutura de parâmetro para `-1`; os campos *`isint`* e *`u`* então são irrelevantes.

Se a função retornar NULL, *`*result_len`* é definido como `-1`, e *`*result_buf`* não é modificado.

Observe que não é possível lidar com resultados de valor definido ao usar essa interface. Além disso, a função deve ser uma função simples, não um agregado, uma função de janela ou um procedimento.