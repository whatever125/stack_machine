from enum import StrEnum, auto


class Signal(StrEnum):
    DS_PUSH = auto()
    DS_POP = auto()

    RS_PUSH = auto()
    RS_POP = auto()

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
    SEL_PC_RS = auto()

    LATCH_MPC = auto()
    SEL_MPC_ZERO = auto()
    SEL_MPC_OPCODE = auto()
    SEL_MPC_NEXT = auto()

    ALU_SUM = auto()
    ALU_SUB = auto()
    ALU_MUL = auto()
    ALU_DIV = auto()
    ALU_MOD = auto()
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

    # 3 - PUSH
    [Signal.DS_PUSH,
     Signal.LATCH_PC, Signal.SEL_PC_NEXT,
     Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
    # 4
    [Signal.LATCH_AR, Signal.SEL_AR_PC,
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

    # 13 - OVER
    [Signal.LATCH_BR,
     Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
    # 14
    [Signal.DS_POP,
     Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
    # 15
    [Signal.DS_PUSH,
     Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
    # 16
    [Signal.LATCH_TOS, Signal.SEL_TOS_BR,
     Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
    # 17
    [Signal.LATCH_BR,
     Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
    # 18
    [Signal.DS_PUSH,
     Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
    # 19
    [Signal.LATCH_TOS, Signal.SEL_TOS_BR,
     Signal.LATCH_PC, Signal.SEL_PC_NEXT,
     Signal.LATCH_MPC, Signal.SEL_MPC_ZERO],

    # 20 - INC
    [Signal.ALU_SUM, Signal.ALU_RIGHT_OP_ZERO, Signal.ALU_INC,
     Signal.LATCH_TOS, Signal.SEL_TOS_ALU,
     Signal.LATCH_PC, Signal.SEL_PC_NEXT,
     Signal.LATCH_MPC, Signal.SEL_MPC_ZERO],

    # 21 - DEC
    [Signal.ALU_SUM, Signal.ALU_RIGHT_OP_ZERO, Signal.ALU_DEC,
     Signal.LATCH_TOS, Signal.SEL_TOS_ALU,
     Signal.LATCH_PC, Signal.SEL_PC_NEXT,
     Signal.LATCH_MPC, Signal.SEL_MPC_ZERO],

    # 22 - ADD
    [Signal.ALU_SUM, Signal.ALU_RIGHT_OP_NOS,
     Signal.LATCH_TOS, Signal.SEL_TOS_ALU,
     Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
    # 23
    [Signal.DS_POP,
     Signal.LATCH_PC, Signal.SEL_PC_NEXT,
     Signal.LATCH_MPC, Signal.SEL_MPC_ZERO],

    # 24 - SUB
    [Signal.ALU_SUB, Signal.ALU_RIGHT_OP_NOS,
     Signal.LATCH_TOS, Signal.SEL_TOS_ALU,
     Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
    # 25
    [Signal.DS_POP,
     Signal.LATCH_PC, Signal.SEL_PC_NEXT,
     Signal.LATCH_MPC, Signal.SEL_MPC_ZERO],

    # 26 - MUL
    [Signal.ALU_MUL, Signal.ALU_RIGHT_OP_NOS,
     Signal.LATCH_TOS, Signal.SEL_TOS_ALU,
     Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
    # 27
    [Signal.DS_POP,
     Signal.LATCH_PC, Signal.SEL_PC_NEXT,
     Signal.LATCH_MPC, Signal.SEL_MPC_ZERO],

    # 28 - DIV
    [Signal.ALU_DIV, Signal.ALU_RIGHT_OP_NOS,
     Signal.LATCH_TOS, Signal.SEL_TOS_ALU,
     Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
    # 29
    [Signal.DS_POP,
     Signal.LATCH_PC, Signal.SEL_PC_NEXT,
     Signal.LATCH_MPC, Signal.SEL_MPC_ZERO],

    # 30 - MOD
    [Signal.ALU_MOD, Signal.ALU_RIGHT_OP_NOS,
     Signal.LATCH_TOS, Signal.SEL_TOS_ALU,
     Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
    # 31
    [Signal.DS_POP,
     Signal.LATCH_PC, Signal.SEL_PC_NEXT,
     Signal.LATCH_MPC, Signal.SEL_MPC_ZERO],

    # 32 - LOAD
    [Signal.LATCH_AR, Signal.SEL_AR_TOS,
     Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
    # 33
    [Signal.LATCH_TOS, Signal.SEL_TOS_MEMORY,
     Signal.LATCH_PC, Signal.SEL_PC_NEXT,
     Signal.LATCH_MPC, Signal.SEL_MPC_ZERO],

    # 34 - SAVE
    [Signal.LATCH_AR, Signal.SEL_AR_TOS,
     Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
    # 35
    [Signal.WRITE,
     Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
    # 36
    [Signal.DS_POP,
     Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
    # 37
    [Signal.LATCH_TOS, Signal.SEL_TOS_DS,
     Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
    # 38
    [Signal.DS_POP,
     Signal.LATCH_PC, Signal.SEL_PC_NEXT,
     Signal.LATCH_MPC, Signal.SEL_MPC_ZERO],

    # 39 - IN
    [Signal.LATCH_TOS, Signal.SEL_TOS_INPUT,
     Signal.LATCH_PC, Signal.SEL_PC_NEXT,
     Signal.LATCH_MPC, Signal.SEL_MPC_ZERO],

    # 40 - OUT
    [Signal.OUT,
     Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
    # 41
    [Signal.DS_POP,
     Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
    # 42
    [Signal.LATCH_TOS, Signal.SEL_TOS_DS,
     Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
    # 43
    [Signal.DS_POP,
     Signal.LATCH_PC, Signal.SEL_PC_NEXT,
     Signal.LATCH_MPC, Signal.SEL_MPC_ZERO],

    # 44 - JMP
    [Signal.LATCH_PC, Signal.SEL_PC_JMP,
     Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
    # 45
    [Signal.LATCH_TOS, Signal.SEL_TOS_DS,
     Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
    # 46
    [Signal.DS_POP,
     Signal.LATCH_MPC, Signal.SEL_MPC_ZERO],

    # 47 - JZ
    [Signal.LATCH_PC, Signal.SEL_PC_JZ,
     Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
    # 48
    [Signal.DS_POP,
     Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
    # 49
    [Signal.LATCH_TOS, Signal.SEL_TOS_DS,
     Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
    # 50
    [Signal.DS_POP,
     Signal.LATCH_MPC, Signal.SEL_MPC_ZERO],

    # 51 - CALL
    [Signal.RS_PUSH,
     Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
    # 52
    [Signal.LATCH_PC, Signal.SEL_PC_JMP,
     Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
    # 53
    [Signal.LATCH_TOS, Signal.SEL_TOS_DS,
     Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
    # 54
    [Signal.DS_POP,
     Signal.LATCH_MPC, Signal.SEL_MPC_ZERO],

    # 55 - RET
    [Signal.LATCH_PC, Signal.SEL_PC_RS,
     Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
    # 56
    [Signal.RS_POP,
     Signal.LATCH_MPC, Signal.SEL_MPC_ZERO],

    # 57 - HALT
    [Signal.HALT]
]
