import requests
from player import Player

class PlayerReader:
    def __init__(self, url:str):
        response = requests.get(url, timeout=10).json()
        self.players = []
        for player_dict in response:
            player = Player(player_dict)
            self.players.append(player)

    def get_players(self):
        return self.players

    def get_nationalities(self):
        return {player.nationality for player in self.players}
