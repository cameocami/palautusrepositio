'''UI module for displaying player statistics using Rich library.'''

from rich.table import Table
from rich.console import Console


class UI:
    '''Class for displaying player statistics in a table format using Rich library.'''
    def __init__(self):
        self.console = Console()
        self.table = Table()

    def display(self):
        '''Display the table in the console.'''
        self.console.print(self.table)

    def clear(self):
        '''Clear the console.'''
        self.console.clear()

    def prompt_season(self):
        '''Prompt the user to enter a season.'''
        input_validity = True
        season = input("Enter season (e.g., 2020-21): ")
        if len(season) != 7:
            input_validity = False
        else:
            if season[4] != '-':
                input_validity = False
            if not (season[:4]+season[5:]).isdigit():
                input_validity = False
        if not input_validity:
            print("Invalid season format. Used default season 2024-25.")
            season = "2024-25"
        return season

    def prompt_nationality(self, nationalities: set):
        '''Prompt the user to enter a nationality.'''
        input_validity = True
        print("Available nationalities:", "/".join(sorted(nationalities)))
        nationality = input("Enter nationality: ").upper()
        if len(nationality) != 3:
            input_validity = False
        else:
            if nationality not in nationalities:
                input_validity = False
        if input_validity is False:
            print("Invalid nationality format. Used default nationality FIN.")
            nationality = "FIN"
        return nationality

    def populate_table(self, season, nationality, players=None):
        '''Populate the table with player statistics.'''
        self.clear()
        self.table = Table(title=f"NHL Player Statistics - {season} ({nationality})")
        self.table.add_column("Name", justify="left", style="cyan", no_wrap=True)
        self.table.add_column("Team", justify="left", style="white")
        self.table.add_column("Goals", justify="right", style="magenta")
        self.table.add_column("Assists", justify="right", style="green")
        self.table.add_column("Points", justify="right", style="yellow")
        for player in players:
            self.table.add_row(
                player.name,
                player.team,
                str(player.goals),
                str(player.assists),
                str(player.points()),
            )
        self.display()
