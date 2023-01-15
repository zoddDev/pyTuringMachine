from tm import *

# TM Example

states = {'q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8'}
alphabet = {'*', '|'}
its = {
    IT('q0', '*', LEFT, 'q1'),
    IT('q0', '|', LEFT, 'q0'),

    IT('q1', '*', LEFT, 'q2'),
    IT('q1', '|', LEFT, 'q1'),

    IT('q2', '*', LEFT, 'q2'),
    IT('q2', '|', '*', 'q3'),

    IT('q3', '*', LEFT, 'q4'),
    IT('q3', '|', '|', 'q3'),

    IT('q4', '*', HALT, 'q4'),
    IT('q4', '|', RIGHT, 'q5'),

    IT('q5', '*', RIGHT, 'q5'),
    IT('q5', '|', '*', 'q6'),

    IT('q6', '*', RIGHT, 'q7'),
    IT('q6', '|', '|', 'q6'),

    IT('q7', '*', '|', 'q8'),
    IT('q7', '|', LEFT, 'q2'),

    IT('q8', '*', '*', 'q8'),
    IT('q8', '|', HALT, 'q8'),
}

initial_state = 'q0'

initial_configuration = Configuration(
    'q0',
    Tape(
        list('*||*|*'),
        0
    ),
    5
)

its_tuple = get_transitions_and_instructions(its)
transitions = its_tuple[0]
instructions = its_tuple[1]

tm = TM(
    states,
    initial_state,
    alphabet,
    instructions,
    transitions,
    initial_configuration
)

# Execute example
result = tm.transitate_until_halt()
print_full_transitions(tm.get_initial_configuration(), result)
