"""A round of a season consisting of a list of matches."""

import itertools
from datetime import date
from random import shuffle
from typing import Generator

from .match import Match, can_match_be_added
from .player import Player


class Round:
    def __init__(self, matches: list[Match], day: date, number_of_courts: int):
        if any(day in p.cannot_play for m in matches for p in m.get_players()):
            raise ValueError("not all players can play on this date")
        self.matches = matches
        self.is_partial = len([p for p in self.get_players()]) != 2 * number_of_courts
        self.day = day

    def get_players(self) -> Generator[Player, None, None]:
        return (p for m in self.matches for p in m.get_players())

    def get_players_of_round_except_match(self, match_index: int) -> Generator[Player, None, None]:
        return (p for i, m in enumerate(self.matches) for p in m.get_players() if i != match_index)

    def replace_match(self, match_index: int, new_match: Match) -> bool:
        if self.is_partial:
            return False
        if any(self.day in p.cannot_play for p in new_match.get_players()):
            return False
        player_of_other_matches = list(self.get_players_of_round_except_match(match_index))
        if any(p in player_of_other_matches for p in new_match.get_players()):
            return False
        self.matches[match_index] = new_match
        return True

    def swap_players(self, p: Player, q: Player) -> bool:
        p_match = next(filter(lambda x: p in x.get_players(), self.matches), None)
        q_match = next(filter(lambda x: q in x.get_players(), self.matches), None)
        if p_match is None or q_match is None or p_match == q_match:
            return False
        p_match.replace_player(p, q)
        q_match.replace_player(q, p)
        return True

    def to_dict(self) -> dict:
        return {"day": str(self.day), "matches": [m.to_dict() for m in self.matches]}

    @classmethod
    def from_dict(cls, data: dict, number_of_courts: int, players: list[Player]) -> "Round":
        day = date.fromisoformat(data["day"])
        matches = [Match.from_dict(m, players) for m in data["matches"]]
        return cls(matches, day, number_of_courts)

    @classmethod
    def create(cls, players: list[Player], day: date, number_of_courts: int) -> "Round":
        matches: list[Match] = []
        possible_players = [p for p in players if day not in p.cannot_play]
        shuffle(possible_players)
        for p, q in itertools.combinations(possible_players, 2):
            m = Match(p, q)
            if can_match_be_added(matches, m):
                matches.append(m)
                if len(matches) == number_of_courts:
                    return cls(matches, day, number_of_courts)
        # partial round ...
        missing_player = [
            p for p in possible_players if not any(p in m.get_players() for m in matches)
        ]
        if len(missing_player) == 1:
            matches.append(Match(missing_player[0], None))
            return cls(matches, day, number_of_courts)
        elif len(missing_player) == 0:
            return cls(matches, day, number_of_courts)
        raise Exception("something went wrong ...")
