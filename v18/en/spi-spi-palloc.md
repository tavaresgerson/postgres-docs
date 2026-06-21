## SPI_palloc

SPI_palloc — allocate memory in the upper executor context

## Synopsis

```
void * SPI_palloc(Size size)
```

## Description

`SPI_palloc` allocates memory in the upper executor context.

This function can only be used while connected to SPI. Otherwise, it throws an error.

## Arguments

`Size size`: size in bytes of storage to allocate

## Return Value

pointer to new storage space of the specified size
