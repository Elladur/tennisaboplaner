# write unit tests for the season class of matchscheduler/season.py
import tempfile
from datetime import date, time, timedelta
from unittest.mock import Mock, patch

import pytest

from matchscheduler.player import Player
from matchscheduler.schedule import Schedule
from matchscheduler.season import Season


@pytest.fixture
def players():
    return {
        Player("John", ["2021-01-01"]),
        Player("Jane", ["2021-01-02"]),
        Player("Bob", ["2021-01-03"]),
        Player("Alice", ["2021-01-04"]),
    }


def test_init(players):
    start = date.fromisoformat("2021-01-01")
    end = date.fromisoformat("2021-01-31")
    number_courts = 2
    s = Season(
        players,
        start,
        end,
        number_courts,
        time.fromisoformat("18:00"),
        time.fromisoformat("20:00"),
    )
    assert s.players == players
    assert s.start == start
    assert s.end == end
    assert s.num_courts == number_courts
    assert s.dates == [
        date.fromisoformat("2021-01-01"),
        date.fromisoformat("2021-01-08"),
        date.fromisoformat("2021-01-15"),
        date.fromisoformat("2021-01-22"),
        date.fromisoformat("2021-01-29"),
    ]
    assert s.schedule is None


def test_from_dict():
    data = {
        "players": [
            {
                "name": "John",
                "cannot_play": ["2021-01-01"],
            },
            {
                "name": "Jane",
                "cannot_play": ["2021-01-02"],
            },
            {
                "name": "Bob",
                "cannot_play": ["2021-01-03"],
            },
            {
                "name": "Alice",
                "cannot_play": ["2021-01-04"],
            },
        ],
        "abo": {
            "start": "2021-01-01",
            "end": "2021-01-31",
            "number_courts": 2,
        },
        "calendar": {
            "time_start": "18:00",
            "time_end": "20:00",
            "title": "Tennisabo",
        },
    }
    s = Season.from_dict(data)
    assert s.players == {
        Player("John", ["2021-01-01"]),
        Player("Jane", ["2021-01-02"]),
        Player("Bob", ["2021-01-03"]),
        Player("Alice", ["2021-01-04"]),
    }
    assert s.start == date.fromisoformat("2021-01-01")
    assert s.end == date.fromisoformat("2021-01-31")
    assert s.num_courts == 2
    assert s.dates == [
        date.fromisoformat("2021-01-01"),
        date.fromisoformat("2021-01-08"),
        date.fromisoformat("2021-01-15"),
        date.fromisoformat("2021-01-22"),
        date.fromisoformat("2021-01-29"),
    ]
    assert s.time_start == time.fromisoformat("18:00")
    assert s.time_end == time.fromisoformat("20:00")
    assert s.calendar_title == "Tennisabo"
    assert s.schedule is None


def test_generate_schedule(players):
    start = date.fromisoformat("2021-01-01")
    end = date.fromisoformat("2021-01-31")
    number_courts = 2
    s = Season(
        players,
        start,
        end,
        number_courts,
        time.fromisoformat("18:00"),
        time.fromisoformat("20:00"),
    )

    return_val = Schedule([], players)
    with patch(
        "matchscheduler.season.ScheduleFactory.generate_valid_schedule", return_value=return_val
    ) as mock:
        s.generate_schedule()

        mock.assert_called_once_with(players, s.dates, number_courts)
        assert s.schedule == return_val


def test_export_season_calls_schedule_export(players):
    start = date.fromisoformat("2021-01-01")
    end = date.fromisoformat("2021-01-31")
    number_courts = 2
    s = Season(
        players,
        start,
        end,
        number_courts,
        time.fromisoformat("18:00"),
        time.fromisoformat("20:00"),
    )

    m = Mock()
    s.schedule = m

    with tempfile.TemporaryDirectory() as temp_dir:
        s.export_season(temp_dir + "/")

    m.export.assert_called_once_with(temp_dir + "/", "Tennisabo", time(18, 0), time(20, 0))


# region integration tests


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
    s.generate_schedule()
    s.optimize_schedule()

    # check that every player plays the same amount of matches
    number_of_matches = {p: len(s.schedule.get_matches_of_player(p)) for p in players}
    assert len(set(number_of_matches.values())) == 1


def test_after_optimization_every_player_playes_against_every_other_player_at_least_once(
    players,
):
    start = date.fromisoformat("2022-01-01")
    end = start + timedelta(weeks=16 - 1)
    num_courts = 2
    s = Season(players, start, end, num_courts, time(18, 0), time(20, 0))
    s.generate_schedule()
    s.optimize_schedule()

    # check that every player plays against every other player at least once
    for p1 in players:
        for p2 in players:
            if p1 != p2:
                assert len(s.schedule.get_matches_of_players({p1, p2})) > 0


# endregion
