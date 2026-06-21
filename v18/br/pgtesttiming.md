## pg_test_timing

pg_test_timing — medir o overhead de tempo

## Sinopse

`pg_test_timing` [*`option`*...]

## Descrição

pg_test_timing é uma ferramenta para medir o tempo de sobrecarga do seu sistema e confirmar que o tempo do sistema nunca retrocede. Sistemas que são lentos em coletar dados de tempo podem fornecer resultados menos precisos do `EXPLAIN ANALYZE`.

## Opções

pg_test_timing aceita as seguintes opções de linha de comando:

`-d duration` `--duration=duration`: Especifica a duração do teste, em segundos. Durações mais longas oferecem uma precisão ligeiramente melhor e têm maior probabilidade de descobrir problemas com o relógio do sistema que se move para trás. A duração padrão do teste é de 3 segundos.

`-V` `--version`: Imprima a versão do pg_test_timing e saia.

`-?` `--help`: Mostrar ajuda sobre os argumentos da linha de comando do comando pg_test_timing e sair.

## Uso

### Interpretando os Resultados

Bons resultados mostrarão que a maioria (>90%) das chamadas de temporização individual levam menos de um microsegundo. O custo médio por ciclo será ainda menor, abaixo de 100 nanosegundos. Este exemplo de um sistema Intel i7-860 usando uma fonte de relógio TSC mostra um desempenho excelente:

```
Testing timing overhead for 3 seconds.
Per loop time including overhead: 35.96 ns
Histogram of timing durations:
  < us   % of total      count
     1     96.40465   80435604
     2      3.59518    2999652
     4      0.00015        126
     8      0.00002         13
    16      0.00000          2
```

Observe que diferentes unidades são usadas para o tempo por ciclo do que para o histograma. O ciclo pode ter resolução dentro de alguns nanosegundos (ns), enquanto as chamadas de temporização individuais só podem resolver até um microsegundo (us).

### Medição do tempo de sobrecarga do Executor

### Introdução
A medição do tempo de sobrecarga do Executor é uma medida que ajuda a entender como o Executor está lidando com a execução de tarefas. É importante entender que o Executor não é um sistema de gerenciamento de tarefas, mas sim um executor que executa tarefas de forma independente.

### O que é o sobrecarga do Executor?
O sobrecarga do Executor é o tempo que o Executor gasta para executar uma tarefa. Esse tempo inclui o tempo de execução da tarefa, mas também o tempo necessário para a execução de tarefas secundárias, como a alocação de memória, a criação de objetos, a verificação de condições, etc.

### Como medir o sobrecarga do Executor?
Para medir o sobrecarga do Executor, você pode usar o seguinte método:

1. **Registre o tempo de execução da tarefa**: Use um cronômetro para medir o tempo que a tarefa leva para ser executada.
2. **Registre o tempo de execução das tarefas secundárias**: Registre o tempo que cada tarefa secundária leva para ser executada.
3. **Calcule o sobrecarga do Executor**: Subtraia o tempo de execução da tarefa do tempo de execução total. Isso dará o sobrecarga do Executor.

### Exemplo
Suponha que você tenha uma tarefa que leva 10 segundos para ser executada e que, além disso, a tarefa também precise de 5 segundos para alocar memória, 3 segundos para criar um objeto e 2 segundos para verificar uma condição. O sobrecarga do Executor seria:

10 segundos (tempo de execução da tarefa) - (5 segundos + 3 segundos + 2 segundos) = 10 segundos - 10 segundos = 0 segundos

### Conclusão
A medição do sobrecarga do Executor é uma ferramenta importante para entender como o Executor está lidando com a execução de tarefas. Se o sobrecarga do Executor for baixo, isso indica que o Executor está executando as tarefas de forma eficiente. Se o sobrecarga do Executor for alto, isso pode indicar problemas com a alocação de memória, a criação de objetos ou a verificação de condições. É importante ajustar o Executor para minimizar o sobrecarga e melhorar a eficiência da execução de tarefas.

Quando o executor de consulta está executando uma declaração usando `EXPLAIN ANALYZE`, as operações individuais são temporizadas e mostram um resumo. O custo do seu sistema pode ser verificado contando as linhas com o programa psql:

```
CREATE TABLE t AS SELECT * FROM generate_series(1,100000);
\timing
SELECT COUNT(*) FROM t;
EXPLAIN ANALYZE SELECT COUNT(*) FROM t;
```

O sistema i7-860 mede o tempo de execução da consulta de contagem em 9,8 ms, enquanto a versão `EXPLAIN ANALYZE` leva 16,6 ms, processando cada uma pouco mais de 100.000 linhas. Essa diferença de 6,8 ms significa que o custo de tempo por linha é de 68 ns, cerca de duas vezes o que o pg_test_timing estimou que seria. Mesmo essa quantidade relativamente pequena de custo de tempo torna a declaração de contagem totalmente cronometrada levando quase 70% mais tempo. Em consultas mais substanciais, o custo de tempo seria menos problemático.

### Mudando as fontes de tempo

Em alguns sistemas Linux mais recentes, é possível alterar a fonte de relógio usada para coletar dados de temporização a qualquer momento. Um segundo exemplo mostra a desaceleração possível ao mudar para a fonte de tempo acpi_pm mais lenta, no mesmo sistema usado para os resultados rápidos acima:

```
# cat /sys/devices/system/clocksource/clocksource0/available_clocksource
tsc hpet acpi_pm
# echo acpi_pm > /sys/devices/system/clocksource/clocksource0/current_clocksource
# pg_test_timing
Per loop time including overhead: 722.92 ns
Histogram of timing durations:
  < us   % of total      count
     1     27.84870    1155682
     2     72.05956    2990371
     4      0.07810       3241
     8      0.01357        563
    16      0.00007          3
```

Nessa configuração, a amostra `EXPLAIN ANALYZE` acima leva 115,9 ms. Isso representa 1061 ns de sobrecarga de temporização, novamente um pequeno múltiplo do que é medido diretamente por essa ferramenta. Tanto tempo de sobrecarga significa que a própria consulta real está consumindo apenas uma pequena fração do tempo contabilizado, a maior parte está sendo consumida em sobrecarga. Nessa configuração, quaisquer `EXPLAIN ANALYZE` que envolvam muitas operações temporizadas seriam inflados significativamente pela sobrecarga de temporização.

O FreeBSD também permite alterar a fonte de tempo em tempo real e registra informações sobre o temporizador selecionado durante o arranque:

```
# dmesg | grep "Timecounter"
Timecounter "ACPI-fast" frequency 3579545 Hz quality 900
Timecounter "i8254" frequency 1193182 Hz quality 0
Timecounters tick every 10.000 msec
Timecounter "TSC" frequency 2531787134 Hz quality 800
# sysctl kern.timecounter.hardware=TSC
kern.timecounter.hardware: ACPI-fast -> TSC
```

Outros sistemas podem permitir apenas a definição da fonte de hora no momento do arranque. Em sistemas Linux mais antigos, a configuração do kernel "relógio" é a única maneira de fazer esse tipo de mudança. E mesmo em alguns mais recentes, a única opção que você verá para uma fonte de relógio é "jiffies". Jiffies é a implementação de relógio de software Linux mais antiga, que pode ter boa resolução quando é respaldada por hardware de temporização suficientemente rápido, como neste exemplo:

```
$ cat /sys/devices/system/clocksource/clocksource0/available_clocksource
jiffies
$ dmesg | grep time.c
time.c: Using 3.579545 MHz WALL PM GTOD PIT/TSC timer.
time.c: Detected 2400.153 MHz processor.
$ pg_test_timing
Testing timing overhead for 3 seconds.
Per timing duration including loop overhead: 97.75 ns
Histogram of timing durations:
  < us   % of total      count
     1     90.23734   27694571
     2      9.75277    2993204
     4      0.00981       3010
     8      0.00007         22
    16      0.00000          1
    32      0.00000          1
```

### Contagem de Hardware e Precisão de Cronometragem

Coletar informações precisas de temporização é normalmente feito em computadores usando relógios de hardware com vários níveis de precisão. Com alguns equipamentos, os sistemas operacionais podem passar o tempo do relógio do sistema quase diretamente para os programas. Um relógio do sistema também pode ser derivado de um chip que simplesmente fornece interrupções de temporização, cliques periódicos em algum intervalo de tempo conhecido. Em qualquer caso, os núcleos dos sistemas operacionais fornecem uma fonte de relógio que oculta esses detalhes. Mas a precisão dessa fonte de relógio e quão rapidamente ela pode retornar resultados varia com base no hardware subjacente.

O uso incorreto do relógio pode resultar em instabilidade do sistema. Teste qualquer alteração na fonte do relógio com muito cuidado. Os padrões do sistema operacional são, às vezes, feitos para favorecer a confiabilidade em detrimento da melhor precisão. E se você estiver usando uma máquina virtual, verifique as fontes de tempo recomendadas compatíveis com ela. O hardware virtual enfrenta dificuldades adicionais ao emular temporizadores, e muitas vezes há configurações por sistema operacional sugeridas pelos fornecedores.

A fonte de relógio do Contador de Marca-Tempo (TSC) é a mais precisa disponível nas CPUs da geração atual. É a maneira preferida de rastrear o tempo do sistema quando é suportada pelo sistema operacional e o relógio TSC é confiável. Existem várias maneiras pelas quais o TSC pode não fornecer uma fonte de temporização precisa, tornando-o não confiável. Os sistemas mais antigos podem ter um relógio TSC que varia com base na temperatura da CPU, tornando-o inutilizável para temporização. Tentar usar TSC em algumas CPUs multicore mais antigas pode resultar em um tempo relatado que é inconsistente entre vários núcleos. Isso pode resultar no tempo indo para trás, um problema que este programa verifica. E até mesmo os sistemas mais novos podem não fornecer um temporizador TSC preciso com configurações de economia de energia muito agressivas.

Sistemas operacionais mais recentes podem verificar os problemas conhecidos do TSC e mudar para uma fonte de relógio mais lenta e estável quando são detectados. Se o seu sistema suporta o tempo do TSC, mas não o usa como padrão, pode ser desativado por um bom motivo. Além disso, alguns sistemas operacionais podem não detectar todos os problemas possíveis corretamente, ou permitir o uso do TSC mesmo em situações em que é conhecido que ele é impreciso.

O Timer de Evento de Alta Precisão (HPET) é o temporizador preferido em sistemas onde ele está disponível e o TSC não é preciso. O próprio chip do temporizador é programável para permitir uma resolução de até 100 nanosegundos, mas você pode não ver muita precisão no relógio do seu sistema.

A Configuração Avançada e a Interface de Energia (ACPI) fornece um Temporizador de Gerenciamento de Energia (PM), que o Linux denomina como acpi_pm. O relógio derivado do acpi_pm, no máximo, fornecerá uma resolução de 300 nanosegundos.

Os temporizadores utilizados em hardware de PCs mais antigos incluem o Temporizador de Intervalo Programável (PIT) 8254, o relógio de tempo real (RTC), o Temporizador Controlador de Interrupções Programável Avançado (APIC) e o temporizador Cyclone. Esses temporizadores visam resolução em milissegundos.

## Veja também

[EXPLAIN](sql-explain.md "EXPLAIN")
