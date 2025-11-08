
from player_reader import PlayerReader
from player_stats import PlayerStats
from ui import UI

def main():
    ui = UI()
    season = ui.prompt_season()
    url = f"https://studies.cs.helsinki.fi/nhlstats/{season}/players"
    reader = PlayerReader(url)
    stats = PlayerStats(reader)
    nationalities = reader.get_nationalities()
    nationality = ui.prompt_nationality(nationalities)
    players = stats.top_scorers_by_nationality(nationality)
    ui.populate_table(season, nationality, players)

if __name__ == "__main__":
    main()
