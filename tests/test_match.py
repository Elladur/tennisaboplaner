# write unit test for match.py

from datetime import date
from matchscheduler.match import Match, MatchFactory
from matchscheduler.player import Player
import pytest
from itertools import combinations


@pytest.mark.parametrize(
    "players, match_date",
    [
        (
            {Player("John", ["2021-01-01"]), Player("Jane", ["2021-01-02"])},
            date.fromisoformat("2021-01-03"),
        ),
        (
            {Player("Bob", ["2021-01-04"]), Player("Alice", ["2021-01-05"])},
            date.fromisoformat("2021-01-06"),
        ),
    ],
)
def test_match_init(players, match_date):
    m = Match(players, match_date)
    assert m.players == players
    assert m.date == match_date


def test_match_init_raises_failure_if_player_cannot_play():
    with pytest.raises(Exception):
        Match(
            (Player("John", ["2021-01-01"]), Player("Jane", ["2021-01-02"])),
            date.fromisoformat("2021-01-02"),
        )


def test_match_init_raises_exception_if_players_are_the_same():
    with pytest.raises(Exception):
        john = Player("John", ["2021-01-01"])
        Match(
            {john, john},
            date.fromisoformat("2021-01-03"),
        )


def test_match_init_raises_exception_if_players_are_not_two():
    with pytest.raises(Exception):
        Match(
            (
                Player("John", ["2021-01-01"]),
                Player("Jane", ["2021-01-02"]),
                Player("Bob", ["2021-01-03"]),
            ),
            date.fromisoformat("2021-01-04"),
        )


def test_match_str():
    m = Match(
        (Player("John", ["2021-01-01"]), Player("Jane", ["2021-01-02"])),
        date.fromisoformat("2021-01-03"),
    )
    assert str(m) == "Jane vs John"


def test_generate_valid_new_match():
    john = Player("John", ["2021-01-01"])
    jane = Player("Jane", ["2021-01-02"])
    bob = Player("Bob", ["2021-01-03"])
    players = [john, jane, bob]
    matches = []
    d = date.fromisoformat("2021-01-05")
    for match in MatchFactory.generate_valid_new_match(players, d, matches):
        assert match.date == d
        assert match not in matches
        matches.append(match)
    assert len(matches) == 3
    for a, b in combinations(players, 2):
        assert {a, b} in [m.players for m in matches]


def test_generate_valid_new_match_gives_a_valid_match():
    john = Player("John", ["2021-01-01"])
    jane = Player("Jane", ["2021-01-02"])
    bob = Player("Bob", ["2021-01-03"])
    players = [john, jane, bob]
    matches = []
    d = date.fromisoformat("2021-01-02")
    for match in MatchFactory.generate_valid_new_match(players, d, matches):
        matches.append(match)
    assert len(matches) == 1
    assert matches[0].players == {john, bob}


def test_generate_valid_new_match_returns_empty_result_if_match_is_alread_in_list():
    john = Player("John", ["2021-01-01"])
    jane = Player("Jane", ["2021-01-02"])
    bob = Player("Bob", ["2021-01-03"])
    players = [john, jane, bob]
    matches = [Match({john, jane}, date.fromisoformat("2021-01-03"))]
    d = date.fromisoformat("2021-01-04")
    result = []
    for match in MatchFactory.generate_valid_new_match(players, d, matches):
        result.append(match)
    for m in matches:
        assert m not in result


def test_generate_valid_new_match_returns_empty_result_if_no_match_could_be_found():
    john = Player("John", ["2021-01-01"])
    jane = Player("Jane", ["2021-01-01"])
    players = [john, jane]
    matches = []
    d = date.fromisoformat("2021-01-01")
    for match in MatchFactory.generate_valid_new_match(players, d, matches):
        matches.append(match)
    assert len(matches) == 0
