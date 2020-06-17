"""CPU functionality."""

import sys


NOP = 0b00000000  # NO OP
LDI = 0b10000010  # load "immediate", set/store value in register
HLT = 0b00000001  # halt the CPU and exit the emulator
PRN = 0b01000111  # print the numeric value stored in a register
LD = 0b10000011
ST = 0b10000100
PUSH = 0b01000101
POP = 0b01000110
PRA = 0b01001000

# ALU ops
ADD = 0b10100000  # add
SUB = 0b10100001  # subtract
MUL = 0b10100010  # multiply
MOD = 0b10100100  # modulo
INC = 0b01100101  # increment
DEC = 0b01100110  # decrement
CMP = 0b10100111  # compute
AND = 0b10101000  # &
NOT = 0b01101001  # !
OR = 0b10101010  # |
XOR = 0b10101011  # ^
SHL = 0b10101100
SHR = 0b10101101
ALU_OP_LIST = [ADD, SUB, MUL, INC, DEC, CMP, AND, NOT, OR, XOR, SHL, SHR, MOD]
ALU_OP_FUNC = [lambda a, b: b+a, lambda a, b: a-b, lambda a, b: b * a, lambda a: a+1,
               lambda a: a-1, lambda a, b: b == a, lambda a, b: b & a, lambda a: a ^ 0b11111111,
               lambda a, b: a | b, lambda a, b: b ^ a, lambda a, b: a << b, lambda a, b: a >> b, lambda a, b: a % b]
ALU_DISPATCH = dict(zip(ALU_OP_LIST, ALU_OP_FUNC))

# PC mutators
CALL = 0b01010000
RET = 0b00010001
INT = 0b01010010
IRET = 0b00010011
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110
JGT = 0b01010111
JLT = 0b01011000
JLE = 0b01011001
JGE = 0b01011010
MUTATORS = [CALL, RET, INT, IRET, JMP, JEQ, JNE, JGT, JLT, JLE, JGE]

SP = 7


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # `R0`-`R6` are cleared to `0`.
        self.reg = [0] * 8  # 8 general-purpose registers
        # `PC` and `FL` registers are cleared to `0`.
        self.pc = 0  # the program counter
        self.fl = 0  # The flags register
        self.ram = [0] * 256  # 256 bytes of memory
        # `R7` is set to `0xF4`.
        self.reg[SP] = 0xF4

    def ram_read(self, mar):
        """
        return value stored at memory address register
        """
        return self.ram[mar]

    def ram_write(self, mar, mdr):
        """
        store memory data register at memory address register
        """
        self.ram[mar] = mdr

    def load(self, program):
        """Load a program into memory."""
        address = 0
        # For now, we've just hardcoded a program:
        if program is None:
            print("no program specified")
            return
        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        # print('maths')
        try:
            foo = ALU_DISPATCH[op]
        except Exception:
            raise Exception("Unsupported ALU operation")
        if reg_b is not None:
            bar = foo(self.reg[reg_a], self.reg[reg_b])
        else:
            bar = foo(self.reg[reg_a])
        return bar

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def push(self, from_register):
        self.reg[SP] -= 1  # decrement the stack pointer
        mar = self.reg[SP]  # this is where we push to
        mdr = self.reg[from_register]  # this is what we push
        self.ram_write(mar, mdr)  # write to memory address

    def pop(self, to_register):
        mar = self.reg[SP]  # get the stack pointer
        popped = self.ram_read(mar)  # read stack at position
        # increment the stack pointer if possible
        if mar < 0xF4:
            self.reg[SP] += 1
        # store result in register
        self.reg[to_register] = popped

    def ldi_foo(self, a, b):
        # place value b into register a
        self.reg[a] = b

    def print_foo(self, a):
        print(self.reg[a])

    def dispatch(self, i, a, b):
        """ return function to be called """
        # first check the memory functions
        foo = dict(zip([LDI, PRN, PUSH, POP],
                       [self.ldi_foo, self.print_foo, self.push, self.pop])).get(i, None)
        if foo is None:
            # is it math then?
            arithmetic = ALU_DISPATCH.get(i, None)
            if arithmetic is not None:
                # store the result in register a
                self.reg[a] = self.alu(i, a, b)
                return
        else:
            if b is not None:
                foo(a, b)
            elif a is not None:
                foo(a)
            else:
                foo()

    def run(self):
        """Run the CPU."""
        # It needs to read the memory address that's stored in register `PC`, and store
        # that result in `IR`, the _Instruction Register_. This can just be a local
        # variable in `run()`.
        IR = self.pc
        # LOOP
        while True:
            # READ
            i = self.ram_read(IR)
            ops = (i & 0b11000000) >> 6
            # check the last 2 bits and determine
            # how many bytes to include with this instruction.
            if ops == 2:
                # read the next two bytes,
                a = self.ram_read(IR+1)
                b = self.ram_read(IR+2)
                # increment the program counter by 3
                IR += 3
            elif ops == 1:
                # read the next byte
                a = self.ram_read(IR+1)
                b = None
                # increment the program counter by 2
                IR += 2
            else:
                # only read instruction, increment by 1
                IR += 1
            # EVALUATE
            if HLT == i:
                break
            self.dispatch(i, a, b)
