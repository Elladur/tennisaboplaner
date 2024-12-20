import pytest

from matchscheduler.match import Match, can_match_be_added
from matchscheduler.player import Player

@pytest.fixture()
def max():
    return Player("Max", ["2024-01-01"], 1)

@pytest.fixture()
def moritz():
    return Player("Moritz", ["2024-01-01"], 1)

@pytest.fixture()
def laura():
    return Player("Laura", [], 1)

@pytest.fixture()
def clara():
    return Player("Clara", [], 1)


def test_create_match(max, moritz):
    m = Match(max, moritz)
    assert m.player1 == max
    assert m.player2 == moritz
    m = Match(moritz, max)
    assert m.player1 == max
    assert m.player2 == moritz

def test_partial_match_possible(max):
    m = Match(max, None)
    assert m.player2 is None

def test_create_match_raises_error_same_player(max):
    with pytest.raises(ValueError):
        _ = Match(max, max)


def test_string_contains_names(max, moritz):
    m = Match(max, moritz)
    result = str(m)
    assert max.name in result
    assert moritz.name in result
    assert "vs" in result

def test_players_get_all_players(max, moritz):
    m = Match(max, moritz)
    assert max in m.get_players()
    assert moritz in m.get_players()

def test_player_partial_match(max):
    m = Match(max, None)
    assert max in m.get_players()
    assert None not in m.get_players()

def test_replace_player_works(max, moritz, laura):
    m = Match(max, moritz)
    expected = Match(laura, max)

    assert m.replace_player(moritz, laura)
    assert m == expected

def test_replace_player_dont_switch_if_player_alread_in_match(max, moritz):
    m = Match(max, moritz)
    
    assert not m.replace_player(max, moritz)
    assert max in m.get_players()

def test_replace_player_dont_switch_if_player_not_available(max, moritz, laura):
    m = Match(max, moritz)
    assert not m.replace_player(laura, laura)
    assert max in m.get_players()
    assert moritz in m.get_players()

def test_to_dict_works(max, moritz):
    assert Match(max, moritz).to_dict() == ("Max", "Moritz")
    assert Match(max, None).to_dict() == ("Max", None)

def test_from_dict_full_match(max, moritz):
    result = Match.from_dict(("Moritz", "Max"), [max, moritz])
    assert result == Match(max, moritz)

def test_from_dict_partial_match(max):
    result = Match.from_dict(("Max", None), [max])
    assert result == Match(max, None)

def test_can_match_be_added(max, moritz, laura, clara):
    matches = [Match(max, moritz)]
    assert can_match_be_added(matches, Match(laura, clara))
    assert can_match_be_added(matches, Match(laura, None))
    assert not can_match_be_added(matches, Match(laura, max))
    assert not can_match_be_added(matches, Match(laura, moritz))
    assert not can_match_be_added(matches, Match(max, None))

