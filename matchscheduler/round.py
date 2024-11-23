"""A round of a season consisting of a list of matches."""

from datetime import date

from .match import Match, MatchFactory, NotValidMatchError, convert_match_to_string
from .player import Player

def create_round(**matches:int):
    return [m for m in matches]

def convert_round_to_string(round: list[int], players: list[Player]):
    "\n".join([convert_match_to_string(m, players) for m in round])