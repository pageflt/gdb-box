# Dimitris Karagkasidis <t.pagef.lt@gmail.com>
# https://github.com/pageflt/gdb-box
import gdb
import re


class BOExamine(gdb.Command):
    # Documentation for GDB's `help` command:
    """Examine memory and display the results in specific byte order.

Usage: box/FMT ADDRESS

Arguments:
   - FMT is a repeat count followed by a size letter and a endianess letter.
       - Size letters: b(byte), h(halfword), w(word), g(giant, 8 bytes)
       - Endianess letters: L(little endian), B(big endian)
   - ADDRESS is an expression for the memory address to examine

The specified number of objects of the specified size are printed in
hexadecimal, according to the specified byte order.

Default count is 1. Default size is w (word). Default endianess is the
native endianess of your architecture."""


    _endian = None

    def __init__(self):
        super(BOExamine, self).__init__("box",
                                        gdb.COMMAND_NONE,
                                        gdb.COMPLETE_NONE)


    def invoke(self, args, from_tty):
        try:
            self.get_endianess()
            fmt, addr_expr = self.parse_args(args)
            data = self.get_data(fmt, addr_expr)
            gdb.write(self.convert_data(fmt[2], data))
        except Exception as ex:
            raise gdb.GdbError(ex)


    def get_endianess(self):
        try:
            if gdb.parameter("endian") in ("little", "big"):
                self._endian = gdb.parameter("endian")
            else:
                s = gdb.execute("show endian", False, True)
                p = (r"\(currently (\w+) endian\)",
                     r"The target is assumed to be (\w+) endian")
                for pattern in p:
                    r = re.search(pattern, s)
                    if r:
                        self._endian = r.group(1)

            if self._endian not in ("big", "little"):
                raise Exception("Could not detect endianess")

        except Exception as ex:
            raise ex


    def parse_args(self, args):
        # Parse user-supplied arguments and return them as:
        #   (fmt, addr_expr)
        # where `addr_expr` is GDB address expressioni, and `fmt` is a tuple:
        #   (count, size, endian)
        # where:
        # - count: number of bytes to examine
        # - size: word size (byte/halfword/word/giant word)
        # - endian: byte order in which to display (little/big)
        args = args.split()

        if not len(args):
            raise Exception("Invalid arguments. Check `help box`.")

        if not args[0].startswith("/"):
            addr_expr = " ".join(args)
            return (1, 'w', self._endian), addr_expr
        else:
            addr_expr = " ".join(args[1:])
            r = re.match(r"\/(\d*)([LB|bhwg])([LB|bhwg]?)", args[0])
            if r:
                count = 1 if r.group(1) == "" else int(r.group(1))
                if r.group(3) != "":
                    if (r.group(2) in "bhwg" and r.group(3) in "bhgw") or \
                       (r.group(2) in "LB" and r.group(3) in "LB"):
                        raise Exception("Invalid format argument")
                    else:
                        size = r.group(2) if r.group(2) in "bhwg" else r.group(3)
                        endian = r.group(3) if r.group(3) in "LB" else r.group(2)
                        endian = "little" if endian == "L" else "big"
                else:
                    size = "w" if r.group(2) in "LB" else r.group(2)
                    endian = self._endian if r.group(2) in "bhwg" else r.group(2)

                return (count, size, endian), addr_expr
            else:
                raise Exception("Invalid FMT argument. Check `help box`.")


    def get_data(self, fmt, addr_expr):
        try:
            x_cmd = "x/%dx%s %s" % (fmt[0],fmt[1], addr_expr)
            return gdb.execute(x_cmd, False, True)
        except Exception as ex:
            raise Exception("Could not examine memory. %s" % ex)


    def convert_data(self, endianess, data):
        try:
            if endianess != self._endian:
                buf = ""
                for line in data.split("\n"):
                    if not line:
                        continue
                    for e in line.split():
                        if e.endswith(":"):
                            buf += "%s\t" % e
                        else:
                            buf += "%s\t" % self._reverse(e)
                    buf = "%s\n" % buf.strip()
                return buf
            return data
        except Exception as ex:
            raise Exception("Could not convert data. %s" % ex)


    def _reverse(self, data):
        try:
            data = list(data.replace("0x", "").decode("hex"))
            data.reverse()
            return "0x%s" % "".join(data).encode("hex")
        except Exception as ex:
            raise ex

BOExamine()
