"""Match class and factory for generating valid matches."""

from typing import Tuple

from line_profiler import profile

from .player import Player

Match = Tuple[int, int | None]


@profile
def create_match(player_id1: int, player_id2: int | None) -> Match:
    # always use smaller int in beginning
    if player_id2 is None:
        return (player_id1, None)
    if player_id1 == player_id2:
        raise ValueError("Player Ids cannot be the same in a match.")
    if player_id1 < player_id2:
        return (player_id1, player_id2)
    return (player_id2, player_id1)


@profile
def can_match_be_added(rounds: list[Match], match: Match) -> bool:
    return not any(p in r for p in match for r in rounds)


@profile
def get_players_of_match(match: Match) -> list[int]:
    return [x for x in match if x is not None]


def convert_match_to_string(match: Match, players: list[Player]) -> str:
    if match[1] is not None:
        return f"{players[match[0]]} vs {players[match[1]]}"
    return f"{players[match[0]]} vs ..."


def replace_player_in_match(match: Match, old_player: int, new_player: int) -> Tuple[Match, bool]:
    if old_player in get_players_of_match(match):
        other_player = match[0] if match[0] != old_player else match[1]
        return create_match(new_player, other_player), True
    return match, False
