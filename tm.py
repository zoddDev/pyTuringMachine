from dis import Instruction
from pickle import EMPTY_DICT
from typing import *
import copy

LEFT: str = "LEFT"
RIGHT: str = "RIGHT"
HALT: str = "HALT"
EMPTY_SYMBOL: str = "_"


class Tape:
    def __init__(self, tape_expr: List[str], from_index: int) -> None:
        self.__tape_NAT = []
        self.__tape_NEG = []

        for i in range(from_index, from_index + len(tape_expr)):
            if i < 0:
                self.__tape_NEG.append(tape_expr[i])
            else:
                self.__tape_NAT.append(tape_expr[i])

    def set(self, symbol: str, index: int):
        if index < 0:
            index = -index
            self.__tape_NEG[index] = symbol
        else:
            self.__tape_NAT[index] = symbol

    def get(self, index: int) -> str:
        if index < 0:
            index = -index
            return self.__tape_NEG[index]
        else:
            return self.__tape_NAT[index]

    def __str__(self, cursor: int) -> str:
        # For char colouring (add \033[... code)
        char = copy.deepcopy(self.get(cursor))
        self.set("\033[0;31m" + copy.deepcopy(char) + "\033[0;m", cursor)

        neg = self.__tape_NEG[::-1]
        negstr = ' '.join(map(str, neg))
        nat = self.__tape_NAT
        natstr = ' '.join(map(str, nat))

        str_result = f"Tape({negstr + (' ' if len(negstr) > 0 else '') + natstr})"

        # Return normal char (remove \033[... code)
        self.set(char, cursor)

        return str_result


class Configuration:
    def __init__(self, state: str, tape: Tape, cursor: int) -> None:
        self.__state = state
        self.__tape = tape
        self.__cursor = cursor

    def get_state(self) -> str:
        return self.__state

    def get_tape(self) -> Tape:
        return self.__tape

    def get_cursor(self) -> int:
        return self.__cursor

    def set_cursor(self, cursor: int) -> None:
        self.__cursor = cursor

    def set_tape(self, tape: Tape) -> None:
        self.__tape = tape

    def set_state(self, state: str) -> None:
        self.__state = state

    def __repr__(self) -> str:
        return f"Configuration({self.__state}, {self.__tape.__str__(self.__cursor)}, {self.__cursor})"


class Instruction:
    def __init__(self, state: str, symbol: str, action: str) -> None:
        self.__state = state
        self.__symbol = symbol
        self.__action = action

    def get_state(self) -> str:
        return self.__state

    def get_symbol(self) -> str:
        return self.__symbol

    def get_action(self) -> str:
        return self.__action

    def __repr__(self) -> str:
        return f"Instruction({self.__state}, {self.__symbol}, {self.__action})"

    def apply(self, configuration: Configuration) -> None:
        current_cursor = configuration.get_cursor()
        current_symbol = configuration.get_tape().get(current_cursor)
        current_state = configuration.get_state()

        assert(current_symbol == self.__symbol and current_state == self.__state)

        next_action = self.get_action()
        if next_action is LEFT:
            configuration.set_cursor(current_cursor - 1)
        elif next_action is RIGHT:
            configuration.set_cursor(current_cursor + 1)
        elif next_action is HALT:
            # Do nothing, just halt
            pass
        else:
            # Write symbol in tape
            configuration.get_tape().set(next_action, current_cursor)


class Transition:
    def __init__(self, state: str, symbol: str, next_state: str) -> None:
        self.__state = state
        self.__symbol = symbol
        self.__next_state = next_state

    def get_state(self) -> str:
        return self.__state

    def get_symbol(self) -> str:
        return self.__symbol

    def get_next_state(self) -> str:
        return self.__next_state

    def __repr__(self) -> str:
        return f"Transition({self.__state}, {self.__symbol}, {self.__next_state})"

    def apply(self, configuration: Configuration) -> None:
        current_state = configuration.get_state()
        current_symbol = configuration.get_tape().get(configuration.get_cursor())
        assert(current_symbol == self.__symbol and current_state == self.__state)

        configuration.set_state(self.__next_state)


class IT:
    # Represents an object that indicates both Transition and Instruction
    def __init__(self, state: str, symbol: str, action: str, next_state: str) -> None:
        self.__state = state
        self.__symbol = symbol
        self.__action = action
        self.__next_state = next_state

    def get_transition(self) -> Transition:
        return Transition(self.__state, self.__symbol, self.__next_state)

    def get_instruction(self) -> Instruction:
        return Instruction(self.__state, self.__symbol, self.__action)


def get_transitions_and_instructions(its: Set[IT]) -> Tuple[Set[Transition], Set[Instruction]]:
    transitions = set()
    instructions = set()

    for it in its:
        transitions.add(it.get_transition())
        instructions.add(it.get_instruction())

    return (transitions, instructions)


class TM:
    def __init__(self, states: Set[str], initial_state: str, alphabet: Set[str], instructions: Set[Instruction], transitions: Set[Transition], initial_configuration: Configuration) -> None:
        assert(len(states) > 0)
        assert(len(alphabet) > 0)
        assert(len(transitions) == len(instructions))
        assert(initial_state in states)

        for a in alphabet:
            assert(len(a) == 1)

        for i in instructions:
            assert(i.get_state() in states)
            assert(i.get_symbol() in alphabet)
            if i.get_action() not in [LEFT, RIGHT, HALT]:
                assert(i.get_action() in alphabet)

        for t in transitions:
            assert(t.get_state() in states)
            assert(t.get_symbol() in alphabet)
            assert(t.get_next_state() in states)

        assert initial_configuration.get_state() is initial_state

        self.__states = states
        self.__initial_state = initial_state
        self.__alphabet = alphabet
        self.__instructions = instructions
        self.__transitions = transitions
        self.__initial_configuration = copy.deepcopy(initial_configuration)
        self.__configuration = initial_configuration

    def get_initial_configuration(self) -> Configuration:
        return self.__initial_configuration

    def set_initial_configuration(self, configuration: Configuration) -> None:
        assert configuration.get_state() is self.__initial_state
        self.__initial_configuration = copy.deepcopy(configuration)
        self.__configuration = configuration

    def transitate(self) -> Tuple[Transition, Instruction, Configuration]:
        current_cursor = self.__configuration.get_cursor()
        current_symbol = self.__configuration.get_tape().get(current_cursor)
        current_state = self.__configuration.get_state()

        transition = None
        for t in self.__transitions:
            if t.get_state() == current_state and t.get_symbol() == current_symbol:
                transition = t
                break
        assert(transition)

        instruction = None
        for i in self.__instructions:
            if i.get_state() is current_state and i.get_symbol() is current_symbol:
                instruction = i
                break
        assert(instruction)

        # Apply transition and instruction to the current configuration
        cpy_t_configuration = copy.deepcopy(self.__configuration)
        cpy_i_configuration = copy.deepcopy(self.__configuration)
        transition.apply(cpy_t_configuration)
        instruction.apply(cpy_i_configuration)

        self.__configuration.set_state(cpy_t_configuration.get_state())
        self.__configuration.set_cursor(cpy_i_configuration.get_cursor())
        self.__configuration.set_tape(cpy_i_configuration.get_tape())

        return (copy.deepcopy(transition), copy.deepcopy(instruction), copy.deepcopy(self.__configuration))

    def transitate_until_halt(self) -> List[Tuple[Transition, Instruction, Configuration]]:
        configurations = []

        stop = False
        while(not stop):
            last_transition = self.transitate()
            configurations.append(last_transition)

            if last_transition[1].get_action() == HALT:
                stop = True

        return configurations

    def reset(self) -> None:
        self.__configuration = copy.deepcopy(self.__initial_configuration)


def print_transition(tp: Tuple[Transition, Instruction, Configuration]) -> None:
    print(f"{tp[2]} |-")


def print_full_transitions(initial_config: Configuration, tp: List[Tuple[Transition, Instruction, Configuration]]) -> None:
    configurations = [initial_config]
    mapped_transitions = list(map(lambda t: t[2], tp))
    for c in mapped_transitions:
        configurations.append(c)

    for c in configurations:
        print(f"{c} |-")
