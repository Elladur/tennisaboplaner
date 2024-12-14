"""Player class for the match scheduler."""

from datetime import date


class Player:
    """A player of the match scheduler."""

    def __init__(self, name: str, cannot_play: list[str], weight: float = 1):
        self.name = name
        self.cannot_play = {date.fromisoformat(i) for i in cannot_play}
        self.weight = weight

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "cannot_play": [str(d) for d in sorted(self.cannot_play)],
            "weight": self.weight,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Player":
        """Create a Player from a dictionary."""
        name = data["name"]
        cannot_play = data["cannot_play"]
        weight = data["weight"]
        return cls(name, cannot_play, weight)

    def __str__(self) -> str:
        return self.name
