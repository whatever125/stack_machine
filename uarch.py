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

    # 12 - OVER TODO
    [Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
    # 13
    [Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
    # 14
    [Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
    # 15
    [Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
    # 16
    [Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
    # 17
    [Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
    # 18
    [Signal.LATCH_PC, Signal.SEL_PC_NEXT,
     Signal.LATCH_MPC, Signal.SEL_MPC_ZERO],

    # 19 - INC
    [Signal.ALU_SUM, Signal.ALU_RIGHT_OP_ZERO, Signal.ALU_INC,
     Signal.LATCH_TOS, Signal.SEL_TOS_ALU,
     Signal.LATCH_PC, Signal.SEL_PC_NEXT,
     Signal.LATCH_MPC, Signal.SEL_MPC_ZERO],

    # 20 - DEC
    [Signal.ALU_SUM, Signal.ALU_RIGHT_OP_ZERO, Signal.ALU_DEC,
     Signal.LATCH_TOS, Signal.SEL_TOS_ALU,
     Signal.LATCH_PC, Signal.SEL_PC_NEXT,
     Signal.LATCH_MPC, Signal.SEL_MPC_ZERO],

    # 21 - ADD
    [Signal.ALU_SUM, Signal.ALU_RIGHT_OP_NOS,
     Signal.LATCH_TOS, Signal.SEL_TOS_ALU,
     Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
    # 22
    [Signal.DS_POP,
     Signal.LATCH_PC, Signal.SEL_PC_NEXT,
     Signal.LATCH_MPC, Signal.SEL_MPC_ZERO],

    # 23 - SUB
    [Signal.ALU_SUB, Signal.ALU_RIGHT_OP_NOS,
     Signal.LATCH_TOS, Signal.SEL_TOS_ALU,
     Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
    # 24
    [Signal.DS_POP,
     Signal.LATCH_PC, Signal.SEL_PC_NEXT,
     Signal.LATCH_MPC, Signal.SEL_MPC_ZERO],

    # 25 - MUL
    [Signal.ALU_MUL, Signal.ALU_RIGHT_OP_NOS,
     Signal.LATCH_TOS, Signal.SEL_TOS_ALU,
     Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
    # 26
    [Signal.DS_POP,
     Signal.LATCH_PC, Signal.SEL_PC_NEXT,
     Signal.LATCH_MPC, Signal.SEL_MPC_ZERO],

    # 27 - DIV
    [Signal.ALU_DIV, Signal.ALU_RIGHT_OP_NOS,
     Signal.LATCH_TOS, Signal.SEL_TOS_ALU,
     Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
    # 28
    [Signal.DS_POP,
     Signal.LATCH_PC, Signal.SEL_PC_NEXT,
     Signal.LATCH_MPC, Signal.SEL_MPC_ZERO],

    # 29 - LOAD
    [Signal.LATCH_AR, Signal.SEL_AR_TOS,
     Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
    # 30
    [Signal.LATCH_TOS, Signal.SEL_TOS_MEMORY,
     Signal.LATCH_PC, Signal.SEL_PC_NEXT,
     Signal.LATCH_MPC, Signal.SEL_MPC_ZERO],

    # 31 - SAVE
    [Signal.LATCH_AR, Signal.SEL_AR_TOS,
     Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
    # 32
    [Signal.WRITE,
     Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
    # 33
    [Signal.DS_POP,
     Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
    # 34
    [Signal.LATCH_TOS, Signal.SEL_TOS_DS,
     Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
    # 35
    [Signal.DS_POP,
     Signal.LATCH_PC, Signal.SEL_PC_NEXT,
     Signal.LATCH_MPC, Signal.SEL_MPC_ZERO],

    # 36 - IN
    [Signal.LATCH_TOS, Signal.SEL_TOS_INPUT,
     Signal.LATCH_PC, Signal.SEL_PC_NEXT,
     Signal.LATCH_MPC, Signal.SEL_MPC_ZERO],

    # 37 - OUT
    [Signal.OUT,
     Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
    # 38
    [Signal.DS_POP,
     Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
    # 39
    [Signal.LATCH_TOS, Signal.SEL_TOS_DS,
     Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
    # 40
    [Signal.DS_POP,
     Signal.LATCH_PC, Signal.SEL_PC_NEXT,
     Signal.LATCH_MPC, Signal.SEL_MPC_ZERO],

    # 41 - JMP
    [Signal.LATCH_PC, Signal.SEL_PC_JMP,
     Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
    # 42
    [Signal.LATCH_TOS, Signal.SEL_TOS_DS,
     Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
    # 43
    [Signal.DS_POP,
     Signal.LATCH_PC, Signal.SEL_PC_NEXT,
     Signal.LATCH_MPC, Signal.SEL_MPC_ZERO],

    # 44 - JZ
    [Signal.LATCH_PC, Signal.SEL_PC_JZ,
     Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
    # 45
    [Signal.DS_POP,
     Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
    # 46
    [
     Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
    # 47
    [
     Signal.LATCH_MPC, Signal.SEL_MPC_ZERO],

    # 48 - HALT
    [Signal.HALT]
]
