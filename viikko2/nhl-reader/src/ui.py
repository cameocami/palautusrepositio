from rich.table import Table
from player_reader import PlayerReader
from rich.console import Console


class UI:
    def __init__(self, player_reader: PlayerReader):
        self.console = Console()
        self.table = Table(title="All Players Stats")
        self.table.add_column("Name", justify="left", style="cyan", no_wrap=True)
        self.table.add_column("Goals", justify="right", style="magenta")
        self.table.add_column("Assists", justify="right", style="green")
        self.table.add_column("Points", justify="right", style="yellow")
        for player in player_reader.players:
            self.table.add_row(str(player.name), str(player.goals), str(player.assists), str(player.goals + player.assists))

        self.console.print(self.table)