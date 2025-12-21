"""Unit tests for KPS game classes"""

import pytest
from kps_pelaaja_vs_pelaaja import KPSPelaajaVsPelaaja
from kps_tekoaly import KPSTekoaly
from tekoaly import Tekoaly
from tekoaly_parannettu import TekoalyParannettu
from tuomari import Tuomari


class TestKPSPelaajaVsPelaaja:
    """Tests for KPSPelaajaVsPelaaja class"""
    
    def test_kps_pvp_initialization(self, tuomari):
        """KPSPelaajaVsPelaaja should initialize correctly"""
        peli = KPSPelaajaVsPelaaja(tuomari)
        assert peli is not None
    
    def test_kps_pvp_pelaa_kierros_valid_moves(self, tuomari):
        """Playing round with valid moves should work"""
        peli = KPSPelaajaVsPelaaja(tuomari)
        tulos = peli.pelaa_kierros('k', 's')
        assert tulos == 'ekan_voitto'
    
    def test_kps_pvp_pelaa_kierros_invalid_first_move(self, tuomari):
        """Invalid first move should return None"""
        peli = KPSPelaajaVsPelaaja(tuomari)
        tulos = peli.pelaa_kierros('x', 'k')
        assert tulos is None
    
    def test_kps_pvp_pelaa_kierros_invalid_second_move(self, tuomari):
        """Invalid second move should return None"""
        peli = KPSPelaajaVsPelaaja(tuomari)
        tulos = peli.pelaa_kierros('k', 'y')
        assert tulos is None
    
    def test_kps_pvp_tallenna_siirto(self, tuomari):
        """Tallenna_siirto should not raise error"""
        peli = KPSPelaajaVsPelaaja(tuomari)
        peli.tallenna_siirto('k')  # Should not raise


class TestKPSTekoaly:
    """Tests for KPSTekoaly class"""
    
    def test_kps_tekoaly_initialization(self, tuomari, tekoaly):
        """KPSTekoaly should initialize correctly"""
        peli = KPSTekoaly(tuomari, tekoaly)
        assert peli is not None
    
    def test_kps_tekoaly_pelaa_kierros_first_move_only(self, tuomari, tekoaly):
        """Playing round with only first move should fetch AI move"""
        peli = KPSTekoaly(tuomari, tekoaly)
        tulos = peli.pelaa_kierros('k')
        assert tulos in ['tasapeli', 'ekan_voitto', 'tokan_voitto']
    
    def test_kps_tekoaly_pelaa_kierros_both_moves(self, tuomari, tekoaly):
        """Playing round with both moves should work"""
        peli = KPSTekoaly(tuomari, tekoaly)
        tulos = peli.pelaa_kierros('k', 's')
        assert tulos == 'ekan_voitto'
    
    def test_kps_tekoaly_hae_vastustajan_siirto(self, tuomari, tekoaly):
        """Should fetch valid opponent move"""
        peli = KPSTekoaly(tuomari, tekoaly)
        siirto = peli.hae_vastustajan_siirto('k')
        assert siirto in ['k', 'p', 's']
    
    def test_kps_tekoaly_tallenna_siirto(self, tuomari, tekoaly):
        """Tallenna_siirto should pass move to AI"""
        peli = KPSTekoaly(tuomari, tekoaly)
        peli.tallenna_siirto('k')
        # Should not raise error
    
    def test_kps_tekoaly_with_parannettu(self, tuomari, tekoaly_parannettu):
        """Should work with advanced AI"""
        peli = KPSTekoaly(tuomari, tekoaly_parannettu)
        
        # Play several rounds
        tulos = peli.pelaa_kierros('k')
        assert tulos in ['tasapeli', 'ekan_voitto', 'tokan_voitto']
        
        peli.tallenna_siirto('k')
        siirto = peli.hae_vastustajan_siirto('k')
        assert siirto in ['k', 'p', 's']


class TestKPSGameMechanics:
    """Tests for game mechanics"""
    
    def test_rock_beats_scissors(self, tuomari):
        """Rock should beat scissors"""
        peli = KPSPelaajaVsPelaaja(tuomari)
        tulos = peli.pelaa_kierros('k', 's')
        assert tulos == 'ekan_voitto'
    
    def test_scissors_beats_paper(self, tuomari):
        """Scissors should beat paper"""
        peli = KPSPelaajaVsPelaaja(tuomari)
        tulos = peli.pelaa_kierros('s', 'p')
        assert tulos == 'ekan_voitto'
    
    def test_paper_beats_rock(self, tuomari):
        """Paper should beat rock"""
        peli = KPSPelaajaVsPelaaja(tuomari)
        tulos = peli.pelaa_kierros('p', 'k')
        assert tulos == 'ekan_voitto'
    
    def test_tie_games(self, tuomari):
        """Same moves should tie"""
        peli = KPSPelaajaVsPelaaja(tuomari)
        
        assert peli.pelaa_kierros('k', 'k') == 'tasapeli'
        assert peli.pelaa_kierros('p', 'p') == 'tasapeli'
        assert peli.pelaa_kierros('s', 's') == 'tasapeli'
    
    def test_second_player_wins(self, tuomari):
        """Test all combinations where second player wins"""
        peli = KPSPelaajaVsPelaaja(tuomari)
        
        assert peli.pelaa_kierros('s', 'k') == 'tokan_voitto'
        assert peli.pelaa_kierros('p', 's') == 'tokan_voitto'
        assert peli.pelaa_kierros('k', 'p') == 'tokan_voitto'


class TestKPSIntegration:
    """Integration tests for KPS games"""
    
    def test_pvp_multiple_rounds(self, tuomari):
        """Test multiple rounds in PvP"""
        peli = KPSPelaajaVsPelaaja(tuomari)
        
        peli.pelaa_kierros('k', 's')
        peli.pelaa_kierros('p', 'p')
        peli.pelaa_kierros('s', 'k')
        
        kirjanpito = tuomari.hae_kirjanpito()
        assert kirjanpito['ekan_voitto'] == 1
        assert kirjanpito['tasapeli'] == 1
        assert kirjanpito['tokan_voitto'] == 1
    
    def test_ai_multiple_rounds(self, tuomari, tekoaly):
        """Test multiple rounds vs AI"""
        peli = KPSTekoaly(tuomari, tekoaly)
        
        for i in range(10):
            tulos = peli.pelaa_kierros('k')
            assert tulos in ['tasapeli', 'ekan_voitto', 'tokan_voitto']
        
        assert tuomari.hae_kierrokset() == 10
