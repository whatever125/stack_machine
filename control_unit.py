import logging
from collections import deque

from isa import Opcode
from uarch import Signal, MICROPROGRAM
import data_path as dp


class ControlUnit:
    def __init__(self, data_path: dp.DataPath) -> None:
        self._data_path: dp.DataPath = data_path
        self._program_counter: int = self._data_path.start_address
        self._micro_program_counter: int = 0
        self._current_tick: int = 0
        self._microprogram = MICROPROGRAM
        self._return_stack: deque[int] = deque()

    def _tick(self) -> None:
        self._current_tick += 1

    def _opcode_to_mpc(self, opcode: Opcode) -> int:
        addresses = {
            Opcode.NOP: 2,
            Opcode.PUSH: 3,
            Opcode.POP: 6,
            Opcode.SWAP: 8,
            Opcode.DUP: 12,
            Opcode.OVER: 13,
            Opcode.INC: 20,
            Opcode.DEC: 21,
            Opcode.ADD: 22,
            Opcode.SUB: 24,
            Opcode.MUL: 26,
            Opcode.DIV: 28,
            Opcode.MOD: 30,
            Opcode.LOAD: 32,
            Opcode.SAVE: 34,
            Opcode.IN: 39,
            Opcode.OUT: 40,
            Opcode.JMP: 44,
            Opcode.JZ: 47,
            Opcode.CALL: 51,
            Opcode.RET: 55,
            Opcode.HALT: 57,
        }
        if opcode in addresses:
            return addresses[opcode]
        return 0

    def _dispatch_micro_instruction(self):
        micro_instruction = self._microprogram[self._micro_program_counter]
        for signal in micro_instruction:
            match signal:
                case Signal.DS_PUSH:
                    self._data_path.ds_push()
                case Signal.DS_POP:
                    self._data_path.ds_pop()
                case Signal.RS_PUSH:
                    self._rs_push()
                case Signal.RS_POP:
                    self._rs_pop()
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

    def _rs_push(self) -> None:
        self._return_stack.append(self._program_counter + 1)

    def _rs_pop(self) -> None:
        self._return_stack.pop()

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
        elif Signal.SEL_PC_RS in micro_instruction:
            if len(self._return_stack) == 0:
                raise Exception("Empty return stack")
            self._program_counter = self._return_stack[-1]

    def _latch_micro_program_counter(self, micro_instruction: list[Signal]) -> None:
        if Signal.SEL_MPC_ZERO in micro_instruction:
            self._micro_program_counter = 0
        elif Signal.SEL_MPC_OPCODE in micro_instruction:
            data = self._data_path.read()
            opcode = Opcode(data)
            self._micro_program_counter = self._opcode_to_mpc(opcode)
        elif Signal.SEL_MPC_NEXT in micro_instruction:
            self._micro_program_counter += 1

    @property
    def program_counter(self):
        return self._program_counter

    def _print_state(self):
        logging.debug(self)

    def __repr__(self) -> str:
        tick = f"Tick: {self._current_tick}"

        micro_instruction = self._microprogram[self._micro_program_counter]
        micro_instruction_repr = f"MicroInstruction: {", ".join(map(lambda signal: signal.name.upper(), micro_instruction))}"

        registers = "\t".join(["PC", "MPC", "AR", "BR", "TOS"])
        values = "\t".join(map(str, [
            self.program_counter,
            self._micro_program_counter,
            self._data_path.address_register,
            self._data_path.buffer_register,
            self._data_path.tos
        ]))

        ds = f"DS: [{', '.join(map(str, self._data_path.data_stack))}]"
        rs = f"RS: [{', '.join(map(str, self._return_stack))}]"

        data = [tick, micro_instruction_repr, registers, values, ds, rs]

        if self._micro_program_counter == 1:
            opcode = self._data_path.memory[self._program_counter]
            if opcode in [Opcode.PUSH]:
                arg = self._data_path.memory[self._program_counter + 1]
                opcode_repr = f"Instruction: {opcode.name.upper()} {arg}"
            else:
                opcode_repr = f"Instruction: {opcode.name.upper()}"
            data.insert(2, opcode_repr)

        return "\n" + "\n".join(data) + "\n"

    def run_simulation(self, tick_limit: int) -> int:
        try:
            while True:
                self._dispatch_micro_instruction()
                self._print_state()
                self._tick()
                if self._current_tick > tick_limit:
                    raise Exception("Exceeded tick limit")
        except StopIteration:
            pass

        return self._current_tick
