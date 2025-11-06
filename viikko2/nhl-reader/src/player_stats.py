from player import Player
from player_reader import PlayerReader

class PlayerStats:
    def __init__(self, reader:PlayerReader):
        self.reader = reader

    def _filter_by(self, criterion:str, filter_criteria:str):
        search_criteria = filter_criteria
        search_criterion = criterion
        return [player for player in self.reader.players if player.search_criteria == search_criterion]

    def top_scorers_by_nationality(self, nationality:str ):

        players_of_nationality = [player for player in self.reader.players if player.nationality == nationality]

        sorted_players = sorted(players_of_nationality, key=lambda player: player.goals + player.assists, reverse=True)

        return sorted_players
            
