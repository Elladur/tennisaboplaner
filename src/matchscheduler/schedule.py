# """a schedule class consisting of a list of rounds
# a schedule is valid if all rounds are valid"""

from copy import copy
from datetime import date

from line_profiler import profile

from .match import Match
from .player import Player
from .round import Round


class Schedule:
    def __init__(self, rounds: list[Round]):
        self.rounds = rounds

    @profile
    def get_match_indizes_of_player(self, player: Player) -> list[tuple[int, int]]:
        return [
            (round_index, match_index)
            for round_index, round in enumerate(self.rounds)
            for match_index, match in enumerate(round.matches)
            if player == match.player1 or player == match.player2
        ]

    @profile
    def get_match_indizes_of_match(self, arg_match: Match) -> list[tuple[int, int]]:
        return [
            (round_index, match_index)
            for round_index, round in enumerate(self.rounds)
            for match_index, match in enumerate(round.matches)
            if match == arg_match
        ]

    @profile
    def change_match(self, round_index: int, match_index: int, match: Match) -> bool:
        return self.rounds[round_index].replace_match(match_index, match)

    @profile
    def swap_players_of_existing_matches(self, round_index: int, p: Player, q: Player) -> bool:
        return self.rounds[round_index].swap_players(p, q)

    @profile
    def switch_matches(self, round1: int, match1: int, round2: int, match2: int) -> bool:
        if self.rounds[round1].is_partial or self.rounds[round2].is_partial:
            return False
        old_match1 = copy(self.rounds[round1].matches[match1])
        old_match2 = copy(self.rounds[round2].matches[match2])

        swapped1 = self.rounds[round1].replace_match(match1, old_match2)
        if swapped1:
            swapped2 = self.rounds[round2].replace_match(match2, old_match1)
            if swapped2:
                return True
            self.rounds[round1].replace_match(match1, old_match1)
            return False
        return False

    def to_dict(self) -> dict:
        return {"rounds": [r.to_dict() for r in self.rounds]}

    @classmethod
    def from_dict(cls, data: dict, number_of_courts: int, players: list[Player]) -> "Schedule":
        rounds = [Round.from_dict(r, number_of_courts, players) for r in data["rounds"]]
        return cls(rounds)

    @classmethod
    def create(cls, players: list[Player], days: list[date], number_of_courts: int) -> "Schedule":
        rounds = []
        for d in days:
            rounds.append(Round.create(players, d, number_of_courts))
        return cls(rounds)
