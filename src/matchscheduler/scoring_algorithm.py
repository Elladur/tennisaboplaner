import itertools

import numpy as np
from line_profiler import profile

from .match import create_match
from .player import Player
from .schedule import get_match_indizes_of_match, get_match_indizes_of_player


class ScoringAlgorithm:
    @profile
    def get_score(self, schedule: list[list[int]], players: list[Player]) -> float:
        """Get the score of this schedule."""
        num_rounds = len(schedule)
        score = (
            num_rounds * self.get_std_of_all_possible_matches(schedule, players)
            + num_rounds * self.get_std_of_player_times_playing(schedule, players)
            + self.get_std_of_pause_between_matches(
                schedule, players
            )  # is calculated as sum of std
            + self.get_std_of_pause_between_playing(
                schedule, players
            )  # is calculated as sum of std
        )
        return score

    @profile
    def get_std_of_player_times_playing(
        self, schedule: list[list[int]], players: list[Player]
    ) -> float:
        """Get the standard deviation of times playing for this schedule."""
        weighted_times_playing = [
            len(get_match_indizes_of_player(schedule, i)) / p.weight for i, p in enumerate(players)
        ]
        return float(np.std(weighted_times_playing))

    @profile
    def get_std_of_all_possible_matches(
        self, schedule: list[list[int]], players: list[Player]
    ) -> float:
        """Get the standard deviation of all possible matches for this schedule."""
        all_possible_matches: dict[tuple[int, int], float] = {}
        for p, q in itertools.combinations(range(len(players)), 2):
            if p != q:
                combined_weight = players[p].weight * players[q].weight
                all_possible_matches[(p, q)] = (
                    len(get_match_indizes_of_match(schedule, create_match(p, q))) / combined_weight
                )
        return np.std(list(all_possible_matches.values()))  # type: ignore

    @profile
    def get_std_of_pause_between_playing(
        self, schedule: list[list[int]], players: list[Player]
    ) -> float:
        """Get the standard deviation of pause between playing for this schedule."""
        pause_between_playing: list[float] = [0] * len(players)
        for i in range(len(players)):
            rounds_playing = [x[0] for x in get_match_indizes_of_player(schedule, i)]
            if len(rounds_playing) > 1:
                pause_between_playing[i] = float(
                    np.std(
                        [
                            rounds_playing[j + 1] - rounds_playing[j]
                            for j in range(len(rounds_playing) - 1)
                        ]
                        + [rounds_playing[0], len(schedule) - rounds_playing[-1]]
                    )
                )
            else:
                pause_between_playing[i] = len(schedule)
        return np.sum(pause_between_playing)

    @profile
    def get_std_of_pause_between_matches(
        self, schedule: list[list[int]], players: list[Player]
    ) -> float:
        """Get the standard deviation of pause between matches for this schedule."""
        std_pause_between_matches: dict[tuple[int, int], float] = {}

        for p, q in itertools.combinations(range(len(players)), 2):
            if p != q:
                matches_playing = get_match_indizes_of_match(schedule, create_match(p, q))
                rounds_playing = sorted([x[0] for x in matches_playing])
                if len(rounds_playing) > 1:
                    std_pause_between_matches[p, q] = float(
                        np.std(
                            [
                                rounds_playing[j + 1] - rounds_playing[j]
                                for j in range(len(rounds_playing) - 1)
                            ]
                            + [rounds_playing[0], len(schedule) - rounds_playing[-1]]
                        )
                    )
                else:
                    std_pause_between_matches[p, q] = len(schedule)
        return np.sum(list(std_pause_between_matches.values()))
