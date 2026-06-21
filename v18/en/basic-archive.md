## F.5. basic_archive — an example WAL archive module [#](#BASIC-ARCHIVE)

* [F.5.1. Configuration Parameters](basic-archive.md#BASIC-ARCHIVE-CONFIGURATION-PARAMETERS)
* [F.5.2. Notes](basic-archive.md#BASIC-ARCHIVE-NOTES)
* [F.5.3. Author](basic-archive.md#BASIC-ARCHIVE-AUTHOR)

`basic_archive` is an example of an archive module. This module copies completed WAL segment files to the specified directory. This may not be especially useful, but it can serve as a starting point for developing your own archive module. For more information about archive modules, see [Chapter 49](archive-modules.md "Chapter 49. Archive Modules").

In order to function, this module must be loaded via [archive_library](runtime-config-wal.md#GUC-ARCHIVE-LIBRARY), and [archive_mode](runtime-config-wal.md#GUC-ARCHIVE-MODE) must be enabled.

### F.5.1. Configuration Parameters [#](#BASIC-ARCHIVE-CONFIGURATION-PARAMETERS)

`basic_archive.archive_directory` (`string`): The directory where the server should copy WAL segment files. This directory must already exist. The default is an empty string, which effectively halts WAL archiving, but if [archive_mode](runtime-config-wal.md#GUC-ARCHIVE-MODE) is enabled, the server will accumulate WAL segment files in the expectation that a value will soon be provided.

These parameters must be set in `postgresql.conf`. Typical usage might be:

```
# postgresql.conf
archive_mode = 'on'
archive_library = 'basic_archive'
basic_archive.archive_directory = '/path/to/archive/directory'
```

### F.5.2. Notes [#](#BASIC-ARCHIVE-NOTES)

Server crashes may leave temporary files with the prefix `archtemp` in the archive directory. It is recommended to delete such files before restarting the server after a crash. It is safe to remove such files while the server is running as long as they are unrelated to any archiving still in progress, but users should use extra caution when doing so.

### F.5.3. Author [#](#BASIC-ARCHIVE-AUTHOR)

Nathan Bossart
