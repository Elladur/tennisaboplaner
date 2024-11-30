"""A round of a season consisting of a list of matches."""

from line_profiler import profile

from .match import Match, get_players_of_match


@profile
def get_players_of_round(round: list[Match]) -> set[int]:
    players = []
    for m in round:
        players += list(get_players_of_match(m))
    return set(players)
