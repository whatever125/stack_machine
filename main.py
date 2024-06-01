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

    io_unit = dp.IOUnit(input_buffer=input_tokens)
    io_controller = dp.IOController()
    io_controller.connect(port=1, unit=io_unit)

    logging.debug(code)
    logging.debug(input_tokens)
    data_path: dp.DataPath = dp.DataPath(
        memory_size=1024,
        program=code,
        io_controller=io_controller)
    control_unit: cu.ControlUnit = cu.ControlUnit(data_path=data_path)
    data_path.control_unit = control_unit

    ticks = control_unit.run_simulation()

    io_controller.disconnect(port=1)

    logging.info(f"Output: {io_unit.get_output()}")
    logging.info(f"Ticks: {ticks}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise Exception("Wrong arguments: machine.py <code_file> <input_file>")
    _, code_file, input_file = sys.argv
    main(code_file, input_file)
