"""Player class for the match scheduler."""

from datetime import date
from itertools import combinations


class Player:
    """A player of the match scheduler."""

    name: str
    cannot_play: list[date]

    def __init__(self, name: str, cannot_play: list[str]):
        self.name = name
        self.cannot_play = [date.fromisoformat(i) for i in cannot_play]

    def to_dict(self) -> dict:
        return {"name": self.name, "cannot_play": [str(d) for d in self.cannot_play]}

    @classmethod
    def from_dict(cls, data: dict) -> "Player":
        """Create a Player from a dictionary."""
        name = data["name"]
        cannot_play = data["cannot_play"]
        return cls(name, cannot_play)

    @classmethod
    def get_all_possible_combinations(cls, players: set["Player"]) -> list[set["Player"]]:
        """Get all possible combinations of players."""
        return [set(i) for i in combinations(players, 2)]

    def __eq__(self, __value: object) -> bool:
        if (
            __value.name == self.name  # type: ignore
            and __value.cannot_play == self.cannot_play  # type: ignore
        ):
            return True
        return False

    def __str__(self) -> str:
        return self.name

    def __hash__(self) -> int:
        return hash((self.name, tuple(self.cannot_play)))

    @classmethod
    def to_string(cls, players: set["Player"]) -> str:
        """Convert a set of players to a string."""
        return ", ".join([p.name for p in players])

    @classmethod
    def set_to_tuple(cls, players: set["Player"]) -> tuple["Player", "Player"]:
        """Convert a set of players to a tuple."""
        if len(players) != 2:
            raise ValueError("A set of players must have two players.")
        return tuple(players)  # type: ignore
