from datetime import datetime
from pathlib import Path

from icalendar import Calendar, Event
from openpyxl import Workbook

from .player import Player
from .schedule import NotValidScheduleError
from .season import Season


class Printer:

    def __init__(self, season: Season):
        self.season = season

    # export schedule into a excel file with each round as a row
    # consisting of the date in the first column and in every next column a match
    def export(self, folderpath: Path) -> None:
        """Export this schedule to an Excel file."""
        if self.season.schedule is None:
            raise NotValidScheduleError("No schedule generated yet.")
        excel = Workbook()
        sheet = excel.active
        sheet.title = "Schedule"  # type: ignore
        sheet.append(  # type: ignore
            ["Date"]
            + [f"Match {i}" for i in range(1, len(self.season.schedule.rounds[0].matches) + 1)]
        )
        for r in sorted(self.season.schedule.rounds, key=lambda r: r.date):
            sheet.append([r.date] + [str(m) for m in r.matches])  # type: ignore

        # add an additional sheet to excel workbook with columns for each player
        # and their match partners
        sheet = excel.create_sheet("Partner by Player")  # type: ignore
        sheet.append(  # type: ignore
            ["Date"] + [str(p) for p in sorted(self.season.players, key=lambda p: p.name)]
        )
        for r in sorted(self.season.schedule.rounds, key=lambda r: r.date):
            row = [str(r.date)]
            matches = r.matches
            for p in sorted(self.season.players, key=lambda p: p.name):
                append_string = ""
                for m in matches:
                    if p in m.players:
                        opponent = m.players.difference({p}).pop()
                        append_string = str(opponent)
                        break
                row.append(append_string)  # type: ignore
            sheet.append(row)  # type: ignore

        # add an additional sheet to excel workbook with columns for each possible match
        # and each row marks with an x if the match is played on that day
        sheet = excel.create_sheet("Matches Overview")  # type: ignore
        sheet.append(  # type: ignore
            ["Date"]
            + [
                Player.to_string(pm)
                for pm in Player.get_all_possible_combinations(self.season.players)
            ]
        )
        for r in sorted(self.season.schedule.rounds, key=lambda r: r.date):
            row = [str(r.date)]
            matches = r.matches
            for pm in Player.get_all_possible_combinations(self.season.players):
                append_string = ""
                for m in matches:
                    if pm == m.players:
                        append_string = "x"
                        break
                row.append(append_string)  # type: ignore
            sheet.append(row)  # type: ignore

        excel.save(folderpath / "schedule.xlsx")

        # create a calendar for each player with his matches
        for p in self.season.players:
            cal = Calendar()
            cal.add("prodid", "-//MatchScheduler//MatchScheduler//EN")
            cal.add("version", "2.0")
            cal.add("name", f"MatchScheduler - {p.name}")
            cal.add("X-WR-CALNAME", f"MatchScheduler - {p.name}")
            cal.add("X-WR-TIMEZONE", "Europe/Vienna")
            cal.add("X-WR-CALDESC", f"MatchScheduler - {p.name}")
            for r in self.season.schedule.rounds:
                if p in r.get_players():
                    event = Event()
                    event.add("summary", self.season.calendar_title)
                    event.add("description", r.export_match_string())
                    event.add("dtstart", datetime.combine(r.date, self.season.time_start))
                    event.add("dtend", datetime.combine(r.date, self.season.time_end))
                    cal.add_component(event)
            with open(folderpath / f"{p.name}.ics", "wb") as f:
                f.write(cal.to_ical())