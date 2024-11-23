# write unit tests for the schedule class of matchscheduler/schedule.py
from datetime import date

import pytest

from matchscheduler.match import Match
from matchscheduler.player import Player
from matchscheduler.round import Round, RoundFactory
from matchscheduler.schedule import NotValidSwapError, Schedule, ScheduleFactory


@pytest.fixture
def players():
    return {
        Player("John", ["2021-01-01"]),
        Player("Jane", ["2021-01-02"]),
        Player("Bob", ["2021-01-03"]),
        Player("Alice", ["2021-01-04"]),
    }


@pytest.fixture
def rounds(players):
    return [
        RoundFactory.generate_valid_round(players, date.fromisoformat("2021-01-07"), 2),
        RoundFactory.generate_valid_round(players, date.fromisoformat("2021-01-14"), 2),
        RoundFactory.generate_valid_round(players, date.fromisoformat("2021-01-21"), 2),
    ]


def test_init_empty():
    s = Schedule([], {})
    assert s.rounds == []
    assert s.players == {}


def test_init_with_values(rounds, players):
    s = Schedule(rounds, players)
    assert s.rounds == rounds
    assert s.players == players


def test_is_valid_if_rounds_are_valid(rounds, players):
    s = Schedule(rounds, players)
    assert s.is_valid() is True


def test_is_valid_is_false_if_rounds_are_not_valid(rounds, players):
    rounds[0].matches[0].date = date.fromisoformat("2021-01-01")
    rounds[0].matches[0].players = {
        next(filter(lambda x: x.name == "John", players)),
        next(filter(lambda x: x.name != "John", players)),
    }
    s = Schedule(rounds, players)
    assert s.is_valid() is False


def test_get_matches(rounds, players):
    s = Schedule(rounds, players)
    assert s.get_matches() == [m for r in rounds for m in r.matches]


def test_get_matches_of_player(rounds, players):
    s = Schedule(rounds, players)
    assert s.get_matches_of_player(next(filter(lambda x: x.name == "John", players))) == [
        m
        for r in rounds
        for m in r.matches
        if next(filter(lambda x: x.name == "John", players)) in m.players
    ]


def test_get_matches_of_player_returns_empty_list_if_player_is_not_in_schedule(rounds, players):
    s = Schedule(rounds, players)
    assert s.get_matches_of_player(Player("Not in schedule", ["2021-01-01"])) == []


def test_get_matches_of_players(rounds, players):
    s = Schedule(rounds, players)
    assert s.get_matches_of_players(
        {
            next(filter(lambda x: x.name == "John", players)),
            next(filter(lambda x: x.name == "Jane", players)),
        }
    ) == [
        m
        for r in rounds
        for m in r.matches
        if next(filter(lambda x: x.name == "John", players)) in m.players
        and next(filter(lambda x: x.name == "Jane", players)) in m.players
    ]


def test_get_matches_of_players_returns_empty_list_if_players_are_not_in_schedule(rounds, players):
    s = Schedule(rounds, players)
    assert (
        s.get_matches_of_players(
            {
                Player("Not in schedule", ["2021-01-01"]),
                Player("Also not in schedule", ["2021-01-01"]),
            }
        )
        == []
    )


def test_swap_matches(rounds, players):
    s = Schedule(rounds, players)
    match1 = s.rounds[0].matches[0]
    match2 = s.rounds[1].matches[0]
    s.swap_matches(0, 0, 1, 0)
    assert s.rounds[0].matches[0].players == match2.players
    assert s.rounds[1].matches[0].players == match1.players


def test_swap_matches_raises_exception_if_swap_is_not_valid(players):
    player1 = players.pop()
    player2 = players.pop()
    player3 = players.pop()
    player4 = players.pop()
    match1 = Match({player1, player2}, date.fromisoformat("2021-02-01"))
    match2 = Match({player3, player4}, date.fromisoformat("2021-02-01"))
    match3 = Match({player1, player2}, date.fromisoformat("2021-02-08"))
    match4 = Match({player3, player4}, date.fromisoformat("2021-02-08"))
    round1 = Round([match1, match2], date.fromisoformat("2021-02-01"), 2)
    round2 = Round([match3, match4], date.fromisoformat("2021-02-08"), 2)
    s = Schedule([round1, round2], players)

    with pytest.raises(NotValidSwapError):
        s.swap_matches(0, 0, 1, 1)
    assert s.rounds[0] == round1
    assert s.rounds[1] == round2


def test_generate_valid_schedule_yields_valid_scheduler(players):
    dates = [
        date.fromisoformat("2021-01-07"),
        date.fromisoformat("2021-01-14"),
        date.fromisoformat("2021-01-21"),
    ]
    s = ScheduleFactory.generate_valid_schedule(players, dates, 2)
    assert s.is_valid() is True
    assert len(s.rounds) == len(dates)
    for r in s.rounds:
        assert len(r.matches) == 2


def test_generate_valid_schedule_raises_exception_if_it_cant_find_any(players):
    dates = [
        date.fromisoformat("2021-01-07"),
        date.fromisoformat("2021-01-14"),
        date.fromisoformat("2021-01-21"),
    ]
    with pytest.raises(Exception):
        ScheduleFactory.generate_valid_schedule(players, dates, 5)
