import re
import sys
from typing import Tuple

from isa import Opcode, write_code, get_opcode_names


def get_meaningful_token(line: str) -> str:
    return line.split(";", 1)[0].strip()


def is_label(value: str) -> bool:
    return bool(re.fullmatch(r"^[a-zA-Z_][a-zA-Z_0-9]*\s*:$", value))


def is_variable(value: str) -> bool:
    return bool(re.fullmatch(
        r"^[a-zA-Z_][a-zA-Z_0-9]*\s*:\s*((-?\d+)|(\"[^\"]*\")|(\'[^\']*\')|(bf\s+\d+))$",
        value))


def is_int(value: str) -> bool:
    return bool(re.fullmatch(r"^-?\d+$", value))


def is_positive_int(value: str) -> bool:
    return bool(re.fullmatch(r"^\d+$", value))


def is_str(value: str) -> bool:
    return bool(re.fullmatch(r"^(\".*\")|(\'.*\')$", value))


def is_bf(value: str) -> bool:
    return bool(re.fullmatch(r"^bf\s+\d+$", value))


def is_opcode0(value: str) -> bool:
    return value.upper() in get_opcode_names()


def is_opcode1(value: str) -> bool:
    pass


def translate_stage_1(text: str) -> Tuple[dict[str, int | list[int]], list[int | str], dict[str, int]]:
    data: dict[str, int | list[int]] = {}
    code: list[int | str] = []
    labels: dict[str, int] = {}
    position = 1
    data_mode = False
    code_mode = False

    for line_num, line in enumerate(text.splitlines(), 1):
        token: str = get_meaningful_token(line)
        if token == "":
            continue

        if token == "section data:":
            if data_mode or code_mode:
                raise Exception(f"wrong section on line {line_num}")
            data_mode = True
            continue
        if token == "section code:":
            if code_mode:
                raise Exception(f"wrong section on line {line_num}")
            code_mode = True
            data_mode = False
            continue

        if is_variable(token):
            if data_mode:
                name: str
                value: str
                name, value = map(lambda s: s.strip(), token.split(":", maxsplit=1))
                if name in labels:
                    raise Exception(f"redefinition of label `{name}` on line {line_num}")
                if is_int(value):
                    data[name] = int(value)
                    labels[name] = position
                    position += 1
                elif is_str(value):
                    data[name] = [len(value) - 2] + [ord(c) for c in value[1:-1]]
                    labels[name] = position
                    position += len(data[name])
                elif is_bf(value):
                    _, size = value.split(maxsplit=1)
                    if is_positive_int(size):
                        data[name] = [0] * int(size)
                        labels[name] = position
                        position += int(size)
                    else:
                        raise Exception(f"buffer size is not positive integer on line {line_num}")
                else:
                    raise Exception(f"invalid variable: `{token}` on line {line_num}")
            elif code_mode:
                raise Exception(f"variable inside code section on line {line_num}")
            else:
                raise Exception(f"variable outside of any section on line {line_num}")

        elif is_label(token):
            if data_mode:
                raise Exception(f"label inside data section on line {line_num}")
            elif code_mode:
                label: str = token[:-1]
                if label in labels:
                    raise Exception(f"redefinition of label `{label}` on line {line_num}")
                labels[label] = position
            else:
                raise Exception(f"label outside of any section on line {line_num}")

        elif " " in token:
            if data_mode:
                raise Exception(f"instruction inside data section on line {line_num}")
            elif code_mode:
                sub_tokens = list(map(lambda s: s.strip(), token.split()))
                if len(sub_tokens) != 2:
                    raise Exception(f"invalid instruction: `{token}` on line {line_num}")
                mnemonic: str
                arg: str
                mnemonic, arg = sub_tokens
                if mnemonic.upper() not in get_opcode_names():
                    raise Exception(f"invalid mnemonic: `{mnemonic}` on line {line_num}")
                opcode: Opcode = Opcode[mnemonic.upper()]
                match opcode:
                    case Opcode.PUSH:
                        code.append(opcode)
                        code.append(arg)
                        position += 2
                    case _:
                        raise Exception(f"`{opcode.name.upper()}` does not take an argument")
            else:
                raise Exception(f"instruction outside of any section on line {line_num}")

        else:
            if data_mode:
                raise Exception(f"instruction inside data section on line {line_num}")
            elif code_mode:
                if token.upper() not in get_opcode_names():
                    raise Exception(f"invalid mnemonic: `{token}` on line {line_num}")
                opcode = Opcode[token.upper()]
                code.append(opcode)
                position += 1
            else:
                raise Exception(f"instruction outside of any section on line {line_num}")

    return data, code, labels


def translate_stage_2(data: dict[str, int | list[int]], code: list[int | str], labels: dict[str, int]) -> list:
    plain_data: list[int] = [item for element in data.values()
                             for item in (element if isinstance(element, list) else [element])]
    code: list[int | str] = [len(plain_data) + 1] + plain_data + code

    for index, instruction in enumerate(code):
        if isinstance(code[index], Opcode):
            if instruction in [Opcode.PUSH]:
                label = code[index + 1]
                if label not in labels.keys():
                    raise Exception(f"label not defined: {label}")
                code[index + 1] = labels[label]
            code[index] = instruction.value
    return code


def translate(text: str) -> list:
    data, code, labels = translate_stage_1(text)
    code = translate_stage_2(data, code, labels)
    return code


def main(source_name: str, target_name: str) -> None:
    with open(source_name, encoding="utf-8") as file:
        text: str = file.read()

    code: list = translate(text)

    write_code(target_name, code)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise Exception("wrong arguments: translator.py <input_file> <target_file>")
    _, source, target = sys.argv
    main(source, target)
    print("translation successful")
