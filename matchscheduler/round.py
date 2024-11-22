"""A round of a season consisting of a list of matches."""

from datetime import date

from .match import Match, MatchFactory, NotValidMatchError
from .player import Player


class Round:
    """A round of a season consisting of a list of matches."""

    def __init__(self, matches: list[Match], date_of_round: date, num_matches: int):
        self.matches = matches
        self.num_matches = num_matches
        self.date = date_of_round

    def to_dict(self) -> dict:
        return {"matches": [m.to_dict() for m in self.matches], "date": str(self.date)}

    @classmethod
    def from_dict(cls, data: dict) -> "Round":
        matches = []
        for x in data["matches"]:
            matches.append(Match.from_dict(x))
        date_of_round = date.fromisoformat(data["date"])
        return cls(matches, date_of_round, len(matches))

    def is_valid(self) -> bool:
        """Check if this round is valid."""
        if len(self.matches) != self.num_matches:
            return False
        # every player can only play in one match,
        # it should return false if any player is in more than one match
        players_in_this_round = []
        for match in self.matches:
            for player in match.players:
                if player in players_in_this_round:
                    return False
                players_in_this_round.append(player)

        # every match has to have the same date as the round
        for match in self.matches:
            if match.date != self.date:
                return False
        return True

    def swap_players(self, match_index: int, players: set[Player]) -> None:
        """Swap the players in the given match with the given players."""
        new_match = None
        current_match = self.matches[match_index]
        try:
            new_match = Match(players, self.matches[match_index].date)
            self.matches[match_index] = new_match
        except NotValidMatchError as exc:
            raise NotValidSwapError("Swap is not valid, because Match is not valid.") from exc
        if not self.is_valid():
            self.matches[match_index] = current_match
            raise NotValidSwapError("Swap is not valid.")

    def swap_players_of_existing_matches(
        self, match_index1: int, match_index2: int, players_to_swap: set[Player]
    ) -> None:
        """Swap the players in the given matches."""
        new_match1 = None
        new_match2 = None
        current_match1 = self.matches[match_index1]
        current_match2 = self.matches[match_index2]
        try:
            new_match1 = Match(
                current_match1.players.symmetric_difference(players_to_swap), self.date
            )
            new_match2 = Match(
                current_match2.players.symmetric_difference(players_to_swap), self.date
            )
            self.matches[match_index1] = new_match1
            self.matches[match_index2] = new_match2
        except NotValidMatchError as exc:
            raise NotValidSwapError("Swap is not valid, because Match is not valid.") from exc
        if not self.is_valid():
            self.matches[match_index1] = current_match1
            self.matches[match_index2] = current_match2
            raise NotValidSwapError("Swap is not valid.")

    def export_match_string(self) -> str:
        """Export the matches of this round as a string."""
        return "\n".join([str(match) for match in self.matches])

    def get_players(self) -> set[Player]:
        """Get the players in this round."""
        players: set[Player] = {p for m in self.matches for p in m.players}
        return players


class NotValidRoundError(Exception):
    """Raised when a round is not valid."""


class NotValidSwapError(Exception):
    """Raised when a swap is not valid."""


class RoundFactory:
    """A factory for generating rounds."""

    @staticmethod
    def generate_valid_round(players: set[Player], date_of_play: date, num_courts: int) -> Round:
        """Generate a valid round for the given players and date."""
        matches: list[Match] = []
        for i in range(num_courts):
            for match in MatchFactory.generate_valid_new_match(players, date_of_play, matches):
                new_proposed_round = Round(matches + [match], date_of_play, i + 1)
                if new_proposed_round.is_valid():
                    matches.append(match)

        r = Round(matches, date_of_play, num_courts)
        if r.is_valid():
            return r
        raise NotValidRoundError("Could not generate a valid round.")
