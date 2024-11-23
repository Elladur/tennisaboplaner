"""a schedule class consisting of a list of rounds
a schedule is valid if all rounds are valid"""

from datetime import date

from .match import Match
from .player import Player
from .round import NotValidRoundError, NotValidSwapError, Round, RoundFactory


class Schedule:
    """A schedule of rounds."""

    def __init__(self, rounds: list[Round], players: set[Player]) -> None:
        self.rounds = rounds
        self.players = players

    def to_dict(self) -> dict:
        return {
            "rounds": [r.to_dict() for r in self.rounds],
            "players": [p.to_dict() for p in self.players],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Schedule":
        rounds = []
        players = set()
        for x in data["rounds"]:
            rounds.append(Round.from_dict(x))
        for x in data["players"]:
            players.add(Player.from_dict(x))
        return cls(rounds, players)

    def is_valid(self) -> bool:
        """Check if this schedule is valid."""
        for r in self.rounds:
            if not r.is_valid():
                return False
        return True

    def get_matches(self) -> list[Match]:
        """Get a list of all matches in this schedule."""
        return [m for r in self.rounds for m in r.matches]

    def get_matches_of_player(self, player: Player) -> list[Match]:
        """Get a list of all matches in this schedule with the given player."""
        return [m for m in self.get_matches() if player in m.players]

    def get_matches_of_players(self, players: set[Player]) -> list[Match]:
        """Get a list of all matches in this schedule with the given player."""
        return [m for m in self.get_matches() if players == m.players]

    def swap_matches(
        self, round_index1: int, match_index1: int, round_index2: int, match_index2: int
    ) -> None:
        """Swap the matches in the given rounds and match indices."""
        round1 = self.rounds[round_index1]
        round2 = self.rounds[round_index2]
        match1 = round1.matches[match_index1]
        match2 = round2.matches[match_index2]
        try:
            round1.swap_players(match_index1, match2.players)
            round2.swap_players(match_index2, match1.players)
        except NotValidSwapError as exc:
            # revert swap
            round1.swap_players(match_index1, match1.players)
            round2.swap_players(match_index2, match2.players)
            # reraise error
            raise exc
        if not self.is_valid():
            raise NotValidScheduleError("Swap is not valid.")


class NotValidScheduleError(Exception):
    """Raised when a schedule is not valid."""


class ScheduleFactory:
    """A factory for schedules."""

    @staticmethod
    def generate_valid_schedule(
        players: set[Player], dates: list[date], num_courts: int
    ) -> Schedule:
        """Generate a valid schedule for the given players and dates."""
        rounds = []
        for d in dates:
            try:
                rounds.append(RoundFactory.generate_valid_round(players, d, num_courts))
            except NotValidRoundError as exc:
                raise NotValidScheduleError("Could not generate a valid schedule.") from exc

        s = Schedule(rounds, players)
        if s.is_valid():
            return s
        raise NotValidScheduleError("Could not generate a valid schedule.")
