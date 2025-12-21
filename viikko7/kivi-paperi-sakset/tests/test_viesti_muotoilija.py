"""Unit tests for ViestiMuotoilija class"""

import pytest
from viesti_muotoilija import ViestiMuotoilija


class TestViestiMuotoilijaLuokkaKonstantit:
    """Tests for ViestiMuotoilija class constants"""
    
    def test_siirtojen_nimet_mapping(self):
        """Test move name mappings"""
        assert ViestiMuotoilija.SIIRTOJEN_NIMET['k'] == 'Kivi'
        assert ViestiMuotoilija.SIIRTOJEN_NIMET['p'] == 'Paperi'
        assert ViestiMuotoilija.SIIRTOJEN_NIMET['s'] == 'Sakset'


class TestMuotoileSiirronNimi:
    """Tests for format_move_name method"""
    
    def test_muotoile_siirron_nimi_kivi(self):
        """Test formatting rock/kivi"""
        assert ViestiMuotoilija.muotoile_siirron_nimi('k') == 'Kivi'
    
    def test_muotoile_siirron_nimi_paperi(self):
        """Test formatting paper/paperi"""
        assert ViestiMuotoilija.muotoile_siirron_nimi('p') == 'Paperi'
    
    def test_muotoile_siirron_nimi_sakset(self):
        """Test formatting scissors/sakset"""
        assert ViestiMuotoilija.muotoile_siirron_nimi('s') == 'Sakset'
    
    def test_muotoile_siirron_nimi_invalid(self):
        """Test formatting invalid move"""
        assert ViestiMuotoilija.muotoile_siirron_nimi('x') == 'x'


class TestMuotoileKierroksenViesti:
    """Tests for muotoile_kierroksen_viesti method"""
    
    def test_muotoile_kierroksen_viesti_pelaaja_mode_tie(self):
        """Test round message in player vs player mode with tie"""
        viesti = ViestiMuotoilija.muotoile_kierroksen_viesti(
            1, 'k', 'k', 'tasapeli', 'pelaaja'
        )
        assert 'Kierros 1' in viesti
        assert 'Pelaaja 1: Kivi' in viesti
        assert 'Pelaaja 2: Kivi' in viesti
        assert 'Tasapeli!' in viesti
    
    def test_muotoile_kierroksen_viesti_pelaaja_mode_first_wins(self):
        """Test round message in player vs player mode with first player win"""
        viesti = ViestiMuotoilija.muotoile_kierroksen_viesti(
            1, 'k', 's', 'ekan_voitto', 'pelaaja'
        )
        assert 'Kierros 1' in viesti
        assert 'Pelaaja 1: Kivi' in viesti
        assert 'Pelaaja 2: Sakset' in viesti
        assert 'Pelaaja 1 voitti!' in viesti
    
    def test_muotoile_kierroksen_viesti_pelaaja_mode_second_wins(self):
        """Test round message in player vs player mode with second player win"""
        viesti = ViestiMuotoilija.muotoile_kierroksen_viesti(
            2, 'p', 'k', 'tokan_voitto', 'pelaaja'
        )
        assert 'Kierros 2' in viesti
        assert 'Pelaaja 1: Paperi' in viesti
        assert 'Pelaaja 2: Kivi' in viesti
        assert 'Pelaaja 2 voitti!' in viesti
    
    def test_muotoile_kierroksen_viesti_tekoaly_mode_tie(self):
        """Test round message in player vs AI mode with tie"""
        viesti = ViestiMuotoilija.muotoile_kierroksen_viesti(
            1, 'p', 'p', 'tasapeli', 'tekoaly'
        )
        assert 'Kierros 1' in viesti
        assert 'Pelaaja 1: Paperi' in viesti
        assert 'Tietokone: Paperi' in viesti
        assert 'Tasapeli!' in viesti
    
    def test_muotoile_kierroksen_viesti_tekoaly_mode_player_wins(self):
        """Test round message in player vs AI mode with player win"""
        viesti = ViestiMuotoilija.muotoile_kierroksen_viesti(
            3, 's', 'p', 'ekan_voitto', 'tekoaly'
        )
        assert 'Kierros 3' in viesti
        assert 'Pelaaja 1: Sakset' in viesti
        assert 'Tietokone: Paperi' in viesti
        assert 'Pelaaja 1 voitti!' in viesti
    
    def test_muotoile_kierroksen_viesti_tekoaly_mode_ai_wins(self):
        """Test round message in player vs AI mode with AI win"""
        viesti = ViestiMuotoilija.muotoile_kierroksen_viesti(
            4, 'k', 'p', 'tokan_voitto', 'parannettu'
        )
        assert 'Kierros 4' in viesti
        assert 'Pelaaja 1: Kivi' in viesti
        assert 'Tietokone: Paperi' in viesti
        assert 'Tietokone voitti!' in viesti


class TestMuotoileVirheviesti:
    """Tests for muotoile_virheviesti method"""
    
    def test_muotoile_virheviesti_invalid_move(self):
        """Test error message for invalid move"""
        viesti = ViestiMuotoilija.muotoile_virheviesti('invalid_move')
        assert 'Virheellinen siirto!' in viesti
        assert 'k, p tai s' in viesti
    
    def test_muotoile_virheviesti_invalid_opponent_move(self):
        """Test error message for invalid opponent move"""
        viesti = ViestiMuotoilija.muotoile_virheviesti('invalid_opponent_move')
        assert 'Virheellinen siirto' in viesti
        assert 'toiselta pelaajalta' in viesti
    
    def test_muotoile_virheviesti_no_game(self):
        """Test error message for no game initialized"""
        viesti = ViestiMuotoilija.muotoile_virheviesti('no_game')
        assert 'Peliä ei ole alustettu' in viesti
    
    def test_muotoile_virheviesti_unknown_error(self):
        """Test error message for unknown error type"""
        viesti = ViestiMuotoilija.muotoile_virheviesti('unknown_error')
        assert 'Virhe tapahtui!' in viesti


class TestViestiMuotoilijaIntegration:
    """Integration tests for ViestiMuotoilija"""
    
    def test_multiple_messages_independence(self):
        """Test that multiple messages are independent"""
        msg1 = ViestiMuotoilija.muotoile_kierroksen_viesti(
            1, 'k', 's', 'ekan_voitto', 'pelaaja'
        )
        msg2 = ViestiMuotoilija.muotoile_kierroksen_viesti(
            2, 'p', 'p', 'tasapeli', 'tekoaly'
        )
        
        assert 'Kierros 1' in msg1
        assert 'Kierros 2' in msg2
        assert msg1 != msg2
