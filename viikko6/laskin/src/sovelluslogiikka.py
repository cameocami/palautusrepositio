class Sovelluslogiikka:
    def __init__(self, arvo=0):
        self._arvo = arvo
        self.edellinen_arvo = []

    def miinus(self, operandi):
        self.edellinen_arvo.append(self._arvo)
        self._arvo = self._arvo - operandi

    def plus(self, operandi):
        self.edellinen_arvo.append(self._arvo)
        self._arvo = self._arvo + operandi

    def nollaa(self):
        self.edellinen_arvo.append(self._arvo)
        self._arvo = 0

    def aseta_arvo(self, arvo):
        self.edellinen_arvo.append(self._arvo)
        self._arvo = arvo

    def arvo(self):
        return self._arvo

    def kumoa(self):
        if self.edellinen_arvo:
            self._arvo = self.edellinen_arvo.pop()
        else:
            self._arvo = 0

    @property
    def kaikki_kumottu(self):
        return len(self.edellinen_arvo) == 0
        