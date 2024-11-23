"""Match class and factory for generating valid matches."""
from .player import Player



def create_match(player_id1, player_id2) -> int:
    return 1 << player_id1 + 1 << player_id2

def convert_match_to_string(match: int, players: list[Player]):
    names = [players[i] for i in range(len(players)) if (match >> i) & 1]
    return f"{names[0]} vs {names[1]}"
