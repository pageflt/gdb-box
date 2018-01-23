# gdb-box

```
Examine memory and display in specific byte order.

Usage:
  box/FMT ADDRESS

  - FMT is a repeat count followed by a size letter and a byte order letter.
      - Size letters: b(byte), h(halfword), w(word), g(giant, 8 bytes)
      - Byte order letters: l(little endian), b(big endian)
  - ADDRESS is an expression for the memory address to examine

The specified number of objects of the specified size are printed in
hexadecimal, according to the specified byte order.
```
