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
    return bool(re.fullmatch(r"^0*[1-9]\d*$", value))


def is_str(value: str) -> bool:
    return bool(re.fullmatch(r"^(\".*\")|(\'.*\')$", value))


def is_bf(value: str) -> bool:
    return bool(re.fullmatch(r"^bf\s+\d+$", value))


def is_opcode0(value: str) -> bool:
    return bool(re.fullmatch(r"^\w+$", value))


def is_opcode1(value: str) -> bool:
    return bool(re.fullmatch(r"^\w+ +\w+$", value))


def translate_stage_1(text: str) -> Tuple[dict[str, int | list[int]], list[Opcode | str], dict[str, int], int]:
    data: dict[str, int | list[int]] = {}
    code: list[Opcode | str] = []
    labels: dict[str, int] = {}
    position = 1
    code_position = position
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
            code_position = position
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
                    pstr = [len(value) - 2] + [ord(c) for c in value[1:-1]]
                    data[name] = pstr
                    labels[name] = position
                    position += len(pstr)
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

        elif is_opcode1(token):
            if data_mode:
                raise Exception(f"instruction inside data section on line {line_num}")
            elif code_mode:
                mnemonic: str
                arg: str
                mnemonic, arg = list(map(lambda s: s.strip(), token.split()))
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

        elif is_opcode0(token):
            if data_mode:
                raise Exception(f"instruction inside data section on line {line_num}")
            elif code_mode:
                if token.upper() not in get_opcode_names():
                    raise Exception(f"invalid mnemonic: `{token}` on line {line_num}")
                opcode = Opcode[token.upper()]
                if opcode in [Opcode.PUSH]:
                    raise Exception(f"`{token.upper()}` must take an argument")
                code.append(opcode)
                position += 1
            else:
                raise Exception(f"instruction outside of any section on line {line_num}")

        else:
            raise Exception(f"invalid instruction format on line {line_num}")

    return data, code, labels, code_position


def translate_stage_2(data: dict[str, int | list[int]], code: list[Opcode | str], labels: dict[str, int]) -> list[int]:
    plain_data: list[int] = [item for element in data.values()
                             for item in (element if isinstance(element, list) else [element])]
    plain_data.insert(0, len(plain_data) + 1)
    plain_code: list[int] = []

    for element in code:
        if isinstance(element, Opcode):
            plain_code.append(element.value)
        elif isinstance(element, str):
            if element not in labels.keys():
                raise Exception(f"label not defined: {element}")
            plain_code.append(labels[element])

    return plain_data + plain_code


def value_to_binary32(value: int) -> str:
    formatted_value = format(value & 0xFFFFFFFF, "032b")
    indices = [0, 4, 8, 12, 16, 20, 24, 28, 32]
    return " ".join([formatted_value[i:j] for i, j in zip(indices, indices[1:]+[None])])


def comment_code(data: dict[str, int | list[int]], code: list[Opcode | str], labels: dict[str, int], code_position: int) -> str:
    address = 0
    commented_code = [f"{address}\t{value_to_binary32(code_position)}\tstart_address = {code_position}"]
    for name, data_value in data.items():
        if isinstance(data_value, int):
            address += 1
            commented_code.append(f"{address}\t{value_to_binary32(data_value)}\t{name} = {data_value}")
        elif isinstance(data_value, list):
            address += 1
            commented_code.append(f"{address}\t{value_to_binary32(data_value[0])}\t{name} : {data_value[0]}")
            for i in data_value[1:]:
                address += 1
                if data_value[0] == 0:
                    commented_code.append(f"{address}\t{value_to_binary32(i)}\t{" " * len(name)}   {i}")
                else:
                    commented_code.append(f"{address}\t{value_to_binary32(i)}\t{" " * len(name)}  `{chr(i)}`")
    for code_value in code:
        address += 1
        if isinstance(code_value, str):
            commented_code.append(f"{address}\t{value_to_binary32(labels[code_value])}\t{code_value}")
        elif isinstance(code_value, Opcode):
            commented_code.append(f"{address}\t{value_to_binary32(code_value)}\t{code_value.name}")
    return "\n".join(commented_code)


def translate(text: str) -> Tuple[list[int], str]:
    data, code, labels, code_position = translate_stage_1(text)
    commented_code = comment_code(data, code, labels, code_position)
    translated_code = translate_stage_2(data, code, labels)
    return translated_code, commented_code


def main(source_name: str, target_name: str) -> None:
    with open(source_name, encoding="utf-8") as file:
        text: str = file.read()

    code, commented_code = translate(text)

    write_code(target_name, code, commented_code)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise Exception("wrong arguments: translator.py <input_file> <target_file>")
    _, source, target = sys.argv
    main(source, target)
    print("translation successful")
