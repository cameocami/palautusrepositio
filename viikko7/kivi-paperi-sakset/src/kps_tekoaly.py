
from kps import KiviPaperiSakset

class KPSTekoaly(KiviPaperiSakset):
    def __init__(self, tuomari, tekoaly):
        super().__init__(tuomari, tekoaly)

    def _toisen_siirto(self, ensimmaisen_siirto):
        tokan_siirto = self._tekoaly.anna_siirto()
        print(f"Tietokone valitsi: {tokan_siirto}")
        self._tekoaly.aseta_siirto(ensimmaisen_siirto)
        return tokan_siirto

