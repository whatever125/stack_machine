from enum import StrEnum, auto


class Signal(StrEnum):
    DS_PUSH = auto()
    DS_POP = auto()

    LATCH_TOS = auto()
    SEL_TOS_DS = auto()
    SEL_TOS_MEMORY = auto()
    SEL_TOS_INPUT = auto()
    SEL_TOS_ALU = auto()
    SEL_TOS_BR = auto()

    LATCH_AR = auto()
    SEL_AR_TOS = auto()
    SEL_AR_PC = auto()

    LATCH_BR = auto()

    LATCH_PC = auto()
    SEL_PC_NEXT = auto()
    SEL_PC_JMP = auto()
    SEL_PC_JZ = auto()

    LATCH_MPC = auto()
    SEL_MPC_ZERO = auto()
    SEL_MPC_OPCODE = auto()
    SEL_MPC_NEXT = auto()

    ALU_SUM = auto()
    ALU_SUB = auto()
    ALU_MUL = auto()
    ALU_DIV = auto()
    ALU_INC = auto()
    ALU_DEC = auto()
    ALU_RIGHT_OP_NOS = auto()
    ALU_RIGHT_OP_ZERO = auto()

    OUT = auto()
    WRITE = auto()

    HALT = auto()

    def __str__(self):
        return str(self.value)


MICROPROGRAM = [
    # 0 - INSTRUCTION FETCH
    [Signal.LATCH_AR, Signal.SEL_AR_PC,
     Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
    # 1
    [Signal.LATCH_MPC, Signal.SEL_MPC_OPCODE],

    # 2 - NOP
    [Signal.LATCH_PC, Signal.SEL_PC_NEXT,
     Signal.LATCH_MPC, Signal.SEL_MPC_ZERO],

    # 3 - WORD
    [Signal.LATCH_PC, Signal.SEL_PC_NEXT,
     Signal.LATCH_MPC, Signal.SEL_MPC_ZERO],

    # 4 - PUSH
    [Signal.DS_PUSH,
     Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
    # 5
    [Signal.LATCH_TOS, Signal.SEL_TOS_MEMORY,
     Signal.LATCH_PC, Signal.SEL_PC_NEXT,
     Signal.LATCH_MPC, Signal.SEL_MPC_ZERO],

    # 6 - POP
    [Signal.LATCH_TOS, Signal.SEL_TOS_DS,
     Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
    # 7
    [Signal.DS_POP,
     Signal.LATCH_PC, Signal.SEL_PC_NEXT,
     Signal.LATCH_MPC, Signal.SEL_MPC_ZERO],

    # 8 - SWAP
    [Signal.LATCH_BR,
     Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
    # 9
    [Signal.DS_POP,
     Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
    # 10
    [Signal.DS_PUSH,
     Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
    # 11
    [Signal.LATCH_TOS, Signal.SEL_TOS_BR,
     Signal.LATCH_PC, Signal.SEL_PC_NEXT,
     Signal.LATCH_MPC, Signal.SEL_MPC_ZERO],

    # 12 - DUP
    [Signal.DS_PUSH,
     Signal.LATCH_PC, Signal.SEL_PC_NEXT,
     Signal.LATCH_MPC, Signal.SEL_MPC_ZERO],

    # 13 - INC
    [Signal.ALU_SUM, Signal.ALU_RIGHT_OP_ZERO, Signal.ALU_INC,
     Signal.LATCH_TOS, Signal.SEL_TOS_ALU,
     Signal.LATCH_PC, Signal.SEL_PC_NEXT,
     Signal.LATCH_MPC, Signal.SEL_MPC_ZERO],

    # 14 - DEC
    [Signal.ALU_SUM, Signal.ALU_RIGHT_OP_ZERO, Signal.ALU_DEC,
     Signal.LATCH_TOS, Signal.SEL_TOS_ALU,
     Signal.LATCH_PC, Signal.SEL_PC_NEXT,
     Signal.LATCH_MPC, Signal.SEL_MPC_ZERO],

    # 15 - ADD
    [Signal.ALU_SUM, Signal.ALU_RIGHT_OP_NOS,
     Signal.LATCH_TOS, Signal.SEL_TOS_ALU,
     Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
    # 16
    [Signal.DS_POP,
     Signal.LATCH_PC, Signal.SEL_PC_NEXT,
     Signal.LATCH_MPC, Signal.SEL_MPC_ZERO],

    # 17 - SUB
    [Signal.ALU_SUB, Signal.ALU_RIGHT_OP_NOS,
     Signal.LATCH_TOS, Signal.SEL_TOS_ALU,
     Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
    # 18
    [Signal.DS_POP,
     Signal.LATCH_PC, Signal.SEL_PC_NEXT,
     Signal.LATCH_MPC, Signal.SEL_MPC_ZERO],

    # 19 - MUL
    [Signal.ALU_MUL, Signal.ALU_RIGHT_OP_NOS,
     Signal.LATCH_TOS, Signal.SEL_TOS_ALU,
     Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
    # 20
    [Signal.DS_POP,
     Signal.LATCH_PC, Signal.SEL_PC_NEXT,
     Signal.LATCH_MPC, Signal.SEL_MPC_ZERO],

    # 21 - DIV
    [Signal.ALU_DIV, Signal.ALU_RIGHT_OP_NOS,
     Signal.LATCH_TOS, Signal.SEL_TOS_ALU,
     Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
    # 22
    [Signal.DS_POP,
     Signal.LATCH_PC, Signal.SEL_PC_NEXT,
     Signal.LATCH_MPC, Signal.SEL_MPC_ZERO],

    # 23 - LOAD
    [Signal.LATCH_AR, Signal.SEL_AR_TOS,
     Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
    # 24
    [Signal.LATCH_TOS, Signal.SEL_TOS_MEMORY,
     Signal.LATCH_PC, Signal.SEL_PC_NEXT,
     Signal.LATCH_MPC, Signal.SEL_MPC_ZERO],

    # 25 - SAVE
    [Signal.LATCH_AR, Signal.SEL_AR_TOS,
     Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
    # 26
    [Signal.WRITE,
     Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
    # 27
    [Signal.DS_POP,
     Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
    # 28
    [Signal.LATCH_TOS, Signal.SEL_TOS_DS,
     Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
    # 29
    [Signal.DS_POP,
     Signal.LATCH_PC, Signal.SEL_PC_NEXT,
     Signal.LATCH_MPC, Signal.SEL_MPC_ZERO],

    # 30 - IN
    [Signal.LATCH_TOS, Signal.SEL_TOS_INPUT,
     Signal.LATCH_PC, Signal.SEL_PC_NEXT,
     Signal.LATCH_MPC, Signal.SEL_MPC_ZERO],

    # 31 - OUT
    [Signal.OUT,
     Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
    # 32
    [Signal.DS_POP,
     Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
    # 33
    [Signal.LATCH_TOS, Signal.SEL_TOS_DS,
     Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
    # 34
    [Signal.DS_POP,
     Signal.LATCH_PC, Signal.SEL_PC_NEXT,
     Signal.LATCH_MPC, Signal.SEL_MPC_ZERO],

    # 35 - JMP
    [Signal.LATCH_PC, Signal.SEL_PC_JMP,
     Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
    # 36
    [Signal.LATCH_TOS, Signal.SEL_TOS_DS,
     Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
    # 37
    [Signal.DS_POP,
     Signal.LATCH_MPC, Signal.SEL_MPC_ZERO],

    # 38 - JZ
    [Signal.LATCH_PC, Signal.SEL_PC_JZ,
     Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
    # 39
    [Signal.DS_POP,
     Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
    # 40
    [Signal.LATCH_TOS, Signal.SEL_TOS_DS,
     Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
    # 41
    [Signal.DS_POP,
     Signal.LATCH_MPC, Signal.SEL_MPC_ZERO],

    # 42 - HALT
    [Signal.HALT]
]
