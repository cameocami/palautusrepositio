"""Unit tests for PeliPalvelu and PeliTehdas classes"""

import pytest
from peli_palvelu import PeliPalvelu, PeliTehdas
from kps_pelaaja_vs_pelaaja import KPSPelaajaVsPelaaja
from kps_tekoaly import KPSTekoaly
from tuomari import Tuomari


class TestPeliTehdas:
    """Tests for PeliTehdas factory class"""
    
    def test_luo_pelaaja_vs_pelaaja(self):
        """Test creating player vs player game"""
        tuomari = Tuomari()
        peli = PeliTehdas.luo_pelaaja_vs_pelaaja(tuomari)
        assert isinstance(peli, KPSPelaajaVsPelaaja)
    
    def test_luo_pelaaja_vs_tekoaly(self):
        """Test creating player vs AI game"""
        tuomari = Tuomari()
        peli = PeliTehdas.luo_pelaaja_vs_tekoaly(tuomari)
        assert isinstance(peli, KPSTekoaly)
    
    def test_luo_pelaaja_vs_parannettu_tekoaly(self):
        """Test creating player vs advanced AI game"""
        tuomari = Tuomari()
        peli = PeliTehdas.luo_pelaaja_vs_parannettu_tekoaly(tuomari)
        assert isinstance(peli, KPSTekoaly)


class TestPeliPalveluInit:
    """Tests for PeliPalvelu initialization"""
    
    def test_peli_palvelu_initializes_without_game(self, peli_palvelu):
        """PeliPalvelu should initialize without a game"""
        assert peli_palvelu.peli is None
        assert peli_palvelu.tuomari is None
        assert peli_palvelu.pelityyppi is None
    
    def test_peli_palvelu_with_custom_factory(self):
        """PeliPalvelu should accept custom factory"""
        custom_factory = PeliTehdas()
        palvelu = PeliPalvelu(custom_factory)
        assert palvelu._peli_tehdas == custom_factory
    
    def test_peli_palvelu_with_custom_judge(self):
        """PeliPalvelu should accept custom judge creator"""
        def custom_judge():
            return Tuomari()
        
        palvelu = PeliPalvelu(tuomari_luoja=custom_judge)
        assert palvelu._tuomari_luoja == custom_judge


class TestAlustaPeli:
    """Tests for alusta_peli method"""
    
    def test_alusta_peli_pelaaja_creates_game(self, peli_palvelu):
        """Alusta_peli should create player vs player game"""
        peli_palvelu.alusta_peli('pelaaja')
        assert peli_palvelu.peli is not None
        assert peli_palvelu.tuomari is not None
        assert peli_palvelu.pelityyppi == 'pelaaja'
    
    def test_alusta_peli_tekoaly_creates_game(self, peli_palvelu):
        """Alusta_peli should create player vs AI game"""
        peli_palvelu.alusta_peli('tekoaly')
        assert peli_palvelu.peli is not None
        assert peli_palvelu.tuomari is not None
        assert peli_palvelu.pelityyppi == 'tekoaly'
    
    def test_alusta_peli_parannettu_creates_game(self, peli_palvelu):
        """Alusta_peli should create player vs advanced AI game"""
        peli_palvelu.alusta_peli('parannettu')
        assert peli_palvelu.peli is not None
        assert peli_palvelu.tuomari is not None
        assert peli_palvelu.pelityyppi == 'parannettu'
    
    def test_alusta_peli_invalid_type(self, peli_palvelu):
        """Alusta_peli should handle invalid game type gracefully"""
        peli_palvelu.alusta_peli('invalid_type')
        assert peli_palvelu.peli is None
    
    def test_alusta_peli_creates_new_judge(self, peli_palvelu):
        """Each game should get a fresh judge"""
        peli_palvelu.alusta_peli('pelaaja')
        judge1 = peli_palvelu.tuomari
        
        peli_palvelu.alusta_peli('tekoaly')
        judge2 = peli_palvelu.tuomari
        
        assert judge1 is not judge2


class TestPelaaSiirtos:
    """Tests for pelaa_kierros method"""
    
    def test_pelaa_kierros_pelaaja_both_moves(self, peli_palvelu):
        """Test playing round in player vs player with both moves"""
        peli_palvelu.alusta_peli('pelaaja')
        tulos, tokan_siirto = peli_palvelu.pelaa_kierros('k', 's')
        
        assert tulos == 'ekan_voitto'
        assert tokan_siirto == 's'
    
    def test_pelaa_kierros_tekoaly_only_first_move(self, peli_palvelu):
        """Test playing round with AI using only first move"""
        peli_palvelu.alusta_peli('tekoaly')
        tulos, tokan_siirto = peli_palvelu.pelaa_kierros('k')
        
        assert tulos in ['tasapeli', 'ekan_voitto', 'tokan_voitto']
        assert tokan_siirto in ['k', 'p', 's']
    
    def test_pelaa_kierros_updates_round_count(self, peli_palvelu):
        """Playing rounds should update round count"""
        peli_palvelu.alusta_peli('pelaaja')
        assert peli_palvelu.hae_kierrosten_maara() == 0
        
        peli_palvelu.pelaa_kierros('k', 's')
        assert peli_palvelu.hae_kierrosten_maara() == 1
        
        peli_palvelu.pelaa_kierros('p', 'p')
        assert peli_palvelu.hae_kierrosten_maara() == 2


class TestTallennaSiirtoTekoalylle:
    """Tests for tallenna_siirto_tekoalylle method"""
    
    def test_tallenna_siirto_tekoalylle_with_ai_game(self, peli_palvelu):
        """Should save move to AI when playing against AI"""
        peli_palvelu.alusta_peli('tekoaly')
        peli_palvelu.tallenna_siirto_tekoalylle('k')
        # Should not raise error
    
    def test_tallenna_siirto_tekoalylle_with_pvp_game(self, peli_palvelu):
        """Should not save move in player vs player"""
        peli_palvelu.alusta_peli('pelaaja')
        peli_palvelu.tallenna_siirto_tekoalylle('k')
        # Should not raise error
    
    def test_tallenna_siirto_tekoalylle_without_game(self, peli_palvelu):
        """Should handle being called without initialized game"""
        peli_palvelu.tallenna_siirto_tekoalylle('k')
        # Should not raise error


class TestHaeVastustajanSiirto:
    """Tests for hae_vastustajan_siirto method"""
    
    def test_hae_vastustajan_siirto_returns_valid_move(self, peli_palvelu):
        """Should return valid move from opponent"""
        peli_palvelu.alusta_peli('tekoaly')
        siirto = peli_palvelu.hae_vastustajan_siirto('k')
        assert siirto in ['k', 'p', 's']
    
    def test_hae_vastustajan_siirto_without_game(self, peli_palvelu):
        """Should return None if no game initialized"""
        siirto = peli_palvelu.hae_vastustajan_siirto('k')
        assert siirto is None


class TestHaePisteet:
    """Tests for hae_pisteet method"""
    
    def test_hae_pisteet_empty_game(self, peli_palvelu):
        """Should return empty dict if no game"""
        pisteet = peli_palvelu.hae_pisteet()
        assert pisteet == {}
    
    def test_hae_pisteet_returns_kirjanpito(self, peli_palvelu):
        """Should return judge's kirjanpito"""
        peli_palvelu.alusta_peli('pelaaja')
        peli_palvelu.pelaa_kierros('k', 's')
        
        pisteet = peli_palvelu.hae_pisteet()
        assert 'tasapeli' in pisteet
        assert 'ekan_voitto' in pisteet
        assert 'tokan_voitto' in pisteet
        assert pisteet['ekan_voitto'] == 1


class TestHaeKierrostenMaara:
    """Tests for hae_kierrosten_maara method"""
    
    def test_hae_kierrosten_maara_empty_game(self, peli_palvelu):
        """Should return 0 if no game"""
        maara = peli_palvelu.hae_kierrosten_maara()
        assert maara == 0
    
    def test_hae_kierrosten_maara_after_rounds(self, peli_palvelu):
        """Should return correct round count"""
        peli_palvelu.alusta_peli('pelaaja')
        peli_palvelu.pelaa_kierros('k', 's')
        peli_palvelu.pelaa_kierros('p', 'p')
        
        assert peli_palvelu.hae_kierrosten_maara() == 2


class TestNollaa:
    """Tests for nollaa method"""
    
    def test_nollaa_clears_game(self, peli_palvelu):
        """Nollaa should clear game state"""
        peli_palvelu.alusta_peli('pelaaja')
        peli_palvelu.nollaa()
        
        assert peli_palvelu.peli is None
        assert peli_palvelu.tuomari is None
        assert peli_palvelu.pelityyppi is None


class TestOnkoPeliPaattynyt:
    """Tests for onko_peli_paattynyt method"""
    
    def test_onko_peli_paattynyt_false_without_game(self, peli_palvelu):
        """Should return False if no game initialized"""
        assert peli_palvelu.onko_peli_paattynyt() is False
    
    def test_onko_peli_paattynyt_false_with_few_wins(self, peli_palvelu):
        """Should return False when no one has 5 wins"""
        peli_palvelu.alusta_peli('pelaaja')
        for i in range(4):
            peli_palvelu.pelaa_kierros('k', 's')  # eka wins
        
        assert peli_palvelu.onko_peli_paattynyt() is False
    
    def test_onko_peli_paattynyt_true_eka_wins(self, peli_palvelu):
        """Should return True when first player gets 5 wins"""
        peli_palvelu.alusta_peli('pelaaja')
        for i in range(5):
            peli_palvelu.pelaa_kierros('k', 's')  # eka wins
        
        assert peli_palvelu.onko_peli_paattynyt() is True
    
    def test_onko_peli_paattynyt_true_toka_wins(self, peli_palvelu):
        """Should return True when second player gets 5 wins"""
        peli_palvelu.alusta_peli('pelaaja')
        for i in range(5):
            peli_palvelu.pelaa_kierros('s', 'k')  # toka wins
        
        assert peli_palvelu.onko_peli_paattynyt() is True


class TestHaeVoittaja:
    """Tests for hae_voittaja method"""
    
    def test_hae_voittaja_returns_none_when_not_over(self, peli_palvelu):
        """Should return None if game not over"""
        peli_palvelu.alusta_peli('pelaaja')
        for i in range(3):
            peli_palvelu.pelaa_kierros('k', 's')
        
        assert peli_palvelu.hae_voittaja() is None
    
    def test_hae_voittaja_returns_1_when_eka_wins(self, peli_palvelu):
        """Should return 1 when first player wins"""
        peli_palvelu.alusta_peli('pelaaja')
        for i in range(5):
            peli_palvelu.pelaa_kierros('k', 's')
        
        assert peli_palvelu.hae_voittaja() == 1
    
    def test_hae_voittaja_returns_2_when_toka_wins(self, peli_palvelu):
        """Should return 2 when second player wins"""
        peli_palvelu.alusta_peli('pelaaja')
        for i in range(5):
            peli_palvelu.pelaa_kierros('s', 'k')
        
        assert peli_palvelu.hae_voittaja() == 2
    
    def test_hae_voittaja_without_game(self, peli_palvelu):
        """Should return None if no game initialized"""
        assert peli_palvelu.hae_voittaja() is None
    
    def test_hae_voittaja_with_more_than_5_wins(self, peli_palvelu):
        """Should return correct winner even with more than 5 wins"""
        peli_palvelu.alusta_peli('pelaaja')
        for i in range(7):
            peli_palvelu.pelaa_kierros('k', 's')
        
        # Game should have stopped at 5, but test that winner is correct
        assert peli_palvelu.hae_voittaja() == 1


class TestOnkoAlustettu:
    """Tests for onko_alustettu method"""
    
    def test_onko_alustettu_false_initially(self, peli_palvelu):
        """Should return False if game not initialized"""
        assert peli_palvelu.onko_alustettu() is False
    
    def test_onko_alustettu_true_after_init(self, peli_palvelu):
        """Should return True after initializing game"""
        peli_palvelu.alusta_peli('pelaaja')
        assert peli_palvelu.onko_alustettu() is True
    
    def test_onko_alustettu_false_after_nollaa(self, peli_palvelu):
        """Should return False after clearing game"""
        peli_palvelu.alusta_peli('pelaaja')
        peli_palvelu.nollaa()
        assert peli_palvelu.onko_alustettu() is False


class TestPeliPalveluIntegration:
    """Integration tests for PeliPalvelu"""
    
    def test_full_game_pvp(self, peli_palvelu):
        """Test complete player vs player game flow"""
        peli_palvelu.alusta_peli('pelaaja')
        assert peli_palvelu.onko_alustettu()
        
        peli_palvelu.pelaa_kierros('k', 's')  # eka wins
        peli_palvelu.pelaa_kierros('p', 'p')  # tie
        peli_palvelu.pelaa_kierros('s', 'k')  # toka wins
        
        pisteet = peli_palvelu.hae_pisteet()
        assert pisteet['ekan_voitto'] == 1
        assert pisteet['tasapeli'] == 1
        assert pisteet['tokan_voitto'] == 1
        assert peli_palvelu.hae_kierrosten_maara() == 3
    
    def test_full_game_ai(self, peli_palvelu):
        """Test complete player vs AI game flow"""
        peli_palvelu.alusta_peli('tekoaly')
        assert peli_palvelu.onko_alustettu()
        
        for _ in range(5):
            tulos, tokan_siirto = peli_palvelu.pelaa_kierros('k')
            assert tulos in ['tasapeli', 'ekan_voitto', 'tokan_voitto']
            assert tokan_siirto in ['k', 'p', 's']
        
        assert peli_palvelu.hae_kierrosten_maara() == 5
    
    def test_game_reset_sequence(self, peli_palvelu):
        """Test playing multiple games in sequence"""
        # First game
        peli_palvelu.alusta_peli('pelaaja')
        peli_palvelu.pelaa_kierros('k', 's')
        assert peli_palvelu.hae_kierrosten_maara() == 1
        
        # Reset
        peli_palvelu.nollaa()
        assert peli_palvelu.onko_alustettu() is False
        
        # Second game
        peli_palvelu.alusta_peli('tekoaly')
        peli_palvelu.pelaa_kierros('p')
        assert peli_palvelu.hae_kierrosten_maara() == 1
