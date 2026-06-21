## 8.12. Tipo de UUID [#](#DATATYPE-UUID)

O tipo de dados `uuid` armazena Identificadores Únicos Universalmente (UUID) conforme definido por [RFC 9562][(https://datatracker.ietf.org/doc/html/rfc9562)], ISO/IEC 9834-8:2005 e normas relacionadas. (Alguns sistemas referem-se a este tipo de dados como um identificador globalmente único, ou GUID, em vez disso.) Este identificador é uma quantidade de 128 bits que é gerada por um algoritmo escolhido para torná-lo muito improvável que o mesmo identificador seja gerado por qualquer outra pessoa no universo conhecido usando o mesmo algoritmo. Portanto, para sistemas distribuídos, esses identificadores fornecem uma garantia de unicidade melhor do que os geradores de sequência, que são únicos apenas dentro de um único banco de dados.

O RFC 9562 define 8 versões diferentes de UUID. Cada versão tem requisitos específicos para gerar novos valores de UUID, e cada versão oferece benefícios e desvantagens distintos. O PostgreSQL oferece suporte nativo para gerar UUIDs usando os algoritmos UUIDv4 e UUIDv7. Alternativamente, os valores de UUID podem ser gerados fora do banco de dados usando qualquer algoritmo. O tipo de dados `uuid` pode ser usado para armazenar qualquer UUID, independentemente da origem e da versão do UUID.

Um UUID é escrito como uma sequência de dígitos hexadecimais minúsculos, em vários grupos separados por hífens, especificamente um grupo de 8 dígitos seguido por três grupos de 4 dígitos seguidos por um grupo de 12 dígitos, para um total de 32 dígitos representando os 128 bits. Um exemplo de um UUID nesta forma padrão é:

```
a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11
```

O PostgreSQL também aceita as seguintes formas alternativas de entrada: uso de algarismos em maiúsculas, o formato padrão cercado por chaves, omissão de alguns ou todos os hífens, adição de um hífen após qualquer grupo de quatro dígitos. Exemplos são:

```
A0EEBC99-9C0B-4EF8-BB6D-6BB9BD380A11
{a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11}
a0eebc999c0b4ef8bb6d6bb9bd380a11
a0ee-bc99-9c0b-4ef8-bb6d-6bb9-bd38-0a11
{a0eebc99-9c0b4ef8-bb6d6bb9-bd380a11}
```

A saída sempre está no formato padrão.

Veja [Seção 9.14][(functions-uuid.md "9.14. UUID Functions")] para saber como gerar um UUID no PostgreSQL.