import requests
from player import Player

def main():
    url = "https://studies.cs.helsinki.fi/nhlstats/2024-25/players"
    response = requests.get(url).json()

    players = []

    for player_dict in response:
        player = Player(player_dict)
        players.append(player)

    print("Suomalaisten pelaajien tilastot:")

    finnish_players = [player for player in players if player.nationality == "FIN"]
    sorted_finns = sorted(finnish_players, key=lambda player: player.goals + player.assists, reverse=True)

    print(f'{"Nimi":30} {"Maalit":>6} {"Syötöt":>8} {"Tehopisteet":>12}')   

    for player in sorted_finns:
       points = player.goals + player.assists
       print(f'{player.name:30} {player.goals:6d} {player.assists:8d} {points:12d}')

if __name__ == "__main__":
    main()
