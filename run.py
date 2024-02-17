from matchscheduler.season import Season
import json
import os
import logging
import logging.config

if __name__ == "__main__":
    logging.config.fileConfig("log.ini")
    logger = logging.getLogger(__name__)
    with open("settings.json", "r", encoding="utf-8") as f:
        # load settings.json into data object
        data = json.load(f)
        s = Season.from_dict(data)
        s.generate_schedule()
        s.optimize_schedule()
        s.export_season(os.getcwd() + "/output/")
        logger.info(f"Current Schedule score is = {s.schedule.get_score()}")
