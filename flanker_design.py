"""
Trial design for the Fish Flanker Task.

This module has no PsychoPy imports, so the rules for what each trial shows
and how a response is scored can be tested on their own.

Cases (column `case` in conditions.xlsx):
    1  all five point left             congruent    correct answer: left
    2  all five point right            congruent    correct answer: right
    3  middle right, flankers left     incongruent  correct answer: right
    4  middle left, flankers right     incongruent  correct answer: left
"""

# For each case: (direction of the four flankers, direction of the middle one)
CASES = {
    1: ('left', 'left'),
    2: ('right', 'right'),
    3: ('left', 'right'),
    4: ('right', 'left'),
}

RESPONSE_KEYS = ('left', 'right')


def directions(case):
    """Return the five directions, left to right on screen, for a case."""
    flanker, middle = CASES[int(case)]
    return [flanker, flanker, middle, flanker, flanker]


def correct_answer(case):
    """The key that matches the middle stimulus."""
    return CASES[int(case)][1]


def congruency(case):
    flanker, middle = CASES[int(case)]
    return 'congruent' if flanker == middle else 'incongruent'


def score(case, response):
    """1 if the response matches the middle stimulus, 0 otherwise (including no response)."""
    return 1 if response == correct_answer(case) else 0


def split_blocks(rows):
    """
    Split the rows of conditions.xlsx into the three blocks, keeping file order.

    Returns a dict with keys 'practice', 'fish' and 'arrow'. Each row is checked:
    its stated corrAns (when present) must agree with the case.
    """
    blocks = {'practice': [], 'fish': [], 'arrow': []}
    for i, row in enumerate(rows, start=2):  # row 1 of the sheet is the header
        case = int(row['case'])
        if case not in CASES:
            raise ValueError(f'conditions.xlsx row {i}: unknown case {case!r}')
        stated = row.get('corrAns')
        if stated not in (None, '') and stated != correct_answer(case):
            raise ValueError(
                f'conditions.xlsx row {i}: corrAns {stated!r} does not match case {case}')
        stimulus = str(row['stimulus']).strip().lower()
        if stimulus not in ('fish', 'arrow'):
            raise ValueError(f'conditions.xlsx row {i}: unknown stimulus {stimulus!r}')
        if int(row['practice']) == 1:
            blocks['practice'].append(row)
        else:
            blocks[stimulus].append(row)
    return blocks
