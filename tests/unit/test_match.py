from matchscheduler import match
import pytest

@pytest.mark.parametrize("player1, player2, expected_result", [
    (1, 2, (1,2)),
    (3, 2, (2,3)),
])
def test_create_match(player1, player2, expected_result):
    assert expected_result == match.create_match(player1, player2)


def test_create_match_errors_with_same_ids():
    with pytest.raises(ValueError):
        match.create_match(1,1)
