import os
import sys

import openpyxl
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import flanker_design as fd  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
CONDITIONS = os.path.join(HERE, '..', 'conditions.xlsx')


@pytest.mark.parametrize('case, shown, answer, kind', [
    (1, ['left'] * 5, 'left', 'congruent'),
    (2, ['right'] * 5, 'right', 'congruent'),
    (3, ['left', 'left', 'right', 'left', 'left'], 'right', 'incongruent'),
    (4, ['right', 'right', 'left', 'right', 'right'], 'left', 'incongruent'),
])
def test_cases(case, shown, answer, kind):
    assert fd.directions(case) == shown
    assert fd.correct_answer(case) == answer
    assert fd.congruency(case) == kind


def test_answer_always_matches_middle():
    for case in fd.CASES:
        assert fd.correct_answer(case) == fd.directions(case)[2]


@pytest.mark.parametrize('case, response, expected', [
    (3, 'right', 1),
    (3, 'left', 0),   # pressed the way the flankers point
    (4, 'left', 1),
    (1, None, 0),     # no response
])
def test_score(case, response, expected):
    assert fd.score(case, response) == expected


def read_rows():
    ws = openpyxl.load_workbook(CONDITIONS, data_only=False).active
    rows = list(ws.iter_rows(values_only=True))
    header = rows[0]
    return [dict(zip(header, r)) for r in rows[1:] if any(v is not None for v in r)]


def test_conditions_file_has_plain_values():
    for row in read_rows():
        assert not str(row['corrAns']).startswith('='), 'corrAns should not be a formula'


def test_conditions_file_blocks():
    blocks = fd.split_blocks(read_rows())
    assert len(blocks['practice']) == 4
    assert len(blocks['fish']) == 25
    assert len(blocks['arrow']) == 25
    assert all(r['stimulus'] == 'fish' for r in blocks['practice'])


def test_split_blocks_rejects_wrong_answer():
    with pytest.raises(ValueError, match='corrAns'):
        fd.split_blocks([{'case': 3, 'practice': 0, 'stimulus': 'fish', 'corrAns': 'left'}])
