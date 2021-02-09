"""7th day of advent of code 2020."""


import enum
import itertools
import pathlib
import typing


HERE = pathlib.Path(__file__).parent
INPUT_FILE_NAME = "input.txt"


class Error(enum.Enum):
    EOC = enum.auto()
    INVALID_INSTRUCTION = enum.auto()
    INFINITE_LOOP = enum.auto()


class Instruction(typing.NamedTuple):
    operation: str
    argument: int


class Effects(typing.NamedTuple):
    ip_delta: int
    accumulator_delta: int


class StackTrace(typing.NamedTuple):
    error: Error
    ip_log: typing.Sequence[int]
    accumulator: int
    last_instruction: typing.Union[Instruction, None]


SourceCode = typing.Sequence[Instruction]


def get_code() -> SourceCode:
    ret = []
    with open(HERE / INPUT_FILE_NAME) as f:
        for line in f:
            operation, argument = line.strip().split(" ", 1)
            argument = int(argument)
            ret.append(Instruction(operation, argument))
    return tuple(ret)


def _parse(instruction: Instruction) -> Effects:
    return {
        "acc": Effects(+1, instruction.argument),
        "jmp": Effects(instruction.argument, 0),
        "nop": Effects(+1, 0)
    }[instruction.operation]


def anti_infinite_loop_emulator(source_code: SourceCode) -> StackTrace:
    accumulator = 0
    ip_log = []
    ip = 0
    while True:
        if ip in ip_log:
            ip_log.append(ip)
            return StackTrace(
                error=Error.INFINITE_LOOP,
                ip_log=ip_log,
                accumulator=accumulator,
                last_instruction=source_code[ip])
        ip_log.append(ip)
        try:
            instruction = source_code[ip]
        except IndexError:
            return StackTrace(
                error=Error.EOC,
                ip_log=ip_log,
                accumulator=accumulator,
                last_instruction=None)
        else:
            try:
                effects = _parse(instruction)
            except KeyError:
                return StackTrace(
                    error=Error.INVALID_INSTRUCTION,
                    ip_log=ip_log,
                    accumulator=accumulator,
                    last_instruction=instruction)
            accumulator += effects.accumulator_delta
            ip += effects.ip_delta


def solve1() -> int:
    return anti_infinite_loop_emulator(get_code()).accumulator


def solve2() -> int:
    source_code = get_code()
    stack_trace = anti_infinite_loop_emulator(source_code)
    if stack_trace.error != Error.INFINITE_LOOP:
        return stack_trace.accumulator
    else:
        for ip in reversed(stack_trace.ip_log[:-1]):
            instruction = source_code[ip]
            try:
                new_operation = {
                    "jmp": "nop",
                    "nop": "jmp"
                }[instruction.operation]
            except KeyError:
                continue
            else:
                corrected_code = tuple(
                    itertools.chain(
                        source_code[:ip],
                        [Instruction(new_operation, instruction.argument)],
                        source_code[ip + 1:]))
                stack_trace = anti_infinite_loop_emulator(corrected_code)
                if stack_trace.error == Error.EOC:
                    return stack_trace.accumulator
        else:
            raise RuntimeError("Should not get here")


def main():
    print(solve1())
    print(solve2())


if __name__ == "__main__":
    main()
