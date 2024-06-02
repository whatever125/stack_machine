import argparse
import logging
from collections import deque

from isa import read_code
import control_unit as cu
import data_path as dp


def main(code_file: str, input_file: str | None, tick_limit: int, char_output: bool, debug_logging: bool, debug_limit: int | None) -> None:
    logging.getLogger().setLevel(logging.DEBUG if debug_logging else logging.INFO)

    code = read_code(code_file)

    if input_file is None:
        input_tokens: deque = deque()
    else:
        with open(input_file, encoding="utf-8") as file:
            input_text: str = file.read()
        input_tokens: deque = deque(map(ord, input_text))
        input_tokens.appendleft(len(input_tokens))

    io_unit = dp.IOUnit(input_buffer=input_tokens)
    io_controller = dp.IOController()
    io_controller.connect(port=1, unit=io_unit)

    data_path: dp.DataPath = dp.DataPath(
        program=code,
        io_controller=io_controller)
    control_unit: cu.ControlUnit = cu.ControlUnit(data_path=data_path)
    data_path.control_unit = control_unit

    ticks, instructions = control_unit.run_simulation(tick_limit=tick_limit, debug_limit=debug_limit)

    io_controller.disconnect(port=1)

    if char_output:
        print(f"Output: {io_unit.get_str_output()}")
    else:
        print(f"Output: {io_unit.get_list_output()}")
    print(f"Ticks: {ticks}, Instructions: {instructions}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Stack processor simulation")
    parser.add_argument("code_file", help="Binary code file name")
    parser.add_argument("input_file", nargs="?", help="Input file name (optional)")
    parser.add_argument("-l", "--limit", type=int, default=200000, help="Tick limit (default - 200000)")
    parser.add_argument("-c", "--char", action='store_true', help="Char output (default - list[int])")
    parser.add_argument("-d", "--debug", action='store_true', help="Debug logging (default - info)")
    parser.add_argument("--debug-limit", type=int, help="Debug limit")

    args = parser.parse_args()

    try:
        main(args.code_file, args.input_file, args.limit, args.char, args.debug, args.debug_limit)
    except Exception as e:
        logging.error(e)
        raise e
