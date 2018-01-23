# Examine memory and display in specific byte order: box/FMT ADDRESS
#
#   - FMT is a repeat count followed by a byte order letter.
#   Byte order letters are l(little-endian) and b (big endian)
#   - ADDRESS is an expression for the memory address to examine

import gdb
import re

class BOExamine(gdb.Command):
    _LE = 0; _BE = 1
    _endian = None

    def __init__(self):
        super(BOPrint, self).__init__("box",
                                      gdb.COMMAND_NONE,
                                      gdb.COMPLETE_NONE)

    def invoke(self, args, from_tty):
        try:
            self._endian = self.get_endianess()
            fmt, addr_expr = self.parse_args(args)
            data = self.get_data(fmt, addr_expr)
            print(self.convert_data(fmt, data)
        except Exception as e:
            raise gdb.GdbError(e)

    def get_endianess(self):
        return(self._LE)

    def parse_args(args):
        pass

    def get_data(fmt, addr_expr):
        pass

    def convert_data(fmt, data):
        pass

BOExamine()
