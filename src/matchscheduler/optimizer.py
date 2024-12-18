import logging
import random
from itertools import combinations

from line_profiler import profile

from matchscheduler.season import Season

from .match import create_match, get_players_of_match
from .scoring_algorithm import ScoringAlgorithm


class Optimizer:

    def __init__(self, season: Season):
        self.season = season
        self.logger = logging.getLogger(__name__)
        self.scorer = ScoringAlgorithm()

    @profile
    def optimize_schedule_by_swapping_players(self, swaps: int) -> int:
        """Optimize the schedule by swapping players."""

        current_score = self.scorer.get_score(self.season.schedule, self.season.players)
        # switch with all possible players
        for round_index, round in enumerate(self.season.schedule):
            if round_index in self.season.fixed_rounds:
                continue
            self.logger.debug(
                "Switching all players: Starting new round %s", self.season.dates[round_index]
            )

            for match_index, current_match in enumerate(round):
                for p, q in combinations(range(len(self.season.players)), 2):
                    possible_match = create_match(p, q)
                    if possible_match == current_match:
                        continue
                    changed = self.season.change_match(round_index, match_index, possible_match)
                    if not changed:
                        continue
                    new_score = self.scorer.get_score(self.season.schedule, self.season.players)
                    if new_score < current_score:
                        swaps += 1
                        self.logger.debug(
                            "Switched players - old score = %.2f - new score = %.2f",
                            current_score,
                            new_score,
                        )
                        current_score = new_score
                        current_match = possible_match
                    else:
                        # swap back to original match
                        self.season.change_match(round_index, match_index, current_match)

        current_score = self.scorer.get_score(self.season.schedule, self.season.players)
        # switch players between matches of a round
        for round_index, round in enumerate(self.season.schedule):
            if round_index in self.season.fixed_rounds:
                continue
            self.logger.debug(
                "Switching players inside round:" + "Starting new round %s",
                self.season.dates[round_index],
            )
            # get all combinations of match indexes
            for match1, match2 in combinations(range(self.season.num_courts), 2):
                for player1, player2 in [
                    (p1, p2)
                    for p1 in get_players_of_match(round[match1])
                    for p2 in get_players_of_match(round[match2])
                ]:
                    swapped = self.season.swap_players_of_existing_matches(
                        round_index, player1, player2
                    )
                    if not swapped:
                        continue
                    new_score = self.scorer.get_score(self.season.schedule, self.season.players)
                    if new_score < current_score:
                        swaps += 1
                        self.logger.debug(
                            "Switched players insied existing round "
                            + "- old score = %.2f - new score = %.2f",
                            current_score,
                            new_score,
                        )
                        current_score = new_score
                        break
                    # swap back to original matches
                    self.season.swap_players_of_existing_matches(round_index, player1, player2)

        return swaps

    @profile
    def optimize_schedule_by_swapping_matches(self, swaps: int) -> int:
        """Optimize the schedule by swapping matches."""
        # cant be removed even if we swap players between existing matches
        # it gives an additional random factor to the algorithmus

        indizes = [
            (i, j) for i in range(len(self.season.schedule)) for j in range(self.season.num_courts)
        ]

        # shuffle index to have a random factor
        # (thus start if schedule is not to optimized)
        index_combination = list(combinations(indizes, 2))
        random.shuffle(index_combination)

        current_score = self.scorer.get_score(self.season.schedule, self.season.players)

        for (round_index1, match_index1), (
            round_index2,
            match_index2,
        ) in index_combination:
            self.logger.debug(
                "try swapping Round %i Match %i with Round %i Match %i",
                round_index1,
                match_index1,
                round_index2,
                match_index2,
            )
            if (
                self.season.schedule[round_index1][match_index1]
                == self.season.schedule[round_index2][match_index2]
                or round_index1 in self.season.fixed_rounds
                or round_index2 in self.season.fixed_rounds
            ):
                continue
            switched = self.season.switch_matches(
                round_index1, match_index1, round_index2, match_index2
            )
            if not switched:
                continue
            new_score = self.scorer.get_score(self.season.schedule, self.season.players)
            if new_score < current_score:
                swaps += 1
                self.logger.debug(
                    "Switched matches - old score = %.2f - new score = %.2f",
                    current_score,
                    new_score,
                )
                current_score = new_score
            else:
                # swap back to original matches
                self.season.switch_matches(round_index1, match_index1, round_index2, match_index2)

        return swaps

    @profile
    def optimize_schedule(self) -> float:
        """Optimize the schedule for this season."""
        swaps = 0
        while True:
            self.logger.info("Starting new round of optimizing ...")

            self.logger.info("Start swapping players ...")
            swaps += self.optimize_schedule_by_swapping_players(swaps)

            self.logger.info("Start swapping matches ...")
            swaps += self.optimize_schedule_by_swapping_matches(swaps)

            if swaps > 0:
                self.logger.info(
                    "Swapped {swaps} times. The current score is: %.3f ",
                    self.scorer.get_score(self.season.schedule, self.season.players),
                )
                swaps = 0
            else:
                self.logger.info("No more swaps feasible.")
                break

        return self.scorer.get_score(self.season.schedule, self.season.players)
