from collections import deque

import control_unit as cu
from uarch import Signal
from isa import Opcode


class DataPath:
    def __init__(self, memory_size: int, program: list, io_controller: 'IOController') -> None:
        self.control_unit: cu.ControlUnit
        self._alu: ALU = ALU(self)

        self._memory_size: int = memory_size
        self._memory: list = [Opcode.NOP] * memory_size
        for index, _ in enumerate(program):
            self._memory[index] = program[index]

        self._address_register: int = 0
        self._buffer_register: int = 0

        self._io_controller: IOController = io_controller

        self._data_stack: deque[int] = deque()
        self._tos: int = 0

    def latch_address_tos(self, micro_instruction: list[Signal]) -> None:
        if Signal.SEL_TOS_DS in micro_instruction:
            self._tos = self.nos
        elif Signal.SEL_TOS_MEMORY in micro_instruction:
            self._tos = self.read()
        elif Signal.SEL_TOS_INPUT in micro_instruction:
            self._tos = self._io_controller.read(self._tos)
        elif Signal.SEL_TOS_ALU in micro_instruction:
            self._tos = self._alu.result(micro_instruction)
        elif Signal.SEL_TOS_BR in micro_instruction:
            self._tos = self._buffer_register

    def latch_address_register(self, micro_instruction: list[Signal]) -> None:
        if Signal.SEL_AR_TOS in micro_instruction:
            self._address_register = self._tos
        elif Signal.SEL_AR_PC in micro_instruction:
            self._address_register = self.control_unit.program_counter

    def latch_buffer_register(self) -> None:
        self._buffer_register = self.nos

    def push(self) -> None:
        self._data_stack.append(self._tos)

    def pop(self) -> None:
        self._data_stack.pop()

    def out(self) -> None:
        symbol = self.nos
        self._io_controller.write(self._tos, symbol)

    def read(self):
        return self._memory[self._address_register]

    def write(self) -> None:
        self._memory[self._address_register] = self.nos

    @property
    def zero(self) -> bool:
        return self._tos == 0

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

    @property
    def start_address(self):
        return self._memory[0]


class ALU:
    def __init__(self, dp: DataPath):
        self._data_path: DataPath = dp

    def result(self, micro_instruction: list[Signal]) -> int:
        left = self._data_path.tos
        if Signal.ALU_RIGHT_OP_ZERO in micro_instruction:
            right = 0
        elif Signal.ALU_RIGHT_OP_NOS in micro_instruction:
            right = self._data_path.nos
        else:
            right = 0

        if Signal.ALU_SUM in micro_instruction:
            result = left + right
        elif Signal.ALU_SUB in micro_instruction:
            result = left - right
        elif Signal.ALU_MUL in micro_instruction:
            result = left * right
        elif Signal.ALU_DIV in micro_instruction:
            result = int(left / right)
        else:
            result = 0

        if Signal.ALU_INC in micro_instruction:
            result += 1
        elif Signal.ALU_DEC in micro_instruction:
            result -= 1

        return result


class IOUnit:
    def __init__(self, input_buffer: deque[int]):
        self._input_buffer: deque[int] = input_buffer
        self._output_buffer: deque[int] = deque()

    def read(self) -> int:
        return self._input_buffer.popleft()

    def write(self, value: int) -> None:
        return self._output_buffer.append(value)

    def get_output(self) -> deque[int]:
        return self._output_buffer


class IOController:
    def __init__(self) -> None:
        self._connected_units: dict[int, IOUnit] = {}

    def connect(self, port: int, unit: IOUnit) -> None:
        self._connected_units[port] = unit

    def disconnect(self, port: int) -> None:
        self._connected_units.pop(port)

    def read(self, port: int) -> int:
        if not self._connected_units[port]:
            raise Exception(f"No device connected to port {port}")
        return self._connected_units[port].read()

    def write(self, port: int, value: int):
        if not self._connected_units[port]:
            raise Exception(f"No device connected to port {port}")
        self._connected_units[port].write(value)
