class Tekoaly:
    def __init__(self):
        self._siirto = 0

    def anna_siirto(self):
        siirrot = {0: "k", 1: "p", 2: "s"}
        self._siirto = self._siirto + 1
        self._siirto = self._siirto % 3

        return siirrot[self._siirto]

    def aseta_siirto(self, siirto):
        # ei tehdä mitään
        pass
