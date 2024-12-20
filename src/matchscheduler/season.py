"""A season consisting of multiple rounds by a given start and end date."""

import logging
from datetime import date, time, timedelta


from .player import Player
from .schedule import Schedule


class Season:
    """A season of matches."""

    def __init__(
        self,
        players: list[Player],
        start: date,
        end: date,
        number_courts: int,
        excluded_dates: list[date],
        schedule: Schedule,
        time_start: time,
        time_end: time,
        overall_cost: float = 0,
        calendar_title: str = "Tennisabo",
    ):
        self.players = players
        self.start = start
        self.end = end
        self.time_start = time_start
        self.time_end = time_end
        self.num_courts = number_courts
        self.excluded_dates = excluded_dates
        self.schedule = schedule
        self.calendar_title = calendar_title
        self.overall_cost = overall_cost
        self.logger = logging.getLogger(__name__)

    @classmethod
    def create(
        cls,
        players: list[Player],
        start: date,
        end: date,
        number_courts: int,
        excluded_dates: list[date],
        time_start: time,
        time_end: time,
        overall_cost: float = 0,
        calendar_title: str = "Tennisabo",
    ) -> "Season":
        days = []
        d = start
        while d <= end:
            if d not in excluded_dates:
                days.append(d)
            d = d + timedelta(days=7)
        schedule = Schedule.create(players, days, number_courts)
        return cls(
            players,
            start,
            end,
            number_courts,
            excluded_dates,
            schedule,
            time_start,
            time_end,
            overall_cost,
            calendar_title,
        )

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
            "schedule": self.schedule.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Season":
        players = [Player.from_dict(p) for p in data["players"]]
        start = date.fromisoformat(data["start"])
        end = date.fromisoformat(data["end"])
        time_start = time.fromisoformat(data["time_start"])
        time_end = time.fromisoformat(data["time_end"])
        number_courts = data["number_courts"]
        excluded_dates = data["excluded_dates"]
        calendar_title = data["calendar_title"]
        overall_cost = data["overall_cost"]
        schedule = Schedule.from_dict(data["schedule"], number_courts, players)
        instance = cls(
            players,
            start,
            end,
            number_courts,
            excluded_dates,
            schedule,
            time_start,
            time_end,
            overall_cost,
            calendar_title,
        )
        return instance

    @classmethod
    def create_from_settings(cls, data: dict) -> "Season":
        """Create a Season from a dictionary."""
        players = [Player.from_dict(p) for p in data["players"]]
        start = date.fromisoformat(data["abo"]["start"])
        end = date.fromisoformat(data["abo"]["end"])
        excluded_dates = [date.fromisoformat(d) for d in data["abo"]["excluded_dates"]]
        time_start = time.fromisoformat(data["calendar"]["time_start"])
        time_end = time.fromisoformat(data["calendar"]["time_end"])
        number_courts = data["abo"]["number_courts"]
        overall_cost = data["abo"]["overall_cost"]
        calendar_title = data["calendar"]["title"]
        return cls.create(
            players,
            start,
            end,
            number_courts,
            excluded_dates,
            time_start,
            time_end,
            overall_cost,
            calendar_title,
        )
