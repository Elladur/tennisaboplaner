import json
from pathlib import Path

from matchscheduler.printer import Printer
from matchscheduler.season import Season


def test_printer(request, tmp_path):
    base_path = Path(request.path).parent
    with open(f"{base_path}/input/test_printer.json", "r", encoding="utf-8") as input:
        # load settings.json into data object
        s = Season.from_dict(json.load(input))
        p = Printer(s)
        p.export(tmp_path)
