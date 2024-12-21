from datetime import date
from unittest.mock import Mock

import pytest

from matchscheduler.match import Match
from matchscheduler.player import Player
from matchscheduler.round import Round
from matchscheduler.schedule import Schedule
from matchscheduler.scoring_algorithm import ScoringAlgorithm


@pytest.fixture()
def players():
    return [
        Player("Max", [], 1),
        Player("Peter", [], 1),
        Player("Ida", [], 2),
    ]


@pytest.fixture()
def schedule_with_one_player_not_playing(players):
    return Schedule(
        [
            Round([Match(players[0], players[1])], date(2024, 1, 1), 1),
            Round([Match(players[0], players[1])], date(2024, 1, 1), 1),
            Round([Match(players[0], players[1])], date(2024, 1, 1), 1),
            Round([Match(players[0], players[1])], date(2024, 1, 1), 1),
            Round([Match(players[0], players[1])], date(2024, 1, 1), 1),
            Round([Match(players[0], players[1])], date(2024, 1, 1), 1),
        ]
    )


@pytest.fixture()
def schedule_even(players):
    return Schedule(
        [
            Round([Match(players[0], players[1])], date(2024, 1, 1), 1),
            Round([Match(players[2], players[1])], date(2024, 1, 1), 1),
            Round([Match(players[2], players[0])], date(2024, 1, 1), 1),
            Round([Match(players[0], players[1])], date(2024, 1, 1), 1),
            Round([Match(players[2], players[1])], date(2024, 1, 1), 1),
            Round([Match(players[2], players[0])], date(2024, 1, 1), 1),
        ]
    )


@pytest.fixture()
def schedule_blocks(players):
    return Schedule(
        [
            Round([Match(players[0], players[1])], date(2024, 1, 1), 1),
            Round([Match(players[0], players[1])], date(2024, 1, 1), 1),
            Round([Match(players[2], players[0])], date(2024, 1, 1), 1),
            Round([Match(players[2], players[0])], date(2024, 1, 1), 1),
            Round([Match(players[2], players[1])], date(2024, 1, 1), 1),
            Round([Match(players[2], players[1])], date(2024, 1, 1), 1),
        ]
    )


@pytest.fixture()
def balenced_to_weight(players):
    return Schedule(
        [
            Round([Match(players[0], players[1])], date(2024, 1, 1), 1),
            Round([Match(players[2], players[0])], date(2024, 1, 1), 1),
            Round([Match(players[2], players[1])], date(2024, 1, 1), 1),
            Round([Match(players[2], players[0])], date(2024, 1, 1), 1),
            Round([Match(players[2], players[1])], date(2024, 1, 1), 1),
            Round([Match(players[2], players[0])], date(2024, 1, 1), 1),
        ]
    )


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
    schedule_with_one_player_not_playing, schedule_even, players
):
    uut = ScoringAlgorithm()
    assert uut.get_std_of_player_times_playing(
        schedule_with_one_player_not_playing, players
    ) > uut.get_std_of_player_times_playing(schedule_even, players)
    assert uut.get_std_of_all_possible_matches(
        schedule_with_one_player_not_playing, players
    ) > uut.get_std_of_all_possible_matches(schedule_even, players)
    assert uut.get_std_of_pause_between_matches(
        schedule_with_one_player_not_playing, players
    ) > uut.get_std_of_pause_between_matches(schedule_even, players)
    assert uut.get_std_of_pause_between_playing(
        schedule_with_one_player_not_playing, players
    ) > uut.get_std_of_pause_between_playing(schedule_even, players)


def test_schedule_block_is_worse(schedule_blocks, schedule_even, players):
    uut = ScoringAlgorithm()
    assert uut.get_std_of_player_times_playing(
        schedule_blocks, players
    ) == uut.get_std_of_player_times_playing(schedule_even, players)
    assert uut.get_std_of_all_possible_matches(
        schedule_blocks, players
    ) == uut.get_std_of_all_possible_matches(schedule_even, players)
    assert uut.get_std_of_pause_between_matches(
        schedule_blocks, players
    ) > uut.get_std_of_pause_between_matches(schedule_even, players)
    assert uut.get_std_of_pause_between_playing(
        schedule_blocks, players
    ) > uut.get_std_of_pause_between_playing(schedule_even, players)


def test_schedule_even_is_worse_than_balanced(balenced_to_weight, schedule_even, players):
    uut = ScoringAlgorithm()
    assert uut.get_score(balenced_to_weight, players) < uut.get_score(schedule_even, players)
    assert uut.get_std_of_player_times_playing(
        balenced_to_weight, players
    ) < uut.get_std_of_player_times_playing(schedule_even, players)
    assert uut.get_std_of_all_possible_matches(
        balenced_to_weight, players
    ) < uut.get_std_of_all_possible_matches(schedule_even, players)
    assert uut.get_std_of_pause_between_matches(
        balenced_to_weight, players
    ) > uut.get_std_of_pause_between_matches(schedule_even, players)
    assert uut.get_std_of_pause_between_playing(
        balenced_to_weight, players
    ) < uut.get_std_of_pause_between_playing(schedule_even, players)
