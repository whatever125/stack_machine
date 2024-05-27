import logging
from isa import Opcode
from uarch import Signal, MICROPROGRAM
from collections import deque


class DataPath:
    _control_unit: 'ControlUnit' = None

    _memory_size: int = None
    _memory: list = None

    _address_register: int = None
    _buffer_register: int = None

    _input_buffer: deque = None
    _output_buffer: list = None

    _data_stack: deque[int] = None
    _tos: int = None

    def __init__(self, memory_size: int, program: list, input_buffer: deque) -> None:
        self._memory_size = memory_size
        self._memory = [{"opcode": Opcode.NOP}] * memory_size
        for index, instruction in enumerate(program):
            self._memory[index] = program[index]

        self._address_register = 0
        self._buffer_register = 0

        self._input_buffer = input_buffer
        self._output_buffer = []

        self._data_stack = deque()
        self._tos = 0

    def latch_address_tos(self, micro_instruction: list[Signal]) -> None:
        if Signal.SEL_TOS_DS in micro_instruction:
            self._tos = self.nos
        elif Signal.SEL_TOS_MEMORY in micro_instruction:
            self._tos = self.read()["arg"]
        elif Signal.SEL_TOS_INPUT in micro_instruction:
            self._tos = self._input_buffer.popleft()
        elif Signal.SEL_TOS_ALU in micro_instruction:
            self._tos = 0  # TODO ALU
        elif Signal.SEL_TOS_BR in micro_instruction:
            self._tos = self._buffer_register

    def latch_address_register(self, micro_instruction: list[Signal]) -> None:
        if Signal.SEL_AR_TOS in micro_instruction:
            self._address_register = self._tos
        elif Signal.SEL_AR_PC in micro_instruction:
            self._address_register = self._control_unit.program_counter

    def latch_buffer_register(self) -> None:
        self._buffer_register = self.nos

    def push(self) -> None:
        self._data_stack.append(self._tos)

    def pop(self) -> None:
        self._data_stack.pop()

    def out(self) -> None:
        symbol = self.nos
        self._output_buffer.append(symbol)

    def read(self) -> dict:
        return self._memory[self._address_register]

    def write(self) -> None:
        self._memory[self._address_register] = {"opcode": "word", "arg": self.nos}

    @property
    def zero(self) -> bool:
        return self._tos == 0

    @property
    def output_buffer(self) -> list:
        return self._output_buffer

    @property
    def data_stack(self):
        return self._data_stack

    @property
    def tos(self) -> int:
        return self._tos

    @property
    def nos(self) -> int:
        if len(self._data_stack) == 0:
            return 0
        return self._data_stack[-1]

    @property
    def address_register(self):
        return self._address_register

    @property
    def buffer_register(self):
        return self._buffer_register


class ControlUnit:
    _data_path: DataPath = None
    _program_counter: int = None
    _micro_program_counter: int = None
    _current_tick: int = None
    _microprogram: list = None

    def __init__(self, data_path: DataPath) -> None:
        self._data_path = data_path
        self._program_counter = 0
        self._micro_program_counter = 0
        self._current_tick = 0
        self._microprogram = MICROPROGRAM

    def _tick(self) -> None:
        self._current_tick += 1

    def _opcode_to_mpc(self, opcode: Opcode) -> int:
        match opcode:
            case Opcode.NOP: return 2
            case Opcode.WORD: return 3
            case Opcode.PUSH: return 4
            case Opcode.POP: return 6
            case Opcode.SWAP: return 8
            case Opcode.OVER: return 12
            case Opcode.INC: return 19
            case Opcode.DEC: return 20
            case Opcode.ADD: return 21
            case Opcode.SUB: return 23
            case Opcode.MUL: return 25
            case Opcode.DIV: return 27
            case Opcode.LOAD: return 29
            case Opcode.SAVE: return 31
            case Opcode.IN: return 36
            case Opcode.OUT: return 37
            case Opcode.JMP: return 41
            case Opcode.JZ: return 44
            case Opcode.HALT: return 48
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

    def run_simulation(self, micro_instructions_limit: int) -> (str, int, int):
        micro_instructions_counter: int = 0
        while micro_instructions_counter < micro_instructions_limit:
            try:
                self.print_state()
                self.dispatch_micro_instruction()
                micro_instructions_counter += 1
            except StopIteration:
                logging.error("HALT")
                break
            except EOFError:
                logging.error("Input buffer is empty!")
                break

        return "".join(self._data_path.output_buffer), micro_instructions_counter, self.current_tick
