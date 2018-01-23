# gdb-box

GDB extension for displaying memory contents in different byte orders.

## Usage
`box/FMT ADDRESS`

Arguments:
   - `FMT` is a repeat count followed by a size letter and a endianess letter.
       - Size letters: b(byte), h(halfword), w(word), g(giant, 8 bytes)
       - Endianess letters: L(little endian), B(big endian)
   - `ADDRESS` is an expression for the memory address to examine

The specified number of objects of the specified size are printed in
hexadecimal, according to the specified byte order.

Default count is 1. Default size is w (word). Default endianess is the
native endianess of your architecture.

For example, to examine 64 bytes (16 words) starting from address `0xffffe4003de5f800` in Big Endian format, the invocation is as follows:
```
(gdb) box/16wB 0xffffe4003de5f800
0xffffe4003de5f800:	0x52540012	0x34568a20	0x02ac61f0	0x08004500
0xffffe4003de5f810:	0x0054f3ba	0x40004001	0xc18ec0a8	0x0202c0a8
0xffffe4003de5f820:	0x020d0800	0x1b287f6e	0x00011451	0x675a0000
0xffffe4003de5f830:	0x00001aea	0x08000000	0x00001011	0x12131415
```

Same region and size, in Little Endian format:
```
(gdb) box/16wL 0xffffe4003de5f800
0xffffe4003de5f800:	0x12005452	0x208a5634	0xf061ac02	0x00450008
0xffffe4003de5f810:	0xbaf35400	0x01400040	0xa8c08ec1	0xa8c00202
0xffffe4003de5f820:	0x00080d02	0x6e7f281b	0x51140100	0x00005a67
0xffffe4003de5f830:	0xea1a0000	0x00000008	0x11100000	0x15141312
```

Again, same memory region, but displayed as half-words in Little Endian format:
```
(gdb) box/32hL 0xffffe4003de5f800
0xffffe4003de5f800:	0x5452	0x1200	0x5634	0x208a	0xac02	0xf061	0x0008	0x0045
0xffffe4003de5f810:	0x5400	0xbaf3	0x0040	0x0140	0x8ec1	0xa8c0	0x0202	0xa8c0
0xffffe4003de5f820:	0x0d02	0x0008	0x281b	0x6e7f	0x0100	0x5114	0x5a67	0x0000
0xffffe4003de5f830:	0x0000	0xea1a	0x0008	0x0000	0x0000	0x1110	0x1312	0x1514
```

## Installation

You can either load the extension manually...

```
(gdb) source /path/to/box.py
```
...or you can add it to your `.gdbinit`:

```
$ cat .gdbinit
[...snip...]
source /path/to/box.py
[...snip...]
```

## How it works?

It's a wrapper around GDB's `x` command that reverses the byte-order when requested. That's all.

## Bugs?

Definitelly. You can open an issue [here](https://github.com/pageflt/gdb-box/issues).
