from isa import Opcode


class DataPath:
    _memory_size: int = None
    _memory: list[dict] = None
    _address_register: int = None

    _input_buffer: list = None
    _output_buffer: list = None

    _stack: list = None
    _tos: int = None

    def __init__(self, memory_size: int, program: list, input_buffer: list) -> None:
        self._memory_size = memory_size
        self._memory = [{"opcode": Opcode.NOP}] * memory_size
        for index, instruction in enumerate(program):
            self._memory[index] = program[index]
        self._address_register = 0

        self._input_buffer = input_buffer
        self._output_buffer = []

        self._stack = []
        self._tos = 0

    def signal_latch_data_addr(self, sel: Opcode) -> None:
        match sel:
            case Opcode.LEFT:
                self._data_address -= 1
            case Opcode.RIGHT:
                self._data_address += 1
            case _:
                raise Exception(f"internal error, incorrect selector: {sel}")

        if self._data_address < 0 or self._data_address >= self._data_memory_size:
            raise Exception(f"internal error, out of memory: {self._data_address}")

    def signal_latch_acc(self) -> None:
        self._accumulator = self._data_memory[self._data_address]

    def signal_wr(self, sel: Opcode) -> None:
        match sel:
            case Opcode.INC:
                self._data_memory[self._data_address] = self._accumulator + 1
            case Opcode.DEC:
                self._data_memory[self._data_address] = self._accumulator - 1
            case Opcode.INPUT:
                if len(self._input_buffer) == 0:
                    raise EOFError("internal error: input buffer is empty")
                symbol = self._input_buffer.pop(0)
                symbol_code = ord(symbol)
                if -128 <= symbol_code <= 127:
                    self._data_memory[self._data_address] = symbol_code
                else:
                    raise Exception(f"input token is out of bound: {symbol_code}")
            case _:
                raise Exception(f"internal error, incorrect selector: {sel}")

    def signal_output(self) -> None:
        symbol = chr(self._accumulator)
        self._output_buffer.append(symbol)

    def read(self) -> dict:
        return self._memory[self._address_register]

    def zero(self) -> bool:
        return self._tos == 0

    @property
    def output_buffer(self) -> list:
        return self._output_buffer

    @property
    def tos(self) -> int:
        return self._tos
