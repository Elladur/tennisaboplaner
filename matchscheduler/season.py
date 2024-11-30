"""A season consisting of multiple rounds by a given start and end date."""

import itertools
import logging
import random
from datetime import date, time, timedelta

from line_profiler import profile

from .match import (Match, can_match_be_added, create_match,
                    get_players_of_match)
from .player import Player
from .round import get_players_of_round


class Season:
    """A season of matches."""

    def __init__(
        self,
        players: list[Player],
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

        self.schedule = self._generate_schedule()
        self.logger = logging.getLogger(__name__)

    def _generate_schedule(self) -> list[list[Match]]:
        season = []
        for d in self.dates:
            season.append(self._generate_valid_round(d))
        return season

    def _generate_valid_round(self, date: date) -> list[Match]:
        rounds: list[Match] = []
        for _ in range(self.num_courts):
            rounds.append(self._generate_valid_match(date, rounds))
        if len(rounds) == self.num_courts:
            return rounds
        raise ValueError()

    def _generate_valid_match(self, date: date, other_matches: list[Match]) -> Match:
        indizes = list(range(len(self.players)))
        random.shuffle(indizes)
        for p, q in itertools.combinations(indizes, 2):
            if (
                date not in self.players[p].cannot_play
                and date not in self.players[q].cannot_play
                and p != q
            ):
                match = create_match(p, q)
                if can_match_be_added(other_matches, match):
                    return match
        raise ValueError()

    @profile
    def change_match(self, round_index: int, match_index: int, match: Match) -> bool:
        old_match = self.schedule[round_index][match_index]
        self.schedule[round_index][match_index] = match
        if self.check_if_round_is_valid(round_index):
            return True
        self.schedule[round_index][match_index] = old_match
        return False

    @profile
    def check_if_round_is_valid(self, round_index: int) -> bool:
        players = get_players_of_round(self.schedule[round_index])
        if len(players) != self.num_courts * 2:
            return False
        date = self.dates[round_index]
        return not any(date in self.players[p].cannot_play for p in players)

    def check_schedule_is_valid(self) -> bool:
        for i in range(len(self.schedule)):
            if not self.check_if_round_is_valid(i):
                return False
        return True

    @profile
    def swap_players_of_existing_matches(self, round_index: int, p: int, q: int) -> None:
        for i, match in enumerate(self.schedule[round_index]):
            if p in get_players_of_match(match):
                other_player = match[0] if match[0] != p else match[1]
                self.schedule[round_index][i] = create_match(q, other_player)
                continue
            if q in get_players_of_match(match):
                other_player = match[0] if match[0] != q else match[1]
                self.schedule[round_index][i] = create_match(p, other_player)
                continue

    @profile
    def switch_matches(self, round1: int, match1: int, round2: int, match2: int) -> bool:
        self.schedule[round1][match1], self.schedule[round2][match2] = (
            self.schedule[round2][match2],
            self.schedule[round1][match1],
        )
        if self.check_if_round_is_valid(round1) and self.check_if_round_is_valid(round2):
            return True
        self.schedule[round1][match1], self.schedule[round2][match2] = (
            self.schedule[round2][match2],
            self.schedule[round1][match1],
        )
        return False

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
            "schedule": self.schedule,
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
        instance.schedule = data["schedule"]
        return instance

    @classmethod
    def create_from_settings(cls, data: dict) -> "Season":
        """Create a Season from a dictionary."""
        players = [Player.from_dict(p) for p in data["players"]]
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
