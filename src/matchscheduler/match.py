"""Match class and factory for generating valid matches."""

from typing import Tuple

from line_profiler import profile

from .player import Player

Match = Tuple[int, int]


@profile
def create_match(player_id1: int, player_id2: int) -> Match:
    # always use smaller int in beginning
    if player_id1 < player_id2:
        return (player_id1, player_id2)
    return (player_id2, player_id1)


@profile
def can_match_be_added(rounds: list[Match], match: Match) -> bool:
    return not any(p in r for p in match for r in rounds)


@profile
def get_players_of_match(match: Match) -> Match:
    return match


def convert_match_to_string(match: Match, players: list[Player]) -> str:
    return f"{players[match[0]]} vs {players[match[1]]}"
