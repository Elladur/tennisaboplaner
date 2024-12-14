from datetime import date

from matchscheduler.player import Player


def test_init():
    name = "Max"
    cant_play = ["2024-01-01", "2025-01-12"]
    weight = 2
    x = Player(name, cant_play, weight)

    assert x.name == name
    assert x.weight == weight
    for y in cant_play:
        assert date.fromisoformat(y) in x.cannot_play


def test_to_dict():
    name = "Max"
    cant_play = ["2024-01-01", "2025-01-12"]
    weight = 2
    x = Player(name, cant_play, weight)

    expected = {"name": name, "cannot_play": cant_play, "weight": weight}
    assert x.to_dict() == expected


def test_from_dict():
    name = "Max"
    cant_play = ["2024-01-01", "2025-01-12"]
    weight = 2
    data_dict = {"name": name, "cannot_play": cant_play, "weight": weight}

    expected = Player(name, cant_play, weight)
    result = Player.from_dict(data_dict)

    assert result.name == expected.name
    assert result.weight == expected.weight
    assert result.cannot_play == expected.cannot_play


def test_to_str():
    name = "Max"
    cant_play = ["2024-01-01", "2025-01-12"]
    weight = 2
    x = Player(name, cant_play, weight)

    assert str(x) == name
