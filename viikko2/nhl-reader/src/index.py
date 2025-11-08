
from player_reader import PlayerReader
from player_stats import PlayerStats
from ui import UI  

def main():
    season = input("Enter season (e.g., 2024-25): ")
    url = f"https://studies.cs.helsinki.fi/nhlstats/{season}/players"
    reader = PlayerReader(url)
    stats = PlayerStats(reader)
    nationalities = set([p.nationality for p in reader.get_players()])
    print("Available nationalities:", "/".join(sorted(nationalities)))
    nationality = input("Enter nationality (or leave empty for all): ").upper()
    players = stats.top_scorers_by_nationality(nationality) if nationality else stats.top_scorers_by_nationality("")
    ui = UI(reader)
    ui.populate_table(players)
    ui.display()

if __name__ == "__main__":
    main()
