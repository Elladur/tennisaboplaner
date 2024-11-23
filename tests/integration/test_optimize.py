import json
from pathlib import Path

from matchscheduler.optimizer import Optimizer
from matchscheduler.scoring_algorithm import ScoringAlgorithm
from matchscheduler.season import Season


def test_optimize(request):
    base_path = Path(request.path).parent
    with open(f"{base_path}/input/settings.json", "r", encoding="utf-8") as input, open(
        f"{base_path}/expected/test_optimize.json", "r", encoding="utf-8"
    ) as expected:
        # load settings.json into data object
        data = json.load(input)
        s = Season.create_from_settings(data)
        o = Optimizer(s)
        score = o.optimize_schedule()

        expected_value = ScoringAlgorithm().get_score(
            Season.from_dict(json.load(expected)).schedule
        )
        assert score <= expected_value * 1.1
