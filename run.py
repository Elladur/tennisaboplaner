import json
import logging
import logging.config
import os
from pathlib import Path

from joblib import Parallel, delayed

from matchscheduler.optimizer import Optimizer
from matchscheduler.printer import Printer
from matchscheduler.season import Season


def task(optimizer: Optimizer) -> float:
    return {"score": optimizer.optimize_schedule(), "season": optimizer.season}


if __name__ == "__main__":
    logging.config.fileConfig("log.ini")
    logger = logging.getLogger(__name__)
    num_jobs = 10
    with open("settings.json", "r", encoding="utf-8") as f:
        # load settings.json into data object
        data = json.load(f)
        seasons = [Optimizer(Season.create_from_settings(data)) for x in range(num_jobs)]
        results = Parallel(n_jobs=num_jobs)(delayed(task)(s) for s in seasons)
        best_result = sorted(results, key=lambda x: x["score"])[0]
        score, s = best_result["score"], best_result["season"]
        p = Printer(s)
        p.export(Path(os.getcwd() + "/output/"))
        logger.info("Current Schedule score is = %.3f", score)
