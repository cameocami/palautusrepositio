
# Luokka pitää kirjaa ensimmäisen ja toisen pelaajan pisteistä sekä tasapelien määrästä.
EKA_VOITTAA = [("k", "s"), ("s", "p"), ("p", "k")]


class Tuomari:
    def __init__(self):
        self._tasapelit = 0
        self._ekan_pisteet = 0
        self._tokan_pisteet = 0
        self._kirjaukset = [self._tasapelit, self._ekan_pisteet, self._tokan_pisteet]
 
    def kirjaa_siirto(self, ekan_siirto, tokan_siirto):
        tulos = self._tulos(ekan_siirto, tokan_siirto)
        self._kirjaukset[tulos] = self._kirjaukset[tulos] + 1

    def __str__(self):
        return f"Pelitilanne: {self._ekan_pisteet} - {self._tokan_pisteet}\nTasapelit: {self._tasapelit}"

    def _tulos(self, eka, toka):
        if eka == toka:
            return 0
        if (eka, toka) in EKA_VOITTAA:
            return 1
        return 2
    
    def nollaa(self):
        self._ekan_pisteet = 0
        self._tokan_pisteet = 0
        self._tasapelit = 0