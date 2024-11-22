"""A season consisting of multiple rounds by a given start and end date."""

import logging
import random
from datetime import date, time, timedelta
from itertools import combinations

from .player import Player
from .round import NotValidSwapError
from .schedule import NotValidScheduleError, Schedule, ScheduleFactory


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
        calendar_title: str = "Tennisabo",
    ):
        self.players = players
        self.start = start
        self.end = end
        self.time_start = time_start
        self.time_end = time_end
        self.num_courts = number_courts
        self.calendar_title = calendar_title
        # generate a list of all dates for the season,
        # they start at start and occur weekly until end
        self.dates = []
        d = start
        while d <= end:
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
        calendar_title = data["calendar_title"]
        instance = cls(players, start, end, number_courts, time_start, time_end, calendar_title)
        instance.schedule = Schedule.from_dict(data["schedule"])
        return instance

    @classmethod
    def create_from_settings(cls, data: dict) -> "Season":
        """Create a Season from a dictionary."""
        players = {Player.from_dict(p) for p in data["players"]}
        start = date.fromisoformat(data["abo"]["start"])
        end = date.fromisoformat(data["abo"]["end"])
        time_start = time.fromisoformat(data["calendar"]["time_start"])
        time_end = time.fromisoformat(data["calendar"]["time_end"])
        number_courts = data["abo"]["number_courts"]
        calendar_title = data["calendar"]["title"]
        return cls(players, start, end, number_courts, time_start, time_end, calendar_title)

    def generate_schedule(self) -> None:
        """Generate a schedule for this season."""
        self.schedule = ScheduleFactory.generate_valid_schedule(
            self.players, self.dates, self.num_courts
        )

    def optimize_schedule_by_swapping_players(self, swaps: int) -> int:
        """Optimize the schedule by swapping players."""
        if self.schedule is None:
            raise NotValidScheduleError("No schedule generated yet.")

        current_score = self.schedule.get_score()
        # switch with all possible players
        for r in self.schedule.rounds:
            self.logger.debug(f"Switching all players: Starting new round {r.date}")

            for match_index, match in enumerate(r.matches):
                current_players = match.players
                for possible_pair in Player.get_all_possible_combinations(
                    self.players.difference(r.get_players()).union(match.players)
                ):
                    if current_players != possible_pair:
                        try:
                            r.swap_players(match_index, possible_pair)
                        except NotValidSwapError:
                            continue
                        new_score = self.schedule.get_score()
                        if new_score < current_score:
                            swaps += 1
                            current_players = possible_pair
                            current_score = new_score
                        else:
                            # swap back to original match
                            r.swap_players(match_index, current_players)

        current_score = self.schedule.get_score()
        # switch players between matches of a round
        for r in self.schedule.rounds:
            self.logger.debug(f"Switching players inside round: Starting new round {r.date}")
            # get all combinations of match indexes
            for i, j in combinations(range(len(r.matches)), 2):
                match1 = r.matches[i]
                match2 = r.matches[j]
                for player1 in match1.players:
                    for player2 in match2.players:
                        try:
                            r.swap_players_of_existing_matches(i, j, {player1, player2})
                        except NotValidSwapError:
                            continue
                        new_score = self.schedule.get_score()
                        if new_score < current_score:
                            swaps += 1
                            current_score = new_score
                        else:
                            # swap back to original matches
                            r.swap_players_of_existing_matches(i, j, {player1, player2})

        return swaps

    def optimize_schedule_by_swapping_matches(self, swaps: int) -> int:
        """Optimize the schedule by swapping matches."""
        # cant be removed even if we swap players between existing matches
        # it gives an additional random factor to the algorithmus
        if self.schedule is None:
            raise NotValidScheduleError("No schedule generated yet.")

        indizes = [(i, j) for i in range(len(self.schedule.rounds)) for j in range(self.num_courts)]

        # shuffle index to have a random factor
        # (thus start if schedule is not to optimized)
        index_combination = list(combinations(indizes, 2))
        random.shuffle(index_combination)

        current_score = self.schedule.get_score()

        for (round_index1, match_index1), (
            round_index2,
            match_index2,
        ) in index_combination:
            self.logger.debug(
                f"try swapping Round {round_index1} "
                + f"Match {match_index1} with Round {round_index2} "
                + f"Match {match_index2}"
            )
            if (
                self.schedule.rounds[round_index1].matches[match_index1].players
                == self.schedule.rounds[round_index2].matches[match_index2].players
            ):
                continue

            try:
                self.schedule.swap_matches(round_index1, match_index1, round_index2, match_index2)
            except NotValidSwapError:
                continue
            new_score = self.schedule.get_score()
            if new_score < current_score:
                swaps += 1
                current_score = new_score
            else:
                # swap back to original matches
                self.schedule.swap_matches(round_index1, match_index1, round_index2, match_index2)
        return swaps

    def optimize_schedule(self) -> None:
        """Optimize the schedule for this season."""
        if self.schedule is None:
            self.generate_schedule()

        swaps = 0
        while True:
            self.logger.info("Starting new round of optimizing ...")

            self.logger.info("Start swapping players ...")
            swaps += self.optimize_schedule_by_swapping_players(swaps)

            self.logger.info("Start swapping matches ...")
            swaps += self.optimize_schedule_by_swapping_matches(swaps)

            if swaps > 0:
                self.logger.info(
                    f"Swapped {swaps} times. "
                    + "The current score is: "
                    + f"{self.schedule.get_score()}."  # type: ignore
                )
                swaps = 0
            else:
                self.logger.info("No more swaps feasible.")
                break

    def export_season(self, folderpath: str) -> None:
        """Export this season to an Excel file."""
        if self.schedule is None:
            raise NotValidScheduleError("No schedule generated yet.")
        self.schedule.export(folderpath, self.calendar_title, self.time_start, self.time_end)
