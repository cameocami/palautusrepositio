'''UI module for displaying player statistics using Rich library.'''

from rich.table import Table
from rich.console import Console

from player_reader import PlayerReader


class UI:
    '''Class for displaying player statistics in a table format using Rich library.'''
    def __init__(self, player_reader: PlayerReader):
        self.console = Console()
        self.reader = player_reader
        self.table = Table()
        self.table.add_column("Name", justify="left", style="cyan", no_wrap=True)
        self.table.add_column("Team", justify="left", style="white")
        self.table.add_column("Goals", justify="right", style="magenta")
        self.table.add_column("Assists", justify="right", style="green")
        self.table.add_column("Points", justify="right", style="yellow")
        self.table.add_column("Nationality", justify="left", style="blue")

    def populate_table(self, players=None):
        '''Populate the table with player statistics.'''
        if players is None:
            players = self.reader.players
        for player in players:
            self.table.add_row(
                player.name,
                player.team,  
                str(player.goals),
                str(player.assists),
                str(player.points()),
                player.nationality
            )

    def display(self):
        '''Display the table in the console.'''
        self.console.print(self.table)

    def clear(self):
        '''Clear the console.'''
        self.console.clear()
