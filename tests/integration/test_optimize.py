import json
from pathlib import Path

from matchscheduler.optimizer import Optimizer
#from matchscheduler.printer import Printer
#from matchscheduler.scoring_algorithm import ScoringAlgorithm
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

        #expected_value = ScoringAlgorithm().get_score(
            #Season.from_dict(json.load(expected)).schedule
        #)
        #assert score <= expected_value * 1.1


#def test_exclusion(request, tmp_path):
    #base_path = Path(request.path).parent
    #with open(f"{base_path}/input/test_exclusion.json", "r", encoding="utf-8") as input:
        #s = Season.create_from_settings(json.load(input))
        #o = Optimizer(s)
        #o.optimize_schedule()
        #p = Printer(s)

        #p.export(tmp_path)
        #assert s.excluded_dates != []
