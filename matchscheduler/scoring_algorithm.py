import numpy as np

from .player import Player
from .schedule import Schedule


class ScoringAlgorithm:

    def get_score(self, schedule: Schedule) -> float:
        """Get the score of this schedule."""
        num_rounds = len(schedule.rounds)
        score = (
            num_rounds * self.get_std_of_all_possible_matches(schedule)
            + num_rounds * self.get_std_of_player_times_playing(schedule)
            + self.get_std_of_pause_between_matches(schedule)  # is calculated as sum of std
            + self.get_std_of_pause_between_playing(schedule)  # is calculated as sum of std
        )
        return score

    def get_std_of_player_times_playing(self, schedule: Schedule) -> float:
        """Get the standard deviation of times playing for this schedule."""
        times_playing: dict[Player, int] = {}
        for p in schedule.players:
            times_playing[p] = len(schedule.get_matches_of_player(p))
        return np.std(list(times_playing.values()))  # type: ignore

    def get_std_of_all_possible_matches(self, schedule: Schedule) -> float:
        """Get the standard deviation of all possible matches for this schedule."""
        all_possible_matches: dict[tuple[Player, Player], int] = {}
        for encounter in Player.get_all_possible_combinations(schedule.players):
            all_possible_matches[Player.set_to_tuple(encounter)] = len(
                schedule.get_matches_of_players(encounter)
            )
        return np.std(list(all_possible_matches.values()))  # type: ignore

    def get_std_of_pause_between_playing(self, schedule: Schedule) -> float:
        """Get the standard deviation of pause between playing for this schedule."""
        pause_between_playing: dict[Player, float] = {}
        min_date = min((r.date for r in schedule.rounds))
        max_date = max((r.date for r in schedule.rounds))
        for p in schedule.players:
            matches = schedule.get_matches_of_player(p)
            matches.sort(key=lambda m: m.date)
            if len(matches) > 1:
                pause_between_playing[p] = np.std(  # type: ignore
                    [(matches[i + 1].date - matches[i].date).days for i in range(len(matches) - 1)]
                    + [  # add difference to first and last date
                        (matches[0].date - min_date).days,
                        (max_date - matches[-1].date).days,
                    ]
                )
            else:
                pause_between_playing[p] = (max_date - min_date).days  # set to maximal
        return np.sum(list(pause_between_playing.values()))  # type: ignore

    def get_std_of_pause_between_matches(self, schedule: Schedule) -> float:
        """Get the standard deviation of pause between matches for this schedule."""
        min_date = min((r.date for r in schedule.rounds))
        max_date = max((r.date for r in schedule.rounds))
        pause_between_matches: dict[tuple[Player, Player], float] = {}
        for encounter in Player.get_all_possible_combinations(schedule.players):
            matches = schedule.get_matches_of_players(encounter)
            matches.sort(key=lambda m: m.date)
            if len(matches) > 1:
                pause_between_matches[Player.set_to_tuple(encounter)] = np.std(  # type: ignore
                    [(matches[i + 1].date - matches[i].date).days for i in range(len(matches) - 1)]
                    + [  # add difference to first and last date
                        (matches[0].date - min_date).days,
                        (max_date - matches[-1].date).days,
                    ]
                )
            else:
                pause_between_matches[Player.set_to_tuple(encounter)] = (
                    max_date - min_date  # set to maximal value
                ).days
        return np.sum(list(pause_between_matches.values()))  # type: ignore
