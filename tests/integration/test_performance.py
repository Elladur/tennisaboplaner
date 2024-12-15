import json
import time
from pathlib import Path

from matchscheduler.optimizer import Optimizer
from matchscheduler.season import Season


def test_performance(request):
    base_path = Path(request.path).parent
    with open(f"{base_path}/input/settings.json", "r") as input:
        # load settings.json into data object
        data = json.load(input)
        s = Season.create_from_settings(data)
        o = Optimizer(s)

        start_time = time.time()
        for _ in range(50):
            o.optimize_schedule()
            o.season._generate_schedule()
        end_time = time.time()

        elapsed_time = end_time - start_time
        assert elapsed_time <= 13  # 9.483287572860718
        # running test without debug over vs ui
        # first try: 22.344756364822388
        # second try: 22.771101236343384
        # third try: 23.330134868621826
