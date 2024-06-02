import struct
from enum import IntEnum, auto


MEMORY_SIZE = 2048
BITS = 32
MIN_SIGN = -(2 ** (BITS - 1))
MAX_SIGN = 2 ** (BITS - 1) - 1


class Opcode(IntEnum):
    # no op
    NOP = 0b00000

    # stack ops
    PUSH = 0b00001
    POP = 0b00010
    SWAP = 0b00011
    DUP = 0b00100
    OVER = 0b00101

    # math ops
    INC = 0b00110
    DEC = 0b00111
    ADD = 0b01000
    SUB = 0b01001
    MUL = 0b01010
    DIV = 0b01011
    MOD = 0b01100

    # memory ops
    LOAD = 0b01101
    SAVE = 0b01110

    # io ops
    IN = 0b01111
    OUT = 0b10000

    # flow ops
    JMP = 0b10001
    JZ = 0b10010
    CALL = 0b10011
    RET = 0b10100
    HALT = 0b11111


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
                    value = struct.unpack("i", data)[0]
                    opcode = Opcode(value)
                    code.append(opcode)
            else:
                value = struct.unpack("i", data)[0]
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
