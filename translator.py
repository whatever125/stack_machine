import sys
from isa import Opcode, Term, write_code


def get_meaningful_token(line: str) -> str:
    return line.split(";", 1)[0].strip()


def translate_stage_1(text: str) -> (list, dict[str: int]):
    code: list = []
    labels: dict[str: int] = {}

    for line_num, line in enumerate(text.splitlines(), 1):
        token: str = get_meaningful_token(line)
        if token == "":
            continue

        position: int = len(code)

        if token[-1] == ":":
            label: str = token[:-1]
            if label in labels.keys():
                raise Exception(f"redefinition of label `{label}` on line {line_num}")
            labels[label] = position
        elif " " in token:
            sub_tokens = token.split()
            if len(sub_tokens) != 2:
                raise Exception(f"invalid instruction: `{token}` on line {line_num}")
            mnemonic, arg = sub_tokens
            opcode: Opcode = Opcode(mnemonic.lower())
            match opcode:
                case Opcode.PUSH:
                    code.append({"opcode": opcode, "arg": arg, "term": Term(line_num, 0, token)})
                case Opcode.WORD:
                    code.append({"opcode": opcode, "arg": int(arg), "term": Term(line_num, 0, token)})
                case _:
                    raise Exception(f"`{opcode.upper()}` does not take an argument")
        else:
            opcode: Opcode = Opcode(token.lower())
            code.append({"opcode": opcode, "term": Term(line_num, 0, token)})
    return code, labels


def translate_stage_2(code: list, labels: dict[str: int]) -> list:
    for instruction in code:
        if instruction["opcode"] == Opcode.PUSH:
            label = instruction["arg"]
            if label not in labels.keys():
                raise Exception(f"label not defined: {label}")
            instruction["arg"] = labels[label]
    return code


def translate(text: str) -> list:
    code, labels = translate_stage_1(text)
    code = translate_stage_2(code, labels)
    return code


def main(source_name: str, target_name: str) -> None:
    with open(source_name) as file:
        text: str = file.read()

    code: list = translate(text)

    write_code(target_name, code)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise Exception("wrong arguments: translator.py <input_file> <target_file>")
    _, source, target = sys.argv
    main(source, target)
    print("translation successful")
