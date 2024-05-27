import logging
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
        match opcode:
            case Opcode.NOP: return 2
            case Opcode.WORD: return 3
            case Opcode.PUSH: return 4
            case Opcode.POP: return 6
            case Opcode.SWAP: return 8
            case Opcode.DUP: return 12
            case Opcode.INC: return 13
            case Opcode.DEC: return 14
            case Opcode.ADD: return 15
            case Opcode.SUB: return 17
            case Opcode.MUL: return 19
            case Opcode.DIV: return 21
            case Opcode.LOAD: return 23
            case Opcode.SAVE: return 25
            case Opcode.IN: return 30
            case Opcode.OUT: return 31
            case Opcode.JMP: return 35
            case Opcode.JZ: return 38
            case Opcode.HALT: return 42
            case _: return 0

    def dispatch_micro_instruction(self):
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
                logging.info(f"{opcode.upper()} {arg}")
            else:
                logging.info(opcode.upper())
            self._micro_program_counter = self._opcode_to_mpc(opcode)
        elif Signal.SEL_MPC_NEXT in micro_instruction:
            self._micro_program_counter += 1

    @property
    def program_counter(self):
        return self._program_counter

    @property
    def current_tick(self):
        return self._current_tick

    def print_state(self):
        logging.debug("\t".join(["PC", "MPC", "AR", "BR", "TOS", "NOS"]))
        logging.debug("\t".join(map(str, [self.program_counter, self._micro_program_counter,
                                          self._data_path.address_register, self._data_path.buffer_register,
                                          self._data_path.tos, " ".join(map(str, list(self._data_path.data_stack)[::-1]))])))
        logging.debug("")

    def run_simulation(self) -> (str, int, int):
        while True:
            try:
                self.print_state()
                self.dispatch_micro_instruction()
                self._tick()
            except StopIteration:
                logging.error("HALT")
                break
            except EOFError:
                logging.error("Input buffer is empty!")
                break

        return self._data_path.output_buffer, self.current_tick
