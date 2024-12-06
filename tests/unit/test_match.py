from matchscheduler import match
import pytest
from matchscheduler import player

@pytest.mark.parametrize("player1, player2, expected_result", [
    (1, 2, (1,2)),
    (3, 2, (2,3)),
])
def test_create_match(player1, player2, expected_result):
    assert expected_result == match.create_match(player1, player2)


def test_create_match_errors_with_same_ids():
    with pytest.raises(ValueError):
        match.create_match(1,1)

@pytest.mark.parametrize("new_match, existing_matches, expected_value", [
    ((1,2), [(3, 4), (5, 6)], True),
    ((10,100), [(3, 4), (5, 6)],True),
    ((3,100), [(3, 4), (5, 6)], False),
])
def test_match_be_added_works_correctly(new_match, existing_matches, expected_value):
    assert match.can_match_be_added(existing_matches, new_match) == expected_value


@pytest.mark.parametrize("arg_match", [
    (1,1), (2, 3)
])
def test_get_players_of_match(arg_match):
    assert arg_match == match.get_players_of_match(arg_match)


@pytest.mark.parametrize("arg_match, players", [
    ((0, 1), [player.Player("Max", []), player.Player("Moritz", [])])
])
def test_convert_match_to_string(arg_match, players):
    result = match.convert_match_to_string(arg_match, players)
    assert result.find(players[arg_match[0]].name) != -1
    assert result.find(players[arg_match[1]].name) != -1