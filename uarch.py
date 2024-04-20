from enum import StrEnum, auto


class Signal(StrEnum):
    DS_PUSH = auto()
    DS_POP = auto()

    LATCH_TOS_DS = auto()
    LATCH_TOS_MEMORY = auto()
    LATCH_TOS_INPUT = auto()
    LATCH_TOS_ALU = auto()

    LATCH_AR_TOS = auto()
    LATCH_AR_PC = auto()

    LATCH_PC_NEXT = auto()
    LATCH_PC_JMP = auto()
    LATCH_PC_JZ = auto()

    LATCH_MPC_ZERO = auto()
    LATCH_MPC_OPCODE = auto()
    LATCH_MPC_NEXT = auto()

    ALU_SUM = auto()
    ALU_SUB = auto()
    ALU_MUL = auto()
    ALU_DIV = auto()
    ALU_INC = auto()
    ALU_DEC = auto()
    ALU_RIGHT_OP_NOS = auto()
    ALU_RIGHT_OP_ZERO = auto()

    OUTPUT = auto()
    MEMORY = auto()

    HALT = auto()

    def __str__(self):
        return str(self.value)
