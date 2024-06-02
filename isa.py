import struct
from enum import IntEnum, auto


MEMORY_SIZE = 2048
BITS = 32
MIN_SIGN = -(2 ** (BITS - 1))
MAX_SIGN = 2 ** (BITS - 1) - 1


class Opcode(IntEnum):
    # no op
    NOP = 0x00000

    # stack ops
    PUSH = 0x00001
    POP = 0x00010
    SWAP = 0x00011
    DUP = 0x00100
    OVER = 0x00101

    # math ops
    INC = 0x00110
    DEC = 0x00111
    ADD = 0x01000
    SUB = 0x01001
    MUL = 0x01010
    DIV = 0x01011
    MOD = 0x01100

    # memory ops
    LOAD = 0x01101
    SAVE = 0x01110

    # io ops
    IN = 0x01111
    OUT = 0x10000

    # flow ops
    JMP = 0x10001
    JZ = 0x10010
    CALL = 0x10011
    RET = 0x10100
    HALT = 0x11111


def get_opcode_names() -> list[str]:
    return [e.name for e in Opcode]


def read_code(filename: str) -> list[Opcode | int]:
    with open(filename, "rb") as file:
        data = file.read(4)
        index = 0
        start: int = struct.unpack("i", data)[0]
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
                    value: int = struct.unpack("i", data)[0]
                    code.append(value)
                else:
                    value: int = struct.unpack("i", data)[0]
                    opcode = Opcode(value)
                    code.append(opcode)
            else:
                value: int = struct.unpack("i", data)[0]
                code.append(value)
            data = file.read(4)
    return code


def write_code(target_name: str, code: list[int]) -> None:
    with open(target_name, "wb") as file:
        file.write(struct.pack(f"{len(code)}i", *code))


def write_commented_code(target_name: str, code: str) -> None:
    with open(
        target_name[: target_name.find(".")] + "_com.txt", "w", encoding="utf-8"
    ) as file:
        file.write(code)
