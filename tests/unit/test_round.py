import pytest

import matchscheduler.round as uut
from matchscheduler.match import create_match


@pytest.mark.parametrize(
    "round, expected",
    [
        ([create_match(1, 2), create_match(3, 4)], {1, 2, 3, 4}),
        ([create_match(1, 2), create_match(2, 4)], {1, 2, 4}),
        ([create_match(1, 2), create_match(2, 1)], {1, 2}),
    ],
)
def test_get_players_of_round(round, expected):
    assert uut.get_players_of_round(round) == expected
