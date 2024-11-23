import logging
import random
from itertools import combinations

from matchscheduler.schedule import NotValidScheduleError
from matchscheduler.season import Season

from .player import Player
from .round import NotValidSwapError
from .schedule import NotValidScheduleError, ScheduleFactory


class Optimizer:

    def __init__(self, season: Season):
        self.season = season
        self.logger = logging.getLogger(__name__)

    def optimize_schedule_by_swapping_players(self, swaps: int) -> int:
        """Optimize the schedule by swapping players."""
        if self.season.schedule is None:
            raise NotValidScheduleError("No schedule generated yet.")

        current_score = self.season.schedule.get_score()
        # switch with all possible players
        for r in self.season.schedule.rounds:
            self.logger.debug(f"Switching all players: Starting new round {r.date}")

            for match_index, match in enumerate(r.matches):
                current_players = match.players
                for possible_pair in Player.get_all_possible_combinations(
                    self.season.schedule.players.difference(r.get_players()).union(match.players)
                ):
                    if current_players != possible_pair:
                        try:
                            r.swap_players(match_index, possible_pair)
                        except NotValidSwapError:
                            continue
                        new_score = self.season.schedule.get_score()
                        if new_score < current_score:
                            swaps += 1
                            current_players = possible_pair
                            current_score = new_score
                        else:
                            # swap back to original match
                            r.swap_players(match_index, current_players)

        current_score = self.season.schedule.get_score()
        # switch players between matches of a round
        for r in self.season.schedule.rounds:
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
                        new_score = self.season.schedule.get_score()
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
        if self.season.schedule is None:
            raise NotValidScheduleError("No schedule generated yet.")

        indizes = [
            (i, j)
            for i in range(len(self.season.schedule.rounds))
            for j in range(self.season.num_courts)
        ]

        # shuffle index to have a random factor
        # (thus start if schedule is not to optimized)
        index_combination = list(combinations(indizes, 2))
        random.shuffle(index_combination)

        current_score = self.season.schedule.get_score()

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
                self.season.schedule.rounds[round_index1].matches[match_index1].players
                == self.season.schedule.rounds[round_index2].matches[match_index2].players
            ):
                continue

            try:
                self.season.schedule.swap_matches(
                    round_index1, match_index1, round_index2, match_index2
                )
            except NotValidSwapError:
                continue
            new_score = self.season.schedule.get_score()
            if new_score < current_score:
                swaps += 1
                current_score = new_score
            else:
                # swap back to original matches
                self.season.schedule.swap_matches(
                    round_index1, match_index1, round_index2, match_index2
                )
        return swaps

    def optimize_schedule(self) -> None:
        """Optimize the schedule for this season."""
        if self.season.schedule is None:
            self.season.schedule = ScheduleFactory.generate_valid_schedule(
                self.season.players, self.season.dates, self.season.num_courts
            )

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
                    + f"{self.season.schedule.get_score()}."  # type: ignore
                )
                swaps = 0
            else:
                self.logger.info("No more swaps feasible.")
                break
