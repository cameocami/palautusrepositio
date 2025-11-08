'''Module defining the Player class representing a NHL hockey player.'''

class Player:
    '''Class representing a NHL hockey player with relevant statistics as attributes.'''
    def __init__(self, player_dictionary: dict):
        self.name = player_dictionary['name']
        self.nationality = player_dictionary['nationality']
        self.goals = player_dictionary['goals']
        self.assists = player_dictionary['assists']
        self.team = player_dictionary['team']
        self.games = player_dictionary['games']

    def __str__(self):
        '''Return a string representation of the player.'''
        return f'{self.name:20}: {self.goals} + {self.assists} : {self.goals + self.assists}'

    def points(self):
        '''Return the total points (goals + assists) of the player.'''
        return self.goals + self.assists

    def __lt__(self, other):
        '''Define less-than comparison based on points for sorting players.'''
        return self.points() < other.points()
