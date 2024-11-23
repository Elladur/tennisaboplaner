import json
import time
from pathlib import Path

from matchscheduler.optimizer import Optimizer
from matchscheduler.season import Season


def test_optimize(request):
    base_path = Path(request.path).parent
    with open(f"{base_path}/input/settings.json", "r") as input:
        # load settings.json into data object
        data = json.load(input)
        s = Season.create_from_settings(data)
        o = Optimizer(s)

        start_time = time.time()
        o.optimize_schedule()
        end_time = time.time()

        elapsed_time = end_time - start_time
        assert elapsed_time <= 4  # 2.4688916206359863
