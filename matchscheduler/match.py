"""Match class and factory for generating valid matches."""

from datetime import date
from itertools import combinations
from typing import Generator

from .player import Player


class Match:
    """A match between two players on a given date."""

    def __init__(self, players: set[Player], date_of_play: date):
        for player in players:
            if date_of_play in player.cannot_play:
                raise NotValidMatchError(f"Player {player.name} cannot play on {date_of_play}.")
        # only two players per match
        if len(set(players)) != 2:
            raise NotValidMatchError("A match must have two players.")

        self.players = players
        self.date = date_of_play

    def to_dict(self) -> dict:
        return {"players": [p.to_dict() for p in self.players], "date": str(self.date)}

    @classmethod
    def from_dict(cls, data: dict) -> "Match":
        players = set()
        for x in data["players"]:
            players.add(Player.from_dict(x))
        return cls(players, date.fromisoformat(data["date"]))

    def __str__(self) -> str:
        names = sorted([p.name for p in self.players])
        return f"{names[0]} vs {names[1]}"


class NotValidMatchError(Exception):
    """Raised when a match is not valid."""


class MatchFactory:
    """A factory for matches."""

    @staticmethod
    def generate_valid_new_match(
        players: set[Player], d: date, matches: list[Match]
    ) -> Generator[Match, None, None]:
        """Generate a valid match for the given players and date."""
        # try random generations of players till we have a valid match
        # if we can't find a valid match, raise an exception
        # if we can find a valid match, return it
        for p, q in combinations(players, 2):
            try:
                m = Match({p, q}, d)
                if m in matches:
                    continue
                yield m
            except NotValidMatchError:
                continue
