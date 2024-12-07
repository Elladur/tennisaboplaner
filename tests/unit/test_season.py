import pytest
from matchscheduler.match import Match, create_match
from matchscheduler.season import Season
from matchscheduler.player import Player
from datetime import date, time
import json


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
def season_instance():
    return Season.from_dict(json.loads("{\"players\": [{\"name\": \"Max\", \"cannot_play\": [\"2024-01-01\", \"2024-01-08\"], \"weight\": 1}, {\"name\": \"Peter\", \"cannot_play\": [\"2024-01-08\"], \"weight\": 1}, {\"name\": \"Ida\", \"cannot_play\": [], \"weight\": 2}, {\"name\": \"Franz\", \"cannot_play\": [], \"weight\": 1}, {\"name\": \"Helmut\", \"cannot_play\": [], \"weight\": 1}, {\"name\": \"Jens\", \"cannot_play\": [], \"weight\": 1}], \"start\": \"2024-01-01\", \"end\": \"2024-04-29\", \"number_courts\": 2, \"time_start\": \"19:00:00\", \"time_end\": \"21:00:00\", \"excluded_dates\": [], \"overall_cost\": 2000, \"calendar_title\": \"Tennisabo\", \"schedule\": [[[2, 3], [1, 5]], [[3, 4], [2, 5]], [[1, 2], [0, 5]], [[1, 2], [4, 5]], [[3, 5], [1, 2]], [[1, 2], [0, 5]], [[1, 3], [4, 5]], [[1, 3], [2, 4]], [[0, 4], [1, 2]], [[3, 5], [0, 4]], [[2, 3], [0, 4]], [[1, 5], [3, 4]], [[0, 5], [1, 4]], [[0, 5], [1, 2]], [[2, 4], [0, 3]], [[1, 4], [0, 3]], [[1, 5], [0, 3]], [[1, 2], [3, 5]]]}"))

def test_init_excludes_dates(player_list):
    excluded_date = ["2024-01-15"]
    season = Season(player_list, date(2024, 1, 1), date(2024, 1, 29), 1, time(19), time(21), excluded_date, 2000)

    assert excluded_date[0] not in [str(d) for d in season.dates]


def test_init_generates_valid_schedule(player_list):
    season = Season(player_list, date(2024, 1, 1), date(2024, 1, 29), 1, time(19), time(21), [], 2000)

    assert season.schedule is not None
    assert season.check_schedule_is_valid()

def test_change_match_changes_match_if_valid(season_instance):
    old_match = season_instance.schedule[3][1]
    new_match = create_match(3, 4)
    result = season_instance.change_match(3, 1, new_match)

    assert result
    assert old_match != new_match
    assert season_instance.schedule[3][1] == new_match