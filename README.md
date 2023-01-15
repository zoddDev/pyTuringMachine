# Turing Machine simulator :snake:

## You can find an already built example: ![main.py](https://github.com/zoddDev/pyTuringMachine/blob/main/main.py)

```python
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
```


## Execution trace
```python
Configuration(q0, Tape(* | | * | *), 5) |-
Configuration(q1, Tape(* | | * | *), 4) |-
Configuration(q1, Tape(* | | * | *), 3) |-
Configuration(q2, Tape(* | | * | *), 2) |-
Configuration(q3, Tape(* | * * | *), 2) |-
Configuration(q4, Tape(* | * * | *), 1) |-
Configuration(q5, Tape(* | * * | *), 2) |-
Configuration(q5, Tape(* | * * | *), 3) |-
Configuration(q5, Tape(* | * * | *), 4) |-
Configuration(q6, Tape(* | * * * *), 4) |-
Configuration(q7, Tape(* | * * * *), 5) |-
Configuration(q8, Tape(* | * * * |), 5) |-
Configuration(q8, Tape(* | * * * |), 5) |-
```

## TODO 📝

- Add interactive command line mode
- Accept JSON as an input
- Add support for any number of tapes
