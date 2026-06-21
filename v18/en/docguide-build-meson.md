## J.4. Building the Documentation with Meson [#](#DOCGUIDE-BUILD-MESON)

To build the documentation using Meson, change to the `build` directory before running one of these commands, or add `-C build` to the command.

To build just the HTML version of the documentation:

```
build$ ninja html
```

For a list of other documentation targets see [Section 17.4.4.3](install-meson.md#TARGETS-MESON-DOCUMENTATION "17.4.4.3. Documentation Targets"). The output appears in the subdirectory `build/doc/src/sgml`.
