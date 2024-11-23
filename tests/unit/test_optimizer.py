from datetime import date, time, timedelta

import pytest

from matchscheduler.optimizer import Optimizer
from matchscheduler.player import Player
from matchscheduler.season import Season


@pytest.fixture
def players():
    return {
        Player("John", ["2021-01-01"]),
        Player("Jane", ["2021-01-02"]),
        Player("Bob", ["2021-01-03"]),
        Player("Alice", ["2021-01-04"]),
    }


def test_after_optimization_every_player_playes_against_every_other_player_at_least_once(
    players,
):
    start = date.fromisoformat("2022-01-01")
    end = start + timedelta(weeks=16 - 1)
    num_courts = 2
    s = Season(players, start, end, num_courts, time(18, 0), time(20, 0))
    o = Optimizer(s)
    o.optimize_schedule()

    # check that every player plays against every other player at least once
    for p1 in players:
        for p2 in players:
            if p1 != p2:
                assert len(s.schedule.get_matches_of_players({p1, p2})) > 0


@pytest.mark.parametrize(
    "start, rounds, num_courts",
    [
        (date.fromisoformat("2022-01-01"), 4, 2),
        (date.fromisoformat("2022-01-01"), 12, 2),
        (date.fromisoformat("2022-01-01"), 4, 1),
        (date.fromisoformat("2022-01-01"), 32, 1),
        (date.fromisoformat("2022-01-01"), 16, 1),
        (date.fromisoformat("2022-01-01"), 8, 1),
    ],
)
def test_after_optimization_every_player_plays_same_amount(players, start, rounds, num_courts):
    end = start + timedelta(weeks=rounds - 1)
    s = Season(players, start, end, num_courts, time(18, 0), time(20, 0))
    o = Optimizer(s)
    o.optimize_schedule()

    # check that every player plays the same amount of matches
    number_of_matches = {p: len(s.schedule.get_matches_of_player(p)) for p in players}
    assert len(set(number_of_matches.values())) == 1
