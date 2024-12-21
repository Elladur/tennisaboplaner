import itertools
from copy import copy
from datetime import date

import pytest

from matchscheduler.match import Match
from matchscheduler.player import Player
from matchscheduler.round import Round
from matchscheduler.schedule import Schedule


@pytest.fixture()
def players():
    return [
        Player("Max", ["2024-01-01"], 1),
        Player("Moritz", ["2024-01-01", "2024-01-08"], 1),
        Player("Laura", [], 1),
        Player("Clara", [], 1),
        Player("Patrick", [], 1),
        Player("Alex", ["2024-01-01", "2024-02-01"], 1),
    ]


@pytest.fixture()
def days_to_play():
    return [
        date(2024, 1, 1),
        date(2024, 1, 8),
        date(2024, 1, 15),
        date(2024, 1, 22),
    ]


@pytest.fixture()
def example_schedule(players, days_to_play):
    return Schedule.create(players, days_to_play, 2)


def test_create_and_init(example_schedule, days_to_play):
    assert len(example_schedule.rounds) == len(days_to_play)
    assert all(r.day in days_to_play for r in example_schedule.rounds)


def test_get_match_indizes_of_player(example_schedule, players):
    for p in players:
        result = example_schedule.get_match_indizes_of_player(p)
        assert all(p in example_schedule.rounds[i].matches[j].get_players() for i, j in result)


def test_get_match_indizes_of_match(example_schedule, players):
    for p, q in itertools.combinations(players, 2):
        m = Match(p, q)
        result = example_schedule.get_match_indizes_of_match(m)
        assert all(m == example_schedule.rounds[i].matches[j] for i, j in result)


def test_switch_matches_ignores_partial_rounds(players):
    schedule = Schedule.from_dict(
        {
            "rounds": [
                {"day": "2024-01-01", "matches": [("Laura", "Patrick"), ("Clara", None)]},
                {"day": "2024-01-08", "matches": [("Laura", "Patrick"), ("Alex", "Clara")]},
                {"day": "2024-01-15", "matches": [("Alex", "Laura"), ("Clara", "Patrick")]},
                {"day": "2024-01-22", "matches": [("Alex", "Moritz"), ("Laura", "Max")]},
            ]
        },
        2,
        players,
    )
    result = schedule.switch_matches(0, 0, 3, 2)
    assert not result


def test_switch_matches_dont_swap_if_round_not_valid(players):
    schedule = Schedule.from_dict(
        {
            "rounds": [
                {"day": "2024-01-01", "matches": [("Laura", "Patrick"), ("Clara", None)]},
                {"day": "2024-01-08", "matches": [("Laura", "Patrick"), ("Alex", "Clara")]},
                {"day": "2024-01-15", "matches": [("Alex", "Laura"), ("Clara", "Patrick")]},
                {"day": "2024-01-22", "matches": [("Alex", "Moritz"), ("Laura", "Max")]},
            ]
        },
        2,
        players,
    )
    result = schedule.switch_matches(1, 0, 2, 0)
    assert not result


def test_switch_matches_dont_swap_if_second_swat_not_valid(players):
    schedule = Schedule.from_dict(
        {
            "rounds": [
                {"day": "2024-01-01", "matches": [("Laura", "Patrick"), ("Clara", None)]},
                {"day": "2024-01-08", "matches": [("Laura", "Patrick"), ("Alex", "Clara")]},
                {"day": "2024-01-15", "matches": [("Alex", "Laura"), ("Clara", "Patrick")]},
                {"day": "2024-01-22", "matches": [("Alex", "Moritz"), ("Laura", "Max")]},
            ]
        },
        2,
        players,
    )
    old_match1 = copy(schedule.rounds[3].matches[0])
    old_match2 = copy(schedule.rounds[2].matches[0])
    result = schedule.switch_matches(3, 0, 2, 0)
    assert not result
    assert old_match1 == schedule.rounds[3].matches[0]
    assert old_match2 == schedule.rounds[2].matches[0]


def test_switch_matches_correclty(players):
    schedule = Schedule.from_dict(
        {
            "rounds": [
                {"day": "2024-01-01", "matches": [("Laura", "Patrick"), ("Clara", None)]},
                {"day": "2024-01-08", "matches": [("Laura", "Patrick"), ("Alex", "Clara")]},
                {"day": "2024-01-15", "matches": [("Alex", "Laura"), ("Clara", "Patrick")]},
                {"day": "2024-01-22", "matches": [("Alex", "Moritz"), ("Laura", "Max")]},
            ]
        },
        2,
        players,
    )
    old_match1 = copy(schedule.rounds[1].matches[0])
    old_match2 = copy(schedule.rounds[3].matches[1])
    result = schedule.switch_matches(1, 0, 3, 1)
    assert result
    assert old_match1 == schedule.rounds[3].matches[1]
    assert old_match2 == schedule.rounds[1].matches[0]


def test_to_dict(example_schedule, days_to_play):
    data = example_schedule.to_dict()
    assert isinstance(data, dict)
    assert "rounds" in data.keys()
    assert len(data["rounds"]) == len(days_to_play)


def test_from_dict(players):
    s = Schedule.from_dict(
        {
            "rounds": [
                {"day": "2024-01-01", "matches": [("Laura", "Patrick"), ("Clara", None)]},
                {"day": "2024-01-08", "matches": [("Laura", "Patrick"), ("Alex", "Clara")]},
                {"day": "2024-01-15", "matches": [("Alex", "Laura"), ("Clara", "Patrick")]},
                {"day": "2024-01-22", "matches": [("Alex", "Moritz"), ("Laura", "Max")]},
            ]
        },
        2,
        players,
    )
    assert isinstance(s, Schedule)
