import pytest

from copy import copy
from matchscheduler.round import Round
from matchscheduler.match import Match
from matchscheduler.player import Player
from datetime import date


@pytest.fixture()
def players():
    return [
        Player("Max", ["2024-01-01", "2024-01-08"], 1),
        Player("Moritz", ["2024-01-01", "2024-01-08"], 1),
        Player("Laura", [], 1),
        Player("Clara", [], 1),
        Player("Patrick", [], 1),
        Player("Alex", ["2024-02-01"], 1),
    ]

@pytest.fixture()
def example_round(players) -> Round:
    return Round([Match(players[0], players[1]), Match(players[2], players[3])], date(2024, 2, 1), 2)

@pytest.fixture()
def example_partial_round(players) -> Round:
    return Round([Match(players[0], players[1])], date(2024, 2, 1), 2)

def test_round_init_full_court(players):
    day = date(2024, 2, 1)
    matches = [Match(players[0], players[1])]
    r = Round(matches, day, 1)
    assert r.matches == matches
    assert not r.is_partial
    assert r.day == day

def test_round_init_partial(players):
    day = date(2024, 2, 1)
    matches = [Match(players[0], players[1])]
    r = Round(matches, day, 2)
    assert r.matches == matches
    assert r.is_partial
    assert r.day == day

def test_round_init_checks_dates(players):
    day = date(2024, 1, 1)
    matches = [Match(players[0], players[1])]
    with pytest.raises(ValueError):
        _ = Round(matches, day, 2)

def test_get_player_of_round(example_round, players):
    result = list(example_round.get_players())
    assert players[0] in result
    assert players[1] in result
    assert players[2] in result
    assert players[3] in result
    assert players[4] not in result

def test_get_player_of_round_except_match(example_round, players):
    result = list(example_round.get_players_of_round_except_match(1))
    assert players[0] in result
    assert players[1] in result
    assert players[2] not in result
    assert players[3] not in result
    assert players[4] not in result

def test_replace_match(example_round, players):
    new_match = Match(players[3], players[4])
    result = example_round.replace_match(1, new_match)
    assert result
    assert example_round.matches[1] == new_match

def test_replace_match_dont_work_if_player_already_plays(example_round, players):
    new_match = Match(players[3], players[1])
    result = example_round.replace_match(1, new_match)
    assert not result
    assert example_round.matches[1] != new_match

def test_replace_match_dont_work_if_player_cant_play_on_date(example_round, players):
    new_match = Match(players[3], players[5])
    result = example_round.replace_match(1, new_match)
    assert not result
    assert example_round.matches[1] != new_match

def test_replace_match_dont_work_on_partial_round(example_partial_round, players):
    new_match = Match(players[2], players[3])
    result = example_partial_round.replace_match(0, new_match)
    assert not result
    assert example_partial_round.matches[0] != new_match

def test_swap_players_works(example_round, players):
    old_match1 = copy(example_round.matches[0])
    old_match2 = copy(example_round.matches[1])
    result = example_round.swap_players(players[0], players[2])
    assert result
    assert old_match1 != example_round.matches[0]
    assert players[2] in example_round.matches[0].get_players()
    assert old_match2 != example_round.matches[1]
    assert players[0] in example_round.matches[1].get_players()

def test_swap_players_doesnt_change_if_not_both_present(example_round, players):
    result = example_round.swap_players(players[0], players[4])
    assert not result