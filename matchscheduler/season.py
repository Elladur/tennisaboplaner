"""A season consisting of multiple rounds by a given start and end date."""

import logging
from datetime import date, time, timedelta

from .player import Player
from .schedule import Schedule


class Season:
    """A season of matches."""

    def __init__(
        self,
        players: set[Player],
        start: date,
        end: date,
        number_courts: int,
        time_start: time,
        time_end: time,
        excluded_dates: list[str],
        overall_cost: float = 0,
        calendar_title: str = "Tennisabo",
    ):
        self.players = players
        self.start = start
        self.end = end
        self.time_start = time_start
        self.time_end = time_end
        self.num_courts = number_courts
        self.calendar_title = calendar_title
        self.overall_cost = overall_cost
        self.excluded_dates = [date.fromisoformat(s) for s in excluded_dates]
        # generate a list of all dates for the season,
        # they start at start and occur weekly until end
        self.dates = []
        d = start
        while d <= end:
            if d not in self.excluded_dates:
                self.dates.append(d)
            d += timedelta(days=7)

        self.schedule: Schedule | None = None
        self.logger = logging.getLogger(__name__)

    def to_dict(self) -> dict:
        return {
            "players": [p.to_dict() for p in self.players],
            "start": str(self.start),
            "end": str(self.end),
            "number_courts": self.num_courts,
            "time_start": str(self.time_start),
            "time_end": str(self.time_end),
            "excluded_dates": [str(d) for d in self.excluded_dates],
            "overall_cost": self.overall_cost,
            "calendar_title": self.calendar_title,
            "schedule": self.schedule.to_dict() if self.schedule is not None else "",
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Season":
        players = {Player.from_dict(p) for p in data["players"]}
        start = date.fromisoformat(data["start"])
        end = date.fromisoformat(data["end"])
        time_start = time.fromisoformat(data["time_start"])
        time_end = time.fromisoformat(data["time_end"])
        number_courts = data["number_courts"]
        excluded_dates = data["excluded_dates"]
        calendar_title = data["calendar_title"]
        overall_cost = data["overall_cost"]
        instance = cls(
            players,
            start,
            end,
            number_courts,
            time_start,
            time_end,
            excluded_dates,
            overall_cost,
            calendar_title,
        )
        instance.schedule = Schedule.from_dict(data["schedule"])
        return instance

    @classmethod
    def create_from_settings(cls, data: dict) -> "Season":
        """Create a Season from a dictionary."""
        players = {Player.from_dict(p) for p in data["players"]}
        start = date.fromisoformat(data["abo"]["start"])
        end = date.fromisoformat(data["abo"]["end"])
        excluded_dates = data["abo"]["excluded_dates"]
        time_start = time.fromisoformat(data["calendar"]["time_start"])
        time_end = time.fromisoformat(data["calendar"]["time_end"])
        number_courts = data["abo"]["number_courts"]
        overall_cost = data["abo"]["overall_cost"]
        calendar_title = data["calendar"]["title"]
        return cls(
            players,
            start,
            end,
            number_courts,
            time_start,
            time_end,
            excluded_dates,
            overall_cost,
            calendar_title,
        )
