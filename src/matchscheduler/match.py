"""Match class and factory for generating valid matches."""

from typing import Generator

from line_profiler import profile
from .player import Player


class Match:
    def __init__(self, player1: Player, player2: Player | None):
        if player1 == player2:
            raise ValueError("players need to be different.")
        if player2 is None:
            self.player1 = player1
            self.player2 = None
        else:
            self.player1, self.player2 = sorted((player1, player2), key=lambda x: x.name)

    def __str__(self):
        second_name = self.player2.name if self.player2 is not None else "..."
        return f"{self.player1.name} vs {second_name}"

    def __hash__(self):
        return hash(str(self))

    @profile
    def get_players(self) -> Generator[Player, None, None]:
        yield self.player1
        if self.player2 is not None:
            yield self.player2

    @profile
    def replace_player(self, old_player: Player, new_player: Player) -> bool:
        if self.player1 == old_player and self.player2 != new_player:
            self.player1 = new_player
            if self.player2 is not None and self.player1.name > self.player2.name:
                self.player1, self.player2 = self.player2, self.player1
            return True
        if self.player2 == old_player and self.player1 != new_player:
            self.player2 = new_player
            if self.player1.name > self.player2.name:
                self.player1, self.player2 = self.player2, self.player1
            return True
        return False

    def __eq__(self, value: object) -> bool:
        if isinstance(value, Match):
            return self.player1 == value.player1 and self.player2 == value.player2
        return False

    def to_dict(self) -> tuple[str, str | None]:
        return (self.player1.name, self.player2.name if self.player2 is not None else None)

    @classmethod
    def from_dict(cls, match: tuple[str, str], players: list[Player]) -> "Match":
        player1_name, player2_name = match
        player1 = next(filter(lambda x: x.name == player1_name, players))
        try:
            player2 = next(filter(lambda x: x.name == player2_name, players))
        except StopIteration:
            player2 = None
        return cls(player1, player2)


@profile
def can_match_be_added(rounds: list[Match], match: Match) -> bool:
    return not any(p in r.get_players() for p in match.get_players() for r in rounds)
