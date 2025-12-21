"""Unit tests for Tuomari class"""

import pytest


class TestTuomariInit:
    """Tests for Tuomari initialization"""
    
    def test_tuomari_initializes_with_zero_scores(self, tuomari):
        """Tuomari should initialize with all scores at zero"""
        kirjanpito = tuomari.hae_kirjanpito()
        assert kirjanpito['tasapeli'] == 0
        assert kirjanpito['ekan_voitto'] == 0
        assert kirjanpito['tokan_voitto'] == 0
    
    def test_tuomari_initializes_with_zero_rounds(self, tuomari):
        """Tuomari should initialize with zero rounds"""
        assert tuomari.hae_kierrokset() == 0


class TestTuomariTulos:
    """Tests for Tuomari.tulos() method"""
    
    def test_tulos_tie_returns_tasapeli(self, tuomari):
        """Same moves should result in tasapeli (tie)"""
        assert tuomari.tulos('k', 'k') == 'tasapeli'
        assert tuomari.tulos('p', 'p') == 'tasapeli'
        assert tuomari.tulos('s', 's') == 'tasapeli'
    
    def test_tulos_first_player_wins(self, tuomari):
        """First player should win correct combinations"""
        assert tuomari.tulos('k', 's') == 'ekan_voitto'  # kivi voittaa sakset
        assert tuomari.tulos('s', 'p') == 'ekan_voitto'  # sakset voittaa paperia
        assert tuomari.tulos('p', 'k') == 'ekan_voitto'  # paperi voittaa kiveä
    
    def test_tulos_second_player_wins(self, tuomari):
        """Second player should win when first loses"""
        assert tuomari.tulos('s', 'k') == 'tokan_voitto'
        assert tuomari.tulos('p', 's') == 'tokan_voitto'
        assert tuomari.tulos('k', 'p') == 'tokan_voitto'


class TestTuomariKirjaaSiirto:
    """Tests for Tuomari.kirjaa_siirto() method"""
    
    def test_kirjaa_siirto_increments_round_count(self, tuomari):
        """Each recorded move should increment round count"""
        assert tuomari.hae_kierrokset() == 0
        tuomari.kirjaa_siirto('k', 's')
        assert tuomari.hae_kierrokset() == 1
        tuomari.kirjaa_siirto('p', 'p')
        assert tuomari.hae_kierrokset() == 2
    
    def test_kirjaa_siirto_records_tie(self, tuomari):
        """Recorded tie should update kirjanpito"""
        tuomari.kirjaa_siirto('k', 'k')
        assert tuomari.hae_kirjanpito()['tasapeli'] == 1
    
    def test_kirjaa_siirto_records_first_player_win(self, tuomari):
        """Recorded first player win should update kirjanpito"""
        tuomari.kirjaa_siirto('k', 's')
        assert tuomari.hae_kirjanpito()['ekan_voitto'] == 1
    
    def test_kirjaa_siirto_records_second_player_win(self, tuomari):
        """Recorded second player win should update kirjanpito"""
        tuomari.kirjaa_siirto('s', 'k')
        assert tuomari.hae_kirjanpito()['tokan_voitto'] == 1
    
    def test_kirjaa_siirto_multiple_rounds(self, tuomari):
        """Multiple rounds should be tracked correctly"""
        tuomari.kirjaa_siirto('k', 's')  # eka wins
        tuomari.kirjaa_siirto('p', 'p')  # tie
        tuomari.kirjaa_siirto('s', 'k')  # toka wins
        
        kirjanpito = tuomari.hae_kirjanpito()
        assert kirjanpito['ekan_voitto'] == 1
        assert kirjanpito['tasapeli'] == 1
        assert kirjanpito['tokan_voitto'] == 1
        assert tuomari.hae_kierrokset() == 3


class TestTuomariNollaa:
    """Tests for Tuomari.nollaa() method"""
    
    def test_nollaa_resets_scores(self, tuomari):
        """Nollaa should reset all scores to zero"""
        tuomari.kirjaa_siirto('k', 's')
        tuomari.kirjaa_siirto('p', 'p')
        tuomari.nollaa()
        
        kirjanpito = tuomari.hae_kirjanpito()
        assert kirjanpito['tasapeli'] == 0
        assert kirjanpito['ekan_voitto'] == 0
        assert kirjanpito['tokan_voitto'] == 0
    
    def test_nollaa_resets_round_count(self, tuomari):
        """Nollaa should reset round count"""
        tuomari.kirjaa_siirto('k', 's')
        tuomari.kirjaa_siirto('p', 'p')
        tuomari.nollaa()
        
        assert tuomari.hae_kierrokset() == 0


class TestTuomariEdgeCases:
    """Tests for edge cases and integration"""
    
    def test_multiple_games_sequence(self, tuomari):
        """Test playing multiple games in sequence"""
        # First game
        tuomari.kirjaa_siirto('k', 's')
        tuomari.kirjaa_siirto('k', 's')
        assert tuomari.hae_kierrokset() == 2
        assert tuomari.hae_kirjanpito()['ekan_voitto'] == 2
        
        # Reset for second game
        tuomari.nollaa()
        tuomari.kirjaa_siirto('p', 'p')
        assert tuomari.hae_kierrokset() == 1
        assert tuomari.hae_kirjanpito()['tasapeli'] == 1
