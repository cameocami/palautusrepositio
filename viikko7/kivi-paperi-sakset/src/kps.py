class KiviPaperiSakset:
    def __init__(self, tuomari, tekoaly=None):
        self._tuomari = tuomari
        self._tekoaly = tekoaly

    def pelaa_kierros(self, ekan_siirto, tokan_siirto=None):
        """Pelaa yhden kierroksen annetulla siirolla
        
        Args:
            ekan_siirto: Ensimmäisen pelaajan siirto
            tokan_siirto: Toisen pelaajan siirto. Jos None, haetaan _toisen_siirto() metodilla
        
        Returns:
            Kierroksen tulos tai None jos siirrot olivat virheellisiä
        """
        if tokan_siirto is None:
            tokan_siirto = self._toisen_siirto(ekan_siirto)
        
        if self._onko_ok_siirto(ekan_siirto) and self._onko_ok_siirto(tokan_siirto):
            self._tuomari.kirjaa_siirto(ekan_siirto, tokan_siirto)
            return self._tuomari.tulos(ekan_siirto, tokan_siirto)
        
        return None

    def pelaa(self):
        ekan_siirto = self._ensimmaisen_siirto()
        tokan_siirto = self._toisen_siirto(ekan_siirto)

        while self._onko_ok_siirto(ekan_siirto) and self._onko_ok_siirto(tokan_siirto):
            self._tuomari.kirjaa_siirto(ekan_siirto, tokan_siirto)
            print(self._tuomari)

            ekan_siirto = self._ensimmaisen_siirto()
            tokan_siirto = self._toisen_siirto(ekan_siirto)
        print("Kiitos!")
        print(self._tuomari)
        self._tuomari.nollaa()
        if self._tekoaly:
            self._tekoaly.nollaa()


    def _ensimmaisen_siirto(self):
        return input("Ensimmäisen pelaajan siirto: ")

    # tämän metodin toteutus vaihtelee eri pelityypeissä
    def _toisen_siirto(self, ensimmaisen_siirto):
        raise NotImplementedError("Tämä metodi pitää korvata aliluokassa")

    def _onko_ok_siirto(self, siirto):
        return siirto in ["k", "p", "s"]
    
    def tallenna_siirto(self, siirto):
        """Tallentaa siirron tekoälylle (jos olemassa)"""
        if self._tekoaly:
            self._tekoaly.aseta_siirto(siirto)
    
    def hae_vastustajan_siirto(self, ensimmaisen_siirto):
        """Hakee vastustajan siirron julkisen rajapinnan kautta"""
        return self._toisen_siirto(ensimmaisen_siirto)
