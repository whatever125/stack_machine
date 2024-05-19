from enum import StrEnum, auto


class Signal(StrEnum):
    DS_PUSH = auto()
    DS_POP = auto()

    LATCH_TOS = auto()
    SEL_TOS_DS = auto()
    SEL_TOS_MEMORY = auto()
    SEL_TOS_INPUT = auto()
    SEL_TOS_ALU = auto()

    LATCH_AR = auto()
    SEL_AR_TOS = auto()
    SEL_AR_PC = auto()

    LATCH_PC = auto()
    SEL_PC_NEXT = auto()
    SEL_PC_JMP_TYPE = auto()

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

    OUTPUT = auto()
    MEMORY = auto()

    HALT = auto()

    def __str__(self):
        return str(self.value)
