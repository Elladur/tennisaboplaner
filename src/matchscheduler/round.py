"""A round of a season consisting of a list of matches."""

from line_profiler import profile

from .match import Match, can_match_be_added
from datetime import date
from .player import Player
import itertools


class Round:
    def __init__(self, matches: list[Match], day:date, number_of_courts: int):
        if any(day in p.cannot_play for m in matches for p in m.players):
            raise ValueError("not all players can play on this date")
        self.matches = matches
        self.partial_round =  (len(matches) < number_of_courts)
        self.day = day

    @profile
    def get_players_of_round(self) -> set[Player]:
        players = []
        for m in self.matches:
            players += list(m.players)
        return set(players)


    @classmethod
    def create(cls, players: list[Player], day: date, number_of_courts: int) -> "Round":
        matches = []
        possible_players = [p for p in players if day not in p.cannot_play]
        for p, q in itertools.combinations(possible_players):
            m = Match(p, q)
            if can_match_be_added(matches, m):
                matches.append(m)
                if len(matches) == number_of_courts:
                    return cls(matches, day, number_of_courts)
        # partial round ...
        missing_player = [p for p in players if not any(p in m.players for m in matches)]
        if len(missing_player) == 1:
            matches.append(Match(missing_player[0], None))
            return cls(matches, day, number_of_courts)
        raise Exception("something went wrong ...")