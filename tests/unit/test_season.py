import json
from datetime import date, time

import pytest

from matchscheduler.match import create_match
from matchscheduler.player import Player
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
def season_instance():
    return Season.from_dict(
        json.loads(
            '{"players": [{"name": "Max", "cannot_play": ["2024-01-01", "2024-01-08"], "weight": 1}, {"name": "Peter", "cannot_play": ["2024-01-08"], "weight": 1}, {"name": "Ida", "cannot_play": [], "weight": 2}, {"name": "Franz", "cannot_play": [], "weight": 1}, {"name": "Helmut", "cannot_play": [], "weight": 1}, {"name": "Jens", "cannot_play": [], "weight": 1}], "start": "2024-01-01", "end": "2024-04-29", "number_courts": 2, "time_start": "19:00:00", "time_end": "21:00:00", "excluded_dates": [], "overall_cost": 2000, "calendar_title": "Tennisabo", "schedule": [[[2, 3], [1, 5]], [[3, 4], [2, 5]], [[1, 2], [0, 5]], [[1, 2], [4, 5]], [[3, 5], [1, 2]], [[1, 2], [0, 5]], [[1, 3], [4, 5]], [[1, 3], [2, 4]], [[0, 4], [1, 2]], [[3, 5], [0, 4]], [[2, 3], [0, 4]], [[1, 5], [3, 4]], [[0, 5], [1, 4]], [[0, 5], [1, 2]], [[2, 4], [0, 3]], [[1, 4], [0, 3]], [[1, 5], [0, 3]], [[1, 2], [3, 5]]]}'  # noqa: E501
        )
    )


def test_init_excludes_dates(player_list):
    excluded_date = ["2024-01-15"]
    season = Season(
        player_list, date(2024, 1, 1), date(2024, 1, 29), 1, time(19), time(21), excluded_date, 2000
    )

    assert excluded_date[0] not in [str(d) for d in season.dates]


def test_init_generates_valid_schedule(player_list):
    season = Season(
        player_list, date(2024, 1, 1), date(2024, 1, 29), 1, time(19), time(21), [], 2000
    )

    assert season.schedule is not None
    assert season.check_schedule_is_valid()


def test_change_match_changes_match_if_valid(season_instance):
    old_match = season_instance.schedule[3][1]
    new_match = create_match(3, 4)
    result = season_instance.change_match(3, 1, new_match)

    assert result
    assert old_match != new_match
    assert season_instance.schedule[3][1] == new_match


def test_change_match_doesnt_change_if_invalid(season_instance):
    old_match = season_instance.schedule[3][1]
    new_match = season_instance.schedule[3][0]
    result = season_instance.change_match(3, 1, new_match)

    assert not result
    assert old_match != new_match
    assert season_instance.schedule[3][1] == old_match


def test_check_if_round_is_valid_returns_false_if_player_number_isnt_correct(season_instance):
    season_instance.schedule[0] = [create_match(1, 2)]
    assert not season_instance.check_if_round_is_valid(0)


def test_check_if_round_is_valid_retunrs_false_if_player_cant_play(season_instance):
    # Max = player 0 cant play on first date
    season_instance.schedule[0] = [create_match(0, 2), create_match(3, 4)]
    assert not season_instance.check_if_round_is_valid(0)


def test_check_if_round_is_valid_returns_true_for_valid_schedule(season_instance):
    for i, _ in enumerate(season_instance.schedule):
        assert season_instance.check_if_round_is_valid(i)


def test_check_schedule_is_valid_returns_true_for_valid_schedule(season_instance):
    assert season_instance.check_schedule_is_valid()


def test_check_schedule_is_valid_returns_false_for_non_valid_schedule(season_instance):
    # Max = player 0 cant play on first date
    season_instance.schedule[0] = [create_match(0, 2), create_match(3, 4)]
    assert not season_instance.check_schedule_is_valid()


def test_swap_players_of_existing_matches_does_swap(season_instance):
    old_round = [x for x in season_instance.schedule[0]]
    season_instance.swap_players_of_existing_matches(0, 2, 1)
    assert season_instance.schedule[0] != old_round


def test_swap_players_of_existing_matches_is_idempotent(season_instance):
    old_round = [x for x in season_instance.schedule[0]]
    season_instance.swap_players_of_existing_matches(0, 2, 1)
    season_instance.swap_players_of_existing_matches(0, 2, 1)
    assert season_instance.schedule[0] == old_round


def test_swap_players_of_existing_matches_is_symmetric(season_instance):
    old_round = [x for x in season_instance.schedule[0]]
    season_instance.swap_players_of_existing_matches(0, 2, 1)
    new_round1 = [x for x in season_instance.schedule[0]]
    season_instance.schedule[0] = old_round
    season_instance.swap_players_of_existing_matches(0, 1, 2)
    new_round2 = [x for x in season_instance.schedule[0]]
    assert new_round1 == new_round2
