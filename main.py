import logging
import sys
from collections import deque

from isa import read_code
import control_unit as cu
import data_path as dp


def main(code_file_name: str, input_file_name: str) -> None:
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

    code: list = read_code(code_file_name)
    with open(input_file_name, encoding="utf-8") as file:
        input_text: str = file.read()
    input_tokens: deque = deque(map(ord, input_text))
    input_tokens.appendleft(len(input_tokens))

    logging.debug(code)
    logging.debug(input_tokens)
    data_path: dp.DataPath = dp.DataPath(1024, code, input_tokens)
    control_unit: cu.ControlUnit = cu.ControlUnit(data_path)
    data_path.control_unit = control_unit

    output, ticks = control_unit.run_simulation()

    logging.info(f"Output: {output}")
    logging.info(f"Ticks: {ticks}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise Exception("Wrong arguments: machine.py <code_file> <input_file>")
    _, code_file, input_file = sys.argv
    main(code_file, input_file)
