'''UI module for displaying player statistics using Rich library.'''

from rich.table import Table
from rich.console import Console

from player_reader import PlayerReader


class UI:
    '''Class for displaying player statistics in a table format using Rich library.'''
    def __init__(self, player_reader: PlayerReader):
        self.console = Console()
        self.table = Table(title="All Players Stats")
        self.table.add_column("Name", justify="left", style="cyan", no_wrap=True)
        self.table.add_column("Goals", justify="right", style="magenta")
        self.table.add_column("Assists", justify="right", style="green")
        self.table.add_column("Points", justify="right", style="yellow")
        for player in player_reader.players:
            pts = player.goals + player.assists
            self.table.add_row(f'{player.name}', f'{player.goals}', f'{player.assists}', f'{pts}')

    def display(self):
        '''Display the table in the console.'''
        self.console.print(self.table)

    def clear(self):
        '''Clear the console.'''
        self.console.clear()
