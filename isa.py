import struct
from enum import IntEnum, auto


class Opcode(IntEnum):
    # no op
    NOP = auto()

    # stack ops
    PUSH = auto()
    POP = auto()
    SWAP = auto()
    DUP = auto()
    OVER = auto()

    # math
    INC = auto()
    DEC = auto()
    ADD = auto()
    SUB = auto()
    MUL = auto()
    DIV = auto()
    MOD = auto()

    # memory
    LOAD = auto()
    SAVE = auto()

    # io
    IN = auto()
    OUT = auto()

    # jump
    JMP = auto()
    JZ = auto()

    # functions
    CALL = auto()
    RET = auto()

    # stop
    HALT = auto()

    def __str__(self):
        return str(self.value)


def get_opcode_names():
    return [e.name for e in Opcode]


def read_code(filename: str) -> list:
    with open(filename, "rb") as file:
        data = file.read(4)
        index = 0
        start = struct.unpack("i", data)[0]
        code = [start]
        data = file.read(4)
        while data:
            index += 1
            if index >= start:
                if (
                    len(code) > 0
                    and isinstance(code[-1], Opcode)
                    and code[-1] in [Opcode.PUSH]
                ):
                    value = struct.unpack("i", data)[0]
                    code.append(value)
                else:
                    value = struct.unpack("i", data)[0]
                    opcode = Opcode(value)
                    code.append(opcode)
            else:
                value = struct.unpack("i", data)[0]
                code.append(value)
            data = file.read(4)
    return code


def write_code(target_name: str, code: list[int], commented_code: str):
    with open(target_name, "wb") as file:
        file.write(struct.pack(f"{len(code)}i", *code))
    with open(
        target_name[: target_name.find(".")] + "_com.txt", "w", encoding="utf-8"
    ) as file:
        file.write(commented_code)
