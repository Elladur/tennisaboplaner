import json
from datetime import date, time

import pytest

from matchscheduler.player import Player
from matchscheduler.schedule import Schedule
from matchscheduler.season import Season


@pytest.fixture()
def player_list():
    return [
        Player("Max", ["2024-01-01", "2024-01-08"], 1),
        Player("Peter", ["2024-01-08"], 1),
        Player("Ida", [], 2),
        Player("Franz", [], 1),
        Player("Helmut", [], 1),
        Player("Jens", [], 1),
    ]


@pytest.fixture()
def season_with_too_less_players():
    player_list = [
        Player("Max", ["2024-01-01", "2024-01-08"], 1),
        Player("Peter", ["2024-01-01"], 1),
        Player("Ida", [], 1),
        Player("Moritz", [], 1),
        Player("Franz", [], 1),
    ]
    return Season(player_list, date(2024, 1, 1), date(2024, 1, 29), 2, time(19), time(21), [], 100)


def test_create_ignores_excluded_dates(player_list):
    excluded_dates = [date(2024, 1, 15), date(2024, 1, 22)]
    s = Season.create(
        player_list, date(2024, 1, 1), date(2024, 3, 1), 2, excluded_dates, time(19), time(21)
    )
    assert s.excluded_dates == excluded_dates
    assert isinstance(s.schedule, Schedule)
    assert all(r.day not in excluded_dates for r in s.schedule.rounds)


def test_from_dict():
    data = {
        "players": [
            {"name": "Max", "cannot_play": ["2024-01-01", "2024-01-08"], "weight": 1},
            {"name": "Peter", "cannot_play": ["2024-01-08"], "weight": 1},
            {"name": "Ida", "cannot_play": [], "weight": 2},
            {"name": "Franz", "cannot_play": [], "weight": 1},
            {"name": "Helmut", "cannot_play": [], "weight": 1},
            {"name": "Jens", "cannot_play": [], "weight": 1},
        ],
        "start": "2024-01-01",
        "end": "2024-03-01",
        "number_courts": 2,
        "time_start": "19:00:00",
        "time_end": "21:00:00",
        "excluded_dates": ["2024-01-15", "2024-01-22"],
        "overall_cost": 0,
        "calendar_title": "Tennisabo",
        "schedule": {
            "rounds": [
                {"day": "2024-01-01", "matches": [("Jens", "Peter"), ("Franz", "Helmut")]},
                {"day": "2024-01-08", "matches": [("Franz", "Ida"), ("Helmut", "Jens")]},
                {"day": "2024-01-29", "matches": [("Helmut", "Peter"), ("Franz", "Max")]},
                {"day": "2024-02-05", "matches": [("Max", "Peter"), ("Franz", "Helmut")]},
                {"day": "2024-02-12", "matches": [("Ida", "Jens"), ("Helmut", "Peter")]},
                {"day": "2024-02-19", "matches": [("Franz", "Peter"), ("Helmut", "Ida")]},
                {"day": "2024-02-26", "matches": [("Max", "Peter"), ("Franz", "Ida")]},
            ]
        },
    }
    s = Season.from_dict(data)
    assert isinstance(s, Season)


def test_to_dict():
    data = {
        "players": [
            {"name": "Max", "cannot_play": ["2024-01-01", "2024-01-08"], "weight": 1},
            {"name": "Peter", "cannot_play": ["2024-01-08"], "weight": 1},
            {"name": "Ida", "cannot_play": [], "weight": 2},
            {"name": "Franz", "cannot_play": [], "weight": 1},
            {"name": "Helmut", "cannot_play": [], "weight": 1},
            {"name": "Jens", "cannot_play": [], "weight": 1},
        ],
        "start": "2024-01-01",
        "end": "2024-03-01",
        "number_courts": 2,
        "time_start": "19:00:00",
        "time_end": "21:00:00",
        "excluded_dates": ["2024-01-15", "2024-01-22"],
        "overall_cost": 0,
        "calendar_title": "Tennisabo",
        "schedule": {
            "rounds": [
                {"day": "2024-01-01", "matches": [("Jens", "Peter"), ("Franz", "Helmut")]},
                {"day": "2024-01-08", "matches": [("Franz", "Ida"), ("Helmut", "Jens")]},
                {"day": "2024-01-29", "matches": [("Helmut", "Peter"), ("Franz", "Max")]},
                {"day": "2024-02-05", "matches": [("Max", "Peter"), ("Franz", "Helmut")]},
                {"day": "2024-02-12", "matches": [("Ida", "Jens"), ("Helmut", "Peter")]},
                {"day": "2024-02-19", "matches": [("Franz", "Peter"), ("Helmut", "Ida")]},
                {"day": "2024-02-26", "matches": [("Max", "Peter"), ("Franz", "Ida")]},
            ]
        },
    }
    s = Season.from_dict(data)
    result = s.to_dict()
    assert result == data


def test_create_from_settings():
    with open("settings.json") as f:
        data = json.load(f)
        s = Season.create_from_settings(data)
        assert isinstance(s, Season)
