from unittest.mock import Mock

import pytest

from matchscheduler.match import create_match
from matchscheduler.player import Player
from matchscheduler.scoring_algorithm import ScoringAlgorithm


@pytest.fixture()
def player_list():
    return [
        Player("Max", ["2024-01-01", "2024-01-08"], 1),
        Player("Peter", ["2024-01-08"], 1),
        Player("Ida", [], 2),
    ]


@pytest.fixture()
def schedule_with_one_player_not_playing():
    return [
        [
            create_match(0, 1),
        ],
        [
            create_match(0, 1),
        ],
        [
            create_match(0, 1),
        ],
        [
            create_match(0, 1),
        ],
        [
            create_match(0, 1),
        ],
        [
            create_match(0, 1),
        ],
    ]


@pytest.fixture()
def schedule_even():
    return [
        [
            create_match(0, 1),
        ],
        [
            create_match(2, 1),
        ],
        [
            create_match(2, 0),
        ],
        [
            create_match(0, 1),
        ],
        [
            create_match(2, 1),
        ],
        [
            create_match(2, 0),
        ],
    ]


@pytest.fixture()
def schedule_blocks():
    return [
        [
            create_match(0, 1),
        ],
        [
            create_match(0, 1),
        ],
        [
            create_match(2, 0),
        ],
        [
            create_match(2, 0),
        ],
        [
            create_match(2, 1),
        ],
        [
            create_match(2, 1),
        ],
    ]


def test_get_score():
    uut = ScoringAlgorithm()
    uut.get_std_of_all_possible_matches = Mock(return_value=2)
    uut.get_std_of_player_times_playing = Mock(return_value=3)
    uut.get_std_of_pause_between_matches = Mock(return_value=5)
    uut.get_std_of_pause_between_playing = Mock(return_value=7)

    result = uut.get_score([[1, 1]], [])
    assert result == 2 + 3 + 5 + 7
    uut.get_std_of_all_possible_matches.assert_called_once()
    uut.get_std_of_player_times_playing.assert_called_once()
    uut.get_std_of_pause_between_matches.assert_called_once()
    uut.get_std_of_pause_between_playing.assert_called_once()


def test_schedule_with_one_player_not_playing_is_worse(
    schedule_with_one_player_not_playing, schedule_even, player_list
):
    uut = ScoringAlgorithm()
    assert uut.get_std_of_player_times_playing(
        schedule_with_one_player_not_playing, player_list
    ) > uut.get_std_of_player_times_playing(schedule_even, player_list)
    assert uut.get_std_of_all_possible_matches(
        schedule_with_one_player_not_playing, player_list
    ) > uut.get_std_of_all_possible_matches(schedule_even, player_list)
    assert uut.get_std_of_pause_between_matches(
        schedule_with_one_player_not_playing, player_list
    ) > uut.get_std_of_pause_between_matches(schedule_even, player_list)
    assert uut.get_std_of_pause_between_playing(
        schedule_with_one_player_not_playing, player_list
    ) > uut.get_std_of_pause_between_playing(schedule_even, player_list)


def test_schedule_block_is_worse(schedule_blocks, schedule_even, player_list):
    uut = ScoringAlgorithm()
    assert uut.get_std_of_player_times_playing(
        schedule_blocks, player_list
    ) == uut.get_std_of_player_times_playing(schedule_even, player_list)
    assert uut.get_std_of_all_possible_matches(
        schedule_blocks, player_list
    ) == uut.get_std_of_all_possible_matches(schedule_even, player_list)
    assert uut.get_std_of_pause_between_matches(
        schedule_blocks, player_list
    ) > uut.get_std_of_pause_between_matches(schedule_even, player_list)
    assert uut.get_std_of_pause_between_playing(
        schedule_blocks, player_list
    ) > uut.get_std_of_pause_between_playing(schedule_even, player_list)
