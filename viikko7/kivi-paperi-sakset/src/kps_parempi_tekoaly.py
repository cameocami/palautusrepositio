
from kps import KiviPaperiSakset

class KPSParempiTekoaly(KiviPaperiSakset):
    def __init__(self, tekoaly):
        self._tekoaly = tekoaly

    def _toisen_siirto(self, ensimmaisen_siirto):
        tokan_siirto = self._tekoaly.anna_siirto()
        print(f"Tietokone valitsi: {tokan_siirto}")
        self._tekoaly.aseta_siirto(ensimmaisen_siirto)
        return tokan_siirto
