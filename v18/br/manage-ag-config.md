## 22.4. Configuração do banco de dados [#](#MANAGE-AG-CONFIG)

Lembre-se de que o servidor PostgreSQL fornece um grande número de variáveis de configuração de tempo de execução. Você pode definir valores padrão específicos para o banco de dados para muitas dessas configurações. [Capítulo 19](runtime-config.md)

Por exemplo, se, por algum motivo, você quiser desabilitar o otimizador GEQO para um banco de dados específico, você normalmente teria que desabilitá-lo para todos os bancos de dados ou garantir que cada cliente que se conecta seja cuidadoso o suficiente para emitir `SET geqo TO off`. Para tornar essa configuração padrão em um banco de dados específico, você pode executar o comando:

```
ALTER DATABASE mydb SET geqo TO off;
```

Isso salvará o ajuste (mas não o definiu imediatamente). Em conexões subsequentes a este banco de dados, ele aparecerá como se `SET geqo TO off;` tivesse sido executado logo antes do início da sessão. Note que os usuários ainda podem alterar este ajuste durante suas sessões; ele será apenas o padrão. Para desfazer qualquer ajuste desse tipo, use `ALTER DATABASE dbname RESET varname`.