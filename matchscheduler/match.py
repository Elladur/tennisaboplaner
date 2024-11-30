"""Match class and factory for generating valid matches."""
from .player import Player
from line_profiler import profile


 
@profile
def create_match(player_id1, player_id2) -> int:
    return (1 << player_id1) + (1 << player_id2)

@profile
def can_match_be_added(rounds: list[int], match: int) -> bool:
    return not any([r & match != 0 for r in rounds])
    #for r in rounds:
        #if r & match != 0:
            #return False
    #return True

@profile
def get_players_of_match(match: int) -> list[int]:
    return [i for i, bit in enumerate(bin(match)[:1:-1]) if bit == '1']
    #positions = []
    #position = 0
    #while match > 0:
        #if match & 1:
            #positions.append(position)
        #match >>= 1
        #position += 1
    #return positions

def convert_match_to_string(match: int, players: list[Player]):
    names = [players[i] for i in range(len(players)) if (match >> i) & 1]
    return f"{names[0]} vs {names[1]}"
