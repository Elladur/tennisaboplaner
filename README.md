# Tennisaboplaner

Tennisaboplaner is a script to schedule matches over a season. It's purpose is to give a schedule, if you are group of people that meet weekly for a tennis match and have only a number of limited courts, for instance indoor / in the winter season. It searches for a schedule in such a way that all people play the same amount, every player faces all others evenly and the matches are evenly distributed per player during the season. Additionally, you can provide prescheduling dates where player can't play. This will be taken into account, when it searches for possible schedules. 

## Requirements

Python needs to be installed.

## Usage

Adapt settings.json to your needs and execute `run.py`. 

```shell
pip install -r requirements.txt
python run.py
```

It will generate a Excel-File in the output-folder which represents the schedule. Additionally, it will create a calendar (*.ics) for each player. 

## Contributing

Pull requests are welcome. Please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.
