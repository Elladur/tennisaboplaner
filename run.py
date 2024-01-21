from matchscheduler.season import Season
import json
import os

if __name__ == "__main__":
    with open("settings.json", "r", encoding="utf-8") as f:
        # load settings.json into data object
        data = json.load(f)
        s = Season.from_dict(data)
        s.generate_schedule()
        s.optimize_schedule()
        s.export_season(os.getcwd() + "/output/")
        print(f"Current Schedule score is = {s.schedule.get_score()}")
