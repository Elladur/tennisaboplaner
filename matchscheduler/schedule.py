# """a schedule class consisting of a list of rounds
# a schedule is valid if all rounds are valid"""

from line_profiler import profile

from .match import Match, get_players_of_match


@profile
def get_match_indizes_of_player(
    schedule: list[list[Match]], player_index: int
) -> list[tuple[int, int]]:
    return [
        (round_index, match_index)
        for round_index, round in enumerate(schedule)
        for match_index, match in enumerate(round)
        if player_index in get_players_of_match(match)
    ]


@profile
def get_match_indizes_of_match(
    schedule: list[list[Match]], arg_match: Match
) -> list[tuple[int, int]]:
    return [
        (round_index, match_index)
        for round_index, round in enumerate(schedule)
        for match_index, match in enumerate(round)
        if match == arg_match
    ]
