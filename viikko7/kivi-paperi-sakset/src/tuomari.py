
# Luokka pitää kirjaa ensimmäisen ja toisen pelaajan pisteistä sekä tasapelien määrästä.



class Tuomari:
    def __init__(self):
        self._kirjanpito = {"tasapeli": 0, "ekan_voitto": 0, "tokan_voitto": 0}
        self._kierrokset = 0
 
    def kirjaa_siirto(self, ekan_siirto, tokan_siirto):
        tulos = self.tulos(ekan_siirto, tokan_siirto)
        self._kirjanpito[tulos] = self._kirjanpito[tulos] + 1
        self._kierrokset += 1

    def hae_kierrokset(self):
        """Palauttaa pelattujen kierrosten määrän"""
        return self._kierrokset

    def hae_kirjanpito(self):
        """Palauttaa kirjanpidon"""
        return self._kirjanpito

    def tulos(self, eka, toka):
        if eka == toka:
            return "tasapeli"
        eka_voittaa = [("k", "s"), ("s", "p"), ("p", "k")]
        if (eka, toka) in eka_voittaa:
            return "ekan_voitto"
        return "tokan_voitto"
    
    def nollaa(self):
        self._kirjanpito["tasapeli"] = 0
        self._kirjanpito["ekan_voitto"] = 0
        self._kirjanpito["tokan_voitto"] = 0
        self._kierrokset = 0