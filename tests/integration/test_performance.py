import json
import time
from pathlib import Path
from datetime import timedelta

from matchscheduler.optimizer import Optimizer
from matchscheduler.season import Season
from matchscheduler.schedule import Schedule


def test_performance(request):
    base_path = Path(request.path).parent
    with open(f"{base_path}/input/settings.json", "r") as input:
        # load settings.json into data object
        data = json.load(input)
        s = Season.create_from_settings(data)
        o = Optimizer(s)

        days = []
        d = s.start
        while d <= s.end:
            if d not in s.excluded_dates:
                days.append(d)
            d = d + timedelta(days=7)

        start_time = time.time()
        for _ in range(50):
            o.optimize_schedule()
            o.season.schedule = Schedule.create(s.players, days, s.num_courts)
        end_time = time.time()

        elapsed_time = end_time - start_time
        assert elapsed_time <= 13  # 9.483287572860718
        # running test without debug over vs ui
        # first try: 22.344756364822388
        # second try: 22.771101236343384
        # third try: 23.330134868621826

        # with classes: 143 seconds