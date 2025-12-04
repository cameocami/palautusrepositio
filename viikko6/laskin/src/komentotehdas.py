
class Summa:
    def __init__(self, sovelluslogiikka):
        self._sovelluslogiikka = sovelluslogiikka

    def suorita(self, operandi):
        self._sovelluslogiikka.plus(operandi)
        return self._sovelluslogiikka.arvo()

    def kumoa(self):
        self._sovelluslogiikka.kumoa()
        return self._sovelluslogiikka.arvo()

class Erotus:
    def __init__(self, sovelluslogiikka):
        self._sovelluslogiikka = sovelluslogiikka

    def suorita(self, operandi):
        self._sovelluslogiikka.miinus(operandi)
        return self._sovelluslogiikka.arvo()
    
    def kumoa(self):
        self._sovelluslogiikka.kumoa()
        return self._sovelluslogiikka.arvo()

class Nollaus:
    def __init__(self, sovelluslogiikka):
        self._sovelluslogiikka = sovelluslogiikka

    def suorita(self, operandi=None):
        self._sovelluslogiikka.nollaa()
        return self._sovelluslogiikka.arvo()

    def kumoa(self):
        self._sovelluslogiikka.kumoa()
        return self._sovelluslogiikka.arvo()
