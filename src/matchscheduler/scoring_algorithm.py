import itertools

import numpy as np
from line_profiler import profile

from .match import Match
from .player import Player
from .schedule import Schedule


class ScoringAlgorithm:
    @profile
    def get_score(self, schedule: Schedule, players: list[Player]) -> float:
        """Get the score of this schedule."""
        num_rounds = len(schedule.rounds)
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
    def get_std_of_player_times_playing(self, schedule: Schedule, players: list[Player]) -> float:
        """Get the standard deviation of times playing for this schedule."""
        weighted_times_playing = [
            len(schedule.get_match_indizes_of_player(p)) / p.weight for p in players
        ]
        return float(np.std(weighted_times_playing))

    @profile
    def get_std_of_all_possible_matches(self, schedule: Schedule, players: list[Player]) -> float:
        """Get the standard deviation of all possible matches for this schedule."""
        all_possible_matches: dict[Match, float] = {}
        for p, q in itertools.combinations(players, 2):
            combined_weight = p.weight * q.weight
            all_possible_matches[Match(p, q)] = (
                len(schedule.get_match_indizes_of_match(Match(p, q))) / combined_weight
            )
        return np.std(list(all_possible_matches.values()))  # type: ignore

    @profile
    def get_std_of_pause_between_playing(self, schedule: Schedule, players: list[Player]) -> float:
        """Get the standard deviation of pause between playing for this schedule."""
        pause_between_playing: list[float] = [0] * len(players)
        for i, p in enumerate(players):
            rounds_playing = [x[0] for x in schedule.get_match_indizes_of_player(p)]
            if len(rounds_playing) > 1:
                pause_between_playing[i] = float(
                    np.std(
                        [
                            rounds_playing[j + 1] - rounds_playing[j]
                            for j in range(len(rounds_playing) - 1)
                        ]
                        + [rounds_playing[0], len(schedule.rounds) - rounds_playing[-1]]
                    )
                )
            else:
                pause_between_playing[i] = len(schedule.rounds)
        return np.sum(pause_between_playing)

    @profile
    def get_std_of_pause_between_matches(self, schedule: Schedule, players: list[Player]) -> float:
        """Get the standard deviation of pause between matches for this schedule."""
        std_pause_between_matches: dict[Match, float] = {}

        for p, q in itertools.combinations(players, 2):
            m = Match(p, q)
            matches_playing = schedule.get_match_indizes_of_match(m)
            rounds_playing = sorted([x[0] for x in matches_playing])
            if len(rounds_playing) > 1:
                std_pause_between_matches[m] = float(
                    np.std(
                        [
                            rounds_playing[j + 1] - rounds_playing[j]
                            for j in range(len(rounds_playing) - 1)
                        ]
                        + [rounds_playing[0], len(schedule.rounds) - rounds_playing[-1]]
                    )
                )
            else:
                std_pause_between_matches[m] = len(schedule.rounds)
        return np.sum(list(std_pause_between_matches.values()))
