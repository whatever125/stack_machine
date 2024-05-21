from data_path import DataPath
from isa import Opcode
from uarch import Signal


class ControlUnit:
    _program_counter: int = None
    _data_path: DataPath = None
    _current_tick: int = None

    _micro_program_counter: int = None
    _microprogram: list = None

    def __init__(self, data_path: DataPath) -> None:
        self._program_counter = 0
        self._data_path = data_path
        self._current_tick = 0

        self._micro_program_counter = 0
        self._microprogram = [
            # 0 - INSTRUCTION FETCH
            [Signal.LATCH_AR, Signal.SEL_AR_PC],
            # 1
            [Signal.LATCH_MPC, Signal.SEL_MPC_OPCODE],

            # 2 - NOP
            [Signal.LATCH_PC, Signal.SEL_PC_NEXT,
             Signal.LATCH_MPC, Signal.SEL_MPC_ZERO],

            # 3 - WORD
            [Signal.LATCH_PC, Signal.SEL_PC_NEXT,
             Signal.LATCH_MPC, Signal.SEL_MPC_ZERO],

            # 4 - PUSH
            [Signal.DS_PUSH,
             Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
            # 5
            [Signal.LATCH_TOS, Signal.SEL_TOS_MEMORY,
             Signal.LATCH_PC, Signal.SEL_PC_NEXT,
             Signal.LATCH_MPC, Signal.SEL_MPC_ZERO],

            # 6 - INC
            [Signal.ALU_SUM, Signal.ALU_RIGHT_OP_ZERO, Signal.ALU_INC,
             Signal.LATCH_TOS, Signal.SEL_TOS_ALU,
             Signal.LATCH_PC, Signal.SEL_PC_NEXT,
             Signal.LATCH_MPC, Signal.SEL_MPC_ZERO],

            # 7 - DEC
            [Signal.ALU_SUM, Signal.ALU_RIGHT_OP_ZERO, Signal.ALU_DEC,
             Signal.LATCH_TOS, Signal.SEL_TOS_ALU,
             Signal.LATCH_PC, Signal.SEL_PC_NEXT,
             Signal.LATCH_MPC, Signal.SEL_MPC_ZERO],

            # 8 - DROP
            [Signal.LATCH_TOS, Signal.SEL_TOS_DS,
             Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
            # 9
            [Signal.DS_POP,
             Signal.LATCH_PC, Signal.SEL_PC_NEXT,
             Signal.LATCH_MPC, Signal.SEL_MPC_ZERO],

            # 10 - SWAP TODO
            [Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
            # 10
            [Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
            # 11
            [Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
            # 12
            [Signal.LATCH_PC, Signal.SEL_PC_NEXT,
             Signal.LATCH_MPC, Signal.SEL_MPC_ZERO],

            # 13 - OVER TODO
            [Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
            # 14
            [Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
            # 15
            [Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
            # 16
            [Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
            # 17
            [Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
            # 18
            [Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
            # 19
            [Signal.LATCH_PC, Signal.SEL_PC_NEXT,
             Signal.LATCH_MPC, Signal.SEL_MPC_ZERO],

            # 20 - ADD
            [Signal.ALU_SUM, Signal.ALU_RIGHT_OP_NOS,
             Signal.LATCH_TOS, Signal.SEL_TOS_ALU,
             Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
            # 21
            [Signal.DS_POP,
             Signal.LATCH_PC, Signal.SEL_PC_NEXT,
             Signal.LATCH_MPC, Signal.SEL_MPC_ZERO],

            # 22 - SUB
            [Signal.ALU_SUB, Signal.ALU_RIGHT_OP_NOS,
             Signal.LATCH_TOS, Signal.SEL_TOS_ALU,
             Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
            # 23
            [Signal.DS_POP,
             Signal.LATCH_PC, Signal.SEL_PC_NEXT,
             Signal.LATCH_MPC, Signal.SEL_MPC_ZERO],

            # 24 - MUL
            [Signal.ALU_MUL, Signal.ALU_RIGHT_OP_NOS,
             Signal.LATCH_TOS, Signal.SEL_TOS_ALU,
             Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
            # 25
            [Signal.DS_POP,
             Signal.LATCH_PC, Signal.SEL_PC_NEXT,
             Signal.LATCH_MPC, Signal.SEL_MPC_ZERO],

            # 26 - DIV
            [Signal.ALU_DIV, Signal.ALU_RIGHT_OP_NOS,
             Signal.LATCH_TOS, Signal.SEL_TOS_ALU,
             Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
            # 27
            [Signal.DS_POP,
             Signal.LATCH_PC, Signal.SEL_PC_NEXT,
             Signal.LATCH_MPC, Signal.SEL_MPC_ZERO],

            # 28 - LOAD
            [Signal.LATCH_AR, Signal.SEL_AR_TOS,
             Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
            # 29
            [Signal.LATCH_TOS, Signal.SEL_TOS_MEMORY,
             Signal.LATCH_PC, Signal.SEL_PC_NEXT,
             Signal.LATCH_MPC, Signal.SEL_MPC_ZERO],

            # 30 - SAVE
            [Signal.LATCH_AR, Signal.SEL_AR_TOS,
             Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
            # 31
            [Signal.WRITE,
             Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
            # 32
            [Signal.DS_POP,
             Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
            # 33
            [Signal.LATCH_TOS, Signal.SEL_TOS_DS,
             Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
            # 34
            [Signal.DS_POP,
             Signal.LATCH_PC, Signal.SEL_PC_NEXT,
             Signal.LATCH_MPC, Signal.SEL_MPC_ZERO],

            # 35 - IN
            [Signal.LATCH_TOS, Signal.SEL_TOS_INPUT,
             Signal.LATCH_PC, Signal.SEL_PC_NEXT,
             Signal.LATCH_MPC, Signal.SEL_MPC_ZERO],

            # 36 - OUT
            [Signal.OUT,
             Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
            # 37
            [Signal.DS_POP,
             Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
            # 38
            [Signal.LATCH_TOS, Signal.SEL_TOS_DS,
             Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
            # 39
            [Signal.DS_POP,
             Signal.LATCH_PC, Signal.SEL_PC_NEXT,
             Signal.LATCH_MPC, Signal.SEL_MPC_ZERO],

            # 40 - JMP
            [Signal.LATCH_PC, Signal.SEL_PC_JMP,
             Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
            # 41
            [Signal.LATCH_TOS, Signal.SEL_TOS_DS,
             Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
            # 42
            [Signal.DS_POP,
             Signal.LATCH_PC, Signal.SEL_PC_NEXT,
             Signal.LATCH_MPC, Signal.SEL_MPC_ZERO],

            # 43 - JZ
            [Signal.LATCH_PC, Signal.SEL_PC_JZ,
             Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
            # 44
            [Signal.DS_POP,
             Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
            # 45
            [Signal.LATCH_TOS, Signal.SEL_TOS_DS,
             Signal.LATCH_MPC, Signal.SEL_MPC_NEXT],
            # 46
            [Signal.DS_POP,
             Signal.LATCH_PC, Signal.SEL_PC_NEXT,
             Signal.LATCH_MPC, Signal.SEL_MPC_ZERO],

            # 47 - HALT
            [Signal.HALT]
        ]

    def _tick(self) -> None:
        self._current_tick += 1

    def _opcode_to_mpc(self, opcode: Opcode) -> int:
        match opcode:
            case Opcode.NOP: return 2
            case Opcode.WORD: return 3
            case Opcode.PUSH: return 4
            case Opcode.INC: return 6
            case Opcode.DEC: return 7
            case Opcode.DROP: return 8
            case Opcode.SWAP: return 10
            case Opcode.OVER: return 14
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

        for signal in micro_instruction:
            match signal:
                case Signal.DS_PUSH:
                    pass

    def _signal_latch_program_counter(self, sel_next: bool) -> None:
        if sel_next:
            self._program_counter += 1
        else:
            instr = self._program_memory[self._program_counter]
            if "arg" in instr:
                address = instr["arg"]
                self._program_counter = address
            else:
                raise Exception(f"internal error: no arg in {instr}")

    def decode_and_execute_instruction(self) -> None:
        if self._program_counter >= self._program_memory_size:
            raise Exception("internal error: out of program memory")

        instr = self._program_memory[self._program_counter]
        opcode = instr["opcode"]

        match opcode:
            case Opcode.RIGHT | Opcode.LEFT:
                self._data_path.signal_latch_data_addr(opcode)
                self._signal_latch_program_counter(sel_next=True)
                self._tick()

            case Opcode.INC | Opcode.DEC | Opcode.INPUT:
                self._data_path.signal_latch_acc()
                self._tick()

                self._data_path.signal_wr(opcode)
                self._signal_latch_program_counter(sel_next=True)
                self._tick()

            case Opcode.PRINT:
                self._data_path.signal_latch_acc()
                self._tick()

                self._data_path.signal_output()
                self._signal_latch_program_counter(sel_next=True)
                self._tick()

            case Opcode.HALT:
                raise StopIteration()

            case Opcode.JMP:
                self._signal_latch_program_counter(sel_next=False)
                self._tick()

            case Opcode.JZ:
                self._data_path.signal_latch_acc()
                self._tick()

                if self._data_path.zero():
                    self._signal_latch_program_counter(sel_next=False)
                else:
                    self._signal_latch_program_counter(sel_next=True)
                self._tick()

    @property
    def current_tick(self):
        return self._current_tick

    def run_simulation(self, micro_instructions_limit: int) -> (str, int, int):
        micro_instructions_counter: int = 0

        while micro_instructions_counter < micro_instructions_limit:
            try:
                self.dispatch_micro_instruction()
                micro_instructions_counter += 1
            except StopIteration:
                print("HALT")
                break
            except EOFError:
                print("Input buffer is empty!")
                break

        return "".join(self._data_path.output_buffer), micro_instructions_counter, self.current_tick
