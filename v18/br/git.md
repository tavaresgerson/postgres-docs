## I.1. Obtendo a Fonte via Git [#](#GIT)

Com o Git, você fará uma cópia de todo o repositório de código em sua máquina local, para que você tenha acesso a todo o histórico e ramos offline. Esta é a maneira mais rápida e flexível de desenvolver ou testar patches.

**Git**

1. Você precisará de uma versão instalada do Git, que você pode obter em <https://git-scm.com>. Muitos sistemas já têm uma versão recente do Git instalada por padrão, ou disponível em seu sistema de distribuição de pacotes.
2. Para começar a usar o repositório Git, faça um clone do espelho oficial:

   ```
   git clone https://git.postgresql.org/git/postgresql.git
   ```

Isso copiará o repositório completo para sua máquina local, então pode levar um tempo para ser concluído, especialmente se você tiver uma conexão lenta com a Internet. Os arquivos serão colocados em um novo subdiretório `postgresql` do seu diretório atual. 3. Sempre que você quiser obter as últimas atualizações no sistema, `cd` no repositório e execute:

   ```
   git fetch
   ```

O Git pode fazer muito mais do que apenas buscar a fonte. Para mais informações, consulte as páginas do manual do Git ou veja o site em <https://git-scm.com>.