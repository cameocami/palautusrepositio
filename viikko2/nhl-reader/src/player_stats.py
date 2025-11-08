'''Module defining the PlayerStats class for analyzing NHL player statistics.'''

from player_reader import PlayerReader

class PlayerStats:
    '''Class for analyzing NHL player statistics with various filtering methods.'''
    def __init__(self, reader:PlayerReader):
        self.reader = reader

    def filter_by_nationality(self, nationality: str):
        return [player for player in self.reader.players if player.nationality == nationality]

    def top_scorers_by_nationality(self, nationality:str ):

        players_of_nationality = self.filter_by_nationality(nationality)

        return sorted(players_of_nationality, reverse=True)
