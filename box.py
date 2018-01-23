# Examine memory and display in specific byte order.
#
# Usage:
#   box/FMT ADDRESS
#
#   - FMT is a repeat count followed by a size letter and a byte order letter.
#       - Size letters: b(byte), h(halfword), w(word), g(giant, 8 bytes)
#       - Byte order letters: l(little endian), b(big endian)
#   - ADDRESS is an expression for the memory address to examine
#
# The specified number of objects of the specified size are printed in
# hexadecimal, according to the specified byte order.
#
# Dimitris Karagkasidis <t.pagef.lt@gmail.com>
# https://github.com/pageflt/gdb-box

import gdb
import re

class BOExamine(gdb.Command):
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
            self.display_data(fmt[2], data)
        except Exception as e:
            raise gdb.GdbError(e)


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

        except Exception as e:
            raise e


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

        if len(args) == 1 and not args[0].startswith("/"):
            # User specified only an address, use default size and endian.
            addr_expr = args[0]
            return (1, 'w', self._endian), addr_expr
        elif len(args) == 2:
            # User specified both format and address.
            addr_expr = args[1]
            r = re.match(r"\/(\d*)([LB|bhwg])([LB|bhwg]?)", args[0])
            if r:
                count = 1 if r.group(1) == "" else int(r.group(1))
                if r.group(3) != "":
                    if (r.group(2) in "bhwg" and r.group(3) in "bhgw") or \
                       (r.group(2) in "LB" and r.group(3) in "LB"):
                        raise Exception("Invalid FMT argument")
                    else:
                        size = r.group(2) if r.group(2) in "bhwg" else r.group(3)
                        endian = r.group(3) if r.group(3) in "LB" else r.group(2)
                        endian = "little" if endian == "L" else "big"
                else:
                    size = "w" if r.group(2) in "LB" else r.group(2)
                    endian = self._endian if r.group(2) in "bhwg" else r.group(2)

                return (count, size, endian), addr_expr
            else:
                raise Exception("Invalid FMT argument")
        else:
            raise Exception("Invalid arguments")


    def get_data(self, fmt, addr_expr):
        try:
            x_cmd = "x/%dx%s %s" % (fmt[0],fmt[1], addr_expr)
            return gdb.execute(x_cmd, False, True)
        except Exception as e:
            raise Exception("Could not examine memory. %s" % e)


    def display_data(self, endianess, data):
        if endianess == self._endian:
            gdb.write(data)
        else:
            output_buffer = ""
            for line in data.split("\n"):
                line = line.split()
                if len(line) > 0:
                    output_buffer += "%s " % line[0]
                    for d in line[1:]:
                        output_buffer += "%s  " % self._convert(endianess, d)
                    output_buffer = output_buffer.strip() + "\n"
            gdb.write(output_buffer)


    def _convert(self, endianess, data):
        if endianess != self._endian:
            data = data.replace("0x", "")
            bytes = []
            for i in range(0, len(data) - 1, 2):
                bytes.append(data[i:i+2])
            bytes.reverse()
            data = "0x%s" % "".join(bytes)
        return data


BOExamine()
