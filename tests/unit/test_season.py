# write unit tests for the season class of matchscheduler/season.py
from datetime import date, time

import pytest

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
        [],
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


def test_create_from_settings():
    data = {
        "players": [
            {
                "name": "John",
                "cannot_play": ["2021-01-01"],
                "weight": 1,
            },
            {
                "name": "Jane",
                "cannot_play": ["2021-01-02"],
                "weight": 1,
            },
            {
                "name": "Bob",
                "cannot_play": ["2021-01-03"],
                "weight": 1,
            },
            {
                "name": "Alice",
                "cannot_play": ["2021-01-04"],
                "weight": 1,
            },
        ],
        "abo": {
            "start": "2021-01-01",
            "end": "2021-01-31",
            "overall_cost": 1000,
            "excluded_dates": [],
            "number_courts": 2,
        },
        "calendar": {
            "time_start": "18:00",
            "time_end": "20:00",
            "title": "Tennisabo",
        },
    }
    s = Season.create_from_settings(data)
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
