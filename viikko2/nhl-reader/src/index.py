
from player_reader import PlayerReader
from player_stats import PlayerStats
from ui import UI  

def main():
    url = "https://studies.cs.helsinki.fi/nhlstats/2024-25/players"
    reader = PlayerReader(url)
    stats = PlayerStats(reader)

    ui = UI(reader)
    
    nationality = input("Enter nationality (or leave empty for all): ").upper()
    players = stats.top_scorers_by_nationality(nationality) if nationality else stats.top_scorers_by_nationality("")
    ui.populate_table(players)
    ui.display()

if __name__ == "__main__":
    main()
