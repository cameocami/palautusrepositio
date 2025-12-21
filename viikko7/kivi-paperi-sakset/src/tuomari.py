
# Luokka pitää kirjaa ensimmäisen ja toisen pelaajan pisteistä sekä tasapelien määrästä.
class Tuomari:
    def __init__(self):
        self.ekan_pisteet = 0
        self.tokan_pisteet = 0
        self.tasapelit = 0
        self._EKA_VOITTAA = [("k", "s"), ("s", "p"), ("p", "k")]

    def kirjaa_siirto(self, ekan_siirto, tokan_siirto):
        if self._tasapeli(ekan_siirto, tokan_siirto):
            self.tasapelit = self.tasapelit + 1
        elif self._eka_voittaa(ekan_siirto, tokan_siirto):
            self.ekan_pisteet = self.ekan_pisteet + 1
        else:
            self.tokan_pisteet = self.tokan_pisteet + 1

    def __str__(self):
        return f"Pelitilanne: {self.ekan_pisteet} - {self.tokan_pisteet}\nTasapelit: {self.tasapelit}"

    # sisäinen metodi joka tarkastaa voittaako eka pelaaja tokan
    def _tasapeli(self, eka, toka):
        return eka == toka
    def _eka_voittaa(self, eka, toka):
        return (eka, toka) in self._EKA_VOITTAA
    
    def nollaa(self):
        self.ekan_pisteet = 0
        self.tokan_pisteet = 0
        self.tasapelit = 0
