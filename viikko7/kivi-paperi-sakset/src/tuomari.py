
# Luokka pitää kirjaa ensimmäisen ja toisen pelaajan pisteistä sekä tasapelien määrästä.
EKA_VOITTAA = [("k", "s"), ("s", "p"), ("p", "k")]


class Tuomari:
    def __init__(self):
        self._ekan_pisteet = 0
        self._tokan_pisteet = 0
        self._tasapelit = 0
 
    def kirjaa_siirto(self, ekan_siirto, tokan_siirto):
        tulos = self._tulos(ekan_siirto, tokan_siirto)

        if tulos == "tasapeli":
            self._tasapelit = self._tasapelit + 1
        elif tulos == "eka_voittaa":
            self._ekan_pisteet = self._ekan_pisteet + 1
        else:
            self._tokan_pisteet = self._tokan_pisteet + 1

    def __str__(self):
        return f"Pelitilanne: {self._ekan_pisteet} - {self._tokan_pisteet}\nTasapelit: {self._tasapelit}"

    def _tulos(self, eka, toka):
        if eka == toka:
            return "tasapeli"
        if (eka, toka) in EKA_VOITTAA:
            return "eka_voittaa"
        return "toka_voittaa"
    
    def nollaa(self):
        self._ekan_pisteet = 0
        self._tokan_pisteet = 0
        self._tasapelit = 0