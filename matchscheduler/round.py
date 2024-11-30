"""A round of a season consisting of a list of matches."""

from line_profiler import profile

from .match import Match, convert_match_to_string, get_players_of_match
from .player import Player


@profile
def get_players_of_round(round: list[Match]) -> set[int]:
    players = []
    for m in round:
        players += list(get_players_of_match(m))
    return set(players)


def convert_round_to_string(round: list[int], players: list[Player]):
    "\n".join([convert_match_to_string(m, players) for m in round])
