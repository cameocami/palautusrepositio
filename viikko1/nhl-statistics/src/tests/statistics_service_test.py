import unittest
from statistics_service import StatisticsService
from player import Player

class PlayerReaderStub:
    def get_players(self):
        return [
            Player("Semenko", "EDM", 4, 12),  #  4+12 = 16
            Player("Lemieux", "PIT", 45, 54), # 45+54 = 99
            Player("Kurri",   "EDM", 37, 53), # 37+53 = 90
            Player("Yzerman", "DET", 42, 56), # 42+56 = 98
            Player("Gretzky", "EDM", 35, 89)  # 35+89 = 124
        ]

class TestStatisticsService(unittest.TestCase):
    def setUp(self):
        # annetaan StatisticsService-luokan oliolle "stub"-luokan olio
        self.stats = StatisticsService(
            PlayerReaderStub()
        )
    def test_initiation_creates_player_list(self):
        self.assertEqual(len(self.stats._players), 5)

    def test_search_existing_player(self):
        existing_player = self.stats.search("Kurri")
        self.assertEqual(existing_player.name, "Kurri")

    def test_search_non_existing_player(self):
        non_existing_player = self.stats.search("Granlund")
        self.assertIsNone(non_existing_player)

    def test_search_partial_name(self):
        partial_player = self.stats.search("Yzer")
        self.assertEqual(partial_player.name, "Yzerman")

    def test_team_returns_correct_players(self):
        edm_players = self.stats.team("EDM")
        self.assertEqual(len(edm_players), 3)
        self.assertIn("Semenko", [player.name for player in edm_players])
        self.assertIn("Kurri", [player.name for player in edm_players])
        self.assertIn("Gretzky", [player.name for player in edm_players])

    def test_team_returns_empty_list_for_no_players(self):
        no_players = self.stats.team("NYR")
        self.assertEqual(len(no_players), 0)

    def test_top_returns_correct_number_of_players(self):
        top_players = self.stats.top(3)
        self.assertEqual(len(top_players), 4)

    def test_top_returns_players_in_correct_order(self):
        top_players = self.stats.top(3)
        expected_order = ["Gretzky", "Lemieux", "Yzerman", "Kurri"]
        actual_order = [player.name for player in top_players]
        self.assertEqual(actual_order, expected_order)

    def test_top_with_zero(self):
        top_players = self.stats.top(0)
        self.assertEqual(len(top_players), 1)
    
    def test_top_with_negative_number(self):
        top_players = self.stats.top(-3)
        self.assertEqual(len(top_players), 0)  # should return empty list
