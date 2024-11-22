import json
from pathlib import Path

from matchscheduler.season import Season


def test_optimize(request):
    base_path = Path(request.path).parent
    with open(f"{base_path}/input/settings.json", "r", encoding="utf-8") as input, open(
        f"{base_path}/expected/test_optimize.json", "r", encoding="utf-8"
    ) as expected:
        # load settings.json into data object
        data = json.load(input)
        s = Season.create_from_settings(data)
        s.generate_schedule()
        s.optimize_schedule()

        expected_value = Season.from_dict(json.load(expected)).schedule.get_score()
        assert s.schedule.get_score() <= expected_value * 1.1
