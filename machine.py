import sys
from control_unit import ControlUnit
from data_path import DataPath
from isa import read_code


def main(code_file_name: str, input_file_name: str) -> None:
    code: list = read_code(code_file_name)
    with open(input_file_name, encoding="utf-8") as file:
        input_text: str = file.read()
        input_tokens: list[str] = list(input_text)

    data_path: DataPath = DataPath(1024, code, input_tokens)
    control_unit: ControlUnit = ControlUnit(data_path)

    output, instructions_counter, ticks = control_unit.run_simulation(1000)

    print("".join(output))
    print(f"instructions_counter: {instructions_counter}, ticks: {ticks}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise Exception("Wrong arguments: machine.py <code_file> <input_file>")
    _, code_file, input_file = sys.argv
    main(code_file, input_file)
