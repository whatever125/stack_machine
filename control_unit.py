import logging
from typing import Tuple

from isa import Opcode
from uarch import Signal, MICROPROGRAM
import data_path as dp


class ControlUnit:
    def __init__(self, data_path: dp.DataPath) -> None:
        self._data_path: dp.DataPath = data_path
        self._program_counter: int = 0
        self._micro_program_counter: int = 0
        self._current_tick: int = 0
        self._microprogram: list = MICROPROGRAM

    def _tick(self) -> None:
        self._current_tick += 1

    def _opcode_to_mpc(self, opcode: Opcode) -> int:
        addresses = {
            Opcode.NOP: 2,
            Opcode.WORD: 3,
            Opcode.PUSH: 4,
            Opcode.POP: 6,
            Opcode.SWAP: 8,
            Opcode.DUP: 12,
            Opcode.INC: 13,
            Opcode.DEC: 14,
            Opcode.ADD: 15,
            Opcode.SUB: 17,
            Opcode.MUL: 19,
            Opcode.DIV: 21,
            Opcode.LOAD: 23,
            Opcode.SAVE: 25,
            Opcode.IN: 30,
            Opcode.OUT: 31,
            Opcode.JMP: 35,
            Opcode.JZ: 38,
            Opcode.HALT: 42,
        }
        if opcode in addresses:
            return addresses[opcode]
        return 0

    def _dispatch_micro_instruction(self):
        micro_instruction = self._microprogram[self._micro_program_counter]
        logging.debug(micro_instruction)
        for signal in micro_instruction:
            match signal:
                case Signal.DS_PUSH:
                    self._data_path.push()
                case Signal.DS_POP:
                    self._data_path.pop()
                case Signal.LATCH_TOS:
                    self._data_path.latch_address_tos(micro_instruction)
                case Signal.LATCH_AR:
                    self._data_path.latch_address_register(micro_instruction)
                case Signal.LATCH_BR:
                    self._data_path.latch_buffer_register()
                case Signal.LATCH_PC:
                    self._latch_program_counter(micro_instruction)
                case Signal.LATCH_MPC:
                    self._latch_micro_program_counter(micro_instruction)
                case Signal.OUT:
                    self._data_path.out()
                case Signal.WRITE:
                    self._data_path.write()
                case Signal.HALT:
                    raise StopIteration
                case _:
                    pass

    def _latch_program_counter(self, micro_instruction: list[Signal]) -> None:
        if Signal.SEL_PC_NEXT in micro_instruction:
            self._program_counter += 1
        elif Signal.SEL_PC_JMP in micro_instruction:
            self._program_counter = self._data_path.tos
        elif Signal.SEL_PC_JZ in micro_instruction:
            if self._data_path.zero:
                self._program_counter = self._data_path.nos
            else:
                self._program_counter += 1

    def _latch_micro_program_counter(self, micro_instruction: list[Signal]) -> None:
        if Signal.SEL_MPC_ZERO in micro_instruction:
            self._micro_program_counter = 0
        elif Signal.SEL_MPC_OPCODE in micro_instruction:
            data = self._data_path.read()
            opcode = data["opcode"]
            if "arg" in data.keys():
                arg = data["arg"]
                logging.info("%s %s", opcode.upper(), arg)
            else:
                logging.info(opcode.upper())
            self._micro_program_counter = self._opcode_to_mpc(opcode)
        elif Signal.SEL_MPC_NEXT in micro_instruction:
            self._micro_program_counter += 1

    @property
    def program_counter(self):
        return self._program_counter

    def print_state(self):
        logging.debug("\t".join(["PC", "MPC", "AR", "BR", "TOS", "NOS"]))
        logging.debug(
            "\t".join(
                map(
                    str,
                    [
                        self.program_counter,
                        self._micro_program_counter,
                        self._data_path.address_register,
                        self._data_path.buffer_register,
                        self._data_path.tos,
                        " ".join(map(str, list(self._data_path.data_stack)[::-1])),
                    ],
                )
            )
        )
        logging.debug("")

    def run_simulation(self) -> Tuple[list, int]:
        while True:
            try:
                self.print_state()
                self._dispatch_micro_instruction()
                self._tick()
            except StopIteration:
                logging.error("HALT")
                break
            except EOFError:
                logging.error("Input buffer is empty!")
                break

        return self._data_path.output_buffer, self._current_tick
