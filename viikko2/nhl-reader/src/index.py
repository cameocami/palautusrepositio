
from player import Player
from player_reader import PlayerReader
from player_stats import PlayerStats
from ui import UI   

def main():
    url = "https://studies.cs.helsinki.fi/nhlstats/2024-25/players"
    reader = PlayerReader(url)
    stats = PlayerStats(reader)
    ui = UI(reader)

if __name__ == "__main__":
    main()
