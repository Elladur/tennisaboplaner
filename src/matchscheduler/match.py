"""Match class and factory for generating valid matches."""

from typing import Tuple

from line_profiler import profile
from datetime import date

from .player import Player

class Match:
    def __init__(self, player1: Player, player2: Player|None):
        if player1 == player2:
            raise ValueError("players need to be different.")
        self.players = (player1, player2) 

    def __str__(self):
        names = sorted(p.name for p in self.players)
        return f"{names[0]} vs {names[1]}"

    def replace_player(self, old_player: Player, new_player: Player) -> bool:
        if old_player in self.players:
            other_player = self.players[0] if self.players[0] != old_player else self.players[1]
            self.players = (new_player, other_player)
            return True
        return False

    def __eq__(self, value: "Match") -> bool:
        return self.players == value.players or (self.players[0] == value.players[1] and self.players[1] == value.players[0])

@profile
def can_match_be_added(rounds: list[Match], match: Match) -> bool:
    return not any(p in r for p in match for r in rounds)
