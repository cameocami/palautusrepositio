"""
PeliPalvelu - Käsittelee pelin logiikan ja tilanhallinnon
Erottaa peliliiketoimintalogiikan Flask-web-kerroksesta
"""

from tuomari import Tuomari
from tekoaly import Tekoaly
from tekoaly_parannettu import TekoalyParannettu
from kps_pelaaja_vs_pelaaja import KPSPelaajaVsPelaaja
from kps_tekoaly import KPSTekoaly


class PeliTehdas:
    """Tehdas peli-instanssien luomiseen"""
    
    @staticmethod
    def luo_pelaaja_vs_pelaaja(tuomari):
        """Luo pelaaja vs pelaaja -pelin"""
        return KPSPelaajaVsPelaaja(tuomari)
    
    @staticmethod
    def luo_pelaaja_vs_tekoaly(tuomari):
        """Luo pelaaja vs tekoäly -pelin"""
        tekoaly = Tekoaly()
        return KPSTekoaly(tuomari, tekoaly)
    
    @staticmethod
    def luo_pelaaja_vs_parannettu_tekoaly(tuomari):
        """Luo pelaaja vs parannettu tekoäly -pelin"""
        tekoaly_parannettu = TekoalyParannettu(10)
        return KPSTekoaly(tuomari, tekoaly_parannettu)


class PeliPalvelu:
    """Hallinnoi pelin tilaa ja operaatioita"""
    
    def __init__(self, peli_tehdas=None, tuomari_luoja=None):
        """Alustaa palvelun
        
        Args:
            peli_tehdas: PeliTehdas-instanssi (injektoitu riippuvuus)
            tuomari_luoja: Funktio joka luo Tuomari-instanssin
        """
        self.peli = None
        self.tuomari = None
        self.pelityyppi = None
        self._peli_tehdas = peli_tehdas or PeliTehdas()
        self._tuomari_luoja = tuomari_luoja or Tuomari
        self._peli_luojat = {
            'pelaaja': self._peli_tehdas.luo_pelaaja_vs_pelaaja,
            'tekoaly': self._peli_tehdas.luo_pelaaja_vs_tekoaly,
            'parannettu': self._peli_tehdas.luo_pelaaja_vs_parannettu_tekoaly
        }
    
    def alusta_peli(self, pelityyppi):
        """Alustaa uuden pelin
        
        Args:
            pelityyppi: 'pelaaja', 'tekoaly', tai 'parannettu'
        """
        self.pelityyppi = pelityyppi
        self.tuomari = self._tuomari_luoja()
        
        luoja = self._peli_luojat.get(pelityyppi)
        if luoja:
            self.peli = luoja(self.tuomari)
    
    def pelaa_kierros(self, ekan_siirto, tokan_siirto=None):
        """Pelaa yhden kierroksen
        
        Args:
            ekan_siirto: Ensimmäisen pelaajan siirto
            tokan_siirto: Toisen pelaajan siirto (valinnainen, AI:n tapauksessa)
        
        Returns:
            tuple: (tulos, tokan_siirto) - kierroksen tulos ja toisen pelaajan siirto
        """
        # Jos toista siirtoa ei annettu, hae se AI:lta
        if tokan_siirto is None:
            tokan_siirto = self.hae_vastustajan_siirto(ekan_siirto)
        
        tulos = self.peli.pelaa_kierros(ekan_siirto, tokan_siirto)
        return tulos, tokan_siirto
    
    def tallenna_siirto_tekoalylle(self, siirto):
        """Tallentaa siirron tekoälyn muistiin"""
        if self.peli:
            self.peli.tallenna_siirto(siirto)
    
    def hae_vastustajan_siirto(self, pelaajan_siirto):
        """Hakee vastustajan siirron tekoälyltä"""
        if self.peli:
            return self.peli.hae_vastustajan_siirto(pelaajan_siirto)
        return None
    
    def hae_pisteet(self):
        """Palauttaa nykyisen pistetilanteen"""
        if self.tuomari:
            return self.tuomari.hae_kirjanpito()
        return {}
    
    def onko_peli_paattynyt(self):
        """Tarkistaa, onko peli päättynyt (joku on saanut 5 voittoa)"""
        if not self.tuomari:
            return False
        kirjanpito = self.tuomari.hae_kirjanpito()
        return kirjanpito.get('ekan_voitto', 0) >= 5 or kirjanpito.get('tokan_voitto', 0) >= 5
    
    def hae_voittaja(self):
        """Palauttaa voittajan numeron (1 tai 2), tai None jos peli ei ole ohi"""
        if not self.onko_peli_paattynyt():
            return None
        kirjanpito = self.tuomari.hae_kirjanpito()
        if kirjanpito.get('ekan_voitto', 0) >= 5:
            return 1
        if kirjanpito.get('tokan_voitto', 0) >= 5:
            return 2
        return None
    
    def hae_kierrosten_maara(self):
        """Palauttaa pelattujen kierrosten lukumäärän"""
        if self.tuomari:
            return self.tuomari.hae_kierrokset()
        return 0
    
    def nollaa(self):
        """Nollaa pelin"""
        self.peli = None
        self.tuomari = None
        self.pelityyppi = None
    
    def onko_alustettu(self):
        """Tarkistaa, onko peli alustettu"""
        return self.peli is not None and self.tuomari is not None
