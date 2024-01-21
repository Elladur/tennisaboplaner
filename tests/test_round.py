import pytest
from datetime import date
from matchscheduler.match import Match
from matchscheduler.player import Player
from matchscheduler.round import Round, RoundFactory, NotValidSwapError


@pytest.mark.parametrize(
    "matches, round_date, num_matches",
    [
        (
            [
                Match(
                    (Player("John", ["2021-01-01"]), Player("Jane", ["2021-01-02"])),
                    date.fromisoformat("2021-01-03"),
                ),
                Match(
                    (Player("Bob", ["2021-01-04"]), Player("Alice", ["2021-01-05"])),
                    date.fromisoformat("2021-01-06"),
                ),
            ],
            date.fromisoformat("2021-01-07"),
            2,
        )
    ],
)
def test_init(matches, round_date, num_matches):
    r = Round(matches, round_date, num_matches)
    assert r.matches == matches
    assert r.num_matches == num_matches
    assert r.date == round_date


def test_is_valid_if_date_is_no_problem():
    r = Round(
        [
            Match(
                (Player("John", ["2021-01-01"]), Player("Jane", ["2021-01-02"])),
                date.fromisoformat("2021-01-07"),
            ),
            Match(
                (Player("Bob", ["2021-01-04"]), Player("Alice", ["2021-01-05"])),
                date.fromisoformat("2021-01-07"),
            ),
        ],
        date.fromisoformat("2021-01-07"),
        2,
    )
    assert r.is_valid()


def test_is_valid_returns_false_if_date_is_a_problem():
    r = Round(
        [
            Match(
                (Player("John", ["2021-01-01"]), Player("Jane", ["2021-01-02"])),
                date.fromisoformat("2021-01-03"),
            ),
            Match(
                (Player("Bob", ["2021-01-04"]), Player("Alice", ["2021-01-05"])),
                date.fromisoformat("2021-01-06"),
            ),
        ],
        date.fromisoformat("2021-01-06"),
        2,
    )
    assert not r.is_valid()


def test_is_valid_returns_false_if_player_is_in_two_matches():
    r = Round(
        [
            Match(
                (Player("John", ["2021-01-01"]), Player("Jane", ["2021-01-02"])),
                date.fromisoformat("2021-01-03"),
            ),
            Match(
                (Player("John", ["2021-01-01"]), Player("Alice", ["2021-01-05"])),
                date.fromisoformat("2021-01-03"),
            ),
        ],
        date.fromisoformat("2021-01-06"),
        2,
    )
    assert not r.is_valid()


def test_generate_valid_round_is_valid():
    players = [
        Player("John", ["2021-01-01", "2021-01-03"]),
        Player("Jane", ["2021-01-02", "2021-01-04"]),
        Player("Bob", ["2021-01-05", "2021-01-06"]),
        Player("Alice", ["2021-01-07", "2021-01-08"]),
    ]
    r = RoundFactory.generate_valid_round(players, date.fromisoformat("2021-01-09"), 2)
    assert r.is_valid()


def test_generate_valid_round_raises_exception_if_it_cant_find_any():
    players = [
        Player("John", ["2021-01-01", "2021-01-03"]),
        Player("Jane", ["2021-01-02", "2021-01-04"]),
        Player("Bob", ["2021-01-05", "2021-01-06"]),
        Player("Alice", ["2021-01-07", "2021-01-08"]),
    ]
    with pytest.raises(Exception):
        RoundFactory.generate_valid_round(players, date.fromisoformat("2021-01-09"), 3)


def test_generate_valid_round_has_excactly_given_amount_of_matches():
    players = [
        Player("John", ["2021-01-01", "2021-01-03"]),
        Player("Jane", ["2021-01-02", "2021-01-04"]),
        Player("Bob", ["2021-01-05", "2021-01-06"]),
        Player("Alice", ["2021-01-07", "2021-01-08"]),
    ]
    r = RoundFactory.generate_valid_round(players, date.fromisoformat("2021-01-09"), 2)
    assert len(r.matches) == 2


def test_generate_valid_round_date_and_number_of_courts_are_same_as_input():
    players = [
        Player("John", ["2021-01-01", "2021-01-03"]),
        Player("Jane", ["2021-01-02", "2021-01-04"]),
        Player("Bob", ["2021-01-05", "2021-01-06"]),
        Player("Alice", ["2021-01-07", "2021-01-08"]),
    ]
    r = RoundFactory.generate_valid_round(players, date.fromisoformat("2021-01-09"), 2)
    assert r.date == date.fromisoformat("2021-01-09")
    assert r.num_matches == 2


def test_swap_players_returns_new_players():
    players = [
        Player("Bob", ["2021-01-05", "2021-01-06"]),
        Player("Alice", ["2021-01-07", "2021-01-08"]),
    ]
    r = RoundFactory.generate_valid_round(players, date.fromisoformat("2021-01-09"), 1)
    r.swap_players(
        0,
        {
            Player("John", ["2021-01-01", "2021-01-03"]),
            Player("Jane", ["2021-01-02", "2021-01-04"]),
        },
    )
    new_match = r.matches[0]
    assert new_match.date == date.fromisoformat("2021-01-09")
    assert {c.name for c in new_match.players} == {"Jane", "John"}


def test_swap_players_raises_exception_if_match_is_not_valid():
    players = [
        Player("John", ["2021-01-01", "2021-01-03"]),
        Player("Jane", ["2021-01-02", "2021-01-04"]),
        Player("Bob", ["2021-01-05", "2021-01-06"]),
        Player("Alice", ["2021-01-07", "2021-01-08"]),
    ]
    r = RoundFactory.generate_valid_round(players, date.fromisoformat("2021-01-03"), 1)
    with pytest.raises(NotValidSwapError, match="Match is not valid."):
        r.swap_players(
            0,
            {
                players[0],
                players[2],  # john vs bob
            },
        )


def test_swap_players_raises_exception_if_round_is_not_valid():
    players = [
        Player("John", ["2021-01-01", "2021-01-03"]),
        Player("Jane", ["2021-01-02", "2021-01-04"]),
        Player("Bob", ["2021-01-05", "2021-01-06"]),
        Player("Alice", ["2021-01-07", "2021-01-08"]),
    ]
    # define a round where john plays against jane and bob against alice
    date_of_play = date.fromisoformat("2021-01-10")
    r = Round(
        [
            Match(
                (players[0], players[1]),  # john vs jane
                date_of_play,
            ),
            Match(
                (players[2], players[3]),  # bob vs alice
                date_of_play,
            ),
        ],
        date_of_play,
        2,
    )

    with pytest.raises(NotValidSwapError, match="Swap is not valid."):
        r.swap_players(
            0,
            {players[0], players[2]},  # john vs bob
        )


def test_swap_players_of_existing_matches_returns_new_matches():
    players = [
        Player("John", ["2021-01-01", "2021-01-03"]),
        Player("Jane", ["2021-01-02", "2021-01-04"]),
        Player("Bob", ["2021-01-05", "2021-01-06"]),
        Player("Alice", ["2021-01-07", "2021-01-08"]),
    ]
    # define a round where john plays against jane and bob against alice
    date_of_play = date.fromisoformat("2021-01-10")
    r = Round(
        [
            Match(
                {players[0], players[1]},  # john vs jane
                date_of_play,
            ),
            Match(
                {players[2], players[3]},  # bob vs alice
                date_of_play,
            ),
        ],
        date_of_play,
        2,
    )

    r.swap_players_of_existing_matches(0, 1, {players[0], players[2]})  # john and bob
    new_matches = r.matches
    assert len(new_matches) == 2
    assert new_matches[0].date == date_of_play
    assert new_matches[1].date == date_of_play
    assert {c.name for c in new_matches[0].players} == {"Bob", "Jane"}
    assert {c.name for c in new_matches[1].players} == {"John", "Alice"}
    assert r.is_valid()


def test_swap_players_of_existing_matches_returns_error_if_players_are_in_same_match():
    players = [
        Player("John", ["2021-01-01", "2021-01-03"]),
        Player("Jane", ["2021-01-02", "2021-01-04"]),
        Player("Bob", ["2021-01-05", "2021-01-06"]),
        Player("Alice", ["2021-01-07", "2021-01-08"]),
    ]
    # define a round where john plays against jane and bob against alice
    date_of_play = date.fromisoformat("2021-01-10")
    r = Round(
        [
            Match(
                {players[0], players[1]},  # john vs jane
                date_of_play,
            ),
            Match(
                {players[2], players[3]},  # bob vs alice
                date_of_play,
            ),
        ],
        date_of_play,
        2,
    )

    with pytest.raises(NotValidSwapError, match="Swap is not valid."):
        r.swap_players_of_existing_matches(
            0, 1, {players[0], players[1]}
        )  # john and jane


def test_swap_players_of_existing_match_retunrs_error_if_players_are_not_already_playing():
    players = [
        Player("John", ["2021-01-01", "2021-01-03"]),
        Player("Jane", ["2021-01-02", "2021-01-04"]),
        Player("Bob", ["2021-01-05", "2021-01-06"]),
        Player("Alice", ["2021-01-07", "2021-01-08"]),
        Player("NewOne", ["2021-01-07", "2021-01-08"]),
    ]
    # define a round where john plays against jane and bob against alice
    date_of_play = date.fromisoformat("2021-01-10")
    r = Round(
        [
            Match(
                {players[0], players[1]},  # john vs jane
                date_of_play,
            ),
            Match(
                {players[2], players[3]},  # bob vs alice
                date_of_play,
            ),
        ],
        date_of_play,
        2,
    )

    with pytest.raises(NotValidSwapError, match="Swap is not valid."):
        r.swap_players_of_existing_matches(0, 1, {players[0], players[4]})


def test_swap_players_of_existing_matches_returns_error_if_index_of_matches_is_out_of_range():
    players = [
        Player("John", ["2021-01-01", "2021-01-03"]),
        Player("Jane", ["2021-01-02", "2021-01-04"]),
        Player("Bob", ["2021-01-05", "2021-01-06"]),
        Player("Alice", ["2021-01-07", "2021-01-08"]),
    ]
    # define a round where john plays against jane and bob against alice
    date_of_play = date.fromisoformat("2021-01-10")
    r = Round(
        [
            Match(
                {players[0], players[1]},  # john vs jane
                date_of_play,
            ),
            Match(
                {players[2], players[3]},  # bob vs alice
                date_of_play,
            ),
        ],
        date_of_play,
        2,
    )

    with pytest.raises(IndexError):
        r.swap_players_of_existing_matches(0, 2, {players[0], players[4]})



@pytest.mark.parametrize(
    "matches, round_date, num_matches, expected_result",
    [
        (
            [
                Match(
                    (Player("John", ["2021-01-01"]), Player("Jane", ["2021-01-02"])),
                    date.fromisoformat("2021-01-03"),
                ),
                Match(
                    (Player("Bob", ["2021-01-04"]), Player("Alice", ["2021-01-05"])),
                    date.fromisoformat("2021-01-06"),
                ),
            ],
            date.fromisoformat("2021-01-07"),
            2,
            {
                Player("John", ["2021-01-01"]), Player("Jane", ["2021-01-02"]), 
                Player("Bob", ["2021-01-04"]), Player("Alice", ["2021-01-05"])
            }
        )
    ],
)
def test_get_players(matches, round_date, num_matches, expected_result):
    r = Round(matches, round_date, num_matches)

    result = r.get_players()
    assert result == expected_result
