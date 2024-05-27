import logging
import sys
from machine import DataPath, ControlUnit
from isa import read_code
from collections import deque


def main(code_file_name: str, input_file_name: str) -> None:
    logging.basicConfig(level=logging.ERROR, stream=sys.stdout)

    code: list = read_code(code_file_name)
    with open(input_file_name, encoding="utf-8") as file:
        input_text: str = file.read()
        input_tokens: deque = deque(input_text)
    input_tokens.append(0)

    logging.debug(code)
    logging.debug(input_tokens)
    data_path: DataPath = DataPath(1024, code, input_tokens)
    control_unit: ControlUnit = ControlUnit(data_path)
    data_path._control_unit = control_unit

    output, instructions_counter, ticks = control_unit.run_simulation(1000)

    print(f"Output: {''.join(output)}")
    print(f"Instructions_counter: {instructions_counter}, ticks: {ticks}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise Exception("Wrong arguments: machine.py <code_file> <input_file>")
    _, code_file, input_file = sys.argv
    main(code_file, input_file)
