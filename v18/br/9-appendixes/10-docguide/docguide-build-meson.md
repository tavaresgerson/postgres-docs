## J.4. Construindo a documentação com Meson [#](#DOCGUIDE-BUILD-MESON)

Para construir a documentação usando o Meson, mude para o diretório `build` antes de executar um desses comandos, ou adicione `-C build` ao comando.

Para construir apenas a versão HTML da documentação:

```
build$ ninja html
```

Para uma lista de outros alvos de documentação, consulte [Seção 17.4.4.3](install-meson.md#TARGETS-MESON-DOCUMENTATION). A saída aparece no subdiretório `build/doc/src/sgml`.