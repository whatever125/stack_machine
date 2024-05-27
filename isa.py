from enum import StrEnum, auto
import json


class Term:
    line: int = None
    position: int = None
    symbol: str = None

    def __init__(self, line: int, position: int, symbol: str):
        self.line = line
        self.position = position
        self.symbol = symbol


class Opcode(StrEnum):
    # no op
    NOP = auto()
    WORD = auto()

    # stack ops
    PUSH = auto()
    POP = auto()
    SWAP = auto()
    DUP = auto()

    # math
    INC = auto()
    DEC = auto()
    ADD = auto()
    SUB = auto()
    MUL = auto()
    DIV = auto()

    # memory
    LOAD = auto()
    SAVE = auto()

    # io
    IN = auto()
    OUT = auto()

    # jump
    JMP = auto()
    JZ = auto()

    # stop
    HALT = auto()

    def __str__(self):
        return str(self.value)


def read_code(filename: str) -> list:
    with open(filename, encoding="utf-8") as file:
        code: list = json.loads(file.read())

    for instruction in code:
        if "opcode" not in instruction:
            raise Exception(f"incorrect json - no opcode in instruction: {instruction}")
        instruction["opcode"] = Opcode(instruction["opcode"])
        if "term" in instruction:
            if len(instruction["term"]) != 3:
                raise Exception(f"incorrect json - incorrect term: {instruction["term"]}")
            instruction["term"] = Term(int(instruction["term"]["line"]),
                                       int(instruction["term"]["position"]),
                                       instruction["term"]["symbol"])
    return code


def write_code(target_name: str, code: list) -> None:
    with open(target_name, "w", encoding="utf-8") as file:
        buffer = []
        for instruction in code:
            buffer.append(json.dumps(instruction, default=vars))
        file.write("[" + ",\n ".join(buffer) + "]")
        # file.write(json.dumps(code, indent=2, default=vars))
