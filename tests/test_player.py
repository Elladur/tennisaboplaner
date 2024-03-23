from datetime import date

import pytest

from matchscheduler.player import Player


@pytest.mark.parametrize("name, date_input", [("John", "2021-01-01"), ("Jane", "2021-01-02")])
def test_player(name, date_input):
    player = Player(name, [date_input])
    assert player.name == name
    assert player.cannot_play == [date.fromisoformat(date_input)]


@pytest.mark.parametrize(
    "dict_player",
    [
        {"name": "John", "cannot_play": ["2021-01-01", "2021-01-02"]},
        {"name": "Jane", "cannot_play": ["2021-01-02"]},
    ],
)
def test_from_dict(dict_player):
    player = Player.from_dict(dict_player)
    assert player.name == dict_player["name"]
    assert player.cannot_play == [date.fromisoformat(i) for i in dict_player["cannot_play"]]


def test_set_to_tuple_works():
    player1 = Player("John", ["2021-01-01"])
    player2 = Player("Jane", ["2021-01-02"])
    result = Player.set_to_tuple({player1, player2})
    for player in result:
        assert player in {player1, player2}


def test_set_to_tuple_raises_error_if_not_two_players():
    player1 = Player("John", ["2021-01-01"])
    with pytest.raises(ValueError):
        Player.set_to_tuple({player1})
