# """a schedule class consisting of a list of rounds
# a schedule is valid if all rounds are valid"""

from line_profiler import profile

from .match import Match, get_players_of_match
from .round import Round
from .player import Player
from datetime import date

class Schedule:
    def __init__(self, rounds: list[Round]):
        self.rounds = rounds


    @profile
    def get_match_indizes_of_player(
        self, player: Player
    ) -> list[tuple[int, int]]:
        return [
            (round_index, match_index)
            for round_index, round in enumerate(self.rounds)
            for match_index, match in enumerate(round.matches)
            if player in match.players
        ]


    @profile
    def get_match_indizes_of_match(
        self, arg_match: Match
    ) -> list[tuple[int, int]]:
        return [
            (round_index, match_index)
            for round_index, round in enumerate(self.rounds)
            for match_index, match in enumerate(round.matches)
            if match == arg_match
        ]

    @classmethod
    def create(cls, players: list[Player], days: list[date], number_of_courts: int) -> "Schedule":
        rounds = []
        for d in days:
            rounds.append(Round.create(players, d, number_of_courts))
        return cls(rounds)
