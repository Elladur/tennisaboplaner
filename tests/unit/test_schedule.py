import pytest

import matchscheduler.schedule as uut


@pytest.mark.parametrize(
    "schedule, player_index, expected",
    [
        ([[(1, 2), (3, 4)], [(1, 4), (2, 3)]], 1, [(0, 0), (1, 0)]),
        ([[(1, 2), (3, 4)], [(1, 4), (2, 3)]], 2, [(0, 0), (1, 1)]),
        ([[(1, 2), (3, 4)], [(1, 4), (2, 3)]], 4, [(0, 1), (1, 0)]),
        ([[(1, 2), (3, 4)], [(1, 4), (2, 3)]], 5, []),
    ],
)
def test_get_match_indizes_of_player(schedule, player_index, expected):
    assert uut.get_match_indizes_of_player(schedule, player_index) == expected


@pytest.mark.parametrize(
    "schedule, match, expected",
    [
        ([[(1, 2), (3, 4)], [(1, 4), (2, 3)], [(1, 2), (3, 4)]], (1, 2), [(0, 0), (2, 0)]),
        ([[(1, 2), (3, 4)], [(1, 4), (2, 3)], [(1, 2), (3, 4)]], (2, 3), [(1, 1)]),
        ([[(1, 2), (3, 4)], [(1, 4), (2, 3)], [(1, 2), (3, 4)]], (5, 6), []),
    ],
)
def test_get_match_indizes_of_match(schedule, match, expected):
    assert uut.get_match_indizes_of_match(schedule, match) == expected
